#!/usr/bin/env python3
"""
splice.py — deterministically apply a batch of ready-to-splice change blocks to a Markdown
PRD. Generic version of the Agent Atelier splicer (P5 assembly).

A block is JSON:
  {
    "cluster": "onboarding",                       # label, for reporting
    "mode": "insert-after" | "replace" | "new-section-before",
    "targetSection": "§7.1",                        # label, for reporting
    "anchorHint": "unique existing phrase",         # the insertion / locate point
    "replaceOld": "exact existing text",            # required for mode=replace
    "finalMarkdown": "the block to insert/replace, in PRD voice"
  }

The BLOCKS file is a JSON array of such blocks (or {"blocks":[...]}; both accepted). The
per-cluster assembler shape [{"cluster":..., "blocks":[...]}, ...] is ALSO accepted and
auto-flattened (the cluster label is hoisted onto each inner block).

Discipline (why this beats hand-editing dozens of insertions):
  * html.unescape every field — agents emit &amp; / &lt; / &gt;.
  * DRY-RUN first: assert every anchor / replaceOld matches EXACTLY ONCE. Fix MISS/DUP first.
  * APPLY from a PRISTINE copy of the last-good baseline (a cp snapshot, not necessarily
    git-committed) so re-runs are idempotent.
  * NOTE: dry-run counts against the UN-mutated doc; apply re-counts against the buffer as it
    mutates, so a block whose finalMarkdown repeats a LATER block's anchor can flip that later
    block to a DUP and FAIL it (reported honestly, not silent). Keep anchors specific/distinct.

Usage:
    # 1. dry-run against the live target (shows match counts; fix any MISS/DUP)
    python3 splice.py dry   --blocks blocks.json --target PRD.md

    # 2. apply from a pristine baseline copy (idempotent)
    cp PRD.md PRD.pristine.md   # once, from the last-good baseline (a cp, not a git commit)
    python3 splice.py apply --blocks blocks.json --target PRD.md --pristine PRD.pristine.md
"""
import argparse
import html
import json
import os
import sys


def U(s):
    """Undo HTML-entity escaping that leaks into agent output."""
    return html.unescape(s) if s else s


def key(b):
    """The text that must match exactly once: replaceOld for replace, else anchorHint.
       .get() so a mode='replace' block that omits replaceOld degrades to an EMPTY-KEY report,
       not a KeyError that aborts the whole batch."""
    return U(b.get("replaceOld", "")) if b.get("mode") == "replace" else U(b.get("anchorHint", ""))


def load_blocks(path):
    """Return a FLAT list of block objects, accepting either shape:
       - a flat array of blocks, or
       - the per-cluster assembler shape [{cluster, blocks:[...]}, ...] (auto-flattened here,
         hoisting each wrapper's `cluster` label onto its inner blocks for the report)."""
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict) and "blocks" in data:
        data = data["blocks"]
    flat = []
    for el in data:
        if isinstance(el, dict) and isinstance(el.get("blocks"), list):
            for inner in el["blocks"]:
                if isinstance(inner, dict) and "cluster" not in inner and "cluster" in el:
                    inner = {**inner, "cluster": el["cluster"]}
                flat.append(inner)
        else:
            flat.append(el)
    return flat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["dry", "apply"])
    ap.add_argument("--blocks", required=True)
    ap.add_argument("--target", required=True, help="the PRD .md to read (dry) / write (apply)")
    ap.add_argument("--pristine", help="apply-mode: pristine baseline copy to build from (idempotent)")
    args = ap.parse_args()

    blocks = load_blocks(args.blocks)

    # dry reads the live target; apply builds from the pristine baseline if given.
    if args.mode == "apply" and args.pristine and not os.path.exists(args.pristine):
        sys.exit(f"pristine baseline not found: {args.pristine} "
                 f"(fix the path — NOT falling back to the mutated target, which would break idempotency)")
    read_from = args.pristine if (args.mode == "apply" and args.pristine) else args.target
    text = open(read_from, encoding="utf-8").read()

    if args.mode == "dry":
        bad = []
        for i, b in enumerate(blocks):
            k = key(b)
            n = text.count(k) if k else -1
            flag = "" if n == 1 else "  <<< " + (
                "EMPTY-KEY (missing anchorHint / wrong block shape)" if not k
                else ("MISS" if n == 0 else "DUP"))
            if n != 1:
                bad.append((i, b, n))
            snippet = k.replace(chr(10), " ")[:46]
            print(f"[{i:>3}] {b.get('cluster','')[:20]:<20} {b.get('mode','')[:16]:<16} cnt={n}{flag}  ⟪{snippet}⟫")
        print(f"\nTOTAL {len(blocks)} | clean(cnt==1): {len(blocks)-len(bad)} | needs-attention: {len(bad)}")
        for i, b, n in bad:
            print(f"   [{i}] {b.get('cluster','')} {b.get('mode')} target={b.get('targetSection')} cnt={n}")
        sys.exit(0 if not bad else 2)

    # ---- apply ----
    applied, failed = [], []
    for i, b in enumerate(blocks):
        k = key(b)
        fm = U(b.get("finalMarkdown", ""))
        if not k or text.count(k) != 1:
            failed.append((i, b, text.count(k) if k else -1))
            continue
        mode = b["mode"]
        try:                                            # one bad block never aborts the batch
            if mode == "replace":
                text = text.replace(k, fm, 1)
            elif mode == "insert-after":
                idx = text.index(k)
                nl = text.find("\n", idx + len(k))      # end of anchor's line (search from anchor END,
                le = nl if nl != -1 else len(text)      #  so a multi-line anchor isn't split; -1 = last line)
                text = text[:le] + "\n\n" + fm + text[le:]
            elif mode == "new-section-before":
                idx = text.index(k)
                ls = text.rfind("\n", 0, idx) + 1       # start of anchor's line (rfind=-1 -> 0 = file start)
                text = text[:ls] + fm + "\n\n" + text[ls:]
            else:
                failed.append((i, b, -99))
                continue
        except Exception as e:
            failed.append((i, b, f"err:{e}"))
            continue
        applied.append(i)

    open(args.target, "w", encoding="utf-8").write(text)
    print(f"APPLIED {len(applied)}/{len(blocks)}  |  FAILED {len(failed)}")
    for i, b, n in failed:
        kk = key(b)
        snippet = kk.replace(chr(10), " ")[:60]
        why = " EMPTY-KEY (missing anchorHint / wrong block shape)" if not kk else ""
        print(f"  FAIL [{i}] {b.get('cluster','')} {b.get('mode')} target={b.get('targetSection')} cnt={n}{why}  ⟪{snippet}⟫")
    sys.exit(0 if not failed else 2)


if __name__ == "__main__":
    main()

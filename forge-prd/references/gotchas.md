# Hard-won gotchas — the rules that prevent the expensive mistakes

Read these once at the start of any forge-prd run. Each was paid for in a real build. They
are the difference between a spec that *looks* foolproof and one that *is*.

## 1. Same-cutoff review panels share blind spots

A fleet of agents built on the same model share the same training cutoff and the same
confident-but-stale beliefs — especially about model names/IDs, API limits, and library
versions. In the Agent Atelier build, an early pass mislabeled the image model; only a
*targeted currency hunt* caught it. **Always scope at least one review lens to CURRENCY &
COMPLETENESS,** and treat every model ID / external limit as "confirm against live docs at
build time" (the BUNNY grounding discipline). A red-team of clones will happily agree on a
wrong fact.

## 2. Durable over ephemeral

Externalize knowledge into files — the spec, working briefs, memory — never leave it in the
conversation. Conversation context is lost to compaction; disk is not. **This very skill is
that principle applied** (it was authored from a durable brief written *before* a compaction,
precisely so nothing was lost). At every phase, write the output to disk (and `git commit`
only when the user asks — see the P5 note below and methodology.md).

## 3. Product-agnostic discipline — grep before you ship

Zero example-domain leakage into the *generic mechanism*. Two different things get confused
here, so be precise:

- **Expected — NOT a leak:** naming the *source system* in §1 (thesis) and §2 (Background &
  motivation) when you are generalizing an existing product. That is provenance — the skeleton
  §2 *requires* it, and the exemplar itself names its source system in §1/§2 (and in an
  illustrative UI mockup). Do not scrub these.
- **The actual leak:** a domain-specific **config VALUE** — a specific offering, a
  forbidden-claim string, a brand-voice phrase, a persona's real name — appearing in the
  generic body (§0, §3–§20) as if it were part of the generic spec. Those belong ONLY in
  Appendix A and the `config/` files.

So the grep yields **candidates, not automatic failures** — eyeball each hit:

```bash
# EDIT THIS FIRST — put YOUR example's name + distinctive nouns here. The defaults are
# deliberate fail-loud placeholders so a verbatim copy-paste cannot silently pass.
NEEDLES='REPLACE_WITH_YOUR_EXAMPLE_NAME|REPLACE_WITH_YOUR_DISTINCTIVE_NOUN'
case "$NEEDLES" in *REPLACE_WITH_*) echo "✗ edit NEEDLES first — a placeholder is still there"; exit 1;; esac
# grep the generic body (Appendix A onward is excluded). Run ONLY on PRD.md — the config/
# files are separate and are the sanctioned home of concrete values, so don't grep them.
awk '/^## +(Appendix A|A\. )/{skip=1} skip==0' PRD.md | grep -inE "$NEEDLES"
# (for the exemplar itself the needles would be:  art of living|sudarshan )
```

A hit in §1/§2 (the source-system name) is fine — as is the example name shown inside an
illustrative UI mockup (e.g. a §12 screen). A **config value** — a specific offering, a
forbidden-claim string, a voice phrase — in §0 or §3–§20 is the leak to fix. A spec with a
config value baked into §7's generic mechanism is not product-agnostic no matter what §7
claims.

## 4. Safety is non-negotiable and fails closed

- Safety-critical config fields (forbidden claims, non-disclosure rules, required framing)
  **block when empty or unconfirmed** — never proceed on an empty safety field.
- **Secrets resolve only into the tool/MCP auth layer, never into model-visible prompts.**
- **Non-disclosure binds words AND images** — a rule that forbids revealing X must cover an
  image that reveals X, not just text.
- **No deepfakes of real people / leaders.**
- **Human edits re-run the deterministic gates** — a human editing an approved item does not
  bypass the safety/lint checks; the gates re-run on the edited version.

## 5. Splicing hygiene (P5)

- `html.unescape` agent output before matching/inserting — agents emit `&amp;`, `&lt;`, `&gt;`.
- **Anchor-must-match-exactly-once** dry-run before any mutation; a MISS means the anchor text
  drifted, a DUP means it is not unique (lengthen it).
- **Inject the canonical entity set** so clusters reference shared entities instead of
  redefining them.
- Keep a **numbered consistency-rules** doc and pass it to *every* assembler AND *every*
  verifier — same rules, both sides.
- **Apply from a pristine copy of the last-good baseline** (a `cp` snapshot, not a git commit)
  so re-runs are idempotent.

## 6. Rate-limit resilience

Big fan-outs lose agents to API-overload and session limits. Keep per-wave counts moderate,
`.filter(Boolean)` the results, and **re-run only the failed slices** (low concurrency). Do
NOT "compensate" for a dead verifier with a hand-waved manual check and call the slice done —
that is exactly the compromise P6 forbids. Re-run the real agent.

## 7. Markdown hygiene in generated specs

- **Balanced code fences.** A mis-paired ```gherkin block silently renders every following
  section as one code block until the next fence — and it can swallow safety-critical prose.
  After any splice, check fence parity (even count of ``` ). This was a real *blocker* in the
  Agent Atelier build.
- `####` for x.y.z depth (don't skip heading levels).
- No orphan merge fragments (a half-spliced sentence, a dangling list item).
- **Every inline §-ref must resolve** to a real section. Broken cross-refs are the most
  common seam defect.

## 8. Loop the red-team until two consecutive clean passes

One clean pass is not enough — **the second pass catches defects the first pass's fixes
introduced.** A fix that renumbers a section breaks the cross-refs that pointed at it; a fix
that adds an enum value needs a writer; a fix that inserts a block can unbalance a fence. Only
stop when a full verifier round comes back clean *after* the previous round's fixes were
applied.

## 9. Scale rigor to the stakes (the inverse gotcha)

The full P4–P6 fleet is right for a product the user intends to ship, be judged on, or calls
"foolproof / comprehensive." It is *overkill* for a throwaway internal tool. Do not fan out 10
auditors and loop a red-team for a one-page utility spec — that is its own failure of
judgment. Ask, or infer from the user's language, and match the process weight to the stakes.

## 10. The intake is a conversation, not a form

The origin motivation of this whole method (Agent Atelier's "dead form" pain): a spec — or a
product — that swallows input and returns opacity is a failure. In P0, intake the idea
conversationally, one focus at a time; and in the *product* you spec, make the config intake a
guided interview, not a wall of fields. Opacity after input is the anti-pattern to design out
at both levels.

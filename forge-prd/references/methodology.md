# forge-prd — the P0–P7 methodology in full

This is the L3 detail behind the SKILL.md workflow spine. It is how the gold-standard
Agent Atelier PRD was actually built. Each phase lists its purpose, concrete sub-steps, and
the exit condition that lets you move on.

---

## P0 — Intake the idea

**Purpose.** Agree on *what* we are speccing and *how far* before writing anything.

**Do it conversationally, one focus at a time** (this is a brainstorming-style phase — do
not interrogate with a wall of questions). Elicit:

- **What the thing is** — the product in one or two sentences.
- **The real-world source system**, if you are generalizing/reverse-engineering one (was
  the case for Agent Atelier → the Paperclip/Art-of-Living engine). If there is one, you
  will study it in P1.
- **The target build platform / stack** — where will this actually be built? (Agent Atelier
  targeted Google Antigravity + Gemini 3 + ADK.) This shapes the architecture section and
  the build governance, but **defer exact model IDs / library versions to build time** —
  the spec says "an image model meeting these requirements", not a pinned version.
- **Who the user is** — their role, expertise, what winning looks like (Agent Atelier was a
  course capstone the user intended to *win*; that raised the bar to "foolproof").
- **The product-agnostic goal** — articulate it as "*the [engine] is constant; the [domain
  thing] is configuration*." For Agent Atelier: "the studio is constant; the brand is
  configuration." This single sentence governs every later decision about what is spec vs
  config.
- **Hard constraints and non-goals** — safety rules, things it must never do, scope you are
  deliberately excluding (YAGNI).
- **Is it agentic / AI?** — decides how much of the whitepaper concept-map applies (P1; see
  `references/whitepaper-map.md`). A non-agentic product uses the *method* (SDD + BUNNY +
  review pipeline) but only the relevant subset of the concept-map.

**Confirm the product NAME early.** It anchors the whole document, the file names, and the
config namespace. Do not proceed with a placeholder if you can settle it.

**Scope check / decomposition.** If the idea spans several independent subsystems (chat +
billing + analytics + …), flag it immediately and help the user decompose into sub-products
that each get their own spec → plan → build cycle. Forge the first sub-PRD; do not try to
spec a platform as one document.

**Exit condition.** You and the user agree, in writing, on: the name, the one-line thesis,
the product-agnostic framing, the target stack, the constraints/non-goals, and whether it
is agentic. Do NOT start drafting or fan out agents before this.

---

## P1 — Understand & ground

**Purpose.** Load the real knowledge the spec must encode — from the source system and from
the frameworks — so the draft is grounded, not invented.

**If generalizing an existing system:** reverse-engineer it properly. Read its code, docs,
and UI. On Agent Atelier, Paperclip was installed locally and its UI source (a React SPA +
WebSocket event stream + recovery cards) was read directly to ground the "Studio Floor"
observability UI in something real rather than imagined. The lesson: **ground the UI/UX in
an actual working reference**, not a mockup, wherever one exists.

**Read the framework sources.** For agentic products, **read the actual whitepaper for each
relevant day** — do not rely on model memory; concept fidelity matters and memory drifts.
Paths and the concept map are in `references/whitepaper-map.md`. For non-agentic products,
read whatever domain framework/standard applies (a payments spec reads the card-network
rules; an accessibility-heavy product reads WCAG; etc.).

**Produce a structured map** — a working note (durable, on disk) capturing: the source
system's architecture and the lessons worth preserving; the concepts that will apply and
where; and the open questions. This is the raw material for P2.

**Exit condition.** A written grounding map exists: source-system understanding + the
concept/framework map + open questions.

---

## P2 — Draft the SDD spec

**Purpose.** Write the first full spec using the canonical skeleton, product-agnostic
throughout.

**Use the skeleton** in `references/sdd-skeleton.md` section by section. Adapt it to the
product — not every product needs every section, and some need extra domain subsystems —
but the *spine* (SDD posture → conceptual model → config model → roster → pipeline as a
state machine → governance → evaluation → data model → build governance → phased contracts)
is what makes it foolproof.

**Product-agnostic discipline (absolute).** Every specific fact becomes a config field
resolved via a `[[VARIABLE]]`-style resolver. NEVER hard-code the worked example into the
generic spec. The worked example lives ONLY in Appendix A ("worked example") and in the
config files — never in the body of the generic spec. **Before shipping, run the scoped
leak-grep from `references/gotchas.md` §3** (it excludes the sanctioned Appendix A / `config/`
zones so it has no false positives) — any hit in the generic body is a leak to fix.

**Author the artifacts alongside the spec.** Do not defer the supporting files to "the
build will generate them." Instruction/rule files ARE source code (Day 4). Author, at least
in skeleton: the agent/role templates, the canon/engine docs (the shared brain), the
policy files, the data schema, and a small golden set. The `/specs` + config file map is
`references/sdd-skeleton.md` Appendix D.

**Voice and formatting (match the exemplar):** bold lead-ins on bullets; inline `§x.y`
cross-references (never line numbers); fenced ```gherkin blocks for acceptance scenarios;
conditional-YAML for config; pinned data-model tables; `####` for x.y.z depth. Keep code
fences balanced (see gotchas — a mis-paired ```gherkin fence silently renders whole
sections as a code block).

**Exit condition.** A complete first-draft PRD exists, product-agnostic, in the exemplar
voice, with the artifact set stubbed alongside it. Snapshot it to disk as the baseline (and
keep a pristine copy for P5's idempotent splice); run `git commit` only when the user asks.

---

## P3 — Wire in the BUNNY build governance

**Purpose.** Make the build *executable, gated, and honest*. Without this, the spec
describes a product but not how to build it safely.

Read `references/bunny-governance.md` and encode into the PRD (exemplar: §18.4 + §19.1):

- The **10-field prompt-contract** per build unit (INTENT · SCOPE · NON-GOALS · INPUTS ·
  INVARIANTS · ACTION · ACCEPTANCE · VERIFY · AUTHORIZATION · ON-FAIL).
- The **validator / executor / authorizer separation** (no actor both does and certifies).
- **Lock-and-proceed / verify-before-next** — a phase locks (VERIFY evidence exists +
  authorized) before the next opens. Full scope is the target, **and a gate is a stop**: the
  Executor halts, presents VERIFY, and waits for an authorization artifact it cannot produce
  itself (`bunny-governance.md` §4). Write every AUTHORIZATION field as that imperative,
  never as a bare role name.
- The **tests-first per-phase gate** — each phase's ACCEPTANCE Gherkin is authored as an
  executable test suite BEFORE its code (red→green); the phase GATE = that suite green + the
  CI eval gate; tests accrue into a growing regression suite every later phase keeps green.
- The **conscious-deviation log** — conform to the tool's ground truth, then log the
  deviation; never silent.
- The **ON-FAIL / grounding disciplines** — don't-fake-MCP, conform to the framework's
  actual shape, report-is-not-the-repo, fail-closed, honest-refusal, verify model IDs / API
  limits / library versions against LIVE docs at build time, supply-chain hygiene.

Turn the phased roadmap (skeleton §19) into a sequence of these gated contracts, blockers
first, each with a concrete VERIFY (evidence, not assertion).

**Exit condition.** The PRD's build plan is a sequence of gated prompt-contracts with
tests-first gates; the governance section is complete.

---

## P4 — Multi-agent foolproofing audit

**Purpose.** Find every gap before the builder does. This is where "foolproof" is earned.

Run the **foolproofing workflow** (`references/workflow-patterns.md` has the full script
shape and schemas). In outline:

- **Fan out ~6–10 adversarial auditors, one per robustness dimension.** Pick the dimensions
  from what actually matters for this product. For Agent Atelier they were:
  intent-capture/onboarding · cadence/planning · troubleshooting-&-recovery ·
  saving-to-post/export · alerts/notifications · approvals · brand/config editing ·
  SDD-buildability ("the smallest quirks") · course-technique maximization. Each auditor
  reads its target sections + the relevant whitepaper and returns structured
  `{gaps[], additions[](targetSection, kind, anchorHint, draftMarkdown), courseTieins[]}`.
- **Add a small design panel (2–3 independent proposals)** for the single most important
  *new* experience (for Agent Atelier: the brand-intake + cadence experience — the user's
  #1 priority). Independent angles → then synthesize the best of all three. This beats
  one-shot design.
- **Consolidate** with synthesizer agents into: (a) a **deduped, section-keyed change-set**
  (each change: id, dimension, targetSection, severity, action, anchorHint, draftMarkdown,
  courseConcept) and (b) a **course-coverage scorecard** (every major concept → current
  strong/partial/missing → planned addition → where in the PRD). The scorecard both drives
  additions and becomes Appendix B.

Scale the pass to the ask: "find any gaps" → a few auditors, light synthesis;
"be comprehensive / foolproof / win" → the full auditor set + design panel + scorecard.

**Exit condition.** A prioritized, deduped, section-keyed change-set exists, ready to assemble
— plus, **for agentic/course products**, a course-coverage scorecard (skip the scorecard for
non-agentic PRDs).

---

## P5 — Assemble the changes into the spec

**Purpose.** Merge many independent findings into ONE coherent document without seam
collisions.

The danger: N agents each drafting additions will redefine the same entities, renumber
sections, and contradict each other at the seams. Prevent it structurally:

- **Cluster the changes by target section**; give ONE assembler agent per cluster.
- Inject into every assembler the **CANONICAL ENTITY SET** — the exact field names of every
  shared entity (Run, QueueItem, AuditEntry, Task, …), so clusters *reference* them rather
  than redefine them.
- Inject the **CONSISTENCY RULES** — an explicit numbered list, e.g.: "one merged definition
  per entity"; "the owner-action model supersedes 'owner sets the Status cell' everywhere";
  "one idempotency hierarchy"; "the exception enum lists every value any consumer sets";
  the section-numbering rule; etc. (Build this list from the collisions you can foresee.)
- Each assembler returns final, merged, **ready-to-splice blocks**:
  `{mode: insert-after | replace | new-section-before, anchorHint, replaceOld?, finalMarkdown}`.

**Apply with the deterministic splicer** (`scripts/splice.py`) — a tiny script beats dozens
of hand-edits and is idempotent:

1. `json.load` the blocks → `html.unescape` **every** field (agents emit `&amp;`/`&lt;`).
2. **Dry-run:** assert every `anchorHint`/`replaceOld` matches **exactly once** in the doc.
   Fix any MISS/DUP before mutating.
3. **Apply from a pristine copy** of the last-good baseline (a `cp` snapshot, not necessarily a
   git commit) so re-runs are idempotent.
4. Report applied/failed. (Dry-run validates against the un-mutated doc; at apply, an earlier
   insertion whose content repeats a later block's anchor can surface that later block as a
   DUP — keep anchors specific.)

**Exit condition.** All blocks spliced; the doc re-reads coherently; snapshot saved.

---

## P6 — Red-team verification

**Purpose.** Catch what the authors and assemblers missed — especially defects created *at
the seams* by the assembly itself.

Run the **red-team workflow** (`references/workflow-patterns.md`). Independent verifier
slices, each owning a region or a lens:

- data-model / pipeline consistency
- approvals / publishing / state transitions
- onboarding / UI
- **a whole-doc cross-ref + consistency + rubric lens** (every inline `§x.y` resolves; every
  enum value has a writer; no contradictions; numbering contiguous; the scorecard is honest)

Give every verifier the same canonical entity set + consistency rules the assemblers had, so
they check against the intended invariants. Each returns `{clean, findings[](severity,
location, issue, suggestedFix)}`.

**Fix every finding. Then loop.** Re-run the verifiers until **two consecutive clean
passes** — the second pass reliably catches defects that the first pass's *fixes* introduced.
No compromise, and do not "compensate" for rate limits by hand-waving a slice: if a verifier
agent dies (session limit / API overload), re-run just that slice rather than skipping it.

Real defects this pass has caught (so you know it earns its cost): a dangling escalation with
no resolver; an enum value that no writer ever set; a mis-paired ```gherkin fence silently
rendering three safety-critical sections as a code block; a tool-name typo that unbound a
safety gate.

**Exit condition.** Two consecutive clean (or clean-modulo-trivial-footnote) verifier passes.
Snapshot saved.

---

## P7 — Export

**Purpose.** Produce the shareable artifacts and verify they rendered correctly.

Run `scripts/export.sh` (or the steps in `scripts/` manually): MD → HTML (Python `markdown`,
extensions `tables, fenced_code, sane_lists, attr_list, toc`, wrapped in the print CSS
template) → **PDF** via Chrome `--headless=new --no-pdf-header-footer --print-to-pdf` →
**DOCX** via `textutil -convert docx`.

**Verify the render** (do not trust it blind):

- page count (`mdimport` then `mdls -name kMDItemNumberOfPages`, or `grep -c '/Type/Page'`)
- code fences balanced (even count of ``` ) — an odd count means a section rendered as code
- zero stray HTML entities in the source
- section numbering contiguous
- spot-read the PDF for ASCII-diagram / wide-table alignment (the mono font-size in the CSS
  is tuned so wide diagrams fit; check it held)

**Exit condition.** MD/PDF/DOCX exist and pass the render checks; share with the user.

---

## Meta-discipline across all phases

- **Durable over ephemeral.** Every phase's output goes to disk (spec, grounding map,
  change-set, scorecard, a design brief), not just the conversation. Compaction is lossy.
- **Snapshot each milestone to disk** (and `cp` a pristine baseline for P5's idempotent
  splice). Run `git commit`/push only when the user asks — do not commit unprompted between
  phases; the pristine-baseline mechanism is a file copy, not a git requirement.
- **Scale the rigor to the stakes.** A throwaway internal tool does not need the full P4–P6
  fleet; a product the user intends to ship or be judged on does. When unsure, lean thorough
  for anything the user calls "important", "foolproof", or "comprehensive".

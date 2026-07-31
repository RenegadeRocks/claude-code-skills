# The multi-agent workflow patterns (P4–P6) — the orchestration DNA

These are the reusable `Workflow`-tool patterns that make the foolproofing (P4), assembly
(P5), and red-team (P6) phases exhaustive and consistent. They were run as workflow scripts
in the Agent Atelier build; the shapes below are generalized so you can regenerate them for
any PRD. Only run these when the user has opted into multi-agent orchestration (Ultracode /
"use a workflow" / an explicit ask); otherwise run a lighter inline version with a few
subagent (`Task`) calls.

The three phases share one anti-collision spine: **a `SHARED` context block** (project facts
every agent must use verbatim), **structured output schemas** (so results are data, not
prose), and **section-keyed change blocks** (so additions splice deterministically).

---

## Inline mode (the DEFAULT — when you don't have the `Workflow` tool)

The patterns below are written in the `Workflow`-tool JS DSL (`parallel()`, `pipeline()`, the
`schema` option). **If you have that tool** (Ultracode / the user asked for a workflow), use it
as written. **If you don't — which is the common case — run the SAME patterns inline with the
`Agent`/subagent tool.** The mapping is one-to-one; only the plumbing changes:

1. **Fan-out → parallel subagent calls.** Use your platform's subagent tool (`Task` in
   standard Claude Code; `Agent` in some builds; or the `Workflow` tool if present). For each
   auditor/designer/verifier, spawn one subagent. Put the **`SHARED` block verbatim** at the
   top of every prompt (this is what keeps them consistent), then the role-specific brief.
   Launch independent subagents **in a single message** so they run concurrently.
2. **Structured output → "return one fenced ```json block".** Subagents can't be schema-forced
   without the Workflow tool, so end every prompt with: *"Return ONLY a single fenced ```json
   block matching this schema: `<paste the schema>`. No prose outside the block."* Then parse
   the block out of each result.
3. **Collect → `blocks.json` → splice.** For assembly (Pattern B), gather the assembler
   results into `blocks.json` and run `scripts/splice.py dry …` then `apply …`. Each assembler
   returns `{cluster, blocks:[…]}`; the splicer consumes a **flat** list of block objects, but
   `splice.py` **auto-flattens** the `[{cluster, blocks:[…]}]` shape (hoisting `cluster` onto
   each block), so you can write the array of wrappers straight to `blocks.json` — or flatten
   yourself by collecting every inner `blocks[]` item into one array. For audit/red-team,
   collect the findings and act on them directly.
4. **Barriers are just "await all before continuing."** Where a pattern shows a `parallel()`
   barrier (e.g. audits → synthesis), inline that means: wait for all the fan-out subagents to
   return, assemble their JSON, then spawn the synthesis subagent with that assembled JSON in
   its prompt.
5. **Loop → re-spawn.** The red-team "loop until two clean passes" is just: fix findings, then
   spawn the verifier subagents again, until a round returns clean.
6. **No subagent tool at all?** Last resort (e.g. a constrained/nested context): run each
   auditor/verifier persona *yourself* as sequential single-agent passes — adopt one role's
   brief at a time, write that pass's JSON to disk, then move to the next lens. Slower and less
   independent, but it still covers the dimensions.

Everything else in this file (the `SHARED` block contents, the schemas, the cluster/consistency
discipline, the splicer) applies **identically** in both modes. Scale the fan-out to the
stakes: a light pass is 2–3 subagents; a "foolproof / comprehensive" pass is the full set.

---

## Pattern A — Foolproofing audit (P4)

Fan out one adversarial auditor per robustness dimension + a small design panel for the most
important new experience, then synthesize. **`parallel()` barrier** is right here only for the
final synthesis (it needs all audits at once); the audits themselves fan out concurrently.

**The `SHARED` block** (author once, pass to every agent) must pin: the project one-liner;
the SDD stakes ("any quirk left unspecified becomes a bug the builder invents"); the PRD path;
the **system facts to use verbatim** (exact agent names, exact pipeline stage names, exact
enum values, the core constructs and their exact field names — so no agent invents variants);
the constraints (product-agnostic; safety invariants); and, for agentic products, the course
concept list with days. This block is the single most important input — it is what keeps 10
agents consistent.

**Auditor schema** (each auditor returns this):

```js
const AUDIT_SCHEMA = {
  type: 'object',
  required: ['dimension', 'gaps', 'additions', 'courseTieins'],
  properties: {
    dimension: { type: 'string' },
    gaps: { type: 'array', items: { type: 'object',
      required: ['title', 'where', 'severity', 'problem'],
      properties: {
        title: { type: 'string' },
        where: { type: 'string', description: 'PRD section(s) affected' },
        severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
        problem: { type: 'string' }, why_it_matters: { type: 'string' } } } },
    additions: { type: 'array', items: { type: 'object',
      required: ['targetSection', 'kind', 'summary', 'draftMarkdown'],
      properties: {
        targetSection: { type: 'string' },
        kind: { type: 'string', description: 'new-subsection|edit|gherkin|data-model|skill|policy|yaml-field' },
        summary: { type: 'string' },
        anchorHint: { type: 'string', description: 'a short unique existing phrase to insert near' },
        draftMarkdown: { type: 'string', description: 'ready-to-insert markdown in the PRD voice' } } } },
    courseTieins: { type: 'array', items: { type: 'object',
      properties: { concept: { type: 'string' }, day: { type: 'string' }, howApplied: { type: 'string' } } } },
    notes: { type: 'string' },
  },
}
```

**Choose the dimensions from what actually matters for the product.** The Agent Atelier set
(a good default menu to adapt): intent-capture/onboarding · cadence/planning ·
troubleshooting-&-recovery · saving-to-post/export · alerts/notifications · approvals ·
config editing · SDD-buildability ("the smallest quirks") · course-technique maximization.
Give each auditor: its dimension label, the target sections to read in full, and a ruthless
brief ("hunt for gaps, holes, ambiguities, missing edge cases, race conditions, idempotency
holes, undefined enums/transitions; propose additive, ready-to-insert fixes; name the
concept+day for each").

**The design panel** — for the single most important *new* experience, spawn 2–3 designers
with *distinct angles* (Agent Atelier: "maximize-brands-in" vs "cadence-first" vs
"robustness/edit/scale-first"), each returning a full design (`intakeFlow`, `cadenceCapture`,
`editingCapturedInfo`, `multiInstanceScaling`, `dataModel`, `gherkin`, `uiNotes`,
`courseTieins`, `standoutIdeas`). Then a **synthesizer** merges the best of all three into one
PRD-ready spec. Independent-then-synthesize beats one-shot design.

**The synthesizers** (barrier — they need all audits): one produces the **deduped,
section-keyed change-set**, one merges the design panel. Change-set schema:

```js
const CHANGESET_SCHEMA = {
  type: 'object',
  // courseScorecard required for agentic/course products; omit or leave [] for non-agentic PRDs
  required: ['changes', 'buildPriority'],
  properties: {
    changes: { type: 'array', items: { type: 'object',
      required: ['id','dimension','targetSection','severity','action','draftMarkdown'],
      properties: {
        id: { type: 'string' }, dimension: { type: 'string' }, targetSection: { type: 'string' },
        severity: { type: 'string', enum: ['blocker','major','minor'] }, action: { type: 'string' },
        anchorHint: { type: 'string' }, draftMarkdown: { type: 'string' }, courseConcept: { type: 'string' } } } },
    courseScorecard: { type: 'array', items: { type: 'object', properties: {
      concept: { type: 'string' }, day: { type: 'string' },
      currentCoverage: { type: 'string', enum: ['strong','partial','missing'] },
      plannedAddition: { type: 'string' }, whereInPRD: { type: 'string' } } } },
    consistencyRisks: { type: 'array', items: { type: 'string' } },
    buildPriority: { type: 'array', items: { type: 'string' }, description: 'ordered change ids, blockers first' },
    notes: { type: 'string' },
  },
}
```

---

## Pattern B — Assembly (P5)

**The problem:** N agents each drafting additions will redefine shared entities, renumber
sections, and contradict each other at the seams. **The fix is structural**, injected into
every assembler:

1. **The CANONICAL ENTITY SET** — the exact field names of every shared entity, written out
   once. Clusters must *reference* these, never redefine them. (This is why §17 of the PRD is
   the join-key spine — it is the source of the canonical set.)
2. **The CONSISTENCY RULES** — an explicit *numbered* list built from the collisions you can
   foresee. Real examples from Agent Atelier: "one merged definition per entity"; "the owner-
   action model supersedes 'owner sets the Status cell' everywhere"; "one idempotency
   hierarchy"; "the exception enum lists every value any consumer sets"; the section-numbering
   rule; "every inline §-ref must resolve to a real section". Pass the SAME list to every
   assembler AND every P6 verifier.

**Cluster the change-set by target section**; one assembler agent per cluster. Each returns
final, merged, **ready-to-splice blocks**:

```js
const BLOCK_SCHEMA = {
  type: 'object',
  required: ['cluster', 'blocks'],
  properties: {
    cluster: { type: 'string' },
    blocks: { type: 'array', items: { type: 'object',
      required: ['mode', 'anchorHint', 'finalMarkdown'],  // for mode:'replace' also require replaceOld
      properties: {
        mode: { type: 'string', enum: ['insert-after', 'replace', 'new-section-before'] },
        targetSection: { type: 'string' },
        anchorHint: { type: 'string', description: 'unique existing phrase; the insertion/replace point' },
        replaceOld: { type: 'string', description: 'for mode=replace: the exact existing text to replace (must match once)' },
        finalMarkdown: { type: 'string', description: 'the final merged block, in PRD voice' } } } },
  },
}
```

**Then apply with the deterministic splicer** (`scripts/splice.py`) — never hand-edit dozens
of insertions:

1. Collect all blocks into one JSON array.
2. `html.unescape` every field (agents emit `&amp;`/`&lt;`).
3. **Dry-run:** assert every `anchorHint`/`replaceOld` matches **exactly once**. Resolve
   every MISS (anchor text drifted) and DUP (anchor not unique — lengthen it) before mutating.
4. **Apply from a pristine copy** of the last-good baseline (a `cp` snapshot; a git commit is
   not required) — idempotent re-runs.
5. Report applied/failed; re-read the doc; snapshot to disk (git commit only if the user asked).

---

## Pattern C — Red-team verification (P6)

Independent verifier slices, each owning a region or a lens, hunting defects **at the seams**
that assembly created. Give every verifier the same canonical entity set + consistency rules
the assemblers had.

**Slices** (adapt to the product): (1) data-model / pipeline consistency; (2) approvals /
publishing / state transitions; (3) onboarding / UI; (4) a **whole-doc cross-ref +
consistency + rubric lens** (every `§x.y` resolves; every enum value has a writer; no
contradictions; numbering contiguous; the scorecard is honest). Verifier schema:

```js
const VERIFY_SCHEMA = {
  type: 'object',
  required: ['slice', 'verdict', 'findings'],
  properties: {
    slice: { type: 'string' },
    verdict: { type: 'object', properties: {
      clean: { type: 'boolean' }, summary: { type: 'string' } } },
    findings: { type: 'array', items: { type: 'object',
      required: ['severity', 'location', 'issue', 'suggestedFix'],
      properties: {
        severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
        location: { type: 'string' }, issue: { type: 'string' }, suggestedFix: { type: 'string' } } } },
  },
}
```

**The loop.** Fix every finding, then **re-run until two consecutive clean passes** — the
second pass catches defects the first pass's fixes introduced. **No compromise:** if a
verifier agent dies (session limit / API overload), re-run *that slice*; do not skip it and
hand-wave a compensating check. (This rule came directly from the user: "don't compensate for
the rate limit… we don't want any compromise.")

**Why it earns its cost** — defects this pass has actually caught: a dangling escalation with
no resolver; an enum value no writer ever set; a mis-paired ```gherkin fence silently
rendering three safety-critical sections as a code block; a tool-name typo that unbound a
safety gate. Authors and assemblers do not see these; independent verifiers do.

---

## Orchestration hygiene (applies to A–C)

- **Structured output over prose.** Always pass a `schema`; you want data you can splice and
  score, not paragraphs to re-parse.
- **Filter nulls.** Big fan-outs lose agents to API-overload / session-limits — `.filter(Boolean)`
  and re-run only the failed items (low concurrency).
- **Moderate per-wave counts.** Keep each wave to a sane fan-out; the workflow tool caps
  concurrency anyway, but moderate waves fail less.
- **`pipeline()` by default, `parallel()` only at true barriers.** Audits→synthesis is a
  barrier (synthesis needs all audits). Verify-each-finding is a pipeline (each finding
  verifies as soon as its review lands). See the Workflow tool docs.
- **Dogfood on this skill's own output.** After authoring or updating a PRD (or this skill),
  run a scaled-down Pattern C over it — adversarial verification is the discipline, and it
  applies to your own work too.

> **Provenance note.** The Agent Atelier build ran these as `Workflow`-tool scripts, but those
> session-local `atelier-prd-*.js` files are **not vendored and not available to a fresh run** —
> don't go looking for them. The schemas and recipes in THIS file (plus the Inline-mode section
> above) are the complete, durable reference; everything you need to run P4–P6 is here.

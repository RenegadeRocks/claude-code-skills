# The canonical SDD section skeleton (the PRD template)

This is the spine of a foolproof spec-driven PRD, generalized from the Agent Atelier PRD
(study `reference-output/EXEMPLAR-PRD.md` for how each of these looks in the flesh). Adapt
per product: drop sections a product genuinely does not need, add domain subsystems it does.
But the **spine** — conceptual model → config model → roster → pipeline-as-state-machine →
governance → evaluation → data model → build governance → phased contracts — is what makes
the document buildable without invention.

Number sections `## 1.`, `### 1.1`, `#### 1.1.1` — a number + period in the heading text. The
**§** sigil is used ONLY in inline cross-references and prose (e.g. "see §7.1"), never in the
heading itself; this matches the gold-standard exemplar. Every inline cross-reference is
`§x.y`, never a line number.

---

## 0. How to read this document (the SDD posture)

State the contract up front:
- This is a **Spec-Driven-Development** document: *the spec is the product; the code is
  regenerated from it.* Anything unspecified is a defect the builder will invent.
- **Architect-mode / no-YOLO:** the builder plans against this spec and proceeds through
  gates; it does not free-associate.
- **Defer to build time:** exact model IDs, library versions, and external API limits are
  confirmed against live docs at build time, not pinned in the spec. The spec states
  *requirements* a model/library must meet, not a version.
- How config resolves: the `[[VARIABLE]]` resolver substitutes placeholders at the tool-call
  boundary (from runtime state, then env). Layer the security rule on top: **secret** vars
  resolve ONLY into the tool/MCP auth layer (never a model-visible prompt); **fact** vars may
  resolve into model-visible text.

## 1. Executive summary

The one-line thesis, then a tight paragraph. What it is, who it is for, why it matters, what
makes it different (usually: the product-agnostic config model).

## 2. Background & motivation

The real system (if generalizing one) and the lessons worth preserving. Why now. What went
wrong with the naive version (for Agent Atelier: the "dead form" — opacity after submit —
motivated the live Studio Floor). Motivate the hard requirements from real pain.

## 3. Goals / non-goals / success metrics

- **Goals** — what it must do.
- **Non-goals (YAGNI)** — what it deliberately will not do. Be explicit; this bounds the
  build.
- **Measurable success metrics** — hard `= 0` targets ONLY where a deterministic check makes
  the failure observable (e.g. "0 safety-field bypasses" is checkable; "0 bad captions" is
  not). Elsewhere use measured rates with confidence intervals. Do not promise unmeasurable
  perfection.

## 4. Personas & journeys

Who uses it, their goals, and the end-to-end journeys. Keep it concrete. These journeys are
what the P4 auditors stress-test.

## 5. Conceptual model (framework grounding)

Map the governing concepts here. For agentic products, this is where the whitepaper concepts
first land: Agent = Model + Harness; the factory model and a specialized agent roster; context
engineering; conductor vs orchestrator (define which mode your top role runs in — see
`references/whitepaper-map.md`). Define the vocabulary the rest of the doc uses. This section
is the bridge from framework to product.

## 6. Architecture

- **Logical components** — the boxes and arrows, substrate-agnostic.
- **Capability requirements** — what each component must be able to do, independent of the
  chosen tech (so the stack can change without a rewrite).
- **Recommended stack** — a concrete recommendation, with the note that versions confirm at
  build time.
- **A simplicity guard** — an explicit statement of what would be over-engineering, to keep
  the build from gold-plating.

## 7. The config model (the product-agnostic core innovation)

**This is usually the most important section** — it is what makes the product general. It
has three parts:
1. **The config object** (the "Brand-Kit" equivalent) — the YAML + assets schema that holds
   everything product-specific. Include the **fail-closed safety fields** (forbidden claims,
   non-disclosure rules, required framing) that block when empty/unconfirmed.
2. **The guided conversational intake** — NOT a dead form. A one-question-at-a-time interview
   that captures intent, with multi-modal ingestion (URL / social handle / brand guide /
   assets) to auto-draft non-safety fields, archetypes/templates for sane defaults,
   progressive disclosure, and *explicit worked-example elicitation of the safety fields*
   (never inferred). Cover editing captured config later (with mandatory safety re-confirm,
   a version bump + audit, and re-resolution timing), and multi-instance scaling
   (clone/switch/templates).
3. **The resolver** — how config populates prompts/tools at run time.

## 8. The agent/role roster (generic, parameterized) + Agent Skills

The roles, each generic and parameterized by config (one role can serve N instances,
selected by an id). Give each a bounded domain. Note which are LLM vs deterministic, which
judge vs act, and the read/draft/act authority ladder. Include the Agent Skills each role
carries (Day 3), and the Skill-vs-MCP-vs-AGENTS.md boundary.

## 9. Canon / engine docs (the shared brain)

The shared knowledge documents the agents read (style, voice, domain rules, the plan). These
are source code (Day 4). Specify how they are seeded from config and re-seeded on edit.

## 10. The production pipeline as a STATE MACHINE

- **The stages**, named exactly, as a state machine (Agent Atelier: PLAN → IDEATE+DRAFT →
  LEDGER LINT → REVIEW → VISUALIZE → CD RENDER PASS → QUEUE → HUMAN GATE → PUBLISH → RECORD).
- **Gherkin acceptance scenarios** for the happy path AND the blocker-grade paths (a state
  machine with named states is what makes acceptance testable and the build unambiguous).
- The transitions, guards, and what each stage consumes/produces.

## 11. Domain subsystems

Whatever the product specifically needs (for Agent Atelier: the visual/typography subsystem,
the offering/campaign subsystem). One subsection each.

## 12. Review / approval / UI / system-of-record

- The approval UX (parity across surfaces, mobile, bulk, request-changes loop,
  approve-with-edits feeding the golden set, roles/delegation, minimizing decisions-per-item).
- The **system of record** (where state lives).
- **A live operator console if the product warrants one** — the "Studio Floor": a live
  visual graph of the agents (who is active now, handoffs, review loops), a continuous
  activity feed, stuck/loop detection with intervene-to-unstick controls (HITL
  participation), first-run/empty/loading/error states, dark+light theming. Ground it in a
  real reference UI if one exists. This is Day-2 A2UI/Generative-UI + Day-4 observability.

## 13. Orchestration & scheduling

The control loop; how work is scheduled; the **run-level cost circuit-breaker** (a per-run
token accumulator + iteration cap — NOT the per-call max-tokens); **crashed-run recovery**
(leases, resumption); poll-based as the documented default.

## 14. Governance / safety / security

Apply the **7-pillar security framework** (Day 4) proportionately. A **Policy Server**
(structural + semantic gating). Fail-closed everywhere safety-critical. Untrusted-content
handling / Confused-Deputy / indirect-injection defenses. The notification model
(event taxonomy, channels, batching/quiet-hours to beat approval fatigue). Secrets handling
(auth layer only). Post-publication correction paths.

## 15. Evaluation

The **7 evaluation dimensions** (Day 4 — *what* you judge): intent satisfaction, functional
correctness, visual & behavioural correctness, cost & efficiency, code quality &
convention-matching, trajectory quality, self-repair — plus a transversal Safety/Responsible-AI
concern. The **methods** (*how* — a separate axis): benchmarks, automated functional testing,
security & safety eval, LLM/agent-as-judge with an explicit rubric, browser-based testing,
trajectory inspection, human review, online eval (plus **convergence** — evaluate whether the
*session* reaches a stable result — as an applied tip, not a distinct method). The golden set.
How approve-with-edits and
reject-reasons feed labeled data back. Deterministic gates are the hard gate; the LLM-judge is
advisory. **Adversarial Red/Blue/Green** (attack / defend / fix — quarantine + auto-refactor)
is a Day-4 security/SecOps
concept (Pillar 6) *applied here as adversarial evaluation* — document it in this chapter (the
exemplar places it at §15.4); it is a security technique, not one of the 7 eval dimensions.

## 16. Integrations

**MCP-first** (Day 2 — "one integration, every framework"). Declared output schemas.
Inspector-verification. The contracts for each integration (inputs, outputs, auth, failure).

## 17. Data model (the join-key spine)

**Pinned entities** with exact field names — this is the spine every other section
references. Define: the core entities, the **join-key** that threads them (Agent Atelier:
`piece_id`), and an **exception axis** — an enum that lists *every* exception/status value
any consumer sets, each with a named writer. This section is where P5's canonical entity set
comes from and what P6 checks hardest. No entity referenced elsewhere may be undefined here;
no enum value may lack a writer.

## 18. Tech stack + build plan + build governance (BUNNY)

The stack, the build plan, and the **BUNNY build governance**
(`references/bunny-governance.md`): prompt-contracts, validator/executor/authorizer split,
lock-and-proceed, the tests-first per-phase gate, the deviation log, the ON-FAIL/grounding
disciplines.

## 19. Phased roadmap = gated prompt-contracts

The roadmap expressed as a sequence of **gated 10-field prompt-contracts**, blockers first,
each with a concrete VERIFY (evidence, not assertion) and a tests-first ACCEPTANCE suite.

Two things this section must carry, learned the hard way:

- **Every AUTHORIZATION field is an imperative, not a role.** *STOP. Present the VERIFY
  evidence and wait. Do not open the next contract on your own authority; it opens when the
  Authorizer writes `authorizations/<unit>.approved`.* A field that reads only "Operator" is
  parsed by builders as metadata, and they run straight through.
- **The suite is shipped, and it needs a hook contract.** Add a short section (the worked
  pattern is a "Test hooks" subsection under Evaluation) listing the minimal stable selectors /
  interfaces / debug affordances the shipped tests locate things by — the only structural
  requirement the spec imposes on the implementation. An artifact that renames a hook fails
  the suite by design.

## 20. Risks & open questions

Honest. The things you are unsure about, the assumptions, the things to confirm at build
time.

## 21. Capstone / submission (only if relevant)

If the PRD is for a course/competition/submission, the section that maps the work to the
rubric and packages the writeup.

## Appendix A — Worked example

The ONLY place the concrete domain example lives in full. This is where the product-agnostic
spec gets shown with real values (Agent Atelier: the Art-of-Living brand kit filled in). Keep
the heading in this `## Appendix A` form — the leak-grep in `references/gotchas.md` §3 anchors
on it to exclude this sanctioned zone.

## Appendix B — Concept map / rubric

The course-coverage scorecard from P4: concept → day → strong/partial/missing → where in the
PRD. For agentic/course products, this is the judge-visible proof of breadth + depth. (Omit
for non-agentic PRDs.)

## Appendix C — Glossary

## Appendix D — /specs & config file map

The artifact set authored alongside the spec:

```
/specs/
  roles/           one file per agent/role (generic, parameterized)
  canon/           the shared-brain docs
  contracts/       the filled 10-field BUNNY prompt-contracts, one per build unit (durable input)
  policies.yaml    role tokens, gates, thresholds, the master kill-switches
  schema/          the data-model schema (mirrors §17)
  golden/          the golden set for evaluation (§15)
  tests/           THE EXECUTABLE ACCEPTANCE SUITE — spec-owned, shipped, not part of the
                   deliverable: harness, every T-xx test, a gated runner, its own package
                   manifest (the harness may have dependencies even when the product may not)
  deviation_log.md the conscious-deviation log (BUNNY)
/authorizations/
  README.md        the human gate as a file: the Authorizer writes <unit>.approved, never the
                   builder; the suite's runner refuses to run the next unit while it is absent
config/
  <instance>.yaml  one config object per product instance (the Brand-Kit)
  assets/          per-instance assets
```

Author these alongside the spec (P2) — do not defer them to regeneration; instruction/rule
files are source code.

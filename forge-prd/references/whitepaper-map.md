# The framework concept map (the 5 "Vibe Coding" whitepapers) — bake these into the PRD

For **agentic / AI products**, this is the body of knowledge a top-quality PRD demonstrates.
The map below is the durable capture; **but at authoring time, READ the actual whitepaper for
each relevant day** — concept fidelity matters and model memory drifts. Record what you weave
in as an Appendix-B scorecard (concept → day → strong/partial/missing → where in the PRD).
(These are multi-page PDFs — Read them in page ranges, e.g. pages 1–20 then 21–40; or lean on
the map below if reading is impractical.)

> **Scope nuance.** The *method* of forge-prd (SDD, BUNNY governance, the multi-agent review
> pipeline) is universal to ANY PRD. This *concept map* is richest for agentic/AI products.
> For a non-agentic idea, apply the relevant subset — do not force-fit all five days.

## The whitepaper vault (read at authoring time)

Resolve the vault directory in this order, first match wins:

1. `$FORGE_PRD_WHITEPAPERS` environment variable, if set.
2. `~/Documents/Satbir Life OS/60-sources/AI Whitepapers/` (the authoring machine's vault).
3. A directory the user names — ask once, only if the PRD is for an agentic/AI product.

If none resolves, skip the PDFs without asking again; the map below is the authored
substitute and is sufficient.

| Day | File | Theme |
|---|---|---|
| 1 | `doc_79be8d5d83f3_Day_1_v3.pdf` | Agents, harness, context engineering, orchestration |
| 2 | `doc_a94840a14963_Agent_Tools__Interoperability_Day_2.pdf` | MCP, A2A/Agent Cards, A2UI |
| 3 | `doc_bf3f834e60ad_Agent_Skills_Day_3.pdf` | Agent Skills / SKILL.md / progressive disclosure |
| 4 | `doc_3c937817f3cb_Vibe_Coding_Agent_Security_and_Evaluation_Day_4.pdf` | Security (7 pillars), evaluation (7 dimensions), observability |
| 5 | `doc_2103526c7ce1_Day_5_v3.pdf` | Spec-Driven Development, Policy Server, HITL, the build workflow |

Prefer the live PDFs whenever a vault resolves.

---

## Day 1 — Agents, harness, context engineering, orchestration

- **Agent = Model + Harness.** The model is a small part; **~90% of an agent is the harness**
  (tools, memory, context, control loop, guards). *PRD implication:* spec the harness in
  detail — the model is the least of it.
- **The factory model.** Your primary output as a developer is no longer code — it is the
  **system that produces code**: the specs + context, the agents, the tests/quality gates, the
  feedback loops, and the guardrails. You design the assembly line and give agents success
  criteria, not step-by-step instructions. *PRD:* the whole document IS that system-design —
  §8 rosters the agents, §15 the quality gates, §18–§19 the line.
- **Context engineering.** The **6 context types** — Instructions, Knowledge, Memory,
  Examples, Tools, Guardrails; **static vs dynamic** context (the split maps onto those types);
  **progressive disclosure** (load detail on demand — the same principle this very skill
  uses); **"context rot"** (long contexts degrade — keep what's loaded relevant). *PRD:* how
  each agent's context is assembled, what's static (canon) vs dynamic (run state), and how
  progressive disclosure keeps prompts lean.
- **Conductor vs orchestrator.** Two modes for driving agents. A **conductor** is hands-on
  and real-time — directing at fine grain, in the loop on implementation detail (watching the
  keystrokes). An **orchestrator** works at a higher level of abstraction — defining goals,
  delegating them to agents, and reviewing results asynchronously, *not* watching
  line-by-line. *PRD:* name which mode your top coordinating role runs in (Agent Atelier's
  Managing Editor is an **orchestrator** — high-level coordination, no IC work) and hold the
  line; an orchestrator that keeps dropping into keystroke-level direction is the smell.
- **Economics / model routing.** Route cheap tasks to cheap models, hard tasks to strong
  ones. *PRD:* a routing note in §6/§13 and cost control in §13 (the run-level breaker).

## Day 2 — Tools & interoperability

- **Specialization (the monolithic ceiling).** A single do-everything agent hits a ceiling; a
  roster of specialized agents with bounded roles scales past it. *PRD:* the §8 roster, each
  role bounded and parameterized.
- **MCP — "one integration, every framework."** The Model Context Protocol as the tool
  substrate: transport (stdio/SSE *per the Day-2 paper* — confirm current MCP transport naming
  at build time; the live spec has moved toward "Streamable HTTP"), **declared output
  schemas**, **Inspector-verification**.
  (MCP also defines resource & prompt primitives, but those come from the standalone MCP
  whitepaper, not the Day-2 paper — don't hunt for them there.) *PRD:* §16 is MCP-first; every
  integration has a declared schema and a contract; secrets live in the MCP auth layer (never
  model-visible).
- **A2A / Agent Cards / bounded domains / the GOTO problem.** Agent-to-agent communication;
  **Agent Cards** advertise a bounded capability; the **GOTO problem** = forcing a
  collaborative agent into a fire-and-forget *tool* wrapper, which injects an unstructured
  GOTO into the orchestrator — A2A resolves it by isolating multi-turn agent routing from the
  (clean, structured) MCP tool layer. *PRD:* if agents talk to each other, do they expose Agent
  Cards? Are domains bounded? Is the hand-off graph structured (a pipeline/state machine) or a
  GOTO tangle?
- **A2UI / Generative UI.** Agents that render UI, not just text — generatively-rendered
  review cards (a Day-4 Vibe-Diff before/after can be *rendered* as one such surface). *PRD:*
  the §12 operator console and per-item review surfaces are A2UI; call it out.
- **AP2 / UCP (autonomous commerce).** A2A extensions for agents that transact or spend:
  mandate-bounded spend, a signed handshake, cryptographic proof-of-payment, and the
  read-operations-vs-financial-actions distinction. *PRD:* pull in ONLY for transactional /
  spend-capable agents — for those, gate financial actions behind mandates + HITL (§12/§14).

## Day 3 — Agent Skills

- **Agent Skills / SKILL.md / progressive disclosure** (**L1 frontmatter → L2 body → L3
  scripts/references**). A skill is a reusable capability packaged for on-demand loading.
  *PRD:* which capabilities are packaged as Skills (§8), and each role's Skills.
- **Skill vs MCP vs AGENTS.md** — the boundary: **Skills** = reusable *procedures/knowledge*;
  **MCP** = *tools/integrations*; **AGENTS.md** = *repo-level standing instructions*. *PRD:*
  put each capability in the right bucket and say why.
- **The read / draft / act authority ladder.** An agent may be allowed to *read*, to *draft*
  (propose, human commits), or to *act* (execute). *PRD:* every role's authority is one of
  these rungs; safety-critical actions sit low on the ladder (draft, human acts).

## Day 4 — Security & evaluation

- **The 7-pillar security framework.** The pillars: (1) Infrastructure & Networking, (2) Data,
  (3) Model, (4) Application & Runtime, (5) Identity & Access Management, (6) Observability &
  Security Ops, (7) Governance. Apply pillar-by-pillar, proportionately. Pillar 6 (SecOps)
  houses **Red / Blue / Green** adversarial teaming (attack / defend / fix — the Green "Agent
  Fixer" does stateful quarantine + auto-refactor, a reactive contain-and-fix) — a
  *security* construct, not one of the 7 eval dimensions, though it is often *applied* as
  adversarial evaluation (the exemplar documents it in the evaluation chapter at §15.4). *PRD:*
  §14 maps each pillar to a concrete control; a scorecard shows coverage.
- **Evaluation — two axes: dimensions and methods.** The **7 dimensions** (*what* you judge):
  (1) intent satisfaction, (2) functional correctness, (3) visual & behavioural correctness,
  (4) cost & efficiency, (5) code quality & convention-matching, (6) trajectory quality,
  (7) self-repair behaviour — plus a transversal **Safety & Responsible-AI** concern. The
  **methods** (*how* you judge — a separate axis): benchmarks, automated functional testing,
  security & safety eval, **LLM/agent-as-judge** (explicit rubric), browser-based testing,
  **trajectory inspection** (judge the path, not just the answer), human review, **online
  eval** (measure in production); **convergence** (reaching a stable result) is an applied tip.
  *PRD:* §15 names the 7 dimensions AND the methods it uses; deterministic gates are hard, the
  LLM-judge advisory.
- **Denial-of-Wallet / observability.** Cost-exhaustion as an attack; **AgBOM** (an agent
  bill-of-materials); **intent-drift** and **trust-decay** monitoring. *PRD:* the run-level
  cost circuit-breaker (§13), observability spans (§12/§14), and a trust model.
- **Supply-chain hygiene.** Verify + pin dependencies. *PRD:* a build-time discipline (BUNNY
  §7).
- **Zero Ambient Authority + JIT downscoping.** No standing broad permissions; grant the
  minimum, just in time. *PRD:* secrets/permissions model in §14.
- **Confused-Deputy / indirect prompt injection.** Untrusted content can hijack an agent's
  authority. *PRD:* §14 untrusted-content handling — quarantine, don't execute instructions
  found in ingested content, keep the deputy from being confused.
- **Vibe-Diff / high-stakes actions.** Before a critical or irreversible tool call, an
  Evaluator Quorum translates the generated action into a **plain-English summary mapping the
  human's fuzzy intent to the proposed execution steps** (a "Vibe-Diff") so the operator
  understands what they are authorising before consent (optionally rendered as a before/after).
  *PRD:* irreversible actions and the master kill-switches in §12/§14 gate behind a Vibe-Diff;
  render it via A2UI (Day 2), and note it composes with the Day-5 HITL checkpoints.

## Day 5 — Spec-Driven Development & the build workflow

- **Spec-Driven Development.** **Markdown + conditional-YAML + BDD/Gherkin.** The spec is the
  product; code regenerates from it. *This is the whole premise of forge-prd* — §0 states the
  posture, §10 is a Gherkin-tested state machine.
- **The Policy Server.** **Structural** gating = fast, deterministic **role/environment
  tool-permission** checks (the "Traffic Lights" — is this tool allowed for this role in this
  environment; e.g. a viewer role cannot call `send_email`, localhost blocks `send_email`).
  **Semantic** gating = a secondary LLM inspects the *intent/content* of the action against
  natural-language policy (e.g. unmasked PII). Offered as a service the pipeline calls. *PRD:*
  §14 Policy Server; fail-closed.
- **Context hygiene / the `[[VARIABLE]]` resolver.** The whitepaper's resolver substitutes
  `[[VARIABLE]]` placeholders at the tool-call boundary from two *sources* (runtime override
  state, then env vars). Layer the security rule on top (the skill's addition, grounded in the
  Day-4 PII-masking narrative): **secret** vars resolve ONLY into the tool/MCP auth layer,
  never a model-visible prompt; **fact** vars may resolve into model-visible text. *PRD:* §0 +
  §7 resolver.
- **HITL checkpoints / approval fatigue.** Human-in-the-loop gates; **approval fatigue**
  (introduced in Day 4 as *confirmation fatigue* — too many gates → rubber-stamping; batch,
  set thresholds, minimize decisions-per-item; it composes with these Day-5 HITL gates). *PRD:*
  §12 approvals + §14 notification batching. (**Vibe-Diff** — the plain-English before/after
  shown before a high-stakes action — is likewise a **Day-4** construct that composes with
  these Day-5 HITL gates and can be rendered via Day-2 A2UI. Note: the vendored exemplar's
  Appendix B tags Vibe-Diff under Day 5 — the concept is *introduced* in Day 4.)
- **The Antigravity build workflow.** Architect/Builder split, **no-YOLO**, sandbox. *PRD:*
  §0 posture + §18 build plan align to it.

---

## The Appendix-B scorecard (the rubric artifact)

Produce this in P4 and ship it as Appendix B. One row per major concept:

| Concept | Day | Current coverage | Planned addition | Where in PRD |
|---|---|---|---|---|
| MCP declared schemas | 2 | partial | add Inspector-verification note | §16.2 |
| Trajectory eval | 4 | missing | add to eval dimensions | §15.4 |
| … | | | | |

It drives the P4 additions AND is the judge-visible proof of breadth + depth for a
course/competition PRD. Keep it **honest** — "strong/partial/missing" reflects the real state,
and P6 checks that the "where in PRD" actually delivers what the row claims.

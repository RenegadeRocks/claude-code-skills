# Agent Atelier — Build Sequence

> **Purpose:** the ordered, gated execution plan for building the complete Agent Atelier under the BUNNY method. Full PRD scope (P0–P6), built and submitted by July 6. Pairs with the spec (#1) and prompt-contracts (#2).
> **Discipline:** lock-and-proceed — each unit *runs and verifies* before the next. Architect-mode/no-YOLO. `/specs` (the PRD) is the source of truth; code regenerates from it.

---

## Phase-by-phase sequence (with gates)

### PHASE 0 — Scaffold `[~30–45m]`
- **P0** — Propose folder structure + pinned stack → owner approves → scaffold `/specs` (PRD + authored artifacts) + `/.agent/skills` + GEMINI.md + MCP tool stubs + CI.
- **GATE:** CI green on stubs; structure approved. → authorize P1.

### PHASE 1 — Single-brand end-to-end build `[~3–5h]`
- **P1-A** — Six core agents (ME, Evergreen, Research, CD, Visual, Ops) for a hard-coded brand; in-process handoffs; §8.1 instruction files.
  - **GATE:** one idea flows through all six agents in role. → P1-B.
- **P1-B** — The pipeline state machine + the `sheets`/`caption_compose`/`image_generate`/`drive` MCP tools; land a piece in the Sheets queue with composited typography.
  - **GATE (PRD §19 P1 exit):** *one on-brand piece passes both gates + the ledger-linter and lands in the Sheets queue for the hard-coded brand.* → P2.

### PHASE 2 — Brand Kit + onboarding `[~3–4h]`
- **P2-A** — Brand Kit schema + `[[VARIABLE]]` resolver; retrofit P1 agents to read config.
  - **GATE:** the P1 brand runs entirely from `brand_kit.yaml`; a second toy brand works via Brand Kit only (the G1 proof); missing-required-var blocks. → P2-B.
- **P2-B** — Brand Onboarding Strategist + intake skill + first-light (safety fields elicited explicitly).
  - **GATE (PRD §19 P2 exit):** *new brand onboarded by interview with zero code changes; produces a piece.* → P3.

### PHASE 3 — Full roster + cadence `[~4–6h]`
- **P3** — Offering Content Agent (brief-per-task) + standing-week scheduler + deterministic ledger-linter (real) + weekly-digest skill.
  - **GATE (PRD §19 P3 exit):** a full week auto-plans/drafts/reviews/queues; a rotation-violating draft is rejected pre-CD. → P4.

### PHASE 4 — Governance & eval `[~5–7h]`
- **P4** — Policy Server (default-deny + claim-grounding + fail-closed + publish-time semantic) + run-level circuit-breaker + append-only audit + CI eval gate.
  - **GATE (PRD §19 P4 exit):** safety/claim scenarios pass; circuit-breaker fires in test; CI eval gate blocks a golden-set regression. → P5.

### PHASE 5 — Approval UI + publishing `[~4–6h]`
- **P5** — Review app + manual handoff + adapter-aware auto-publish (byte-serving + first-comment + carousel cap + idempotency; Instagram-Login path).
  - **GATE (PRD §19 P5 exit):** owner approves via Sheets + app; manual publish works; auto-publish gated, idempotent, audited. → P6.

### PHASE 6 — Improvement loop + multi-brand `[~4–6h]`
- **P6** — Corrections mining → monthly retro + independent post-publication audit (escape rates w/ CIs) + CD↔owner calibration + a second brand.
  - **GATE (PRD §19 P6 exit):** escape-rate audit reports CIs; calibration tracked; two brands run on the same unchanged agent code (the ultimate G1 proof). → feature-complete vs PRD.

---

## Critical-path notes

1. **P1-B is the load-bearing capstone unit.** It's where MCP becomes real and the pipeline closes. Budget the most care here — if MCP↔ADK wiring fights you, it's the §10.3 ON-FAIL: simplest conformant MCP server, never a faked inline function. The engineering fallback is always a genuine, conformant MCP server — never a false MCP claim.
2. **Resist scope creep ruthlessly inside each phase.** The PRD is vast; the temptation to add "just the Policy Server stub" during P1 is how phase boundaries blur. Build the phase you're in, verify, *then* proceed to the next. Same lock-and-proceed discipline that shipped BUNNY M-A.
3. **Verify against live docs at build time** (model IDs, Instagram API limits, ADK/MCP specifics) — only a live 404 proves a model absent; never silent-fallback (§14.3). Your training/codelab knowledge may be stale.

## One-line summary
Build P0 → P1 → P2 → P3 → P4 → P5 → P6 (the full PRD), lock-and-proceed throughout, feature-complete and submitted by July 6.

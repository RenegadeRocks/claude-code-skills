# Agent Atelier — Build Prompt-Contracts

> **Scope:** the full Agent Atelier PRD (v2). Pairs with `01_AGENT_ATELIER_SPEC.md`. **Format:** BUNNY method §6.3 ten-field prompt-contracts, organized along the PRD §19 phase roadmap (P0–P6). Each contract = one build unit; **build + VERIFY before the next** (lock-and-proceed).
> **Executor:** Antigravity (Gemini 3 + ADK), Architect mode / no-YOLO. **Validator:** review each against the PRD before moving on. **Source of truth:** the PRD — regenerate code from it; these contracts govern the build, they do not replace the spec.
> **Build target:** the complete Agent Atelier — P0 through P6 — built in sequence and submitted by July 6. The phases are the full ordered plan; gates are quality checkpoints (lock-and-proceed, verify-before-next).

> **Build posture (PRD §0, §18.2):** propose folder structure + pinned stack for confirmation FIRST; generate tests/docs/logging alongside features; pin every model/library version at build time and verify against live docs (only a live 404 proves a model absent — §14.3). `/specs` is the durable root; code is disposable.

---

## PHASE 0 — Spec & scaffold

### CONTRACT P0 — Repo, /specs, GEMINI.md, tool stubs
1. **INTENT** — Stand up the SDD skeleton so the PRD is the regenerable root and agents have a home.
2. **SCOPE** — Repo; `/specs` (this PRD + the §Appendix-D authored artifacts: agent templates, canon docs, `policies.yaml`, `brand_kit.schema.json`, `resolver.md`, `golden_set.md`, `secrets.md`); `/.agent/skills`; `GEMINI.md`/`AGENTS.md` (project DNA + skills router); MCP tool **stubs** (§16); CI green on stubs.
3. **NON-GOALS** — No agent logic, no real tools, no Brand Kit resolution yet.
4. **INPUTS** — The PRD; ADK; Antigravity.
5. **INVARIANTS** — Folder structure approved by owner before scaffolding (no-YOLO). `/specs` is the source of truth. Secrets via vault reference only (§14.6) from day one.
6. **ACTION** — Propose structure → on approval, scaffold; commit the PRD + authored artifacts; stub the MCP tools; wire CI.
7. **ACCEPTANCE** — PRD §19 P0 exit: *Architect plan approved; CI green on stubs.*
8. **VERIFY** — CI passes on stubs; `/specs` + `/.agent/skills` present; GEMINI.md routes to the skills catalog.
9. **AUTHORIZATION** — Owner authorizes P1.
10. **ON-FAIL** — If Antigravity/ADK project layout differs from assumption, conform to the tool's actual layout (ground truth) and log the deviation.

---

## PHASE 1 — Single-brand end-to-end build

### CONTRACT P1-A — The six core agents (hard-coded test brand)
1. **INTENT** — Bring up the §8 roster minus the Strategist/Offering agents, for ONE hard-coded brand, so a piece can flow end-to-end. This is the multi-agent-system concept (ADK) made real.
2. **SCOPE** — ADK agents: **Managing Editor** (orchestrator), **Evergreen Content**, **Research & Verification**, **Creative Director** (judge), **Visual Production**, **Publishing & Operations**. In-process handoffs (§13.3 default). Each agent's §8.1 instruction file (Identity/Canon/Procedure/Delegation/Hard-rules/Heartbeat/Memory). Brand facts hard-coded for now (Brand Kit comes P2).
3. **NON-GOALS** — No Brand Kit/resolver (P2). No Offering agent (P3). No Policy Server/auto-publish (P4). No Review app (P5). Instagram publish NOT wired (manual/Sheets only).
4. **INPUTS** — P0 scaffold; the canon/engine docs (§9) as `/specs/canon`; Gemini via ADK.
5. **INVARIANTS** — Managing Editor does **no IC work** (delegates only). CD **never edits** drafts (verdicts only). Separation of concerns mirrors the PRD roles exactly.
6. **ACTION** — Build the six agents + their instruction files; wire ME→content→CD→Visual→Ops handoffs.
7. **ACCEPTANCE** — A test idea flows PLAN→DRAFT→(lint stub)→REVIEW→VISUALIZE→QUEUE for the hard-coded brand; agents coordinate in order.
8. **VERIFY** — Run one piece through; confirm each agent acts in role; capture the run (the "real multi-agent system" moment).
9. **AUTHORIZATION** — Owner authorizes P1-B.
10. **ON-FAIL** — If ADK sub-agent I/O differs from assumption, conform to ADK's convention; don't force the assumed hand-off shape.

### CONTRACT P1-B — The pipeline state machine + Sheets gate + Caption-Composer
1. **INTENT** — Make the §10.1 pipeline real end-to-end and land a piece in the Sheets approval queue, with brand typography composited.
2. **SCOPE** — The state machine (PLAN→…→RECORD); the **`sheets` MCP tool** (calendar/queue/ledger/append-only audit — §12.2 integrity: queue sheet ≠ audit trail; orchestrator sole writer of derived status; publish-once guard keyed by `piece_id`); the **`caption_compose` MCP tool** (text-free image in, OCR check, composite brand type system, scrim, channel aspect ratio ≥1080px short edge — §11.2); the **`image_generate`** + **`drive`** MCP tools (text-free generation; host asset).
3. **NON-GOALS** — No claim-grounding/semantic gate yet (P4 — Research returns VERIFIED stubs). No auto-publish.
4. **INPUTS** — P1-A agents; the MCP tool stubs from P0 (now implemented).
5. **INVARIANTS** — Image model renders **NO text** (OCR-verified invariant, §11.2). Scrim behind every line (unreadable first line = reject). Sheets append-only for ledger/audit; idempotent publish guard.
6. **ACTION** — Implement the four MCP tools; wire the pipeline; land a piece in the Sheets queue.
7. **ACCEPTANCE** — PRD §19 P1 exit: *one on-brand piece passes both gates and the ledger-linter and lands in the Sheets queue for the hard-coded test brand (no Review app).*
8. **VERIFY** — Run end-to-end; confirm the piece in Sheets with image (composited type, scrim, correct ratio), caption, alt text; OCR text-free check fires on a baked-glyph test. Capture this end-to-end run.
9. **AUTHORIZATION** — Owner authorizes P2.
10. **ON-FAIL** — If MCP↔ADK wiring is harder than the codelab suggested, fall back to the simplest conformant MCP server the docs support; do NOT fake MCP with an inline function (the protocol is the concept).

---

## PHASE 2 — Brand Kit + onboarding (the G1 core innovation)

### CONTRACT P2-A — Brand Kit schema + [[VARIABLE]] resolver
1. **INTENT** — Lift every brand-specific fact out of the agents into config, so "new brand" = config not code (G1).
2. **SCOPE** — `brand_kit.schema.json` (required/optional, enums, the three **fail-closed** safety fields must be owner-confirmed to validate); the `[[VARIABLE]]` **resolver** (§7.2.1: substitution at prompt-assembly; precedence Brand-Kit→env→error; fail-closed on missing required; secrets resolve **only** into tool/MCP auth layer never model-visible context; resolved values are literals, no re-resolution); the §7.3 seeding map (which field seeds which canon).
3. **NON-GOALS** — No interview yet (P2-B). No Offering agent (P3).
4. **INPUTS** — P1 slice (now the brand facts get externalized); PRD §7.2 schema + Appendix A worked example.
5. **INVARIANTS** — Unresolved required variable **blocks the run** and surfaces to owner (nothing drafted/published). Secrets never inlined into prompts.
6. **ACTION** — Author schema + resolver; retrofit the P1 agents to read `[[VARIABLE]]`s instead of hard-coded facts.
7. **ACCEPTANCE** — The P1 hard-coded brand now runs entirely from a `brand_kit.yaml`; a missing required var blocks with an owner-surfaced gap; the AOL Appendix-A kit validates.
8. **VERIFY** — Swap the brand facts to a second toy brand via Brand Kit only — the same agents produce that brand's piece with zero code change (the G1 proof). Run the "unresolved var blocks" scenario.
9. **AUTHORIZATION** — Owner authorizes P2-B.
10. **ON-FAIL** — If the resolver's serialization (lists/objects into prompts) is ambiguous at a use-site, define the per-site format explicitly (§7.2.1) rather than dumping raw YAML.

### CONTRACT P2-B — Brand Onboarding Strategist + first-light
1. **INTENT** — Capture a brand through a guided conversational interview (not a dead form), producing a valid Brand Kit (G3).
2. **SCOPE** — The **Strategist** agent (§7.1): one question at a time; proposes defaults; **source-ingests** (URL/handle/PDF/logo) to auto-draft **non-safety** fields; **elicits each safety-prohibition field explicitly with worked examples** (read/draft/act ladder — it reads/drafts, owner acts); the **`intake-interview` skill**; first-light commissions one end-to-end test post **including a deliberate near-violation** to surface unstated prohibitions.
3. **NON-GOALS** — Strategist must **not** silently auto-draft claims_forbidden/non_disclosure_rules/required_framing from marketing sources (which never contain prohibitions).
4. **INPUTS** — P2-A schema + resolver; the §7.1 intake design.
5. **INVARIANTS** — Safety fields elicited explicitly, never inferred-and-shipped. Output Brand Kit passes schema validation. No agent code/engine doc modified during onboarding (G1).
6. **ACTION** — Build the Strategist + intake skill; wire source ingestion; wire first-light.
7. **ACCEPTANCE** — PRD §19 P2 exit: *new brand onboarded by interview with zero code changes; produces a piece.* The §7.1 onboarding scenario passes (one-at-a-time; drafts non-safety from sources; elicits safety explicitly; valid kit; first-light near-violation).
8. **VERIFY** — Onboard a fresh brand by interview; confirm zero code change + a produced piece + first-light surfaces a planted prohibition gap.
9. **AUTHORIZATION** — Owner authorizes P3.
10. **ON-FAIL** — If source-ingestion is brittle, fall back to strong defaults + explicit elicitation (the §20 mitigation); the interview, not ingestion, is the load-bearing part.

---

## PHASE 3 — Full roster + cadence

### CONTRACT P3 — Offering Content Agent + standing-week scheduler + ledger-linter + digest
1. **INTENT** — Complete the roster and the always-on rhythm; make anti-repetition deterministic.
2. **SCOPE** — The **Offering Content Agent** (one role; Offering Brief as **dynamic context selected by `offering_id`** — adding an offering = new Brief + cadence slot, no agent-tree change/redeploy, G1); the **standing-week scheduler** (Cloud Scheduler tick → ME orchestrator → task graph w/ blocked-by wake, §13.2); the **deterministic ledger-linter** (§9.4 — the real implementation now, not the P1 stub: hook-in-3, back-to-back-shape, aphorism-1-in-5, idea-rerun-30d, treatment-label-repeat, research-min); the **`weekly-digest` skill** (the anti-silent-stall surface — what shipped/queued/missed/spend/CD↔owner rate).
3. **NON-GOALS** — No Policy Server/claim-grounding/auto-publish (P4).
4. **INPUTS** — P2 Brand Kit + Strategist (Offering Briefs now drafted at intake); the §9.4 linter rules; §13 control loop.
5. **INVARIANTS** — Offering granularity (budget/memory/pause) re-keyed by `offering_id`. **No first-piece self-pause** (routines produce into the queue; gate is at publish). The linter hard-blocks pre-CD (it's what makes "countable violations =0" *true*).
6. **ACTION** — Build the Offering agent + brief-per-task selection; the scheduler/tick; the real linter; the digest skill.
7. **ACCEPTANCE** — PRD §19 P3 exit: *a full week auto-plans/drafts/reviews/queues; a rotation-violating draft is rejected pre-CD.* The §10.2 anti-repetition scenario passes deterministically.
8. **VERIFY** — Run a simulated week; confirm slots fill, the digest posts, and a planted rotation-violating draft bounces at the linter before CD.
9. **AUTHORIZATION** — Owner authorizes P4.
10. **ON-FAIL** — If event-wake is hard, poll-based graph advancement is the documented default (§13.2); Firestore/Pub-Sub are the event-driven upgrade path layered on once the poll-based default is verified.

---

## PHASE 4 — Governance & evaluation (the credibility core)

### CONTRACT P4 — Policy Server + claim-grounding + circuit-breaker + CI eval gate
1. **INTENT** — Wire the safety/governance apparatus before any publish tool is enabled.
2. **SCOPE** — The **Policy Server** (§14.2): structural default-deny `policies.yaml` (all 8 roles × tools × {preview,production}, unlisted=blocked) on all tools; **deterministic claim-grounding** on caption_compose/publish (numeric/verb claim ⇒ near-verbatim match to a VERIFIED `locked_sentence`, every number equal, else BLOCK); **fail-closed safety** on the three fields; **publish-time-only semantic referee** (a second Gemini call at instagram_publish; NOT on every draft — CD is the draft-time judge). The **run-level cost circuit-breaker** (§13.2 — per-run token accumulator + iteration cap; aborts + pauses; distinct from max_output_tokens). Append-only **audit trail**. The **CI eval gate** (§18.2 step 4: pinned judge model + rubric, temp 0; pass/fail on automated §15.2 checks + golden-set threshold; holistic CD verdict advisory in CI).
3. **NON-GOALS** — Still no auto-publish enabling (that's P5, owner-only, never auto-flipped).
4. **INPUTS** — P3 full roster; the §14.2 gate spec; `golden_set.md` (negatives labeled from owner decisions).
5. **INVARIANTS** — Default-deny (any role absent from `policies.yaml` is blocked). Semantic referee runs **only** at publish (avoids LLM-on-LLM + Denial-of-Wallet). Circuit-breaker is the run-accumulator, not a per-call cap.
6. **ACTION** — Author `policies.yaml` (all 8 roles); build the Policy Server middleware; the claim-grounding check; the breaker around the runner; the CI eval gate.
7. **ACCEPTANCE** — PRD §19 P4 exit: *safety/claim scenarios pass; circuit-breaker fires in test; CI eval gate blocks a golden-set regression.* The §10.3 blocker scenarios pass (cost breaker aborts a runaway; safety-field-unconfirmed fails closed; a claim can't ship unverified; non-disclosure binds words+image).
8. **VERIFY** — Run each §10.3 scenario; confirm the breaker fires on a forced runaway; confirm a golden-set regression blocks CI.
9. **AUTHORIZATION** — Owner authorizes P5.
10. **ON-FAIL** — If the semantic referee is costly/flaky, keep the deterministic gates (which are the falsifiable ones) and treat the referee as the secondary catch the PRD already frames it as.

---

## PHASE 5 — Approval UI + publishing

### CONTRACT P5 — Review app + manual handoff + adapter-aware auto-publish
1. **INTENT** — Add the rich in-product review surface and the (gated) publish path.
2. **SCOPE** — The **Review app** (§12.1 — rich view over the same audit trail as Sheets); **manual publish handoff** (frictionless bundle); **adapter-aware auto-publish** (§12.3: only when `auto_publish_enabled` AND mode auto/auto_after_trust-met AND all gates pass AND a channel adapter exists; **byte-serving check** — asset must serve raw `image/*` 200, not a Drive viewer page; **publish-then-comment** for first-comment hashtags; carousel cap confirmed at build time; **idempotent** via publish-once guard). `instagram_publish` is the only launch adapter (Instagram-Login path preferred).
3. **NON-GOALS** — No Reels/Stories auto-publish (feed single-image + carousel only). Other channels manual-only until an adapter is registered.
4. **INPUTS** — P4 governance (publish must pass the Policy Server + byte-serving rule); §12.3 publishing spec.
5. **INVARIANTS** — `auto_publish_enabled` is a master kill-switch; enabling auto-publish is **owner-only, never auto-flipped** (a §14.4 high-stakes action with a Vibe-Diff). Published asset is studio-hosted + byte-serving-valid, never a raw provider URL.
6. **ACTION** — Build the Review app; the manual handoff; the Instagram adapter + byte-serving check + publish-then-comment + idempotency.
7. **ACCEPTANCE** — PRD §19 P5 exit: *owner approves via Sheets and the app; manual publish works; auto-publish gated, idempotent & audited.* The §10.2/§10.3 publish scenarios pass (async Sheets approval; auto-publish precedence; idempotent under duplicate polling; non-image URL blocked; trust-window resets on a violation).
8. **VERIFY** — Approve via both Sheets and app; manual-publish a piece; force a duplicate-approval poll (no double-post); force a Drive-viewer URL (publish blocks).
9. **AUTHORIZATION** — Owner authorizes P6.
10. **ON-FAIL** — Verify Instagram API prerequisites at build time (Business/Creator account; Instagram-Login vs Facebook-Login path); if blocked, manual handoff is the unaffected default.

---

## PHASE 6 — Improvement loop

### CONTRACT P6 — Corrections mining + retro tuning + post-publication audit + multi-brand
1. **INTENT** — Close the learning loop and prove multi-brand.
2. **SCOPE** — Mine the **corrections log** (owner approves/edits/rejects) into the **monthly CD retro** (qualitative triage → engine/canon amendments); the **independent post-publication audit** (§15.3 — sample N published, biased to edited/escalated/auto; re-check with a fresh-context Gemini judge + human spot-audit; report **escape rates with CIs** — the §3.3 numbers); **CD↔owner calibration** tracked; run a **second brand** alongside the first.
3. **NON-GOALS** — No KMeans/fixed-k clustering, no formal before/after experiment harness (directional, owner-driven — §15.3).
4. **INPUTS** — P1–P5 running; the §15.3 audit + calibration design.
5. **INVARIANTS** — Escape rates come from the **independent** audit (not the gate that produced the content — unfalsifiable otherwise). Golden set labeled from **owner** decisions, not CD verdicts.
6. **ACTION** — Build corrections-mining → retro; the post-publication audit; calibration surfacing in the digest; onboard a second brand.
7. **ACCEPTANCE** — PRD §19 P6 exit: *escape-rate audit reports CIs; CD↔owner calibration tracked; a second brand runs alongside the first.*
8. **VERIFY** — Produce one audit report with CIs; confirm two brands run from two Brand Kits on the same unchanged agent code (the ultimate G1 proof).
9. **AUTHORIZATION** — Owner declares the system feature-complete vs the PRD.
10. **ON-FAIL** — If multi-brand surfaces single-process limits, the PRD's DB + object-store migration is the documented next step (§12.2).

---

## Build-order summary (lock-and-proceed; verify-before-next)

P0 scaffold → **P1-A six agents → P1-B pipeline + Sheets + Caption-Composer** (multi-agent + MCP + skills + a gate, end-to-end, one brand) → P2 Brand Kit + Strategist (the G1 innovation) → P3 Offering agent + scheduler + linter + digest → P4 Policy Server + claim-grounding + breaker + CI eval → P5 Review app + publishing → P6 improvement loop + multi-brand.

**The complete Agent Atelier is the build target — P0 through P6, in order, by July 6.** Each phase is a build unit that is locked-and-proceeded: every unit VERIFIED before the next begins. The demo shows the full end-to-end flow and the writeup describes the complete built system. Same one-milestone-verified-before-the-next discipline that carried BUNNY M-A.

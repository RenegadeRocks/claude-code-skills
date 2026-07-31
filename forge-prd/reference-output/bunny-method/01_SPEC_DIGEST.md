# Agent Atelier — Capstone Spec (plan + design)

> **Scope:** the **full Agent Atelier PRD** (v2, 2026-06-30) — the complete 8-agent, product-agnostic content studio. This spec is the one-page architectural digest of that PRD for capstone purposes; the PRD remains the source of truth (regenerate code from the PRD, not this).
> **Track:** Agents for Business. **Platform:** Google Antigravity (Gemini 3 + ADK). **Method:** built under the BUNNY agentic-engineering harness (spec-first, prompt-contracts, conscious-deviation logging, validator/executor/authorizer separation) — the differentiator.
> **Build-scope note:** the artifacts cover the full PRD, and the full PRD is the build target. The complete Agent Atelier (all phases P0–P6) is built in sequence and submitted by July 6. Build-sequence (#4) lays out that ordered plan end-to-end.

---

## PART A — PLAN (what & why)

### A1. Problem
Rebuilding a social-content studio for a new brand today means **rewriting agent prompts and canon by hand** (the AOL/Paperclip system is hard-wired to one brand). Agent Atelier makes "new brand" a **configuration action, not an engineering action** (PRD §2.2). The core promise: **the studio is constant; the brand is configuration** (§1).

### A2. Goals (PRD §3.1, verbatim intent)
- **G1 Product-agnostic** — stand up a working studio for a new brand by supplying only a **Brand Kit**, zero agent-code/engine-doc changes.
- **G2 Faithful reproduction** — reproduce the AOL engine's roster, pipeline, craft rules, governance — generalized, not weakened.
- **G3 Intuitive onboarding** — a guided conversational intake (not a dead form) producing a valid Brand Kit.
- **G4 HITL by default, autonomous-capable** — default human approval gate; per-brand opt-in to auto-publish once trusted.
- **G5 Google-native, simple** — Gemini/Imagen/Drive/Sheets/ADK; pluggable where a non-Google option is genuinely better.
- **G6 Governed & evaluated** — every shipped piece passes safety/compliance gating + automated quality eval before a human.

### A3. Non-goals (PRD §3.2 — YAGNI)
Not Paperclip's multi-company SaaS control plane; not a general scheduler/analytics suite; not paid ads/commerce/Shopping tags; not multi-language NLG R&D; not an agent marketplace; **static assets only in v1** (single images, carousels, static 9:16 covers; Reel *scripts* yes, motion video no; no interactive Stories); no participant/cohort messaging.

### A4. Success metrics (PRD §3.3 — the honest two-kinds model)
Hard **=0** only where a deterministic structural check makes it observable (brand-specific onboarding code changes; countable rotation-rule violations reaching a human; runaway-cost incidents). **Measured escape rates with CIs** where the only honest measure is an independent audit (semantic/visual repetition; unverifiable claims published <2% 95%CI; safety/non-disclosure violations <1% 95%CI). The §15.3 independent post-publication audit produces these numbers (a gate grading its own output is unfalsifiable).

### A5. Course-concept coverage (PRD Appendix B — the rubric anchor)
≥3 required, this PRD hits **all of them**: Day-1 harness/factory/context-engineering/routing; **Day-2 MCP** (§16) + A2A/GOTO (§13.3); **Day-3 Agent Skills/progressive disclosure/SKILL.md** (§8.3) + read/draft/act ladder (§14.1); Day-4 7-pillar security (§14) + 7-dimension eval (§15) + Denial-of-Wallet (§13.2); **Day-5 Spec-Driven Development** (this doc + Gherkin), Policy Server (§14.2), [[VARIABLE]] resolver (§7), HITL/Vibe-Diff (§14.4), Antigravity workflow (§18). This breadth is itself a differentiator.

---

## PART B — DESIGN (how)

### B1. The conceptual spine (PRD §5)
**Agent = Model + Harness** — ~10% model, ~90% harness; almost all of Agent Atelier's value and this spec is harness (canon docs, per-agent instructions, pipeline, gates, budgets); the Gemini model underneath is swappable. **Factory model** — the owner's output is the *system that produces posts*, not the posts. **Static vs dynamic context** — generic engine + brand identity always-loaded; brand specifics retrieved on demand via progressive disclosure (this is what makes it product-agnostic AND token-efficient). **Conductor/orchestrator** — support both human modes + the Managing Editor as agent-orchestrator.

### B2. The agent company (PRD §8 — 8 generic roles)
| Role | Tier | Mandate (one line) |
|------|------|---------------------|
| **Managing Editor** | Reasoning (Gemini 3 Pro) | Strategy, weekly rhythm, delegation, human interface, unblocking. No IC work. |
| **Research & Verification** | Reasoning | Terminal source of facts; maintains the VERIFIED Claim Bank; enforces source allowlist. |
| **Evergreen Content** | Reasoning | The always-on category voice; owns topical territory between offerings. |
| **Offering Content** (1 role, brief-per-task) | Reasoning | Each offering's spotlight/campaign/in-program/retention; selects Offering Brief by `offering_id`. |
| **Creative Director** | Reasoning (judge) | Sole quality judge; reviews every piece pre- and post-render; owns the engine docs. |
| **Visual Production** | Operational (Flash) | Every image/carousel slide + alt text; image pipeline + caption compositing. |
| **Publishing & Operations** | Operational (Flash) | Calendar, ledger linter/audit, approval-queue handoff, weekly visibility digest. |
| **Brand Onboarding Strategist** | Reasoning | Conducts intake; compiles/maintains the Brand Kit + Offering Briefs. |

Running instances for N offerings = 6 fixed + 1 Offering Content (N briefs) + 1 Strategist. Every agent's instruction file follows the §8.1 skeleton (Identity · Canon-to-load · Procedure · Delegation · Hard-rules-from-Brand-Kit · Heartbeat · Memory).

### B3. The Brand Kit — the core innovation (PRD §7)
Everything brand-specific lives in `brand_kit.yaml` + `assets/` + a secrets reference; agents reference it via `[[VARIABLE]]` placeholders resolved at runtime (§7.2.1 resolver: substitution at prompt-assembly, fail-closed on missing required vars, secrets resolve **only** into the tool/MCP auth layer never model-visible context). The Strategist (§7.1) interviews the owner, may auto-draft non-safety fields from ingested sources, but **must elicit each safety-prohibition field explicitly** (claims_forbidden / non_disclosure_rules / required_framing) — these three **fail closed** (empty/unconfirmed = block + route to human). First-light deliberately generates a near-violation to surface unstated prohibitions. The Offerings model (§7.4) replaces hard-coded program agents: one Offering Content role, Brief-per-task selected by `offering_id`.

### B4. The harness brain — canon/engine docs (PRD §9)
Generic, version-controlled, `[[VARIABLE]]`-resolved per brand: **Creative Engine** (variety/anti-drab; hook+shape packs selected by `brand_type`; one-idea/specificity/plain-speech/format-rotation rules), **Visual Engine** (variety-by-message; treatment menu; quality bar; non-disclosure binds words AND image), **Research/Claim Bank** (PENDING→VERIFIED→RETIRED; locked wording; source_hash decay), **Content Ledger + deterministic linter** (the thing that makes "countable rotation violations =0" *true* — hook within 3 posts, back-to-back shape, aphorism 1-in-5 cap, idea-rerun 30d, treatment-label repeat), **Cadence Plan** (standing week + campaign mode; no first-piece self-pause), voice/channel/visual/asset guides.

### B5. The production pipeline (PRD §10.1 — the state machine)
`[PLAN]` ME creates weekly slots+language → `[IDEATE+DRAFT]` content agent (read ledger → pick language → find idea → hook+shape+format → caption → visual brief → assemble) → `[LEDGER LINT]` Ops deterministic linter → `[REVIEW]` CD Gate-0 Scroll-Test + Gate-1 Compliance (verdict approve/revise≤2/reject; round-3 escalate) → `[VISUALIZE]` Visual agent (text-free image → OCR check → composite typography → channel-format → host → alt text) → `[CD RENDER PASS]` post-render multimodal → `[QUEUE]` Ops ledger-audit + handoff bundle → `[HUMAN GATE]` owner approves in Sheets → `[PUBLISH]` manual or auto → `[RECORD]` append-only audit.

### B6. Governance, safety, security (PRD §14 — 7-pillar mapped)
**Read/draft/act ladder per-capability** (§14.1). **Policy Server** (§14.2) middleware in front of tool calls: *structural* default-deny `policies.yaml` (role×tool×env, unlisted=blocked) on all tools; *deterministic claim-grounding* on caption_compose/publish (numeric/verb claims must match a VERIFIED locked_sentence, every number equal); *fail-closed safety* on the three fields; *semantic LLM referee* at publish-time only (avoids LLM-on-LLM on every draft). **Run-level cost circuit-breaker** (§13.2 — encodes the real ~631k-token runaway: per-run token accumulator + hard iteration cap, distinct from per-call max_output_tokens). **HITL + Vibe-Diff** (§14.4) for high-stakes/canon changes; auto-publish never auto-flipped. **Append-only audit** separate from the editable queue sheet. **Sandboxing + secrets vault** (§14.6).

### B7. Evaluation (PRD §15 — CD as sole LLM-judge)
Gate-0 craft + Gate-1 compliance offline; the 7 course dimensions mapped (§15.2: intent/functional/visual/cost/quality/trajectory/self-repair); golden set with **negative exemplars labeled from owner decisions** (breaks the good-only circularity); CD↔owner agreement + false-approve rate is the explicit trust signal gating auto-publish; independent post-publication audit produces the §3.3 escape rates with CIs.

### B8. Stack & substrate (PRD §6.3, §18)
Antigravity (sandboxed browser E2E) · ADK (multi-agent) · Gemini 3 Pro (reasoning/judge) + `gemini-flash-latest` alias (operational) + optional Flash-Lite (mechanical) · Vertex AI Agent Engine (durable Sessions + Memory Bank) or Cloud Run · MCP servers (§16) · Sheets + Drive/GCS (system of record) · Nano Banana Pro (`gemini_image_pro` token) / Imagen fallback / Replicate optional · Cloud Scheduler. **Confirm all model IDs + API limits against live docs at build time** (§0/§14.3 — only a live 404 proves a model doesn't exist; never silent-fallback).

### B9. Integrations (PRD §16 — MCP-first, "one integration, every framework")
`image_generate` · `caption_compose` · `drive` · `sheets` · `research_fetch` · `instagram_publish` (only launch adapter; Instagram-Login path preferred) · optional `notify`/`calendar`. The cost breaker wraps the runner, not a tool.

### B10. Data model (PRD §17)
Brand · BrandKit · Offering · CanonDoc · Agent · Task(`offering_id`) · Draft(`visual_brief` mandatory) · Review · Asset · LedgerRow · QueueItem · ClaimBankEntry · Run(`total_tokens`+`iterations` for the breaker) · AuditEntry. Storage Sheets/Drive default, DB pluggable.

---

## PART C — How this is built (method + the build plan)

### C1. Method (the differentiator)
Built under the BUNNY harness: **spec-first** (this + the PRD) → **prompt-contracts** per build unit (#2) → build → **verify before next** → **conscious-deviation logging**. This is the Day-5 "spec-driven, production-grade, governed fleet" thesis demonstrated on a real, serious build — the reason the submission reads production-grade where others show a notebook that ran once. The method is *how the system is built*.

### C2. The build plan (all phases, in sequence)
The PRD §19 phases P0–P6 are the full ordered plan, built start to finish and submitted by July 6. Each gate is a quality checkpoint — lock-and-proceed, verify-before-next — not a stopping line. The build proceeds: stand up the harness and substrate (P0), the Phase-1 single-brand end-to-end build (Managing Editor + Evergreen + Research + CD + Visual + Ops; idea→lint→review→render→Sheets-queue→approve; Caption-Composer; first test brand) which exercises multi-agent (ADK) + MCP + skills + the pipeline + a gate end-to-end, then the Offerings model and second brand, full governance/Policy Server, evaluation harness, onboarding Strategist, and auto-publish trust calibration through P6. The build-sequence (#4) carries the ordered task list across the whole plan, so each phase locks against its acceptance criteria before the next begins. The completed end-to-end system is the demo; the writeup describes that complete built system.

### C3. Honest risk register (PRD §20 + capstone reality)
| Risk | Mitigation |
|------|------------|
| Image-model fidelity | text-free generation + OCR backstop + composited type + CD multimodal pass + regenerate-on-fail (§11, §20). |
| Auto-publish trust | human-default; auto gated behind concrete trust_threshold + calibration + Policy Server + audit; never auto-flipped. |
| Cost runaway | run-level circuit-breaker + per-agent/per-offering budgets + model routing (§13.2). |

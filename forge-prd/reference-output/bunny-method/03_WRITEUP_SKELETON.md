# Agent Atelier — Kaggle Writeup Skeleton

> **Purpose:** the structure + prompts for the ≤2,500-word Kaggle Writeup. **Track:** Agents for Business. Each section gives a target word count, what to say, and the evidence to attach. Fill the brackets; keep the total ≤2,500 (Kaggle penalizes over-limit). **Lead with the working system; land the BUNNY method as the differentiator; describe the complete built system accurately.**

> **Required attachments (Overview §Submission):** cover image (use the §6.1 architecture diagram), a ≤5-min YouTube video, a public project link (the GitHub repo with setup steps is the accepted substitute for a live demo). Select the **Agents for Business** track on the Writeup.

---

## Title + subtitle (~25 words)
- **Title:** Agent Atelier — [e.g. "A Product-Agnostic AI Content Studio: the studio is constant, the brand is configuration"].
- **Subtitle:** one line naming the business problem + the agent approach (e.g. "An 8-agent ADK studio that turns a one-time Brand Kit into an always-on, governed social feed for any brand").

## 1. The business problem (~250 words) — *why this matters, money on the line*
- Open with the enterprise pain: producing a **steady, on-brand, factually-safe social feed** is expensive, manual, and doesn't scale across brands. Marketing teams/agencies rebuild the whole pipeline per client.
- The cost framing (Agents-for-Business rubric: "cost or revenue on the line"): every new brand today = **re-engineering** (rewriting agent prompts + canon by hand). State the inefficiency concretely.
- The insight: **the studio should be constant; the brand should be configuration.** Onboarding a brand becomes a *config action, not an engineering action* — that's the cost lever.
- Ground it in reality: this generalizes a **real, working system** (Paperclip/AOL — an 8-agent studio producing live wellness content). You're not theorizing; you're lifting a proven engine into a product-agnostic one. *(Attribution: your team's prior work — state it.)*
- **Evidence:** one line on the existing system's real output cadence.

## 2. What Agent Atelier is (~300 words) — *the system, concretely*
- The one-paragraph product: describe a brand once via a **guided interview** → a company of **8 cooperating AI agents** plans, writes, illustrates, quality-reviews, and queues an on-brand social feed → a human approves → publish.
- Name the 8 agents and their one-line mandates (Managing Editor / Research & Verification / Evergreen / Offering / Creative Director / Visual / Publishing-Ops / Strategist) — show it's a *company*, not a prompt.
- The core innovation: the **Brand Kit** — all brand-specific facts in config; generic agents reference `[[VARIABLE]]`s; the same agents run for a coffee brand, an NGO, a SaaS, a meditation school — only the Brand Kit changes.
- The governance promise: **every piece passes safety + compliance + quality gating before a human sees it**; human-in-the-loop by default, auto-publish only once a brand is *trusted* (measured).
- **Evidence:** the §6.1 architecture diagram (also your cover image); a screenshot of a piece in the Sheets queue.

## 3. Agent architecture & the course concepts (~600 words) — *the technical heart; hit the rubric*
> This is where you demonstrate the **3+ required course concepts**. Be explicit — judges look for them by name. (Appendix B of the PRD maps all of them; name each as implemented in the finished system.)

- **Multi-agent system (ADK)** — the 8-role company; in-process handoffs; the Managing Editor as orchestrator; the production pipeline (PLAN→IDEATE→LINT→REVIEW→VISUALIZE→QUEUE→PUBLISH). Show the agents *coordinating*.
- **MCP servers** — every external capability over MCP ("one integration, every framework"): `sheets`, `image_generate`, `caption_compose`, `drive`, `research_fetch`, `instagram_publish`. Show a real MCP tool-call in the demo.
- **Agent Skills (progressive disclosure)** — SKILL.md anatomy (L1 frontmatter / L2 body / L3 scripts); the packaged skills (draft-a-piece, verify-a-claim, compose-caption, ledger-lint, weekly-digest, intake-interview).
- **(Day-5) Spec-Driven Development** — the whole thing regenerates from a 45-page spec; `/specs` is the source of truth, code is disposable. This is your *strongest* alignment to Day 5.
- **(Day-4) Security & evaluation** — name the ones you wired: the **Policy Server** (default-deny + claim-grounding + fail-closed safety), the **run-level cost circuit-breaker** (the real ~631k-token lesson), the **read/draft/act ladder**, the **Creative Director as LLM-judge** across 7 eval dimensions.
- Keep each concept to a tight paragraph + a pointer to where it lives in the repo. Name each concept as implemented in the finished system and point to the code that runs it.

## 4. What makes it production-grade — the BUNNY method (~450 words) — *the differentiator*
> This is your wedge. Most submissions are a notebook that ran once. Yours is built under a **governed engineering harness** — and you can prove it.

- Name the method: a **spec-first, contract-governed** build process (the BUNNY agentic-engineering method), with **validator/executor/authorizer separation**, **one-milestone-verified-before-the-next**, and **conscious-deviation logging**.
- Tie it to Day 5 directly: the course's thesis is "spec-driven, production-grade, governed, observable fleet" — the method is *exactly that*, demonstrated on a real build, not described.
- Concrete proof points (pick 2–3): the **prompt-contracts** governing each build unit (attach one); the **report-is-not-the-repo** grounding discipline (you verify against the codebase, not descriptions); the **fail-closed/honest-refusal** discipline baked into the contracts (e.g. "don't fake MCP — if an integration can't be reached, the contract degrades to the simplest conformant MCP server rather than a stub that pretends").
- The framing that *builds* credibility: the build is governed end-to-end by the harness, so the claims in the writeup are grounded in code that runs. Say plainly: *"This is a serious, fully-specified product — built the way production agent fleets should be."* That grounding is more persuasive to judges than any unverified claim.
- **Evidence:** link the PRD (the 45-page SDD is itself a differentiator); attach one prompt-contract; the conscious-deviation log if you have one.

## 5. Demo (~250 words) — *what the judges will see*
- Walk the 5-min video's arc in prose: a **Brand Kit in** → agents coordinate → a piece drafted → linted → CD-reviewed → image generated + typography composited → landed in the Sheets queue → "and here's the governed harness behind it." The demo walks the full end-to-end system.
- State the reproducibility path: the public repo + README run-steps (the accepted live-demo substitute); name the test brand (the AOL Appendix-A kit is a ready worked example).
- Show the complete flow in the demo: the full 8-agent pipeline from Brand Kit through publish-queue, exactly as specified in the PRD.
- **Evidence:** the YouTube link; the repo link; 2–3 key screenshots in the Media Gallery.

## 6. Results, limitations, what's next (~250 words) — *honest close*
- What the complete system does; the metrics model (the §3.3 hard-=0 vs measured-escape-rate-with-CIs honesty — the evaluation is falsifiable by design).
- Limitations, stated plainly (PRD §20): image-model fidelity (mitigated by text-free + OCR + composited type + CD pass); static-assets-only v1 (a deliberate product non-goal, per the PRD).
- What's next: genuine future enhancements beyond the PRD — e.g. additional publishing channels (LinkedIn, X, TikTok), richer analytics-driven strategy loops, and a self-serve onboarding console.
- Close on the thesis: **the studio is constant; the brand is configuration** — and the harness is why it's trustworthy.

---

## Word-budget check
| Section | Target |
|---|---|
| Title/subtitle | 25 |
| 1. Business problem | 250 |
| 2. What it is | 300 |
| 3. Architecture + concepts | 600 |
| 4. The method (differentiator) | 450 |
| 5. Demo | 250 |
| 6. Results/limits/next | 250 |
| **Total** | **~2,125** (≈375 headroom under the 2,500 cap) |

## Submission checklist (Overview §Submission Requirements)
- [ ] Writeup ≤2,500 words, **Agents for Business** track selected
- [ ] Cover image attached (the architecture diagram)
- [ ] ≤5-min video on YouTube, attached to the Media Gallery
- [ ] Public project link (GitHub repo + README setup steps) attached
- [ ] Repo is public and the README lets a stranger run the full system end-to-end
- [ ] Writeup accurately describes the complete built system
- [ ] Submitted (not left as draft) before **July 6, 2026 11:59 PM PT**

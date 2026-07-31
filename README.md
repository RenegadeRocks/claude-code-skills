# Claude Code Personal Skill Library

Ten custom skills for [Claude Code](https://claude.com/claude-code), most built on 2026-07-07 from a deep research pass over this machine's projects, agent systems (Hermes + OpenClaw), and ~800 Claude Code sessions. Each skill encodes a recurring workflow, a hard-won lesson, or a quality bar so future sessions apply it automatically.

Every skill was verified against live machine facts and tested with dummy-data scenarios before release.

## Installation

Copy any skill folder into `~/.claude/skills/`:

```bash
cp -R <skill-name> ~/.claude/skills/
```

Claude Code picks it up automatically — invoke explicitly (e.g. `/game-verify`) or let it trigger when a conversation matches its description.

---

## The Skills

### 🤖 Agent Fleet Operations

| Skill | What it does |
|---|---|
| [**agent-fleet-doctor**](agent-fleet-doctor/SKILL.md) | Diagnoses and repairs the two AI agent systems on this Mac mini (Hermes "Rehmat" and OpenClaw "Josh/hosh/saraswati"). Contains the full system map, gateway recovery commands, the safe config-change procedure, a known-failure-modes table, and the "Bing Bong" test for vetting fallback models before wiring them in. |

### 🎮 Game Studio

| Skill | What it does |
|---|---|
| [**game-verify**](game-verify/SKILL.md) | Pre-ship verification for single-file HTML games. Enforces *played gameplay* as the standard of proof — a rendering title screen is not a verified game. Covers syntax checks, mobile-viewport playtesting, complete-loop validation, and DPR crispness. |
| [**game-portfolio-triage**](game-portfolio-triage/SKILL.md) | Audits and ranks game prototypes like a serious game director: original hook > strong fantasy > expandable mechanic > market distinctiveness > aesthetic identity — and never by polish. Produces evidence-backed Top 5 / Next 5 / kill-notes reports. |

### 📢 Proof & Shipping

| Skill | What it does |
|---|---|
| [**public-proof**](public-proof/SKILL.md) | Turns finished work into public evidence: a case study, LinkedIn drafts in an authentic personal voice (with an explicit banned-AI-slop list), and a vault archive entry. Built to fix the "strong work that stays invisible" problem. |
| [**oss-release**](oss-release/SKILL.md) | The go-public checklist for a repo: secrets archaeology across full git *history* (not just HEAD), runs-without-keys demo mode, README-for-strangers, license and hygiene — ending in an explicit safe-to-flip-public verdict. |

### 🖥️ Mac Mini Infrastructure

| Skill | What it does |
|---|---|
| [**mac-service-deploy**](mac-service-deploy/SKILL.md) | Runbook for deploying persistent services on the Mac mini: launchd vs PM2, Tailscale vs Cloudflare tunnel (including the Airtel QUIC-block → `--protocol http2` fix), reboot-survival testing, and log hygiene. |

### 📐 Systems & Specs

| Skill | What it does |
|---|---|
| [**system-to-spec**](system-to-spec/SKILL.md) | Extracts a portable spec from an already-*working* system so it can be rebuilt on any platform: behavior inventory, invariant-vs-configuration split, Gherkin acceptance tests, and cold-rebuild fidelity checks. |
| [**forge-prd**](forge-prd/SKILL.md) | Turns an idea or existing system into a professional, foolproof Spec-Driven-Development PRD: the spec IS the product. Grounded in framework research, governed by the BUNNY build harness with tests-first per-phase gates, adversarially red-teamed until clean, then exported to MD/PDF/DOCX. Strongest for agentic/multi-agent products; the method applies to any PRD. Ships with reference outputs, a methodology library, and export scripts. |

### 📚 Learning & Family

| Skill | What it does |
|---|---|
| [**learning-capsule**](learning-capsule/SKILL.md) | Converts a work session or topic into a durable learning artifact: plain-English explanation, the concepts that decided the outcome, a transferable lesson, and spaced-repetition review cards. |
| [**family-studio**](family-studio/SKILL.md) | Building for the family: educational games and stories for the kids, and teaching/admin support tools for Art of Living work — with hard rules (no accounts, no data collection, offline single-file HTML, celebration over punishment). |

---

## Design Notes

- Skills follow the [Agent Skills](https://agentskills.io/specification) format: one folder per skill, `SKILL.md` with `name` + `description` frontmatter, where the description holds only *triggering conditions* so the skill body stays authoritative.
- Several skills are personalized to this specific machine (paths, launchd labels, exemplar plists). Adapt those details before reusing elsewhere.
- Testing approach: baseline failures came from real documented history; each skill was then exercised by an independent agent against dummy fixtures (including a fake repo with a secret planted in git history, and a dummy prototype portfolio) and corrected until behavior matched intent.

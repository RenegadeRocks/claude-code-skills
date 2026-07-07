---
name: game-portfolio-triage
description: Use when auditing, ranking, or curating game prototypes — picking which daily prototypes deserve full-game development, portfolio review of Hermes Game Studio or Codex output, "which of my games is best", or selecting demo/showcase candidates.
---

# Game Portfolio Triage

Audit prototypes as a **serious game director / portfolio scout**, not a cheerleader. The owner is a 20-year game designer — generic praise is worthless to him. Make hard, evidence-backed decisions.

## Where the Portfolio Lives

- `~/Documents/AI projects/Hermes Game Studio/daily-prototypes/` — one dated dir per prototype (60+)
- `~/Documents/AI projects/Hermes Game Studio/full-games/` — promoted projects (e.g. bell-diver)
- `~/Documents/AI-Projects/Codex/` — dated hardened/reviewed games
- Stand-alone: `~/space-invaders-rajni`, `~/space-invaders-telegram`, SwarmGrinder, dungeon-crawler under `~/Documents/AI-Projects/claudecode/`

## Ranking Rubric (in priority order)

1. **Original hook** — is the core idea something you haven't seen? One-line test: does the pitch make you want to play *right now*?
2. **Strong fantasy** — clear role + stakes ("pull the sea home before dawn" beats "match the tiles")
3. **Expandable mechanic** — does the verb support 20+ hours of design space (upgrades, enemies, modes) or is it exhausted in 60 seconds?
4. **Market distinctiveness** — would it stand out on itch.io/Steam mobile? Check the prototype's own `trend-brief.md` claims against the build.
5. **Emotional/aesthetic identity** — authored palette, tone, feel; not template art

**Explicitly do NOT rank by polish.** A rough build with a novel expandable hook beats a juicy clone. Polish is purchasable; hooks are not. A pitch that *leads* with polish or juice is a red flag, not a selling point.

## Method

1. Enumerate candidates; read `one-page-pitch.md` + `README.md` for each (fast pass).
2. Shortlist ~15 on hook alone. For those, read `review.md`/`iteration-log.md` and **play the build** (mobile viewport) — the pitch often overpromises.
3. Score 1–5 on each rubric axis, with a file- or play-based evidence line per score. No score without evidence.
4. Cut hard. Ties break toward expandability, then distinctiveness.

## Output Format

- **Top 5** — for each: hook in one line, why it wins (evidence), what a 2-week vertical slice would prove, biggest risk
- **Next 5** — one line each: what would promote it
- **Kill notes** — patterns across the rejected pool (e.g. "reflex-only verbs", "no fail state"), so tomorrow's prototypes improve
- One **portfolio-level observation**: what the last N days of prototypes say about where the studio's taste is drifting

## Guardrails

- Never say "all of these are great." If everything scores 4+, the rubric was applied too softly — recalibrate against the single best item.
- Quote the prototype's own artifacts when judging (pitch vs. delivered build gaps are a key signal).
- If a build won't load, that's a data point for triage, not a reason to skip it silently — note it.

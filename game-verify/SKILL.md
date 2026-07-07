---
name: game-verify
description: Use before delivering, shipping, or declaring done any single-file HTML game or daily prototype — including Hermes Game Studio prototypes, Codex games, Telegram/WhatsApp game deliveries — or when a game cron failed verification, a game shows a black screen, controls don't work on mobile, or "it renders but is it playable?".
---

# Game Verify

Pre-ship verification for single-file HTML games. **A rendering title screen is NOT a verified game.** The recurring failure: syntax is fine, title renders, but nobody actually played it. Verification means *played gameplay*, not loaded page.

## The Bar (all must pass)

**Structural**
- [ ] Single self-contained `index.html` — no CDN, no external assets, no build step
- [ ] JS parses: extract `<script>` contents to a temp `.js` file, run `node --check` on it
- [ ] No console errors on load (check via browser, not assumption)

**Playability (test by PLAYING, 10–15 seconds minimum)**
- [ ] First meaningful player action possible within ~3 seconds of pressing start
- [ ] Complete loop exists: title → play → escalation → ending/fail state (not an endless demo)
- [ ] One clear verb the player understands without instructions
- [ ] At least one tradeoff or resource decision (not pure reflex)
- [ ] Losing is possible; dying/failing restarts cleanly

**Mobile-first (test at phone viewport, e.g. 390×844)**
- [ ] Fully playable with one thumb — zero keyboard required
- [ ] Title and HUD text readable at phone size
- [ ] Canvas is DPR-crisp (`devicePixelRatio` scaling — no blurry canvas)
- [ ] No accidental scroll/zoom during play (`touch-action`, `preventDefault`)

**Feel**
- [ ] Audio via WebAudio synth (no audio files); haptics where sensible
- [ ] Authored visual identity (palette from the pitch, not default colors)
- [ ] Juice on key events: hit feedback, score pop, screen response

## How to Actually Test

1. `node --check` the extracted script(s) — catches the classic syntax blocker.
2. Open in a real browser at mobile viewport (use gstack `/browse` or Playwright). Screenshot title.
3. **Play it**: perform the core verb, take damage/fail once, reach or force an ending. Screenshot mid-play.
4. Check console for errors after the play session, not just after load.

## Hermes Studio Artifacts (when verifying a daily prototype)

Prototype dirs live at `~/Documents/AI projects/Hermes Game Studio/daily-prototypes/YYYY-MM-DD-slug/` and must contain: `index.html`, `README.md`, `trend-brief.md`, `one-page-pitch.md`, `iteration-log.md`, `build-notes.md` (+ `review.md` after QA). Confirm `build-notes.md` records what was *actually tested*, not what should work.

## Verdict Format

Report PASS/FAIL per section with evidence (what you played, what you saw). A FAIL lists the smallest fix that would flip it. Never report "verified" on load-only evidence — that is the exact failure this skill exists to prevent.

---
name: family-studio
description: Use when building anything for the family or seva — educational games, study tools, quizzes, or stories for the kids; teaching materials, program support, or admin automation for Rajni's Art of Living work; bedtime stories, riddles, or kid-friendly AI tools.
---

# Family Studio

Building for the family: the kids (study support, educational play, stories) and Rajni's Art of Living teaching (materials, admin relief). Different bar than portfolio work — the user here is a child or a volunteer, not a game-industry audience.

## Hard Rules (family software)

- **No accounts, no data collection, no external calls.** Single-file, offline-capable HTML — delivered as one file over Telegram/WhatsApp, opens on any phone.
- Mobile/touch-first (kids use phones/tablets); works with one thumb.
- Age-appropriate difficulty curves: forgiving fail states, fast retries, celebration over punishment. A kid should feel *smart*, not tested.
- Language: default English, but ask whether Hindi/Punjabi text should be included for family/AOL audiences — don't assume.
- Kid content: no ads-style dark patterns, no timers that induce panic (unless the game IS about time and the kid chose it).

## Educational Game Recipe

1. Pick ONE learning target (times tables, spelling set, history facts) — a game that teaches three things teaches none.
2. Wrap it in a real game verb (the owner is a game designer — mechanics-first, worksheet-never): shooting the right answer beats selecting it; collecting, dodging, and building all work.
3. Difficulty ramps with mastery, not time. Track streaks in `localStorage`; adapt. Make level-ups visible, celebrated events — not silent stat changes.
4. Always run **game-verify** on the build (mobile playability section especially) — no exceptions; family games ship broken more often because "it's just for the kids."

## Stories, Riddles, Quizzes

- Bedtime stories: their world (India, family, seva values) as texture, not moralizing sermons. Pratchett-flavored wit lands in this house.
- Riddles/quizzes as single-file HTML with reveal interactions, or plain text for WhatsApp forwarding — ask which delivery.

## Art of Living / Rajni Support

- Tone: seva, service, warmth — **zero commercial hype**. Never marketing-speak for spiritual content.
- Fit: schedule/participant tracking, program handout formatting, session materials, certificate generation — admin relief so she can teach.
- **Instagram/social content for AOL is Paperclip's job** (the multi-agent studio) — don't duplicate it here; build tools, not posts.
- Anything using real participant data stays local (no cloud services), and confirm with the user before touching such data at all.

## Delivery

Hand over as: the file + a one-line WhatsApp-forwardable description ("Tap to open — a times-tables blaster for Anaya, works offline"). If it's a keeper, suggest a `public-proof` write-up — family builds are his most distinctive public story.

---
name: learning-capsule
description: Use when the user wants to LEARN from work just done — "explain what you did", "teach me", "what should I understand here", after a complex fix or build the user watched, when studying a course topic (Kaggle, AI courses), or when a hard-won lesson deserves to be retained rather than lost.
---

# Learning Capsule

Turn work or a topic into a durable learning artifact. The owner is a non-programmer who builds through AI — every session is also a curriculum. He runs spaced repetition (MomentumOS uses SM-2), so capsules include review cards.

## Capsule Format

```markdown
# <Topic> — YYYY-MM-DD

## What happened (plain English)
2–4 sentences a smart non-programmer follows. Game-design analogies land
best (roles, rules, win/fail states, resource tradeoffs).

## The concepts that mattered (3–7)
- **<concept>** — what it is in one line, and WHY it decided the outcome here.

## The transferable lesson
One paragraph: the pattern he'll meet again, stripped of today's specifics.

## Review cards (3–5, Q on one line, A on the next)
Q: ...
A: ...

## Try it yourself (optional, 15 min)
One concrete exercise on his own machine/projects.
```

## Rules

- **Explain what it DOES, not what it's called.** Jargon gets one plain-English gloss on first use, then may be used freely.
- Concepts must come from *this* session's actual decision points — not a generic tour of the technology.
- Cards test understanding ("why did X fail when Y?"), not vocabulary recall.
- Honest difficulty: if something is genuinely advanced, say "this is deep water; here's the 80% version."

## Where It Goes

Save to `~/Documents/Satbir Life OS/60-sources/` as `YYYY-MM-DD-learning-<slug>.md` (create nothing outside this vault path). Mention the file path in the reply so Rehmat's vault-watching picks it up. If the topic belongs to an active course (e.g. Kaggle companion), say so — he may want the cards in that track instead.

## When NOT to Use

Routine work with no new concept (a config bump, a re-run). A capsule for trivia trains him to skip capsules. If asked to "remember" something operational rather than educational, that's session memory, not a capsule.

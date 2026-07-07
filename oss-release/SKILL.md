---
name: oss-release
description: Use when taking a private repo public, open-sourcing a project, preparing a GitHub release, "make this repo presentable", or pre-publication checks — secrets in git history, license selection, README for strangers, demo mode without API keys.
---

# OSS Release

Checklist for taking a repo public. Exemplar: `~/Documents/AI-Projects/MiCA-OSS/` (see its `OSS_NOTES.md`). The two failure modes this prevents: **a secret in git history** and **a repo strangers can't run**.

## 1. Secrets Archaeology (history, not just HEAD)

- `git log -p | grep -iE "api[_-]?key|secret|token|password|sk-|bearer" ` — scan the FULL history; a key deleted in HEAD still ships in history.
- Use `gitleaks detect` if available (`brew install gitleaks`).
- Check for committed `.env`, `*.json` credential files, hardcoded phone numbers/emails, absolute paths leaking the username, and `.bak`/`.clobbered` config copies.
- If history is dirty: fresh-start repo (new init, single clean commit) is usually cheaper than history rewriting for a solo project. Confirm with the user before either.

## 2. Runs-Without-Keys (the MiCA pattern)

A stranger must get value in <5 minutes with zero paid keys:
- Demo mode or mock data path, documented in README (MiCA uses `Ctrl+Shift+D` / localStorage toggle)
- `.env.example` with every variable, a comment each, no real values
- Graceful degradation when keys are missing (feature disabled, not crash)

## 3. README for Strangers

Order: one-line what-it-is → screenshot/GIF (near the top — this repo sells visually or not at all) → quickstart (copy-paste commands, tested from a clean clone) → demo mode → configuration table → architecture sketch → license. Test the quickstart in a fresh directory before claiming it works.

## 4. Hygiene

- LICENSE file (default MIT, per prior projects) with correct name/year
- Delete: `.bak` files, `tmp/`, OS junk, dead branches, TODO-littered files that embarrass
- `.gitignore` covers env files, DBs, node_modules, `__pycache__`
- Repo description + topics set on GitHub; pin if flagship
- Tag `v1.0.0` (or honest `v0.x`) with release notes: what it does, what's rough

## 5. Announce

Once public, **public-proof** skill handles the case study + post. Don't skip it — an unannounced repo is invisible.

## Verdict Format

Report as a checklist with pass/fail/fixed per item, plus a final "safe to flip public: yes/no" with the blocking items named. Never say safe-to-publish without having run the history scan.

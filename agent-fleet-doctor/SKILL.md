---
name: agent-fleet-doctor
description: Use when a personal AI agent (Rehmat, Josh, hosh, saraswati) is stuck, offline, silent on Discord/Telegram/WhatsApp, replying non-stop (runaway), when a cron job failed, when changing agent models/fallbacks/config, or when the OpenClaw or Hermes gateway needs restart or repair on this Mac mini.
---

# Agent Fleet Doctor

Diagnose and repair the two agent systems on this Mac mini. **First rule: identify WHICH system before touching anything** — they have been confused before (an OpenClaw problem was once investigated in Hermes).

## System Map

| | Hermes | OpenClaw |
|---|---|---|
| Agent(s) | **Rehmat** | **Josh** (main), **hosh**, **saraswati** |
| Channels | Discord (primary), Telegram, WhatsApp | Telegram (Josh + hosh bots), WhatsApp |
| Home | `~/.hermes/` (code: `~/.hermes/hermes-agent/`) | `~/.openclaw/` |
| Config | `~/.hermes/config.yaml` | `~/.openclaw/openclaw.json` — **clobber-prone, never hand-edit** |
| CLI | `hermes` (`~/.local/bin/hermes`) | `openclaw` |
| Gateway launchd label | `ai.hermes.gateway` | `ai.openclaw.gateway` (port 18789) |
| Cron | `~/.hermes/cron/` | `~/.openclaw/cron/` + several launchd jobs |

Related launchd jobs (`ls ~/Library/LaunchAgents/`): `com.openclaw.hosh-daily-intel` (+watchdog, +telegram, +health-check), `com.openclaw.pankaj-whatsapp-monitor`, `com.openclaw.whatsapp-daily-digest`, `ai.openclaw.telegram-agent-watchdog`, `com.metaclaw`.

## Recovery Runbook

1. Is the gateway running? `launchctl list | grep -E "hermes|openclaw"` (exit status + PID).
2. Force-restart:
   - Hermes: `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`
   - OpenClaw: `openclaw gateway restart` (handles launchd handoff), then `openclaw gateway status`.
3. Check logs: `~/.hermes/logs/`, `~/.openclaw/logs/`, and `log show --last 10m --predicate 'subsystem contains "launchd"'` if the job won't start.
4. Cron failures: Hermes `~/.hermes/cron/` job state; OpenClaw `~/.openclaw/cron/` (`jobs-state.json*`, `runs/`). Note: the hosh-intel/hosh-telegram/pankaj-monitor/whatsapp-digest jobs run under **launchd** (`com.openclaw.*`), not OpenClaw's internal cron — check `launchctl list` for those. Common causes below.

## Safe Config Changes (OpenClaw)

Never hand-edit `openclaw.json` (see the many `.clobbered` backups). Always:
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-cc-before-<change>
openclaw config patch --file /tmp/patch.json --dry-run   # objects merge, arrays REPLACE
openclaw config patch --file /tmp/patch.json
openclaw config validate && openclaw gateway restart
```
Model registry: `models.providers.<id>.models`. Agent fallback chains: `agents.list[].model.fallbacks` and `agents.defaults.model.fallbacks`. **Because arrays REPLACE, any patch touching an array (`agents.list`, a `fallbacks` list, a `models` list) must contain the complete final array, not just the new item** — always review the `--dry-run` diff before applying.

## Known Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Rehmat asked to restart, never returns | launchd `KeepAlive{SuccessfulExit:false}` only relaunches on non-zero exit; restart dispatch bug | `kickstart -k` as above; check `gateway/run.py` restart dispatch detects launchd via `XPC_SERVICE_NAME` |
| Agent replies non-stop until /stop (runaway) | Free **reasoning** model as fallback (e.g. Nemotron) — doesn't signal turn-end | Swap to instruction-tuned (`-it`) model; test first (below) |
| "Codex/subscription limit reached" | ChatGPT Plus weekly agent cap is separate from app chat; all `openai/*` fail together → cascade to fallback | Wait for reset or rely on fallback chain |
| Cloudflare tunnel down / app unreachable | ISP (Airtel) blocks QUIC/UDP | `--protocol http2` in the tunnel plist |
| Cron "model not in allowlist" | Job references a retired model id | Point job at a registered model via config patch |
| OpenRouter fallback 401/429 | Revoked key / shared free pool rate limit | Verify key; free-tier 429s are transient |

## Testing a Candidate Fallback Model (before wiring it in)

Reasoning models make bad agent backends. Register the model, then run one turn: `openclaw agent --agent <id> ...` (see `openclaw agent --help`) with a nonsense prompt like **"Bing Bong"**. Pass = exactly one reply, then stops. Ramble/loop = reject. Also check it returns 200 (free pool 429s are common — retry once before judging).

## Hard Rules

- **Never print tokens/keys into the transcript** (gateway token, OpenRouter key). For iOS/device pairing (and only pairing — it's not for API keys), have the user run `openclaw qr` themselves since the QR embeds the admin token.
- 4 Hermes cron jobs were repointed Telegram→Discord in June 2026 — **ask before reverting**.
- Back up before every config change; state what you changed and how to revert.
- Touch only the service you diagnosed — many look-alike launchd jobs live here.

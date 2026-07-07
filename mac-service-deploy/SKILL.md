---
name: mac-service-deploy
description: Use when deploying, hosting, or keeping alive a web app or background service on this Mac mini — launchd plists, PM2, Cloudflare tunnel, Tailscale access, nightly sync jobs, "make it survive reboot", "access it from my phone", or a locally-hosted app that went unreachable.
---

# Mac Service Deploy

Runbook for running services persistently on this Mac mini. Working exemplars already on the machine — copy their patterns, don't invent new ones.

## Decision: How Is It Accessed?

| Need | Mechanism | Exemplar |
|---|---|---|
| Private, own devices only | **Tailscale** (no public exposure) | MomentumOS |
| Public URL / phone on 4G | **Cloudflare named tunnel** | HealthBuster (`com.healthbuster.tunnel`) |
| Localhost only | launchd/PM2 alone | metaclaw |

Default to Tailscale for personal tools; tunnel only when a public URL is genuinely needed. Tailscale is installed but often stopped — check `tailscale status` first and start it if needed. Simplest private access: bind the app to `0.0.0.0` and hit the Mac's tailnet IP from the phone; `tailscale serve` (check `tailscale serve --help` for current syntax) adds HTTPS on top.

## Keep-Alive: launchd vs PM2

- **Python/FastAPI or shell services** → launchd plist in `~/Library/LaunchAgents/`. Exemplars to copy: `com.healthbuster.server.plist` (server), `com.healthbuster.garmin.plist` (scheduled sync via `StartCalendarInterval`).
- **Node/Next.js apps** → PM2: `pm2 start pm2.config.cjs && pm2 save` (`pm2 startup` already configured — `pm2.root.plist` exists). Exemplar: MomentumOS `DEPLOY.md`.

launchd essentials: `RunAtLoad` + `KeepAlive` for servers; absolute binary paths (launchd has no shell PATH — use `/opt/homebrew/bin/...`; for Python apps use the app's venv interpreter, e.g. `<app>/.venv/bin/python3`); `StandardOutPath`/`StandardErrorPath` into `~/Library/Logs/` — NOT `/tmp`, which macOS wipes on reboot (some exemplar plists get this wrong; don't copy that part). User LaunchAgents need a logged-in session (fine on this always-logged-in mini). Load with `launchctl bootstrap gui/$(id -u) <plist>`; force-restart with `launchctl kickstart -k gui/$(id -u)/<label>`.

## Cloudflare Tunnel Gotchas (learned the hard way)

- **Airtel blocks QUIC/UDP** → the tunnel MUST run with `--protocol http2` or it dies silently.
- Use the **named tunnel** (config in `~/.cloudflared/config.yml`), never quick tunnels — quick-tunnel URLs are volatile.
- New hostname: add the ingress rule **before** the catch-all in `config.yml`, then `cloudflared tunnel route dns <tunnel> <hostname>`, then restart the tunnel service.
- Verify from a phone **on 4G, not WiFi** — LAN success proves nothing about the tunnel.

## Deployment Checklist

1. Build/prepare app; run it manually once and hit it with `curl` — never wrap a broken app in launchd.
2. Create plist (copy an exemplar) or PM2 entry; load it; confirm with `launchctl list | grep <label>` (PID present, status 0) or `pm2 status`.
3. Wire access (Tailscale serve / tunnel ingress). Verify from the actual client device.
4. Scheduled jobs (nightly syncs): separate plist with `StartCalendarInterval`, logging to a file you name in the report.
5. **Reboot test or equivalent**: at minimum `kickstart -k` and confirm it comes back. A service that can't survive restart isn't deployed.
6. Report: label, port, URL, log paths, and the one-line restart command — this line is what gets pasted into a memory/vault note.

## Guardrails

- Many unrelated launchd jobs live here (agents, watchdogs, monitors) — `kickstart` only the label you created.
- Ports in use: 18789 (OpenClaw gateway), 8000 (HealthBuster). Check `lsof -i :<port>` before claiming one.
- Secrets go in `.env` or plist `EnvironmentVariables`, never echoed into the transcript.

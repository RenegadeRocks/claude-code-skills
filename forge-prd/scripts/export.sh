#!/usr/bin/env bash
# export.sh — P7 export pipeline: PRD.md -> HTML -> PDF (+ DOCX) with render verification.
# macOS ONLY (uses textutil, mdls, /Applications Chrome). On Linux, run manually:
#   python3 -m venv v && v/bin/pip install markdown && v/bin/python build_html.py IN.md OUT.html "Title"
#   chromium --headless=new --no-pdf-header-footer --print-to-pdf=OUT.pdf "file://$PWD/OUT.html"   # or: weasyprint OUT.html OUT.pdf
#   pandoc OUT.html -o OUT.docx    # textutil is macOS-only
#
# Usage:  ./export.sh /path/to/PRD-name.md ["Document Title"]
# Produces, alongside the .md:  PRD-name.html, PRD-name.pdf, PRD-name.docx
#
# Steps: markdown->HTML (throwaway venv) -> Chrome headless ->PDF -> textutil ->DOCX,
# then verifies: page count, code-fence balance, stray HTML entities, section contiguity.
set -euo pipefail

SRC="${1:?usage: export.sh PRD.md [title]}"
TITLE="${2:-PRD}"
[ -f "$SRC" ] || { echo "no such file: $SRC" >&2; exit 1; }

DIR="$(cd "$(dirname "$SRC")" && pwd)"
BASE="$(basename "$SRC" .md)"
HTML="$DIR/$BASE.html"
PDF="$DIR/$BASE.pdf"
DOCX="$DIR/$BASE.docx"
HERE="$(cd "$(dirname "$0")" && pwd)"

# --- 1. Markdown -> HTML (throwaway venv so we never touch the system python) ---
VENV="$(mktemp -d)/prd-venv"
python3 -m venv "$VENV"
"$VENV/bin/pip" -q install markdown >/dev/null
"$VENV/bin/python" "$HERE/build_html.py" "$SRC" "$HTML" "$TITLE"

# --- 2. HTML -> PDF via Chrome headless (no header/footer chrome) ---
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
[ -x "$CHROME" ] || { echo "No Google Chrome / Chrome Canary found. Install Chrome, or run the HTML->PDF step manually (HTML is at $HTML)." >&2; exit 1; }
# build a proper file:// URL so paths with spaces (e.g. "My Documents") survive
URL="$(python3 -c 'import sys,pathlib; print(pathlib.Path(sys.argv[1]).as_uri())' "$HTML")"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PDF" "$URL" 2>/dev/null
echo "PDF written:  $PDF"

# --- 3. HTML -> DOCX via textutil ---
textutil -convert docx "$HTML" -output "$DOCX"
echo "DOCX written: $DOCX"

# --- 4. Render verification (FAILS CLOSED on the brief-critical checks) ---
echo
echo "=== render verification ==="
FAIL=0
# page count (informational)
mdimport "$PDF" >/dev/null 2>&1 || true
PAGES="$(mdls -name kMDItemNumberOfPages -raw "$PDF" 2>/dev/null || true)"
# mdls returns (null) on a just-created file (Spotlight is async); fall back to counting
# page objects in the PDF. Chrome writes "/Type /Page" WITH a space, and it's a binary file:
case "$PAGES" in ''|'(null)') PAGES="$(grep -a -c '/Type */Page' "$PDF" 2>/dev/null || true)";; esac
case "$PAGES" in ''|0) PAGES='?';; esac
echo "pages: $PAGES"
# GATE: code-fence balance (odd => a section silently rendered as a code block)
FENCES="$(grep -c '^```' "$SRC" || true)"
if [ $((FENCES % 2)) -eq 0 ]; then echo "code fences: $FENCES (balanced ✓)";
  else echo "code fences: $FENCES (ODD ✗ — a fence is unclosed; a section is rendering as code)"; FAIL=1; fi
# GATE: stray HTML entities in PROSE only (entities inside fenced code blocks can be legit)
ENT="$(awk '/^```/{f=!f; next} !f' "$SRC" | grep -oE '&(amp|lt|gt|quot|nbsp|#[0-9]+);' | wc -l | tr -d ' ' || true)"
if [ "$ENT" -eq 0 ]; then echo "stray HTML entities in prose: 0 ✓";
  else echo "stray HTML entities in prose: $ENT ✗ (leaked &amp;/&lt; outside code fences — unescape them)"; FAIL=1; fi
# top-level section numbering (human spot-check — contiguity is not auto-asserted)
echo "top-level sections found (human spot-check for contiguity):"
grep -oE '^## +§?[0-9]+' "$SRC" | grep -oE '[0-9]+' | tr '\n' ' ' || true
echo
echo "Spot-read the PDF for ASCII-diagram / wide-table alignment before shipping."
if [ "$FAIL" -ne 0 ]; then echo "RENDER VERIFICATION FAILED ✗ — fix the ✗ items above before shipping." >&2; exit 2; fi
echo "render verification passed ✓"

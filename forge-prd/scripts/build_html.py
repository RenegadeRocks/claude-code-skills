#!/usr/bin/env python3
"""
build_html.py — render a PRD Markdown file to a print-ready HTML file.

Generic version of the Agent Atelier build script. The print CSS is tuned so wide
ASCII diagrams and tables fit on A4 (small mono font-size for <pre>).

Usage:
    python3 build_html.py SRC.md OUT.html ["Document Title"]

Requires the `markdown` package. Install in a throwaway venv (P7):
    python3 -m venv /tmp/prd-venv && /tmp/prd-venv/bin/pip install markdown
    /tmp/prd-venv/bin/python build_html.py SRC.md OUT.html "Title"
"""
import sys
import markdown

if len(sys.argv) < 3:
    sys.exit("usage: build_html.py SRC.md OUT.html [title]")

SRC, OUT = sys.argv[1], sys.argv[2]
TITLE = sys.argv[3] if len(sys.argv) > 3 else "PRD"

with open(SRC, encoding="utf-8") as f:
    text = f.read()

body = markdown.markdown(
    text,
    extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"],
    output_format="html5",
)

CSS = """
@page { size: A4; margin: 15mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 11px; line-height: 1.5; color: #1b1b1b; margin: 0;
  -webkit-font-smoothing: antialiased;
}
h1 { font-size: 22px; line-height: 1.2; margin: 0 0 4px; color: #111; }
h2 { font-size: 16px; margin: 22px 0 6px; padding-bottom: 3px;
     border-bottom: 1.5px solid #d8d8d8; color: #111; break-after: avoid; }
h3 { font-size: 13px; margin: 16px 0 4px; color: #1a1a1a; break-after: avoid; }
h4 { font-size: 11.5px; margin: 12px 0 3px; color: #333; break-after: avoid;
     text-transform: none; letter-spacing: .2px; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 2px 0; }
strong { color: #111; }
a { color: #1a5fb4; text-decoration: none; }
hr { border: none; border-top: 1px solid #e2e2e2; margin: 16px 0; }
blockquote {
  border-left: 3px solid #c4c4c4; margin: 8px 0; padding: 2px 0 2px 12px;
  color: #3a3a3a; background: #fafafa;
}
code {
  font-family: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
  background: #f0f1f2; padding: 1px 4px; border-radius: 3px; font-size: 0.88em;
}
pre {
  background: #f7f8fa; border: 1px solid #e3e6ea; border-radius: 6px;
  padding: 10px 12px; overflow: hidden; white-space: pre; break-inside: avoid;
}
pre code {
  font-family: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
  background: none; padding: 0; font-size: 8.5px; line-height: 1.28; color: #222;
}
table {
  border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.5px;
  break-inside: auto;
}
th, td { border: 1px solid #cdd2d7; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #eef0f2; font-weight: 600; }
tr { break-inside: avoid; }
"""

html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{TITLE}</title>
<style>{CSS}</style></head>
<body>
{body}
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_doc)

print(f"HTML written: {OUT} ({len(html_doc)} bytes)")

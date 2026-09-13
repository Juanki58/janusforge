# -*- coding: utf-8 -*-
"""Build Janusforge investor brief PDF (+ HTML fallback) from Markdown."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parents[1]
SRC_MD = ROOT / "docs" / "investors" / "JANUSFORGE_INVESTOR_BRIEF.md"
OUT_PDF = ROOT / "docs" / "investors" / "JANUSFORGE_INVESTOR_BRIEF.pdf"
OUT_HTML = ROOT / "docs" / "investors" / "JANUSFORGE_INVESTOR_BRIEF.html"

CSS = """
@page { size: A4; margin: 1.7cm 1.5cm 1.9cm 1.5cm; }
body {
  font-family: Helvetica, Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.45;
  color: #1a1a1a;
}
h1 {
  font-size: 18pt;
  margin: 0 0 0.4em 0;
  color: #111;
  page-break-after: avoid;
}
h2 {
  font-size: 12.5pt;
  margin-top: 1.15em;
  color: #222;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.15em;
  page-break-after: avoid;
}
h3 {
  font-size: 11pt;
  margin-top: 0.9em;
  page-break-after: avoid;
}
p, li { margin: 0.28em 0; }
ul, ol { margin: 0.3em 0 0.5em 1.2em; }
blockquote {
  border-left: 3px solid #555;
  margin: 0.55em 0;
  padding: 0.2em 0.75em;
  color: #333;
  background: #f6f6f6;
}
code, pre {
  font-family: Courier, monospace;
  font-size: 8pt;
}
pre {
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 0.5em;
  white-space: pre-wrap;
  word-wrap: break-word;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.55em 0;
  font-size: 8.5pt;
  table-layout: fixed;
}
th, td {
  border: 1px solid #bbb;
  padding: 0.25em 0.32em;
  vertical-align: top;
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
th { background: #eee; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.0em 0; }
.meta { color: #555; font-size: 9pt; margin-bottom: 1.0em; }
.cover-note {
  font-size: 9.5pt;
  color: #333;
  background: #f0f0f0;
  border: 1px solid #ccc;
  padding: 0.55em 0.7em;
  margin: 0.8em 0 1.1em 0;
}
a { color: #1a1a1a; text-decoration: none; }
"""


def normalize_unicode(text: str) -> str:
    """Map specialty chars to PDF-safe forms for Helvetica / WinAnsi."""
    repl = {
        "\u0394": "Delta",
        "\u03b1": "alpha",
        "\u03b2": "beta",
        "\u03b3": "gamma",
        "\u03bc": "u",
        "\u00b1": "+/-",
        "\u00d7": "x",
        "\u00b0": " deg",
        "\u00a7": "sec. ",
        "\u2079": "9",
        "\u2078": "8",
        "\u2077": "7",
        "\u2076": "6",
        "\u2075": "5",
        "\u2074": "4",
        "\u00b3": "3",
        "\u00b2": "2",
        "\u00b9": "1",
        "\u2070": "0",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u21d2": "=>",
        "\u2212": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00b7": " | ",
        "\u2248": "~",
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u226a": "<<",
        "\u226b": ">>",
        "\u2713": "[ok]",
        "\u2717": "[x]",
        "\u26a0": "[!]",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def build_html(md_text: str) -> str:
    md_text = normalize_unicode(md_text)
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    cover = (
        '<div class="cover-note">'
        "<strong>Nota de lectura:</strong> documento de credibilidad cientifica. "
        "No es un deck Series-A, no contiene proyecciones financieras ni claims de farmaco. "
        "Autoridad: RESEARCH_STATE.md."
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='latin-1'/>"
        f"<style>{CSS}</style></head><body>"
        f"{cover}{body}"
        "</body></html>"
    )


def main() -> int:
    if not SRC_MD.is_file():
        print(f"[FAIL] missing source: {SRC_MD}", file=sys.stderr)
        return 1

    md_text = SRC_MD.read_text(encoding="utf-8")
    html = build_html(md_text)
    OUT_HTML.write_text(html, encoding="latin-1", errors="replace")
    print(f"[OK] HTML -> {OUT_HTML.relative_to(ROOT)}")

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PDF.open("wb") as fh:
        status = pisa.CreatePDF(html, dest=fh, encoding="latin-1")
    if status.err:
        print(
            f"[WARN] PDF had {status.err} error(s); HTML fallback kept at "
            f"{OUT_HTML.relative_to(ROOT)}",
            file=sys.stderr,
        )
        print(
            "Retry with: pandoc docs/investors/JANUSFORGE_INVESTOR_BRIEF.md "
            "-o docs/investors/JANUSFORGE_INVESTOR_BRIEF.pdf",
            file=sys.stderr,
        )
        return 2

    print(f"[OK] PDF  -> {OUT_PDF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

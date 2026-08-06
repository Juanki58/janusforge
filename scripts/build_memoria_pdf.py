# -*- coding: utf-8 -*-
"""Build consolidated Janusforge memoria PDF from project markdown docs."""
from __future__ import annotations

import io
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "exports" / "janusforge_memoria_completa.pdf"

SECTIONS = [
    (
        "Guia Maestra Nivel 0 — Fundamentacion biotecnologica y hoja de ruta de quimiotipos",
        ROOT / "docs" / "guia_maestra_biotecnologia_quimiotipos.md",
    ),
    (
        "Apendice A — Literatura fibrosis CB1/CB2",
        ROOT / "docs" / "literatura_fibrosis_cb1_cb2.md",
    ),
    (
        "Apendice B — Quimioma cannábico CB1/CB2",
        ROOT / "docs" / "quimioma_cannabico_cb1_cb2.md",
    ),
    (
        "Apendice C — Quimiotipos varinas / THCV–THCVA",
        ROOT / "docs" / "quimiotipos_varinas_thcv.md",
    ),
    (
        "Apendice D — Criterio de exito Janus",
        ROOT / "docs" / "criterio_exito_janus.md",
    ),
    (
        "Apendice E — Informe retrospectivo: separacion del panel",
        ROOT / "results" / "reports" / "retrospective_panel_separation.md",
    ),
]

CSS = """
@page { size: A4; margin: 1.8cm 1.6cm 2.0cm 1.6cm; }
body {
  font-family: Helvetica, Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.45;
  color: #1a1a1a;
}
h1 { font-size: 18pt; margin: 0 0 0.6em 0; color: #111; page-break-before: always; }
h1.cover { page-break-before: avoid; font-size: 22pt; margin-top: 2.5cm; }
h2 { font-size: 13pt; margin-top: 1.2em; color: #222; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
h3 { font-size: 11.5pt; margin-top: 1em; color: #333; }
h4 { font-size: 10.5pt; margin-top: 0.8em; }
p, li { margin: 0.35em 0; }
blockquote {
  border-left: 3px solid #666;
  margin: 0.6em 0;
  padding: 0.2em 0.8em;
  color: #333;
  background: #f7f7f7;
}
code, pre {
  font-family: Courier, monospace;
  font-size: 8.5pt;
}
pre {
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 0.6em;
  white-space: pre-wrap;
  word-wrap: break-word;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.7em 0;
  font-size: 8.5pt;
}
th, td {
  border: 1px solid #bbb;
  padding: 0.25em 0.4em;
  vertical-align: top;
  text-align: left;
}
th { background: #eee; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.2em 0; }
.meta { color: #555; font-size: 9.5pt; margin-bottom: 1.5em; }
.toc li { margin: 0.25em 0; }
.section-label {
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
  color: #666;
  margin-bottom: 0.3em;
}
a { color: #1a1a1a; text-decoration: none; }
"""


def normalize_unicode(text: str) -> str:
    """Map specialty chars to PDF-safe forms for Helvetica."""
    repl = {
        "\u0394": "Delta",
        "\u03b4": "delta",
        "\u2079": "9",
        "\u2081": "1",
        "\u2082": "2",
        "\u2083": "3",
        "\u2084": "4",
        "\u2085": "5",
        "\u2086": "6",
        "\u2087": "7",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u2500": "-",
        "\u2502": "|",
        "\u250c": "+",
        "\u2510": "+",
        "\u2514": "+",
        "\u2518": "+",
        "\u251c": "+",
        "\u2524": "+",
        "\u252c": "+",
        "\u2534": "+",
        "\u253c": "+",
        "\u2550": "=",
        "\u2551": "|",
        "\u2554": "+",
        "\u2557": "+",
        "\u255a": "+",
        "\u255d": "+",
        "\u2560": "+",
        "\u2563": "+",
        "\u2566": "+",
        "\u2569": "+",
        "\u256c": "+",
        "\u25ba": ">",
        "\u2022": "*",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2248": "~",
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u00b7": "*",
        "\u2713": "[ok]",
        "\u2717": "[x]",
        "\u2193": "v",
        "\u2191": "^",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def strip_first_h1(md: str) -> str:
    lines = md.splitlines()
    out = []
    skipped = False
    for line in lines:
        if not skipped and line.startswith("# "):
            skipped = True
            continue
        out.append(line)
    return "\n".join(out).lstrip("\n")


def md_to_html_body(md_text: str) -> str:
    md_text = normalize_unicode(md_text)
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )


def build_html() -> str:
    parts = []
    toc_items = []
    bodies = []

    for title, path in SECTIONS:
        if not path.exists():
            raise FileNotFoundError(path)
        raw = path.read_text(encoding="utf-8")
        body_md = strip_first_h1(raw)
        bodies.append((title, body_md, path))
        toc_items.append(f"<li>{normalize_unicode(title)}</li>")

    cover = f"""
    <h1 class="cover">Janusforge — Memoria completa</h1>
    <p class="meta">
      Copia consolidada para visualizacion (castellano).<br/>
      Incluye Guia Maestra Nivel 0 y documentacion narrativa clave del proyecto.<br/>
      Generado: 2026-08-06 &nbsp;|&nbsp; Repo: janusforge
    </p>
    <h2>Contenido</h2>
    <ol class="toc">
      {''.join(toc_items)}
    </ol>
    <p class="meta">Documento de trabajo interno. Fuentes Markdown originales en <code>docs/</code> y <code>results/reports/</code>.</p>
    """
    parts.append(cover)

    for title, body_md, path in bodies:
        rel = path.relative_to(ROOT).as_posix()
        html_body = md_to_html_body(body_md)
        parts.append(
            f'<div class="section-label">Fuente: {rel}</div>'
            f"<h1>{normalize_unicode(title)}</h1>"
            f"{html_body}"
        )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Janusforge — Memoria completa</title>
<style>{CSS}</style>
</head>
<body>
{''.join(parts)}
</body>
</html>
"""


def main() -> None:
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    html = build_html()
    with open(OUT_PDF, "wb") as out_f:
        result = pisa.CreatePDF(io.BytesIO(html.encode("utf-8")), dest=out_f, encoding="utf-8")
    if result.err:
        raise SystemExit(f"xhtml2pdf reported errors: {result.err}")
    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"OK: {OUT_PDF} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()

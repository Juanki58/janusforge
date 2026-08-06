# -*- coding: utf-8 -*-
"""Build consolidated Janusforge memoria PDF from project markdown docs."""
from __future__ import annotations

import io
import re
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "exports" / "janusforge_memoria_completa.pdf"

SECTIONS = [
    (
        "Guía Maestra Nivel 0 v1.0 — Track 1 (ligando) vs Track 2 (supply)",
        ROOT / "docs" / "guia_maestra_biotecnologia_quimiotipos.md",
    ),
    (
        "Apéndice A — Literatura fibrosis CB1/CB2",
        ROOT / "docs" / "literatura_fibrosis_cb1_cb2.md",
    ),
    (
        "Apéndice B — Quimioma cannábico CB1/CB2",
        ROOT / "docs" / "quimioma_cannabico_cb1_cb2.md",
    ),
    (
        "Apéndice C — Quimiotipos varinas / THCV–THCVA",
        ROOT / "docs" / "quimiotipos_varinas_thcv.md",
    ),
    (
        "Apéndice D — Criterio de éxito Janus",
        ROOT / "docs" / "criterio_exito_janus.md",
    ),
    (
        "Apéndice E — Informe retrospectivo: separación del panel",
        ROOT / "results" / "reports" / "retrospective_panel_separation.md",
    ),
]

CSS = """
@page { size: A4; margin: 1.6cm 1.5cm 1.8cm 1.5cm; }
body {
  font-family: Helvetica, Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.4;
  color: #1a1a1a;
}
h1 {
  font-size: 16pt;
  margin: 0 0 0.5em 0;
  color: #111;
  page-break-after: avoid;
}
h1.cover { font-size: 22pt; margin-top: 2.0cm; }
.section { page-break-before: always; }
.cover-wrap { page-break-before: avoid; }
h2 {
  font-size: 12.5pt;
  margin-top: 1.1em;
  color: #222;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.15em;
  page-break-after: avoid;
}
h3 { font-size: 11pt; margin-top: 0.9em; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin-top: 0.7em; page-break-after: avoid; }
p, li { margin: 0.3em 0; }
ul { margin: 0.3em 0 0.5em 1.2em; }
ol { margin: 0.3em 0 0.5em 1.2em; }
blockquote {
  border-left: 3px solid #666;
  margin: 0.5em 0;
  padding: 0.15em 0.7em;
  color: #333;
  background: #f7f7f7;
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
  font-size: 8pt;
  table-layout: fixed;
}
th, td {
  border: 1px solid #bbb;
  padding: 0.22em 0.3em;
  vertical-align: top;
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
th { background: #eee; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.0em 0; }
.meta { color: #555; font-size: 9.5pt; margin-bottom: 1.2em; }
.toc li { margin: 0.2em 0; }
.section-label {
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 0.4pt;
  color: #666;
  margin: 0 0 0.25em 0;
}
.kv { margin: 0.45em 0 0.7em 0; }
.kv p { margin: 0.25em 0; }
.kv .k { font-weight: bold; }
a { color: #1a1a1a; text-decoration: none; }
"""


def normalize_unicode(text: str) -> str:
    """Map specialty chars to PDF-safe forms for Helvetica / WinAnsi."""
    repl = {
        # Greek / symbols used in the docs
        "\u0394": "Delta",
        "\u03b4": "delta",
        "\u03b1": "alpha",
        "\u03b2": "beta",
        "\u03b3": "gamma",
        "\u03bc": "u",
        "\u00b1": "+/-",
        "\u00d7": "x",
        "\u00b0": " deg",
        "\u00a7": "sec. ",
        # superscripts / subscripts
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
        "\u207a": "+",
        "\u207b": "-",
        "\u207f": "n",
        "\u2080": "0",
        "\u2081": "1",
        "\u2082": "2",
        "\u2083": "3",
        "\u2084": "4",
        "\u2085": "5",
        "\u2086": "6",
        "\u2087": "7",
        "\u2088": "8",
        "\u2089": "9",
        # arrows (keep meaning readable; avoid ^/v inversion)
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u2193": " down ",
        "\u2191": " up ",
        "\u21d2": "=>",
        # dashes / minus / quotes
        "\u2212": "-",  # minus sign (frequent bug: became '?')
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00b7": " | ",  # middle dot: do NOT map to '*' (breaks markdown italics)
        # comparisons
        "\u2248": "~",
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u226a": "<<",
        "\u226b": ">>",
        "\u2243": "~",
        # box drawing
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
        "\u25bc": "v",
        "\u2713": "[ok]",
        "\u2717": "[x]",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    # collapse whitespace introduced by arrow replacements
    text = re.sub(r"[ \t]{2,}", " ", text)
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


def strip_md_attrs(md: str) -> str:
    """Remove Pandoc/MD attribute blocks like {#refs} that leak into PDF."""
    md = re.sub(r"\{#[^}]+\}", "", md)
    md = re.sub(r"\{\.[^}]+\}", "", md)
    return md


def _split_row(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [c.strip() for c in raw.split("|")]


def _is_sep_row(cells: list[str]) -> bool:
    if not cells:
        return False
    # CommonMark allows 2+ dashes; docs use both |---| and |--|
    nonempty = [c for c in cells if c != ""]
    if not nonempty:
        return False
    return all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in nonempty)


def convert_two_col_kv_tables(md: str) -> str:
    """Turn 2-column key/value markdown tables into paragraphs (xhtml2pdf-safe)."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (
            "|" in line
            and i + 1 < len(lines)
            and "|" in lines[i + 1]
            and _is_sep_row(_split_row(lines[i + 1]))
        ):
            header = _split_row(line)
            if len(header) == 2:
                j = i + 2
                rows: list[list[str]] = []
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    cells = _split_row(lines[j])
                    if _is_sep_row(cells):
                        break
                    if len(cells) == 2:
                        rows.append(cells)
                        j += 1
                    else:
                        break
                # Only rewrite if it looks like a KV table (empty/minimal header
                # or bold keys in first column).
                header_empty = all(not c.strip() for c in header)
                keys_bold = rows and all(
                    r[0].startswith("**") and r[0].endswith("**") for r in rows
                )
                if rows and (header_empty or keys_bold):
                    out.append("")
                    for key, val in rows:
                        key_clean = key.strip("* ").strip()
                        out.append(f"**{key_clean}:** {val}")
                        out.append("")
                    i = j
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def simplify_fenced_diagrams(md: str) -> str:
    """Replace box-drawing ASCII diagrams with readable bullet lists when detected."""

    def repl(match: re.Match[str]) -> str:
        body = match.group(1)
        if "CANDIDATO JANUS" in body or "Edición Genética" in body or "Edicion Genetica" in body:
            return (
                "\n**Rutas de obtención del candidato Janus validado:**\n\n"
                "1. Edición genética CRISPR/Cas9 (knockout de olivetol sintasa)\n"
                "2. Biología sintética / fermentación en levaduras (S. cerevisiae)\n"
                "3. Síntesis orgánica / derivación semi-sintética (hipótesis H1-H5)\n"
            )
        # Generic: keep as indented preformatted text without fences if short
        return match.group(0)

    return re.sub(r"```(?:text|ascii|)?\n(.*?)```", repl, md, flags=re.DOTALL)


def preprocess_md(md_text: str) -> str:
    md_text = strip_md_attrs(md_text)
    md_text = convert_two_col_kv_tables(md_text)
    md_text = simplify_fenced_diagrams(md_text)
    # Soften markdown links: keep label; add path only when it differs
    def _link_repl(m: re.Match[str]) -> str:
        label, href = m.group(1), m.group(2)
        label_plain = label.replace("`", "").strip()
        if href.startswith(("http://", "https://", "mailto:")):
            return f"{label_plain} ({href})"
        href_name = href.rstrip("/").split("/")[-1]
        if (
            label_plain == href
            or label_plain == href_name
            or label_plain.endswith(href_name)
            or href.endswith(label_plain)
        ):
            return label_plain
        return f"{label_plain} ({href})"

    md_text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, md_text)
    return md_text


def md_to_html_body(md_text: str) -> str:
    md_text = preprocess_md(md_text)
    md_text = normalize_unicode(md_text)
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )


def build_html() -> str:
    toc_items = []
    bodies = []

    for title, path in SECTIONS:
        if not path.exists():
            raise FileNotFoundError(path)
        raw = path.read_text(encoding="utf-8")
        body_md = strip_first_h1(raw)
        bodies.append((title, body_md, path))
        toc_items.append(f"<li>{normalize_unicode(title)}</li>")

    cover = normalize_unicode(
        """
    <div class="cover-wrap">
    <h1 class="cover">Janusforge - Memoria completa</h1>
    <p class="meta">
      Copia consolidada para visualización (castellano).<br/>
      Incluye Guía Maestra Nivel 0 y documentación narrativa clave del proyecto.<br/>
      Generado: 2026-08-06 &nbsp;|&nbsp; Repo: janusforge
    </p>
    <h2>Contenido</h2>
    <ol class="toc">
      __TOC__
    </ol>
    <p class="meta">Documento de trabajo interno. Fuentes Markdown originales en <code>docs/</code> y <code>results/reports/</code>.</p>
    </div>
    """
    ).replace("__TOC__", "".join(toc_items))

    parts = [cover]
    for title, body_md, path in bodies:
        rel = path.relative_to(ROOT).as_posix()
        html_body = md_to_html_body(body_md)
        parts.append(
            f'<div class="section">'
            f'<div class="section-label">Fuente: {rel}</div>'
            f"<h1>{normalize_unicode(title)}</h1>"
            f"{html_body}"
            f"</div>"
        )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Janusforge - Memoria completa</title>
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

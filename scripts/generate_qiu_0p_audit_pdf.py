# -*- coding: utf-8 -*-
"""Generate Spanish A4 PDF of Qiu 0P state-of-art audit from markdown."""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(r"C:\Users\juanc\projects\janusforge")
SRC = ROOT / "results" / "reports" / "qiu_0p_state_of_art_audit.md"
OUT = ROOT / "results" / "reports" / "qiu_0p_state_of_art_audit.pdf"
PAGE = A4

NAVY = HexColor("#1a365d")
TEAL = HexColor("#0d7377")
LIGHT = HexColor("#f0f4f8")
BORDER = HexColor("#cbd5e0")
MUTED = HexColor("#4a5568")
WARN = HexColor("#c05621")
SOFT = HexColor("#fffaf0")
MINT = HexColor("#e6fffa")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r'<font face="Courier" size="7.5">\1</font>', s)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<link href="\2" color="#0d7377"><u>\1</u></link>',
        s,
    )
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", s)
    # emoji status markers kept as text
    return s


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="H1",
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=TEAL,
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="H3",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
        spaceBefore=6,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyBullet",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=black,
        leftIndent=10,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Cell",
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=black,
    )
)
styles.add(
    ParagraphStyle(
        name="CellHead",
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=white,
    )
)
styles.add(
    ParagraphStyle(
        name="Meta",
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=MUTED,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=NAVY,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Quote",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10.5,
        textColor=MUTED,
        leftIndent=6,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CodeBlock",
        fontName="Courier",
        fontSize=7,
        leading=9,
        textColor=NAVY,
        backColor=LIGHT,
        leftIndent=4,
        rightIndent=4,
        spaceBefore=4,
        spaceAfter=6,
    )
)


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = PAGE
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 11 * mm, w, 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(14 * mm, h - 7 * mm, "Janusforge — Qiu 0P · Auditoría del estado del arte")
    canvas.setFont("Helvetica", 6.5)
    canvas.drawRightString(w - 14 * mm, h - 7 * mm, "Solo investigación · No consejo médico/legal")
    canvas.setFillColor(BORDER)
    canvas.rect(0, 0, w, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(
        14 * mm,
        3.5 * mm,
        "2026-08-13 · Capas: PUBLICADO · REPO · INFERENCIA · NOT FOUND · BLOCKED",
    )
    canvas.drawRightString(w - 14 * mm, 3.5 * mm, f"Pág. {doc.page}")
    canvas.restoreState()


def make_table(headers, rows, usable_w: float):
    n = max(len(headers), 1)
    # heuristic widths: first col narrower if many cols
    if n == 2:
        widths = [usable_w * 0.32, usable_w * 0.68]
    elif n == 3:
        widths = [usable_w * 0.28, usable_w * 0.42, usable_w * 0.30]
    elif n == 4:
        widths = [usable_w * 0.22, usable_w * 0.28, usable_w * 0.25, usable_w * 0.25]
    else:
        widths = [usable_w / n] * n

    data = [[Paragraph(md_inline(h), styles["CellHead"]) for h in headers]]
    for row in rows:
        # pad/truncate to header length
        cells = list(row) + [""] * (n - len(row))
        data.append([Paragraph(md_inline(c), styles["Cell"]) for c in cells[:n]])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ]
        )
    )
    return t


def box(text: str, bg, border, usable_w: float):
    p = Paragraph(md_inline(text), styles["Callout"])
    t = Table([[p]], colWidths=[usable_w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 1.0, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def split_table_row(line: str) -> list[str]:
    raw = line.strip().strip("|")
    return [c.strip() for c in raw.split("|")]


def is_sep_row(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells if c)


def parse_md(text: str):
    """Yield structured blocks from markdown."""
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # closing fence
            yield ("code", "\n".join(buf), lang)
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = split_table_row(lines[i])
                if not is_sep_row(cells):
                    rows.append(cells)
                i += 1
            if rows:
                headers = rows[0]
                body = rows[1:]
                yield ("table", headers, body)
            continue

        if stripped.startswith("> "):
            buf = [stripped[2:]]
            i += 1
            while i < n and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:])
                i += 1
            yield ("quote", " ".join(buf))
            continue

        if stripped.startswith("---") and set(stripped) <= {"-", " "}:
            yield ("hr",)
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if m:
            level = len(m.group(1))
            yield ("h", level, m.group(2).strip())
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                # gather continuation lines (indented or blank-then-indent)
                i += 1
                while i < n:
                    cont = lines[i]
                    if not cont.strip():
                        # peek next
                        if i + 1 < n and (
                            lines[i + 1].startswith("   ")
                            or lines[i + 1].startswith("\t")
                        ):
                            i += 1
                            continue
                        break
                    if cont.startswith("   ") or cont.startswith("\t"):
                        item += " " + cont.strip()
                        i += 1
                        continue
                    break
                items.append(item)
            yield ("ol", items)
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < n and (
                lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")
            ):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            yield ("ul", items)
            continue

        # paragraph: merge until blank / structural
        buf = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt:
                break
            if nxt.startswith("#") or nxt.startswith("|") or nxt.startswith(">") or nxt.startswith("```") or nxt.startswith("---") or re.match(r"^\d+\.\s+", nxt) or nxt.startswith("- ") or nxt.startswith("* "):
                break
            buf.append(nxt)
            i += 1
        yield ("p", " ".join(buf))


def build_story():
    md = SRC.read_text(encoding="utf-8")
    story = []
    usable_w = PAGE[0] - 28 * mm

    # Cover
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("Janusforge", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Qiu 0P — Auditoría del estado del arte<br/>(pasada exhaustiva documental)",
            ParagraphStyle("CT2", parent=styles["CoverTitle"], fontSize=13.5, leading=17),
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        HRFlowable(
            width="55%",
            thickness=1.4,
            color=TEAL,
            spaceBefore=2,
            spaceAfter=8,
            hAlign="CENTER",
        )
    )
    story.append(
        Paragraph(
            "Investigación + auditoría solo · Sin docking nuevo, MD, NCE ni ensayos",
            styles["CoverSub"],
        )
    )
    story.append(
        Paragraph(
            "Fecha: 2026-08-13 · Idioma: Español · Formato A4 · Origen: qiu_0p_state_of_art_audit.md",
            styles["CoverSub"],
        )
    )
    story.append(Spacer(1, 5 * mm))

    story.append(
        make_table(
            ["Campo", "Valor"],
            [
                [
                    "Naturaleza",
                    "Auditoría documental del **estado del arte** (Qiu 0P) tras pasada exhaustiva de retrieval",
                ],
                [
                    "No es",
                    "FTO · dictamen de patentabilidad · consejo médico/legal · claim de fármaco",
                ],
                [
                    "Capas epistémicas",
                    "**PUBLICADO** · **REPO** · **INFERENCIA** · **NOT FOUND** · **BLOCKED**",
                ],
                [
                    "Política",
                    "Ahorrar gasto; **no inventar** potencias Ki/IC₅₀/EC₅₀",
                ],
            ],
            usable_w,
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        box(
            "**Nota de portada — anexos relacionados:** "
            "`results/reports/qiu_0p_exhaustiveness_check.md` (checklist de exhaustividad de fuentes) · "
            "`results/reports/qiu_0p_compound_landscape.csv` (paisaje tabular de compuestos / gaps honestos). "
            "Este PDF reproduce las conclusiones científicas del markdown fuente **sin alterarlas**.",
            MINT,
            TEAL,
            usable_w,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        box(
            "**Aviso:** El PDF principal de Qiu sigue **BLOCKED** en vías públicas; "
            "las tablas numéricas de Ki/IC₅₀/EC₅₀ de 14/15/20/24 permanecen **NOT FOUND**. "
            "H1-a discovery = **SKIP**; ancla operativa = **CONDICIONAL**.",
            SOFT,
            WARN,
            usable_w,
        )
    )
    story.append(PageBreak())

    for block in parse_md(md):
        kind = block[0]
        if kind == "h":
            level, title = block[1], block[2]
            # Skip duplicate top title on body (already on cover)
            if level == 1 and title.startswith("Qiu 0P"):
                continue
            style = {1: "H1", 2: "H2", 3: "H3"}[level]
            story.append(Paragraph(md_inline(title), styles[style]))
        elif kind == "p":
            story.append(Paragraph(md_inline(block[1]), styles["Body"]))
        elif kind == "quote":
            story.append(Paragraph(md_inline(block[1]), styles["Quote"]))
        elif kind == "hr":
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=BORDER,
                    spaceBefore=4,
                    spaceAfter=4,
                )
            )
        elif kind == "table":
            headers, rows = block[1], block[2]
            story.append(Spacer(1, 2 * mm))
            story.append(make_table(headers, rows, usable_w))
            story.append(Spacer(1, 2 * mm))
        elif kind == "ul":
            for item in block[1]:
                story.append(Paragraph(md_inline(f"• {item}"), styles["BodyBullet"]))
        elif kind == "ol":
            for idx, item in enumerate(block[1], 1):
                story.append(Paragraph(md_inline(f"**{idx}.** {item}"), styles["BodyBullet"]))
        elif kind == "code":
            code = block[1]
            # keep as preformatted block in a tinted table
            p = Preformatted(code, styles["CodeBlock"])
            t = Table([[p]], colWidths=[usable_w])
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(Spacer(1, 2 * mm))
            story.append(t)
            story.append(Spacer(1, 2 * mm))

    story.append(Spacer(1, 5 * mm))
    story.append(
        box(
            "**Cierre PDF:** Documento generado desde `qiu_0p_state_of_art_audit.md` con reportlab "
            "(mismo enfoque tipográfico que `janusforge_dossier_estado_programa.pdf`). "
            "Conclusiones científicas intactas.",
            MINT,
            TEAL,
            usable_w,
        )
    )
    return story


def main():
    if not SRC.is_file():
        raise SystemExit(f"Source missing: {SRC}")

    story = build_story()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=15 * mm,
        bottomMargin=12 * mm,
        title="Janusforge — Qiu 0P Auditoría del estado del arte",
        author="Janusforge R&D",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    size = OUT.stat().st_size
    n_pages = "?"
    try:
        from pypdf import PdfReader

        n_pages = len(PdfReader(str(OUT)).pages)
    except Exception:
        try:
            from PyPDF2 import PdfReader

            n_pages = len(PdfReader(str(OUT)).pages)
        except Exception:
            pass

    print(f"PDF written: {OUT}")
    print(f"Size bytes: {size}")
    print(f"Pages: {n_pages}")
    print(f"Page size: A4 portrait {PAGE[0]:.1f} x {PAGE[1]:.1f} pt")
    if size < 1000:
        raise SystemExit("PDF too small / empty")


if __name__ == "__main__":
    main()

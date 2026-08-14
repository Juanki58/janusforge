# -*- coding: utf-8 -*-
"""Generate wide landscape PDF dossier for Janusforge collaborators."""
from pathlib import Path
import re

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

OUT = Path(r"C:\Users\juanc\projects\janusforge\results\reports\janusforge_dossier_estado_programa.pdf")
PAGE = landscape(A4)

NAVY = HexColor("#1a365d")
TEAL = HexColor("#0d7377")
LIGHT = HexColor("#f0f4f8")
BORDER = HexColor("#cbd5e0")
MUTED = HexColor("#4a5568")
WARN = HexColor("#c05621")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8">\1</font>', s)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<link href="\2" color="#0d7377"><u>\1</u></link>',
        s,
    )
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    return s


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="H1",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=TEAL,
        spaceBefore=10,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyBullet",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=black,
        leftIndent=12,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Cell",
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=black,
    )
)
styles.add(
    ParagraphStyle(
        name="CellHead",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=white,
    )
)
styles.add(
    ParagraphStyle(
        name="Meta",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=NAVY,
        spaceAfter=4,
    )
)


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = PAGE
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(15 * mm, h - 7.5 * mm, "Janusforge — Dossier de estado del programa")
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(w - 15 * mm, h - 7.5 * mm, "Investigación · No consejo médico/legal")
    canvas.setFillColor(BORDER)
    canvas.rect(0, 0, w, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(
        15 * mm,
        4 * mm,
        "2026-08-13 · Uso colaboradores/asesores · Capas: Literatura | Cómputo | Hipótesis | Producto futuro",
    )
    canvas.drawRightString(w - 15 * mm, 4 * mm, f"Pág. {doc.page}")
    canvas.restoreState()


def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(md_inline(h), styles["CellHead"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(md_inline(c), styles["Cell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def box(text, bg, border):
    p = Paragraph(md_inline(text), styles["Callout"])
    t = Table([[p]], colWidths=[PAGE[0] - 40 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 1.2, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def main():
    story = []
    usable_w = PAGE[0] - 30 * mm

    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph("Janusforge", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Dossier de estado del programa<br/>(resumen ejecutivo ampliado)",
            ParagraphStyle(
                "CT2", parent=styles["CoverTitle"], fontSize=16, leading=20
            ),
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        HRFlowable(
            width="60%",
            thickness=1.5,
            color=TEAL,
            spaceBefore=2,
            spaceAfter=8,
            hAlign="CENTER",
        )
    )
    story.append(
        Paragraph(
            "Visión terapéutica · Trabajo computacional y planificación · Estado operativo y próximos pasos",
            styles["CoverSub"],
        )
    )
    story.append(
        Paragraph(
            "Fecha: 2026-08-13 · Idioma: Español · Formato apaisado (A4 landscape)",
            styles["CoverSub"],
        )
    )
    story.append(Spacer(1, 6 * mm))

    story.append(
        make_table(
            ["Campo", "Valor"],
            [
                [
                    "Naturaleza",
                    "Documento de **estado de programa de investigación** (colaboradores / asesores)",
                ],
                [
                    "No es",
                    "Consejo médico · consejo legal · FTO · dictamen de patentabilidad · claim de fármaco",
                ],
                ["Confidencialidad", "Sin SMILES de NCE propietarias no publicadas"],
                [
                    "Capas epistémicas",
                    "**Literatura** | **Observación computacional** | **Hipótesis** | **Producto futuro**",
                ],
            ],
            col_widths=[45 * mm, usable_w - 45 * mm],
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(
        box(
            "**Aviso de honestidad científica:** El docking **no** demuestra eficacia clínica. "
            "**Qiu-14** es vehículo de validación **publicado**, no invención Janusforge. "
            "Los scores Vina son **solo computacionales**. Este documento no afirma que Janusforge ya tenga un fármaco.",
            HexColor("#fffaf0"),
            WARN,
        )
    )
    story.append(PageBreak())

    # 1
    story.append(Paragraph("1. ¿Qué producto queremos?", styles["H1"]))
    story.append(
        Paragraph(
            md_inline(
                "**Visión terapéutica (producto futuro, no logrado aún):** un ligando (o familia) con perfil "
                "**Janus / Yin–Yang**: **CB1 antagonista** (bloqueo / no-agonismo limpio) y **CB2 agonista**, "
                "pensado como candidato de descubrimiento para **fibrosis orgánica**, con **fibrosis pulmonar "
                "idiopática (IPF)** como indicación prioritaria de motivación."
            ),
            styles["Body"],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "No se busca “cualquier cannabinoide”, ni maximizar afinidad indiferenciada, ni reclamar un fármaco listo. "
                "El norte farmacológico es el **perfil dual de receptores**; la fibrosis es el para qué clínico."
            ),
            styles["Body"],
        )
    )
    story.append(
        make_table(
            ["Track", "Rol", "Prioridad"],
            [
                [
                    "**Track 1 — Drug discovery**",
                    "Scaffold sintético Janus (URB447 / Yin–Yang tipo Qiu; H1–H5 THCV-like = contraste cerrado)",
                    "**#1**",
                ],
                ["**Track 2 — Supply**", "Estándares, controles, biomasa si aplica", "Secundario"],
            ],
            col_widths=[55 * mm, usable_w - 80 * mm, 25 * mm],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "Fuentes: `docs/guia_maestra_biotecnologia_quimiotipos.md`, `docs/literatura_fibrosis_cb1_cb2.md`, "
                "`docs/mapa_ligandos_janus_cb1_cb2.md`."
            ),
            styles["Meta"],
        )
    )

    # 2
    story.append(Paragraph("2. ¿Por qué importa para la salud?", styles["H1"]))
    story.append(
        Paragraph(
            md_inline(
                "(Nivel literatura — motivación biológica; **no** es claim de cura ni de fármaco Janusforge.)"
            ),
            styles["Meta"],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "La **fibrosis** es acumulación patológica de matriz extracelular; la **IPF** es una enfermedad "
                "pulmonar progresiva con necesidad médica alta: los antifibróticos aprobados ralentizan, pero no "
                "detienen ni revierten el daño establecido."
            ),
            styles["Body"],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "En el sistema endocannabinoide, la literatura asocia con frecuencia **CB1** con un brazo a menudo "
                "**profibrótico / proinflamatorio** (p. ej. evidencia en IPF humana y modelos bleomicina; "
                "Cinar et al., JCI Insight 2017) y **CB2** con un brazo a menudo **antiinflamatorio / antifibrótico**."
            ),
            styles["Body"],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "En fibrosis renal experimental, la **combinación** CB1-ant + CB2-ago ha mostrado efectos superiores "
                "a cada brazo por separado — motiva la hipótesis de un **único ligando Janus**, sin confundir eso "
                "con una demostración ya hecha."
            ),
            styles["Body"],
        )
    )
    story.append(
        box(
            "**Hueco real:** racional CB1↓ / CB2↑ sólido a nivel de brazos separados o combos; "
            "**no** hay aquí demostración antifibrótica monomolecular equivalente con URB447, GW405833, "
            "AM1710 o Qiu-14. Qiu 2023 plantea potencial Yin–Yang como hipótesis, no como ensayo IPF del compuesto 14.",
            HexColor("#e6fffa"),
            TEAL,
        )
    )

    # 3
    story.append(Paragraph("3. Qué hemos hecho (timeline operativo)", styles["H1"]))
    story.append(Paragraph("3.1 Contexto previo (cerrado / contraste)", styles["H2"]))
    story.append(
        Paragraph(
            md_inline(
                "• Hipótesis **H1–H5** THCV-like exploradas in silico; **NO-GO** de membrana MD → pivot a eje sintético (Opción D / URB447 / Yin–Yang)."
            ),
            styles["BodyBullet"],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "• Lead histórico **JANUS_D2_22**: Vina favorable, pero MD CB1 20 ns + **feature_swap** lo sacan del brazo positivo. "
                "**No** se prioriza por Vina más negativo."
            ),
            styles["BodyBullet"],
        )
    )

    story.append(Paragraph("3.2 Cadena Qiu 0D → 0J (cómputo + QC)", styles["H2"]))
    story.append(
        make_table(
            ["Hito", "Qué hizo", "Veredicto"],
            [
                ["**0D**", "Verificación estructural 2D Qiu 14/15/20/24", "PASS 4/4"],
                ["**0E**", "Preparación PDBQT + auditoría", "PASS 4/4"],
                [
                    "**0F**",
                    "Docking CB2 (6PT0), Vina 1.2.7, protocolo bloqueado",
                    "PASS 4/4 (obs. log↔PDBQT 15/20)",
                ],
                ["**0G**", "Geometría de poses + comparación D1 / farmacóforo", "PASS / COMPLETE"],
                ["**0H / 0I**", "Auditoría + matriz de evidencia", "PASS WITH OBSERVATIONS"],
                ["**0J**", "QC visual; STOP/PIVOT (sin nuevo docking/MD/SAR)", "Vigente"],
            ],
            col_widths=[28 * mm, usable_w - 78 * mm, 50 * mm],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "Integración 0D–0G: **PASS WITH OBSERVATIONS**. Matriz 0I **no** autoriza SAR ni convierte Vina en potencia. "
                "Scores Vina CB2 (ej.): Qiu-14 ≈ −9.9 — **solo computacionales**, ≠ ranking farmacológico."
            ),
            styles["Body"],
        )
    )

    story.append(Paragraph("3.3 Planificación y gates (2026-08-12)", styles["H2"]))
    story.append(
        make_table(
            ["Hito", "Estado"],
            [
                ["**0K**", "Plan H1/H2 **cerrado** (CB2-first; umbrales numéricos TBD)"],
                ["**0IP**", "Landscape novelty **borrador — necesita counsel** (no clearance)"],
                ["**0L**", "Spec experimental H1-a **cerrada**; wet no iniciado"],
                ["**0M**", "Handoff wet **BLOCKED** hasta TBDs pre-estudio"],
                ["**Paquete CRO H1-a**", "Índice + carpeta `SEND/` lista para RFQs comparables"],
                [
                    "**0N**",
                    "Cómputo opcional estilo Ge 2023: **NOT READY** (congelado; no ruta crítica)",
                ],
            ],
            col_widths=[45 * mm, usable_w - 45 * mm],
        )
    )

    story.append(Paragraph("3.4 Organigrama vigente", styles["H2"]))
    story.append(
        Paragraph(
            md_inline(
                "<font face='Courier' size='7.5'>"
                "0D–0J → 0K → 0IP → 0L → 0M/CRO → <b>WET H1-a</b> (ruta crítica) → H1-b → H2 → H3 gated<br/>"
                "→ NCE (solo blue-ocean) → IP GATE / counsel → síntesis NCE propia<br/>"
                "0N paralelo opcional — NOT READY; no sustituye H1-a"
                "</font>"
            ),
            styles["Body"],
        )
    )

    story.append(PageBreak())

    # 4
    story.append(Paragraph("4. Qué está demostrado vs no demostrado", styles["H1"]))
    story.append(
        make_table(
            ["Afirmación", "Estado", "Capa"],
            [
                ["Identidad 2D Qiu 14/15/20/24 verificada", "**Demostrado (QC)**", "Cómputo"],
                ["Pipeline PDBQT + docking CB2 con QC trazable", "**Demostrado (QC)**", "Cómputo"],
                [
                    "Poses Qiu en región ortostérica-like CB2 (geometría)",
                    "**Demostrado (geometría)**",
                    "Cómputo",
                ],
                ["D2_20/06 mayor overlap vs Qiu; D2_22 feature_swap", "**Observado**", "Cómputo"],
                ["Scores Vina como números del motor", "**Observados**", "Cómputo"],
                ["Vina = afinidad / Ki / potencia / ranking", "**No demostrado**", "—"],
                ["Qiu-14 reproduce Janus en panel Janusforge", "**No demostrado** (H1)", "Hipótesis"],
                ["D2_20/06 son agonistas CB2 o Janus", "**No demostrado** (H2/H3)", "Hipótesis"],
                ["Un ligando Janus monomolecular trata IPF", "**No demostrado**", "—"],
                ["Janusforge posee un fármaco / NCE clínica", "**No aplica / falso**", "—"],
                ["Qiu-14 es invención Janusforge", "**Falso** (prior art publicado)", "Literatura"],
                ["Landscape 0IP = FTO / patentabilidad", "**No** (borrador interno)", "—"],
            ],
            col_widths=[usable_w * 0.52, usable_w * 0.28, usable_w * 0.20],
        )
    )

    # 5
    story.append(Paragraph("5. Vehículo Qiu-14 vs futura NCE + IP gate", styles["H1"]))
    story.append(Paragraph("5.1 Qiu-14 (publicado)", styles["H2"]))
    story.append(
        Paragraph(
            md_inline(
                "• **Rol:** ancla / control positivo literario para calibrar el panel (H1).<br/>"
                "• **No es** NCE Janusforge, inventorship ni producto final.<br/>"
                "• **Química (publicada):** pirazol-3-carboxamida con o-morfolinofenilo + CONH–1-adamantilo (Qiu et al. 2023).<br/>"
                "• **Literatura:** CB1-ant + CB2-ago; hipótesis S173/S285. Ki/IC₅₀ de tabla experimental "
                "**no recuperados en repo** — no se inventan como umbrales PASS.<br/>"
                "• Copias directas = **prior art** (zona roja 2 del landscape)."
            ),
            styles["Body"],
        )
    )

    story.append(Paragraph("5.2 Futura NCE propia", styles["H2"]))
    story.append(
        Paragraph(
            md_inline(
                "Solo **después** de validación húmeda H1/H2 y **dentro** de hipótesis de espacio blanco documentadas, "
                "con revisión de patentabilidad/FTO con **counsel**, decisión de filing, y **sin** SMILES propietarios "
                "en documentos públicos hasta autorización."
            ),
            styles["Body"],
        )
    )

    story.append(Paragraph("5.3 Tres momentos IP", styles["H2"]))
    story.append(
        make_table(
            ["Momento", "Significado"],
            [
                ["**1**", "Controles / cómputo (0D–0J + Qiu publicado) = calibración científica"],
                [
                    "**2**",
                    "Ventana de invención = NCE propia + datos CB1/CB2 experimentales + SAR defendible",
                ],
                [
                    "**3**",
                    "Gate de divulgación = counsel **antes** de cualquier divulgación pública de NCE",
                ],
            ],
            col_widths=[28 * mm, usable_w - 28 * mm],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "Landscape (borrador): presión Makriyannis/Vemuri, Qiu 2023, Sanofi/rimonabant; ideas blue-ocean = "
                "hipótesis, **no clearance**. Fuentes: `docs/ip_gate_janusforge.md`, `results/reports/qiu_0ip_novelty_landscape.md`."
            ),
            styles["Meta"],
        )
    )

    # 6
    story.append(Paragraph("6. Plan de validación experimental H1/H2", styles["H1"]))
    story.append(
        Paragraph(
            md_inline(
                "**Estado:** plan **cerrado** en 0K; **ningún ensayo húmedo ejecutado**. "
                "Direcciones de signo fijadas; **magnitudes PASS/KILL = TBD**."
            ),
            styles["Body"],
        )
    )
    story.append(
        make_table(
            ["Hipótesis", "Material", "Orden", "Endpoint (dirección)", "Siguiente"],
            [
                ["**H1-a**", "Qiu-14", "CB2 primero", "Agonismo funcional hCB2", "PASS→H1-b; KILL→stop ancla"],
                ["**H1-b**", "Qiu-14", "Tras H1-a PASS", "Antagonismo / control CB1", "PASS→ancla H1; luego H2"],
                [
                    "**H2-a**",
                    "D2_20 y/o D2_06",
                    "CB2 primero",
                    "Agonismo CB2",
                    "Transfiere o mata overlap→act.",
                ],
                ["**H2-b**", "Mismo D2", "Opcional", "CB1", "Informativo hacia H3"],
                [
                    "**H3**",
                    "D2 vs Qiu-14",
                    "Solo si H1+H2 PASS",
                    "Signo Janus dual",
                    "Transferencia (sin fibrosis aún)",
                ],
            ],
            col_widths=[22 * mm, 35 * mm, 32 * mm, 55 * mm, usable_w - 144 * mm],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "**Fuera del plan:** H4 (SAR Qiu regio), H5 (fibrosis). **D2_22** fuera del brazo positivo. "
                "**No constituyen PASS:** Vina, overlap, Jaccard, MD D2_22, ni literatura como sustituto de re-ensayo."
            ),
            styles["Body"],
        )
    )

    story.append(PageBreak())

    # 7
    story.append(Paragraph("7. Estado operativo (bloqueos actuales)", styles["H1"]))
    story.append(
        make_table(
            ["Ítem", "Estado", "Comentario"],
            [
                ["Cómputo 0D–0J", "**Cerrado**", "STOP/PIVOT: no más docking/MD/SAR como siguiente paso"],
                ["Spec H1-a (0L)", "**Cerrada**", "Lista para rellenar TBD pre-lab"],
                ["Handoff wet (0M)", "**BLOCKED**", "Paquete listo; wet no arranca"],
                ["Paquete CRO", "**Listo para envío**", "`cro_package_h1a/SEND/` — RFQs comparables"],
                ["Material Qiu-14", "**TBD-11**", "Compra / síntesis contrato / autores — pendiente"],
                ["Criterio PASS H1-a", "**TBD-05**", "Debe firmarlo el PI **antes** del primer run"],
                ["Formato ensayo / células", "TBD-01, TBD-02…", "Ver registro 0M §7"],
                ["0N (Ge 2023–style)", "**NOT READY**", "SI ACS bloqueada; no es gate; no sustituye CRO"],
                ["NCE propietaria", "**No iniciada** (correcto)", "Tras wet + IP gate"],
            ],
            col_widths=[45 * mm, 40 * mm, usable_w - 85 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        box(
            "**Bloqueos duros antes del primer wet H1-a:** sistema celular; formato funcional; **TBD-05 firmado**; "
            "ventana de concentraciones; controles/Z′; pureza/COA Qiu-14; material en mano; CRO vs in-house + SOP; "
            "plan de réplicas y análisis. **Política de fase:** retorno en síntesis + ensayo + cotizaciones CRO, no en más cómputo.",
            HexColor("#fffaf0"),
            WARN,
        )
    )

    # 8
    story.append(Paragraph("8. Próximos pasos recomendados", styles["H1"]))
    steps = [
        "**Enviar** el set idéntico `results/reports/cro_package_h1a/SEND/` a 2–3 CROs (cover + RFQ síntesis + RFQ ensayo CB2 + nota NDA/IP).",
        "**Cerrar presupuesto** y elegir vía (bundle o separados).",
        "**Asegurar Qiu-14** (TBD-11) con identidad vs ancla 0D y COA (TBD-10).",
        "**Cerrar TBDs pre-estudio** con PI + CRO — especialmente **TBD-05** — y actualizar 0M solo cuando el gate esté checked.",
        "**Ejecutar H1-a** (único gate húmedo inmediato).",
        "Según resultado: plan **H1-b** o stop/pivot (0K §7). **No** saltar a NCE.",
        "**0N:** solo si se obtiene SI ACS y autorización explícita; permanece opcional.",
        "Tras H1/H2 PASS (si aplica): NCE en hipótesis blue-ocean + **IP REVIEW con counsel** antes de divulgación o síntesis propietaria.",
    ]
    for i, s in enumerate(steps, 1):
        story.append(Paragraph(md_inline(f"**{i}.** {s}"), styles["BodyBullet"]))

    # 9
    story.append(Paragraph("9. Anexos — rutas de informes clave", styles["H1"]))
    story.append(Paragraph("9.1 Norma / visión", styles["H2"]))
    story.append(
        make_table(
            ["Documento", "Ruta"],
            [
                ["Guía maestra (tracks)", "`docs/guia_maestra_biotecnologia_quimiotipos.md`"],
                ["Literatura fibrosis CB1/CB2", "`docs/literatura_fibrosis_cb1_cb2.md`"],
                ["Mapa ligandos Janus", "`docs/mapa_ligandos_janus_cb1_cb2.md`"],
                ["IP gate (protocolo)", "`docs/ip_gate_janusforge.md`"],
            ],
            col_widths=[55 * mm, usable_w - 55 * mm],
        )
    )
    story.append(Paragraph("9.2 Cómputo / planificación / CRO", styles["H2"]))
    story.append(
        make_table(
            ["Documento", "Ruta"],
            [
                ["Integración QC 0D–0G", "`results/reports/qiu_0d_0g_integration_qc.md`"],
                ["Matriz evidencia 0I", "`results/reports/qiu_0i_evidence_matrix.md`"],
                ["Plan H1/H2 (0K)", "`results/reports/qiu_0k_validation_plan_h1_h2.md`"],
                ["Spec H1-a (0L)", "`results/reports/qiu_0l_h1a_experimental_spec.md`"],
                ["Handoff wet (0M)", "`results/reports/qiu_0m_h1a_wet_handoff.md`"],
                ["Landscape IP (0IP)", "`results/reports/qiu_0ip_novelty_landscape.md`"],
                ["Estado 0N", "`results/reports/qiu_0n_status.md`"],
                ["Índice paquete CRO", "`results/reports/cro_package_h1a/00_index.md`"],
                ["Carpeta SEND (RFQs)", "`results/reports/cro_package_h1a/SEND/`"],
            ],
            col_widths=[55 * mm, usable_w - 55 * mm],
        )
    )
    story.append(
        Paragraph(
            md_inline(
                "Precedente literario: Qiu et al., Bioorg. Chem. 2023; DOI: https://doi.org/10.1016/j.bioorg.2023.106377"
            ),
            styles["Meta"],
        )
    )

    story.append(Spacer(1, 6 * mm))
    story.append(
        box(
            "**Cierre:** Janusforge tiene **visión clara** (Janus CB1↓/CB2↑ para fibrosis/IPF), "
            "**cómputo y planificación trazables** hasta un handoff H1-a listo en papel, y está "
            "**bloqueado operativamente** en material Qiu-14, criterios TBD (esp. TBD-05) y ejecución CRO — "
            "con **0N congelado** y **IP gate** obligatorio antes de cualquier NCE propietaria. "
            "No es consejo médico ni legal.",
            HexColor("#e6fffa"),
            TEAL,
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        title="Janusforge — Dossier de estado del programa",
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
    print(f"Page size: A4 landscape {PAGE[0]:.1f} x {PAGE[1]:.1f} pt")
    if size < 1000:
        raise SystemExit("PDF too small / empty")


if __name__ == "__main__":
    main()

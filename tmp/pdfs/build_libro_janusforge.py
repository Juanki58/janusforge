from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "janusforge_libro_borrador_con_estructura.pdf"
STRUCTURE_IMAGE = Path(r"C:\Users\juanc\AppData\Local\Temp\codex-clipboard-f2e1d663-9dcf-4086-8584-7394c5096266.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="BookTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=29, leading=35, alignment=TA_CENTER, textColor=colors.HexColor("#17324D"),
    spaceAfter=20,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=14, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#45627A"),
))
styles.add(ParagraphStyle(
    name="Chapter", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=20, leading=25, textColor=colors.HexColor("#17324D"), spaceAfter=16,
))
styles.add(ParagraphStyle(
    name="BodyBook", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=10.7, leading=16.2, alignment=TA_JUSTIFY, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="Quote", parent=styles["BodyText"], fontName="Helvetica-Oblique",
    fontSize=12, leading=18, alignment=TA_JUSTIFY, leftIndent=18, rightIndent=18,
    textColor=colors.HexColor("#35566F"), spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5,
    leading=11, textColor=colors.HexColor("#526B7F"),
))

chapters = [
    ("1. La pregunta Janus", [
        "Janusforge nace de una pregunta farmacológica concreta: si la biología de CB1 y CB2 apunta en direcciones distintas en procesos fibróticos, ¿podría un solo ligando modular ambos brazos de forma útil? La formulación es deliberadamente exigente. No se busca cualquier molécula cannabinoide, ni una afinidad alta sin contexto. Se busca evitar agonismo CB1 no deseado y sostener una dirección agonista en CB2.",
        "La fibrosis, y en particular la fibrosis pulmonar idiopática como motivación prioritaria, proporciona el problema clínico. Sin embargo, el proyecto no afirma que una molécula de Janusforge haya demostrado eficacia antifibrótica. El propósito clínico y el criterio de receptor son capas diferentes: primero se necesita un perfil farmacológico defendible; después podrá preguntarse si ese perfil se traduce en un beneficio en modelos de enfermedad.",
        "Esta distinción es el primer activo del programa. Evita que una narrativa terapéutica atractiva transforme resultados computacionales iniciales en promesas clínicas. El libro cuenta una exploración que todavía está antes del ensayo funcional, pero que ha sido diseñada para llegar a él con preguntas claras y decisiones auditables."
    ]),
    ("2. Dos tracks para no perder el foco", [
        "La documentación normativa dividió Janusforge en dos tracks. El Track 1 es descubrimiento de fármacos: diseño, comparación y validación de ligandos Janus. El Track 2 contempla suministro, estándares, biomasa, breeding y otras rutas de acceso al material. Ambos pueden ser útiles, pero no responden a la misma pregunta.",
        "Esta separación impidió que el origen vegetal, la disponibilidad de cannabis o el interés por quimiotipos se convirtieran en un sustituto de la evidencia de receptor. El Track 2 queda disponible como apoyo estratégico; el Track 1 conserva la prioridad diaria. Es una decisión sencilla en apariencia, pero protege al programa de uno de los desvíos habituales de proyectos de cannabinoides: confundir procedencia natural con validación farmacológica.",
        "También crea una arquitectura legible para colaboradores. Un químico medicinal, un investigador de ensayos o una CRO pueden saber qué parte del trabajo les concierne sin asumir que la cadena de suministro decide qué compuesto debe avanzar."
    ]),
    ("3. THCV como brújula imperfecta", [
        "THCV fue el prototipo natural que permitió definir la hipótesis. Su interés no consiste en ser el producto final del proyecto, sino en mostrar que el espacio cannabinoide puede sugerir una dirección Janus incompleta. La literatura y los mapas internos advierten que el comportamiento de CB1 puede depender de contexto, dosis y ocupación, el llamado flip funcional.",
        "A partir de ahí, el proyecto abandonó la pregunta superficial de cuál molécula se parece más a un cannabinoide conocido. La pregunta operativa pasó a ser cuál candidato ofrece una separación más limpia de referencias como THCV y THC, sin caer en una dirección de agonismo CB1 fuerte. Esto generó criterios explícitos y anti-criterios igual de explícitos.",
        "Un score de docking aislado, una similitud visual con CBD o una narrativa antiinflamatoria no constituyen éxito Janus. El umbral requiere coherencia funcional futura y, antes de ella, filtros comparativos que no finjan ser una respuesta experimental."
    ]),
    ("4. La primera campaña H1-H5", [
        "La primera etapa de diseño recorrió varias hipótesis THCV-like. Los Batches 1 y 2 exploraron cambios de cadena, acidez, ésteres, sustituyentes y volumen. Hubo señales proxy puntuales, especialmente alrededor de una modificación 1-prima, pero los resultados no se interpretaron como una familia ya validada.",
        "En Batch 3, JANUS_H1_02c fue el mejor resultado computacional de esta línea. Superó el gate proxy de comparación frente a THCV y THC y justificó una evaluación dinámica más exigente. Este momento es importante porque muestra que el repositorio sí es capaz de generar hipótesis seleccionables, no solo documentación negativa.",
        "Pero la dinámica molecular en membrana POPC de 20 ns no mostró una ventaja convincente frente a THCV en el mecanismo geométrico elegido. El programa aplicó un NO-GO al andamiaje fitocannabinoide como eje principal. La lección no fue que el docking sea inútil, sino que es insuficiente para responder a una pregunta funcional."
    ]),
    ("5. Pivot a scaffolds sintéticos", [
        "El NO-GO de la línea THCV-like abrió un pivot hacia precedentes sintéticos Yin-Yang, con URB447 y otras referencias como mapa conceptual. El objetivo no era copiar moléculas publicadas ni reclamar inventos ajenos. Era explorar si scaffolds menos dependientes del lenguaje fitocannabinoide podían ofrecer hipótesis más rígidas y testeables.",
        "Se prepararon y documentaron los receptores CB1 5TGZ y CB2 6PT0, las cajas de docking y el procedimiento de comparación. El panel dual usó un protocolo reproducible y referencias internas. El gate de Vina fue definido como filtro de ocupación y pose: una forma de ordenar decisiones, no una medida de Ki, potencia, eficacia ni selectividad farmacológica.",
        "Esta disciplina semántica importa. Al poner límites al instrumento, el proyecto puede aprovecharlo sin permitir que sustituya el experimento. Esa es la base de la siguiente historia: el candidato con el mejor resultado de docking no sobrevivió el filtro posterior."
    ]),
    ("6. D2_22: una lección decisiva", [
        "JANUS_D2_22 fue el ex-lead del Batch D1/Option D por docking dual. Sus resultados Vina fueron los mejores del panel y sus poses para CB1 y CB2 se conservan localmente. Por esa razón se justificó una simulación de membrana adicional. Era una decisión razonable de priorización, no una declaración de éxito farmacológico.",
        "La MD en POPC de 20 ns para CB1 5TGZ finalizó correctamente, con artefactos y métricas trazables. Sin embargo, la lectura geométrica no apoyó el mecanismo de contención inactiva que el programa buscaba priorizar. La separación TM3-TM6 se solapó más con el régimen de referencia THC que con el patrón de THCV. Una TM6 relativamente estable no equivalía a un receptor funcionalmente bloqueado.",
        "La decisión documentada es NO-GO de trinquete CB1: D2_22 queda descartado como lead funcional. Debe mantenerse como caso histórico y visualizable, pero nunca etiquetarse como lead activo. Esta honestidad metodológica es una de las contribuciones más valiosas de Janusforge."
    ]),
    ("7. La línea Qiu y el control publicado", [
        "En paralelo se auditó una serie de compuestos publicada por Qiu y colaboradores. El trabajo 0D a 0J verificó identidad estructural, preparó entradas de docking, analizó poses y documentó control de calidad. Esta cadena confirma lo que realmente confirma: la trazabilidad de un proceso computacional alrededor de un precedente publicado.",
        "Qiu-14 no es una invención Janusforge ni un producto potencial propio. Su papel actual es el de vehículo de validación: una referencia publicada que permite plantear una primera hipótesis H1-a, orientada a detectar una señal funcional hCB2 en un formato de ensayo aún por cerrar operativamente.",
        "El uso de un control publicado es prudente. Si la señal no se observa, el programa gana una respuesta y evita diseñar una campaña propietaria sobre una base débil. Si se observa, la señal no concede derechos de propiedad intelectual, pero proporciona una base experimental para definir la siguiente pregunta."
    ]),
    ("8. De la simulación al ensayo", [
        "La transición más importante ya no es computacional. Janusforge cerró una especificación experimental H1-a CB2-first para Qiu-14. El documento distingue material, identidad, controles, formato de ensayo y decisiones aún pendientes. Los umbrales cuantitativos de PASS/KILL se mantienen como TBD cuando no existen datos suficientes para fijarlos honestamente.",
        "Además, el repositorio contiene un paquete para CRO: cartas de RFQ, requisitos de síntesis y ensayo, nota de confidencialidad y una matriz interna para comparar propuestas. Esto convierte una idea de laboratorio en una acción externalizable y comparable. No equivale a haber iniciado trabajo húmedo; equivale a estar preparado para pedir las cotizaciones correctas.",
        "La ruta crítica es enviar el mismo paquete a dos o tres proveedores, comparar capacidades y cerrar los TBD junto con el proveedor seleccionado antes de emitir una orden. El siguiente resultado importante será experimental, no un nuevo score."
    ]),
    ("9. Qué sabemos y qué no sabemos", [
        "El proyecto ha demostrado preparación, ejecución y auditoría de varios pasos computacionales. Ha demostrado también que dos propuestas priorizadas por docking no superaron el criterio dinámico escogido. Estas observaciones negativas son reales y útiles, pero no equivalen a una clasificación farmacológica completa.",
        "No se ha demostrado afinidad, potencia, eficacia, selectividad funcional CB1/CB2, actividad antifibrótica, exposición periférica, seguridad ni beneficio clínico de una molécula propia. Tampoco debe leerse una pose en 6PT0 o 5TGZ como si fuera una medida funcional. La evidencia experimental publicada de terceros es contexto; no es evidencia sobre una NCE de Janusforge.",
        "Esta frontera no reduce el valor del proyecto. Lo hace más fiable. La literatura, la observación computacional, la hipótesis y la visión de producto están etiquetadas como capas distintas. Cualquier futura presentación debería conservar exactamente esta estructura."
    ]),
    ("10. Propiedad intelectual y confidencialidad", [
        "El repositorio contiene un landscape de prior art y un gate de IP que sitúan correctamente el problema. El espacio de pirazoles, las familias rimonabant, los compuestos Qiu y ciertas reclamaciones duales relacionadas con fibrosis representan zonas ocupadas o potencialmente sensibles. El análisis no pretende ser una opinión de libertad de operación ni de patentabilidad.",
        "La política de confidencialidad es apropiada: no publicar SMILES, SDF, PDBQT o tablas de NCE propietarias; usar identificadores y mantener las estructuras bajo control. Las hipótesis llamadas blue ocean son preguntas de diseño, no permisos para sintetizar ni afirmaciones de espacio libre.",
        "La secuencia correcta es validar con el control publicado, obtener evidencia experimental, elegir una familia propia bajo confidencialidad y pasar por counsel antes de divulgar estructuras o iniciar una campaña de síntesis propietaria. Una buena estrategia IP no acelera el dato; impide que el dato futuro se desperdicie."
    ]),
    ("11. El visor molecular y la narrativa", [
        "El visor local basado en FastAPI y 3Dmol.js tiene un valor operativo claro. Permite inspeccionar receptores, poses y archivos locales sin sacar material sensible fuera del equipo. Es útil para control de calidad, conversaciones de química medicinal y preparación de reuniones técnicas.",
        "Pero una interfaz también comunica prioridades. Por coherencia con los informes científicos, D2_22 debe mostrarse como ex-lead de docking y NO-GO funcional, no como lead vigente. Puede ser la primera estructura que un usuario quiera ver, porque ilustra cómo el programa tomó una decisión. No debe convertirse por eso en el compuesto recomendado para avanzar.",
        "Alinear etiquetas, asistentes y documentos de estado evitará que una comodidad de navegación cree una contradicción con la evidencia. Es una corrección pequeña que protege la credibilidad completa del repositorio."
    ]),
    ("12. El próximo capítulo", [
        "La siguiente fase de Janusforge es concreta. Primero, consolidar un estado único del programa y corregir cualquier etiqueta histórica que sugiera que D2_22 sigue activo. Segundo, enviar RFQs H1-a comparables. Tercero, seleccionar CRO y cerrar criterios de decisión antes del ensayo. Cuarto, ejecutar H1-a y decidir con transparencia si Qiu-14 merece pasar a la comprobación separada de CB1.",
        "Solo después de una señal experimental y de la revisión de propiedad intelectual tendría sentido reabrir un diseño de NCE propio. También entonces tendría sentido decidir si más MD, redocking o métodos de reproducción de mayor fidelidad aportan valor. Hoy no son la ruta crítica.",
        "La historia correcta de Janusforge no es que ya haya descubierto un fármaco. Es que ha creado un proceso que formula una hipótesis dual, prueba sus propias ilusiones computacionales, descarta lo que no resiste y prepara el primer experimento que puede cambiar el estado del programa."
    ]),
]

INK = colors.HexColor("#17324D")
TEAL = colors.HexColor("#238A8D")
GOLD = colors.HexColor("#C98A24")
PALE = colors.HexColor("#EAF3F4")
RED = colors.HexColor("#B34B4B")

def hexagon(d, x, y, r, stroke=INK):
    pts = []
    for dx, dy in [(0,r),(.866*r,.5*r),(.866*r,-.5*r),(0,-r),(-.866*r,-.5*r),(-.866*r,.5*r)]:
        pts.extend([x+dx,y+dy])
    d.add(Polygon(pts, strokeColor=stroke, fillColor=None, strokeWidth=1.4))

def mol_thcv():
    d = Drawing(430, 175)
    d.add(String(8, 155, "Molecula de referencia publica: delta9-THCV", fontName="Helvetica-Bold", fontSize=12, fillColor=INK))
    # Schematic cannabinoid scaffold: aromatic ring, oxygenated ring and propyl side chain.
    hexagon(d, 112, 86, 34); hexagon(d, 170, 86, 34)
    d.add(Line(138, 104, 146, 108, strokeColor=INK, strokeWidth=1.4))
    d.add(Line(138, 68, 146, 64, strokeColor=INK, strokeWidth=1.4))
    d.add(String(95, 121, "OH", fontName="Helvetica-Bold", fontSize=10, fillColor=RED))
    d.add(String(176, 112, "O", fontName="Helvetica-Bold", fontSize=10, fillColor=RED))
    d.add(Line(82, 86, 50, 86, strokeColor=INK, strokeWidth=1.6))
    d.add(Line(50, 86, 28, 104, strokeColor=INK, strokeWidth=1.6))
    d.add(Line(28, 104, 8, 86, strokeColor=INK, strokeWidth=1.6))
    d.add(String(8, 65, "C3", fontName="Helvetica-Bold", fontSize=10, fillColor=TEAL))
    d.add(Line(198, 68, 230, 52, strokeColor=INK, strokeWidth=1.6))
    d.add(Line(230, 52, 265, 70, strokeColor=INK, strokeWidth=1.6))
    d.add(String(275, 65, "scaffold fitocannabinoide", fontName="Helvetica", fontSize=10, fillColor=colors.HexColor("#45627A")))
    d.add(String(8, 16, "Uso en Janusforge: semilla / control de referencia. No representa un candidato propio ni un perfil funcional ya limpio.", fontName="Helvetica", fontSize=9, fillColor=colors.HexColor("#45627A")))
    return d

def mol_urb447():
    d = Drawing(430, 175)
    d.add(String(8, 155, "Molecula de referencia publica: URB447", fontName="Helvetica-Bold", fontSize=12, fillColor=INK))
    # Schematic pyrrole-centered comparator, deliberately captioned as conceptual representation.
    d.add(Polygon([130,112,160,98,154,64,105,64,98,98], strokeColor=INK, fillColor=None, strokeWidth=1.5))
    d.add(String(122, 81, "N", fontName="Helvetica-Bold", fontSize=11, fillColor=RED))
    d.add(Line(105, 64, 70, 43, strokeColor=INK, strokeWidth=1.5)); hexagon(d, 42, 30, 23)
    d.add(Line(160, 98, 202, 114, strokeColor=INK, strokeWidth=1.5)); hexagon(d, 230, 124, 23)
    d.add(Line(154, 64, 194, 46, strokeColor=INK, strokeWidth=1.5)); d.add(String(198, 38, "CONH2", fontName="Helvetica-Bold", fontSize=10, fillColor=RED))
    d.add(String(8, 16, "Uso en Janusforge: comparador publicado de diseno Janus/periferia. No es una molecula inventada por el proyecto.", fontName="Helvetica", fontSize=9, fillColor=colors.HexColor("#45627A")))
    return d

def flow_diagram():
    d = Drawing(430, 145)
    d.add(String(8, 125, "Mapa de decision del programa", fontName="Helvetica-Bold", fontSize=12, fillColor=INK))
    labels = [(8,"literatura"),(102,"docking/QC"),(196,"MD / gates"),(290,"ensayo H1-a")]
    for x, lab in labels:
        d.add(Rect(x, 66, 82, 34, rx=6, ry=6, fillColor=PALE, strokeColor=TEAL))
        d.add(String(x+8, 80, lab, fontName="Helvetica-Bold", fontSize=9, fillColor=INK))
    for x in [90,184,278]:
        d.add(Line(x,83,x+12,83,strokeColor=GOLD,strokeWidth=2)); d.add(Polygon([x+12,83,x+7,87,x+7,79],fillColor=GOLD,strokeColor=GOLD))
    d.add(String(8, 25, "Regla: un resultado solo avanza si supera el gate de su propia capa. El docking no equivale a funcion.", fontName="Helvetica", fontSize=9, fillColor=colors.HexColor("#45627A")))
    return d

def evidence_diagram():
    d = Drawing(430, 150)
    d.add(String(8, 130, "Escalera de evidencia", fontName="Helvetica-Bold", fontSize=12, fillColor=INK))
    rows=[("Vision clinica", "futuro"),("Hipotesis Janus", "por probar"),("MD / docking", "observacion"),("Literatura y QC", "base")]
    for i,(a,b) in enumerate(rows):
        x=45+i*38; y=20+i*23; w=330-i*76
        d.add(Rect(x,y,w,19,fillColor=[colors.HexColor("#E3EEF2"),colors.HexColor("#D5E8E9"),colors.HexColor("#BBDADB"),colors.HexColor("#9DC6C8")][i],strokeColor=TEAL))
        d.add(String(x+8,y+5,a,fontName="Helvetica-Bold",fontSize=8,fillColor=INK))
        d.add(String(x+w-55,y+5,b,fontName="Helvetica",fontSize=8,fillColor=colors.HexColor("#45627A")))
    return d

def timeline_diagram():
    d=Drawing(430,120)
    d.add(String(8,102,"Cronologia resumida",fontName="Helvetica-Bold",fontSize=12,fillColor=INK))
    d.add(Line(25,55,400,55,strokeColor=TEAL,strokeWidth=2))
    items=[(38,"H1-H5",TEAL),(125,"NO-GO\nmembrana",RED),(225,"Option D\nD2_22",GOLD),(315,"H1-a / CRO",TEAL)]
    for x,label,c in items:
        d.add(Circle(x,55,6,fillColor=c,strokeColor=c));
        for j,line in enumerate(label.split("\n")):
            d.add(String(x-20,32-j*10,line,fontName="Helvetica-Bold",fontSize=8,fillColor=INK))
    return d

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7E0E6"))
    canvas.line(2*cm, 1.55*cm, A4[0]-2*cm, 1.55*cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526B7F"))
    canvas.drawString(2*cm, 1.0*cm, "Janusforge - borrador interno")
    canvas.drawRightString(A4[0]-2*cm, 1.0*cm, f"{doc.page}")
    canvas.restoreState()

story = []
story += [Spacer(1, 4.7*cm), Paragraph("JANUSFORGE", styles["BookTitle"]),
          Paragraph("Del mapa cannabinoide a la decisión experimental", styles["Subtitle"]),
          Spacer(1, 1.7*cm), Paragraph("Borrador de libro del proyecto", styles["Subtitle"]),
          Spacer(1, 1.0*cm), Paragraph("13 de agosto de 2026", styles["Subtitle"]),
          Spacer(1, 3.5*cm), Paragraph("Documento interno. No es consejo médico, regulatorio ni legal. No contiene estructuras propietarias no publicadas.", styles["Small"]), PageBreak()]

story += [Paragraph("Índice", styles["Chapter"])]
toc = [["Capítulo", "Tema"]] + [[title.split(". ")[0], title.split(". ", 1)[1]] for title, _ in chapters]
table = Table(toc, colWidths=[2.4*cm, 13.1*cm], repeatRows=1)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17324D")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("LEADING", (0,0), (-1,-1), 15),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#EFF4F6")]),
    ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#D7E0E6")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story += [table, Spacer(1, 0.8*cm), Paragraph("Nota de lectura", styles["Chapter"]), Paragraph("Cada capítulo resume un tramo de trabajo y conserva la frontera entre literatura, cálculo, hipótesis y evidencia experimental. Se han omitido estructuras y datos propietarios deliberadamente.", styles["BodyBook"]), PageBreak()]

# Lámina visual suministrada por el usuario: se mantiene separada del texto
# para que la edición conserve la lectura sobria del borrador original.
if STRUCTURE_IMAGE.exists():
    story += [Paragraph("Figura 1. Vista estructural receptor-ligando", styles["Chapter"]),
              Spacer(1, 0.25*cm), Image(str(STRUCTURE_IMAGE), width=15.0*cm, height=11.25*cm),
              Spacer(1, 0.35*cm),
              Paragraph("Representación estructural proporcionada por el usuario. La proteína se muestra en cinta coloreada y el ligando en verde. La imagen es ilustrativa de una pose o complejo local; por sí sola no demuestra afinidad, eficacia ni perfil farmacológico Janus.", styles["BodyBook"]),
              PageBreak()]

for i, (title, paras) in enumerate(chapters):
    story.append(Paragraph(title, styles["Chapter"]))
    if i == 0:
        story.append(Paragraph("<i>" + "El rigor del proyecto no consiste en convertir hipótesis en certezas, sino en saber qué experimento puede decidirlas." + "</i>", styles["Quote"]))
    for p in paras:
        story.append(Paragraph(p, styles["BodyBook"]))
    # Las figuras se colocan al final, llenando el espacio editorial libre
    # sin interrumpir la lectura de la versión narrativa original.
    if i == 0:
        story.append(Spacer(1, 0.35*cm)); story.append(flow_diagram())
    if i == 2:
        story.append(Spacer(1, 0.25*cm)); story.append(mol_thcv())
    if i == 4:
        story.append(Spacer(1, 0.25*cm)); story.append(mol_urb447())
    if i == 5:
        story.append(Spacer(1, 0.3*cm)); story.append(timeline_diagram())
    if i == 8:
        story.append(Spacer(1, 0.3*cm)); story.append(evidence_diagram())
    story.append(PageBreak())

story += [Paragraph("Fuentes internas principales", styles["Chapter"])]
sources = [
    "README.md y docs/README.md", "docs/criterio_exito_janus.md", "docs/lecciones_aprendidas_track1.md",
    "docs/ip_gate_janusforge.md", "results/reports/janusforge_dossier_estado_programa.md",
    "results/reports/h1_h5_design_history.md", "results/reports/option_d_batch_d1_gate_summary.md",
    "results/reports/md_d2_22_20ns_summary.md", "results/reports/qiu_0l_h1a_experimental_spec.md",
    "results/reports/qiu_0n_status.md", "results/reports/qiu_0ip_novelty_landscape.md",
    "results/reports/cro_package_h1a/00_index.md",
]
for s in sources:
    story.append(Paragraph("- " + s, styles["BodyBook"]))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Fin del borrador. Para una edición futura: añadir figuras seleccionadas, cronología detallada, glosario de receptores y una bibliografía externa normalizada.", styles["Quote"]))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2.1*cm, title="Janusforge - borrador de libro", author="Janusforge")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)

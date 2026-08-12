# Documentación — janusforge

Índice breve de la documentación del proyecto.

### Nivel 0 — Documento Normativo (Norma Fuente Matrix)

| Documento | Contenido |
|-----------|-----------|
| [guia_maestra_biotecnologia_quimiotipos.md](guia_maestra_biotecnologia_quimiotipos.md) | **Documento Normativo Nivel 0 v1.0 (Oficial / Congelada):** desacopla **Track 1** (*Drug Discovery* — ligando / análogos H1–H5, prioritario) de **Track 2** (*Supply Chain* — síntesis, breeding/MAS A-nat, fermentación, CRISPR). Matriz de auditoría retroactiva. |

### Nivel ≥1 — Documentos operativos

| Documento | Contenido |
|-----------|-----------|
| [quimioma_cannabico_cb1_cb2.md](quimioma_cannabico_cb1_cb2.md) | **Brújula química** (castellano): mapa vivo del quimioma cannábico CB1/CB2, THCV como prototipo Janus imperfecto, análogos permitidos, criterios de fibrosis como filtro *segundo*, reglas de pipeline y fracaso temprano. Enlaza la tabla operativa de semillas. |
| [quimiotipos_varinas_thcv.md](quimiotipos_varinas_thcv.md) | **Varinas / THCV–THCVA** (castellano): biosíntesis C3 vs C5, landraces africanas (matices vs marketing), ratios, implicación planta→análogos; hipótesis H1–H5 THCV-like ancladas al gap retrospectivo Vina. |
| [criterio_exito_janus.md](criterio_exito_janus.md) | **Criterio de éxito** in silico / pre-ensayo (1 página): qué significa “perfil Janus más limpio que THCV”; incluye superar separación THCV–THC en el panel retrospectivo. |
| [mecanismo_flip_thcv_cb1.md](mecanismo_flip_thcv_cb1.md) | **Mecanismo del flip CB1** de Δ9-THCV (castellano): equilibrio R ⇌ R\*, C3 vs C5 / toggle TM6, tabla de eficacia esquemática, implicación H1–H5 y matiz Vina ≠ α. |
| [literatura_fibrosis_cb1_cb2.md](literatura_fibrosis_cb1_cb2.md) | **Memoria biológica** (castellano): fibrosis / IPF, eje endocannabinoide CB1/CB2, hipótesis Janus (CB1 antagonista + CB2 agonista), precedentes, gaps. Documento vivo; el norte químico remite al quimioma. |
| [literatura_prioridad_y_novelty.md](literatura_prioridad_y_novelty.md) | **Auditoría de novelty / prior art** (castellano, 2026-08-06): concepto Janus×fibrosis = prior art; THCV×IPF sin paper primario (ventana); NCE periférico H1–H5 = white space. Claims teóricos de uso no viables. |
| [ip_gate_janusforge.md](ip_gate_janusforge.md) | **IP gate operativo** (2026-08-12): 0K → 0IP → 0L → wet H1/H2 → blue-ocean NCE → 🛑 counsel → filing; confidencialidad; **not legal advice**. Landscape: [`../results/reports/qiu_0ip_novelty_landscape.md`](../results/reports/qiu_0ip_novelty_landscape.md). 0L: [`../results/reports/qiu_0l_h1a_experimental_spec.md`](../results/reports/qiu_0l_h1a_experimental_spec.md). |
| [mapa_ligandos_janus_cb1_cb2.md](mapa_ligandos_janus_cb1_cb2.md) | **Mapa de precedentes Janus** (castellano, 2026-08-10): URB447 / GW405833 / AM1710 / compuesto 14 (Qiu); umbral ≈ −11 kcal/mol ↔ nM; fibrosis (combo AM6545+AM1241 vs hueco monomolecular); lectura Batch D1 / D2_22. |
| [lecciones_aprendidas_track1.md](lecciones_aprendidas_track1.md) | **Lecciones Track 1** (castellano, 2026-08-11): docking/gate, SAR H1–H5, MD; **D2_22 descartado** (NO-GO trinquete); GPU pausa; plan pirazol Qiu; sin SMILES. |
| [apendice_ip_supply_botanico.md](apendice_ip_supply_botanico.md) | **Apéndice IP / supply botánico:** puerta abierta a coste cero (patentes de método, cáñamo/AEMPS, breeding IRTA–CSIC). No eleva Track 2: ejecución diaria = Track 1 in silico. |

**Informes Track 1 recientes (results/reports):**  
[`../results/reports/md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md) (MD + falla biofísica) · [`../results/reports/next_iter_pyrazole_qiu_plan.md`](../results/reports/next_iter_pyrazole_qiu_plan.md) (plan pausado) · [`../results/reports/option_d_pivot_urb447.md`](../results/reports/option_d_pivot_urb447.md) · [`../results/reports/option_d_batch_d1_gate_summary.md`](../results/reports/option_d_batch_d1_gate_summary.md).

**Datos operativos (mapa, no hit table masiva):**  
[`../data/libraries/quimioma_semillas.csv`](../data/libraries/quimioma_semillas.csv) — semillas / controles / comparadores con SMILES curados (PubChem) y roles.

### Exportación consolidada

| Archivo | Contenido |
|---------|-----------|
| [exports/janusforge_memoria_completa.pdf](exports/janusforge_memoria_completa.pdf) | Copia PDF legible: Guía Maestra Nivel 0 v1.0 + literatura fibrosis + quimioma + varinas/THCV + criterio de éxito + novelty/FTO + apéndice IP botánico + informe retrospectivo. Regenerar con `python scripts/build_memoria_pdf.py` (requiere `markdown` y `xhtml2pdf`). |

Para el overview técnico del repo, ver el [README raíz](../README.md).

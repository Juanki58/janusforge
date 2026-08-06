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
| [literatura_fibrosis_cb1_cb2.md](literatura_fibrosis_cb1_cb2.md) | **Memoria biológica** (castellano): fibrosis / IPF, eje endocannabinoide CB1/CB2, hipótesis Janus (CB1 antagonista + CB2 agonista), precedentes, gaps. Documento vivo; el norte químico remite al quimioma. |

**Datos operativos (mapa, no hit table masiva):**  
[`../data/libraries/quimioma_semillas.csv`](../data/libraries/quimioma_semillas.csv) — semillas / controles / comparadores con SMILES curados (PubChem) y roles.

### Exportación consolidada

| Archivo | Contenido |
|---------|-----------|
| [exports/janusforge_memoria_completa.pdf](exports/janusforge_memoria_completa.pdf) | Copia PDF legible: Guía Maestra Nivel 0 v1.0 (Track 1 ligando vs Track 2 supply) + literatura fibrosis + quimioma + varinas/THCV + criterio de éxito + informe retrospectivo. Regenerar con `python scripts/build_memoria_pdf.py` (requiere `markdown` y `xhtml2pdf`). |

Para el overview técnico del repo, ver el [README raíz](../README.md).

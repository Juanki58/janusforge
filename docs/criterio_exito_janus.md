# Criterio de éxito Janus (in silico / pre-ensayo)

> Una página operativa. Complementa [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md).  
> Fecha: 2026-08-06. Gates funcionales pre-ensayo + gate de separación proxy (panel retrospectivo; sin docking masivo nuevo).

---

## Pregunta que responde este criterio

¿Qué significa, *antes* de binding húmedo y de fibrosis, que un candidato tenga un **perfil Janus más limpio que THCV**?

THCV es la semilla: CB1 antagonista (a menudo) + CB2 agonista parcial, con **flip CB1** dosis-dependiente. “Más limpio que THCV” no es “más potente en un modelo de fibrosis”, ni “más parecido a CBD”.

---

## Umbral mínimo (gates en orden)

Un análogo / hit se considera **mejora pre-ensayo** respecto a THCV si, en la evidencia disponible (literatura + SAR +, más adelante, binding/función), cumple de forma acumulativa:

| # | Gate | Lectura operativa |
|---|------|-------------------|
| 1 | **Menos evidencia de flip CB1** | En la ventana dosis/ocupación relevante: antagonismo o modulación negativa de CB1 **sin** agonismo CB1 residual claro a alta ocupación (o con margen terapéutico argumentable). Si solo hay hipótesis SAR sin dato funcional, el gate queda *abierto*, no pasado. |
| 2 | **CB2 ago mantenido** | Agonismo CB2 (parcial aceptable) al menos comparable en dirección al de THCV; no sacrificar CB2 ago para “apagar” CB1 si el resultado es un ligando inerte o solo CB1-ant sin brazo CB2. |
| 3 | **Sin dirección anti-semilla** | No desplazar el SAR hacia agonismo CB1 fuerte (patrón THC / THCP / cadenas C5–C7). |
| 4 | **Periferia hipotética o diseñada** (deseable) | Polaridad, ácidos/ésteres, TPSA, eflujo o entrega pulmonar que hagan *plausible* menor carga SNC vs THCV neutro. Hipótesis documentada ≠ gate pasado; sí es ventaja de priorización. |
| 5 | **Fibrosis** | Solo **después** de 1–3 (y preferible 4). Un readout antifibrótico con CB1 sucio **no** cuenta como éxito Janus. |

---

## Qué cuenta como éxito / fracaso temprano (brazo mapa)

| Resultado | Significado |
|-----------|-------------|
| **Éxito de mapa** | Existe al menos una hipótesis THCV-like (o minor promovido) con narrativa SAR testeable que *podría* pasar gates 1–2 mejor que THCV, sin caer en anti-semilla. |
| **Éxito pre-Vina** | Priorización documentada (tabla de semillas + criterios) lista para anclar docking/binding; no se exige score Vina aún. |
| **Fracaso temprano “solo planta”** | THCV sigue flip-prone y ningún natural del inventario mejora 1–2; entonces el norte pasa a **análogos THCV-like**, no se abandona el perfil Janus (véase quimioma §7). |

---

## Gate de separación proxy (análogo vs THCV natural)

Tras la retrospectiva del panel (THCV vs THC: gap dual ≈ **−0.20 kcal/mol** — poca separación scaffold-scaffold), un análogo THCV-like cuenta como **éxito de separación in silico** solo si, en el **mismo panel retrospectivo** (mismos receptores, cajas, exhaustiveness/seed), supera de forma clara la separación THCV–THC (dual y, preferible, ejes CB1/CB2) frente a anti-semillas — **sin** incumplir gates 1–3 funcionales cuando haya dato. Un score alto aislado no basta (anti-criterio abajo). Detalle de hipótesis: [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md).

### Batch 1–2 (H1–H5) — ejecución local

Track 1 se genera y dockea **en local** (`scripts/generate_h1_h5_candidates.py`, `scripts/generate_h1_h5_batch2.py` → Vina 5TGZ/6PT0). Estructuras/SMILES de análogos nuevos **no se publican** (gitignored). Resúmenes públicos sin SMILES: [`../results/reports/h1_h5_batch1_gate_summary.md`](../results/reports/h1_h5_batch1_gate_summary.md), [`../results/reports/h1_h5_batch2_gate_summary.md`](../results/reports/h1_h5_batch2_gate_summary.md). Historial de diseño (lecciones, sin estructuras): [`../results/reports/h1_h5_design_history.md`](../results/reports/h1_h5_design_history.md). Gate duro proxy: `dual < dual_THCV` **y** `(dual_THC − dual) > 0.40` kcal/mol (claramente > ~0.20).
---

## Anti-criterios (no son éxito)

- Score de docking alto en CB1 o CB2 **sin** coherencia con el perfil funcional deseado.
- Similitud a CBD, “cannabinoide antifibrótico” genérico, o polifarmacología atractiva en inflamación.
- Potencia CB1 agonista (aunque sea “muy activa”).
- Narrativa de IPF sin gate de receptor.

---

## Referencia rápida

Semillas y roles: [`../data/libraries/quimioma_semillas.csv`](../data/libraries/quimioma_semillas.csv) · biología fibrosis: [`literatura_fibrosis_cb1_cb2.md`](literatura_fibrosis_cb1_cb2.md) · varinas / diseño THCV-like: [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md).

Retrospectiva Vina del panel (afinidad/pose proxy, no gates funcionales): [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md).

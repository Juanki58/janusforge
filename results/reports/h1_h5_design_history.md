# H1–H5 design history (public)

> **No SMILES.** Solo IDs, lecciones de gate proxy y política IP.  
> Vina = afinidad/pose — no éxito Janus funcional ([`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

## Política IP (constante)

- SMILES / SDF / PDBQT / CSV de análogos de diseño: **solo** paths gitignored  
  (`data/libraries/h1_h5*`, `data/processed/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Informes públicos en `results/reports/`: IDs, scores, pass/fail — **sin estructuras**.
- No publicar estructuras concretas en `docs/`.

## Iteración 1 — librería de diseño (Batch 1)

- Resumen: [`h1_h5_batch1_gate_summary.md`](h1_h5_batch1_gate_summary.md)
- Panel local: `data/libraries/h1_h5_batch1.csv` (gitignored)
- Hipótesis muestreadas: H1 (cadena/rama), H2 (ácido/éster), H3 (ω-F), H4 (9,10-H2), H5 (ArOMe lite)
- Gate duro: `dual < dual_THCV` **y** `(dual_THC − dual) > 0.40`
- **Resultado:** 1/7 PASS — solo **JANUS_H1_02** (1′-metil en THCV neutro), marginal
- **Lección:** la rama 1′-Me movió la aguja; ácidos/ésteres H2 debilitaron CB1 (dual peor). No hit Janus.

## Iteración 2 — H1×H2 + volumen 1′ (Batch 2)

- Resumen: [`h1_h5_batch2_gate_summary.md`](h1_h5_batch2_gate_summary.md)
- Panel local: `data/libraries/h1_h5_batch2.csv` (gitignored)
- Diseño: híbridos 1′-rama × THCVA (COOH / éster metílico) + volumen mayor en 1′ sobre THCV neutro (etil, ciclopropilo)
- Misma métrica de gate; refs delta9-THCV / delta9-THC en el mismo run
- Pregunta crítica: ¿el híbrido mejora, o el COOH mata CB1 otra vez?
- **Resultado:** 0/6 PASS. El COOH/éster **mata CB1 otra vez** (CB1 ≪ THCV); volumen 1′ neutro (Et/cPr) no supera el umbral claro vs THC. 1′-Me (Batch 1) sigue siendo el único PASS proxy marginal.
- Lecciones: ver “Lecciones técnicas” en el resumen Batch 2.

## Cierre — barrido rápido (Batch 1–2)

- **Fin de fase** de exploración rápida H1–H5 (hipótesis anchas: cadena/rama, ácidos/ésteres, ω-F, 9,10-H2, ArOMe lite, híbridos H1×H2, volumen 1′ Et/cPr).
- Único PASS proxy marginal acumulado: **JANUS_H1_02** (1′-metilo sobre scaffold THCV-like neutro).
- Vina estático ≠ éxito Janus funcional; gates 1–3 siguen abiertos.

## Siguiente fase — refino scaffold JANUS_H1_02 (Batch 3 planificado, no ejecutado)

- Plan público (IDs conceptuales, sin SMILES): [`h1_h5_batch3_plan.md`](h1_h5_batch3_plan.md)
- Estrategia Batch 3:
  1. **Bioisósteros no polares / extremo de cadena lipofílica** manteniendo **1′-Me**, para intentar amplificar el gap vs THC hacia **>0.80** kcal/mol si es posible (proxy; no garantía funcional).
  2. **Periferia / TPSA** vía éteres pequeños, F estratégico o bioisósteros de fenol — **sin ácidos libres (-COOH)** que penalicen el bolsillo CB1 en Vina estático.
- Docking Batch 3: **no ejecutado** en este cierre de fase.

## Scripts (genéricos; sin SMILES de análogos)

- `scripts/generate_h1_h5_candidates.py` — Batch 1
- `scripts/generate_h1_h5_batch2.py` — Batch 2
- `scripts/analyze_h1_h5_gate.py` — gate + informes (`--batch h1_h5_batchN`)
- Prep/dock: `scripts/prepare_panel_3d.py`, `scripts/run_retrospective_dock.py`

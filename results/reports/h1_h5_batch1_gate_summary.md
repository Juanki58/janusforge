# Iteración 1 — librería de diseño (H1–H5) — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).  
> Historial: [`h1_h5_design_history.md`](h1_h5_design_history.md).

- Fecha: 2026-08-06
- Panel local: `data/libraries/h1_h5_batch1.csv` (gitignored)
- Scores: `results/docking/h1_h5_batch1/retrospective_scores.csv` (gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=12; seed=42

## Métrica de gate duro

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Referencias en el mismo run: dual_THCV = **-9.450**, dual_THC = **-9.321**, gap THCV−THC = **-0.129** kcal/mol
- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > 0.40` (claramente > separación THCV–THC ≈ 0.20)

**Resultado agregado:** 1/7 candidatos de diseño pasaron el gate. Exhaustiveness=12; seed=42.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |
|----|-----------|---------------|-----|-----|------|---------|--------|-------------|
| delta9-THCV | REF | sí | -9.039 | -9.860 | -9.450 | 0.000 | -0.129 | ref |
| delta9-THC | REF | sí | -8.603 | -10.039 | -9.321 | 0.129 | 0.000 | ref |
| JANUS_H1_01 | H1 C4/CBDB-like | sí | -8.783 | -9.914 | -9.348 | +0.101 | -0.027 | fail |
| JANUS_H1_02 | H1 1'-Me | sí | -9.303 | -10.254 | -9.779 | -0.329 | -0.458 | PASS |
| JANUS_H2_01 | H2 THCVA | sí | -7.877 | -10.191 | -9.034 | +0.415 | +0.287 | fail |
| JANUS_H2_02 | H2 THCVA-OMe | sí | -7.818 | -10.060 | -8.939 | +0.511 | +0.382 | fail |
| JANUS_H3_01 | H3 ω-F (3'-F) | sí | -8.911 | -9.824 | -9.367 | +0.082 | -0.046 | fail |
| JANUS_H4_01 | H4 9,10-H2 | sí | -8.341 | -9.588 | -8.964 | +0.485 | +0.357 | fail |
| JANUS_H5_01 | H5 ArOMe lite | sí | -9.184 | -9.279 | -9.232 | +0.218 | +0.089 | fail |

## Veredicto

**1/7 PASS (solo JANUS_H1_02), y es marginal** (gap vs THC 0.458 kcal/mol, umbral 0.40). En este run el gap THCV–THC cayó a −0.129 (vs ≈−0.20 en retrospectiva exh=8): el proxy es ruidoso. H2 (ácidos/ésteres) empeoran dual por CB1 débil — esperable y no = fallo de periferia. H1-C4, H3-F, H4, H5 no baten a THCV. **No hay hit Janus**; hace falta binding/función.

**Lección → Batch 2:** 1′-Me movió la aguja; siguiente iteración = H1×H2 + volumen 1′ ([`h1_h5_design_history.md`](h1_h5_design_history.md)).

## IP

- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Detalle con SMILES (local): `results/hits/h1_h5_batch1/gate_detail.md`.

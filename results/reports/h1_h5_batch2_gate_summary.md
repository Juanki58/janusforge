# Iteración 2 — H1×H2 híbridos + volumen 1′ — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).  
> Historial: [`h1_h5_design_history.md`](h1_h5_design_history.md).

- Fecha: 2026-08-06
- Panel local: `data/libraries/h1_h5_batch2.csv` (gitignored)
- Scores: `results/docking/h1_h5_batch2/retrospective_scores.csv` (gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=12; seed=42

## Métrica de gate duro

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Referencias en el mismo run: dual_THCV = **-9.392**, dual_THC = **-9.196**, gap THCV−THC = **-0.196** kcal/mol
- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > 0.40` (claramente > separación THCV–THC ≈ 0.20)

**Resultado agregado:** 0/6 candidatos de diseño pasaron el gate. Exhaustiveness=12; seed=42.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |
|----|-----------|---------------|-----|-----|------|---------|--------|-------------|
| delta9-THCV | REF | sí | -8.924 | -9.859 | -9.392 | 0.000 | -0.196 | ref |
| delta9-THC | REF | sí | -8.338 | -10.054 | -9.196 | 0.196 | 0.000 | ref |
| JANUS_H1H2_01 | H1xH2 1'-Me-THCVA | sí | -6.570 | -10.344 | -8.457 | +0.934 | +0.739 | fail |
| JANUS_H1_03 | H1 1'-Et | sí | -8.745 | -10.113 | -9.429 | -0.037 | -0.233 | fail |
| JANUS_H1_04 | H1 1'-cPr | sí | -8.664 | -10.067 | -9.366 | +0.026 | -0.170 | fail |
| JANUS_H1H2_02 | H1xH2 1'-Me-ester | sí | -6.480 | -9.773 | -8.127 | +1.265 | +1.069 | fail |
| JANUS_H1H2_03 | H1xH2 1'-Et-THCVA | sí | -6.119 | -10.245 | -8.182 | +1.210 | +1.014 | fail |
| JANUS_H1H2_04 | H1xH2 1'-Et-ester | sí | -5.900 | -9.826 | -7.863 | +1.529 | +1.333 | fail |

## Veredicto

**0/6 PASS.** El híbrido **no mejora**: el COOH/éster aromático **mata CB1 otra vez** (CB1 ≈ −5.9 a −6.6 vs THCV −8.9) pese a CB2 decente; dual queda claramente peor que THCV. Volumen 1′ neutro: Et (H1_03) gana dual por un pelo (−9.429 vs −9.392) pero gap vs THC solo 0.233 ≪ 0.40; cPr no ayuda. **1′-Me (Batch 1) sigue siendo el único PASS proxy marginal.** Vina ≠ Janus; gates funcionales abiertos.

## IP

- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Detalle con SMILES (local): `results/hits/h1_h5_batch2/gate_detail.md`.

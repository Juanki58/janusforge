# Qiu pirazol — Batch 1 (Compound 14 / QIU_*; docking only) — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

- Fecha: 2026-08-11
- Panel local: `data/libraries/qiu_pyrazole_batch1.csv` (gitignored)
- Scores: `results/docking/qiu_pyrazole_batch1/retrospective_scores.csv` (gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=10; seed=42

## Métrica de gate (primaria: rank vs URB447)

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Ancla sintética en el mismo run: dual_URB447 = **-10.448**
- Referencias fitocannabinoides (secundarias): dual_THCV = **-9.357**, dual_THC = **-9.221**, gap THCV−THC = **-0.136** kcal/mol
- **PASS rank-gate** solo si: (1) `dual < dual_URB447` y (2) `(dual_THC − dual) > 0.80`
- Legacy THCV-gate (`dual < THCV` y gap vs THC > 0.40): **informativo** — demasiado fácil en scaffolds sintéticos; **no** decide este lote
- MD / OpenMM: **pausada** (solo docking CPU)

**Resultado agregado:** rank-gate **3/11**; legacy THCV-gate 5/11 (no decisivo). Exhaustiveness=10; seed=42.

## Compound 14 SMILES

- **Estado:** reconstrucción desde descriptores publicados (N1-2-morfolinofenilo, C3-adamantilo, C4-Me, C5-Ph); **sin CID PubChem / depósito ChEMBL** en esta recuperación.
- Ki/IC₅₀ de la tabla experimental: **no recuperados** (no inventados).
- ID de panel: `QIU_14`. Análogos mínimos: `QIU_01`–`QIU_07`.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs URB447 | gap vs THC | rank-gate | legacy THCV |
|----|-----------|---------------|-----|-----|------|-----------|------------|-----------|-------------|
| QIU_14 | QIU14_ortho_morpholine | sí | -8.456 | -10.419 | -9.438 | 1.011 | 0.216 | fail | fail |
| QIU_01 | QIU_para_morpholine_negctrl | sí | -10.202 | -11.933 | -11.067 | -0.619 | 1.846 | PASS | PASS |
| QIU_02 | QIU_meta_morpholine | sí | -9.265 | -13.167 | -11.216 | -0.768 | 1.995 | PASS | PASS |
| QIU_03 | QIU_no_morpholine | sí | -9.286 | -12.061 | -10.674 | -0.226 | 1.453 | PASS | PASS |
| QIU_04 | QIU_C5_pCl | sí | -5.185 | -9.687 | -7.436 | 3.012 | -1.785 | fail | fail |
| QIU_05 | QIU_C4_H | sí | -7.656 | -11.524 | -9.590 | 0.858 | 0.369 | fail | fail |
| QIU_06 | QIU_ortho_piperidine | sí | -7.326 | -10.886 | -9.106 | 1.342 | -0.115 | fail | fail |
| QIU_07 | QIU_C3_cyclohexyl | sí | -7.929 | -9.406 | -8.668 | 1.780 | -0.553 | fail | fail |
| URB447 | URB447_seed | sí | -9.274 | -11.622 | -10.448 | 0.000 | 1.227 | fail | PASS |
| GW405833 | YY_GW405833 | sí | -9.928 | -9.994 | -9.961 | 0.487 | 0.740 | fail | PASS |
| AM1710 | YY_AM1710 | sí | -8.271 | -10.010 | -9.140 | 1.308 | -0.081 | fail | fail |
| delta9-THCV | REF | sí | -8.827 | -9.886 | -9.357 | 1.091 | 0.136 | ref | ref |
| delta9-THC | REF | sí | -8.383 | -10.059 | -9.221 | 1.227 | 0.000 | ref | ref |

## Ranking por dual (vs URB447; sin SMILES)

- Rank-gate PASS: **3** · evaluados: **11** · dual_URB447=-10.448 · umbral gap vs THC > 0.80

| rank | ID | hipótesis | CB1 | CB2 | dual | vs URB447 | gap vs THC | rank-gate |
|------|----|-----------|-----|-----|------|-----------|------------|-----------|
| 1 | QIU_02 | QIU_meta_morpholine | -9.265 | -13.167 | -11.216 | -0.768 | 1.995 | PASS |
| 2 | QIU_01 | QIU_para_morpholine_negctrl | -10.202 | -11.933 | -11.067 | -0.619 | 1.846 | PASS |
| 3 | QIU_03 | QIU_no_morpholine | -9.286 | -12.061 | -10.674 | -0.226 | 1.453 | PASS |
| 4 | URB447 | URB447_seed | -9.274 | -11.622 | -10.448 | 0.000 | 1.227 | fail |
| 5 | GW405833 | YY_GW405833 | -9.928 | -9.994 | -9.961 | 0.487 | 0.740 | fail |
| 6 | QIU_05 | QIU_C4_H | -7.656 | -11.524 | -9.590 | 0.858 | 0.369 | fail |
| 7 | QIU_14 | QIU14_ortho_morpholine | -8.456 | -10.419 | -9.438 | 1.011 | 0.216 | fail |
| 8 | AM1710 | YY_AM1710 | -8.271 | -10.010 | -9.140 | 1.308 | -0.081 | fail |
| 9 | QIU_06 | QIU_ortho_piperidine | -7.326 | -10.886 | -9.106 | 1.342 | -0.115 | fail |
| 10 | QIU_07 | QIU_C3_cyclohexyl | -7.929 | -9.406 | -8.668 | 1.780 | -0.553 | fail |
| 11 | QIU_04 | QIU_C5_pCl | -5.185 | -9.687 | -7.436 | 3.012 | -1.785 | fail |

## IDs rank-gate PASS

1. `QIU_02` — dual=-11.216, vs URB447=-0.768, gap vs THC=1.995
2. `QIU_01` — dual=-11.067, vs URB447=-0.619, gap vs THC=1.846
3. `QIU_03` — dual=-10.674, vs URB447=-0.226, gap vs THC=1.453


## Veredicto

**Resultado Qiu Batch 1 (docking only; MD pausada):** rank-gate (dual < URB447=-10.448 **y** gap vs THC > 0.80): **3/11**. Legacy THCV-gate (informativo, fácil en sintéticos): 5/11. Top por dual: QIU_02 (dual=-11.216, ΔURB=-0.768, gapTHC=1.995), QIU_01 (dual=-11.067, ΔURB=-0.619, gapTHC=1.846), QIU_03 (dual=-10.674, ΔURB=-0.226, gapTHC=1.453), URB447 (dual=-10.448, ΔURB=0.000, gapTHC=1.227), GW405833 (dual=-9.961, ΔURB=0.487, gapTHC=0.740). **QIU_14 (Compound 14 reconstruido):** dual=-9.438, vs URB447=1.011, gap vs THC=0.216; rank-gate=fail (legacy THCV-gate=fail). SMILES Compound 14 = reconstrucción desde descriptores publicados (sin CID PubChem/ChEMBL). Vina ≠ Janus funcional. **OpenMM/MD no lanzada.**

## IP

- CSV/SDF/PDBQT de panel: gitignored (`data/libraries/qiu_pyrazole*`, `results/docking/qiu_pyrazole*`, `results/hits/qiu_pyrazole*`).
- Detalle con SMILES (local): `results/hits/qiu_pyrazole_batch1/gate_detail.md`.
- Plan Qiu: [`next_iter_pyrazole_qiu_plan.md`](next_iter_pyrazole_qiu_plan.md); D2_22 descartado: [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md); MD pausada.


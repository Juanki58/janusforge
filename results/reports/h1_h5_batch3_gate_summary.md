# Iteración 3 — refino JANUS_H1_02 (1′-Me) — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

- Fecha: 2026-08-06
- Panel local: `data/libraries/h1_h5_batch3.csv` (gitignored)
- Scores: `results/docking/h1_h5_batch3/retrospective_scores.csv` (gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=12; seed=42

## Métrica de gate duro

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Referencias en el mismo run: dual_THCV = **-9.392**, dual_THC = **-9.196**, gap THCV−THC = **-0.196** kcal/mol
- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > 0.40` (claramente > separación THCV–THC ≈ 0.20)

**Resultado agregado:** 5/7 candidatos de diseño pasaron el gate. Exhaustiveness=12; seed=42.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |
|----|-----------|---------------|-----|-----|------|---------|--------|-------------|
| delta9-THCV | REF | sí | -8.924 | -9.859 | -9.392 | 0.000 | -0.196 | ref |
| delta9-THC | REF | sí | -8.338 | -10.054 | -9.196 | 0.196 | 0.000 | ref |
| JANUS_H1_02 | H1_02 control | sí | -9.303 | -10.254 | -9.779 | -0.387 | -0.583 | PASS |
| JANUS_H1_02a | H1_02a ω-F | sí | -9.245 | -10.179 | -9.712 | -0.320 | -0.516 | PASS |
| JANUS_H1_02b | H1_02b ether | sí | -9.186 | -9.847 | -9.517 | -0.125 | -0.321 | fail |
| JANUS_H1_02c | H1_02c chain bioisostere | sí | -9.524 | -10.581 | -10.052 | -0.661 | -0.856 | PASS |
| JANUS_H1_02d | H1_02d strategic F | sí | -8.972 | -10.258 | -9.615 | -0.223 | -0.419 | PASS |
| JANUS_H1_02e | H1_02e phenol bioisostere | sí | -8.843 | -9.496 | -9.169 | 0.222 | 0.027 | fail |
| JANUS_H1_02f | H1_02f short chain | sí | -9.317 | -10.179 | -9.748 | -0.357 | -0.552 | PASS |

## Aspiración (informativa)

- Gap vs THC > ~0.80 kcal/mol: JANUS_H1_02c


## Veredicto

**5/7 PASS** (H1_02 control, 02a ω-F, **02c** bioisóstero de cadena, 02d F en rama, 02f cadena corta). Éteres de fenol (02b OMe, 02e OEt) fallan: 02e empeora dual vs THCV; 02b gana a THCV pero gap vs THC 0.32 < 0.40.

**Crítico vs H1_02:** solo **JANUS_H1_02c** mejora dual (−10.052 vs −9.779) y es el único con gap vs THC **0.856 > 0.80** (aspiración). ω-F / F-rama / cadena corta PASS pero no superan al control. Mantener periferia **sin** ácidos sigue validado (ningún colapso CB1 tipo Batch 2). Vina ≠ Janus; gates funcionales abiertos.

## Lead #1 in silico: JANUS_H1_02c

**Selección:** único diseño que mejora dual vs control H1_02 y alcanza la aspiración gap vs THC **0.856** kcal/mol.

Matices (no sobreinterpretar):

- El gap **0.856 es proxy Vina** (ocupación/afinidad de pose), no evidencia de agonismo ni de Janus α.
- **Éteres de fenol fallan** (02b/02e): enmascarar el OH no es el camino en este panel.
- **ω-F (02a) PASS** y mejora vs THCV, pero **no bate** al control H1_02 ni a 02c.
- **Siguiente paso = MD** en CB1 inactivo 5TGZ: lead vs Δ9-THCV (¿1′-metilo como trinquete geométrico?). Protocolo y limitaciones: [`md_lead_plan.md`](md_lead_plan.md). Script: `scripts/run_md_openmm_lead.py`.
- Nota: **Vina ≠ α**; una MD corta en agua (sin membrana) tampoco prueba agonismo — solo estabilidad geométrica del estado inactivo.

## Lecciones técnicas

- Extremo de cadena no polar (bioisóstero tipo 02c) amplifica el gap proxy vs THC sin tocar anillo A ácido.
- Enmascarar fenol (OMe/OEt) no ayuda — o empata flojo o pierde dual.
- 1′-Me como eje se confirma: control H1_02 vuelve a PASS en el mismo protocolo exh=12/seed=42.

## IP

- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- MD local: `results/md/` (gitignored); sin estructuras en informes públicos.
- Detalle con SMILES (local): `results/hits/h1_h5_batch3/gate_detail.md`.
- Historial: [`h1_h5_design_history.md`](h1_h5_design_history.md).


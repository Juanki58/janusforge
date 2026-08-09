# Opción D — panel sintético URB447 / Yin-Yang (Batch 1) — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

- Fecha: 2026-08-10
- Panel local: `data/libraries/option_d_batch1.csv` (gitignored)
- Scores: `results/docking/option_d_batch1/retrospective_scores.csv` (gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=12; seed=42

## Métrica de gate duro

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Referencias en el mismo run: dual_THCV = **-9.450**, dual_THC = **-9.321**, gap THCV−THC = **-0.129** kcal/mol
- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > 0.40` (claramente > separación THCV–THC ≈ 0.20)

**Resultado agregado:** 3/4 ligandos evaluados (sintéticos / ex-lead) pasaron el gate. Exhaustiveness=12; seed=42.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |
|----|-----------|---------------|-----|-----|------|---------|--------|-------------|
| URB447 | URB447_seed | sí | -9.543 | -11.703 | -10.623 | -1.173 | -1.302 | PASS |
| AM1710 | YY_AM1710 | sí | -8.079 | -10.115 | -9.097 | 0.352 | 0.224 | fail |
| GW405833 | YY_GW405833 | sí | -10.157 | -9.932 | -10.044 | -0.595 | -0.723 | PASS |
| delta9-THCV | REF | sí | -9.039 | -9.860 | -9.450 | 0.000 | -0.129 | ref |
| delta9-THC | REF | sí | -8.603 | -10.039 | -9.321 | 0.129 | 0.000 | ref |
| JANUS_H1_02c | H1_02c_exlead | sí | -9.445 | -10.958 | -10.201 | -0.752 | -0.880 | PASS |

## Aspiración (informativa)

- Gap vs THC > ~0.80 kcal/mol: URB447, JANUS_H1_02c


## Veredicto

**Resultado:** 3/4 PASS (URB447, GW405833, JANUS_H1_02c). Sintéticos publicados evaluados: URB447, AM1710, GW405833; PASS: URB447, GW405833. **Ex-lead fitocannabinoide H1_02c:** dual=-10.201, gap vs THC=0.880 (PASS en este run) — contexto post NO-GO MD membrana; no reabre Track 1 como eje. **URB447 (semilla sintética Track D):** dual=-10.623, gap vs THC=1.302 (PASS). Umbrales = mismos que H1–H5 (dual < THCV y gap vs THC > 0.40). Vina = afinidad/pose proxy; **no** éxito Janus funcional. Qiu 2023 citado en docs, sin SMILES en panel (estructura no en PubChem fiable).

## IP

- CSV/SDF/PDBQT de panel: gitignored (`data/libraries/option_d*`, `results/docking/option_d*`, `results/hits/option_d*`).
- Detalle con SMILES (local): `results/hits/option_d_batch1/gate_detail.md`.
- Pivot Track D: [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md); NO-GO membrana: [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md).


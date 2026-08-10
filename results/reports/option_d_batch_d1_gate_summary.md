# Opción D — Batch D1 (derivados URB447 / Yin-Yang) — gate summary (public)

> **No SMILES.** Structures and pose files stay local/gitignored. Vina = affinity/pose proxy only — not functional Janus success (see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

- Fecha: 2026-08-10
- **Alias:** Batch D1 = cribado de **derivados** URB447 / Yin-Yang (IDs `JANUS_D2_*` + seeds URB447 / GW405833 + refs THCV / THC)
- **Fuente reutilizada:** panel/scores de `option_d_batch2` (docking CPU ya completo; **no** se rehizo Vina)
- Panel local: `data/libraries/option_d_batch2.csv` (gitignored)
- Scores: `results/docking/option_d_batch2/retrospective_scores.csv` (gitignored)
- Poses: `results/docking/option_d_batch2/{cb1,cb2}/` (36+36 docked; gitignored)
- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness=8; seed=42
- **Lead Opción D (confirmado 2026-08-10):** **JANUS_D2_22** (Bz_pCF3; dual=−11.277)
- **MD / OpenMM: PAUSADA** (calor / decisión explícita pendiente) — **no** lanzar 20 ns POPC ni OpenMM hasta reabrir

Informe técnico hermano (mismo run): [`option_d_batch2_gate_summary.md`](option_d_batch2_gate_summary.md).

## Métrica de gate duro

- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)
- Referencias en el mismo run: dual_THCV = **-9.416**, dual_THC = **-9.188**, gap THCV−THC = **-0.228** kcal/mol
- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > 0.40` (claramente > separación THCV–THC ≈ 0.20)

**Resultado agregado:** 34/34 ligandos evaluados (sintéticos / derivados / seeds) pasaron el gate. Exhaustiveness=8; seed=42.

## Tabla (IDs + scores; sin SMILES)

| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |
|----|-----------|---------------|-----|-----|------|---------|--------|-------------|
| URB447 | URB447_seed | sí | -9.731 | -11.660 | -10.695 | -1.279 | -1.507 | PASS |
| GW405833 | YY_GW405833 | sí | -10.002 | -10.064 | -10.033 | -0.617 | -0.845 | PASS |
| delta9-THCV | REF | sí | -8.973 | -9.859 | -9.416 | 0.000 | -0.228 | ref |
| delta9-THC | REF | sí | -8.338 | -10.039 | -9.188 | 0.228 | 0.000 | ref |
| JANUS_D2_01 | NBn_pF | sí | -9.653 | -12.060 | -10.857 | -1.441 | -1.668 | PASS |
| JANUS_D2_02 | NBn_pBr | sí | -8.968 | -11.615 | -10.291 | -0.875 | -1.103 | PASS |
| JANUS_D2_03 | NBn_pMe | sí | -9.731 | -12.081 | -10.906 | -1.490 | -1.717 | PASS |
| JANUS_D2_04 | NBn_pOMe | sí | -9.419 | -11.612 | -10.515 | -1.099 | -1.327 | PASS |
| JANUS_D2_05 | NBn_pCF3 | sí | -10.134 | -12.168 | -11.151 | -1.735 | -1.963 | PASS |
| JANUS_D2_06 | NBn_pCN | sí | -9.523 | -12.030 | -10.776 | -1.360 | -1.588 | PASS |
| JANUS_D2_07 | NBn_H | sí | -9.689 | -11.816 | -10.753 | -1.337 | -1.564 | PASS |
| JANUS_D2_08 | NBn_mCl | sí | -9.538 | -11.449 | -10.494 | -1.078 | -1.305 | PASS |
| JANUS_D2_09 | NBn_oCl | sí | -9.536 | -10.970 | -10.253 | -0.837 | -1.065 | PASS |
| JANUS_D2_10 | N_phenethyl | sí | -10.190 | -12.098 | -11.144 | -1.728 | -1.956 | PASS |
| JANUS_D2_11 | C5_Et | sí | -9.639 | -11.402 | -10.520 | -1.104 | -1.332 | PASS |
| JANUS_D2_12 | C5_nPr | sí | -9.206 | -11.481 | -10.343 | -0.927 | -1.155 | PASS |
| JANUS_D2_13 | C5_iPr | sí | -9.512 | -11.273 | -10.393 | -0.976 | -1.204 | PASS |
| JANUS_D2_14 | C5_H | sí | -9.116 | -11.254 | -10.185 | -0.769 | -0.996 | PASS |
| JANUS_D2_15 | C5_CF3 | sí | -10.497 | -11.698 | -11.098 | -1.681 | -1.909 | PASS |
| JANUS_D2_16 | NHMe | sí | -9.465 | -10.919 | -10.192 | -0.776 | -1.004 | PASS |
| JANUS_D2_17 | NMe2 | sí | -9.112 | -10.170 | -9.641 | -0.225 | -0.453 | PASS |
| JANUS_D2_18 | Bz_pF | sí | -9.996 | -11.557 | -10.777 | -1.361 | -1.588 | PASS |
| JANUS_D2_19 | Bz_pCl | sí | -10.001 | -11.510 | -10.755 | -1.339 | -1.567 | PASS |
| JANUS_D2_20 | Bz_pMe | sí | -10.052 | -11.656 | -10.854 | -1.438 | -1.665 | PASS |
| JANUS_D2_21 | Bz_pOMe | sí | -9.652 | -11.185 | -10.418 | -1.002 | -1.230 | PASS |
| JANUS_D2_22 | Bz_pCF3 | sí | -10.205 | -12.350 | -11.277 | -1.861 | -2.089 | PASS |
| JANUS_D2_23 | C2Ph_pF | sí | -9.720 | -11.892 | -10.806 | -1.390 | -1.618 | PASS |
| JANUS_D2_24 | C2Ph_pCl | sí | -9.808 | -11.266 | -10.537 | -1.121 | -1.348 | PASS |
| JANUS_D2_25 | C2Ph_pMe | sí | -10.016 | -11.334 | -10.675 | -1.259 | -1.487 | PASS |
| JANUS_D2_26 | C2Ph_pOMe | sí | -9.638 | -10.609 | -10.123 | -0.707 | -0.935 | PASS |
| JANUS_D2_27 | NBn_pF_C5Et | sí | -10.107 | -11.637 | -10.872 | -1.456 | -1.684 | PASS |
| JANUS_D2_28 | NBn_pMe_NHMe | sí | -9.430 | -11.058 | -10.244 | -0.828 | -1.056 | PASS |
| JANUS_D2_29 | NBn_pF_Bz_pF | sí | -9.910 | -12.015 | -10.963 | -1.546 | -1.774 | PASS |
| JANUS_D2_30 | C5_CH2OH | sí | -9.363 | -11.063 | -10.213 | -0.797 | -1.025 | PASS |
| JANUS_D2_31 | NBn_pF_NHMe | sí | -9.069 | -11.312 | -10.191 | -0.774 | -1.002 | PASS |
| JANUS_D2_32 | Bz_pF_C5Et | sí | -10.336 | -11.529 | -10.933 | -1.517 | -1.744 | PASS |

## Top PASS (rank por dual; sin SMILES)

- PASS: **34** · fail: **0** · evaluados: **34**

| rank | ID | hipótesis | CB1 | CB2 | dual | gap vs THC |
|------|----|-----------|-----|-----|------|------------|
| 1 | JANUS_D2_22 | Bz_pCF3 | -10.205 | -12.350 | -11.277 | 2.089 |
| 2 | JANUS_D2_05 | NBn_pCF3 | -10.134 | -12.168 | -11.151 | 1.963 |
| 3 | JANUS_D2_10 | N_phenethyl | -10.190 | -12.098 | -11.144 | 1.956 |
| 4 | JANUS_D2_15 | C5_CF3 | -10.497 | -11.698 | -11.098 | 1.909 |
| 5 | JANUS_D2_29 | NBn_pF_Bz_pF | -9.910 | -12.015 | -10.963 | 1.774 |
| 6 | JANUS_D2_32 | Bz_pF_C5Et | -10.336 | -11.529 | -10.933 | 1.744 |
| 7 | JANUS_D2_03 | NBn_pMe | -9.731 | -12.081 | -10.906 | 1.717 |
| 8 | JANUS_D2_27 | NBn_pF_C5Et | -10.107 | -11.637 | -10.872 | 1.684 |
| 9 | JANUS_D2_01 | NBn_pF | -9.653 | -12.060 | -10.857 | 1.668 |
| 10 | JANUS_D2_20 | Bz_pMe | -10.052 | -11.656 | -10.854 | 1.665 |

## IDs filtrados (PASS) rankeados por dual

1. `JANUS_D2_22` — dual=-11.277, gap vs THC=2.089
2. `JANUS_D2_05` — dual=-11.151, gap vs THC=1.963
3. `JANUS_D2_10` — dual=-11.144, gap vs THC=1.956
4. `JANUS_D2_15` — dual=-11.098, gap vs THC=1.909
5. `JANUS_D2_29` — dual=-10.963, gap vs THC=1.774
6. `JANUS_D2_32` — dual=-10.933, gap vs THC=1.744
7. `JANUS_D2_03` — dual=-10.906, gap vs THC=1.717
8. `JANUS_D2_27` — dual=-10.872, gap vs THC=1.684
9. `JANUS_D2_01` — dual=-10.857, gap vs THC=1.668
10. `JANUS_D2_20` — dual=-10.854, gap vs THC=1.665
11. `JANUS_D2_23` — dual=-10.806, gap vs THC=1.618
12. `JANUS_D2_18` — dual=-10.777, gap vs THC=1.588
13. `JANUS_D2_06` — dual=-10.776, gap vs THC=1.588
14. `JANUS_D2_19` — dual=-10.755, gap vs THC=1.567
15. `JANUS_D2_07` — dual=-10.753, gap vs THC=1.564
16. `URB447` — dual=-10.695, gap vs THC=1.507
17. `JANUS_D2_25` — dual=-10.675, gap vs THC=1.487
18. `JANUS_D2_24` — dual=-10.537, gap vs THC=1.348
19. `JANUS_D2_11` — dual=-10.520, gap vs THC=1.332
20. `JANUS_D2_04` — dual=-10.515, gap vs THC=1.327
21. `JANUS_D2_08` — dual=-10.494, gap vs THC=1.305
22. `JANUS_D2_21` — dual=-10.418, gap vs THC=1.230
23. `JANUS_D2_13` — dual=-10.393, gap vs THC=1.204
24. `JANUS_D2_12` — dual=-10.343, gap vs THC=1.155
25. `JANUS_D2_02` — dual=-10.291, gap vs THC=1.103
26. `JANUS_D2_09` — dual=-10.253, gap vs THC=1.065
27. `JANUS_D2_28` — dual=-10.244, gap vs THC=1.056
28. `JANUS_D2_30` — dual=-10.213, gap vs THC=1.025
29. `JANUS_D2_16` — dual=-10.192, gap vs THC=1.004
30. `JANUS_D2_31` — dual=-10.191, gap vs THC=1.002
31. `JANUS_D2_14` — dual=-10.185, gap vs THC=0.996
32. `JANUS_D2_26` — dual=-10.123, gap vs THC=0.935
33. `GW405833` — dual=-10.033, gap vs THC=0.845
34. `JANUS_D2_17` — dual=-9.641, gap vs THC=0.453

## Veredicto

**Batch D1 (derivados URB447 / Yin-Yang):** cribado docking CPU dual CB1/CB2 **completado** reutilizando el run `option_d_batch2` (36 ligandos docked × 2 receptores; exh=8). Gate: 34/34 PASS; 0 fail. **Lead = JANUS_D2_22** (dual=−11.277); runners-up: JANUS_D2_05 (−11.151), JANUS_D2_10 (−11.144), JANUS_D2_15 (−11.098), JANUS_D2_29 (−10.963). Semilla URB447: dual=−10.695 (PASS). **MD membrana / OpenMM diferida** hasta decisión explícita (GPU pesada en pausa). Vina = afinidad/pose proxy; **no** éxito Janus funcional. Poses locales gitignored bajo `results/docking/option_d_batch2/{cb1,cb2}/` (visor: Re-escanear).

## IP

- CSV/SDF/PDBQT de panel: gitignored (`data/libraries/option_d*`, `results/docking/option_d*`, `results/hits/option_d*`).
- Detalle con SMILES (local): `results/hits/option_d_batch2/gate_detail.md`.
- Pivot Track D: [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md); NO-GO membrana: [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md).

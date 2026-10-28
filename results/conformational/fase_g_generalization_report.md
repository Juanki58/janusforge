# Phase G — Generalización out-of-sample 8GUR (CB2)

**Generado:** 2026-08-19 10:11 UTC  
**Rama:** `feat/fase-g-conformational-validation`

## Bloque de gobernanza

```yaml
PHASE_G: COMPLETE
CONTRACT_v1.0: FROZEN
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION
EXPLORATORY_DELTA_CUTOFF: documented_as_exploratory_only
```

## Level-0 — 8GUR

- **Verificación:** PASS
- **PDB:** 8GUR (2.84 Å cryo-EM)
- **Receptor:** CB2 cadena `R`
- **Ligando:** CP55,940 (9GF) (retirado para huella conformacional)
- **Estado:** active_agonist_cp55940_gi

## Q1 — ¿El coordinate separa activo/inactivo out-of-sample?

**Veredicto Q1:** **GENERALIZES**

> 8GUR (2.321) clusters with active refs (mean 2.302, max 2.302) and separates from 5ZTY (3.950); Δ(blind→inactive)=1.630 norm units.

### Distancias CB2_STATE_DISTANCE (espacio CB2 normalizado; centroide activo 6PT0+6KPF)

| PDB | Estado | Distancia (norm) | Distancia (raw) |
|-----|--------|------------------|-----------------|
| 6PT0 | active_agonist_win_gi | 2.3019 | 50.0552 |
| 6KPF | active_agonist_cryoem | 2.3019 | 50.0552 |
| 8GUR **blind** | active_agonist_cp55940_gi | 2.3205 | 37.0292 |
| 5ZTY | inactive_antagonist_am10257 | 3.9501 | 73.6374 |

### Métricas conformacionales (raw)

| PDB | TM3–TM6 IC (Å) | TM3–TM5 disp (Å) | Trp258 χ1 (°) | Trp258 χ2 (°) | Ser268 χ1 (°) | Phe183 disp (Å) | Phe183 tilt (°) |
|-----|---------------|------------------|---------------|---------------|---------------|-----------------|-----------------|
| 6PT0 | 15.3343 | 14.1979 | 105.2525 | -87.928 | -37.0916 | 0.0 | 59.0214 |
| 6KPF | 14.796 | 14.0337 | 80.8281 | -65.4814 | -126.1712 | 27.3566 | 43.5999 |
| 8GUR | 14.4229 | 13.9035 | 95.3914 | -68.1782 | -115.2557 | 4.4421 | 60.0615 |
| 5ZTY | 10.2797 | 13.8586 | 107.1005 | -134.1433 | -39.026 | 20.1205 | 58.0848 |

### Cutoff exploratorio (NO confirmatorio): Δ ≥ 2.0 Å vs 6PT0

| PDB | Δ TM3–TM6 | Δ TM3–TM5 | Δ Trp258 χ1 | Δ Ser268 χ1 | Δ Phe183 disp |
|-----|-----------|-----------|-------------|-------------|---------------|
| 6PT0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 6KPF | -0.5383 | -0.1642 | -24.4244 | -89.0796 | 27.3566 |
| 8GUR | -0.9114 | -0.2944 | -9.8611 | -78.1641 | 4.4421 |
| 5ZTY | -5.0546 | -0.3393 | 1.848 | -1.9344 | 20.1205 |

> Δ ≥ 2.0 Å (or any numeric cutoff) is EXPLORATORY only; not used as confirmatory validation evidence.

## Q2 — Leave-one-out (centroide 6PT0 solo)

**Veredicto Q2:** **PARTIAL**

> Trend preserved (blind 3.089 < inactive 4.080) but margin vs 6KPF (4.604) not robust under LOO.

| PDB | Distancia LOO (norm) | Rol |
|-----|----------------------|-----|
| 6KPF | 4.6039 | blind (active ref held out) |
| 8GUR | 3.089 | blind OOS |
| 5ZTY | 4.0805 | negativo |

## Q3 — THCV (sonda mecanística; NO prueba funcional)

- Fuente: `C:\Users\juanc\projects\janusforge\results\docking\thcv_seed\thcv_seed_evaluation.json`
- **CB2:** estado docked = 6PT0 (active agonist)
  - Afinidad: -9.857 kcal/mol
  - Microswitches pose: {'Phe117(3.32)': 3.7, 'Trp258(6.48)': 5.91, 'Ser285(7.39)': 4.04}
  - Sonda mecanística ONLY — pose docked contra 6PT0 activo; NO prueba funcional agonista/antagonista/modulador.
- **CB1:** estado docked = 5TGZ (inactive antagonist-bound)
  - Afinidad: -8.964 kcal/mol
  - Microswitches pose: {'Phe200(3.36)': 6.95, 'Trp356(6.48)': 3.72}
  - Espacio CB1 separado — docked contra 5TGZ inactivo; NO comparable numéricamente a distancias CB2.

## CB1 cross-reference (espacio normalizado SEPARADO)

> Separate normalized CB1 coordinate space — NOT comparable to CB2 distances.

| PDB | Estado | Distancia CB1 (norm vs 5XRA activo) |
|-----|--------|-------------------------------------|
| 5TGZ | inactive_antagonist_am6538 | 4.899 |
| 5XRA | active_agonist_am11542 | 0.0 |

## Alineamiento TM (Level-0 infra)

| PDB | TM Cα pares | RMSD post (Å) | Cadena |
|-----|-------------|---------------|--------|
| 6PT0 | 178 | 0.0 | R |
| 6KPF | 178 | 22.406 | R |
| 5ZTY | 178 | 15.202 | A |
| 8GUR | 178 | 3.511 | R |

## Scripts

- `scripts/conformational/evaluate_8gur_generalization.py`
- `scripts/conformational/align_multistate.py`

# Micronetwork local modes — HU-308 vs HU-433

**Generado:** 2026-08-20T08:03:57.768384+00:00  
**Branch:** `feat/micronetwork-falsification-test`

**Pregunta primaria:** ¿HU-308 y HU-433 presentan microdescriptores locales reproduciblemente diferentes?

**Enlace falsificación previa:** [`results\conformational\micronetwork_falsification_report.md`](results\conformational\micronetwork_falsification_report.md)

## Veredicto definitivo

**`INDETERMINATE`**

*State disagreement (plasticity): 6PT0=IDENTICAL_LOCAL_MODES, 6KPF=DISTINCT_LOCAL_MODES. Difference in one state not reproduced in the other.*

## Criterios congelados (resolución estructural, no incertidumbre de docking)

| Criterio | Regla |
|----------|-------|
| DISTINCT_LOCAL_MODES | Δd > 0.3 Å en ≥2 componentes de distancia **o** Δtorsion > 10.0° |
| IDENTICAL_LOCAL_MODES | Ningún criterio cumplido |
| INDETERMINATE | Poses ausentes o discrepancia entre 6PT0 y 6KPF |

## LOCAL_MICROSWITCH_VECTOR por sonda y estado

| Estado | Sonda | Pose | dist_Trp258 (Å) | dist_Phe183 (Å) | dist_Ser285 (Å) | torsion_Trp258 (°) |
|--------|-------|------|-----------------|-----------------|-----------------|-------------------|
| 6PT0 | HU-308 | `data\docking_poses\micronetwork_test\6PT0\HU-308\HU-308_docked.pdbqt` | 5.15 | 4.53 | 3.33 | 0.00 |
| 6PT0 | HU-433 | `data\docking_poses\micronetwork_test\6PT0\HU-433\HU-433_docked.pdbqt` | 6.47 | 4.28 | 3.06 | 0.00 |
| 6KPF | HU-308 | `data\docking_poses\micronetwork_test\6KPF\HU-308\HU-308_docked.pdbqt` | 4.20 | 4.20 | 2.70 | 33.14 |
| 6KPF | HU-433 | `data\docking_poses\micronetwork_test\6KPF\HU-433\HU-433_docked.pdbqt` | 4.51 | 4.44 | 3.06 | 33.14 |

## Comparación HU-308 vs HU-433 por estado

### 6PT0
- **Veredicto estado:** `IDENTICAL_LOCAL_MODES`
- Δdist_Trp258 = 1.3238 Å
- Δdist_Phe183 = 0.2498 Å
- Δdist_Ser285 = 0.2724 Å
- Δtorsion_Trp258 = 0.0°
- Componentes dist > 0.3 Å: 1

### 6KPF
- **Veredicto estado:** `DISTINCT_LOCAL_MODES`
- Δdist_Trp258 = 0.3153 Å
- Δdist_Phe183 = 0.2392 Å
- Δdist_Ser285 = 0.3605 Å
- Δtorsion_Trp258 = 0.0°
- Componentes dist > 0.3 Å: 2

## Controles co-cristal (vectores de referencia, sin re-dock)

| Control | dist_Trp258 | dist_Phe183 | dist_Ser285 | torsion_Trp258 |
|---------|-------------|-------------|-------------|----------------|
| 6PT0 | 4.92 | 4.21 | 3.35 | 0.00 |
| 6KPF | 3.87 | 3.86 | 3.07 | 33.14 |
| 8GUR_CP55940 | 4.89 | 4.55 | 2.61 | 22.03 |
| 5ZTY_AM10257 | 3.91 | 4.16 | 4.49 | 46.24 |

## Scripts

- `scripts/run_micronetwork_directed_dock.py`
- `scripts/conformational/test_micronetwork_modes.py`

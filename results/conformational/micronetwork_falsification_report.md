# Test de falsificación de microred — Par enantiomérico HU-308 / HU-433

**Generado:** 2026-08-19T12:57:02.006691+00:00  
**Branch:** `feat/micronetwork-falsification-test`

## Candados de gobernanza

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
CONTRACT_v1.0: FROZEN
DESCRIPTOR_FROZEN_BEFORE_EXECUTION: true
```

## Definición del descriptor (congelado pre-ejecución)

```
LOCAL_MICROSWITCH_VECTOR = [
  dist_Trp258,    # dist mín átomos pesados ligando → anillo indol Trp258^6.48 (Å)
  dist_Phe183,    # dist centroide ligando → centroide anillo aromático Phe183^ECL2 (Å)
  dist_Ser285,    # dist mín átomos pesados ligando → O hidroxilo Ser285^7.39 (Å)
  torsion_Trp258  # desviación chi1/chi2 cadena lateral Trp258 vs pose canónica 6PT0 (°)
]
```

## Procedencia de σ

**Método:** Option B: half-range of 6PT0 vs 6KPF co-crystallised ligand descriptors

**Limitación:** 6PT0 (WIN55,212-2) and 6KPF (AM12033) are different ligands; σ includes ligand-identity variance → conservative (overestimates σ)

| Componente | σ estimada |
|------------|-----------|
| dist_Trp258_A | 0.5267 |
| dist_Phe183_A | 0.1742 |
| dist_Ser285_A | 0.1385 |
| torsion_Trp258_deg | 16.568 |

**N observaciones:** 2
**PDBs fuente:** 6PT0, 6KPF

## Pose canónica de referencia Trp258 (6PT0)

- chi1 = 105.25°
- chi2 = -87.93°

## LOCAL_MICROSWITCH_VECTOR por sonda

| Sonda | Rol | Estado | dist_Trp258 (Å) | dist_Phe183 (Å) | dist_Ser285 (Å) | torsion_Trp258 (°) |
|-------|-----|--------|-----------------|-----------------|-----------------|-------------------|
| 6PT0 | reference_agonist | COMPUTED | 4.92 | 4.21 | 3.35 | 0.00 |
| 6KPF | cross_check_agonist | COMPUTED | 3.87 | 3.86 | 3.07 | 33.14 |
| 8GUR | positive_control | COMPUTED | 4.89 | 4.55 | 2.61 | 22.03 |
| 5ZTY | negative_control | COMPUTED | 3.91 | 4.16 | 4.49 | 46.24 |
| HU-308 | primary_probe_A | NO_POSE_AVAILABLE | — | — | — | — |
| HU-433 | primary_probe_B | NO_POSE_AVAILABLE | — | — | — | — |

## Distancias de control entre sondas

| Par | Euclídea raw | Euclídea normalizada |
|-----|-------------|---------------------|
| 6PT0_vs_6KPF | 33.1558 | 3.9995 |
| 6PT0_vs_8GUR | 22.0459 | 5.8228 |
| 6PT0_vs_5ZTY | 46.2661 | 8.9284 |
| 6KPF_vs_8GUR | 11.1829 | 5.547 |
| 6KPF_vs_5ZTY | 13.1852 | 10.4284 |
| 8GUR_vs_5ZTY | 24.3059 | 13.9704 |

## Veredicto primario: D(HU-308, HU-433) vs umbral

**Veredicto: `INDETERMINATE`**

**Razón:** No docked poses available for HU-308 and/or HU-433. Cannot compute ΔV between enantiomers. Docking with Vina against 6PT0 (and cross-check on 6KPF) is required.

## Nota secundaria de farmacología

Contexto farmacológico documentado (NO usado como training truth): Trabajo reciente con derivados de HU-308 en CB2 encontró continua de actividad asociada con la interacción con Trp258^6.48. El paper original de HU-308/HU-433 (Mechoulam et al.) reportó que HU-433 tiene mucho menor afinidad hCB2 pero mayor potencia biológica en algunos modelos; diferencias en [35S]GTPγS no estadísticamente significativas; los autores propusieron orientaciones de unión diferentes. Estos datos contextualizan pero NO validan el descriptor.

## Nota de literatura

Este test conecta con evidencia externa: trabajo reciente con derivados de
HU-308 en CB2 encontró continua de actividad asociada con la interacción
Trp258^6.48. El paper original de HU-308/HU-433 reportó resultados
notablemente inusuales: HU-433 tiene mucho menor afinidad hCB2 pero mucho
mayor potencia biológica en algunos modelos; las diferencias en [35S]GTPγS
no fueron estadísticamente significativas; los autores propusieron
orientaciones de unión diferentes. Este contexto se documenta SIN tratarlo
como training truth.

## Razón explícita de INDETERMINATE

No existen poses dockeadas para HU-308 ni HU-433 en el repositorio.
El test requiere poses de Vina (o equivalente) contra 6PT0 como receptor
primario, con verificación cruzada en 6KPF. Las poses de los ligandos
co-cristalizados (WIN55,212-2 en 6PT0, AM12033 en 6KPF, CP55,940 en 8GUR,
AM10257 en 5ZTY) se computan como controles para validar la infraestructura
del descriptor.

### Pasos requeridos para resolver INDETERMINATE → veredicto definitivo

1. Preparar ligandos HU-308 y HU-433 (SMILES → 3D → PDBQT)
2. Docking Vina contra 6PT0_clean.pdb con grid configs/grid_cb2_6pt0.txt
3. Extraer best pose para cada enantiómero
4. Re-ejecutar este script (detectará poses automáticamente)
5. Verificación cruzada: repetir contra 6KPF

## Resolución posterior — docking dirigido HU-308/HU-433

Tras el veredicto INDETERMINATE inicial, se completó docking Vina dirigido
(exhaustiveness=16, seed=42) contra 6PT0 y 6KPF. Ver:

- [`micronetwork_modes_report.md`](micronetwork_modes_report.md)
- [`micronetwork_modes_report.json`](micronetwork_modes_report.json)

**Veredicto modos locales:** `INDETERMINATE` — discrepancia entre estados
(6PT0=IDENTICAL_LOCAL_MODES, 6KPF=DISTINCT_LOCAL_MODES); plasticidad conformacional.

## Scripts

- `scripts/conformational/test_micronetwork_falsification.py`
- `scripts/conformational/test_micronetwork_modes.py`
- `scripts/run_micronetwork_directed_dock.py`

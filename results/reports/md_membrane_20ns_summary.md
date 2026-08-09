# MD 20 ns — Membrane POPC: JANUS_H1_02c vs Δ9-THCV vs Δ9-THC on CB1 inactive (5TGZ)

> **Public report:** no SMILES, no coordinates. Trajectories / CSV / DCD / PDB stay local under `results/md/membrane/` (gitignored).  
> Script: [`scripts/run_md_openmm_membrane_lead.py`](../../scripts/run_md_openmm_membrane_lead.py) · plan: [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md) · prior soluble MD: [`md_lead_2ns_summary.md`](md_lead_2ns_summary.md)

## Setup (executed)

| Item | Value |
|------|--------|
| Receptor | 5TGZ CB1 chimera (same strip as soluble MD) |
| Ligands | JANUS_H1_02c, delta9-THCV, delta9-THC (Vina MODEL 1 poses) |
| Membrane | POPC bilayer (`amber14/lipid17`) + TIP3P + NaCl 0.15 M |
| FF | Protein `amber14-all`; ligand **GAFF2** (`gaff-2.11` via OpenFF) |
| Barostat | `MonteCarloMembraneBarostat` XY isotropic / Z free |
| Protocol | Min → NVT + NPT membrane equil ~1 ns → **NPT production 20.0 ns**, 300 K, seed 42 |
| Platform | OpenMM **CUDA** |
| Frames | 2000 / ligand |
| Status | **Batch membrane completo** — tres ligandos `status: ok` |

TM ranges (UniProt): TM3 185–220; TM6 332–369. RMSD vs minimized frame of each trajectory. Phenolic H-bond = % frames with ligand OH → protein O/N within 3.5 Å.

## Metrics (production 20 ns)

| Metric | JANUS_H1_02c | delta9-THCV | delta9-THC |
|--------|-------------:|------------:|-----------:|
| TM6 Cα RMSD mean ± sd (Å) | 1.31 ± 0.22 | **1.20 ± 0.22** | 1.22 ± 0.21 |
| TM6 Cα RMSD final (Å) | 1.46 | 1.48 | 1.73 |
| TM3–TM6 COM mean ± sd (Å) | **11.93 ± 0.30** | 13.07 ± 0.26 | 12.06 ± 0.26 |
| TM3–TM6 axis angle mean ± sd (°) | 12.98 ± 1.23 | 13.78 ± 1.10 | **10.04 ± 1.11** |
| Phenolic H-bond persistence (%) | 84.6 | **89.1** | 33.5 |

Sources: `results/md/membrane/<id>/metrics_summary.json` (and aggregate CSV local).

## Go / no-go vs plan

Criterios de [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md) (Track 1 → ensayo in vitro si GO):

| # | Criterio | Observado | Gate |
|---|----------|-----------|------|
| 1 | H1_02c congela TM6 (menor RMSD medio) **mejor que THCV** | Lead 1.31 > THCV 1.20 Å (≈igual sd) | **FAIL** |
| 2 | H1_02c restringe TM3–TM6 mejor que THCV | COM más cerrado: 11.93 vs 13.07 Å; ángulo ligeramente menor | **PASS** (parcial: distancia sí; fluctuación similar) |
| 3 | H1_02c recupera H-bond fenólico vs THCV | 84.6% vs 89.1% (mucho mejor que agua 55%, aún ≤ THCV) | **PARCIAL** |
| 4 | Patrón se diferencia de THC | Fenol claro (84.6 vs 33.5%); TM6 similar; COM casi igual a THC; ángulo THC *más cerrado*, no más abierto | **PARCIAL** |

**Veredicto gate: NO-GO** (no se cumple el paquete GO; el lead no mejora de forma consistente el panel vs THCV en membrana).

## Critical verdict — ¿trinquete? ¿H1_02c mejor que THCV y distinto de THC?

**No hay evidencia clara de trinquete térmico a favor de JANUS_H1_02c en este triplete 20 ns × 1 réplica.**

1. **Vs THCV:** el lead **no** congela mejor TM6 (RMSD medio peor/igual). Sí muestra TM3–TM6 más cerrado en media (~1.1 Å). El H-bond fenólico **se recupera** respecto a MD en agua (55% → 85%), pero sigue ligeramente por debajo de THCV (89%). En conjunto: **no es mejor que THCV** en el criterio compuesto del plan.
2. **Vs THC:** el fenol sí separa (agonista ~34% vs lead/THCV ~85–89%). Pero la geometría TM3–TM6 **no** muestra al agonista “abriendo” el pozo inactivo relativo al lead (COM casi idéntico; ángulo de ejes incluso menor en THC). Diferenciación parcial, no el patrón activación esperado.
3. **Conclusión operativa:** batch membrane completo → **NO-GO Track 1 computacional** según el plan: andamiaje fitocannabinoide (serie 1′-Me / H1_02c) **no gana** el gate de priorización frente a THCV en POPC. Evaluar **Opción D (URB447 / Yin-Yang)** o, si se insiste en Track 1, réplicas ≥3 / ventanas más largas antes de ensayo — no como “go” sino como exploración.

## Limitations (must read)

1. **1 réplica / 20 ns** — ruido térmico y sesgo de pose inicial; gate de priorización, no prueba funcional.
2. **Vina pose ≠ ensemble unido** — arranque docking.
3. **5TGZ quimera** (flavodoxina strip; ICL3 gap) ≠ CB1 nativo completo.
4. H-bond fenólico flexible (cualquier aceptor proteína), no fijado a S7.39.
5. Sin controles de integridad de membrana reportados aquí (área/lípido, thickness, RMSD lípido).
6. Patrón TM3–TM6 de THC no encaja con la expectativa “más abierto”; interpretar con cautela (timescale / métrica / quimera).

## Local artifacts (gitignored)

- Aggregate CSV: `results/md/membrane/h1_02c_vs_thcv_vs_thc_5tgz_popc.csv`
- Per ligand: `results/md/membrane/<id>/production.dcd`, `metrics_summary.json`, `frame_metrics.csv`, …

## Status

**Batch membrane completo (2026-08-09):** JANUS_H1_02c, delta9-THCV, delta9-THC — 20 ns OK cada uno. Informe gate: este archivo.

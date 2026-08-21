# P2 MSM convergence report — GPCRmd WT dyn2126

**Generated (UTC):** 2026-08-21T11:16:14Z
**Scope:** Stage-1 convergence ONLY (no A/B/C networks, no biology).
**Data:** Morales-Pastor / GPCRmd publication 1540 / dyn2126 (5 WT replicas).

## SHA256 verification

- Manifest: `data\external\morales_pastor_2025\trajectories\MANIFEST.json`
- All OK: **True**

## Software

- `numpy`: 2.4.6
- `scipy`: 1.18.0
- `sklearn`: 1.9.0
- `matplotlib`: 3.11.1
- `MDAnalysis`: 2.10.0
- `deeptime`: 0.4.5
- `mdtraj`: 1.11.1
- `python`: 3.12.13

## Featurization

- Type: pairwise Cα distances among TM1–TM7
- Numbering: **human CB2 UniProt (P34972) / GPCRdb spans**

- **TM1:** 31–56
- **TM2:** 67–91
- **TM3:** 107–132
- **TM4:** 148–172
- **TM5:** 193–217
- **TM6:** 239–264
- **TM7:** 276–300

- n_Cα: 178
- n_pairwise_features: 15753
- n_replicas: 5
- n_frames_total: 1995
- frames_per_replica: [399, 399, 399, 399, 399]

## Implied timescales

- **ITS verdict:** `NON_CONVERGENT`
- Detail: pathological ITS spectrum: 5/10 lags with non-finite or non-positive slowest timescale; connected-state counts=[25, 25, 8, 1, 8, 1, 8, 1, 1, 1]
- Lag used for MSM/PCCA+: **1 frames** (~1 ns assumed)
- Plot: `results\msm_model\implied_timescales.png`
- ITS JSON: `results\msm_model\implied_timescales.json`

## PCCA+

- **n_metastable (mathematically isolable):** **2**
- Selection method: `max_spectral_gap`

## Populations (% of assigned frames)

| Macrostate | n_frames | population % | π (PCCA stationary) |
|------------|----------|--------------|---------------------|
| 0 | 1079 | 54.09 | 0.4959 |
| 1 | 916 | 45.91 | 0.5041 |

## Assignments

- `results\msm_model\frame_macrostate_assignments.npz`
- `results\msm_model\dtrajs_microstates.npz`

## Provisional label (human decision — NOT auto-advanced)

- Lean: **`P2_INSUFFICIENT_SAMPLING`**
- Gate remains open for human: declare `P2_INSUFFICIENT_SAMPLING` vs proceed to network stage.

## Explicit stop

- No persistence/communication network extraction.
- No biological interpretation of macrostates.
- No P5 / docking / de novo.

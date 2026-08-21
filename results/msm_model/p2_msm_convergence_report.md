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

## ACTA DE CIERRE EXPERIMENTAL — COMPUERTA P2 (FASE 1)

**Status:** **CLOSED** — human decision registered 2026-08-21.  
**Verdict:** **`P2_INSUFFICIENT_SAMPLING`** (justified by MSM non-convergence / ITS `NON_CONVERGENT`).

**Physical justification:** Five WT trajs + **1995** aggregated frames lack statistical evidence for a convergent MSM; without that validation, reliable separation of the underlying metastable landscape is impossible. That suffices to close P2 Gate 1 and **abort** A/B/C network analysis between states.

**Epistemology (locks — no overreach):**
- Do **not** claim non-convergent ITS proves transitions are non-Markovian as a biological absolute.
- Do **not** claim the 2 mathematically isolable macrostates are “almost certainly noise.”
- Do **not** decide among A RED_ESTABLE / B RUTAS_POR_ESTADO / C DISTRIBUIDA — we do **not** yet know CB2 is a distributed network (or any of the three).
- Honest **“we do not know”** is the valuable result. Gates prevented fabricating a biological story on a sampling artifact.

**Evidence retained:**
- this report (`results/msm_model/p2_msm_convergence_report.md`)
- `results/msm_model/implied_timescales.png` (+ `implied_timescales.json`)
- pipeline commit **`2dcff23`** · builder `scripts/network_core/p2_msm_builder.py`

**Downstream:** `P2_NETWORK_A_B_C = ABORTED` · P3/P4/P6 **BLOCKED** · P5 remains **HYPOTHESIS_READY** (independent; **not** substitute for P2) · `DEEP_PAUSE = TRUE` · `REPOSITORY = SEALED` · `COMPUTATION = PAUSED`.

**Next human decision (register only — do not execute):** invest in the sampling required by P2 **OR** open the independent membrane question (P5 redesign in silico) — **not** “what script today?”

## Explicit stop

- No persistence/communication network extraction.
- No biological interpretation of macrostates.
- No P5 / docking / de novo / new MSM.

# Experiment X8 — Representation vs N (Gate-1 diagnosis)

**Fecha pre-registro:** 2026-09-09  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script.  
**Scope:** satellite discrimination test only. **Does not** reopen P2 A/B/C, P5, docking, de novo, or hub hunt.

---

## Question

With the **same 1995 frames** (5× GPCRmd/1540 WT dyn2126), does a **reduced** Cα distance featurization improve MSM implied-timescale behavior vs the original high-D TM1–7 pairwise set?

This discriminates:

| Hypothesis | Meaning |
|------------|---------|
| Representation-limited | High-D pairwise features were the bottleneck; a small interpretable set yields materially better ITS |
| Sampling-limited | Even with reduced D, ITS remains pathological / NON_CONVERGENT like baseline |

---

## Baseline (frozen; do not recompute for comparison)

| Item | Value |
|------|--------|
| Commit | `2dcff23` |
| Report | `results/msm_model/p2_msm_convergence_report.md` |
| Featurization | 178 TM Cα → **15 753** pairwise distances |
| Frames | 5 × 399 = **1995** |
| ITS verdict | **`NON_CONVERGENT`** |
| Pathological detail | 5/10 lags non-finite/non-positive slowest ITS; connected-state counts `=[25, 25, 8, 1, 8, 1, 8, 1, 1, 1]` |

Reuse the same assessment function philosophy as `scripts/network_core/p2_msm_builder.py` (`assess_its_convergence`).

---

## Data (identical to P2)

```
DIR  = data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/
PSF  = 24306_dyn_2126.psf
XTCs = 24307…24311_trj_2126.xtc
Manifest SHA verification required (same as p2_msm_builder).
```

---

## Reduced feature set (FIXED a priori — 24 Cα–Cα distances)

Human CB2 (UniProt P34972). Distances = ‖CA_i − CA_j‖ in Å. Sources: Ballesteros–Weinstein numbers from project atlas / `residue_maps.MICROSWITCHS["cb2"]` / LigACN hub list — **not** chosen after inspecting X8 ITS.

| # | Residues | BW / role |
|---|----------|-----------|
| 1 | 131–245 | Arg3.50 – Lys6.35 (primary IC TM3–TM6; Phase F/G) |
| 2 | 131–240 | Arg3.50 – Asp6.30 (DRY–TM6 IC sink) |
| 3 | 131–258 | Arg3.50 – Trp6.48 |
| 4 | 128–245 | Tyr3.47-region – Lys6.35 |
| 5 | 211–258 | Pro5.50 – Trp6.48 (canonical TM5–TM6) |
| 6 | 207–258 | TM5 mid/IC-adjacent – Trp6.48 |
| 7 | 215–245 | TM5 IC – Lys6.35 |
| 8 | 215–240 | TM5 IC – Asp6.30 |
| 9 | 201–258 | TM5 mid – Trp6.48 |
| 10 | 258–291 | Trp6.48 – Asn7.45 |
| 11 | 258–295 | Trp6.48 – Asn7.49 (NPxxY) |
| 12 | 258–285 | Trp6.48 – Ser7.39 |
| 13 | 245–291 | Lys6.35 – Asn7.45 |
| 14 | 240–295 | Asp6.30 – Asn7.49 |
| 15 | 264–295 | TM6 C-term – Asn7.49 |
| 16 | 131–295 | Arg3.50 – Asn7.49 |
| 17 | 131–291 | Arg3.50 – Asn7.45 |
| 18 | 83–291 | Ala2.53 hub – Asn7.45 |
| 19 | 79–291 | Ala2.49 hub – Asn7.45 |
| 20 | 87–285 | Phe87 – Ser285 (LigACN S out-neighbors of ligand) |
| 21 | 183–258 | Phe ECL2 – Trp6.48 |
| 22 | 268–285 | Ser6.58 – Ser7.39 |
| 23 | 287–295 | Leu7.41 – Asn7.49 (hub corridor) |
| 24 | 302–295 | Arg8.46 – Asn7.49 |

**n_features = 24** (≪ 15 753). No other distances may be added after seeing results.

---

## MSM hyperparameters (match p2_msm_builder where possible)

```text
TICA_LAG_FRAMES = 5
TICA_DIM        = 5          # keep; reduced D still projected
N_MICROSTATES   = 25
KMEANS_MAX_ITER = 500
KMEANS_SEED     = 20260821
ITS_LAGS_FRAMES = (1, 2, 5, 10, 15, 20, 25, 30, 40, 50)
N_ITS           = 8
FRAME_DT_NS     = 1.0        # assumed; report in frames + assumed ns
ITS_FLAT_REL_TOL     = 0.25
ITS_MARGINAL_REL_TOL = 0.50
```

Pipeline: reduced distances → tICA → K-means → ITS grid → same `assess_its_convergence` logic.

**Note:** With only 24 input dims, tICA dim=5 is still valid. Do **not** retune microstate count after seeing ITS.

---

## “Materially improves” (locked definition)

ITS **materially improves** vs baseline iff **all** of the following hold:

1. **Finite positive slowest ITS** at **≥ 3** successful lag points.  
2. **Connected-state counts do not collapse to 1** at a majority of successful lags (i.e. `#lags with n_connected ≤ 1` < half of successful lags).  
3. **Qualitative flattening:** assessment verdict is `CONVERGENT` **or** `MARGINAL` (not `NON_CONVERGENT`), **or** if still `NON_CONVERGENT`, the failure mode is **not** the baseline-style pathological spectrum (`n_finite_slowest < 3` or ≥ half lags non-finite/non-positive) **and** conditions (1)–(2) hold with late-vs-mid relative change ≤ `ITS_MARGINAL_REL_TOL`.

If reduced run cannot be compared fairly (SHA fail, missing atoms for registered pairs, software missing, etc.) → `X8_INDETERMINATE`.

---

## Verdicts (ONLY these labels)

| Label | Criterion |
|-------|-----------|
| `X8_REPRESENTATION_LIMITED` | Materially improves (definition above) |
| `X8_SAMPLING_LIMITED` | Still `NON_CONVERGENT` / pathological like baseline (fails material-improvement) |
| `X8_INDETERMINATE` | Cannot compare fairly |

---

## Forbidden interpretations

- Do **not** claim new switches, Gi mechanism, or A/B/C architecture.  
- Do **not** reopen `P2_NETWORK_A_B_C`.  
- Do **not** treat improved ITS (if any) as license for P5 / cholesterol post-hoc rescue of P1.  
- P2 remains **`CLOSED (INSUFFICIENT_SAMPLING)`** unless a separate PI decision reopens sampling.

---

## Outputs

| Path | Content |
|------|---------|
| `scripts/network_core/x8_reduced_featurization_msm.py` | Runner |
| `results/msm_model/x8_reduced_featurization_report.md` | Human report + verdict |
| `results/msm_model/x8_reduced_featurization_report.json` | Machine payload |
| `results/msm_model/x8_implied_timescales.png` | ITS plot |
| `results/msm_model/x8_implied_timescales.json` | ITS matrix |

---

## CLI

```bash
micromamba run -n janus_p1 python scripts/network_core/x8_reduced_featurization_msm.py
```

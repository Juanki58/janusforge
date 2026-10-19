# EXTERNAL — Dutta & Shukla 2023 Final_MSM kinetic comparison (CB1 vs CB2)

**Generated:** 2026-09-10T09:59:00.731415+00:00
**Pre-registration:** `docs/synthesis/EXPERIMENT_EXTERNAL_DUTTA_MSM.md`
**Mode:** `EXTERNAL_COMPARISON` — does **not** reopen P2 Gate-1 / structural A/B/C.

## Verdicts

- `EXT_KINETICS_CB1_CB2_DISTINCT`
- `EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES`
- `EXT_KINETIC_PATTERN_A`

## Inventory

| Receptor | Trajs | Frames | T median | Microstate labels | Truncations |
|----------|------:|-------:|---------:|------------------:|------------:|
| CB1 | 7582 | 4191680 | 600 | 400 | 0 |
| CB2 | 4972 | 2785341 | 600 | 600 | 0 |

Lag = **1 frame** (physical Δt **unknown** from pickles → all dwells in frames).
Hard metastable label = `argmax(state_prob)`; clustering.pkl = microstates (alignment only).

## Populations (hard occupancy)

| State | CB1 π̂ | CB2 π̂ |
|------:|-------:|-------:|
| 0 | 0.0340 | 0.0754 |
| 1 | 0.2855 | 0.0972 |
| 2 | 0.1451 | 0.1895 |
| 3 | 0.0701 | 0.1719 |
| 4 | 0.3938 | 0.0364 |
| 5 | 0.0716 | 0.4297 |

- H_norm(π̂) CB1=0.834, CB2=0.850
- Spearman ρ(π̂_CB1, π̂_CB2)=-0.257
- L1 ‖π̂_CB1−π̂_CB2‖₁=1.0914 (bootstrap p=0.0000)

## Kinetics (lag=1)

- Frobenius ‖P_CB1−P_CB2‖_F=0.0360 (bootstrap p=0.0000)
- Mean row TV=0.0097
- Top-exit path Jaccard overlap=0.200

### Mean dwell (frames)

| State | CB1 | CB2 |
|------:|----:|----:|
| 0 | 231.78 | 186.95 |
| 1 | 290.23 | 53.68 |
| 2 | 185.48 | 70.66 |
| 3 | 323.62 | 43.23 |
| 4 | 360.62 | 157.02 |
| 5 | 150.21 | 380.32 |

### Soft kinetic graph metrics

| Metric | CB1 | CB2 |
|--------|----:|----:|
| mean row_entropy_norm | 0.009 | 0.033 |
| edge_sparsity (τ=0.05) | 0.000 | 0.000 |
| mean n_strong_out | 0.00 | 0.00 |

**Caveat (lag=1):** metastable hard labels are highly self-persistent at one frame (near-diagonal P; row entropy ≈0; no off-diagonal edges ≥τ). `EXT_KINETIC_PATTERN_A` therefore mainly reflects lag-1 stickiness of published metastable states, not a structural LigACN architecture. Population differences remain the primary CB1≠CB2 kinetic discriminator here.

### Bootstrap CI (traj resample, B=200)

- CB1 mean_row_entropy_norm: {'mean': 0.009413023096489533, 'ci95_lo': 0.007929657178018761, 'ci95_hi': 0.010927581043681757}
- CB2 mean_row_entropy_norm: {'mean': 0.032527612780047385, 'ci95_lo': 0.02930131367598389, 'ci95_hi': 0.03555828407976292}
- CB1 edge_sparsity: {'mean': 0.0, 'ci95_lo': 0.0, 'ci95_hi': 0.0}
- CB2 edge_sparsity: {'mean': 0.0, 'ci95_lo': 0.0, 'ci95_hi': 0.0}

## Epistemic locks

- `EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES` (no coords → no LigACN/networks per state).
- `P2_MSM_TRANSITIONS` remains **CLOSED (INSUFFICIENT_SAMPLING)** on our GPCRmd data.
- Dutta K=6 is **not** a template for refitting our MSM.

## Plots

- (none)

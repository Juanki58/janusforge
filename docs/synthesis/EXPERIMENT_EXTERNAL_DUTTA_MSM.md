# Experiment — EXTERNAL comparison: Dutta & Shukla 2023 Final_MSM (CB1 vs CB2)

**Fecha pre-registro:** 2026-09-10  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script.  
**Scope:** **`EXTERNAL_COMPARISON`** of published Dutta & Shukla 2023 MSM objects only.  
**PI authorization:** YES (this turn).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Kinetic structure from discrete state sequences + state probabilities | Claiming our P2 GPCRmd Gate-1 is now `CONVERGENT` |
| Soft probe of A/B/C **only at kinetic level** (transition graph from counts) | Using Dutta’s 6 states as a fitting template for our failed MSM |
| External CB1 vs CB2 comparison labels below | Deciding structural architecture A/B/C (LigACN / contact networks per state) |
| Documenting that trajs are still missing | Reopening `P2_NETWORK_A_B_C` or treating this as Stage-1 of P2 |

**Without trajectories we cannot** rebuild LigACN persistence/communication networks per metastable state → we **cannot** fully decide architecture A/B/C as defined in [`P2_STATE_ROUTE_PREGISTRATION.md`](P2_STATE_ROUTE_PREGISTRATION.md) (those need coordinates/contacts).

**We can** analyze kinetic structure from discrete labels + probabilities.

```text
EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES   # locked a priori
P2_MSM_TRANSITIONS = CLOSED (INSUFFICIENT_SAMPLING)  # unchanged
P2_NETWORK_A_B_C   = ABORTED                         # unchanged
```

---

## Questions (locked)

1. **Populations.** What are stationary / empirical state populations for CB1 vs CB2 (6 metastable states)?
2. **Kinetics.** Transition matrix / dwell statistics — are CB1 and CB2 kinetics similar or distinct?
3. **Soft kinetic A/B/C probe (counts only).** Is the lag-1 transition graph sparse with stable hubs (A-like), state-dependent pathway structure (B-like), or diffuse / near-complete mixing (C-like)? Metrics defined a priori below — **not** structural networks.
4. **Structural A/B/C.** Explicitly **`INDETERMINATE_NO_TRAJECTORIES`**.

---

## Data (locked)

```
DIR = data/external/dutta_shukla_2023/msm/
CB1_state_prob.pkl
CB1_msm_feature_final_clustering.pkl
CB2_state_prob.pkl
CB2_msm_feature_final_clustering.pkl
MANIFEST.json   # SHA256 verify before analysis
```

Provenance: Box `Final_MSM` via user browser download 2026-09-10; see `msm/MANIFEST.json` / `BLOCKED_README.md`.  
DOI: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

**Object roles (from deposit README / safe inspect — not kinetic results):**

| File | Role |
|------|------|
| `*_state_prob.pkl` | Soft membership `(T, 6)` over **6 metastable** states |
| `*_msm_feature_final_clustering.pkl` | **Microstate / cluster** indices `(T,)` (hundreds of labels) — used for length alignment / integrity only; **not** the 6-state discrete sequence |

**Alignment rule:** for each receptor, for each trajectory index `i`, require `len(clustering[i]) == state_prob[i].shape[0]`; if mismatch, truncate both to `min(T)` and record `n_aligned_truncations`. Drop trajs with empty sequences.

**Hard assignment (6 metastable):** discrete state per frame = `argmax(state_prob[t])` ∈ {0…5}. Soft probabilities used for **empirical soft populations** (mean over frames of `state_prob`) as a secondary check vs hard occupancy. Microstate clustering is **not** analyzed as the primary kinetic graph in this experiment.

**Lag:** transition counts at **lag = 1 frame** on hard metastable labels. Frame physical time: **UNKNOWN a priori** from pickles alone → report all times in **frames**; if Methods elsewhere give Δt, document as assumed annotation only (does not change count-based verdicts).

---

## Metrics (locked a priori)

### Populations

- Hard occupancy π̂_k = (# frames labeled k) / N_frames (pooled).  
- Soft occupancy π̃_k = mean of state_prob[:, k] over frames.  
- Entropy H(π) = −∑ π_k log π_k (natural log); report also normalized H / log(K), K=6.  
- Rank-order correlation of π̂(CB1) vs π̂(CB2) (Spearman ρ) and L1 distance ‖π̂_CB1 − π̂_CB2‖₁.

### Transitions / dwells

- Count matrix C_ij = # of observed i→j at lag 1 (pooled; also per-traj for bootstrap).  
- Row-normalized P_ij = C_ij / ∑_j C_ij (add-one smoothing **only** if a row has zero mass — flag if used).  
- Mean dwell (frames) per state from run-lengths on hard labels.  
- Self-transition rate P_ii; escape rate 1−P_ii.  
- Frobenius ‖P_CB1 − P_CB2‖_F and mean absolute row-wise TV distance (½∑_j |P1_ij−P2_ij| averaged over i).

### Soft kinetic A/B/C pattern (counts-only; NOT structural)

Fixed thresholds (do not retune after seeing results):

| Metric | Definition | Role |
|--------|------------|------|
| `row_entropy` | For each i: H_i = −∑_j P_ij log P_ij; report mean and max over i | High → diffuse outflows |
| `row_entropy_norm` | H_i / log(K) | Scale-free |
| `edge_sparsity` | Fraction of off-diagonal entries with P_ij ≥ τ, τ=0.05 | Sparse vs dense graph |
| `n_strong_out` | Mean over i of #{j≠i : P_ij ≥ τ} | Hub-like vs multi-path |
| `top_path_overlap` | For each i, take top-1 destination j*(i)=argmax_{j≠i} P_ij; overlap = Jaccard of directed edges {(i,j*)} between CB1 and CB2 | Shared dominant exits |

**Pattern labels (optional soft):**

| Label | A priori rule |
|-------|----------------|
| `EXT_KINETIC_PATTERN_A` | Both receptors: mean `row_entropy_norm` ≤ 0.45 **and** `edge_sparsity` ≤ 0.35 **and** mean `n_strong_out` ≤ 2.0 (stable sparse hubs / few exits) |
| `EXT_KINETIC_PATTERN_B` | Not A; **and** CB1 vs CB2 `top_path_overlap` ≤ 0.50 **or** mean abs row-TV ≥ 0.25 (state-dependent / receptor-distinct pathways) |
| `EXT_KINETIC_PATTERN_C` | Both receptors: mean `row_entropy_norm` ≥ 0.75 **and** `edge_sparsity` ≥ 0.60 (diffuse near-complete mixing) |
| `EXT_KINETIC_PATTERN_INDETERMINATE` | None of the above cleanly, or conflicting CB1/CB2 pattern classes |

If CB1 and CB2 individually map to different A/B/C kinetic classes → `EXT_KINETIC_PATTERN_INDETERMINATE` (report per-receptor soft tags in JSON).

### Bootstrap / comparison tests

- Resample **trajectories** with replacement (B=200, seed=20260910).  
- 95% percentile intervals for π̂, mean dwell, mean row_entropy_norm, edge_sparsity.  
- CB1 vs CB2: two-sided bootstrap test on ‖π̂_CB1−π̂_CB2‖₁ and Frobenius ‖P_CB1−P_CB2‖_F vs null that pools all trajs and randomly splits into sizes n_CB1, n_CB2 (same B).  
- **Distinct** if both empirical stats exceed 97.5th percentile of null **or** 95% CIs for L1(π) and Frobenius(P) exclude equality-compatible near-zero band defined as null median (report p_boot = fraction of null ≥ observed).  
- **Similar** if both p_boot > 0.10 **and** L1(π) < 0.20 **and** mean row-TV < 0.15.  
- Else **`INDETERMINATE`**.

---

## Verdict labels (ONLY these)

| Label | Meaning |
|-------|---------|
| `EXT_KINETICS_CB1_CB2_DISTINCT` | Bootstrap / distance criteria for Distinct |
| `EXT_KINETICS_CB1_CB2_SIMILAR` | Similar criteria |
| `EXT_KINETICS_CB1_CB2_INDETERMINATE` | Neither |
| `EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES` | Always (this experiment) |
| `EXT_KINETIC_PATTERN_A` \| `B` \| `C` \| `INDETERMINATE` | Soft counts-only pattern |

---

## Forbidden interpretations

- Do **not** claim P2 CONVERGENT.  
- Do **not** fit our GPCRmd MSM to K=6.  
- Do **not** claim structural RED_ESTABLE / RUTAS_POR_ESTADO / DISTRIBUIDA.  
- Do **not** open P5 / docking / hub hunt from this result.

---

## Outputs

| Path | Content |
|------|---------|
| `scripts/network_core/external_dutta_msm_compare.py` | Runner |
| `results/network_core/external_dutta_msm_compare.md` | Human report + verdicts |
| `results/network_core/external_dutta_msm_compare.json` | Machine payload |
| `results/network_core/external_dutta_msm_compare_*.png` | Optional plots (populations, P heatmaps) |

---

## CLI

```bash
micromamba run -n janus_p1 python scripts/network_core/external_dutta_msm_compare.py
```

---

*Fin pre-registro. Ejecutar solo tras commit/presence of this file; do not edit thresholds after seeing results.*

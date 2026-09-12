# EXTERNAL own MSM — N=100 vs N=200 traj comparison

**Fecha:** 2026-09-12  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**PI:** scale-up autorizado (“si”) tras piloto `f45e5b8`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_APO_OWN_MSM.md`  
**Settings:** SAME X8 24 Cα, SAME tICA/K/MSM (no retune)

| Metric | Pilot (`--n-per-state 50`) | Scale-up (`--n-per-state 100`) |
|--------|----------------------------|--------------------------------|
| Trajs (inactive+active filename class) | 50+50 = **100** | 100+100 = **200** |
| Frames total | **56 246** | **109 080** (~1.94×) |
| Featurization | X8 24 Cα; align id=1.0 | identical |
| tICA / K-means | lag=5, dim=5, K=50 | identical |
| ITS verdict | `NON_CONVERGENT` | `NON_CONVERGENT` |
| ITS slowest late-vs-mid rel. Δ | **0.953** | **0.800** (improved, still ≫0.50) |
| Recommended lag | 30 frames | 30 frames |
| Soft CK | `CK_SOFT_PASS` (rel Frob 0.212) | `CK_SOFT_PASS` (rel Frob 0.227) |
| Stage-0 | `EXT_OWN_MSM_NON_CONVERGENT` | `EXT_OWN_MSM_NON_CONVERGENT` |
| Contacts | **ABORTED** | **ABORTED** |
| Artifacts | `cb2_apo_own_msm_report_pilot_n50.*` | `cb2_apo_own_msm_report.*` (current) |

## Interpretation (locked epistemology)

- Doubling traj count **softened** ITS drift (0.95→0.80) but **does not** cross the locked MARGINAL (≤0.50) / CONVERGENT (≤0.25) gates.
- Soft CK remains pass at lag 30; CK **does not** override ITS for Stage-0.
- Verdict remains **`EXT_OWN_MSM_NON_CONVERGENT`**; contacts stay aborted (no fabricated A/B/C).
- Still **EXTERNAL own map** only; **not** P2 reopen; **not** Dutta I1–I4; **no** Gi.
- Further N increase is again a **human / PI** decision — do **not** retune pairs/K after this result.

## Engineering notes (scale-up enablement)

- Cache gate fixed: `cache_nbytes()` no longer double-counts `bytes_written`.
- Orphan `.nc` not in the current stratified set are pruned so N=200 fits the locked ≤8 GB `_cache_own_msm/` budget without unpacking the full zip.

# EXTERNAL — CB2_APO **own** MSM report

**Generated (UTC):** `2026-09-12T19:56:12Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_APO_OWN_MSM.md`
**Commit tip (at run):** see git after commit

## Epistemology

- EXTERNAL own MSM on stratified local `CB2_APO` trajs (not full 142 GB unpack).
- **Our states `OWN_Sk` ≠ Dutta I1–I4**; no Final_MSM pickle alignment.
- Does **not** reopen P2 GPCRmd as CONVERGENT. No Gi / docking.

## Verdicts

- **Stage-0:** `EXT_OWN_MSM_NON_CONVERGENT`
- ITS: `NON_CONVERGENT`
- Soft CK: `CK_SOFT_PASS`
- Allow contacts: `NO`
- P2 unchanged: `CLOSED_INSUFFICIENT_SAMPLING`
- Dutta states: `NOT_ALIGNED_OWN_STATES_ONLY`

## Sampling

- N per filename class (inactive/active): **100**
- N trajs total: **200**
- n_frames_total: **109080**
- Cache: `data\external\dutta_shukla_2023\trajectories\CB2_APO\_cache_own_msm`
- Assumed frame dt: **0.1 ns** (MDA dts recorded in JSON)

## Featurization

- X8-like 24 Cα–Cα (UniProt → topo via alignment)
- Alignment identity: `1.0`
- All pairs OK: `True`

## MSM / ITS

- tICA lag=5, dim=5; K-means K=50
- **ITS verdict:** `NON_CONVERGENT`
- Detail: slowest ITS relative change late-vs-mid thirds = 0.800 (flat≤0.25, marginal≤0.5)
- Recommended lag: **30** frames
- Soft CK: `{'status': 'CK_SOFT_PASS', 'lag_frames': 30, 'lag2_frames': 60, 'rel_frobenius_error': 0.2268554635896912, 'threshold': 0.35, 'n_shared_states': 50}`
- ITS plot: `results\msm_model\cb2_apo_own_msm_its.png`

## PCCA+ / π (our states)

_No populations (Stage-0 abort before PCCA+)._

## Contacts

- See `results/network_core/cb2_apo_own_msm_contacts.md`
- Contact verdict (if run): `ABORTED`

## Software

- `numpy`: 2.4.6
- `scipy`: 1.18.0
- `sklearn`: 1.9.0
- `matplotlib`: 3.11.1
- `MDAnalysis`: 2.10.0
- `deeptime`: 0.4.5
- `python`: 3.12.13

## Scale-up status (PI-authorized)

- **Run:** `--n-per-state 100` (= **200** trajs), **109 080** frames; SAME X8 / tICA / K / MSM as pilot (no retune).
- **Stage-0:** `EXT_OWN_MSM_NON_CONVERGENT` (ITS late-vs-mid rel Δ ≈ **0.800**; soft CK pass at lag 30 does **not** override).
- Contacts / soft A/B/C: **ABORTED**.
- **vs pilot (N=100 trajs / `--n-per-state 50`):** ITS Δ 0.953 → 0.800 (improved, still NON_CONVERGENT). See `results/msm_model/cb2_apo_own_msm_n100_vs_n200.md` and `cb2_apo_own_msm_report_pilot_n50.*`.

## Hard locks

- P2 CLOSED (INSUFFICIENT_SAMPLING) — unchanged
- No fake alignment to Dutta pickles
- No Gi / docking

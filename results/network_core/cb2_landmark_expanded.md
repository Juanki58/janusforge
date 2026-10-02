# EXTERNAL — CB2 expanded geometric landmark contact maps

**Generated (UTC):** `2026-09-20T23:30:41Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_LANDMARK_EXPANDED.md`
**Git SHA:** `ff26bf01ad55edb3036fe7ab0bee23c92121f333`

## Epistemology

- EXTERNAL **geometric** labeling: nearest of Gate0-pass landmarks (Dutta-6 + cryo/crystal panel).
- **Geometric proximity ≠ MSM metastable identity.** Not kinetic MSM; not P2; no Gi claims.
- Soft compare to prior Dutta-6 STABLE (Jaccard≈0.82) and PDB snapshot B.

## Verdicts

- **`EXT_LANDMARK_EXPANDED_STABLE`**
- Q maps: `SIMILAR_OVERALL`
- Soft vs Dutta-6 STABLE: `EXT_LANDMARK_EXPANDED_SOFT_AGREE_DUTTA6_STABLE`
- Soft vs PDB snapshot B: `EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_PDB_B`
- `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `TRUE`
- P2 unchanged: `CLOSED_ABORTED_NOT_CONVERGENT`

## Gate 0 — numbering / alignment (per-PDB drop)

- Pass: `True`  verdict=`GATE0_PASS`
- Matched Cα (common UniProt): `265`
- Landmark order (pass): `['dutta_inactive', 'dutta_I1', 'dutta_I2', 'dutta_I3', 'dutta_I4', 'dutta_active', '5ZTY', '6KPC', '6KPF', '6PT0', '8GUQ', '8GUR', '8GUS', '8GUT', '8X3L', '9U7L']`
- Topo UniProt median offset (resid−UP): `-20`
- Dropped: `0`
  - PASS `dutta_inactive` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_inactive (geometric)
  - PASS `dutta_I1` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_I1 (geometric)
  - PASS `dutta_I2` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_I2 (geometric)
  - PASS `dutta_I3` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_I3 (geometric)
  - PASS `dutta_I4` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_I4 (geometric)
  - PASS `dutta_active` chain=`_` id_topo=`1.0` id_UP=`1.0` — Dutta Fig.6 dutta_active (geometric)
  - PASS `5ZTY` chain=`A` id_topo=`0.9859154929577465` id_UP=`0.973421926910299` — inactive / antagonist AM10257
  - PASS `6KPC` chain=`A` id_topo=`0.9821428571428571` id_UP=`0.9696969696969697` — active crystal / E3R
  - PASS `6KPF` chain=`R` id_topo=`0.9964788732394366` id_UP=`1.0` — active + Gi / AM12033-class
  - PASS `6PT0` chain=`R` id_topo=`1.0` id_UP=`1.0` — active + Gi / WIN 55,212-2
  - PASS `8GUQ` chain=`R` id_topo=`0.9964788732394366` id_UP=`1.0` — active + Gi / Olorinab (βarr-biased)
  - PASS `8GUR` chain=`R` id_topo=`0.9963898916967509` id_UP=`1.0` — active + Gi / CP55,940
  - PASS `8GUS` chain=`R` id_topo=`0.9964788732394366` id_UP=`1.0` — active + Gi / HU-308
  - PASS `8GUT` chain=`R` id_topo=`0.9964788732394366` id_UP=`1.0` — active + Gi / LEI-102
  - PASS `8X3L` chain=`R` id_topo=`0.9964539007092199` id_UP=`1.0` — active + G / entropy-driven
  - PASS `9U7L` chain=`R` id_topo=`1.0` id_UP=`1.0` — active + PAM Ec21a + CP55,940

## Contact definition

- Primary: `getcontacts_vdw_envelope_plus_alloviz_filters` — |AB| < Rvdw(A)+Rvdw(B)+0.5 Å
- Exclude sequential `|Δresid|==1`: `True`
- p_ij thr: `0.1` within hard-assigned landmark frames
- Hard assign: argmin RMSD; soft τ=`2.0` Å (sensitivity)

## Sampling

- N_per_state=`50` seed=`20260913` cache=`data\external\dutta_shukla_2023\trajectories\CB2_APO\_cache_landmark_expanded\nc` sources=`{'cache_copy': 100, 'zip': 0, 'already': 0}`

## Hard-assign occupancy

- `dutta_inactive`: n_frames=`4076` frac=`0.07246737545781033` mean_rmsd=`1.5626416406487247` LOW_N=`False`
- `dutta_I1`: n_frames=`4251` frac=`0.0755787078192227` mean_rmsd=`1.669940534444088` LOW_N=`False`
- `dutta_I2`: n_frames=`11319` frac=`0.2012409771361519` mean_rmsd=`1.3713334392136114` LOW_N=`False`
- `dutta_I3`: n_frames=`8157` frac=`0.14502364612594673` mean_rmsd=`1.534959859075844` LOW_N=`False`
- `dutta_I4`: n_frames=`2006` frac=`0.03566475838281833` mean_rmsd=`1.8809819169018733` LOW_N=`False`
- `dutta_active`: n_frames=`14678` frac=`0.2609607794332041` mean_rmsd=`2.059051506961445` LOW_N=`False`
- `5ZTY`: n_frames=`884` frac=`0.015716673185648757` mean_rmsd=`1.7084116149816206` LOW_N=`False`
- `6KPC`: n_frames=`231` frac=`0.0041069587170643245` mean_rmsd=`2.301800103974036` LOW_N=`False`
- `6KPF`: n_frames=`0` frac=`0.0` mean_rmsd=`None` LOW_N=`True`
- `6PT0`: n_frames=`4406` frac=`0.0783344593393308` mean_rmsd=`2.1304602020110504` LOW_N=`False`
- `8GUQ`: n_frames=`254` frac=`0.004515876684564235` mean_rmsd=`2.201290385746301` LOW_N=`False`
- `8GUR`: n_frames=`44` frac=`0.0007822778508693952` mean_rmsd=`2.404063343600453` LOW_N=`True`
- `8GUS`: n_frames=`5850` frac=`0.10400739608149913` mean_rmsd=`2.129020124563514` LOW_N=`False`
- `8GUT`: n_frames=`89` frac=`0.0015823347438040038` mean_rmsd=`2.2370652004403264` LOW_N=`True`
- `8X3L`: n_frames=`0` frac=`0.0` mean_rmsd=`None` LOW_N=`True`
- `9U7L`: n_frames=`1` frac=`1.7779042065213526e-05` mean_rmsd=`2.049068879108236` LOW_N=`True`

## Pairwise Jaccard (primary VdW, occupied landmarks)

- mean=`0.8305`  min=`0.7435`  max=`0.9206`
- frac_core=`0.6043`  frac_state_specific=`0.0119`
- path_turnover_frac=`0.14410144297928001`  (Dutta-6 path defined=`True`)
- Δmean_j vs Dutta-6 prior (0.8214): `0.009072451411627047`

### n_edges

- `dutta_inactive`: `1123`
- `dutta_I1`: `1104`
- `dutta_I2`: `1131`
- `dutta_I3`: `1103`
- `dutta_I4`: `1166`
- `dutta_active`: `1170`
- `5ZTY`: `1181`
- `6KPC`: `1161`
- `6KPF`: `0`
- `6PT0`: `1175`
- `8GUQ`: `1116`
- `8GUR`: `1073`
- `8GUS`: `1135`
- `8GUT`: `1145`
- `8X3L`: `0`
- `9U7L`: `804`

### Path turnover (Dutta-6 subset)

- `dutta_inactive→dutta_I1`: appear=51 disappear=70 turnover=0.103
- `dutta_I1→dutta_I2`: appear=111 disappear=84 turnover=0.160
- `dutta_I2→dutta_I3`: appear=46 disappear=74 turnover=0.102
- `dutta_I3→dutta_I4`: appear=167 disappear=104 turnover=0.213
- `dutta_I4→dutta_active`: appear=91 disappear=87 turnover=0.142

## Soft-weight sensitivity (does not drive primary)

- mean soft entropy (nats): `2.754344958278483`
- soft mean_jaccard: `0.9791259182896823`
- soft class (annotation): `EXT_LANDMARK_EXPANDED_STABLE`
- differs from hard primary class: `False`

## Resumen PI (ES)

Landmark geométrico CB2 expandido (Dutta-6 + panel cryo/cristal): Gate0 OK (landmarks=16, Cα comunes=265, drop=ninguno). N=50+50 trajs, frames=56246. Veredicto duro: **EXT_LANDMARK_EXPANDED_STABLE** (mean Jaccard=0.830, Δ vs Dutta-6 prior=0.009, frac_core=0.604, path_turnover=0.14410144297928001). Soft Dutta-6: EXT_LANDMARK_EXPANDED_SOFT_AGREE_DUTTA6_STABLE. Soft PDB-B: EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_PDB_B. Importante: proximidad geométrica ≠ identidad MSM; sin claims Gi. P2 sin cambios. SHA `ff26bf01ad55edb3036fe7ab0bee23c92121f333`.

## Forbidden

- No Gi claims; no docking; no P2 CONVERGENT; landmark ≠ MSM state.


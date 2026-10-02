# EXTERNAL — CB2 geometric landmark contact maps

**Generated (UTC):** `2026-09-12T23:05:20Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_LANDMARK_CONTACTS.md`
**Git SHA:** `22d2af1d282a6bd72d55863fed2e4156032d930f`

## Epistemology

- EXTERNAL **geometric** labeling: nearest of 6 Dutta Fig. 6 PDB landmarks (RMSD Cα).
- **Geometric proximity ≠ MSM metastable identity.** Not kinetic MSM; not pickles; not P2; no Gi.

## Verdicts

- **`EXT_LANDMARK_CONTACTS_STABLE`**
- Q maps: `SIMILAR_OVERALL`
- Soft compare vs PDB snapshot B: `EXT_LANDMARK_SOFT_DISAGREE_PDB_B`
- `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `TRUE`
- P2 unchanged: `CLOSED_ABORTED_NOT_CONVERGENT`

## Gate 0 — numbering / alignment

- Pass: `True`  verdict=`GATE0_PASS`
- Matched Cα: `284`
- Topo UniProt median offset (resid−UP): `-20`

## Contact definition

- Primary: `getcontacts_vdw_envelope_plus_alloviz_filters` — |AB| < Rvdw(A)+Rvdw(B)+0.5 Å
- Exclude sequential `|Δresid|==1`: `True`
- p_ij thr: `0.1` within hard-assigned landmark frames
- Hard assign: argmin RMSD; soft τ=`2.0` Å (sensitivity)

## Sampling

- N_per_state=`50` seed=`20260913` cache=`data\external\dutta_shukla_2023\trajectories\CB2_APO\_cache_landmark_contacts\nc` sources=`{'cache_copy': 3, 'zip': 95, 'already': 2}`

## Hard-assign occupancy

- `inactive`: n_frames=`5490` frac=`0.09760694093802226` mean_rmsd=`1.886438891199309` LOW_N=`False`
- `I1`: n_frames=`3655` frac=`0.06498239874835544` mean_rmsd=`1.8220138811543565` LOW_N=`False`
- `I2`: n_frames=`12510` frac=`0.2224158162358212` mean_rmsd=`1.7112516139697338` LOW_N=`False`
- `I3`: n_frames=`8837` frac=`0.15711339473029193` mean_rmsd=`1.8808123168808828` LOW_N=`False`
- `I4`: n_frames=`1020` frac=`0.018134622906517798` mean_rmsd=`2.4478318122602003` LOW_N=`False`
- `active`: n_frames=`24734` frac=`0.43974682644099133` mean_rmsd=`2.4347711418986298` LOW_N=`False`

## Pairwise Jaccard (primary VdW, occupied landmarks)

- mean=`0.8214`  min=`0.7401`  max=`0.9103`
- frac_core=`0.6503`  frac_state_specific=`0.0244`
- path_turnover_frac=`0.1409`

### n_edges

- `inactive`: `1138`
- `I1`: `1101`
- `I2`: `1132`
- `I3`: `1105`
- `I4`: `1175`
- `active`: `1165`

### Path turnover

- `inactive→I1`: appear=45 disappear=82 turnover=0.107
- `I1→I2`: appear=110 disappear=79 turnover=0.156
- `I2→I3`: appear=39 disappear=66 turnover=0.090
- `I3→I4`: appear=171 disappear=101 turnover=0.213
- `I4→active`: appear=82 disappear=92 turnover=0.138

## Soft-weight sensitivity (does not drive primary)

- mean soft entropy (nats): `1.7528822080468547`
- soft mean_jaccard: `0.9652587705458101`
- soft class (annotation): `EXT_LANDMARK_CONTACTS_STABLE`
- differs from hard primary class: `False`

## Resumen PI (ES)

Landmark geométrico CB2 (6 PDBs Dutta): Gate0 OK (Cα emparejados=284, offset topo−UniProt≈-20). N=50+50 trajs, frames=56246. Veredicto duro: **EXT_LANDMARK_CONTACTS_STABLE** (mean Jaccard=0.821, path turnover=0.141, frac_core=0.650). Compare PDB snapshot: EXT_LANDMARK_SOFT_DISAGREE_PDB_B. Importante: proximidad geométrica ≠ identidad MSM. P2 sin cambios. SHA `22d2af1d282a6bd72d55863fed2e4156032d930f`.

## Forbidden

- No Gi; no docking; no P2 CONVERGENT; landmark ≠ MSM state.


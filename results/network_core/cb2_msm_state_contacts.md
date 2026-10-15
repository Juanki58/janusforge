# EXTERNAL — CB2 MSM metastable-state contact probabilities

**Generated (UTC):** `2026-09-12T11:14:27Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_MSM_STATE_CONTACTS.md`

## Epistemology

- EXTERNAL MSM-state contacts (Dutta & Shukla 2023 Final_MSM + CB2_APO.zip).
- Filename `inactive`/`active` ≠ MSM macrostate.
- Does **not** reopen P2 as CONVERGENT; no Gi claims.

## Verdicts

- **`EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT`**
- Soft compare vs PDB snapshot B: `EXT_MSM_SOFT_COMPARE_NA`
- Filename ≠ MSM state: `TRUE`
- P2 status: `CLOSED_ABORTED_NOT_CONVERGENT`

## Gate 0 — traj ↔ MSM alignment

- ok=`False` method=`None`
- n_traj_msm=`4972` zip_n_nc=`4971`
- **Missing mapping key:** No co-deposited traj filename/path list of length n_traj aligned to CB2_state_prob.pkl list indices. Pickles are anonymous list[ndarray] only. Zip has 4971 .nc vs MSM n_traj=4972 (delta=1). Zip helper CB2_APO/list has only 5 short-traj names (not MSM order). Authors' load order (glob / box pagination) is not reconstructible from available artifacts. Lexicographic / zip-member / natural sort are NOT accepted without independent validation.

Rejected heuristics (not used):

- `lexicographic_sort_of_nc_names`
- `zip_member_order`
- `natural_sort`
- `filename_inactive_active_as_msm_label`
- `majority_hard_state_without_index_map`

## Macrostate label map (authors’ code)

- Source: `ShuklaGroup/Cannabinoid_activation Main_Figure_6/CB2-APO_vampnet_states_TPT.py labels=['I1','I2','I3','Inactive','I4','Active']`

| argmax idx | label |
|----------:|-------|
| 0 | `I1` |
| 1 | `I2` |
| 2 | `I3` |
| 3 | `inactive` |
| 4 | `I4` |
| 5 | `active` |

## Stationary / empirical populations π (bonus; no traj alignment needed)

- n_frames pooled = `2785341`

| state | π̂ hard | π̃ soft |
|-------|--------:|--------:|
| `inactive` | 0.1719 | 0.1597 |
| `I1` | 0.0754 | 0.0842 |
| `I2` | 0.0972 | 0.0978 |
| `I3` | 0.1895 | 0.1951 |
| `I4` | 0.0364 | 0.0401 |
| `active` | 0.4297 | 0.4232 |

- Trajs with dominant hard frac ≥0.9: `4827` / `4972`

## Contact analysis

- **Skipped.** Gate 0 failed — no per-state contact matrices / Jaccard / hub degrees.
- Would have used VdW+0.5 Å, `p_ij≥0.1` (primary) / `0.5` (secondary), pilot N=5 trajs/macrostate, frame_cap=200.

## Soft compare (annotation)

- Prior PDB: `EXT_PDB_CONTACTS_STATE_DEPENDENT` / `EXT_STRUCTURAL_ABC_SNAPSHOT_B`.
- Prior filename pilot: `EXT_APO_PILOT_CONTACTS_INDETERMINATE` (Jaccard≈0.78).
- This run soft tag: `EXT_MSM_SOFT_COMPARE_NA`.

## Forbidden claims (reminder)

- No Gi; no docking; no P2 CONVERGENT; no fake traj↔MSM map.

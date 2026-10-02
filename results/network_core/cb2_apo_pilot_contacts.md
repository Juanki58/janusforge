# EXTERNAL — CB2_APO pilot contact maps (inactive vs active)

**Generated (UTC):** `2026-09-12T09:05:39Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_APO_PILOT_CONTACTS.md`

## Epistemology

- EXTERNAL **trajectory pilot** (1 inactive + 1 active `.nc` + shared prmtop).
- **Few trajs ≠ ensemble.** Not P2 CONVERGENT; not Gi mechanism; not P1 hub hunt.

## Verdicts

- **`EXT_APO_PILOT_CONTACTS_INDETERMINATE`**
- Q2 maps: `DIFFERS_SUBSTANTIALLY`
- Soft compare vs prior PDB snapshot B: `EXT_APO_PILOT_SOFT_DISAGREE_PDB_B`
- Single-traj limit: `TRUE`
- Needs more trajs (stratified zip sample): `YES`
- P2 status: `CLOSED_ABORTED_NOT_CONVERGENT`

## Smoke-open

- Topology: `CB2-APO_inactive_pr_1-strip.prmtop` sha256=`db7182785383…`
- Expect n_atoms=4566; both pilots atoms_ok=`True`

- `inactive`: `CB2-APO_inactive_pr_9_frame_99-strip.nc` n_atoms=4566 n_frames=600 n_edges_vdw=1072 sha256=`d9bfed9a0d45…`
- `active`: `CB2-APO_active_pr_10_frame_28-strip.nc` n_atoms=4566 n_frames=600 n_edges_vdw=1085 sha256=`81bdf4e02f65…`

## Contact definition

- Primary: `getcontacts_vdw_envelope_plus_alloviz_filters` — |AB| < Rvdw(A)+Rvdw(B)+0.5 Angstrom; A,B non-hydrogen
- `p_ij` threshold: `0.1` (P1)
- Exclude sequential `|Δresid|==1`: `True`
- Selection: `protein` (apo)

## Metrics (primary VdW persistence)

- jaccard(inactive, active) = **0.7768**
- n_edges inactive=1072 active=1085
- n_shared=943 n_union=1214
- frac_private inactive=0.1203 active=0.1309 mean=0.1256

## Soft compare to prior PDB experiment

- Prior: `EXT_PDB_CONTACTS_STATE_DEPENDENT` / `EXT_STRUCTURAL_ABC_SNAPSHOT_B` (6 state PDBs; mean Jaccard≈0.64; path turnover≈0.35).
- This pilot soft tag: `EXT_APO_PILOT_SOFT_DISAGREE_PDB_B` (contact-map class only; not ensemble promotion).

## LigACN hubs (descriptive)

- Alignment identity: `1.0000`
- Note: Project hub labels use UniProt P34972 indices; topo resid may differ (N-term truncation).

- `ALA:79`: status=`OK` topo=`ALA:59` resid=`59` aa=`ALA`
- `ALA:83`: status=`OK` topo=`ALA:63` resid=`63` aa=`ALA`
- `LEU:287`: status=`OK` topo=`LEU:255` resid=`255` aa=`LEU`
- `ASN:291`: status=`OK` topo=`ASN:259` resid=`259` aa=`ASN`
- `ASN:295`: status=`OK` topo=`ASN:263` resid=`263` aa=`ASN`
- `ARG:302`: status=`OK` topo=`ARG:270` resid=`270` aa=`ARG`

### Hub degrees (inactive | active)

| hub | inactive | active |
|---|---|---|
| `ALA:79` | 10 | 10 |
| `ALA:83` | 7 | 9 |
| `LEU:287` | 8 | 9 |
| `ASN:291` | 10 | 10 |
| `ASN:295` | 8 | 8 |
| `ARG:302` | 10 | 7 |

### Hub-incident edge Jaccard (inactive vs active)

- `ALA:79`: 1.0000
- `ALA:83`: 0.7778
- `LEU:287`: 0.7000
- `ASN:291`: 1.0000
- `ASN:295`: 0.4545
- `ARG:302`: 0.4167

## Secondary Cα 8Å (sensitivity)

- jaccard_ca=0.7967 (not used for verdicts)

## Robustness note

- Primary N=1 traj/state → always `EXT_APO_PILOT_NEEDS_MORE_TRAJS=YES`.
- Stratified **5+5** extracted from local `CB2_APO.zip` (no full unpack) →
  `results/network_core/cb2_apo_pilot_contacts_sample5.{md,json}`.
- Sample5: jaccard=0.7702, mean_frac_private=0.1298 → **`EXT_APO_PILOT_CONTACTS_INDETERMINATE`**
  (same soft class as primary; still soft-disagrees PDB snapshot B). Not P2 CONVERGENT.

## Forbidden claims (reminder)

- No Gi mechanism; no docking/de novo; no P2 CONVERGENT; pilot ≠ ensemble.

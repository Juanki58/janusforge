# EXTERNAL — CB2 state PDB contact maps (Dutta & Shukla 2023)

**Generated (UTC):** `2026-09-11T13:13:46Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_STATE_PDB_CONTACTS.md`

## Epistemology

- EXTERNAL structural **snapshot** comparison of published state PDBs.
- **One PDB ≠ ensemble.** Not P2 CONVERGENT; not Gi mechanism; not P1 hub hunt.

## Verdicts

- **`EXT_PDB_CONTACTS_STATE_DEPENDENT`**
- **`EXT_STRUCTURAL_ABC_SNAPSHOT_B`** (snapshot-only soft A/B/C)
- Q1 maps: `DIFFERS_SUBSTANTIALLY`

## Contact definition

- Primary: `getcontacts_vdw_envelope_plus_alloviz_filters` — |AB| < Rvdw(A)+Rvdw(B)+0.5 Angstrom; A,B non-hydrogen
- Exclude sequential `|Δresid|==1`: `True`
- Secondary (sensitivity): Cα < 8.0 Å, `|Δresid|>=2`

## Data / integrity

- `inactive`: `CB2_ref_inactive_3_b.pdb` sha256=`d641a808852c…` n_edges_vdw=813 n_edges_ca=1057
- `I1`: `CB2_ref_inactive_I1_b.pdb` sha256=`50fefbbe30fb…` n_edges_vdw=802 n_edges_ca=1040
- `I2`: `CB2_ref_inactive_I2_b.pdb` sha256=`311109f8a6ec…` n_edges_vdw=851 n_edges_ca=1066
- `I3`: `CB2_ref_inactive_I3_b.pdb` sha256=`142e770e64d7…` n_edges_vdw=781 n_edges_ca=1054
- `I4`: `CB2_ref_inactive_I4_b.pdb` sha256=`dca5531acdc1…` n_edges_vdw=834 n_edges_ca=1058
- `active`: `CB2_ref_inactive_active_b.pdb` sha256=`41816e10f2ca…` n_edges_vdw=828 n_edges_ca=1058

- Manifest verified: `True`
- Hub alignment identity (inactive ref): `1.0000`

## Pairwise Jaccard (primary VdW)

- mean=0.6429  min=0.5959  max=0.6928
- frac_core=0.3590  frac_state_specific=0.0472
- path_turnover_frac=0.3476

### Matrix

| | inactive | I1 | I2 | I3 | I4 | active |
|---|---|---|---|---|---|---|
| **inactive** | 1.000 | 0.686 | 0.693 | 0.659 | 0.596 | 0.636 |
| **I1** | 0.686 | 1.000 | 0.665 | 0.686 | 0.604 | 0.617 |
| **I2** | 0.693 | 0.665 | 1.000 | 0.664 | 0.634 | 0.636 |
| **I3** | 0.659 | 0.686 | 0.664 | 1.000 | 0.601 | 0.620 |
| **I4** | 0.596 | 0.604 | 0.634 | 0.601 | 1.000 | 0.647 |
| **active** | 0.636 | 0.617 | 0.636 | 0.620 | 0.647 | 1.000 |

## Path turnover (inactive→…→active)

- `inactive→I1`: appear=145 disappear=156 turnover=0.314
  - appear sample: ALA:108–LEU:215, ALA:15–VAL:18, ALA:196–HIE:199, ALA:196–LEU:115, ALA:196–LYS:213, ALA:196–TYR:189, ALA:212–ARG:270, ALA:212–VAL:200
  - disappear sample: ACE:202–LEU:207, ALA:108–ARG:111, ALA:123–PRO:119, ALA:130–ARG:127, ALA:17–CYS:20, ALA:17–PHE:77, ALA:17–VAL:72, ALA:203–ARG:206
- `I1→I2`: appear=191 disappear=142 turnover=0.335
  - appear sample: ACE:202–ARG:206, ALA:108–ARG:111, ALA:123–THR:126, ALA:130–LEU:51, ALA:17–CYS:20, ALA:196–VAL:200, ALA:203–ARG:206, ALA:212–ARG:210
  - disappear sample: ACE:1–LYS:3, ALA:108–LEU:215, ALA:142–MET:95, ALA:179–LEU:176, ALA:17–LYS:13, ALA:196–HIE:199, ALA:196–LEU:115, ALA:196–LEU:193
- `I2→I3`: appear=130 disappear=200 turnover=0.336
  - appear sample: ACE:1–ASP:4, ACE:1–LYS:3, ACE:1–TYR:5, ACE:202–HIE:279, ACE:202–SER:276, ALA:108–LEU:215, ALA:130–ARG:127, ALA:142–MET:95
  - disappear sample: ACE:202–ARG:206, ALA:123–TYR:121, ALA:130–LEU:51, ALA:130–PHE:52, ALA:203–ARG:206, ALA:203–MET:205, ALA:212–ARG:210, ALA:212–LEU:215
- `I3→I4`: appear=228 disappear=175 turnover=0.399
  - appear sample: ACE:1–ASP:81, ACE:1–PHE:86, ACE:1–VAL:80, ACE:202–ARG:204, ACE:202–ARG:206, ALA:123–PRO:119, ALA:130–LEU:125, ALA:130–PHE:52
  - disappear sample: ACE:1–ASP:4, ACE:1–LYS:3, ACE:1–TYR:5, ACE:202–HIE:279, ACE:202–SER:276, ALA:108–LEU:215, ALA:123–ARG:129, ALA:123–THR:126
- `I4→active`: appear=175 disappear=181 turnover=0.353
  - appear sample: ACE:1–LYS:3, ACE:202–LEU:115, ACE:202–PRO:118, ALA:108–TYR:189, ALA:123–TYR:121, ALA:179–LEU:176, ALA:196–ARG:204, ALA:196–MET:205
  - disappear sample: ACE:1–ASP:81, ACE:1–PHE:86, ACE:1–VAL:80, ACE:202–ARG:204, ACE:202–ARG:206, ALA:123–PRO:119, ALA:130–PHE:52, ALA:15–PRO:11

## LigACN hubs (descriptive)

- `ALA:79`: status=`OK` pdb=`ALA:59` resid=`59` aa=`ALA`
- `ALA:83`: status=`OK` pdb=`ALA:63` resid=`63` aa=`ALA`
- `LEU:287`: status=`OK` pdb=`LEU:255` resid=`255` aa=`LEU`
- `ASN:291`: status=`OK` pdb=`ASN:259` resid=`259` aa=`ASN`
- `ASN:295`: status=`OK` pdb=`ASN:263` resid=`263` aa=`ASN`
- `ARG:302`: status=`OK` pdb=`ARG:270` resid=`270` aa=`ARG`

### Per-state hub degrees

| hub | inactive | I1 | I2 | I3 | I4 | active |
|---|---|---|---|---|---|---|
| `ALA:79` | 8 | 7 | 7 | 5 | 8 | 7 |
| `ALA:83` | 8 | 5 | 7 | 6 | 8 | 7 |
| `LEU:287` | 7 | 5 | 5 | 5 | 5 | 7 |
| `ASN:291` | 10 | 9 | 8 | 7 | 9 | 9 |
| `ASN:295` | 7 | 7 | 5 | 6 | 6 | 5 |
| `ARG:302` | 5 | 7 | 3 | 5 | 4 | 5 |

## Secondary Cα 8Å (sensitivity)

- mean_jaccard_ca=0.7953 (not used for verdicts)

## Forbidden claims (reminder)

- No Gi mechanism; no docking/de novo; no P2 CONVERGENT; snapshot ≠ ensemble.

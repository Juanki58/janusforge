# Dual validation — static hubs × functional enrichment

> **PI closure (2026-08-21):** Combined verdict **`CORE_TOPOLOGICAL_ONLY`** locked. Six hubs = real static bottlenecks; PrefCoup_Gαi2 set enrichment **not** supported. Not a switch / not `CB2_Gi_NETWORK_CANDIDATE`. Dual-test ancla **`cfb2a51`** preserved. `LINE_PAUSE = TRUE` — no re-run.

**Run UTC:** `2026-08-20T19:26:38Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Mode:** `CLOSED_DUAL_VALIDATION` / READ_ONLY_DATA / `LINE_PAUSE`
**Literature (PRIMARY):** Morales-Pastor et al., *Nat Commun* (2025), DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)

## Governance locks

```yaml
mode: CLOSED_DUAL_VALIDATION
MODO: READ_ONLY_DATA
LINE_PAUSE: TRUE
DUAL_HUB_TEST: CLOSED
STATIC_BOTTLENECKS: SUPPORTED
FUNCTIONAL_Gi_ENRICHMENT: NOT_SUPPORTED
CB2_Gi_NETWORK_CANDIDATE: NOT_ESTABLISHED
CB2_MINIMAL_GI_CORE: NOT_FOUND
DE_NOVO: STOP
DOCKING: STOP
NEW_HUB_SEARCH: STOP
DE_NOVO_GENERATION: STOP
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
NEW_SEARCH: STOP
CONTRACT_v1.0: ARCHIVED_HISTORICAL
TECHNICAL_SEARCH_TRAJ: STOP
hub_list: FIXED_A_PRIORI_NO_RETUNE
literature_doi: 10.1038/s41467-025-60003-0
dual_test_commit: cfb2a51
```

## Fixed hub set (a priori)

| LigACN | Short | Ballesteros |
|--------|-------|-------------|
| `ALA:79` | ALA79 | 2.49 |
| `ALA:83` | ALA83 | 2.53 |
| `LEU:287` | LEU287 | 7.41 |
| `ASN:291` | ASN291 | 7.45 |
| `ASN:295` | ASN295 | 7.49 |
| `ARG:302` | ARG302 | 8.46 |

**S (verified only):** ['8D0:1', 'SER:285', 'PHE:87']
**T:** ['ARG:131', 'ASP:240', 'SER:303', 'SER:69']
**Not forced:** ['TRP:258', 'PHE:183']

---

## Test A — Topology

**Tag:** [INTERNAL_REANALYSIS]

- Graph: 100 nodes × **239** directed edges (WT_degeneracy).
- PI text mentioned 117 edges; recovered WT_degeneracy DiGraph has 239 directed weight>0 off-diagonal edges (same construction as static_ligacn_topology). Documented actual count.
- Nulls: **1000** exact (in,out)-degree-matched knockouts.
- Matching rule: `exact_in_out_degree_multiset_match`
- Hub IO multiset: `{'2,3': 2, '3,2': 2, '3,4': 1, '4,4': 1}`
- **Primary metric:** `pct_disconn`
- Rule: TOPOLOGICAL_BOTTLENECK_SUPPORTED iff empirical one-sided p < 0.05 for pct_disconn after hub knockout vs exact (in,out)-degree-matched null knockouts of equal size (upper-tail: larger %Disconn = stronger impact). Equivalently: observed impact in upper ≥95th percentile of nulls. Secondary metrics (residual connectivity, ΔL, Eff_res) reported but do not override the primary call unless primary is undefined.

| Metric | WT | Hub KO | Null mean | p |
|--------|----|--------|-----------|---|
| %Disconn (S×T) | 0.0000 | 0.3333 | 0.0265 | **0.000999** |
| Residual connectivity (ligand→T) | 1.0000 | 1.0000 | 1.0000 | 1 |
| ΔL mean path length S→T | 0 (ref) | 10.6667 | 0.3248 | 0.000999 |
| Eff_res (directed global efficiency) | 0.117596 | 0.097184 | 0.103753 | 0.1558 |

**Outcome A:** `TOPOLOGICAL_BOTTLENECK_SUPPORTED`

---

## Test B — Function

**Tag:** [INTERNAL_REANALYSIS] + [LITERATURA_PRIMARIA] categories from Morales-Pastor SD1

### Safeguard: membership ≠ statistical attribution

1. **Position membership:** position_membership = which hubs appear in PrefCoup/Coup/Uncoupled lists
2. **Statistically attributable bias:** Fisher one-sided PrefCoup_Gi enrichment of the hub-position mutant *set* vs non-hub background (expression-filtered).
3. Multiple mutations: Each mutation/category reported separately under per_hub_mutations; no premature single-label collapse.

Expression filter: exclude surface expression **<25.0% WT**.

### Per-hub mutations (not collapsed)

#### `ALA:79` (ALA79, 2.49) — PRESENT
- **A79V** [EXCLUDED_LOW_EXPR]: raw=`NoCoup_Gi_bArr` → mapped=`Uncoupled_No_effect`; %wt_expr=20.42946591; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0

#### `ALA:83` (ALA83, 2.53) — PRESENT
- **A83V** [IN_TEST]: raw=`NoCoup_Gi_bArr` → mapped=`Uncoupled_No_effect`; %wt_expr=72.1045113; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0

#### `LEU:287` (LEU287, 7.41) — PRESENT
- **L287A** [IN_TEST]: raw=`Coup_Gi_bArr` → mapped=`Coup_Gαi2_βarr1`; %wt_expr=51.15821889; Gi2_Emax_raw=1.04638928666667; bArr1_Emax_raw=0.100127372333333

#### `ASN:291` (ASN291, 7.45) — PRESENT
- **N291A** [IN_TEST]: raw=`PrefCoup_Gi` → mapped=`PrefCoup_Gαi2`; %wt_expr=101.8849675; Gi2_Emax_raw=0.396139751333333; bArr1_Emax_raw=0.0

#### `ASN:295` (ASN295, 7.49) — PRESENT
- **N295A** [IN_TEST]: raw=`NoCoup_Gi_bArr` → mapped=`Uncoupled_No_effect`; %wt_expr=77.92948329; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0

#### `ARG:302` (ARG302, 8.46) — PRESENT
- **R302A** [IN_TEST]: raw=`PrefCoup_Gi` → mapped=`PrefCoup_Gαi2`; %wt_expr=85.16676041; Gi2_Emax_raw=1.08423460433333; bArr1_Emax_raw=0.0

### Position membership (expression-filtered)

- PrefCoup_Gαi2: [{'node': 'ASN:291', 'mutant': 'N291A'}, {'node': 'ARG:302', 'mutant': 'R302A'}]
- Coup_Gαi2_βarr1: [{'node': 'LEU:287', 'mutant': 'L287A'}]
- Uncoupled/No_effect: [{'node': 'ALA:83', 'mutant': 'A83V'}, {'node': 'ASN:295', 'mutant': 'N295A'}]
- Excluded low expression: [{'node': 'ALA:79', 'mutant': 'A79V', 'pct_wt_expression': 20.42946591, 'coupling_profile_mapped': 'Uncoupled_No_effect'}]

### Statistical attribution (Fisher)

- Contingency: `[[2, 3], [58, 263]]`
- Odds ratio: **3.023**
- p (greater): **0.2296**
- Hub mutants in test: 5
- Hub category counts: `{'NoCoup_Gi_bArr': 2, 'PrefCoup_Gi': 2, 'Coup_Gi_bArr': 1}`
- Background note: Prior narrative 14 PrefCoup / 20 Coup does not match full SD1 (64 PrefCoup_Gi / 250 Coup_Gi_bArr unfiltered; 60/249 after ≥25.0% WT expression). Enrichment uses expression-filtered full mutagenic background.

**Outcome B:** `FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED`

---

## Test C — Convergence

- Skipped: Skipped: requires A and B both SUPPORTED

---

## Combined verdict

**`CORE_TOPOLOGICAL_ONLY`**

Interpretation (exact): CORE_TOPOLOGICAL_ONLY → network architecture without sufficient functional evidence

Plain meaning: important roads ≠ proven controllers of the PrefCoup_Gαi2 decision. Physical architecture ≠ functional output.

**Hypothesis eliminated (Test B):** “The six static hubs are the functional core of Gαi2 bias.” Do **not** overclaim “the network has no relation to Gαi2” (other hubs / dynamics / combinations / redundancy / metric mismatch still possible).

Limit: Topology ≠ causal Gi necessity unless B supports; even CORE_CANDIDATE_SUPPORTED is a network candidate pending human review — not a switch.

Forbidden language in this deliverable: switch / núcleo universal probado / CORE_FOUND / CB2_Gi_NETWORK_CANDIDATE (not established).

**`LINE_PAUSE = TRUE`** — preserve `cfb2a51` as clean negative / topology-only result. No re-run, no next phase, no crossing topology×dynamics unless jointly decided later.

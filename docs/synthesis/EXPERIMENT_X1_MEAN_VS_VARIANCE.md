# Experiment X1 — Mean contact persistence vs temporal variance

**Fecha pre-registro:** 2026-09-09  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script.  
**Scope:** satellite discrimination test only. **Does not** reopen P1 as a hub hunt, does not invent new contact cutoffs, does not claim Gi mechanism.

---

## Question

Do high **temporal variance** contacts (“breathing” edges) overlap the static LigACN / six-hub neighborhood more than a degree-of-freedom-matched null, and more than high **mean** persistence contacts?

This discriminates whether static LigACN topology aligns with:

| Channel | Interpretation (descriptive only) |
|---------|-----------------------------------|
| High mean occupancy | Persistent contacts |
| High temporal variance | Breathing / flickering contacts |

---

## Data

Identical to P1:

```
DIR  = data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/
PSF  = 24306_dyn_2126.psf
XTCs = 24307…24311_trj_2126.xtc   # 5 replicas × 399 frames
```

---

## Contact definition (REUSE — DO NOT invent after seeing results)

Exact copy of P1 `CONTACT_DEF` in `scripts/network_core/p1_dynamic_hub_validation.py`:

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
p_ij_edge_threshold: 0.1   # used only to define the eligible edge pool filter below
exclude_sequential_protein: True  # drop |resid_i − resid_j| == 1 for protein–protein
selection: "protein or resname 8D0"
VdW radii: H 1.20, C 1.70, N 1.55, O 1.52, S 1.80, P 1.80, F 1.47, CL 1.75, BR 1.85, I 1.98
```

**No new distance cutoff.** Full GetContacts chemotype angles are not reimplemented (same P1 limitation).

---

## Metrics (locked)

For each unordered residue-pair edge `e={u,v}`:

1. **Mean occupancy**  
   `mean_e = (# frames with contact) / N_frames`  
   pooled over all 5 replicas (N_frames = sum of frames used).

2. **Temporal variance** (Bernoulli / binary indicator)  
   `var_e = mean_e * (1 − mean_e)`  
   (exact population variance of I_t ∈ {0,1}; sample form `n/(n−1)·var` reported but **ranking uses population form**).

3. **CV** (descriptive only; not primary ranking):  
   `cv_e = sqrt(var_e) / mean_e` for `mean_e > 0`.

**Eligible edge pool for ranking** (fixed a priori):

- Protein–protein or protein–ligand (8D0) pairs under CONTACT_DEF geometry accumulation.  
- Exclude sequential protein pairs `|Δresid|==1`.  
- Keep edges with **`mean_e ≥ 0.1`** (same AlloViz / P1 `p_ij` threshold) so the pool matches the P1 persistence graph edge set philosophy.  
- Undirected labels: `RESNAME:resid` as in P1 (`ALA:79`, `8D0:1`, …).

**Top-k:** `k = 200` (fixed). If `|pool| < k`, use `k_eff = |pool|` and mark `X1_INDETERMINATE` if `k_eff < 50`.

**Rank lists:**

- `TOP_MEAN`: top-k by `mean_e` descending (ties broken by label lexicographic).  
- `TOP_VAR`: top-k by `var_e` descending (ties broken by label lexicographic).

---

## Static reference sets (locked)

From Morales-Pastor Supp Data 3 (`41467_2025_60003_MOESM5_ESM.xlsx`, sheet `WT_degeneracy`) — same loader as `test_hubs_dual_validation.py`:

**Six hubs (frozen):**  
`ALA:79`, `ALA:83`, `LEU:287`, `ASN:291`, `ASN:295`, `ARG:302`

**S / T (frozen):**  
S = `8D0:1`, `SER:285`, `PHE:87`  
T = `ARG:131`, `ASP:240`, `SER:303`, `SER:69`

| Reference | Definition |
|-----------|------------|
| `REF_LIGACN` | Undirected edges `{u,v}` where directed LigACN has `w(u→v)>0` or `w(v→u)>0` |
| `REF_HUB_NBHD` | Undirected LigACN edges where **at least one** endpoint is in the six hubs **or** is a 1-hop LigACN neighbor of a hub (closed neighborhood edge set) |

Primary overlap test uses **`REF_HUB_NBHD`**. Report `REF_LIGACN` as secondary.

**Overlap statistic:**  
`overlap(list, REF) = |set(list) ∩ REF|`  
also report Jaccard `|∩| / |∪|` for the two top-k sets vs REF.

---

## Null model (locked)

```text
name: random_k_subset_from_eligible_pool
n_null: 1000
alpha: 0.05
RNG_SEED: 20260821
```

For each ranking channel (MEAN, VAR) and each REF:

1. Draw `n_null` random subsets of size `k` from the eligible edge pool (without replacement within a draw).  
2. Null overlaps = `|subset ∩ REF|`.  
3. Empirical upper-tail p: `(1 + #null ≥ observed) / (1 + n_null)`.  
4. **Beats null** iff `p ≤ alpha` (enrichment of REF among top-k).

Also compare channels: VAR “more than MEAN” iff  
`overlap_VAR > overlap_MEAN` **and** VAR beats null while MEAN does not;  
**or** both beat null and `overlap_VAR − overlap_MEAN` exceeds the 95th percentile of `(null_VAR − null_MEAN)` paired differences from the same null draws (shared random subsets).

---

## Verdicts (ONLY these labels)

| Label | Criterion |
|-------|-----------|
| `X1_VARIANCE_ALIGNS_STATIC` | VAR enrichment vs `REF_HUB_NBHD` beats null **and** aligns more than MEAN (rule above) |
| `X1_MEAN_ALIGNS_STATIC` | MEAN beats null / aligns more; VAR does not meet VAR-wins rule |
| `X1_NEITHER` | Neither MEAN nor VAR beats null on `REF_HUB_NBHD` |
| `X1_INDETERMINATE` | SHA/data failure, `k_eff < 50`, empty REF, or software missing |

If both beat null and neither dominates under the paired-difference rule → `X1_NEITHER` (neither channel uniquely aligns; do not invent a fifth label).

---

## Forbidden interpretations

- Do **not** call variance edges “new switches.”  
- Do **not** reinterpret P1 as rescued by cholesterol / membrane.  
- Do **not** claim Gi coupling mechanism.  
- Descriptive overlap only.

---

## Outputs

| Path | Content |
|------|---------|
| `scripts/network_core/x1_mean_vs_variance_contacts.py` | Runner |
| `results/network_core/x1_mean_vs_variance_report.md` | Human report + verdict |
| `results/network_core/x1_mean_vs_variance_report.json` | Machine payload |
| `results/network_core/x1_rank_lists.json` | Top-k mean / variance edge lists + overlaps |

---

## CLI

```bash
micromamba run -n janus_p1 python scripts/network_core/x1_mean_vs_variance_contacts.py
```

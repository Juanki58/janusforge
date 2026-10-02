# X1 — Mean contact vs temporal variance

**Generated (UTC):** 2026-09-09T20:12:37.303670+00:00
**Pre-registration:** `docs\synthesis\EXPERIMENT_X1_MEAN_VS_VARIANCE.md`
**X1 verdict:** `X1_MEAN_ALIGNS_STATIC`

## Contact definition (P1 reuse)

- `getcontacts_vdw_envelope_plus_alloviz_filters`
- Geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Angstrom; A,B non-hydrogen
- Eligible pool: `mean ≥ 0.1` (AlloViz / P1 threshold)
- Top-k: **200** (k_eff=200)

## Static references

- LigACN directed edges: 239
- REF_LIGACN undirected: 176
- REF_HUB_NBHD: 66

## Results (primary = REF_HUB_NBHD)

- Eligible edges: **1128**
- Frames pooled: **1995**
- Overlap top-mean ∩ hub-nbhd: **25** (p=0.0010; beats_null=True)
- Overlap top-var ∩ hub-nbhd: **0** (p=1.0000; beats_null=False)
- Null hub overlap mean / p95: 11.48 / 16.05
- Secondary LigACN overlaps mean/var: 74 / 2
- var_more_than_mean: **False**

## Verdict

**`X1_MEAN_ALIGNS_STATIC`**

## Governance

- Descriptive overlap only; not a new switch claim.
- Does not reopen P1 hub hypothesis or rescue via cholesterol.

## Artifacts

- `results/network_core/x1_rank_lists.json`
- `results/network_core/x1_mean_vs_variance_report.json`


# EXTERNAL — Toggle-continuo vs PrefCoup multi-trigger

**Run UTC:** `2026-10-02T23:01:01Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_TOGGLE_VS_MULTITRIGGER.md`  
**Mode:** literature discrimination table — no MD.

## Verdict

**`EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT`**

> Ganzoni/Kosar: continuo de eficacia en el bolsillo vía Trp258^6.48.  
> Morales SI Note 1: PrefCoup_Gαi2 por **varios** triggers (CWxP no universal entre clusters).  
> Predicción `ligando → Trp258 → Gαi2` suficiente = **rechazada** como modelo operativo.  
> No reabre P2; no claim Gi del proyecto.

## Discrimination table

| # | Prediction | Toggle-continuum | Multi-trigger PrefCoup | Relation |
|---|------------|------------------|------------------------|----------|
| 1 | PrefCoup_Gαi2 arises from mutations that need not hit W258 | Neutral/underspecified — continuum is ligand–W258 efficacy, not PrefCoup mutant census | SUPPORTED — clusters 1–3 mutate sites across TM3/5/7/ECL2; W258 not required as mutant site | **LEVEL_OK** |
| 2 | W258 partner-contact stability changes in some PrefCoup clusters only | Would predict W258 contacts always central if toggle were unique PrefCoup gate | SUPPORTED — SI Note 1: cluster1 W258–L195↑; cluster2 W258–C288/N291↓; cluster3 CWxP not highlighted | **CONFLICT** |
| 3 | Single-position HU-308 edits retune efficacy continuum via W258 without unique PrefCoup path claim | SUPPORTED — Ganzoni / Kosar | Compatible — does not assert single PrefCoup trigger | **LEVEL_OK** |
| 4 | Na-site / NPxxY / DRY appear as PrefCoup features independent of CWxP in ≥1 cluster | False if toggle-only model of PrefCoup | SUPPORTED — cluster3 NPxxY+Na+DRY; cluster2 Na+DRY+EC TM7/1/2; CWxP not universal | **CONFLICT** |
| 5 | Operational chain ligando → Trp258 → Gαi2 is sufficient | Tempting over-read of Ganzoni — NOT claimed as Gi-sufficient by authors as unique path | REJECTED — multiple triggers → same PrefCoup; LigACN distributed | **CONFLICT** |

## Governance

```text
VERDICT: EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT
P2_REOPEN: FALSE
Gi_FUNCTIONAL_CLAIM: FALSE
DOCKING: STOP
```

## References

1. Ganzoni et al. — DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)
2. Kosar et al. — DOI [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461)
3. Morales-Pastor et al. + SI Note 1 — DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)

---

*Fin EXTERNAL toggle vs multi-trigger.*

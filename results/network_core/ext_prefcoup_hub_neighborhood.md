# EXTERNAL — PrefCoup cluster-2/3 → hub neighborhood

**Run UTC:** `2026-10-02T23:01:01Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_PREFCOUP_HUB_NEIGHBORHOOD.md`  
**Source:** Morales-Pastor SI Note 1 (MOESM1)

## Verdict

**`EXT_PREFCOUP_HUB_NEIGHBORHOOD_OVERLAP`**

> N291 es hub exacto en contactos cluster-2 (W258–N291) y mutante PrefCoup cluster-3.  
> C288≈L287 y D80≈A79 son **proxies adyacentes** (no identidad).  
> N295 (hub) aparece en contactos NPxxY de cluster-3.  
> No reabre Fisher PrefCoup / P1 / P2.

## Proxy map

| SI residue | Hub proxy | Relation |
|------------|-----------|----------|
| N291 | ASN291 | exact |
| C288 | LEU287 | adjacent Δseq=1 |
| D80 | ALA79 | adjacent Δseq=1 (Na-site) |

## Contact inventory (SI Note 1)

| Cluster | Contact | Stability (PrefCoup) | Class | Hub link |
|---------|---------|----------------------|-------|----------|
| 2 | W258–C288 | less_stable | **PROXY_NEIGHBOR** | LEU287 |
| 2 | W258–N291 | less_stable | **EXACT_HUB** | ASN291 |
| 2 | S292–S47 | more_stable | **NON_HUB** | — |
| 2 | R131–T127 | more_stable | **NON_HUB** | — |
| 2 | C40–F87 | more_stable | **NON_HUB** | — |
| 2 | C40–F91 | less_stable | **NON_HUB** | — |
| 2 | S285–G44 | less_stable | **NON_HUB** | — |
| 3 | N295–N51 (NPxxY) | more_stable | **EXACT_HUB** | ASN295 |
| 3 | NPxxY–D80 | more_stable | **EXACT_HUB** | ASN295 |
| 3 | R131–T127 | more_stable | **NON_HUB** | — |
| 3 | R131–T246 | more_stable | **NON_HUB** | — |

## PrefCoup mutant overlay (prior)

- Cluster 2 mutants: 77, 117, 217
- Cluster 3 mutants: 199, 205, **291**, **302** (hubs N291, R302)

## Governance

```text
VERDICT: EXT_PREFCOUP_HUB_NEIGHBORHOOD_OVERLAP
PROXY_NEQ_IDENTITY: TRUE
Gi_ENRICHMENT_REOPEN: FALSE
P2_REOPEN: FALSE
```

---

*Fin EXTERNAL PrefCoup hub neighborhood.*

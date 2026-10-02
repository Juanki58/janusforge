# Experiment — EXTERNAL: PrefCoup cluster-2/3 contacts → hub neighborhood inventory

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — SI inventory only.  
**Scope:** **`EXTERNAL_PREFCOUP_HUB_NEIGHBORHOOD`** — mapear contactos destacados de PrefCoup clusters 2/3 (SI Note 1) a vecindad de hubs congelados (N291; C288≈L287; D80≈A79).  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Inventario SI Note 1 / Fig. 5E contactos vs hubs | Reabrir Test B PrefCoup Fisher / Gi enrichment |
| Proxies explícitos C288≈L287, D80≈A79 (adyacencia UniProt) | Tratar proxy como identidad residual |
| Veredicto `EXT_PREFCOUP_HUB_NEIGHBORHOOD_*` | Docking; P2 reopen; DEER inventado |

```text
P1 / P2 / STATIC dual-test = UNCHANGED
Gi_claims = STOP
EXT_PREFCOUP_HUB_NEIGHBORHOOD_* = NEW
```

**Pregunta discriminante:**

> ¿Los contactos PrefCoup cluster-2/3 publicados tocan hubs Janusforge (o vecinos inmediatos publicados), o son un objeto disjunto?

---

## Locked maps

### Hubs (fixed)

ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46)

### Proxies (SI → hub neighborhood; locked)

| SI residue | BW/GPCRdb | Hub proxy | Relation |
|------------|-----------|-----------|----------|
| N291 | 7x45 | **ASN291** | exact |
| C288 | 7x41 | LEU287 | adjacent (Δseq=1); SI uses C288 not L287 |
| D80 | 2x50 | ALA79 | adjacent (Δseq=1); Na-site |

### PrefCoup clusters (published)

- Cluster 2 mutants: 77, 117, 217  
- Cluster 3 mutants: 199, 205, 291, 302  

Contacts from SI Note 1 (not mutant list alone).

---

## Scoring

Per contact: `EXACT_HUB` | `PROXY_NEIGHBOR` | `NON_HUB` | `INDETERMINATE`

Aggregate:

| Call | Criterio |
|------|----------|
| **`EXT_PREFCOUP_HUB_NEIGHBORHOOD_OVERLAP`** | ≥1 EXACT_HUB in cluster 2 or 3 highlighted contacts **and** ≥1 PROXY_NEIGHBOR |
| **`EXT_PREFCOUP_HUB_NEIGHBORHOOD_PARTIAL`** | Exact **or** proxy only (not both classes) |
| **`EXT_PREFCOUP_HUB_NEIGHBORHOOD_ABSENT`** | No exact/proxy in cluster 2/3 SI contacts |
| **`EXT_PREFCOUP_HUB_NEIGHBORHOOD_INDETERMINATE`** | SI Note 1 unavailable |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_PREFCOUP_HUB_NEIGHBORHOOD.md` |
| Report | `results/network_core/ext_prefcoup_hub_neighborhood.md` |
| JSON | `results/network_core/ext_prefcoup_hub_neighborhood.json` |
| Script | `scripts/network_core/ext_prefcoup_hub_neighborhood.py` |

---

*Fin pre-registro. SI inventory only.*

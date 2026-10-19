# EXTERNAL inventory — hubs ↔ LigACNtop / PrefCoup clusters

**Run UTC:** `2026-09-21T19:03:33Z`  
**Branch context:** `feat/cb2-hubs-functional-topology-test`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_HUBS_VS_LIGACN_INVENTORY.md`  
**Literature:** Morales-Pastor et al., *Nat Commun* (2025), DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)

## Verdict

**Primary (LigACNtop):** `EXT_HUBS_IN_LIGACNTOP`  
**PrefCoup overlay (secondary):** `PARTIAL`  

> EXTERNAL inventory only. Does **not** reopen P1, P2, or Gi enrichment claims. Static dual-test remains `CORE_TOPOLOGICAL_ONLY`.

## Plain-language answer

Los seis hubs caen **dentro de LigACNtop** (6/6 nodos con degeneracy≥0.146; distancia 0). No son un objeto topológico disjunto del mapa publicado. Overlay PrefCoup clusters 1–3: 2/6 posiciones hub (N291A y R302A en cluster 3); el resto no está en mutantes PrefCoup simulados de esos clusters. Esto **no** reabre el enrichment Fisher del dual-test ni P1 dinámico.

## Provenance

- MOESM5 (Supp Data 3): `results/network_core/_raw_downloads/41467_2025_60003_MOESM5_ESM.xlsx` sha256=`ff53ec7bf227e0d2c3e5ced9fb81e2e56e61fb5d6ec373c1e3f2c574e77c09b9`
- MOESM3 (Supp Data 1): `results/network_core/_raw_downloads/41467_2025_60003_MOESM3_ESM.xlsx` sha256=`f296cb131c22d32de9985fe54fb17422f72385aed2b0596e8ed180f07b7e2a7a`
- LigACNtop cutoff: degeneracy ≥ **0.146** (Morales-Pastor Methods / Fig. 3)
- LigACNtop edges / nodes: **33** / **41**
- PrefCoup `groups` verify match: `True`

## Per-hub inventory

| Hub | BW | in LigACN | in LigACNtop | dist→top | max degeneracy | PrefCoup cluster | SD1 profile |
|-----|----|-----------|--------------|----------|----------------|------------------|-------------|
| `ALA:79` | 2.49 | True | **True** | 0 | 0.2265 | NOT_IN_SIMULATED_PREFCOUP_CLUSTERS | A79V / NoCoup_Gi_bArr / not simulated |
| `ALA:83` | 2.53 | True | **True** | 0 | 0.3760 | NOT_IN_SIMULATED_PREFCOUP_CLUSTERS | A83V / NoCoup_Gi_bArr / not simulated |
| `LEU:287` | 7.41 | True | **True** | 0 | 0.4165 | NOT_IN_SIMULATED_PREFCOUP_CLUSTERS | L287A / Coup_Gi_bArr / not simulated |
| `ASN:291` | 7.45 | True | **True** | 0 | 0.4055 | 3 | N291A / PrefCoup_Gi / simulated |
| `ASN:295` | 7.49 | True | **True** | 0 | 0.3990 | NOT_IN_SIMULATED_PREFCOUP_CLUSTERS | N295A / NoCoup_Gi_bArr / not simulated |
| `ARG:302` | 8.46 | True | **True** | 0 | 0.3015 | 3 | R302A / PrefCoup_Gi / simulated |

### LigACNtop edges incident to hubs

- `ALA:79`: ALA:83→ALA:79 (0.2265), ALA:79→SER:75 (0.1565)
- `ALA:83`: PHE:87→ALA:83 (0.3760), ALA:83→ALA:79 (0.2265), ALA:83→PHE:81 (0.1575)
- `LEU:287`: LEU:287→LEU:289 (0.4165), SER:285→LEU:287 (0.3855)
- `ASN:291`: LEU:289→ASN:291 (0.4055), ASN:291→ASN:295 (0.3990)
- `ASN:295`: ASN:291→ASN:295 (0.3990), ASN:295→VAL:297 (0.1560)
- `ARG:302`: ARG:302→THR:246 (0.3015), ILE:298→ARG:302 (0.2955)

## PrefCoup clusters 1–3 (published mutant positions)

- **Cluster 1:** 109, 125, 176, 285, 292
- **Cluster 2:** 77, 117, 217
- **Cluster 3:** 199, 205, 291, 302
- PrefCoup simulated not in `groups`: 297, 61

## Aggregates

- Hubs in LigACNtop: **6/6**
- Hubs in any PrefCoup cluster 1–3: **2/6**
- Jaccard(hubs, LigACNtop nodes): **0.1463**

## Governance

```yaml
mode: EXTERNAL_HUBS_VS_LIGACN_INVENTORY
MODO: READ_ONLY_DATA
P1_DYNAMIC_HUBS: CLOSED_NOT_SUPPORTED_UNCHANGED
P2_MSM: CLOSED_INSUFFICIENT_SAMPLING_UNCHANGED
STATIC_DUAL_TEST: CORE_TOPOLOGICAL_ONLY_UNCHANGED
Gi_claims: STOP
docking: STOP
de_novo: STOP
hub_list: FIXED_A_PRIORI_NO_RETUNE
literature_doi: 10.1038/s41467-025-60003-0
prefcoup_code: https://github.com/GPCRmd/prefcoup_cb2r
zenodo: 10.5281/zenodo.15270434
```


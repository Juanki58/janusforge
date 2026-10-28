# Experiment — EXTERNAL inventory: six Janusforge hubs ↔ LigACNtop / PrefCoup clusters

**Fecha pre-registro:** 2026-09-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — definiciones y veredicto bloqueados **antes** de fijar el call final del inventario.  
**Scope:** **`EXTERNAL_HUBS_VS_LIGACN_INVENTORY`** — cruce de índices UniProt P34972 (seis hubs congelados) con Morales-Pastor Supp Data 3 (LigACNtop) + clusters PrefCoup 1–3 del SI / código publicado.  
**PI authorization:** YES (ítem 2 de [`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md) §4.2 — esfuerzo bajo).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Inventario de **membresía / distancia** hubs ↔ LigACNtop y ↔ PrefCoup clusters 1–3 | Reabrir P1 como hub hunt / retunar el set de seis hubs |
| Reconstrucción **reproducible** de LigACNtop desde `WT_degeneracy` con cutoff publicado | Afirmar mecanismo Gi / PrefCoup enrichment (ya cerrado en dual-test) |
| Overlay descriptivo con SD1 (categoría mutante en posición hub) | Reabrir P2 Gate-1; MSM; docking / de novo |
| Veredicto EXTERNAL `EXT_HUBS_*` | Sustituir `CORE_TOPOLOGICAL_ONLY` / `STATIC_BOTTLENECKS` |

```text
P1_DYNAMIC_HUBS                 = CLOSED (NOT_SUPPORTED)           # unchanged
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
STATIC_LIGACN / dual-test       = CORE_TOPOLOGICAL_ONLY (cfb2a51)  # unchanged
EXT_HUBS_VS_LIGACN_*            = NEW (this experiment)
Gi / docking / de novo          = STOP
```

**Explicit non-claim (locked):**

> Este inventario **no** rescata P1, **no** afirma que los seis hubs controlen PrefCoup_Gαi2, y **no** reabre P2.  
> Solo aclara si el objeto topológico Janusforge (seis hubs) cae **dentro** de LigACNtop / clusters publicados o es un objeto **distinto**.

**Pregunta discriminante (locked):**

> ¿Los seis hubs congelados (ALA79, ALA83, LEU287, ASN291, ASN295, ARG302) son nodos / vecinos de **LigACNtop** (y/o mutantes en PrefCoup clusters 1–3), o un objeto topológico disjunto del mapa publicado?

---

## Fixed objects (locked)

### Six hubs (a priori — no retune)

| LigACN label | Short | BW |
|--------------|-------|----|
| `ALA:79` | ALA79 | 2.49 |
| `ALA:83` | ALA83 | 2.53 |
| `LEU:287` | LEU287 | 7.41 |
| `ASN:291` | ASN291 | 7.45 |
| `ASN:295` | ASN295 | 7.49 |
| `ARG:302` | ARG302 | 8.46 |

### LigACN / LigACNtop (Morales-Pastor Methods)

- **Source:** Supp Data 3 = `41467_2025_60003_MOESM5_ESM.xlsx` sheet `WT_degeneracy`  
  Path canónico: `results/network_core/_raw_downloads/41467_2025_60003_MOESM5_ESM.xlsx`
- **LigACN graph:** directed edge `u→v` iff cell `(u,v) > 0` (misma construcción que `static_ligacn_topology` / dual-test).
- **LigACNtop (publicado):** edges con **degeneracy ≥ 0.146** (Methods: *Computing the distance to … LigACN top*; Fig. 3 caption cutoff 0.146).
- **LigACNtop nodes:** endpoints de esas edges.
- **Distance hub → LigACNtop:** hop-count en el grafo **no dirigido** de contactos LigACN (`w>0` en cualquier dirección) desde el hub hasta el nodo LigACNtop más cercano. Distancia **0** = el hub es nodo LigACNtop.

### PrefCoup clusters 1–3

- Clusters de **mutantes PrefCoup_Gαi2 simulados** (PCA contact frequencies + K-means / groups publicados), **no** clusters de residuos arbitarios.
- Fuente preferida (en orden): (1) notebook publicado [GPCRmd/prefcoup_cb2r](https://github.com/GPCRmd/prefcoup_cb2r) `clustering.ipynb` dict `groups`; (2) Zenodo [10.5281/zenodo.15270434](https://doi.org/10.5281/zenodo.15270434) si aporta labels; (3) SI Fig. 2 / Source Data si está local.
- Overlay: ¿la **posición** de cada hub aparece como `mutant_id` en cluster 1, 2 o 3?
- SD1 (`MOESM3`) solo para categoría acoplamiento en esa posición (inventario; **no** Fisher nuevo).

---

## Metrics (locked)

Para cada hub reportar:

1. `in_LigACN` (bool)  
2. `in_LigACNtop` (bool; dist==0)  
3. `dist_to_LigACNtop` (int | null)  
4. `max_incident_degeneracy` (float)  
5. `ligacntop_edges_incident` (list)  
6. `prefcoup_cluster` (`1|2|3|NONE|NOT_IN_SIMULATED_PREFCOUP`)  
7. `sd1_coupling_profile` + `sd1_simulated` (desde MOESM3)

Agregados:

- `n_hubs_in_LigACNtop` / 6  
- `n_hubs_in_any_PrefCoup_cluster` / 6  
- `jaccard_hubs_vs_LigACNtop_nodes` = `|hubs ∩ top_nodes| / |hubs ∪ top_nodes|` (sobre sets de labels)

---

## Verdict rules (locked — primary = LigACNtop)

| Call | Criterio |
|------|----------|
| **`EXT_HUBS_IN_LIGACNTOP`** | ≥ **5/6** hubs con `in_LigACNtop=True` |
| **`PARTIAL`** | **2–4/6** en LigACNtop **o** todos en LigACN pero mayoría solo a distancia 1 del top |
| **`DISTINCT`** | ≤ **1/6** en LigACNtop **y** mediana `dist_to_LigACNtop` ≥ 2 |
| **`INDETERMINATE_MISSING_SUPP`** | Falta MOESM5 local **y** no se puede recuperar desde Nature SI / mirror; o cutoff 0.146 no reproducible |

**PrefCoup overlay (secundario, no override del call primario):**

- Reportar `prefcoup_overlay = FULL | PARTIAL | NONE | INDETERMINATE`  
  - FULL: ≥5/6 hubs en algún cluster 1–3  
  - PARTIAL: 1–4/6  
  - NONE: 0/6  
  - INDETERMINATE: no se recuperó `groups` / membership

---

## Fail-closed

- Si falta `MOESM5` → intentar descarga Springer ESM; si falla → `INDETERMINATE_MISSING_SUPP` (no inventar cutoff ni matriz).  
- Si falta membership de clusters → inventario LigACNtop igual; overlay PrefCoup = `INDETERMINATE` (no inventar clusters desde figuras).  
- No retunar hubs; no añadir residuos “parecidos”.

---

## Outputs (locked)

| Artefacto | Path |
|-----------|------|
| Este pre-reg | `docs/synthesis/EXPERIMENT_HUBS_VS_LIGACN_INVENTORY.md` |
| Script | `scripts/network_core/hubs_vs_ligacn_inventory.py` |
| Results | `results/network_core/hubs_vs_ligacn_inventory.{md,json}` |

---

## Literature anchors

1. Morales-Pastor et al., *Nat Commun* (2025) DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)  
2. Code: [GPCRmd/prefcoup_cb2r](https://github.com/GPCRmd/prefcoup_cb2r) · Zenodo [10.5281/zenodo.15270434](https://doi.org/10.5281/zenodo.15270434)  
3. Prior Janusforge: `hubs_dual_validation_*`, `static_ligacn_topology_*`, `x1_mean_vs_variance_*`

---

*Fin del pre-registro. Flags P1/P2 / CORE_TOPOLOGICAL_ONLY no se modifican por este experimento.*

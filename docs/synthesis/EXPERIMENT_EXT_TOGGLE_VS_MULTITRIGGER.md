# Experiment — EXTERNAL: Toggle-continuo (Trp258/Ganzoni) vs multi-trigger PrefCoup (Morales SI Note 1)

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — lit discrimination table only.  
**Scope:** **`EXTERNAL_TOGGLE_VS_MULTITRIGGER`** — tabla de predicciones que discriminan “continuo de eficacia vía Trp258^6.48” vs “múltiples triggers PrefCoup_Gαi2”.  
**PI authorization:** YES (blanket advance; EXTERNAL optics without GPU).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Tabla lit. de predicciones mutuamente discriminantes | Afirmar Gi funcional del proyecto como probado |
| Citar Ganzoni / Kosar / Morales SI Note 1 / Fig. 5 | Reabrir P2; docking; inventar distancias DEER |
| Veredicto `EXT_TOGGLE_VS_MULTITRIGGER_*` | Colapsar a “toggle = mecanismo único” o “toggle irrelevante” |
| Preferir INDETERMINATE si papers no dan predicción | Reabrir P1 como hub hunt |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P1_DYNAMIC_HUBS                 = CLOSED (NOT_SUPPORTED)           # unchanged
STATIC_LIGACN                   = CORE_TOPOLOGICAL_ONLY            # unchanged
Gi / docking / de novo / Tier B = STOP
EXT_TOGGLE_VS_MULTITRIGGER_*    = NEW
```

**Explicit non-claim:**

> Discriminar **niveles** (eficacia de bolsillo vs PrefCoup multi-entrada) ≠ demostrar mecanismo Janusforge.  
> Ambos papers pueden ser verdaderos a distinto nivel sin armonización post hoc.

**Pregunta discriminante:**

> ¿Qué predicciones observables separarían un modelo operativo “continuo Trp258 basta” de “PrefCoup requiere / admite triggers fuera del toggle”?

---

## Source set (locked)

| # | Source | DOI / path | Role |
|---|--------|------------|------|
| 1 | Ganzoni et al. *Chem. Sci.* 2026 | [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B) | Continuo eficacia vía W258^6.48 |
| 2 | Kosar et al. *ACS Cent. Sci.* 2024 | [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461) | Inverso / constricción toggle |
| 3 | Morales-Pastor et al. 2025 + SI Note 1 | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); MOESM1 in `_raw_downloads/` | Multi-trigger PrefCoup clusters 1–3 |
| 4 | Prior survey | `CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md` | Tension table (no reopen) |

---

## Discriminating predictions (locked a priori)

For each row: expected under **TOGGLE_CONTINUUM** vs **MULTI_TRIGGER_PREFCOUP**, and whether they **CONFLICT** (mutually exclusive) or **LEVEL_OK** (compatible at different levels).

1. PrefCoup_Gαi2 can arise from mutations **without** requiring W258 as the mutated site.  
2. Contact stability of W258–partner pairs changes in **some but not all** PrefCoup clusters (SI Note 1).  
3. Single-position HU-308 scaffold edits retune efficacy continuum via W258 **without** claiming unique PrefCoup path.  
4. Na-site / NPxxY / DRY perturbations appear as PrefCoup cluster features **independent** of CWxP in ≥1 cluster.  
5. Operational model `ligando → Trp258 → Gαi2` as **sufficient** chain.

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_TOGGLE_VS_MULTITRIGGER_DISCRIMINABLE`** | ≥3 filas CONFLICT con ancla lit. clara; fila 5 = CONFLICT rejected |
| **`EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT`** | ≥3 filas LEVEL_OK + ≥1 CONFLICT (coexistencia de niveles con ≥1 predicción exclusiva) |
| **`EXT_TOGGLE_VS_MULTITRIGGER_INDETERMINATE`** | SI / papers no accesibles |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_TOGGLE_VS_MULTITRIGGER.md` |
| Report | `results/network_core/ext_toggle_vs_multitrigger.md` |
| JSON | `results/network_core/ext_toggle_vs_multitrigger.json` |
| Script | `scripts/network_core/ext_toggle_vs_multitrigger.py` |

---

*Fin pre-registro. Lit-only.*

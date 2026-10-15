# Experiment — EXTERNAL: EPR/NMR experimental anchors ↔ repo coords / hubs / Phase F–G

**Fecha pre-registro:** 2026-09-22  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — definiciones y reglas de veredicto locked **antes** del checklist final.  
**Scope:** **`EXTERNAL_EPR_NMR_ANCHORS`** — checklist cualitativa de sitios CW-EPR (Yeliseev) + DNP-MAS NMR vs predicciones ya en repo (hubs, Phase F/G, contactos estáticos / landmarks).  
**PI authorization:** YES (ítem ★ default / §4.3 de [`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md)).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Tabla sitio experimental → observación lit. → predicción cualitativa del repo | Inventar restraints DEER/FRET / distancias NMR para MD |
| Cruzar índices UniProt P34972 con hubs / TM3–TM6 / TM7 / ICL3 | Reabrir P2 Gate-1; MSM; docking / de novo |
| Afirmar compatibilidad / tensión / ausencia de predicción | Claim funcional Gi; “validamos” Phase G con EPR |
| Veredicto `EXT_EPR_NMR_ANCHORS_*` | Tratar CW-EPR o line-width NMR como mapa de activación completo |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P1_DYNAMIC_HUBS                 = CLOSED (NOT_SUPPORTED)           # unchanged
DEER_CB2_DISTANCE_MAP           = ABSENT (literature)              # locked
Gi / docking / de novo          = STOP
EXT_EPR_NMR_ANCHORS_*           = NEW (this experiment)
```

**Explicit non-claim (locked):**

> Este checklist **no** añade restraints al MD, **no** afirma mecanismo Gi, y **no** reabre P2.  
> Solo pregunta si las anclas experimentales **cualitativas** (movilidad / restricción local) son compatibles con lo que el repo ya predice en Phase F/G + hubs/contactos, y dónde un **futuro DEER** discriminaría.

**Pregunta discriminante (locked):**

> ¿Phase F/G + hubs/contactos predicen **más movilidad / libertad conformacional** donde CW-EPR y DNP-NMR la ven (ICL3), y **más orden / sensibilidad ligando** en TM7 (M293), sin fingir un mapa de distancias DEER?

---

## Fixed experimental anchors (locked a priori)

### A) Yeliseev et al. CW-EPR (2021)

- DOI [10.1016/j.bbamem.2021.183603](https://doi.org/10.1016/j.bbamem.2021.183603) · PMC [PMC8154700](https://pmc.ncbi.nlm.nih.gov/articles/PMC8154700/)
- **IL3 / ICL3 center:** labels ~H217–H226 (p.ej. G225C) → **alta movilidad** (C2/C1 ↑).
- **A270C** (punta **extracelular** TM6): más móvil con agonista CP-55,940 vs inverso SR-144,528.
- **DEER:** propuesto como siguiente paso; **no** mapa de distancias CB2 publicado.

### B) DNP-MAS NMR (ACS Omega 2023)

- DOI [10.1021/acsomega.3c04681](https://doi.org/10.1021/acsomega.3c04681)
- **M237–R238 (ICL3):** espacio conformacional **amplio** (líneas anchas) bajo ligandos ensayados.
- **M293–V294 (TM7, cerca NPxxY):** espacio **más restringido**; sitio **sensible al ligando**.

### C) Colesterol (contexto, no restricción)

- Yeliseev *Sci. Rep.* 2021 [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6): MD → ICL3–TM6 IC (≈221–236) más desplazado/fluctuante con colesterol — ancla P5, **no** usada aquí como Gate.

---

## Repo objects to cross (locked — no new MD)

| Objeto | Path / ancla |
|--------|----------------|
| Six hubs | ALA79, ALA83, LEU287, ASN291, ASN295, ARG302 (`DYNAMIC_REANALYSIS_PROTOCOL` / dual-test) |
| Phase F fingerprint | `results/conformational/fase_f_conformational_fingerprint.md` — TM3–TM6 IC, Trp258 χ, ECL2 |
| Phase G | `results/conformational/fase_g_generalization_report.md` — GENERALIZES macro |
| Landmark soft | `EXT_LANDMARK_CONTACTS_STABLE` / expanded |
| Static topology | `STATIC_BOTTLENECKS` TM2/TM7/H8; hubs in LigACNtop (`EXT_HUBS_IN_LIGACNTOP`) |
| Atlas | [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md) |

**Predicciones cualitativas a priori (antes del call):**

1. **ICL3 flexible:** Phase F/G modelan apertura IC TM3–TM6; cristal inactivo 5ZTY **elimina** IL3 → predicción repo: ICL3 **no** es región “rígida de hub permanente”. Esperado: **compatible** con alta movilidad EPR/NMR en ICL3.
2. **TM7 ordenado / red:** hubs LEU287 / ASN291 / ASN295 en TM7–NPxxY; static bottlenecks → predicción: M293 en entorno **ordenado / acoplado a red**, no loop floppy. Esperado: **compatible** con NMR “restricted + ligand-sensitive”.
3. **A270 EC TM6:** Phase F/G priorizan IC + toggle W258^6.48, **no** punta EC A270 → predicción específica **ausente** → fila = `NO_PRIOR_PRED` (no inventar).
4. **DEER:** `ABSENT` — filas DEER = `NO_RESTRAINTS`.

---

## Scoring per site (locked)

| Call por sitio | Criterio |
|----------------|----------|
| `AGREE` | Predicción cualitativa del repo y observación lit. apuntan en la **misma dirección** (flex vs orden; IC opening) |
| `TENSION` | Direcciones opuestas explícitas |
| `NO_PRIOR_PRED` | Sitio experimental fuera del alcance de Phase F/G / hubs (honest gap) |
| `ABSENT_RESTRAINT` | Técnica de distancia no publicada (DEER) |

---

## Aggregate verdict rules (locked)

| Call | Criterio |
|------|----------|
| **`EXT_EPR_NMR_ANCHORS_AGREE`** | ≥3 sitios con predicción prior (excl. DEER) = `AGREE` y **0** `TENSION` |
| **`EXT_EPR_NMR_ANCHORS_PARTIAL_AGREE`** | Mezcla `AGREE` + `NO_PRIOR_PRED`; **0** `TENSION` fuerte |
| **`EXT_EPR_NMR_ANCHORS_TENSION`** | ≥1 `TENSION` en ICL3 flex o TM7 order |
| **`EXT_EPR_NMR_ANCHORS_INDETERMINATE`** | Docs Phase F/G / hubs no localizables |

Secondary annotation (no override): `DEER_CB2 = ABSENT`.

---

## Outputs (locked)

| Artefacto | Path |
|-----------|------|
| Pre-reg (este) | `docs/synthesis/EXPERIMENT_EXT_EPR_NMR_ANCHORS.md` |
| Report | `results/network_core/ext_epr_nmr_anchors.md` |
| Machine | `results/network_core/ext_epr_nmr_anchors.json` |
| Optional helper | `scripts/network_core/ext_epr_nmr_anchors.py` |

---

## Fail-closed

- No inventar distancias DEER “típicas” de class A.  
- No usar colesterol Yeliseev para reabrir P5 execution.  
- No promover soft landmark STABLE a “red rígida que niega ICL3 flex”.

---

*Fin pre-registro. Checklist EXTERNAL; sin restraints; sin reopen P2.*

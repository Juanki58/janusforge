# Experiment — EXTERNAL: DEER candidate design (DOC ONLY)

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — documentation design only.  
**Scope:** **`EXTERNAL_DEER_CANDIDATES`** — pares candidatos para un futuro DEER CB2, anclados a sitios Yeliseev / Phase F–G / hubs, **sin distancias inventadas**.  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Lista de pares sitio–sitio con **motivo discriminante** | Inventar r₀ / distancias DEER / restraints MD |
| Citar que DEER CB2 **no está publicado** | Tratar CW-EPR como mapa de distancias |
| Veredicto `EXT_DEER_CANDIDATES_*` | Ejecutar MD; P2 reopen; Gi claim |

```text
DEER_CB2_DISTANCE_MAP = ABSENT   # locked
RESTRAINTS_ADDED      = FALSE
EXT_DEER_CANDIDATES_* = NEW
```

**Pregunta discriminante (condicional, futuro):**

> Si hubiera muestreo propio, ¿qué pares DEER separarían apertura IC TM3–TM6 (activación) de flexibilidad ICL3-local vs orden TM7/hub corridor?

---

## Locked candidate pairs (no distances)

| ID | Site A | Site B | Why discriminate | Status |
|----|--------|--------|------------------|--------|
| D1 | ICL3 center (~G225C class) | TM6 IC / ICL3 edge | Local ICL3 mobility vs global | DESIGN_ONLY |
| D2 | TM3 IC (near R131 DRY) | TM6 IC (near T246 / IC tip) | Activation opening (Phase F/G axis) | DESIGN_ONLY |
| D3 | M293 / TM7 hub corridor | TM2 / A79–A83 neighborhood | Hub–hub corridor persistence | DESIGN_ONLY |
| D4 | A270C (TM6 EC tip) | ECL2 / vestibule | EC tip mobility (EPR lit.) — **no prior Phase F pred.** | DESIGN_ONLY |
| D5 | N291 / N295 | R302 H8 | TM7–H8 static bottleneck neighborhood | DESIGN_ONLY |

**Explicit:** no Å values; no spin-label rotamer library run here.

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_DEER_CANDIDATES_DESIGNED_NO_DISTANCES`** | ≥4 pares con motivo + DEER map ABSENT affirmed |
| **`EXT_DEER_CANDIDATES_INDETERMINATE`** | Anchors EPR/Phase F docs missing |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_DEER_CANDIDATES.md` |
| Report | `results/network_core/ext_deer_candidates.md` |
| JSON | `results/network_core/ext_deer_candidates.json` |
| Script | `scripts/network_core/ext_deer_candidates.py` |

---

*Fin pre-registro. DOC ONLY.*

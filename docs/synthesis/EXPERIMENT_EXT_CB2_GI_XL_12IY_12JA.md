# Experiment — EXTERNAL extension: Mnpotra 2014 XL pairs on PDB 12IY / 12JA

**Fecha pre-registro:** 2026-10-19  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** extensión de protocolo locked — **mismo método / mismas ventanas** que [`EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md`](EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md).  
**Scope:** **`EXTERNAL_CB2_GI_XL_12IY_12JA`** — contraste de proximidad intermolecular CB2↔Gαi1 en estructuras Rachman 2026.  
**PI authorization:** YES (orden PI 2026-10-19: extender comparación a 12IY y 12JA).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Aplicar parejas XL + ventanas Cα del parent 2014 | Inventar nuevo protocolo / umbrales |
| Descargar mmCIF RCSB si no hay `.pdb` | Claim funcional Gi; hubs; cerrar P3 |
| Reportar `N/A_NO_GI` si el depósito no tiene Gi | Reabrir P2; avanzar P5; docking; Tier B MD |
| Veredicto `EXT_CB2_GI_XL_12IY_12JA_*` | Inventar contactos si residuos no mapeables |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)
P5_MEMBRANE                     = NOT advanced
PROTOCOL                        = SAME_AS_EXT_CB2_GI_CROSSLINK_2014
XL_MEASURES                     = INTERMOLECULAR_PROXIMITY_ONLY
EXT_CB2_GI_XL_12IY_12JA_*       = NEW (this extension)
```

**Explicit non-claim:** XL = proximidad intermolecular CB2↔Gi bajo geometría del reactivo. **No** distancias intramoleculares de CB2; **no** prueba de hubs Janusforge.

**Pregunta discriminante:**

> Bajo las ventanas Cα–Cα locked de Mnpotra 2014, ¿12IY y 12JA son geométricamente compatibles con las tres parejas XL, o hay tensión / depósitos sin Gi (`INDETERMINATE` / `N/A_NO_GI`)?

---

## Structures (locked)

| PDB | Esperado | Nota atlas |
|-----|----------|------------|
| **12IY** | Puede ser receptor-only (refinamiento local '5249) | Atlas: activo + Gi (serie); **verificar** contenido real del depósito |
| **12JA** | CB2–Gi + agonista '1029 | Complejo Gi |
| **12IZ** (appendix only) | CB2–Gi + '5249 | Contraparte Gi de la serie 12IY; **no** sustituye el panel PI |

Fuentes: RCSB mmCIF (`files.rcsb.org/download/{id}.cif`) — no hay `.pdb` legacy para estos IDs. Local: `data/external/cb2_landmark_expanded/`.

---

## Metrics (locked — identical to parent)

| Pair | Window |
|------|--------|
| C134–C351 (HgCl2) | Cα–Cα **7–10 Å** |
| K245–K349 (DSS) | Cα–Cα **≤24.2 Å** |
| K215–K317 (DSS) | Cα–Cα **≤24.2 Å** |

Calls: `WITHIN` / `BORDERLINE` / `OUT` / `MISSING` / `N/A_NO_GI` — mismos criterios que parent.

---

## Aggregate verdict rules (locked)

| Call | Criterio |
|------|----------|
| **`EXT_CB2_GI_XL_12IY_12JA_SUPPORTED`** | 12IY y 12JA ambos con Gi mapeable y las 3 parejas `WITHIN` |
| **`EXT_CB2_GI_XL_12IY_12JA_PARTIAL`** | 12JA ALL_WITHIN (o WITHIN/BORDERLINE) y 12IY `N/A_NO_GI` u otro mapeo incompleto |
| **`EXT_CB2_GI_XL_12IY_12JA_TENSION`** | 12JA con mayoría OUT |
| **`EXT_CB2_GI_XL_12IY_12JA_INDETERMINATE`** | 12JA no mapeable |

12IZ appendix no override el veredicto primario.

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg (este) | `docs/synthesis/EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md` |
| Report | `results/network_core/ext_cb2_gi_xl_12iy_12ja.md` |
| Machine | `results/network_core/ext_cb2_gi_xl_12iy_12ja.json` |
| Helper | `scripts/network_core/ext_cb2_gi_xl_12iy_12ja.py` |

---

## Run

```text
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/ext_cb2_gi_xl_12iy_12ja.py
```

---

*Fin pre-registro. EXTERNAL discrimination-only.*

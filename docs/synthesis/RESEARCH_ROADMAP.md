# RESEARCH ROADMAP — contrato científico CB2 (P1–P6)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — contrato científico congelado post-P1; sin docking, sin de novo, sin P5 execution, sin MD nuevo  
**Autoridad de freeze / flags:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) (`RESEARCH_STATUS = POST_P1_BOUNDARY_FROZEN`)  
**Pre-registro técnico P1:** [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) · `P1_NULL` en [`scripts/network_core/dynamic_pipeline.py`](../../scripts/network_core/dynamic_pipeline.py)  
**P1 deliverable:** [`results/network_core/p1_dynamic_hub_validation.md`](../../results/network_core/p1_dynamic_hub_validation.md) (tip `31a881c`)  
**Self-test seco (andamiaje):** `python scripts/network_core/dynamic_pipeline.py --self-test` (tip técnico `b91b57c`)  
**Mapa multicapa (docs only):** [`CB2_DYNAMIC_INTERACTION_LAYERS.md`](CB2_DYNAMIC_INTERACTION_LAYERS.md)  
**Alias legado:** [`CB2_RESEARCH_ROADMAP.md`](CB2_RESEARCH_ROADMAP.md) → redirige aquí (evitar duplicación)

---

## Estado consolidado (freeze)

| Item | Status |
|------|--------|
| Phase G | **GENERALIZES** — macro coordinate OOS structural signal |
| HU-308 / HU-433 | **INDETERMINATE** — no universal static local mode |
| Static topology | **CORE_TOPOLOGICAL_ONLY** — clear aggregate hubs, no Gi enrichment |
| P1 dynamic | **NOT_SUPPORTED** — six hubs not persistent dynamic skeleton (GPCRmd/1540 WT) |
| P2 | **`READY_FOR_EXECUTION`** — dry frozen at `aaeec78`; **NOT executed**; gate = convergencia → A/B/C; Dutta 6 states do not condition analysis |
| P3 | **BLOCKED** — until landscape known |
| P4 | **BLOCKED** — until landscape known; comparable CB1 missing |
| P5 | **HYPOTHESIS_READY** — rutas dinámicas entre estados (0% vs 40% chol); **NO execution** |

### Regla de decisión (lock — anti-expansión)

**Do not run a question because it is interesting; run it when it produces clear discrimination between two (or more) plausible hypotheses.**

Postura anclada en `bb7b57a` (menos open search, más discriminating questions). Evita expansión infinita. Freeze intacto.

### Locks

```
POST_HOC_EXCUSES              = FORBIDDEN
DE_NOVO_GENERATION            = STOP
DOCKING                       = STOP
COMPUTATION                   = PAUSED
P5_EXECUTION                  = BLOCKED_PENDING_DECISION
SIX_HUBS_DYNAMIC_SKELETON     = REFUTED_UNDER_GPCRMD_WT
DECISION_RULE                 = DISCRIMINATION_ONLY
P2_OBJECT                     = OWN_MSM_GPCRMD_WT_THEN_ABC
P2                            = READY_FOR_EXECUTION  # dry frozen at aaeec78; NOT executed
DUTTA_SHUKLA                  = EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE  # 6 states do not condition analysis
```

---

## Objetivo (qué es / qué no es)

**Sí:** construir un **mapa causal de CB2** que sobreviva **falsificación sucesiva** (P1→P5). Cada puerta cierra o abre la siguiente. El resultado válido puede ser switch local, red distribuida, o arquitectura estado-dependiente.

**No:** encontrar una molécula. **P6 no existe** hasta que P1–P5 sobrevivan. P6 solo pregunta qué **perturbación química** mueve una red **ya mostrada** como controladora de salida funcional.

```
PRIMARY_OBJECTIVE = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
≠ “find the switch”
≠ “find a ligand”
```

---

## Árbol de decisión (contrato)

```
P1  ¿Los hubs sobreviven dinámicamente?
    │
    ├─ NO  → cerrar hipótesis de hubs (como núcleo dinámico)
    │         P2 = READY_FOR_EXECUTION (dry @ aaeec78; NOT executed)
    │
    └─ YES → (historical; not taken)
P2  Gate structure (locked):
    1. Own MSM converges?
       NO  → P2_INSUFFICIENT_SAMPLING → STOP
       YES → 2
    2. Architecture:
       A RED_ESTABLE | B RUTAS_POR_ESTADO | C DISTRIBUIDA
                        │
                        ├─ A RED_ESTABLE → red relativamente estable (cambia intensidad)
                        │
                        ├─ B RUTAS_POR_ESTADO → P3 (blocked until landscape known)
                        │         ¿Los cambios se relacionan con Gαi2?
                        │         │
                        │         ├─ NO  → arquitectura sin vínculo funcional demostrado
                        │         │
                        │         └─ YES → P4 (blocked until landscape known)
                        │                   ¿CB1 es distinto?
                        │                   │
                        │                   ├─ NO  → base débil de selectividad conformacional
                        │                   │
                        │                   └─ YES → P5 (independent membrane line)
                        │                             ¿La membrana modifica?
                        │                             │
                        │                             ├─ NO  → Nivel A suficiente
                        │                             │
                        │                             └─ YES → P6 (far)
                        │                                       ¿Puede una perturbación química desplazar?
                        │                                       (solo si P1–P5 sobrevivieron)
                        │
                        └─ C DISTRIBUIDA → altamente distribuida sin rutas dominantes
```

**Regla dura:** no saltar puertas; no abrir P6 compute (docking / de novo / diseño) mientras P1–P5 no estén resueltas en el sentido del árbol. **First real result to review = convergence**, not preferred biological story. **`DECISION_RULE = DISCRIMINATION_ONLY`**.

---

## Cuatro historias P1/P2 (mapa → contraste A/B/C)

Cualquiera es resultado científico válido. **No** se prefiere “persistent” a priori. En P2, estas historias se colapsan al **contraste de modelos A/B/C**:

| Historia (legado) | Modelo P2 | Lectura breve |
|-------------------|-----------|----------------|
| **Persistent** | **A RED_ESTABLE** | Red relativamente estable; cambios sobre todo de intensidad |
| **Persistent + plastic** | **A/B frontera** | Núcleo estable con plasticidad de rutas — discriminar vs A puro / B |
| **State-specific** | **B RUTAS_POR_ESTADO** | Rutas distintas dominan en estados distintos |
| **Highly distributed** | **C DISTRIBUIDA** | Sin rutas dominantes / null no concentra flujo |

Discriminación con protocolo dinámico + MSM (cuando se ejecute); **no** narrativa post hoc; **no** hub hunt. Dutta 6 states do not condition analysis.

---

## Gate P1 (único criterio de entrada al árbol)

Los hubs estáticos deben **vencer un null estructura-compatible pre-definido** y pasar **reproducibilidad** entre réplicas / estados.

| Elemento | Fuente canónica (no inventar otro null) |
|----------|------------------------------------------|
| Null | `P1_NULL` en `scripts/network_core/dynamic_pipeline.py` |
| Nombre | `exact_in_out_degree_multiset_match` |
| Métrica primaria | `pct_disconn` (cola superior) |
| α | `0.05` |
| Repro | Spearman rank hubs ≥ `0.7` entre réplicas/estados; si falla → `INDETERMINATE`, **no** retocar α |
| Protocolo | [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) |
| CLI | `dynamic_pipeline.py --self-test` · `run_dynamic_hub_persistence.py` (bloqueado sin traj) |

**Prohibido en P1:** `W = -ln(p)` universal; umbral a priori “>50% del flujo”; retuning de α / lista de hubs tras ver traj; llamar al resultado “switch”.

**Estado ahora:** **P1 COMPLETE** (`P1_NOT_SUPPORTED`) on GPCRmd/1540 WT only — artifacts `results/network_core/p1_dynamic_hub_validation.{json,md}`; CLI `scripts/network_core/p1_dynamic_hub_validation.py`. **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`**. **`P2 = READY_FOR_EXECUTION`** (dry frozen at `aaeec78`; **NOT executed**). **P3/P4 BLOCKED** until landscape known. **P5 = HYPOTHESIS_READY**, **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**. No auto-run MSM; no P5 compute.

---

## Puertas P1–P6 (una pregunta = una puerta)

### P1 — ¿Los hubs sobreviven dinámicamente?

**Pregunta:** ¿Los seis hubs del mapa estático son nodos dinámicos reales (persistencia **y** comunicación), o artefactos del grafo agregado?

**Si NO:** cerrar la hipótesis de que esos seis hubs forman un **esqueleto dinámico persistente** bajo las traj analizadas (no cierra causalidad biológica absoluta).  
**Si YES:** abrir P2.

**Contexto repo (ya cerrado en estático):** Test A bottleneck **SUPPORTED**; Test B PrefCoup Gαi2 **NOT_SUPPORTED** → `STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY` (`cfb2a51`). Eso **no** responde P1.

Hubs fijos a priori: ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46).

**Resultado P1 (2026-08-21, GPCRmd only):** **`P1_NOT_SUPPORTED`**. Channels A/B kept separate. Neither channel exceeded pre-registered null with reproducibility.  
**Lectura estricta:** P1 **no** refuta causalidad biológica de hubs en sentido absoluto. P1 **sí** refuta que esos seis hubs constituyan un **esqueleto dinámico persistente bajo GPCRmd/1540 WT**. **Prohibido:** post hoc “faltaba colesterol”; salto hubs-failed → red plenamente distribuida. Deja abiertas A–D (distributed / state-dependent / routes ≠ static LigACN / lipid-dependent routes). P1 does **not** answer Gi / CB1 / MSM / membrane / chemical switch. Hub hypothesis **CLOSED**; **`P2 = READY_FOR_EXECUTION`** (not executed).

### P2 — Own MSM (5 WT GPCRmd) → convergencia → A/B/C (no hub hunt) **`READY_FOR_EXECUTION`**

**Reformulación PI:** P2 construye un **MSM propio** sobre las **5 trayectorias WT GPCRmd Morales-Pastor** — **independiente** del MSM Dutta & Shukla. Dutta = **comparación externa posterior únicamente** (**6 states do not condition analysis**; K≠6 no es error automático).

Pre-registro: [`P2_STATE_ROUTE_PREGISTRATION.md`](P2_STATE_ROUTE_PREGISTRATION.md) · dry: `scripts/network_core/p2_dry_pipeline.py` (frozen at `aaeec78`).

**Gate structure (locked):**

```
1. Own MSM converges?  NO → P2_INSUFFICIENT_SAMPLING → STOP
                       YES → 2
2. Architecture: A RED_ESTABLE | B RUTAS_POR_ESTADO | C DISTRIBUIDA
```

**First real result to review = convergence**, not a preferred biological story.

| Modelo | Label | Claim |
|--------|--------|--------|
| **A** | **RED_ESTABLE** | Rutas dominantes **invariantes** (>80% overlap); cambia sobre todo **intensidad** |
| **B** | **RUTAS_POR_ESTADO** | **Rutas distintas** dominan por estado |
| **C** | **DISTRIBUIDA** | Comunicación **altamente distribuida** sin rutas dominantes |

| Lectura | Siguiente |
|---------|-----------|
| **A RED_ESTABLE** | P3 opcional / lit. |
| **B RUTAS_POR_ESTADO** | abrir P3 (cambios a interpretar funcionalmente) — blocked until landscape known |
| **C DISTRIBUIDA** | sin core prefabricado; no inventar hubs |
| `P2_INSUFFICIENT_SAMPLING` | pausa — **no** abrir P5 como sustituto |

**Estado ahora:** **`READY_FOR_EXECUTION`** — dry synthetic frozen at `aaeec78`; real MSM **NOT EXECUTED**. Ancla: `bb7b57a`.

### P3 — ¿Los cambios se relacionan con Gαi2? **BLOCKED** (until landscape known)
**Pregunta:** ¿Nodos/rutas dinámicas se enriquecen hacia lectura Gαi2 (y/o β-arr), sin afirmar switch?

**Si NO:** arquitectura física sin vínculo funcional demostrado (extiende Test B al régimen dinámico).  
**Si YES:** abrir P4.

`CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` hasta evidencia dinámica + revisión humana (nunca automática).

### P4 — ¿CB1 es distinto? **BLOCKED** (until landscape known; comparable CB1 missing)

**Pregunta:** ¿El control conformacional CB2 es específico de receptor o compartido con CB1?

**Si NO:** base débil de selectividad conformacional CB2-vs-CB1.  
**Si YES:** abrir P5.

`CB1_COMPARISON = BLOCKED` hasta desbloqueo explícito + datos.

### P5 — ¿La membrana modifica? **HYPOTHESIS_READY** (NO execution)

**Pregunta (independiente; no rescata P1):** ¿La composición lipídica cambia la distribución de estados conformacionales y la red de comunicación de CB2?

**Pregunta refinada (preferida):** ¿El colesterol cambia las **rutas dinámicas** que CB2 usa para transitar entre estados?  
(No meramente “¿cambia la actividad?” — eso ya tiene ancla lit.)

Design candidate (conceptual): **0% vs ~40% colesterol**. Ancla lit.: Yeliseev et al. (2021) MRI-2646, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6), PMID [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/).

**Si NO:** Nivel A suficiente.  
**Si YES:** abrir P6 (química en contexto de membrana).

Gobernanza: Nivel A = `ACTIVE_BASELINE`; Nivel B = `FUTURE_PRIORITY_HYPOTHESIS` (prep conceptual only); Nivel C archivado; heterómero A2A–CB2 = **Nivel-C-adjacent / futura** (DOI [10.1111/bph.16502](https://doi.org/10.1111/bph.16502); 2025 DOI [10.1016/j.bcp.2025.117280](https://doi.org/10.1016/j.bcp.2025.117280)) — **no** pipeline; **`P5 = HYPOTHESIS_READY`** · **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**. **`POST_HOC_EXCUSES = FORBIDDEN`** — no usar colesterol como excusa de P1.

### P6 — ¿Puede una perturbación química desplazar?

**Pregunta:** ¿Qué intervención química mueve la red / equilibrio hacia un estado funcional concreto **en un contexto ya caracterizado**?

**P6 no existe hasta que P1–P5 sobrevivan.**  
No es “mejor pose” ni campaña de docking/de novo. `DOCKING` / `DE_NOVO` = **STOP**.

---

## Linaje empírico → árbol (no circular)

```
Phase G (MACRO) 🟢 GENERALIZES
        │
        ▼
Phase H / micronetwork 🟡 INDETERMINATE  ──► alimenta P2
        │
        ▼
Static LigACN + 6 hubs 🟢 bottlenecks
        │
        ▼
Dual validation cfb2a51
  A 🟢 topological · B 🔴 PrefCoup
  → CORE_TOPOLOGICAL_ONLY ──► cierra “6 hubs = switch Gi”
        │
        ▼
P1     DONE → P1_NOT_SUPPORTED / SIX_HUBS_DYNAMIC_SKELETON=REFUTED_UNDER_GPCRMD_WT
       (hub hypothesis CLOSED; A–D still open as rival architectures)
P2     READY_FOR_EXECUTION (dry frozen at aaeec78; NOT executed)
       Gate1 convergencia → P2_INSUFFICIENT_SAMPLING | Gate2 A RED_ESTABLE / B RUTAS_POR_ESTADO / C DISTRIBUIDA
       Dutta 6 states do not condition analysis; first review = convergence
P3     BLOCKED until landscape known
P4     BLOCKED until landscape known (comparable CB1 missing)
P5     HYPOTHESIS_READY — independent membrane line (0% vs 40% chol; dynamic routes) — NO execution
P6     FAR (docking/de novo STOP)
```

Anclas: cfb2a51 · c2869b0 · 2a1193c · tip técnico pipeline seco `b91b57c` · P1 real `31a881c` / p1_dynamic_hub_validation · postura `bb7b57a` · P2 dry `aaeec78`.

---

## Conclusión PI (frontera epistemológica)

Proyecto congelado en una **frontera epistemológica**, **NO** porque el mecanismo esté resuelto.

**Sin overreach:** The simple model that a few static hubs constitute the CB2→Gi mechanism is **not supported** by the analyzed data. That does **not** mean CB2 is definitively a distributed network under all conditions — it means **that concrete explanation did not survive the dynamic test**.

**Rigurosa:** NOT “A switch does not exist.” YES: “There is still insufficient evidence to reduce CB2 functional control to a unique switch or to a small persistent static skeleton.”

**Regla de decisión (lock):** no correr preguntas por ser interesantes; solo si **discriminan** entre ≥2 hipótesis plausibles.

**Gates:** **`P2 = READY_FOR_EXECUTION`** (dry @ `aaeec78`; **NOT executed**) = own MSM → convergencia → A/B/C (Dutta external only); P3/P4 blocked until landscape known; P5 membrane/cholesterol independent (not P1 rescue); P6 far. **Cortafuegos:** no modelar todas las capas a la vez. Al ejecutar: no reinterpretar Phase G / HU INDETERMINATE / CORE_TOPOLOGICAL_ONLY / P1_NOT_SUPPORTED. **First result to review = convergence.** **Postura (`bb7b57a`):** fenómeno no resuelto → experimento mínimo discriminante.

---

## Índice cruzado

| Documento | Rol |
|-----------|-----|
| [RESEARCH_STATE.md](../../RESEARCH_STATE.md) | Flags / freeze (POST_P1_BOUNDARY_FROZEN; P2 READY_FOR_EXECUTION) |
| [CB2_DYNAMIC_INTERACTION_LAYERS.md](CB2_DYNAMIC_INTERACTION_LAYERS.md) | Mapa multicapa + giro a transiciones |
| [DYNAMIC_REANALYSIS_PROTOCOL.md](DYNAMIC_REANALYSIS_PROTOCOL.md) | Pre-registro P1–P3 + P1_NULL |
| [P2_STATE_ROUTE_PREGISTRATION.md](P2_STATE_ROUTE_PREGISTRATION.md) | P2 own MSM GPCRmd + gate convergencia → A/B/C |
| [CB2_ALLOSTERIC_NETWORK.md](CB2_ALLOSTERIC_NETWORK.md) | Morales-Pastor, Dutta–Shukla (lit.), Trp258 |
| [HU308_HU433_PARADOX.md](HU308_HU433_PARADOX.md) | Smoum / Ganzoni; microestados |
| [DOCKING_LIMITS_AND_GOVERNANCE.md](DOCKING_LIMITS_AND_GOVERNANCE.md) | Por qué P6 ≠ docking score |
| Dual validation report | Ancla cfb2a51 — entrada estática a P1/P3 |
| [results/network_core/p1_dynamic_hub_validation.md](../../results/network_core/p1_dynamic_hub_validation.md) | **P1 verdict** (GPCRmd only) |

---

## Próximo paso

1. **`P2 = READY_FOR_EXECUTION`** — dry frozen at `aaeec78`; **real MSM NOT EXECUTED** this docs-only turn.  
2. When executed: own MSM on 5 WT GPCRmd → Gate1 convergencia → Gate2 A RED_ESTABLE / B RUTAS_POR_ESTADO / C DISTRIBUIDA; Dutta ≠ template. P3/P4 still gated on landscape. **`DECISION_RULE = DISCRIMINATION_ONLY`**.  
3. **P5** stays **HYPOTHESIS_READY** (independent membrane line) — **P5_EXECUTION = BLOCKED_PENDING_DECISION**; not a substitute for failed Gate1.  
4. **No** docking / de novo / MD nuevo / hub hunt / post-hoc cholesterol excuse.

---

*Fin RESEARCH_ROADMAP.md — P2 = READY_FOR_EXECUTION (dry @ aaeec78; NOT executed); convergencia antes de A/B/C; Dutta 6 states do not condition analysis.*

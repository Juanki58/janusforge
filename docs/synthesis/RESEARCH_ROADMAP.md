# RESEARCH ROADMAP — contrato científico CB2 (P1–P6)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — acta de cierre P2 + congelación profunda; **`REPOSITORY = SEALED`**; sin compute, sin redes A/B/C, sin docking, sin de novo, sin P5 execution, sin MD/MSM nuevo  
**Autoridad de freeze / flags:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) (`RESEARCH_STATUS = DEEP_PAUSE_SEALED`)  
**P2 evidence:** [`results/msm_model/p2_msm_convergence_report.md`](../../results/msm_model/p2_msm_convergence_report.md) · [`implied_timescales.png`](../../results/msm_model/implied_timescales.png) · commit **`2dcff23`** / `p2_msm_builder.py`  
**Pre-registro técnico P1:** [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) · `P1_NULL` en [`scripts/network_core/dynamic_pipeline.py`](../../scripts/network_core/dynamic_pipeline.py)  
**P1 deliverable:** [`results/network_core/p1_dynamic_hub_validation.md`](../../results/network_core/p1_dynamic_hub_validation.md) (tip `31a881c`)  
**Self-test seco (andamiaje):** `python scripts/network_core/dynamic_pipeline.py --self-test` (tip técnico `b91b57c`)  
**Mapa multicapa (docs only):** [`CB2_DYNAMIC_INTERACTION_LAYERS.md`](CB2_DYNAMIC_INTERACTION_LAYERS.md)  
**Alias legado:** [`CB2_RESEARCH_ROADMAP.md`](CB2_RESEARCH_ROADMAP.md) → redirige aquí (evitar duplicación)

---

## ACTA DE CIERRE EXPERIMENTAL: COMPUERTA P2 (FASE 1)

**Verdict:** **`INSUFFICIENT_SAMPLING`**.  
**Physical justification:** Five WT trajs + 1995 aggregated frames lack statistical evidence for a convergent MSM; without that validation, reliable separation of the underlying metastable landscape is impossible.  
**Epistemology:** Do not claim transitions are non-Markovian as biological absolute; do not claim we know distributed vs stable vs state-dependent. Honest “we do not know” is the valuable result. Gates prevented fabricating a biological story on a sampling artifact.

### Definitive YAML freeze (21 Aug 2026)

```yaml
P1_STATIC_HUBS           : CLOSED (NOT_SUPPORTED)
P2_MSM_TRANSITIONS       : CLOSED (INSUFFICIENT_SAMPLING)
P2_NETWORK_A_B_C         : ABORTED
P3_GALPHA_I2             : BLOCKED
P4_CB1_COMPARISON        : BLOCKED
P5_MEMBRANE              : HYPOTHESIS_READY  # independent; NOT substitute for P2
P6_CHEMICAL_PERTURBATION : BLOCKED
DE_NOVO_GENERATION       : STOP
DOCKING                  : STOP
COMPUTATION              : PAUSED
POST_HOC_EXCUSES         : FORBIDDEN
DEEP_PAUSE               : TRUE
REPOSITORY               : SEALED
```

**Next conversation = strategic resource allocation only:** massive adaptive sampling for P2 **OR** redesign independent membrane (P5) in silico — **NOT** “what script today?”

---

## Estado consolidado (freeze post-P2 — SEALED)

| Item | Status |
|------|--------|
| Phase G | **GENERALIZES** — macro coordinate OOS structural signal |
| HU-308 / HU-433 | **INDETERMINATE** — no universal static local mode |
| Static topology | **CORE_TOPOLOGICAL_ONLY** — clear aggregate hubs, no Gi enrichment |
| P1 dynamic | **CLOSED (NOT_SUPPORTED)** — six hubs not persistent dynamic skeleton (GPCRmd/1540 WT) |
| P2 MSM transitions | **CLOSED (INSUFFICIENT_SAMPLING)** — @ `2dcff23`; ITS NON_CONVERGENT |
| P2 network A/B/C | **ABORTED** — no convergent MSM → no A/B/C |
| P3 | **BLOCKED** |
| P4 | **BLOCKED** |
| P5 | **HYPOTHESIS_READY** — independent; **NOT** substitute for P2; **NO execution** |
| P6 | **BLOCKED** |
| Repository | **SEALED** · **`DEEP_PAUSE = TRUE`** |

### Regla de decisión (lock — anti-expansión)

**Do not run a question because it is interesting; run it when it produces clear discrimination between two (or more) plausible hypotheses.**

Postura anclada en `bb7b57a`. Evita expansión infinita. **`DEEP_PAUSE = TRUE`** · **`REPOSITORY = SEALED`**.

### Locks

```
POST_HOC_EXCUSES              = FORBIDDEN
DE_NOVO_GENERATION            = STOP
DOCKING                       = STOP
COMPUTATION                   = PAUSED
DEEP_PAUSE                    = TRUE
REPOSITORY                    = SEALED
P5_EXECUTION                  = BLOCKED_PENDING_DECISION
SIX_HUBS_DYNAMIC_SKELETON     = REFUTED_UNDER_GPCRMD_WT
DECISION_RULE                 = DISCRIMINATION_ONLY
P2_MSM_TRANSITIONS            = CLOSED (INSUFFICIENT_SAMPLING)
P2_NETWORK_A_B_C              = ABORTED
DUTTA_SHUKLA                  = EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE
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
    ├─ NO  → cerrar hipótesis de hubs (como núcleo dinámico)  ✓ taken
    │
    └─ YES → (historical; not taken)
P2  Gate structure (executed @ 2dcff23):
    1. Own MSM converges?
       NO  → P2_INSUFFICIENT_SAMPLING → STOP  ✓ taken
       YES → 2
    2. Architecture A/B/C → ABORTED (no convergent MSM; NOT DECIDED)
P3–P6  BLOCKED / P5 HYPOTHESIS_READY only (independent; not P2 substitute)
```

**Regla dura:** no saltar puertas; no fabricar biología sobre artefacto de sampling. Gates worked. **`DECISION_RULE = DISCRIMINATION_ONLY`**. **Next = strategic resource allocation only.**

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

**Estado ahora:** **P1 COMPLETE** (`P1_NOT_SUPPORTED`) on GPCRmd/1540 WT only. **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`**. **`P2_MSM_TRANSITIONS = CLOSED (INSUFFICIENT_SAMPLING)`** @ `2dcff23`. **`P2_NETWORK_A_B_C = ABORTED`**. **P3/P4/P6 BLOCKED**. **P5 = HYPOTHESIS_READY**, **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**. **`DEEP_PAUSE = TRUE`** · **`REPOSITORY = SEALED`**. No compute.

---

## Puertas P1–P6 (una pregunta = una puerta)

### P1 — ¿Los hubs sobreviven dinámicamente?

**Pregunta:** ¿Los seis hubs del mapa estático son nodos dinámicos reales (persistencia **y** comunicación), o artefactos del grafo agregado?

**Si NO:** cerrar la hipótesis de que esos seis hubs forman un **esqueleto dinámico persistente** bajo las traj analizadas (no cierra causalidad biológica absoluta).  
**Si YES:** abrir P2.

**Contexto repo (ya cerrado en estático):** Test A bottleneck **SUPPORTED**; Test B PrefCoup Gαi2 **NOT_SUPPORTED** → `STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY` (`cfb2a51`). Eso **no** responde P1.

Hubs fijos a priori: ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46).

**Resultado P1 (2026-08-21, GPCRmd only):** **`P1_NOT_SUPPORTED`**. Channels A/B kept separate. Neither channel exceeded pre-registered null with reproducibility.  
**Lectura estricta:** P1 **no** refuta causalidad biológica de hubs en sentido absoluto. P1 **sí** refuta que esos seis hubs constituyan un **esqueleto dinámico persistente bajo GPCRmd/1540 WT**. **Prohibido:** post hoc “faltaba colesterol”; salto hubs-failed → red plenamente distribuida. Deja abiertas A–D (distributed / state-dependent / routes ≠ static LigACN / lipid-dependent routes). Hub hypothesis **CLOSED**.

### P2 — Own MSM (5 WT GPCRmd) → convergencia → A/B/C **`CLOSED (INSUFFICIENT_SAMPLING)`**

**Reformulación PI:** P2 construyó un **MSM propio** sobre las **5 trayectorias WT GPCRmd Morales-Pastor** — **independiente** del MSM Dutta & Shukla. Dutta = **comparación externa posterior únicamente**.

Pre-registro: [`P2_STATE_ROUTE_PREGISTRATION.md`](P2_STATE_ROUTE_PREGISTRATION.md) · dry: `scripts/network_core/p2_dry_pipeline.py` (frozen at `aaeec78`) · MSM: `scripts/network_core/p2_msm_builder.py` @ **`2dcff23`**.

**Gate 1 result (2026-08-21):** ITS **`NON_CONVERGENT`**. Five trajs + **1995** aggregated frames do **not** provide enough evidence for a convergent MSM that would allow A/B/C network analysis between states → **`P2_INSUFFICIENT_SAMPLING`** → **STOP**. **`P2_NETWORK_A_B_C = ABORTED`**.

**Epistemology locks:** Do **not** claim non-convergent ITS proves transitions are non-Markovian as biological absolute. Do **not** claim the 2 macrostates are “almost certainly noise.” Do **not** decide among A/B/C — architecture **NOT DECIDED**. Honest we-do-not-know. Gates worked.

| Modelo | Label | Status |
|--------|--------|--------|
| **A** | **RED_ESTABLE** | **NOT DECIDED** (aborted) |
| **B** | **RUTAS_POR_ESTADO** | **NOT DECIDED** (aborted) |
| **C** | **DISTRIBUIDA** | **NOT DECIDED** (aborted) |
| `P2_INSUFFICIENT_SAMPLING` | Gate 1 stop | **TAKEN** — **no** abrir P5 como sustituto |

**Evidence:** [`p2_msm_convergence_report.md`](../../results/msm_model/p2_msm_convergence_report.md) · [`implied_timescales.png`](../../results/msm_model/implied_timescales.png) · commit **`2dcff23`**.

### P3 — ¿Los cambios se relacionan con Gαi2? **BLOCKED**

### P4 — ¿CB1 es distinto? **BLOCKED**

### P5 — ¿La membrana modifica? **HYPOTHESIS_READY** (NO execution; independent; **NOT** substitute for P2)

**Pregunta (independiente; no rescata P1/P2):** ¿La composición lipídica cambia la distribución de estados conformacionales y la red de comunicación de CB2?

**Pregunta refinada (preferida):** ¿El colesterol cambia las **rutas dinámicas** que CB2 usa para transitar entre estados?

Design candidate (conceptual): **0% vs ~40% colesterol**. Ancla lit.: Yeliseev et al. (2021) MRI-2646, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6).

Gobernanza: **`P5 = HYPOTHESIS_READY`** · **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**. **`POST_HOC_EXCUSES = FORBIDDEN`**.

### P6 — ¿Puede una perturbación química desplazar? **BLOCKED**

**P6 no existe hasta que P1–P5 sobrevivan.** `DOCKING` / `DE_NOVO` = **STOP**.

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
P2     CLOSED (INSUFFICIENT_SAMPLING) @ 2dcff23 — A/B/C ABORTED; architecture NOT DECIDED
P3     BLOCKED
P4     BLOCKED
P5     HYPOTHESIS_READY — independent membrane line — NO execution; NOT substitute for P2
P6     BLOCKED (docking/de novo STOP)
REPOSITORY SEALED · DEEP_PAUSE = TRUE · COMPUTATION = PAUSED
```

Anclas: cfb2a51 · c2869b0 · 2a1193c · tip técnico pipeline seco `b91b57c` · P1 real `31a881c` · postura `bb7b57a` · P2 dry `aaeec78` · **P2 MSM `2dcff23`**.

---

## Conclusión PI (frontera epistemológica)

Proyecto en **`DEEP_PAUSE` / `REPOSITORY = SEALED`**, **NO** porque el mecanismo esté resuelto.

**Sin overreach:** The simple model that a few static hubs constitute the CB2→Gi mechanism is **not supported**. Five trajs + 1995 frames do **not** support a convergent MSM for A/B/C. That does **not** mean CB2 is definitively a distributed network — architecture A/B/C remains **NOT DECIDED**. Honest we-do-not-know.

**Gates:** P1 CLOSED (NOT_SUPPORTED); **P2 CLOSED (INSUFFICIENT_SAMPLING)** · A/B/C **ABORTED**; P3/P4/P6 BLOCKED; P5 HYPOTHESIS_READY (independent; not substitute). **Next = strategic resource allocation only** (sampling for P2 OR independent P5) — not “what script today?”

---

## Índice cruzado

| Documento | Rol |
|-----------|-----|
| [RESEARCH_STATE.md](../../RESEARCH_STATE.md) | Flags / freeze (`DEEP_PAUSE_SEALED`; acta P2) |
| [p2_msm_convergence_report.md](../../results/msm_model/p2_msm_convergence_report.md) | **P2 Gate 1 evidence** (`2dcff23`) |
| [implied_timescales.png](../../results/msm_model/implied_timescales.png) | ITS NON_CONVERGENT plot |
| [CB2_DYNAMIC_INTERACTION_LAYERS.md](CB2_DYNAMIC_INTERACTION_LAYERS.md) | Mapa multicapa + giro a transiciones |
| [DYNAMIC_REANALYSIS_PROTOCOL.md](DYNAMIC_REANALYSIS_PROTOCOL.md) | Pre-registro P1–P3 + P1_NULL |
| [P2_STATE_ROUTE_PREGISTRATION.md](P2_STATE_ROUTE_PREGISTRATION.md) | P2 own MSM GPCRmd + gate convergencia → A/B/C |
| [CB2_ALLOSTERIC_NETWORK.md](CB2_ALLOSTERIC_NETWORK.md) | Morales-Pastor, Dutta–Shukla (lit.), Trp258 |
| [HU308_HU433_PARADOX.md](HU308_HU433_PARADOX.md) | Smoum / Ganzoni; microestados |
| [DOCKING_LIMITS_AND_GOVERNANCE.md](DOCKING_LIMITS_AND_GOVERNANCE.md) | Por qué P6 ≠ docking score |
| Dual validation report | Ancla cfb2a51 — entrada estática a P1/P3 |
| [p1_dynamic_hub_validation.md](../../results/network_core/p1_dynamic_hub_validation.md) | **P1 verdict** (GPCRmd only) |

---

## Próximo paso

1. **`REPOSITORY = SEALED`** · **`DEEP_PAUSE = TRUE`** · **`COMPUTATION = PAUSED`** — no compute this turn.  
2. **P2 closed:** `INSUFFICIENT_SAMPLING` @ `2dcff23`; A/B/C **ABORTED**; architecture **NOT DECIDED**.  
3. **Human decision only:** invest in sampling required by P2 **OR** open independent membrane (P5) redesign — **NOT** “what script today?”  
4. **P5** stays **HYPOTHESIS_READY** — not a substitute for failed Gate 1.  
5. **No** docking / de novo / MD nuevo / hub hunt / network A/B/C / post-hoc excuses.

---

*Fin RESEARCH_ROADMAP.md — ACTA P2: CLOSED (INSUFFICIENT_SAMPLING) @ 2dcff23; A/B/C ABORTED; DEEP_PAUSE SEALED; next = strategic resource allocation only.*

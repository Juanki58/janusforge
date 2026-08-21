# RESEARCH STATE — Janusforge CB₂ (frontera post-P1 congelada)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — consolidación / freeze; **no** P5 execution, **no** docking, **no** de novo, **no** MD nuevo, **no** análisis nuevo  
**Objetivo primario:** **caracterizar el mecanismo de control conformacional de CB2** (switch local, red distribuida, o arquitectura estado-dependiente — cualquiera es resultado válido). **No** es objetivo principal “encontrar el switch.”  
**Anclas de linaje (preservar):** `cfb2a51` (dual-test limpio → topología-only) · `c2869b0` (jerarquía ambiental A/B/C + `Q_membrana` parked) · `2a1193c` (reposo científico / frontera) · `31a881c` (P1 GPCRmd)  
**Roadmap P1–P6 (contrato científico):** [`docs/synthesis/RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md) · alias [`docs/synthesis/CB2_RESEARCH_ROADMAP.md`](docs/synthesis/CB2_RESEARCH_ROADMAP.md)  
**P1 deliverable:** [`results/network_core/p1_dynamic_hub_validation.md`](results/network_core/p1_dynamic_hub_validation.md)  
**Pipeline seco / self-test:** `python scripts/network_core/dynamic_pipeline.py --self-test` (andamiaje `b91b57c`; no sustituye traj)  
**Bitácora extendida:** [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md)  
**Puntero síntesis:** [`docs/cb2_mechanistic_frontier_synthesis.md`](docs/cb2_mechanistic_frontier_synthesis.md) (este archivo es la autoridad de freeze / flags)

---

## Estado consolidado (freeze post-P1)

| Item | Status |
|------|--------|
| Phase G | **GENERALIZES** — macro coordinate OOS structural signal |
| HU-308 / HU-433 | **INDETERMINATE** — no universal static local mode |
| Static topology | **CORE_TOPOLOGICAL_ONLY** — clear aggregate hubs, no Gi enrichment |
| P1 dynamic | **NOT_SUPPORTED** — six hubs **not** a persistent dynamic skeleton under analyzed traj (GPCRmd/1540 WT) |
| P2 | **BLOCKED** — Dutta/Shukla MSM missing |
| P3 | **BLOCKED** |
| P4 | **BLOCKED** — comparable CB1 missing |
| P5 | **HYPOTHESIS_READY** — 0% vs 40% cholesterol design candidate; **NO execution** |

### Lectura estricta de P1 (lenguaje obligatorio)

P1 **no** refuta causalidad biológica de hubs en sentido absoluto.  
P1 **sí** refuta la hipótesis concreta de que esos **seis hubs** constituyen un **esqueleto dinámico persistente bajo las trayectorias analizadas** (GPCRmd/1540 WT).

**Prohibido:** “P1 falló porque faltaba colesterol” (post hoc).  
**Prohibido saltar:** hubs fallaron → la red es plenamente distribuida.  
**Estricto:** los seis hubs estáticos **no** forman una subred dinámica persistente detectable bajo este análisis. Quedan abiertas A–D: (A) distribuida / (B) estado-dependiente / (C) rutas ≠ static LigACN / (D) rutas lipídico-dependientes.

**P5 (independiente; no rescata P1):** ¿La composición lipídica cambia la distribución de estados conformacionales y la red de comunicación de CB2?  
**Pregunta refinada (preferida):** ¿El colesterol cambia las **rutas dinámicas** que CB2 usa para transitar entre estados? (no meramente “¿cambia la actividad?” — eso ya tiene ancla lit.)  
Nivel B = **future priority hypothesis**, prep conceptual only. Ancla lit.: Yeliseev et al. (2021) MRI-2646, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6). **`P5_EXECUTION = BLOCKED_PENDING_DECISION`.**

**Mapa multicapa (docs only):** [`docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md`](docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md) — capas ligando↔microswitch↔hélices↔red↔efector↔membrana↔heterómero↔iones/agua↔tiempo; **no** modelar todas a la vez.

**Giro de objeto P2 (evolución conceptual — no ejecución):** tras P1, el objeto pasa de **hubs permanentes** a **transiciones** — “¿qué conexiones aparecen, desaparecen o cambian de fuerza al pasar entre estados?” `P2` sigue **BLOCKED** (MSM).

---

## Cierre PI — frontera epistemológica (framing obligatorio)

El proyecto está congelado en una **frontera epistemológica**, **NO** porque el mecanismo esté resuelto.

**Claim importante sin overreach:**  
“The simple model that a few static hubs constitute the CB2→Gi mechanism is **not supported** by the analyzed data.”  
Eso **no** significa que CB2 sea definitivamente una red distribuida bajo todas las condiciones — significa que **esa explicación concreta no sobrevivió el test dinámico**.

**Conclusión final (rigurosa):**  
- **NOT:** “A switch does not exist.”  
- **YES:** “There is still insufficient evidence to reduce CB2 functional control to a unique switch or to a small persistent static skeleton.”

**Future gates (delimitados — sin reinterpretar cierres previos):**

| Gate | Estado | Requisito / lectura |
|------|--------|---------------------|
| P2 microstates / **transitions** | **BLOCKED** | needs missing MSM (Dutta/Shukla); objeto = rutas entre estados (no core permanente) |
| P3 Gi link | **BLOCKED** | gated on P2 |
| P4 CB1 | **BLOCKED** | needs comparable set |
| P5 membrane/cholesterol | **HYPOTHESIS_READY** | independent; **not** rescue of P1; pregunta refinada = rutas dinámicas entre estados; no execution |
| P6 chemical perturbation | **NOT OPEN** | only after earlier gates yield a solid enough mechanism |

**Al reabrir:** se sabe exactamente qué pregunta contestar y qué resultados **no** deben reinterpretarse (Phase G GENERALIZES; HU-308/433 INDETERMINATE; static `CORE_TOPOLOGICAL_ONLY`; P1 `NOT_SUPPORTED` / `SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`).

---

## Hipótesis de trabajo (redacción exacta — no modelo final)

**Objetivo primario (desplazamiento):** caracterizar el **mecanismo de control conformacional** de CB2. Si resulta un switch, bien; si resulta una red distribuida, también bien. Dejar de buscar “el switch” como meta principal.

Working hypothesis (framing): CB2 activity appears to emerge from the interaction among ligand, conformational landscape, and membrane environment, but the **quantitative contribution of each component is not yet resolved**.

**Prohibido afirmar:** que el “modelo final” **demuestra** un sistema tripartito definitivo, o que se **resolvió** la termodinámica de CB2. Ligando / paisaje / membrana son ejes de una **hipótesis multivariable**, no un veredicto cuantitativo cerrado.

**TRIPARTITE** = **working hypothesis / framing only** — **NOT** a demonstrated final model; quantitative weights still unresolved (lenguaje preservado desde `2a1193c`).

**No es búsqueda circular:** el siguiente paso informativo está ordenado en P1–P6 ([`RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md)). El cómputo de trayectorias permanece bloqueado por datos, no por falta de pregunta. Andamiaje técnico: self-test del pipeline seco (`dynamic_pipeline.py --self-test`, tip `b91b57c`).

---

## Mapa de convergencia comunitaria (consolidado — 4 bloques)

**Alcance:** registro de **convergencia internacional de preguntas** en la literatura CB2 — **no** colaboraciones del proyecto. Grupos nombrados (Selent / IMIM–UPF, Bouvier, Veprintsev, Sykes, y afines) = **contexto de campo** etiquetado **[SUPPORTED_INTERPRETATION]** (“el campo trabaja preguntas emparentadas”) o **[HIPÓTESIS_ABIERTA]** cuando el vínculo mecánico al repo no está cerrado. Claims científicos abajo citan solo papers ya en repo con DOI.

### 1. Redes alostéricas y sesgo funcional

**[LITERATURA_PRIMARIA]** Morales-Pastor et al. (2025): ~360 mutantes, MD, acoplamiento Gαi2 / β-arr1; LigACN **distribuida** (muchos puntos de entrada, no un switch único). DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/). Coherente con el cierre propio **`STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY`** (Test B negativo ≠ “la red no existe”).

### 2. Complejo cuaternario y acoplamiento

**Tema de literatura (IDs primarios pendientes si no están en repo):** interfaz TM3 / TM5 / TM6–Gαi; apertura coordinada con TM5 intracelular. **[HIPÓTESIS_ABIERTA]** / tema a anclar con DOI primario — **no** inventar citas de “crosslinking de complejo cuaternario” sin ID verificado en `RESEARCH_STATE` / síntesis. Paisaje multi-estado CB1/CB2 ya anclado: **[LITERATURA_PRIMARIA]** Dutta & Shukla (2023), DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

### 3. Biofísica de membrana / liposomas reconstituidos

**[LITERATURA_PRIMARIA]** Estabilización por PS / lípidos aniónicos y pliegue funcional en sistemas reconstituidos — Kimura et al. (2012), DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425); Vukoti et al. (2012), DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290). **[HIPÓTESIS_ABIERTA]** Acoplamiento electrostático con H8 (p.ej. Arg302^8.46 como hub estático del repo) — plausible como tema de campo; **no** demostrado por Test B ni por `Q_membrana` (parked).

### 4. Colesterol y vía lipídica

**[LITERATURA_PRIMARIA]** Colesterol / MRI-2646: modulación de equilibrio basal y clase de eficacia — Yeliseev et al. (2021), DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6). **Tema de literatura (ID primario pendiente si no verificado aquí):** entrada lateral de ligando lipídico por corredor TM6–TM7. Encaja Nivel B (`MEMBRANE_MILIEU = FUTURE_HYPOTHESIS`); **no** en pipeline.

### Significado para el repositorio

| Lectura | Estado |
|---------|--------|
| Fin de búsqueda ciega (de novo / filtros empíricos de docking) | **`DOCKING_CAMPAIGNS` / `DE_NOVO_GENERATION` / `OPEN_ENDED_SEARCHES` = STOP** |
| Interpretación `CORE_TOPOLOGICAL_ONLY` | Autopista estática TM7–H8 / base TM2 = **flujo mecánico basal candidato**; selección fina de vía requiere dinámica temporal + acoplamiento de membrana — **[SUPPORTED_INTERPRETATION]**, **no** demostrado por Test B |
| Economía de recursos | Entrada futura = **reanálisis de datos públicos** (no campaña ciega nueva) |
| Proveniencia | **`DATA_PROVENANCE_AUDIT: PARTIAL` — GPCRmd/1540 WT traj recovered locally; Dutta–Shukla Box MSM still HTTP 404** (`RECOVERY_ATTEMPT=DONE`; Sink T from Methods; MOESM2 recovered) |

---

## Flags de freeze (exactos — autoridad)

```
RESEARCH_STATUS                 = POST_P1_BOUNDARY_FROZEN
DYNAMIC_REANALYSIS              = P1_DONE_FROZEN
P1_VERDICT                      = P1_NOT_SUPPORTED
SIX_HUBS_DYNAMIC_SKELETON       = REFUTED_UNDER_GPCRMD_WT
P2                              = BLOCKED
P3                              = BLOCKED
P4                              = BLOCKED
P5                              = HYPOTHESIS_READY
P5_EXECUTION                    = BLOCKED_PENDING_DECISION
POST_HOC_EXCUSES                = FORBIDDEN
DE_NOVO_GENERATION              = STOP
DOCKING                         = STOP
DOCKING_EXECUTION               = STOP
COMPUTATION_ACTIVE              = NONE
COMPUTATION                     = PAUSED
ORTHOSTERIC_DESIGN              = PAUSED
MACRO_COORDINATE                = VALIDATED_OUT_OF_SAMPLE
FUNCTIONAL_EFFICACY             = INDETERMINATE
HU308_HU433_MICROSTATE          = INDETERMINATE
STATIC_LIGACN                   = CORE_TOPOLOGICAL_ONLY
MEMBRANE_MILIEU                 = FUTURE_HYPOTHESIS
NEW_PHASE                       = DO_NOT_OPEN
LINE_PAUSE                      = TRUE
PRIMARY_OBJECTIVE               = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
```

**Locks duros (post-P1):**

```
POST_HOC_EXCUSES              = FORBIDDEN
DE_NOVO_GENERATION            = STOP
DOCKING                       = STOP
COMPUTATION                   = PAUSED
P5_EXECUTION                  = BLOCKED_PENDING_DECISION
SIX_HUBS_DYNAMIC_SKELETON     = REFUTED_UNDER_GPCRMD_WT
```

**Aliases / legado (compatibilidad con cierres previos):** `ORTOSTERIC_THCV_DESIGN = PAUSED` · `CORE_TOPOLOGICAL_ONLY = CLOSED` · `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` · `ROADMAP_ACTIVE_PREP` (prep pre-P1) · `FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY` (legado `2a1193c`) · `P1_DONE_AWAITING_JOINT_REVIEW` (superseded by `P1_DONE_FROZEN`).

Preservados sin reabrir: **`STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY`**, locks **docking / de novo**, **Niveles A/B/C**, **P5 = HYPOTHESIS_READY / no execution**, pregunta de reactivación `ligand+receptor+membrane → P(metastable states)` archivada, linaje **`cfb2a51` / `c2869b0` / `2a1193c` / `31a881c`**.

**Lectura de estado:** **P1 ejecutado** (GPCRmd/1540 WT only) → **`P1_NOT_SUPPORTED`** / **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`** — ver `results/network_core/p1_dynamic_hub_validation.md`. **No** implica causalidad biológica absoluta falsa; **no** implica red plenamente distribuida. **P2–P4 BLOCKED** (MSM / CB1). **P5 HYPOTHESIS_READY**, execution blocked. Sin auto-P2 / sin P5 compute.

---

## Trayectoria registrada

```
THCV / orthosteric
  → Contract v1.0 too restrictive
  → conformational landscape
  → Phase G GENERALIZES (macro OOS)
  → microstates HU-308 / HU-433
  → Phase H INDETERMINATE
  → static LigACN
  → CORE_TOPOLOGICAL_ONLY
  → literature + membrane
  → multivariable system hypothesis
     (ligand × landscape × membrane; weights unresolved)
```

---

## Explicitamente NO demostrado

| Afirmación | Estado |
|------------|--------|
| Unique “switch” | **NO** |
| Static hubs control Gαi2 | **NO** (`FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED`) |
| `CB2_Gi_NETWORK_CANDIDATE` exists | **NO** (`NOT_ESTABLISHED`) |
| TPSA ≡ pharmacological periphery | **NO** |
| Lipid milieu alone explains functional variability | **NO** |
| Usable chemical strategy already in hand | **NO** |

---

## Lectura final PI (narrativa registrada)

1. **Origen.** Se buscó una molécula “switch” ortostérica CB1/CB2; el contrato geométrico resultó demasiado restrictivo → **`ORTHOSTERIC_DESIGN = PAUSED`**.
2. **Generalización.** CB2 es **multi-estado**. **[LITERATURA_PRIMARIA]** Dutta & Shukla (2023) documentan paisajes conformacionales distintos CB1/CB2 (DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)). **[OBSERVACIÓN_PROPIA]** Phase G: coordenada macro distingue activo vs inactivo OOS → **`MACRO_COORDINATE = VALIDATED_OUT_OF_SAMPLE`**.
3. **Límite.** Macroconformación sola ≠ función fina (**`FUNCTIONAL_EFFICACY = INDETERMINATE`**). Coherente con **[LITERATURA_PRIMARIA]** Morales-Pastor et al. (2025): red alostérica **distribuida**, muchos puntos de entrada — no un switch único (DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/)).
4. **Corrección Trp258.** **[LITERATURA_PRIMARIA]** Puede ser nodo de control potente (Ganzoni 2026: continuo funcional vía HU-308 / Trp258^6.48; DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B); ensayo-dependiente), **pero no necesariamente único** — nodo local como entrada a una red mayor. El paradoxo **HU-308 / HU-433** permanece fundamental (**[LITERATURA_PRIMARIA]** Smoum 2015, DOI [10.1073/pnas.1503395112](https://doi.org/10.1073/pnas.1503395112)) → **`HU308_HU433_MICROSTATE = INDETERMINATE`**.
5. **Seis hubs.** **`STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY`**. **[INTERNAL_REANALYSIS]** Knockout rompe la red estática; **sin** enriquecimiento PrefCoup_Gαi2 → no es núcleo funcional. Encaja transmisión **distribuida / estado-dependiente**.
6. **Membrana no es distracción inventada** — y tampoco está resuelta. **[LITERATURA_PRIMARIA]** Colesterol puede elevar actividad constitutiva y cambiar clase de ligando (MRI-2646 — Yeliseev 2021, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6), PMID [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/)); fosfolípidos aniónicos (p.ej. PS) estabilizan CB2 funcional (Kimura 2012 DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425); Vukoti 2012 DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290)). Temperatura afecta estabilidad ≠ regulador farmacológico fisiológico central → **jerarquía A/B/C**. **`MEMBRANE_MILIEU = FUTURE_HYPOTHESIS`**.

### Dos ejes de modulación (conceptuales — no termodinámica resuelta)

| | Eje | Cadena (esquema) |
|---|-----|------------------|
| **A. Interno** | Ligando → microswitches → red conformacional → salida funcional | Trp258, TM5/6/7, NPxxY, … |
| **B. Entorno** | Membrana / lípidos → estabilidad y equilibrio conformacional → salida funcional | Colesterol (MRI-2646); PS/CHS |

Estos ejes **organizan la hipótesis de trabajo**; **no** demuestran pesos relativos ni un sistema tripartito cuantitativo cerrado.

### Cadena de transmisión (framing PI — no colapsar)

```
ligando → microswitch → red de comunicación → TM5/6/7 → interfaz IC → Gαi2 / β-arr
```

**Prohibido como modelo operativo:** `ligando → Trp258 → Gαi2`. Trp258 puede ser entrada potente (**[LITERATURA_PRIMARIA]** Ganzoni 2026, DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)) pero **no** switch binario suficiente (**[LITERATURA_PRIMARIA]** Morales-Pastor 2025).

**Breathing / tiempo:** que hubs estáticos no sobrevivan dinámicamente bajo promedios multi-config es **coherente** con P1 estricto — **sin** post hoc de membrana. Detalle: [`docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md`](docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md).

### Pregunta original reformulada (parked)

No: *“encontrar una molécula con una forma dada.”*  
Más cerca: *“encontrar una perturbación química que mueva una red conformacional de CB2 hacia un estado funcional concreto **dentro de un contexto de membrana dado**.”*  
La pregunta del switch químico **no era absurda** — estaba **mal formulada**.

### Pregunta de reactivación (archivada — DO NOT RUN)

```
ligand + receptor + membrane  →  P(metastable states)
```

Si se reabre investigación: **medir cómo cambia esa distribución** — no lenguaje de “mejor docking score” / “pose óptima”.

### Oración de cierre (frontera epistemológica)

> Buen final provisional porque **no** dice “encontramos el switch”: dice qué preguntas ya no son razonables, cuáles siguen abiertas, y qué clase de experimento necesitaría una respuesta real. La hipótesis multivariable (ligando × paisaje × membrana) es más sólida que el switch inicial; sus contribuciones cuantitativas **no** están resueltas.

### Veredicto operativo

**`STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY`** — no `CB2_Gi_NETWORK_CANDIDATE`, no “switch”.

Lectura llana: los seis hubs son cuellos de botella topológicos reales en el mapa estático; el enriquecimiento celular PrefCoup_Gαi2 para ese *set* **no** está soportado. Carreteras importantes ≠ controladores demostrados de la decisión funcional que importa.

**Arquitectura física ≠ salida funcional.**

### Hipótesis eliminada (Test B)

❌ *“Los seis hubs estáticos son el núcleo funcional del sesgo Gαi2.”* — **eliminada** por Test B (`FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED`).

No sobreclaim: *“La red no tiene relación con Gαi2.”* sigue siendo demasiado fuerte (otros hubs / dinámica / combinaciones / redundancia / mismatch de métrica siguen posibles).

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto (Phase F/G/H, micronetwork, Contract v1.0, distancias medidas desde JSON del repo) |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada externa — requiere DOI, PMID o PDB |
| **[INTERNAL_REANALYSIS]** | Reanálisis sobre objetos públicos recuperados |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |
| **[INDETERMINATE]** | Bloqueado / irreproducible / datos incompletos |

---

## Gobernanza vigente

```yaml
# Freeze YAML — post-P1 boundary frozen (2026-08-21); honestidad epistemológica
STAGE: POST_P1_BOUNDARY_FROZEN
PRIMARY_OBJECTIVE: CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL  # not "find the switch"
EMPIRICAL_FOUNDATION:
  MACRO_STATE_RECOGNITION: VALIDATED  # Phase G / 8GUR GENERALIZES
  LOCAL_MICRO_NETWORK: INDETERMINATE  # HU-308/HU-433 — no universal static local mode
  STATIC_LIGACN_TOPOLOGY: CORE_TOPOLOGICAL_ONLY  # cfb2a51 — aggregate hubs, no Gi enrichment
  P1_DYNAMIC_HUBS: NOT_SUPPORTED  # six hubs ≠ persistent dynamic skeleton under GPCRmd/1540 WT
  DATA_PROVENANCE_AUDIT: PARTIAL  # GPCRmd/1540 WT local; Dutta–Shukla Box MSM still missing
THEORETICAL_MODEL:
  FRAMEWORK: TRIPARTITE_WORKING_HYPOTHESIS  # NOT demonstrated model
  NOTE: ligand × conformational ensemble × lipid bilayer; weights unresolved
  KEY_MODULATORS_CANDIDATE: [Allosteric Network, Cholesterol, Anionic Phospholipids]
PIPELINE_LOCKS:
  POST_HOC_EXCUSES: FORBIDDEN
  DOCKING_CAMPAIGNS: STOP
  DOCKING: STOP
  DE_NOVO_GENERATION: STOP
  OPEN_ENDED_SEARCHES: STOP
  COMPUTATION_ACTIVE: NONE
  COMPUTATION: PAUSED
  P5_EXECUTION: BLOCKED_PENDING_DECISION
  SIX_HUBS_DYNAMIC_SKELETON: REFUTED_UNDER_GPCRMD_WT
RESEARCH_STATUS: POST_P1_BOUNDARY_FROZEN
DYNAMIC_REANALYSIS: P1_DONE_FROZEN
P1_VERDICT: P1_NOT_SUPPORTED
P2: BLOCKED  # Dutta/Shukla MSM missing
P3: BLOCKED
P4: BLOCKED  # comparable CB1 missing
P5: HYPOTHESIS_READY  # 0% vs 40% cholesterol design candidate; NO execution
# Flags exactos preservados (autoridad — no relajar locks docking/de novo)
DE_NOVO_GENERATION: STOP
DOCKING_EXECUTION: STOP
ORTHOSTERIC_DESIGN: PAUSED
MACRO_COORDINATE: VALIDATED_OUT_OF_SAMPLE
FUNCTIONAL_EFFICACY: INDETERMINATE
HU308_HU433_MICROSTATE: INDETERMINATE
STATIC_LIGACN: CORE_TOPOLOGICAL_ONLY
MEMBRANE_MILIEU: FUTURE_HYPOTHESIS
NEW_PHASE: DO_NOT_OPEN
LINE_PAUSE: TRUE
# Aliases / legado
ORTOSTERIC_THCV_DESIGN: PAUSED
CORE_TOPOLOGICAL_ONLY: CLOSED
CB2_Gi_NETWORK_CANDIDATE: NOT_ESTABLISHED
DOCKING: STOP
COMPUTATION: PAUSED
ROADMAP_ACTIVE_PREP: LEGACY_ALIAS  # superseded by POST_P1_BOUNDARY_FROZEN
FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY: LEGACY_ALIAS
P1_DONE_AWAITING_JOINT_REVIEW: LEGACY_ALIAS  # superseded by P1_DONE_FROZEN
# Detalle operativo
STATIC_BOTTLENECKS: SUPPORTED
FUNCTIONAL_Gi_ENRICHMENT: NOT_SUPPORTED
CB2_MINIMAL_GI_CORE: NOT_FOUND
DUAL_HUB_TEST: CLOSED
NEW_HUB_SEARCH: STOP
NEW_VARIABLES_IN_PIPELINE: NONE
CONTRACT_v1.0: ARCHIVED_HISTORICAL
THRESHOLD_MODIFICATION: STOP
MODO: POST_P1_BOUNDARY_FROZEN / DOCUMENTATION_ONLY / NO_P5_COMPUTE
STATIC_GRAPH_ANALYSIS: CLOSED
DUAL_VALIDATION_HUBS: CLOSED
SINK_SET_T: EXTRACTED  # Arg131(3x50), Asp240(6x30), Ser303(8x47), Ser69(2x39)
CB1_COMPARISON: BLOCKED  # roadmap P4
DATA_PROVENANCE: PARTIAL  # GPCRmd/1540 WT traj local; Dutta–Shukla Box MSM HTTP 404
DATA_PROVENANCE_AUDIT: PARTIAL
RECOVERY_ATTEMPT: DONE  # one-shot 2026-08-21; log results/network_core/traj_recovery_attempt.md
TECHNICAL_SEARCH_TRAJ: STOP
ACTIVE_ACTION: DOCS_FREEZE_ONLY  # no traj / no P5 / no docking / no de novo
DUAL_TEST_COMMIT: cfb2a51
ABC_HIERARCHY_COMMIT: c2869b0
FREEZE_COMMIT: 2a1193c
P1_COMMIT: 31a881c
Q_MEMBRANA: HYPOTHESIS_READY_NO_EXECUTION  # = roadmap P5; P5_EXECUTION BLOCKED_PENDING_DECISION
NIVEL_A_CANONICAL: ACTIVE_BASELINE
NIVEL_B_CHOLESTEROL_LIPIDS: FUTURE_PRIORITY_HYPOTHESIS  # conceptual prep only; = P5
NIVEL_C_SECONDARY_MODULATORS: ARCHIVED_NOT_JUSTIFIED
WORKING_HYPOTHESIS: LIGAND_x_LANDSCAPE_x_MEMBRANE  # weights unresolved; not a final tripartite model
REACTIVATION_QUESTION: ligand+receptor+membrane -> P(metastable states)  # archived; DO NOT RUN as docking score hunt
P5_QUESTION: Does lipid composition change CB2 conformational-state distribution and communication network?
P5_QUESTION_REFINED: Does cholesterol change the dynamic routes CB2 uses to transit between states?
P2_OBJECT: TRANSITIONS  # evolution after P1; not hub permanence; still BLOCKED pending MSM
DYNAMIC_INTERACTION_LAYERS: docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md  # docs only; do not model all layers at once
HETEROMER_LAYER: FUTURE_NIVEL_C_ADJACENT  # A2A–CB2 lit registered; NOT in pipeline
ARCHIVED_NEXT_CALCULATION: PARKED
DYNAMIC_REANALYSIS: P1_DONE_FROZEN
NEXT: DECISION_GATE_ONLY  # no auto-P2; no P5 compute
ROADMAP: docs/synthesis/RESEARCH_ROADMAP.md
DRY_PIPELINE_SELFTEST: scripts/network_core/dynamic_pipeline.py --self-test
AUTHOR_REQUEST_CONTINGENCY_MORALES: REGISTERED_DO_NOT_EMAIL
```

**Cortafuegos de gobernanza (formal):**

```
RESEARCH_STATUS = POST_P1_BOUNDARY_FROZEN
DYNAMIC_REANALYSIS = P1_DONE_FROZEN
P1_VERDICT = P1_NOT_SUPPORTED
SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT
P2 = BLOCKED
P3 = BLOCKED
P4 = BLOCKED
P5 = HYPOTHESIS_READY
P5_EXECUTION = BLOCKED_PENDING_DECISION
POST_HOC_EXCUSES = FORBIDDEN
DE_NOVO_GENERATION = STOP
DOCKING = STOP
COMPUTATION = PAUSED
ORTHOSTERIC_DESIGN = PAUSED
MACRO_COORDINATE = VALIDATED_OUT_OF_SAMPLE
FUNCTIONAL_EFFICACY = INDETERMINATE
HU308_HU433_MICROSTATE = INDETERMINATE
STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY
MEMBRANE_MILIEU = FUTURE_HYPOTHESIS
NEW_PHASE = DO_NOT_OPEN
LINE_PAUSE = TRUE
NEW_VARIABLES_IN_PIPELINE = NONE
PRIMARY_OBJECTIVE = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
```

**Estado del repositorio:** `STAGE: POST_P1_BOUNDARY_FROZEN` — frontera post-P1 documentada; **no** P5 compute; **no** docking/de novo; **TRIPARTITE_WORKING_HYPOTHESIS** (no modelo demostrado); `DATA_PROVENANCE_AUDIT: PARTIAL`; anclas `cfb2a51` / `c2869b0` / `2a1193c` / `31a881c`; variables nuevas en pipeline = **cero**.

**[OBSERVACIÓN_PROPIA]** Diseño químico / de_novo / docking / nueva búsqueda de hubs / **nueva fase** / **P5 execution** **STOP**. `LINE_PAUSE = TRUE`. `COMPUTATION_ACTIVE = NONE`. Objetivo = mecanismo de control conformacional, **no** “find the switch.”  
**[INTERNAL_REANALYSIS]** Dual validation (`cfb2a51`) → **`CORE_TOPOLOGICAL_ONLY`**. P1 (`31a881c`) → **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`** (no causalidad biológica absoluta; no salto a “red plenamente distribuida”). Prohibido: “switch” como meta, “núcleo universal probado”, `CORE_FOUND`, `CB2_Gi_NETWORK_CANDIDATE`, “termodinámica CB2 resuelta”, “modelo tripartito final demostrado”, post hoc “faltaba colesterol”, P5 como rescate de P1.
---

## Jerarquía ambiental A/B/C (cortafuegos PI — DOCUMENTATION ONLY)

**No se abre fase (`NEW_PHASE = DO_NOT_OPEN`). No se añade variable al pipeline.** `STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY`. `LINE_PAUSE = TRUE`. Linaje A/B/C: `c2869b0`. **`MEMBRANE_MILIEU = FUTURE_HYPOTHESIS`**.

Separar ejes **A (interno / ligando→red)** y **B (entorno / lípidos→equilibrio)** como **organización conceptual** de la hipótesis de trabajo — **no** como termodinámica CB2 resuelta ni modelo tripartito demostrado.

| Nivel | Alcance | Evidencia | Estado en el proyecto |
|-------|---------|-----------|------------------------|
| **Nivel A: Núcleo Canónico** | Receptor + Ligando + Conformación | PDB structures, deep mutagenesis, LigACN WT | **Activo / Línea Base** (`CORE_TOPOLOGICAL_ONLY`) |
| **Nivel B: Entorno Directo** | Colesterol + composición lipídica (PS / aniónicos) | Modulación de actividad basal y cambio de clase farmacológica (p.ej. MRI-2646; efecto alostérico hacia regiones intracelulares / reclutamiento G; interfaz H8) | **Hipótesis Prioritaria Futura** (sin computación activa) |
| **Nivel C: Moduladores Secundarios** | Temperatura, Redox/Oxidación, pH local | Efectos bifísicos generales de estabilidad/cinética | **Archivado / No Justificado** (evitar dilución) |

### Lectura por nivel

**Nivel A — mandatory for current baseline.** Receptor + ligando + conformación bastan para el modelo *actual* del repo (PDB / mutagénesis / LigACN). **[OBSERVACIÓN_PROPIA]** / **[INTERNAL_REANALYSIS]** — línea base; **no** implica que el entorno sea irrelevante en la hipótesis de trabajo.

**Nivel B — environmental with direct CB2 evidence (future hypothesis).** Puede entrar en un *programa futuro* porque experimentos muestran que la farmacología puede cambiar; **no** está en el pipeline ahora; **no** se afirma que el medio lipídico solo explique la variabilidad funcional.

- **[LITERATURA_PRIMARIA]** MRI-2646: agonista parcial en membranas **sin** colesterol → antagonista neutro / agonista inverso parcial **con** colesterol; el colesterol eleva la actividad basal y puede ejercer efecto alostérico sobre regiones intracelulares que afectan el reclutamiento de G-proteína — Yeliseev et al., *Sci Rep* (2021), DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6), PMID [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/).
- **[LITERATURA_PRIMARIA]** Composición lipídica (CHS / PS aniónicos) estabiliza el pliegue funcional de CB2 y modula la eficiencia de activación de G — Vukoti et al., *PLoS One* (2012), DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290), PMID [23056277](https://pubmed.ncbi.nlm.nih.gov/23056277/); Kimura et al., *J Biol Chem* (2012), DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425), PMID [22134924](https://pubmed.ncbi.nlm.nih.gov/22134924/).
- **[HIPÓTESIS_ABIERTA]** Que los hubs estáticos del repo (TM7–H8 / base TM2) dependan de microdominios de colesterol/lípidos aniónicos — **no** demostrado aquí; ver `Q_membrana` (parked).

**Nivel C — not yet justified for central mechanism.** Temperatura fisiológica como modulador fino, oxidación/redox, pH local y otros mods: pueden afectar actividad/estabilidad físicamente, pero **no** son un “switch” fisiológico del mecanismo central. **Archivado / no justificado** — no diluir el foco.

### Pregunta aparcada (formal — NO EXECUTION) = **roadmap P5** (`HYPOTHESIS_READY`)

**`Q_membrana` / P5 (independiente; no rescata P1):** ¿La composición lipídica cambia la distribución de estados conformacionales y la red de comunicación de CB2?  
**Refinada (preferida):** ¿El colesterol cambia las **rutas dinámicas** CB2 entre estados? (actividad basal/clase ya anclada en lit. — no es la pregunta nueva.)

Design candidate (conceptual only): membranas **0% vs ~40% colesterol** — ancla lit. Yeliseev et al. (2021) MRI-2646, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6).  
**`P5 = HYPOTHESIS_READY`** · **`P5_EXECUTION = BLOCKED_PENDING_DECISION`** · Nivel B = future priority hypothesis, prep conceptual only.

Legacy formulation (still parked, not preferred framing): ¿Constituyen los hubs del eje TM7–H8 y base de TM2 propiedades intrínsecas del receptor o su conectividad está gobernada por microdominios de colesterol y lípidos aniónicos?

Si se reanuda más adelante: empezar por **Nivel B** (colesterol / composición lipídica), **no** por temperatura/oxidación/pH. Sin MD de colesterol ahora, sin docking, sin de novo, sin nueva fase hasta decisión conjunta explícita. **Prohibido** usar P5 como excusa post hoc de P1.

**Cross-link:** informe hubs [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) (ancla `cfb2a51`) · P1 [`results/network_core/p1_dynamic_hub_validation.md`](results/network_core/p1_dynamic_hub_validation.md) · roadmap [`docs/synthesis/RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md).
---

## Entregable cerrado — dual validation hubs (A/B)

**Informe:** [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md)  
**JSON:** [`results/network_core/hubs_dual_validation_report.json`](results/network_core/hubs_dual_validation_report.json)  
**Script:** [`scripts/network_core/test_hubs_dual_validation.py`](scripts/network_core/test_hubs_dual_validation.py)  
**Literatura PRIMARY:** Morales-Pastor et al. DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)

| Campo | Valor |
|-------|--------|
| Hubs (fijos) | ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46) |
| Test A | **`TOPOLOGICAL_BOTTLENECK_SUPPORTED`** — primary `%Disconn` p≈0.001 vs 1000 exact (in,out)-degree-matched nulls |
| Test B | **`FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED`** — Fisher PrefCoup_Gi p≈0.23 (membership ≠ atribución estadística; mutaciones listadas por separado) |
| Test C | Skipped (requiere A∧B) |
| Combined | **`CORE_TOPOLOGICAL_ONLY`** — network architecture without sufficient functional evidence |
| Formal name | *not assigned* (`CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED`) |
| Ancla commit | **`cfb2a51`** — preservar; no re-correr |
| Gobernanza post-cierre | `LINE_PAUSE = TRUE` · `DUAL_HUB_TEST = CLOSED` · `CB2_MINIMAL_GI_CORE = NOT_FOUND` |

**Safeguard B:** position membership (p.ej. N291A, R302A ∈ PrefCoup_Gi tras filtro expr.) ≠ sesgo estadísticamente atribuible al *set* vs background.

**Hipótesis eliminada:** “Los seis hubs estáticos son el núcleo funcional del sesgo Gαi2.” — no sobreclaim “la red no tiene relación con Gαi2.”

---

## Entregable cerrado — topología estática

**Informe lead:** [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md)  
**Métricas:** [`results/network_core/static_ligacn_topology_metrics.json`](results/network_core/static_ligacn_topology_metrics.json)  
**Veredicto:** [`results/network_core/static_topological_verdict.json`](results/network_core/static_topological_verdict.json)  
**Script:** [`scripts/network/analyze_static_ligacn_topology.py`](scripts/network/analyze_static_ligacn_topology.py)

| Campo | Valor |
|-------|--------|
| `STATIC_TOPOLOGICAL_BOTTLENECKS` | **`TOPOLOGICAL_HUBS_IDENTIFIED`** |
| Source Set S (verificado) | `8D0:1`, `SER:285`, `PHE:87` |
| AUSENTE (no sustituidos) | `TRP:258`, `PHE:183` (fuera de WT_degeneracy; sí hay columnas `*-LIG` en SD2 Inactive) |
| Sink Set T | ARG:131, ASP:240, SER:303, SER:69 (4/4 reachable) |
| Hubs enriquecidos (no-S/T) | ALA:83, ALA:79, ASN:291, ASN:295, LEU:287, ARG:302 |
| Límite | Solo propiedades de la red agregada publicada — **no** causalidad Gi; arquitectura candidata ≠ switch |

**Futuro parked (no ahora):** cruzar topología con dinámica — solo decisión conjunta posterior. Frontera actual = **`CORE_TOPOLOGICAL_ONLY`**.

---

## Separación en cuatro niveles (directiva PI — cierre epistemológico)

**Naming:** no decir «switch found». Hubs estáticos ≠ microswitches / controladores Gi demostrados.

| # | Nivel | Dominio | Pregunta | Estatus |
|---|-------|---------|----------|---------|
| 1 | **MACROCONFORMACIÓN** | TM3–TM6 | ¿Reconoce estados activos? | 🟢 **Sí** — generalización OOS (Phase G) |
| 2 | **MICRO-RED LOCAL** | Trp258 / Ser285 / ECL2 | ¿Cómo modifica cada ligando esa conformación? | 🟡 Dependiente del estado; sin pose rígida universal (micronetwork) |
| 3 | **TOPOLOGÍA ESTÁTICA** | TM7 / TM2 / NPxxY / H8 | ¿Hay bottlenecks reales en el mapa estático? | 🟢 **Sí** — `STATIC_BOTTLENECKS = SUPPORTED` (ALA79, ALA83, LEU287, ASN291, ASN295, ARG302). S verificado **sin** forzar TRP258/PHE183 (**AUSENTE**) |
| 4 | **FUNCIÓN Gαi2** | PrefCoup / sesgo Gi | ¿Muestran estos hubs enriquecimiento PrefCoup demostrado? | 🔴 **No** — `FUNCTIONAL_Gi_ENRICHMENT = NOT_SUPPORTED` (Test B). Veredicto conjunto **`CORE_TOPOLOGICAL_ONLY`** |

**Arquitectura física ≠ salida funcional.** Nivel 3 🟢 no eleva nivel 4.

### Dual validation (CLOSED — ancla `cfb2a51`)

Hubs fijos × knockout degree-matched (A) × SD1 PrefCoup Fisher (B) → **`CORE_TOPOLOGICAL_ONLY`**.  
Deliverable: `results/network_core/hubs_dual_validation_report.md`.  
**`DUAL_HUB_TEST = CLOSED`** · **`LINE_PAUSE = TRUE`** — pausa real; sin compute.

### Parked (NO EJECUTAR)

1. Cruzar topología con dinámica — solo si se decide conjuntamente más adelante. Aceptar **`CORE_TOPOLOGICAL_ONLY`** como frontera del modelo actual por ahora.
2. **`Q_membrana`** (**roadmap P5** / Nivel B futuro): hubs TM7–H8 / base TM2 — ¿intrínsecos o gobernados por microdominios de colesterol / lípidos aniónicos? Si se reanuda: empezar por colesterol/composición lipídica, **no** temperatura/oxidación/pH. Orden: tras P1–P3.

**No es:** otro docking, librería química, retune de Contract, nueva búsqueda de hubs, MD de colesterol, ni nueva fase.

**Estado gobernanza:** `CB2_MINIMAL_GI_CORE = NOT_FOUND` · `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` · `CB1_COMPARISON = BLOCKED` · `DUAL_HUB_TEST = CLOSED` · `NEW_VARIABLES_IN_PIPELINE = NONE` · `Q_MEMBRANA = PARKED`

**Protocolo (histórico / dinámico):** [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md)  
**Informe previo (core dinámico INDETERMINATE):** [`results/network_core/cb2_minimal_gi_core_report.md`](results/network_core/cb2_minimal_gi_core_report.md)  
**Auditoría:** [`results/network_core/data_audit.md`](results/network_core/data_audit.md)  
**Proveniencia:** [`results/network_core/provenance_recovery_log.md`](results/network_core/provenance_recovery_log.md)
---

## Diagrama de estado

```
LITERATURA / DATOS PÚBLICOS
        │
        ├── 1 ESTADO GLOBAL (TM3–TM6)     🟢 Phase G OOS
        ├── 2 MICROESTADO (Trp258/Ser285/ECL2)  🟡 state-dependent
        ├── CB2 LigACN SD1–3 local ✓
        ├── Sink Set T EXTRACTED ✓
        └── traj GPCRmd / Box MSM = ENLACE only
                  │
                  ▼
        3 TOPOLOGÍA ESTÁTICA
        STATIC_BOTTLENECKS = SUPPORTED
        DUAL_HUB_TEST = CLOSED (cfb2a51)
        verdict: CORE_TOPOLOGICAL_ONLY
        ≠ switch; CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED
                  │
                  ▼
        4 FUNCIÓN Gαi2
        FUNCTIONAL_Gi_ENRICHMENT = NOT_SUPPORTED
        CB2_MINIMAL_GI_CORE = NOT_FOUND
        (hipótesis “6 hubs = núcleo funcional Gi bias” ELIMINADA)
                  │
                  ▼
                 LINE_PAUSE = TRUE (pausa compute; frontera post-P1 congelada)
                 RESEARCH_STATUS = POST_P1_BOUNDARY_FROZEN
                 DYNAMIC_REANALYSIS = P1_DONE_FROZEN
                 P1_VERDICT = P1_NOT_SUPPORTED
                 SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT
                 P2–P4 = BLOCKED · P5 = HYPOTHESIS_READY (NO execution)
                 NEW_PHASE = DO_NOT_OPEN
                 COMPUTATION_ACTIVE = NONE
                 NEW_VARIABLES_IN_PIPELINE = NONE
                 A/B/C firewall · P5_EXECUTION = BLOCKED_PENDING_DECISION
                 MEMBRANE_MILIEU = FUTURE_HYPOTHESIS
                 PRIMARY_OBJECTIVE = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
                 working hyp. (weights unresolved)
                 linaje: cfb2a51 → c2869b0 → 31a881c (P1) → freeze docs
```

---

## Roadmap P1–P6 (contrato científico — árbol de decisión)

**Autoridad detallada:** [`docs/synthesis/RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md)  
**Estado:** `POST_P1_BOUNDARY_FROZEN` · freeze docking/de novo/P5-exec · P1 = `NOT_SUPPORTED` (esqueleto dinámico de seis hubs refutado bajo GPCRmd WT)

```
P1 hubs = persistent dynamic skeleton under GPCRmd/1540 WT?
  NO → P1_NOT_SUPPORTED (strict: six static hubs ≠ detectable persistent dynamic subnet)
       leaves open A–D (distributed / state-dependent / routes≠static / lipid-dependent)
  YES → P2 architecture changes across microstates?
         NO → approximately stable network
         YES → P3 changes relate to Gαi2?
                NO → architecture without demonstrated functional link
                YES → P4 CB1 different?
                       NO → weak conformational selectivity basis
                       YES → P5 membrane modifies?
                              NO → Level A sufficient
                              YES → P6 chemical perturbation can shift?
                                    (P6 does not exist until P1–P5 survive)
```

Cada respuesta abre/cierra **una sola puerta**. Cómputo = **PAUSED**; P5 execution = **BLOCKED_PENDING_DECISION**. P1 **no** se “rescata” con colesterol post hoc.

---
## Registro provisional — tabla de resultados (literatura / abierto)

**[LITERATURA_PRIMARIA]** / **[HIPÓTESIS_ABIERTA]** / **[INTERNAL_REANALYSIS]**

| Pregunta | Estado |
|----------|--------|
| ¿Hay una red CB2→efector intracelular? | 🟢 Establecido por literatura (ACN/LigACN; Morales-Pastor 2025, DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID 40500255) |
| ¿Qué hubs/bottlenecks topológicos tiene LigACN WT estático hacia Sink T? | 🟢 **`TOPOLOGICAL_HUBS_IDENTIFIED`** — ver `static_ligacn_topology_report.md` (**no** causal; arquitectura candidata, no switch) |
| ¿La red está concentrada en Trp258/Ser285? | 🔴 No como “único switch”; Trp258 **AUSENTE** del grafo WT_degeneracy; Ser285 es miembro de S (contacto ligando verificado) |
| ¿TM7 participa especialmente en ruta agonismo/Gi? | 🟢 Apoyado (literatura + hubs ASN:291/295, LEU:287, ARG:302 en mapa estático) |
| ¿CB2 posee una única coordenada conformacional suficiente para Gi? | 🔴 No demostrado |
| ¿Los 6 hubs son bottleneck topológico degree-matched? | 🟢 **A SUPPORTED** (`TOPOLOGICAL_BOTTLENECK_SUPPORTED`, p≈0.001) — ver dual validation |
| ¿El set está enriquecido en PrefCoup_Gαi2 (Fisher, expr≥25%)? | 🔴 **B NOT_SUPPORTED** (p≈0.23) — membership parcial ≠ atribución estadística |
| ¿Candidate conjunto topología∧función? | 🔴 **`CORE_TOPOLOGICAL_ONLY`** — `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` |
| ¿Los 6 hubs son el núcleo funcional del sesgo Gαi2? | 🔴 **ELIMINADA** (Test B) — no sobreclaim “la red no tiene relación con Gαi2” |
| ¿Los 6 hubs son esqueleto dinámico persistente (GPCRmd/1540 WT)? | 🔴 **`P1_NOT_SUPPORTED`** / **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`** — no refuta causalidad biológica absoluta; no salta a “red plenamente distribuida”; deja abiertas A–D |
| ¿Núcleo mínimo Gi encontrado? | 🔴 **`CB2_MINIMAL_GI_CORE = NOT_FOUND`** |
| ¿Colesterol / lípidos aniónicos cambian farmacología CB2? | 🟢 **[LITERATURA_PRIMARIA]** Sí (MRI-2646 / basal / PS–CHS) — Yeliseev 2021 DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6); Kimura 2012 DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425); Vukoti 2012 DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290) — **Nivel B, no en pipeline** |
| ¿Composición lipídica cambia estados + red de comunicación CB2? (P5) | ⏸ **`HYPOTHESIS_READY`** — **[HIPÓTESIS_ABIERTA]**; design candidate 0% vs 40% chol; **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**; independiente de P1 |
| ¿Colesterol cambia **rutas dinámicas** entre estados? (P5 refinada) | ⏸ **`HYPOTHESIS_READY`** — framing preferido; no execution |
| ¿Objeto P2 = transiciones (conexiones que cambian entre estados)? | ⏸ **Registrado** — evolución post-P1; **`P2 = BLOCKED`** (MSM); ver capas |
| ¿Heterómero A2A–CB2 como perturbación alostérica no-ligando-CB2? | ⏸ **Nivel-C-adjacent / futura** — **[LITERATURA_PRIMARIA]** DOI [10.1111/bph.16502](https://doi.org/10.1111/bph.16502) (PMID 39044481); 2025 DOI [10.1016/j.bcp.2025.117280](https://doi.org/10.1016/j.bcp.2025.117280) — **no** pipeline |
| ¿Hubs TM7–H8 / TM2 intrínsecos vs entorno lipídico? (`Q_membrana` legacy) | ⏸ **PARKED / subsumed under P5** — no execution |
| ¿Temperatura / redox / pH como switch central? | 🔴 **Nivel C archivado** — no justificado para mecanismo central |

---

## Mapa epistemológico (cuatro niveles — PI)

| Nivel | Dominio | Estatus | Evidencia clave |
|-------|---------|---------|-----------------|
| **1 — MACROCONFORMACIÓN** | TM3–TM6 | 🟢 **Sí (OOS)** | **[OBSERVACIÓN_PROPIA]** Phase G: 8GUR (2.32) ≈ 6KPF (2.30) ≪ 5ZTY (3.95); veredicto **GENERALIZES** |
| **2 — MICRO-RED LOCAL** | Trp258 / Ser285 / ECL2 | 🟡 **Estado-dependiente** | **[OBSERVACIÓN_PROPIA]** Micronetwork **INDETERMINATE** (6PT0 identical / 6KPF distinct); sin pose rígida universal; Phase H **INDETERMINATE** |
| **3 — TOPOLOGÍA ESTÁTICA** | TM7 / TM2 / NPxxY / H8 | 🟢 **Bottlenecks reales** | **[INTERNAL_REANALYSIS]** `STATIC_BOTTLENECKS = SUPPORTED` (ALA79, ALA83, LEU287, ASN291, ASN295, ARG302); S sin forzar TRP258/PHE183 |
| **4 — FUNCIÓN Gαi2** | PrefCoup / sesgo Gi | 🔴 **No demostrado** | **[INTERNAL_REANALYSIS]** `FUNCTIONAL_Gi_ENRICHMENT = NOT_SUPPORTED`; hipótesis “6 hubs = núcleo funcional Gi bias” **eliminada**; `CB2_MINIMAL_GI_CORE = NOT_FOUND` |
---

## Contradicciones abiertas (registro maestro)

**[OBSERVACIÓN_PROPIA]** Tabla canónica en [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) §7. Resumen — **sin armonización post hoc**:

| Tema | Evidencia en conflicto | Estado |
|------|------------------------|--------|
| **HU-433** | Ki radioligando menor vs potencia biológica mayor (Smoum 2015, DOI [10.1073/pnas.1503395112](https://doi.org/10.1073/pnas.1503395112); PMID 26124120); GTPγS Emax no siempre significativo; orientaciones distintas propuestas; Phase H INDETERMINATE | **ABIERTA** |
| **AM630** | Inverse agonist (cAMP −152%) vs comportamiento casi neutral (GTPγS −22%) en Soethoudt 2017 (DOI [10.1038/ncomms13958](https://doi.org/10.1038/ncomms13958); PMID 28045051); Phase H = PROTEAN | **ABIERTA** |
| **Trp258^6.48** | Literatura: continuo funcional vía toggle (Ganzoni 2026, DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)) **y** ACN distribuida **no** reducida a Trp258 (Morales-Pastor 2025) vs proyecto: micronetwork INDETERMINATE (6PT0 enmascara / 6KPF detecta) | **ABIERTA** |
| **WIN 55,212-2** | cAMP full agonist (98%) vs GTPγS partial agonist (49%) — Soethoudt 2017 | **ABIERTA** |
| **Docking → función** | Rachman 2026: template activo/inactivo no predice clase funcional; Phase E lit-activos FAIL Contract v1.0 | **ABIERTA** |
| **8GUS vs 6PT0** | Pose experimental HU-308 (PDB **8GUS**) vs colapso centroide en docking 6PT0 | **ABIERTA** |

> **Regla:** todas las filas = **ABIERTA**. No se inventa resolución. La corrección «Trp258 no es switch único» (**[LITERATURA_PRIMARIA]**) **no** cierra la fila Trp258 del paradox del par HU-308/HU-433.

---

## Cierre ordenado de fases conformacionales

| Fase | Veredicto | Fecha cierre | Fuente |
|------|-----------|--------------|--------|
| **F** — Huella conformacional | COMPLETE | 2026-08-19 | `results/conformational/fase_f_conformational_fingerprint.md` |
| **G** — Generalización 8GUR OOS | **GENERALIZES** (Q1); Q2 PARTIAL | 2026-08-19 | `results/conformational/fase_g_generalization_report.md` |
| **H** — Ordinal funcional H0/H1 | **INDETERMINATE** | 2026-08-19 | `results/conformational/fase_h_ordinal_functional_report.md` |
| **Micronetwork** HU-308 vs HU-433 | **INDETERMINATE** | 2026-08-20 | `results/conformational/micronetwork_modes_report.md` |

### Notas de cierre

**[OBSERVACIÓN_PROPIA]**

- **Phase G:** coordenada macro CB2_STATE_DISTANCE generaliza out-of-sample a **8GUR** (CP55,940 + Gi, ciego).
- **Phase H:** HU-433 sin fila Gi comparable forzada; AM630 = PROTEAN; proyección conformacional insuficiente para ordinal.
- **Micronetwork:** plasticidad de estado — no promover DISTINCT 6KPF como ley del par enantiomérico.
- **Retenidos por directiva PI:** GENERALIZES / INDETERMINATE / INDETERMINATE — no reinterpretar.

---

## Congelación científica (frontera epistemológica)

| Ámbito | Estado |
|--------|--------|
| `RESEARCH_STATUS` | **`FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY`** |
| Retrospectivo A–E (`results/docking/`) | **CLOSED_AND_ARCHIVED** — read-only |
| Calibración multistate | **CLOSED** (2026-08-19) |
| Contract v1.0 | **ARCHIVED_HISTORICAL** — testigo 6PT0, no predictor funcional |
| `ORTHOSTERIC_DESIGN` | **PAUSED** |
| `DE_NOVO_GENERATION` / `DOCKING_EXECUTION` | **STOP** |
| `COMPUTATION_ACTIVE` | **NONE** |
| `MACRO_COORDINATE` | **VALIDATED_OUT_OF_SAMPLE** (Phase G) |
| `FUNCTIONAL_EFFICACY` / `HU308_HU433_MICROSTATE` | **INDETERMINATE** |
| `STATIC_LIGACN` | **CORE_TOPOLOGICAL_ONLY** (ancla `cfb2a51`) |
| `MEMBRANE_MILIEU` | **FUTURE_HYPOTHESIS** |
| `NEW_PHASE` | **DO_NOT_OPEN** |
| `LINE_PAUSE` | **TRUE** |
| Variables nuevas en pipeline | **NONE** |
| Jerarquía A/B/C | **Preservada** (`c2869b0`) |
| `Q_membrana` | **PARKED** (DO NOT RUN) |
| Hipótesis de trabajo (ligando × paisaje × membrana) | **Abierta** — pesos **no** resueltos; **no** modelo tripartito final |
| Pregunta reactivación `P(metastable states)` | **Archivada** — medir distribución, no docking score |
| `ARCHIVED_NEXT_CALCULATION` (núcleo dinámico CB2→Gi) | **PARKED** — documentado abajo; **NOT NOW** |
| `DYNAMIC_REANALYSIS` | **FUTURE / BLOCKED_PENDING_TRAJECTORIES** — dos redes; sin `W=-ln(p)` universal; sin umbral a priori >50% |
| `DATA_PROVENANCE_AUDIT` | **PARTIAL** — SI/endpoints; traj/MSM **not** fully recovered |

---

## ARCHIVED_NEXT_CALCULATION — núcleo dinámico CB2→Gi (PI — PARKED / NOT NOW)

**Estado:** **`PARKED`**. Documentación de viabilidad y protocolo epistemológico corregido. **`COMPUTATION_ACTIVE = NONE`**. **`NEW_PHASE = DO_NOT_OPEN`**. **`RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY`**.  
**Prohibido ahora:** descargar trayectorias, correr MD, docking, de novo, análisis de red dinámica.

### Roadmap flags (formal)

```
DYNAMIC_REANALYSIS = FUTURE / BLOCKED_PENDING_TRAJECTORIES
PRIMARY:   do static hubs persist as dynamic nodes?
SECONDARY: does communication change across metastable states?
TERTIARY:  do dynamic nodes show functional enrichment?
NO_ASSUMPTION: no switch, no core, no prefabricated survival threshold
CURRENT:
  COMPUTATION = PAUSED
  DOCKING = STOP
  DE_NOVO = STOP
  RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY
```

### Distinción: “calcularlo” ≠ inventar desde cero

Reconstruir / reanalizar un **núcleo dinámico CB2→Gi** a partir de **datos publicados** es técnicamente viable — **no** equivale a inventar energías absolutas ni moléculas *de novo*.

| Fuente | Escala / objeto | DOI |
|--------|-----------------|-----|
| **[LITERATURA_PRIMARIA]** Dutta & Shukla (2023) | ~700 μs MSM / VAMPnets; ~6 estados metaestables cada CB1/CB2 | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| **[LITERATURA_PRIMARIA]** Morales-Pastor et al. (2025) | WT CB2 ~2 μs acumulados; LigACN ortostérico→intracelular; mutagénesis / Gαi2 | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0) |

### Corrección epistemológica (protocolo dinámico aparcado)

**No** fijar `W_ij = -ln(p_ij)` como representación universal de red dinámica. Persistencia de contacto ≠ comunicación conformacional:

- `p_ij` = cuánto tiempo existe un contacto
- correlación / mutual information / transfer entropy ≈ cuán relacionadas están las mociones

Un contacto muy persistente puede ser estructuralmente estable y transmitir poca información de perturbación.

**Dos redes dinámicas separadas (mantener ambas):**

```
TRAJECTORIES
   │
   ├──► PERSISTENCE NETWORK
   │      W_contact = f(p_ij)
   │
   └──► COMMUNICATION NETWORK
          W_info = f(correlation / mutual information)
```

Solo entonces preguntar si los seis hubs estáticos aparecen en **ambas**.

**Sin criterio a priori >50% de supervivencia.** **No** imponer “los seis deben retener >50% del flujo”. Medir primero: fracción de flujo, distribución por microestado, estabilidad entre réplicas; luego comparar seis hubs vs null apropiado. Descubrir: supervivencia real / estado-específica / rutas sustituidas / redundancia profunda.

### Pregunta primaria (framing científico)

**No:** “¿dónde está el switch?”  
**Sí:** “¿Está la comunicación alostérica de CB2 restringida a una subred persistente, o se redistribuye dinámicamente entre múltiples rutas?”

Cadena: **MACROSTATE → microestados → red dinámica → rutas alternativas → Gαi / β-arrestin**.  
**Sin** asunción a priori de que exista un core.

| Prioridad | Pregunta |
|-----------|----------|
| **PRIMARY** | ¿Persisten los hubs estáticos como nodos dinámicos (en **ambas** redes)? |
| **SECONDARY** | ¿Cambia la comunicación entre estados metaestables? |
| **TERTIARY** | ¿Los nodos dinámicos muestran enriquecimiento funcional (Gαi / β-arr)? |

### Niveles de dificultad (solo registro)

| # | Nivel | Viabilidad |
|---|-------|------------|
| 1 | Reproducir lo publicado | Relativamente factible |
| 2 | Dos redes propias (persistencia + comunicación; caminos, centralidad, robustez; **sin** umbral prefabricado) | Factible con cuidado |
| 3 | Causalidad funcional | Mucho más duro — requiere dinámica conjunta + mutagénesis / Gαi (datos Morales-Pastor existen) |

### Regla crítica (gobernanza)

**No** correr ~700 μs MD propios como primer paso. Si se descongela: **análisis a posteriori** de trayectorias originales **si** se recuperan (`DATA_PROVENANCE_AUDIT` sigue **PARTIAL**; GPCRmd 1540 / Box = `ENLACE_REGISTRADO`). MD nuevo **solo** si el análisis publicado **no** puede responder la pregunta.

### Membrana también calculable más tarde

Colesterol cambia farmacología CB2; MD con/sin ~40% colesterol (~2 μs) — **[LITERATURA_PRIMARIA]** Yeliseev et al., DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6). **`Q_membrana` / `MEMBRANE_MILIEU` = FUTURE** — no ahora.

### Tabla de viabilidad (registro)

| Objetivo | Semáforo |
|----------|----------|
| Reproducir dinámica publicada | 🟢 |
| Reconstruir **dos** redes dinámicas (persistencia + comunicación) | 🟢 |
| Comparar hubs estáticos vs ambas redes (sin umbral a priori) | 🟢 / 🟡 |
| vs CB1 | 🟡 |
| Vincular mutagénesis Gαi | 🟡 |
| Probar causalidad farmacológica | 🔴 — no solo cálculo |
| Colesterol + dinámica | 🟡 — más costoso |

### Cálculo NEXT recomendado SI se descongela (NOT NOW)

1. Construir **ambas** redes (persistencia y comunicación); **no** colapsar a `W = -ln(p)`.
2. ¿Aparecen los **seis hubs estáticos** en **ambas** redes? Medir flujo / distribución / réplicas — **sin** umbral >50% prefabricado.
3. ¿Cambia la comunicación entre microestados / metaestables (redistribución vs subred fija)?
4. ¿Los nodos dinámicos se enriquecen hacia mutaciones / lectura Gαi2 / β-arrestin?

| Resultado | Lectura |
|-----------|---------|
| Hubs en **ambas** redes + estabilidad entre estados | Evidencia más fuerte para **subred persistente** (nombre: **nunca** “switch”). `CB2_Gi_NETWORK_CANDIDATE` **solo** si dual criteria + revisión humana. |
| Persistencia ≠ comunicación, o rutas sustituidas / estado-específicas | Comunicación **redistribuida** — `CORE_TOPOLOGICAL_ONLY` era propiedad del grafo agregado, no mecanismo dinámico fijo. También es respuesta clara. |
| Null / réplicas no separan seis hubs | Sin core prefabricado; no inventar supervivencia. |

**Naming lock:** no “switch”; no “core” a priori; `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` hasta criterios duales post-revisión.

### Andamiaje técnico (pre-registro — NO traj real)

| Artefacto | Ruta |
|-----------|------|
| Protocolo congelado | [`docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md`](docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md) |
| Pipeline seco + null P1 + self-tests | [`scripts/network_core/dynamic_pipeline.py`](scripts/network_core/dynamic_pipeline.py) |
| Gate status | [`scripts/network_core/prepare_dynamic_reanalysis.py`](scripts/network_core/prepare_dynamic_reanalysis.py) |
| Entry P1 | [`scripts/network_core/run_dynamic_hub_persistence.py`](scripts/network_core/run_dynamic_hub_persistence.py) |
| Status JSON | `results/network_core/dynamic_reanalysis_status.json` |
| Self-test JSON | `results/network_core/dynamic_pipeline_selftest.json` |

```bash
python scripts/network_core/dynamic_pipeline.py --self-test --status
```

---

## Índice — síntesis consolidada (`docs/synthesis/`)

| Documento | Contenido |
|-----------|-----------|
| [`docs/synthesis/CB2_STRUCTURE_ATLAS.md`](docs/synthesis/CB2_STRUCTURE_ATLAS.md) | Atlas PDB: 5ZTY, 6PT0, 6KPF, 8GUS/UR/UQ/UT, 12IY/IZ/JA, 8X3L, 9U7L; Level-0; Phase F/G |
| [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) | Par enantiomérico; 8GUS experimental; Soethoudt/Hanuš; micronetwork INDETERMINATE; **contradicciones abiertas** |
| [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) | ACN/LigACN (Morales-Pastor 2025); MSM (Dutta & Shukla 2023); Trp258 no switch único; frontera MD |
| [`docs/synthesis/RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md) | **Contrato científico** P1–P6 + árbol de decisión; P6 solo tras P1–P5 |
| [`docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md`](docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md) | **Mapa multicapa** + giro P2 a transiciones; cortafuegos (no todas las capas a la vez) |
| [`docs/synthesis/CB2_RESEARCH_ROADMAP.md`](docs/synthesis/CB2_RESEARCH_ROADMAP.md) | Alias / redirect → `RESEARCH_ROADMAP.md` |
| [`docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md`](docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md) | **Pre-registro técnico data-blind** P1–P3: dos redes; null degree-matched; self-tests sintéticos; `BLOCKED_PENDING_TRAJECTORIES` |
| [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo estático histórico + puntero al dinámico; `CB2_MINIMAL_GI_CORE = NOT_FOUND` |
| [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md) | Topología estática LigACN→T (**CLOSED**; `STATIC_BOTTLENECKS = SUPPORTED`) |
| [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) | Dual A/B (**CLOSED**, `cfb2a51`) → **`CORE_TOPOLOGICAL_ONLY`** |
| [`docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md`](docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md) | Límites estáticos; Rachman 2026; INDETERMINATE; gobernanza completa |

---

## Índice — artefactos conformacionales

| Artefacto | Ruta |
|-----------|------|
| Phase F report + matrix | `results/conformational/fase_f_conformational_fingerprint.md`, `cb2_state_distance_matrix.json` |
| Phase G report | `results/conformational/fase_g_generalization_report.md` |
| Phase H report | `results/conformational/fase_h_ordinal_functional_report.md` |
| Micronetwork report | `results/conformational/micronetwork_modes_report.md` |
| Micronetwork falsification | `results/conformational/micronetwork_falsification_report.md` |

---

## Índice — documentos de gobernanza relacionados

| Documento | Ruta |
|-----------|------|
| Bitácora maestra (extendida) | `docs/JANUSFORGE_RESEARCH_STATE.md` |
| Síntesis frontera metodológica | `docs/cb2_mechanistic_frontier_synthesis.md` |
| Balance epistemológico | `docs/epistemic_balance_calibration_2026-08-19.md` |
| Reformulación switch | `docs/switch_hypothesis_allosteric_reformulation.md` |
| Mapa alostérico (HIPÓTESIS) | `docs/cb2_allosteric_switch_map.md` |
| Calibración multistate | `docs/cb2_multistate_calibration_synthesis.md` |

---

## Próximo paso — LINE_PAUSE (frontera post-P1 congelada)

**[OBSERVACIÓN_PROPIA]**

1. **`RESEARCH_STATUS = POST_P1_BOUNDARY_FROZEN`.** P1 = `NOT_SUPPORTED` bajo GPCRmd/1540 WT; **`SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`**. Hipótesis de trabajo multivariable; **no** modelo tripartito demostrado.
2. Lectura estricta P1: **no** refuta causalidad biológica absoluta de hubs; **sí** refuta esqueleto dinámico persistente de esos seis bajo traj analizadas. Sin post hoc colesterol; sin salto a “red plenamente distribuida” (A–D abiertas).
3. Explicitamente NO: switch único; hubs estáticos controlan Gαi2; `CB2_Gi_NETWORK_CANDIDATE`; TPSA ≡ periferia; lípido solo explica variabilidad; estrategia química usable lista; P5 como rescate de P1.
4. A/B/C preservada (`c2869b0`); **P5 = HYPOTHESIS_READY** (0% vs 40% chol; Yeliseev MRI-2646 DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6)); pregunta refinada = **rutas dinámicas** entre estados; **`P5_EXECUTION = BLOCKED_PENDING_DECISION`**; Nivel B = future priority, conceptual prep only.
5. P2–P4 **BLOCKED** (MSM / CB1). Objeto P2 registrado = **transiciones** (no hubs permanentes). Sin auto-P2.
6. Capas de interacción dinámica documentadas (`CB2_DYNAMIC_INTERACTION_LAYERS.md`); **no** modelar todas a la vez. Heterómero = futura / no pipeline.
7. **`LINE_PAUSE = TRUE`.** **`NEW_PHASE = DO_NOT_OPEN`.** **`COMPUTATION = PAUSED`.** Sin docking, de novo, MD, ni P5 compute.

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`) — tabla consolidada + locks post-P1
2. [`results/network_core/p1_dynamic_hub_validation.md`](results/network_core/p1_dynamic_hub_validation.md) — veredicto P1 (`31a881c`)
3. [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) — ancla `cfb2a51`
4. [`docs/synthesis/RESEARCH_ROADMAP.md`](docs/synthesis/RESEARCH_ROADMAP.md) — contrato P1–P6
5. [`docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md`](docs/synthesis/CB2_DYNAMIC_INTERACTION_LAYERS.md) — mapa multicapa + giro P2→transiciones
6. [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) — Morales-Pastor / Dutta–Shukla / Trp258
7. [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) — Smoum / Ganzoni; contradicciones abiertas

---

*Fin RESEARCH_STATE.md. 2026-08-21 — STAGE POST_P1_BOUNDARY_FROZEN at epistemological frontier (mechanism NOT solved); P1_NOT_SUPPORTED; SIX_HUBS_DYNAMIC_SKELETON=REFUTED_UNDER_GPCRMD_WT; P2 object → transitions (still BLOCKED); multilayer map registered; P5=HYPOTHESIS_READY (routes between states) / P5_EXECUTION=BLOCKED_PENDING_DECISION; POST_HOC_EXCUSES=FORBIDDEN; DE_NOVO/DOCKING=STOP; COMPUTATION=PAUSED; CORE_TOPOLOGICAL_ONLY; linaje cfb2a51 / c2869b0 / 2a1193c / 31a881c; documentation only — no P5 compute / no MD / no docking / no de novo.*
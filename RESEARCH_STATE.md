# RESEARCH STATE — Janusforge CB₂ (congelación científica / frontera epistemológica)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — reposo científico; **no** compute, **no** docking, **no** de novo, **no** nueva fase, **no** push  
**Anclas de linaje (preservar):** `cfb2a51` (dual-test limpio → topología-only) · `c2869b0` (jerarquía ambiental A/B/C + `Q_membrana` parked) · `2a1193c` (reposo científico / frontera)  
**Bitácora extendida:** [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md)  
**Puntero síntesis:** [`docs/cb2_mechanistic_frontier_synthesis.md`](docs/cb2_mechanistic_frontier_synthesis.md) (este archivo es la autoridad de freeze)

---

## Hipótesis de trabajo (redacción exacta — no modelo final)

The project ends with a more realistic **working hypothesis**: CB2 activity appears to emerge from the interaction among ligand, conformational landscape, and membrane environment, but the **quantitative contribution of each component is not yet resolved**.

**Prohibido afirmar:** que el “modelo final” **demuestra** un sistema tripartito definitivo, o que se **resolvió** la termodinámica de CB2. Ligando / paisaje / membrana son ejes de una **hipótesis multivariable**, no un veredicto cuantitativo cerrado.

**TRIPARTITE** = **working hypothesis / framing only** — **NOT** a demonstrated final model; quantitative weights still unresolved (lenguaje preservado desde `2a1193c`).

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
| Proveniencia | **`DATA_PROVENANCE_AUDIT: PARTIAL` — SI/endpoints registered; traj/MSM download not completed** (GPCRmd 1540 / Box = `ENLACE_REGISTRADO`; Sink T from Methods; MOESM2 recovered) |

---

## Flags de freeze (exactos — autoridad)

```
RESEARCH_STATUS           = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY
DE_NOVO_GENERATION        = STOP
DOCKING_EXECUTION         = STOP
COMPUTATION_ACTIVE        = NONE
ORTHOSTERIC_DESIGN        = PAUSED
MACRO_COORDINATE          = VALIDATED_OUT_OF_SAMPLE
FUNCTIONAL_EFFICACY       = INDETERMINATE
HU308_HU433_MICROSTATE    = INDETERMINATE
STATIC_LIGACN             = CORE_TOPOLOGICAL_ONLY
MEMBRANE_MILIEU           = FUTURE_HYPOTHESIS
NEW_PHASE                 = DO_NOT_OPEN
LINE_PAUSE                = TRUE
```

**Aliases / legado (compatibilidad con cierres previos):** `ORTOSTERIC_THCV_DESIGN = PAUSED` · `CORE_TOPOLOGICAL_ONLY = CLOSED` · `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` · `DOCKING = STOP` · `COMPUTATION = PAUSED`.

Preservados sin reabrir: **Niveles A/B/C**, **`Q_membrana` = PARKED**, pregunta de reactivación `ligand+receptor+membrane → P(metastable states)` archivada, linaje **`cfb2a51` / `c2869b0` / `2a1193c`**.

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
# Freeze YAML — frontera definida y archivada (2026-08-21); honestidad epistemológica
STAGE: FRONTIER_DEFINED_AND_ARCHIVED
EMPIRICAL_FOUNDATION:
  MACRO_STATE_RECOGNITION: VALIDATED  # Phase G / 8GUR
  LOCAL_MICRO_NETWORK: STATE_DEPENDENT  # HU-308/HU-433
  STATIC_LIGACN_TOPOLOGY: CORE_TOPOLOGICAL_ONLY  # cfb2a51
  DATA_PROVENANCE_AUDIT: PARTIAL  # SI/endpoints registered; traj/MSM download not completed
THEORETICAL_MODEL:
  FRAMEWORK: TRIPARTITE_WORKING_HYPOTHESIS  # NOT demonstrated model
  NOTE: ligand × conformational ensemble × lipid bilayer; weights unresolved
  KEY_MODULATORS_CANDIDATE: [Allosteric Network, Cholesterol, Anionic Phospholipids]
PIPELINE_LOCKS:
  DOCKING_CAMPAIGNS: STOP
  DE_NOVO_GENERATION: STOP
  OPEN_ENDED_SEARCHES: STOP
  COMPUTATION_ACTIVE: NONE
RESEARCH_STATUS: FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY
# Flags exactos preservados (autoridad — no relajar)
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
# Detalle operativo
STATIC_BOTTLENECKS: SUPPORTED
FUNCTIONAL_Gi_ENRICHMENT: NOT_SUPPORTED
CB2_MINIMAL_GI_CORE: NOT_FOUND
DUAL_HUB_TEST: CLOSED
NEW_HUB_SEARCH: STOP
NEW_VARIABLES_IN_PIPELINE: NONE
CONTRACT_v1.0: ARCHIVED_HISTORICAL
THRESHOLD_MODIFICATION: STOP
MODO: LINE_PAUSE / READ_ONLY_DATA / DOCUMENTATION_ONLY
STATIC_GRAPH_ANALYSIS: CLOSED
DUAL_VALIDATION_HUBS: CLOSED
SINK_SET_T: EXTRACTED  # Arg131(3x50), Asp240(6x30), Ser303(8x47), Ser69(2x39)
CB1_COMPARISON: BLOCKED
DATA_PROVENANCE: PARTIAL  # SI/endpoints registered; traj/MSM download not completed (GPCRmd 1540 / Box = ENLACE_REGISTRADO; MOESM2 recovered; Sink T from Methods)
DATA_PROVENANCE_AUDIT: PARTIAL  # same honesty line — NOT fully RESOLVED for trajectories
TECHNICAL_SEARCH_TRAJ: STOP
ACTIVE_ACTION: LINE_PAUSE  # true pause — no compute
DUAL_TEST_COMMIT: cfb2a51  # preserve clean negative / topology-only result
ABC_HIERARCHY_COMMIT: c2869b0  # A/B/C + Q_membrana parked
FREEZE_COMMIT: 2a1193c  # reposo científico / frontera (pre-mapa)
Q_MEMBRANA: PARKED  # DO NOT RUN
NIVEL_A_CANONICAL: ACTIVE_BASELINE
NIVEL_B_CHOLESTEROL_LIPIDS: FUTURE_PRIORITY_HYPOTHESIS  # no active compute
NIVEL_C_SECONDARY_MODULATORS: ARCHIVED_NOT_JUSTIFIED
WORKING_HYPOTHESIS: LIGAND_x_LANDSCAPE_x_MEMBRANE  # weights unresolved; not a final tripartite model
REACTIVATION_QUESTION: ligand+receptor+membrane -> P(metastable states)  # archived; DO NOT RUN as docking score hunt
ARCHIVED_NEXT_CALCULATION: PARKED  # DO NOT RUN — see section below; no traj download, no MD, no analysis now
```

**Cortafuegos de gobernanza (formal):**

```
RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY
DE_NOVO_GENERATION = STOP
DOCKING_EXECUTION = STOP
COMPUTATION_ACTIVE = NONE
ORTHOSTERIC_DESIGN = PAUSED
MACRO_COORDINATE = VALIDATED_OUT_OF_SAMPLE
FUNCTIONAL_EFFICACY = INDETERMINATE
HU308_HU433_MICROSTATE = INDETERMINATE
STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY
MEMBRANE_MILIEU = FUTURE_HYPOTHESIS
NEW_PHASE = DO_NOT_OPEN
LINE_PAUSE = TRUE
NEW_VARIABLES_IN_PIPELINE = NONE
Q_MEMBRANA = PARKED
```

**Estado del repositorio (reposo científico):** `STAGE: FRONTIER_DEFINED_AND_ARCHIVED` — congelado en frontera epistemológica — **TRIPARTITE_WORKING_HYPOTHESIS** (no modelo demostrado); `DATA_PROVENANCE_AUDIT: PARTIAL`; anclas `cfb2a51` / `c2869b0` / `2a1193c`; variables nuevas en pipeline = **cero**.

**[OBSERVACIÓN_PROPIA]** Diseño químico / de_novo / docking / nueva búsqueda de hubs / **nueva fase** **STOP** (`NEW_PHASE = DO_NOT_OPEN`). `LINE_PAUSE = TRUE`. `COMPUTATION_ACTIVE = NONE`.  
**[INTERNAL_REANALYSIS]** Dual validation (`cfb2a51`) → **`CORE_TOPOLOGICAL_ONLY`**. Topología ≠ necesidad causal Gi. Prohibido: “switch”, “núcleo universal probado”, `CORE_FOUND`, `CB2_Gi_NETWORK_CANDIDATE`, “termodinamica CB2 resuelta”, “modelo tripartito final demostrado”, “GPCRmd traj / Box MSM fully recovered”.
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

### Pregunta aparcada (formal — DO NOT RUN)

**`Q_membrana`:** ¿Constituyen los hubs del eje TM7–H8 y base de TM2 propiedades intrínsecas del receptor o su conectividad está gobernada por microdominios de colesterol y lípidos aniónicos?

Si se reanuda más adelante: empezar por **Nivel B** (colesterol / composición lipídica), **no** por temperatura/oxidación/pH. Sin MD de colesterol, sin docking, sin de novo, sin nueva fase hasta decisión conjunta explícita.

**Cross-link:** informe hubs [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) (ancla `cfb2a51`).
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
2. **`Q_membrana`** (Nivel B futuro): hubs TM7–H8 / base TM2 — ¿intrínsecos o gobernados por microdominios de colesterol / lípidos aniónicos? Si se reanuda: empezar por colesterol/composición lipídica, **no** temperatura/oxidación/pH.

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
                 LINE_PAUSE = TRUE (pausa real; no compute)
                 RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY
                 NEW_PHASE = DO_NOT_OPEN
                 COMPUTATION_ACTIVE = NONE
                 NEW_VARIABLES_IN_PIPELINE = NONE
                 A/B/C firewall · Q_membrana PARKED
                 MEMBRANE_MILIEU = FUTURE_HYPOTHESIS
                 working hyp. (weights unresolved)
                 linaje: cfb2a51 → c2869b0
```

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
| ¿Núcleo mínimo Gi encontrado? | 🔴 **`CB2_MINIMAL_GI_CORE = NOT_FOUND`** |
| ¿Colesterol / lípidos aniónicos cambian farmacología CB2? | 🟢 **[LITERATURA_PRIMARIA]** Sí (MRI-2646 / basal / PS–CHS) — Yeliseev 2021 DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6); Kimura 2012 DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425); Vukoti 2012 DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290) — **Nivel B, no en pipeline** |
| ¿Hubs TM7–H8 / TM2 intrínsecos vs entorno lipídico? (`Q_membrana`) | ⏸ **PARKED** — **[HIPÓTESIS_ABIERTA]**; DO NOT RUN; si se reanuda → Nivel B primero |
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
| `DATA_PROVENANCE_AUDIT` | **PARTIAL** — SI/endpoints; traj/MSM **not** fully recovered |

---

## ARCHIVED_NEXT_CALCULATION — núcleo dinámico CB2→Gi (PI — PARKED / NOT NOW)

**Estado:** **`PARKED`**. Documentación de viabilidad y recomendación PI. **`COMPUTATION_ACTIVE = NONE`**. **`NEW_PHASE = DO_NOT_OPEN`**. **`RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY`**.  
**Prohibido ahora:** descargar trayectorias, correr MD, docking, de novo, análisis de red dinámica, push.

### Distinción: “calcularlo” ≠ inventar desde cero

Reconstruir / reanalizar un **núcleo dinámico CB2→Gi** a partir de **datos publicados** es técnicamente viable — **no** equivale a inventar energías absolutas ni moléculas *de novo*.

| Fuente | Escala / objeto | DOI |
|--------|-----------------|-----|
| **[LITERATURA_PRIMARIA]** Dutta & Shukla (2023) | ~700 μs MSM / VAMPnets; ~6 estados metaestables cada CB1/CB2 | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| **[LITERATURA_PRIMARIA]** Morales-Pastor et al. (2025) | WT CB2 ~2 μs acumulados; LigACN ortostérico→intracelular; mutagénesis / Gαi2 | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0) |

**Pregunta abierta concreta (archivada):** ¿cuál es el **conjunto mínimo dinámico de nodos** necesario para comunicación Gαi, con arquitectura CB1 distinta?

### Niveles de dificultad (solo registro)

| # | Nivel | Viabilidad |
|---|-------|------------|
| 1 | Reproducir lo publicado | Relativamente factible |
| 2 | Núcleo mínimo propio (borrado de nodos, caminos más cortos, centralidad dinámica, persistencia temporal, robustez) | Factible con cuidado |
| 3 | Causalidad funcional | Mucho más duro — requiere dinámica conjunta + mutagénesis / Gαi (datos Morales-Pastor existen) |

### Regla crítica (gobernanza)

**No** correr ~700 μs MD propios como primer paso. Si se descongela: **análisis a posteriori** de trayectorias originales **si** se recuperan (`DATA_PROVENANCE_AUDIT` sigue **PARTIAL**; GPCRmd 1540 / Box = `ENLACE_REGISTRADO`). MD nuevo **solo** si el análisis publicado **no** puede responder la pregunta.

### Membrana también calculable más tarde

Colesterol cambia farmacología CB2; MD con/sin ~40% colesterol (~2 μs) — **[LITERATURA_PRIMARIA]** Yeliseev et al., DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6). **`Q_membrana` / `MEMBRANE_MILIEU` = FUTURE** — no ahora.

### Tabla de viabilidad (registro)

| Objetivo | Semáforo |
|----------|----------|
| Reproducir dinámica publicada | 🟢 |
| Reconstruir red dinámica | 🟢 |
| Núcleo mínimo | 🟢 / 🟡 |
| vs CB1 | 🟡 |
| Vincular mutagénesis Gαi | 🟡 |
| Probar causalidad farmacológica | 🔴 — no solo cálculo |
| Colesterol + dinámica | 🟡 — más costoso |

### Cálculo NEXT recomendado SI se descongela (NOT NOW)

1. ¿Sobreviven los **seis hubs estáticos** cuando la red pasa a ser **dinámica**?
2. ¿Los nodos supervivientes quedan **más cercanos** a mutaciones que alteran Gαi2?

| Resultado | Lectura |
|-----------|---------|
| **Ambos sí** | Evidencia más fuerte para un **candidato de subred dinámica** (nombre: **nunca** “switch”; meta precisa = subred dinámica robusta reconocimiento de ligando → salida Gαi en CB2). `CB2_Gi_NETWORK_CANDIDATE` **solo** si dual criteria + revisión humana. |
| **No** | Confirma que **`CORE_TOPOLOGICAL_ONLY`** era propiedad del grafo agregado, no mecanismo dinámico — también es una respuesta clara. |

**Naming lock:** no “switch”; `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` hasta criterios duales post-revisión.

---

## Índice — síntesis consolidada (`docs/synthesis/`)

| Documento | Contenido |
|-----------|-----------|
| [`docs/synthesis/CB2_STRUCTURE_ATLAS.md`](docs/synthesis/CB2_STRUCTURE_ATLAS.md) | Atlas PDB: 5ZTY, 6PT0, 6KPF, 8GUS/UR/UQ/UT, 12IY/IZ/JA, 8X3L, 9U7L; Level-0; Phase F/G |
| [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) | Par enantiomérico; 8GUS experimental; Soethoudt/Hanuš; micronetwork INDETERMINATE; **contradicciones abiertas** |
| [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) | ACN/LigACN (Morales-Pastor 2025); MSM (Dutta & Shukla 2023); Trp258 no switch único; frontera MD |
| [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo dinámico (histórico); `CB2_MINIMAL_GI_CORE = NOT_FOUND`; cruzar topología×dinámica parked |
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

## Próximo paso — LINE_PAUSE (frontera epistemológica)

**[OBSERVACIÓN_PROPIA]**

1. **`RESEARCH_STATUS = FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY`.** Hipótesis de trabajo multivariable; **no** modelo tripartito demostrado; **no** termodinámica CB2 resuelta.
2. Trayectoria: THCV/ortostérico → Contract restrictivo → paisaje → Phase G → microestados → Phase H IND → LigACN estático → `CORE_TOPOLOGICAL_ONLY` → literatura + membrana → hipótesis multivariable → mapa de convergencia + `ARCHIVED_NEXT_CALCULATION` parked.
3. Explicitamente NO: switch único; hubs estáticos controlan Gαi2; `CB2_Gi_NETWORK_CANDIDATE`; TPSA ≡ periferia; lípido solo explica variabilidad; estrategia química usable lista; traj GPCRmd/Box “fully recovered”.
4. A/B/C preservada (`c2869b0`); `Q_membrana` parked; `MEMBRANE_MILIEU = FUTURE_HYPOTHESIS`.
5. Reactivación archivada: `ligand+receptor+membrane → P(metastable states)` — medir cambios de distribución, no “mejor pose”.
6. **`ARCHIVED_NEXT_CALCULATION = PARKED`** — ver sección arriba; **no** ejecutar.
7. **`LINE_PAUSE = TRUE`.** **`NEW_PHASE = DO_NOT_OPEN`.** **`COMPUTATION_ACTIVE = NONE`.** Sin docking, de novo, push, MD, ni download de traj.

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`) — hipótesis de trabajo + flags + mapa de convergencia + `ARCHIVED_NEXT_CALCULATION` + NO demostrado
2. [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) — ancla `cfb2a51`
3. [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md)
4. [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) — Morales-Pastor / Dutta–Shukla / Trp258
5. [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) — Smoum / Ganzoni; contradicciones abiertas
6. [`results/network_core/provenance_recovery_log.md`](results/network_core/provenance_recovery_log.md) — PARTIAL; traj = ENLACE_REGISTRADO

---

*Fin RESEARCH_STATE.md. 2026-08-21 — STAGE FRONTIER_DEFINED_AND_ARCHIVED; FROZEN_AT_EPISTEMOLOGICAL_BOUNDARY; TRIPARTITE_WORKING_HYPOTHESIS (weights unresolved; NOT demonstrated model); DATA_PROVENANCE_AUDIT PARTIAL (traj not recovered); CORE_TOPOLOGICAL_ONLY; ARCHIVED_NEXT_CALCULATION PARKED; LINE_PAUSE=TRUE; NEW_PHASE=DO_NOT_OPEN; COMPUTATION_ACTIVE=NONE; linaje cfb2a51 / c2869b0 / 2a1193c; documentation only — no compute / no MD / no nueva fase.*
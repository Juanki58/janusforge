# RESEARCH STATE — Janusforge CB₂ (congelación analítica)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Ancla dual-test (preservar):** `cfb2a51` — resultado limpio negativo / topología-only (no reescribir ni re-correr)  
**Tipo:** PI closure — línea hubs **`CORE_TOPOLOGICAL_ONLY`** + **pausa real** (`LINE_PAUSE = TRUE`) + cortafuegos jerárquico A/B/C (docs only)  
**Bitácora extendida:** [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md)

### Veredicto PI (LOCKED)

**`CORE_TOPOLOGICAL_ONLY`** — no `CB2_Gi_NETWORK_CANDIDATE`, no “switch”.

Lectura llana: los seis hubs son cuellos de botella topológicos reales en el mapa estático; el enriquecimiento celular PrefCoup_Gαi2 para ese *set* **no** está soportado. Carreteras importantes ≠ controladores demostrados de la decisión funcional que importa.

**Arquitectura física ≠ salida funcional.**

**Framing (no experimento nuevo):** no “un switch CB2”, sino **un paisaje energético de CB2 cuyo comportamiento emerge de proteína + ligando + membrana**. Evitar dispersión: no colesterol→temperatura→oxidación→pH→fosforilación→todo.

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
# PI closure — línea hubs (2026-08-21)
CORE_TOPOLOGICAL_ONLY: LOCKED
STATIC_BOTTLENECKS: SUPPORTED
FUNCTIONAL_Gi_ENRICHMENT: NOT_SUPPORTED
CB2_Gi_NETWORK_CANDIDATE: NOT_ESTABLISHED
CB2_MINIMAL_GI_CORE: NOT_FOUND
DUAL_HUB_TEST: CLOSED
LINE_PAUSE: TRUE
COMPUTATION: PAUSED
DE_NOVO: STOP
DOCKING: STOP
NEW_HUB_SEARCH: STOP
NEW_VARIABLES_IN_PIPELINE: NONE
# aliases / legado
DE_NOVO_GENERATION: STOP
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
NEW_SEARCH: STOP
CONTRACT_v1.0: ARCHIVED_HISTORICAL
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
MODO: LINE_PAUSE / READ_ONLY_DATA
STATIC_GRAPH_ANALYSIS: CLOSED
DUAL_VALIDATION_HUBS: CLOSED
SINK_SET_T: EXTRACTED  # Arg131(3x50), Asp240(6x30), Ser303(8x47), Ser69(2x39)
CB1_COMPARISON: BLOCKED
DATA_PROVENANCE: PARTIAL  # SI/SD1–3 local; traj/Box = ENLACE_REGISTRADO
TECHNICAL_SEARCH_TRAJ: STOP
ACTIVE_ACTION: LINE_PAUSE  # true pause — no compute
RESEARCH_STATUS: CORE_TOPOLOGICAL_ONLY__LINE_PAUSE
DUAL_TEST_COMMIT: cfb2a51  # preserve clean negative / topology-only result
Q_MEMBRANA: PARKED  # DO NOT RUN
NIVEL_B_CHOLESTEROL_LIPIDS: FUTURE_PRIORITY_HYPOTHESIS  # no active compute
NIVEL_C_SECONDARY_MODULATORS: ARCHIVED_NOT_JUSTIFIED
```

**Cortafuegos de gobernanza (formal):**

```
CORE_TOPOLOGICAL_ONLY locked
STATIC_BOTTLENECKS = SUPPORTED
FUNCTIONAL_Gi_ENRICHMENT = NOT_SUPPORTED
CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED
LINE_PAUSE = TRUE
NEW_VARIABLES_IN_PIPELINE = NONE
DE_NOVO / DOCKING = STOP
COMPUTATION = PAUSED
```

**Estado del repositorio (reposo):** resultado consolidado **`CORE_TOPOLOGICAL_ONLY`** (ancla `cfb2a51`); variables añadidas al pipeline = **cero**; equilibrio metodológico = claro lo demostrado, frontera matemática precisa de lo que el modelo actual no alcanza, jerarquía A/B/C para no diluir el foco.

**[OBSERVACIÓN_PROPIA]** Diseño químico / de_novo / docking / nueva búsqueda de hubs / Phase I **STOP**. `LINE_PAUSE = TRUE`.  
**[INTERNAL_REANALYSIS]** Dual validation (`cfb2a51`) → **`CORE_TOPOLOGICAL_ONLY`**. Topología ≠ necesidad causal Gi. Prohibido: “switch”, “núcleo universal probado”, `CORE_FOUND`, `CB2_Gi_NETWORK_CANDIDATE`.
---

## Jerarquía ambiental A/B/C (cortafuegos PI — DOCUMENTATION ONLY)

**No se abre fase. No se añade variable al pipeline.** La frontera cerrada sigue siendo **`CORE_TOPOLOGICAL_ONLY`**. `LINE_PAUSE = TRUE` preservado.

| Nivel | Alcance | Evidencia | Estado en el proyecto |
|-------|---------|-----------|------------------------|
| **Nivel A: Núcleo Canónico** | Receptor + Ligando + Conformación | PDB structures, deep mutagenesis, LigACN WT | **Activo / Línea Base** (`CORE_TOPOLOGICAL_ONLY`) |
| **Nivel B: Entorno Directo** | Colesterol + composición lipídica (PS / aniónicos) | Modulación de actividad basal y cambio de clase farmacológica (p.ej. MRI-2646; efecto alostérico hacia regiones intracelulares / reclutamiento G; interfaz H8) | **Hipótesis Prioritaria Futura** (sin computación activa) |
| **Nivel C: Moduladores Secundarios** | Temperatura, Redox/Oxidación, pH local | Efectos bifísicos generales de estabilidad/cinética | **Archivado / No Justificado** (evitar dilución) |

### Lectura por nivel

**Nivel A — mandatory for current model.** Receptor + ligando + conformación son suficientes para el modelo actual (evidencia PDB / mutagénesis / LigACN). **[OBSERVACIÓN_PROPIA]** / **[INTERNAL_REANALYSIS]** — línea base locked.

**Nivel B — environmental with direct CB2 evidence.** Puede entrar en un *modelo futuro* porque experimentos muestran que la farmacología puede cambiar; **no** está en el pipeline ahora.

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
                 NEW_VARIABLES_IN_PIPELINE = NONE
                 A/B/C firewall · Q_membrana PARKED
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

## Congelación analítica

| Ámbito | Estado |
|--------|--------|
| Retrospectivo A–E (`results/docking/`) | **CLOSED_AND_ARCHIVED** — read-only |
| Calibración multistate | **CLOSED** (2026-08-19) |
| Contract v1.0 | **ARCHIVED_HISTORICAL** — testigo 6PT0, no predictor funcional |
| de_novo / threshold / docking / diseño ortostérico | **STOP** / **PAUSED** |
| Fase I | **NO ABIERTA** — no usar ese nombre para el reanálisis |
| SMRF / 0Q.1 literatura | Documental; no reabre compute (ver bitácora extendida) |
| Proveniencia de datos | **PARTIAL** — SD1–3 + MOESM2 + Sink T local; traj/Box ENLACE_REGISTRADO |
| Topología estática LigACN | **CLOSED** — `STATIC_BOTTLENECKS = SUPPORTED` |
| Dual hub test (A/B) | **CLOSED** — ancla `cfb2a51`; veredicto **`CORE_TOPOLOGICAL_ONLY`** |
| Función PrefCoup del set de 6 hubs | **NOT_SUPPORTED** — hipótesis núcleo funcional Gi bias **eliminada** |
| `CB2_Gi_NETWORK_CANDIDATE` | **NOT_ESTABLISHED** |
| `CB2_MINIMAL_GI_CORE` | **NOT_FOUND** |
| Línea hubs | **`LINE_PAUSE = TRUE`** — pausa real; cruzar topología×dinámica parked |
| Variables nuevas en pipeline | **NONE** |
| Jerarquía A/B/C | **Documentada** — A = línea base; B = hipótesis prioritaria futura; C = archivado |
| `Q_membrana` | **PARKED** (DO NOT RUN) |

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

## Próximo paso — LINE_PAUSE (pausa real)

**[OBSERVACIÓN_PROPIA]**

1. Veredicto locked: **`CORE_TOPOLOGICAL_ONLY`** (ancla `cfb2a51`). Arquitectura física ≠ salida funcional.
2. Cuatro niveles epistémicos: (1) macro 🟢 (2) micro-red 🟡 (3) topología estática 🟢 (4) función Gαi2 🔴.
3. Cortafuegos ambiental A/B/C: A = núcleo canónico activo; B = colesterol/lípidos (futuro, sin compute); C = archivado.
4. Hipótesis “6 hubs = núcleo funcional del sesgo Gαi2” **eliminada**; no sobreclaim “la red no tiene relación con Gαi2”.
5. Parked: topología × dinámica; **`Q_membrana`**. Frontera del modelo actual = `CORE_TOPOLOGICAL_ONLY`.
6. **`LINE_PAUSE = TRUE`.** `NEW_VARIABLES_IN_PIPELINE = NONE`. Sin docking, de novo, hub hunting, traj recovery, MD colesterol, push, ni compute.

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`) — veredicto PI + gobernanza + A/B/C + `Q_membrana`
2. [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md) — ancla `cfb2a51`
3. [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md)
4. [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md)
5. [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) — contradicciones abiertas

---

*Fin RESEARCH_STATE.md. 2026-08-21 — PI closure: CORE_TOPOLOGICAL_ONLY; LINE_PAUSE=TRUE; A/B/C firewall; Q_membrana PARKED; cfb2a51 preservado; NEW_VARIABLES_IN_PIPELINE=NONE; no compute.*

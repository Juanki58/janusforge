# CB2 — capas de interacción dinámica (mapa PI)

**Fecha:** 2026-08-21  
**Tipo:** **DOCUMENTATION ONLY** — consolidación conceptual; **no** compute, **no** P5/P2 execution, **no** docking, **no** de novo  
**Autoridad de freeze:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) (`RESEARCH_STATUS = POST_P1_BOUNDARY_FROZEN`)  
**Contrato P1–P6:** [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md)

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto |
| **[INTERNAL_REANALYSIS]** | Reanálisis sobre objetos públicos recuperados |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada — DOI / PMID / PDB verificados aquí |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |
| **[SUPPORTED_INTERPRETATION]** | Lectura de campo coherente con evidencia citada, no ley cerrada |

---

## 1. Propósito

Registrar el **mapa multicapa** de interacciones dinámicas de CB2 como objeto de lectura PI — **sin** modelar todas las capas a la vez (cortafuegos metodológico / dispersión).

**Estado operativo:** `COMPUTATION = PAUSED` · `P2 = BLOCKED` (MSM) · `P5 = HYPOTHESIS_READY` (no execution).

---

## 2. Registro de capas

| Capa | Qué cambia | Evidencia en CB2 | Etiqueta |
|------|------------|------------------|----------|
| **Ligando ↔ microswitch** | Contactos locales Trp258^6.48, Ser285^7.39, vecinos | **Strong** — continuo / protean vía Trp258 | **[LITERATURA_PRIMARIA]** Ganzoni 2026, DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B). **[OBSERVACIÓN_PROPIA]** micronetwork **INDETERMINATE** (6PT0/6KPF) |
| **Microswitch ↔ hélices** | TM5 / TM6 / TM7; motivos DRY, NPxxY, CWxP, PIF | **Strong** | **[LITERATURA_PRIMARIA]** Morales-Pastor 2025, DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0), PMID [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/); Dutta & Shukla 2023, DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) (TM5/6/7 en transición) |
| **Red interna** | Comunicación entre regiones distantes (LigACN / ACN) | **Strong** | **[LITERATURA_PRIMARIA]** Morales-Pastor 2025 (mismo DOI/PMID). **[INTERNAL_REANALYSIS]** estático `CORE_TOPOLOGICAL_ONLY`; P1 `SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT` |
| **Red ↔ efector** | Acoplamiento Gαi2 / β-arrestin | Experimental + MD (lit.) | **[LITERATURA_PRIMARIA]** Morales-Pastor 2025 — perfilado mutantes Gαi2 / β-arr1. **[OBSERVACIÓN_PROPIA]** Test B PrefCoup **NOT_SUPPORTED** para el *set* de seis hubs |
| **Receptor ↔ membrana** | Colesterol, PS / lípidos aniónicos | Experimental + MD (lit.) | **[LITERATURA_PRIMARIA]** Yeliseev 2021 MRI-2646, DOI [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6), PMID [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/); Kimura 2012 DOI [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425); Vukoti 2012 DOI [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290). Nivel B = `FUTURE_HYPOTHESIS` |
| **Receptor ↔ otro GPCR** | Heteromerización; interfaces TM6 / TM1–TM7 | Experimental + MD | **[LITERATURA_PRIMARIA]** Llinàs del Torrent *et al.* 2024 (A2A–CB2; TM6 ↔ TM1/7), DOI [10.1111/bph.16502](https://doi.org/10.1111/bph.16502), PMID [39044481](https://pubmed.ncbi.nlm.nih.gov/39044481/). **[LITERATURA_PRIMARIA]** CBD sesga función del heterómero A2A–CB2 (2025), DOI [10.1016/j.bcp.2025.117280](https://doi.org/10.1016/j.bcp.2025.117280). **Nivel-C-adjacent / futura** — **no** en pipeline |
| **Iones / agua ↔ receptor** | Na+, red de agua, egress Na | **Strong en class A GPCR**; **parcial en CB2** | **[LITERATURA_PRIMARIA]** Morales-Pastor 2025 incluye **sitio de unión de sodio** entre motivos ACN CB2 (mismo DOI). **No** overclaim: dinámica detallada Na egress / water network class-A **≠** demostrada aquí como mecanismo CB2-específico cerrado — **[HIPÓTESIS_ABIERTA]** / tema class-A a anclar aparte |
| **Tiempo** | Estados metaestables y transiciones | MSM / MD | **[LITERATURA_PRIMARIA]** Dutta & Shukla 2023 (mismo DOI). **P2 BLOCKED** hasta MSM recuperable |

---

## 3. Framings clave (lectura obligatoria)

### 3.1 Ligando → microswitch (continuo / protean)

**[LITERATURA_PRIMARIA]** El ligando puede **empujar** el microswitch (Trp258 importa) en un **continuo** de eficacia — **no** es un interruptor binario suficiente hacia Gαi2 (Ganzoni 2026).  
**[LITERATURA_PRIMARIA]** LigACN **no** se reduce a Trp258 (Morales-Pastor 2025).

### 3.2 Cadena de transmisión (no colapsar)

```
ligando → microswitch → red de comunicación → TM5/6/7 → interfaz IC → Gαi2 / β-arr
```

**Prohibido como modelo operativo:** `ligando → Trp258 → Gαi2` (salta red + hélices + interfaz).

### 3.3 Tiempo / breathing y lectura de P1

**[SUPPORTED_INTERPRETATION]** Que hubs estáticos **no** sobrevivan como esqueleto dinámico persistente es **esperable** si se promedian muchas configuraciones / estados.  
**[INTERNAL_REANALYSIS]** Eso **soporta** la lectura estricta de P1 (`P1_NOT_SUPPORTED` / `SIX_HUBS_DYNAMIC_SKELETON = REFUTED_UNDER_GPCRMD_WT`) **sin** excusa post hoc de membrana (`POST_HOC_EXCUSES = FORBIDDEN`).

### 3.4 Membrana — pregunta P5 refinada

**No (ya hay evidencia de actividad):** “¿El colesterol cambia la actividad de CB2?” — **[LITERATURA_PRIMARIA]** Yeliseev 2021 et al.  
**Sí (P5 conceptual):** “¿El colesterol cambia las **rutas dinámicas** que CB2 usa para transitar entre estados?”

`P5 = HYPOTHESIS_READY` · `P5_EXECUTION = BLOCKED_PENDING_DECISION` · independiente de P1.

### 3.5 Heterómero — expansión de “interacción dinámica”

CB2 puede recibir **perturbación alostérica** que **no** proviene de un ligando CB2 (protomer A2A / ligandos del heterómero).  
**Registro:** Nivel-C-adjacent / capa futura — **no** pipeline ahora (`NEW_VARIABLES_IN_PIPELINE = NONE`).

---

## 4. Diagrama de sistema (conceptual)

```
MEMBRANA (colesterol / PS / lípidos)
   + ligando ortostérico / alostérico
   + otro GPCR (heterómero; futura)
            │
            ▼
     CB2 conformacional
            │
            ├── agua / Na+ (parcial CB2; class-A fuerte)
            └── microswitches (Trp258, Ser285, …)
                    │
                    ▼
            red alostérica (comunicación)
                    │
                    ▼
               TM5 / TM6 / TM7
                    │
                    ▼
            Gαi2  /  β-arrestin
                    │
                    ▼
              cambios en el tiempo
         (metaestables / transiciones)
```

Las flechas son **organización de lectura**, no un modelo termodinámico cuantitativo cerrado (`TRIPARTITE_WORKING_HYPOTHESIS` — pesos unresolved).

---

## 5. Cortafuegos metodológico

**No** modelar todas las capas simultáneamente (dispersión de pregunta y de compute).

| Permitido ahora | Prohibido ahora |
|-----------------|-----------------|
| Consolidar mapa + framings en docs | P2/P3/P4/P5 compute |
| Refinar pregunta P2 → **transiciones** | Inventar estados MSM sin depósito |
| Mantener gates P1–P6 | Docking / de novo / MD nuevo |
| Heterómero como capa futura | Añadir heterómero al pipeline |

Los gates del roadmap **siguen válidos**.

---

## 6. Giro del objeto de investigación (evolución de P2 — no ejecución)

Tras el fallo de P1 del **esqueleto permanente de seis hubs**:

| Antes (objeto) | Ahora (objeto registrado) |
|----------------|---------------------------|
| **Hubs** — “¿qué residuo está siempre en el centro?” | **Transiciones** — “¿qué interacciones cambian de forma sistemática al pasar de un estado a otro?” |

**Pregunta natural de P2 (reformulación):**  
Mapear **dinámica de rutas entre estados** — conexiones que **aparecen, desaparecen o cambian de fuerza** durante una transición funcional — **no** buscar un core permanente.

**Después (más tarde):** qué parte controla el **ligando** vs la **membrana** (enlace conceptual a P5 refinado).

**Estado:** `P2 = BLOCKED` pending MSM (Dutta–Shukla). Esto es **evolución del objeto**, no apertura de fase ni cómputo.

---

## 7. Cross-links

| Documento | Rol |
|-----------|-----|
| [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Freeze / flags |
| [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md) | Gates P1–P6 + giro P2 |
| [`CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md`](CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md) | Encuesta bibliográfica independiente (soporte / cualificación / contradicción) |
| [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) | ACN / Trp258 / MSM |
| [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) | Continuo / protean / contradicciones abiertas |
| [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) | Pre-registro técnico (aún hubs-framed; objeto P2 evoluciona arriba) |

---

*Fin CB2_DYNAMIC_INTERACTION_LAYERS.md — mapa multicapa + giro a transiciones; COMPUTATION=PAUSED; sin P5/P2 compute.*

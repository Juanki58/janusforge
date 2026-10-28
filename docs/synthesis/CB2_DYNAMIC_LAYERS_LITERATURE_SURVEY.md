# CB2 — encuesta bibliográfica de capas dinámicas

**Fecha:** 2026-08-21  
**Tipo:** **DOCUMENTATION ONLY** — encuesta independiente de literatura primaria; **no** compute, **no** P2/P5, **no** docking/MD  
**Ámbito:** soporte / cualificación / contradicción del mapa multicapa en [`CB2_DYNAMIC_INTERACTION_LAYERS.md`](CB2_DYNAMIC_INTERACTION_LAYERS.md) tras `P1_NOT_SUPPORTED`  
**Freeze:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) (`COMPUTATION = PAUSED`)

### Leyenda epistemológica (obligatoria)

| Tag | Uso en este documento |
|-----|------------------------|
| **[LITERATURA_PRIMARIA]** | Afirmación anclada a paper peer-reviewed con DOI/PMID (y PDB si estructural) verificados en esta encuesta |
| **[EXTRAPOLACIÓN_CLASE_A]** | Evidencia fuerte en class A / otros GPCR; **no** demostrada como mecanismo CB2-específico cerrado |
| **[HIPÓTESIS_ABIERTA]** | Lectura coherente pero no demostrada; no armonizar post hoc con P1 |

---

## 1. Executive summary

| Pregunta del framing | Veredicto de literatura | Tag dominante |
|----------------------|-------------------------|---------------|
| Ligando → continuo Trp258^6.48 / protean | **Bien soportado** en CB2 (Ganzoni 2026; Kosar 2024) | **[LITERATURA_PRIMARIA]** |
| Red alostérica distribuida LigACN / PrefCoup Gαi2 | **Bien soportado** (Morales-Pastor 2025) | **[LITERATURA_PRIMARIA]** |
| Estados metaestables; promedio estático ≠ mecanismo | **Bien soportado** en CB1/CB2 MSM (Dutta–Shukla 2023); breathing class-A (Aranda-García 2025) | **[LITERATURA_PRIMARIA]** + **[EXTRAPOLACIÓN_CLASE_A]** |
| Colesterol / lípidos modulando farmacología CB2 e IC | **Bien soportado** (Yeliseev 2021; Kimura 2012; Vukoti 2012) | **[LITERATURA_PRIMARIA]** |
| Heterómero A2A–CB2 → TM6 / acoplamiento G | **Bien soportado** como capa futura (Llinàs 2024; Rivas-Santisteban 2025) | **[LITERATURA_PRIMARIA]** |
| Na+/agua class A vs CB2 | **Parcial en CB2**; fuerte en class A | **[LITERATURA_PRIMARIA]** (parcial) + **[EXTRAPOLACIÓN_CLASE_A]** |
| Estudiar **transiciones / contactos cambiantes** vs hubs permanentes | **Coherente** con MSM + surveys dinámicos; **no** prueba el veredicto P1 del repo | **[SUPPORTED_INTERPRETATION]** vía lit. |

**Bottom line:** el mapa multicapa del proyecto está **alineado** con literatura primaria CB2 en capas 1–5 y parcialmente en 6–7. Lo que la literatura **no** otorga es: (i) causalidad de los seis hubs estáticos del repo; (ii) que colesterol “rescate” P1; (iii) un mecanismo Na+/agua CB2 cerrado equivalente al class-A canónico; (iv) que `P1_NOT_SUPPORTED` implique red “plenamente distribuida” como ley biológica.

---

## 2. Tabla capa-por-capa (evidencia + citas)

| Capa (mapa PI) | Qué dice la literatura | Soporte | Contradicciones / matices | Tag |
|----------------|------------------------|---------|---------------------------|-----|
| **1. Ligando ↔ microswitch** | Modificaciones en una posición del scaffold HU-308 afinan la interacción con Trp258^6.48 y producen un **continuo** de eficacia (agonismo pleno → inverso parcial); ligandos de baja eficacia muestran **comportamiento protean** / assay-dependent (Ganzoni et al., *Chem. Sci.* 2026). Trabajo previo del mismo linaje: inverso-agonismo vía constricción del toggle (Kosar et al., *ACS Cent. Sci.* 2024). | Strong CB2 | **No** implica `ligando → Trp258 → Gαi2` como cadena suficiente; Morales-Pastor muestra múltiples triggers hacia PrefCoup Gαi2. Micronetwork propia 6PT0/6KPF = INDETERMINATE (fuera de esta encuesta). | **[LITERATURA_PRIMARIA]** |
| **2. Microswitch ↔ hélices** | MSM CB1/CB2 (~700 μs): activación vía motivos / TM5–TM6–TM7 y estados intermedios I1–I4 (Dutta & Shukla 2023). LigACN HU-210 incluye DRY, CWxP-región, NPxxY (Morales-Pastor 2025). | Strong CB2 | Dutta–Shukla enfatiza **selectividad de subtipo** y volumen de pocket; no es un mapa de “hubs permanentes” del repo. | **[LITERATURA_PRIMARIA]** |
| **3. Red interna (LigACN / ACN)** | ACN por frecuencias de contacto (H-bond, hidrofóbico, agua-mediado); LigACN = 100 shortest paths ortostérico→IC; mutantes PrefCoup Gαi2 enriquecidos cerca de nodos de alta transmisión / conectividad; **múltiples mecanismos** convergen al mismo sesgo (Morales-Pastor 2025). | Strong CB2 | LigACN es red de **contactos ligand-stabilized** sobre MD WT, no esqueleto de seis hubs del análisis estático del proyecto. Test B PrefCoup del repo = observación propia, no refutada ni confirmada por lit. como set de seis. | **[LITERATURA_PRIMARIA]** |
| **4. Red ↔ efector** | Mutagénesis profunda (~360) + profiling Gαi2 / β-arr1; clusters PrefCoup Gαi2 modulan DRY, sitio Na, CWxP, NPxxY de formas distintas (Morales-Pastor 2025). | Strong CB2 | Sesgo depende de agonista / tipo de mutación — los autores advierten que **no** hay un mecanismo universal único de bias. | **[LITERATURA_PRIMARIA]** |
| **5. Receptor ↔ membrana** | Colesterol ↑ actividad basal CB2 y **reclasifica** MRI-2646 (agonista parcial sin chol → antagonista/inversor parcial con chol); MD sugiere efecto alostérico en regiones IC / reclutamiento G (Yeliseev et al. 2021). PS/CHS aniónicos ↑ activación G hasta ~50 mol% (Kimura 2012); PS/CHS estabilizan fold funcional (Vukoti 2012). | Strong CB2 (farmacología / reconstitución) | **No** demuestra que colesterol cambie las *rutas dinámicas entre estados* (pregunta P5 refinada = **[HIPÓTESIS_ABIERTA]**). Kimura: no correlación con orden de cadenas HC. | **[LITERATURA_PRIMARIA]**; P5 routes = **[HIPÓTESIS_ABIERTA]** |
| **6. Receptor ↔ otro GPCR** | Heterómero A2A–CB2: apo/agonista-A2A bloquea señalización CB2 vía interfaz **TM6** (impide opening IC para G); antagonista A2A desplaza a interfaz **TM1/7** y facilita CB2 (Llinàs del Torrent 2024). CBD sesga el heterómero desacoplando β-arr sin romper el complejo (Rivas-Santisteban 2025). | Strong experimental + MD | Capa **futura / Nivel-C-adjacent**; no entra al pipeline actual. | **[LITERATURA_PRIMARIA]** |
| **7. Iones / agua** | Class A: pocket Na+ hidratado, colapso en activación (Katritch 2014 review). CB1/CB2: rutas de entrada Na distintas; sitio secundario en CB1 **ausente en CB2** (Dutta et al. 2022). Morales-Pastor: N291^7.45 / S292^7.46 del sitio Na estánan en LigACN; mutación directa de esos motivos limita expresión. | Parcial CB2 | Dinámica detallada de egress Na / water network class-A **≠** mecanismo CB2 cerrado aquí. | CB2 parcial **[LITERATURA_PRIMARIA]**; egress/water class-A **[EXTRAPOLACIÓN_CLASE_A]** |
| **8. Tiempo / metaestables** | Seis estados metaestables CB1 y CB2; docking afinidad estado-dependiente (Dutta–Shukla 2023). Survey MD a gran escala: “breathing” IC nano–μs; sitios alostéricos a menudo cerrados sin modulador; inserciones lipídicas como marcadores (Aranda-García et al. 2025; coautor Morales-Pastor). Reviews: dinámicas / bias / alosterismo (Conflitti 2025; BPH 2024 dynamics). | Strong CB + class A | Breathing/survey = **[EXTRAPOLACIÓN_CLASE_A]** si se aplica como ley a CB2 sin traj propia estratificada por estado. | **[LITERATURA_PRIMARIA]** (CB MSM) + **[EXTRAPOLACIÓN_CLASE_A]** (GPCRome) |

---

## 3. Qué es consistente con el hallazgo P1 (`P1_NOT_SUPPORTED`)

Lectura estricta del repo: los **seis hubs estáticos no forman un esqueleto dinámico persistente** bajo GPCRmd/1540 WT — **no** “la red no existe”, **no** “causalidad biológica falsa”.

| Afirmación | Consistencia con lit. | Tag |
|------------|----------------------|-----|
| Un promedio sobre muchas configuraciones puede **borrar** contactos estado-específicos | Coherente con MSM de estados metaestables (Dutta–Shukla 2023) y con “breathing” / plasticidad de sitios (Aranda-García 2025) | **[SUPPORTED_INTERPRETATION]** |
| Comunicación alostérica CB2 es **distribuida** / multi-trigger, no un switch único | Directamente Morales-Pastor 2025 (múltiples mecanismos → mismo PrefCoup Gαi2) | **[LITERATURA_PRIMARIA]** |
| Trp258 es entrada potente pero **insuficiente** como modelo operativo `→ Gαi2` | Ganzoni 2026 (continuo en toggle) **y** Morales-Pastor (LigACN no reducible a un residuo) — **tensión productiva, no contradicción lógica** | **[LITERATURA_PRIMARIA]** |
| Objeto de estudio debería migrar a **transiciones / contactos que cambian** | Coherente con MSM, path analysis de contactos, y reviews de dinámica GPCR 2024–2025 | **[SUPPORTED_INTERPRETATION]** |
| Membrana puede modular farmacología **sin** servir de excusa post hoc de P1 | Yeliseev/Kimura establecen modulación lipídica **independiente**; no predicen el resultado de hubs dinámicos del repo | **[LITERATURA_PRIMARIA]** (modulación) + gobernanza propia (`POST_HOC_EXCUSES = FORBIDDEN`) |

---

## 4. Qué **aún NO** sigue de la literatura

1. **Que los seis hubs topológicos estáticos del repo deban ser hubs dinámicos persistentes** — la lit. no define ese set; LigACN es otra construcción (shortest paths / transmisión).  
2. **Que `P1_NOT_SUPPORTED` implique “red plenamente distribuida” como conclusión biológica** — opciones A–D del estado siguen abiertas; lit. soporta *existencia* de ACN distribuida, no el veredicto experimental del pipeline.  
3. **Que colesterol cambie las rutas dinámicas entre metaestables (P5 refinada)** — lit. muestra cambio de **clasificación farmacológica / basal / IC allosterism** (Yeliseev), no un mapa de rutas de transición colesterol-dependiente.  
4. **Mecanismo Na+/agua CB2 equivalente al canónico class-A** — hay sitio Na en LigACN y MD de binding CB1≠CB2; **no** hay aquí demostración cerrada de egress + water-wire como motor CB2.  
5. **Heterómero como parte del mecanismo ortostérico monómero** — lit. lo establece como capa distinta; el mapa PI correctamente lo marca futura.  
6. **Que estudio de transiciones “explique” o “rescate” P1** — evolucionar el objeto P2 es metodológicamente coherente; **no** es re-interpretación post hoc del fallo de esqueleto permanente.

---

## 5. Conflictos abiertos (no armonizar)

| Tensión | Polos | Estado |
|--------|-------|--------|
| **Toggle vs red** | Ganzoni/Kosar: Trp258 como palanca de eficacia continua | Morales-Pastor: mismo motif CWxP es *uno* de varios clusters PrefCoup; múltiples entradas | **Ambos true a distinto nivel** — no colapsar a switch único ni a “Trp258 irrelevante” |
| **Colesterol y agonista pleno** | Yeliseev 2021: colesterol reclasifica MRI-2646 y ↑ basal | Trabajos previos del mismo grupo: colesterol **no** afectó activación por CP-55,940 (citado en Yeliseev) | **Ligando-dependiente** — no generalizar “colesterol siempre cambia efficacy” |
| **Aniónicos vs colesterol** | Kimura: activación G correlaciona con potencial de superficie aniónico, **no** con orden HC de chol/CHS | Yeliseev: chol en bilayers definidas sí ↑ basal | Mecanismos **distintos** (carga vs packing/allosterismo IC) — no fusionar |
| **CB2 Na vs CB1 Na** | Dutta 2022: sitio secundario CB1 ausente en CB2; rutas de entrada distintas | Katritch 2014: canónico class A | CB2 **no** es copia del narrative class-A completo |
| **MSM docking en Dutta–Shukla** | Usa docking sobre metaestables para selectividad | Gobernanza del repo: docking ≠ función / P(score) prohibido como proxy de mecanismo | Usar MSM para **estados/transiciones**; no reabrir hunt de scores |

---

## 6. Bibliografía corta (DOI / PMID verificados)

### Primaria CB2 (núcleo del framing)

| # | Cita | DOI | PMID | Relevancia en una línea |
|---|------|-----|------|-------------------------|
| 1 | Morales-Pastor et al., *Nat. Commun.* 2025 | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0) | [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/) | LigACN/ACN distribuida; PrefCoup Gαi2; multi-trigger; sitio Na en red |
| 2 | Ganzoni et al., *Chem. Sci.* 2026 | [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B) | *(no indexado PMID al momento de la encuesta; DOI RSC verificado)* | Continuo de eficacia vía Trp258^6.48; protean/assay-dependent |
| 3 | Kosar et al., *ACS Cent. Sci.* 2024 | [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461) | *(PMC11117691; PMID vía PMC)* | Inverso-agonistas HU-308 restringen toggle Trp258 |
| 4 | Dutta & Shukla, *Commun. Biol.* 2023 | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) | [37147497](https://pubmed.ncbi.nlm.nih.gov/37147497/) | MSM ~700 μs; metaestables CB1/CB2; promedio ≠ camino de activación |
| 5 | Yeliseev et al., *Sci. Rep.* 2021 | [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6) | [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/) | Colesterol modula basal y reclasifica MRI-2646; MD → IC/G |
| 6 | Kimura et al., *J. Biol. Chem.* 2012 | [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425) | [22134924](https://pubmed.ncbi.nlm.nih.gov/22134924/) | PS/CHS aniónicos regulan activación G de CB2 reconstituido |
| 7 | Vukoti et al., *PLoS ONE* 2012 | [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290) | [23056277](https://pubmed.ncbi.nlm.nih.gov/23056277/) | PS/CHS estabilizan CB2 funcional en micelas/bilayers |
| 8 | Llinàs del Torrent et al., *Br. J. Pharmacol.* 2024 | [10.1111/bph.16502](https://doi.org/10.1111/bph.16502) | [39044481](https://pubmed.ncbi.nlm.nih.gov/39044481/) | Heterómero A2A–CB2: interfaz TM6 vs TM1/7 controla opening G |
| 9 | Rivas-Santisteban et al., *Biochem. Pharmacol.* 2025 | [10.1016/j.bcp.2025.117280](https://doi.org/10.1016/j.bcp.2025.117280) | [40885321](https://pubmed.ncbi.nlm.nih.gov/40885321/) | CBD sesga A2A–CB2: desacopla β-arr sin romper el heterómero |
| 10 | Dutta, Selvam & Shukla, *ACS Chem. Neurosci.* 2022 | [10.1021/acschemneuro.1c00760](https://doi.org/10.1021/acschemneuro.1c00760) | [35019279](https://pubmed.ncbi.nlm.nih.gov/35019279/) | Na+ CB1≠CB2 (rutas/sitio secundario); matiza extrapolación class A |

### Class A / surveys (ancla, no sobreclaim CB2)

| # | Cita | DOI | PMID | Relevancia |
|---|------|-----|------|------------|
| 11 | Katritch et al., *Trends Biochem. Sci.* 2014 | [10.1016/j.tibs.2014.03.002](https://doi.org/10.1016/j.tibs.2014.03.002) | [24767681](https://pubmed.ncbi.nlm.nih.gov/24767681/) | Canónico Na+/agua class A — **[EXTRAPOLACIÓN_CLASE_A]** |
| 12 | Aranda-García et al., *Nat. Commun.* 2025 | [10.1038/s41467-025-57034-y](https://doi.org/10.1038/s41467-025-57034-y) | [40016203](https://pubmed.ncbi.nlm.nih.gov/40016203/) | Breathing IC; sitios alostéricos ocultos; lípidos como sondas — GPCRome |
| 13 | Conflitti et al., *Nat. Rev. Drug Discov.* 2025 | [10.1038/s41573-024-01083-3](https://doi.org/10.1038/s41573-024-01083-3) | [39747671](https://pubmed.ncbi.nlm.nih.gov/39747671/) | Review: dinámicas funcionales / microswitches / ACN para discovery |

### Anclas estructurales (PDB; no papers nuevos)

| PDB | Uso en framing |
|-----|----------------|
| [6KPC](https://www.rcsb.org/structure/6KPC) | Referencia estructural usada en figuras Morales-Pastor (LigACN) |
| [6PT0](https://www.rcsb.org/structure/6PT0) / [6KPF](https://www.rcsb.org/structure/6KPF) | Estados activos CB2 del atlas del proyecto (micronetwork INDETERMINATE — observación propia) |

---

## 7. Cross-links

| Documento | Rol |
|-----------|-----|
| [`CB2_DYNAMIC_INTERACTION_LAYERS.md`](CB2_DYNAMIC_INTERACTION_LAYERS.md) | Mapa multicapa que esta encuesta audita |
| [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Freeze / `P1_NOT_SUPPORTED` |
| [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) | ACN / Trp258 / MSM |
| [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) | Continuo / protean / contradicciones abiertas |
| [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md) | Gates P1–P6; objeto P2 → transiciones |

---

*Fin CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md — encuesta docs-only; COMPUTATION=PAUSED; sin armonización post hoc de P1.*

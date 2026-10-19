# PUBLIC DATA LEADS — CB2 (informe para PI)

**Fecha:** 2026-09-20 · **Update:** 2026-10-19 (XL 2014; 12IY/12JA XL extension; trafficking; surface×cAMP design; deferred probes/GRAB)  
**Tipo:** DOCUMENTATION ONLY — síntesis de literatura + depósitos públicos 2019–2026; **sin** compute nuevo.  
**Audiencia:** PI (español, postura de credibilidad).  
**Autoridad de freeze:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) · acta EXTERNAL [`ACTA_EXTERNAL_CB2_APO_2026-09.md`](ACTA_EXTERNAL_CB2_APO_2026-09.md) · roadmap [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md)

### Epistémico (no negociable)

| Capa | Qué puede decir este documento | Qué **no** puede decir |
|------|--------------------------------|-------------------------|
| **EXTERNAL** | Otros labs estudian control conformacional / hubs / redes / MSM de CB2; hay datos y papers aprovechables **en otra pregunta** | Que descargar trajs heterogéneas reabra **P2 Gate-1** |
| **P2 (nuestro)** | Sigue `CLOSED (INSUFFICIENT_SAMPLING)` hasta Gate-1 sobre target Tier B propio | Que un MSM ajeno o un zip de 85–142 GB “sustituya” nuestro muestreo GPCRmd |

**Claim estrecho que sí defendemos:** los dumps heterogéneos públicos **no** reabren *nuestra* compuerta P2.  
**Claim que NO defendemos:** “no hay literatura ni datos útiles en la misma dirección.” Eso es falso.

---

### Nuevo anclaje primario: crosslinks CB2–Gαi1 (2014)

**[LITERATURA_PRIMARIA]** Mnpotra et al. mapearon la interfaz CB2–Gαi1 con crosslinking químico y LC-MS/MS e identificaron tres pares: Cys134^3.54–Cys351, Lys245^6.35–Lys349 y Lys215^5.64–Lys317 (DOI [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916)). Completa el identificador primario pendiente que constaba en [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md); no constituye evidencia de una ruta alostérica intramolecular de CB2.

**[OBSERVACIÓN_PROPIA · EXTERNAL 2026-10-19]** Pre-reg [`EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md`](EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md) → veredicto **`EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED`** ([`ext_cb2_gi_crosslink_2014.md`](../../results/network_core/ext_cb2_gi_crosslink_2014.md)). En siete PDBs CB2–Gi locales (`6PT0`, `6KPF`, `8GUQ`, `8GUR`, `8GUS`, `8GUT`, `8X3L`), las distancias Cα–Cα cumplen los rangos del artículo: Cys134–Cys351 **7.65–8.28 Å** (HgCl₂: 7–10 Å), Lys245–Lys349 **15.48–16.26 Å** y Lys215–Lys317 **21.62–23.20 Å** (DSS: ≤24.2 Å). Auditoría descriptiva con endpoints SG/NZ y hashes: [`ext_cb2_gi_crosslink_audit.md`](../../results/network_core/ext_cb2_gi_crosslink_audit.md). Proximidad **intermolecular** ≠ hubs Janusforge / P3 / alostería intramolecular. Tráfico 2025: [`TRAFFICKING_CONFOUNDER_CB2_2025.md`](TRAFFICKING_CONFOUNDER_CB2_2025.md). P2/P5 unchanged.

## 1. No sois únicos

Muchos grupos trabajan activación, redes alostéricas, toggle, MSM y estructuras de CB2 (y CB1 comparativo). Vuestra singularidad, si la hay, está en la **gobernanza epistémica** (gates, EXTERNAL ≠ P2, discriminación pre-registrada) — no en el tema biológico.

### Labs / papers con nombre (núcleo 2019–2026)

| Quién | Qué estudian (alineado con vosotros) | Ancla |
|-------|--------------------------------------|--------|
| **Selent / Morales-Pastor et al.** (IMIM–UPF + Veprintsev / Bouvier) | ACN + LigACN (100 shortest paths), hubs de transmisión, PrefCoup Gαi2 vs βarr; MD GPCRmd 1540 | DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); GPCRmd [1540](https://gpcrmd.org/dynadb/publications/1540/); código [GPCRmd/prefcoup_cb2r](https://github.com/GPCRmd/prefcoup_cb2r); Zenodo [10.5281/zenodo.15270434](https://doi.org/10.5281/zenodo.15270434) |
| **Shukla / Dutta (UIUC)** | MSM/VAMPnets ~700 µs CB1 vs CB2; pipelines alostéricos por metaestable; toggle CB2 **poco acoplado** a IC vs TM5 | DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1); GitHub [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) |
| **Shukla / Dutta — AEA binding** | Adaptive sampling + MSM de **entrada** de anandamida (TM1–TM7 vs TM5–TM6); ~900 µs CB1+CB2 | DOI [10.1016/j.jbc.2026.111434](https://doi.org/10.1016/j.jbc.2026.111434); Illinois Data Bank [IDB-6705697](https://databank.illinois.edu/datasets/IDB-6705697) (`CB2_ana_bind.zip` ~85 GB) |
| **Hua / Liu / Li / Wu (ShanghaiTech et al.)** | Cryo-EM panel agonistas selectivos (CP, HU-308, Olorinab, LEI-102) | DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PDB **8GUR/8GUS/8GUQ/8GUT** |
| **Xing / Xie / Xu (Pitt / Van Andel)** | CB2–Gi WIN; contraste agonista/antagonista | DOI [10.1016/j.cell.2020.01.007](https://doi.org/10.1016/j.cell.2020.01.007); PDB **6PT0** |
| **Hua / Liu (Cell 2020)** | Cristal agonista 6KPC + cryo Gi 6KPF; CB1 colesterol | DOI [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008) |
| **Li / Stevens (Scripps) et al.** | Cristal inactivo AM10257 | DOI [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011); PDB **5ZTY** |
| **Gertsch / Carreira (Ganzoni, Kosar)** | Toggle W258^6.48 como continuo de eficacia / inverso-agonismo | Ganzoni *Chem. Sci.* [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B); Kosar *ACS Cent. Sci.* [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461) |
| **Abrol / Heo (CSUN)** | Complejos CB2–Gi vs βarr2 (± fosfo-C-term; mutantes Q63R, L133I); trajs Zenodo | Paper [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100); Zenodo [10.5281/zenodo.14227796](https://doi.org/10.5281/zenodo.14227796); GPCRmd entry 2091 (un traj) |
| **Yeliseev / Gawrisch (NIAAA)** | EPR site-selective (CW); colesterol reclasifica ligandos; **DEER propuesto, no publicado como mapa de distancias CB2** | EPR [10.1016/j.bbamem.2021.183603](https://doi.org/10.1016/j.bbamem.2021.183603) / PMC [PMC8154700](https://pmc.ncbi.nlm.nih.gov/articles/PMC8154700/); colesterol [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6) |
| **DNP-MAS NMR (ACS Omega 2023)** | Ensemble local: TM7 ligando-sensible; ICL3 siempre flexible | DOI [10.1021/acsomega.3c04681](https://doi.org/10.1021/acsomega.3c04681) |
| **Wang / Li et al.** | PAM Ec21a + CP55940 + Gi (vestíbulo ECL2) | DOI [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6); PDB **9U7L** |
| **Shen / Shao et al.** | Entropy-driven subtype recognition; cryo CB2–G | DOI [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121); PDB **8X3L** |
| **Mnpotra / Reggio / Song** | Crosslinking químico CB2–Gαi1 (Cys–Cys / Lys–Lys); interfaz experimental | DOI [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916); PMC [PMC4106340](https://pmc.ncbi.nlm.nih.gov/articles/PMC4106340/) |
| **Oyagawa / Grimsey / Glass** | Tráfico anterógrado CB2 inducido por ligando (chaperoning); confusor de ensayos largos | DOI [10.1007/s00018-025-05961-w](https://doi.org/10.1007/s00018-025-05961-w); PMC [PMC12748375](https://pmc.ncbi.nlm.nih.gov/articles/PMC12748375/) |

Atlas interno ya lista la mayoría de PDBs: [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md). Encuesta de capas: [`CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md`](CB2_DYNAMIC_LAYERS_LITERATURE_SURVEY.md).

---

## 2. Veredictos ya publicados (para no reinventar)

| Claim que alguien ya testeó | Veredicto en literatura | Implicación para Janusforge |
|-----------------------------|-------------------------|-----------------------------|
| “Toggle W258^6.48 es el interruptor IC de CB2” | **Dutta–Shukla 2023:** rotación del toggle tiene **efecto mínimo** en movimiento IC; TM5 IC más acoplado a TM6/TM7. **Ganzoni/Kosar:** el toggle **sí** afina un **continuo de eficacia** en el bolsillo | No colapsar a “toggle = mecanismo”; tampoco a “toggle irrelevante”. Dos niveles. |
| “Hay un hub único / un solo camino” | **Morales-Pastor 2025:** **múltiples** triggers → mismo PrefCoup Gαi2; LigACN + ACN completa | Alineado con nuestro objetivo “caracterizar arquitectura”, no “encontrar el switch”. |
| “Redes alostéricas cambian inactive→active” | **Dutta:** CB1 sí muestra pipelines distintos por metaestable; **CB2:** pipelines EC→IC **sin** distinción clara active-like vs inactive-like (Supp Fig. 22 del paper) | Compatible con nuestro soft **`EXT_LANDMARK_CONTACTS_STABLE`** — sin confundirlo con MSM. |
| “Seis hubs estáticos = esqueleto dinámico persistente” | **Nadie** publica *ese* set exacto como ley; LigACN es otra construcción (degeneracy / shortest paths) | Nuestro P1 `NOT_SUPPORTED` bajo GPCRmd WT **no** contradice Morales-Pastor; pregunta distinta. |
| “Hay DEER/FRET de distancias de activación CB2 listas para restricción” | **No.** Yeliseev 2021 = CW-EPR (movilidad IL3 / punta EC TM6); DEER = *siguiente paso propuesto*. TR-FRET 2025 = **cinética de ligando**, no distancias intramoleculares de activación | Anclas experimentales = **cualitativas / sitio-específicas**, no mapa de restraints tipo NMR structure. |

---

## 3. Tabla: dato/paper → pregunta NUEVA para nosotros → esfuerzo

*(Espera de PC/cluster; nada de esto reabre P2 Gate-1.)*

| Dato / paper | Pregunta NUEVA (discriminación) | Esfuerzo | Capa | Status (2026-09-22) |
|--------------|----------------------------------|----------|------|---------------------|
| Panel PDB público más allá de 6 refs Dutta Fig.6: **5ZTY, 6KPC, 6KPF, 6PT0, 8GUR/S/Q/T, 8X3L, 9U7L** ([atlas](CB2_STRUCTURE_ATLAS.md)) | ¿El soft-STABLE de contactos se mantiene al cruzar **ligando / PAM / Gi** vs solo el camino geométrico Dutta? | **Bajo** (solo PDBs) | EXTERNAL | ✅ `EXT_LANDMARK_EXPANDED_*` (prior) |
| Morales-Pastor Supp Data 3 (degeneracy; ya usado en X1/P1) + clusters PrefCoup 1–3 | ¿Nuestros seis hubs caen en **LigACNtop** / clusters publicados, o son un objeto topológico distinto? (inventario, no rescue de P1) | **Bajo** | EXTERNAL / lit. | ✅ `EXT_HUBS_IN_LIGACNTOP` |
| Yeliseev CW-EPR sitios (IL3, A270C TM6 EC) + DNP-NMR M293 TM7 / M237 ICL3 | ¿Phase F/G + contactos estáticos predicen **más movilidad** donde EPR/NMR la ven? Checklist de anclas, no restricción MD | **Bajo** | EXTERNAL | ✅ `EXT_EPR_NMR_ANCHORS_PARTIAL_AGREE` |
| Abrol Zenodo avg PDB / prmtop Gi vs βarr2 ([10.5281/zenodo.14227796](https://doi.org/10.5281/zenodo.14227796)) | En **complejo efector**, ¿qué contactos IC difieren Gi vs βarr — sin MSM de activación? | **Medio** (descarga selectiva de avg frames, no 100 GB) | EXTERNAL (hacia P3, no P2) | ✅ `EXT_ABROL_IC_EFFECTOR_PARTIAL` (P3 sigue BLOCKED) |
| GPCRmd 1540 WT (+ mutantes si se bajan) + AlloViz / 100 shortest paths (protocolo del paper) | ¿Reproducimos degeneracy LigACN en **nuestro** pipeline de contactos? Test de método, no Gate-1 | **Medio** | EXTERNAL / método | ⏳ open (medio esfuerzo; no hoy) |
| Illinois AEA `CB2_ana_bind` ([IDB-6705697](https://databank.illinois.edu/datasets/IDB-6705697)) | ¿Rutas de **entrada** de endocannabinoide (canal TM1–7) intersectan LigACNtop / ECL2-PAM? | **Medio** si solo paper+readme; **alto** si unpack 85 GB → **no recomendado mientras se espera PC** | EXTERNAL (≠ activación apo) | ✅ lit-only vía P4-lite (no unpack 85 GB) |
| Dutta Box trajs + filelist ordenado (request ya draft) | Contactos **por metaestable** Dutta (bloqueado hoy: `INDETERMINATE_NO_ALIGNMENT`) | **Medio** (depende de respuesta humana) | EXTERNAL frozen hasta filelist | ⏳ email draft ready — waiting human send/reply |
| Paper AEA / Dutta pipelines CB1 vs CB2 (sin traj) | Lectura P4-lite: ¿qué hipótesis CB1≠CB2 ya están **cerradas en lit.** antes de desbloquear P4? | **Bajo** | Lit. only | ✅ `EXT_P4LITE_ASYMMETRIES_CLOSED_IN_LIT` |
| Ganzoni toggle-continuo vs Morales PrefCoup multi-trigger (SI Note 1) | Tabla de predicciones discriminantes (niveles eficacia vs PrefCoup) | **Bajo** | Lit. only | ✅ `EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT` |
| Morales SI Note 1 cluster 2/3 contacts × hubs (N291; C288≈L287; D80≈A79) | ¿Vecindad hub en contactos PrefCoup publicados? | **Bajo** | EXTERNAL / SI | ✅ `EXT_PREFCOUP_HUB_NEIGHBORHOOD_OVERLAP` |
| 8GUS HU-308 + 9U7L Ec21a × hubs TM7 (+ AEA helix TM1–7 / TM5–6) | Intersección geométrica estática de capas | **Bajo** | EXTERNAL / PDB | ✅ `EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL` |
| Yeliseev EPR sitios → diseño DEER futuro | Pares candidatos **sin** distancias inventadas | **Bajo** | DOC only | ✅ `EXT_DEER_CANDIDATES_DESIGNED_NO_DISTANCES` |
| Wang 9U7L mutagénesis vs Qi/Niswender assay-dependent EC21a | Checklist struct↔PAM vs tensión farmacológica | **Bajo** | Lit. + PDB | ✅ `EXT_EC21A_PAM_STRUCT_ASSAY_PARTIAL` |
| Abrol IC contacts × LigACN Sink Set T | ¿Sinks Morales tocan fingerprint efector Abrol? | **Bajo** | EXTERNAL | ✅ `EXT_ABROL_LIGACN_SINK_OVERLAP` (P3 BLOCKED) |
| Dutta Supp Fig. 22 tunnels × hubs | Membership residue-level vs solo claim cualitativo EC→IC | **Bajo** | SI caption | ✅ `EXT_DUTTA_SF22_TUNNEL_HUB_QUALITATIVE_ONLY` |
| Mnpotra 2014 XL CB2–Gi (C134–C351; K245–K349; K215–K317) × panel cryo local | ¿Proximidad intermolecular XL compatible con geometría moderna CB2–Gi? (no hubs/P3) | **Bajo** | EXTERNAL | ✅ `EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED` (2026-10-19) |
| Oyagawa 2025 anterograde trafficking | ¿Registrar confusor de abundancia superficial en ensayos de horas? | **Bajo** (DOC) | EXTERNAL / assay | ✅ `TRAFFICKING_CONFOUNDER_CB2_2025` REGISTERED |
| Fluorescent paired probes (Chem. Sci. 2024) | Ortogonal localization/state — **DEFERRED** | — | FUTURE | ⏸ DEFERRED (PI 2026-10-19) |
| GRAB-CB2 / eCB2.0 (IJMS 2026) | Sensor fluorescente de activación — **DEFERRED** | — | FUTURE | ⏸ DEFERRED (PI 2026-10-19) |
| Sharma 2023 BRET kinetics / lipophilicity | Reanálisis cinético vs TR-FRET leads — **DEFERRED** | — | FUTURE | ⏸ DEFERRED (PI 2026-10-19) |
| Ahn Q63R / H316Y variants | Sensibilidad de fondo genético — **DEFERRED** | — | FUTURE | ⏸ DEFERRED (PI 2026-10-19) |
| 12IY / 12JA XL extension (same Mnpotra windows) | ¿Parejas XL 2014 compatibles en estructuras Rachman 2026? | **Bajo** | EXTERNAL | ✅ `EXT_CB2_GI_XL_12IY_12JA_PARTIAL` |
| Surface + cAMP time series (design only) | ¿Separar confusor de abundancia (Oyagawa) de cinética de señal (Sharma)? | **Design** | FUTURE wet-lab | 📋 `EXPERIMENT_DESIGN_SURFACE_CAMP_TIMESERIES` (not run) |

---

## 4. Top 3 análisis recomendados (datos públicos existentes; no pretenden reabrir P2)

### 1) Ensemble de landmarks cryo/cristal **más allá de Dutta-6** (esfuerzo bajo)

- **Qué:** contact fingerprints / RMSD-hard-assign (mismo espíritu que `EXT_LANDMARK_CONTACTS_*`) sobre el panel del atlas (incl. **9U7L** PAM, **8GUQ** βarr-biased, **8GUS** HU-308).  
- **Pregunta nueva:** ¿la estabilidad de mapa es propiedad del **camino inactive→active geométrico** o se rompe con diversidad de ligando/PAM/efector?  
- **No es:** MSM, ni Gate-1, ni A/B/C cinético.

### 2) Inventario “seis hubs Janusforge ↔ LigACNtop / PrefCoup clusters” (esfuerzo bajo)

- **Qué:** cruzar índices UniProt P34972 (hubs congelados) con Supp Data 3 + clusters 1–3 del SI Morales-Pastor.  
- **Pregunta nueva:** ¿objeto propio vs objeto publicado — solape, vecindad 1-hop, o disjuntos?  
- **No es:** reabrir P1 como hub hunt; es **clarificar identidad del objeto** para el informe.

### 3) Tabla de anclas experimentales EPR/NMR ↔ coordenadas ya en repo (esfuerzo bajo) — ✅ DONE 2026-09-22

- **Qué:** mapa sitio→predicción cualitativa (movilidad / restricción) desde Phase F/G y contactos estáticos; explicitar **ausencia de DEER CB2**.  
- **Pregunta nueva:** ¿dónde un futuro DEER (sitios Yeliseev) discriminaría RED_ESTABLE vs rutas-por-estado **si** hubiera muestreo propio?  
- **No es:** fingir restraints que no existen.  
- **Hecho:** [`EXPERIMENT_EXT_EPR_NMR_ANCHORS.md`](EXPERIMENT_EXT_EPR_NMR_ANCHORS.md) · `results/network_core/ext_epr_nmr_anchors.md` → **`EXT_EPR_NMR_ANCHORS_PARTIAL_AGREE`**.

*(Abrol avg Gi vs βarr IC contacts — ✅ DONE 2026-09-22: [`EXPERIMENT_EXT_ABROL_IC_CONTACTS.md`](EXPERIMENT_EXT_ABROL_IC_CONTACTS.md) → `EXT_ABROL_IC_EFFECTOR_PARTIAL`; P3 sigue BLOCKED.)*

---

## 5. Gaps: qué peers han hecho y Janusforge **aún no**

| Hecho por peers | Estado Janusforge | Notas |
|-----------------|-------------------|--------|
| LigACN / suboptimal paths / degeneracy (Morales-Pastor) | Usamos Supp Data + tests; **no** re-pipeline AlloViz completo en mutantes | Gap de método, no de tema |
| MSM activación µs-scale (Dutta) | EXTERNAL kinetics + landmarks + own MSM non-convergent; **P2 propio** insuficiente | Correcto no fingir |
| MSM **binding** AEA (Illinois) | No tocado | Pregunta distinta (entrada ≠ activación) |
| Complejos Gi vs βarr MD (Abrol) | P3 BLOCKED | Dato existe; decisión de scope |
| Panel cryo-EM multi-ligando como landmarks de red | Atlas + Phase G; **no** fingerprint de contactos multi-PDB post-Dutta-6 | Hueco **bajo esfuerzo** |
| Toggle continuo (Ganzoni) + multi-trigger (Morales-Pastor) | ✅ Discriminación formal | `EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT` (2026-10-02) |
| Colesterol / membrana como rutas (Yeliseev) | P5 HYPOTHESIS_READY, no ejecutado | Independiente; no rescate P1 |
| CB1 comparación de red | P4 BLOCKED | Lit. ya da asimetría de pipelines |
| DEER/FRET distancias activación | **Nadie** (CB2) ha entregado el mapa | No inventar anclas |

---

## 6. Mensaje corto para el PI (copiable)

> No somos los únicos que investigamos control conformacional, hubs de comunicación y activación de CB2. Selent/Morales-Pastor, Shukla/Dutta, Hua/Liu, Xing/Xie, Abrol, Yeliseev/Gawrisch, Gertsch/Carreira y otros ya publicaron redes LigACN, MSM, cryo-EM, toggle y EPR.  
>  
> La afirmación estrecha del proyecto es otra: **datos públicos heterogéneos no reabren nuestra P2 Gate-1** (muestreo propio insuficiente). Eso no implica que no haya literatura ni depósitos aprovechables **en preguntas EXTERNAL** (landmarks ampliados, inventario hubs↔LigACN, anclas EPR/NMR, opcionalmente Abrol Gi/βarr).  
>  
> Mientras llega el PC: priorizar los tres análisis de esfuerzo bajo arriba; no descargar 85–142 GB “por si acaso”.

---

## 7. Referencias mínimas (DOI)

1. Morales-Pastor et al. (2025) [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)  
2. Dutta & Shukla (2023) [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)  
3. Dutta & Shukla AEA (2026) [10.1016/j.jbc.2026.111434](https://doi.org/10.1016/j.jbc.2026.111434) · data [10.13012/B2IDB-6705697_V1](https://doi.org/10.13012/B2IDB-6705697_V1)  
4. Li et al. cryo panel (2023) [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9)  
5. Xing et al. 6PT0 (2020) [10.1016/j.cell.2020.01.007](https://doi.org/10.1016/j.cell.2020.01.007)  
6. Hua et al. 6KPC/6KPF (2020) [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008)  
7. Li et al. 5ZTY (2019) [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011)  
8. Ganzoni et al. (2026) [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)  
9. Kosar et al. (2024) [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461)  
10. Heo & Abrol (2025) [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100) · Zenodo [10.5281/zenodo.14227796](https://doi.org/10.5281/zenodo.14227796)  
11. Yeliseev et al. EPR (2021) [10.1016/j.bbamem.2021.183603](https://doi.org/10.1016/j.bbamem.2021.183603)  
12. DNP-MAS NMR CB2 (2023) [10.1021/acsomega.3c04681](https://doi.org/10.1021/acsomega.3c04681)  
13. Wang et al. Ec21a / 9U7L (2026) [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6)  
14. Shen et al. 8X3L (2024) [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121)
15. Mnpotra et al. CB2–Gαi1 crosslinking (2014) [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916)  
16. Oyagawa et al. trafficking (2025) [10.1007/s00018-025-05961-w](https://doi.org/10.1007/s00018-025-05961-w)  

---

## 8. Leads 2026-10-19 (PI decision) — ejecutado / diferido

**Decisión PI:** nota bibliográfica + comparación estructural del crosslinking CB2–Gi 2014; registrar tráfico 2025 como confusor de ensayos largos; **diferir** sondas fluorescentes (2024), GRAB-CB2 (2026), cinética/lipofilia y variantes. **No** reopen P2; **no** advance P5.

| Lead | Status | Artefacto / veredicto |
|------|--------|------------------------|
| Crosslinking CB2–Gi Mnpotra 2014 | ✅ DONE | [`EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md`](EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md) · `results/network_core/ext_cb2_gi_crosslink_2014.*` → **`EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED`** |
| Tráfico anterógrado Oyagawa 2025 | ✅ REGISTERED | [`TRAFFICKING_CONFOUNDER_CB2_2025.md`](TRAFFICKING_CONFOUNDER_CB2_2025.md) |
| Sondas fluorescentes pareadas (Chem. Sci. 2024) | ⏸ DEFERRED | PMC [PMC11485011](https://pmc.ncbi.nlm.nih.gov/articles/PMC11485011/) — fase futura |
| GRAB-CB2 / eCB2.0 (IJMS 2026) | ⏸ DEFERRED | PMC [PMC12984142](https://pmc.ncbi.nlm.nih.gov/articles/PMC12984142/) — fase futura |
| Sharma 2023 BRET kinetics / lipophilicity | ⏸ DEFERRED | PMC [PMC10094510](https://pmc.ncbi.nlm.nih.gov/articles/PMC10094510/) |
| Variantes Q63R / H316Y | ⏸ DEFERRED | PubMed [20124950](https://pubmed.ncbi.nlm.nih.gov/20124950/) |
| 12IY / 12JA XL (Rachman 2026) | ✅ DONE | [`EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md`](EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md) → **`EXT_CB2_GI_XL_12IY_12JA_PARTIAL`** (12JA ALL_WITHIN; 12IY N/A_NO_GI; 12IZ appendix ALL_WITHIN) |
| Surface + Gi/cAMP time series | 📋 DESIGN ONLY | [`EXPERIMENT_DESIGN_SURFACE_CAMP_TIMESERIES.md`](EXPERIMENT_DESIGN_SURFACE_CAMP_TIMESERIES.md) — no wet-lab; no P2/P5 reopen |

**Epistémico XL (recordatorio):** compatibilidad geométrica intermolecular ≠ prueba de hubs ni de mecanismo Gi funcional.


*Fin del informe. Flags de freeze P2 / EXTERNAL no se modifican por este documento.*


**Actualización 2026-10-19:** ampliada auditoría geométrica de crosslinks Mnpotra a **12JA**; los tres pares cumplen los criterios Cα publicados. **12IY se excluye** del conjunto CB2–Gi: RCSB lo clasifica como CB2 receptor-only. Propuesta documental de ensayo temporal de CB2 superficial + Gi/cAMP: [EXPERIMENT_CB2_SURFACE_SIGNAL_TIMECOURSE.md](EXPERIMENT_CB2_SURFACE_SIGNAL_TIMECOURSE.md). No altera P2/P5 ni autoriza trabajo de laboratorio.

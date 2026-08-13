# Qiu 0P — Auditoría exhaustiva del estado del arte (ahorrar gasto)

> **Fecha:** 2026-08-13  
> **Modo:** investigación + auditoría **solo**. **Prohibido** en este paso: docking nuevo, MD, NCE, síntesis, PDBQT, ensayos, campañas SAR.  
> **Mentalidad:** no buscar “0P PASS para continuar”; buscar qué **no** hace falta pagar.  
> **CSV paisaje:** [`qiu_0p_compound_landscape.csv`](qiu_0p_compound_landscape.csv)  
> **Contexto repo:** 0D–0J, 0K/0L/0IP/0N, mapa_ligandos, literatura_fibrosis, ip_gate, guia_maestra, cro_package_h1a.

**Capas epistémicas usadas en todo el documento:**

| Capa | Significado |
|------|-------------|
| **PUBLICADO** | Paper / SI / patente / DB con texto recuperado |
| **REPO** | Ya documentado en janusforge (0D–0N, docs) |
| **INFERENCIA** | Lectura estratégica; **no** es dato experimental nuevo |
| **NOT FOUND** | Ausencia en esta búsqueda — **no** inventar |

---

## Resumen ejecutivo (ahorro)

1. **Qiu-14 ya tiene claim funcional publicado** (agonista CB2 + antagonista CB1 por **cAMP**, SI Fig. S5; controles CP55940 / rimonabant). Eso **no** es “desconocido”.  
2. **Lo que falta y justifica duda de dinero:** (a) **números** Ki/IC₅₀/EC₅₀ **no** están en PubChem / ChEMBL / BindingDB / texto abierto; (b) **cero** reproducción independiente del compuesto 14; (c) **cero** fibrosis / in vivo / celular antifibrótica con Qiu-14.  
3. **H1-a como descubrimiento de “¿es agonista CB2?”** → **reproducción cualitativa** → **no justificar gasto** solo para redescubrir el signo.  
4. **H1-a como ancla operativa Janus en el panel CRO de janusforge** → incertidumbre **real pero estrecha**; alternativa más barata: controles comerciales (CP55,940 / JWH133 + antagonista CB1) + aceptar Qiu como motivación literaria.  
5. **MD / 0N / más docking no sustituyen H1-a** y **no** cierran potencia ni fibrosis; Ge LRIP ~62–70% success y está **BLOCKED** en repo.  
6. **Acción más barata que más reduce incertidumbre documental:** recuperar PDF Qiu + tablas de potencia (**TBD-18**). Luego decidir si aún hace falta material Qiu-14.

---

## 1. Qiu-14 — deep dive

### 1.1 Identidad / nombres / estructuras

| Campo | Valor | Estado |
|-------|-------|--------|
| Paper | Qiu et al., *Bioorg. Chem.* **133**, 106377 (2023) | PUBLICADO |
| DOI / PMID | https://doi.org/10.1016/j.bioorg.2023.106377 · PMID 36731294 | PUBLICADO |
| Preprint SSRN | abstract_id=4276225 (2022-11) | PUBLICADO abstract |
| Autores / afiliación | Yanli Qiu et al.; ShanghaiTech / SHUTCM; corr. Zhao / Yang / Tao / Suwen Zhao | PUBLICADO |
| Nombre de programa | “Yin-Yang ligand”; compuesto **14** (lead) | PUBLICADO |
| Alt names | Qiu-14 / compound 14 / QIU_14 (repo) | REPO |
| Chemotype | 1H-pirazol-3-carboxamida; **N1** = 2-morfolinofenilo; **C3** = CONH–(1-adamantilo); **C4** = Me; **C5** = Ph | PUBLICADO + REPO 0D |
| SMILES / InChI / InChIKey | Ver `data/libraries/qiu_0d_structures.csv` — InChIKey `QQXQVTJJXRACOB-UHFFFAOYSA-N` | REPO 0D YES |
| Formula / MW | C₃₁H₃₆N₄O₂ / 496.66 | REPO 0D |
| PubChem CID | **NOT FOUND** (PUG InChIKey → 404) | NOT FOUND |
| ChEMBL / BindingDB | **NOT FOUND** para InChIKey / SMILES Qiu | NOT FOUND |
| Vecinos 15 / 20 / 24 | meta-morph; o-Me-piperazine; CH₂-Ad linker | REPO 0D YES |

**SI (mmc1, cache local):** Scheme S1 numera 14/15/16 (o/m/p-morfolina), 20 (piperazina), 24 (CH₂-Ad); Fig. S5 = cAMP CB2 ago + CB1 ant de **14**; Fig. S6 docking regio o/m/p en CB1 5TGZ; Fig. S11–S13 paneles farmacológicos de la serie; Fig. S14 MM-GBSA vs actividad (correlación aproximada).

### 1.2 Binding / funcional / celular / in vivo

| Endpoint | Hallazgo | Capa |
|----------|----------|------|
| Binding radioligando (Ki) | Tablas numéricas **no recuperadas** en texto abierto / DBs | NOT FOUND (números) |
| Funcional CB2 | **Agonismo** por ensayo **cAMP**; control **CP55940**; 3 exp. × triplicado (SI Fig. S5A) | PUBLICADO cualitativo |
| Funcional CB1 | **Antagonismo** por cAMP; control **rimonabant** (SI Fig. S5B) | PUBLICADO cualitativo |
| Selectividad numérica | **NOT FOUND** abierta | NOT FOUND |
| Cellular (fibrosis / inmuno propio) | **NOT FOUND** para Qiu-14 | NOT FOUND |
| In vivo | **NOT FOUND** para Qiu-14 | NOT FOUND |
| Mecanismo propuesto | H-bond morfolina–**S173** (CB1) / **S285** (CB2); docking + MD ~100 ns (figuras paper/SI) | PUBLICADO (hipótesis computacional) |

### 1.3 Patentes / citas / follow-up

| Tema | Hallazgo |
|------|----------|
| Patente de composición Qiu-14 dedicada | **NOT FOUND** en esta pasada (Google Patents / nombres autores) — **≠** prueba de inexistencia (CN posible) |
| Citing post-2023 | OpenAlex / EuropePMC **citedByCount = 1**: *A novel CB2 agonist peptide with bone-promoting activity*, *Bioorg. Chem.* 2025, DOI https://doi.org/10.1016/j.bioorg.2025.108770 (PMID 40714479) — **péptido**, **no** reutiliza 14/15/20/24 |
| Reproducción independiente de Qiu-14 | **NOT FOUND** |

### 1.4 ¿H1-a es mera reproducción o incertidumbre real?

| Pregunta | Respuesta honesta |
|----------|-------------------|
| ¿Existe evidencia publicada CB2-ago / CB1-ant para el **14**? | **Sí** (un laboratorio; cAMP; SI). |
| ¿Está calibrada en DBs públicas con números? | **No**. |
| ¿Hay réplica independiente? | **No**. |
| ¿H1-a “descubrir el signo CB2” aporta conocimiento nuevo al mundo? | **Poco** — es reproducción cualitativa. |
| ¿H1-a aporta valor a *janusforge* como ancla de panel? | Solo si el programa **insiste** en Qiu-14 como control Janus operativo; si no, **controles comerciales** bastan y ahorran síntesis + ensayo del 14. |

**Veredicto §1:** la evidencia publicada **basta para no pagar un ensayo de descubrimiento**; **no** basta sola como ancla cuantitativa del programa ni como prueba antifibrótica. La incertidumbre que **sí** queda (potencia exacta, transferabilidad de ensayo, réplica) se reduce primero con **PDF/tablas** (barato), no con MD.

---

## 2. Paisaje de quimiotipos

| Familia | Ejemplos | Relación con hipótesis Janus | Saturación |
|---------|----------|------------------------------|------------|
| **Pirazol-3-carboxamida Yin-Yang** | Qiu 14/15/20/24 | Diseño racional CB1-ant/CB2-ago; switch N1-o-morfolina | Una campaña 2023; poco citado |
| **Pirazol CB1 clásico** | Rimonabant / AM6538 | CB1-only histórico; template de Qiu | Muy saturado (Sanofi US5624941 etc.) |
| **Pirazol CB2 ant** | AM10257 | Adamantilo en C3; control Qiu | Estructura cristalina CB2 |
| **Pirrol Janus** | URB447 | Precedente Janus periférico más cercano conceptualmente a D2 | Pequeña clase |
| **Indol / oxazinoindol** | GW405833 | Janus-like; morfolinoetilo | Clase conocida |
| **Cannabilactona** | AM1710 | Janus-like; lejos de pirazol | Clase conocida |
| **CB2 selectivos (agonistas)** | JWH133, Ge thiazolidinedionas, benzoxazinas, etc. | Responden brazo CB2; **no** Janus | Saturado en agonistas CB2 |
| **Markush fibrosis CB1/CB2** | WO2022026478 / US20230234928 | Claims mixtos + fibrosis; exemplares no = Qiu-14 | Presión IP (counsel) |
| **Fitocannabinoide imperfecto** | THCV | Janus natural con flip CB1 | Prior art farmacológico |

**Respuesta a la hipótesis Janus:** el *concepto* CB1↓+CB2↑ está **ocupado**; el hueco sigue siendo **NCE + datos de fibrosis** (pulmón/hígado/riñón), no “inventar Yin-Yang”. Qiu-14 responde la hipótesis **farmacológica de receptor**, **no** la antifibrótica.

---

## 3. Precedentes compute → experimento (CB2 / cannabinoides)

| Estudio | Método | Predicción | Ensayo | Tasa / límite |
|---------|--------|------------|--------|---------------|
| **Ge et al. 2023** ACS Chem Neurosci https://doi.org/10.1021/acschemneuro.3c00580 | LRIP + docking + MD + MM-PBSA-WSAS | Agonista vs antagonista CB2 | Ca²⁺ CHO-CB1/CB2 | Overall ~**69%**; CB2-selective ago ~**62%**; campaña derivados claim ~**70%** |
| **Ji/Wang 2020** ACS Chem Neurosci https://doi.org/10.1021/acschemneuro.9b00696 | Docking + MD + MM-PBSA | Afinidad/selectividad CB1/CB2 | Correlación con datos publicados | R² ~0.60 (mejor que score docking solo ~0.37) — **no** predice función Janus |
| **Qiu 2023** | Docking + MD + MM-GBSA | Hipótesis S173/S285 | cAMP serie pirazol | Correlación MM-GBSA–actividad **aproximada** (SI Fig. S14); función Yin-Yang **ensayada**, no sustituida por cómputo |
| **Dhopeshwarkar 2017** | Farmacología experimental (poca CADD) | — | Binding + función | Gold-standard Janus relectura — sin claim de “MD = PASS” |

**Límite duro:** incluso los mejores protocolos CB2 dejan **~30–40%** de error funcional. **No** hay precedente creíble de “MD/LRIP reemplaza ensayo H1-a” para un ancla de programa.

---

## 4. Precedentes MD / HPC en CB2 — ¿más simulación reemplaza H1-a?

| Trabajo | Qué hizo | ¿Predijo agonismo/antagonismo/selectividad validada? |
|---------|----------|-----------------------------------------------------|
| Qiu 2023 | MD ~100 ns; ocupación H-bond Ser | Hipótesis mecánica **post-hoc** alineada con cAMP ya medido |
| Ge 2023 | MD 115 ns + LRIP | Función predicha con error no trivial → **siempre** wet |
| Hua/Xie et al. | Homología + MD 50 ns + mutación | Residuos hotspot; no Janus |
| Lipid entry CB2 (2022) JCIM https://doi.org/10.1021/acs.jcim.2c00865 | MD + mutación A282F | Entrada por membrana validada experimentalmente — **no** sustituye EC₅₀ de Qiu-14 |
| PNAS 2024 entropy CB2 https://doi.org/10.1073/pnas.2401091121 | cryo-EM + metadynamics + mutación | Selectividad por entropía; diseño de ligandos **otros** — no Qiu |

**Repo 0N:** Ge LRIP **NOT READY** (SI ACS bloqueada); scoped MD **BLOCKED** (prep/GPU). Governance: 0N **no** es gate farmacológico.

**Respuesta clave:** **No.** Más simulación **no** reemplaza H1-a ni el conocimiento de potencia. Como mucho, MD ortogonal podría hablar de **estabilidad de pose** (ya parcialmente hecha por Qiu). Gastar HPC antes de wet = **mala asignación** frente a recuperar PDF o un ensayo barato dirigido.

---

## 5. Tabla amplia de ligandos

Ver CSV completo: [`qiu_0p_compound_landscape.csv`](qiu_0p_compound_landscape.csv).

Regla aplicada: **NOT FOUND** cuando faltan números; **nunca** inventar Ki/EC₅₀ de Qiu.

---

## 6. Patentes (ciencia ≠ patente ≠ inferencia; **no** es FTO)

| Familia / doc | Fecha / solicitante | Relación | Saturación vs hueco |
|---------------|---------------------|----------|---------------------|
| **WO2022026478A1** / **US20230234928A1** | ~2020 priority; Makriyannis / Vemuri; MAKScientific | Pyrazoles + claims CB1-ant/CB2-ago + fibrosis hígado/**pulmón**/riñón; ejemplo Compound 1 = CB1 Ki 1 nM, CB2 >1000 nM | Claims de uso/clase **ocupados**; exemplificación ≠ Qiu-14 |
| **US5624941** (Sanofi) | 1990s | Diarylpirazol CB1 (rimonabant lineage) | Muy saturado |
| Pyrazole CB modulators (BMS EP1670460, UConn JP2005507875, RTI US9133128, etc.) | 2000s–2010s | Markush pirazol / morpholine / adamantyl aparecen en claim language amplio | Espacio genérico ocupado |
| Adamantyl CB2 agonists (p.ej. US9090615 class) | — | Adamantilo como motivo CB2 | Motivo común |
| **Patente composición Qiu-14** | — | **NOT FOUND** esta pasada | Hueco documental (counsel CN/PCT) |

**Separación:** (ciencia) Qiu publicó Yin-Yang pirazol · (patente) Makriyannis claims fibrosis dual · (inferencia) Qiu-14 **no** es NCE janusforge; es vehículo de validación / prior art científico.

---

## 7. Fibrosis & CB2 (escalera; **no** asumir Qiu-14)

| Nivel | Evidencia | ¿Incluye Qiu-14? |
|-------|-----------|------------------|
| Receptor | CB1↑ profibrótico (IPF Cinar 2017 https://doi.org/10.1172/jci.insight.92281); CB2 protector en revisiones https://doi.org/10.1002/prp2.1219 | No |
| Ligando (brazo único) | JWH133 bleomicina pulmonar https://doi.org/10.1186/s12890-023-02747-3; CB1 ant periféricos (AM6545 etc.) | No |
| Ligando Janus monomolecular en fibrosis | URB447 / GW / AM1710 / **Qiu-14**: **NOT FOUND** en auditorías del repo | **No** |
| Combo CB1-ant + CB2-ago | AM6545 + AM1241 > mono en nefropatía diabética experimental | No (dos fármacos) |
| Clínico | MRI-1867 = CB1/iNOS (no CB2 ago) | No |

**Lectura:** la escalera biológica **soporta la hipótesis de programa**, **no** valida el compuesto 14.

---

## 8. Qué se puede saltar (0D…H2)

| Ítem | ¿Equivalente publicado? | ¿Reproducción? | ¿Incertidumbre genuina? | ¿Más inversión? |
|------|-------------------------|----------------|-------------------------|-----------------|
| **0D** estructuras | Sí (figuras/SI) | Ya hecha REPO PASS | Baja | **NO GASTAR** más |
| **Qiu structures 15/20/24** | Identidad sí; farmaco números no | Identidad hecha | Potencia relativa abierta | **NO** síntesis/ensayo salvo SAR futuro |
| **0E PDBQT** | N/A publicado | Hecho REPO | Baja (QC) | **NO** regenerar |
| **0F docking** | Qiu hizo docking propio | Hecho REPO | Vina≠afinidad | **NO** redocking |
| **0G pose** | Parcial vs figuras Qiu | Hecho REPO | Pose≠función | **NO** |
| **0H / 0J** | N/A | Hecho REPO | Observaciones log↔PDBQT | **NO** más QC visual de pago |
| **0N MD/LRIP** | Qiu MD + Ge precedente | Ge **NOT READY**; scoped **BLOCKED** | No cierra H1-a | **NO JUSTIFICADO** ahora |
| **H1-a** CB2 funcional Qiu-14 | **Sí cualitativo** (cAMP) | Sería reproducción del signo | Potencia + panel propio | Ver DECISIÓN: **skip discovery**; optional solo si ancla Janus |
| **H1-b** CB1 | **Sí cualitativo** | Reproducción del signo | Misma lógica | Condicionado a H1-a; no primero |
| **H2** D2_20/06 | **NOT FOUND** farmaco | No | Alta si se insiste en D2 | **No** sintetizar/ensayar hasta decisión de eje; docking overlap **no** autoriza |

---

## 9. Evidencia post-Qiu 2023

| Tipo | Hallazgo |
|------|----------|
| Citas OpenAlex/EuropePMC | **1** (2025 péptido CB2 óseo) |
| Papers que ensayan 14/15/20/24 | **NOT FOUND** |
| Reproducciones / contradicciones del Yin-Yang pirazol Qiu | **NOT FOUND** |
| Misma familia follow-up SAR de autores | **NOT FOUND** en esta pasada |

**Explícito:** tras Qiu 2023 **no** hay cadena experimental independiente que fortalezca Qiu-14. El campo **no** ha “cerrado” el compuesto por uso comunitario.

---

## 10. DECISIÓN 0P

### Tabla de clasificación

| Paso / gasto | Código | Justificación breve |
|--------------|--------|---------------------|
| Identidad 0D Qiu 14/15/20/24 | 🟢 YA RESUELTO / NO GASTAR | PASS 4/4 |
| PDBQT / docking / pose QC 0E–0J | 🟢 YA RESUELTO / NO GASTAR | Cadena hecha; Vina≠farmacología |
| Recuperar PDF Qiu + tablas Ki/EC₅₀ (TBD-18) | 🟢 BARATO Y ÚTIL | Única pieza documental que falta; guia dosis si hay wet |
| Controles comerciales CB2/CB1 en cualquier panel futuro | 🟢 BARATO Y ÚTIL | Sustituyen “descubrir” Qiu-14 como ago/ant |
| H1-a como descubrimiento CB2-ago de Qiu-14 | 🔴 NO JUSTIFICADO | Ya publicado (cAMP) |
| H1-a como ancla Janus operativa en CRO | 🟡 INCERTIDUMBRE REAL | Solo si el programa **exige** Yin-Yang monomolecular como control; si no, skip |
| H1-b | 🟡 / 🔴 | No antes de decidir H1-a; descubrimiento CB1-ant = reproducción |
| H2 D2_20/06 (síntesis + ensayo) | 🔴 NO JUSTIFICADO **ahora** | Sin farmaco publicada; depende de estrategia post-ancla |
| 0N / MD / LRIP / FEP / más docking | 🔴 NO JUSTIFICADO | No reemplaza wet; Ge blocked; Qiu ya MD |
| Fibrosis / in vivo Qiu-14 | 🟠 INFORMACIÓN INSUFICIENTE | No gastar hasta ancla receptor clara **y** decisión de indicación |
| Patente FTO formal | 🟠 INFORMACIÓN INSUFICIENTE | Landscape 0IP; **counsel**, no más cómputo |

### Cinco preguntas

1. **¿Qué sabemos de verdad de Qiu-14?**  
   Chemotipo 2D verificado; Yin-Yang **funcional cualitativo** (cAMP) en un paper+SI; hipótesis S173/S285 por docking/MD; **sin** números abiertos, **sin** réplica, **sin** fibrosis, **sin** CID/ChEMBL.

2. **¿Qué hay de CB2/CB1 para este chemotipo?**  
   El **orto-morfolina + adamantil-carboxamida** es el switch Yin-Yang **según Qiu**; meta/para y otros N1 son SAR de la misma campaña con números **no recuperados**. No hay landscape experimental externo del mismo exacto chemotype.

3. **¿Qué demostraron otros experimentalmente?**  
   Janus: URB447, GW405833, AM1710. CB2 fibrosis: JWH133 etc. Combo CB1-ant+CB2-ago: AM6545+AM1241. Compute→wet CB2: Ge ~62–70%. **Nadie** demostró antifibrosis con Qiu-14.

4. **¿Qué trabajo nuestro se elimina por ya publicado?**  
   Redescubrir el **signo** CB2-ago/CB1-ant de Qiu-14; rehacer docking/MD de mecanismo S173/S285; más QC de poses; Ge-style LRIP como sustituto de ensayo.

5. **¿Experimento/análisis de menor coste que más reduce incertidumbre?**  
   **(1)** Recuperar PDF/tablas Qiu (**barato**). **(2)** Si el norte es validar el *panel* (no el 14): un ensayo CB2 con **agonista comercial** + antagonista CB1 comercial. **(3)** H1-a Qiu-14 solo si se necesita explícitamente el ancla Yin-Yang monomolecular para H2/H3. **No** más docking. **No** 0N primero.

### Recomendación explícita H1-a

| Rol de H1-a | Recomendación 0P |
|-------------|------------------|
| Descubrimiento / “¿Qiu-14 activa CB2?” | **SKIP** — ya PUBLICADO |
| Ancla Yin-Yang operativa janusforge | **CONDICIONAL** — solo si PI mantiene Qiu-14 como control del programa; si no, **SKIP** y usar refs comerciales |
| Antes de cualquier H1-a de pago | **Hacer TBD-18 (PDF)** y cotizar síntesis solo si se confirma la necesidad del ancla |

**Preferencia 0P (ahorro):** **SKIP H1-a discovery**; **no** ejecutar 0N; **no** H2 aún; **sí** recuperar literatura numérica; reservar wet barato a controles comerciales si se abre cualquier panel.

---

## Fuentes ancla (no exhaustivo)

1. Qiu et al. 2023 — https://doi.org/10.1016/j.bioorg.2023.106377 · PMID 36731294 · SI mmc1 (repo `data/papers/`)  
2. LoVerme URB447 — https://doi.org/10.1016/j.bmcl.2008.12.059  
3. Dhopeshwarkar Janus — https://doi.org/10.1124/jpet.116.236539  
4. Ge LRIP — https://doi.org/10.1021/acschemneuro.3c00580  
5. Cinar IPF CB1 — https://doi.org/10.1172/jci.insight.92281  
6. JWH133 fibrosis pulmonar — https://doi.org/10.1186/s12890-023-02747-3  
7. WO2022026478A1 / US20230234928A1  
8. Citing Qiu — https://doi.org/10.1016/j.bioorg.2025.108770  
9. Repo: `qiu_0d`…`qiu_0n`, `qiu_0ip`, `mapa_ligandos_janus_cb1_cb2.md`, `literatura_fibrosis_cb1_cb2.md`, `literatura_prioridad_y_novelty.md`

---

## Cierre

```text
0P = AUDIT COMPLETE — SAVE-MONEY ORIENTED
NO NEW COMPUTE
H1-a DISCOVERY = SKIP
0N / MORE DOCKING = DO NOT FUND NOW
NEXT CHEAPEST = RECOVER QIU PDF TABLES (TBD-18)
```

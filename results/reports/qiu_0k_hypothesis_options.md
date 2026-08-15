# Qiu 0K — Opciones de hipótesis de validación experimental (post 0J STOP/PIVOT)

> **Plan cerrado en** [`qiu_0k_validation_plan_h1_h2.md`](qiu_0k_validation_plan_h1_h2.md) (H1 primaria Qiu-14 CB2→CB1; H2 backup D2_20/06; H3 gated; D2_22 OUT; umbrales TBD; sin ensayos). Este archivo permanece como framing de opciones / H4–H5 fuera del plan cerrado.

> **Alcance:** framing de hipótesis **falsables** para ensayo húmedo / siguiente ciencia.  
> **No** protocolos detallados, **no** docking, **no** MD, **no** dual-CB1 computacional.  
> **Fecha:** 2026-08-12  
> **Decisión de cadena:** 0D→0J cerrada con **STOP/PIVOT** (sin más cómputo en esta rama hasta autorización).  
> **Upstream:** [`qiu_0i_evidence_matrix.md`](qiu_0i_evidence_matrix.md) · [`qiu_0j_visual_qc.md`](qiu_0j_visual_qc.md) · [`qiu_0h_pose_audit.md`](qiu_0h_pose_audit.md) · [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md) · [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md) · [`qiu_0d_0g_integration_qc.md`](qiu_0d_0g_integration_qc.md) · [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md) · [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md)

**Axiomas obligatorios (heredados 0G–0I):**  
docking/Vina/pose overlap ≠ afinidad ≠ potencia ≠ farmacología Janus ·  
pose-comparable ≠ mismo farmacóforo ≠ misma farmacología ·  
**no** elevar D2_22 por Vina (overlap mid + feature_swap; MD CB1 ya NO-GO).

---

## 1. Hechos ya cerrados (computacional + límites)

- **Cadena Qiu 0D→0J:** identidad 2D de 14/15/20/24 verificada; PDBQT + docking CB2 (6PT0) QC PASS; análisis/auditoría/visual QC de poses MODEL 1 **PASS** (0J confirma orientaciones 0G/0H).
- **Ocupación CB2:** best poses Qiu y D2_20/06/22 co-ocupan la misma caja ortostérica-like (centroids ~1–2.4 Å del consenso Qiu; Jaccard vs unión Qiu hasta 0.76).
- **Geometría cross-chemotype:** D2_20 y D2_06 son el cluster de **mayor overlap** con Qiu (canonical_like: Bz↔Ad / NBn↔N1-het espacial); D2_22 es **pose_comparable** pero mid-pack (Jac ~0.56) con **feature_swap** — no “más Qiu-like”.
- **Chemotipo mismatch explícito:** Qiu = pirazol + CONH–Ad/CH₂–Ad + morph/piperazine; D2 = URB447-like (pirrol + aril-cetona + N-bencilo). Correspondencias espaciales ≠ identidad química de farmacóforo.
- **0 H-bonds geometry-OK** (criterio 0G) en las 7 poses auditadas; proximidades polares (p. ej. THR114, TYR25 en 15) **no** se relabelan como H-bonds ni como prueba de mecanismo S285.
- **Scores Vina** (Qiu −9.9…−11.6; D2_22 −12.35 más negativo del set D1 CB2) son **números de docking** solamente — no ranking farmacológico.
- **D2_22 MD membrana 20 ns (CB1 5TGZ):** **NO-GO de trinquete** — COM TM3–TM6 solapa régimen THC, no contención tipo THCV; descartado como lead funcional (ex-lead de docking). *No* reclamar Janus ni antifibrosis desde ese MD.
- **STOP/PIVOT 0J:** sin MD adicional y sin dual-CB1 docking en esta decisión; la validación pendiente es **experimental** (o cierre de rama), no más score.

---

## 2. Qué NO está demostrado

| Afirmación | Estado |
|------------|--------|
| Afinidad experimental (Ki/IC₅₀) de Qiu 14/15/20/24 en tablas propias del repo | **No recuperada** (mapa: bifuncionalidad publicada para cpd 14; números no inventados) |
| Que Vina CB2 de janusforge predice potencia Qiu o D2 | **No** |
| Que pose-comparable D2↔Qiu implica mismo farmacóforo químico | **No** |
| Que D2_20/06/22 tienen (o no) actividad CB1/CB2 experimental | **Desconocido** (sin ensayo húmedo janusforge) |
| Perfil Janus (CB1-ant + CB2-ago) de análogos D2 | **Desconocido** |
| Mecanismo morfolina–S173 (CB1) / S285 (CB2) como hecho estructural en nuestras poses | **No** (0 H-bonds OK; hipótesis Qiu de literatura, no medida aquí) |
| Selectividad CB1 vs CB2 (binding o funcional) para D2 o para re-ensayo Qiu | **No medida aquí** |
| Eficacia antifibrótica (IPF / bleomicina / fenótipo fibroblasto) de Qiu o D2 | **No** (mapa: hueco antifibrótico monomolecular real) |
| Elevación de D2_22 por score Vina o por “lead histórico” | **Prohibida** (geometría + MD NO-GO) |
| Estabilidad de pose en MD / ensamble CB2 | **No hecha** (STOP deliberado) |
| Dual CB1 docking 5TGZ para Qiu 0F / D2 en esta cadena 0D–0J | **No hecha** |

**Capas epistémicas a no mezclar:**

| Capa | Qué soporta |
|------|-------------|
| **Literatura** | Qiu 2023: diseño Yin–Yang; cpd **14** descrito como CB1-ant / CB2-ago; URB447/GW405833/AM1710 como precedentes Janus de otras familias; racional fibrosis CB1↑ / CB2↓ |
| **Computación janusforge** | Identidad 2D Qiu; ocupación/geometría CB2; overlap D2_20/06 > D2_22; límites estáticos |
| **Desconocido D2** | Binding, función, selectividad, Janus, fibrosis de D2_20/06 (y resto D1) |

---

## 3. Hipótesis candidatas (wet / next science)

### H1 — Ancla Qiu: el Yin–Yang publicado es reproducible en ensayo propio

| Campo | Contenido |
|-------|-----------|
| **H#** | **H1.** El compuesto Qiu **14** (y, si se dispone, 15/20/24 como SAR regio/linker) muestra **antagonismo funcional CB1** y **agonismo funcional CB2** en el panel de ensayo del proyecto. |
| **Qué la motiva** | **Literatura** (Qiu 2023 + mapa Janus) + objetivo de proyecto. La geometría 0G–0J solo dice que 14 ocupa CB2 de forma coherente; **no** prueba α. |
| **Predicción falsable** | En cAMP y/o β-arrestin (o GTPγS): CB2 = agonismo (EC₅₀ / Emax vs control CB2-ago); CB1 = antagonismo/neutral vs agonista de referencia (IC₅₀ o shift). Binding opcional como apoyo, no sustituto de función. |
| **Ensayo mínimo** | Panel funcional dual en células con hCB1 y hCB2 (mismo lote de ensayo); controles: agonista CB2 conocido + antagonista/agonista CB1; vehículo. **Sin** fibrosis aún. |
| **PASS** | CB2 agonismo y CB1 antagonismo detectables a concentraciones ≤ umbral predefinido (p. ej. ≤10 µM) con curva monótona y Z' aceptable. |
| **FAIL / kill** | Sin efecto CB2-ago **o** sin antagonismo CB1 (agonismo CB1, o inactividad en ambos) → no usar Qiu-14 como ancla operativa del programa; revisar identidad del material / ensayo antes de pivotar química. |
| **Coste/riesgo** | **Bajo–medio** (CRO / in-house binding+funcional; sin síntesis NCE si hay acceso a refs). |
| **Dependencia** | **Refs Qiu publicados** (compra/síntesis-contrato del 14; idealmente 15 como regio-control). **No** requiere D2. |

---

### H2 — Geometría canónica D2 predice actividad CB2 (sin asumir Janus aún)

| Campo | Contenido |
|-------|-----------|
| **H#** | **H2.** **D2_20 y/o D2_06** (mejor overlap geométrico con Qiu que D2_22) unen y **agonizan CB2** a potencia útil de hit (≥ micromolar claro), pese al chemotipo URB447-like ≠ Qiu. |
| **Qué la motiva** | **Geometría** 0G–0J (Jac 0.76; canonical_like) + **objetivo** Janus (brazo CB2 primero). Honestidad: overlap ≠ farmacología. |
| **Predicción falsable** | Al menos uno de D2_20/D2_06 muestra binding CB2 (Ki/IC₅₀) **y** agonismo funcional CB2; D2_22 (control negativo de priorización geométrica, no de “peor Vina”) no se usa como lead — puede correrse como **comparador** si ya está sintetizado. |
| **Ensayo mínimo** | Binding CB2 + funcional CB2 (cAMP o β-arrestin). CB1 en paralelo solo si el coste es marginal; si no, fase 2. |
| **PASS** | ≥1 de {D2_20, D2_06} con CB2-ago claro (p. ej. EC₅₀ ≤ 10 µM y Emax ≥ 30% del control, o criterio equivalente pre-registrado). |
| **FAIL / kill** | Ninguno de D2_20/06 activa CB2 por encima del umbral → **matar** la inferencia “overlap Qiu-like ⇒ CB2-ago en serie URB447”; no escalar SAR D2 por docking. |
| **Coste/riesgo** | **Medio–alto** (síntesis NCE D2 + ensayo). |
| **Dependencia** | **Síntesis D2_20/06** (o stock existente). Qiu refs útiles como controles positivos si H1 PASS. |

---

### H3 — Transferencia Janus cross-chemotype (la apuesta dura)

| Campo | Contenido |
|-------|-----------|
| **H#** | **H3.** Si H1 PASS, entonces D2_20/06 reproducen el **mismo vector Janus** (CB1-ant + CB2-ago), no solo ocupación CB2. |
| **Qué la motiva** | **Objetivo de proyecto** (monomolecular Janus) + geometría canónica D2↔Qiu como *hipótesis de diseño*, no como evidencia. |
| **Predicción falsable** | Perfil funcional dual alineado en signo con Qiu-14 (CB2↑, CB1↓/bloqueo), aunque potencias puedan diferir órdenes de magnitud. |
| **Ensayo mínimo** | Tras H1+H2: funcional **CB1 y CB2** en el mismo panel para D2_20/06 vs Qiu-14. |
| **PASS** | Ambos brazos del signo Janus presentes en ≥1 análogo D2 priorizado. |
| **FAIL / kill** | CB2-ago sin antagonismo CB1, o CB1-ago, o inactividad CB1 con CB2 débil → **no** reclamar “Qiu-like Janus” por pose; la serie D2 queda como CB2-biased / mono-brazo como máximo. |
| **Coste/riesgo** | **Alto** (síntesis + dual funcional; riesgo de falsear la tesis de transferencia). |
| **Dependencia** | **NCE D2** + **refs Qiu** (control). No usar D2_22 como proxy de éxito por Vina. |

---

### H4 — SAR regio/linker Qiu: la orientación de pose no decide la farmacología publicada

| Campo | Contenido |
|-------|-----------|
| **H#** | **H4.** Entre Qiu **14 / 15 / 20 / 24**, el perfil CB2 (y CB1 si se mide) **no** se ordena por score Vina ni por rotación visual (15→TYR25; 24 N1 +x); el orto-morfolina–Ad (14) sigue siendo el ancla Yin–Yang de la serie. |
| **Qué la motiva** | **Literatura** (serie Qiu) + **geometría** (variación de pose documentada) — para no sobreinterpretar 0J. |
| **Predicción falsable** | Ranking funcional experimental ≠ ranking Vina 0F (−11.6 de 24 / −11.2 de 15 ≠ “mejores”); 14 mantiene bifuncionalidad relativa o al menos CB2-ago competitivo en el set. |
| **Ensayo mínimo** | Binding o funcional CB2 (mínimo) en el cuarteto si hay acceso; CB1 solo en 14 + 1 regio (15) si presupuesto corto. |
| **PASS** | Datos experimentales permiten un orden; Vina no lo predice (documentar desacoplo). |
| **FAIL / kill** | Si solo 24/15 (mejores Vina) son activos y 14 es inerte → cuestionar identidad del material **o** la utilidad del ancla 14; no “arreglar” con más docking. |
| **Coste/riesgo** | **Medio** (más compuestos Qiu; sin D2). |
| **Dependencia** | **Refs Qiu** 14/15/(20/24). |

---

### H5 — (Backup fenotípico) Janus funcional ⇒ señal antifibrótica *in vitro* superior a mono-brazo

| Campo | Contenido |
|-------|-----------|
| **H#** | **H5.** Un ligando con H1/H3 PASS reduce marcadores fibróticos (p. ej. α-SMA / Col1a1 en fibroblastos pulmonares estimulados) **más** que un CB2-ago selectivo o un CB1-ant solo a concentraciones equi-eficaces de receptor. |
| **Qué la motiva** | **Objetivo IPF** + literatura combo CB1-ant+CB2-ago; **no** soportado por docking. |
| **Predicción falsable** | Efecto fenotípico dual > mono-brazo (o al menos no inferior con toxicidad comparable). |
| **Ensayo mínimo** | Fenotipo fibroblasto / TGF-β (una lectura primaria); solo **después** de PASS funcional de receptor. |
| **PASS** | Superioridad o no-inferioridad predefinida vs mono-brazo + citotoxicidad OK. |
| **FAIL / kill** | Sin beneficio vs mono-brazo → el valor Janus queda en PK/ocupación, no en fenotipo; no priorizar dualidad por dogma. |
| **Coste/riesgo** | **Alto** (ensayo fenotípico; interpretabilidad). |
| **Dependencia** | Material con perfil Janus ya confirmado (Qiu y/o D2). **No** primera hipótesis. |

---

## 4. Recomendación priorizada

### Primaria: **H1** (ancla Qiu-14 funcional)

**Por qué:** cierra el hueco epistémico más barato y más alineado con el norte Janus: la literatura ya afirma Yin–Yang para el **14**; el repo **no** tiene Ki/IC₅₀ propios ni re-ensayo. 0D–0J solo garantizan que el 14 que dockeamos es el chemotipo publicado y que ocupa CB2 de forma coherente — **no** que el programa tenga un control positivo usable. Sin H1 PASS, cualquier apuesta D2 por “parecerse a Qiu en pose” es circular.

**Honestidad docking:** un FAIL de H1 no se “arregla” con más Vina/MD; un PASS de H1 **no** autoriza elevar D2_20/06 sin ensayo (H2/H3).

### Backup: **H2** (D2_20/06 → CB2 primero), luego **H3** solo si H1+H2 PASS

**Por qué backup:** si hay capacidad de síntesis D2 y/o H1 ya calibró el ensayo, el siguiente falsador eficiente es “¿el cluster de mejor overlap hace CB2-ago?”. Eso prueba o mata la utilidad de la geometría 0G–0J para priorizar URB447-like **sin** resucitar D2_22 (MD NO-GO + feature_swap).

**No recomendar ahora:** más MD, dual-CB1 docking, o H5 fenotípico como primer gasto. **No** priorizar D2_22 por Vina.

| Orden sugerido | Hipótesis | Condición de entrada |
|----------------|-----------|----------------------|
| 1 | H1 | Acceso a Qiu-14 (mínimo) |
| 2 | H2 | Síntesis/stock D2_20 y/o D2_06 |
| 3 | H3 | H1 PASS **y** H2 PASS |
| 4 | H4 | Acceso a ≥2–3 Qiu de la serie |
| 5 | H5 | Janus funcional ya demostrado |

---

## 5. Preguntas abiertas (el usuario debe cerrarlas para fijar H)

1. **¿Hay acceso real a compuestos Qiu 14 (y 15/20/24)?** Compra, material de autores, o síntesis-contrato — ¿sí/no/plazo?
2. **¿Capacidad de síntesis NCE para D2_20 y/o D2_06** (mg escala ensayo)? ¿D2_22 ya existe en stock solo como comparador histórico?
3. **¿Primera campaña solo CB2** (binding+funcional) o **dual CB1+CB2** desde el día 1? (H1 recomienda dual; H2 admite CB2-first.)
4. **¿Umbrales PASS numéricos** aceptables (p. ej. EC₅₀ ≤ 1 µM vs ≤ 10 µM; Emax mínimo)?
5. **¿CRO vs in-house** y presupuesto techo de la primera campaña (¿solo H1, o H1+H2)?
6. **¿Se acepta explícitamente el STOP de cómputo** (sin MD / sin dual-CB1 docking) hasta tener readout húmedo, o hay una pregunta estructural residual autorizada?
7. **¿IPF fenotípico es gate temprano o solo post-Janus?** (H5 = tarde.)
8. **¿Recuperación de tabla Ki/IC₅₀ del PDF Qiu** sigue siendo prioridad documental en paralelo al wet, o se sustituye por re-ensayo propio?

---

## Cierre

**0K no lanza ensayos ni protocolos.** Fija opciones falsables tras **0J STOP/PIVOT**.  
La apuesta primaria es **calibrar el ancla literaria (H1)**; la backup es **matar o salvar la transferencia geométrica D2_20/06→CB2 (H2→H3)** sin rehabilitar D2_22 por score.

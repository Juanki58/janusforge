# Qiu 0K — Plan de validación H1/H2 (cerrado; CB2-first)

> **Estado:** **PLAN CERRADO** — decisión de hipótesis y orden de ensayo fijados.  
> **No** se ejecutan ensayos en este documento. **No** umbrales numéricos inventados: todo PASS/KILL cuantitativo = **TBD** hasta definición experimental pre-lab.  
> **Fecha:** 2026-08-12  
> **Base de opciones:** [`qiu_0k_hypothesis_options.md`](qiu_0k_hypothesis_options.md)  
> **Evidencia computacional (solo geometría/QC):** [`qiu_0i_evidence_matrix.md`](qiu_0i_evidence_matrix.md) · [`qiu_0j_visual_qc.md`](qiu_0j_visual_qc.md) · 0D–0H / farmacóforo / comparación D1  
> **Literatura / mapa:** [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md) (claims PUBLISHED citados con cuidado; Ki/IC₅₀ Qiu **no recuperados** en repo)

**Capas epistémicas (obligatorias en cada fila/sección):**

| Capa | Significado |
|------|-------------|
| **PUBLISHED** | Qiu 2023 / farmacología conocida en literatura o mapa del repo |
| **OBSERVED 0D–0J** | Solo geometría/QC computacional janusforge (identidad, ocupación, overlap, scores Vina como números de docking) |
| **HYPOTHESIS** | A probar en ensayo húmedo; **no** PASS por cómputo |

---

## 1. Decision lock

| Decisión | Valor cerrado |
|----------|----------------|
| **Primaria** | **H1** — Qiu-14 como ancla funcional del programa |
| **Orden receptor H1** | **CB2 primero** (agonismo funcional) → **CB1 como control** (antagonismo / no-agonismo) |
| **Backup** | **H2** — D2_20 y/o D2_06 (cluster de mayor overlap geométrico con Qiu) |
| **Orden receptor H2** | **CB2 primero**; CB1 **opcional / fase 2** solo si H2-CB2 PASS y presupuesto lo permite |
| **H3** | **Solo si H1 PASS y H2 PASS** — transferencia Janus (CB1-ant + CB2-ago) en D2; no entrada temprana |
| **H4 / H5** | **Fuera del plan de validación cerrado**; quedan como opciones documentadas en 0K options, no gates de esta campaña |
| **D2_22** | **OUT** del brazo positivo de hipótesis. Puede citarse solo como **control negativo/histórico** (feature_swap + MD CB1 NO-GO); **no** target de validación ni material a pedir para el brazo PASS |
| **Cómputo** | STOP/PIVOT 0J vigente: **sin** nuevo docking, MD ni SAR en esta decisión |

**Resumen en una frase:** calibrar Qiu-14 (H1, CB2→CB1); si hay material D2, probar transferencia CB2 en D2_20/06 (H2); Janus dual D2 (H3) solo tras ambos PASS; D2_22 no es hipótesis positiva.

---

## 2. Evidence layers (Published | Observed 0D–0J | Still hypothesis)

| Entidad | **PUBLISHED** | **OBSERVED 0D–0J** | **Still HYPOTHESIS** (wet) |
|---------|---------------|--------------------|----------------------------|
| **Qiu-14** | Diseño Yin–Yang; descrito como **antagonista CB1 + agonista CB2** (Qiu et al. 2023; mapa Janus). Hipótesis literaria morfolina–S173 (CB1) / S285 (CB2). **Ki/IC₅₀/EC₅₀ numéricos de la tabla experimental: no recuperados en repo** — no inventar. Sin demostración antifibrótica monomolecular en mapa. | Identidad 2D o-morph + CONH–Ad **PASS** (0D); PDBQT/docking CB2 6PT0 QC **PASS**; MODEL 1 ocupación ortostérica-like; Ad −x / N1-het +z; 0 H-bonds geometry-OK; Vina best ≈ −9.9 (score-only). Visual QC 0J confirma orientación. | Reproducibilidad del perfil Janus **en el panel janusforge**; potencia/eficacia propias; utilidad como control positivo operativo; cualquier umbral PASS del proyecto |
| **Serie Qiu (15/20/24 context)** | Misma familia Yin–Yang publicada (regio/linker); SAR de literatura **no** re-tabulada aquí sin números recuperados | 0D–0J: identidades verificadas; co-ocupación CB2; variaciones de pose (15→TYR25; 24 rotación N1; 20 casi idéntico a 14); scores Vina observados (15/24 más negativos que 14) — **≠ ranking farmacológico** | Actividad relativa 14 vs 15/20/24 en ensayo propio (H4 opcional, **no** gate de este plan) |
| **D2_20** | Ninguna farmacología CB1/CB2 publicada en repo para este análogo D1 | URB447-like; Jac vs unión Qiu **~0.76**; patrón **canonical_like** vs Ad/N1-het; co-ocupación CB2; Vina CB2 score-only ≈ −11.7; 0 H-bonds OK | Binding/agonismo CB2; antagonismo CB1; perfil Janus; cualquier potencia |
| **D2_06** | Igual — sin actividad experimental documentada en repo | Jac **~0.76**; **canonical_like**; co-ocupación; Vina ≈ −12.0 score-only; 0 H-bonds OK | Igual que D2_20 |
| **D2_22 (nota solo)** | N/A como target positivo | Pose_comparable mid (Jac ~0.56); **feature_swap**; Vina CB2 más negativo del set D1 (**no elevar**); MD membrana CB1 20 ns **NO-GO** trinquete | **No** hipótesis positiva. Si se ensaya algún día: solo comparador histórico / negativo de priorización geométrica — **fuera** de materiales del brazo H1/H2 PASS |

---

## 3. Main table — hipótesis → experimento → PASS / KILL → siguiente decisión

**Convención:** Criterio PASS / KILL cuantitativo = **TBD** (§4). Direcciones de signo (CB2-ago, CB1-ant) sí están fijadas; magnitudes no.

| Hipótesis | Experimento | Endpoint | Criterio PASS | Criterio KILL | Siguiente decisión |
|-----------|-------------|----------|---------------|---------------|--------------------|
| **H1-a** (primaria; CB2-first) | Funcional **hCB2** con Qiu-14 vs vehículo + control agonista CB2 conocido | Agonismo CB2 (cAMP y/o β-arrestin / GTPγS — formato **TBD**): EC₅₀ / Emax o lectura equivalente pre-registrada | Señal de **agonismo CB2** clara vs vehículo, con curva/calidad de ensayo aceptable (**umbrales numéricos TBD**; no usar Vina ni overlap) | Sin agonismo CB2 por encima del umbral TBD (o señal no interpretable tras QC de material/ensayo) | Si PASS → **H1-b** (CB1 control). Si KILL → stop Qiu-14 como ancla; revisar identidad/lote/ensayo antes de pivotar eje (§7) |
| **H1-b** (CB1 control; solo tras H1-a PASS) | Funcional **hCB1** con Qiu-14 vs vehículo + agonista CB1 de referencia (± antagonista ref.) | Antagonismo / bloqueo CB1 (IC₅₀, right-shift, o no-agonismo + bloqueo — formato **TBD**); **no** exigir Ki binding como sustituto | **Antagonismo CB1** (o perfil compatible con ant/neutral) detectable bajo criterios TBD; sin agonismo CB1 residual claro en la ventana TBD | Agonismo CB1 claro, o inactividad CB1 con fallo de control positivo, o perfil incompatible con ancla Yin–Yang | Si PASS → H1 **PASS** (ancla operativa). Siguiente: **H2** si hay material D2_20/06; si no, pausa wet hasta síntesis. **H3 no** aún. Si KILL → no ancla Janus usable; no autorizar H3; §7 |
| **H2-a** (backup; CB2-first) | Funcional (± binding) **hCB2** con **D2_20 y/o D2_06** | Agonismo CB2 (y/o ocupación CB2 si binding corre en paralelo) | ≥1 de {D2_20, D2_06} con **CB2-ago** claro bajo umbrales TBD | Ninguno activa CB2 por encima del umbral TBD | Si PASS → opcional **H2-b** o documentar H2-CB2 PASS y esperar gate H3. Si KILL → **matar** inferencia “overlap Qiu-like ⇒ CB2-ago URB447-like”; no escalar SAR D2 por docking; §7 |
| **H2-b** (opcional; CB1 tras H2-a PASS) | Funcional **hCB1** en el mismo análogo D2 que pasó H2-a | Antagonismo CB1 / signo Janus parcial | CB1-ant (o compatible) bajo TBD — **no** obligatorio para declarar H2 PASS de transferencia CB2 | CB1-ago fuerte o perfil que descarte uso Janus temprano | Informa prioridad hacia **H3** vs “CB2-biased only”. H2 se considera PASS de backup por **H2-a**; H2-b no bloquea H3 si se decide dual en H3 |
| **H3** (**gated**: solo si **H1 PASS y H2 PASS**) | Panel funcional **dual** CB1+CB2: D2_20/06 vs Qiu-14 (control positivo H1) | Signo Janus: CB2↑ y CB1↓/bloqueo en ≥1 D2 priorizado | Ambos brazos del signo presentes bajo TBD (potencias pueden diferir órdenes de magnitud) | Solo CB2-ago sin CB1-ant; o CB1-ago; o inactividad CB1 con CB2 débil | Si PASS → candidato transferencia cross-chemotype (aún sin fibrosis). Si KILL → D2 queda como máximo CB2-biased; **no** reclamar “Qiu-like Janus” por pose |

**Fuera de tabla (explícito):** H4 (SAR Qiu regio) y H5 (fenotipo fibrosis) **no** son gates de este plan cerrado.

---

## 4. TBD register — umbrales y definiciones pre-lab

Cada ítem debe cerrarse **antes** de iniciar el wet lab (CRO o in-house). Responsable sugerido: **lead experimental / PI del proyecto** (definir en kickoff).

| ID | Qué falta | Por qué importa | Quién / qué lo define |
|----|-----------|-----------------|------------------------|
| **TBD-01** | Sistema celular / ensayo (línea, densidades, hCB1 vs hCB2 ortólogos) | Comparabilidad H1↔H2↔H3 | Lead ensayo + CRO |
| **TBD-02** | Formato funcional CB2 (cAMP vs β-arrestin vs GTPγS; ortostérico vs lectura funcional) | Endpoint H1-a / H2-a | Lead ensayo |
| **TBD-03** | Formato funcional CB1 (antagonismo vs agonista ref.; IC₅₀ vs Schild vs Emax residual) | Endpoint H1-b / H2-b / H3 | Lead ensayo |
| **TBD-04** | Binding opcional: radioligando vs fluorescence; Ki vs IC₅₀ | No sustituye función; si se corre, criterios propios | Lead ensayo |
| **TBD-05** | **Mín. agonismo CB2** (EC₅₀ techo, Emax mín. % del control ago, o Δ señal vs vehículo) | PASS/KILL H1-a, H2-a | PI + lead ensayo (**no** copiar Vina; literatura Qiu numérica **ausente** en repo → no usar como gate inventado) |
| **TBD-06** | **Máx. / techo** para antagonismo CB1 (p.ej. IC₅₀ techo, % bloqueo a concentración fija) | PASS/KILL H1-b, H3 | PI + lead ensayo |
| **TBD-07** | Ventana de concentración de screening (p.ej. tope µM) y número de puntos de curva | Interpretable vs toxicidad/artefacto | Lead ensayo |
| **TBD-08** | Controles: agonista CB2 ref., agonista CB1 ref., antagonista CB1 ref., **vehículo**, Z'/CV aceptables | QC de campaña | Lead ensayo + CRO |
| **TBD-09** | Criterio de “agonismo CB1 residual inaceptable” (flip / dirty CB1) | Kill H1-b / H3 | PI (alineado a `criterio_exito_janus.md` gates cualitativos; **números TBD**) |
| **TBD-10** | Identidad/pureza mínima del material (HPLC, LC-MS, NMR) y lote Qiu-14 | Evitar falso KILL H1 | Química / supplier |
| **TBD-11** | Acceso Qiu-14 (compra / autores / síntesis-contrato) y plazo | Entrada H1 | Ops / química |
| **TBD-12** | Capacidad de síntesis mg-scale **D2_20** y **D2_06** | Entrada H2 | Química |
| **TBD-13** | Política explícita: **no ordenar D2_22** para brazo positivo | Evitar rehabilitación por stock | Ops / PI |
| **TBD-14** | Si H2-b es obligatorio o solo informativo antes de H3 | Secuencia presupuesto | PI |
| **TBD-15** | Criterio H3 de “mismo vector Janus” (¿mismo signo basta, o selectividad mínima CB2/CB1?) | PASS H3 | PI |
| **TBD-16** | Presupuesto techo campaña 1 (¿solo H1, o H1+H2?) | Alcance | PI / finance |
| **TBD-17** | CRO vs in-house | Ejecución | PI |
| **TBD-18** | Recuperación documental de tabla Ki/IC₅₀ Qiu (PDF) en paralelo — **contexto literature-reported only**, **nunca** auto-gate PASS janusforge salvo que se adopte por escrito como criterio literature-reported | Evitar inventar números; opcional calibración | Documentación / PI |

**Conteo TBD:** **18** ítems en registro.

**Nota:** Cualquier valor “p.ej. ≤10 µM” en documentos 0K *options* es **ilustrativo histórico**, **no** adoptado aquí como Criterio PASS.

---

## 5. Explicit non-claims (cómputo ≠ PASS H1/H2)

Los siguientes **no** constituyen PASS, ni KILL, ni ranking farmacológico para H1/H2/H3:

1. Scores **Vina** / ranking energético (Qiu o D2).  
2. **Pose overlap**, Jaccard de contactos, Δcentroid, atom-cloud overlap.  
3. Patrón **canonical_like** vs **feature_swap** (geometría solamente).  
4. Co-ocupación de caja ortostérica-like CB2.  
5. Proximidades polares / “0 H-bonds geometry-OK” / hipótesis S285–morfolina **sin** medida experimental.  
6. MD de **D2_22** (histórico NO-GO) como evidencia a favor o en contra de D2_20/06.  
7. Claims **PUBLISHED** de Qiu-14 como sustituto de **re-ensayo propio** (valen como motivación H1, no como PASS janusforge).

**Axioma heredado 0G–0I:** docking/Vina/pose overlap ≠ afinidad ≠ potencia ≠ farmacología Janus.

---

## 6. Materials

| Material | Rol en plan cerrado | Acción |
|----------|---------------------|--------|
| **Qiu-14** | Ancla H1 (obligatorio para primaria) | Obtener (compra / contrato / autores). Verificar identidad vs 0D SMILES. |
| Qiu 15/20/24 | **No** requeridos para H1/H2 gate | Opcional SAR (H4) — fuera de este plan |
| **D2_20** | H2 backup (prioridad geométrica) | **Sintetizar** (o confirmar stock) a escala ensayo |
| **D2_06** | H2 backup (co-prioridad con D2_20) | **Sintetizar** (o confirmar stock) |
| **D2_22** | **No** brazo positivo | **No ordenar** para validación H1/H2/H3. Solo nota histórica/negativa si ya existe en archivo |
| Controles farmacológicos | Refs CB1/CB2 | Definir en TBD-08 |
| Receptor/células | Panel hCB1 / hCB2 | TBD-01 |

---

## 7. Stop rules — cuándo pivotar

| Condición | Acción |
|-----------|--------|
| **H1-a KILL** (sin CB2-ago Qiu-14 tras QC material/ensayo) | **Stop** uso de Qiu-14 como ancla operativa. No lanzar H3. Revisar identidad/lote/formato; si confirmado, **pivotar fuera del eje Qiu** como control positivo del programa |
| **H1-a PASS + H1-b KILL** (CB2-ago sin antagonismo CB1 usable) | Qiu-14 **no** sirve como ancla Janus; posible CB2-biased only. **No** H3. Decidir si el eje Qiu sigue como ref. CB2 o se abandona para Janus |
| **H1 PASS + sin material D2 en horizonte** | Pausar wet D2; **no** reabrir docking/MD para “sustituir” H2 |
| **H2-a KILL** (D2_20 y D2_06 sin CB2-ago) | **Matar** transferencia geométrica overlap→CB2 en serie URB447-like. **No** SAR D2 motivado por 0G–0J. Pivotar química D2 / otra semilla; Qiu-14 (si H1 PASS) permanece ancla literaria/ensayo |
| **H1 PASS + H2 PASS + H3 KILL** | D2 = como máximo CB2-biased; **no** claim Janus cross-chemotype. Seguir Qiu u otras semillas para dualidad |
| **Tentación de rehabilitar D2_22** por Vina o stock | **Prohibido** como hipótesis positiva; MD CB1 NO-GO + feature_swap ya cerrados |
| **Presión por más cómputo** antes de readout húmedo | Mantener **STOP/PIVOT 0J** salvo pregunta estructural **autorizada por escrito** fuera de este plan |

---

## 8. Cierre

Plan de validación **cerrado**: H1 (Qiu-14, CB2→CB1) → H2 (D2_20/06, CB2-first) → H3 solo si ambos PASS; D2_22 fuera; umbrales **TBD** (18); ningún ensayo ejecutado aquí; ningún PASS computacional.

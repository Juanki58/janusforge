# Qiu / D1 — 0I Matriz de evidencia (0D–0H)

> **Alcance:** consolidación **únicamente** de resultados ya existentes (0D–0H). Sin nuevos cálculos, sin redocking, sin Vina, sin modificar/regenerar PDBQT, sin SAR.
>
> **Fecha:** 2026-08-12
>
> **Fuentes (read-only):**  
> [`qiu_0d_structure_verification.md`](qiu_0d_structure_verification.md) · [`qiu_0e_pdbqt_preparation.md`](qiu_0e_pdbqt_preparation.md) · [`qiu_0e_raw_pdbqt_audit.md`](qiu_0e_raw_pdbqt_audit.md) · [`qiu_0f_docking_protocol.md`](qiu_0f_docking_protocol.md) · [`qiu_0f_docking_qc.md`](qiu_0f_docking_qc.md) · [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md) · [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md) · [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md) · [`qiu_0d_0g_integration_qc.md`](qiu_0d_0g_integration_qc.md) · [`qiu_0h_pose_audit.md`](qiu_0h_pose_audit.md)

---

## 1. Resumen ejecutivo

**Propósito de 0I:** integrar en una sola matriz la evidencia ya documentada para Qiu 14/15/20/24 (cadena completa 0D–0H) y para D2_20 / D2_06 / D2_22 (poses D1 batch2 + comparación / farmacóforo / 0H; **sin** cadena 0D/0E/0F Qiu). Separar capas epistémicas: identidad estructural → preparación → score de docking (computacional) → geometría/farmacóforo → observaciones de poses — y declarar explícitamente qué **no** está respaldado (actividad, afinidad experimental, mecanismo, “misma farmacología”, elevar D2_22 por Vina).

| Cadena / bloque | Estado previo documentado |
|-----------------|---------------------------|
| 0D estructura Qiu | PASS 4/4 |
| 0E PDBQT Qiu | PASS 4/4 (prep + auditoría bruta) |
| 0F docking CB2 Qiu | PASS 4/4 **con observación** log↔PDBQT en 15/20 |
| 0G pose analysis Qiu | PASS 4/4 |
| Comparación D1 CB2 vs Qiu | COMPLETE |
| Farmacóforo geométrico D2↔Qiu | COMPLETE |
| Integración QC 0D–0G | PASS WITH OBSERVATIONS |
| 0H auditoría poses Qiu+D2 | PASS WITH OBSERVATIONS |

**Estado global 0I:** **PASS WITH OBSERVATIONS** (ver §6).

---

## 2. Matriz de evidencia

### 2.1 Qiu 14 / 15 / 20 / 24 (cadena 0D–0H)

| Campo | Qiu 14 | Qiu 15 | Qiu 20 | Qiu 24 |
|-------|--------|--------|--------|--------|
| **Estructura 0D** | YES — o-morph + CONH–Ad; SMILES/InChI verificados | YES — m-morph + CONH–Ad | YES — o-Me-piperazine + CONH–Ad | YES — o-morph + CONH–CH₂–Ad |
| **QC PDBQT 0E** | PASS — 38 átomos; formal 0; REMARK SMILES = 0D | PASS — 38 átomos; formal 0; SMILES = 0D | PASS — 39 átomos; formal 0; SMILES = 0D | PASS — 39 átomos; formal 0; SMILES = 0D |
| **Docking bruto 0F** | rc=0; log 9 / PDBQT 9; best −9.919 | rc=0; log **9** / PDBQT **8**; best −11.201 | rc=0; log **6** / PDBQT **5**; best −9.986 | rc=0; log 9 / PDBQT 9; best −11.606 |
| **Farmacóforo / ocupación 0G** | Región comparable; Ad −x; N1-het +z; Jaccard alto vs 20 | Región comparable; m-morph → TYR25; Ad mismo subpocket | Casi idéntico a 14 (Jaccard contactos 1.00 vs 14) | Misma región; **rotación** N1-morph (+x) vs 14/15/20 |
| **Auditoría poses 0H** | MODEL 1; region 4/5; 0 H-bonds OK | MODEL 1; region 5/5; 0 H-bonds OK; log↔PDBQT conservado | MODEL 1; region 4/5; 0 H-bonds OK; log↔PDBQT conservado | MODEL 1; region 4/5; 0 H-bonds OK; rotación documentada |
| **Discrepancias / observaciones** | Stereo InChI 3D vs 0D omitido; polar prox. THR114 (no H-bond) | **log↔PDBQT (+1, `energy_range`)**; polar prox. THR114/TYR25 | **log↔PDBQT (+1, `energy_range`)**; &lt;9 modos en log | CH₂-Ad; morfología rotada en caja |
| **Conclusiones respaldadas** | Identidad 2D; prep íntegra; docking ejecutado QC; ocupación ortostérica-like CB2; scores Vina observados | Igual + contacto TYR25 geométrico | Igual + co-localización vs 14 | Igual + Ad en mismo subpocket pese a rotación |
| **Conclusiones NO respaldadas** | Actividad / Ki / IC₅₀ / “mejor ligando” / H-bond a SER285 / mecanismo | Igual; no interpretar score más negativo como potencia | Igual | Igual; rotación ≠ cambio de mecanismo |

**Scores = Vina `REMARK` / log solamente — no afinidad experimental.**

### 2.2 D2_20 / D2_06 / D2_22 (D1 batch2; sin cadena Qiu 0D–0F)

| Campo | JANUS_D2_20 | JANUS_D2_06 | JANUS_D2_22 |
|-------|-------------|-------------|-------------|
| **Estructura 0D (Qiu)** | **N/A** — no es compuesto Qiu; scaffold URB447-like (Bz_pMe) | **N/A** — URB447-like (NBn_pCN) | **N/A** — URB447-like (Bz_pCF₃); lead histórico D1 |
| **QC PDBQT 0E (Qiu)** | **N/A** — ligando preexistente D1 batch2 | **N/A** | **N/A** |
| **Docking / score** | Score-only CB2 batch2: **−11.656** (MODEL 1; 9 poses) | Score-only: **−12.03** (MODEL 1; 8 poses) | Score-only: **−12.35** (MODEL 1; 9 poses) — más negativo del set D1 CB2; **no** elevar |
| **Correspondencia farmacofórica 0G** | pose_comparable; Jac vs Qiu union **0.76**; TYR25 yes; ejes espaciales canónicos vs Qiu | pose_comparable; Jac **0.76**; TYR25 yes; canónico | pose_comparable mid-pack; Jac **0.56**; Δcent ~2.14 Å; **feature_swap** |
| **Auditoría poses 0H** | Region 5/5; 0 H-bonds OK; pattern=canonical_like | Region 5/5; 0 H-bonds OK; pattern=canonical_like | Region 4/5; 0 H-bonds OK; pattern=**feature_swap** |
| **Discrepancias / observaciones** | Chemotipo ≠ Qiu (cetona/bencilo vs Ad/CONH/morph); prep pipeline puede diferir | Igual | feature_swap; mid overlap; Vina top ≠ más Qiu-like |
| **Conclusiones respaldadas** | Co-ocupación caja CB2; correspondencias espaciales parciales feature↔residuo; TYR25 en shell | Igual | Co-ocupación caja; feature_swap documentado; score Vina observado |
| **Conclusiones NO respaldadas** | Misma farmacología / mismo farmacóforo químico / actividad / afinidad | Igual | Igual + **no** priorizar por Vina más negativo |

---

## 3. Clasificación de conclusiones

| Conclusión | Clasificación | Base (fuentes) |
|------------|---------------|----------------|
| Identidad estructural 2D Qiu 14/15/20/24 verificada (SMILES/InChI/chemotype) | **SUPPORTED** | 0D PASS 4/4 |
| Integridad de preparación PDBQT Qiu (SMILES exactos, carga formal 0, chemotype SMARTS, QC bruto) | **SUPPORTED** | 0E prep + raw audit PASS 4/4 |
| Existencia / QC de docking CB2 0F (rc=0, config bloqueada, artefactos válidos) ×4 | **SUPPORTED** | 0F QC PASS 4/4 |
| Scores Vina como **salida computacional** observada (no potencia) | **SUPPORTED** (como números) | 0F/0G/0H REMARK |
| Modos log no escritos en PDBQT para Qiu **15** y **20** (`energy_range` default) | **OBSERVATION** | 0F QC; conservado en 0G/0H/integración/0I |
| Qiu 20 &lt; `num_modes=9` modos distintos en log | **OBSERVATION** | 0F QC |
| Best poses Qiu ocupan región de unión comparable (centroids / Jaccard) | **SUPPORTED** (geometría) | 0G PASS 4/4 |
| D1 D2_20/06/22 pose_comparable a consenso Qiu (gates centroid/Jaccard) | **SUPPORTED** (geometría occupation) | comparación 0G vs D1 |
| Correspondencias espaciales parciales feature↔residuo (p.ej. pyrrole↔pyrazole) | **OBSERVATION** / inferencia estructural | farmacóforo geom.; 0H |
| D2_22 **feature_swap** vs patrón Ad/N1-het de D2_20/06 | **OBSERVATION** | farmacóforo + 0H |
| Chemotipo mismatch Ad/CONH/morph vs URB447 cetona/bencilo | **OBSERVATION** | comparación + farmacóforo + 0H |
| Ningún H-bond geometry-OK (criterio 0G) en las 7 poses auditadas | **OBSERVATION** | 0G; 0H |
| Stereo InChIKey capa 3D Meeko vs 0D stereo-omitido | **OBSERVATION** | 0E audit (no falla QC) |
| Aminas terciarias neutras “as drawn”; protonación fisiológica no explorada | **OBSERVATION** / **NEEDS REVIEW** si se exige estado a pH 7.4 | 0E |
| PDF Elsevier/SSRN Qiu no obtenido; 0D vía CDN/SI | **OBSERVATION** | 0D |
| Actividad biológica / Ki / IC₅₀ / eficacia | **NOT SUPPORTED** | — |
| Afinidad experimental a partir de Vina | **NOT SUPPORTED** | — |
| Mecanismo de unión / “mismo modo farmacológico” | **NOT SUPPORTED** | — |
| “Misma farmacología” Qiu ↔ D2 por co-ocupación | **NOT SUPPORTED** | axioma pose≠farmacóforo≠farmacología |
| Elevar / priorizar D2_22 por Vina CB2 más negativo | **NOT SUPPORTED** | comparación + farmacóforo + 0H |
| SAR / ranking de compuestos por score o overlap | **NOT SUPPORTED** | scope 0I |
| Identidad química de features “conservados” cross-chemotype (más allá de espacial) | **NOT SUPPORTED** | farmacóforo |

---

## 4. Separación explícita de capas

### 4.1 Identidad estructural

- **Qiu:** 0D establece 1H-pirazol-3-carboxamida publicada (C4=Me, C5=Ph, C3–CONH–R³, N1–Ph–R¹) con SMILES/InChI YES para 14/15/20/24.
- **D2:** sin paso 0D Qiu; chemotipo URB447-like (pirrol + aril-cetona + N-bencilo) documentado por SMARTS en comparación/farmacóforo/0H — **no** es identidad Qiu.

### 4.2 Integridad de preparación

- **Qiu:** 0E PASS — REMARK SMILES = 0D; formal charge 0; chemotypes o/m-morph / Me-pip / CH₂-Ad correctos; auditoría bruta sin fallos QC.
- **D2:** **N/A** para pipeline Qiu 0E; ligandos batch2 preexistentes; posible diferencia de prep vs Qiu (limitación documentada).

### 4.3 Resultado de docking (computacional; ≠ actividad)

- **Qiu:** 0F PASS — Vina 1.2.7, receptor 6PT0, box/exhaustiveness/seed bloqueados; scores y n poses como artefactos.
- **D2:** scores CB2 batch2 existentes (score-only); no re-ejecutados en 0I.
- **Regla:** ningún número Vina se convierte aquí en potencia, selectividad o ranking farmacológico.

### 4.4 Similitud geométrica de farmacóforo

- Co-ocupación de caja ortostérica-like CB2 (centroids ~1–2.4 Å del consenso Qiu).
- Correspondencias espaciales parciales (p.ej. pyrrole↔pyrazole 12/12 spatial_ok; otros ejes 6–8/12).
- Mismatch químico explícito: Ad / CONH–Ad / morph–piperazine **ausentes** en D2.
- D2_22: feature_swap respecto al patrón canónico de D2_20/06.

### 4.5 Observaciones de poses

- Orientaciones Qiu (Ad −x; N1-het +z salvo 24 rotado; 15 con TYR25).
- 0H: 0 H-bonds geometry-OK en 7/7; polaridades como proximidades.
- Conservación espacial de ejes en D2_20/06 vs pérdida/swap en D2_22.

### 4.6 Inferencias farmacológicas que NO pueden hacerse

- Actividad, afinidad experimental, mecanismo, selectividad CB1/CB2, perfil Janus.
- “Mismo farmacóforo” o “misma farmacología” a partir de pose-comparable.
- Priorizar D2_22 (u otro) por Vina más negativo.
- SAR o diseño de análogos autorizado por 0I.

---

## 5. Discrepancias conservadas

1. **Qiu 15 — log↔PDBQT:** log 9 modos / PDBQT 8 MODELs; fila extra fuera de ventana `energy_range` (default motor; omitido en protocolo). **Conservada sin “arreglar”.**
2. **Qiu 20 — log↔PDBQT:** log 6 / PDBQT 5; además &lt;9 modos distintos en log. **Conservada.**
3. **0G/0H** analizan solo MODELs escritos → paisaje energético más allá de esas poses desconocido.
4. **D2_22 feature_swap** vs D2_20/06 (benzoyl↔N1-het / benzyl↔Ad) — geometría only.
5. **Chemotipo mismatch** Ad/CONH/morph (Qiu) vs URB447 cetona/bencilo (D2) — sin transferencia de Ad a átomos D2.
6. **Ningún H-bond geometry-OK** bajo criterio 0G (ángulo ≥120°) en poses auditadas; contactos O···THR114 etc. = polar proximity.
7. Stereo InChIKey 3D vs 0D stereo-omitido (conectividad OK).
8. Σq parcial ≈ +0.002 (14/15/20) — redondeo Gasteiger; formal 0.
9. Protonación fisiológica de aminas terciarias no explorada.
10. Receptor estático único (6PT0 agonista); sin MD/ensamble.
11. PDF fuente Qiu no obtenido; 0D vía CDN figuras + SI.
12. Pipelines prep D1 vs Qiu pueden diferir.

---

## 6. Veredicto global

**`PASS WITH OBSERVATIONS`**

**Rationale:** la cadena Qiu 0D→0E→0F→0G cierra PASS 4/4 por paso; comparación D1, farmacóforo geométrico y 0H están COMPLETE / PASS WITH OBSERVATIONS con artefactos trazables. Las observaciones abiertas (especialmente **15/20 log↔PDBQT `energy_range`**, chemotipo mismatch, D2_22 feature_swap, ausencia de H-bonds geometry-OK, límites estáticos/Vina≠afinidad) impiden un PASS limpio sin invalidar el QC de ejecución ni la consolidación.

---

## 7. Pasos justificados después de 0I

Opciones para **decidir** (no iniciadas por 0I):

1. **QC visual** de best poses Qiu + D2_20/06/22 en receptor 6PT0 (confirmación humana de ocupación/orientación).
2. **Chequeo dual CB1** (5TGZ) con protocolo análogo — solo si se autoriza docking/comparación CB1 (fuera del alcance 0I).
3. **MD / ensemble ortogonal** sobre poses escritas seleccionadas — estabilidad geométrica, no SAR automático.
4. **Diseño de ensayo húmedo** (binding/funcional CB2 ± CB1) para validar hipótesis biológicas — evidencia experimental, no Vina.
5. **Stop / pivot** si la decisión de validación no requiere más cómputo (p.ej. priorizar wet assay o cerrar rama D2_22 por overlap mid + feature_swap).
6. **Revisión de protonación** (estados cargados de morph/piperazine) solo si se autoriza prep nueva — **no** regenerar PDBQT bajo 0I.

---

## Cierre

**0I no autoriza SAR ni nuevo docking.** Esta matriz solo consolida evidencia 0D–0H ya existente y clasifica qué está respaldado, qué es observación y qué no se puede concluir.

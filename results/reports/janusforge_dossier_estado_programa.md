# Janusforge — Dossier de estado del programa (resumen ejecutivo ampliado)

| | |
|---|---|
| **Documento** | Estado del programa de investigación (uso interno / colaboradores / asesores) |
| **Fecha** | 2026-08-13 |
| **Idioma** | Español |
| **Naturaleza** | Documento de **estado de programa de investigación**, no consejo médico ni legal |
| **Confidencialidad** | Sin SMILES de NCE propietarias no publicadas |

---

## Aviso importante (léase primero)

Este dossier resume el **estado real** del programa Janusforge: qué se ha hecho (cómputo + planificación), cuál es la **visión de producto de salud**, y qué falta para avanzar a laboratorio húmedo.

**No afirma** que el docking demuestre eficacia clínica, ni que Janusforge ya disponga de un fármaco. **Qiu-14** es un **vehículo de validación publicado**, no una invención / NCE de Janusforge. Los scores de AutoDock Vina son **solo computacionales**. Las zonas IP “rojo/azul” son **borrador de landscape interno**, no dictamen FTO ni de patentabilidad.

Capas usadas en todo el documento:

| Capa | Significado |
|------|-------------|
| **Literatura** | Publicado en papers / mapas del repo |
| **Observación computacional** | Identidad, preparación, docking, geometría de poses (QC) |
| **Hipótesis** | A probar en ensayo húmedo o en diseño futuro |
| **Producto futuro** | Visión terapéutica; aún no materializada |

---

## 1. ¿Qué producto queremos?

**Visión terapéutica (producto futuro, no logrado aún):** un ligando (o familia) con perfil **Janus / Yin–Yang**:

- **CB1 antagonista** (o bloqueo / no-agonismo limpio en CB1), y  
- **CB2 agonista**,  

pensado como candidato de descubrimiento para **fibrosis orgánica**, con **fibrosis pulmonar idiopática (IPF)** como indicación prioritaria de motivación.

No se busca “cualquier cannabinoide”, ni maximizar afinidad indiferenciada, ni reclamar un fármaco listo. El norte farmacológico es el **perfil dual de receptores**; la fibrosis es el *para qué* clínico que da sentido al programa.

**Decisión de tracks (norma del proyecto):**

| Track | Rol | Prioridad |
|-------|-----|-----------|
| **Track 1 — Drug discovery** | Scaffold sintético Janus (precedentes URB447 / Yin–Yang tipo Qiu; H1–H5 THCV-like = fase cerrada / contraste) | **#1** |
| **Track 2 — Supply** | Estándares, controles, biomasa si aplica | Secundario |

Fuentes: `docs/guia_maestra_biotecnologia_quimiotipos.md`, `docs/literatura_fibrosis_cb1_cb2.md`, `docs/mapa_ligandos_janus_cb1_cb2.md`.

---

## 2. ¿Por qué importa para la salud?

*(Nivel literatura — motivación biológica; **no** es claim de cura ni de fármaco Janusforge.)*

La **fibrosis** es acumulación patológica de matriz extracelular; la **IPF** es una enfermedad pulmonar progresiva con necesidad médica alta: los antifibróticos aprobados ralentizan, pero no detienen ni revierten el daño establecido.

En el sistema endocannabinoide, la literatura asocia con frecuencia:

- **CB1** → brazo a menudo **profibrótico / proinflamatorio** (p. ej. evidencia en IPF humana y modelos bleomicina; Cinar et al., *JCI Insight* 2017).  
- **CB2** → brazo a menudo **antiinflamatorio / antifibrótico** en varios órganos.

Además, en fibrosis renal experimental, la **combinación** de un antagonista CB1 + un agonista CB2 ha mostrado efectos superiores a cada brazo por separado — lo que motiva la hipótesis de un **único ligando Janus**, sin confundir eso con una demostración ya hecha.

**Hueco real (literatura + mapa del repo):** el racional CB1↓ / CB2↑ en fibrosis es sólido a nivel de brazos separados o combos; **no** se ha documentado aquí una demostración antifibrótica monomolecular equivalente con URB447, GW405833, AM1710 o Qiu-14. Qiu 2023 plantea potencial terapéutico Yin–Yang (p. ej. lesión hepática crónica) como hipótesis, no como ensayo de fibrosis pulmonar del compuesto 14.

---

## 3. Qué hemos hecho (timeline operativo)

### 3.1 Contexto previo (cerrado / contraste)

- Hipótesis **H1–H5** sobre andamiaje THCV-like exploradas in silico; **NO-GO** de membrana MD → pivot a eje sintético (Opción D / URB447 / Yin–Yang).  
- Lead histórico de docking D1 **JANUS_D2_22**: scores Vina favorables en panel, pero MD membrana CB1 20 ns y análisis de pose (**feature_swap**) lo sacan del brazo positivo de validación. **No** se prioriza por Vina más negativo.

### 3.2 Cadena Qiu 0D → 0J (cómputo + QC) — cerrada con observaciones

| Hito | Qué hizo | Veredicto documentado |
|------|----------|------------------------|
| **0D** | Verificación estructural 2D Qiu 14/15/20/24 | PASS 4/4 |
| **0E** | Preparación PDBQT + auditoría | PASS 4/4 |
| **0F** | Docking CB2 (6PT0), Vina 1.2.7, protocolo bloqueado | PASS 4/4 (obs. log↔PDBQT en 15/20) |
| **0G** | Análisis geométrico de poses + comparación D1 / farmacóforo | PASS / COMPLETE |
| **0H / 0I** | Auditoría + matriz de evidencia | PASS WITH OBSERVATIONS |
| **0J** | QC visual; STOP/PIVOT: sin nuevo docking/MD/SAR en esta decisión | Vigente |

**Integración 0D–0G:** `PASS WITH OBSERVATIONS` (`qiu_0d_0g_integration_qc.md`).  
**Matriz 0I:** consolida capas; **no** autoriza SAR ni convierte Vina en potencia (`qiu_0i_evidence_matrix.md`).

Scores Vina CB2 observados (ejemplos; **solo computacionales**): Qiu-14 ≈ −9.9; Qiu-15/24 más negativos — **≠ ranking farmacológico**.

### 3.3 Planificación y gates (2026-08-12)

| Hito | Estado |
|------|--------|
| **0K** | Plan H1/H2 **cerrado** (CB2-first; umbrales numéricos TBD) |
| **0IP** | Landscape novelty **borrador — necesita counsel** (no clearance) |
| **0L** | Spec experimental H1-a **cerrada**; wet no iniciado |
| **0M** | Handoff wet **BLOCKED** hasta TBDs pre-estudio |
| **Paquete CRO H1-a** | Índice + carpeta `SEND/` lista para RFQs comparables |
| **0N** | Cómputo opcional estilo Ge 2023: **`NOT READY`** (congelado; no ruta crítica) |

### 3.4 Organigrama vigente

```text
0D–0J (cómputo / QC)
  → 0K (plan H1/H2)
  → 0IP (landscape)
  → 0L (spec H1-a)
  → 0M / CRO → WET H1-a  ← RUTA CRÍTICA ACTUAL
  → (PASS) H1-b → H2 → (PASS) H3 gated
  → NCE solo en hipótesis blue-ocean documentadas
  → 🛑 IP GATE / revisión con counsel
  → síntesis & ensayos de NCE propia

0N (paralelo opcional) — NOT READY; no sustituye H1-a
```

---

## 4. Qué está demostrado vs no demostrado

| Afirmación | Estado | Capa |
|------------|--------|------|
| Identidad 2D de Qiu 14/15/20/24 verificada en repo | **Demostrado (QC)** | Observación computacional |
| Pipeline PDBQT + docking CB2 ejecutado con QC trazable | **Demostrado (QC)** | Observación computacional |
| Best poses Qiu ocupan región ortostérica-like CB2 (geometría) | **Demostrado (geometría)** | Observación computacional |
| D2_20 / D2_06 con overlap geométrico mayor vs consenso Qiu; D2_22 con feature_swap | **Observado** | Observación computacional |
| Scores Vina como números de salida del motor | **Observados** | Observación computacional |
| Vina = afinidad / Ki / potencia / ranking farmacológico | **No demostrado** | — |
| Qiu-14 reproduce perfil Janus en el panel de Janusforge | **No demostrado** (hipótesis H1) | Hipótesis |
| D2_20/06 son agonistas CB2 o Janus | **No demostrado** (hipótesis H2/H3) | Hipótesis |
| Un ligando Janus monomolecular cura o trata IPF | **No demostrado** | — |
| Janusforge posee un fármaco / NCE clínica | **Falso / no aplica** | — |
| Qiu-14 es invención Janusforge | **Falso** — es prior art publicado | Literatura |
| Landscape 0IP = FTO / patentabilidad | **No** — borrador interno | — |

---

## 5. Vehículo de validación Qiu-14 vs futura NCE + IP gate

### 5.1 Qiu-14 (publicado)

- **Rol:** ancla / control positivo **literario** para calibrar el panel experimental (H1).  
- **No es** NCE Janusforge, ni inventorship, ni producto final.  
- **Química (nivel publicado):** pirazol-3-carboxamida con *o*-morfolinofenilo + CONH–1-adamantilo (familia Yin–Yang Qiu et al. 2023).  
- **Literatura:** descrito como antagonista CB1 + agonista CB2; hipótesis morfolina–S173 (CB1) / S285 (CB2). Valores numéricos Ki/IC₅₀ de la tabla experimental **no recuperados en el repo** — no se inventan como umbrales PASS.  
- Copias directas de Qiu-14 = **prior art científico** (zona roja 2 del landscape).

### 5.2 Futura NCE propia (producto futuro)

Solo **después** de validación húmeda H1/H2 (según plan) y **dentro** de hipótesis de espacio blanco documentadas, con:

1. Revisión de patentabilidad / FTO con **counsel** registrado,  
2. Decisión de filing,  
3. **Sin** SMILES propietarios en documentos públicos hasta autorización.

### 5.3 Tres momentos IP (protocolo interno)

| Momento | Significado |
|---------|-------------|
| **1** | Controles / cómputo (0D–0J + uso de Qiu publicado) = calibración científica |
| **2** | Ventana de invención = NCE propia + datos CB1/CB2 experimentales + familia SAR defendible |
| **3** | Gate de divulgación = revisión con counsel **antes** de cualquier divulgación pública de NCE |

**Zonas landscape (borrador; necesita counsel):** presión de familias tipo Makriyannis/Vemuri (fibrosis dual-claim), Qiu 2023, y espacio Sanofi/rimonabant; ideas “blue ocean” = hipótesis exploratorias, **no clearance**.

Fuentes: `docs/ip_gate_janusforge.md`, `results/reports/qiu_0ip_novelty_landscape.md`.

---

## 6. Plan de validación experimental H1/H2

**Estado:** plan **cerrado** en 0K; **ningún ensayo húmedo ejecutado**. Direcciones de signo fijadas; **magnitudes PASS/KILL = TBD** (no inventadas).

| Hipótesis | Material | Orden | Endpoint (dirección) | Siguiente |
|-----------|----------|-------|----------------------|-----------|
| **H1-a** (primaria) | Qiu-14 | **CB2 primero** | Agonismo funcional hCB2 vs vehículo + ref. agonista | PASS → H1-b; KILL → stop ancla Qiu-14 |
| **H1-b** | Qiu-14 | Tras H1-a PASS | Antagonismo / control CB1 | PASS → ancla H1; luego H2 si hay material D2 |
| **H2-a** (backup) | D2_20 y/o D2_06 | CB2 primero | Agonismo CB2 | Transfiere o mata inferencia overlap→actividad |
| **H2-b** | Mismo D2 | Opcional | CB1 | Informativo hacia H3 |
| **H3** | D2 vs Qiu-14 | **Solo si H1 y H2 PASS** | Signo Janus dual | Transferencia cross-chemotype (aún sin fibrosis) |

**Fuera del plan cerrado:** H4 (SAR Qiu regio), H5 (fenotipo fibrosis).  
**D2_22:** fuera del brazo positivo (control histórico/negativo solamente).

**No constituyen PASS:** scores Vina, overlap de poses, Jaccard, co-ocupación, MD de D2_22, ni claims de literatura como sustituto de re-ensayo propio.

Detalle: `qiu_0k_validation_plan_h1_h2.md`, `qiu_0l_h1a_experimental_spec.md`.

---

## 7. Estado operativo (bloqueos actuales)

| Ítem | Estado | Comentario |
|------|--------|------------|
| Cómputo 0D–0J | **Cerrado** (PASS WITH OBSERVATIONS) | STOP/PIVOT: no más docking/MD/SAR como siguiente paso |
| Spec H1-a (0L) | **Cerrada** | Lista para rellenar TBD pre-lab |
| Handoff wet (0M) | **`BLOCKED`** | Paquete listo; wet no arranca |
| Paquete CRO | **Listo para envío** (`cro_package_h1a/SEND/`) | RFQ síntesis Qiu-14 + ensayo CB2 + nota NDA/IP |
| Material Qiu-14 | **TBD-11** | Compra / síntesis contrato / autores — pendiente |
| Criterio PASS H1-a | **TBD-05** | Debe firmarlo el PI **antes** del primer run |
| Formato ensayo / células | **TBD-01, TBD-02, …** | Ver registro 0M §7 |
| 0N (Ge 2023–style) | **`NOT READY`** | SI ACS bloqueada; no es gate; no sustituye CRO→H1-a |
| NCE propietaria | **No iniciada** (correcto) | Tras wet + IP gate |

**Bloqueos duros antes del primer wet H1-a** (resumen 0M): sistema celular; formato funcional; **TBD-05 firmado**; ventana de concentraciones; controles/Z′; pureza/COA Qiu-14; material en mano; CRO vs in-house + SOP; plan de réplicas y análisis.

**Política de fase actual:** retorno de esfuerzo en **síntesis + ensayo + cotizaciones CRO**, no en más cómputo.

---

## 8. Próximos pasos recomendados

Orden sugerido (alineado a docs oficiales):

1. **Enviar** el set idéntico `results/reports/cro_package_h1a/SEND/` a 2–3 CROs (cover + RFQ síntesis + RFQ ensayo CB2 + nota NDA/IP).  
2. **Cerrar presupuesto** y elegir vía (síntesis + ensayo bundle o separados).  
3. **Asegurar Qiu-14** (TBD-11) con identidad vs ancla 0D y COA (TBD-10).  
4. **Cerrar TBDs pre-estudio** con PI + CRO — especialmente **TBD-05** — y actualizar 0M a *handoff ready* solo cuando el gate §7 esté checked.  
5. **Ejecutar H1-a** (único gate húmedo inmediato).  
6. Según resultado: plan **H1-b** o stop/pivot (0K §7). **No** saltar a NCE.  
7. **0N:** solo si se obtiene SI ACS y autorización explícita; permanece opcional y fuera de la ruta crítica.  
8. Tras H1/H2 PASS (si aplica): diseño NCE en hipótesis blue-ocean + **🛑 IP REVIEW con counsel** antes de divulgación o campaña de síntesis propietaria.

---

## 9. Anexos — rutas de informes clave

### Norma / visión

| Documento | Ruta |
|-----------|------|
| Guía maestra (tracks) | `docs/guia_maestra_biotecnologia_quimiotipos.md` |
| Literatura fibrosis CB1/CB2 | `docs/literatura_fibrosis_cb1_cb2.md` |
| Mapa ligandos Janus | `docs/mapa_ligandos_janus_cb1_cb2.md` |
| IP gate (protocolo) | `docs/ip_gate_janusforge.md` |

### Cómputo Qiu / integración

| Documento | Ruta |
|-----------|------|
| Integración QC 0D–0G | `results/reports/qiu_0d_0g_integration_qc.md` |
| Matriz de evidencia 0I | `results/reports/qiu_0i_evidence_matrix.md` |
| Plan H1/H2 (0K) | `results/reports/qiu_0k_validation_plan_h1_h2.md` |
| Spec H1-a (0L) | `results/reports/qiu_0l_h1a_experimental_spec.md` |
| Handoff wet (0M) | `results/reports/qiu_0m_h1a_wet_handoff.md` |
| Landscape IP (0IP) | `results/reports/qiu_0ip_novelty_landscape.md` |
| Estado 0N | `results/reports/qiu_0n_status.md` |
| Protocolo 0N (gobernanza) | `results/reports/qiu_0n_ge2023_reproduction_protocol.md` |

### CRO

| Documento | Ruta |
|-----------|------|
| Índice paquete CRO | `results/reports/cro_package_h1a/00_index.md` |
| Carpeta SEND (RFQs) | `results/reports/cro_package_h1a/SEND/` |

### Precedente literario ancla (Qiu-14)

Qiu et al., *Bioorg. Chem.* 2023; DOI: https://doi.org/10.1016/j.bioorg.2023.106377

---

## Cierre en una frase

Janusforge tiene **visión clara** (Janus CB1↓/CB2↑ para fibrosis/IPF), **cómputo y planificación trazables** hasta un handoff H1-a listo en papel, y está **bloqueado operativamente** en material Qiu-14, criterios TBD (esp. TBD-05) y ejecución CRO — con **0N congelado** y **IP gate** obligatorio antes de cualquier NCE propietaria.

*— Fin del dossier. No es consejo médico ni legal.*

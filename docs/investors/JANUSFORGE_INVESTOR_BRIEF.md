# Janusforge — Brief para inversores / interlocutores técnicos

**Tipo:** documento de credibilidad (no deck Series-A; no proyección financiera)  
**Fecha:** 2026-09-13  
**Idioma primario:** español · **Abstract EN** abajo  
**Autoridad científica:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md)  
**Fuente regenerable PDF:** este Markdown · script `scripts/build_investor_brief_pdf.py`  
**Rama de referencia:** `feat/cb2-hubs-functional-topology-test`

---

## English abstract (short)

Janusforge is an early computational research program on **CB2 conformational control**, not a drug company and not a Series-A biotech package. Locked results: static LigACN hubs are **topology-only** (no Gi enrichment); dynamic hub skeleton **P1 CLOSED NOT_SUPPORTED**; own MSM **P2 CLOSED INSUFFICIENT_SAMPLING**; architecture models A/B/C **NOT DECIDED**. External Dutta work: geometric landmarks **STABLE** (soft-A), own MSM **NON_CONVERGENT**, PDB soft-B disagreement, filelist blocked. Repo is in **DEEP_PAUSE**; docking/de novo **STOP**. Next capital use is honest sampling capacity (NVIDIA MD workstation / cluster toward ≥20 µs), not a claim that the CB2 switch was found.

---

## 1. Qué es esto (y qué no es)

**Janusforge** es un programa de investigación computacional sobre el receptor cannabinoide **CB2 (CNR2)**. El norte científico actual es **caracterizar el mecanismo de control conformacional** del receptor (switch local vs red distribuida vs arquitectura estado-dependiente — cualquiera es resultado válido).

**No es:**

- un paquete Series-A de biotech con pipeline clínico;
- un claim de haber “encontrado el switch de CB2”;
- una demostración de mecanismo Gi / sesgo funcional cerrado;
- una campaña activa de docking o diseño *de novo* (ambas en **STOP**);
- un producto farmacéutico listo para licencia.

La misión histórica del repo (ligandos “Janus” CB1-ant / CB2-ago × fibrosis) **sigue como contexto de programa**, pero **no** es el entregable científico congelado hoy. Lo que se puede mostrar con rigor es la **línea de mecanismo CB2** y la disciplina del cuaderno.

---

## 2. Estado actual (un párrafo)

El proyecto está en **DEEP_PAUSE** con una excepción acotada: campaña de **muestreo masivo P2 pre-registrada** (docs + checklist; **sin** producción µs local hoy). P1 (seis hubs estáticos como esqueleto dinámico persistente) está **CLOSED (NOT_SUPPORTED)**. P2 (MSM propio sobre GPCRmd WT) está **CLOSED (INSUFFICIENT_SAMPLING)** — ITS no convergente con ~2 µs / 1995 frames. La discriminación arquitectónica A/B/C (**red estable / rutas por estado / distribuida**) quedó **ABORTED / NOT DECIDED**. LigACN estático: **CORE_TOPOLOGICAL_ONLY** (bottlenecks reales; **sin** enriquecimiento PrefCoup_Gαi2). Trabajo EXTERNAL Dutta: landmarks geométricos **STABLE** (lectura soft-A); own MSM **NON_CONVERGENT** (N=200); desacuerdo soft vs snapshot PDB-B; filelist de alineación bloqueado. Docking / de novo **STOP**. Hardware actual (GTX 1060) **no** produce el Tier B-min (≥20 µs) necesario para reabrir Gate-1 con honestidad.

---

## 3. Qué se aprendió (valor real)

| Aprendizaje | Lectura estricta |
|-------------|------------------|
| Coordenada macroconformacional CB2 (activo vs inactivo) | **GENERALIZES** out-of-sample (Phase G) — reconocimiento estructural; **no** eficacia funcional fina |
| Seis hubs LigACN (TM2 / TM7 / H8) | Bottlenecks topológicos **reales** en el grafo estático; **no** núcleo funcional Gi demostrado |
| Dual test topología × función | Veredicto **CORE_TOPOLOGICAL_ONLY** — arquitectura ≠ salida funcional |
| Persistencia dinámica de esos seis hubs (P1) | **NOT_SUPPORTED** bajo trayectorias GPCRmd/1540 WT analizadas |
| MSM propio (P2 Gate-1) | Muestreo insuficiente para MSM convergente; **no** se inventó biología sobre ITS fallido |
| Featurización reducida (X8) | Sigue NON_CONVERGENT → el cuello es **sampling**, no solo representación |
| EXTERNAL landmarks Dutta | Mapas de contacto geométricos estables entre 6 PDBs; **geométrico ≠ identidad MSM** |
| EXTERNAL own MSM (N=200) | Todavía NON_CONVERGENT; no reabre P2 GPCRmd |
| Gobernanza | Pre-registros, gates, actas freeze, `POST_HOC_EXCUSES = FORBIDDEN` — el cuaderno cierra puertas cuando debe |

**Frase útil sin overreach:** el modelo simple de que unos pocos hubs estáticos constituyen el mecanismo CB2→Gi **no está soportado** por los datos analizados. Eso **no** prueba que CB2 sea “plenamente distribuido” bajo todas las condiciones.

---

## 4. Qué NO se afirma (anti-hype)

| Claim tentador | Estado en el repo |
|----------------|-------------------|
| “Encontramos el switch de CB2” | **NO** |
| “Demostramos el mecanismo Gi” | **NO** (`FUNCTIONAL_Gi_ENRICHMENT = NOT_SUPPORTED`) |
| “Arquitectura A/B/C resuelta” | **NOT DECIDED** |
| “Nuestro MSM converge” | **NO** (P2 + EXTERNAL own MSM) |
| “Landmark geométrico = estado metaestable Dutta” | **NO** (`GEOMETRIC_NEQ_MSM`) |
| “Ya producimos µs de MD propios a escala Tier B” | **NO** |
| Proyecciones financieras / tamaño de equipo / IP portfolio | **No inventados aquí** |
| Drug claims / lead clínico | **Fuera de alcance de este brief** |

---

## 5. Riesgos y límites (sinceros)

1. **Muestreo.** Sin ensemble ≥ Tier B-min (~≥20 µs pre-registrados, réplicas independientes), Gate-1 no se reabre. El hardware actual no lo alcanza.
2. **Datos externos incompletos.** Pickles Final_MSM Dutta recuperados (cinética CB1≠CB2); trayectorias alineadas / filelist **bloqueados** → A/B/C estructural externo **INDETERMINATE**.
3. **Confusión geométrico↔MSM.** Soft-A geométrico puede coexistir con cinética undecided; no forzar narrativa.
4. **Scope creep.** Interés ≠ umbral de reopen. Docking/de novo siguen STOP precisamente para no quemar capital en score hunting.
5. **TRL bajo.** Esto es ciencia de mecanismo temprana, no asset listo para partnering farmacéutico.
6. **Una sola línea de compute.** PI / notebook + agentes documentados; no hay “equipo Series-A” detrás del freeze.

---

## 6. Uso de capital siguiente (honesto)

**Prioridad #1 — capacidad de muestreo MD**

- Torre / workstation **NVIDIA** (o acceso cluster equivalente) capaz de producción OpenMM/GROMACS CUDA.
- Objetivo científico pre-registrado: alcanzar **Tier B-min (≥20 µs)** del experimento P2 para **re-testear Gate-1** (ITS / convergencia), no para “encontrar el switch”.
- Smoke Tier A (infra) ≠ Gate-1. Credibilidad > pretend MD.

**Prioridad #2 (después, QUEUED)**

- Línea membrana / colesterol (**P5**): hipótesis lista; **no** ejecuta ahora; **no** rescata P1/P2.

**No pedir capital para (ahora):**

- campañas de docking / librerías *de novo*;
- narrativa de fármaco Janus cerrado;
- “completar el mecanismo Gi” sin MSM convergente.

Detalle técnico: [`docs/synthesis/EXPERIMENT_P2_MASSIVE_SAMPLING.md`](../synthesis/EXPERIMENT_P2_MASSIVE_SAMPLING.md).

---

## 7. Nivel de investigación (opinión sincera)

### Lectura TRL-like / madurez académica

| Dimensión | Rating honesto | Comentario |
|-----------|----------------|------------|
| Madurez de **programa fármaco** | **TRL ~1–2** (idea / principios observados) | No hay asset clínico ni lead defendible activo |
| Madurez de **mecanismo CB2 (este repo)** | **Preprint-grade early / tesis doctoral temprana** | Preguntas bien formuladas; gates; cierres negativos útiles |
| Madurez de **infra MD a escala de campo** | **Pre-productivo** | Stack documentado; producción µs **aún no** |
| Madurez de **gobernanza / notebook** | **Alta para un proyecto individual** | Freeze YAML, pre-regs, actas, anti-post-hoc |
| Comparación vs lab académico CB2 MD/MSM | **Por debajo** de grupos con cientos de µs publicados | Correcto: no fingir paridad con Dutta (~700 µs) o Morales (~2 µs WT ya reanalizables) |
| Comparación vs biotech Series-A | **No comparable** | Este documento no debe usarse como si lo fuera |

### Opinión (tono brief / inversores)

Janusforge, en su estado actual, es **investigación de mecanismo computacional temprana con disciplina epistémica por encima de la media**, no un paquete de inversión biotech maduro. El valor demostrable hoy es: (i) haber **falsificado** con limpieza varias hipótesis atractivas pero frágiles; (ii) saber **exactamente** qué experimento discrimina la siguiente frontera (muestreo → MSM convergente → A/B/C); (iii) haber **parado** docking/de novo cuando el cuaderno lo exigía. El valor **no** demostrable hoy es un mecanismo CB2→Gi cerrado, un switch, ni un pipeline de fármaco.

Quien invierta tiempo o capital aquí debería hacerlo como **apoyo a ciencia de muestreo y rigor**, no como compra de un asset farmacéutico. Si alguien necesita un pitch de “ya tenemos el interruptor de CB2”, este proyecto **no** lo es — y eso es precisamente lo que lo hace creíble.

---

## 8. Equipo / rigor del cuaderno (sin inventar tamaño)

- Trabajo organizado como **cuaderno científico versionado en Git** (commits citables, flags de freeze, pre-registros antes de ver resultados).
- Autoridad operativa: `RESEARCH_STATE.md` (no slides).
- Regla de decisión: **solo preguntas que discriminen ≥2 hipótesis** (`DISCRIMINATION_ONLY`).
- No se inventan aquí headcount, advisors, ni portfolio de patentes.

---

## 9. Tabla de flags (snapshot)

```text
PRIMARY_OBJECTIVE          = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
STATIC_LIGACN              = CORE_TOPOLOGICAL_ONLY
P1_STATIC_HUBS             = CLOSED (NOT_SUPPORTED)
P2_MSM_TRANSITIONS         = CLOSED (INSUFFICIENT_SAMPLING)
P2_NETWORK_A_B_C           = ABORTED
ARCHITECTURE_A_B_C         = NOT DECIDED
EXTERNAL_LANDMARKS         = EXT_LANDMARK_CONTACTS_STABLE
EXTERNAL_OWN_MSM           = EXT_OWN_MSM_NON_CONVERGENT
DUTTA_FILELIST             = BLOCKED
P2_MASSIVE_SAMPLING        = PREREGISTERED (no µs production today)
P5_MEMBRANE                = HYPOTHESIS_READY / QUEUED
DOCKING / DE_NOVO          = STOP
DEEP_PAUSE                 = TRUE (scoped lift only for sampling campaign)
```

---

## 10. Lecturas recomendadas (repo)

| Documento | Rol |
|-----------|-----|
| [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Autoridad de freeze |
| [`docs/synthesis/RESEARCH_ROADMAP.md`](../synthesis/RESEARCH_ROADMAP.md) | Contrato P1–P6 |
| [`docs/synthesis/EXPERIMENT_P2_MASSIVE_SAMPLING.md`](../synthesis/EXPERIMENT_P2_MASSIVE_SAMPLING.md) | Uso de capital / muestreo |
| [`docs/synthesis/ACTA_EXTERNAL_CB2_APO_2026-09.md`](../synthesis/ACTA_EXTERNAL_CB2_APO_2026-09.md) | Freeze EXTERNAL |
| [`results/msm_model/p2_msm_convergence_report.md`](../../results/msm_model/p2_msm_convergence_report.md) | Evidencia Gate-1 |
| [`results/network_core/hubs_dual_validation_report.md`](../../results/network_core/hubs_dual_validation_report.md) | CORE_TOPOLOGICAL_ONLY |

---

## 11. Regenerar PDF / HTML

```powershell
# Desde la raíz del repo
python scripts/build_investor_brief_pdf.py
```

Salidas:

- `docs/investors/JANUSFORGE_INVESTOR_BRIEF.pdf`
- `docs/investors/JANUSFORGE_INVESTOR_BRIEF.html` (fallback / preview)

Si `xhtml2pdf` falla en otra máquina:

```powershell
pandoc docs/investors/JANUSFORGE_INVESTOR_BRIEF.md -o docs/investors/JANUSFORGE_INVESTOR_BRIEF.pdf --pdf-engine=xelatex
# o:
pandoc docs/investors/JANUSFORGE_INVESTOR_BRIEF.md -o docs/investors/JANUSFORGE_INVESTOR_BRIEF.html -s
```

---

*Fin del brief. 2026-09-13 — credibilidad > hype; muestreo primero; sin claim de switch.*

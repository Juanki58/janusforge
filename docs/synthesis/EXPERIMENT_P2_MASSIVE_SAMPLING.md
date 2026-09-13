# Experiment — P2 massive sampling campaign (pre-registration)

**Fecha pre-registro:** 2026-09-13  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de producción MD pesada y **antes** de cualquier re-test Gate-1.  
**PI authorization:** YES — decisión humana “adelante” = **muestreo masivo FIRST**, luego P5 membrana (**QUEUED**, no started).  
**Autoridad de flags:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) · acta EXTERNAL [`ACTA_EXTERNAL_CB2_APO_2026-09.md`](ACTA_EXTERNAL_CB2_APO_2026-09.md) · Gate-1 evidence [`p2_msm_convergence_report.md`](../../results/msm_model/p2_msm_convergence_report.md)

---

## 1. Qué significaba históricamente “muestreo masivo”

| Lectura | Contenido | Es esto? |
|---------|-----------|----------|
| **P2 reopen (correcta)** | Invertir en **más muestreo dinámico** para que un MSM propio sobre el sistema Morales/GPCRmd (o equivalente WT CB2) pueda **pasar Gate-1 (ITS / convergencia)** y solo entonces A/B/C | **SÍ — este experimento** |
| Acta EXTERNAL opción 1 | “Muestreo masivo / adaptativo (línea P2 GPCRmd u own MSM con N cualitativamente mayor…) — inversión de recurso, **no** piloto incremental” | **SÍ** |
| X8 (2026-09-09) | Misma data 1995 frames; featurización 24-D → ITS sigue `NON_CONVERGENT` → cuello = **sampling**, no representación | Confirma que hace falta **filmar más**, no retocar features |
| EXTERNAL Dutta zip / landmarks / own MSM N=200 | Reanálisis de depósito distinto; veredictos locked; **no** es GPCRmd P2 | **NO — congelado; no sustituye** |
| P5 membrana / colesterol | Línea independiente; no rescata P1/P2 | **NO ahora — QUEUED** |

**Lock de identidad:** “Filmar más” = **nuevas trayectorias MD** (o adquisición de depósito público **cualitativamente mayor** en tiempo agregado + réplicas independientes) compatibles con el objeto P2. **No** es desempaquetar más del zip Dutta ni re-correr scripts EXTERNAL.

**Baseline que falló Gate-1 (`2dcff23`):** Morales-Pastor WT CB2–HU-210 GPCRmd pub 1540 / dyn2126 = **5 × ~400 ns ≈ 2 µs** acumulados → **1995 frames** → ITS `NON_CONVERGENT` → `P2_INSUFFICIENT_SAMPLING`. Literature WT ACN = same 5×400 ns scale ([DOI 10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)).

---

## 2. Pregunta que discrimina (única)

¿Un ensemble WT CB2 con **muestreo pre-registrado ≥ Tier B-min** produce un MSM propio con Gate-1 **`CONVERGENT`** bajo los mismos criterios de diagnóstico (ITS finitos / aplanamiento relativo pre-registrado; CK / bootstrap / LOO cuando aplique), de modo que se pueda **reabrir** Stage-1 A/B/C?

| Si Gate-1 pasa | Si Gate-1 falla de nuevo |
|----------------|---------------------------|
| `P2_MSM_TRANSITIONS` puede pasar a interpretación Stage-1 (A/B/C) **solo tras** revisión humana del reporte | Permanece `CLOSED (INSUFFICIENT_SAMPLING)` o se registra `STILL_INSUFFICIENT` — **no** inventar biología |

---

## 3. Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Producción MD / adaptive sampling **pre-registrada** hacia Tier B | Declarar P2 `CONVERGENT` por tener scripts, logs, o ns de equilibration |
| Re-test Gate-1 **solo si** se cumple el target de muestreo registrado | Usar Dutta zip / landmarks / Final_MSM pickles como “más sampling P2” |
| Smoke-test de stack (Docker/CUDA) documentado como **infra**, no como Gate-1 | Abrir P5, docking, de novo, hub hunt, Gi |
| Checklist cluster / Colab / qué debe proveer el PI | Fingir progreso con más análisis EXTERNAL |

```text
P2_MSM_TRANSITIONS     = CLOSED (INSUFFICIENT_SAMPLING)   # until Gate-1 PASSES on registered target
P2_NETWORK_A_B_C       = ABORTED                          # until Gate-1 passes
ARCHITECTURE_A_B_C     = NOT DECIDED
P5_MEMBRANE            = HYPOTHESIS_READY / QUEUED        # NOT started
P5_EXECUTION           = BLOCKED_PENDING_DECISION         # remains
EXTERNAL_CB2_APO       = SYNTHESIS_FROZEN                 # acta 2026-09-13
DUTTA_ZIP_ANALYSIS     = FROZEN                           # not P2 sampling
DEEP_PAUSE             = TRUE                             # lifted ONLY for this scoped campaign
COMPUTATION            = SCOPED_P2_SAMPLING_CAMPAIGN_ONLY
```

**Explicit non-claims (pre-registered):**

1. Este pre-registro **no** reabre P2 como `CONVERGENT`.  
2. Completar Tier A (infra / smoke) **≠** Gate-1.  
3. P5 permanece **QUEUED** — no execution.  
4. Capítulo EXTERNAL Dutta **sigue frozen**.  
5. Credibilidad > pretend MD.

---

## 4. Sistema (locked)

| Campo | Valor |
|-------|--------|
| Objeto científico | **CB2 WT** (UniProt P34972), línea **Morales/GPCRmd-compatible** (agonist-bound WT usado en P2: HU-210 / depósito dyn2126) **o** apo WT **solo si** se pre-registra featurización y se acepta que **no** es el mismo objeto que Gate-1 histórico |
| Default recomendado | **CB2 WT + HU-210** (o ligando del depósito GPCRmd 1540), membrana POPC (o composición GPCRmd), Amber/CHARMM según stack elegido — **documentar FF + box antes de producción** |
| Datos ya locales (análisis only) | `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/` — 5× `.xtc` + PSF/PDB; **~2 µs ya consumidos en Gate-1**; no hay más frames Morales locales |
| Software preferido | **OpenMM CUDA** (repo: `environments/environment-md.yml` / membrane yml; histórico Docker Linux) **o** GROMACS/AMBER en cluster si el PI aporta módulos |
| Featurización Gate-1 retest | **Fija a priori** antes de ver ITS: (A) baseline P2 pairwise TM Cα **o** (B) set X8 24-D — elegir **una** y no retocar post-hoc |

---

## 5. Targets de muestreo (honest tiers)

### Baseline (ya ejecutado — no cuenta como campaña nueva)

| Métrica | Valor |
|---------|--------|
| Tiempo agregado | **~2.0 µs** (5 × ~400 ns) |
| Frames (P2 builder) | **1995** |
| Veredicto | `NON_CONVERGENT` / `INSUFFICIENT_SAMPLING` |

### Tier A — local feasible (infra / smoke only)

| Item | Spec |
|------|------|
| Objetivo | Restaurar stack GPU + **smoke** ≤ **2 ns** de producción (o solo min+equil ≤ 200 ps) en un sistema CB2 reconstruido **si** Docker/CUDA vuelve |
| **No es** | Muestreo para Gate-1 |
| Eligible Gate-1 reopen? | **NO** |
| Walltime (histórico GTX 1060) | Soluble ~57–59 ns/day (OpenMM CUDA Docker); membrana POPC ~2–3× más lento → orden **~20–30 ns/day** |
| Estimación 2 ns smoke (membrana) | ~2–3 h GPU **si** stack CUDA vivo |
| Estado 2026-09-13 | **NO START production** — ver §6 |

### Tier B-min — cluster / Colab (umbral mínimo para **re-test** Gate-1)

| Item | Spec |
|------|------|
| Tiempo agregado **nuevo** | **≥ 20 µs** (≈ **10×** Morales WT usados en P2) |
| Réplicas / semillas | **≥ 20** independientes (adaptive o multi-seed; documentar esquema) |
| Frames (orden) | Depende stride; p.ej. 100 ps → ~2×10⁵ frames; registrar stride real |
| Eligible Gate-1 reopen? | **SÍ — re-test permitido**; convergencia **no garantizada** |
| Walltime GTX 1060 alone | A ~25 ns/day membrana: 20 000 ns ≈ **~800 días GPU** → **no local** |
| Walltime cluster (ej. 8× A100-class) | Orden **días–semanas** según throughput y adaptive overhead |

### Tier B-full — campaña seria (hacia escala landscape)

| Item | Spec |
|------|------|
| Tiempo agregado | **≥ 100 µs** adaptive (orden Dutta-class lower bound; Dutta lit. ~700 µs CB1/CB2 — **aspiracional**, no obligatorio en B-min) |
| Eligible | Re-test Gate-1 + mejor chance de CK/LOO estables |
| Local GTX 1060 | **Inviable** (años) |

**Regla:** Solo tras cumplir el target **registrado** (B-min o B-full) se autoriza re-ejecutar `p2_msm_builder` / pipeline Gate-1. Resultado puede seguir siendo `NON_CONVERGENT` — eso es un resultado válido.

---

## 6. Assessment hardware local (2026-09-13) — honest

| Recurso | Hallazgo |
|---------|----------|
| GPU | **NVIDIA GeForce GTX 1060 6GB** (Driver 536.99 / CUDA 12.2 capability reported by nvidia-smi) |
| CPU / RAM | Intel i5-6600K (4c/4t), **~16 GB** RAM |
| OpenMM nativo Windows | Instalado **8.5.2**; platforms: **Reference / CPU / OpenCL** — **sin CUDA** |
| GROMACS / AMBER CLI | **Ausentes** en PATH |
| micromamba / conda | **No** en PATH (sesión actual) |
| WSL2 | **Roto** (VHDX path not found) |
| Docker | CLI 29.6.2 presente; servicio **`com.docker.service` = Stopped**; daemon socket ausente → **no GPU container hoy** |
| Histórico MD repo | OpenMM CUDA **vía Docker Linux** (~57–59 ns/day soluble CB1); scripts `run_md_openmm_*.py` son **CB1 lead / POPC**, **no** protocolo CB2 Morales P2 |
| Morales traj local | 5× xtc (~74 MB c/u) + PSF/PDB — **análisis only**; sin frames adicionales |

**Veredicto operativo:** local **no** puede producir muestreo **Tier B-min** en tiempo humano razonable. Tier A production smoke **tampoco** puede arrancar hoy sin restaurar Docker (o WSL) + CUDA env + sistema CB2.  
→ **NO se lanza MD de producción en este turno.**  
→ **NO** se finge progreso con más análisis Dutta.

---

## 7. Checklist — qué debe proveer el PI / infra (Tier B)

Marcar antes de producción pesada:

- [ ] Acceso cluster **o** Colab Pro / cloud GPU (A100/L40S-class preferible; T4/V100 solo para smoke)
- [ ] Módulo o container: OpenMM+CUDA **o** GROMACS/AMBER + tipología documentada
- [ ] Estructura de partida CB2 WT (PDB/GPCRmd) + ligando (HU-210 si se replica objeto P2) + membrana
- [ ] Presupuesto: **≥ 20 µs** (B-min) wall-clock estimado firmado
- [ ] Almacenamiento traj (xtc/dcd/nc) + backups; manifiesto SHA
- [ ] Featurización Gate-1 elegida (P2-TM vs X8) **antes** de ver ITS
- [ ] Criterios Gate-1 re-copiados de `p2_msm_builder` / pre-reg P2 (sin retune post-hoc)
- [ ] Confirmación escrita: P5 sigue QUEUED; EXTERNAL Dutta frozen

**Colab nota:** viable para **pilotos ns–décenas de ns** y aprendizaje de setup; **B-min 20 µs** suele exigir cluster o campaña multi-sesión muy larga — no prometer Colab free como solución B-min.

---

## 8. Cloud options (survey 2026-09-13)

Survey for PI (Spain/EU): paid GPU rental vs academic HPC for **Tier B-min ≥ 20 µs** membrane GPCR OpenMM/GROMACS. Prices fluctuate; re-check before purchase. **No accounts created in this survey.**

### Throughput assumptions (order-of-magnitude)

| Sistema | GPU típica | ns/day (orden) | Fuente / nota |
|---------|------------|----------------|---------------|
| Soluble pequeño (~44k átomos) | L40S / A100 | ~250–550 | Shadeform/SimAtomic OpenMM 2025 |
| ApoA1-class / membrana media | A100 / RTX 4090 | ~100–400+ | OpenMM org benchmarks (PME) |
| **CB2 GPCR + POPC (este experimento)** | A100 / L40S / 4090 | **~100–300** (usar **150–200** en presupuesto) | Escala respecto GTX 1060 local ~20–30 ns/day membrana; **benchmarkear 1–2 ns en el cloud elegido** |
| Walltime 20 000 ns @ 200 ns/day | 1 GPU | **~100 GPU-días** (~3–4 meses 1×GPU; ~1–2 sem con 8×GPU paralelas / multi-réplica) | Réplicas ≥20 → paralelizar |

**Coste B-min (orden, USD 2026):** RTX 4090 @ ~$0.35–0.70/h → **~$800–1 700** por 20 µs serial; A100 @ ~$1.2–1.8/h → **~$3 000–6 000**. Hyperscalers (AWS/GCP/Azure) suelen **2–4×** más caros. Colab Pro/Pro+ **no** cubre 20 µs continuo de forma realista.

### Comparativa corta

| Opción | Rol vs 20 µs | Precio/h (orden) | Notas PI EU |
|--------|--------------|------------------|-------------|
| **Colab Free** | Solo smoke corto | $0 | ≤~12 h/sesión; GPU no garantizada |
| **Colab Pro (~$10/mo) / Pro+ (~$50/mo)** | Piloto / setup | Unidades de cómputo | Pro+ hasta ~24 h background; A100 quema unidades rápido; **insuficiente solo para B-min** |
| **RunPod** | **Primario pagado** | 4090 ~$0.34–0.69; A100 ~$1.2–1.8 | UI simple, pods persistentes, región EU; templates nvidia+CUDA |
| **Vast.ai** | Trial barato / spot | 4090 desde ~$0.1–0.5; A100 variable | Marketplace; **checkpoint obligatorio**; fiabilidad uneven |
| Paperspace (DO Gradient) | Notebook cómodo | A100 ~$3.1–3.2 + plan Growth | Caro vs RunPod para MD largo |
| Lambda Labs | Fiable, ML-oriented | A100 ~$1.3–1.8 | Buena UX; poca/no región EU tipificada |
| CoreWeave | Enterprise / multi-GPU | A100 ~$2.7/GPU (nodos 8×) | Overkill / caro para lab pequeño |
| AWS g5 / p3 / p4 | Compliance / org | g5 ~$1+/h; p3.2xl ~$3; p4d 8×A100 ~$22–33 | EU (Ireland etc.); premium; Spot ayuda |
| GCP / Azure GPU | Idem + créditos | A100 on-demand ~$3–4/h típico | GCP Research Credits: faculty hasta ~$5k (España elegible) |
| **RES (Red Española de Supercomputación)** | **Primario académico** | **Gratis** (calls) | PI EU/ES; HPC + AI/GPU; calls ~6 meses + **fast-track** semanal; [res.es](https://www.res.es/) |

### Recomendación operativa

1. **Primario (gratis, si timeline lo permite):** solicitud **RES** (HPC o AI/GPU) — URL/España encaja; fast-track para smoke, ordinary call para campaña ≥20 µs.  
2. **Primario pagado (arrancar ya):** **RunPod** Secure Cloud — 1× **RTX 4090** o **L40S**, imagen nvidia + OpenMM (o GROMACS), volume persistente, checkpoint cada 5–10 ns; escalar a N pods = N réplicas.  
3. **Trial barato (esta semana):** **Vast.ai** 4090 2–10 ns **o** Colab Pro smoke ≤2 ns — medir **ns/day reales** del sistema CB2 antes de comprometer presupuesto B-min.  
4. **No** planificar B-min solo con Colab; **no** AWS/GCP on-demand como primera opción de coste.

---

## 9. Failure modes (pre-registered)

| Modo | Lectura | Acción |
|------|---------|--------|
| Stack local no restaura CUDA | Tier A blocked | Permanecer en checklist cluster; no OpenCL “producción” como fake CUDA |
| Smoke 2 ns OK, sin Tier B | Infra validada only | **No** tocar label P2 |
| Tier B-min producido, ITS aún `NON_CONVERGENT` | Sampling still insufficient **or** landscape needs B-full / adaptive | Registrar `STILL_INSUFFICIENT`; human decision B-full vs stop |
| Adaptive sesgado / undersampled basins | CK/LOO fallan | No A/B/C; report diagnostics only |
| Tentación Dutta zip | Fuera de objeto | **Forbidden** under this campaign |
| Abrir P5 “mientras tanto” | Violación prioridad PI | P5 stays QUEUED |

---

## 10. Gate-1 retest criteria (when Tier B met)

Reuse Stage-0 spirit from [`P2_STATE_ROUTE_PREGISTRATION.md`](P2_STATE_ROUTE_PREGISTRATION.md) + builder `@ 2dcff23`:

1. ITS spectrum: lags con timescales finitos/positivos; **no** colapso patológico de connected states.  
2. Relative flattening criterion as implemented in builder (document numeric threshold in run MANIFEST **before** run).  
3. Optional: bootstrap metastable stability + LOO across replicas.  
4. Soft CK **does not** override failed ITS (same lock as EXTERNAL own MSM).

| Outcome label | Meaning |
|---------------|---------|
| `P2_GATE1_CONVERGENT` | May proceed to Stage-1 A/B/C **after human review** |
| `P2_GATE1_STILL_INSUFFICIENT` | Sampling campaign completed target but Gate-1 fails |
| `P2_GATE1_NOT_RUN` | Target not met (current state) |

**Until `P2_GATE1_CONVERGENT`:** `P2_MSM_TRANSITIONS` remains **`CLOSED (INSUFFICIENT_SAMPLING)`**.

---

## 11. Campaign status snapshot

```yaml
EXPERIMENT: P2_MASSIVE_SAMPLING
PREREG_DATE: 2026-09-13
PI_DECISION: MASSIVE_SAMPLING_FIRST
P5: QUEUED_NOT_STARTED
EXTERNAL_DUTTA: FROZEN
TIER_A_PRODUCTION_TODAY: NOT_STARTED  # Docker stopped; no CUDA OpenMM; WSL broken
TIER_B: CHECKLIST_LOCKED_AWAITING_CLUSTER
P2_REOPEN_AS_CONVERGENT: FALSE
ACTIVE_ACTION: DOCS_PREREG_PLUS_INFRA_CHECKLIST
CLOUD_SURVEY: 2026-09-13  # §8 RunPod primary paid; RES primary academic; Colab/Vast trial only
```

---

*Fin pre-registro. Credibilidad > pretend MD. “Adelante” autoriza la **ruta** de muestreo; no autoriza mentir sobre ns locales.*

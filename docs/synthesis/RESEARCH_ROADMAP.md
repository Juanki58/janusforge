# RESEARCH ROADMAP — contrato científico CB2 (P1–P6)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — contrato científico; sin docking, sin de novo, sin download/ejecución de trayectorias, sin MD nuevo  
**Autoridad de freeze / flags:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) (`RESEARCH_STATUS = ROADMAP_ACTIVE_PREP`)  
**Pre-registro técnico P1:** [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) · `P1_NULL` en [`scripts/network_core/dynamic_pipeline.py`](../../scripts/network_core/dynamic_pipeline.py)  
**Self-test seco (andamiaje):** `python scripts/network_core/dynamic_pipeline.py --self-test` (tip técnico `b91b57c`)  
**Alias legado:** [`CB2_RESEARCH_ROADMAP.md`](CB2_RESEARCH_ROADMAP.md) → redirige aquí (evitar duplicación)

---

## Objetivo (qué es / qué no es)

**Sí:** construir un **mapa causal de CB2** que sobreviva **falsificación sucesiva** (P1→P5). Cada puerta cierra o abre la siguiente. El resultado válido puede ser switch local, red distribuida, o arquitectura estado-dependiente.

**No:** encontrar una molécula. **P6 no existe** hasta que P1–P5 sobrevivan. P6 solo pregunta qué **perturbación química** mueve una red **ya mostrada** como controladora de salida funcional.

```
PRIMARY_OBJECTIVE = CHARACTERIZE_CB2_CONFORMATIONAL_CONTROL
≠ “find the switch”
≠ “find a ligand”
```

---

## Árbol de decisión (contrato)

```
P1  ¿Los hubs sobreviven dinámicamente?
    │
    ├─ NO  → cerrar hipótesis de hubs (como núcleo dinámico)
    │
    └─ YES → P2
              ¿La arquitectura cambia entre microestados?
              │
              ├─ NO  → red aproximadamente estable
              │         (candidato a subred fija; P3 opcional / lit.)
              │
              └─ YES → P3
                        ¿Los cambios se relacionan con Gαi2?
                        │
                        ├─ NO  → arquitectura sin vínculo funcional demostrado
                        │
                        └─ YES → P4
                                  ¿CB1 es distinto?
                                  │
                                  ├─ NO  → base débil de selectividad conformacional
                                  │
                                  └─ YES → P5
                                            ¿La membrana modifica?
                                            │
                                            ├─ NO  → Nivel A suficiente
                                            │
                                            └─ YES → P6
                                                      ¿Puede una perturbación química desplazar?
                                                      (solo si P1–P5 sobrevivieron)
```

**Regla dura:** no saltar puertas; no abrir P6 compute (docking / de novo / diseño) mientras P1–P5 no estén resueltas en el sentido del árbol.

---

## Cuatro historias P1/P2 (no elegir a priori)

Cualquiera es resultado científico válido. **No** se prefiere “persistent” sobre las demás.

| Historia | Lectura breve |
|----------|----------------|
| **Persistent** | Hubs / rutas estables en ambas redes y entre estados → subred aproximadamente fija |
| **Persistent + plastic** | Núcleo persistente con rutas que se redistribuyen → control + plasticidad |
| **Highly distributed** | Null no separa / flujo no concentrado → sin core prefabricado usable |
| **State-specific** | Supervivencia o rutas solo en algunos microestados / metaestables |

Estas historias se discriminan con el protocolo dinámico (dos redes; outcomes pre-registrados), no con narrativa post hoc.

---

## Gate P1 (único criterio de entrada al árbol)

Los hubs estáticos deben **vencer un null estructura-compatible pre-definido** y pasar **reproducibilidad** entre réplicas / estados.

| Elemento | Fuente canónica (no inventar otro null) |
|----------|------------------------------------------|
| Null | `P1_NULL` en `scripts/network_core/dynamic_pipeline.py` |
| Nombre | `exact_in_out_degree_multiset_match` |
| Métrica primaria | `pct_disconn` (cola superior) |
| α | `0.05` |
| Repro | Spearman rank hubs ≥ `0.7` entre réplicas/estados; si falla → `INDETERMINATE`, **no** retocar α |
| Protocolo | [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) |
| CLI | `dynamic_pipeline.py --self-test` · `run_dynamic_hub_persistence.py` (bloqueado sin traj) |

**Prohibido en P1:** `W = -ln(p)` universal; umbral a priori “>50% del flujo”; retuning de α / lista de hubs tras ver traj; llamar al resultado “switch”.

**Estado ahora:** **P1 COMPLETE** (`P1_NOT_SUPPORTED`) on GPCRmd/1540 WT only — artifacts `results/network_core/p1_dynamic_hub_validation.{json,md}`; CLI `scripts/network_core/p1_dynamic_hub_validation.py`. **P2–P6 BLOCKED** (Dutta–Shukla MSM data debt). STOP for joint review — no auto-P2.

---

## Puertas P1–P6 (una pregunta = una puerta)

### P1 — ¿Los hubs sobreviven dinámicamente?

**Pregunta:** ¿Los seis hubs del mapa estático son nodos dinámicos reales (persistencia **y** comunicación), o artefactos del grafo agregado?

**Si NO:** cerrar hipótesis de hubs como núcleo dinámico.  
**Si YES:** abrir P2.

**Contexto repo (ya cerrado en estático):** Test A bottleneck **SUPPORTED**; Test B PrefCoup Gαi2 **NOT_SUPPORTED** → `STATIC_LIGACN = CORE_TOPOLOGICAL_ONLY` (`cfb2a51`). Eso **no** responde P1.

Hubs fijos a priori: ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46).

**Resultado P1 (2026-08-21, GPCRmd only):** **`P1_NOT_SUPPORTED`**. Channels A/B kept separate. Neither channel exceeded pre-registered null with reproducibility. Suggested story (non-forced): **distributed**. P1 does **not** answer Gi / CB1 / MSM / membrane / chemical switch. **P2 not opened.**

### P2 — ¿La arquitectura cambia entre microestados? **BLOCKED** (MSM debt)

**Pregunta:** ¿La comunicación es una subred fija o se redistribuye entre metaestables / microestados?

**Si NO:** red aproximadamente estable.  
**Si YES:** abrir P3 (cambios a interpretar funcionalmente).

No elegir a priori entre las cuatro historias de arriba.

### P3 — ¿Los cambios se relacionan con Gαi2?

**Pregunta:** ¿Nodos/rutas dinámicas se enriquecen hacia lectura Gαi2 (y/o β-arr), sin afirmar switch?

**Si NO:** arquitectura física sin vínculo funcional demostrado (extiende Test B al régimen dinámico).  
**Si YES:** abrir P4.

`CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` hasta evidencia dinámica + revisión humana (nunca automática).

### P4 — ¿CB1 es distinto?

**Pregunta:** ¿El control conformacional CB2 es específico de receptor o compartido con CB1?

**Si NO:** base débil de selectividad conformacional CB2-vs-CB1.  
**Si YES:** abrir P5.

`CB1_COMPARISON = BLOCKED` hasta desbloqueo explícito + datos.

### P5 — ¿La membrana modifica?

**Pregunta:** `Q_membrana` — ¿la arquitectura de P1–P4 es intrínseca (Nivel A) o gobernada por microdominios lipídicos (Nivel B)?

**Si NO:** Nivel A suficiente.  
**Si YES:** abrir P6 (química en contexto de membrana).

Gobernanza: Nivel A = `ACTIVE_BASELINE`; Nivel B = `FUTURE_PRIORITY_HYPOTHESIS` (= esta puerta); Nivel C archivado; `Q_MEMBRANA = PARKED` (`c2869b0`).

### P6 — ¿Puede una perturbación química desplazar?

**Pregunta:** ¿Qué intervención química mueve la red / equilibrio hacia un estado funcional concreto **en un contexto ya caracterizado**?

**P6 no existe hasta que P1–P5 sobrevivan.**  
No es “mejor pose” ni campaña de docking/de novo. `DOCKING` / `DE_NOVO` = **STOP**.

---

## Linaje empírico → árbol (no circular)

```
Phase G (MACRO) 🟢 GENERALIZES
        │
        ▼
Phase H / micronetwork 🟡 INDETERMINATE  ──► alimenta P2
        │
        ▼
Static LigACN + 6 hubs 🟢 bottlenecks
        │
        ▼
Dual validation cfb2a51
  A 🟢 topological · B 🔴 PrefCoup
  → CORE_TOPOLOGICAL_ONLY ──► cierra “6 hubs = switch Gi”
        │
        ▼
P1     DONE → P1_NOT_SUPPORTED (GPCRmd/1540 WT; A⊥B)
P2–P3  BLOCKED (Dutta–Shukla MSM missing — do NOT invent states from Morales)
P4     BLOCKED
P5     Q_membrana PARKED = Nivel B
P6     no abierto (docking/de novo STOP)
```

Anclas: `cfb2a51` · `c2869b0` · `2a1193c` · tip técnico pipeline seco `b91b57c` · P1 real `p1_dynamic_hub_validation`.

---

## Índice cruzado

| Documento | Rol |
|-----------|-----|
| [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Flags / freeze (`ROADMAP_ACTIVE_PREP`) |
| [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) | Pre-registro P1–P3 + `P1_NULL` |
| [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) | Morales-Pastor, Dutta–Shukla, Trp258 |
| [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) | Smoum / Ganzoni; microestados |
| [`DOCKING_LIMITS_AND_GOVERNANCE.md`](DOCKING_LIMITS_AND_GOVERNANCE.md) | Por qué P6 ≠ docking score |
| Dual validation report | Ancla `cfb2a51` — entrada estática a P1/P3 |
| `results/network_core/p1_dynamic_hub_validation.md` | **P1 verdict** (GPCRmd only) |

---

## Próximo paso

1. **Joint review of P1** (`P1_NOT_SUPPORTED`) — STOP; no auto-P2.  
2. **P2–P6 remain BLOCKED** until Dutta–Shukla MSM (explicit data debt).  
3. **No** docking / de novo / MD nuevo / threshold retuning / Gαi2 reinterpretation.  
4. Author email = parallel contingency only (do not send for P1).

---

*Fin RESEARCH_ROADMAP.md — contrato científico: mapa causal por falsificación sucesiva, no búsqueda de molécula.*

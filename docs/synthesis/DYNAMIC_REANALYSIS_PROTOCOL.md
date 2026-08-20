# Protocolo — reanálisis dinámico CB2 (pre-registro computacional)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `COMPUTATIONAL_PREREGISTRATION / DATA_BLIND`  
**Estado:** Metodología **congelada antes** de ver trayectorias reales. Valor máximo del pre-registro = data-blind.  
**Ancla:** `RESEARCH_STATE.md` → `ARCHIVED_NEXT_CALCULATION` / `DYNAMIC_REANALYSIS` (`17c8a28` + andamiaje).  
**Histórico estático:** [`MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](MINIMAL_CORE_REANALYSIS_PROTOCOL.md).  
**Roadmap (contrato científico):** [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md) P1–P3 · alias [`CB2_RESEARCH_ROADMAP.md`](CB2_RESEARCH_ROADMAP.md).

### Gobernanza

```yaml
MODO: COMPUTATIONAL_PREREGISTRATION / DATA_BLIND
DYNAMIC_REANALYSIS: BLOCKED_PENDING_TRAJECTORIES
TRAJ_DOWNLOAD: STOP
NEW_MD: STOP
NEW_DOCKING: STOP
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP   # includes alpha, hub list, null rule
CONTRACT_v1.0: ARCHIVED_HISTORICAL
```

1. **Ningún** criterio / peso / umbral / lista de hubs se modifica tras ver traj reales.
2. Nunca llamar al resultado **“switch”**.
3. Sin `.xtc` / MSM locales → `BLOCKED_PENDING_TRAJECTORIES` / `INDETERMINATE` (fail closed).
4. Tests sintéticos **sí** se ejecutan ahora (validan el null y la separación de redes) — **no** sustituyen traj reales.

---

## Pipeline congelado (orden fijo)

```
TRAJECTORIES
    → normalize / select frames
    → PERSISTENCE NET     W_contact = f(p_ij)
    → COMMUNICATION NET   W_info = f(correlation / MI [/ TE])
    → microstates / MSM
    → centrality + paths + robustness
    → mutagenesis cross          (P3)
    → CB1 comparison             (P4)
    → optional membrane module   (P5, PARKED)
```

**Prohibido:** colapsar a `W = -ln(p)` universal; mezclar métricas de persistencia y comunicación; umbral a priori “>50% del flujo”.

---

## Preguntas P1–P3 (técnicas)

| Código | Pregunta |
|--------|----------|
| **P1** | ¿Persisten los seis hubs estáticos en **ambas** redes? |
| **P2** | ¿Cambian las rutas entre microestados / metaestables? |
| **P3** | ¿Los nodos dinámicos se relacionan con Gi / β-arrestin? |

**Framing primario:** ¿subred persistente o redistribución dinámica? — **no** “¿dónde está el switch?”

---

## Hubs / S / T (fijos a priori)

| Hubs | ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46) |
|------|----------------------------------------------------------------------------------|
| **S** | `8D0:1`, `SER:285`, `PHE:87` |
| **T** | `ARG:131`, `ASP:240`, `SER:303`, `SER:69` |
| **AUSENTE** | `TRP:258`, `PHE:183` (no forzar) |

---

## P1 null (pre-definido en código — no inventar post hoc)

Definido en `scripts/network_core/dynamic_pipeline.py` → `P1_NULL`:

| Campo | Valor congelado |
|-------|-----------------|
| Estructura | `exact_in_out_degree_multiset_match` |
| Métrica primaria | `pct_disconn` (cola superior) |
| α | `0.05` |
| Reproducibilidad | Spearman rank hubs ≥ `0.7` entre réplicas/estados; si falla → `INDETERMINATE`, **no** retocar α |

También: estabilidad réplica/estado documentada; outcomes solo de la tabla § Outcomes.

---

## Outcomes pre-registrados

| Código | Uso |
|--------|-----|
| `HUBS_SURVIVE_BOTH_NETWORKS` | Hubs en ambas redes + estabilidad |
| `STATE_SPECIFIC` | Supervivencia estado-dependiente |
| `SUBSTITUTED_ROUTES` | Persistencia ≠ comunicación / rutas alternativas |
| `REDUNDANT_DISTRIBUTED` | Null no separa |
| `INDETERMINATE` | Datos / mapeo / repro irresoluble |
| `BLOCKED_PENDING_TRAJECTORIES` | Paths reales ausentes (**ahora**) |

---

## Inputs reales esperados (cuando existan)

```
data/external/morales_pastor_2025/trajectories/   # .xtc/.dcd + topología + MANIFEST.json
data/external/dutta_shukla_2023/msm/              # MSM/features + MANIFEST.json
```

Marcadores: `MANIFEST.json` **o** archivos `.xtc/.dcd/.trr/.nc/.h5/.pdb/.gro/.tpr`.  
Hoy: ausentes → status JSON `BLOCKED_PENDING_TRAJECTORIES`.

Deps opcionales (guardadas): MDAnalysis (traj), PyEMMA (MSM). No requeridas para self-tests.

---

## Self-tests sintéticos (obligatorios ahora)

Demuestran, **sin** traj reales:

1. Red sin señal → no falsos hubs (p ≥ α)
2. Bottleneck plantado → se recupera (p < α, flujo alto)
3. Null degree-matched: FPR no inflada
4. Persistencia vs comunicación no mezcladas
5. Microestados estables a seed / orden de frames (perm. de etiquetas OK)

```bash
python scripts/network_core/dynamic_pipeline.py --self-test
# o (status + self-test)
python scripts/network_core/dynamic_pipeline.py --self-test --status
```

Artefactos: `results/network_core/dynamic_pipeline_selftest.json`, `dynamic_reanalysis_status.json`.

---

## CLIs

| Script | Rol |
|--------|-----|
| `scripts/network_core/dynamic_pipeline.py` | Pipeline seco + null + self-tests |
| `scripts/network_core/prepare_dynamic_reanalysis.py` | Gate de paths / status |
| `scripts/network_core/run_dynamic_hub_persistence.py` | Entry P1 (bloqueado sin traj) |

Cuando lleguen traj reales: **press play** — cero retuning post hoc.

---

*Fin pre-registro. Citar este archivo como locked protocol en cualquier cómputo dinámico futuro.*

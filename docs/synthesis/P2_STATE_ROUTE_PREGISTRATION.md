# P2 pre-registration — own GPCRmd MSM → A/B/C (two-stage)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `COMPUTATIONAL_PREREGISTRATION / DATA_BLIND`  
**Estado:** **DRY FROZEN** (synthetic pipeline) — **real MSM NOT EXECUTED** (await human green light)  
**Parent protocol:** [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md)  
**Roadmap / state:** [`RESEARCH_ROADMAP.md`](RESEARCH_ROADMAP.md) · [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md)  
**Dry CLI:** `scripts/network_core/p2_dry_pipeline.py` · tests: `tests/test_p2_pipeline.py`  
**Optional external lit. deposit (not P2 input):** [`DATA_REQUEST_DUTTA_SHUKLA_MSM.md`](DATA_REQUEST_DUTTA_SHUKLA_MSM.md)

---

## Official reformulation (PI lock)

**P2 = own MSM** built on the **5 WT GPCRmd Morales-Pastor trajectories** (dyn2126 / GPCRmd pub 1540), **independent** of Dutta & Shukla MSM.

```
5 GPCRmd WT trajs → fixed featurization → tICA → lag selection → MSM
→ convergence + bootstrap + LOO
→ INSUFFICIENT_SAMPLING | interpretable MSM → metastable states → A/B/C
```

### Hard rule — Dutta is not a template

| Allowed | Forbidden |
|---------|-----------|
| Dutta & Shukla as **external comparison later** (after own MSM) | Using Dutta as fitting target / template (“must recover 6 states”) |
| Own K (e.g. 4 vs 6) if justified by **our** convergence diagnostics | Treating different state counts as automatic error vs Dutta |

---

## Two decision stages (mandatory)

### Stage 0 — Is the MSM statistically interpretable and sufficiently convergent?

Diagnostics (pre-registered conceptually; dry uses synthetic mocks):

- Implied timescale gap / spectral gap proxy  
- Bootstrap stability of metastable partitioning  
- Leave-one-traj-out (LOO) agreement across the 5 WT replicas  

| Outcome | Action |
|---------|--------|
| **No** | `INSUFFICIENT_SAMPLING` → **STOP** — do **not** invent an A/B/C story |
| **Yes** | `MSM_INTERPRETABLE` → proceed to Stage 1 |

### Stage 1 — Only if Stage 0 passes: what architecture A/B/C emerges?

| Code | Claim |
|------|--------|
| `ESCENARIO_A` (Stable) | Dominant topological routes **invariant** (>80% overlap across metastable states); intensity may change |
| `ESCENARIO_B` (Routes by state) | Significant edge variance; each microstate distinct vs nulls |
| `ESCENARIO_C` (Distributed) | No reproducible dominant routes in any state (signal diluted) |

Object: **transition / changing edges**, not permanent hubs (`NO_NEW_HUBS`).

---

## Gobernanza

```yaml
P2_OBJECT: OWN_MSM_GPCRMD_WT_THEN_ABC
P2_DATA_SOURCE: morales_pastor_2025_gpcrmd_wt_5traj
P2_EXECUTION_REAL: BLOCKED_PENDING_HUMAN_GREEN_LIGHT
P2_DRY: FROZEN_SYNTHETIC_ONLY
DUTTA_SHUKLA: EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE
P5_EXECUTION: BLOCKED_PENDING_DECISION
NEW_HUB_HUNT: STOP
NEW_DOCKING: STOP
DE_NOVO_GENERATION: STOP
NO_REAL_DATA_IN_DRY: true
NO_INTERNET: true
```

**Strategic lock:** P2 first, P5 after. Do **not** open P5 because Stage 0 fails.

---

## Real P2 inputs (when unparked — not this turn)

| Item | Value |
|------|--------|
| Trajectories | 5× WT GPCRmd Morales-Pastor (local: `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/`) |
| Topology | companion PDB/PSF from same deposit |
| Featurization | **fixed a priori** before seeing A/B/C (document in MANIFEST when unparked) |
| MSM stack | tICA → lag selection → MSM → CK / bootstrap / LOO |
| Dutta deposit | optional later comparison only |

---

## Dry pipeline (current freeze)

Synthetic only — **never** opens `.xtc`:

1. `mock_msm_convergence_gate` → `INSUFFICIENT_SAMPLING` | `MSM_INTERPRETABLE`  
2. If proceed: mock frame→state labels → persistence + communication nets  
3. Classify `ESCENARIO_A` / `B` / `C` with degree-matched nulls + ≥3-replica edge intersection  

```bash
python -m pytest tests/test_p2_pipeline.py -v
python scripts/network_core/p2_dry_pipeline.py --self-demo
```

---

## Outcomes (pre-registered)

| Code | Meaning |
|------|---------|
| `INSUFFICIENT_SAMPLING` | Stage 0 fail — stop |
| `ESCENARIO_A` / `B` / `C` | Stage 1 architecture call |
| `INDETERMINATE` | Stage 1 gates / repro fail |
| `BLOCKED_PENDING_HUMAN_GREEN_LIGHT` | Real MSM not started |

### Downstream (do not execute here)

| Call | Next (human review) |
|------|---------------------|
| A | P3 optional / lit. |
| B | Consider P3 on **changing** routes |
| C | No prefabricated core; no hub hunt |
| Insufficient sampling | Stay paused — never open P5 as substitute |

---

*Fin P2 pre-registro. Dry frozen; real GPCRmd MSM awaits human green light.*

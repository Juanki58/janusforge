# P2 pre-registration — own GPCRmd MSM → A/B/C (two-stage)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `COMPUTATIONAL_PREREGISTRATION / DATA_BLIND`  
**Estado:** **`P2 = READY_FOR_EXECUTION`** — dry frozen at tip `aaeec78`; **real MSM NOT EXECUTED**  
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
→ P2_INSUFFICIENT_SAMPLING | interpretable MSM → metastable states → A/B/C
```

### Hard rule — Dutta is not a template

| Allowed | Forbidden |
|---------|-----------|
| Dutta & Shukla as **external comparison later** (after own MSM) | Using Dutta as fitting target / template (“must recover 6 states”) |
| Own K (e.g. 4 vs 6) if justified by **our** convergence diagnostics | Treating different state counts as automatic error vs Dutta |

**Dutta’s 6 states do not condition the analysis.**

---

## Gate structure (locked)

```
1. Own MSM converges?
   NO  → P2_INSUFFICIENT_SAMPLING → STOP
   YES → 2
2. Architecture:
   A RED_ESTABLE | B RUTAS_POR_ESTADO | C DISTRIBUIDA
```

**First real result to review = convergence**, not a preferred biological story.

### Stage 0 — Is the MSM statistically interpretable and sufficiently convergent?

Diagnostics (pre-registered conceptually; dry uses synthetic mocks):

- Implied timescale gap / spectral gap proxy  
- Bootstrap stability of metastable partitioning  
- Leave-one-traj-out (LOO) agreement across the 5 WT replicas  

| Outcome | Action |
|---------|--------|
| **No** | `P2_INSUFFICIENT_SAMPLING` → **STOP** — do **not** invent an A/B/C story |
| **Yes** | `MSM_INTERPRETABLE` → proceed to Stage 1 |

### Stage 1 — Only if Stage 0 passes: what architecture A/B/C emerges?

| Code | Label | Claim |
|------|--------|--------|
| `ESCENARIO_A` | **RED_ESTABLE** | Dominant topological routes **invariant** (>80% overlap across metastable states); intensity may change |
| `ESCENARIO_B` | **RUTAS_POR_ESTADO** | Significant edge variance; each microstate distinct vs nulls |
| `ESCENARIO_C` | **DISTRIBUIDA** | No reproducible dominant routes in any state (signal diluted) |

Object: **transition / changing edges**, not permanent hubs (`NO_NEW_HUBS`).

---

## Gobernanza

```yaml
P2: READY_FOR_EXECUTION  # dry frozen at aaeec78; NOT executed
P2_OBJECT: OWN_MSM_GPCRMD_WT_THEN_ABC
P2_DATA_SOURCE: morales_pastor_2025_gpcrmd_wt_5traj
P2_EXECUTION_REAL: NOT_EXECUTED  # READY_FOR_EXECUTION ≠ started
P2_DRY: FROZEN_AT_aaeec78
DUTTA_SHUKLA: EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE  # 6 states do not condition analysis
P1_HUB_HYPOTHESIS: CLOSED
P3: BLOCKED_UNTIL_LANDSCAPE_KNOWN
P4: BLOCKED_UNTIL_LANDSCAPE_KNOWN
P5: INDEPENDENT_MEMBRANE_LINE  # HYPOTHESIS_READY; no execution
P6: FAR
P5_EXECUTION: BLOCKED_PENDING_DECISION
NEW_HUB_HUNT: STOP
NEW_DOCKING: STOP
DE_NOVO_GENERATION: STOP
NO_REAL_DATA_IN_DRY: true
NO_INTERNET: true
FIRST_RESULT_TO_REVIEW: CONVERGENCE_NOT_BIOLOGICAL_STORY
```

**Strategic lock:** P1 closed the hub hypothesis. P3/P4 blocked until landscape known. P5 = independent membrane line. P6 far. Do **not** open P5 because Stage 0 fails.

---

## Real P2 inputs (when executed — not this docs-only turn)

| Item | Value |
|------|--------|
| Trajectories | 5× WT GPCRmd Morales-Pastor (local: `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/`) |
| Topology | companion PDB/PSF from same deposit |
| Featurization | **fixed a priori** before seeing A/B/C (document in MANIFEST when started) |
| MSM stack | tICA → lag selection → MSM → CK / bootstrap / LOO |
| Dutta deposit | optional later comparison only |

---

## Dry pipeline (frozen at `aaeec78`)

Synthetic only — **never** opens `.xtc`:

1. `mock_msm_convergence_gate` → `P2_INSUFFICIENT_SAMPLING` | `MSM_INTERPRETABLE`  
2. If proceed: mock frame→state labels → persistence + communication nets  
3. Classify `ESCENARIO_A` (**RED_ESTABLE**) / `B` (**RUTAS_POR_ESTADO**) / `C` (**DISTRIBUIDA**) with degree-matched nulls + ≥3-replica edge intersection  

```bash
python -m pytest tests/test_p2_pipeline.py -v
python scripts/network_core/p2_dry_pipeline.py --self-demo
```

---

## Outcomes (pre-registered)

| Code | Meaning |
|------|---------|
| `P2_INSUFFICIENT_SAMPLING` | Stage 0 fail — stop |
| `ESCENARIO_A` / `B` / `C` | Stage 1: RED_ESTABLE / RUTAS_POR_ESTADO / DISTRIBUIDA |
| `INDETERMINATE` | Stage 1 gates / repro fail |
| `READY_FOR_EXECUTION` | Dry frozen; real MSM **not** started |

### Downstream (do not execute here)

| Call | Next (human review) |
|------|---------------------|
| A RED_ESTABLE | P3 optional / lit. |
| B RUTAS_POR_ESTADO | Consider P3 on **changing** routes |
| C DISTRIBUIDA | No prefabricated core; no hub hunt |
| `P2_INSUFFICIENT_SAMPLING` | Stay paused — never open P5 as substitute |

---

*Fin P2 pre-registro. `P2 = READY_FOR_EXECUTION` (dry frozen at `aaeec78`); real GPCRmd MSM **NOT EXECUTED**.*

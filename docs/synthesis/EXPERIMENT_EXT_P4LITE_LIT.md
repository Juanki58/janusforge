# Experiment — EXTERNAL P4-lite: CB1≠CB2 / AEA asymmetries already closed in literature

**Fecha pre-registro:** 2026-09-22  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — lit-only; **no trajectories**.  
**Scope:** **`EXTERNAL_P4LITE_LIT`** — inventariar qué asimetrías CB1≠CB2 (activación + AEA binding) ya están **cerradas en papers** antes de desbloquear P4 compute.  
**PI authorization:** YES ([`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md) §3 fila P4-lite).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Síntesis paper+readme de asimetrías publicadas | Descargar / unpack `CB*_ana_bind.zip` (85–93 GB) |
| Citar MSM/VAMPnet claims de Dutta–Shukla como **lit.** | Reabrir P4 como compute; afirmar que lit. **es** nuestro P4 |
| Veredicto `EXT_P4LITE_*` | Reabrir P2; docking; Gi efficacy |

```text
P4_CB1_COMPARISON               = BLOCKED                      # unchanged (compute)
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)
EXT_KINETICS_CB1_CB2_DISTINCT   = prior EXTERNAL (pickles)     # soft support only
EXT_P4LITE_*                    = NEW (this experiment)
TRAJECTORIES_AEA                = NOT_DOWNLOADED
```

**Explicit non-claim:**

> “Cerrado en literatura” ≠ “P4 del repo COMPLETE”.  
> P4 propio sigue BLOCKED hasta decisión humana de compute CB1.  
> Este doc evita reinventar asimetrías ya publicadas.

**Pregunta discriminante:**

> ¿Qué hipótesis CB1≠CB2 (pipelines de activación; mecanismos de entrada AEA) están ya **resueltas en lit.** de modo que P4 compute, si algún día se abre, debe **discriminar otra cosa** (p.ej. red propia Janusforge) en vez de redescubrir toggle/pipelines/AEA?

---

## Source set (locked)

| # | Paper | DOI | Role |
|---|-------|-----|------|
| 1 | Dutta & Shukla 2023 activation MSM | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) | CB1≠CB2 activation / pipelines / toggle |
| 2 | Dutta & Shukla AEA binding 2026 | [10.1016/j.jbc.2026.111434](https://doi.org/10.1016/j.jbc.2026.111434) | AEA entry / selectivity |
| 3 | Illinois Data Bank readme | [IDB-6705697](https://databank.illinois.edu/datasets/IDB-6705697) | Metadata only (no unpack) |
| 4 | Dutta et al. 2022 Na+ | [10.1021/acschemneuro.1c00760](https://doi.org/10.1021/acschemneuro.1c00760) | Na site/path asymmetry |
| 5 | Prior EXTERNAL kinetics | `results/network_core/external_dutta_msm_compare.md` | Soft: `EXT_KINETICS_CB1_CB2_DISTINCT` |

---

## Claims to classify (locked a priori)

For each claim: `CLOSED_IN_LIT` | `OPEN_FOR_P4` | `OUT_OF_SCOPE`

1. Twin-toggle translational (CB1) vs W6.48 rotational (CB2).  
2. Allosteric EC↔IC pipelines state-dependent in CB1 vs poorly state-stratified in CB2.  
3. AEA primary entry via TM1–TM7 lipid channel (both); alternate TM5–TM6 **CB2-only**.  
4. AEA: induced-fit / N-term in CB1 vs conformational selection / larger pocket entropy in CB2.  
5. Secondary Na+ site present in CB1, absent in CB2.  
6. Janusforge six-hub dynamic skeleton CB1 vs CB2.  
7. Our geometric landmark STABLE class transfers to CB1.

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_P4LITE_ASYMMETRIES_CLOSED_IN_LIT`** | Claims 1–5 = `CLOSED_IN_LIT`; 6–7 = `OPEN_FOR_P4` or `OUT_OF_SCOPE` |
| **`EXT_P4LITE_PARTIAL`** | Mix; ≥2 of 1–5 closed |
| **`EXT_P4LITE_INDETERMINATE`** | Cannot access papers/readme |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_P4LITE_LIT.md` |
| Report | `results/network_core/ext_p4lite_lit.md` |
| JSON | `results/network_core/ext_p4lite_lit.json` |

---

*Fin pre-registro. Lit-only; no traj; P4 compute remains BLOCKED.*

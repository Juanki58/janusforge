# EXTERNAL P4-lite — CB1≠CB2 / AEA asymmetries closed in literature

**Run UTC:** `2026-09-22T05:05:00Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_P4LITE_LIT.md`  
**Mode:** literature + public readme only — **no trajectory download**.

## Verdict

**`EXT_P4LITE_ASYMMETRIES_CLOSED_IN_LIT`**

> Claims 1–5 (toggle, pipelines, AEA paths/mechanisms, Na asymmetry) are already closed in peer-reviewed lit.  
> Claims 6–7 (Janusforge hubs / landmark class on CB1) remain open for a future P4 — **P4 compute stays BLOCKED**.

## Claim table

| # | Claim | Status | Anchor |
|---|-------|--------|--------|
| 1 | CB1 twin-toggle **translation** (W6.48/F3.36) vs CB2 **rotation** of W6.48 (F3.36 largely static) | **CLOSED_IN_LIT** | Dutta & Shukla 2023 [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| 2 | CB1 allosteric EC↔IC pipelines **state-dependent** (inactive-like vs active-like); CB2 pipelines **without clear active/inactive distinction** (Supp Fig. 22) | **CLOSED_IN_LIT** | Same; soft support: repo `EXT_KINETICS_CB1_CB2_DISTINCT` (populations; no coords) |
| 3 | AEA primary entry **TM1–TM7** lipid channel (CB1+CB2); alternate **TM5–TM6 path CB2-only** (less favorable) | **CLOSED_IN_LIT** | Dutta & Shukla AEA 2026 [10.1016/j.jbc.2026.111434](https://doi.org/10.1016/j.jbc.2026.111434); IDB-6705697 readme (no unpack) |
| 4 | AEA: CB1 **induced-fit** (N-term into pocket, enthalpy); CB2 **conformational selection** + larger pocket **entropy** | **CLOSED_IN_LIT** | Same AEA paper / NSF PAR preprint |
| 5 | Secondary Na+ coordination site in CB1 **absent** in CB2; distinct entry routes | **CLOSED_IN_LIT** | Dutta et al. 2022 [10.1021/acschemneuro.1c00760](https://doi.org/10.1021/acschemneuro.1c00760) |
| 6 | Six Janusforge hubs as CB1↔CB2 dynamic skeleton | **OPEN_FOR_P4** | Not tested in those papers; our P1 is CB2-only `NOT_SUPPORTED` |
| 7 | Geometric landmark contact-map STABLE class transfers to CB1 | **OPEN_FOR_P4** | Our EXTERNAL landmarks are CB2; no CB1 panel run |

## What P4 should *not* rediscover

If P4 compute is ever authorized, it should **not** aim to re-prove (1)–(5). Those are literature facts. A honest P4 would ask something **object-specific** to Janusforge (e.g. whether *our* contact/hub objects differ CB1 vs CB2 under a pre-registered discrimination), still without reopening P2 Gate-1 via foreign trajs.

## Explicit non-downloads

| Deposit | Action this turn |
|---------|------------------|
| `CB2_ana_bind.zip` ~85 GB | **NOT downloaded** |
| `CB1_ana_bind.zip` ~93 GB | **NOT downloaded** |
| Illinois readme | Consulted via public metadata only |

## Governance

```text
VERDICT: EXT_P4LITE_ASYMMETRIES_CLOSED_IN_LIT
P4_COMPUTE: BLOCKED (unchanged)
P2_REOPEN: FALSE
AEA_TRAJ_UNPACK: FALSE
```

---

*Fin P4-lite. Lit closed ≠ P4 done.*

# EXTERNAL — Abrol IC fingerprint vs LigACN Sink Set T

**Run UTC:** `2026-10-02T23:01:03Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_ABROL_LIGACN_SINKS.md`  
**Input:** `ext_abrol_ic_contacts.json` (parsed_from_ext_abrol_ic_contacts.json)

## Verdict

**`EXT_ABROL_LIGACN_SINK_OVERLAP`**

> 4/4 sinks de LigACN aparecen en ≥1 set de contactos IC Abrol (avg frames).  
> P3 sigue **BLOCKED**. Avg frame ≠ MSM. Sin claim Gi.

## Sink membership

| Sink | BW | In any Abrol IC | Systems |
|------|----|-----------------|---------|
| ARG:131 | 3x50 | **True** | WT_BARR2_NoP, WT_BARR2_P, WT_Gi_Empty, WT_Gi_GDP |
| ASP:240 | 6x30 | **True** | WT_Gi_Empty |
| SER:303 | 8x47 | **True** | WT_BARR2_P, WT_Gi_Empty |
| SER:69 | 2x39 | **True** | WT_BARR2_P |

## Governance

```text
VERDICT: EXT_ABROL_LIGACN_SINK_OVERLAP
P3_PROJECT_GATE: BLOCKED
Gi_FUNCTIONAL_CLAIM: FALSE
P2_REOPEN: FALSE
```

---

*Fin Abrol × LigACN sinks.*

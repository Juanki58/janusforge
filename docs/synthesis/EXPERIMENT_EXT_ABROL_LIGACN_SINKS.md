# Experiment — EXTERNAL: Abrol IC fingerprint vs LigACN Sink Set T

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — reuse local Abrol inventory + Morales sinks.  
**Scope:** **`EXTERNAL_ABROL_LIGACN_SINKS`** — solape de residuos IC en contacto con efector (Abrol avg frames) con Sink Set T de LigACN (Morales Methods).  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Set intersection Abrol IC contacts × Sink T | Completar P3; Gi functional claim |
| Report Jaccard / membership | MSM; P2 reopen |
| Veredicto `EXT_ABROL_LIGACN_SINK_*` | Docking |

```text
P3_PROJECT_GATE = BLOCKED unchanged
EXT_ABROL_IC_EFFECTOR_PARTIAL = prior (inputs)
EXT_ABROL_LIGACN_SINK_* = NEW
```

**Sink Set T (locked; same as static topology script):**

ARG:131 (3x50), ASP:240 (6x30), SER:303 (8x47), SER:69 (2x39)

**Inputs:** `results/network_core/ext_abrol_ic_contacts.json` (must exist).

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_ABROL_LIGACN_SINK_OVERLAP`** | ≥3/4 sinks appear in ≥1 Abrol IC contact set |
| **`EXT_ABROL_LIGACN_SINK_PARTIAL`** | 1–2/4 sinks in any Abrol set |
| **`EXT_ABROL_LIGACN_SINK_ABSENT`** | 0/4 |
| **`EXT_ABROL_LIGACN_SINK_INDETERMINATE`** | Abrol JSON missing |

Secondary: note which sinks differ Gi vs βarr2 (inventory only).

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_ABROL_LIGACN_SINKS.md` |
| Report | `results/network_core/ext_abrol_ligacn_sinks.md` |
| JSON | `results/network_core/ext_abrol_ligacn_sinks.json` |
| Script | `scripts/network_core/ext_abrol_ligacn_sinks.py` |

---

*Fin pre-registro. P3 remains BLOCKED.*

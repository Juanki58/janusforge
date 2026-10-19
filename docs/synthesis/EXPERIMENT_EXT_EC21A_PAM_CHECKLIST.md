# Experiment — EXTERNAL: Ec21a PAM structural vs pharmacological assay checklist

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — lit + static structure checklist.  
**Scope:** **`EXTERNAL_EC21A_PAM_CHECKLIST`** — cruzar contactos estructurales Ec21a (9U7L / Wang) con mutagénesis / ensayos (Wang) y farmacología assay-dependent (Niswender/Qi 2024).  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Checklist struct contact ↔ mutante ↔ readout | Docking bitopic; Gi claim Janusforge |
| Registrar tensión assay-dependent | Armonizar Wang PAM vs Qi inverse-agonist post hoc |
| Veredicto `EXT_EC21A_PAM_*` | Inventar Emax no citados |

```text
docking = STOP
P2 = CLOSED unchanged
EXT_EC21A_PAM_* = NEW
```

**Pregunta discriminante:**

> ¿Los residuos del plug estructural predicen pérdida selectiva de PAM (CP55 preservado) en ensayos Wang, y cómo tensiona eso la farmacología complicated de EC21a en otros ensayos?

---

## Locked rows

| Residue | Struct role (9U7L/Wang) | Mutant lit. effect | Assay note |
|---------|-------------------------|--------------------|------------|
| S268^6.58 | Portion II contact | CP55≈ok; PAM almost abolished | Wang cAMP/GloSensor-class |
| K278^7.32 | Portion II | CP55≈ok; PAM almost abolished | Wang |
| F183 ECL2 | Portion I/II | F183A PAM loss; F183L partial rescue | Wang |
| I186 ECL2 | Portion I enclosure | I186A PAM loss | Wang |
| P176 / P178 | ECL2 flexibility | PAM abolished / attenuated | Wang / atlas |
| E181 ECL2 | Map poorly resolved | Slight PAM atten. | Wang |
| F106 / P184 / M22 / Y25 | Portion III pocket | Mixed; some abolish cellular response | Wang |
| EC21a scaffold (Qi 2024) | — | Inverse agonist / assay-dependent at CB2 | PI hydrolysis / GIRK — **tension** |

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_EC21A_PAM_STRUCT_ASSAY_ALIGNED`** | ≥4 Wang mutantes AGREE struct→PAM-loss; 0 strong cross-lab TENSION |
| **`EXT_EC21A_PAM_STRUCT_ASSAY_PARTIAL`** | Wang panel mostly AGREE **and** Qi/Niswender TENSION recorded |
| **`EXT_EC21A_PAM_STRUCT_ASSAY_TENSION`** | Struct panel contradicts Wang mutagensis |
| **`EXT_EC21A_PAM_INDETERMINATE`** | Sources unavailable |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_EC21A_PAM_CHECKLIST.md` |
| Report | `results/network_core/ext_ec21a_pam_checklist.md` |
| JSON | `results/network_core/ext_ec21a_pam_checklist.json` |
| Script | `scripts/network_core/ext_ec21a_pam_checklist.py` |

---

*Fin pre-registro.*

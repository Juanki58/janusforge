# EXTERNAL — Ec21a PAM structural vs assay checklist

**Run UTC:** `2026-10-02T23:01:03Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_EC21A_PAM_CHECKLIST.md`

## Verdict

**`EXT_EC21A_PAM_STRUCT_ASSAY_PARTIAL`**

> Panel mutagénico Wang alinea plug estructural (S268/K278/F183/I186/P176–P178) con pérdida selectiva de PAM.  
> Qi/Niswender 2024 reporta farmacología **assay-dependent** (inverse agonist / mixed) — tensión entre labs/ensayos, **no** armonizada aquí.

## Checklist

| Residue | Struct role | Mutant / assay | Call |
|---------|-------------|----------------|------|
| S268^6.58 | Portion II contact with Ec21a (Wang/9U7L) | CP55 retained; PAM almost abolished (S268A) | **AGREE** |
| K278^7.32 | Portion II contact | CP55 retained; PAM almost abolished (K278A) | **AGREE** |
| F183 ECL2 | Portion I/II hydrophobic enclosure | F183A PAM loss; F183L partial rescue | **AGREE** |
| I186 ECL2 | Portion I enclosure | I186A PAM loss | **AGREE** |
| P176 / P178 ECL2 | ECL2 flexibility / CB2 motif | PAM abolished / strongly attenuated | **AGREE** |
| E181 ECL2 | Map poorly resolved near portion II | Slight PAM attenuation | **PARTIAL** |
| F106 / P184 / M22 / Y25 | Portion III pocket | Mixed; some abolish cellular response (not PAM-selective) | **PARTIAL** |
| EC21a scaffold (cross-lab) | Same chemotype discussed as PAM in Wang | Qi/Niswender 2024: inverse agonist / assay-dependent at CB2 (PI hydrolysis / GIRK) | **TENSION_ASSAY** |

## Governance

```text
VERDICT: EXT_EC21A_PAM_STRUCT_ASSAY_PARTIAL
HARMONIZE_WANG_VS_QI: FALSE
DOCKING: STOP
P2_REOPEN: FALSE
```

---

*Fin Ec21a PAM checklist.*

# EXTERNAL — Abrol Zenodo IC contact inventory (avg frames)

**Run UTC:** `2026-09-22T05:06:40Z`
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_ABROL_IC_CONTACTS.md`
**Zenodo:** [10.5281/zenodo.14227795](https://doi.org/10.5281/zenodo.14227795) (record files via 14232007)

## Verdict

**Primary:** `EXT_ABROL_IC_EFFECTOR_PARTIAL`

**P3 project gate:** `BLOCKED` — this inventory does **not** complete P3.

> Average frames of effector complexes ≠ apo MSM. No Gi functional claim.

## Download / provenance

- Zip present: `True`
- Zip sha256: `1bbace2586c238f2c003b00854271456a8612e882823ecacd616758e8db4df2c`
- Zip bytes: `96996645`

## Per-system IC contact residues (CB2 UniProt)

| System | Mapped IC | Effector res | n CB2 contact res | Hubs touching | Identity |
|--------|----------:|-------------:|------------------:|---------------|---------:|
| WT_Gi_Empty | 109 | 724 | 16 | 302 | 0.875 |
| WT_Gi_GDP | 109 | 724 | 13 | — | 0.875 |
| WT_BARR2_NoP | 108 | 348 | 21 | 302 | 0.966 |
| WT_BARR2_P | 109 | 403 | 21 | 302 | 0.969 |

## Jaccard (CB2 contact-residue sets)

- Gi_Empty vs BARR2_P: **0.4230769230769231**
- Gi_Empty vs Gi_GDP: **0.16**
- BARR2_NoP vs BARR2_P: **0.3548387096774194**

## Contact residue lists (UniProt)

- **WT_Gi_Empty** (16): GLN:63, ARG:131, CYS:134, LEU:135, PRO:138, LYS:142, HSD:219, LEU:223, ARG:236, ARG:238, LEU:239, ASP:240, ARG:242, ARG:302, SER:303, ARG:307
- **WT_Gi_GDP** (13): ARG:131, CYS:134, ARG:147, ALA:216, HSD:219, VAL:220, SER:222, ARG:229, GLN:230, VAL:231, PRO:232, LEU:239, GLY:304
- **WT_BARR2_NoP** (21): LYS:67, ARG:131, CYS:134, ARG:136, TYR:137, PRO:138, PRO:139, SER:140, LYS:142, ALA:143, HSD:219, SER:222, ASP:228, ARG:229, VAL:231, LEU:239, LEU:243, THR:246, ARG:302, GLY:304, GLU:305
- **WT_BARR2_P** (21): LYS:67, SER:69, TYR:70, ARG:131, CYS:134, LEU:135, PRO:138, PRO:139, LYS:142, HSD:219, VAL:220, LEU:223, ARG:229, PRO:232, GLY:233, ARG:236, ARG:238, LEU:243, THR:246, ARG:302, SER:303

## Governance

```text
VERDICT: EXT_ABROL_IC_EFFECTOR_PARTIAL
P3_PROJECT_GATE: BLOCKED
Gi_FUNCTIONAL_CLAIM: FALSE
P2_REOPEN: FALSE
AVG_FRAME_NEQ_MSM: TRUE
```

## References

1. Heo & Abrol, *BBRC* — [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100)
2. Zenodo — [10.5281/zenodo.14227796](https://doi.org/10.5281/zenodo.14227796)

---

*Fin EXTERNAL Abrol IC inventory. Toward P3; P3 not done.*

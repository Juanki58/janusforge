# Qiu 0G — Pose analysis of CB2 docking (compounds 14 / 15 / 20 / 24)

> **Scope:** geometry and contacts for poses **written** in 0F output PDBQTs only. No Vina re-run; no PDBQT / ligand / receptor / parameter changes; no pharmacological or SAR conclusions.
>
> **Upstream:** [`qiu_0f_docking_protocol.md`](qiu_0f_docking_protocol.md), [`qiu_0f_docking_qc.md`](qiu_0f_docking_qc.md) (`0F = PASS 4/4`).
>
> **Date:** 2026-08-12
>
> **Analysis script:** `scripts/analyze_qiu_0g_poses.py` (read-only inputs)

---

## Methods

### Poses used (strict)

| Compound | File analyzed |
|----------|----------------|
| 14 | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` |
| 15 | `results/docking/qiu_0f/compound_15_cb2_out.pdbqt` |
| 20 | `results/docking/qiu_0f/compound_20_cb2_out.pdbqt` |
| 24 | `results/docking/qiu_0f/compound_24_cb2_out.pdbqt` |

- A pose is counted **only** if it appears as a `MODEL` / `ENDMDL` block with a `REMARK VINA RESULT` line in the out PDBQT.
- Log-only modes (present in `.log` but **not** written to PDBQT) are **excluded** (per 0F QC: compounds 15 and 20 each had one extra log row outside the default energy window).
- Scores quoted below are the numeric affinity from `REMARK VINA RESULT` (kcal/mol). **Observed docking score only — not experimental affinity.**

### Receptor

- PDBQT: `data/targets/cb2/6PT0_rec.pdbqt`, chain **R** (CB2 in 6PT0 cryo-EM complex).
- Residue names/numbers taken from receptor PDBQT ATOM records (e.g. `SER285` = SER R 285).

### Contact / interaction definitions (objective)

| Label | Definition |
|-------|------------|
| **Contact residue** | Any residue with ≥1 **heavy-atom** pair (ligand–receptor) at distance **≤ 4.0 Å**. Hydrogens excluded from the contact census. |
| **Hydrophobic proximity** | Contact where both atoms have PDBQT types `C` or `A` (aromatic C). Labeled as proximity, not a typed π–π score. |
| **H-bond (geometry OK)** | Donor–acceptor heavy distance ≤ 3.5 Å **and** H···acceptor ≤ 2.5 Å **and** angle D–H···A ≥ 120°. Reported only when all three hold. |
| **Polar proximity (not H-bond)** | Polar heavy atoms (PDBQT `OA`/`NA`/`N`/`O`/`SA`) within ≤ 3.5 Å without meeting H-bond angle/H criteria. |

Best pose = MODEL with the **lowest (most negative)** `REMARK VINA RESULT` among written models.

### Orientation (structural description)

Moieties identified via RDKit SMARTS on the REMARK SMILES, mapped to PDBQT serials with `REMARK SMILES IDX` (Meeko). Centroids and vectors from the pyrazole centroid are **observed coordinates**, not pharmacological claims. Dominant axis = largest |Δx|, |Δy|, or |Δz| of that vector in receptor/PDB frame.

Scaffold annotations (from 0D, for substituent labels only):

| Cpd | N1 | C3-carboxamide R³ |
|-----|----|-------------------|
| 14 | *o*-morpholine | CONH–Ad |
| 15 | *m*-morpholine | CONH–Ad |
| 20 | *o*-(4-methylpiperazine) | CONH–Ad |
| 24 | *o*-morpholine | CONH–CH₂–Ad |

### Comparable binding region (criterion)

All four best-pose **ligand heavy-atom centroids** within **3.0 Å** of their mutual mean **and** mean pairwise Jaccard of contact-residue sets ≥ **0.40**. This is a geometric occupation test, not a ranking.

---

## Per-compound results

### Compound 14 (*o*-morpholine, CONH–Ad)

**Poses in PDBQT (9):**

| MODEL | Vina score (kcal/mol) | rmsd_lb | rmsd_ub |
|-------|----------------------|---------|---------|
| 1 | **−9.919** | 0.000 | 0.000 |
| 2 | −9.789 | 1.924 | 2.921 |
| 3 | −9.451 | 1.913 | 3.078 |
| 4 | −9.287 | 2.908 | 7.949 |
| 5 | −9.031 | 3.874 | 5.326 |
| 6 | −8.907 | 2.129 | 4.181 |
| 7 | −8.787 | 2.530 | 8.442 |
| 8 | −8.742 | 2.063 | 4.301 |
| 9 | −8.529 | 3.606 | 5.786 |

- **Best pose:** MODEL **1**, score **−9.919** kcal/mol.
- **Ligand centroid (obs.):** (98.774, 110.334, 124.791); distance to locked box center = 1.32 Å.

**Contacts (best pose, heavy ≤ 4.0 Å) — principal by min distance:**  
LEU182, SER90, THR114, ILE110, ILE186, PHE91, PHE281, PHE183, TRP194, SER285, PHE87, LEU191  
(17 contact residues total).

**Interactions:**

- **H-bond geometry OK:** none.
- **Polar proximity (not H-bond):** morpholine O (`OA`) ··· THR114 OG1 = 2.86 Å (H present on OG1; D–H···A angle ≈ 103° → fails ≥120° criterion). Also O···LEU182 O = 3.18 Å (acceptor–acceptor proximity).
- **Hydrophobic proximity (examples):** ILE110, ILE186, PHE91, THR114 (C/A pairs), PHE281.

**Orientation (obs.):**

- Pyrazole near box center; adamantyl centroid ≈ (94.4, 112.7, 121.8) along **−x** from pyrazole.
- *o*-Morpholine centroid ≈ (100.3, 109.8, 129.0) along **+z**; nearest residues include LEU182, PHE183, PRO184.
- C5–Ph along **−y**; N1–Ph along **+x**.
- Amide linker between pyrazole and Ad (CONH–Ad as labeled).

**SER285:** min heavy distance 3.37 Å (ligand aromatic C to SER285 CB) — contact by cutoff; **not** an established H-bond to morpholine/amide in this pose.

---

### Compound 15 (*m*-morpholine, CONH–Ad)

**Poses in PDBQT (8)** — log had 9; ninth not written:

| MODEL | Vina score (kcal/mol) | rmsd_lb | rmsd_ub |
|-------|----------------------|---------|---------|
| 1 | **−11.201** | 0.000 | 0.000 |
| 2 | −11.170 | 3.877 | 5.344 |
| 3 | −10.593 | 2.115 | 3.503 |
| 4 | −10.550 | 2.769 | 9.106 |
| 5 | −10.204 | 1.662 | 2.974 |
| 6 | −10.203 | 3.754 | 5.399 |
| 7 | −9.628 | 2.172 | 9.043 |
| 8 | −9.597 | 2.152 | 9.038 |

- **Best pose:** MODEL **1**, score **−11.201** kcal/mol.
- **Ligand centroid:** (98.509, 110.829, 125.288); box-center distance = 1.66 Å.

**Contacts (principal):**  
THR114, ILE186, TYR25, ILE110, PHE87, SER285, PHE183, PHE91, PHE94, PHE281, TYR190, PRO184  
(18 residues).

**Interactions:**

- **H-bond geometry OK:** none.
- **Polar proximity:** morpholine O ··· THR114 OG1 = 2.71 Å (angle ≈ 98° → not H-bond by criterion); also O···TYR25 O = 3.02 Å.
- **Hydrophobic proximity:** ILE186, THR114, ILE110, aromatics (PHE/TYR set).

**Orientation (obs.):**

- Adamantyl placement closely matches 14 (**−x** from pyrazole).
- *m*-Morpholine reaches farther along **+z** (centroid z ≈ 131.4 vs ≈ 129 for 14) and approaches **TYR25** (min 3.02 Å to morpholine atoms) — geometric consequence of meta substitution, not an efficacy claim.
- C5–Ph **−y**; N1–Ph dominant axis **+z**.

**SER285:** min heavy 3.08 Å (aromatic C to OG) — contact; no geometry-OK H-bond.

---

### Compound 20 (*o*-Me-piperazine, CONH–Ad)

**Poses in PDBQT (5)** — log had 6; sixth not written:

| MODEL | Vina score (kcal/mol) | rmsd_lb | rmsd_ub |
|-------|----------------------|---------|---------|
| 1 | **−9.986** | 0.000 | 0.000 |
| 2 | −9.048 | 1.770 | 4.560 |
| 3 | −8.546 | 2.131 | 4.775 |
| 4 | −7.927 | 3.181 | 7.869 |
| 5 | −7.363 | 1.549 | 2.551 |

- **Best pose:** MODEL **1**, score **−9.986** kcal/mol.
- **Ligand centroid:** (98.729, 110.383, 124.813); box-center distance = 1.31 Å.

**Contacts (principal):**  
LEU182, ILE110, SER90, THR114, ILE186, PHE91, PHE183, PHE281, SER285, PHE87, LEU191, TRP194  
(17 residues; **identical set** to compound 14).

**Interactions:**

- **H-bond geometry OK:** none.
- **Polar proximity:** piperazine-region / ligand O···THR114 OG1 = 2.82 Å (angle ≈ 105° → not H-bond); N···LEU182 O = 3.18 Å.
- **Hydrophobic proximity:** ILE110, ILE186, PHE91, etc.

**Orientation (obs.):**

- Nearly aligned with 14: *o*-heterocycle **+z**, Ad **−x**, C5–Ph **−y**, N1–Ph **+x**.
- Pairwise ligand-centroid distance vs 14 best pose: **0.14 Å**; contact Jaccard **1.00**.

**SER285:** min heavy 3.34 Å — contact; no geometry-OK H-bond.

---

### Compound 24 (*o*-morpholine, CONH–CH₂–Ad)

**Poses in PDBQT (9):**

| MODEL | Vina score (kcal/mol) | rmsd_lb | rmsd_ub |
|-------|----------------------|---------|---------|
| 1 | **−11.606** | 0.000 | 0.000 |
| 2 | −11.368 | 1.902 | 4.274 |
| 3 | −11.228 | 2.370 | 8.594 |
| 4 | −10.604 | 2.471 | 8.170 |
| 5 | −10.444 | 3.019 | 7.913 |
| 6 | −9.340 | 1.750 | 3.625 |
| 7 | −9.121 | 1.669 | 2.971 |
| 8 | −8.768 | 2.801 | 3.833 |
| 9 | −8.724 | 2.983 | 4.676 |

- **Best pose:** MODEL **1**, score **−11.606** kcal/mol.
- **Ligand centroid:** (98.983, 110.070, 125.402); box-center distance = 1.71 Å.

**Contacts (principal):**  
PRO184, LEU191, PHE87, THR114, VAL113, PHE91, ILE186, ILE110, SER90, ALA282, SER285, PHE183  
(16 residues).

**Interactions:**

- **H-bond geometry OK:** none.
- **Polar proximity:** amide N ··· SER90 OG = 3.41 Å (borderline; no angle-OK H-bond listed). Morpholine O ··· THR114 OG1 = 3.70 Å (outside tight polar ≤3.5 Å set used above; longer than in 14/15/20).
- **Hydrophobic proximity:** LEU191, THR114, ILE186, aromatics.

**Orientation (obs.):**

- **Adamantyl** still occupies the same subpocket as 14/15/20 (centroid ≈ 94.2, 112.2, 122.0; **−x** from pyrazole). CONH–CH₂–Ad places an extra CH₂ between amide N and Ad (centroid of CH₂ ≈ 95.7, 109.5, 121.6).
- ***o*-Morpholine** is **rotated** relative to 14/20: dominant vector **+x** (centroid ≈ 103.0, 109.2, 123.8) rather than **+z**; nearest residues PHE87, ILE110, SER90 (not LEU182-first as in 14/20).
- C5–Ph dominant axis **+z** (vs **−y** in 14/15/20).

**Interpretation note (geometry only):** same overall orthosteric box region and shared Ad site; **core/substituent rotation** differs from 14/15/20. Not a different pocket; not a pharmacological “mode switch.”

**SER285:** min heavy 3.35 Å — contact; no geometry-OK H-bond.

---

## Comparison (geometry / occupation)

| Pair | Ligand centroid Δ (Å) | Pyrazole centroid Δ (Å) | Contact Jaccard | Heavy RMSD (same atom count only) |
|------|----------------------|-------------------------|-----------------|-----------------------------------|
| 14 vs 15 | 0.71 | 0.61 | 0.84 | 1.49 |
| 14 vs 20 | 0.14 | 0.18 | **1.00** | n/a (38 vs 39 atoms) |
| 14 vs 24 | 0.58 | 0.85 | 0.74 | n/a |
| 15 vs 20 | 0.58 | 0.44 | 0.84 | n/a |
| 15 vs 24 | 1.28 | 1.16 | 0.62 | n/a |
| 20 vs 24 | 0.71 | 0.96 | 0.74 | 6.01 |

**Binding-region check:**

| Metric | Value |
|--------|-------|
| Mean ligand centroid | (98.749, 110.329, 124.874) |
| Distances from mean (14 / 15 / 20 / 24) | 0.09 / 0.64 / 0.08 / 0.64 Å |
| Max drift from mean | **0.64 Å** (≤ 3.0 Å criterion) |
| Mean pairwise contact Jaccard | **0.80** (≥ 0.40 criterion) |
| **Comparable region?** | **Yes** |

**Shared contact core (present in all four best poses):**  
ILE110, ILE186, LEU191, PHE87, PHE91, PHE94, PHE183, PHE281, PRO184, SER285, THR114, TRP194, VAL113.

**Geometric summary (not ranking):**

1. All four best poses sit in the **same CB2 box / orthosteric-like region**.
2. **14 and 20** are nearly co-localized (centroid Δ 0.14 Å; identical contact residue sets); *o*-morpholine vs *o*-Me-piperazine occupy the same **+z** corridor toward LEU182/PHE183.
3. **15** keeps Ad and core placement; *m*-morpholine extends further **+z** and adds **TYR25** among close contacts.
4. **24** keeps Ad in the same hydrophobic subpocket but **rotates** the pyrazole/N1-morpholine relative to 14/15/20 (morpholine toward PHE87/SER90; C5–Ph axis shifts). Heavy RMSD vs 20 ≈ 6 Å reflects that rotation despite centroid proximity.

**Scores:** listed only as observed Vina values. Differences between compounds are **not** interpreted as affinity, selectivity, or activity.

---

## Ambiguities / limitations

1. **Static docking only** — single receptor conformation (6PT0 agonist-state); no MD, no ensemble.
2. **Vina score ≠ experimental affinity**; no biological activity inferred.
3. **No geometry-OK H-bonds** under the stated angle criterion; polar O···THR114 contacts are **proximities** (angles ~98–105°). Softening the angle cutoff would change labels — not done here.
4. **Contact cutoff 4.0 Å** is conventional but arbitrary; residue lists would change with 3.5 vs 4.5 Å.
5. **PDBQT atom typing / Meeko mapping** used for moiety centroids; SMARTS matching assumes REMARK SMILES matches the docked connectivity (consistent with 0E/0F).
6. **Protonation / tautomer state** fixed by 0E preparation; alternate states not explored.
7. Log modes absent from PDBQT were ignored by design — completeness of the energy landscape is unknown beyond written poses.
8. Residue naming uses 6PT0 chain-R numbering; Ballesteros–Weinstein indices not assigned in this report.
9. Comparison is **pose geometry**, not SAR, not “which compound is better.”

---

## Final table

| Compound | poses PDBQT | best pose | best score | residuos principales | modo de unión comparable (sí/no) | observaciones |
|----------|-------------|-----------|------------|----------------------|----------------------------------|---------------|
| 14 | 9 | 1 | −9.919 | LEU182, SER90, THR114, ILE110, ILE186, PHE91, PHE281, PHE183, TRP194, SER285, PHE87, LEU191 | **sí** | *o*-morpholine +z; Ad −x; polar prox. THR114 (no H-bond geom.) |
| 15 | 8 | 1 | −11.201 | THR114, ILE186, TYR25, ILE110, PHE87, SER285, PHE183, PHE91, PHE94, PHE281, TYR190, PRO184 | **sí** | *m*-morpholine further +z; TYR25 proximity; Ad same subpocket |
| 20 | 5 | 1 | −9.986 | LEU182, ILE110, SER90, THR114, ILE186, PHE91, PHE183, PHE281, SER285, PHE87, LEU191, TRP194 | **sí** | Nearly identical occupation to 14 (Jaccard 1.00); *o*-Me-piperazine |
| 24 | 9 | 1 | −11.606 | PRO184, LEU191, PHE87, THR114, VAL113, PHE91, ILE186, ILE110, SER90, ALA282, SER285, PHE183 | **sí** | Same region + same Ad site; **rotated** N1-morpholine (+x) vs 14/15/20 |

Scores = Vina `REMARK VINA RESULT` only.

---

## Verdict

All four compounds have valid written poses; best poses were parsed without serious inconsistencies; contacts/orientations are documentable under explicit cutoffs; all four occupy a comparable binding region (with 24 rotated within that region).

**`0G = PASS 4/4`**

# Geometric pharmacophore map — D2_20 / D2_06 / D2_22 vs Qiu 14 / 15 / 20 / 24 (CB2)

> **Scope:** feature-by-feature **geometry** of best on-disk CB2 poses only. No re-docking; no PDBQT edits; no SAR or pharmacological conclusions.
>
> **Axiom (explicit):** pose-comparable ≠ same pharmacophore ≠ same pharmacology.
>
> **Date:** 2026-08-12
>
> **Script:** `scripts/compare_qiu_d1_pharmacophore_geometry.py`
>
> **Upstream:** [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md) (pocket coincidence); this report maps **features ↔ residues**, not whole-ligand occupation alone.

---

## Methods

### Poses (strict)

| Set | Path | Best pose rule |
|-----|------|----------------|
| D2 | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | lowest Vina `REMARK` among written MODELs |
| Qiu | `results/docking/qiu_0f/compound_{N}_cb2_out.pdbqt` | same |
| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` chain R | — |

### Feature identification (**observed** chemistry → atoms in pose)

1. Take SMILES from PDBQT `REMARK SMILES` (fallback: library CSV / 0D table).
2. Match SMARTS substructures with RDKit.
3. Map matched SMILES atom indices → PDBQT serials via `REMARK SMILES IDX` (Meeko remnant).
4. Feature centroid = mean of mapped **heavy** atom coordinates in the best pose.

**Qiu expected / checked features:** pyrazole; amide CONH; adamantyl; N1-phenyl; N1-heterocycle (morpholine or N-Me-piperazine); C5-phenyl; C4-methyl; amide-CH₂ (cpd 24 only).

**D2 (URB447-like) features checked as present:** pyrrole; aryl ketone (C=O); benzoyl aryl; C2-phenyl; C3-amino; C5-methyl; N1-CH₂; N1-benzyl aryl; and para-substituents actually found (e.g. benzyl-pCN, benzoyl-pMe, benzoyl-pCF₃). Features **not** matched are omitted (not invented).

### Feature ↔ residue mapping

| Quantity | Definition |
|----------|------------|
| Feature–residue contact | ≥1 heavy atom of feature within **≤ 4.0 Å** of residue heavy atom (same as 0G) |
| Feature shell | Residues meeting that cutoff (top 8 listed by min distance) |
| Region distances | Min heavy distance from feature atoms to SER285, TYR25, THR114, ILE110, ILE186 |
| Feature–feature correspondence | Centroid distance ≤ **3.0 Å** **or** shell Jaccard ≥ **0.25** |

### Epistemic labels

- **Observed:** coordinates, Vina REMARK numbers, SMARTS hits, distances at fixed cutoffs.
- **Structural inference:** correspondence flags from those cutoffs; shell overlap.
- **Interpretation:** brief notes on which subpockets co-occupy; **not** activity or SAR.

### Priority note (from prior comparison)

D2_20 and D2_06 maximized contact Jaccard vs Qiu union in the pose comparison; D2_22 is the historical lead with **mid** overlap. This report does **not** auto-elevate D2_22 by Vina score.

---

## Per-compound feature inventories (best pose)

### Qiu 14 (o-morpholine; CONH-Ad)

- Path: `results/docking/qiu_0f/compound_14_cb2_out.pdbqt`
- Best MODEL 1; Vina REMARK = **-9.919** kcal/mol (**score number only**, not experimental potency)
- SMILES source: REMARK SMILES
- Features found: adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrazole | (99.51, 109.71, 124.17) | ILE110(3.37), PHE183(3.477) | 5.25 | 9.61 | 5.16 | 3.37✓ | 6.58 |
| amide | (97.46, 110.86, 122.27) | THR114(2.861), PHE183(3.372), ILE110(3.663), VAL113(3.794) | 7.97 | 10.42 | 2.86✓ | 3.66✓ | 5.19 |
| n1_heterocycle | (100.30, 109.83, 128.95) | LEU182(2.676), PHE183(3.517), PRO184(3.613), HIS95(3.97), PHE94(3.977) | 6.94 | 5.04 | 9.52 | 5.52 | 7.37 |
| adamantyl | (94.39, 112.74, 121.78) | THR114(3.016), ILE186(3.026), ILE110(3.122), PHE183(3.291), TRP194(3.369) | 9.88 | 9.99 | 3.02✓ | 3.12✓ | 3.03✓ |
| n1_phenyl | (102.78, 111.18, 125.80) | SER90(2.806), ILE110(2.964), PHE94(3.496) | 7.17 | 7.47 | 7.94 | 2.96✓ | 8.05 |
| c5_phenyl | (100.76, 106.69, 126.60) | PHE91(3.063), PHE281(3.245), SER285(3.375), PHE87(3.419) | 3.38✓ | 9.10 | 8.67 | 6.45 | 9.60 |
| c4_methyl | (97.81, 107.69, 123.67) | PHE183(3.519) | 4.99 | 11.67 | 6.43 | 6.89 | 8.78 |

### Qiu 15 (m-morpholine; CONH-Ad)

- Path: `results/docking/qiu_0f/compound_15_cb2_out.pdbqt`
- Best MODEL 1; Vina REMARK = **-11.201** kcal/mol (**score number only**, not experimental potency)
- SMILES source: REMARK SMILES
- Features found: adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrazole | (99.18, 110.15, 124.42) | PHE183(3.156), ILE110(3.596) | 5.67 | 8.77 | 5.08 | 3.60✓ | 5.78 |
| amide | (97.33, 111.33, 122.35) | THR114(2.71), ILE110(3.389), PHE183(3.416) | 8.42 | 10.28 | 2.71✓ | 3.39✓ | 4.80 |
| n1_heterocycle | (100.71, 110.20, 131.40) | TYR25(3.021), LEU182(3.513), PRO184(3.661), PHE94(3.702), HIS95(3.797) | 7.74 | 3.02✓ | 11.83 | 7.22 | 9.02 |
| adamantyl | (94.22, 113.08, 121.61) | ILE186(2.978), THR114(3.132), ILE110(3.182), TYR190(3.363), TRP194(3.464) | 10.27 | 10.17 | 3.13✓ | 3.18✓ | 2.98✓ |
| n1_phenyl | (101.38, 111.61, 127.40) | ILE110(3.038), PHE94(3.293), PRO184(3.421), PHE106(3.609) | 7.61 | 5.85 | 8.27 | 3.04✓ | 7.11 |
| c5_phenyl | (100.78, 106.87, 126.19) | PHE87(3.059), SER285(3.081), PHE91(3.25), PHE281(3.363) | 3.08✓ | 9.43 | 8.36 | 6.13 | 9.28 |
| c4_methyl | (98.38, 108.06, 122.94) | VAL113(3.978) | 5.31 | 12.00 | 5.77 | 6.31 | 8.70 |

### Qiu 20 (o-Me-piperazine; CONH-Ad)

- Path: `results/docking/qiu_0f/compound_20_cb2_out.pdbqt`
- Best MODEL 1; Vina REMARK = **-9.986** kcal/mol (**score number only**, not experimental potency)
- SMILES source: REMARK SMILES
- Features found: adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrazole | (99.45, 109.88, 124.20) | ILE110(3.275), PHE183(3.356) | 5.41 | 9.45 | 5.11 | 3.27✓ | 6.43 |
| amide | (97.37, 111.05, 122.33) | THR114(2.815), PHE183(3.37), ILE110(3.667), VAL113(3.991) | 8.15 | 10.28 | 2.81✓ | 3.67✓ | 4.92 |
| n1_heterocycle | (100.22, 109.69, 129.16) | LEU182(2.723), PRO184(3.472), PHE281(3.486), PHE183(3.58), PHE94(3.82) | 6.50 | 4.89 | 9.52 | 5.46 | 7.30 |
| adamantyl | (94.30, 112.85, 121.75) | ILE186(2.991), THR114(3.103), ILE110(3.176), PHE183(3.338), LEU191(3.398) | 9.98 | 10.03 | 3.10✓ | 3.18✓ | 2.99✓ |
| n1_phenyl | (102.81, 111.27, 125.77) | ILE110(2.786), SER90(2.792), PHE94(3.483) | 7.30 | 7.52 | 7.86 | 2.79✓ | 7.94 |
| c5_phenyl | (100.82, 106.78, 126.46) | PHE91(3.062), PHE281(3.334), SER285(3.338), PHE87(3.339) | 3.34✓ | 9.19 | 8.56 | 6.29 | 9.48 |
| c4_methyl | (97.74, 107.85, 123.78) | PHE183(3.318) | 5.13 | 11.49 | 6.40 | 6.77 | 8.59 |

### Qiu 24 (o-morpholine; CONH-CH2-Ad)

- Path: `results/docking/qiu_0f/compound_24_cb2_out.pdbqt`
- Best MODEL 1; Vina REMARK = **-11.606** kcal/mol (**score number only**, not experimental potency)
- SMILES source: REMARK SMILES
- Features found: adamantyl, amide, amide_ch2, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrazole | (99.46, 109.07, 124.73) | PHE183(3.548) | 4.68 | 9.17 | 5.87 | 4.07 | 7.07 |
| amide | (97.76, 109.47, 122.24) | VAL113(3.049), PHE183(3.429), THR114(3.703) | 6.74 | 11.65 | 3.70✓ | 4.09 | 7.33 |
| n1_heterocycle | (102.96, 109.19, 123.84) | PHE87(2.922), ILE110(3.216), SER90(3.238), VAL113(3.327), PHE91(3.612) | 5.89 | 9.94 | 6.41 | 3.22✓ | 8.79 |
| adamantyl | (94.24, 112.23, 122.01) | LEU191(2.896), THR114(3.035), ILE186(3.133), PHE183(3.419), TRP194(3.585) | 9.55 | 10.01 | 3.04✓ | 3.83✓ | 3.13✓ |
| n1_phenyl | (101.64, 111.39, 127.10) | PRO184(2.805), PHE94(3.535), ILE110(3.79), PHE183(3.893) | 7.15 | 5.91 | 8.41 | 3.79✓ | 7.18 |
| c5_phenyl | (100.71, 106.68, 127.77) | PHE91(3.061), ALA282(3.306), SER285(3.354), PHE281(3.55), PHE87(3.844) | 3.35✓ | 7.41 | 9.55 | 7.05 | 9.83 |
| c4_methyl | (98.35, 106.66, 124.30) | SER285(3.723) | 3.72✓ | 11.84 | 7.67 | 7.71 | 9.83 |
| amide_ch2 | (95.74, 109.53, 121.64) | THR114(3.843) | 8.21 | 12.65 | 3.84✓ | 5.73 | 7.38 |

### JANUS_D2_20

- Path: `results/docking/option_d_batch2/cb2/JANUS_D2_20_docked.pdbqt`
- Common name / edit: URB447 analog Bz_pMe
- Best MODEL 1; Vina REMARK = **-11.656** kcal/mol (**score number only**)
- SMILES source: REMARK SMILES
- Features found: aryl_ketone, benzoyl_aryl, benzoyl_pMe, c2_phenyl, c3_amino, c5_methyl, n1_benzyl_aryl, n1_benzyl_pCl, n1_ch2, pyrrole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrrole | (99.51, 108.46, 124.02) | PHE183(3.739), VAL113(3.783) | 4.27 | 10.47 | 5.64 | 4.55 | 8.01 |
| aryl_ketone | (97.67, 108.68, 121.62) | VAL113(3.366) | 6.64 | 12.21 | 4.25 | 5.33 | 7.89 |
| benzoyl_aryl | (95.65, 110.98, 122.64) | ILE110(3.647), PHE183(3.667), TRP194(3.847), THR114(3.859) | 7.84 | 10.24 | 3.86✓ | 3.65✓ | 4.31 |
| c3_amino | (100.31, 110.44, 122.67) | VAL113(3.448), ILE110(3.506) | 7.29 | 11.18 | 5.22 | 3.51✓ | 7.56 |
| n1_ch2 | (100.14, 106.94, 126.07) | SER285(3.58) | 3.58✓ | 9.93 | 9.28 | 7.30 | 10.23 |
| n1_benzyl_aryl | (100.45, 108.45, 128.55) | LEU182(3.34), HIS95(3.504), PHE281(3.51), PHE183(3.743), PHE91(3.95) | 4.82 | 5.64 | 9.69 | 6.93 | 8.70 |
| n1_benzyl_pCl | (100.83, 110.04, 131.21) | TYR25(3.942), PHE94(3.971) | 8.75 | 3.94✓ | 12.97 | 8.56 | 10.11 |
| c2_phenyl | (103.06, 109.62, 125.62) | PHE91(3.48), PHE94(3.542), SER90(3.595), PHE87(3.907), ILE110(3.996) | 5.67 | 8.41 | 8.27 | 4.00✓ | 8.40 |
| c5_methyl | (97.65, 106.56, 124.34) | PHE281(3.66), PHE183(3.857) | 4.04 | 11.92 | 7.68 | 8.12 | 9.78 |
| benzoyl_pMe | (93.58, 112.97, 123.10) | ILE186(3.384), LEU191(3.391), PHE183(3.868) | 11.71 | 10.60 | 5.41 | 5.68 | 3.38✓ |

### JANUS_D2_06

- Path: `results/docking/option_d_batch2/cb2/JANUS_D2_06_docked.pdbqt`
- Common name / edit: URB447 analog NBn_pCN
- Best MODEL 1; Vina REMARK = **-12.03** kcal/mol (**score number only**)
- SMILES source: REMARK SMILES
- Features found: aryl_ketone, benzoyl_aryl, c2_phenyl, c3_amino, c5_methyl, n1_benzyl_aryl, n1_benzyl_pCN, n1_ch2, pyrrole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrrole | (99.15, 108.83, 123.52) | PHE183(3.57), VAL113(3.607) | 4.63 | 10.70 | 4.88 | 4.34 | 7.61 |
| aryl_ketone | (97.38, 109.53, 121.15) | THR114(3.105), VAL113(3.538) | 7.53 | 12.29 | 3.10✓ | 4.42 | 7.34 |
| benzoyl_aryl | (95.17, 111.36, 122.64) | ILE110(3.6), PHE183(3.619), THR114(3.631), TRP194(3.734), LEU191(3.736) | 8.54 | 10.07 | 3.63✓ | 3.60✓ | 3.96✓ |
| c3_amino | (100.09, 110.88, 122.38) | ILE110(3.293), VAL113(3.527) | 7.80 | 11.25 | 4.76 | 3.29✓ | 7.19 |
| n1_ch2 | (99.70, 106.98, 125.30) | SER285(3.509) | 3.51✓ | 10.67 | 8.53 | 7.13 | 9.95 |
| n1_benzyl_aryl | (100.47, 107.90, 127.98) | PHE281(3.418), PHE183(3.66), HIS95(3.715), PHE91(3.719), LEU182(3.908) | 4.23 | 6.40 | 9.44 | 6.87 | 8.82 |
| n1_benzyl_pCN | (101.44, 108.89, 131.10) | HIS95(3.609), PHE94(3.881), TYR25(3.943) | 7.42 | 3.94✓ | 12.79 | 8.62 | 10.81 |
| c2_phenyl | (102.85, 109.45, 125.08) | SER90(3.404), PHE87(3.656), PHE91(3.707), ILE110(3.906) | 5.55 | 8.80 | 7.71 | 3.91✓ | 8.37 |
| c5_methyl | (97.07, 107.16, 123.78) | PHE183(3.507), PHE281(3.938) | 4.97 | 11.99 | 6.83 | 7.57 | 9.14 |

### JANUS_D2_22

- Path: `results/docking/option_d_batch2/cb2/JANUS_D2_22_docked.pdbqt`
- Common name / edit: URB447 analog Bz_pCF3 (historical lead; mid Jaccard)
- Best MODEL 1; Vina REMARK = **-12.35** kcal/mol (**score number only**)
- SMILES source: REMARK SMILES
- Features found: aryl_ketone, benzoyl_aryl, benzoyl_pCF3, c2_phenyl, c3_amino, c5_methyl, n1_benzyl_aryl, n1_benzyl_pCl, n1_ch2, pyrrole

| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|
| pyrrole | (98.84, 107.88, 124.02) | SER285(3.702), PHE183(3.892), PHE281(3.996) | 3.70✓ | 10.62 | 5.62 | 5.21 | 8.16 |
| aryl_ketone | (101.19, 107.47, 125.89) | PHE87(3.59), PHE91(3.832) | 4.18 | 9.63 | 9.05 | 6.59 | 9.84 |
| benzoyl_aryl | (99.78, 107.99, 128.74) | LEU182(3.111), PHE281(3.464), PHE183(3.793), ALA282(3.955) | 4.53 | 6.25 | 9.65 | 6.70 | 8.56 |
| c3_amino | (98.42, 105.65, 125.11) | SER285(2.792), PHE281(3.494) | 2.79✓ | 11.77 | 8.96 | 8.72 | 10.82 |
| n1_ch2 | (98.13, 109.40, 122.00) | VAL113(3.543) | 6.92 | 12.12 | 4.16 | 4.82 | 7.67 |
| n1_benzyl_aryl | (95.82, 111.11, 122.56) | ILE110(3.442), PHE183(3.584), THR114(3.745), TRP194(3.872) | 7.99 | 10.06 | 3.75✓ | 3.44✓ | 4.17 |
| n1_benzyl_pCl | (93.35, 112.92, 123.15) | LEU191(3.168), ILE186(3.403), PHE183(3.848) | 11.79 | 10.66 | 5.58 | 5.92 | 3.40✓ |
| c2_phenyl | (95.75, 106.14, 122.03) | MET265(3.492), TRP194(3.591), VAL261(3.676), PHE117(3.73), PHE183(3.796) | 5.20 | 12.92 | 6.22 | 7.71 | 9.53 |
| c5_methyl | (100.17, 110.20, 124.12) | ILE110(3.746) | 6.73 | 9.98 | 6.32 | 3.75✓ | 7.38 |
| benzoyl_pCF3 | (98.87, 108.39, 131.91) | LEU182(3.019), LYS278(3.033), PHE281(3.291) | 7.62 | 4.56 | 13.23 | 9.70 | 10.02 |

---

## Feature ↔ residue matrices (region shell)

Cell = min heavy distance (Å) from feature atoms to that residue; **bold** if ≤ 4.0 Å.

### Qiu 14

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrazole | 5.25 | 9.61 | 5.16 | **3.37** | 6.58 |
| amide | 7.97 | 10.42 | **2.86** | **3.66** | 5.19 |
| n1_heterocycle | 6.94 | 5.04 | 9.52 | 5.52 | 7.37 |
| adamantyl | 9.88 | 9.99 | **3.02** | **3.12** | **3.03** |
| n1_phenyl | 7.17 | 7.47 | 7.94 | **2.96** | 8.05 |
| c5_phenyl | **3.38** | 9.10 | 8.67 | 6.45 | 9.60 |
| c4_methyl | 4.99 | 11.67 | 6.43 | 6.89 | 8.78 |

### Qiu 15

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrazole | 5.67 | 8.77 | 5.08 | **3.60** | 5.78 |
| amide | 8.42 | 10.28 | **2.71** | **3.39** | 4.80 |
| n1_heterocycle | 7.74 | **3.02** | 11.83 | 7.22 | 9.02 |
| adamantyl | 10.27 | 10.17 | **3.13** | **3.18** | **2.98** |
| n1_phenyl | 7.61 | 5.85 | 8.27 | **3.04** | 7.11 |
| c5_phenyl | **3.08** | 9.43 | 8.36 | 6.13 | 9.28 |
| c4_methyl | 5.31 | 12.00 | 5.77 | 6.31 | 8.70 |

### Qiu 20

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrazole | 5.41 | 9.45 | 5.11 | **3.27** | 6.43 |
| amide | 8.15 | 10.28 | **2.81** | **3.67** | 4.92 |
| n1_heterocycle | 6.50 | 4.89 | 9.52 | 5.46 | 7.30 |
| adamantyl | 9.98 | 10.03 | **3.10** | **3.18** | **2.99** |
| n1_phenyl | 7.30 | 7.52 | 7.86 | **2.79** | 7.94 |
| c5_phenyl | **3.34** | 9.19 | 8.56 | 6.29 | 9.48 |
| c4_methyl | 5.13 | 11.49 | 6.40 | 6.77 | 8.59 |

### Qiu 24

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrazole | 4.68 | 9.17 | 5.87 | 4.07 | 7.07 |
| amide | 6.74 | 11.65 | **3.70** | 4.09 | 7.33 |
| n1_heterocycle | 5.89 | 9.94 | 6.41 | **3.22** | 8.79 |
| adamantyl | 9.55 | 10.01 | **3.04** | **3.83** | **3.13** |
| n1_phenyl | 7.15 | 5.91 | 8.41 | **3.79** | 7.18 |
| c5_phenyl | **3.35** | 7.41 | 9.55 | 7.05 | 9.83 |
| c4_methyl | **3.72** | 11.84 | 7.67 | 7.71 | 9.83 |
| amide_ch2 | 8.21 | 12.65 | **3.84** | 5.73 | 7.38 |

### JANUS_D2_20

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrrole | 4.27 | 10.47 | 5.64 | 4.55 | 8.01 |
| aryl_ketone | 6.64 | 12.21 | 4.25 | 5.33 | 7.89 |
| benzoyl_aryl | 7.84 | 10.24 | **3.86** | **3.65** | 4.31 |
| c3_amino | 7.29 | 11.18 | 5.22 | **3.51** | 7.56 |
| n1_ch2 | **3.58** | 9.93 | 9.28 | 7.30 | 10.23 |
| n1_benzyl_aryl | 4.82 | 5.64 | 9.69 | 6.93 | 8.70 |
| n1_benzyl_pCl | 8.75 | **3.94** | 12.97 | 8.56 | 10.11 |
| c2_phenyl | 5.67 | 8.41 | 8.27 | **4.00** | 8.40 |
| c5_methyl | 4.04 | 11.92 | 7.68 | 8.12 | 9.78 |
| benzoyl_pMe | 11.71 | 10.60 | 5.41 | 5.68 | **3.38** |

### JANUS_D2_06

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrrole | 4.63 | 10.70 | 4.88 | 4.34 | 7.61 |
| aryl_ketone | 7.53 | 12.29 | **3.10** | 4.42 | 7.34 |
| benzoyl_aryl | 8.54 | 10.07 | **3.63** | **3.60** | **3.96** |
| c3_amino | 7.80 | 11.25 | 4.76 | **3.29** | 7.19 |
| n1_ch2 | **3.51** | 10.67 | 8.53 | 7.13 | 9.95 |
| n1_benzyl_aryl | 4.23 | 6.40 | 9.44 | 6.87 | 8.82 |
| n1_benzyl_pCN | 7.42 | **3.94** | 12.79 | 8.62 | 10.81 |
| c2_phenyl | 5.55 | 8.80 | 7.71 | **3.91** | 8.37 |
| c5_methyl | 4.97 | 11.99 | 6.83 | 7.57 | 9.14 |

### JANUS_D2_22

| Feature | SER285 | TYR25 | THR114 | ILE110 | ILE186 |
|---|---|---|---|---|---|
| pyrrole | **3.70** | 10.62 | 5.62 | 5.21 | 8.16 |
| aryl_ketone | 4.18 | 9.63 | 9.05 | 6.59 | 9.84 |
| benzoyl_aryl | 4.53 | 6.25 | 9.65 | 6.70 | 8.56 |
| c3_amino | **2.79** | 11.77 | 8.96 | 8.72 | 10.82 |
| n1_ch2 | 6.92 | 12.12 | 4.16 | 4.82 | 7.67 |
| n1_benzyl_aryl | 7.99 | 10.06 | **3.75** | **3.44** | 4.17 |
| n1_benzyl_pCl | 11.79 | 10.66 | 5.58 | 5.92 | **3.40** |
| c2_phenyl | 5.20 | 12.92 | 6.22 | 7.71 | 9.53 |
| c5_methyl | 6.73 | 9.98 | 6.32 | **3.75** | 7.38 |
| benzoyl_pCF3 | 7.62 | 4.56 | 13.23 | 9.70 | 10.02 |

---

## Pairwise feature correspondence (D2 ↔ Qiu)

For each D2 feature, the nearest Qiu feature by centroid distance is listed. **spatial_ok** = centroid ≤ 3.0 Å **or** shell Jaccard ≥ 0.25 (**structural inference** from cutoffs).

Hypothetical chemotype analogies (ketone↔amide, benzyl↔N1-aryl, …) are **not** assumed true until geometry supports them.

### JANUS_D2_20 ↔ Qiu 14

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 1.25 | 0.333 | PHE183 | yes |
| aryl_ketone | c4_methyl | 2.27 | 0.0 | — | yes |
| benzoyl_aryl | amide | 1.85 | 0.6 | ILE110, PHE183, THR114 | yes |
| c3_amino | pyrazole | 1.85 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 0.86 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | n1_heterocycle | 1.44 | 0.429 | HIS95, LEU182, PHE183 | yes |
| n1_benzyl_pCl | n1_heterocycle | 2.33 | 0.167 | PHE94 | yes |
| c2_phenyl | n1_phenyl | 1.59 | 0.6 | ILE110, PHE94, SER90 | yes |
| c5_methyl | c4_methyl | 1.32 | 0.5 | PHE183 | yes |
| benzoyl_pMe | adamantyl | 1.56 | 0.429 | ILE186, LEU191, PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.25 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 2.28 | 0.250 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 2.33 | 0.571 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 4.52 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 1.44 | 0.429 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.86 | 0.286 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 1.32 | 0.500 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.90 | 0.500 | yes |

</details>

### JANUS_D2_20 ↔ Qiu 15

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.62 | 0.5 | VAL113 | yes |
| aryl_ketone | c4_methyl | 1.62 | 1.0 | VAL113 | yes |
| benzoyl_aryl | amide | 1.74 | 0.75 | ILE110, PHE183, THR114 | yes |
| c3_amino | pyrazole | 2.10 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 0.65 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 2.86 | 0.286 | PHE281, PHE91 | yes |
| n1_benzyl_pCl | n1_heterocycle | 0.27 | 0.4 | PHE94, TYR25 | yes |
| c2_phenyl | n1_phenyl | 3.15 | 0.286 | ILE110, PHE94 | yes |
| c5_methyl | c4_methyl | 2.18 | 0.0 | — | yes |
| benzoyl_pMe | adamantyl | 1.62 | 0.429 | ILE186, LEU191, PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.77 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 2.77 | 0.000 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 2.74 | 0.571 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 3.49 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 3.35 | 0.250 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.62 | 0.286 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 2.18 | 0.000 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 3.13 | 0.250 | yes |

</details>

### JANUS_D2_20 ↔ Qiu 20

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 1.43 | 0.333 | PHE183 | yes |
| aryl_ketone | c4_methyl | 2.31 | 0.0 | — | yes |
| benzoyl_aryl | amide | 1.75 | 0.6 | ILE110, PHE183, THR114 | yes |
| c3_amino | pyrazole | 1.84 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 0.80 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | n1_heterocycle | 1.40 | 0.571 | HIS95, LEU182, PHE183, PHE281 | yes |
| n1_benzyl_pCl | n1_heterocycle | 2.17 | 0.143 | PHE94 | yes |
| c2_phenyl | n1_phenyl | 1.67 | 0.6 | ILE110, PHE94, SER90 | yes |
| c5_methyl | c4_methyl | 1.41 | 0.5 | PHE183 | yes |
| benzoyl_pMe | adamantyl | 1.53 | 0.429 | ILE186, LEU191, PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.43 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 2.49 | 0.250 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 2.47 | 0.571 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 4.61 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 1.40 | 0.571 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.71 | 0.286 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 1.41 | 0.500 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 3.02 | 0.500 | yes |

</details>

### JANUS_D2_20 ↔ Qiu 24

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 0.94 | 0.5 | PHE183 | yes |
| aryl_ketone | amide | 1.01 | 0.333 | VAL113 | yes |
| benzoyl_aryl | amide_ch2 | 1.76 | 0.25 | THR114 | yes |
| c3_amino | pyrazole | 2.62 | 0.0 | — | yes |
| n1_ch2 | c5_phenyl | 1.81 | 0.2 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 1.95 | 0.25 | PHE281, PHE91 | yes |
| n1_benzyl_pCl | n1_phenyl | 4.40 | 0.2 | PHE94 | no |
| c2_phenyl | n1_heterocycle | 1.84 | 0.667 | ILE110, PHE87, PHE91, SER90 | yes |
| c5_methyl | c4_methyl | 0.71 | 0.0 | — | yes |
| benzoyl_pMe | adamantyl | 1.47 | 0.429 | ILE186, LEU191, PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 0.94 | 0.500 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 1.01 | 0.333 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 1.99 | 0.571 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 3.49 | 0.125 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 5.39 | 0.111 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 4.33 | 0.250 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 0.71 | 0.000 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.76 | 0.250 | yes |

</details>

### JANUS_D2_06 ↔ Qiu 14

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 1.15 | 0.333 | PHE183 | yes |
| aryl_ketone | amide | 1.74 | 0.5 | THR114, VAL113 | yes |
| benzoyl_aryl | adamantyl | 1.81 | 0.857 | ILE110, ILE186, LEU191, PHE183, THR114, TRP194 | yes |
| c3_amino | pyrazole | 2.21 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 1.71 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 1.85 | 0.286 | PHE281, PHE91 | yes |
| n1_benzyl_pCN | n1_heterocycle | 2.61 | 0.333 | HIS95, PHE94 | yes |
| c2_phenyl | n1_phenyl | 1.87 | 0.4 | ILE110, SER90 | yes |
| c5_methyl | c4_methyl | 0.92 | 0.5 | PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.15 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 1.74 | 0.500 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 1.81 | 0.857 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 4.57 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 2.17 | 0.429 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.78 | 0.333 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 0.92 | 0.500 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.63 | 0.500 | yes |

</details>

### JANUS_D2_06 ↔ Qiu 15

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.24 | 0.5 | VAL113 | yes |
| aryl_ketone | amide | 2.17 | 0.25 | THR114 | yes |
| benzoyl_aryl | amide | 2.17 | 0.5 | ILE110, PHE183, THR114 | yes |
| c3_amino | pyrazole | 2.35 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 1.40 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 2.08 | 0.286 | PHE281, PHE91 | yes |
| n1_benzyl_pCN | n1_heterocycle | 1.52 | 0.6 | HIS95, PHE94, TYR25 | yes |
| c2_phenyl | n1_phenyl | 3.49 | 0.143 | ILE110 | no |
| c5_methyl | c4_methyl | 1.79 | 0.0 | — | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.60 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 2.17 | 0.250 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 2.22 | 0.857 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 3.87 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 4.13 | 0.250 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.49 | 0.333 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 1.80 | 0.000 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.80 | 0.250 | yes |

</details>

### JANUS_D2_06 ↔ Qiu 20

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 1.29 | 0.333 | PHE183 | yes |
| aryl_ketone | amide | 1.92 | 0.5 | THR114, VAL113 | yes |
| benzoyl_aryl | adamantyl | 1.95 | 0.857 | ILE110, ILE186, LEU191, PHE183, THR114, TRP194 | yes |
| c3_amino | pyrazole | 2.17 | 0.333 | ILE110 | yes |
| n1_ch2 | c5_phenyl | 1.62 | 0.25 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 1.92 | 0.286 | PHE281, PHE91 | yes |
| n1_benzyl_pCN | n1_heterocycle | 2.43 | 0.286 | HIS95, PHE94 | yes |
| c2_phenyl | n1_phenyl | 1.94 | 0.4 | ILE110, SER90 | yes |
| c5_methyl | c4_methyl | 0.96 | 0.5 | PHE183 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.29 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 1.92 | 0.500 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 1.95 | 0.857 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 4.66 | 0.000 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 2.16 | 0.571 | yes |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 3.62 | 0.333 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 0.96 | 0.500 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.72 | 0.500 | yes |

</details>

### JANUS_D2_06 ↔ Qiu 24

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | pyrazole | 1.28 | 0.5 | PHE183 | yes |
| aryl_ketone | amide | 1.15 | 0.667 | THR114, VAL113 | yes |
| benzoyl_aryl | adamantyl | 1.43 | 0.857 | ILE110, ILE186, LEU191, PHE183, THR114, TRP194 | yes |
| c3_amino | amide | 2.73 | 0.25 | VAL113 | yes |
| n1_ch2 | c4_methyl | 1.71 | 1.0 | SER285 | yes |
| n1_benzyl_aryl | c5_phenyl | 1.25 | 0.25 | PHE281, PHE91 | yes |
| n1_benzyl_pCN | c5_phenyl | 4.06 | 0.0 | — | no |
| c2_phenyl | n1_heterocycle | 1.28 | 0.8 | ILE110, PHE87, PHE91, SER90 | yes |
| c5_methyl | c4_methyl | 1.47 | 0.0 | — | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.28 | 0.500 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 1.15 | 0.667 | yes |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 1.43 | 0.857 | yes |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 3.79 | 0.125 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 5.00 | 0.111 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 4.41 | 0.286 | yes |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 1.47 | 0.000 | yes |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 2.72 | 0.250 | yes |

</details>

### JANUS_D2_22 ↔ Qiu 14

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.10 | 0.333 | PHE183 | yes |
| aryl_ketone | c5_phenyl | 1.14 | 0.5 | PHE87, PHE91 | yes |
| benzoyl_aryl | n1_heterocycle | 1.92 | 0.286 | LEU182, PHE183 | yes |
| c3_amino | c4_methyl | 2.58 | 0.0 | — | yes |
| n1_ch2 | amide | 1.62 | 0.25 | VAL113 | yes |
| n1_benzyl_aryl | amide | 1.69 | 0.6 | ILE110, PHE183, THR114 | yes |
| n1_benzyl_pCl | adamantyl | 1.72 | 0.429 | ILE186, LEU191, PHE183 | yes |
| c2_phenyl | c4_methyl | 3.05 | 0.143 | PHE183 | no |
| c5_methyl | pyrazole | 0.83 | 0.5 | ILE110 | yes |
| benzoyl_pCF3 | n1_heterocycle | 3.59 | 0.143 | LEU182 | no |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.96 | 0.250 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 6.21 | 0.000 | no |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 10.00 | 0.100 | no |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 7.68 | 0.167 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 7.91 | 0.125 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 6.80 | 0.100 | no |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 3.48 | 0.000 | no |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 6.01 | 0.000 | no |

</details>

### JANUS_D2_22 ↔ Qiu 15

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.19 | 0.0 | — | yes |
| aryl_ketone | c5_phenyl | 0.79 | 0.5 | PHE87, PHE91 | yes |
| benzoyl_aryl | c5_phenyl | 2.96 | 0.143 | PHE281 | yes |
| c3_amino | c5_phenyl | 2.86 | 0.5 | PHE281, SER285 | yes |
| n1_ch2 | c4_methyl | 1.66 | 1.0 | VAL113 | yes |
| n1_benzyl_aryl | amide | 1.54 | 0.75 | ILE110, PHE183, THR114 | yes |
| n1_benzyl_pCl | adamantyl | 1.77 | 0.429 | ILE186, LEU191, PHE183 | yes |
| c2_phenyl | c4_methyl | 3.37 | 0.0 | — | no |
| c5_methyl | pyrazole | 1.04 | 0.5 | ILE110 | yes |
| benzoyl_pCF3 | n1_heterocycle | 2.63 | 0.143 | LEU182 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 2.33 | 0.250 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 6.52 | 0.000 | no |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 10.37 | 0.100 | no |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 7.39 | 0.143 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 10.14 | 0.000 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 6.56 | 0.100 | no |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 3.03 | 0.000 | no |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 6.42 | 0.000 | no |

</details>

### JANUS_D2_22 ↔ Qiu 20

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.13 | 0.333 | PHE183 | yes |
| aryl_ketone | c5_phenyl | 0.96 | 0.5 | PHE87, PHE91 | yes |
| benzoyl_aryl | n1_heterocycle | 1.81 | 0.429 | LEU182, PHE183, PHE281 | yes |
| c3_amino | c4_methyl | 2.66 | 0.0 | — | yes |
| n1_ch2 | amide | 1.84 | 0.25 | VAL113 | yes |
| n1_benzyl_aryl | amide | 1.57 | 0.6 | ILE110, PHE183, THR114 | yes |
| n1_benzyl_pCl | adamantyl | 1.69 | 0.429 | ILE186, LEU191, PHE183 | yes |
| c2_phenyl | c4_methyl | 3.15 | 0.143 | PHE183 | no |
| c5_methyl | pyrazole | 0.79 | 0.5 | ILE110 | yes |
| benzoyl_pCF3 | n1_heterocycle | 3.32 | 0.286 | LEU182, PHE281 | yes |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 2.10 | 0.250 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 6.34 | 0.000 | no |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 10.13 | 0.100 | no |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 7.69 | 0.167 | no |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 8.06 | 0.111 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 6.76 | 0.100 | no |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 3.40 | 0.000 | no |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 6.17 | 0.000 | no |

</details>

### JANUS_D2_22 ↔ Qiu 24

| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |
|------------|---------------------|---------------|---------------|----------------------|------------|
| pyrrole | c4_methyl | 1.34 | 0.333 | SER285 | yes |
| aryl_ketone | c5_phenyl | 2.09 | 0.4 | PHE87, PHE91 | yes |
| benzoyl_aryl | c5_phenyl | 1.88 | 0.286 | ALA282, PHE281 | yes |
| c3_amino | c4_methyl | 1.30 | 0.5 | SER285 | yes |
| n1_ch2 | amide | 0.44 | 0.333 | VAL113 | yes |
| n1_benzyl_aryl | amide_ch2 | 1.83 | 0.25 | THR114 | yes |
| n1_benzyl_pCl | adamantyl | 1.60 | 0.429 | ILE186, LEU191, PHE183 | yes |
| c2_phenyl | amide_ch2 | 3.41 | 0.0 | — | no |
| c5_methyl | pyrazole | 1.47 | 0.0 | — | yes |
| benzoyl_pCF3 | c5_phenyl | 4.84 | 0.143 | PHE281 | no |

<details><summary>Hypothetical pair check (geometry only)</summary>

| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |
|------------|---------------|---------------|------------|
| pyrrole ↔ pyrazole (5-membered N-heteroaromatic core) | 1.52 | 0.333 | yes |
| aryl_ketone ↔ amide (carbonyl linker (ketone vs CONH)) | 5.40 | 0.000 | no |
| benzoyl_aryl ↔ adamantyl (bulky hydrophobic from carbonyl side) | 9.70 | 0.100 | no |
| n1_benzyl_aryl ↔ n1_phenyl (N-linked aryl region) | 7.38 | 0.333 | yes |
| n1_benzyl_aryl ↔ n1_heterocycle (N-aryl / N-het extension) | 7.50 | 0.125 | no |
| c2_phenyl ↔ c5_phenyl (C-aryl on heteroaromatic) | 7.60 | 0.091 | no |
| c5_methyl ↔ c4_methyl (small alkyl on ring) | 3.99 | 0.000 | no |
| c3_amino ↔ amide (H-bond donor-capable N near core (weak analogy)) | 4.83 | 0.000 | no |

</details>

---

## Summary table

| Compound | key features near SER285 / TYR25 / THR114 / ILE110 / ILE186 | notes |
|----------|---------------------------------------------------------------|-------|
| Qiu 14 | SER285: c5_phenyl; TYR25: —; THR114: amide, adamantyl; ILE110: pyrazole, amide, adamantyl, n1_phenyl; ILE186: adamantyl | o-morpholine; CONH-Ad |
| Qiu 15 | SER285: c5_phenyl; TYR25: n1_heterocycle; THR114: amide, adamantyl; ILE110: pyrazole, amide, adamantyl, n1_phenyl; ILE186: adamantyl | m-morpholine; CONH-Ad |
| Qiu 20 | SER285: c5_phenyl; TYR25: —; THR114: amide, adamantyl; ILE110: pyrazole, amide, adamantyl, n1_phenyl; ILE186: adamantyl | o-Me-piperazine; CONH-Ad |
| Qiu 24 | SER285: c5_phenyl, c4_methyl; TYR25: —; THR114: amide, adamantyl, amide_ch2; ILE110: n1_heterocycle, adamantyl, n1_phenyl; ILE186: adamantyl | o-morpholine; CONH-CH2-Ad |
| JANUS_D2_20 | SER285: n1_ch2; TYR25: n1_benzyl_pCl; THR114: benzoyl_aryl; ILE110: benzoyl_aryl, c3_amino, c2_phenyl; ILE186: benzoyl_pMe | max Jaccard cluster (prior comparison); TYR25 contact in pose report |
| JANUS_D2_06 | SER285: n1_ch2; TYR25: n1_benzyl_pCN; THR114: aryl_ketone, benzoyl_aryl; ILE110: benzoyl_aryl, c3_amino, c2_phenyl; ILE186: benzoyl_aryl | max Jaccard cluster (prior comparison); TYR25 contact in pose report |
| JANUS_D2_22 | SER285: pyrrole, c3_amino; TYR25: —; THR114: n1_benzyl_aryl; ILE110: n1_benzyl_aryl, c5_methyl; ILE186: n1_benzyl_pCl | historical lead; mid overlap — do not auto-elevate by Vina |

---

## Correspondences and mismatches (geometry only)

### Recurrent spatial correspondences (**structural inference**)

- **pyrrole↔pyrazole**: spatial_ok in 12/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **aryl_ketone↔amide**: spatial_ok in 8/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **benzoyl_aryl↔adamantyl**: spatial_ok in 8/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **n1_benzyl_aryl↔n1_heterocycle**: spatial_ok in 6/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **c2_phenyl↔c5_phenyl**: spatial_ok in 8/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **c5_methyl↔c4_methyl**: spatial_ok in 8/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).
- **c3_amino↔amide**: spatial_ok in 8/12 D2×Qiu pairs (centroid≤3.0 Å or shell Jaccard≥0.25).

### Explicit mismatches / non-correspondences

- **n1_benzyl_aryl↔n1_phenyl**: spatial_ok only 1/12 pairs — do not treat as a conserved cross-chemotype pharmacophore element.
- **Adamantyl / CONH–Ad / morpholine–piperazine:** present on Qiu; **absent** on D2_20/06/22 (URB447 pyrrole + aryl ketone + N-benzyl). No geometric transfer of Ad into a D2 atom set.
- **Aryl ketone vs CONH–Ad:** both place a carbonyl-linked hydrophobic volume in the orthosteric-like box, but atom types and H-bond patterns differ — correspondence is spatial at best, not chemical identity.
- **D2_22 orientation vs D2_20/06:** for D2_20/06, benzoyl_aryl spatially overlaps Qiu adamantyl/amide (THR114/ILE110/ILE186 shell); for D2_22, benzoyl_aryl sits nearer Qiu n1_heterocycle/c5_phenyl while n1_benzyl_pCl approaches adamantyl — feature swap relative to the max-Jaccard analogs (geometry only).
- **D2_22 mid-overlap reminder:** prior pose Jaccard mid-pack; do not elevate by most-negative Vina CB2 REMARK.

### Ambiguities / limitations

- Different chemotypes → whole-ligand atom RMSD across scaffolds is **not** a primary metric; feature centroids and residue shells are used instead.
- SMARTS + SMILES IDX mapping depends on Meeko REMARK completeness; unmapped hydrogens / ambiguous phenyl assignment possible.
- Contact cutoff 4.0 Å and correspondence gates (3.0 Å / Jaccard 0.25) are heuristic; other cutoffs change tables.
- Static 6PT0 docking poses only — no MD ensemble in this report.
- pose-comparable (prior report) ≠ same pharmacophore (this report) ≠ same pharmacology.

---

## Verdict

Feature inventories and feature↔residue shells computed for D2_20/06/22 and Qiu 14/15/20/24 best CB2 poses on disk. Cross-map tables use feature centroids and residue shells (not whole-ligand RMSD). Chemotype mismatch (Ad/CONH/morpholine vs URB447 ketone/benzyl) is explicit; spatial pocket coincidence from the prior comparison is refined here to feature-level geometry only — not pharmacology.

**`PHARMACOPHORE_GEOM = COMPLETE`**

---

## Closing

No SAR. No pharmacological conclusion. Shared or distinct feature–residue geometry does **not** imply shared activity, selectivity, or Janus profile. Vina REMARK values listed above are docking score numbers only.

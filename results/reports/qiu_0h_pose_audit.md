# Qiu 0H — Descriptive CB2 pose audit (Qiu 14/15/20/24 vs D2_20/06/22)

> **Scope:** read-only geometry / contacts for **existing** best PDBQT poses. No re-docking; no Vina; no PDBQT edits.
>
> **No SAR / no pharmacological conclusions / no affinity claims from Vina scores.**
>
> **Date:** 2026-08-12
>
> **Script:** `scripts/audit_qiu_0h_poses.py`
>
> **Upstream:** [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md), [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md), [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md), [`qiu_0d_0g_integration_qc.md`](qiu_0d_0g_integration_qc.md)

---

## Methods

### Poses used (strict)

| Set | Path pattern | IDs |
|-----|----------------|-----|
| Qiu | `results/docking/qiu_0f/compound_{N}_cb2_out.pdbqt` | 14, 15, 20, 24 |
| D2 | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | JANUS_D2_20, JANUS_D2_06, JANUS_D2_22 |
| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` chain R | — |

- A pose counts **only** if it is a `MODEL` / `ENDMDL` block with `REMARK VINA RESULT` in the PDBQT.
- Qiu log-only modes not written to out PDBQT are **excluded** (same 0F/0G rule; compounds **15** and **20**).
- **Comparable pose** = MODEL with the **lowest (most negative)** Vina REMARK among written models.

### Cutoffs (reuse 0G / pharmacophore geometry)

| Label | Definition |
|-------|------------|
| **Contact residue** | ≥1 ligand–receptor heavy-atom pair ≤ **4.0 Å** |
| **H-bond (geometry OK)** | D–A ≤ 3.5 Å **and** H···A ≤ 2.5 Å **and** angle D–H···A ≥ 120.0° |
| **Polar proximity (not H-bond)** | Polar heavy (OA/NA/N/O/SA/OS) ≤ 3.5 Å without geometry-OK H-bond |
| **Hydrophobic proximity** | C/A–C/A pairs within contact cutoff |
| **Feature correspondence** | Feature centroid ≤ **3.0 Å** **or** shell Jaccard ≥ **0.25** |
| **0G region shell** | SER285, TYR25, THR114, ILE110, ILE186 |

### Epistemic labels (required)

| Label | Meaning |
|-------|---------|
| **Observación** | Coordinates, Vina REMARK numbers, contact lists, SMARTS hits, distances at fixed cutoffs |
| **Inferencia** | Jaccard / correspondence / conservation / feature-swap flags from those cutoffs |
| **Interpretación** | Brief structural notes (scaffold orientation, occupation); **not** activity or SAR |

---

## Inventory

| Item | Status |
|------|--------|
| Receptor | present |
| Qiu 14 out PDBQT | present (9 MODELs) |
| Qiu 15 out PDBQT | present (8 MODELs) |
| Qiu 20 out PDBQT | present (5 MODELs) |
| Qiu 24 out PDBQT | present (9 MODELs) |
| JANUS_D2_20 docked PDBQT | present (9 MODELs) |
| JANUS_D2_06 docked PDBQT | present (8 MODELs) |
| JANUS_D2_22 docked PDBQT | present (9 MODELs) |

---

## Per-compound audits

### Qiu 14 (o-morpholine; CONH-Ad)

**Path:** `results/docking/qiu_0f/compound_14_cb2_out.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 9 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-9.919** kcal/mol | Observación (score-only) |
| Ligand centroid | (98.774, 110.334, 124.791) | Observación |
| Dist. to box center | 1.318 Å | Observación |

#### 2. Contacts / interactions

- **Observación — contact residues (heavy ≤ 4.0 Å, principal):** LEU182, SER90, THR114, ILE110, ILE186, PHE91, PHE281, PHE183, TRP194, SER285, PHE87, LEU191
- **Observación — n contacts:** 17
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - O(OA) ··· THR114 OG1(OA) = 2.861 Å
  - O(OA) ··· LEU182 O(OA) = 3.175 Å
- **Observación — hydrophobic proximity (examples):** ILE110(2.964 Å), ILE186(3.026 Å), PHE91(3.063 Å), THR114(3.069 Å), PHE281(3.245 Å), PHE183(3.291 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.375 | yes |
| TYR25 | 5.041 | no |
| THR114 | 2.861 | yes |
| ILE110 | 2.964 | yes |
| ILE186 | 3.026 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrazole | Centroid |
|-------|----------------------------|----------|
| adamantyl | -x | (94.390, 112.740, 121.783) |
| n1_heterocycle | +z | (100.300, 109.826, 128.947) |
| c5_phenyl | -y | (100.757, 106.689, 126.603) |
| n1_phenyl | +x | (102.777, 111.181, 125.801) |
| amide | -x | (97.460, 110.855, 122.271) |

*Label: Observación (coordinates); Interpretación: structural placement only — not pharmacology.*

#### 5. Conservation vs Qiu 0G feature map

- **Observación:** features found = adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole
- **Interpretación:** this is a Qiu reference pose; conservation column applies to D2 compounds below.

---

### Qiu 15 (m-morpholine; CONH-Ad)

**Path:** `results/docking/qiu_0f/compound_15_cb2_out.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 8 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-11.201** kcal/mol | Observación (score-only) |
| Ligand centroid | (98.533, 110.694, 125.354) | Observación |
| Dist. to box center | 1.93 Å | Observación |

**Observación (prior 0F/0G):** compound 15 had ≥1 log mode not written to PDBQT (`energy_range`); this audit uses written MODELs only.

#### 2. Contacts / interactions

- **Observación — contact residues (heavy ≤ 4.0 Å, principal):** THR114, ILE186, TYR25, ILE110, PHE87, SER285, PHE183, PHE91, PHE94, PHE281, TYR190, PRO184
- **Observación — n contacts:** 18
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - O(OA) ··· THR114 OG1(OA) = 2.71 Å
  - O(OA) ··· TYR25 O(OA) = 3.021 Å
  - O(OA) ··· ILE110 O(OA) = 3.389 Å
- **Observación — hydrophobic proximity (examples):** ILE186(2.978 Å), ILE110(3.038 Å), PHE87(3.059 Å), THR114(3.132 Å), PHE91(3.25 Å), SER285(3.287 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.081 | yes |
| TYR25 | 3.021 | yes |
| THR114 | 2.71 | yes |
| ILE110 | 3.038 | yes |
| ILE186 | 2.978 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrazole | Centroid |
|-------|----------------------------|----------|
| adamantyl | -x | (94.225, 113.078, 121.610) |
| n1_heterocycle | +z | (100.713, 110.202, 131.396) |
| c5_phenyl | -y | (100.775, 106.871, 126.190) |
| n1_phenyl | +z | (101.381, 111.609, 127.400) |
| amide | -z | (97.325, 111.334, 122.347) |

*Label: Observación (coordinates); Interpretación: structural placement only — not pharmacology.*

#### 5. Conservation vs Qiu 0G feature map

- **Observación:** features found = adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole
- **Interpretación:** this is a Qiu reference pose; conservation column applies to D2 compounds below.
- **Observación:** TYR25 in region shell (m-morpholine extension) — consistent with 0G.

---

### Qiu 20 (o-Me-piperazine; CONH-Ad)

**Path:** `results/docking/qiu_0f/compound_20_cb2_out.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 5 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-9.986** kcal/mol | Observación (score-only) |
| Ligand centroid | (98.772, 110.394, 124.914) | Observación |
| Dist. to box center | 1.446 Å | Observación |

**Observación (prior 0F/0G):** compound 20 had ≥1 log mode not written to PDBQT (`energy_range`); this audit uses written MODELs only.

#### 2. Contacts / interactions

- **Observación — contact residues (heavy ≤ 4.0 Å, principal):** LEU182, ILE110, SER90, THR114, ILE186, PHE91, PHE183, PHE281, SER285, PHE87, LEU191, TRP194
- **Observación — n contacts:** 17
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - O(OA) ··· THR114 OG1(OA) = 2.815 Å
  - N(NA) ··· LEU182 O(OA) = 3.176 Å
- **Observación — hydrophobic proximity (examples):** ILE110(2.786 Å), ILE186(2.991 Å), PHE91(3.062 Å), THR114(3.103 Å), PHE183(3.318 Å), PHE281(3.334 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.338 | yes |
| TYR25 | 4.888 | no |
| THR114 | 2.815 | yes |
| ILE110 | 2.786 | yes |
| ILE186 | 2.991 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrazole | Centroid |
|-------|----------------------------|----------|
| adamantyl | -x | (94.296, 112.846, 121.747) |
| n1_heterocycle | +z | (100.215, 109.689, 129.161) |
| c5_phenyl | -y | (100.818, 106.784, 126.458) |
| n1_phenyl | +x | (102.806, 111.269, 125.771) |
| amide | -x | (97.371, 111.047, 122.327) |

*Label: Observación (coordinates); Interpretación: structural placement only — not pharmacology.*

#### 5. Conservation vs Qiu 0G feature map

- **Observación:** features found = adamantyl, amide, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole
- **Interpretación:** this is a Qiu reference pose; conservation column applies to D2 compounds below.

---

### Qiu 24 (o-morpholine; CONH-CH2-Ad)

**Path:** `results/docking/qiu_0f/compound_24_cb2_out.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 9 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-11.606** kcal/mol | Observación (score-only) |
| Ligand centroid | (98.918, 109.893, 124.438) | Observación |
| Dist. to box center | 0.899 Å | Observación |

#### 2. Contacts / interactions

- **Observación — contact residues (heavy ≤ 4.0 Å, principal):** PRO184, LEU191, PHE87, THR114, VAL113, PHE91, ILE186, ILE110, SER90, ALA282, SER285, PHE183
- **Observación — n contacts:** 16
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - N(N) ··· SER90 OG(OA) = 3.407 Å
- **Observación — hydrophobic proximity (examples):** PRO184(2.805 Å), LEU191(2.896 Å), PHE91(3.061 Å), THR114(3.096 Å), ILE186(3.133 Å), ILE110(3.216 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.354 | yes |
| TYR25 | 5.912 | no |
| THR114 | 3.035 | yes |
| ILE110 | 3.216 | yes |
| ILE186 | 3.133 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrazole | Centroid |
|-------|----------------------------|----------|
| adamantyl | -x | (94.237, 112.231, 122.009) |
| n1_heterocycle | +x | (102.959, 109.193, 123.839) |
| c5_phenyl | +z | (100.712, 106.684, 127.771) |
| n1_phenyl | +z | (101.636, 111.395, 127.097) |
| amide | -z | (97.762, 109.473, 122.239) |

*Label: Observación (coordinates); Interpretación: structural placement only — not pharmacology.*

#### 5. Conservation vs Qiu 0G feature map

- **Observación:** features found = adamantyl, amide, amide_ch2, c4_methyl, c5_phenyl, n1_heterocycle, n1_phenyl, pyrazole
- **Interpretación:** this is a Qiu reference pose; conservation column applies to D2 compounds below.
- **Inferencia (vs 14/15/20):** N1-heterocycle dominant axis differs (rotated within same box) — consistent with 0G.

---

### JANUS_D2_20

**Path:** `results/docking/option_d_batch2/cb2/JANUS_D2_20_docked.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 9 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-11.656** kcal/mol | Observación (score-only) |
| Ligand centroid | (99.346, 109.365, 125.055) | Observación |
| Dist. to box center | 1.595 Å | Observación |

#### 2. Contacts / interactions

- **Observación — contact residues (principal):** LEU182, VAL113, ILE186, LEU191, PHE91, HIS95, ILE110, PHE281, PHE94, SER285, SER90, PHE183
- **Observación — n contacts:** 16
- **Observación — H-bond geometry OK:** none
- **Observación — hydrophobic proximity (examples):** ILE186(3.384 Å), LEU191(3.391 Å), PHE91(3.48 Å), PHE281(3.51 Å), PHE94(3.542 Å), ILE110(3.647 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.58 | yes |
| TYR25 | 3.942 | yes |
| THR114 | 3.859 | yes |
| ILE110 | 3.506 | yes |
| ILE186 | 3.384 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrrole | Centroid |
|-------|---------------------------|----------|
| benzoyl_aryl | -x | (95.647, 110.976, 122.642) |
| n1_benzyl_aryl | +z | (100.453, 108.452, 128.554) |
| aryl_ketone | -z | (97.669, 108.678, 121.624) |
| c2_phenyl | +x | (103.060, 109.625, 125.623) |
| c3_amino | +y | (100.307, 110.439, 122.669) |

*Label: Observación; Interpretación: URB447-like scaffold placement — not Ad/CONH identity.*

#### 5. Conservation / loss of 0G features (vs Qiu map)

| D2 feature | Qiu feature | spatial_ok | Status | Label |
|------------|-------------|------------|--------|-------|
| pyrrole | pyrazole | 4/4 | conserved_spatial | Inferencia |
| aryl_ketone | amide | 4/4 | conserved_spatial | Inferencia |
| benzoyl_aryl | adamantyl | 4/4 | conserved_spatial | Inferencia |
| n1_benzyl_aryl | n1_heterocycle | 3/4 | conserved_spatial | Inferencia |
| c2_phenyl | c5_phenyl | 4/4 | conserved_spatial | Inferencia |
| c5_methyl | c4_methyl | 4/4 | conserved_spatial | Inferencia |

- **Observación — Qiu-only features absent on D2:** adamantyl, amide, n1_heterocycle, amide_ch2
- **Inferencia — benzoyl/benzyl vs Ad/N1-het orientation pattern:** Qiu 14=canonical_like, Qiu 15=canonical_like, Qiu 20=canonical_like, Qiu 24=canonical_like
- **Inferencia:** orientation pattern closer to canonical Ad↔benzoyl / N1-het↔benzyl spatial pairing (vs D2_22).

---

### JANUS_D2_06

**Path:** `results/docking/option_d_batch2/cb2/JANUS_D2_06_docked.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 8 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-12.03** kcal/mol | Observación (score-only) |
| Ligand centroid | (99.374, 109.275, 124.924) | Observación |
| Dist. to box center | 1.527 Å | Observación |

#### 2. Contacts / interactions

- **Observación — contact residues (principal):** THR114, ILE110, SER90, PHE281, PHE183, SER285, VAL113, HIS95, PHE87, PHE91, TRP194, LEU191
- **Observación — n contacts:** 16
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - O(OA) ··· THR114 OG1(OA) = 3.105 Å
- **Observación — hydrophobic proximity (examples):** PHE281(3.418 Å), PHE183(3.507 Å), ILE110(3.6 Å), VAL113(3.607 Å), PHE87(3.656 Å), PHE91(3.719 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 3.509 | yes |
| TYR25 | 3.943 | yes |
| THR114 | 3.105 | yes |
| ILE110 | 3.293 | yes |
| ILE186 | 3.955 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrrole | Centroid |
|-------|---------------------------|----------|
| benzoyl_aryl | -x | (95.175, 111.355, 122.635) |
| n1_benzyl_aryl | +z | (100.468, 107.896, 127.977) |
| aryl_ketone | -z | (97.383, 109.527, 121.150) |
| c2_phenyl | +x | (102.849, 109.452, 125.085) |
| c3_amino | +y | (100.090, 110.881, 122.384) |

*Label: Observación; Interpretación: URB447-like scaffold placement — not Ad/CONH identity.*

#### 5. Conservation / loss of 0G features (vs Qiu map)

| D2 feature | Qiu feature | spatial_ok | Status | Label |
|------------|-------------|------------|--------|-------|
| pyrrole | pyrazole | 4/4 | conserved_spatial | Inferencia |
| aryl_ketone | amide | 4/4 | conserved_spatial | Inferencia |
| benzoyl_aryl | adamantyl | 4/4 | conserved_spatial | Inferencia |
| n1_benzyl_aryl | n1_heterocycle | 3/4 | conserved_spatial | Inferencia |
| c2_phenyl | c5_phenyl | 4/4 | conserved_spatial | Inferencia |
| c5_methyl | c4_methyl | 4/4 | conserved_spatial | Inferencia |

- **Observación — Qiu-only features absent on D2:** adamantyl, amide, n1_heterocycle, amide_ch2
- **Inferencia — benzoyl/benzyl vs Ad/N1-het orientation pattern:** Qiu 14=canonical_like, Qiu 15=canonical_like, Qiu 20=canonical_like, Qiu 24=canonical_like
- **Inferencia:** orientation pattern closer to canonical Ad↔benzoyl / N1-het↔benzyl spatial pairing (vs D2_22).

---

### JANUS_D2_22

**Path:** `results/docking/option_d_batch2/cb2/JANUS_D2_22_docked.pdbqt`

#### 1. Comparable pose

| Field | Value | Label |
|-------|-------|-------|
| Poses in PDBQT | 9 | Observación |
| Best MODEL | **1** | Observación |
| Vina REMARK | **-12.35** kcal/mol | Observación (score-only) |
| Ligand centroid | (97.885, 108.410, 125.271) | Observación |
| Dist. to box center | 1.93 Å | Observación |

#### 2. Contacts / interactions

- **Observación — contact residues (principal):** SER285, LEU182, LYS278, LEU191, PHE281, ILE186, ILE110, MET265, VAL113, PHE183, PHE87, TRP194
- **Observación — n contacts:** 18
- **Observación — H-bond geometry OK:** none
- **Observación — polar proximity (not H-bond):**
  - N(N) ··· SER285 OG(OA) = 2.792 Å
- **Observación — hydrophobic proximity (examples):** ILE110(3.442 Å), PHE281(3.464 Å), VAL113(3.543 Å), PHE183(3.584 Å), TRP194(3.591 Å), VAL261(3.676 Å)

#### 3. Region distances (whole ligand → residue)

| Residue | min heavy (Å) | ≤4.0 Å? |
|---------|---------------|---------|
| SER285 | 2.792 | yes |
| TYR25 | 4.562 | no |
| THR114 | 3.745 | yes |
| ILE110 | 3.442 | yes |
| ILE186 | 3.403 | yes |

*Label: Observación*

#### 4. Orientation of key groups

| Group | Dominant axis from pyrrole | Centroid |
|-------|---------------------------|----------|
| benzoyl_aryl | +z | (99.777, 107.987, 128.744) |
| n1_benzyl_aryl | +y | (95.819, 111.111, 122.559) |
| aryl_ketone | +x | (101.194, 107.465, 125.891) |
| c2_phenyl | -x | (95.750, 106.142, 122.035) |
| c3_amino | -y | (98.422, 105.646, 125.114) |

*Label: Observación; Interpretación: URB447-like scaffold placement — not Ad/CONH identity.*

#### 5. Conservation / loss of 0G features (vs Qiu map)

| D2 feature | Qiu feature | spatial_ok | Status | Label |
|------------|-------------|------------|--------|-------|
| pyrrole | pyrazole | 4/4 | conserved_spatial | Inferencia |
| aryl_ketone | amide | 0/4 | lost_or_weak | Inferencia |
| benzoyl_aryl | adamantyl | 0/4 | lost_or_weak | Inferencia |
| n1_benzyl_aryl | n1_heterocycle | 0/4 | lost_or_weak | Inferencia |
| c2_phenyl | c5_phenyl | 0/4 | lost_or_weak | Inferencia |
| c5_methyl | c4_methyl | 0/4 | lost_or_weak | Inferencia |

- **Observación — Qiu-only features absent on D2:** adamantyl, amide, n1_heterocycle, amide_ch2
- **Inferencia — benzoyl/benzyl vs Ad/N1-het orientation pattern:** Qiu 14=feature_swap, Qiu 15=feature_swap, Qiu 20=feature_swap, Qiu 24=feature_swap
- **Inferencia:** D2_22 shows **feature_swap** vs Qiu Ad/N1-het pairing more often than D2_20/06 (consistent with pharmacophore geometry report).
- **Interpretación:** mid pocket-overlap + swapped feature placement; do **not** elevate by most-negative Vina REMARK.

---

## Cross-comparison (Qiu ↔ D2) — descriptive

Not a ranking. Occupation and feature conservation only.

### Pocket occupation (Observación + Inferencia)

| Pair | Δcentroid (Å) | Contact Jaccard | Cloud overlap @2 Å | Notes |
|------|---------------|-----------------|--------------------|-------|
| Qiu_14 ↔ JANUS_D2_20 | 1.156 | 0.833 | 0.882 | high Jaccard cluster vs Qiu |
| Qiu_14 ↔ JANUS_D2_06 | 1.224 | 0.833 | 0.909 | high Jaccard cluster vs Qiu |
| Qiu_14 ↔ JANUS_D2_22 | 2.173 | 0.522 | 0.742 | mid overlap; feature-swap orientation |
| Qiu_15 ↔ JANUS_D2_20 | 1.586 | 0.789 | 0.701 | both contact TYR25 shell |
| Qiu_15 ↔ JANUS_D2_06 | 1.705 | 0.789 | 0.724 | both contact TYR25 shell |
| Qiu_15 ↔ JANUS_D2_22 | 2.376 | 0.5 | 0.599 | mid overlap; feature-swap orientation |
| Qiu_20 ↔ JANUS_D2_20 | 1.187 | 0.833 | 0.871 | high Jaccard cluster vs Qiu |
| Qiu_20 ↔ JANUS_D2_06 | 1.271 | 0.833 | 0.868 | high Jaccard cluster vs Qiu |
| Qiu_20 ↔ JANUS_D2_22 | 2.202 | 0.522 | 0.734 | mid overlap; feature-swap orientation |
| Qiu_24 ↔ JANUS_D2_20 | 0.918 | 0.684 | 0.835 | high Jaccard cluster vs Qiu |
| Qiu_24 ↔ JANUS_D2_06 | 0.909 | 0.684 | 0.858 | high Jaccard cluster vs Qiu |
| Qiu_24 ↔ JANUS_D2_22 | 1.99 | 0.619 | 0.664 | mid overlap; feature-swap orientation |

### Feature conservation summary (Inferencia)

| D2 | Conserved spatial axes (≥2/4 Qiu) | Weak/lost axes | Qiu-only absent | Orientation vs Ad/het |
|----|-----------------------------------|----------------|-----------------|----------------------|
| JANUS_D2_20 | pyrrole↔pyrazole, aryl_ketone↔amide, benzoyl_aryl↔adamantyl, n1_benzyl_aryl↔n1_heterocycle, c2_phenyl↔c5_phenyl, c5_methyl↔c4_methyl | — | adamantyl, amide, n1_heterocycle, amide_ch2 | canonical_like |
| JANUS_D2_06 | pyrrole↔pyrazole, aryl_ketone↔amide, benzoyl_aryl↔adamantyl, n1_benzyl_aryl↔n1_heterocycle, c2_phenyl↔c5_phenyl, c5_methyl↔c4_methyl | — | adamantyl, amide, n1_heterocycle, amide_ch2 | canonical_like |
| JANUS_D2_22 | pyrrole↔pyrazole | aryl_ketone↔amide, benzoyl_aryl↔adamantyl, n1_benzyl_aryl↔n1_heterocycle, c2_phenyl↔c5_phenyl, c5_methyl↔c4_methyl | adamantyl, amide, n1_heterocycle, amide_ch2 | feature_swap |

### Brief pairwise notes

- **Observación:** All seven best poses sit in the same CB2 orthosteric-like box (centroids within ~1–2.4 Å of Qiu consensus; consistent with prior D1 comparison).
- **Observación:** No geometry-OK H-bonds under 0G criteria for any of the seven audited poses (polar proximities may exist).
- **Inferencia:** D2_20 and D2_06 conserve more spatial axes vs Qiu Ad/amide/N1-het map; D2_22 more often shows benzoyl↔N1-het / benzyl↔Ad feature swap.
- **Observación:** Adamantyl, CONH–Ad amide, and morpholine/piperazine are Qiu-only; D2 poses use pyrrole + aryl ketone + N-benzyl chemistry.
- **Interpretación:** Shared occupation ≠ same pharmacophore ≠ same pharmacology (axiom from pharmacophore geometry report).

---

## Ambiguities / limitations

1. Static docking only (6PT0); no MD / ensemble.
2. Vina REMARK ≠ experimental affinity.
3. Compounds 15 and 20: log had extra modes not written to PDBQT — excluded by design (0F/0G).
4. No geometry-OK H-bonds under stated angle criterion; polar O···Thr/Ser contacts are proximities.
5. Contact cutoff 4.0 Å and feature gates (3.0 Å / Jaccard 0.25) are heuristic.
6. Cross-chemotype whole-ligand RMSD omitted; cloud overlap and residue Jaccard are occupation proxies.
7. D1 vs Qiu ligand preparation pipelines may differ; same receptor PDBQT.
8. Chemotype mismatch (Ad/CONH/morpholine vs URB447 ketone/benzyl) limits chemical identity of 'conserved' features — spatial only.
9. D2_22 feature-swap is geometric inference; not a pharmacological mode claim.

---

## Summary table

| Compound | MODEL | Vina (score-only) | Region hits | H-bonds OK | Key orientation note |
|----------|-------|-------------------|-------------|------------|----------------------|
| Qiu_14 | 1 | -9.919 | 4/5 | 0 | Ad -x; N1-het +z; C5-Ph -y |
| Qiu_15 | 1 | -11.201 | 5/5 | 0 | Ad -x; N1-het +z; C5-Ph -y |
| Qiu_20 | 1 | -9.986 | 4/5 | 0 | Ad -x; N1-het +z; C5-Ph -y |
| Qiu_24 | 1 | -11.606 | 4/5 | 0 | Ad -x; N1-het +x; C5-Ph +z |
| JANUS_D2_20 | 1 | -11.656 | 5/5 | 0 | Bz -x; NBn +z; pattern=canonical_like |
| JANUS_D2_06 | 1 | -12.03 | 5/5 | 0 | Bz -x; NBn +z; pattern=canonical_like |
| JANUS_D2_22 | 1 | -12.35 | 4/5 | 0 | Bz +z; NBn +y; pattern=feature_swap |

---

## Verdict

All 7 poses audited cleanly from written PDBQTs with consistent cutoffs. Observations retained: Qiu 15/20 log↔PDBQT energy_range mismatch; chemotype mismatch (Ad/CONH vs URB447); D2_22 feature-swap; no geometry-OK H-bonds under 0G criteria. These are documented limitations, not file failures.

**`0H = PASS WITH OBSERVATIONS`**

---

## Closing

No SAR. No pharmacological conclusion. Shared pocket occupation or feature↔residue geometry does **not** imply shared activity, selectivity, or Janus profile. Vina REMARK values are docking score numbers only.

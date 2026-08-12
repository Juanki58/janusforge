# Qiu 0G vs Option D Batch D1 — CB2 geometric pose comparison

> **Scope:** geometry / pocket occupation of **existing on-disk** CB2 poses only. No re-docking; no PDBQT edits; no pharmacological or SAR conclusions.
>
> **Date:** 2026-08-12
>
> **Script:** `scripts/compare_qiu_0g_vs_d1_cb2.py` (read-only inputs; regenerates `qiu_0g_vs_d1_cb2_pose_comparison_data.json` locally)
>
> **Upstream:** [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md), [`qiu_0f_docking_qc.md`](qiu_0f_docking_qc.md), [`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md)

---

## Methods

### Poses used (strict)

| Set | Path pattern | n |
|-----|----------------|---|
| **D1 (Batch2 CB2)** | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | 36 |
| **Qiu 0G refs** | `results/docking/qiu_0f/compound_{14,15,20,24}_cb2_out.pdbqt` | 4 |

- A pose counts **only** if it is a `MODEL` / `ENDMDL` block with `REMARK VINA RESULT` in the PDBQT.
- Qiu log-only modes (not written to out PDBQT) are **excluded** (same rule as 0G).
- Best pose = MODEL with the **lowest (most negative)** Vina score among written models.

### Receptor

- `data/targets/cb2/6PT0_rec.pdbqt`, chain **R** (same as Qiu 0F/0G).

### Contact / occupation definitions (match 0G)

| Label | Definition |
|-------|------------|
| **Contact residue** | ≥1 ligand–receptor **heavy-atom** pair at distance **≤ 4.0 Å** (hydrogens excluded). |
| **Ligand centroid** | Mean of ligand heavy-atom coordinates (best pose). |
| **Qiu consensus centroid** | Mean of the four Qiu best-pose ligand centroids. |
| **Contact Jaccard** | \|A ∩ B\| / \|A ∪ B\| for contact-residue sets. |
| **Atom-cloud overlap** | Mean of (fraction of A heavy atoms within **2.0 Å** of any B heavy atom) and the reverse. Used as a cross-chemotype pocket-occupation proxy. |
| **0G region shell** | Contact to **SER285, TYR25, THR114, ILE110, ILE186** (highlighted in 0G). |

**Not used:** whole-ligand RMSD between D1 and Qiu chemotypes (different atom counts / scaffolds — not meaningful).

### Two comparison tracks (kept separate)

| Track | What it means | What it does **not** mean |
|-------|----------------|---------------------------|
| **Pose comparable** | Geometry / occupation metrics below | Affinity, efficacy, Janus profile |
| **Score comparable** | Numeric Vina `REMARK` values side-by-side | Experimental potency (Kᵢ / IC₅₀ / ΔG) |

### Pose-comparable gates (documented heuristic)

A D1 best pose is labeled:

- **pose_comparable** if distance to Qiu consensus centroid ≤ **3.0 Å** **and** Jaccard vs Qiu contact **union** ≥ **0.40**
- **pose_partially_comparable** if centroid or (Jaccard + ≥3/5 region hits) only
- **pose_different** otherwise

These thresholds reuse the 0G “comparable region” spirit (centroid drift ≤ 3 Å; Jaccard ≥ 0.40), applied D1→Qiu.

### Epistemic labels

- **Observed:** coordinates, Vina REMARK numbers, contact lists at fixed cutoffs.
- **Inference:** Jaccard / cloud-overlap / classification labels from those cutoffs.
- **Interpretation:** brief structural notes (scaffold features); not activity claims.

---

## Inventory confirmation

| Item | Status |
|------|--------|
| Receptor `6PT0_rec.pdbqt` | present |
| Qiu outs 14 / 15 / 20 / 24 | **4/4** present |
| D1 CB2 `*_docked.pdbqt` | **36/36** present |

**D1 IDs:** `JANUS_D2_01`…`32`, `URB447`, `GW405833`, `delta9-THCV`, `delta9-THC`.

---

## Qiu reference best poses (geometry + score columns)

| Cpd | poses in PDBQT | best MODEL | best Vina (kcal/mol) | ligand centroid | 0G region hits |
|-----|----------------|------------|----------------------|-----------------|----------------|
| 14 | 9 | 1 | −9.919 | (98.774, 110.334, 124.791) | SER285, THR114, ILE110, ILE186 |
| 15 | 8 | 1 | −11.201 | (98.533, 110.694, 125.354) | SER285, **TYR25**, THR114, ILE110, ILE186 |
| 20 | 5 | 1 | −9.986 | (98.772, 110.394, 124.914) | SER285, THR114, ILE110, ILE186 |
| 24 | 9 | 1 | −11.606 | (98.918, 109.893, 124.438) | SER285, THR114, ILE110, ILE186 |

**Observed Qiu consensus centroid:** (98.749, 110.329, 124.874)

**Observed Qiu intersection contacts (all four):**  
ILE110, ILE186, LEU191, PHE87, PHE91, PHE94, PHE183, PHE281, PRO184, SER285, THR114, TRP194, VAL113  
(matches 0G shared core).

Scores = Vina only (**score comparable**, not experimental affinity).

---

## Summary: D1 vs Qiu consensus (pose + score)

Sorted by contact Jaccard vs Qiu **union** (pose track), then ascending centroid distance.

| ID | Vina CB2 (score) | Δcentroid→Qiu mean (Å) | Jaccard vs Qiu union | Jaccard vs Qiu ∩ | mean cloud overlap @2 Å | 0G region n/5 | TYR25 | SER285 | pose class |
|----|------------------|------------------------|----------------------|------------------|-------------------------|---------------|-------|--------|------------|
| JANUS_D2_20 | −11.656 | 1.15 | **0.76** | 0.71 | 0.82 | 5 | yes | yes | pose_comparable |
| JANUS_D2_06 | −12.030 | 1.23 | **0.76** | 0.71 | 0.84 | 5 | yes | yes | pose_comparable |
| JANUS_D2_32 | −11.529 | 0.99 | 0.71 | 0.75 | 0.84 | 4 | no | yes | pose_comparable |
| URB447 | −11.660 | 1.05 | 0.71 | 0.75 | 0.86 | 4 | no | yes | pose_comparable |
| JANUS_D2_30 | −11.063 | 1.16 | 0.71 | 0.75 | 0.85 | 4 | no | yes | pose_comparable |
| JANUS_D2_08 | −11.449 | 1.17 | 0.71 | 0.65 | 0.83 | 4 | no | yes | pose_comparable |
| JANUS_D2_23 | −11.892 | 1.25 | 0.71 | 0.75 | 0.83 | 4 | no | yes | pose_comparable |
| JANUS_D2_05 | −12.168 | 1.42 | 0.71 | 0.75 | 0.83 | 4 | no | yes | pose_comparable |
| JANUS_D2_16 | −10.919 | 1.50 | 0.70 | 0.72 | 0.80 | 4 | no | yes | pose_comparable |
| JANUS_D2_28 | −11.058 | 1.58 | 0.70 | 0.72 | 0.79 | 4 | no | yes | pose_comparable |
| JANUS_D2_02 | −11.615 | 1.22 | 0.67 | 0.69 | 0.84 | 4 | no | yes | pose_comparable |
| JANUS_D2_12 | −11.481 | 1.35 | 0.67 | 0.69 | 0.81 | 4 | no | yes | pose_comparable |
| JANUS_D2_26 | −10.609 | 1.86 | 0.64 | 0.65 | 0.74 | 4 | no | yes | pose_comparable |
| JANUS_D2_15 | −11.698 | 1.68 | 0.62 | 0.72 | 0.79 | 4 | no | yes | pose_comparable |
| JANUS_D2_01 | −12.060 | 1.91 | 0.62 | 0.63 | 0.66 | 4 | no | yes | pose_comparable |
| JANUS_D2_04 | −11.612 | 1.96 | 0.62 | 0.63 | 0.70 | 4 | no | yes | pose_comparable |
| JANUS_D2_03 | −12.081 | 2.01 | 0.62 | 0.63 | 0.68 | 4 | no | yes | pose_comparable |
| JANUS_D2_10 | −12.098 | 1.88 | 0.61 | 0.61 | 0.70 | 4 | no | yes | pose_comparable |
| JANUS_D2_24 | −11.266 | 1.79 | 0.60 | 0.68 | 0.76 | 4 | no | yes | pose_comparable |
| JANUS_D2_18 | −11.557 | 1.92 | 0.58 | 0.67 | 0.74 | 4 | no | yes | pose_comparable |
| JANUS_D2_11 | −11.402 | 1.96 | 0.58 | 0.67 | 0.69 | 4 | no | yes | pose_comparable |
| JANUS_D2_14 | −11.254 | 2.02 | 0.58 | 0.67 | 0.68 | 4 | no | yes | pose_comparable |
| JANUS_D2_31 | −11.312 | 1.52 | 0.57 | 0.65 | 0.77 | 4 | no | yes | pose_comparable |
| JANUS_D2_25 | −11.334 | 1.87 | 0.56 | 0.72 | 0.76 | 4 | no | yes | pose_comparable |
| **JANUS_D2_22** | **−12.350** | **2.14** | **0.56** | **0.55** | **0.68** | **4** | **no** | **yes** | **pose_comparable** |
| JANUS_D2_13 | −11.273 | 2.06 | 0.54 | 0.61 | 0.74 | 4 | no | yes | pose_comparable |
| JANUS_D2_27 | −11.637 | 2.07 | 0.54 | 0.61 | 0.68 | 4 | no | yes | pose_comparable |
| GW405833 | −10.064 | 2.10 | 0.54 | 0.61 | 0.79 | 4 | no | yes | pose_comparable |
| JANUS_D2_07 | −11.816 | 2.15 | 0.54 | 0.61 | 0.67 | 4 | no | yes | pose_comparable |
| JANUS_D2_09 | −10.970 | 1.84 | 0.52 | 0.50 | 0.73 | 3 | no | yes | pose_comparable |
| JANUS_D2_21 | −11.185 | 1.99 | 0.48 | 0.53 | 0.72 | 4 | no | yes | pose_comparable |
| JANUS_D2_19 | −11.510 | 2.15 | 0.48 | 0.53 | 0.70 | 4 | no | yes | pose_comparable |
| JANUS_D2_29 | −12.015 | 2.21 | 0.48 | 0.53 | 0.70 | 4 | no | yes | pose_comparable |
| delta9-THC | −10.039 | 1.64 | 0.48 | 0.62 | 0.67 | 3 | no | no | pose_comparable |
| JANUS_D2_17 | −10.170 | 2.41 | 0.46 | 0.59 | 0.69 | 4 | no | yes | pose_comparable |
| delta9-THCV | −9.859 | 2.00 | 0.44 | 0.56 | 0.60 | 3 | no | no | pose_comparable |

**Classification counts (inference):** pose_comparable **36/36**; partially **0**; different **0**.

**Centroid drift (observed):** distance to Qiu mean ranges **0.99–2.41 Å** (all ≤ 3.0 Å). Max pairwise centroid distance to any Qiu ref is **2.86 Å** (D2_17 vs 15).

---

## Centroid distances to each Qiu ref (Å) — pose track

| ID | vs 14 | vs 15 | vs 20 | vs 24 |
|----|------:|------:|------:|------:|
| JANUS_D2_20 | 1.16 | 1.59 | 1.19 | 0.92 |
| JANUS_D2_06 | 1.22 | 1.70 | 1.27 | 0.91 |
| JANUS_D2_32 | 0.97 | 1.56 | 1.05 | 0.53 |
| URB447 | 1.04 | 1.58 | 1.10 | 0.68 |
| JANUS_D2_30 | 1.14 | 1.70 | 1.21 | 0.72 |
| JANUS_D2_08 | 1.15 | 1.71 | 1.22 | 0.74 |
| JANUS_D2_23 | 1.23 | 1.78 | 1.30 | 0.83 |
| JANUS_D2_05 | 1.44 | 1.80 | 1.46 | 1.23 |
| **JANUS_D2_22** | **2.17** | **2.38** | **2.20** | **1.99** |
| JANUS_D2_17 | 2.40 | 2.86 | 2.49 | 2.00 |
| delta9-THCV | 1.94 | 2.59 | 2.07 | 1.42 |
| delta9-THC | 1.58 | 2.27 | 1.71 | 1.00 |

(Full 36×4 matrix in local JSON from the script.)

---

## JANUS_D2_22 (prior docking lead) — explicit callout

| Metric | Value | Track |
|--------|-------|-------|
| Best Vina CB2 | **−12.350** (MODEL 1; 9 poses written) | score comparable only |
| Ligand centroid | (97.885, 108.410, 125.271) | observed |
| Δ to Qiu consensus | **2.14 Å** | pose |
| Centroid vs Qiu 14 / 15 / 20 / 24 | 2.17 / 2.38 / 2.20 / 1.99 Å | pose |
| Jaccard vs Qiu union / ∩ | 0.56 / 0.55 | pose |
| Mean atom-cloud overlap @2 Å | 0.68 | pose |
| Fraction of 0G core residues contacted | 11/13 (0.85) | pose |
| 0G region shell | SER285, THR114, ILE110, ILE186 (**not** TYR25) | pose |
| Pose class | **pose_comparable** | inference |

**Shared contacts with Qiu 14 (example):** ILE110, ILE186, LEU182, LEU191, PHE87, PHE91, PHE183, PHE281, SER285, THR114, TRP194, VAL113.

**Structural observation (not SAR):** D2_22 SMARTS labels show aryl-ketone + pyrrole-like + CF3 — **no** adamantyl / CONH–Ad amide / morpholine of the Qiu set. Occupation of the same CB2 box is geometric coincidence of docking poses, not chemotype identity.

**Interpretation (geometry only):** among D1, D2_22 is **not** the closest pose-overlap to Qiu (mid-pack Jaccard 0.56; centroid ~2.1 Å). Its Vina CB2 number is the most negative in this D1 CB2 set — that is a **score** observation only and must not be read as experimental potency or as “more Qiu-like.”

---

## Top pose-overlap D1 compounds (vs Qiu region)

Highest contact Jaccard vs Qiu union (and strong cloud overlap):

1. **JANUS_D2_20** — Jac 0.76; Δcent 1.15 Å; cloud 0.82; **all five** 0G region residues including **TYR25**
2. **JANUS_D2_06** — Jac 0.76; Δcent 1.23 Å; cloud 0.84; **TYR25** yes
3. **JANUS_D2_32**, **URB447**, **JANUS_D2_30**, **JANUS_D2_08**, **JANUS_D2_23**, **JANUS_D2_05** — Jac 0.71; centroids ~1.0–1.4 Å; SER285/THR114/ILE110/ILE186 yes; TYR25 no

**Closest to Qiu consensus centroid:** JANUS_D2_32 (0.99 Å), URB447 (1.05 Å).

**TYR25 contact (observed):** only **JANUS_D2_20** and **JANUS_D2_06** among D1 (plus Qiu **15** among refs). Most D1 poses match the 14/20/24-like shell without TYR25.

**Lower overlap (still pose_comparable by gates):** `delta9-THCV` (Jac 0.44; no SER285), `JANUS_D2_17` (Jac 0.46; farthest centroid 2.41 Å), `delta9-THC` (Jac 0.48; no SER285). These still sit in the same box by centroid criterion but share fewer contacts with the Qiu union.

---

## Orientation notes (structural observation only)

| Series | Observed scaffold features (SMARTS on REMARK SMILES) | Pocket note |
|--------|------------------------------------------------------|-------------|
| Qiu 14/15/20/24 | adamantyl + CONH amide + pyrazole; morpholine (14/15/24) or piperazine (20) | Ad/amide pyrazoles in 0G orthosteric-like region |
| URB447 / most JANUS_D2_* | aryl-ketone + pyrrole-like (URB447-family); some CF3 / N-benzyl variants | Same CB2 box by centroid/contacts; **different** functional-group set (ketone vs CONH–Ad) |
| GW405833 | morpholine + pyrrole-like | Morpholine present (also in Qiu N1-sub); still not Ad-amide |
| THCV / THC | phytocannabinoid (no Ad/amide/pyrazole labels) | Occupy box with fewer shared contacts; no SER285 in best pose |

**Inference:** D1 and Qiu **co-occupy** the same CB2 docking region under 0G cutoffs; substituent chemical identity (Ad/amide vs URB447 ketone scaffold) is **not** the same. Do not equate shared pocket occupation with shared pharmacology.

---

## Score-comparable column (Vina only)

| Set | Best-pose Vina range (kcal/mol) |
|-----|----------------------------------|
| Qiu 14/15/20/24 | −9.919 … −11.606 |
| D1 CB2 (36) | −9.859 (THCV) … −12.350 (D2_22) |

These numbers are **docking scores from written PDBQTs**. They are **not** experimental affinities and are **not** converted to potency claims here. Qiu −11.201 / −11.606 and D1 dual/CB2 scores from gate summaries remain score proxies only ([`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md)).

---

## Limitations

1. **Static docking only** — single CB2 conformation (6PT0); no MD / ensemble in this comparison.
2. **Vina ≠ experimental affinity**; score columns are not potency.
3. **Cross-chemotype ligand RMSD omitted by design**; cloud overlap @2 Å and residue Jaccard are occupation proxies, cutoff-sensitive.
4. **Contact cutoff 4.0 Å** inherited from 0G; 3.5 / 4.5 Å would change residue lists.
5. **Different preparation pipelines** (D1 batch2 vs Qiu 0E/0F) — same receptor PDBQT, but ligand prep / protonation may differ.
6. **Orientation SMARTS** are coarse (presence/absence); no Ad vector transfer onto URB447 scaffolds.
7. Pose PDBQTs are local/gitignored; this report records derived geometry metrics only.
8. All 36 pass the stated gates — that reflects a shared box, **not** that every D1 pose is indistinguishable from Qiu 15/24.

---

## Verdict

All required files present (36 D1 CB2 + 4 Qiu outs + receptor). Best poses extracted; centroid, contact Jaccard, atom-cloud overlap, and 0G region occupation computed with 0G cutoffs. **D1 and Qiu occupy a comparable CB2 region** (centroids within ~1–2.4 Å of Qiu mean; Jaccard vs Qiu union 0.44–0.76). Top pose-overlap: **D2_20 / D2_06** (and URB447 / D2_32 cluster). Prior lead **D2_22** is pose-comparable but mid-pack on overlap (Δcent 2.14 Å, Jac 0.56); its top Vina CB2 score is score-track only.

**`COMPARISON = COMPLETE`**

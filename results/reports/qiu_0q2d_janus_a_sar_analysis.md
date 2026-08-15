# 0Q.2d — SAR analysis of audited Janus **A** ligands only

**Date:** 2026-08-15  
**Branch:** `cursor/qiu-protocol-ip-cro-0p`  
**Authority:** `qiu_0q2c_dataset_audit.md` (Janus A list + assay facts)  
**Supporting:** `qiu_0q2c_janus_ligand_dataset.md/.csv`; `qiu_0q2_smrf_expand_v2.md` (Vasiljevik pair context); `qiu_0d_structure_verification.md` (Qiu-14 SMILES)

**Scope:** Structure and SAR for the **four** audit-grade Janus **A** compounds only.  
**Absolute bans respected:** no new molecule design, no proposed substitutions, no docking/MD, no invented mechanisms. Correlation vs SAR-pair-backed features are separated.

**Janus A set (n = 4):** URB447 · Qiu-14 · Vasiljevik-27 · Vasiljevik-30

**Grade scale (this report):**

| Grade | Meaning |
|-------|---------|
| **STRONG** | Same-lab dual functional panels + within-family structural neighbor(s) that close the claim |
| **MODERATE** | Usable same-lab dual-func contrast, but multi-site edit and/or incomplete comparator arm |
| **WEAK** | Suggestive within-family signal with major assay gaps, or cross-scaffold coincidence only |
| **UNSUPPORTED** | Author narrative, docking, or cross-scaffold pattern without auditable SAR pairs |

---

## 1. Unequivocal chemical structures

SMILES were generally **not printed** in primary OA text. IUPAC from primary / audited reconstruction; SMILES from PubChem (URB447) or 0D reconstruction matching published schemes (Qiu-14); Vasiljevik SMILES derived 1:1 from primary experimental IUPAC names (PMC3904296).

### 1.1 URB447 (JAN-1; LoVerme/Piomelli 8b)

| Field | Value |
|-------|--------|
| **IUPAC (primary abstract)** | [4-amino-1-(4-chlorobenzyl)-2-methyl-5-phenyl-1H-pyrrol-3-yl](phenyl)methanone |
| **Scaffold** | 4-amino-3-benzoylpyrrole |
| **SMILES** | `CC1=C(C(=C(N1CC2=CC=C(C=C2)Cl)C3=CC=CC=C3)N)C(=O)C4=CC=CC=C4` |
| **InChIKey** | `KGXYGMKEFDUWNB-UHFFFAOYSA-N` |
| **Formula** | C₂₅H₂₁ClN₂O |
| **Source** | LoVerme et al. *BMCL* 2009 DOI [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059); PubChem CID 25195055 (SMILES) |
| **Key substituents** | N1 = *p*-chlorobenzyl; C2 = Me; C3 = benzoyl; C4 = NH₂; C5 = Ph |

### 1.2 Qiu-14 (JAN-4)

| Field | Value |
|-------|--------|
| **IUPAC (0D from SI Scheme S1 / GA)** | *N*-(adamantan-1-yl)-4-methyl-1-(2-morpholinophenyl)-5-phenyl-1*H*-pyrazole-3-carboxamide |
| **Scaffold** | 1H-pyrazole-3-carboxamide |
| **SMILES (0D, RDKit)** | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` |
| **InChIKey** | `QQXQVTJJXRACOB-UHFFFAOYSA-N` |
| **Formula** | C₃₁H₃₆N₄O₂ |
| **Source** | Qiu et al. *Bioorg. Chem.* 2023 DOI [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377); SI Scheme S1 (identity); `qiu_0d_structure_verification.md` |
| **Key substituents** | N1 = 2-morpholinophenyl (**ortho**); C3 = CONH–(1-adamantyl); C4 = Me; C5 = Ph |

### 1.3 Vasiljevik-27 (JAN-5)

| Field | Value |
|-------|--------|
| **IUPAC (primary experimental)** | 1-butyl-7-methoxy-3-(naphthalen-1-ylmethyl)-1H-indole |
| **Scaffold** | 7-methoxy-N-butylindole (aminoalkylindole-related) |
| **SMILES (from IUPAC)** | `CCCCn1cc(Cc2cccc3ccccc23)c2cccc(OC)c21` |
| **Source** | Vasiljevik et al. *J. Med. Chem.* 2013 DOI [10.1021/jm400268b](https://doi.org/10.1021/jm400268b); PMC3904296 |
| **Key substituents** | N1 = *n*-butyl; C3 = CH₂–(1-naphthyl); C7 = OMe |

### 1.4 Vasiljevik-30 (JAN-6)

| Field | Value |
|-------|--------|
| **IUPAC (primary experimental)** | 1-butyl-7-methoxy-3-(naphthalen-2-yl)-1H-indole |
| **Scaffold** | same as V-27 |
| **SMILES (from IUPAC)** | `CCCCn1cc(-c2ccc3ccccc3c2)c2cccc(OC)c21` |
| **Source** | same as V-27 |
| **Key substituents** | N1 = *n*-butyl; C3 = **direct** 2-naphthyl (no methylene); C7 = OMe |

---

## 2. Shared substructures across the set (what actually overlaps)

Honest overlap among **all four** Janus A ligands is **minimal**.

| Putative shared motif | Present in | Chemically identical across A set? | Comment |
|----------------------|------------|--------------------------------------|---------|
| Aromatic N-heterocycle core | all 4 | **NO** — pyrrole vs pyrazole vs indole | Only “heteroaromatic core” at high abstraction |
| N1 lipophilic/aryl substitution | all 4 | **NO** — *p*Cl-benzyl vs *o*-morpholinophenyl vs *n*-butyl | Different attachment chemistry |
| Peripheral bulky aryl / polycycle distal to core | all 4 | **NO** — C5-Ph + benzoyl (URB); C5-Ph + Ad-amide (Qiu); naphthyl (V) | Different linkers and positions |
| Carbonyl next to core | URB, Qiu | **NO** — ketone (URB C3) vs carboxamide (Qiu C3) | V-27/30 **lack** C3 carbonyl |
| Phenyl at a “C5-like” ring position | URB, Qiu | **YES** within those two only | Absent on V-27/30 |
| Naphthalene | V-27, V-30 | **YES** within Vasiljevik pair only | Absent on URB/Qiu |
| 1-Adamantyl | Qiu-14 only among A | — | Not shared |
| Morpholine | Qiu-14 only among A | — | Not shared |

**Verdict on set-wide substructure:** There is **no** single shared chemotype fragment that is chemically conserved across all four A ligands. The set is a **phenotype-defined multi-scaffold collection**, not a common pharmacophore series.

---

## 3. Structural differences (pairwise / by family)

### 3.1 Within Vasiljevik (only within-family A pair)

| | V-27 | V-30 |
|---|------|------|
| Core | identical 1-butyl-7-methoxyindole | identical |
| C3 | CH₂–(1-naphthyl) | direct bond to **2**-naphthyl |
| Edit type | methylene linker + 1-naphthyl regio | no linker + 2-naphthyl regio |
| Distance from identity | **two** changes (linker **and** naphthyl attachment atom) | — |

They are **near neighbors**, not regioisomers of each other (V-27 is 1-naphthyl**methyl**; V-30 is 2-naphthyl **direct**). Closest audited minimal-edit neighbors are **V-35** (1-naphthyl direct) — see §7.

### 3.2 URB447 vs Qiu-14

| Feature | URB447 | Qiu-14 |
|---------|--------|--------|
| Core | pyrrole | pyrazole |
| N1 | CH₂–(*p*Cl-Ph) | *o*-morpholino-Ph (direct N–Ar) |
| C3 | Ph–C(=O)– | –C(=O)NH–(1-Ad) |
| C4 | NH₂ | Me |
| C5 | Ph | Ph |
| Extra polarity | 4-NH₂ | morpholine O/N |

**Comparable honestly:** only the loose diaryl-heterocycle + distal lipophile pattern at high abstraction. **Not** atom-mapped SAR.

### 3.3 URB447 / Qiu-14 vs Vasiljevik-27/30

| Feature | URB / Qiu | V-27 / V-30 |
|---------|-----------|-------------|
| Core | 5-membered azole | fused indole |
| C3 carbonyl | present | **absent** |
| Distal aryl | benzoyl-Ph or Ad-amide | naphthyl |
| N-alkyl | benzyl / N-aryl | *n*-butyl |
| 7-OMe | no | yes |

**Comparable honestly:** almost nothing at fragment identity level.

---

## 4. What can **really** be compared across families

| Comparison level | Valid? | What it supports |
|------------------|--------|------------------|
| **Within Vasiljevik** (27 vs 30; vs 19/35) | **YES** | Real SAR narrative (see §7) |
| **Within URB series** (5b/8a/3c vs 447) | **PARTIAL** | Binding emergence; function incomplete on neighbors |
| **Within Qiu series** (14 vs 15/20/24) | **STRUCTURE YES; PHARMACOLOGY OA NO** | Identity contrast only until paywalled phenotypes audited |
| **Across URB ↔ Qiu ↔ Vasiljevik** | **NO for atom-level SAR** | Only phenotype co-occurrence / weak correlations |
| **Docking-aligned “shared poses”** | **Banned / not used** | Computational (Qiu S173/S285, S8) — not SAR evidence here |

**Honest rule:** Cross-family statements that treat morpholine, adamantyl, naphthyl, or *p*Cl-benzyl as interchangeable Janus “features” are **correlations at best**, not SAR.

---

## 5. Existing CB1/CB2 functional data (audit only — no new claims)

From `qiu_0q2c_dataset_audit.md` (primary facts locked).

| Ligand | CB1 | CB2 | Comparability | Janus A note |
|--------|-----|-----|---------------|--------------|
| **URB447** | Binding IC50 **313±72 nM** (rat cerebellum, [³H]WIN). GTPγS: blocks WIN EC50 **4.9±0.8 µM**; **no** basal GTPγS ↓ → **neutral antagonist** | Binding IC50 **41±23 nM** (hCB2 CHO). mCB2 HEK: ↓ isoproterenol-cAMP @ **1 µM** → **agonist**. EC50/Emax: **NF** | **HIGH** (same paper) | Full A |
| **Qiu-14** | SI Fig **S5B**: cAMP **antagonist** (ctrl rimonabant). IC50/Emax: **NF OA** | SI Fig **S5A**: cAMP **agonist** (ctrl CP55,940). EC50/Emax: **NF OA** | **HIGH** for direction | A on **direction**; potencies open gap |
| **V-27** | Ki mCB1 **15.4±2.2 nM**. AC @10 µM **18%**. Antagonizes agonist **3** (Fig 3B); blocks 3-hypothermia → **neutral antagonist** | Ki hCB2 **10.9±3.1 nM**. Table 1 AC **33%**; Fig 4 CRC narrative **~40–50%** → **agonist** | **HIGH** | Full A |
| **V-30** | Ki mCB1 **37.3±11.8 nM** (audit corrects dataset 37.2). AC **16%**. Ant of agonist **3**; hypothermia block → **neutral antagonist** | Ki hCB2 **26.5±1.5 nM**. Table 1 AC **21%**; Fig 4 narrative ago-class → **agonist** | **HIGH** | Full A |

**Contrast ligands used only as audited neighbors (not Janus A):**

| Ligand | Audit role | CB1 / CB2 (audit) |
|--------|------------|-------------------|
| **V-19** | OFF contrast (dual ago) | CB1 ago (AC IC50 ~45 nM); CB2 ago |
| **V-35** | PARTIAL / B | AC screen CB1 **39%**, CB2 **37%**; Ki + ant-of-agonist **NF** |
| **URB 5b / 8a / 3c** | D (binding / incomplete) | 5b inactive bind both; 8a CB2 weak bind; 3c dual **binding** only — function NF |
| **Qiu-15 / 20 / 24** | D (OA pharmacology NF) | Identity YES; phenotype/potency **NF OA** — author Yin-Yang loss = **not** upgraded |

---

## 6. Features that appear associated with Janus phenotype

Split into **correlation** (seen among A ligands or loosely shared) vs **SAR-pair-backed** (within-family neighbor evidence).

### 6.1 Correlation-only (cross-scaffold or single-compound)

| Feature | Where seen | Why correlation only |
|---------|------------|----------------------|
| Dual CB2-ago + CB1-ant phenotype | all 4 A | Definition of the set — not an explanatory chemical feature |
| Distal bulky hydrophobic mass | naphthyl (V), Ad (Qiu), Ph/benzoyl (URB) | Different chemistry/positions; no matched cross-scaffold pair |
| N1 lipophilic substituent | all 4 | Chemically non-identical; no shared fragment |
| Neutral (non-inverse) CB1 antagonism | URB447, V-27/30 | Qiu typed only as “antagonist” (S5B); not shown as neutral; no cross-family pair |
| Nanomolar–sub-µM binding with functional Janus | URB, V-27/30 | Qiu potencies NF OA; circular with phenotype |

### 6.2 SAR-pair-backed (within family)

| Feature / change | Pair | Evidence class (audit) |
|------------------|------|------------------------|
| C3 pharmacophore rewrite (ketone–CH₂–aryl → naphthylmethyl / 2-naphthyl) accompanies CB1 ago → neutral ant while CB2 ago retained | **V-19 ↔ V-27 / V-30** | **YES usable** (multi-mod) |
| CH₂ insertion at C3–naphthyl (1-naphthyl → 1-naphthylmethyl) | **V-35 ↔ V-27** | **PARTIAL** (35 lacks ant/Ki) |
| 1-naphthyl vs 2-naphthyl (direct) | **V-35 ↔ V-30** | **PARTIAL** (same) |
| N1-*p*-chlorobenzyl enables dual **binding** vs N1-H | **5b ↔ URB447** | **PARTIAL** (5b function NF) |
| 4-NH₂ / amide vs benzoyl neighbors | **8a / 3c ↔ URB447** | **PARTIAL weak** (func incomplete; 3c dual bind ≠ Janus) |
| *o*-morpholine / Me-piperazine / CH₂-Ad vs Qiu-14 | **14 ↔ 15/20/24** | **PARTIAL blocked** (OA phenotype NF) |

---

## 7. Correlation vs SAR-pair for each candidate pattern

### Pattern P1 — Vasiljevik C3 rewrite flips CB1 ago→neutral ant (CB2 ago retained)

- **Claim:** Replacing the C3 ketone–CH₂–(2,3-F₂Ph) of **19** with naphthylmethyl (**27**) or 2-naphthyl (**30**) converts dual-agonist OFF → Janus ON in the same lab.  
- **Backing:** Full Ki + AC + ant-of-agonist for 27/30; dual-ago for 19 (`qiu_0q2c_dataset_audit.md` Real SAR pairs; expand v2 JN-V1).  
- **Caveat:** Edit is **multi-site**, not single-atom.  
- **Grade: MODERATE** (strongest usable Janus ON/OFF contrast in the A-adjacent set; not STRONG because not minimal/single-edit)

### Pattern P2 — Methylene insertion (V-35 → V-27) is a Janus ON switch

- **Claim:** Adding CH₂ between indole C3 and 1-naphthyl converts screen-ago-class **35** into confirmed Janus **27**.  
- **Backing:** Minimal identifiable edit; 27 closed Janus; 35 AC screen only (CB1 39% → 27 18%) — **ant panel and Ki on 35 NF**.  
- **Grade: WEAK** (best *candidate* small edit; cannot close ON/OFF)

### Pattern P3 — 1- vs 2-naphthyl regio (V-35 → V-30) is a Janus ON switch

- **Claim:** Switching direct 1-naphthyl (**35**) to direct 2-naphthyl (**30**) yields Janus.  
- **Backing:** Same asymmetry as P2 — Janus closed only on **30**.  
- **Grade: WEAK**

### Pattern P4 — Both naphthyl attachment modes (1-naphthylmethyl **and** 2-naphthyl) tolerate Janus within Vasiljevik

- **Claim:** Among confirmed Janus A, two distinct C3–naphthyl presentations both work (**27** and **30**).  
- **Backing:** Both A-grade dual-func same paper; they are **not** a single-edit pair to each other.  
- **Grade: MODERATE** (within-family phenotype tolerance; not an ON/OFF rule)

### Pattern P5 — URB N1-*p*-chlorobenzyl is required for Janus

- **Claim:** Adding N1-*p*Cl-benzyl to **5b** produces Janus URB447.  
- **Backing:** Binding ON emergence clear (5b >1000 / >1000 → 447 313 / 41 nM); **5b dual function NF**.  
- **Grade: WEAK** (binding-supported emergence; Janus function asymmetric)

### Pattern P6 — URB 4-NH₂ distinguishes Janus from 8a

- **Claim:** 4-NH₂ on 3-benzoyl is the Janus feature vs **8a**.  
- **Backing:** Binding shifts documented; **8a function NF**.  
- **Grade: WEAK**

### Pattern P7 — URB adamantyl-amide **3c** is a Janus neighbor

- **Claim:** Dual binder **3c** informs Janus SAR.  
- **Backing:** Dual affinity only; function **NF** — audit grade **D** for Janus.  
- **Grade: UNSUPPORTED** (for Janus phenotype)

### Pattern P8 — Qiu *ortho*-morpholine is necessary/sufficient for Yin-Yang

- **Claim:** *o*-morpholine (14) vs *m*/*p* (15/16), Me-piperazine (20), or CH₂-Ad (24) controls Janus.  
- **Backing:** Structures YES; **14** direction A; comparators phenotype/potency **NF OA**. Author narrative + docking S6 = not experimental SAR here.  
- **Grade: UNSUPPORTED** (as OA-audited SAR; structures alone ≠ phenotype SAR)

### Pattern P9 — Shared “bulky distal hydrophobe” across scaffolds explains Janus

- **Claim:** Naphthyl / adamantyl / benzoyl-phenyl are interchangeable Janus determinants.  
- **Backing:** Co-occurrence among A ligands only; **no** cross-scaffold matched pair.  
- **Grade: UNSUPPORTED**

### Pattern P10 — Shared N1 lipophile across scaffolds explains Janus

- **Claim:** N1 benzyl / N-aryl / N-butyl are a common Janus feature.  
- **Backing:** Chemically non-identical; no matched cross-family pair.  
- **Grade: UNSUPPORTED**

### Pattern P11 — Neutral CB1 antagonism (vs inverse) is a Janus signature of the A set

- **Claim:** Janus A ligands are characteristically **neutral** CB1 antagonists.  
- **Backing:** Explicit for URB447 and V-27/30; Qiu S5B = antagonist vs rimonabant control — **neutral vs inverse not OA-resolved**.  
- **Grade: WEAK** (true for 3/4 with caveats; not a structural SAR feature)

### Pattern P12 — C3 carbonyl is required for Janus

- **Claim:** Carbonyl next to core is needed.  
- **Backing:** Present on URB/Qiu; **absent** on Janus A V-27/30 — falsified as a universal rule by the A set itself.  
- **Grade: UNSUPPORTED**

### Pattern P13 — Phenyl at C5 of a five-membered azole is a Janus feature

- **Claim:** C5-Ph shared by URB447 and Qiu-14 drives Janus.  
- **Backing:** Present on two scaffolds; absent on V A ligands; no OFF neighbor that isolates C5-Ph with dual func.  
- **Grade: UNSUPPORTED** (cross-scaffold coincidence)

---

## 8. Final pattern classification table

| ID | Pattern | Evidence type | Grade |
|----|---------|---------------|-------|
| **P1** | V-19 → V-27/30 C3 rewrite: dual-ago → Janus | SAR-pair (usable, multi-mod) | **MODERATE** |
| **P2** | V-35 → V-27 methylene insertion = Janus ON | SAR-pair (partial) | **WEAK** |
| **P3** | V-35 → V-30 1→2 naphthyl = Janus ON | SAR-pair (partial) | **WEAK** |
| **P4** | V-27 and V-30 both Janus (two naphthyl modes) | Within-family A consistency | **MODERATE** |
| **P5** | URB 5b → 447 via N1-*p*Cl-benzyl | SAR-pair (partial; bind only on OFF) | **WEAK** |
| **P6** | URB 8a → 447 via 4-NH₂ | SAR-pair (partial weak) | **WEAK** |
| **P7** | URB 3c as Janus SAR neighbor | Binding only | **UNSUPPORTED** |
| **P8** | Qiu *o*-morpholine / regio / CH₂-Ad switch | Structure yes; OA phenotype NF | **UNSUPPORTED** |
| **P9** | Cross-scaffold bulky hydrophobe | Correlation only | **UNSUPPORTED** |
| **P10** | Cross-scaffold N1 lipophile | Correlation only | **UNSUPPORTED** |
| **P11** | Neutral CB1 ant as A-set signature | Functional observation (3/4) | **WEAK** |
| **P12** | C3 carbonyl required for Janus | Falsified by V-27/30 | **UNSUPPORTED** |
| **P13** | C5-Ph azole as cross-scaffold Janus feature | Correlation only | **UNSUPPORTED** |

**Counts:** STRONG **0** · MODERATE **2** · WEAK **5** · UNSUPPORTED **6**

**No STRONG pattern:** Consistent with expand v2 / audit — no Class-A single-edit Janus ON/OFF pair with both arms fully typed.

---

## 9. Bottom line

1. The four Janus **A** ligands span **three scaffolds** (pyrrole, pyrazole-3-carboxamide, 7-methoxyindole) with **almost no identical shared fragments**.  
2. The only **SAR-pair-backed** Janus narrative sits in the **Vasiljevik** family (**P1 MODERATE**; **P2/P3 WEAK**).  
3. URB neighbors support **binding emergence** at N1 (**P5 WEAK**), not closed functional ON/OFF.  
4. Qiu regio/C3 neighbors are **structurally defined** but **OA-pharmacology-blocked** (**P8 UNSUPPORTED** as SAR).  
5. Cross-scaffold “common features” (**P9–P10, P12–P13**) are **UNSUPPORTED** as causal SAR.

---

## Paths / sources

| File | Role |
|------|------|
| `results/reports/qiu_0q2d_janus_a_sar_analysis.md` | This report |
| `results/reports/qiu_0q2c_dataset_audit.md` | Janus A authority + assay facts |
| `results/reports/qiu_0q2c_janus_ligand_dataset.md` | Dataset + SAR-eligible pairs |
| `results/reports/qiu_0q2_smrf_expand_v2.md` | Vasiljevik map / JN-V1–V3 |
| `results/reports/qiu_0d_structure_verification.md` | Qiu-14 SMILES/IUPAC |

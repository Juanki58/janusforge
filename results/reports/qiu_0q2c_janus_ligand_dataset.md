# 0Q.2c — Audited CB1/CB2 Janus ligand dataset (primary experimental)

**Date:** 2026-08-15  
**Branch:** `cursor/qiu-protocol-ip-cro-0p`  
**Scope:** Inventory of ligands with **primary experimental** CB1 and/or CB2 evidence, prioritized for Janus phenotype (CB2 agonist + CB1 antagonist/inverse), dual-receptor functional comparability, and near-neighbor SAR.  
**CSV:** [`qiu_0q2c_janus_ligand_dataset.csv`](qiu_0q2c_janus_ligand_dataset.csv)

**Absolute bans respected:** no docking, MD, or NCE design in this deliverable. Potencies are copied only when labeled in primary sources. Missing values = **NOT FOUND**. Evidence tags: **EXPERIMENTAL** (measured) vs **COMPUTATIONAL** (docking/MD; noted only as limitation) vs **INFERRED** (not used as fact).

**Secondary context only (verified against primary):** `qiu_0q2_smrf_expand.md` / v2, `qiu_0q_smrf_matrix`, `qiu_0q1_final`, independent audit, `qiu_0p_external_evidence_table`.

---

## Definitions

| Term | Meaning here |
|------|----------------|
| **Janus ON** | Experimental **CB2 agonist** **and** experimental **CB1 antagonist or inverse agonist** (functional; binding dual affinity alone is insufficient) |
| **Janus OFF** | Documented dual/mono profile that is **not** CB2-ago + CB1-ant/inv (includes dual-ago, mono-CB2, opposite dual) |
| **PARTIAL** | One arm typed; other arm incomplete, screen-only, or pathway-ambiguous |
| **UNKNOWN** | Identity/synthesis known; dual functional phenotype **NOT FOUND** in OA primary text |
| **ANCHOR** | Classic assay reference ligand (role label), not a Janus candidate |
| **Comparability** | **HIGH** = same lab / same assay family for both receptors (or matched pair); **MEDIUM** = multi-lab but same modality family; **LOW** = mixed assays / historical recombination |

---

## Executive counts

| Metric | n |
|--------|---|
| Compounds in dataset | **28** |
| Janus **ON** | **6** (URB447, GW405833, AM1710, Qiu-14, Vasiljevik-27, Vasiljevik-30) |
| Janus **PARTIAL** | **2** (Vasiljevik-35, AM1714) |
| Janus **UNKNOWN** | **4** (Qiu-15/16/20/24) |
| Janus **OFF** / opposite / mono | **11** |
| Assay **ANCHOR** tools | **5** (CP55,940, WIN55,212-2, SR144528, AM630, SR141716A/rimonabant) |
| SAR-eligible pairs/families (usable + partial) | **6** (see § SAR) |

---

## Master compound table

Parameters are quoted as published (IC50 ≠ Ki ≠ EC50). “NOT IN OA SOURCE” / “NOT FOUND” = not recoverable from open primary text used here.

### A. Janus ON anchors

| ID | Name | Structure | Scaffold | CB1 | CB2 | Janus | Primary ref | Comparability | evidence_tag | Notes |
|----|------|-----------|----------|-----|-----|-------|-------------|---------------|--------------|-------|
| JAN-1 | **URB447** (8b) | IUPAC: [4-amino-1-(4-chlorobenzyl)-2-methyl-5-phenyl-1H-pyrrol-3-yl](phenyl)methanone (primary abstract). SMILES: **NOT IN OA SOURCE** as SMILES string | pyrrole | Binding IC50 **313±72 nM** (rat cerebellum, [³H]WIN); GTPγS: blocks WIN EC50 **4.9±0.8 µM**; **no** basal GTPγS ↓ → **neutral antagonist** | Binding IC50 **41±23 nM** (hCB2 CHO); mCB2 HEK: ↓ isoproterenol-cAMP @ **1 µM** → **agonist** | **ON** | LoVerme/Piomelli *BMCL* 2009 [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059); PMC3690177 | **HIGH** (same paper dual func) | EXPERIMENTAL | First declared mixed CB1-ant/CB2-ago |
| JAN-2 | **GW405833** | IUPAC: 1-(2,3-dichlorobenzoyl)-5-methoxy-2-methyl-3-[2-(4-morpholinyl)ethyl]-1H-indole (JPET). SMILES: **NOT IN OA SOURCE** | aminoalkylindole | Ki **4772±1676 nM** (Valenzano 2005); JPET 2017: **noncompetitive antagonist** multi-pathway (AC/ERK/PIP2/internalization); DSE IC50 **2.6 µM**; arrestin ambiguous | Ki **3.92±1.58 nM** hCB2; historical **CB2 agonist** (partial/protean caveats: Yao 2008; Mancini 2009) | **ON** (reanalysis) | Dhopeshwarkar *JPET* 2017 [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539); binding Valenzano *Neuropharmacol* 2005 [10.1016/j.neuropharm.2004.12.008](https://doi.org/10.1016/j.neuropharm.2004.12.008) | **MEDIUM** (CB1 Mackie; CB2 multi-lab) | EXPERIMENTAL | Protean CB2 literature complicates “ago” arm |
| JAN-3 | **AM1710** | IUPAC: 1-hydroxy-9-methoxy-3-(2-methyloctan-2-yl)benzo[c]chromen-6-one (JPET). SMILES: **NOT IN OA SOURCE** | cannabilactone | Ki rat CB1 **360 nM** (95% CI 330–390); JPET: low-potency **competitive ant/inv**; arrestin low-eff. ago (pathway-dependent) | Ki hCB2 **6.7 nM**; cAMP EC50 **11 nM**, Emax **48%** → **partial agonist** | **ON** (complex) | Khanolkar *JMC* 2007 [10.1021/jm070441u](https://doi.org/10.1021/jm070441u); Dhopeshwarkar *JPET* 2017 | **MEDIUM** | EXPERIMENTAL | Janus signaling not pathway-uniform |
| JAN-4 | **Qiu-14** | N1-phenyl **ortho-morpholinyl**; C3-amide **1-adamantyl** (SI Scheme S1 / OCR). SMILES: **NOT IN OA SOURCE** | pyrazole-3-carboxamide | cAMP/HTRF **antagonist** (SI Fig. S5B; ctrl rimonabant). IC50/Emax: **NOT FOUND OA** | cAMP/HTRF **agonist** (SI Fig. S5A; ctrl CP55,940). EC50/Emax: **NOT FOUND OA** | **ON** (direction) | Qiu *Bioorg. Chem.* 2023 [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377); SI mmc1 | **HIGH** for direction (same SI assays); potencies paywalled | EXPERIMENTAL (phenotype); potencies NF | S173/S285 claims = **COMPUTATIONAL** (docking/MD) — not experimental for 14 |
| JAN-5 | **Vasiljevik-27** | IUPAC: 1-butyl-7-methoxy-3-(naphthalen-1-ylmethyl)-1H-indole | aminoalkylindole | Ki mCB1 **15.4 nM**; AC screen **18%** @ 10 µM; **blocks agonist 3** → **neutral antagonist** | Ki hCB2 **10.9 nM**; AC ago ~40–50% class | **ON** | Vasiljevik *JMC* 2013 [10.1021/jm400268b](https://doi.org/10.1021/jm400268b); PMC3904296 | **HIGH** | EXPERIMENTAL | Same-lab dual package |
| JAN-6 | **Vasiljevik-30** | IUPAC: 1-butyl-7-methoxy-3-(naphthalen-2-yl)-1H-indole | aminoalkylindole | Ki mCB1 **37.2 nM**; AC **16%**; **blocks agonist 3** → **neutral antagonist** | Ki hCB2 **26.5 nM**; AC ago-class | **ON** | same | **HIGH** | EXPERIMENTAL | Same-lab dual package |

### B. Near-neighbors / series (Janus OFF, PARTIAL, UNKNOWN)

| ID | Name | Structure | Scaffold | CB1 | CB2 | Janus | Primary ref | Comparability | evidence_tag | Notes |
|----|------|-----------|----------|-----|-----|-------|-------------|---------------|--------------|-------|
| N-URB-5b | **5b** (URB precursor) | (4-amino-2-methyl-5-phenylpyrrol-3-yl)(phenyl)methanone — N1-H (no pCl-benzyl) | pyrrole | Binding IC50 **>1000 nM** | Binding IC50 **>1000 nM** | **OFF** (inactive binding) | LoVerme 2009 Table 1 | **HIGH** vs URB447 binding | EXPERIMENTAL | Dual **func** for 5b: **NOT FOUND** |
| N-URB-8a | **8a** | 3-benzoyl without 4-NH₂ | pyrrole | Binding IC50 **>1000 nM** | Binding IC50 **498±32 nM** | **OFF** / incomplete | same | **HIGH** binding | EXPERIMENTAL | Func vs URB447: incomplete |
| N-URB-3c | **3c** | NH-2-adamantyl amide series | pyrrole | Binding IC50 **70±10 nM** | Binding IC50 **11±4 nM** | **OFF** (binding dual ≠ Janus) | same | **HIGH** binding | EXPERIMENTAL | Func CB1/CB2: **NOT FOUND** |
| N-Q15 | **Qiu-15** | N1-phenyl **meta-morpholinyl**; C3 1-adamantyl | pyrazole | Phenotype/potency: **NOT FOUND OA** | Phenotype/potency: **NOT FOUND OA** | **UNKNOWN** | Qiu 2023 SI identity; main tables paywalled | **HIGH** identity; pharmacology OA incomplete | EXPERIMENTAL identity; pharmacology NF OA | Author claims lose Yin-Yang — **not OA-verifiable** |
| N-Q16 | **Qiu-16** | N1-phenyl **para-morpholinyl**; C3 1-adamantyl (SI / expand v2) | pyrazole | **NOT FOUND OA** | **NOT FOUND OA** | **UNKNOWN** | same | same | same | same |
| N-Q20 | **Qiu-20** | N1 **ortho-4-methylpiperazinyl**; adamantyl series | pyrazole | **NOT FOUND OA** | **NOT FOUND OA** | **UNKNOWN** | same | same | same | same |
| N-Q24 | **Qiu-24** | N1 o-morpholinyl; C3 **CH₂-1-adamantyl** | pyrazole | **NOT FOUND OA** | **NOT FOUND OA** | **UNKNOWN** | same | same | same | same |
| N-V19 | **Vasiljevik-19** | IUPAC: 1-(1-butyl-7-methoxy-1H-indol-3-yl)-2-(2,3-difluorophenyl)ethanone | AAI | Ki **1.7 nM**; AC **51%** @ 10 µM; AC IC50 **~45 nM** → **agonist** | Ki **0.81 nM**; AC **52%** → **agonist** | **OFF** (dual ago) | Vasiljevik 2013 | **HIGH** | EXPERIMENTAL | Best same-lab contrast to 27/30 |
| N-V35 | **Vasiljevik-35** | IUPAC: 1-butyl-7-methoxy-3-(naphthalen-1-yl)-1H-indole | AAI | AC screen **39%** @ 10 µM (ago-class); Ki: **NOT FOUND**; ant-of-agonist: **NOT FOUND** | AC **37%** | **PARTIAL** | same | **HIGH** screen; ant incomplete | EXPERIMENTAL (screen) | Closest minimal-edit neighbor to 27 |
| N-V17 | **Vasiljevik-17** | 1-(1-butyl-7-methoxy-1H-indol-3-yl)-2-(4-fluorophenyl)ethanone | AAI | Ki **387 nM**; AC **−4%** | Ki **281 nM**; AC **22%** | **OFF** (weak) | same | **HIGH** | EXPERIMENTAL | Not potency-matched to Janus pair |
| N-AM1714 | **AM1714** | 9-OH cannabilactone (vs AM1710 9-OMe) | cannabilactone | CB1 ant panel matching JPET: **NOT FOUND** | CB2 ago-class (binding selectivity vs AM1710 in Khanolkar) | **PARTIAL** / insufficient | Khanolkar 2007 | **LOW** for Janus | EXPERIMENTAL binding | Insufficient for Janus SAR |
| X-MRI2687 | **MRI2687** | IUPAC: 2-(6-methyl-2-((2,2,3,3-tetramethylcyclopropane-1-carbonyl)imino)benzo[d]thiazol-3(2H)-yl)ethyl acetate. SMILES: **NOT FOUND** in primary | benzothiazole | β-arrestin2: **partial agonist** EC50 **114±15 nM**, Emax **6.0±0.3** fold | β-arrestin2: **inverse agonist** EC50 **0.24±0.06 nM**, Emax **0.75±0.04** | **OFF** (mono-CB2 inv; CB1 ago) | Li/Hua *Cell* 2019 [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011) | **HIGH** | EXPERIMENTAL | **NOT Yin-Yang** |
| X-MRI2594 | **MRI2594** | IUPAC: 2-(4,5-dimethyl-2-((2,2,3,3-tetramethylcyclopropane-1-carbonyl)imino)thiazol-3(2H)-yl)ethyl acetate | thiazole | β-arrestin2: **agonist** EC50 **310±54 nM**, Emax **28±2** | β-arrestin2: **agonist** EC50 **0.17±0.03 nM**, Emax **2.0±0.2** | **OFF** (dual ago-class) | same | **HIGH** | EXPERIMENTAL | Pair with 2687 = CB2 ago↔inv only |
| X-HU308 | **HU-308** | Classical CB2-selective agonist (Hanus 1999 lineage; cryo-EM 8GUS). SMILES: **NOT IN OA SOURCE** (this audit) | pinene/cannabilactone-related | Historically CB2-selective; dedicated Janus CB1-ant panel in Kosar 2024: **NOT FOUND** as CB1 ant switch | **Agonist** (active-state CB2–HU-308 cryo-EM DOI 10.1038/s41467-023-37112-9) | **OFF** | Kosar *ACS Cent. Sci.* 2024 [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461); Li *Nat Commun* 2023 | **MEDIUM** | EXPERIMENTAL | Parent for (R)-1 series |
| X-R1 | **(R)-1** | HU-308 scaffold + **C(2′) phenyl** (+ azide/amine mods vs HU-308) | same | CB1 ant switch: **NOT FOUND**; CB2-selective binding for related probes | cAMP: pEC50 **6.95**, Emax **−44%** → **inverse agonist**; Kd **39.1 nM** | **OFF** | Kosar 2024 | **HIGH** vs ago-3 | EXPERIMENTAL | Mono-CB2 flip |
| X-ago3 | **ago-3** | Same as (R)-3 scaffold **minus** C(2′) phenyl | same | Not the claim focus | cAMP: pEC50 **8.47**, Emax **+112%** → **agonist** | **OFF** | Kosar 2024 | **HIGH** | EXPERIMENTAL | Matched control for phenyl flip |
| X-AM10257 | **AM10257** | N-(adamantan-1-yl)-1-(5-hydroxypentyl)-4-methyl-5-phenyl-1H-pyrazole-3-carboxamide (PDB 5ZTY / 9JU) | pyrazole | **Agonist** (author: opposing dual) | Ki **0.08 nM**; AC Schild logKB **−8.30**; β-arrestin2 inv EC50 **0.20±0.04 nM**, Emax **0.70±0.05** → **inv/ant** | **OFF** (**opposite** dual) | Li *Cell* 2019 | **HIGH** | EXPERIMENTAL | Opposite of Janus definition |

### C. Assay anchors (role = panel calibration)

| ID | Name | Structure | Scaffold | CB1 | CB2 | Janus | Primary ref | Comparability | evidence_tag | Role |
|----|------|-----------|----------|-----|-----|-------|-------------|---------------|--------------|------|
| A-CP | **CP55,940** | IUPAC in Ross 1999 methods. SMILES: **NOT REQUIRED** (tool) | nonclassical cannabinoid | Binding Ki **5.0±0.8 nM** (hCB1 CHO, [³H]CP55,940); **agonist** | Binding Ki **1.8±0.2 nM** (hCB2); **agonist** | **ANCHOR** | Ross *Br J Pharmacol* 1999 Table 1 [10.1038/sj.bjp.0702351](https://doi.org/10.1038/sj.bjp.0702351); PMC1565857 | HIGH within paper | EXPERIMENTAL | Nonselective ago control |
| A-WIN | **WIN55,212-2** | IUPAC in Ross methods | aminoalkylindole | **Agonist**; used as radioligand / agonist in URB447 GTPγS | **Agonist**; cryo-EM CB2–WIN (6PT0) | **ANCHOR** | Ross 1999; Xing *Cell* 2020 [10.1016/j.cell.2020.01.007](https://doi.org/10.1016/j.cell.2020.01.007) | HIGH within papers | EXPERIMENTAL | Nonselective ago / radioligand |
| A-SR144 | **SR144528** | IUPAC in Ross methods / Rinaldi-Carmona | diarylpyrazole | Primary discovery: Ki **400 nM** (brain/hCB1). Ross panel: Ki **>10 µM** (hCB1 CHO) | Primary: Ki **0.6 nM** (spleen/hCB2); ant of CP55,940 AC EC50 **10 nM**. Ross: Ki **5.6±1.1 nM** (hCB2) | **ANCHOR** | Rinaldi-Carmona *JPET* 1998 PMID 9454810; Ross 1999 Table 1 | HIGH within each paper; **do not merge** Ki across labs | EXPERIMENTAL | CB2-selective ant/inv tool |
| A-AM630 | **AM630** | 6-iodopravadoline | aminoalkylindole-related | Ki **5152±567 nM**; weak **partial agonist** @ µM cAMP | Ki **31.2±12.4 nM**; GTPγS inv EC50 **76.6 nM**; enhances forskolin-cAMP | **ANCHOR** | Ross 1999 Table 1 PMC1565857 | **HIGH** | EXPERIMENTAL | CB2-selective inv/ant tool |
| A-RIM | **SR141716A (rimonabant)** | IUPAC in Ross methods | diarylpyrazole | Selective **inverse agonist/antagonist** (classic); URB447 paper cites Ki **1.98±0.36 nM** (Rinaldi-Carmona 1994) | IC50 **>1000 nM** (URB447 Table 1 footnote) | **ANCHOR** | Rinaldi-Carmona *FEBS Lett* 1994; cited in LoVerme 2009 | HIGH as CB1 ctrl | EXPERIMENTAL | CB1 ant/inv control (Qiu SI S5B) |

---

## Evidence hygiene (mandatory)

| Claim type | Examples in this dataset | Status |
|------------|--------------------------|--------|
| Measured binding / function | URB447 IC50/GTPγS/cAMP; Vasiljevik Ki/AC; MRI β-arrestin2; AM630 Ki | **EXPERIMENTAL** |
| Qiu-14 dual direction in SI S5 | CB1 ant + CB2 ago curves | **EXPERIMENTAL** (no OA numbers) |
| Qiu S173/S285 H-bonds; MRI/(R)-1 Trp6.48 docking/MD | Mechanism narratives | **COMPUTATIONAL** — not potency evidence |
| “Ortho-morpholine is the switch” for Qiu without OA comparator numbers | Author interpretation | **INFERRED** until paywalled tables audited |
| Invented / converted potencies | — | **Banned** — none included |

---

## SAR-eligible for Janus phenotype

Pairs/families where **structural neighbors** + **dual functional data** could support Janus SAR study. Classification: **usable** / **partial** / **not usable**.

| ID | Pair / family | Structural relationship | Dual-func status | Classification | Why |
|----|---------------|-------------------------|------------------|----------------|-----|
| SAR-V1 | **Vasiljevik-19 ↔ 27 / 30** | Multi-mod C3 rewrite (ketone–CH₂–aryl → naphthylmethyl / 2-naphthyl) | Both arms fully typed same lab (19 dual-ago; 27/30 Janus) | **usable** | Clearest published same-lab **Janus ON vs OFF** contrast with Ki + AC + ant-of-agonist. Edit is **not minimal** — usable for multi-site SAR narrative, not single-atom rules |
| SAR-V2 | **Vasiljevik-35 ↔ 27** | Insert **CH₂** (1-naphthyl → 1-naphthylmethyl) | 27 Janus closed; 35 screen only (no ant panel / no Ki) | **partial** | Best **minimal-edit candidate**; cannot close ON/OFF without ant confirmation on 35 |
| SAR-V3 | **Vasiljevik-35 ↔ 30** | 1-naphthyl ↔ 2-naphthyl (direct) | Same asymmetry as SAR-V2 | **partial** | Small regio change; same missing ant panel on 35 |
| SAR-URB1 | **5b ↔ URB447** | Add N1-p-chlorobenzyl | URB447 dual func closed; 5b binding-inactive only | **partial** | Strong **emergence** story for binding; 5b lacks dual functional assays |
| SAR-URB2 | **8a / 3c ↔ URB447** | 4-NH₂ / amide vs benzoyl-amino | Binding closed; func incomplete for 8a/3c | **partial** (weak) | 3c dual binder ≠ Janus without function |
| SAR-Q1 | **Qiu-14 ↔ 15 / 20 / 24** | N1 regio / piperazine / C3 CH₂-Ad | 14 direction only; comparators OA NF | **partial** | Author Yin-Yang switch claim; **blocked by paywall** for potencies/phenotypes |
| SAR-AM | **AM1714 ↔ AM1710** | 9-OH ↔ 9-OMe | AM1710 Janus complex; AM1714 CB1 ant NF | **not usable** (for Janus) | Binding selectivity neighbor only |
| SAR-MRI | **MRI2687 ↔ MRI2594** | Arm-1 thiazole ↔ benzothiazole | Dual β-arrestin2 closed | **not usable** (for Janus) | Excellent **mono-CB2** ago↔inv SAR; CB1 stays ago-class — **wrong phenotype** |
| SAR-HU | **ago-3 ↔ (R)-1 / (R)-3** | ± C(2′) phenyl | Multi-assay CB2 ago↔inv | **not usable** (for Janus) | Class-A mono-CB2 flip; no CB1-ant arm |
| SAR-OPP | **AM10257 alone / vs Janus pyrazoles** | Pyrazole with Ad amide | Opposite dual typed | **not usable** (for Janus) | Teaches **opposite** dual (CB2 inv + CB1 ago) |

**Summary:** **1 usable** family (Vasiljevik 19↔27/30), **5 partial** (V35↔27, V35↔30, URB 5b→447, URB 8a/3c, Qiu series), **4 not usable for Janus** (AM1714, MRI, HU/ago-3, AM10257). Counting distinct pair/family rows scored usable+partial = **6**.

---

## Gaps that remain (do not invent)

1. Qiu **14/15/20/24** numeric IC50/EC50/Emax — main PDF paywalled.  
2. Vasiljevik-**35** antagonist-of-agonist + Ki.  
3. Independent replication of any Janus dual outside original labs.  
4. SMILES strings generally **not printed** in primary OA text for these series — IUPAC/structure schemes used instead.  
5. Gerasi/Makriyannis thesis duals — **embargoed** (not in this dataset).

---

## Paths

| File | Path |
|------|------|
| This report | `results/reports/qiu_0q2c_janus_ligand_dataset.md` |
| CSV (one row/compound) | `results/reports/qiu_0q2c_janus_ligand_dataset.csv` |

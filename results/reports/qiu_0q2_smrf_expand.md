# 0Q.2 ÔÇö SMRF EXPAND (official launch)

**Fecha:** 2026-08-15  
**Workstream:** Option B ÔÇö historical Janus / near-neighbor functional expand  
**Prior locks (unchanged by this step):** `0Q-SMRF = MODERATE`; `0Q.1-FINAL = EXPAND`; Class-A pairs MRI2687ÔåöMRI2594 and HU-308/(ago-3)Ôåö(R)-1 = **mono-CB2 only (NOT Janus)**; `0M = FROZEN`; Qiu-14 = validation vehicle only  
**Bans:** no docking/MD campaigns; no NCE; no activity prediction; no causal SAR rules from correlation alone; binding Ôëá function; inactivity Ôëá antagonism  
**Do NOT jump to 0Q.3** ÔÇö end with user-review recommendation only

**Success criterion (this step):**  
Is there a **reproducible literature relationship** between a **small structural change** and appearance/disappearance of **Janus phenotype** (CB2 agonist + CB1 antagonist/inverse), especially precedents that already demonstrated CB2-ago + CB1-ant/inv?

**Machine-readable pairs:** [`qiu_0q2_smrf_expand_pairs.csv`](qiu_0q2_smrf_expand_pairs.csv)

**Primary sources preferred this session:** LoVerme/Piomelli *BMCL* 2009 (URB447 OA PDF); Dhopeshwarkar *JPET* 2017; Vasiljevik *JMC* 2013 (PMC3904296 / KU ScholarWorks PDF); Qiu 2023 OA SI; Khanolkar *JMC* 2007; prior 0Q matrix/CSV as secondary inventory only.

---

## Executive verdict

### `0Q.2 = WEAK` (for the structural-switch claim)

| Claim | Support |
|-------|---------|
| Janus phenotype (CB2 **ago** + CB1 **ant/inv**) exists experimentally across scaffolds / labs | **Yes ÔÇö MODERATEÔÇôSTRONG for phenotype existence** |
| Matched **small structural change** ÔåÆ Janus on/off with dual-arm functional potencies closed in OA | **WEAK** ÔÇö best candidates incomplete (URB binding-led; Qiu comparator phenotypes OA NF; Vasiljevik multi-mod SAR) |
| Universal single-edit ÔÇ£Janus switchÔÇØ rule across chemotypes | **NOT SUPPORTED** |
| Class-A mono-CB2 pairs (MRI / HU) carry Janus | **NO** (locked in 0Q.1-FINAL) |

**Recommendation for user review:** **EXPAND FURTHER**  
(Not KEEP-as-is: structural Janus switch still open. Not KILL: Janus ligands are real and multi-scaffold.)

---

## SPECIAL SECTION ÔÇö JANUS table only

Compounds with **experimental** CB2 agonism **and** CB1 antagonism/inverse agonism (not binding-only; not opposite dual CB1-ago/CB2-inv).

| ID | Compound | Scaffold | CB2 | CB1 | Typed parameters | Same lab dual func? | Near analogs that lose / lack Janus | Quality | Primary DOI |
|----|----------|----------|-----|-----|------------------|---------------------|--------------------------------------|---------|-------------|
| JAN-1 | **URB447** | pyrrole | **Ago** (mCB2 HEK cAMP Ôåô at 1 ┬ÁM vs isoproterenol) | **Neutral ant** (rat GTP╬│S: blocks WIN; no basal GTP╬│S Ôåô) | Binding **IC50** rat CB1 **313┬▒72 nM**; hCB2 **41┬▒23 nM**; GTP╬│S ant **EC50 4.9┬▒0.8 ┬ÁM**; cAMP ago qualitative @ 1 ┬ÁM | Yes (LoVerme/Piomelli) | **5b** (des-N1-pClBn): binding inactive both; **8a** (des-4-NHÔéé): weak CB2 binding, limited CB1 ÔÇö dual **func** for 8a/5b **NOT FOUND** | **B** | [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059) |
| JAN-2 | **GW405833** (L-768242) | aminoalkylindole | **Ago** (historical Valenzano/others; protean caveats) | **Noncomp. ant** multi-pathway (AC, ERK, PIP2, internalization); arrestin **time-dependent / ambiguous** | Binding **Ki** hCB2 **3.92┬▒1.58 nM**; CB1 **4772┬▒1676 nM**; DSE block **IC50 2.6 ┬ÁM**; AC/ERK block @ ~0.3ÔÇô1 ┬ÁM | Dual CB1 func = Mackie lab 2017; CB2 ago = multi-lab legacy | No matched same-series JanusÔåönon-Janus functional pair audited here | **B** | [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539); Valenzano [10.1016/j.neuropharm.2004.12.008](https://doi.org/10.1016/j.neuropharm.2004.12.008) |
| JAN-3 | **AM1710** | cannabilactone | **Ago** (cAMP **EC50 11 nM**, **Emax 48%**) | **Low-pot. competitive ant/inv** (AC slight Ôåæ alone; right-shift CP); arrestin **low-eff. ago** ÔåÆ pathway-ambiguous | Binding **Ki** hCB2 **6.7 nM**; rat CB1 **360 nM** | CB1 Janus panel = Mackie 2017; CB2 = Makriyannis/Khanolkar + Mackie | **AM1714** (9-OH vs 9-OMe): higher CB2 selectivity (binding); **CB1 ant panel for AM1714 = NOT FOUND** in JPET ÔåÆ cannot claim Janus loss | **B** | [10.1021/jm070441u](https://doi.org/10.1021/jm070441u); [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539) |
| JAN-4 | **Qiu-14** | pyrazole-3-carboxamide (Ad) | **Ago** (cAMP/HTRF SI Fig. S5A) | **Ant** (cAMP/HTRF SI Fig. S5B) | Direction only; **EC50/IC50/Emax = NOT FOUND OA** | Yes (Qiu/Tao) | Authors claim **15/16/20/24** lose Yin-Yang via N1/C3 edits ÔÇö **comparator phenotypes/potencies OA NF** (curves exist S11ÔÇôS13) | **B** (anchor); pairs **C** | [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377) |
| JAN-5 | **Vasiljevik-27** | aminoalkylindole (JWH-073-M4 lineage) | **Ago** (AC inhibition ~40ÔÇô50% in CHO-hCB2) | **Neutral ant** (little AC inhibition alone; blocks agonist **3** AC) | Binding **Ki** mCB1 **15.4 nM**; hCB2 **10.9 nM** | Yes (Prisinzano/Prather) | Same series: **19** = high-affinity **CB1 ago** (AC IC50 ~45 nM) + CB2 ago ÔÇö **not Janus**; **17** = weak dual affinity + weak CB1 AC | **B** | [10.1021/jm400268b](https://doi.org/10.1021/jm400268b) |
| JAN-6 | **Vasiljevik-30** | same | **Ago** (AC ~40ÔÇô50%) | **Neutral ant** (same pattern as 27) | Binding **Ki** mCB1 **37.2 nM**; hCB2 **26.5 nM** | Yes | Same as JAN-5 | **B** | same |

**Janus ligand count (experimental dual phenotype):** **6**  
**Closed Class-A Janus structural switch pairs:** **0**  
**Usable JanusÔåönear-neighbor structural pairs (B/C):** **ÔëÑ4** (URB 5bÔåÆURB447; URB 8aÔåÆURB447; Vasiljevik 19 vs 27/30; Qiu-14 vs regio/C3 ÔÇö C)

**Explicit non-Janus (do not promote into this table):**
- MRI2687 / MRI2594 ÔÇö mono-CB2 invÔåöago; CB1 remains ago-class (0Q.1-FINAL)
- HU-308 / ago-3 / (R)-1 ÔÇö mono-CB2 agoÔåÆinv
- AM10257 ÔÇö **opposite** dual (CB2 inv + CB1 ago)

---

## Search order executed

1. **Direct Janus** ÔÇö URB447; GW405833; AM1710; Qiu-14; Vasiljevik 27/30  
2. **Janus / non-Janus within series** ÔÇö URB Table 1 neighbors; Qiu N1 regio / C3; Vasiljevik 19 vs 27/30; AM1710 vs AM1714 (incomplete)  
3. **CB1/CB2 pairs with small changes** ÔÇö URB N1-benzyl / 4-NHÔéé; Qiu o/m/p-morpholine  
4. **Efficacy switches mono-receptor** ÔÇö carry-forward A pairs only as **negative** for Janus claim  
5. **Other SAR** ÔÇö photoswitch Azo (Qiu/Tao 2026) noted as **partial / pending full-text numeric audit** ÔÇö not used to close 0Q.2

---

## Full pair matrix (preferred fields)

Conventions: `PARAM:` typed; `NF` = NOT FOUND; **HIP├ôTESIS** = not a design rule.

### Block 1 ÔÇö Direct Janus anchors (single-molecule or reanalysis)

| pair_id | A | B | scaffold | exact change | CB1 assay / result | CB2 assay / result | Ki/IC50/EC50/Emax | same lab | func evid | struct evid | mech | class | DOI |
|---------|---|---|----------|--------------|--------------------|--------------------|-------------------|----------|-----------|-------------|------|-------|-----|
| J0-URB | URB447 | ÔÇö | pyrrole | n/a (anchor) | GTP╬│S neutral ant EC50 **4.9┬▒0.8 ┬ÁM** | cAMP ago @ 1 ┬ÁM | Binding IC50 CB1 **313┬▒72**; CB2 **41┬▒23** | yes | yes | no | peripheral restriction (authors) | **B** | 10.1016/j.bmcl.2008.12.059 |
| J0-GW | GW405833 | ÔÇö | indole | n/a (Janus reanalysis) | multi-pathway noncomp. ant; DSE IC50 **2.6 ┬ÁM** | CB2 ago legacy | Ki CB2 **3.92**; CB1 **4772** nM | no (multi-lab) | yes | no | originally ÔÇ£CB2-selectiveÔÇØ | **B** | 10.1124/jpet.116.236539 |
| J0-AM | AM1710 | ÔÇö | cannabilactone | n/a | low-pot. CB1 ant/inv (AC/ERK); arrestin ambiguous | cAMP EC50 **11 nM** Emax **48%** | Ki CB2 **6.7**; CB1 **360** nM | no | yes | no | complex Janus | **B** | 10.1021/jm070441u + 10.1124/jpet.116.236539 |
| J0-Q14 | Qiu-14 | ÔÇö | pyrazole Ad | o-morph on N1-Ph | cAMP ant (S5B) | cAMP ago (S5A) | potencies **NF OA** | yes | yes (dir.) | no | S173/S285 = **COMPUTATIONAL** | **B** | 10.1016/j.bioorg.2023.106377 |
| J0-V27 | Vasiljevik-27 | ÔÇö | aminoalkylindole | n/a (anchor) | AC: neutral ant; blocks agonist 3 | AC: ago ~40ÔÇô50% | Ki CB1 **15.4**; CB2 **10.9** nM | yes | yes | no | dual designed for alcohol | **B** | 10.1021/jm400268b |
| J0-V30 | Vasiljevik-30 | ÔÇö | aminoalkylindole | n/a | same pattern | same pattern | Ki CB1 **37.2**; CB2 **26.5** nM | yes | yes | no | same | **B** | same |

### Block 2 ÔÇö Janus / non-Janus near neighbors (same series)

| pair_id | A (non/partial) | B (Janus) | exact change | region | CB1 | CB2 | typed params | same lab | notes | class |
|---------|-----------------|-----------|--------------|--------|-----|-----|--------------|----------|-------|-------|
| JN-URB1 | **5b** | URB447 | add N1-p-chlorobenzyl | **N1** | 5b inactive binding; URB447 dual + GTP╬│S ant | URB447 CB2 ago @ 1 ┬ÁM | IC50 binding + GTP╬│S EC50 + cAMP qual. | yes | Best URB **emergence** pair; 5b lacks dual **func** panels | **B** |
| JN-URB2 | **8a** | URB447 | add 4-NHÔéé on 3-benzoyl | **C4** | 8a weak/limited; URB447 IC50 313 nM | 8a weak CB2 binding; URB447 IC50 41 nM + ago | mostly **binding** for 8a | yes | Functional Janus incomplete for 8a ÔåÆ prefer JN-URB1 | **C** |
| JN-Q1 | Qiu-15 | Qiu-14 | m-morph ÔåÆ o-morph | **N1-regio** | 14 ant; 15 phenotype **NF OA** | 14 ago; 15 **NF OA** | all potencies **NF** | yes | Author switch claim; docking collisions = **COMP** | **C** |
| JN-Q2 | Qiu-16 | Qiu-14 | p-morph ÔåÆ o-morph | **N1-regio** | same pattern | same | **NF** | yes | same | **C** |
| JN-Q3 | Qiu-20 | Qiu-14 | o-4-Me-piperazinyl ÔåÆ o-morph | **N1** | same | same | **NF** | yes | same | **C** |
| JN-Q4 | Qiu-24 | Qiu-14 | C3 CHÔéé-Ad ÔåÆ Ad (keep o-morph) | **C3** | same | same | **NF** | yes | ÔÇ£steric clash 24ÔÇØ as experimental fact = **REJECT** | **C** |
| JN-V1 | **19** | **27 / 30** | multi-mod within aminoalkylindole SAR (not single-atom) | multi | **19:** CB1 **ago** (AC IC50 ~45 nM); **27/30:** CB1 neutral ant | both CB2 ago-class | Ki: 19 CB1 **1.7** / CB2 **0.81** nM vs 27/30 above | yes | Clearest **same-lab** Janus vs dual-ago contrast; change **not** minimal single-region | **B** |
| JN-AM14 | AM1714 | AM1710 | 9-OH Ôåö 9-OMe | C9 | AM1714 CB1 ant **NF** | both CB2 ago (binding/selectivity) | AM1714 ~490├ù CB2 sel. (binding) | partial | **Insufficient** for Janus on/off | **C/D** |

### Block 3 ÔÇö Explicit non-Janus (carry-forward; do not reclassify as Janus)

| pair_id | A | B | phenotype | class | note |
|---------|---|---|-----------|-------|------|
| T1 | MRI2687 | MRI2594 | CB2 inv Ôåö ago; CB1 ago-class both | **A mono-CB2** | NOT Yin-Yang |
| T2 | ago-3 | (R)-1 | CB2 ago ÔåÆ inv | **A mono-CB2** | NOT Yin-Yang |
| S1 | AM10257 | ÔÇö | CB2 inv + CB1 ago | **B opposite** | Opposite to Janus definition |

---

## HIP├ôTESIS only (not design rules)

1. **HIP├ôTESIS:** Polar N / N1-benzyl enabling dual affinity (URB series) can coincide with Janus emergence ÔÇö supported only as **series narrative + binding**, not as a transferable causal rule.  
2. **HIP├ôTESIS:** N1-phenyl ortho-morpholine is necessary/sufficient for Qiu Yin-Yang ÔÇö **author claim**; comparator OA phenotypes incomplete; mechanism residues S173/S285 = **COMPUTATIONAL**.  
3. **HIP├ôTESIS:** Aminoalkylindole SAR can flip CB1 efficacy (ago ÔåÆ neutral ant) while retaining CB2 agonism (Vasiljevik 19 vs 27/30) ÔÇö **experimental in one lab**, multi-mod, not a single-edit law.  
4. **HIP├ôTESIS:** Trp6.48 bulk toggles (MRI / HU) generalize to Janus dual ÔÇö **NOT SUPPORTED** by those pairsÔÇÖ CB1 phenotypes.

---

## Answers to success criterion

1. **Does Janus (CB2-ago + CB1-ant/inv) exist in literature with experimental functional evidence?**  
   **YES** ÔÇö ÔëÑ6 ligands across pyrrole, indole, cannabilactone, pyrazole, aminoalkylindole.

2. **Is there a reproducible *small structural change* Ôåö Janus on/off relationship?**  
   **WEAK.** Best signals: URB N1-benzyl emergence (binding-complete, func-asymmetric); Vasiljevik series efficacy split (func-complete, edit not minimal); Qiu N1 regio (author claim, OA incomplete). **No Class-A closed Janus switch pair.**

3. **Do 0Q.1 Class-A pairs answer this?**  
   **NO** ÔÇö they answer mono-CB2 efficacy switching only.

4. **What would raise 0Q.2 toward MODERATE/STRONG without docking/NCE?**  
   - Qiu main PDF: numeric CB1 IC50 / CB2 EC50/Emax for **14 vs 15/16/20/24** on same cAMP platform  
   - Full Vasiljevik Table 1 structural map: list exact edits distinguishing **19** vs **27/30**  
   - AM1714 (and close cannabilactones) CB1 antagonism panel matching JPET methods  
   - Independent replication of any one Janus ligandÔÇÖs dual arms

---

## Classification & recommendation

| Item | Result |
|------|--------|
| **0Q.2 overall** | **WEAK** (structural Janus switch); phenotype existence separately **supported** |
| **Janus ligand count** | **6** |
| **Class-A Janus structural pairs** | **0** |
| **Recommendation** | **EXPAND FURTHER** |
| **KEEP?** | No ÔÇö framing would overstate closed SAR |
| **KILL?** | No ÔÇö multi-scaffold experimental Janus is real |
| **0Q.3?** | **Do not start** until user reviews this expand |
| **Global `0Q-SMRF`** | Remains **MODERATE** (no change proposed) |
| **0M** | Remains **FROZEN** |

---

## Paths

| Deliverable | Path |
|-------------|------|
| This report | `results/reports/qiu_0q2_smrf_expand.md` |
| Optional CSV | `results/reports/qiu_0q2_smrf_expand_pairs.csv` |
| Parent matrix | `results/reports/qiu_0q_smrf_matrix.md` |
| 0Q.1-FINAL | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` |

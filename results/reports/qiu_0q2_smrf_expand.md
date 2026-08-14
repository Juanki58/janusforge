# 0Q.2 — SMRF EXPAND (official launch)

**Fecha:** 2026-08-15  
**Workstream:** Option B — historical Janus / near-neighbor functional expand  
**Prior locks (unchanged by this step):** `0Q-SMRF = MODERATE`; `0Q.1-FINAL = EXPAND`; Class-A pairs MRI2687↔MRI2594 and HU-308/(ago-3)↔(R)-1 = **mono-CB2 only (NOT Janus)**; `0M = FROZEN`; Qiu-14 = validation vehicle only  
**Bans:** no docking/MD campaigns; no NCE; no activity prediction; no causal SAR rules from correlation alone; binding ≠ function; inactivity ≠ antagonism  
**Do NOT jump to 0Q.3** — end with user-review recommendation only

**Success criterion (this step):**  
Is there a **reproducible literature relationship** between a **small structural change** and appearance/disappearance of **Janus phenotype** (CB2 agonist + CB1 antagonist/inverse), especially precedents that already demonstrated CB2-ago + CB1-ant/inv?

**Machine-readable pairs:** [`qiu_0q2_smrf_expand_pairs.csv`](qiu_0q2_smrf_expand_pairs.csv)

**Primary sources preferred this session:** LoVerme/Piomelli *BMCL* 2009 (URB447 OA PDF); Dhopeshwarkar *JPET* 2017; Vasiljevik *JMC* 2013 (PMC3904296 / KU ScholarWorks PDF); Qiu 2023 OA SI; Khanolkar *JMC* 2007; prior 0Q matrix/CSV as secondary inventory only.

---

## Executive verdict

### `0Q.2 = WEAK` (for the structural-switch claim)

| Claim | Support |
|-------|---------|
| Janus phenotype (CB2 **ago** + CB1 **ant/inv**) exists experimentally across scaffolds / labs | **Yes — MODERATE–STRONG for phenotype existence** |
| Matched **small structural change** → Janus on/off with dual-arm functional potencies closed in OA | **WEAK** — best candidates incomplete (URB binding-led; Qiu comparator phenotypes OA NF; Vasiljevik multi-mod SAR) |
| Universal single-edit “Janus switch” rule across chemotypes | **NOT SUPPORTED** |
| Class-A mono-CB2 pairs (MRI / HU) carry Janus | **NO** (locked in 0Q.1-FINAL) |

**Recommendation for user review:** **EXPAND FURTHER**  
(Not KEEP-as-is: structural Janus switch still open. Not KILL: Janus ligands are real and multi-scaffold.)

---

## SPECIAL SECTION — JANUS table only

Compounds with **experimental** CB2 agonism **and** CB1 antagonism/inverse agonism (not binding-only; not opposite dual CB1-ago/CB2-inv).

| ID | Compound | Scaffold | CB2 | CB1 | Typed parameters | Same lab dual func? | Near analogs that lose / lack Janus | Quality | Primary DOI |
|----|----------|----------|-----|-----|------------------|---------------------|--------------------------------------|---------|-------------|
| JAN-1 | **URB447** | pyrrole | **Ago** (mCB2 HEK cAMP ↓ at 1 µM vs isoproterenol) | **Neutral ant** (rat GTPγS: blocks WIN; no basal GTPγS ↓) | Binding **IC50** rat CB1 **313±72 nM**; hCB2 **41±23 nM**; GTPγS ant **EC50 4.9±0.8 µM**; cAMP ago qualitative @ 1 µM | Yes (LoVerme/Piomelli) | **5b** (des-N1-pClBn): binding inactive both; **8a** (des-4-NH₂): weak CB2 binding, limited CB1 — dual **func** for 8a/5b **NOT FOUND** | **B** | [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059) |
| JAN-2 | **GW405833** (L-768242) | aminoalkylindole | **Ago** (historical Valenzano/others; protean caveats) | **Noncomp. ant** multi-pathway (AC, ERK, PIP2, internalization); arrestin **time-dependent / ambiguous** | Binding **Ki** hCB2 **3.92±1.58 nM**; CB1 **4772±1676 nM**; DSE block **IC50 2.6 µM**; AC/ERK block @ ~0.3–1 µM | Dual CB1 func = Mackie lab 2017; CB2 ago = multi-lab legacy | No matched same-series Janus↔non-Janus functional pair audited here | **B** | [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539); Valenzano [10.1016/j.neuropharm.2004.12.008](https://doi.org/10.1016/j.neuropharm.2004.12.008) |
| JAN-3 | **AM1710** | cannabilactone | **Ago** (cAMP **EC50 11 nM**, **Emax 48%**) | **Low-pot. competitive ant/inv** (AC slight ↑ alone; right-shift CP); arrestin **low-eff. ago** → pathway-ambiguous | Binding **Ki** hCB2 **6.7 nM**; rat CB1 **360 nM** | CB1 Janus panel = Mackie 2017; CB2 = Makriyannis/Khanolkar + Mackie | **AM1714** (9-OH vs 9-OMe): higher CB2 selectivity (binding); **CB1 ant panel for AM1714 = NOT FOUND** in JPET → cannot claim Janus loss | **B** | [10.1021/jm070441u](https://doi.org/10.1021/jm070441u); [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539) |
| JAN-4 | **Qiu-14** | pyrazole-3-carboxamide (Ad) | **Ago** (cAMP/HTRF SI Fig. S5A) | **Ant** (cAMP/HTRF SI Fig. S5B) | Direction only; **EC50/IC50/Emax = NOT FOUND OA** | Yes (Qiu/Tao) | Authors claim **15/16/20/24** lose Yin-Yang via N1/C3 edits — **comparator phenotypes/potencies OA NF** (curves exist S11–S13) | **B** (anchor); pairs **C** | [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377) |
| JAN-5 | **Vasiljevik-27** | aminoalkylindole (JWH-073-M4 lineage) | **Ago** (AC inhibition ~40–50% in CHO-hCB2) | **Neutral ant** (little AC inhibition alone; blocks agonist **3** AC) | Binding **Ki** mCB1 **15.4 nM**; hCB2 **10.9 nM** | Yes (Prisinzano/Prather) | Same series: **19** = high-affinity **CB1 ago** (AC IC50 ~45 nM) + CB2 ago — **not Janus**; **17** = weak dual affinity + weak CB1 AC | **B** | [10.1021/jm400268b](https://doi.org/10.1021/jm400268b) |
| JAN-6 | **Vasiljevik-30** | same | **Ago** (AC ~40–50%) | **Neutral ant** (same pattern as 27) | Binding **Ki** mCB1 **37.2 nM**; hCB2 **26.5 nM** | Yes | Same as JAN-5 | **B** | same |

**Janus ligand count (experimental dual phenotype):** **6**  
**Closed Class-A Janus structural switch pairs:** **0**  
**Usable Janus↔near-neighbor structural pairs (B/C):** **≥4** (URB 5b→URB447; URB 8a→URB447; Vasiljevik 19 vs 27/30; Qiu-14 vs regio/C3 — C)

**Explicit non-Janus (do not promote into this table):**
- MRI2687 / MRI2594 — mono-CB2 inv↔ago; CB1 remains ago-class (0Q.1-FINAL)
- HU-308 / ago-3 / (R)-1 — mono-CB2 ago→inv
- AM10257 — **opposite** dual (CB2 inv + CB1 ago)

---

## Search order executed

1. **Direct Janus** — URB447; GW405833; AM1710; Qiu-14; Vasiljevik 27/30  
2. **Janus / non-Janus within series** — URB Table 1 neighbors; Qiu N1 regio / C3; Vasiljevik 19 vs 27/30; AM1710 vs AM1714 (incomplete)  
3. **CB1/CB2 pairs with small changes** — URB N1-benzyl / 4-NH₂; Qiu o/m/p-morpholine  
4. **Efficacy switches mono-receptor** — carry-forward A pairs only as **negative** for Janus claim  
5. **Other SAR** — photoswitch Azo (Qiu/Tao 2026) noted as **partial / pending full-text numeric audit** — not used to close 0Q.2

---

## Full pair matrix (preferred fields)

Conventions: `PARAM:` typed; `NF` = NOT FOUND; **HIPÓTESIS** = not a design rule.

### Block 1 — Direct Janus anchors (single-molecule or reanalysis)

| pair_id | A | B | scaffold | exact change | CB1 assay / result | CB2 assay / result | Ki/IC50/EC50/Emax | same lab | func evid | struct evid | mech | class | DOI |
|---------|---|---|----------|--------------|--------------------|--------------------|-------------------|----------|-----------|-------------|------|-------|-----|
| J0-URB | URB447 | — | pyrrole | n/a (anchor) | GTPγS neutral ant EC50 **4.9±0.8 µM** | cAMP ago @ 1 µM | Binding IC50 CB1 **313±72**; CB2 **41±23** | yes | yes | no | peripheral restriction (authors) | **B** | 10.1016/j.bmcl.2008.12.059 |
| J0-GW | GW405833 | — | indole | n/a (Janus reanalysis) | multi-pathway noncomp. ant; DSE IC50 **2.6 µM** | CB2 ago legacy | Ki CB2 **3.92**; CB1 **4772** nM | no (multi-lab) | yes | no | originally “CB2-selective” | **B** | 10.1124/jpet.116.236539 |
| J0-AM | AM1710 | — | cannabilactone | n/a | low-pot. CB1 ant/inv (AC/ERK); arrestin ambiguous | cAMP EC50 **11 nM** Emax **48%** | Ki CB2 **6.7**; CB1 **360** nM | no | yes | no | complex Janus | **B** | 10.1021/jm070441u + 10.1124/jpet.116.236539 |
| J0-Q14 | Qiu-14 | — | pyrazole Ad | o-morph on N1-Ph | cAMP ant (S5B) | cAMP ago (S5A) | potencies **NF OA** | yes | yes (dir.) | no | S173/S285 = **COMPUTATIONAL** | **B** | 10.1016/j.bioorg.2023.106377 |
| J0-V27 | Vasiljevik-27 | — | aminoalkylindole | n/a (anchor) | AC: neutral ant; blocks agonist 3 | AC: ago ~40–50% | Ki CB1 **15.4**; CB2 **10.9** nM | yes | yes | no | dual designed for alcohol | **B** | 10.1021/jm400268b |
| J0-V30 | Vasiljevik-30 | — | aminoalkylindole | n/a | same pattern | same pattern | Ki CB1 **37.2**; CB2 **26.5** nM | yes | yes | no | same | **B** | same |

### Block 2 — Janus / non-Janus near neighbors (same series)

| pair_id | A (non/partial) | B (Janus) | exact change | region | CB1 | CB2 | typed params | same lab | notes | class |
|---------|-----------------|-----------|--------------|--------|-----|-----|--------------|----------|-------|-------|
| JN-URB1 | **5b** | URB447 | add N1-p-chlorobenzyl | **N1** | 5b inactive binding; URB447 dual + GTPγS ant | URB447 CB2 ago @ 1 µM | IC50 binding + GTPγS EC50 + cAMP qual. | yes | Best URB **emergence** pair; 5b lacks dual **func** panels | **B** |
| JN-URB2 | **8a** | URB447 | add 4-NH₂ on 3-benzoyl | **C4** | 8a weak/limited; URB447 IC50 313 nM | 8a weak CB2 binding; URB447 IC50 41 nM + ago | mostly **binding** for 8a | yes | Functional Janus incomplete for 8a → prefer JN-URB1 | **C** |
| JN-Q1 | Qiu-15 | Qiu-14 | m-morph → o-morph | **N1-regio** | 14 ant; 15 phenotype **NF OA** | 14 ago; 15 **NF OA** | all potencies **NF** | yes | Author switch claim; docking collisions = **COMP** | **C** |
| JN-Q2 | Qiu-16 | Qiu-14 | p-morph → o-morph | **N1-regio** | same pattern | same | **NF** | yes | same | **C** |
| JN-Q3 | Qiu-20 | Qiu-14 | o-4-Me-piperazinyl → o-morph | **N1** | same | same | **NF** | yes | same | **C** |
| JN-Q4 | Qiu-24 | Qiu-14 | C3 CH₂-Ad → Ad (keep o-morph) | **C3** | same | same | **NF** | yes | “steric clash 24” as experimental fact = **REJECT** | **C** |
| JN-V1 | **19** | **27 / 30** | multi-mod within aminoalkylindole SAR (not single-atom) | multi | **19:** CB1 **ago** (AC IC50 ~45 nM); **27/30:** CB1 neutral ant | both CB2 ago-class | Ki: 19 CB1 **1.7** / CB2 **0.81** nM vs 27/30 above | yes | Clearest **same-lab** Janus vs dual-ago contrast; change **not** minimal single-region | **B** |
| JN-AM14 | AM1714 | AM1710 | 9-OH ↔ 9-OMe | C9 | AM1714 CB1 ant **NF** | both CB2 ago (binding/selectivity) | AM1714 ~490× CB2 sel. (binding) | partial | **Insufficient** for Janus on/off | **C/D** |

### Block 3 — Explicit non-Janus (carry-forward; do not reclassify as Janus)

| pair_id | A | B | phenotype | class | note |
|---------|---|---|-----------|-------|------|
| T1 | MRI2687 | MRI2594 | CB2 inv ↔ ago; CB1 ago-class both | **A mono-CB2** | NOT Yin-Yang |
| T2 | ago-3 | (R)-1 | CB2 ago → inv | **A mono-CB2** | NOT Yin-Yang |
| S1 | AM10257 | — | CB2 inv + CB1 ago | **B opposite** | Opposite to Janus definition |

---

## HIPÓTESIS only (not design rules)

1. **HIPÓTESIS:** Polar N / N1-benzyl enabling dual affinity (URB series) can coincide with Janus emergence — supported only as **series narrative + binding**, not as a transferable causal rule.  
2. **HIPÓTESIS:** N1-phenyl ortho-morpholine is necessary/sufficient for Qiu Yin-Yang — **author claim**; comparator OA phenotypes incomplete; mechanism residues S173/S285 = **COMPUTATIONAL**.  
3. **HIPÓTESIS:** Aminoalkylindole SAR can flip CB1 efficacy (ago → neutral ant) while retaining CB2 agonism (Vasiljevik 19 vs 27/30) — **experimental in one lab**, multi-mod, not a single-edit law.  
4. **HIPÓTESIS:** Trp6.48 bulk toggles (MRI / HU) generalize to Janus dual — **NOT SUPPORTED** by those pairs’ CB1 phenotypes.

---

## Answers to success criterion

1. **Does Janus (CB2-ago + CB1-ant/inv) exist in literature with experimental functional evidence?**  
   **YES** — ≥6 ligands across pyrrole, indole, cannabilactone, pyrazole, aminoalkylindole.

2. **Is there a reproducible *small structural change* ↔ Janus on/off relationship?**  
   **WEAK.** Best signals: URB N1-benzyl emergence (binding-complete, func-asymmetric); Vasiljevik series efficacy split (func-complete, edit not minimal); Qiu N1 regio (author claim, OA incomplete). **No Class-A closed Janus switch pair.**

3. **Do 0Q.1 Class-A pairs answer this?**  
   **NO** — they answer mono-CB2 efficacy switching only.

4. **What would raise 0Q.2 toward MODERATE/STRONG without docking/NCE?**  
   - Qiu main PDF: numeric CB1 IC50 / CB2 EC50/Emax for **14 vs 15/16/20/24** on same cAMP platform  
   - Full Vasiljevik Table 1 structural map: list exact edits distinguishing **19** vs **27/30**  
   - AM1714 (and close cannabilactones) CB1 antagonism panel matching JPET methods  
   - Independent replication of any one Janus ligand’s dual arms

---

## Classification & recommendation

| Item | Result |
|------|--------|
| **0Q.2 overall** | **WEAK** (structural Janus switch); phenotype existence separately **supported** |
| **Janus ligand count** | **6** |
| **Class-A Janus structural pairs** | **0** |
| **Recommendation** | **EXPAND FURTHER** |
| **KEEP?** | No — framing would overstate closed SAR |
| **KILL?** | No — multi-scaffold experimental Janus is real |
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

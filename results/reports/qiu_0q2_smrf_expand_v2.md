# 0Q.2 — SMRF EXPAND v2 (second pass)

**Fecha:** 2026-08-15  
**Workstream:** Option B — historical Janus / near-neighbor functional expand (second OA pass only)  
**Prior locks (unchanged):** `0Q-SMRF = MODERATE`; `0Q.1-FINAL = EXPAND`; Class-A MRI / HU pairs = **mono-CB2 only (NOT Janus)**; `0M = FROZEN`; Qiu-14 = validation vehicle only  
**Bans:** no docking/MD; no NCE; no synthesis; no 0Q.3; do not touch `cursor/pr1`–`pr5`  
**Parent v1:** [`qiu_0q2_smrf_expand.md`](qiu_0q2_smrf_expand.md)  
**Machine-readable pairs:** [`qiu_0q2_smrf_expand_v2_pairs.csv`](qiu_0q2_smrf_expand_v2_pairs.csv)

**Success criterion (unchanged):**  
Is there a **reproducible published relationship** between a **small defined structural change** and appearance/disappearance of **Janus phenotype** (CB2 agonist + CB1 antagonist/inverse)?

---

## Executive verdict

### `0Q.2-v2 = WEAK` (structural Janus ON/OFF switch)

| Claim | Support after v2 |
|-------|------------------|
| Janus phenotype exists experimentally (multi-scaffold, multi-lab) | **YES — MODERATE–STRONG** (unchanged; 6 anchors + Vasiljevik structural map closed) |
| Matched **small structural change** → Janus ON/OFF with dual-arm functional panels closed in published OA | **Still WEAK** — best new pairs are **suggestive Class B**, not Class A |
| Universal single-edit Janus switch rule | **NOT SUPPORTED** |
| Class-A mono-CB2 pairs carry Janus | **NO** (locked) |

### Critical question (explicit)

**Is there ANY published precedent allowing: “a small defined structural change converts Janus OFF→ON or ON→OFF”?**

**NO.**

No peer-reviewed, OA-auditable Class **A** pair was found in which:
1. A and B are structurally close with an **identifiable minimal edit**,
2. both have **functional** CB1 **and** CB2 readouts on a comparable platform,
3. and the Janus phenotype (CB2 ago + CB1 ant/inv) **appears or disappears** with that edit.

Best published signals remain **Class B** (Vasiljevik methylene / naphthyl regio screens; URB N1-benzyl binding emergence; Vasiljevik 19 vs 27/30 multi-mod with full ant confirmation) or **Class C** (Qiu N1-regio author claim without OA potencies).

---

## What changed vs v1

| Item | v1 | v2 |
|------|----|----|
| Vasiljevik **19 / 27 / 30** exact structures | multi-mod, graphics unresolved | **Closed from PMC experimental names** |
| Best small-edit Janus candidates | JN-URB1; JN-V1 | **+ JN-V2 (35↔27 methylene)** and **JN-V3 (35↔30 1-/2-naphthyl)** — Class **B** |
| Qiu 14 vs 15/16/20/24 potencies | NF OA | **Still NF OA** (SI S11–S13 curves exist; OCR/captions lack IC50/EC50/Emax; phenotypes of comparators not assignable from OCR alone) |
| GW405833 / AM1710 matched Janus neighbors | none | **Still none** with dual-func Janus on/off |
| New series (Gerasi / Makriyannis thesis AM8641→AM12435) | not audited | **Noted only** — full text **embargoed until 2027-07-22**; not usable as published Class A |
| Class-A Janus structural pairs | **0** | **0** |

---

## SPECIAL SECTION — JANUS anchors (phenotype existence)

Compounds with **experimental** CB2 agonism **and** CB1 antagonism/inverse (not binding-only; not opposite dual).

| ID | Compound | Scaffold | CB2 | CB1 | Typed parameters | Same lab dual func? | Near analogs that lose / lack Janus | Quality | Primary DOI |
|----|----------|----------|-----|-----|------------------|---------------------|--------------------------------------|---------|-------------|
| JAN-1 | **URB447** | pyrrole | Ago (mCB2 HEK cAMP ↓ @ 1 µM vs isoproterenol) | Neutral ant (rat GTPγS: blocks WIN; no basal GTPγS ↓) | Binding IC50 rat CB1 **313±72 nM**; hCB2 **41±23 nM**; GTPγS ant EC50 **4.9±0.8 µM** | Yes (LoVerme/Piomelli) | **5b** inactive binding both; **8a** weak CB2 binding — dual **func** for 5b/8a **NF** | **B** | [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059) |
| JAN-2 | **GW405833** | aminoalkylindole | Ago (legacy; protean caveats) | Noncomp. ant multi-pathway; arrestin ambiguous | Ki hCB2 **3.92±1.58 nM**; CB1 **4772±1676 nM**; DSE IC50 **2.6 µM** | Dual CB1 = Mackie 2017; CB2 = multi-lab | No matched same-series Janus↔non-Janus functional pair | **B** | [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539) |
| JAN-3 | **AM1710** | cannabilactone | Ago (cAMP EC50 **11 nM**, Emax **48%**) | Low-pot. competitive ant/inv; arrestin low-eff. ago | Ki hCB2 **6.7 nM**; rat CB1 **360 nM** | CB1 panel Mackie 2017; CB2 Makriyannis+Mackie | **AM1714** (9-OH): higher CB2 binding selectivity; **CB1 ant panel NF** | **B** | [10.1021/jm070441u](https://doi.org/10.1021/jm070441u); JPET 2017 |
| JAN-4 | **Qiu-14** | pyrazole-3-carboxamide | Ago (cAMP/HTRF S5A) | Ant (cAMP/HTRF S5B) | Direction only; **EC50/IC50/Emax = NF OA** | Yes (Qiu/Tao) | Authors claim **15/16/20/24** lose Yin-Yang — **comparator potencies/phenotypes OA NF** | **B** (anchor); pairs **C** | [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377) |
| JAN-5 | **Vasiljevik-27** | aminoalkylindole | Ago (CHO-hCB2 AC ~40–50%) | Neutral ant (blocks agonist **3** AC) | Ki mCB1 **15.4 nM**; hCB2 **10.9 nM** | Yes | See Block 2: **19** dual-ago; **35** dual-ago-class screen | **B** | [10.1021/jm400268b](https://doi.org/10.1021/jm400268b) |
| JAN-6 | **Vasiljevik-30** | same | Ago (~40–50% AC) | Neutral ant (same pattern) | Ki mCB1 **37.2 nM**; hCB2 **26.5 nM** | Yes | Same | **B** | same |

**Janus ligand count:** **6**  
**Closed Class-A Janus structural switch pairs:** **0**  
**Best usable Janus↔near-neighbor pairs (B/C):** URB 5b→447; Vasiljevik **35↔27**; **35↔30**; **19↔27/30**; Qiu 14 vs regio/C3 (**C**)

**Explicit non-Janus (do not promote):** MRI2687/MRI2594; HU-308/ago-3/(R)-1; AM10257 (opposite dual).

---

## Vasiljevik structural map (v2 closure — primary advance)

All from Vasiljevik et al. *J. Med. Chem.* 2013, PMC3904296 experimental section + Tables 1–2 + Figs. 3–4.

| Cpd | Exact structure (IUPAC from paper) | CB1 AC % @ 10 µM (screen) | CB2 AC % @ 10 µM | Follow-up | Phenotype label |
|-----|-------------------------------------|----------------------------|------------------|-----------|-----------------|
| **19** | 1-(1-Butyl-7-methoxy-1H-indol-3-yl)-2-(2,3-difluorophenyl)ethanone | **51** | **52** | Ki CB1 **1.7** / CB2 **0.81** nM; CB1 AC IC50 **~45 nM** | **CB1 ago + CB2 ago** (NOT Janus) |
| **27** | 1-Butyl-7-methoxy-3-(naphthalen-1-ylmethyl)-1H-indole | **18** | **33** | Ki 15.4 / 10.9 nM; **blocks agonist 3**; little intrinsic CB1 AC | **Janus** |
| **30** | 1-Butyl-7-methoxy-3-(naphthalen-2-yl)-1H-indole | **16** | **21** | Ki 37.2 / 26.5 nM; **blocks agonist 3** | **Janus** |
| **35** | 1-Butyl-7-methoxy-3-(naphthalen-1-yl)-1H-indole | **39** | **37** | No Ki; **no** formal ant-of-agonist panel | **dual ago-class (screen only)** |
| **17** | 1-(1-Butyl-7-methoxy-1H-indol-3-yl)-2-(4-fluorophenyl)ethanone | **−4** | **22** | Ki 387 / 281 nM (weak) | low-affinity CB1-null / weak CB2 ago — **not closed Janus** |

**Structural differences that matter:**

1. **19 → 27/30:** entire C3 pharmacophore rewritten (ketone–CH2–aryl → CH2-naphthyl or direct naphthyl). **Multi-mod.** Full Janus vs dual-ago functional contrast — Class **B**.
2. **35 → 27:** insert **methylene** between indole C3 and 1-naphthyl. **Minimal identifiable edit.** Screen: CB1 AC 39%→18% with CB2 ago retained; **27** has confirmed CB1 neutral ant. **35 lacks ant confirmation** → Class **B** (best small-edit *candidate*, not Class A).
3. **35 → 30:** **1-naphthyl → 2-naphthyl** attachment regioisomer (both direct C–C). Screen CB1 AC 39%→16%; **30** Janus-confirmed; **35** not ant-confirmed → Class **B**.

---

## Full pair matrix (v2)

Conventions: `PARAM:` typed; `NF` = NOT FOUND; **HIPÓTESIS** ≠ design rule.

### Block 1 — Janus anchors

| pair_id | A | B | scaffold | exact change | CB1 | CB2 | typed params | same lab | class | DOI |
|---------|---|---|----------|--------------|-----|-----|--------------|----------|-------|-----|
| J0-URB | URB447 | — | pyrrole | n/a | GTPγS neutral ant EC50 **4.9±0.8 µM** | cAMP ago @ 1 µM | IC50 CB1 **313±72**; CB2 **41±23** | yes | **B** | 10.1016/j.bmcl.2008.12.059 |
| J0-GW | GW405833 | — | indole | n/a | multi-pathway noncomp. ant | CB2 ago legacy | Ki CB2 **3.92**; CB1 **4772** nM | no | **B** | 10.1124/jpet.116.236539 |
| J0-AM | AM1710 | — | cannabilactone | n/a | low-pot. ant/inv | cAMP EC50 **11 nM** Emax **48%** | Ki CB2 **6.7**; CB1 **360** | no | **B** | 10.1021/jm070441u + JPET |
| J0-Q14 | Qiu-14 | — | pyrazole | o-morph N1-Ph | cAMP ant (S5B) | cAMP ago (S5A) | potencies **NF OA** | yes | **B** | 10.1016/j.bioorg.2023.106377 |
| J0-V27 | Vasiljevik-27 | — | AAI | n/a | AC neutral ant; blocks **3** | AC ago | Ki 15.4 / 10.9 | yes | **B** | 10.1021/jm400268b |
| J0-V30 | Vasiljevik-30 | — | AAI | n/a | same | same | Ki 37.2 / 26.5 | yes | **B** | same |

### Block 2 — Janus / non-Janus near neighbors

| pair_id | A (non/partial) | B (Janus) | exact change | region | CB1 | CB2 | typed params | same lab | notes | class |
|---------|-----------------|-----------|--------------|--------|-----|-----|--------------|----------|-------|-------|
| JN-URB1 | **5b** | URB447 | add N1-p-chlorobenzyl | **N1** | 5b inactive binding; URB447 dual + GTPγS ant | URB447 CB2 ago @ 1 µM | IC50 + GTPγS + cAMP qual. | yes | Best URB **emergence**; 5b lacks dual **func** | **B** |
| JN-URB2 | **8a** | URB447 | add 4-NH₂ on 3-benzoyl | **C4** | 8a weak; URB447 IC50 313 nM | 8a weak CB2; URB447 ago | mostly binding for 8a | yes | Func incomplete for 8a | **C** |
| JN-URB3 | **3c** | URB447 | adamantyl-amide vs 3-benzoyl-4-NH₂ | C3/C4 | 3c binding IC50 CB1 **70±10**, CB2 **11±4** — **func NF** | func NF | binding only for 3c | yes | Dual affinity ≠ Janus | **D** |
| JN-Q1–Q4 | Qiu-15/16/20/24 | Qiu-14 | N1 regio / o-Me-piperazine / C3 CH₂-Ad | N1 / C3 | 14 ant; comparators **phenotype NF OA** | 14 ago; comparators **NF OA** | all potencies **NF** | yes | Author switch + docking S6 = **COMP** | **C** |
| JN-V1 | **19** | **27 / 30** | rewrite C3: ketone–CH₂–(2,3-F₂Ph) → CH₂-1-naphthyl or 2-naphthyl | multi | **19:** CB1 ago AC IC50 ~45 nM; **27/30:** neutral ant | both CB2 ago-class | Ki + AC + ant-of-agonist for 27/30 | yes | Clearest **same-lab full-func** contrast; **not** minimal edit | **B** |
| JN-V2 | **35** | **27** | insert CH₂ (1-naphthyl → 1-naphthylmethyl) | **C3 linker** | 35: AC 39% (ago-class screen); 27: AC 18% + **blocks 3** | both ago-class | screen AC + Janus package for 27 only | yes | **Best minimal-edit candidate**; 35 lacks ant panel → not Class A | **B** |
| JN-V3 | **35** | **30** | 1-naphthyl → 2-naphthyl (direct) | **naphthyl regio** | 35: 39%; 30: 16% + blocks 3 | both ago-class | same asymmetry | yes | Small regio change; ant only for 30 | **B** |
| JN-V4 | **17** | **27/30** | 4-F-Ph ethanone (weak Ki) vs naphthyl Janus | multi | 17: AC −4% but Ki ~387 nM | 17: 22% AC | weak affinity | yes | Not a fair potency-matched pair | **C/D** |
| JN-AM14 | AM1714 | AM1710 | 9-OH ↔ 9-OMe | C9 | AM1714 CB1 ant **NF** | both CB2 ago-class (binding) | binding selectivity only | partial | Insufficient | **C/D** |

### Block 3 — Explicit non-Janus / opposite / pending

| pair_id | A | B | phenotype | class | note |
|---------|---|---|-----------|-------|------|
| T1 | MRI2687 | MRI2594 | CB2 inv ↔ ago; CB1 ago-class both | **A mono-CB2** | NOT Yin-Yang |
| T2 | ago-3 | (R)-1 | CB2 ago → inv | **A mono-CB2** | NOT Yin-Yang |
| S1 | AM10257 | — | CB2 inv + CB1 ago | **B opposite** | Opposite dual |
| P1_AZO | Azo23 | photoisom. | opposite-control claim | **B pending** | DOI 10.1016/j.ejmech.2026.118883 — numeric audit pending |
| P2_GERASI | AM8641 series | AM12435 et al. | dual CB1-ant / CB2-ago program | **PENDING embargo** | Northeastern thesis; available **2027-07-22**; abstract claims minimal-mod approach — **cannot score Class A until readable** |

---

## Series deep-dive notes (v2)

### URB447 (LoVerme/Piomelli 2009 OA PDF)
- Table 1 binding closed: **5b** >1000 / >1000; **8a** >1000 / 498±32; **8b URB447** 313±72 / 41±23; **3c** 70±10 / 11±4 nM.
- Only URB447 has GTPγS CB1 ant + cAMP CB2 ago.
- **3c** dual binder is **not** a Janus switch pair without function → Class **D** for Janus claim.
- No new Class A pair.

### GW405833
- Janus = reanalysis (Mackie 2017) of a historical CB2 tool (Valenzano 2005).
- Protean / inverse-ago CB2 literature (Mancini 2009; Yao 2008) complicates “CB2 ago” arm.
- **No OA matched analog pair** with dual CB1+CB2 functional Janus on/off.

### AM1710 / cannabilactones
- AM1714 remains binding-selectivity neighbor only (Khanolkar 2007); CB1 ant panel matching JPET **NF**.
- Molecules 2019 chain-substituted cannabilactones discuss class CB1 neutral ant/low-pot. inv as a **class claim**, not a closed A↔B structural switch pair for AM1710.

### Qiu 14/15/20/24
- Identities verified (SI Scheme / OCR): **14** o-morph+Ad; **15** m-morph; **16** p-morph; **20** o-4-Me-piperazinyl; **24** o-morph + CH₂-Ad.
- Functional direction for **14** only (S5). S11–S13 = “all compounds” curves — **no annotated EC50/IC50/Emax** in SI text/OCR.
- Author “N1-phenyl arm switch” + docking collisions (S6) remain **claim + COMPUTATIONAL**, not closed experimental Class A.
- Alleged numeric potencies from prior hypothesis tables: **REJECT / NF** (unchanged vs 0Q matrix).

### Vasiljevik (best same-lab functional contrast)
- Upgraded from v1: exact IUPAC for 19/27/30/35/17.
- **JN-V1** remains the only pair with **both** dual-ago and Janus arms fully functionally typed — but edit is **not small**.
- **JN-V2 / JN-V3** are the closest published small edits — Class **B** because the non-Janus arm (**35**) lacks antagonist-of-agonist confirmation.

### Other Yin-Yang literature
- Gerasi 2025 thesis (AM8641 → optimized duals; cryo-EM CB2; AM12435 in vivo): **embargoed**. Abstract implies designed duals via minimal modifications — **potential future Class A source**, not current evidence.
- No additional peer-reviewed OA Class A Janus structural switch located in this pass.

---

## HIPÓTESIS only (not design rules)

1. **HIPÓTESIS:** N1-pCl-benzyl enables URB447 Janus emergence — binding-supported; function asymmetric vs 5b.
2. **HIPÓTESIS:** Qiu ortho-morpholine is necessary/sufficient for Yin-Yang — author claim; OA comparator phenotypes incomplete; S173/S285 = **COMPUTATIONAL**.
3. **HIPÓTESIS:** Removing/replacing the C3 carbonyl / reshaping the naphthyl linker in AAIs can flip CB1 ago→neutral ant while retaining CB2 ago (Vasiljevik) — **experimental in one lab**, multi-mod for the fully typed pair.
4. **HIPÓTESIS:** Methylene insertion (35→27) or 1→2 naphthyl (35→30) is a Janus ON switch — **suggestive from screen + Janus confirmation on one arm only**.
5. **HIPÓTESIS:** Trp6.48 toggles (MRI/HU) generalize to Janus dual — **NOT SUPPORTED**.

---

## Answers to success criterion

1. **Does Janus (CB2-ago + CB1-ant/inv) exist with experimental functional evidence?**  
   **YES** — ≥6 ligands across pyrrole, indole, cannabilactone, pyrazole, aminoalkylindole.

2. **Is there a reproducible *small structural change* ↔ Janus on/off relationship?**  
   **NO as Class A.**  
   **WEAK as Class B:** JN-V2/JN-V3 (small edit, incomplete non-Janus ant panel); JN-URB1 (func asymmetric); JN-V1 (func complete, edit not small); Qiu regio (**C**).

3. **Do 0Q.1 Class-A pairs answer this?**  
   **NO** — mono-CB2 only.

4. **What would raise 0Q.2 toward MODERATE/STRONG without docking/NCE?**  
   - Qiu main PDF: typed CB1 IC50 / CB2 EC50/Emax for **14 vs 15/16/20/24** on same cAMP platform  
   - Vasiljevik-style ant-of-agonist panel for **35** (and preferably Ki) on same platform as 27/30  
   - Unembargo / publication of Gerasi AM8641 minimal-mod pairs with dual-arm numbers  
   - Independent replication of any one Janus dual-arm profile

---

## Classification & recommendation

| Item | Result |
|------|--------|
| **0Q.2-v2 overall** | **WEAK** (structural Janus switch); phenotype existence **supported** |
| **Janus ligand count** | **6** |
| **Class-A Janus structural pairs** | **0** |
| **Class A Janus switch found?** | **NO** |
| **Recommendation** | **KEEP** |
| Why not EXPAND FURTHER now? | Second OA pass closed Vasiljevik structures and still found **no Class A**; remaining blockers are **paywall/embargo**, not unsearched OA series |
| Why not KILL? | Multi-scaffold experimental Janus is real; inventory remains useful |
| **0Q.3?** | **Do not start** |
| **Global `0Q-SMRF`** | Remains **MODERATE** (no change proposed) |
| **0M** | Remains **FROZEN** |
| **PR branches pr1–pr5** | **Not touched** |

**User-facing one-liner:**  
`0Q.2-v2 = WEAK` | Class A Janus switch = **NO** | Recommendation = **KEEP** (no auto 0Q.3)

---

## Paths

| Deliverable | Path |
|-------------|------|
| This report | `results/reports/qiu_0q2_smrf_expand_v2.md` |
| CSV | `results/reports/qiu_0q2_smrf_expand_v2_pairs.csv` |
| Parent v1 | `results/reports/qiu_0q2_smrf_expand.md` |
| Parent matrix | `results/reports/qiu_0q_smrf_matrix.md` |

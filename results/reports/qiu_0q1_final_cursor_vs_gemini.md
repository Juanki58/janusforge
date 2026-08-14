# 0Q.1-FINAL — Cursor vs Gemini reconciliation (Class-A pairs)

**Fecha:** 2026-08-15  
**Inputs:**
1. **Cursor audit:** `results/reports/qiu_0q1_primary_audit_A_pairs.md`
2. **Gemini / pasted audit:** `C:\Users\juanc\AppData\Local\Temp\Se ha pegado el markdown(4).md` (872 lines; user comparison input)
3. **Context matrix:** `results/reports/qiu_0q_smrf_matrix.md` (`0Q-SMRF = MODERATE` — **unchanged** by this FINAL)

**Primary re-check this session:**
- Li/Hua *Cell* 2019 — PMC **PMC6713262** / DOI [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011)
- Kosar et al. *ACS Cent. Sci.* 2024 — PMC **PMC11117691** / DOI [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461)

**Bans respected:** no NCE; no docking/MD campaigns; no invented potencies; experimental vs computational vs inferred kept separate.

---

## Meta: what the two AI audits actually are

| Check | Finding |
|-------|---------|
| Structure / sections | Same template (ACCESS → Pair1 → Pair2 → Final table → Answers 1–7 → Recommendation) |
| Material claims | **Congruent** — same Class A, same YES/NO scopes, same EXPAND, same MODERATE lock |
| Numeric facts | **Same** (MRI EC50/Emax; ago-3 / (R)-1 pEC50/Emax; Kd 39.1 nM) |
| Formatting | Pasted file has **broken markdown tables** (each cell on its own `|` row) and minor bold/backtick punctuation differences; ~455 chars shorter after whitespace/table-junk normalization |
| Disagreement on A/B/C/D, YES/NO/INSUFFICIENT, or Trp mechanism tags | **NONE found** |

**Interpretation:** For 0Q.1-FINAL, treat Input 2 as an independent second pass that **confirms** the Cursor audit rather than a competing narrative. Where “Cursor vs Gemini” is cited below, “agreement” is near-total; residual notes are formatting / provenance, not scientific conflict.

**Global SMRF note (mandatory):** `0Q-SMRF = MODERATE` remains. FINAL recommendation is **EXPAND** (claim-splitting + literature matrix), **not KILL** of the mono-CB2 switch — therefore **no proposal to revise** the global SMRF verdict in this step.

---

## 1. Side-by-side comparison

### Pair 1 — MRI2687 ↔ MRI2594

| Topic | Cursor | Gemini (pasted) | AGREE / DISAGREE | Primary-source adjudication |
|-------|--------|-----------------|------------------|-----------------------------|
| IDs / IUPAC / HRMS | MRI2594 C17… 339.1740; MRI2687 C20… 375.1736 | Same | **AGREE** | **Verified** STAR Methods (PMC6713262): names + HRMS match |
| Single-change? | YES at arm-1 region; NOT single-atom | Same | **AGREE** | **Verified:** authors: “only differ in ‘arm 1’” — 6-methylbenzothiazole vs 4,5-dimethylthiazole |
| CB2 phenotype | 2594 **ago**; 2687 **inv**; β-arrestin2 | Same | **AGREE** | **Verified Fig. 6C:** 2594 EC50 **0.17±0.03** nM, Emax **2.0±0.2**; 2687 EC50 **0.24±0.06** nM, Emax **0.75±0.04** |
| CB1 phenotype | Both ago-class (2594 full fold; 2687 partial) | Same | **AGREE** | **Verified Fig. 6D:** 2594 EC50 **310±54** nM, Emax **28.0±2.0**; 2687 EC50 **114±15** nM, Emax **6.0±0.3** |
| Yin-Yang dual? | **NO** | **NO** | **AGREE** | Primary: CB1 stays agonist-class; authors note CB2-ant/CB1-ago *motif* elsewhere (AM10257), not for this pair as CB1-ant+CB2-ago |
| Comparability | **HIGH** | **HIGH** | **AGREE** | Same β-arrestin2 platform / paper |
| Mechanism tags | Func = **EXPERIMENTAL**; Trp pose = **author-proposed + docking/MD (COMP)**; co-crystal MRI = **NOT FOUND** | Same | **AGREE** | **Verified:** Fig. 6B docking; MD methods for Trp rotamer; no MRI–CB2 co-crystal in paper |
| Class | **A** | **A** | **AGREE** | Sustained by experimental functional flip + structure context |
| Switch demonstrated? | **YES** mono-CB2; **NO** Yin-Yang | Same | **AGREE** | Primary supports |

**Better-supported claim:** Both AIs correctly state the facts. Prefer **primary Fig. 6** wording: MRI2687 = CB2 inverse agonist; MRI2594 = CB2 agonist; arm-1 bulk toward Trp6.48 is **author + computational** explanation of an **experimental** phenotype flip.

---

### Pair 2 — HU-308 → (R)-1 (fair control: ago-3)

| Topic | Cursor | Gemini (pasted) | AGREE / DISAGREE | Primary-source adjudication |
|-------|--------|-----------------|------------------|-----------------------------|
| Design claim | C(2′) phenyl flips ago→inv | Same | **AGREE** | **Verified** abstract/Scheme 1: phenyl at gem-dimethylheptyl → inverse agonists (S)/(R)-1 |
| HU-308→(R)-1 single-edit? | **NO** (phenyl + azide + OH→NH2) | Same | **AGREE** | **Verified** design text: azide + allylic alcohol→amine added for conjugation/selectivity |
| Fair matched pair | **ago-3** vs phenyl series (eq 1) | Same | **AGREE** | **Verified:** ago-3 “same scaffold … except that it lacks the C(2′) phenyl” |
| CB2 numbers | ago-3 pEC50 **8.47**, Emax **+112%**; (R)-1 **6.95**, **−44%** | Same | **AGREE** | **Verified Table 3** (cAMP HTRF) |
| Gi / arrestin | (R)-1 Gi pEC50 **6.80**, Emax **−28%**; no β-arrestin recruitment | Same | **AGREE** | **Verified Table 4** + text |
| Binding | (R)-1 Kd **39.1 nM** | Same | **AGREE** | **Verified** abstract / binding section |
| CB1 ant switch? | **NOT shown** / CB2-selective | Same | **AGREE** | No dedicated CB1 ago/ant phenotype table for (R)-1 comparable to CB2 Table 3 in retrieved full text |
| Comparability | HIGH for ago-3; MEDIUM for multi-change HU-308→(R)-1 | Same | **AGREE** | Primary supports distinction |
| Mechanism tags | Func multi-assay = **EXPERIMENTAL**; Trp engagement = **docking/MD (COMP)**; (R)-1 co-crystal = **NOT FOUND** | Same | **AGREE** | **Verified:** docking into 5ZTY; MD of (S)/(R)-3 vs ago-3 |
| Class | **A** | **A** | **AGREE** | Sustained |
| Switch demonstrated? | **YES** mono-CB2 via phenyl (ago-3 control); **NO** Yin-Yang | Same | **AGREE** | Primary supports |

**Better-supported claim:** Both AIs correctly isolate **ago-3** as the single-region control. Prefer labeling the **experimental** switch as **ago-3 → (R)-series**, and treat literal HU-308→(R)-1 as **multi-change design lineage**, not the clean SAR pair.

---

## 2. Corrected consensus facts table (verified only)

| Fact | Evidence type | Source |
|------|---------------|--------|
| MRI2594 / MRI2687 differ only in arm-1 heterocycle (4,5-dimethylthiazole ↔ 6-methylbenzothiazole); shared TMCP-imino + N3-acetoxyethyl | Experimental (synthesis + structures) | *Cell* 2019 STAR Methods + Fig. 6A |
| CB2 β-arrestin2: MRI2594 ago EC50 0.17±0.03 nM, Emax 2.0±0.2; MRI2687 inv EC50 0.24±0.06 nM, Emax 0.75±0.04 | **Experimental** | Fig. 6C |
| CB1 β-arrestin2: MRI2594 ago EC50 310±54 nM, Emax 28.0±2.0; MRI2687 partial ago EC50 114±15 nM, Emax 6.0±0.3 | **Experimental** | Fig. 6D |
| CB2–AM10257 crystal **5ZTY** informs pocket; MRI poses = docking; Trp MD = computational | Mixed (struct exp. + COMP for MRI) | *Cell* 2019 |
| Direct MRI–CB2 co-crystal | **NOT FOUND** | Primary |
| (R)-1 CB2 Kd 39.1 nM; cAMP inv pEC50 6.95, Emax −44%; Gi inv pEC50 6.80, Emax −28% | **Experimental** | *ACS Cent. Sci.* 2024 |
| ago-3 (no C2′ Ph): cAMP ago pEC50 8.47, Emax +112% | **Experimental** | Table 3 + eq 1 |
| Phenyl series: no β-arrestin recruitment; no ERK/Ca2+ activation (stated for probes) | **Experimental** | Main text panels |
| HU-308→(R)-1 also adds azide + alcohol→amine | Experimental design statement | Design section |
| Trp2586.48 engagement by C(2′) phenyl | **Author-proposed + COMP** (docking/MD) | Scheme 1, Fig. 1C, MD section |
| (R)-1–CB2 co-crystal | **NOT FOUND** | Primary |
| Either pair is a demonstrated CB1-ant + CB2-ago Yin-Yang structural rule | **Not supported** by these A pairs | Both papers’ functional tables |

---

## 3. Individual conclusions after reconciliation

### MRI2687 ↔ MRI2594

| Question | Verdict | Scope |
|----------|---------|-------|
| Predictable CB1/CB2 **dual** phenotype modulation via this structural change? | **NO** | CB1 remains agonist-class (full↔partial only) |
| Predictable **CB2** phenotype modulation (ago ↔ inv/ant) via arm-1 bulk? | **YES** | Thiazole chemotype; same-assay pair |
| Survive as Class **A**? | **YES** | **Mono-CB2** function switch only — **not** Yin-Yang |

### HU-308 / (R)-1 (via ago-3)

| Question | Verdict | Scope |
|----------|---------|-------|
| Predictable dual Yin-Yang via C(2′) phenyl? | **NO** | CB2-selective platform; no CB1 ant switch shown |
| Predictable **CB2** ago → inv via C(2′) phenyl? | **YES** | When attributed via **ago-3** matched control; multi-assay |
| Survive as Class **A**? | **YES** | **Mono-CB2**; label HU-308→(R)-1 carefully as multi-mod lineage |

**Neither pair:** INSUFFICIENT for the experimental phenotype flip itself — evidence is sufficient for mono-CB2. **INSUFFICIENT** only if the claim is universal dual CB1/CB2 switch law (that claim fails → **NO**, not INSUFFICIENT).

---

## 4. Answers (locked after reconciliation)

1. **Does MRI pair survive as A?**  
   **YES** — mono-CB2 ago↔inv/ant (arm-1 bulk). **Not** as Yin-Yang dual SAR.

2. **Does HU-308 pair survive as A?**  
   **YES** — mono-CB2 ago→inv, with **ago-3** as fair single-region control.

3. **What both share**  
   - Experimental CB2 **efficacy-mode** flips (ago ↔ inv/ant), not mere potency loss.  
   - Design narrative: **bulk toward Trp2586.48**, informed by inactive CB2 **5ZTY**.  
   - Matched / near-matched chemotypes in one paper.  
   - Trp contact = **proposed + computational**; phenotype = **experimental**.

4. **What they do NOT share**  
   - Scaffold (thiazole vs cannabilactone/pinene).  
   - Exact edit (heterocycle fusion vs C2′ phenyl).  
   - Assay breadth (β-arrestin2-centric vs cAMP/Gi/arrestin/ERK/Ca2+).  
   - CB1 outcome (MRI: both CB1 agonists; HU series: CB2-selective).  
   - Neither demonstrates CB1-ant + CB2-ago as the product of the same edit.

5. **General molecular switch claim?**  
   **NO** as a universal dual CB1/CB2 law.  
   **Restricted YES:** local bulk toward Trp6.48 can flip **CB2** ago↔inv across ≥2 scaffolds (mono-receptor claim). Yin-Yang remains a **separate** Class-B historical phenotype, not established by these A pairs.

6. **What would elevate evidence?** *(literature / historical / wet-orthogonal — **not** mandatory docking/MD/NCE)*  
   - Co-crystal or cryo-EM of MRI pair and of (R)-1 / ago-3 with CB2.  
   - Direct Trp258 mutagenesis with these exact ligands.  
   - Multi-pathway panel on MRI pair (cAMP + Gi + arrestin).  
   - Independent lab replication.  
   - Single-edit HU-308 ± C2′ phenyl without azide/amine confounders.  
   - For dual claims: matched open-potency pairs that flip CB1 and CB2 in opposite directions (outside these two A pairs; continue SMRF B/C matrix).

---

## 5. 0Q.1-FINAL recommendation

### **EXPAND**

| Option | Decision | Why |
|--------|----------|-----|
| **KEEP** (as-is, no framing change) | Partial — keep both as Class A mono-CB2 | Evidence holds, but framing must stay split |
| **EXPAND** | **SELECTED** | Split claims: (i) Trp6.48-linked **mono-CB2** efficacy switch (A, supported) vs (ii) Yin-Yang dual CB1/CB2 (B/C matrix; not carried by these A pairs). Continue historical literature expansion of B/C Janus pairs and Qiu OA gaps |
| **KILL** | Rejected | Experimental CB2 switches are real in both primary papers; killing would contradict verified Fig. 6 / Tables 3–4 |

**Global `0Q-SMRF`:** remains **MODERATE**. No update proposed (KILL of the entire switch hypothesis did **not** occur).

**Explicit next-step ban:**  
**No NCE, no docking, no MD** as a mandatory next step from 0Q.1-FINAL.  
EXPAND here means **literature / claim-framing expand only** (SMRF matrix, OA potency gaps, Class B Janus documentation) — not compute campaigns.

---

## 6. Paths

| Item | Path |
|------|------|
| This FINAL | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` |
| Cursor audit | `results/reports/qiu_0q1_primary_audit_A_pairs.md` |
| Gemini/pasted input | `C:\Users\juanc\AppData\Local\Temp\Se ha pegado el markdown(4).md` |
| Parent matrix (MODERATE unchanged) | `results/reports/qiu_0q_smrf_matrix.md` |

---

## Executive return

| Item | Result |
|------|--------|
| **FINAL recommendation** | **EXPAND** |
| **MRI consensus** | Class **A** survives — **YES** mono-CB2; **NO** Yin-Yang |
| **HU-308/(R)-1 consensus** | Class **A** survives — **YES** mono-CB2 via ago-3; **NO** Yin-Yang; multi-change HU-308→(R)-1 labeled carefully |
| **AI conflict** | **None material** — pasted Gemini input confirms Cursor |
| **SMRF global** | **MODERATE** unchanged |

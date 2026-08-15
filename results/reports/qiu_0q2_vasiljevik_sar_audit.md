# 0Q.2 — Vasiljevik-series Janus SAR primary audit (binding ≠ function)

**Date:** 2026-08-15  
**Branch:** `cursor/qiu-protocol-ip-cro-0p`  
**Scope:** Vasiljevik et al. aminoalkylindole family **only** (+ immediate JWH-073 / M4 lineage numbers tabulated in primary sources).  
**Bans respected:** no docking/MD; no NCE/design; no Qiu-14 / MRI / HU-308 extrapolation; no 0Q.3; PR1–PR5 untouched.

**Primary sources used:**

| Ref | Citation | Access this pass |
|-----|----------|------------------|
| **V2013** | Vasiljevik et al., *J. Med. Chem.* **56**, 4537–4550 (2013). DOI [10.1021/jm400268b](https://doi.org/10.1021/jm400268b); PMC3904296; KU ScholarWorks author PDF | **OA** — Tables 1–2, Figs 3–4, experimental names |
| **B2012** | Brents et al., *Biochem. Pharmacol.* **83**, 952–961 (2012). DOI [10.1016/j.bcp.2012.01.004]; PMC3288656 | **OA** — JWH-073-M4 CB1 GTPγS lineage (compound **4** in V2013) |
| ACS SI `jm400268b_si_001.pdf` | HPLC only (authors: compounds 17–37) | **NOT RETRIEVED** this pass (ACS Cloudflare); HPLC purity only — **not required** for functional matrix |

**Janus definition (this audit):** experimental **CB2 agonist** + experimental **CB1 antagonist or inverse agonist** in **functional** assays. Binding alone ≠ Janus.  
**Janus column values:** **YES** / **NO** / **INSUFFICIENT** only.

**Dictamen (exact one):** 🟡 **SAR SUGERENTE PERO INSUFICIENTE**

---

## Identity note — compound **19** (author-manuscript conflict)

| Field | Evidence |
|-------|----------|
| **Section heading (PMC/KU)** | “1-(1-Butyl-7-methoxy-1H-indol-3-yl)-2-(2,3-difluorophenyl)ethanone (**19**)” — **same string reused for compound 37** |
| **Experimental body for 19** | Synthesized with **1-naphthoyl chloride**; ¹H NMR lacks ethanone CH₂; HRMS `[M+Na+CH₃CN]` calcd **C₂₆H₂₆N₂NaO₂** → consistent with **(1-butyl-7-methoxy-1H-indol-3-yl)(naphthalen-1-yl)methanone** |
| **Compound 37 body** | Made from **2-(2,3-difluorophenyl)acetic acid**; ethanone CH₂ present; HRMS matches F₂ ethanone |

**Structure used in this audit for 19:** **(1-butyl-7-methoxy-1H-indol-3-yl)(naphthalen-1-yl)methanone** (7-OMe-JWH-073), from synthesis/NMR/HRMS — **not** the duplicated ethanone heading.  
Prior 0Q notes that treated 19 as 2,3-difluorophenyl ethanone are **superseded** for this chemotype audit.

---

## Assay platforms (V2013 — comparable within series)

| Layer | CB1 | CB2 |
|-------|-----|-----|
| **Binding screen** | % displacement of [³H]CP-55,940 @ **1 µM** (mouse CB1 membranes) | same @ **1 µM** (hCB2) |
| **Binding Ki** | full CRC → **Ki** mCB1 (selected compounds only) | full CRC → **Ki** hCB2 |
| **Function screen** | % vehicle inhibition of **AC** @ **10 µM** (Neuro2A endogenous CB1) | % AC inhibition @ **10 µM** (CHO-hCB2) |
| **Function follow-up** | AC CRC; **antagonism of agonist 3** (Fig 3B); in vivo hypothermia block (27/30) | AC CRC (Fig 4); CHO-WT null control for 27/30 |

CP-55,940 AC anchors (Table 1): CB1 **45%**, CB2 **37%**.

---

## Extraction matrix (required columns)

Binding and function kept separate. Missing numeric values = **NOT REPORTED**.

| Compuesto | Cambio Estructural vs. 19 | CB1 Binding (Ki / Kd) | CB2 Binding (Ki / Kd) | CB1 Función (IC50 / % Inh / Ensayo) | CB2 Función (EC50 / Emax / Ensayo) | ¿Fenotipo Janus Probado Experimentalmente? | Fuente Primaria (Ref / Tabla / DOI) |
|-----------|---------------------------|------------------------|------------------------|-------------------------------------|-------------------------------------|---------------------------------------------|--------------------------------------|
| **19** | reference: 7-OMe, *n*-butyl, C3=**1-naphthoyl** | Ki **1.7 ± 0.3 nM** (mCB1) | Ki **0.81 ± 0.4 nM** (hCB2) | AC @10 µM **51%**; AC IC50 **~45 nM** → **agonist** | AC @10 µM **52%**; Fig 4 CRC ago-class → **agonist**; EC50/Emax **NOT REPORTED** | **NO** (dual agonist) | V2013 Tables 1–2; Figs 3–4; DOI 10.1021/jm400268b |
| **27** (TV-5-249) | C3: 1-naphthoyl → **1-naphthylmethyl** (C=O removed; CH₂ linker) | Ki **15.4 ± 2.2 nM** | Ki **10.9 ± 3.1 nM** | AC @10 µM **18%**; little AC CRC inhib.; **antagonizes agonist 3** (Fig 3B); blocks 3-hypothermia → **neutral antagonist** | AC @10 µM **33%**; Fig 4 text **~40–50%** AC inhib. ago-class; CHO-WT null; EC50/Emax **NOT REPORTED** | **YES** | V2013 T1–T2; Figs 3–5; DOI 10.1021/jm400268b |
| **30** (TV-6-41) | C3: 1-naphthoyl → **direct 2-naphthyl** (no carbonyl; regio change) | Ki **37.3 ± 11.8 nM** | Ki **26.5 ± 1.5 nM** | AC @10 µM **16%**; ant of agonist **3**; hypothermia block → **neutral antagonist** | AC @10 µM **21%**; Fig 4 ago-class narrative; CHO-WT null; EC50/Emax **NOT REPORTED** | **YES** | V2013 T1–T2; Figs 3–5 |
| **35** | C3: 1-naphthoyl → **direct 1-naphthyl** | Ki **NOT REPORTED** | Ki **NOT REPORTED** | AC @10 µM **39%** (ago-class screen); ant-of-agonist **NOT REPORTED** | AC @10 µM **37%** (ago-class screen); EC50/Emax **NOT REPORTED** | **INSUFFICIENT** | V2013 Table 1 |
| **23** | C3: 1-naphthoyl → **1-naphthylacetyl** (insert CH₂ between C=O and naphthyl) | Ki **NOT REPORTED**; %disp @1 µM **81%** | Ki **NOT REPORTED**; %disp **91%** | AC @10 µM **34%** | AC @10 µM **−40%** (sign atypical vs CP); EC50 **NOT REPORTED** | **INSUFFICIENT** (CB2 direction ambiguous; no ant panel) | V2013 Table 1 |
| **17** | C3: 1-naphthoyl → **4-F-phenylacetyl** | Ki **387 ± 77 nM** | Ki **281 ± 51 nM** | AC @10 µM **−4%**; ant-of-agonist **NOT REPORTED** | AC @10 µM **22%**; EC50 **NOT REPORTED** | **INSUFFICIENT** (weak affinity; CB1 null screen without ant confirmation) | V2013 T1–T2 |
| **21** | C3: 1-naphthoyl → **phenylacetyl** | Ki **NOT REPORTED**; %disp **69%** | Ki **NOT REPORTED**; %disp **91%** | AC @10 µM **34%** | AC @10 µM **16%** | **NO** (dual ago-class screen; not Janus) | V2013 Table 1 |
| **31** | C3: 1-naphthoyl → **4-F-benzoyl** (methanone, phenyl) | Ki **NOT REPORTED**; %disp **84%** | Ki **NOT REPORTED**; %disp **99%** | AC @10 µM **45%** | AC @10 µM **38%** | **NO** (dual ago-class) | V2013 Table 1 |
| **32** | C3 → **2-F-phenylacetyl** | Ki **NOT REPORTED**; %disp **84%** | Ki **NOT REPORTED**; %disp **99%** | AC @10 µM **45%** | AC @10 µM **1%** | **NO** / **INSUFFICIENT** for CB2 (near-null CB2 AC; no ant at CB1) | V2013 Table 1 |
| **37** | C3 → **2,3-F₂-phenylacetyl** (true ethanone; heading twin of mislabeled 19 title) | Ki **NOT REPORTED**; %disp **80%** | Ki **NOT REPORTED**; %disp **97%** | AC @10 µM **35%** | AC @10 µM **−6%** | **NO** (CB1 ago-class; CB2 not ago) | V2013 Table 1 |
| **28** | N1: *n*-butyl → **2-morpholinoethyl**; C3 remains **1-naphthoyl**; 7-OMe | Ki **NOT REPORTED**; %disp **100%** | Ki **NOT REPORTED**; %disp **100%** | AC @10 µM **39%** | AC @10 µM **37%** | **NO** (dual ago-class) | V2013 Table 1 |
| **25** | 7-OMe → **5-OMe**; C3 **1-naphthoyl** | Ki **NOT REPORTED**; %disp **90%** | Ki **NOT REPORTED**; %disp **90%** | AC @10 µM **47%** | AC @10 µM **31%** | **NO** | V2013 Table 1 |
| **26** | 7-OMe → **5-OH**; C3 **1-naphthoyl** | Ki **NOT REPORTED**; %disp **97%** | Ki **NOT REPORTED**; %disp **91%** | AC @10 µM **39%** | AC @10 µM **37%** | **NO** | V2013 Table 1 |
| **4** (JWH-073-M4) | 7-OMe → **7-OH**; C3 **1-naphthoyl**; N1 *n*-butyl (parent metabolite scaffold) | Ki **24.2 ± 17.2 nM** (V2013); B2012 reports CB1 Ki **~122 nM** in brain homogenate panel — **do not merge labs** | Ki **78.3 ± 36.2 nM** (V2013); B2012 CB2 Ki **NOT REPORTED** | V2013 AC @10 µM **55%** → **agonist** in AC; B2012 [³⁵S]GTPγS: **neutral** (no basal act./inhib.) + competitive ant — **assay-discordant CB1 efficacy** | V2013 AC @10 µM **38%** → **agonist**; B2012 CB2 function **NOT REPORTED** | **NO** in V2013 AC package; **INSUFFICIENT** as Janus (CB2 ago V2013 + CB1 ant only in B2012 GTPγS — **not same assay**) | V2013 T1–T2; B2012 Figs 2–5 / text; DOI 10.1016/j.bcp.2012.01.004 |
| **3** (JWH-073) | 7-OMe → **H**; C3 **1-naphthoyl** | Ki **12.9 ± 3.4 nM** | Ki **9.8 ± 0.9 nM** | used as **full CB1 agonist** tool (Fig 3B); AC % for 3 alone in T1 **NOT REPORTED** | CB2 function for 3 in V2013 **NOT REPORTED** | **NO** (CB1 agonist tool; not Janus) | V2013 Table 2; Fig 3B |

**Optional CSV:** `results/reports/qiu_0q2_vasiljevik_sar_audit.csv`

---

## Same-paper dual-function census

| Set | n | Members |
|-----|---|---------|
| Series analogs with **both** CB1 + CB2 AC % in Table 1 (excl. CP control) | **14** | 4, 17, 19, 21, 23, 25, 26, 27, 28, 30, 31, 32, 35, 37 |
| Of those with **Ki** both receptors | **5** | 4, 17, 19, 27, 30 (+ lineage **3**) |
| Janus **YES** (closed dual func) | **2** | **27**, **30** |
| Janus **NO** (typed non-Janus dual func) | **8** | 19, 21, 25, 26, 28, 31, 4 (AC), (+ 3 as ago tool) |
| Janus **INSUFFICIENT** | **4** | 17, 23, 32, **35** |

---

## Structural changes backed by same-paper comparable assays

| Change | Pair | Same assays? | What is closed | Gap |
|--------|------|--------------|----------------|-----|
| C3 **naphthoyl → 1-naphthylmethyl** | **19 → 27** | **YES** (Ki + AC + ant-of-3 for 27; Ki + AC ago for 19) | CB1 **ago → neutral ant**; CB2 **ago retained** | Multi-atom (carbonyl removal); not a CB2 efficacy invert |
| C3 **naphthoyl → direct 2-naphthyl** | **19 → 30** | **YES** (same) | same phenotype flip | Multi-change (linker + regio) |
| C3 **direct 1-naphthyl → 1-naphthylmethyl** | **35 → 27** | **PARTIAL** | 27 Janus closed; 35 AC screen only | **35** Ki + ant **NOT REPORTED** |
| C3 **direct 1-naphthyl → direct 2-naphthyl** | **35 → 30** | **PARTIAL** | same | same gap on **35** |
| C3 naphthoyl → naphthylacetyl | **19 → 23** | screen only | both bind; CB2 AC sign odd | no Ki; no ant; CB2 unclear |
| 7-OMe → 7-OH on naphthoyl | **19 → 4** | Ki+AC yes | both dual ago in V2013 AC | does **not** create Janus in AC; B2012 GTPγS CB1 ant is **different assay** |

**No tabulated pair** isolates a single edit that **inverts CB2** (ago↔inv) **while CB1 antagonism is held constant**.

---

## Mandatory answers (tabulated data only)

1. **Clear continuous SAR progression?** **No** — phenotype jump is real for 19→27/30, but edits are multi-site and the closest single-edit candidate (**35**) lacks Ki + antagonist confirmation.
2. **Concrete chemical change that activates/inverts CB2 efficacy while maintaining CB1 antagonism?** **No** — published closed change is CB1 **ago → neutral ant** with **CB2 agonism retained**, not a CB2 efficacy invert under fixed CB1 antagonism.
3. **Divergent A/B switch pairs under identical conditions?** **Yes (limited)** — **19 (NO)** vs **27/30 (YES)** fully typed same lab/assays; **35** vs **27/30** is divergent on screen only → incomplete.
4. **Simultaneous CB1-ant + CB2-ago in paired functional assays demonstrated?** **Yes** — for **27** and **30** only (AC + ant-of-agonist + CB2 AC ago; CHO-WT control).
5. **Are assays methodologically comparable across series members?** **Yes within V2013** (shared binding/AC platforms). **No** for merging B2012 GTPγS (M4) with V2013 AC without caveat.

---

## Final dictamen

### 🟡 **SAR SUGERENTE PERO INSUFICIENTE**

**Why not 🟢:** No minimal-edit ON/OFF pair with **both** arms fully functionally typed; no rule that toggles CB2 efficacy under maintained CB1 antagonism; n Janus YES = 2, from multi-mod C3 rewrites vs naphthoyl **19**.  
**Why not 🔴:** Same-lab dual functional Janus for **27/30** is experimental fact; **19** is a real dual-agonist OFF contrast under identical assays.

**0Q decision after this pass:** treat the Vasiljevik chemotype Janus observation as **historical literature fact only** — **do not** promote a chemotype design rule; **CLOSE further 0Q chemotype-rule hunting** on this series unless new primary dual-func data (e.g. ant panel on **35**) appear. No NCE/design.

---

## Paths

| File | Path |
|------|------|
| This audit | `results/reports/qiu_0q2_vasiljevik_sar_audit.md` |
| Matrix CSV | `results/reports/qiu_0q2_vasiljevik_sar_audit.csv` |
| Local OA extracts | `data/papers/vasiljevik_2013/` (PMC HTML, KU PDF, parsed T1/T2) |

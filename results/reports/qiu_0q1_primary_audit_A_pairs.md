# 0Q.1 — Primary audit of SMRF Class-A pairs

**Fecha:** 2026-08-14  
**Scope:** Primary-literature audit of the two Class-A pairs listed in `qiu_0q_smrf_matrix.md` / `qiu_0q_smrf_pairs.csv`.  
**Pairs:** (1) MRI2687 ↔ MRI2594; (2) HU-308 → (R)-1 (with matched control ago-3).  
**Bans respected:** no molecule design, docking/MD campaigns, NCE, rule extrapolation, or filling missing data.  
**Status note (mandatory):** This is **0Q.1 only**. Global verdict **`0Q-SMRF = MODERATE` is NOT changed** by this deliverable.

**Inputs read first:** `results/reports/qiu_0q_smrf_matrix.md`, `results/reports/qiu_0q_smrf_pairs.csv`.

---

## ACCESS (paywall / OA)

| Pair | Primary DOI | Access this session | Full text / SI used |
|------|-------------|---------------------|---------------------|
| MRI2687 ↔ MRI2594 | [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011) | **PARTIAL OA / mirror.** PMCID **PMC6713262** (NIHMS) exists; PMC HTML/PDF blocked by reCAPTCHA here. EuropePMC abstract OA. **Usable full main text + STAR Methods** recovered from publisher-PDF mirror (Newswise copy of Elsevier PDF). ScienceDirect landing paywalled. | Main text + STAR Methods (synthesis names, Figure 6 numbers). SI figures cited in main text (Fig. S2 schemes; Fig. S6 docking/MD). |
| HU-308 → (R)-1 | [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461) | **OA full text.** PMC **PMC11117691**; ACS Cent. Sci. HTML OA. SI PDF fetch timed out this session; main-text tables + methods sufficient for phenotype switch. | Full PMC/ACS HTML (Tables 1–4; Scheme 1–2; eq 1 ago-3 control). |

Secondary corroboration (not used to invent numbers): Yeliseev et al. *Sci. Rep.* 2021 [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6) / PMC7881127 — same MRI chemotype; membrane-context note for related benzothiazoles.

---

## Pair 1 — MRI2687 ↔ MRI2594

### A. Identification

| Item | Evidence |
|------|----------|
| Names | **MRI2687** (also MRI-2687); **MRI2594** (also MRI-2594) |
| IUPAC / source names | **MRI2594:** 2-(4,5-dimethyl-2-((2,2,3,3-tetramethylcyclopropane-1-carbonyl)imino)thiazol-3(2H)-yl)ethyl acetate. **MRI2687:** 2-(6-methyl-2-((2,2,3,3-tetramethylcyclopropane-1-carbonyl)imino)benzo[d]thiazol-3(2H)-yl)ethyl acetate. |
| SMILES | **NOT FOUND** as SMILES strings in primary text. Identities fixed by IUPAC + NMR/HRMS in STAR Methods. |
| HRMS | MRI2594 [M+H]+ found 339.1740 (calcd 339.1742, C17H27N2O3S); MRI2687 [M+H]+ found 375.1736 (calcd 375.1742, C20H27N2O3S). |
| Primary ref | Li, Hua, … Liu et al., *Cell* **176**, 459–467.e13 (2019). DOI **10.1016/j.cell.2018.12.011**. PMID **30639103**. |
| Year | **2019** (online 2019-01-10; issue Jan 24, 2019) |
| Lab / roles | Structure/docking narrative: **Liu / Hua / Li** (ShanghaiTech iHuman). Ligand synthesis of MRI pair: **Iyer / Kunos** (NIAAA) in STAR Methods. Functional β-arrestin assays: **Bohn** lab (Scripps). Scaffold lineage: A-836339-related thiazole (authors). Crystal context ligand AM10257: **Makriyannis** CDD. |

### B. Structural change

Authors state the ligands **“only differ in arm 1”**: extended central **6-methylbenzothiazole** (MRI2687) vs **4,5-dimethylthiazole** (MRI2594).

**Is it a single-change pair?** **YES at the intended region (arm-1 / central heterocycle bulk)** — shared tetramethylcyclopropane carboximidoyl + N3-(2-acetoxyethyl). **NOT a single-atom edit:** difference = thiazole → **benzo-fused** thiazole + methyl topology change (4,5-dimethyl vs 6-methyl on benzothiazole).

**ALL differences listed:**

1. Heterocycle core: 4,5-dimethylthiazole (2594) vs 6-methylbenzo[d]thiazole (2687).  
2. Extra fused benzene ring atoms in 2687 (bulk toward Trp2586.48 in authors’ model).  
3. Methyl substitution pattern change (two methyls on thiazole vs one methyl on benzothiazole C6).  
4. No other scaffold arms differ in the published chemical names (same cyclopropane amide; same ethyl acetate).

### C. CB1 assays / results (no conversion)

Assay: **β-arrestin2 recruitment** (same platform as CB2 in Fig. 6).

| Ligand | Role claimed | EC50 | Emax (fold) |
|--------|--------------|------|-------------|
| CP55,940 (ctrl) | ago | 17.9 ± 1.4 nM | 20.6 ± 0.9 |
| **MRI2594** | **agonist** | **310.0 ± 54.0 nM** | **28.0 ± 2.0** |
| **MRI2687** | **partial agonist** | **114.0 ± 15.0 nM** | **6.0 ± 0.3** |

**Not a CB1 antagonist switch.** Both remain CB1 agonists (2594 stronger efficacy fold; 2687 partial). Binding Ki CB1 for the pair: **NOT FOUND** as primary pair numbers in retrieved main text.

### D. CB2 assays / results (no conversion)

Assay: **β-arrestin2 recruitment** (Fig. 6C).

| Ligand | Role claimed | EC50 | Emax (fold) |
|--------|--------------|------|-------------|
| CP55,940 | ago ctrl | 2.3 ± 0.6 nM | 2.3 ± 0.1 |
| **MRI2594** | **agonist** | **0.17 ± 0.03 nM** | **2.0 ± 0.2** |
| **MRI2687** | **inverse agonist** | **0.24 ± 0.06 nM** | **0.75 ± 0.04** |
| AM10257 | inv/ant ctrl | 0.20 ± 0.04 nM | 0.70 ± 0.05 |

Directions: **CB2 ago (2594) ↔ CB2 inv/ant (2687)**. Same lab/assay for the pair. Secondary literature (Yeliseev 2021) reports MRI-2594 Ki 0.031 nM / EC50 0.09 nM in GTPγS CHO membranes and MRI-2687 as inverse in that setting — corroborative, not required for the Cell primary claim.

### E. Comparability

**HIGH** for CB2 function within *Cell* 2019: same β-arrestin2 assay, same paper, matched pair designed together.  
Caveats (do not downgrade below HIGH for the CB2 switch itself): mechanism poses = docking into 5ZTY; MD = computational. Related benzothiazoles can show membrane-cholesterol-dependent classification shifts (Yeliseev 2021) — relevant for generalization, not for denying the published pair contrast.

### F. Functional change type

**CB2 efficacy mode switch: agonist ↔ inverse agonist/antagonist** (not mere potency loss).  
**CB1:** potency/efficacy change within agonist class (full ↔ partial) — **not** an ago↔ant switch.  
**Not Yin-Yang CB1-ant + CB2-ago.**

### G. Mechanism (tiered; do not promote)

| Tier | Content |
|------|---------|
| **(1) Experimentally demonstrated** | Functional phenotype contrast in β-arrestin2 (Fig. 6C–D). Receptor pocket context from **crystal CB2–AM10257 (5ZTY)**. Mutagenesis in paper targets AM10257 pocket residues (F87/F91/F94/H95) affecting CP55,940 — **related pocket validation**, not a direct Trp258 mutagenesis of the MRI pair itself. |
| **(2) Author-proposed** | Arm-1 length/bulk differentially engages **Trp2586.48** toggle; 2687 confines inactive rotamer; 2594 does not. |
| **(3) Computational** | Docking of both ligands into AM10257-bound CB2; 200 ns MD of Trp258 rotamer (Fig. S6). |
| **(4) Unknown** | Direct co-crystal of MRI2687 or MRI2594 with CB2: **NOT FOUND**. |

### H. Quality

**A** — Matched designed pair; quantitative functional parameters both arms; structural receptor context; synthesis characterized. Deduction from “perfect”: docking/MD for pose; single assay modality (β-arrestin2) for the switch figure; not multi-pathway panel like the HU paper.

### I. Individual conclusion

**YES** — this pair shows we can **predictably modulate CB2 phenotype (ago ↔ inv/ant)** via **arm-1 / central-heterocycle bulk** toward the Trp6.48 region on this thiazole chemotype.  
**NO** — it does **not** show predictable dual Yin-Yang (CB1-ant + CB2-ago) modulation: CB1 stays agonist-class.

**Survives as Class A?** **YES** (for mono-CB2 function switch, as in the SMRF matrix).

---

## Pair 2 — HU-308 → (R)-1

### A. Identification

| Item | Evidence |
|------|----------|
| Names | Parent agonist **HU-308**; inverse agonists **(S)-1** / **(R)-1**; matched agonist control **ago-3** (same scaffold as (S)/(R)-3 **minus** C(2′) phenyl). |
| SMILES | **NOT FOUND** as SMILES in PMC full text. Structures given as schemes/figures. |
| Primary ref | Kosar, Sarott, … Frank, Grether, Carreira, *ACS Cent. Sci.* **10**, 956–968 (2024). DOI **10.1021/acscentsci.3c01461**. PMC **PMC11117691**. |
| Year | **2024** (published online 2024-03-11) |
| Lab | **Carreira / Frank** (ETH Zurich chemistry/probe design) with **Grether** (Roche) and collaborators (Hua, Veprintsev, et al.). |

### B. Structural change

**Claimed switch modification:** add **phenyl at C(2′)** of the gem-dimethylheptyl side chain (new stereocenter; *R* preferred).

**HU-308 → (R)-1 is NOT single-change.** ALL differences vs HU-308 stated by authors:

1. **C(2′) phenyl** (switch claim).  
2. **Terminal azide** inserted on the side chain.  
3. **Allylic alcohol → amine** (for conjugation / affinity-selectivity from prior work).

**Clean single-region matched pair in the same paper:** **ago-3 → (R)-3 / (S)-3** — “same scaffold … except that it lacks the C(2′) phenyl substituent” (eq 1). That is the experimental isolation of the phenyl as the functional flip.

### C. CB1 assays / results (no conversion)

Focus is CB2 selectivity. For fluorescent derivatives of the platform (Table 1, 37 °C TR-FRET): e.g. (R)-2 Kd CB2 18.9 nM vs CB1 1740 nM (92-fold); (R)-9 25.9 vs 7050 nM (272-fold).  
**(R)-1 CB1 functional ago/ant panel:** **NOT FOUND** as a dedicated CB1 cAMP/BRET phenotype table comparable to CB2 Table 3.  
HU-308 historically CB2-selective agonist (cited). **No claim that the phenyl creates CB1 antagonism.**

### D. CB2 assays / results (no conversion)

**cAMP HTRF** (hCB2-CHO; Table 3; norm CP-55,940 = 100%, basal = 0% unless noted):

| Probe | pEC50 | Emax (%) | Phenotype |
|-------|-------|----------|-----------|
| **ago-3** (no C2′ Ph) | **8.47** | **+112** | **agonist** |
| **(R)-1** | **6.95** | **−44** | **inverse agonist** |
| (S)-1 | 5.57 | −44 | inverse agonist |

**Gi-CASE BRET** (Table 4): (R)-1 pEC50 **6.80**, Emax **−28%** (inv).  
**β-arrestin BRET:** (R)-1 / (S)-1 / (R)-3 / (S)-3 — **no recruitment** (baseline); HU-308/HU-210 recruit.  
**ERK / Ca2+:** probes do not activate (live-cell panels).  
**Binding:** (R)-1 Kd **39.1 nM** (TR-FRET); kinetic Kd 11.6 nM (Table 2).  

Multiple fluorescent conjugates retain inverse profile → **within-series reproduction**.

### E. Comparability

**HIGH** for the phenyl-isolated contrast **ago-3 vs (R)-series** (same lab; cAMP + Gi BRET + arrestin + live-cell).  
For literal **HU-308 vs (R)-1**: **MEDIUM** — multi-change (phenyl + azide + alcohol→amine); phenotype direction still clear, but single-variable attribution requires ago-3.

### F. Functional change type

**CB2 agonist → CB2 inverse agonist** (efficacy sign flip in cAMP/Gi; not mere activity loss). Multi-pathway non-activation (arrestin/ERK/Ca2+) supports inv/ant, not silent binder.  
**Not a CB1/CB2 dual opposite (Yin-Yang) switch.**

### G. Mechanism (tiered)

| Tier | Content |
|------|---------|
| **(1) Experimentally demonstrated** | Functional ago→inv upon C(2′) phenyl (ago-3 vs phenyl series); multi-assay; CB2-selective binding; crystal structures of **HU-308–CB2 active (8GUS)** and **AM10257–CB2 inactive (5ZTY)** used as experimental structural context for design. |
| **(2) Author-proposed** | C(2′) phenyl engages **Trp2586.48**, restricting toggle motion / stabilizing inactive state. |
| **(3) Computational** | Docking of (R)-1 into 5ZTY; MD of (S)-3/(R)-3 vs ago-3 corroborating phenyl–Trp engagement. |
| **(4) Unknown** | Co-crystal of (R)-1 with CB2: **NOT FOUND**. |

### H. Quality

**A** — Strongest multi-assay functional flip in the A set; matched ago-3 control isolates phenyl; series reproduction with probes. Deduction: HU-308→(R)-1 itself is multi-mod; Trp mechanism remains docking/MD-supported rather than co-crystal/(R)-1 mutagenesis.

### I. Individual conclusion

**YES** — this case shows we can **predictably flip CB2 phenotype ago → inv/ant** by **installing bulk (phenyl) toward the Trp6.48 secondary pocket** on the HU-308 cannabilactone/pinene scaffold, **when compared via the matched ago-3 control**.  
**NO** — literal HU-308→(R)-1 is not a pure single-edit pair; **NO** evidence here for dual CB1-ant/CB2-ago Yin-Yang from this modification.

**Survives as Class A?** **YES** (mono-CB2 function switch; use ago-3 as the fair matched agonist for the phenyl claim).

---

## Final table

| Par | Cambio estructural | CB1 | CB2 | Tipo de cambio funcional | Comparabilidad | Mecanismo experimental | Evidencia | ¿Switch demostrado? |
|-----|--------------------|-----|-----|--------------------------|----------------|------------------------|-----------|---------------------|
| MRI2687 ↔ MRI2594 | Arm-1: 4,5-dimethylthiazole ↔ 6-methylbenzothiazole (shared cyclopropane-imino + ethyl acetate) | Both ago (2594 full fold; 2687 partial); β-arrestin2 EC50 310 nM / 114 nM | 2594 ago (EC50 0.17 nM, Emax 2.0); 2687 inv (EC50 0.24 nM, Emax 0.75) | CB2 ago ↔ inv/ant; CB1 stays ago-class | HIGH (same assay/lab) | Functional pair + 5ZTY pocket context; Trp pose = docking/MD (not exp. co-crystal of MRI) | A | **YES** (mono-CB2); **NO** Yin-Yang dual |
| HU-308 → (R)-1 (fair: ago-3 → phenyl series) | Add C(2′) phenyl; HU-308→(R)-1 also azide + allylic OH→NH2 | CB2-selective; no CB1 ant switch shown | ago-3: cAMP pEC50 8.47, Emax +112%; (R)-1: pEC50 6.95, Emax −44%; Gi inv; no β-arrestin | CB2 ago → inv/ant (sign-flip) | HIGH for ago-3 pair; MEDIUM for multi-change HU-308→(R)-1 | Multi-assay phenotype + 8GUS/5ZTY context; Trp mechanism docking/MD | A | **YES** (mono-CB2 via phenyl); **NO** Yin-Yang dual |

---

## Answers 1–7

1. **Does MRI2687/MRI2594 survive as A?**  
   **YES** — for **mono-CB2** ago↔inv/ant driven by arm-1 bulk. Not as a Yin-Yang dual SAR pair.

2. **Does HU-308/(R)-1 survive as A?**  
   **YES** — for **mono-CB2** ago→inv, with **ago-3** as the fair single-region control. Label the multi-change HU-308→(R)-1 carefully.

3. **What do both cases really share?**  
   - Experimental **CB2 efficacy-mode flips** (ago ↔ inv/ant), not just potency loss.  
   - Design narrative centered on **bulk near Trp2586.48** (CWxP toggle), informed by **CB2 inactive structure 5ZTY**.  
   - Matched / near-matched chemotypes within one lab paper.  
   - Mechanism of Trp engagement is **author-proposed + computational**, with experimental functional readout.

4. **What do they NOT share?**  
   - Scaffold (thiazole vs HU-308 cannabilactone/pinene).  
   - Exact chemical edit (heterocycle fusion vs C2′ phenyl).  
   - Assay panels (β-arrestin2-centric vs cAMP/Gi/arrestin/ERK/Ca2+).  
   - CB1 outcome (MRI: both CB1 agonists; HU series: CB2-selective, no dual opposite).  
   - Neither is a demonstrated **CB1-ant + CB2-ago** Yin-Yang structural rule.

5. **Can we already claim a general molecular switch?**  
   **NO** — not a universal “one modification → predictable CB1/CB2 dual phenotype” law. What is supported: **local bulk toward Trp6.48 can flip CB2 ago↔inv across ≥2 scaffolds** (restricted mono-receptor claim). Dual Yin-Yang remains **separate / not established by these A pairs**.

6. **What experiment / historical data would elevate evidence?**  
   - Co-crystal or cryo-EM of **MRI2687 / MRI2594** and **(R)-1 / ago-3** with CB2.  
   - Direct **Trp258** mutagenesis with these exact ligands (functional rescue/collapse).  
   - Same multi-pathway panel on the MRI pair (cAMP + Gi + arrestin).  
   - Independent lab replication.  
   - Explicit single-edit HU-308 ± C2′ phenyl without azide/amine confounders.  
   - For dual claims: matched pairs that flip **CB1 and CB2 in opposite directions** with open potencies (out of scope of these two A pairs).

7. **Expand 0Q or close hypothesis?**  
   **Expand 0Q** — keep A-pairs as mono-CB2 toggle evidence; split claims (mono-CB2 Trp-bulk vs dual Yin-Yang); continue historical matrix on Janus B/C pairs. **Do not close** the mono-CB2 switch hypothesis; **do not promote** it to a general CB1/CB2 dual switch.

---

## Recommendation (mandatory)

### **EXPAND**

- **Keep** both pairs as **Class A** for **mono-CB2** ago↔inv/ant.  
- **Expand** 0Q framing: separate (i) Trp6.48-linked CB2 efficacy switch from (ii) Yin-Yang dual CB1/CB2.  
- **Do not KILL** — experimental switches are real.  
- **Do not** change global **`0Q-SMRF = MODERATE`** in this 0Q.1 step.

---

## Paths

| Item | Path |
|------|------|
| This audit | `results/reports/qiu_0q1_primary_audit_A_pairs.md` |
| Parent matrix | `results/reports/qiu_0q_smrf_matrix.md` |
| Pairs CSV | `results/reports/qiu_0q_smrf_pairs.csv` |

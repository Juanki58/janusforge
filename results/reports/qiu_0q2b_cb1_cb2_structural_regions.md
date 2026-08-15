# 0Q.2b — CB1 vs CB2 structural regions map (experimental structures)

**Fecha:** 2026-08-15  
**Workstream:** Literature / structure inventory only (no NCE, no mass docking, no MD execution)  
**Prior locks (unchanged):** `0Q-SMRF = MODERATE`; `0Q.1-FINAL = EXPAND` (Class-A = **mono-CB2 only**, not Janus); `0Q.2 / 0Q.2-v2 = WEAK` for structural Janus ON/OFF (**0 Class-A Janus pairs**); `0M = FROZEN`  
**Evidence tags used throughout:** **EXPERIMENTAL** | **COMPUTATIONAL** | **INFERRED / AUTHOR-PROPOSED** | **NOT FOUND**

**Success question:** Can a **common structural region** be identified that (1) differentiates CB1 from CB2 experimentally and (2) is compatible with the functional switches documented in 0Q.1 / 0Q.2?

---

## Executive answer

| Question | Verdict |
|----------|---------|
| Regions that **experimentally differentiate** CB1 vs CB2 (selectivity / pocket geometry / ligand-dependent activation)? | **YES** — several (best: **Leu/Val6.51**; **ECL2** sequence/contacts; **inactive-pocket volume / N-term packing** from paired structures) |
| Region that hosts **0Q.1 Class-A mono-CB2 ago↔inv** switches? | **YES (with caveat)** — authors converge on **Trp6.48** / arm-1 bulk; phenotype = **EXPERIMENTAL**; Trp contact for MRI/(R)-1 = **AUTHOR-PROPOSED + COMPUTATIONAL**; Trp is **conserved** CB1↔CB2 (not a sequence differentiator) |
| Region that hosts **Janus** (CB2-ago + CB1-ant/inv) with experimental structural/mutagenesis closure? | **NOT FOUND** for any audited Janus ligand |
| **Common region** that can mechanistically host **both** (a) mono-CB2 ago↔inv **and** (b) dual Janus? | **INSUFFICIENT** — and current evidence treats them as **different phenomena** |
| Explicit: can a common differentiating region be identified **for Janus control**? | **INSUFFICIENT** |

**Bottom line:** CB1/CB2 discrimination has experimental structural anchors; 0Q.1 efficacy flips have a credible CB2 toggle narrative (Trp6.48) that is **not** a CB1≠CB2 sequence difference and **does not** produce Janus in those Class-A pairs. Janus remains a **functional phenotype without a closed experimental structural locus**.

---

## 1. Inventory — key experimental CB1 / CB2 structures (through 2026)

Source: RCSB Search API `reference_sequence_identifiers` = UniProt **P21554** (CB1) / **P34972** (CB2), `results_content_type = experimental`, queried 2026-08-15.  
Counts: **CB1 = 34** entries; **CB2 = 14** entries (includes NMR fragments and peptide-only constructs).

### 1.1 CB2 — full-receptor experimental complexes (priority)

| PDB | Method | Res. (Å) | Ligand (CCD / common) | State (ligand class) | Primary paper / DOI | Year |
|-----|--------|----------|------------------------|----------------------|---------------------|------|
| **5ZTY** | X-ray | 2.8 | **9JU = AM10257** | **Inactive** (CB2 ant/inv) | Li/Hua et al. *Cell* [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011) | 2019 |
| **6KPC** | X-ray | 3.2 | AM-series agonist (paper: AM12033 lineage) | **Active-like** (agonist-bound crystal) | Hua et al. *Cell* [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008) | 2020 |
| **6KPF** | cryo-EM | 2.9 | same paper agonist + **Gi** | **Active** | same | 2020 |
| **6PT0** | cryo-EM | 3.2 | **WI5 = WIN 55,212-2** + Gi | **Active** | Xing et al. *Cell* [10.1016/j.cell.2020.01.007](https://doi.org/10.1016/j.cell.2020.01.007) | 2020 |
| **8GUQ** | cryo-EM | 3.08 | **KNF = Olorinab (APD371)** + G | **Active** | Li/Hua/van der Stelt *Nat Commun* [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9) | 2023 |
| **8GUR** | cryo-EM | 2.84 | **9GF = CP55,940** + G | **Active** | same | 2023 |
| **8GUS** | cryo-EM | ~3.0 | **HU-308** + G | **Active** | same | 2023 |
| **8GUT** | cryo-EM | 2.98 | **KO8 = LEI-102** + Gi | **Active** | same | 2023 |
| **8X3L** | cryo-EM | 3.13 | **XWD** (CB2-selective ago) + G | **Active** | Shen et al. *PNAS* [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121) | 2024 |
| **9U7L** | cryo-EM | 3.2 | CP55,940 + **PAM Ec21a (A1EOL)** | **Active + PAM** | Wang et al. *Nat Commun* [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6) | 2026 |
| **12IY / 12IZ / 12JA** | cryo-EM | 2.7–2.9 | agonists **'5249** / **'1029** (CCD A1DB5/A1DB6) | **Active** | *J. Med. Chem.* [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835) | 2026 |
| **2KI9** | NMR | — | TM6 peptide fragment | fragment only | 2009 | — |

**Local repo anchors:** `data/targets/cb2/6PT0*` (WIN–CB2–Gi); API cache `data/papers/qiu_2023_bioorg/api/external0p/pdb_5zty.json`.  
**Critical prior correction (0Q audit):** **8F7V is not CB2** (plasmin inhibitor).

### 1.2 CB1 — key full-receptor experimental complexes

| PDB | Method | Res. (Å) | Ligand | State | Primary DOI | Year |
|-----|--------|----------|--------|-------|-------------|------|
| **5TGZ** | X-ray | 2.8 | **AM6538** (antagonist; local prep ligand ZDG/AM6538 family) | **Inactive** | Hua et al. *Cell* [10.1016/j.cell.2016.10.004](https://doi.org/10.1016/j.cell.2016.10.004) | 2016 |
| **5U09** | X-ray | 2.6 | **Taranabant (7DY)** | **Inactive** (inv ago) | Shao et al. *Nature* [10.1038/nature20613](https://doi.org/10.1038/nature20613) | 2016 |
| **5XR8** | X-ray | 2.95 | **AM841** | **Active-like** (ago crystal) | Hua et al. *Nature* [10.1038/nature23272](https://doi.org/10.1038/nature23272) | 2017 |
| **5XRA** | X-ray | 2.8 | **AM11542 (8D3)** | **Active-like** | same | 2017 |
| **6N4B** | cryo-EM | 3.0 | **MDMB-Fubinaca (KCA)** + Gi | **Active** | Krishna Kumar et al. *Cell* [10.1016/j.cell.2018.11.040](https://doi.org/10.1016/j.cell.2018.11.040) | 2019 |
| **6KPG** | cryo-EM | 3.0 | agonist + Gi (Hua 2020) | **Active** | [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008) | 2020 |
| **6KQI** | X-ray | 3.25 | **CP55,940 (9GF)** + NAM **ORG27569 (9GL)** | ago + allosteric | Shao et al. *Nat Chem Biol* [10.1038/s41589-019-0387-2](https://doi.org/10.1038/s41589-019-0387-2) | 2019 |
| **7V3Z** | X-ray | 3.29 | **CP55,940** | ago crystal | Wang et al. *JACS* [10.1021/jacs.1c06847](https://doi.org/10.1021/jacs.1c06847) | 2021 |
| **7FEE / 7WV9** | X-ray / cryo-EM | 2.7 / 3.36 | CP55,940 + **ZCZ011 (7IC)** PAM | ago ± PAM ± Gi | Yang et al. *Nat Chem Biol* [10.1038/s41589-022-01038-y](https://doi.org/10.1038/s41589-022-01038-y) | 2022 |
| **8GHV** | cryo-EM | 2.8 | **2-AG analog (ZI5)** + Gi | **Active** | [10.1038/s41467-023-37864-4](https://doi.org/10.1038/s41467-023-37864-4) | 2023 |
| **8WU1 / 8WRZ** | cryo-EM | 3.2 / 3.6 | Fubinaca lineage / arrestin complexes | active / β-arr | *Cell* / *Protein Cell* 2023–24 | |
| **9B9Y/Z / 9BA0** | cryo-EM | 3.1–3.5 | taranabant / peripheral & biased inverse agonists | **Inactive / inv** | [10.1038/s41467-024-54206-0](https://doi.org/10.1038/s41467-024-54206-0) | 2024 |
| **9B54 / 9B65** | cryo-EM | 2.86 / 3.03 | biased ago + Gi | **Active** | *Nature* [10.1038/s41586-025-08618-7](https://doi.org/10.1038/s41586-025-08618-7) | 2025 |
| **23IV / 23IW** | cryo-EM | 2.42 | novel indazole agonists + Gi | **Active** | *Cell* [10.1016/j.cell.2026.03.020](https://doi.org/10.1016/j.cell.2026.03.020) | 2026 |

**Local repo anchor:** `data/targets/cb1/5TGZ*` (inactive CB1; chimera caveats documented in prior MD reports).

**NOT FOUND (relevant to this program):** co-crystal / cryo-EM of **MRI2687, MRI2594, (R)-1 / ago-3, Qiu-14, URB447, GW405833, AM1710, Vasiljevik-27/30** with CB1 or CB2.

---

## 2. BW / common-position map — orthosteric pocket & activation motifs

Human numbering from UniProt **P21554** (CB1) / **P34972** (CB2); BW from primary structure papers (Hua/Li *Cell*/*Nature*; Xing *Cell* 2020; Li *Nat Commun* 2023) and comparative reviews citing the same coordinates.

### 2.1 Conserved orthosteric / toggle positions (same AA class CB1≈CB2)

| BW | CB1 | CB2 | Role (literature type) |
|----|-----|-----|------------------------|
| 2.57 | F170 | F87 | Aromatic lid; mutagens affect CP55,940 (**EXPERIMENTAL** mut: Li *Cell* 2019 Fig. 3C F87A EC50 shift) |
| 2.60 | S173 | S90 | Polar contact site; Qiu H-bond claim for **14** = **COMPUTATIONAL** only |
| 2.61 / 2.64 / 2.65 | F174 / F177 / H178 | F91 / F94 / H95 | Arm-3 / TM2 aromatic cluster; CB2 mutagens F91/F94/H95 impair CP55,940 (**EXPERIMENTAL**, Li 2019) |
| 3.32 | V196 | V113 | Hydrophobic core contact |
| 3.36 | F200 | F117 | Twin-toggle latch with Trp6.48 in CB1 (**EXPERIMENTAL** structures 5XR8/5XRA); CB2 activation involves F117–W258 rearrangement (**EXPERIMENTAL** 5ZTY vs 6PT0) |
| 5.39 / 5.43 | Y275 / W279 | Y190 / W194 | Pocket floor / aromatic |
| **6.48** | **W356** | **W258** | **Toggle**; confined rotamer in CB2–AM10257 (**EXPERIMENTAL** 5ZTY); bulk toward Trp proposed for MRI/(R)-1 (**AUTHOR + COMP**) |
| 7.35 / 7.39 / 7.42 | F379 / S383 / C386 | F281 / S285 / C288 | TM7 wall; S7.39 H-bond to many classical agonists (**EXPERIMENTAL** contacts in CP/HU structures; mutagenesis literature) |

### 2.2 Sequence-divergent positions with experimental functional weight

| BW / loop | CB1 | CB2 | CB1 vs CB2 difference | Published function |
|-----------|-----|-----|----------------------|--------------------|
| **3.29** | **L193** | **I110** | Leu ↔ Ile (conservative size) | Ala mut CB1 ↓ agonist affinity (**EXPERIMENTAL** Shim/McAllister lineage); reciprocal chemotype selectivity mutagens in recent isomer work (**EXPERIMENTAL**, see §5) |
| **6.51** | **L359** | **V261** | γ-branched Leu ↔ β-branched Val | Reciprocal mutagens reverse THC cAMP efficacy CB1↔CB2 (**EXPERIMENTAL** Llinàs del Torrent *JCIM* 2023 [10.1021/acs.jcim.3c01054](https://doi.org/10.1021/acs.jcim.3c01054)); MD mechanism = **COMPUTATIONAL** |
| **ECL2** | F268, I267, … | F183, L182, … | Loop sequence + local packing differ; F* conserved as aromatic lid | F268A CB1 / F183 mut CB2 abolish or severely impair binding (**EXPERIMENTAL** Ahn 2009; Feng 2014); ECL2 energy contribution in GW405833 docking (**COMPUTATIONAL**, Xing *Cell* 2020) |
| N-term / pocket volume | long N-term can occupy inactive CB1 pocket | short N-term helix outside pocket | Inactive CB1 pocket ~**822 Å³** vs CB2 ant ~**447 Å³** ≈ CB1 ago ~**384 Å³** | **EXPERIMENTAL** volumes from Hua/Li structures (5TGZ vs 5ZTY vs 5XRA) |

**INFERRED (do not elevate):** overall “CB1 larger / CB2 narrower” as a universal Janus design rule — volumes are **state- and ligand-dependent**, not a single static cavity.

---

## 3. 0Q.1 switches — what authors claimed (tiered)

### 3.1 MRI2687 ↔ MRI2594 (*Cell* 2019; PDB context **5ZTY**)

| Claim | Tag |
|-------|-----|
| CB2: 2594 agonist ↔ 2687 inverse (β-arrestin2) | **EXPERIMENTAL** |
| CB1: both agonist-class (full ↔ partial) | **EXPERIMENTAL** |
| Arm-1 bulk engages **Trp2586.48** to confine inactive rotamer | **AUTHOR-PROPOSED** + **COMPUTATIONAL** (docking into AM10257 pocket; MD of Trp rotamer) |
| Direct MRI–CB2 co-crystal | **NOT FOUND** |
| Mutagenesis of Trp258 with MRI ligands | **NOT FOUND** (paper mutagens F87/F91/F94/H95 validate AM10257 pocket for CP55,940 — related, not MRI-specific) |
| Yin-Yang CB1-ant + CB2-ago from this edit | **NO** (locked 0Q.1-FINAL) |

### 3.2 HU-308 / ago-3 → (R)-1 phenyl (*ACS Cent. Sci.* 2024; context **8GUS** active / **5ZTY** inactive)

| Claim | Tag |
|-------|-----|
| C(2′) phenyl flips CB2 ago → inv (ago-3 control; cAMP/Gi) | **EXPERIMENTAL** |
| CB1 antagonism from phenyl | **NOT shown** (CB2-selective platform) |
| Phenyl engages **Trp2586.48** | **AUTHOR-PROPOSED** + **COMPUTATIONAL** (docking/MD) |
| (R)-1–CB2 co-crystal | **NOT FOUND** |

**Shared 0Q.1 motif:** local **bulk toward conserved Trp6.48** on CB2 → mono-receptor efficacy mode switch. **Not** a CB1≠CB2 residue difference; **not** Janus.

---

## 4. Janus ligands — experimental structural / mutagenesis link to CB1 vs CB2?

| Ligand | Dual phenotype (0Q.2) | Experimental co-structure CB1/CB2 | Experimental mutagens for Janus mechanism | Structural discrimination claim in primary lit |
|--------|----------------------|-----------------------------------|-------------------------------------------|-----------------------------------------------|
| **URB447** | CB2 ago + CB1 neutral ant | **NOT FOUND** | **NOT FOUND** | Authors: peripheral restriction / SAR — **no pocket residue map** |
| **GW405833** | CB2 ago (legacy/protean caveats) + CB1 noncomp. ant (Mackie 2017) | **NOT FOUND** | **NOT FOUND** for Janus arms | Xing *Cell* 2020: **docking** vs active CB2 / inactive CB1 **5TGZ**; residual energy → ECL2 / W6.48 narrative = **COMPUTATIONAL** |
| **AM1710** | CB2 ago + low-pot. CB1 ant/inv | **NOT FOUND** | **NOT FOUND** | Functional Janus only (JPET 2017); no structure |
| **Qiu-14** | CB2 ago + CB1 ant (cAMP direction) | **NOT FOUND** | **NOT FOUND** | S173 / S285 H-bonds = **COMPUTATIONAL** (docking/MD); conserved Ser≠selectivity residue |
| **Vasiljevik-27/30** | CB2 ago + CB1 neutral ant | **NOT FOUND** | **NOT FOUND** | SAR / AC assays only; C3 naphthyl geometry — **no receptor residue assignment** |

**Verdict:** for Janus, all audited structural “explanations” are **COMPUTATIONAL or absent**. No experimental residue can yet be labeled “the Janus discrimination site.”

---

## 5. Candidate regions table (deliverable core)

| Region | Residues (BW + human) | CB1 vs CB2 difference | Link to published function | Compatible with 0Q.1 switches? | Compatible with Janus? | Confidence | Sources |
|--------|----------------------|----------------------|----------------------------|--------------------------------|------------------------|------------|---------|
| **Toggle Trp6.48 / twin F3.36** | CB1 W356<sup>6.48</sup> + F200<sup>3.36</sup>; CB2 W258<sup>6.48</sup> + F117<sup>3.36</sup> | **Sequence conserved**; **mechanism differs** (CB1 twin latch vs CB2 Trp confinement by ant arm-1) | Activation / inactive lock; MRI & (R)-1 bulk narrative | **YES** for mono-CB2 ago↔inv (phenotype EXP; pose COMP); **NO** Yin-Yang in A pairs | **INSUFFICIENT** — conserved AA cannot explain opposite dual arms; GW405833 Trp story = docking | **HIGH** for activation physics; **LOW** for CB1≠CB2 sequence discrimination; **LOW** for Janus | 5ZTY, 5XR8/5XRA, 6PT0; Li *Cell* 2019; Hua *Nature* 2017; 0Q.1 audits |
| **Position 6.51** | CB1 **L359**; CB2 **V261** | **Leu ↔ Val** | Reciprocal mutagens flip THC efficacy CB1↔CB2 | **Partial / unknown** — adjacent to Trp toggle; **not** claimed by MRI/HU authors for their switches | **INSUFFICIENT** — no Janus ligand mutagens at 6.51 | **HIGH** for CB1/CB2 *activation* discrimination (THC/JWH-133); **INSUFFICIENT** for Janus control | Llinàs del Torrent *JCIM* 2023; structures show both side chains in pocket |
| **ECL2 aromatic lid** | CB1 F268 (+ I267 etc.); CB2 F183 (+ L182 etc.) | Loop sequence **divergent**; Phe lid conserved | Mutagens abolish binding; docking energy for GW405833 | Unlikely primary for arm-1 Trp bulk flips | **INSUFFICIENT** — GW405833 ECL2 argument = **COMP** only | **MEDIUM–HIGH** for binding/selectivity; **LOW** for Janus | Ahn 2009; Feng 2014; Xing *Cell* 2020 (COMP for GW) |
| **TM3 3.29** | CB1 **L193**; CB2 **I110** | Leu ↔ Ile | Affinity / isomer selectivity mutagens | Not claimed by 0Q.1 A pairs | **INSUFFICIENT** | **MEDIUM** for selectivity; **LOW** Janus | Shim/McAllister; Frontiers 2026 comparative table; recent isomer mutagens |
| **Inactive pocket volume / N-term packing** | Global orthosteric cavity | CB2–AM10257 pocket ≈ CB1–ago pocket ≪ CB1–ant pocket | Explains many ant selectivity patterns; AM10257 = CB2 inv + CB1 partial ago (**EXPERIMENTAL** opposite dual — **not** Janus) | Compatible with why CB2 ant pocket is “ago-like” for CB1 — **explains opposite dual**, not Janus | **NO / misleading** if used as Janus rule (predicts CB2-ant/CB1-ago more than CB2-ago/CB1-ant) | **HIGH** as structural observation; **LOW** as Janus host | Li *Cell* 2019 volumes; Hua CB1 structures |
| **TM2 aromatic cluster (2.57–2.65)** | F/H cluster conserved | Mostly conserved | Mutagens impair CB2 ligand potency (EXP) | Peripheral to Trp arm-1 story | **INSUFFICIENT** | **MEDIUM** for binding; **LOW** Janus | Li *Cell* 2019 mutagens |
| **Ser2.60 / Ser7.39** | S173/S383; S90/S285 | **Conserved** Ser | Classical agonist H-bonds (EXP contacts); Qiu Janus H-bonds | Not the 0Q.1 switch locus | **NO experimental link** for Qiu-14; claim = **COMP** | **HIGH** as conserved contact; **INSUFFICIENT/reject** as CB1≠CB2 Janus discriminator | Structures 8GUR/8GUS etc.; Qiu abstract/SI |
| **Aminoalkylindole C3 / naphthyl SAR (ligand side)** | n/a (ligand region) | n/a | Vasiljevik CB1 ago→neutral ant while CB2 ago retained (**EXPERIMENTAL** func) | Different chemotype from MRI/HU | Suggests Janus can arise from **ligand geometry**, not a proven shared receptor microdomain | **MEDIUM** for phenotype existence; **LOW** for mapped receptor region | Vasiljevik *JMC* 2013; 0Q.2-v2 |

---

## 6. Are mono-CB2 switches and Janus the same phenomenon?

| Comparison | Mono-CB2 (0Q.1 Class A) | Janus (0Q.2 Class B anchors) |
|------------|-------------------------|------------------------------|
| Phenotype | CB2 ago ↔ inv; CB1 stays ago or is unused | CB2 **ago** + CB1 **ant/inv** |
| Best structural narrative | Bulk → **conserved Trp6.48** on CB2 | **No closed experimental locus** |
| CB1 outcome of “same” bulk logic | MRI: still CB1 ago; HU: CB2-selective | Requires **opposite** CB1 efficacy relative to CB2 |
| Class-A structural switch pairs | **2** (mono-CB2) | **0** |
| Mechanistic identity? | — | **No evidence they share one differentiating region** |

**INFERRED (labeled):** Trp6.48 bulk that **inactivates CB2** is the wrong directional logic for **CB2 agonism** half of Janus; any shared “toggle region” story would need **receptor-asymmetric** coupling (different CB1 vs CB2 consequences of the same pose) — currently **COMPUTATIONAL speculation**, contradicted by MRI CB1 remaining agonist-class.

---

## 7. Explicit answers

1. **Can a common differentiating region be identified for Janus control?**  
   **INSUFFICIENT.**

2. **Top candidate regions (ranked for this program’s questions):**  
   - **For CB1≠CB2 experimental discrimination:** **Leu/Val6.51** (HIGH); **ECL2** (MEDIUM–HIGH); **inactive pocket volume / N-term** (HIGH observation, wrong sign for Janus).  
   - **For 0Q.1 mono-CB2 switches:** **Trp6.48 / arm-1 bulk** (HIGH phenotype; MEDIUM mechanism pending co-crystal/mutagen).  
   - **For Janus control:** **none with experimental residue closure** — best literature hints remain ligand SAR (Vasiljevik C3; URB N1-benzyl) without receptor locus.

3. **Do mono-CB2 and Janus share a host region?**  
   **INSUFFICIENT / effectively different phenomena** on current evidence. Do **not** promote Trp6.48 Class-A findings as a Janus structural switch (locked 0Q.1-FINAL / 0Q.2).

---

## 8. What remains unknown

- Co-structures of any Janus tool (URB447, GW405833, AM1710, Qiu-14, Vasiljevik-27/30) with CB1 **and** CB2 in matching functional states.  
- Direct mutagenesis of **W6.48**, **L/V6.51**, or **ECL2** with **matched Janus / non-Janus** ligand pairs.  
- Whether Qiu ortho-morpholine “switch” maps to any divergent residue (S173/S285 are conserved → weak CB1≠CB2 discriminator even if H-bonds were real).  
- Whether Gerasi/Makriyannis dual CB1-ant/CB2-ago minimal-mod pairs (thesis embargo to 2027) will supply Class-A structural evidence.  
- Pathway-level Janus (arrestin vs G) for several anchors (GW/AM1710 ambiguity) — orthogonal to pocket residue ID.

---

## 9. Locks / non-actions

| Item | Status |
|------|--------|
| Global `0Q-SMRF` | **MODERATE** (no change proposed) |
| 0Q.1 Class A | Remain **mono-CB2**; **not** reclassified Janus |
| 0Q.2 Janus structural switch | Remains **WEAK**; **0** Class-A pairs |
| NCE / docking / MD | **Not authorized** by this step |
| Claim “Janus structural switch = Trp6.48” | **REJECT** as experimental Class A |

---

## 10. Paths

| Deliverable | Path |
|-------------|------|
| This report | `results/reports/qiu_0q2b_cb1_cb2_structural_regions.md` |
| Parents | `qiu_0q1_final_cursor_vs_gemini.md`; `qiu_0q2_smrf_expand.md`; `qiu_0q2_smrf_expand_v2.md`; `qiu_0q_independent_scientific_audit.md` |

---

*End 0Q.2b. Inventory and residue map only; Janus control locus remains experimentally open.*

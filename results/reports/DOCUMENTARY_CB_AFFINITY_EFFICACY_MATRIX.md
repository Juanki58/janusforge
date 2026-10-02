# Matriz documental — afinidad / eficacia CB1–CB2 (corpus local)

**Fecha:** 2026-08-17  
**Rol:** Analista documental (no modelador)  
**Nombre del archivo:** `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md`  
**Nota de naming:** el framing *esterase / soft-drug* **no** describe el corpus recuperado (búsqueda local de `esterase` / `soft-drug` / `carboxylesterase` → vacío útil). Se nombra por contenido real: afinidad, eficacia, periferia, metabolito solo cuando aparece.

**Prohibiciones respetadas:** sin docking/MD/QSAR; sin inventar números; sin convertir cualitativo → %; Ki ≠ IC50 ≠ EC50; sin promoción Gold; **PIPELINE = STOP**.

---

## 1. Scope note (fuentes locales usadas)

| Bloque | Paths / piezas |
|--------|----------------|
| Docs janusforge | `docs/mapa_ligandos_janus_cb1_cb2.md`, `docs/literatura_prioridad_y_novelty.md`, `docs/literatura_fibrosis_cb1_cb2.md`, `docs/quimioma_cannabico_cb1_cb2.md`, `docs/criterio_exito_janus.md` |
| Round1 evidence | `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md`, `ROUND1.5`–`1.8`, `ROUND1_ORDEN2` / `ORDEN4`, `ROUND1.1_CERTIFICATION_*`, `CB2_Experimental_Master_Dataset_v1.0_Round1*.md`, `qiu_0q_smrf_matrix.md` |
| SI / extracts Qiu | `data/papers/mmc1_document.txt`, OCR SI (`image*_ocr.txt`), `results/reports/qiu_0q_*` |
| Primarios / abstracts en disco | Valenzano abstract (`data/papers/_recon_tmp/orden4_pubmed_abs.txt`); Khanolkar abstract (via Round1.5/ORDEN2); Hanuš extract (`hanus_epmc_extract.txt`); Dhop Table 2 HTML (`dhop_table2.html`); Vicasinabin Frontiers extract; Han 2017 extract; Vasiljevik 2013 PMC HTML; Soethoudt extract (PK half-life context only) |

**No se usó:** nueva campaña bibliográfica; ChEMBL/vendor como sustituto Gold (solo se anota PARTIAL/HOLD cuando Round1 ya lo documentó).

**Convenciones de celda:** `NOT_REPORTED` = paper/local extract no da el dato; `NOT_IN_LOCAL_CORPUS` = no hay material local; `N/A` = columna no aplica al diseño/fenotipo; `PARTIAL/HOLD` = citado en docs/Round1 pero primario tabular no recuperado — **no Gold**.

---

## 2. Tabla consolidada

| paper | compound | modification | CB1 affinity | CB2 affinity | efficacy | esterase stability/deactivation | metabolite | metabolite activity | in vivo model | duration | key conclusion |
|-------|----------|--------------|--------------|--------------|----------|--------------------------------|------------|---------------------|---------------|----------|----------------|
| LoVerme 2009 *BMCL*; DOI `10.1016/j.bmcl.2008.12.059` (Round1.9; SMRF J1; mapa) | **URB447** | Diarylpyrrole; N1-*p*-Cl-benzyl + 4-NH₂ + 3-benzoyl (vs des-benzyl 5b / des-NH₂ 8a en serie) | Binding **IC50 313±72 nM** (**r**CB1); ≠ Ki. GTPγS ant **EC50 4.9±0.8 µM** (neutral ant; SMRF/LoVerme lineage) | Binding **IC50 41±23 nM** (**h**CB2); ≠ Ki | CB1: neutral antagonist (GTPγS). CB2: cAMP ↓ @ **1 µM** (**m**CB2 HEK) — **no EC50/Emax** | N/A (no soft-drug design in paper) | NOT_REPORTED | NOT_REPORTED | Metabolic / food intake; peripherally restricted (brain entry not appreciable — qualitative LoVerme/docs) | NOT_REPORTED (PK half-life) | First explicit **CB1-ant / CB2-ago** peripheral Janus; IC50≠Ki≠EC50; func CB2 qualitative mCB2 only (REVIEW, no Gold) |
| Valenzano 2005 *Neuropharmacology*; DOI `10.1016/j.neuropharm.2004.12.008` (abstract local; R1.6–1.9) | **GW405833** | Indole N-acyl; 2,3-dichlorobenzoyl + 5-OMe + morpholinoethyl (structure Fig.1 **NOT_VERIFIED** local PDF) | Binding: abstract “high affinity” **r/h** CB2 focus; numeric **h**CB1 Ki **NOT_VERIFIED** in recovered abstract (mapa cita rango lit. 1.9–4.8 µM — secondary map, not Valenzano table lock) | Abstract: selective high-affinity bind **r + h** CB2; numeric Ki/EC50 table **NOT_FOUND** (PDF unrecovered) | Forskolin cAMP: **partial agonist ≈50%** vs CP55,940 (**qualitative only**). Exact **14±2 nM / 48±4%** = **NOT_VERIFIED** | N/A | NOT_REPORTED | NOT_REPORTED | Rat pain models (neuropathic, incisional, inflammatory); CB2 KO loss of antihyperalgesia; i.p. 0.3–100 mg/kg | Abstract: linear plasma ↑; **substantial CNS penetration**; analgesia/sedation/catalepsy at **100 mg/kg** (not ≤30) | CB2-selective partial ago (~50%); CNS-penetrant; numeric EC50/Emax/structure **unlocked** → REVIEW |
| Dhopeshwarkar & Mackie 2016 *JPET* PMC4959096 Table 2 (local HTML; mix-check ≠ Valenzano) | **GW405833** | Same chemotype; **separate assay** | NOT_REPORTED in this table row | Functional **m**CB2 HEK cyclase/arrestin (not binding Ki) | Cyclase: Emax **0** (inactive); arrestin Emax **4±2.6** | N/A | NOT_REPORTED | NOT_REPORTED | NOT_REPORTED (this table) | N/A | **Do not pool** with Valenzano ~50% (species/assay diverge; R1.9 D5/U6) |
| Dhopeshwarkar et al. 2017 *JPET*; DOI `10.1124/jpet.116.236539` (mapa / SMRF J3 — Janus reanalysis) | **GW405833** | Phenotype re-read as Janus | Functional CB1 **antagonism** (noncompetitive; assay-dependent) — Ki map lit. **~1.9–4.8 µM** (docs; primary table not re-opened here) | CB2 ago (partial/protean lit.); Ki map **~4–12 nM** (docs) | CB1 ant + CB2 ago (multi-pathway) | N/A | NOT_REPORTED | NOT_REPORTED | NOT_IN_LOCAL_CORPUS (full 2017 PDF) | NOT_IN_LOCAL_CORPUS | Bifunctional ≠ URB447 mechanism; “Janus” experimental reanalysis |
| Khanolkar 2007 *J. Med. Chem.*; DOI `10.1021/jm070441u` (abstract only; R1.5/ORDEN2) | **AM1710** (= **4b**, 9-methoxy; **≠5a**; **5=AM1714**) | Cannabilactone / benzo[*c*]chromen-6-one; 9-OMe vs 9-OH (AM1714) | Claimed Ki **~360 nM**: **PARTIAL/HOLD** — Table 1 **NOT_FOUND** | Claimed Ki **~6.7 nM** / 54-fold CB2 sel.: **PARTIAL/HOLD** — Table 1 **NOT_FOUND**; abstract: 54-fold CB2 sel. **DIRECT** | Abstract: CB2 **agonists**; GTPγS **11.2±1.8 / 89±3%** ownership **NOT_FOUND** | N/A | NOT_REPORTED | NOT_REPORTED | Peripheral analgesia (**4b** and **5**) — abstract qualitative | NOT_REPORTED | Identity **4b=AM1710** locked; numeric Ki/EC50 Gold-unsafe until Tables 1–2 recovered |
| Dhopeshwarkar & Mackie 2016 Table 2 (local; HEK-**m**CB2) | **AM1710** | Same; **m**CB2 functional only | N/A (table = CB2 pathways) | Cyclase EC50 **11 nM** (CI 5.5–15.6); arrestin EC50 **4** (CI 1.6–7.1) | Cyclase Emax **48±4.3**; arrestin Emax **91±3.6** | N/A | NOT_REPORTED | NOT_REPORTED | NOT_REPORTED | N/A | Real numbers but **≠** Khanolkar hCB2 GTPγS; **≠** human Level-0/Gold |
| Qiu 2023 *Bioorg. Chem.*; DOI `10.1016/j.bioorg.2023.106377` + SI `mmc1_document.txt` Fig. S5 | **Qiu-14** | Pyrazole Yin-Yang; N1-Ph **ortho-morpholinyl** + C3 **1-adamantyl** amide | Func: CB1 **antagonist** cAMP/HTRF (ctrl rimonabant) — **IC50/Ki NOT FOUND OA** | Func: CB2 **agonist** cAMP/HTRF (ctrl CP55,940) — **EC50/Emax NOT FOUND OA** | Dual opposite **qualitative** only (n=3×triplicate curves) | N/A | NOT_REPORTED | NOT_REPORTED | NOT_REPORTED (fibrosis claim = potential only in docs) | NOT_REPORTED | Designed Yin-Yang; numeric potencies OA **NF**; S173/S285 = **computational only** (challenge/out of Gold) |
| Qiu 2023 SI Figs. S6/S11–S13 (OCR/SMRF) | **Qiu-15 / 16 / 20 / 24** | 15 *m*-morph; 16 *p*-morph; 20 *o*-4-Me-piperazinyl; 24 CH₂-adamantyl | Curves present; phenotype/IC50 **NOT FOUND OA** | Curves present; phenotype/EC50 **NOT FOUND OA** | Comparator Yin-Yang potencies **NOT FOUND** | N/A | N/A | N/A | NOT_REPORTED | NOT_REPORTED | Structural identities SI-verified; SAR numbers hypothesis-only → REJECT as fact |
| Hanuš 1999 *PNAS*; DOI `10.1073/pnas.96.25.14228` / PMC24419 (local extract) | **HU-308** | CB2-selective classical cannabinoid (Structure V) | Binding **Ki >10 µM** (does not bind CB1 efficiently) | Binding **Ki 22.7±3.9 nM** | cAMP forskolin **h**CB2 CHO: **EC50 5.57 nM** (95% CL 1.68–18.5); **Emax 108.6±8.4%** (CP=100 atomicity caveat R1.9) | N/A | NOT_REPORTED | NOT_REPORTED | Mouse tetrad inactive (no CB1 CNS tetrad); ↓BP, anti-inflammatory, peripheral analgesia (blocked by SR144528) | NOT_REPORTED (compound t½); Soethoudt later PK is **separate lab** | Peripheral CB2 tool; functional numbers recovered but **not Gold** (SMILES/Emax-ref) |
| Soethoudt 2017 *Nat Commun* (local extract; consensus probe) | **HU-308** (profiling) | Same chemotype, multi-assay panel | Selective vs CB1 in panel | Multi-pathway CB2 ago (pEC50 etc. in SI — treat as **later profiling**, not Hanuš substitute) | Full/potent ago narratives in text; numeric SI separate | N/A | NOT_REPORTED | NOT_REPORTED | In vivo selectivity studies among HU308/HU910/JWH133 | Oral/i.v. PK: half-lives discussed; **HU910** longest **~7 h** (text); HU308 vehicle-specific | Probe consensus; **do not pool** as Gold for Hanuš row |
| Grether et al. 2024 *Frontiers Pharmacol*; DOI `10.3389/fphar.2024.1426446` (local extract) | **Vicasinabin / RG7774** | Clinical CB2-selective agonist | No bind endogenous CB1 brain membranes (qualitative extract) | **Ki 51.3±16.2 nM** (hCB2 cell line); related spleen Ki ~31.9–39.7 nM | **h**CB2 cAMP **EC50 2.81±0.28 nM**; **m**CB2 cAMP **2.60±0.14 nM**; narrative **“full agonist”** — **no numeric %**. β-arr **EC50 99.69±5.72 nM** (≠ Round1 ~22) | N/A | NOT_REPORTED | NOT_REPORTED | Ocular / diabetic retinopathy program context in paper | Plasma PK table: **T1/2** e.g. **9.04 h** (one species row in extract); brain:plasma **0.0955–…**; “meaningful CNS penetration” in tox | Potent CB2 ago; Emax% missing + β-arr conflict → REVIEW |
| Mukhopadhyay 2016 *Br J Pharmacol*; DOI `10.1111/bph.13338` (Round1.9) | **LEI-101** (HCl in paper; free-base InChIKey stored) | Imidazolidinedione peripheral CB2 tool | Selectivity vs CB1 stated in lineage; absolute CB1 Ki detail **NOT fully tabulated in Round1.9 excerpt** | Func multi-assay **h**CB2 | Keep **pEC50** (do not convert): β-arr **7.0±0.3** Emax **41±6%**; GTPγS **6.6±0.2** Emax **65±8%**; cAMP **8.0±0.1** Emax **NOT REPORTED** | N/A | NOT_REPORTED | NOT_REPORTED | Peripheral tool / nephropathy context (paper lineage) | NOT_REPORTED | Peripheral CB2; salt/identity + cAMP footnote provenance block Gold |
| Han 2017 *ACS Med Chem Lett*; DOI `10.1021/acsmedchemlett.7b00396` (local extract) | **APD371 / olorinab** (= **cmpd 6**, not 17) | (S,S) CB2 ago; pyrazine ketone series | β-arr **h**CB1 **EC50 >10,000 nM** | β-arr **h**CB2 **EC50 6.2 nM**; **r**CB2 **7.6 nM** | Emax **106%** / **100%** vs CP55,940 (**β-arrestin PathHunter only** — **not** cAMP). cAMP Emax **NOT_VERIFIED** | N/A (LM stability >60 min h/r/m — microsomal, **≠ esterase soft-drug**) | NOT_REPORTED | NOT_REPORTED | Chronic pain hypothesis; cmpd **5** largely peripherally restricted (b/p); **17** high CNS (contrast) | NOT_REPORTED (parent t½) | Clinical CB2 ago candidate; assay class = β-arr |
| Tam 2012 *Cell Metab*; DOI `10.1016/j.cmet.2012.07.002` (Round1.1 Q11-21) | **JD5037** | Peripheral CB1 inverse agonist (ibipinabant analog) | Binding **Ki 0.35 nM** (CB1) | **>700-fold** CB1 over CB2 (selectivity statement); absolute CB2 Ki **optional / Chorvat BMCL** | CB1 inverse agonist (peripheral); **not** CB2 agonist | N/A | NOT_REPORTED | NOT_REPORTED | Metabolic disease models (Tam lineage) | NOT_REPORTED | **CB2-negative control** / CB1-only comparator for Janus panels |
| Pertwee 2008 / Bolognini 2010 / McPartland 2015 (docs quimioma/fibrosis — qualitative) | **Δ9-THCV** | Phytocannabinoid C3; PoC Janus imperfecto | Antagonist / negative modulator *in vitro* & low-dose *in vivo*; **flip** to ago at high dose | Partial CB2 agonist (heterogeneous assays) | Dual imperfect; bifásico CB1 | N/A (ésteres/ácidos = hipótesis H2 docs, **not** measured esterase soft-drug) | Decarboxilación THCVA→THCV (biosynth note) | NOT_REPORTED as soft-drug metabolite package | Inflamación/dolor models in lit.; **no IPF primary** in novelty audit | Dose-window bifásica (low ant / high ago) | Seed PoC — **not** clean peripheral Janus drug |
| Vasiljevik 2013 *J Med Chem* / PMC3904296 (local HTML Table 2 + text) | **VAS-27** (cmpd **27**) | Aminoalkylindole dual design from JWH-073-M4 scaffold | **m**CB1 **Ki 15.4±2.2 nM** | **h**CB2 **Ki 10.9±3.1 nM** | CB1: neutral ant / weak partial (little AC inhib; antagonizes agonist **3**). CB2: AC inhib ~CP-like partial–full (40–50% panel text) | N/A | Parent series motivated by **JWH-073 monohydroxy metabolites** (Brents) — not esterase soft-drug | Metabolite **4** (JWH-073-M4): neutral ant lead historically; here **4** acts as CB1 ago in AC assay (paper notes contrast) | Mouse: blocks agonist hypothermia; ↓ oral alcohol self-admin; blocks alcohol CPP | Thermoreg monitoring 0–10 h AUC described | Dual **CB1 neutral ant / CB2 ago**; alcohol models |
| Vasiljevik 2013 (same) | **VAS-30** (cmpd **30**) | Same series lead | **m**CB1 **Ki 37.3±11.8 nM** (text also 37.2) | **h**CB2 **Ki 26.5±1.5 nM** | Same dual phenotype as 27 | N/A | As above | As above | Same alcohol models as 27 | Same | Second dual lead; Round1.1 notes 37.2 vs 37.3 typo risk |
| Huffman 1999 lineage (Round1 CSV Ki 3.4; CERT WITH_SCOPE venue) | **JWH-133** | Classical CB2-selective ago | Lit. CB1 weak (Round1 cites Ki **677** lineage — verify primary) | Binding **Ki ~3.4 nM** (Round1; venue *Bioorg Med Chem* WITH_SCOPE) | CB2-selective ago (docs fibrosis: bleomycin model in later lit — not this Ki paper) | N/A | NOT_REPORTED | NOT_REPORTED | Bleomycin pulmonary fibrosis cited in `literatura_fibrosis` (separate papers) | NOT_IN_LOCAL_CORPUS (t½ for Huffman) | CB2 antifibrotic tool class; not Janus |
| Cinar / US9765031 / NCT04531150 (docs fibrosis/novelty — **no local numeric primary table**) | **MRI-1867 / zevaquenabant** | Hybrid **CB1 + iNOS** peripheral | Peripheral CB1 antagonism (program) | **N/A** (not CB2-ago Janus) | Dual CB1/iNOS — **not** CB1-ant/CB2-ago | NOT_IN_LOCAL_CORPUS | NOT_IN_LOCAL_CORPUS | NOT_IN_LOCAL_CORPUS | IPF / bleomycin / inhaled vs systemic (docs DOIs) | Clinical Ph1 cited | Competitor **indication** (periphery+multi-target), **different mechanism** |
| Mapa / fibrosis docs (combo citation only) | **AM6545 + AM1241** | Combo CB1-ant + CB2-ago (two drugs) | AM6545 = peripheral CB1 ant (affinity **NOT_IN_LOCAL_CORPUS** numeric) | AM1241 = CB2 ago (Soethoudt panel has AM1241 rows — optional; not expanded here) | Combo > each arm in diabetic kidney fibrosis (mapa qualitative) | N/A | N/A | N/A | Experimental diabetes / renal fibrosis | NOT_REPORTED | Rationale for **monomolecular** Janus gap — not a single soft-drug |

---

## 3. Gaps / NOT_IN_LOCAL_CORPUS

| Gap | Status |
|-----|--------|
| **Esterase / soft-drug / CES deactivation** matrices for Janus leads | **NOT_IN_LOCAL_CORPUS** (no usable local papers) |
| Soft-drug CB1 antagonists with measured plasma esterase → inactive acid | **NOT_IN_LOCAL_CORPUS** (JD5037/URB447 = peripheral restriction, not ester soft-drug) |
| Khanolkar 2007 Tables 1–2 (AM1710 Ki / GTPγS cells) | **NOT_FOUND** |
| Valenzano 2005 full PDF / Fig.1 / Table 2 (GW EC50/Emax/structure) | **NOT_FOUND** |
| Qiu 2023 main-text numeric Ki/IC50/EC50 for 14/15/16/20/24 | **NOT FOUND OA** (SI = qualitative S5 + MM-GBSA) |
| Absolute CB2 Ki for JD5037 (Chorvat BMCL 2012 table) | Optional polish — **not opened** |
| AM6545 / AM1241 standalone Ki/EC50 package | **NOT_IN_LOCAL_CORPUS** as primary extract (combo only in mapa) |
| Monlunabant / MRI-1891 numeric pharmacology | Named in docs only |
| Ester prodrug THCV/THCVA → esterase half-life | Hypothesis H2 in docs only |
| GOLD_CONFIRMED promotion of any row above | **N = 0** (Round1.9) |

---

## 4. Pipeline note

**Documentary only.** This matrix consolidates **already-on-disk** evidence for affinity/efficacy/periphery/metabolite columns.  

**STOP** on computational work: no docking, MD, QSAR, scoring, Gold promotion, or new literature campaigns authorized from this file.

---

## 5. Parent return

| Field | Value |
|-------|-------|
| **Path** | `results/reports/DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md` |
| **Row count** | **20** compound-rows (incl. multi-paper splits for GW/AM1710/HU-308 and combo/control rows) |
| **Compounds covered** | URB447; GW405833; AM1710; Qiu-14 (+15/16/20/24 qualitative); HU-308; Vicasinabin/RG7774; LEI-101; APD371/olorinab; JD5037; THCV; VAS-27/30; JWH-133; MRI-1867/zevaquenabant; AM6545+AM1241 |
| **Main gaps** | Soft-drug/esterase empty; Khanolkar & Valenzano tables missing; Qiu potencies OA NF; Gold = 0 |
| **Pipeline** | **STOP** |

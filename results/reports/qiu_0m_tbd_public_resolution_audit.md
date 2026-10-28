# 0M — Auditoría de TBD resolubles (fuentes públicas / docs CRO)

> **Verdict:** `0M-TBD-AUDIT = COMPLETE`  
> **Date:** 2026-08-12  
> **Upstream:** [qiu_0m_h1a_wet_handoff.md](qiu_0m_h1a_wet_handoff.md) · [qiu_0l_h1a_experimental_spec.md](qiu_0l_h1a_experimental_spec.md) · [qiu_0k_validation_plan_h1_h2.md](qiu_0k_validation_plan_h1_h2.md)  
> **Optional parallel package (cross-link only):** [cro_package_h1a/00_index.md](cro_package_h1a/00_index.md) — do not depend on it for this audit.  
> **Constraints honored:** no wet execution; no NCE; no docking/MD; **no invented** concentrations, purity cutoffs, PASS/KILL numbers, or designation of a single CRO system as “the answer.”

**Epistemic rule:** anything recovered from Qiu 2023 (DOI [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377)) or CRO catalogs is **PUBLISHED / VENDOR-DOCUMENTED context** — never auto-adopted as Janusforge PASS gate unless PI signs it in writing (0K TBD-18 / 0L §6 / 0M §6).

---

## 1. Alcance

| In | Out |
|----|-----|
| H1-a TBD register in **0M §3.2** (+ Local-A–D) | Inventing numeric PASS/KILL or µM windows |
| Partial fill from **public papers**, SI captions already in-repo, **CRO/vendor catalog pages**, RFQ quote-field menus | Closing gates without PI / lab sign-off |
| Cross-check 0L / 0K wording for same TBD ids | Wet run, NCE, docking/MD |
| Note typical **CRO quote fields** without prescribing thresholds | Picking one CRO catalog SKU as mandatory system |

**Sources used for *context* (not gates):**

| Source | What it contributes |
|--------|---------------------|
| Qiu SI captions in-repo (`data/papers/mmc1_document.txt` / `mmc1_extract.txt`) | **PUBLISHED:** CB2 agonism of compound 14 via **cAMP**; control **CP55940**; CB1 ant control **Rimonabant**; CB2 ant panel control **AM10257**; “three independent experiments performed in triplicate”; HPLC spectra section for final ligands |
| PubMed abstract (PMID 36731294) | **PUBLISHED:** Yin–Yang claim (CB1 ant + CB2 ago); no substitute for recovered numeric tables |
| Example CRO/vendor public pages (non-exclusive) | Menu of **hCB2** functional formats (e.g. cAMP Gi / CHO-K1), named **reference agonists** (often CP55,940), TAT, sample-volume / # concentration options for EC₅₀ calculation — **illustrative of quote fields**, not a selected vendor |
| 0D / mapa repo | Identity of Qiu-14 chemotype OK; **Ki/IC₅₀/EC₅₀ tables still not recovered as PASS numbers** |

**0K TBD-03/04/06/09/12–15** remain **out of H1-a start scope** (0M §3.2) and are not audited for wet unlock here.

---

## 2. TBD resolubles (parcialmente) vía público/CRO — tabla detallada

| TBD id | Short name | Why publicly / CRO-doc resolvable (vs lab-only) | Evidence needed | Still must confirm with laboratory / PI |
|--------|------------|------------------------------------------------|-----------------|----------------------------------------|
| **TBD-01** | Cellular system / hCB2 construct | CRO/vendor catalogs publicly list host line, species, accession/Uniprot, coupling mode, kit vs custom; Qiu SI confirms **functional cAMP** pharmacology but does **not** (in recovered captions) fully lock Janusforge’s host/construct | Full-text Qiu **Methods** (cell line, transient vs stable, density); ≥2 CRO assay datasheets/SOP summaries for hCB2 agonist mode; RFQ fields: construct, passage limits, plating density, forskolin/stimulant policy | Which **specific** system Janusforge will run; density; transient vs stable; whether to match Qiu or accept CRO default — **PI/lead choice** |
| **TBD-02** | Functional format (cAMP / β-arrestin / GTPγS) | **PUBLISHED** Qiu SI: compound 14 CB2 agonism “as determined by the **cAMP assay**”; public CRO menus also offer β-arrestin / GTPγS for hCB2 — format options are documentable without wet | Qiu Methods + SI Fig. S5/S13 captions; CRO catalog rows for each format (readout physics, units, agonist mode); brief rationale memo (literature match vs platform availability) | Primary format **locked for H1-a** (may follow Qiu cAMP or diverge); units and reporting convention for EC₅₀/Emax — **PI/lead** |
| **TBD-07** | Conc. window + # curve points | CRO quote pages state **how many concentrations** they need to return EC₅₀ and stock/volume minima; literature (once full PDF/tables recovered) can show **reported** windows — informs RFQ, does not set Janusforge gate | CRO RFQ: # dose points offered, top-test options, stock requirements; Qiu figures/tables for **reported** concentration axes (PUBLISHED only); do **not** invent µM | Exact min–max, spacing, and # points for **this** study; artifact/viability rationale — **lead ensayo + PI** |
| **TBD-08** | Ref agonist, vehicle, Z′/CV | **PUBLISHED** Qiu SI: **CP55940** as CB2 agonist control; CRO catalogs commonly name a control activator and list QC metrics as quote/SOP fields; vehicle % is often in SOP brochure | Qiu SI + Methods (ref ID/conc **as published**); CRO datasheet: reference agonist ID, vehicle/DMSO policy, plate QC metrics available (Z′, CV, etc.); RFQ: “report plate QC; state acceptance SOP version” | Acceptance limits for Z′/CV; final DMSO%; reference **concentration** in Janusforge plates; whether to use Qiu’s published control ID or CRO default — **PI + CRO SOP on file** |
| **TBD-10** | Purity / ID minima + lot COA | Custom-synthesis CRO RFQs and supplier COA templates **publicly define fields** (HPLC %, LC-MS, NMR, lot ID); Qiu SI includes **HPLC spectra of final ligands** (published practice) — informs *what to request*, not the cutoff number | Synthesis RFQ/COA template fields; Qiu SI HPLC/NMR sections as **identity practice** context; 0D chemotype checklist for ID vs published structure | Numeric purity/ID **acceptance cutoffs** for H1-a; lot release sign-off — **química / PI** (no invented %) |
| **TBD-11** | Qiu-14 access path & timeline | Purchase catalogs, custom-synthesis quotes, and author/institution contact paths are **ops-documentable** without wet; structure identity anchored in 0D / published figures | RFQ synthesis (mg scale, chemotype description per 0D — **no Janusforge NCE SMILES**); commercial availability search notes; author correspondence log; delivery ETA before wet | Material **in hand** (or firm delivery date); identity vs 0D on the **actual lot** — lab/ops confirmation |
| **TBD-17** | CRO vs in-house path | Public CRO capability pages (formats, TAT, geographies) + in-house capacity inventory allow a **documented comparison**; does not by itself pick the path | Side-by-side of ≥2 CRO options (format, TAT, sample reqs) vs in-house SOP availability; confidentiality terms | Final **execution path** and named SOP version on file — **PI** |
| **TBD-18** | Optional recovery of Qiu table numbers | Explicitly a **public-document** recovery task (full PDF / SI tables); 0K/0L already forbid auto-PASS | Full Qiu 2023 PDF + SI pharmacology tables/figures (Ki/IC₅₀/EC₅₀ **as published**); citation log | Whether PI **adopts any literature number in writing** as Janusforge criterion (default: **context only**) |
| **Local-A** | Tech / bio replicate n; days | Qiu SI **PUBLISHED:** “mean ± SEM of **three independent experiments** performed in **triplicate**” — literature context for n; CRO SOPs often state default replicate policy as quote fields | Qiu SI Fig. S5 caption; CRO SOP brochure / RFQ “n tech / n bio / independent days” fields | Janusforge pre-registered n and independent-day plan — **lead ensayo** (may differ from Qiu) |
| **Local-B** | Curve model / outlier / plate-fail SOP | Analysis conventions are typically in **CRO SOP** or kit manuals (public or under NDA brochure) — version can be requested before wet | Named SOP/version from chosen site; curve-model options offered; outlier/plate-fail rules document | Which SOP version is **binding** for H1-a and PI sign-off before unblinding — **lead ensayo** |
| **Local-C** | Optional CB2 antagonist; viability cutoffs | Common CB2 antagonists appear on **public catalogs** and Qiu SI (**AM10257** as CB2 antagonist-panel control — PUBLISHED); viability assays are standard CRO add-ons — IDs/options resolvable; cutoffs are not | Catalog/SOP for optional antagonist ID; Qiu SI Fig. S12 context; CRO viability assay menu + report fields | Whether to **run** antagonist/viability; antagonist conc.; viability **acceptance cutoffs** — **lead ensayo** |
| **Local-D** | Temp / incubation / plate format | Covered by **CRO SOP** when outsourced; kit manuals publish typical incubation/plate parameters as documentation (not Janusforge invention) | CRO/in-house SOP: temperature, incubation time, plate format, reader | If in-house: lock parameters; if CRO: confirm SOP version covers Local-D so it is not open — **lead / CRO** |

**Count (publicly / partially resolvable):** **12**

---

## 3. Evidencia a solicitar en RFQ / dossier

Use as a **request checklist** (fields only — no thresholds invented here). Aligns with optional [cro_package_h1a](cro_package_h1a/00_index.md) RFQs if present.

### 3.1 Assay CRO / kit RFQ fields

- Assay class: functional **hCB2 agonism** (H1-a PROTOCOL)
- Format menu available: cAMP / β-arrestin / GTPγS (and which is proposed)
- Host cell / construct / species / accession or Uniprot
- Reference agonist **identity** (and whether concentration is CRO-standard vs sponsor-defined)
- Vehicle / max DMSO% policy
- # concentration points offered for EC₅₀; sample volume / stock strength requirements
- Plate QC metrics reported (e.g. Z′, CV) and **SOP version** that defines acceptance
- Default tech/bio replicate policy; independent-day options
- Optional: CB2 antagonist co-incubation; viability at top concentration
- TAT; report contents (raw + fitted EC₅₀/Emax); confidentiality

### 3.2 Synthesis / material RFQ fields (Qiu-14 validation vehicle)

- Chemotype / identity per **0D** (published vehicle — not Janusforge NCE)
- Deliverable amount (mg-scale for H1-a)
- COA fields: HPLC, LC-MS, NMR, lot ID, appearance, residual solvents if offered
- Storage / shipping; ETA before first wet date
- Do **not** attach proprietary Janusforge NCE structures

### 3.3 Literature dossier (parallel, TBD-18)

- Full Qiu 2023 PDF + SI pharmacology tables
- Extract **as PUBLISHED** only: assay type, controls, any Ki/IC₅₀/EC₅₀, replicate statement
- Explicit banner: **not** Janusforge PASS unless PI adopts in writing

---

## 4. TBD necesariamente lab/PI (no cerrables solo con público)

Names only (no fake resolution):

- **TBD-05** — Min CB2 agonism PASS/KILL numeric criterion (EC₅₀ ceiling and/or Emax % of ref and/or Δ vs vehicle) — **must be PI-signed**; literature (TBD-18) may inform but never auto-closes
- **TBD-16** — Budget scope (H1-a only vs broader campaign) — finance/PI; CRO quotes inform cost but do not choose scope

*(Final lock of any partially filled TBD in §2 still requires lab/PI sign-off; §4 lists items that **cannot** even be partially closed by public/CRO docs alone.)*

**Count (necessarily lab/PI-only):** **2**

---

## 5. Veredicto: qué se puede desbloquear sin lab vs qué bloquea aún

| Desbloqueable sin wet (ops / docs) | Sigue bloqueando wet start |
|------------------------------------|----------------------------|
| Menu of cell systems & formats (TBD-01/02) from CRO catalogs + Qiu **cAMP** context | **TBD-05** unsigned PASS/KILL numbers |
| RFQ-comparable quote fields for refs, QC metrics, dose-point counts (TBD-07/08) | PI lock of **exact** conc. grid, Z′/CV limits, vehicle % |
| Material path RFQs + COA field list (TBD-10/11) | Lot in hand + purity **acceptance** numbers |
| CRO vs in-house comparison dossier (TBD-17) | Named path + SOP version on file |
| Literature table recovery workflow (TBD-18); Local-A–D option sheets from SOP/catalogs | Pre-registered replicate/analysis/optional antagonist/viability **decisions** |
| — | **TBD-16** if PO is budget-gated |

**Bottom line:** public/CRO documentation can **partially fill 12** H1-a TBDs (menus, published Qiu methods context, RFQ fields) and **cannot** replace the **2** pure PI locks (**TBD-05**, **TBD-16**). Wet remains blocked until §7 of 0M is checked — including PI-signed **TBD-05** — even after RFQs return.

**`0M-TBD-AUDIT = COMPLETE`**

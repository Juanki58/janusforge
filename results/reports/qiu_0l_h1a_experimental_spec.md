# Qiu 0L — H1-a experimental specification (CB2-first; no wet execution)

> **Status:** **SPEC CLOSED** — ready for pre-lab TBD fill; **no wet started**  
> **Date:** 2026-08-12  
> **Hypothesis:** **H1-a only** — Qiu-14 → functional **hCB2** agonism (CB2-first)  
> **Out of scope here:** H1-b, H2, H3, H4, H5; docking/MD; NCE design; numeric PASS thresholds (all **TBD**)  
> **Upstream (read-only):** [`qiu_0k_validation_plan_h1_h2.md`](qiu_0k_validation_plan_h1_h2.md) · [`qiu_0k_hypothesis_options.md`](qiu_0k_hypothesis_options.md) · [`qiu_0i_evidence_matrix.md`](qiu_0i_evidence_matrix.md) · [`qiu_0d_structure_verification.md`](qiu_0d_structure_verification.md)  
> **IP framing:** [`docs/ip_gate_janusforge.md`](../../docs/ip_gate_janusforge.md) · [`qiu_0ip_novelty_landscape.md`](qiu_0ip_novelty_landscape.md) — **not legal advice**

**Epistemic layers (mandatory):**

| Layer | Use in this spec |
|-------|------------------|
| **PUBLISHED** | Qiu 2023 literature claims / map (motivation only) |
| **PROTOCOL DECISIONS** | Choices locked by 0K / this 0L for H1-a design |
| **TBD** | Must be filled before wet; **not invented here** |

---

## 0. IP / inventorship framing (non-negotiable)

1. **Qiu-14 is a published validation vehicle**, not a Janusforge NCE and not inventorship.  
2. Direct copies of Qiu-14 are **scientific prior art** (RED ZONE 2 in 0IP) — useful as **control**, not as product.  
3. After H1/H2 PASS, any **virtual NCE** work must stay within documented **blue-ocean hypotheses** and pass **🛑 IP GATE / counsel** before disclosure or synthesis campaign ([`docs/ip_gate_janusforge.md`](../../docs/ip_gate_janusforge.md)).  
4. **No proprietary NCE SMILES** in this document.  
5. **No wet execution** authorized by writing this spec alone — execution still needs TBD closure + ops go.

---

## 1. Objective (H1-a)

**PROTOCOL DECISION:** Determine whether **Qiu-14** produces a clear **CB2 agonist** functional signal in the project’s chosen hCB2 assay format, versus vehicle, with a known CB2 agonist reference control.

| If | Then (per 0K) |
|----|----------------|
| H1-a **PASS** (criteria TBD) | Proceed to plan **H1-b** (CB1 control) — separate spec |
| H1-a **KILL** | Stop Qiu-14 as operational anchor; QC material/assay before pivoting axis |

**PUBLISHED (motivation only):** Qiu et al. describe compound 14 as Yin–Yang (CB1-ant + CB2-ago). Repo has **not** recovered numeric Ki/IC₅₀/EC₅₀ tables — **do not invent literature numbers as PASS gates** ([`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md)).

---

## 2. Test article

| Item | Spec |
|------|------|
| **Compound** | Qiu-14 (published Yin–Yang lead) |
| **Identity anchor** | Match 0D chemotype: o-morpholinophenyl + CONH–1-adamantyl pyrazole-3-carboxamide ([`qiu_0d_structure_verification.md`](qiu_0d_structure_verification.md)) |
| **Role** | Positive **literature control / validation vehicle** |
| **Source** | **TBD-11** — purchase / contract synthesis / authors |
| **Purity / ID** | **TBD-10** — HPLC, LC-MS, NMR minima; lot recorded |
| **Vehicle** | **TBD** — DMSO% / buffer compatible with assay (must match vehicle control) |

**PROTOCOL DECISION:** Do **not** require Qiu-15/20/24 for H1-a gate (0K).

---

## 3. Experimental system

| Element | Status | Notes |
|---------|--------|-------|
| Receptor | **PROTOCOL:** human **CB2** (hCB2) | Ortholog/construct **TBD-01** |
| Host cells / membranes | **TBD-01** | Line, density, transfection vs stable; CRO kit vs in-house |
| Assay class | **PROTOCOL:** **functional** CB2 agonism (not binding-as-substitute) | Binding optional later (**TBD-04**), not H1-a gate |
| Readout format | **TBD-02** | Choose one primary: cAMP **or** β-arrestin **or** GTPγS (document why) |
| Temperature / time / plate format | **TBD** | CRO SOP or in-house protocol |

**Explicit non-claims:** Docking Vina, pose overlap, Jaccard, and “0 H-bonds geometry-OK” from 0D–0J are **not** endpoints and **not** PASS criteria.

---

## 4. Controls

| Control | Role | Status |
|---------|------|--------|
| **Vehicle** | Baseline | Required (**TBD-08**) |
| **CB2 agonist reference** | Positive control / Emax scale | Required — identity & conc. **TBD-08** |
| **Optional CB2 antagonist** | Confirm signal is CB2-mediated | **TBD** (recommended if ambiguous) |
| **Cytotoxicity / viability** | Artifact check at top conc. | **TBD** |
| **Z′ / CV acceptance** | Plate QC | **TBD-08** |

---

## 5. Concentration range, replicates, curve

| Element | Status |
|---------|--------|
| Conc. window (min–max) | **TBD-07** — do not invent µM ceiling here |
| Number of curve points | **TBD-07** |
| Replicates (tech / bio) | **TBD** |
| Independent days / n | **TBD** |
| Curve model | **TBD** — e.g. 4PL; constraints documented |

**Note:** Any “e.g. ≤10 µM” in 0K *options* is **illustrative historical only**, **not** adopted as PASS ([`qiu_0k_validation_plan_h1_h2.md`](qiu_0k_validation_plan_h1_h2.md) §4).

---

## 6. Endpoint & analysis

| Element | Spec |
|---------|------|
| **Primary endpoint** | **PROTOCOL:** CB2 **agonism** (direction locked) |
| **Reported metrics** | EC₅₀ and/or Emax (or equivalent pre-registered readout) — units **TBD-02** |
| **Comparator** | vs vehicle; scaled vs CB2 agonist ref (**TBD-08**) |
| **Analysis plan** | Pre-register before unblinding wet data: curve fit, outlier rules, plate fail rules — **TBD** |
| **Literature Qiu numbers** | May be recovered in parallel (**TBD-18**) as **context only**, never auto-PASS unless PI adopts in writing |

---

## 7. PASS / KILL (qualitative directions only)

| Decision | Direction (PROTOCOL from 0K) | Numeric threshold |
|----------|------------------------------|-------------------|
| **PASS** | Clear **CB2 agonism** vs vehicle with acceptable assay quality | **TBD-05** (EC₅₀ ceiling and/or Emax min % of ref — **not invented here**) |
| **KILL** | No CB2 agonism above TBD threshold, **or** signal uninterpretable after material/assay QC | Same TBD-05 / QC rules |
| **Next** | PASS → authorize drafting **H1-b** spec; KILL → 0K §7 stop/pivot | — |

---

## 8. Materials & logistics checklist

- [ ] Qiu-14 lot secured (**TBD-11**)  
- [ ] Identity vs 0D confirmed (**TBD-10**)  
- [ ] Assay format locked (**TBD-02**)  
- [ ] Cell system locked (**TBD-01**)  
- [ ] Controls ordered (**TBD-08**)  
- [ ] Conc. grid locked (**TBD-07**)  
- [ ] PASS numbers written & signed by PI (**TBD-05**)  
- [ ] CRO vs in-house (**TBD-17**) + budget (**TBD-16**)  
- [ ] Confidentiality: results of Qiu-14 OK to discuss as published control; any **future proprietary NCE** stays under IP gate  

---

## 9. TBD register (H1-a subset of 0K)

Carried from 0K; must close before wet:

| ID | What is missing | Why it matters |
|----|-----------------|----------------|
| **TBD-01** | Cellular system / hCB2 construct | Comparability and interpretability |
| **TBD-02** | Functional format (cAMP / β-arrestin / GTPγS) | Defines endpoint physics |
| **TBD-05** | Min CB2 agonism criterion (EC₅₀ / Emax / Δ vs vehicle) | PASS/KILL without inventing numbers |
| **TBD-07** | Conc. window + curve points | Artifact vs potency window |
| **TBD-08** | Ref agonist, vehicle, Z′/CV | Assay QC |
| **TBD-10** | Purity / ID minima for Qiu-14 | Avoid false KILL |
| **TBD-11** | Access path & timeline for Qiu-14 | Can H1-a start? |
| **TBD-16** | Budget scope (H1-a only vs H1 full) | Ops |
| **TBD-17** | CRO vs in-house | Execution path |
| **TBD-18** | Optional recovery of Qiu table numbers | Literature context only |

Additional H1-a locals (not numbered in 0K): viability cutoffs; tech/bio replicate n; analysis SOP version.

---

## 10. Explicit non-scope

- No wet lab execution in this document.  
- No H1-b / H2 / H3 protocols.  
- No docking, MD, or SAR campaigns.  
- No modification of 0D–0K result files.  
- No proprietary Janusforge NCE SMILES.  
- No numeric PASS thresholds invented.  
- No claim that H1-a PASS = patentable invention.

---

## 11. Cierre

**0L = SPEC CLOSED for H1-a (Qiu-14, CB2-first).** Wet remains blocked on TBD closure + execution authorization. IP gate remains mandatory before any post-H1/H2 proprietary NCE design/disclosure.

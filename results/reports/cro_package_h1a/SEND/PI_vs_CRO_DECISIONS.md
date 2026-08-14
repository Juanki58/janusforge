# PI vs CRO decisions — H1-a RFQ (keep quotes comparable)

> **Date:** 2026-08-12  
> **Rule:** RFQ asks for **presupuesto técnico** (quote). It is **not** a closed work order and does **not** set TBD-05.  
> **Do not invent** numeric PASS/KILL thresholds.

Cross-ref: `qiu_0m_h1a_wet_handoff.md` §3.2 / §7 · `RFQ_ASSAY_CB2_H1A.md` §7–8.

---

## Traffic-light status (program)

| Layer | Status | Meaning |
|-------|--------|---------|
| Qiu-14 identity (DOI / SMILES / chemotype) | 🟢 | Ready to quote synthesis |
| H1-a scientific framing (CB2-first functional) | 🟢 | Scientifically unblocked |
| Compute context (no docking/MD in RFQ) | 🟢 | Explicitly out of scope |
| RFQ technical package (SEND four-pack) | 🟡 | Sendable for quotes; blanks intentional |
| **TBD-05** numeric Go/No-Go | 🔴 | **PI decision** — blank until signed |
| Material in hand (TBD-11 / COA TBD-10) | 🔴 | Blocks wet start |
| CRO selected + PO | 🔴 | After comparable quotes + locks |

**Summary:** H1-a is **scientifically unblocked**, **operationally blocked** until TBD-05 (+ material / platform locks) close.  
**0N:** frozen / NOT READY — not a gate on this RFQ.

---

## 🔴 PI / Janusforge must decide (esp. before PO / wet)

| ID | Decision | RFQ posture | Who |
|----|----------|-------------|-----|
| **TBD-05** | Numeric PASS/KILL (EC₅₀ ceiling and/or Emax % ref and/or Δ vs vehicle) | **Left blank** — CRO must **not** invent sponsor thresholds | **PI** (CRO may advise) |
| **TBD-10** | Material purity / ID minima for assay use | Quote commercial purity offers (≥95/98%); acceptance later | **PI** |
| **TBD-11** | Qiu-14 access path (buy / synthesize / authors) | Synthesis RFQ is one path; not a purchase PO | Ops / PI |
| **TBD-17** | CRO vs in-house execution | RFQ explores CRO path only | PI |
| **TBD-16** | Budget scope | Quote first; PO later | PI / finance |
| Prefer catalog CB2 cAMP vs custom | Optional after quotes | Do not pre-lock in RFQ | PI + lead ensayo |
| Sign pre-study lock | Written lock of TBD-01/02/05/07/08/10 | After CRO selected | PI + CRO |

**Without TBD-05 signed → no H1-a PASS claim and no wet start** (0M hard stop).

---

## 🟡 Ask CRO in the RFQ (quote fields — comparable across CROs)

| Ask | Where | Notes |
|-----|-------|-------|
| Price 10 / 25 / 50 mg Qiu-14 | Synth RFQ §2, §7 | Same tiers all CROs |
| Purity method offered + COA/NMR/LC-MS inclusions | Synth RFQ §3–4, §7 | Offer ≠ TBD-10 lock |
| Lead time, shipping, Incoterms, NDA | Synth RFQ §5, §7 | |
| Propose hCB2 system / kit | Assay RFQ → fills **TBD-01 proposal** | PI locks later |
| Propose format (cAMP / β-arr / GTPγS) | Assay → **TBD-02 proposal** | PI locks later |
| Propose conc. window + # points | Assay → **TBD-07 proposal** | Not PASS numbers |
| Controls, replicates, days, QC (Z′/CV) | Assay §4, §8 | Feeds TBD-08 / Local-A |
| Price CB2 (sponsor-supplied) | Assay §8 #3 | |
| Price CB2 if CRO synthesizes (bundle) | Assay §8 #4 | Separate lines preferred |
| Optional CB1 stage-2 **separate** price | Assay §3, §8 #9 | Not required for CB2 quote |
| Currency, validity, quote ID | Both RFQs | |

---

## What the RFQ must **not** pretend

- That TBD-05 is already set  
- That literature EC₅₀/Emax = auto-PASS  
- That this email/RFQ is a purchase order or study start  
- That docking/MD/NCE are in scope  

---

## Sequence (ops)

```text
Identical SEND RFQ → comparable quotes → select CRO
  → PI locks TBD-05 (+ TBD-01/02/07/08/10) in writing with CRO
  → material on hand (TBD-11) → PO / wet H1-a
```

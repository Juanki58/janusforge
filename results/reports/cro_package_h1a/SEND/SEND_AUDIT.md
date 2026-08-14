# SEND package audit — H1-a CRO RFQ (Qiu-14)

> **Audit date:** 2026-08-12  
> **Folder:** `results/reports/cro_package_h1a/SEND/`  
> **Full verbatim dump (cross-session):** [`../SEND_FULL_TEXT_DUMP.md`](../SEND_FULL_TEXT_DUMP.md)  
> **0M handoff (read-only):** `results/reports/qiu_0m_h1a_wet_handoff.md` → **`0M = BLOCKED`** (wet not executed)

---

## Verdict: **SEND-READY** for RFQ / presupuesto técnico (with one omit rule)

H1-a is **scientifically unblocked**, **operationally blocked** (TBD-05 🔴, material 🔴, CRO selection 🔴).  
Sending the RFQ does **not** start wet work and does **not** invent TBD-05.

**Omit rule (do not treat as NEEDS FIX invent):** Cover letter attachment table still names `COMPARISON_SCORECARD.md` — **do not email it**; attach only the four RFQ/NDA files listed below.

| Layer | Light | Note |
|-------|-------|------|
| Qiu-14 identity | 🟢 | DOI, SMILES, chemotype, InChIKey in synth RFQ |
| H1-a framing | 🟢 | CB2-first functional; binding not gate |
| Compute context | 🟢 | Docking/MD/NCE out of RFQ scope |
| RFQ technical four-pack | 🟡 | Sendable; blanks intentional |
| TBD-05 | 🔴 | PI must set before PO/wet — **blank in RFQ** |
| Material (TBD-11/10) | 🔴 | Not in hand / COA not locked |
| CRO selected | 🔴 | After comparable quotes |

**0N:** frozen / NOT READY — mention only; not a gate on SEND.

---

## Required four-pack check

| File | Status |
|------|--------|
| `RFQ_COVER_LETTER.md` | PRESENT |
| `RFQ_SYNTHESIS_QIU14.md` | PRESENT |
| `RFQ_ASSAY_CB2_H1A.md` | PRESENT |
| `NDA_IP_NOTE.md` | PRESENT |

None missing.

---

## Exact attach list (email)

1. `RFQ_COVER_LETTER.md`  
2. `RFQ_SYNTHESIS_QIU14.md`  
3. `RFQ_ASSAY_CB2_H1A.md`  
4. `NDA_IP_NOTE.md`  

### Omit from email

- `COMPARISON_SCORECARD.md` (sponsor-internal)  
- `SEND_AUDIT.md`, `PI_vs_CRO_DECISIONS.md`, `CRO_SHORTLIST.md`, `CRO_CONTACTS.md`, `EMAIL_DRAFTS.md`  
- Dossier 01 / ficha 02 / IP whitespace / proprietary NCE  
- `SEND_FULL_TEXT_DUMP.md` / `qiu_0m` (internal)

Optional: convert the four to PDF if a portal rejects `.md`.

---

## File-by-file (what each contains)

| File | Contents | Email? |
|------|----------|--------|
| `RFQ_COVER_LETTER.md` | EN cover + short ES; scope; TBD-05 blank policy; four-file attach list | **Yes** |
| `RFQ_SYNTHESIS_QIU14.md` | SMILES, DOI, tiers 10/25/50 mg, COA/NMR/LC-MS, quote table | **Yes** |
| `RFQ_ASSAY_CB2_H1A.md` | CRO proposes platform; blank TBD-01/02/05/07/08/10; quote lines | **Yes** |
| `NDA_IP_NOTE.md` | Published vehicle only; mutual NDA for commercials | **Yes** |
| `COMPARISON_SCORECARD.md` | Empty 3-CRO matrix | No |
| Meta (EMAIL / CRO / PI / AUDIT) | Sponsor send kit | No |

---

## What is READY vs correct / omit

### READY (send for quotes)

- Identity + SMILES present  
- Comparable synth tiers  
- Assay is proposal-based (CRO fills platform quote fields)  
- TBD-05 blank **and explained** (not a bug)  
- IP note clear  

### Do **not** “fix” before send

- Do **not** invent TBD-05 numbers  
- Do **not** fill PASS/KILL from literature  

### Sponsor fill before clicking send

- Sender name / email / phone in mail body  
- Choose 2–3 CROs from `CRO_SHORTLIST.md`  
- For Eurofins: use web form (forms-only caveat)

### Caveats (not NEEDS FIX)

- Markdown vs PDF intake  
- TBD blanks will prompt questions — answer: propose platform; PI locks TBD-05 before PO  

---

## Align with 0M

`qiu_0m` = **BLOCKED** until pre-study gate (§7) including **TBD-05 signed**.  
RFQ sending is the correct next ops step; wet remains hard-stopped.

---

## Related

| Doc | Use |
|-----|-----|
| [`PI_vs_CRO_DECISIONS.md`](PI_vs_CRO_DECISIONS.md) | 🔴 PI vs 🟡 CRO quote asks |
| [`CRO_SHORTLIST.md`](CRO_SHORTLIST.md) | Providers + public contacts |
| [`EMAIL_DRAFTS.md`](EMAIL_DRAFTS.md) | ES presupuesto técnico |
| [`../SEND_FULL_TEXT_DUMP.md`](../SEND_FULL_TEXT_DUMP.md) | Full verbatim for other session |

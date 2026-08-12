# Paquete CRO H1-a — Índice

> **Ruta:** `results/reports/cro_package_h1a/`  
> **Fecha:** 2026-08-12  
> **Decisión operativa:** Qiu-14 → presupuesto → síntesis → H1-a → Go/No-Go  
> **Política:** **NO compute ahora** — sin docking, MD, generación masiva ni diseño NCE.

---

## SEND these files (email-ready)

**Folder:** [`SEND/`](SEND/) — **identical package** to 2–3 CROs for comparable quotes.

| Send | File | Audience |
|------|------|----------|
| **1** | [`SEND/RFQ_COVER_LETTER.md`](SEND/RFQ_COVER_LETTER.md) | CRO BD (EN + short ES) |
| **2** | [`SEND/RFQ_SYNTHESIS_QIU14.md`](SEND/RFQ_SYNTHESIS_QIU14.md) | Synthesis quote |
| **3** | [`SEND/RFQ_ASSAY_CB2_H1A.md`](SEND/RFQ_ASSAY_CB2_H1A.md) | Assay quote (TBD-05 blank) |
| **4** | [`SEND/NDA_IP_NOTE.md`](SEND/NDA_IP_NOTE.md) | Legal/BD intake |
| *(internal)* | [`SEND/COMPARISON_SCORECARD.md`](SEND/COMPARISON_SCORECARD.md) | Sponsor only — do **not** email unless you want CROs to see the blank matrix |

### Human send checklist (3 steps)

1. **Email the same four files** (cover + synthesis RFQ + assay RFQ + NDA/IP note) to each of 2–3 CROs — no edits per CRO except the To: line.  
2. **Keep the scorecard internal**; fill after quotes return (price, timeline, purity, assay platform, includes synthesis?, NDA).  
3. **Do not PO / start wet** until PI + selected CRO jointly lock blank TBD fields (esp. **TBD-05**); no invented PASS/KILL numbers in the RFQ.

---

## Working drafts (pre-SEND / internal)

| # | Archivo | Uso |
|---|---------|-----|
| 00 | [00_index.md](00_index.md) | Este mapa + flujo Go/No-Go |
| 01 | [01_dossier_cientifico_0d_0j.md](01_dossier_cientifico_0d_0j.md) | Dossier corto: demostrado / inferencia / no probado |
| 02 | [02_ficha_h1a.md](02_ficha_h1a.md) | Ficha experimental H1-a (PASS/KILL + TBD) |
| 03 | [03_rfq_sintesis_qiu14.md](03_rfq_sintesis_qiu14.md) | Draft RFQ síntesis (superseded for email by `SEND/`) |
| 04 | [04_rfq_ensayo_cb2.md](04_rfq_ensayo_cb2.md) | Draft RFQ ensayo (superseded for email by `SEND/`) |
| 05 | [05_ip_whitespace_brief.md](05_ip_whitespace_brief.md) | Brief IP RED/BLUE (not legal advice; internal) |

**Upstream (read-only):**  
[`../qiu_0d_0g_integration_qc.md`](../qiu_0d_0g_integration_qc.md) · [`../qiu_0i_evidence_matrix.md`](../qiu_0i_evidence_matrix.md) · [`../qiu_0j_visual_qc.md`](../qiu_0j_visual_qc.md) · [`../qiu_0k_validation_plan_h1_h2.md`](../qiu_0k_validation_plan_h1_h2.md) · [`../qiu_0l_h1a_experimental_spec.md`](../qiu_0l_h1a_experimental_spec.md) · [`../qiu_0m_h1a_wet_handoff.md`](../qiu_0m_h1a_wet_handoff.md) · [`../qiu_0ip_novelty_landscape.md`](../qiu_0ip_novelty_landscape.md) · [`../../docs/ip_gate_janusforge.md`](../../docs/ip_gate_janusforge.md)

---

## Cómo usar para 3 cotizaciones comparables

1. Enviar el set **SEND/** idéntico a ≥2–3 CROs (síntesis, ensayo, o bundle).  
2. Pedir precios en las **mismas unidades** (mg / líneas CB2 / CB1 aparte).  
3. Adjuntar dossier 01 + ficha 02 **solo** si el CRO pide más contexto; **no** adjuntar NCE propietarios ni SMILES Janusforge.  
4. Comparar con [`SEND/COMPARISON_SCORECARD.md`](SEND/COMPARISON_SCORECARD.md).

---

## Flujo Go/No-Go tras H1-a

```text
Qiu-14 (publicado) → presupuesto → síntesis/COA → cerrar TBD H1-a → ensayo CB2
        │
        ├─ H1-a PASS (bajo TBD-05 firmado) → plan H1-b (CB1) — fuera de este RFQ
        └─ H1-a KILL → stop Qiu-14 como ancla; QC material/ensayo; no NCE
```

**Qiu-14 = vehículo de validación publicado, no invención Janusforge.**

---

## Política NO-compute-now (explícita)

En esta fase **está prohibido** como siguiente paso de trabajo:

- Nuevo docking / Vina / redocking CB1 o CB2  
- MD / ensemble  
- Generación masiva de moléculas / SAR computacional  
- Diseño o divulgación de NCE propietario  

El retorno €/hora está en **síntesis + ensayo húmedo + citas comparables**, no en más cómputo.

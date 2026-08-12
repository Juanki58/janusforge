# Paquete CRO H1-a — Índice

> **Ruta:** `results/reports/cro_package_h1a/`  
> **Fecha:** 2026-08-12  
> **Decisión operativa:** Qiu-14 → presupuesto → síntesis → H1-a → Go/No-Go  
> **Política:** **NO compute ahora** — sin docking, MD, generación masiva ni diseño NCE.

---

## Mapa del paquete

| # | Archivo | Uso |
|---|---------|-----|
| 00 | [00_index.md](00_index.md) | Este mapa + flujo Go/No-Go |
| 01 | [01_dossier_cientifico_0d_0j.md](01_dossier_cientifico_0d_0j.md) | Dossier corto: demostrado / inferencia / no probado |
| 02 | [02_ficha_h1a.md](02_ficha_h1a.md) | Ficha experimental H1-a (PASS/KILL + TBD) |
| 03 | [03_rfq_sintesis_qiu14.md](03_rfq_sintesis_qiu14.md) | RFQ síntesis pequeña escala Qiu-14 |
| 04 | [04_rfq_ensayo_cb2.md](04_rfq_ensayo_cb2.md) | RFQ ensayo funcional CB2 (± CB1 stage 2) |
| 05 | [05_ip_whitespace_brief.md](05_ip_whitespace_brief.md) | Brief IP RED/BLUE (not legal advice) |

**Upstream (read-only):**  
[`../qiu_0d_0g_integration_qc.md`](../qiu_0d_0g_integration_qc.md) · [`../qiu_0i_evidence_matrix.md`](../qiu_0i_evidence_matrix.md) · [`../qiu_0j_visual_qc.md`](../qiu_0j_visual_qc.md) · [`../qiu_0k_validation_plan_h1_h2.md`](../qiu_0k_validation_plan_h1_h2.md) · [`../qiu_0l_h1a_experimental_spec.md`](../qiu_0l_h1a_experimental_spec.md) · [`../qiu_0m_h1a_wet_handoff.md`](../qiu_0m_h1a_wet_handoff.md) · [`../qiu_0ip_novelty_landscape.md`](../qiu_0ip_novelty_landscape.md) · [`../../docs/ip_gate_janusforge.md`](../../docs/ip_gate_janusforge.md)

---

## Cómo usar para 3 cotizaciones comparables

1. Enviar **el mismo** [03](03_rfq_sintesis_qiu14.md) a ≥3 CROs de síntesis (o 1 síntesis + compra si existe).  
2. Enviar **el mismo** [04](04_rfq_ensayo_cb2.md) a ≥3 CROs de ensayo (checklist de campos obligatorios al final de 04).  
3. Pedir precios en las **mismas unidades** (mg / n placas / CB1 como línea separada).  
4. Adjuntar solo dossier 01 + ficha 02 si el CRO pide contexto; **no** adjuntar NCE propietarios ni SMILES Janusforge.  
5. Comparar: plazo, pureza pedida (RFQ), formato de informe, y si CB1 stage 2 está cotizado aparte.

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

---

## Acciones humanas inmediatas

1. Enviar RFQs 03 y 04 a 3 CROs cada uno (o bundle si un CRO hace ambos).  
2. Cerrar TBDs hard-stop de la ficha 02 **antes** del primer wet (PI + CRO).  
3. Esperar cotizaciones → elegir proveedor → PO solo tras TBD-05/10/11 firmados.

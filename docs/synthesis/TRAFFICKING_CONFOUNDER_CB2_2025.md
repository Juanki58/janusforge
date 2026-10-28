# TRAFFICKING_CONFOUNDER_CB2_2025 — ligand-induced anterograde trafficking

**Fecha:** 2026-10-19  
**Tipo:** DOCUMENTATION ONLY — registro de confusor interpretativo; **sin** experimento nuevo.  
**Capa:** EXTERNAL / assay interpretation  
**PI authorization:** YES (decisión PI 2026-10-19).  
**Autoridad de freeze:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) · [`ACTA_EXTERNAL_CB2_APO_2026-09.md`](ACTA_EXTERNAL_CB2_APO_2026-09.md)

---

## Bibliographic note

| Field | Value |
|-------|-------|
| Citation | Oyagawa et al., *Cellular and Molecular Life Sciences* (2025) |
| Title | Insights into cannabinoid receptor 2 (CB2) anterograde trafficking and pharmacological chaperoning |
| DOI | [10.1007/s00018-025-05961-w](https://doi.org/10.1007/s00018-025-05961-w) |
| PMID | 41275039 |
| PMC | [PMC12748375](https://pmc.ncbi.nlm.nih.gov/articles/PMC12748375/) |

### What the paper reports (narrow)

- En sistemas celulares heterólogos, exposición **sostenida** a agonistas CB2 y también a algunos **inverse agonists** aumentó la entrega anterógrada de CB2 a la superficie (chaperoning farmacológico).  
- El efecto es **tiempo-dependiente** y puede **coexistir** con internalización de la población superficial ya presente.  
- **2-AG** no produjo tráfico anterógrado en las condiciones ensayadas.  
- Un motivo di-lisina (KK) en la cola C-terminal es necesario para la entrega basal a superficie.  
- Los autores piden verificación en sistemas **endógenos**.

---

## Why it is a confounder for Janusforge (locked)

| Ensayo / lectura | Riesgo si la duración es de horas |
|------------------|-----------------------------------|
| Eficacia aparente / Emax | Cambio de **abundancia superficial** ≠ cambio de eficacia intrínseca por residuo/hub |
| Sesgo / bias scores | Reserva de receptor y pools accesibles pueden moverse con el ligando y el tiempo |
| Comparaciones agonista vs inverse | Ambos pueden chaperonear → no interpretar solo como “activación vs silenciamiento” |
| Lecturas de localización vs señal | Coexistencia tráfico↑ + internalización complica endpoints únicos |

**Claim estrecho que sí registramos:** en ensayos **prolongados (horas)**, la abundancia superficial de CB2 puede cambiar por chaperoning ligando-inducido; eso es un confusor de interpretación farmacológica.

**Claims que NO hacemos:**

1. Que el tráfico demuestre (o refute) control conformacional intramolecular / hubs.  
2. Que haya que reabrir P2 o avanzar P5 por este paper.  
3. Que sistemas endógenos ya estén validados (los autores lo dejan abierto).

---

## Operational note (for future assay design — not authorized now)

Si en el futuro se diseñan ensayos celulares de horas:

1. Emparejar **superficie** (p. ej. binding no permeable / epitope tag) con la lectura de señal en el mismo eje temporal.  
2. Registrar ligando, concentración y duración; no colapsar a un único endpoint.  
3. Tratar 2-AG vs ligandos sintéticos como perfiles de tráfico potencialmente distintos.  
4. No usar este confusor como justificación de MD Tier B ni de reopen de gates.

---

## Status

```text
FLAG: TRAFFICKING_CONFOUNDER_CB2_2025 = REGISTERED
LAYER: EXTERNAL_ASSAY_INTERPRETATION
P2_REOPEN: FALSE
P5_ADVANCE: FALSE
CONFORMATIONAL_CLAIM: FALSE
```

Linked from [`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md) §3 / deferred leads.

---

*Fin. DOCUMENTATION ONLY.*

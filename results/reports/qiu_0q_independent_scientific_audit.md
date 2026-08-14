# 0Q — Auditoría científica independiente DESTROY-THE-HYPOTHESIS (CB1/CB2 · Qiu-14 · Janusforge)

**Fecha:** 2026-08-13  
**Alcance:** bloques 1–13 del brief del usuario (+ resumen ejecutivo = §0 / §14 bibliografía).  
**Método:** fuentes primarias (PubMed/EuropePMC abstracts, SI abierto Qiu, PMC URB447, RCSB REST UniProt P34972, Nature/Cell/JPET DOIs, ClinicalTrials.gov, textos de patentes locales).  
**No-autoridad:** informes Cursor 0P previos (incluido `qiu_0p_external_evidence_table.md`) = nota secundaria únicamente.  
**Bans respetados:** sin docking, sin MD, sin diseño NCE, sin campañas de docking; sin inventar datos.  
**Paywall explícito:** PDF principal Qiu *Bioorg. Chem.* 2023 (**DOI 10.1016/j.bioorg.2023.106377**) **no OA** (EuropePMC `isOpenAccess:N`; Unpaywall local inválido; PDFs SSRN locales son HTML/stubs corruptos). Potencias numéricas Ki/IC50/EC50 de 14/15/20/24 **no recuperables** aquí.

**Distinciones obligatorias usadas abajo:** experimental ≠ computacional ≠ especulación; docking ≠ actividad; patente ≠ FTO; publicado ≠ validado independientemente.

---

## 0. Resumen ejecutivo (≤1 página)

### Veredicto de clasificación: **D — NO-GO sobre la hipótesis Janusforge actual**

La hipótesis operativa a destruir era, en esencia: *“hace falta un programa computacional (docking/MD/diseño) anclado en Qiu-14 para inventar un ligando Janus CB1-antagonista / CB2-agonista útil en fibrosis.”* Esa hipótesis **no sobrevive** a la evidencia primaria.

**Por qué D (no E):** el espacio CB1/CB2 en fibrosis **sigue biológicamente interesante** (datos *in vivo* clásicos + híbridos periféricos CB1/iNOS en clínica temprana). Pero **Janusforge-como-diseño-estructural-de-NCE** es redundante y prematuro.

### Bullets ejecutivos

1. **Janus CB1-ant / CB2-ago ya está resuelto conceptualmente desde 2009** (URB447; IC50 CB1 313 nM / CB2 41 nM; PMC3690177). Qiu 2023 es **diseño de quimiotipo Yin-Yang en pirazol**, no invención del concepto.
2. **Qiu-14 existe experimentalmente en un solo lab** (síntesis + cAMP CB1-ant/CB2-ago en SI Fig. S5). **Sin números públicos, sin binding Ki, sin in vivo, sin fibrosis, sin réplica independiente.** Mecanismo S173/S285 = **docking/MD**, no mutagénesis de 14.
3. **Combo antifibrótico CB1↓ + CB2↑ ya se propuso en 2007** (Mallat/Lotersztajn) y aparece en **WO2022026478** (Makriyannis; mixed CB1-ant/CB2-ago para fibrosis). Qiu-14-for-fibrosis: **NOT FOUND**.
4. **Estructuras CB2 experimentales abundan** (RCSB UniProt P34972: 14 entradas experimentales; incluye 5ZTY, 6KPC, 6KPF, 6PT0, 8GUQ/R/S/T, 8X3L, 9U7L PAM 2026). **8F7V no es CB2** (plasmina) — error a no propagar.
5. **Compute→wet en CB2 ya tiene hit rates publicados** (p.ej. V-SYNTHES ~33%; Xing 2021 ~7/15 binding; Ge 2023 ~70% función LRIP *dentro de su serie*). Eso **no justifica** campañas de docking Janusforge antes de números Qiu y tool compounds comerciales.
6. **Clínica CB2 sola en fibrosis-adjacent falló** (lenabasum CF Ph2b no metió primary; Corbus 2020). CB1 central = toxicidad psiquiátrica conocida (rimonabant). Dual híbrido CB1/iNOS (zevaquenabant) está más avanzado que cualquier Janus pirazol Qiu.
7. **Ahorro inmediato:** no docking/MD/resíntesis/NCE. **Hacer barato:** pedir/comprar PDF Qiu; inventariar URB447/GW405833 comerciales como tools. **Hacer solo si** potencias Qiu son nM útiles *y* tool Janus muestra señal en ensayo de fibrosis.

---

## 1. Qiu-14 exacto (identidad, síntesis, ensayos, claims)

### Identidad química (experimental SI, no inventada)

| Ítem | Evidencia primaria | Tipo |
|------|-------------------|------|
| Ancla | Qiu et al., *Bioorg. Chem.* **133**:106377 (2023); PMID **36731294**; DOI **10.1016/j.bioorg.2023.106377** | Publicado (paywall) |
| Preprint | SSRN **4276225** (2022-11); mismo abstract | Preprint |
| Scaffold | Pirazol-3-carboxamida estilo rimonabant | Experimental (SI Scheme S1 OCR) |
| **Cpd 14** | N1-fenilo **orto-morfolinilo**; amida C3 = **1-adamantilo** | Experimental (OCR `image15_ocr.txt`) |
| Cpd 15 | Morfolinilo **meta**, adamantilo | Experimental |
| Cpd 20 | 4-Metilpiperazinilo **orto** (serie adamantilo) | Experimental |
| Cpd 24 | Morfolinilo **orto**, R3 = **CH₂-1-adamantilo** | Experimental |
| PubChem/ChEMBL CID exacto 14 | **NOT FOUND** (lookup InChIKey local vacío) | Ausencia |

### Síntesis y caracterización

- **Scheme S1** (SI): ruta pirazol + acoplamiento amida (HATU-class).  
- **HPLC** etiqueta `14:` y sección NMR de ligandos finales en SI (`mmc1_document.txt`).  
- Cristales de ligandos en Fig. S2: **5/6/8/9/12/13** — **no 14**. Conformacional 14 = cálculo HF/6-31G(d) (Fig. S4) → **computacional**.  
- Conclusión: **síntesis reclamada + caracterización SI presente**; tablas ¹H/¹³C numéricas de 14 = imágenes, no texto recuperable.

### Ensayos CB1/CB2 (binding vs funcional)

| Ensayo | Resultado abierto | Controles | Calidad |
|--------|-------------------|-----------|---------|
| CB2 **agonista** cAMP | Fig. **S5A** — dirección agonista para 14; n=3×triplicado | CP55,940 | Experimental funcional; **sin EC50/%Emax públicos** |
| CB1 **antagonista** cAMP | Fig. **S5B** | Rimonabant | Idem; **sin IC50 públicos** |
| Series CB1-ant / CB2-ant / CB2-ago | Figs. S11–S13 | Rimonabant / AM10257 / CP55,940 | Curvas; OCR incompleto para paneles 14 |
| Binding radioligando Ki | **NOT FOUND** en SI/abstract abierto | — | Hueco / paywall |

**Importante:** perfil Janus de 14 = **funcional recombinante cAMP**, no binding dual publicado en abierto, no nativo, no in vivo.

### Roles 14 / 15 / 20 / 24 (desde SI + abstract)

| Cpd | Rol en narrativa Qiu | Evidencia abierta |
|-----|----------------------|-------------------|
| **14** | Highlight Yin-Yang: orto-morfolina = “switch” | Fig. S5 ambos brazos; abstract |
| **15** | Meta-morfolina: docking sugiere colisiones (Fig. S6) | Docking = **computacional**; farmacología serie en S11–S13 (números paywalled) |
| **20** | Orto-piperazinilo metilo (variante N) | Docking Fig. S7; farmacología paywalled |
| **24** | Homólogo CH₂-adamantilo | Identidad SI; farmacología paywalled |

### Experimental vs mecanístico

| Claim | Clasificación |
|-------|----------------|
| 14 es CB1-ant + CB2-ago en cAMP | **Experimental** (un lab) |
| Orto-morfolina es el switch SAR | **Experimental** (serie) + interpretación |
| H-bond a **S173 (CB1)** y **S285 (CB2)** | **Computacional** (docking + MD; abstract) |
| MM-GBSA correlaciona con actividad (Fig. S14 / Tables S1–S2) | **Computacional** |
| Utilidad terapéutica / fibrosis | **Especulación / NOT FOUND** para Qiu-14 |

### Follow-ups / patentes autores

- Citer OpenAlex/EuropePMC: Chen et al. 2025 peptide CB2 (*Bioorg. Chem.* 10.1016/j.bioorg.2025.108770) — no reutiliza 14.  
- Mismos autores: **photoswitch** Yin-Yang Azo (*Eur. J. Med. Chem.* 2026, DOI **10.1016/j.ejmech.2026.118883**) — tema dual opposite control; **no es réplica de 14 ni fibrosis**.  
- Patente composición Qiu-14 / Tao Yin-Yang: **NOT FOUND** en probes locales Google Patents (inventor Qiu/Tao). **≠ FTO.**

---

## 2. Precedentes Janus (CB1-ant/inv + CB2-ago) — tabla completa

| Compuesto | Quimiotipo | CB1 | CB2 | Evidencia primaria | ¿Janus validado? | ¿Fibrosis? |
|-----------|------------|-----|-----|--------------------|------------------|------------|
| **URB447** | Pirrol | Antagonista neutro; IC50 **313±72 nM** (rat) | Agonista; IC50 **41±23 nM** (hCB2) | LoVerme/Piomelli *BMCL* 2009 DOI **10.1016/j.bmcl.2008.12.059**; PMC3690177 | **Sí (1º declarado)** | No (feeding/peso; usos posteriores HI neonatal, cáncer) |
| **GW405833** | Indol | Antagonismo CB1 complejo (JPET 2017); históricamente “CB2-selectivo” | Agonista parcial CB2 (Ki ~3.9 nM hCB2) | Valenzano *Neuropharmacol* 2005 DOI **10.1016/j.neuropharm.2004.12.008**; Dhopeshwarkar *JPET* 2017 DOI **10.1124/jpet.116.236539** | **Sí (reanálisis Janus)** | No (dolor); nota: antiallodinia en KO puede ser CB1-dependiente (contradicción in vivo) |
| **AM1710** | Cannabilactona | Antagonista/inv bajo / agonista arrestina débil en CB1 (JPET) | Agonista CB2 | Dhopeshwarkar *JPET* 2017; Khanolkar *JMC* 2007 DOI **10.1021/jm070441u** | **Sí (Janus complejo)** | No (dolor neuropático) |
| **Qiu-14** | Pirazol adamantil orto-morfolina | Antagonista cAMP | Agonista cAMP | Qiu 2023 + SI Fig. S5 | **Sí (publicado; sin números OA)** | **NOT FOUND** |
| Combo farmacológica CB1-ant + CB2-ago (separados) | — | p.ej. rimonabant | p.ej. JWH133 / O-1966 | Concepto fibrosis Mallat 2007 DOI **10.1517/14728222.11.3.403** | Concepto **sí** | **Propuesto**; no = un solo NCE Janus Qiu |

### ¿Qiu-14 es novedad de concepto o de diseño?

- **Concepto Yin-Yang / Janus:** **NO novedoso** (URB447 2009; JPET 2017).  
- **Diseño structure-guided del switch orto-morfolina en pirazol adamantilo:** **novedad de diseño química** reclamada por Qiu (abstract).  
- **Implicación para Janusforge:** reinventar el *concepto* vía docking es **redundante**; copiar el *diseño* 14 sin números ni disease data es **apuesta cara**.

---

## 3. Familias químicas CB2 — ¿algo hace Janusforge redundante?

| Familia / agente | Estado | Por qué importa |
|------------------|--------|-----------------|
| Agonistas CB2 clásicos (CP55,940, WIN55,212-2, HU-308, JWH) | Tools ubicuos | Benchmarks estructurales (PDB) |
| **Lenabasum (JBT-101)** | CB2 ago clínica; Ph2b CF **falló** primary (Corbus 2020; NCT03451045) | CB2 sola ≠ camino claro a fibrosis clínica |
| **Olorinab (APD371)** | CB2 ago periférico; Ph2a Crohn dolor; Ph2b IBS CAPTIVATE mixed | Familia clínica avanzada **sin** Janus |
| **LEI-102** + estructuras 8GUT | Ago selectivo + cryo-EM 2023 | Diseño CB2 selectivo ya estructuralmente guiado |
| **Zevaquenabant (MRI-1867)** | CB1 periférico + iNOS; fibrosis hígado/pulmón/riñón; Ph1 NCT04531150 | Dual-target fibrosis **más maduro** que Janus Qiu |
| Anticuerpos agonistas CB2 (AB120/AB150, 2026) | Preclínico fibrosis hígado (hPCLS) | Alternativa no-small-molecule |
| URB447 / GW405833 / AM1710 | Tools Janus ya descritos | **Hacen redundante inventar Janus “de cero”** para POC |

**Conclusión bloque 3:** Janusforge no es el único ni el mejor camino; **tool compounds + dual CB1/iNOS** ya cubren gran parte del “por qué dual”.

---

## 4. Inventario experimental CB2 (PDB) — UniProt P34972

Consulta RCSB Search API (2026-08-13), `reference_sequence_identifiers` = **P34972**, experimental: **total_count = 14**.

| PDB | Método | Res. | Ligando / notas | DOI primario | Año |
|-----|--------|------|-----------------|--------------|-----|
| **5ZTY** | X-ray | 2.8 Å | Antagonista **AM10257** (9JU) | 10.1016/j.cell.2018.12.011 | 2019 |
| **6KPC** | X-ray | 3.2 Å | Agonista (serie AM / E3R) | 10.1016/j.cell.2020.01.008 | 2020 |
| **6KPF** | cryo-EM | 2.9 Å | Complejo Gi (mismo paper Hua) | 10.1016/j.cell.2020.01.008 | 2020 |
| **6PT0** | cryo-EM | 3.2 Å | **WIN 55,212-2** + Gi | 10.1016/j.cell.2020.01.007 | 2020 |
| **8GUQ** | cryo-EM | 3.08 Å | CB2–G | 10.1038/s41467-023-37112-9 | 2023 |
| **8GUR** | cryo-EM | 2.84 Å | **CP55,940**–CB2–G | idem | 2023 |
| **8GUS** | cryo-EM | ~3.0 Å | **HU-308**–CB2–G | idem | 2023 |
| **8GUT** | cryo-EM | 2.98 Å | **LEI-102**–CB2–Gi | idem | 2023 |
| **8X3L** | cryo-EM | 3.13 Å | CB2–G; selectividad entropy-driven | 10.1073/pnas.2401091121 | 2024 |
| **9U7L** | cryo-EM | 3.2 Å | PAM **Ec21a** + CP55,940 | 10.1038/s41467-026-72923-6 | 2026 |
| **2KI9** | NMR | — | Hélice 6 fragmento | 10.1016/j.bbrc.2009.04.099 | 2009 |
| **12IY / 12IZ / 12JA** | (en lista UniProt) | — | Entradas legacy/relacionadas en hit list P34972 | Verificar caso a caso antes de usar como plantilla docking | — |

**Corrección crítica:** **8F7V = inhibidor macrocíclico de plasmina**, *no* CB2 (RCSB título; ChemMedChem 2023). Cualquier inventario previo que lo liste como CB2 está **equivocado**.

**No existe** complejo experimental CB2–Qiu-14.

---

## 5. Mutagénesis — experimental vs modelada

| Residuo / tema | Evidencia | Aplica a Qiu-14? |
|----------------|-----------|------------------|
| Hotspots CB2 (F87, F91, F94, H95, F183, W194, S285, etc.) | Mutagénesis + estructuras Li/Hua *Cell* 2019; Xing *Cell* 2020; Li/Hua/van der Stelt *Nat Commun* 2023 | Para **sus** ligandos |
| S285<sup>7.39</sup> | Contactos estructurales + mutaciones en literatura (p.ej. Rhee 2002; estructuras 2023) | **No** prueba H-bond de Qiu-14 |
| S173 CB1 (claim Qiu) | Propuesto por docking/MD Qiu | **Modelado** para 14 |
| Mutantes diseñados para validar Yin-Yang 14 | **NOT FOUND** en open text | Hueco |

**Regla:** mutagénesis de la literatura CB2 **no se puede reutilizar como validación del mecanismo Qiu-14** sin experimento dedicado.

---

## 6. Compute validado experimentalmente en CB2 — hit rates

| Estudio | Método | Hit rate / éxito | DOI | Nota |
|---------|--------|------------------|-----|------|
| Sadybekov et al. 2022 | V-SYNTHES docking giga-library → antagonistas CB | **~33%**; 14 sub-µM | 10.1038/s41586-021-04220-9 | Binding; no Janus fibrosis |
| Xing et al. 2021 | DL–pharmacophore–docking ChemDiv | **7/15** affinity (pKi 5.15–6.66); subset antag cAMP | 10.3390/molecules26216679 | Antagonistas |
| Szymczak et al. 2023 | VS 7M → 16 testados | **2/16** antagonistas novel (Ki 65 & 210 nM) | 10.1021/acs.jcim.2c01503 | ~12.5% hits útiles |
| Ge et al. 2023 | LRIP function-based + síntesis | Abstract: **~70%** success rate función en serie diseñada | 10.1021/acschemneuro.3c00580 | Función ago/antag **dentro de diseño racional**, no VS ciego |

**Implicación destroy:** hit rates existen y son modestos–buenos **para binding/función mono-target**. **Ninguno** demuestra que docking prediga *simultáneamente* CB1-ant + CB2-ago + eficacia fibrosis. Docking≠actividad; MM-GBSA Qiu = correlación interna, no validación externa.

---

## 7. Fibrosis CB1/CB2 — in vitro / in vivo / humano; novedad combo Janus

| Nivel | Hallazgo | Fuente | Tipo |
|-------|----------|--------|------|
| Humano (expresión) | CB1/CB2 up en hígado cirrótico / células fibrogénicas | Julien 2005; Teixeira-Clerc 2006 | Experimental (tejido) |
| In vivo CB2 | KO CB2 → más fibrosis CCl₄; agonismo antifibrogénico en HSC | Julien *Gastroenterology* 2005 DOI **10.1053/j.gastro.2004.12.050** | Experimental |
| In vivo CB1 | Antagonismo/KO CB1 ↓ fibrosis (varios modelos) | Teixeira-Clerc *Nat Med* 2006 DOI **10.1038/nm1421** | Experimental |
| Concepto combo | “CB2 agonists + CB1 antagonists” como estrategia | Mallat *Expert Opin Ther Targets* 2007 DOI **10.1517/14728222.11.3.403** | Review/opinión experta |
| Dual CB1/iNOS | MRI-1867 superior a solo CB1 o solo iNOS; hígado/pulmón/riñón; hPCLS | Cinar *JCI Insight* 2016; Cinar et al. *JCI Insight* 2025 DOI insight.jci.org/articles/view/187967 | Experimental + traslacional |
| Humano clínico CB2 | Lenabasum CF Ph2b **no primary** | Corbus PR 2020; NCT03451045 | Experimental clínica **negativa** |
| Humano CB1 | Rimonabant retirado (psiquiatría) — no fibrosis approval | Histórico regulatorio | Seguridad |
| Qiu-14 fibrosis | **NOT FOUND** | PubMed probes 0P/esta auditoría | Ausencia |
| Janus monomolecular fibrosis | Claim en **patente** WO2022026478; no = fármaco aprobado | Texto local `WO2022026478_text.txt` | Patente ≠ validación |

**Novedad Janus-combo para fibrosis:** el *concepto* **no es nuevo (2007 + patente)**. Un NCE pirazol Qiu-like **específico** para fibrosis **no está demostrado**. Eso no justifica docking; como máximo justifica tool-compound wet test.

---

## 8. Landscape de patentes preliminar (2000–2026) — semáforo (≠ FTO)

| Familia / tema | Semáforo | Notas |
|----------------|----------|-------|
| Mixed **CB1-ant / CB2-ago** para fibrosis (Makriyannis WO**2022026478** / US**20230234928**) | 🔴 | Inventario conceptual/claims overlapping con “Janus fibrosis”; scaffolds distintos a Qiu-14 en texto local, pero **espacio claim amplio** (pirazoles mencionados) |
| CB1 antag / inverse (Sanofi rimonabant family et al.) | 🟡 | Arte saturado; CNS liability conocida |
| CB2 selectivos clínicos (Arena/Corbus etc.) | 🟡 | Freedom depende de claims concretos |
| Qiu-14 / Tao composition filing | 🟢/❓ | **NOT FOUND** en probes abiertos; posible CNIPA no scrapeado |
| Photoswitch Qiu 2026 | 🟡 | Follow-on autores; no FTO |

**Disclaimer legal:** esto **no es FTO**. Semáforo = riesgo de solapamiento temático para decisión de gasto R&D.

---

## 9. Disponibilidad / comercial

| Compuesto | Comercial / accesible? | Fuente |
|-----------|------------------------|--------|
| **Qiu-14 / 15 / 20 / 24** | **NOT FOUND** como catálogo (PubChem CID vacío) | Ausencia |
| **URB447** | Sí (p.ej. SCBT CAS **1132922-57-6**; IC50 citados en ficha) | Vendor |
| **GW405833** | Sí (Cayman, Sigma, Tocris/R&D 2374; CAS **180002-83-9**) | Vendor |
| **AM1710** | Limitado / custom (CAS **335371-36-3**; MedKoo “not in stock”, BOC lista) | Vendor parcial |
| Controles CP55,940 / rimonabant / WIN | Ubicuos | Vendor |

**Implicación ahorro:** POC Janus+fibrosis se puede plantear con **URB447 ± GW405833** sin sintetizar Qiu-14.

---

## 10. Tabla maestra

| QUESTION | ALREADY ANSWERED? | EVIDENCE | QUALITY | NEED REPEAT? |
|----------|-------------------|----------|---------|--------------|
| ¿Existe Yin-Yang/Janus CB1-ant/CB2-ago? | **SÍ** | URB447 2009; JPET 2017; Qiu 2023 | Alta (multi-lab para concepto) | **NO** reinventar concepto |
| ¿Qiu-14 sintetizado? | **SÍ** | SI Scheme S1 + HPLC/NMR | Media-alta (un lab) | No resintetizar hasta ver números |
| ¿Potencia nM de Qiu-14? | **NO (público)** | Paywall main tables | Bloqueado | Obtener PDF / email autores |
| ¿Binding Ki CB1/CB2 de 14? | **NO** | Ausente en SI abierto | — | Solo si se avanza wet |
| ¿Mecanismo S173/S285 para 14? | **NO experimentalmente** | Solo docking/MD | Baja para decision | Mutagénesis solo si lead avanza |
| ¿Qiu-14 funciona in vivo / fibrosis? | **NO** | NOT FOUND | — | Solo tras potencias útiles |
| ¿Estructuras CB2 bastan para diseño? | **SÍ (abundantes)** | PDB P34972 ×14 | Alta | No más “descubrir bolsillo” |
| ¿Docking predice hits CB2? | **Parcialmente** | Hit rates 12–33% (VS); ~70% función en Ge serie | Media | No campañas masivas Janusforge |
| ¿Combo CB1↓+CB2↑ antifibrosis es idea nueva? | **NO** | Mallat 2007; WO2022026478 | Alta (concepto) | No |
| ¿CB2 ago clínico en fibrosis funciona? | **Dudoso/negativo parcial** | Lenabasum CF Ph2b fail | Alta (clínica) | No asumir CB2 = fibrosis win |
| ¿Hay FTO para Qiu-14? | **NO evaluado** | Patente ≠ FTO; Qiu filing NOT FOUND | Baja | Counsel solo si hay lead |
| ¿Janusforge docking/MD añade valor ahora? | **NO demostrado** | Redundancia + bans + paywall | — | **NO** |

---

## 11. Qué se puede AHORRAR / HACER / HACER SOLO SI X

### AHORRAR (parar ya)

- Docking / MD / pose campaigns / pharmacophore “discovery” de Yin-Yang.  
- Resíntesis de la serie Qiu “por si acaso”.  
- Diseño NCE masivo / virtual screening giga para Janus fibrosis.  
- Mutagénesis S173/S285 “para confirmar docking Qiu” antes de potencias.  
- Re-preparar receptores / grids “porque 8F7V” u otros PDBs erróneos.

### HACER (barato, alto valor de información)

1. **Email autores** (Tao / Yang / Zhao) pidiendo tabla de potencias 14/15/20/24 o PDF compliant.  
2. Si no hay respuesta: **comprar 1 artículo** Elsevier (~decenas USD / acceso institucional).  
3. Inventario de compra **URB447 + GW405833** (y controles) como tools.  
4. Lectura FTO *light* solo de WO2022026478 claims vs chemotipo pirazol-orto-morfolina (abogado, no docking).  
5. Decisión binaria post-números: ¿EC50/IC50 en rango útil (<~100–300 nM ambos brazos)? si no → stop.

### HACER SOLO SI X

| Acción | Condición X |
|--------|-------------|
| Ensayo fibrosis in vitro (HSC / PCLS) con tool Janus | X = URB447/GW accesibles **y** endpoint fibrosis ya validado en lab |
| Resíntesis Qiu-14 | X = números Qiu nM **y** tools no bastan (selectividad/PK) |
| Mutagénesis mecanismo | X = lead wet con dual profile robusto |
| Cualquier compute pose | X = **prohibido por brief actual**; solo endurecimiento local de código si el usuario lo pide aparte |
| In vivo fibrosis | X = in vitro positivo + PK/tox mínimas + counsel patente |

---

## 12. Máximo 5 gaps reales (con experimento / coste / alternativa compute)

| # | Gap real | Experimento que lo cierra | Coste orden | Alternativa compute? |
|---|----------|---------------------------|-------------|----------------------|
| 1 | Potencias numéricas Qiu-14/15/20/24 | PDF / email / BindingDB si aparece | **$0–50** | **No** — paywall no se “dockea” |
| 2 | Réplica independiente dual cAMP/βarr de un Janus tool | CRO assay panel CB1/CB2 en URB447 o GW405833 | **$2–8k** | No |
| 3 | ¿Janus tool antifibrótico in vitro? | HSC activadas o hPCLS + marcadores colágeno/αSMA | **$5–20k** | No |
| 4 | ¿Qiu-14 patentado en CN? | Búsqueda CNIPA + counsel | **$1–5k** | No |
| 5 | Mecanismo ortostérico de un lead real | Mutagénesis dirigida post-lead | **$10–30k** | Modelado solo como hipótesis, no decisión |

*(Si tras 1–3 la señal es negativa: el gap “diseñar mejor NCE Janus” **no justifica gasto** — es un pozo.)*

---

## 13. GO / NO-GO — clasificación A–E

| Código | Significado operativo |
|--------|----------------------|
| **A** | GO fuerte: hipótesis intacta, gastar en path actual |
| **B** | GO condicional: gates baratos, luego wet acotado |
| **C** | HOLD: congelar diseño; solo adquisición de datos públicos |
| **D** | NO-GO del path/hipótesis actual; espacio no necesariamente muerto |
| **E** | NO-GO del espacio terapéutico completo |

### Clasificación 0Q: **D**

**Justificación crítica (destroy):**

1. El **concepto Janus** ya estaba resuelto (URB447 2009; GW/AM 2017).  
2. El **concepto combo fibrosis CB1↓+CB2↑** ya estaba publicado (2007) y patentado (WO2022026478).  
3. Qiu-14 aporta **diseño químico Yin-Yang**, no prueba de enfermedad; potencias **paywalled**; mecanismo **computacional**.  
4. Estructuras CB2 **sobran** (hasta PAM 2026); no hay déficit estructural que cure un programa de docking.  
5. Clínica CB2 (lenabasum) y toxicidad CB1 central **destruyen la narrativa ingenua** “agoniza CB2 + antagoniza CB1 → fármaco fibrosis”.  
6. Por tanto: **NO-GO a Janusforge-como-motor-de-diseño-NCE/docking**.  

**Puerta estrecha (no A/B del programa compute):** si tras obtener números Qiu y un test barato con URB447 hay señal fibrosis, el proyecto podría **reabrirse como B wet-tool**, no como campaña de docking. Eso sería un **proyecto distinto**.

**Por qué no E:** zevaquenabant, datos Lotersztajn y PAMs CB2 muestran que el eje endocannabinoide en fibrosis **no está muerto** — solo que **esta hipótesis de ejecución está destruida**.

---

## 14. Bibliografía (enlaces)

1. Qiu et al. (2023) *Bioorg. Chem.* — https://doi.org/10.1016/j.bioorg.2023.106377 — PMID https://pubmed.ncbi.nlm.nih.gov/36731294/  
2. Qiu et al. SSRN preprint — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4276225  
3. LoVerme et al. (2009) URB447 — https://doi.org/10.1016/j.bmcl.2008.12.059 — PMC https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3690177/  
4. Dhopeshwarkar et al. (2017) Janus GW405833/AM1710 — https://doi.org/10.1124/jpet.116.236539  
5. Valenzano et al. (2005) GW405833 — https://doi.org/10.1016/j.neuropharm.2004.12.008  
6. Julien et al. (2005) CB2 antifibrogenic — https://doi.org/10.1053/j.gastro.2004.12.050  
7. Teixeira-Clerc et al. (2006) CB1 antagonism fibrosis — https://doi.org/10.1038/nm1421  
8. Mallat et al. (2007) combo strategy review — https://doi.org/10.1517/14728222.11.3.403  
9. Li et al. (2019) CB2 crystal 5ZTY — https://doi.org/10.1016/j.cell.2018.12.011  
10. Xing et al. (2020) CB2–Gi 6PT0 — https://doi.org/10.1016/j.cell.2020.01.007  
11. Hua et al. (2020) 6KPC/6KPF — https://doi.org/10.1016/j.cell.2020.01.008  
12. Li et al. (2023) 8GUR/8GUS/8GUT — https://doi.org/10.1038/s41467-023-37112-9  
13. Shen et al. (2024) 8X3L — https://doi.org/10.1073/pnas.2401091121  
14. Wang et al. (2026) 9U7L PAM — https://doi.org/10.1038/s41467-026-72923-6  
15. Sadybekov et al. (2022) V-SYNTHES — https://doi.org/10.1038/s41586-021-04220-9  
16. Xing et al. (2021) VS CB2 antag — https://doi.org/10.3390/molecules26216679  
17. Szymczak et al. (2023) VS CB2 — https://doi.org/10.1021/acs.jcim.2c01503  
18. Ge et al. (2023) LRIP CB2 — https://doi.org/10.1021/acschemneuro.3c00580  
19. Cinar et al. (2016) MRI-1867 liver fibrosis — https://doi.org/10.1172/jci.insight.87336  
20. Cinar et al. (2025) CB1 AM pulmonary fibrosis / zevaquenabant — https://doi.org/10.1172/jci.insight.187967  
21. WO2022026478 — https://patents.google.com/patent/WO2022026478A1  
22. US20230234928 — https://patents.google.com/patent/US20230234928A1  
23. Lenabasum CF Ph2b (Corbus) — https://ir.corbuspharma.com/news-events/press-releases/detail/342/corbus-pharmaceuticals-announces-phase-2b-study-of-lenabasum-for-treatment-of-cystic-fibrosis-did-not-meet-primary-endpoint — NCT03451045 https://clinicaltrials.gov/study/NCT03451045  
24. Qiu/Tao photoswitch 2026 — https://doi.org/10.1016/j.ejmech.2026.118883  
25. RCSB entries — https://www.rcsb.org/structure/5ZTY · 6PT0 · 6KPC · 8GUR · 9U7L  

### Locales consultados (secundarios / SI)

- `data/papers/mmc1_document.txt`, `data/papers/qiu_2023_bioorg/mmc1_fulltext_deep.txt`, `data/papers/image15_ocr.txt`  
- `data/papers/qiu_2023_bioorg/api/WO2022026478_text.txt`, `US20230234928_text.txt`  
- `data/papers/qiu_2023_bioorg/api/external0p/pdb_*.json`  
- Nota secundaria (no autoridad): `results/reports/qiu_0p_external_evidence_table.md`

---

*Fin 0Q. Auditoría independiente orientada a destruir la hipótesis de gasto; gap residual = potencias Qiu + POC wet con tools comerciales, no compute.*

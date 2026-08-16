# 0Q-SMRF — Auditoría histórica del “molecular switch” (CB1/CB2)

**Fecha:** 2026-08-13  
**Workstream:** Option **B** — `0Q-SMRF = ACTIVE`  
**Option A:** `0M = RESERVE` (wet H1-a handoff packaged but not critical path while SMRF runs)  
**Contexto separado:** auditoría 0Q independiente = **D NO-GO** para path docking-NCE (`qiu_0q_independent_scientific_audit.md`); SMRF no reabre docking/NCE.  
**Bans:** sin NCE; sin docking/MD nuevos; sin inferir mecanismo solo desde estructura; no mezclar binding↔función, IC50↔EC50, antagonismo↔inactividad, pérdida de actividad↔steric clash, docking↔evidencia experimental.  
**Hipótesis tabular Qiu-14/15/20/24** (p.ej. “96%→antagonist 0.04 µM”, “steric clash” para 24): **WORKING HYPOTHESIS ONLY** — cada número verificado en Qiu 2023 + SI; si no aparece → **NOT FOUND / TBD**. No se copia como hecho.

**Machine-readable pairs:** [`qiu_0q_smrf_pairs.csv`](qiu_0q_smrf_pairs.csv)

---

## Status lock

| Option | Track | Status |
|--------|-------|--------|
| **A** | 0M wet H1-a handoff | **RESERVE** |
| **B** | 0Q-SMRF historical switch matrix | **ACTIVE** |

---

## Final verdict

### `0Q-SMRF = MODERATE`

| Claim | Support | Primary refs |
|-------|---------|--------------|
| Existen ligandos **Janus / Yin-Yang** (CB1-ant/inv + CB2-ago) en **varios scaffolds** | **Sí (experimental, multi-lab)** | LoVerme 2009 URB447; Dhopeshwarkar 2017 GW405833/AM1710; Qiu 2023 cpd 14 (cualitativo SI) |
| Existe **switch estructural reproducible ago↔inv/ant en CB2** (toggle Trp6.48) | **Sí (experimental + cristal/cryo-informed; multi-serie)** | Li/Hua 2019 MRI2687↔MRI2594; Soethoudt/Carreira-type HU-308→(R)-1 2024 |
| El **N1-orto-morfolina Qiu** es un switch Yin-Yang **reproducido** con potencias abiertas multi-par | **No verificado en OA** | Qiu abstract + SI Fig. S5 solo para 14; 15/20/24 números **NOT FOUND** |
| Relación única “una modificación → CB1-ant + CB2-ago” universal | **NOT SUPPORTED** | Janus aparece por caminos químicos distintos; no hay un solo switch compartido |
| Mecanismo Qiu S173/S285 H-bond | **COMPUTATIONAL only** | Qiu abstract; SI docking/MD Figs. S6–S10 |

---

## Workflow 0Q.1 → 0Q.5 (resumen)

### 0Q.1 — Hechos sin “por qué”
Inventario molécula→estructura→mod→ensayo→CB1→CB2→resultado (ver matriz §4 y CSV). Ningún número Qiu de la tabla-hipótesis entró como hecho.

### 0Q.2 — Pares preferidos
Prioridad a cambio de **una región**, mismo lab/plataforma, ensayos funcionales comparables. Mejores: MRI2687/MRI2594; HU-308 / ago-3 vs (R)-1; Qiu-14 vs regioisomeros (identidad sí; fenotipo B incompleto OA).

### 0Q.3 — Etiquetas de fenotipo
Solo: `CB1 ago` / `CB1 ant/inv` / `CB2 ago` / `CB2 ant/inv` / `inactive` / `ambiguous`.  
**Nunca** convertir Ki/IC50 de binding en agonismo.

### 0Q.4 — Mecanismo después de datos
Etiquetado `EXPERIMENTAL` / `COMPUTATIONAL` / `INFERRED`.

### 0Q.5 — ¿Existe switch reproducible?
- **Mono-CB2 ago↔inv/ant:** **sí** (A-class, multi-pair).  
- **Dual opuesto CB1/CB2 (Yin-Yang):** **fenotipo existe**; **regla estructural única reproducible: no**.  
- **Switch Qiu N1-orto-morfolina como ley SAR abierta:** **débil / incompleto** (un ancla experimental; pares sin potencias OA).

---

## Counts

| Bucket | n |
|--------|---|
| **Pares verificados** (ambos extremos con evidencia experimental usable; o Janus documentado con parámetros tipados) | **11** |
| **Pares rechazados / solo-hipótesis** (números no hallados, docking-as-fact, steric clash no experimental) | **7** |
| Clase **A** (cambio funcional experimental, multi-par / reproducido) | **2** (+1 serie HU con múltiples sondas) |
| Clase **B** (señal experimental aislada o Janus sin SAR-pair cerrado) | **6** |
| Clase **C** (correlación débil / fenotipo B incompleto OA) | **4** |
| Clase **D** (solo computacional) | **3** (mecanismos / colisiones docking Qiu) |

---

## Hypothesis table — REJECTED as fact (Qiu 14/15/20/24)

| Alleged claim | Verification (Qiu 2023 OA + local SI) | Status |
|---------------|----------------------------------------|--------|
| Numeric potencies (Ki/IC50/EC50/%) for 14/15/20/24 as in prior paste | Main PDF paywalled; SI tables = MM-GBSA only; curve OCR sin EC50 anotado | **NOT FOUND** |
| “96% → antagonist 0.04 µM” (o similares) | No aparece en abstract, SI captions, ni OCR de curvas | **REJECT — hypothesis-only** |
| “Steric clash” causa fenotipo de **24** | Fig. S6 habla de colisiones **meta/para morph (15/16)** en docking CB1 — **COMPUTATIONAL**; no es evidencia experimental de 24 | **REJECT as experimental fact** |
| H-bond S173 (CB1) / S285 (CB2) explica Yin-Yang de 14 | Abstract: “based on the docking study and molecular dynamic simulation” | **COMPUTATIONAL** |
| Binding Ki dual para 14 | SI abierto | **NOT FOUND** |

**Identidades estructurales verificadas (SI Scheme S1 / OCR `image15_ocr.txt`):**

| Cpd | Estructura (experimental SI) |
|-----|------------------------------|
| **14** | N1-Ph **orto-morpholinyl**; C3-amide = **1-adamantyl** |
| **15** | N1-Ph **meta-morpholinyl**; C3 = 1-adamantyl |
| **16** | N1-Ph **para-morpholinyl**; C3 = 1-adamantyl |
| **20** | N1-Ph **orto-4-methylpiperazinyl**; C3 = 1-adamantyl |
| **24** | N1-Ph **orto-morpholinyl**; C3 = **CH₂-1-adamantyl** |

**Fenotipo 14 verificado (funcional):** SI Fig. S5 — CB2 **agonist** cAMP/HTRF (ctrl CP55,940); CB1 **antagonist** cAMP/HTRF (ctrl rimonabant); n=3×triplicado. **EC50/IC50/Emax numéricos: NOT FOUND en OA.**

---

## Top switches (A / B)

### Clase A (reproducibles / multi-evidencia)

1. **MRI2687 → MRI2594** (arm-1 / core size toward Trp2586.48)  
   - Fenotipo: **CB2 ant/inv → CB2 ago** (funcional)  
   - Estructura cristal CB2–AM10257 informa el modelo; par diseñado + ensayado  
   - DOI: [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011)  
   - **No es Yin-Yang CB1/CB2**; es switch **intra-CB2**.

2. **HU-308 / ago-3 → (R)-1** (adición de fenilo C(2′) en cadena gem-dimetil)  
   - Fenotipo: **CB2 ago → CB2 ant/inv** (cAMP, Gi BRET, sin β-arrestin; multi-panel)  
   - (R)-1: Kd CB2 **39.1 nM**; cAMP pEC50 **6.95**, Emax **−44%** (vs basal/agonist norms del paper)  
   - ago-3 (sin fenilo C2′): cAMP pEC50 **8.47**, Emax **112%**  
   - DOI: [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461)  
   - Serie con múltiples sondas = **reproducción dentro de familia**.

### Clase B (señales Janus / Yin-Yang experimentales; no = regla SAR única)

| Switch / caso | Scaffold | Fenotipo | Parámetros tipados | DOI |
|---------------|----------|----------|--------------------|-----|
| **URB447** (vs 5b inactivo / 8a débil binding) | pirrol | CB1 **neutral ant** + CB2 **ago** | Binding IC50 rat CB1 **313±72 nM**, hCB2 **41±23 nM**; GTPγS CB1 ant EC50 **4.9±0.8 µM**; cAMP CB2 ago a 1 µM | [10.1016/j.bmcl.2008.12.059](https://doi.org/10.1016/j.bmcl.2008.12.059) |
| **GW405833** | aminoalkylindole / oxazinoindole-class indol | CB2 **ago** + CB1 **noncomp. ant** (reanálisis) | Ki hCB2 **3.92±1.58 nM**, Ki CB1 **4772±1676 nM** (Valenzano); ant CB1 multi-pathway (JPET) | [10.1016/j.neuropharm.2004.12.008](https://doi.org/10.1016/j.neuropharm.2004.12.008); [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539) |
| **AM1710** | cannabilactona | CB2 **ago** + CB1 **low-pot. ant/inv** (arrestina compleja) | Ki hCB2 **6.7 nM**; Ki rat CB1 **360 nM**; CB2 cAMP EC50 **11 nM**, Emax **48%** (cit. JPET) | [10.1021/jm070441u](https://doi.org/10.1021/jm070441u); [10.1124/jpet.116.236539](https://doi.org/10.1124/jpet.116.236539) |
| **Qiu-14** | pirazol adamantil | CB1 **ant** + CB2 **ago** (cAMP) | Parámetros numéricos **NOT FOUND** OA; dirección experimental SI S5 | [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377) |
| **AM10257** (molécula única) | pirazol | CB2 **inv/ant** + CB1 **ago** (opuesto a Yin-Yang Qiu) | Ki CB2 **0.08 nM**; perfil funcional CB2 inv + CB1 ago reportado | [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011) |
| **Azo23** cis/trans (autores Qiu/Tao) | azo photoswitch | Opposite control CB1/CB2 (claim) | Quimiotipo ≠ 14/15/20/24; potencias exactas no auditadas aquí en full text | [10.1016/j.ejmech.2026.118883](https://doi.org/10.1016/j.ejmech.2026.118883) |

---

## SMRF matrix (columnas 1–17)

Convenciones: `PARAM:` etiqueta obligatoria; `NF` = NOT FOUND; `TBD` = needs main PDF; `INFERRED` = no de autores.

### Bloque Qiu 2023 (prioridad 1)

| # | A | B | scaffold | exact mod | region | CB1 assay | CB1 result | CB2 assay | CB2 result | EC50/IC50/Emax | same assay/lab | exp evid | struct evid | mutag | mech authors | mech later | DOI |
|---|---|---|----------|-----------|--------|-----------|------------|-----------|------------|----------------|----------------|----------|-------------|-------|--------------|------------|-----|
| Q1 | Qiu-14 | Qiu-15 | pyrazole-3-carboxamide | o-morph → m-morph on N1-Ph | **N1-regio** | cAMP/HTRF ant (S5/S11) | **14:** CB1 ant/inv (func); IC50 **NF**. **15:** curve S11; phenotype/IC50 **NF** | cAMP/HTRF ago (S5/S13) + ant panel S12 | **14:** CB2 ago (func); EC50/Emax **NF**. **15:** panels present; phenotype **NF** | **which:** EC50/IC50/Emax all **NF** OA | yes (Qiu lab) | yes (assays) | no for complex; ligand crystals ≠14/15 | no for pair | N1-Ph arm = switch; o-morph → Yin-Yang; meta collisions (**docking**) | steric clash as cause of loss = **INFERRED/COMPUTATIONAL** | 10.1016/j.bioorg.2023.106377 |
| Q2 | Qiu-14 | Qiu-16 | same | o-morph → p-morph | **N1-regio** | cAMP ant | 14: CB1 ant; 16: curve S11, phenotype **NF** | cAMP ago/ant panels | 14: CB2 ago; 16: **NF** phenotype | all **NF** | yes | yes | no | no | para collisions (**docking** S6) | same | same |
| Q3 | Qiu-14 | Qiu-20 | same | o-morph → o-4-Me-piperazinyl | **N1** | cAMP ant | 14: CB1 ant; 20: curve S11, phenotype **NF** | cAMP ago/ant | 14: CB2 ago; 20: **NF** | all **NF** | yes | yes | no | no | docking poses S7 | **INFERRED** SAR | same |
| Q4 | Qiu-14 | Qiu-24 | same | CONH–Ad → CONH–CH₂–Ad | **C3** | cAMP ant | 14: CB1 ant; 24: curve S11, phenotype **NF** | cAMP ago/ant | 14: CB2 ago; 24: **NF** | all **NF** | yes | yes | no | no | authors discuss Ad homologs in series | “steric clash 24” as fact = **REJECT** (not in SI as experiment) | same |
| Q5 | Qiu-15 | Qiu-16 | same | m-morph → p-morph | **N1-regio** | cAMP ant | both curves; phenotypes **NF** | cAMP panels | **NF** | **NF** | yes | yes (curves) | no | no | docking collisions meta/para | **INFERRED** | same |

**Clase:** Q1–Q4 = **C** para claim Yin-Yang switch multi-par (ancla 14 = B); Q5 = **C/D**.  
**Nota S11 OCR:** paneles listan 5–13, 15–30; **cpd 14 ausente en S11 OCR** (cubierto en S5).

### Bloque Janus cross-scaffold (prioridad 2)

| # | A | B | scaffold | exact mod | region | CB1 assay | CB1 result | CB2 assay | CB2 result | EC50/IC50/Emax | same lab | exp | struct | mut | mech authors | mech later | DOI |
|---|---|---|----------|-----------|--------|-----------|------------|-----------|------------|----------------|----------|-----|--------|-----|--------------|------------|-----|
| J1 | 5b (des-N1-pClBn) | URB447 | pyrrole | add N1-p-chlorobenzyl (+ keep 4-NH₂ / 3-benzoyl) | **N1** | rat CB1 binding + GTPγS | 5b: inactive binding (authors); URB447: IC50 **313±72 nM**; GTPγS ant EC50 **4.9±0.8 µM** (neutral ant) | hCB2 binding + mCB2 cAMP | URB447 IC50 **41±23 nM**; cAMP ↓ (ago) at 1 µM | **IC50** (binding) + **EC50** GTPγS + cAMP qualitative | yes (LoVerme) | yes | no | no | polar 4-NH₂ enables dual affinity; peripheral restriction | Janus concept first declared | 10.1016/j.bmcl.2008.12.059 |
| J2 | 8a (3-benzoyl, no 4-NH₂) | URB447 | pyrrole | introduce 4-NH₂ | **other** (C4) | binding | 8a: weak CB2 / limited; URB447 dual IC50 as above | binding | URB447 IC50 41 nM | **IC50** binding | yes | yes (binding); func mainly URB447 | no | no | 4-NH₂ favorable at both sites | dual func of 8a **NF** → pair class **B/C** | same |
| J3 | GW405833 | (historical “CB2-selective” label) | indole | n/a (phenotype reanalysis) | other | HEK CB1: AC, ERK, PIP2, internalization, arrestin | CB1 **ant** (noncomp.); arrestin time-dependent **ambiguous** | CHO/hCB2 binding + ago legacy | CB2 **ago** (partial / protean literature) | Ki CB2 **3.92 nM**; Ki CB1 **4772 nM**; vendor EC50s not used as primary | no (multi-lab) | yes | no ligand-CB crystal for GW | no for Janus claim | originally CB2-selective ago | Janus = **EXPERIMENTAL** reanalysis 2017 | 10.1124/jpet.116.236539 |
| J4 | AM1710 | (same) | cannabilactone | n/a | other | CB1 pathways JPET | CB1 **ant/inv** low pot.; arrestin **weak ago** → phenotype **ambiguous** on arrestin | CB2 cAMP | CB2 **ago** EC50 **11 nM**, Emax **48%** | Ki / EC50 / Emax labeled | no | yes | no | no | CB2-selective tool historically | Janus complex | 10.1021/jm070441u + 10.1124/jpet.116.236539 |

### Bloque CB2 toggle switches (prioridad 3–7; función mono-receptor)

| # | A | B | scaffold | exact mod | region | CB1 assay | CB1 result | CB2 assay | CB2 result | EC50/IC50/Emax | same lab | exp | struct | mut | mech authors | mech later | DOI |
|---|---|---|----------|-----------|--------|-----------|------------|-----------|------------|----------------|----------|-----|--------|-----|--------------|------------|-----|
| T1 | MRI2687 | MRI2594 | thiazole (A-836339-related) | arm-1 bulk: 6-Me-benzothiazole ↔ 4,5-dimethylthiazole | **other** (arm1 / toggle contact) | not the switch focus | CB1 not claimed as switch driver | AC / functional CB2 | **2687:** CB2 **ant/inv**; **2594:** CB2 **ago** | numeric EC50 pair in main fig (paper); use paper tables for exact — direction verified | yes (Li/Hua) | yes | yes (5ZTY informs; docking of pair) | yes (CB2 mutagenesis in paper) | arm1 length toggles Trp2586.48 | — | 10.1016/j.cell.2018.12.011 |
| T2 | HU-308 / ago-3 | (R)-1 | cannabilactone / HU-308 | add C(2′) phenyl on side chain | **other** | selectivity binding | CB2-selective; CB1 weak | cAMP HTRF + Gi BRET + arrestin | ago-3: **CB2 ago**; (R)-1: **CB2 ant/inv** | ago-3: pEC50 **8.47**, Emax **112%** (cAMP); (R)-1: pEC50 **6.95**, Emax **−44%**; Kd **39.1 nM** | yes | yes | crystal-informed + MD (**COMP** for mechanism detail) | related literature mut on toggle | phenyl engages Trp2586.48 | MD corroboration = **COMPUTATIONAL** | 10.1021/acscentsci.3c01461 |
| T3 | Ge-6 | Ge-39 | Ge 2023 series | multi-mod (not single-region guaranteed) | other | CB1 selectivity reported in series | selective CB2 focus | in vitro functional | **6:** CB2 **ago**; **39:** CB2 **ant** | abstract: LRIP design; ~70% function success — pair not single-atom switch | yes | yes | no | hotspot residues discussed | LRIP / residue interaction profiles (**COMP** design + wet confirm) | — | 10.1021/acschemneuro.3c00580 |

### Single-molecule opposite dual (not a SAR pair)

| # | A | B | note | CB1 | CB2 | class | DOI |
|---|---|---|------|-----|-----|-------|-----|
| S1 | AM10257 | — | pyrazole from rimonabant optimization (N1 alkyl + C3 Ad) | **CB1 ago** (reported) | **CB2 inv/ant** (Ki 0.08 nM; AC Schild logKB −8.30) | **B** (opposite Janus vs Qiu) | 10.1016/j.cell.2018.12.011 |

---

## Classification A–D (alleged switches)

| ID | Alleged switch | Class | Why |
|----|----------------|-------|-----|
| T1 | MRI2687↔MRI2594 CB2 ago/inv | **A** | Experimental functional pair + structure + mutagenesis context |
| T2 | HU-308→(R)-1 CB2 ago→inv | **A** | Multi-assay; multiple probes reproduce inv profile |
| J1 | URB447 Janus emergence | **B** | Clear dual experimental; limited matched functional SAR pairs |
| J3/J4 | GW405833 / AM1710 Janus | **B** | Experimental; not designed as Qiu-like N1 switch |
| Q0 | Qiu-14 Yin-Yang | **B** | Experimental cAMP both arms; single lab; numbers OA **NF**; no independent replica |
| Q1–Q4 | Qiu N1/C3 as Yin-Yang toggle | **C** | Structures + assays exist; comparator phenotypes/potencies OA **NF** |
| D1 | S173/S285 H-bond | **D** | Docking/MD only |
| D2 | meta/para steric clash (15/16) as experimental mechanism | **D** | SI Fig. S6 docking |
| D3 | “steric clash” for Qiu-24 as fact | **D / REJECT** | Not experimental evidence in OA SI |
| HX | Numeric hypothesis table 14/15/20/24 | **REJECT** | Numbers not found |

---

## Answers (brief 0Q.5)

1. **¿Existe un molecular switch de verdad?**  
   **Sí, en sentido restringido:** modificaciones locales pueden cambiar **función CB2** ago↔inv/ant de forma reproducible (toggle Trp6.48).  
   **Parcial** para **Yin-Yang dual** CB1-ant/CB2-ago: el *fenotipo* existe en varios chemotipos; **no** hay una regla estructural única verificada.

2. **¿Específico del scaffold Qiu?**  
   Autores proponen N1-Ph como switch; **solo cpd 14** tiene Yin-Yang **cualitativo** verificado en SI abierto. **No** hay multi-par abierto con potencias que demuestre que *orto-morfolina* es condición necesaria/suficiente.

3. **¿Across scaffolds?**  
   **Janus fenotipo:** sí (pirrol, indol, cannabilactona, pirazol).  
   **Misma modificación química:** **no**.

4. **Modificaciones más fuertes (evidencia):**  
   - Contacto/bulk hacia **Trp6.48** (arm1 / C2′-Ph) → ago↔inv **CB2**.  
   - Polar N / N1-bencilo en serie URB → aparición de dual affinity + Janus func.  
   - **o-Morpholinyl** Qiu → Yin-Yang **candidato** (B), no ley A.

5. **Qué no se reproduce / no verifica:**  
   - Tabla numérica hipótesis Qiu.  
   - Steric clash de **24** como hecho.  
   - S173/S285 como mecanismo experimental.  
   - Un único switch N1 que genere Yin-Yang en todos los scaffolds.

6. **Qué contradice la hipótesis operativa “switch Qiu = path de diseño”:**  
   - Janus ya existía (2009/2017) sin pirazol-orto-morfolina.  
   - AM10257 muestra **opuesto** (CB2-ant / CB1-ago) en pirazol relacionado.  
   - GW405833: antiallodinia in vivo puede ser **CB1-dependiente** pese a label CB2 (contradicción traslacional).  
   - Paywall: no se puede rankear 14 vs 15/20/24 con evidencia abierta.

7. **Ya resuelto en literatura:**  
   - Existencia de Yin-Yang/Janus ligands.  
   - Toggle Trp6.48 como eje de **función CB2**.  
   - Estructuras CB2 ago/ant abundantes.  
   - Combo conceptual CB1↓+CB2↑ (Mallat 2007) — fuera de SMRF químico pero contexto.

8. **Sigue sin respuesta:**  
   - Potencias numéricas Qiu 14/15/20/24 y fenotipos abiertos de 15/20/24.  
   - ¿La serie Qiu reproduce Yin-Yang en >1 análogo con misma plataforma?  
   - ¿Algún switch estructural predice **simultáneamente** CB1-ant + CB2-ago fuera de azar/chemotipo?  
   - Mutagénesis S173/S285 **sobre Qiu-14**.  
   - Réplica independiente de Qiu-14.

---

## Evidence table (verdict support)

| Evidence | Type | Supports |
|----------|------|----------|
| SI Fig. S5 Qiu-14 CB2 ago + CB1 ant cAMP | EXPERIMENTAL | Yin-Yang exists on Qiu scaffold (B) |
| Qiu abstract N1-Ph switch + o-morph | EXPERIMENTAL claim + COMP mechanism | Switch hypothesis (unproven multi-par OA) |
| URB447 IC50 + GTPγS + cAMP | EXPERIMENTAL | Cross-scaffold Janus (B) |
| GW405833 / AM1710 JPET | EXPERIMENTAL | Cross-scaffold Janus (B) |
| MRI2687 / MRI2594 Cell 2019 | EXPERIMENTAL + STRUCTURAL | CB2 function switch (A) |
| HU-308 → (R)-1 ACS Cent Sci | EXPERIMENTAL (+ COMP MD) | CB2 function switch (A) |
| Hypothesis numeric table / steric-24 | — | **REJECTED** |
| S173/S285 H-bond | COMPUTATIONAL | Mechanism only (D) |
| 0Q independent audit D NO-GO docking-NCE | Program context | SMRF ≠ reopen docking |

---

## Program implication (Option B)

- **ACTIVE work:** completar potencias Qiu (PDF/email), expandir pares A-class CB2 toggle vs Yin-Yang dual, decidir si wet usa **tool Janus comercial** (URB447/GW) antes que resíntesis Qiu.  
- **RESERVE Option A (0M):** no arrancar wet H1-a como ruta crítica mientras SMRF cierra gaps de evidencia histórica.  
- **No** reabrir docking/NCE (alineado con 0Q D NO-GO).

---

## Paths

| Deliverable | Path |
|-------------|------|
| Main report | `results/reports/qiu_0q_smrf_matrix.md` |
| Pairs CSV | `results/reports/qiu_0q_smrf_pairs.csv` |
| Context audit | `results/reports/qiu_0q_independent_scientific_audit.md` |
| 0M status | `results/reports/qiu_0m_h1a_wet_handoff.md` → **RESERVE** |

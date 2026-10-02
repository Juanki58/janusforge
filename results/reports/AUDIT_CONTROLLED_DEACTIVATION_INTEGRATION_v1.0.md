# AUDIT — Controlled-deactivation × Janusforge (v1.0)

| | |
|---|---|
| **Fecha** | 2026-08-17 |
| **Rol** | Analista documental bajo PI — primera auditoría de integración |
| **Alcance cerrado** | Tres primarios Makriyannis/Nikas: Sharma 2013, Nikas 2015, Kulkarni 2016 |
| **Arquitectura normativa (fija)** | **CB1 antagonista + CB2 agonista**; filtro de indicación **después** de receptor-first |
| **Prohibiciones respetadas** | Sin diseño NCE; sin docking/MD/QSAR; sin cambio de pipeline/criterios; sin promover soft-drug Janus a “probado”; sin commit de pipeline |
| **Docs/** | **No actualizados** (preferido; ver §10) |

**Clasificación de hallazgos:** cada finding card termina en exactamente uno de: **INTEGRABLE** | **CONDICIONAL** | **NO INTEGRABLE**.

**Convención de evidencia:** `FACT` = literal del primario recuperado; `INTERPRETATION` = lectura conservadora; `IMPLICACIÓN PARA JANUSFORGE` = solo sobre arquitectura CB1-ant/CB2-ago + ADME/periferia/duración como hipótesis; `EVIDENCE GAP` = lo que falta para transferir.

---

## 1. Executive summary

| Veredicto | N |
|-----------|---|
| **INTEGRABLE** | **2** |
| **CONDICIONAL** | **5** |
| **NO INTEGRABLE** | **6** |

**Veredicto global (conservador):** el trío primario **sí establece** un chemotype soft-drug / controlled-deactivation en scaffold **clásico THC/HHC** (éster labile → ácido inactivo; duración modulable; validación roedor ± primate). **No establece** — y en fenotipo receptor **contradice** — el perfil Janus normativo (**CB1-ant / CB2-ago**). Los leads son **agonistas CB1 potentes** (y, cuando se midió, **agonistas CB2**). Por tanto: principios ADME/duración = **CONDICIONAL** como hipótesis documental; fenotipo de la serie y cualquier “regla de diseño ester soft → Janus” = **NO INTEGRABLE**.

**Recuperación de fuentes**

| Paper | DOI / PMC | Local pre-audit | OA usado |
|-------|-----------|-----------------|----------|
| Sharma et al. 2013 | `10.1021/jm4016075` / **PMC3905450** | **NOT_IN_LOCAL_CORPUS** (sin carpeta/PDF previo) | Author manuscript HTML PMC (extract local: `data/papers/_recon_tmp/soft_drug_audit/sharma_*`) |
| Nikas et al. 2015 | `10.1021/jm501165d` / **PMC4306527** | **NOT_IN_LOCAL_CORPUS** | Idem (`nikas_*`) |
| Kulkarni et al. 2016 | `10.1021/acs.jmedchem.6b00717` / **PMC5532543** | **NOT_IN_LOCAL_CORPUS** | Idem (`kulkarni_*`); Unpaywall green OA; PDF NCBI bloqueado por captcha → HTML manuscript |

PDF binarios ACS/NCBI **no** se usaron (captcha/500). Números citados abajo vienen del **author manuscript PMC** (tablas/texto). Donde la tabla HTML no renderizó filas numéricas completas (Nikas Table 1), se marca y se usa texto/Table 3/Table 2 recuperables.

---

## 2. Janusforge assumptions under audit (hipótesis vs hecho)

Fuentes leídas (docs + reports; claims soft-drug tratados como **hipótesis** hasta check primario):

| Claim / supuesto en corpus Janus | Status pre-audit | Status post-audit (este trío) |
|----------------------------------|------------------|-------------------------------|
| Arquitectura: **CB1-ant + CB2-ago**; fibrosis **después** de receptor | **NORMATIVA / FACT** de programa (`guia_maestra`, `criterio_exito`, `quimioma`) | **Sin cambio** — fuera de alcance alterar |
| Gate 4: periferia vía “polaridad, ácidos/ésteres, TPSA…” (`criterio_exito`) | **Hipótesis deseable** (≠ gate pasado) | Sigue hipótesis; soft-drug ester ≠ automáticamente “periferia” |
| H2: ácidos/ésteres/prodrugs THCVA-like para BBB/ADME (`guia_maestra`, `quimiotipos_varinas`) | **Hipótesis H2** (fase H1–H5 **cerrada** como eje) | Soft-drug Makriyannis **no** valida H2 como Janus; fenotipo opuesto en CB1 |
| `quimioma` fila “Ácidos / ésteres (THCVA, profármacos)” → sesgo periférico | Hipótesis de mapa | Mezcla conceptual: **prodrug / polaridad** ≠ **soft-drug esterase → ácido inactivo** |
| Lecciones: COOH/COOMe en anillo A hunden CB1 Vina (`lecciones_aprendidas`) | Proxy in silico, no esterase | **No confligir** con ésteres de cadena lateral C3 del trío (posición distinta) |
| `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX`: esterase/soft-drug **NOT_IN_LOCAL_CORPUS** | Correcto al 2026-08-17 pre-esta auditoría | Este report **llena** el gap documental; **no** implica integración pipeline |
| Round1.9: GOLD_CONFIRMED = 0; URB447 etc. REVIEW | FACT documental | Soft-drug series **no** entra a Gold Janus (fenotipo agonista) |
| Soft-drug CB1-ant con metabolito ácido inactivo medido | Ausente / hipótesis | **Sigue ausente** en este trío (aquí el parent es **ago**) |

---

## 3. Sharma 2013 — primary map

**Cita:** Sharma R, Nikas SP, et al. *Controlled-Deactivation Cannabinergic Ligands.* J Med Chem. 2013;56(24):10142–10157. DOI `10.1021/jm4016075`. PMC3905450.

**Diseño (FACT):** (−)-Δ⁸-THC con **éster metabolically labile en posición 2′** de la cadena C3; sustituyentes α (1′-Me, gem-Me₂, ciclobutilo) para modular hidrólisis; metabolito ácido **3** previsto inactivo; “depot effect” + esterasas plasmáticas.

**Fenotipo funcional (FACT):** leads = **agonistas CB1** (cAMP forskolin ↓); hipotermia/analgesia **CB1-mediadas**.

### Tabla 1 (binding + plasma) — extract PMC

| Compd | Nota estructural (texto) | rCB1 Ki (nM) | mCB2 Ki | hCB2 Ki | mouse t½ (min) | rat t½ (min) |
|-------|--------------------------|--------------|---------|---------|----------------|--------------|
| (−)-Δ⁸-THC | control | 47.6 | 39.3 | ND | ND | ND |
| **2a** | éster (sin/menor 1′-bulk) | 27.1±4.5 | 40.4±7.6 | 51.5±11.2 | 0.7 | <0.5 |
| **3a** | ácido metabolito | >10,000 | >10,000 | ND | ND | ND |
| **2b** | 1′-(R)-Me | 1.6±0.2 | 4.5±0.3 | 3.7±0.2 | 5.9 | 10.5 |
| **3b** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **2c** | 1′-(S)-Me | 0.6±0.2 | 6.2±1.1 | 6.3±1.2 | 4.0 | 4.3 |
| **3c** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **2d** | 1′-gem-Me₂ | 0.3±0.1 | 2.1±1.1 | 1.7±0.4 | 12.4 | 120 |
| **3d** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **2e** | 1′-ciclobutilo | 0.7±0.2 | 3.0±0.5 | 3.0±0.7 | 36.3 | 263 |
| **3e** | ácido | >10,000 | >10,000 | ND | ND | ND |

Orden estabilidad (texto): **2a < 2c ≤ 2b < 2d < 2e**.

### Tabla 2 — rCB1 cAMP (FACT)

| Compd | EC50 (nM) | Emax (%) vs CP-55,940 |
|-------|-----------|------------------------|
| 2a | N.R. (hasta 5 µM) | — |
| 2b | N.R. | — |
| **2c** | 4.2 (1.7–10.9) | **63** |
| **2d** | 0.5 (0.1–1.2) | **92** |
| **2e** | 0.4 (0.2–1.2) | **90** |

**In vivo (FACT):** 2c/2d/2e hipotermia; 2d onset más rápido / duración más corta vs Δ⁸-THC-DMH (hipotermia + analgesia). Ácidos 3b–3e: sin hipotermia.

**CB2 función:** afinidad alta en binding; **no** se priorizó antagonismo CB1 ni perfil Janus. Abstract: “potent **CB1 receptor agonists**”.

---

## 4. Nikas 2015 — primary map

**Cita:** Nikas SP, Sharma R, et al. *Probing the Carboxyester Side Chain in Controlled Deactivation (−)-Δ⁸-Tetrahydrocannabinols.* J Med Chem. 2015 (epub 2014); DOI `10.1021/jm501165d`. PMC4306527. PMID 25470070.

**Diseño (FACT):** SAR del **carboxiéster en cadena 3-alquilo** (éster / reverse ester / tioéster / amida; ω-Br, CN, imidazolilo); lead **10a = AM7438** (3-cianopropil éster del ácido 2-metilpropanoico sobre Δ⁸-THC).

**Fenotipo (FACT):** **agonista CB1** potente/eficaz; onset/offset relativamente rápido; metabolito ácido **inactivo** (abstract + narrativa).

### Lead AM7438 (10a) — números recuperados

| Endpoint | Valor | Fuente PMC |
|----------|-------|------------|
| Affinity | Abstract: **picomolar** CB receptors | Abstract |
| Ki (Table 3, key analogues) | Valores listados en rango **0.5–0.9 nM (rCB1)** / **0.8–1.4 nM (mCB2)** para leads de alta afinidad vs Δ⁸-THC 47.6/39.3 | Table 3 texto |
| Table 1 filas numéricas completas | **PARTIAL** — HTML manuscript no entregó grid numérico completo en extract | Gap de parseo, no de paper |
| rCB1 cAMP EC50 | **0.9 (0.3–1.5) nM**; Emax **89%** | **Table 2** |
| Comparadores Table 2 | 2b EC50 0.5 nM Emax 92%; 2c 0.4 nM Emax 90% | Table 2 |
| Plasma | t½ modulable; CN/imidazolilo **aumentan** estabilidad vs 2b (3–31×) | Texto SSR |
| In vivo | 10a ~**10×** más potente + onset más rápido + duración más corta vs 2b menos polar; analgesia offset más rápido | Texto + Table 4 (clogP/tPSA/duración hipotermia: 10a t < 6 h vs 2b 6–12 h vs DMH >12 h) |

**Ácido metabolito:** abstract — **inactive**; coherente con diseño Sharma (ácidos Ki >10,000). Filas ácido específicas de AM7438 en Table 1: **no tabuladas limpiamente en extract** → gap menor; claim de inactividad sí es primario (abstract/conclusiones).

**CB2:** binding alto en serie; función enfatizada en **CB1 ago** (cAMP, hipotermia, analgesia). **No** CB1 antagonista.

---

## 5. Kulkarni 2016 — primary map

**Cita:** Kulkarni S, Nikas SP, et al. *Novel C-Ring-Hydroxy-Substituted Controlled Deactivation Cannabinergic Analogues.* J Med Chem. 2016;59(14):6903–6919. DOI `10.1021/acs.jmedchem.6b00717`. PMC5532543.

**Diseño (FACT):** 2ª generación — éster 2′/3′ en cadena + **OH en C9 o C11** (HHC/THC) para polaridad/depot; lead **3b = AM7499**.

**Fenotipo (FACT):** **agonistas CB1 y CB2** (cAMP); hipotermia CB-mediada; discriminación de droga en **squirrel monkeys** vs no-hidrolizable 11-OH-Δ⁸-THC-DMH (**3g**).

### Tabla 1 (selección)

| Compd | ID | rCB1 Ki | mCB2 | hCB2 | mouse t½ | rat t½ |
|-------|-----|---------|------|------|----------|--------|
| **3g** | 11-OH-Δ⁸-THC-DMH (no soft) | 0.7 | 0.2 | 0.5 | ND | ND |
| **2a** | 1ª gen (Sharma-like) | 0.3±0.1 | 2.1±1.1 | 1.7±0.4 | 12.4 | 120 |
| **3a** | C11-OH éster | 0.6±0.2 | 1.5±0.5 | 0.8±0.3 | 5.0 | 39.1 |
| **4a** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **3b (AM7499)** | C11-OH HHC gem-Me₂ butyl ester | **2.4±0.3** | **0.1±0.05** | **3.1±0.5** | **3.1** | **39.2** |
| **4b** | ácido de 3b | >10,000 | >10,000 | ND | ND | ND |
| **3c** | C9-eq-OH | 0.1±0.05 | 0.2±0.1 | 0.2±0.1 | 2.7 | 10.2 |
| **4c** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **3d** | C9-ax-OH | 3.1±0.8 | 6.6±1.5 | 4.5±1.1 | 2.8 | 5.6 |
| **4d** | ácido | >10,000 | >10,000 | ND | ND | ND |
| **3e / 3f** | afinidad débil | cientos nM | … | … | ND | ND |

### Tabla 2 — función (FACT)

| Compd | rCB1 EC50 / Emax | hCB2 EC50 / Emax | Clasificación paper |
|-------|------------------|------------------|---------------------|
| **3a** | 4.6 nM / 89% | 5.7 nM / 83% | **agonist / agonist** |
| **3b (AM7499)** | **2.5 nM / 87%** | **0.3 nM / 82%** | **agonist / agonist** |
| **3c** | 8.6 nM / 85% | 9.0 nM / 85% | **agonist / agonist** |

**Primate (FACT):** 3b ~**3×** más potente y ~**4×** duración más corta vs 3g en discriminación; onset ~15 min; t½ discriminativo citado **48 min** (dosis 0.001 mg/kg). Entrenamiento con AM4054 (CB1 full ago) — readout **agonista CB1**, no antagonista.

---

## 6. Compound / claim → primary source table

| Claim | Compound(s) | Primary locus | Status |
|-------|-------------|---------------|--------|
| Éster 2′ en Δ⁸-THC = soft spot | 2a–2e | Sharma Fig.1–3, Abstract | FACT |
| Ácidos metabolito Ki >10,000 CB1/CB2 | 3a–3e; 4a–4f | Sharma T1; Kulkarni T1 | FACT |
| Plasma t½ modulable por bulk 1′ | 2a–2e | Sharma T1 + texto | FACT |
| CB1 ago funcional (cAMP) | 2c–2e; 10a; 3a–3c | Sharma T2; Nikas T2; Kulkarni T2 | FACT |
| Hipotermia/analgesia CB1 | 2c–2e; 10a; 3a–3c | Sharma/Nikas/Kulkarni in vivo | FACT |
| AM7438 = 10a; picomolar; ácido inactivo | AM7438 | Nikas Abstract + T2/T3/T4 | FACT (T1 grid PARTIAL en extract) |
| Polaridad ω-CN acorta duración vs éster menos polar | 10a vs 2b | Nikas in vivo + T4 | FACT |
| AM7499 = 3b; CB1+CB2 ago; primate shorter DoA | AM7499 | Kulkarni Abstract, T1–T2, NHP | FACT |
| Soft-drug = CB1-ant / CB2-ago Janus | — | **Ningún** de los tres | **NOT_SUPPORTED** |
| Soft-drug ester = restricción periférica / no CNS | — | Papers miden **CNS CB1 behaviors** (hipotermia, tetrad-like, discriminación) | **NOT_SUPPORTED** como periferia |
| Esterase soft-drug ya en corpus Janus leads (URB447…) | — | Documentary matrix | Sigue N/A (diseños distintos) |

---

## 7. Finding cards

### F1 — Soft-drug ester → ácido inactivo (chemotype clásico)

- **FACT:** En Sharma/Kulkarni, ácidos correspondientes tienen Ki **>10,000 nM** en CB1/CB2 (T1); Nikas abstract: ácido de AM7438 **inactive**.
- **INTERPRETATION:** El principio “parent activo / metabolito carboxílico inactivo” está **primariamente demostrado** en este chemotype THC/HHC-éster.
- **IMPLICACIÓN PARA JANUSFORGE:** Solo como **precedente ADME de clase soft-drug**, no como evidencia de fenotipo Janus.
- **EVIDENCE GAP:** No hay en este trío un **CB1 antagonista** (ni Yin-Yang) con el mismo soft spot.
- **CONDICIONAL**

### F2 — Duración de acción modulable (esterasa + depot/polaridad)

- **FACT:** t½ plasma escala con bulk 1′ (Sharma); polaridad ω-CN / OH C-ring acorta DoA in vivo (Nikas T4; Kulkarni vs 3g; NHP ~4× más corto).
- **INTERPRETATION:** Controlled-deactivation es un **paquete PK/PD** (hidrólisis + lipofilia), no solo “poner un éster”.
- **IMPLICACIÓN PARA JANUSFORGE:** Hipótesis documental útil si algún día hubiera un Janus **ya dual** que necesitara acortar exposición; **no** autoriza insertar ésteres en screening actual.
- **EVIDENCE GAP:** Transfer a scaffolds Janus (URB447/pirazol/…) y a **antagonismo** CB1 no medido.
- **CONDICIONAL**

### F3 — Fenotipo receptor de la serie = agonismo CB1 (± CB2)

- **FACT:** Sharma T2 / Nikas T2 / Kulkarni T2: **agonist** en cAMP; Kulkarni 3b también **hCB2 agonist** EC50 0.3 nM.
- **INTERPRETATION:** El programa Makriyannis de estos papers optimiza **agonistas** “más seguros por duración corta”, no Janus.
- **IMPLICACIÓN PARA JANUSFORGE:** Transferir SAR/leads de esta serie al norte CB1-ant/CB2-ago sería **anti-semilla** (`criterio_exito` gate 3).
- **EVIDENCE GAP:** N/A — el gap es conceptual: fenotipo opuesto.
- **NO INTEGRABLE**

### F4 — Validación in vivo roedor + NHP

- **FACT:** Hipotermia/analgesia rata/ratón; discriminación squirrel monkey (Kulkarni) confirma DoA más corta vs no-hidrolizable.
- **INTERPRETATION:** Soft-drug approach **in vivo** es real para **agonistas CB**.
- **IMPLICACIÓN PARA JANUSFORGE:** No sustituye validación de un Janus periférico antifibrótico.
- **EVIDENCE GAP:** Sin fibrosis, sin CB1-ant, sin dual Janus.
- **CONDICIONAL** (como precedente metodológico DoA; **no** como PoC Janus)

### F5 — “Ésteres → periferia / menor CNS” (docs H2 / gate 4)

- **FACT:** Los papers usan endpoints **centrales** (hipotermia, analgesia, discriminación agonista).
- **INTERPRETATION:** Soft-drug aquí controla **tiempo de agonismo CNS**, no demuestra exclusión BBB como URB447/JD5037.
- **IMPLICACIÓN PARA JANUSFORGE:** Conflar H2 “ésteres/prodrugs periféricos” con este trío es **incorrecto**.
- **EVIDENCE GAP:** Medidas brain:plasma / BBB en estos tres = no recuperadas como paquete de periferia.
- **NO INTEGRABLE** (como soporte de periferia Janus)

### F6 — Afinidad dual CB1/CB2 alta en soft esters

- **FACT:** Kis sub-nM–nM en ambos receptores (Sharma 2c–2e; Kulkarni 3a–3c).
- **INTERPRETATION:** El soft spot **no** destruye binding CB2 en este scaffold; pero la **función** es ago/ago, no ant/ago.
- **IMPLICACIÓN PARA JANUSFORGE:** Binding dual ≠ perfil Janus.
- **EVIDENCE GAP:** Antagonismo CB1 en esta serie: **no reportado** (y contradictorio con cAMP ago).
- **NO INTEGRABLE** (como evidencia Janus)

### F7 — Precedente documental de que “esterase soft-drug” existe en cannabinoides

- **FACT:** Tres primarios OA recuperados; matrices Ki/t½/EC50/in vivo.
- **INTERPRETATION:** Cierra el vacío “NOT_IN_LOCAL_CORPUS” de la matriz documental **para esta clase**, no para leads Janus.
- **IMPLICACIÓN PARA JANUSFORGE:** Actualizar inventario de literatura en **reports**; no cambiar gates.
- **EVIDENCE GAP:** Ninguno para el claim estrecho “soft-drug cannabinoid agonists existen”.
- **INTEGRABLE** (solo como **hecho bibliográfico / inventario**)

### F8 — Metabolito ácido inactivo elimina confusión metabólica vs 11-OH-THC

- **FACT:** Papers contrastan con 11-OH-THC psicoactivo de larga duración; ácidos soft **inactivos**.
- **INTERPRETATION:** Principio de **detoxificación predecible** en agonistas clásicos.
- **IMPLICACIÓN PARA JANUSFORGE:** Relevante solo si el parent Janus ya es correcto; un ácido inactivo no “limpia” un parent CB1-ago.
- **EVIDENCE GAP:** Aplicación a antagonistas / duales.
- **CONDICIONAL**

### F9 — Declarar estrategia soft-drug Janus “probada”

- **FACT:** Cero compuestos de este trío con CB1-ant + CB2-ago.
- **INTERPRETATION:** Cualquier claim de “Janus soft-drug validated” sería **extrapolación prohibida**.
- **IMPLICACIÓN PARA JANUSFORGE:** Mantener lenguaje de **hipótesis** si se menciona soft-drug.
- **EVIDENCE GAP:** Primario Janus × soft-drug × (idealmente) periferia.
- **NO INTEGRABLE**

### F10 — Usar AM7438 / AM7499 / 2d como seeds de generación Janusforge

- **FACT:** Son **CB1 agonists** potentes (y AM7499 también CB2 ago).
- **INTERPRETATION:** Como semillas de Track 1 Janus = dirección anti-semilla.
- **IMPLICACIÓN PARA JANUSFORGE:** No candidatos / no seeds de diseño (alcance cerrado).
- **EVIDENCE GAP:** N/A.
- **NO INTEGRABLE**

### F11 — Separación conceptual soft-drug vs restricción periférica vs prodrug

- **FACT:** Documentary matrix ya distinguía URB447 (periferia) ≠ soft-drug; este trío confirma soft-drug agonista CNS-activo.
- **INTERPRETATION:** Tres herramientas distintas: (A) soft-drug DoA, (B) polar/efflux periferia, (C) prodrug→neutro.
- **IMPLICACIÓN PARA JANUSFORGE:** Mantener vocabulario separado en documentación futura.
- **EVIDENCE GAP:** Ninguno para la distinción conceptual.
- **INTEGRABLE** (como **higiene documental**)

### F12 — Lecciones Vina COOH/COOMe anillo A vs éster cadena C3

- **FACT:** Soft spot de estos papers está en **cadena C3**, no carboxilación aromática tipo H2/THCVA.
- **INTERPRETATION:** No hay conflicto primario directo con “COOH anillo A hunde CB1 Vina”; son palancas distintas.
- **IMPLICACIÓN PARA JANUSFORGE:** No reinterpretar lecciones H2 con Sharma/Nikas.
- **EVIDENCE GAP:** SAR cruzado posición éster × fenotipo ant/ago.
- **CONDICIONAL** (no mezclar; sin integrar como regla)

### F13 — Species differences plasma esterase

- **FACT:** Rat vs mouse t½ difieren (p.ej. 2d 12.4 vs 120 min; Kulkarni texto: rat plasma menos activo); Nikas nota carboxylesterasas en ratón/rata **no** en plasma humano.
- **INTERPRETATION:** Extrapolación humana de t½ plasma **no trivial**.
- **IMPLICACIÓN PARA JANUSFORGE:** Cualquier futuro soft-drug Janus requeriría matriz especie/CES humana — gap, no diseño ahora.
- **EVIDENCE GAP:** Datos CES humanos para chemotypes Janus.
- **NO INTEGRABLE** (como supuesto de traslación directa)

---

## 8. Conflicts with Janusforge assumptions

| Asunción Janus | Conflicto con primarios | Severidad |
|----------------|-------------------------|-----------|
| Norte CB1-**ant** / CB2-**ago** | Serie = CB1-**ago** (± CB2-ago) | **Alto** — fenotipo opuesto en CB1 |
| Gate 3 anti-semilla (evitar ago CB1 fuerte) | Leads con EC50 sub-nM–nM ago CB1 | **Alto** |
| H2/gate4: ésteres ≈ periferia | Endpoints CNS; DoA de agonismo central | **Medio** — confusión conceptual |
| Soft-drug como “mejora Janus” implícita | Soft-drug mejora **seguridad por duración** de **agonistas**, no dualidad ant/ago | **Alto** si se promociona sin matices |
| Cannabis-first THCV-like | Chemotype Δ⁸-THC/HHC ago es **anti-PoC** para flip (empuja ago) | **Medio** (ya H1–H5 cerrado) |
| Documentary: soft-drug vacío | Ahora hay OA recovery — actualizar **report**, no doctrina | **Bajo** (inventario) |

**No hay conflicto** con la norma “indicación después de receptor”: estos papers ni siquiera pasan el filtro receptor Janus.

---

## 9. What is NOT transferable

1. **Fenotipo CB1/CB2** de AM7438 / AM7499 / 2c–2e → **no** es Janus dual.
2. **SAR de potencia agonista** (gem-Me₂, ciclobutilo, CN-terminal, C11-OH) como reglas para generar CB1-ant.
3. **Soft-drug = periferia** (URB447-like).
4. **Ácido inactivo** como prueba de que un parent Janus “se apaga bien” — solo se midió sobre parents ago.
5. **Validación NHP** de DoA agonista ≠ PoC fibrosis / IPF / CB1-ant.
6. **Extrapolación a plasma humano** sin CES data.
7. **Cualquier NCE / seed / screening tweak** derivado de este audit.

---

## 10. Recommendations for PI (solo documentación)

1. **No cambiar pipeline, gates, ni `docs/` normativos** en esta ronda.
2. Tratar Sharma/Nikas/Kulkarni como **precedente de clase soft-drug agonista clásico**, citado en reports si se habla de controlled-deactivation — **nunca** como ancla Janus.
3. Si se menciona soft-drug en docs futuros: exigir frase del tipo *“demostrado en CB1 agonists clásicos; transferencia a CB1-ant/CB2-ago = no primaria”*.
4. Mantener separación léxica: **soft-drug DoA** ≠ **restricción periférica** ≠ **prodrug THCVA**.
5. Opcional (fuera de esta auditoría): añadir una fila en una futura revisión de `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX` apuntando a este report — **no hecho aquí** para evitar scope creep.
6. **No** abrir campaña de candidatos soft-Janus sin primario dual explícito.

**`docs/` actualizados:** **No.**

---

## 11. STOP statement

**STOP.** No se autoriza trabajo computacional (docking/MD/QSAR), búsqueda de candidatos, modificación de generación/screening, ni promoción Gold a partir de este audit. Entregable = **solo** este informe documental. Arquitectura Janus (**CB1-ant + CB2-ago**, indicación after receptor) **permanece**.

---

## Parent return

| Campo | Valor |
|-------|-------|
| **Path** | `results/reports/AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` |
| **INTEGRABLE** | **2** (F7 inventario bibliográfico; F11 higiene conceptual soft≠periferia≠prodrug) |
| **CONDICIONAL** | **5** (F1 ácido inactivo; F2 DoA; F4 in vivo/NHP como DoA; F8 detox; F12 no mezclar posiciones) |
| **NO INTEGRABLE** | **6** (F3 fenotipo ago; F5 periferia; F6 binding≠Janus; F9 “Janus soft proven”; F10 seeds; F13 traslación humana) |
| **Top 3 implications** | (1) Soft-drug cannabinoid **sí** es primario — pero en **agonistas CB1**, no Janus. (2) Éster labile → ácido inactivo / DoA corta = **CONDICIONAL** solo como hipótesis ADME si ya hubiera dual correcto. (3) Docs H2/gate4 **no** quedan validados como periferia por este trío; **no** reescribir `docs/`. |
| **docs/ updated?** | **No** |

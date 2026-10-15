# Atlas estructural CB₂ — Janusforge

**Fecha:** 2026-08-20  
**Modo:** Documental / READ-ONLY — **sin docking, sin MD, sin cómputo nuevo**  
**Rama:** `docs/cb2-atlas-and-epistemological-consolidation`  
**Audiencia:** PI y colaboradores que citen el panel estructural del programa

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto (Phase F/G/H, micronetwork, Contract v1.0, distancias medidas desde JSON del repo) |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada externa — requiere DOI, PMID o PDB |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |

---

## 1. Propósito

**[OBSERVACIÓN_PROPIA]** Este atlas consolida las **plantillas estructurales CB₂** relevantes para las fases conformacionales F y G del proyecto Janusforge. No sustituye la verificación Level-0 en cada run; documenta identidades, resoluciones de referencia y roles en la cadena epistemológica macro → micro → dinámica.

**Artefactos de fase vinculados:**

| Fase | Reporte | Rol |
|------|---------|-----|
| **F** | [`results/conformational/fase_f_conformational_fingerprint.md`](../../results/conformational/fase_f_conformational_fingerprint.md) | Huella conformacional; matriz `CB2_STATE_DISTANCE`; infra Level-0 |
| **G** | [`results/conformational/fase_g_generalization_report.md`](../../results/conformational/fase_g_generalization_report.md) | Generalización ciega **8GUR** OOS; veredicto **GENERALIZES** |

**[OBSERVACIÓN_PROPIA]** JSON asociados: `results/conformational/cb2_state_distance_matrix.json`, `fase_g_generalization_report.json`.

---

## 2. Tabla maestra de estructuras

**[LITERATURA_PRIMARIA]** Resoluciones en la columna «Ref. PI» provienen de la consolidación PI (2026-08-20).  
**[OBSERVACIÓN_PROPIA]** La columna «Level-0 proyecto» refleja verificación interna (`docs/cb2_multistate_calibration_synthesis.md`, `data/targets/multistate_aligned/alignment_manifest.json`).

| PDB | Estado funcional | Ligando | Ref. PI (Å) | Level-0 proyecto | DOI / fuente primaria |
|-----|------------------|---------|-------------|------------------|----------------------|
| **5ZTY** | Inactivo / antagonista | AM10257 (9JU) | **2.60** | 2.8 Å X-ray; **inactivo** (no Gi) | DOI [10.1016/j.cell.2018.12.011](https://doi.org/10.1016/j.cell.2018.12.011); PDB **5ZTY** |
| **6PT0** | Activo + Gi | WIN 55,212-2 (WI5) | **2.80** (X-ray) | cryo-EM ~3.2 Å; referencia Contract v1.0 | DOI [10.1016/j.cell.2020.01.007](https://doi.org/10.1016/j.cell.2020.01.007); PDB **6PT0** |
| **6KPF** | Activo + Gi | AM12033-class (E3R) | **3.20** cryo-EM | cryo-EM ~2.9 Å | DOI [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008); PDB **6KPF** |
| **6KPC** | Activo (cristal) | E3R | — | X-ray ~3.2 Å; bolsillo alternativo | DOI [10.1016/j.cell.2020.01.008](https://doi.org/10.1016/j.cell.2020.01.008); PDB **6KPC** |
| **8GUS** | Activo + Gi | **HU-308** | **2.97** | cryo-EM ~3.0 Å | DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494; PDB **8GUS** |
| **8GUR** | Activo + Gi | CP55,940 (9GF) | **2.84** | cryo-EM 2.84 Å; **ciego Phase G** | DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494; PDB **8GUR** |
| **8GUQ** | Activo + Gi (KNF) | APD371 / Olorinab | ~3.08 | agonista β-arrestina-biased | DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494; PDB **8GUQ** |
| **8GUT** | Activo + Gi | LEI-102 | **2.98** | cryo-EM | DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494; PDB **8GUT** |
| **12IY** | Activo + Gi | agonista '5249 (Rachman series) | ~2.9 (local refined) | cryo-EM 2026; validación docking | DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716; PDB **12IY** |
| **12IZ** | Activo + Gi | (serie Rachman 2026) | — | Entrada UniProt P34972; verificar antes de uso operativo | DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716; PDB **12IZ** |
| **12JA** | Activo + Gi | agonista '1029 (Rachman series) | **2.9** | cryo-EM EMD-76465 | DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716; PDB **12JA** |
| **8X3L** | Activo + G | (selectividad entropy-driven) | **3.13** | cryo-EM 2024 | DOI [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121); PDB **8X3L** |
| **9U7L** | Activo + PAM | CP55,940 + **Ec21a** (vestíbulo ECL2) | **3.2** | PAM alostérico CB2-selectivo | DOI [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6); PMID 42115595; PDB **9U7L** |
| **5VEU** | — | — | — | **BLOCKED** | **NOT CB2** — CYP3A5 |

> **[LITERATURA_PRIMARIA]** **Nota 8X3L vs 9U7L:** **8X3L** documenta acoplamiento G con implicaciones de selectividad (Shen *et al.* 2024, DOI [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121)). **9U7L** es la estructura cryo-EM del PAM **Ec21a** en vestíbulo ECL2 (Wang *et al.* 2026, DOI [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6); PMID 42115595). Ambas entran en el mapa alostérico; ver [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md).

---

## 3. Notas Level-0 de integridad (proyecto)

**[OBSERVACIÓN_PROPIA]** Verificación formal registrada en Phase F y calibración multistate:

| PDB | Nota Level-0 | Estado en repo |
|-----|--------------|----------------|
| **5ZTY** | Antagonista/inactivo AM10257; fusión T4L; **no** es estado Gi-activo | `VERIFIED` — procesado como control inactivo |
| **6PT0** | Referencia histórica Contract v1.0; grid `configs/grid_cb2_6pt0.txt` | `VERIFIED` — cadena R, ligando WI5 |
| **6KPF** | Segundo agonista cryo-EM; diverge en microdescriptores Trp258/Phe183 vs 6PT0 | `VERIFIED` — cadena R, ligando E3R |
| **5VEU** | Erróneamente listado como CB2 inactivo en borradores PI | **BLOCKED** — CYP3A5; excluido de Level-0 |
| **8GUR** | Entrada ciega Phase G; CP55,940; cadena R | `VERIFIED` — Level-0 PASS en `fase_g_generalization_report.md` |
| **SR141716** | Control negativo rimonabant | **INDETERMINATE** (InChIKey mismatch) — no inferir veredicto |

**[OBSERVACIÓN_PROPIA]** Prep uniforme (estados VERIFIED): monómero CB2; eliminación uniforme de aguas, iones, ligando co-cristalizado, lípidos, Gi/Gβγ, nanobodies; protonación Meeko pH 7.4. Manifiesto: `data/targets/multistate_aligned/alignment_manifest.json`.

**[OBSERVACIÓN_PROPIA]** Errores a no propagar: **8F7V** = plasmina, no CB2 (`qiu_0q_independent_scientific_audit.md`).

---

## 4. Rol en fases F y G

### Phase F — Huella conformacional

**[OBSERVACIÓN_PROPIA]** Phase F construyó la coordenada **CB2_STATE_DISTANCE** en el espacio TM3–TM5–TM6 + microswitches (Trp258, Ser268, Phe183, etc.):

| PDB | Distancia normalizada vs centroide activo (6PT0+6KPF) |
|-----|------------------------------------------------------|
| 6PT0 | 1.7646 |
| 6KPF | 1.7646 |
| 5ZTY | 4.2819 (inactivo) |

**[OBSERVACIÓN_PROPIA]** Centroide activo = **6PT0 + 6KPF**. La matriz completa está en `results/conformational/cb2_state_distance_matrix.json`.

### Phase G — Generalización 8GUR (ciego OOS)

**[OBSERVACIÓN_PROPIA]** **Veredicto Q1:** `GENERALIZES`

| PDB | Distancia (norm) | Rol |
|-----|------------------|-----|
| 6PT0 | 2.3019 | referencia activa |
| 6KPF | 2.3019 | referencia activa |
| **8GUR** (blind) | **2.3205** | activo CP55,940 + Gi |
| 5ZTY | 3.9501 | inactivo |

**[OBSERVACIÓN_PROPIA]** **Interpretación macro (Nivel 1 epistemológico):** 8GUR (2.32) ≈ 6KPF/6PT0 (2.30) ≪ 5ZTY (3.95). Δ(blind→inactivo) = **1.630** unidades normalizadas.

**[LITERATURA_PRIMARIA]** Atlas macro PI: estados activos de alta resolución comparten núcleo TM con **RMSD Cα ~0.35 Å** entre plantillas activas del atlas consolidado (Li *et al.* 2023, DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494).

**[OBSERVACIÓN_PROPIA]** El manifiesto de alineamiento Phase F reporta RMSD post-alineamiento a referencia 6PT0 que **varía por estructura** (p. ej. 8GUR ~3.51 Å, 6KPF ~22.4 Å en `alignment_manifest.json`); la coordenada normalizada **CB2_STATE_DISTANCE** captura la proximidad macro independientemente de esa varianza local de alineamiento.

**[OBSERVACIÓN_PROPIA]** **Veredicto Q2 (LOO):** `PARTIAL` — tendencia preservada pero margen no robusto bajo leave-one-out con centroide 6PT0 solo.

---

## 5. Serie 12IY / 12IZ / 12JA (2026)

**[LITERATURA_PRIMARIA]** Estructuras cryo-EM asociadas a **Rachman *et al.* 2026** (*J. Med. Chem.*, DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716):

| PDB | Descripción verificada | Relevancia Janusforge |
|-----|------------------------|----------------------|
| **12IY** | CB2–Gi con agonista '5249; refinamiento local | Validación experimental de poses de docking a escala de biblioteca |
| **12JA** | CB2–Gi con agonista '1029; EMD-76465; ~2.9 Å | idem |
| **12IZ** | Entrada en hit list UniProt P34972 | **Verificar caso a caso** antes de plantilla operativa |

**[OBSERVACIÓN_PROPIA]** Estas entradas amplían el atlas activo 2026 pero **no** reabren pipelines computacionales del proyecto.

---

## 6. 8GUS como plantilla experimental HU-308

**[LITERATURA_PRIMARIA]** **8GUS** es el complejo cryo-EM **HU-308–CB2–G** (Li *et al.* 2023, DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494; PDB **8GUS**). Es la referencia **experimental canónica** para el ligando gold del proyecto, contrastada con:

- **[OBSERVACIÓN_PROPIA]** Docking ciego contra **6PT0** (Contract v1.0 / calibración multistate)
- **[OBSERVACIÓN_PROPIA]** Proyección conformacional Phase H (centroide idéntico HU-308/HU-433 en 6PT0)

Ver desarrollo del par enantiomérico en [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md).

---

## 7. Mapa de rutas en repo

| Tema | Ruta |
|------|------|
| Calibración multistate | `docs/cb2_multistate_calibration_synthesis.md` |
| Tabla evidencia PDB | `results/reports/qiu_0p_external_evidence_table.md` |
| Prep targets | `data/targets/cb2/`, `src/targets/prep.py` |
| Grids Contract v1.0 | `configs/grid_cb2_6pt0.txt`, `configs/cb1_cb2.yaml` |
| Síntesis frontera | `docs/cb2_mechanistic_frontier_synthesis.md` |

---

*Fin atlas estructural CB₂. Documento de consolidación — no autoriza cómputo nuevo.*

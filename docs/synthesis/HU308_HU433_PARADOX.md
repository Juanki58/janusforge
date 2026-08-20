# Par enantiomérico HU-308 / HU-433 — disociación afinidad ↔ funcional

**Fecha:** 2026-08-20  
**Modo:** Documental / READ-ONLY — **sin docking, sin MD, sin cómputo nuevo**  
**Rama:** `docs/cb2-atlas-and-epistemological-consolidation`

---

## 1. Enunciado del paradox (sin forzar etiquetas funcionales)

El par **HU-308 (C3)** / **HU-433 (C1)** son estereoisómeros documentados como agonistas CB₂ selectivos. La literatura reporta **disociación entre afinidad de unión y eficacia/potencia funcional Gi**, orientación en bolsillo y sesgo de vía — **no** equivalencia simple «mayor Ki → mayor Emax».

**Prohibición epistemológica:** no afirmar superioridad funcional de un enantiómero sobre el otro sin fila Gi comparable en primarios recuperados. No entrenar clasificadores funcionales a partir de proxies de docking.

---

## 2. Cronología experimental (2015–2026)

| Periodo | Fuente | Hallazgo relevante | Uso en Janusforge |
|---------|--------|-------------------|-------------------|
| **1999** | Hanuš *et al.* PNAS | HU-308: Ki CB₂ ~22.7 nM; agonista selectivo | Referencia gold lit-activa; Exam A Contract v1.0 |
| **2015** | Hanuš *et al.* PNAS; patente US20110269842A1 | HU-433 (C1): Ki CB₂ **12.2 nM** vs HU-308 22.7 nM; sin CB₁ apreciable | Caso de calibración — mayor afinidad, no implica mayor eficacia Gi |
| **2017** | Soethoudt *et al.* *Nat Commun* DOI [10.1038/ncomms13958](https://doi.org/10.1038/ncomms13958) | Panel hCB2 CHO unificado: CP55940-normalized cAMP + GTPγS | Base Phase H ordinal |
| **2023** | Li *et al.* *Nat Commun* DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9) | **8GUS** = cryo-EM HU-308–CB2–Gi (~2.97 Å) | Plantilla experimental canónica HU-308 |
| **2026** | Ganzoni *et al.* *Chem. Sci.* DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B) | Modificaciones en posición única del scaffold HU-308 modulan **Trp258^6.48** → continuo agonismo parcial / antagonismo / inverse parcial | Contexto dinámico del toggle switch; no resuelve el par C3/C1 |

---

## 3. Evidencia de afinidad vs orientación vs señal

### 3.1 Afinidad (Ki)

| Compuesto | Ki CB₂ (literatura) | Fuente |
|-----------|---------------------|--------|
| HU-308 | 22.7 ± 3.9 nM | Hanuš 1999 (`fase_h_ordinal_functional_report.md`) |
| HU-433 | 12.2 nM | Patente US20110269842A1; Hanuš 2015 (citado en Phase H) |

HU-433 presenta **mayor afinidad** reportada. Esto **no** implica automáticamente mayor eficacia Gi ni mejor candidato terapéutico.

### 3.2 Eficacia Gi — panel Soethoudt 2017 (Phase H H0)

Datos auditados en `results/conformational/fase_h_ordinal_functional_report.md`:

| Compuesto | Ensayo | Emax % vs CP55,940 | Clase ordinal | Comparabilidad |
|-----------|--------|-------------------|---------------|----------------|
| HU-308 | GTPγS | 97 | TOTAL | LEVEL_0_HIGH |
| HU-308 | cAMP | 98–108.6 | TOTAL | LEVEL_0_MODERATE–HIGH |
| HU-433 | cAMP | — | **INDETERMINATE** | Sin fila hCB2 Gi comparable con referencia CP55,940 en primarios recuperados |
| HU-433 | GTPγS | — | **INDETERMINATE** | idem |

**Cautela PI (Phase H):** HU-308/HU-433 = **caso pareado**, no misma clase funcional demostrada por ordinal convergente.

### 3.3 mini-Gαi vs β-arrestin

- Phase H **prohíbe** β-arrestin y ERK como proxy de clase Gi (`FORBIDDEN_PATHWAYS: beta_arrestin, ERK_phosphorylation`).
- Morales-Pastor *et al.* 2025 (Nat Commun, DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)) perfila **Gαi2 y β-arrestin1** en mutantes CB2R — evidencia externa de que el acoplamiento preferencial Gαi2 vs β-arrestin es **modulable** por la red alostérica (ACN), no reducible a distancia ortostérica estática.
- **8GUQ** (APD371/Olorinab) documenta agonismo con sesgo β-arrestina en cryo-EM — contraste de vía relevante para el atlas, **no** aplicado al par HU-308/HU-433 en este repo.

---

## 4. 8GUS (experimental) vs docking ciego (6PT0)

| Observador | PDB / método | Qué captura |
|------------|--------------|-------------|
| **Experimental** | **8GUS** (HU-308 + Gi) | Pose co-cristalizada / cryo-EM del enantiómero C3 en complejo de señalización |
| **Proyecto estático** | **6PT0** + Vina + Contract v1.0 | Snapshot WIN 55,212-2 + proxies geométricos congelados |
| **Calibración multistate** | 6PT0 / 5ZTY / 6KPF | HU-308 y HU-433 **acomodados** (Vina) en los tres estados; contactos Ser285/Trp258/Phe183 difieren (`cb2_multistate_calibration_synthesis.md` §5.1) |

**Disociación clave:** 8GUS ancla la química **HU-308** en estado activo acoplado a G. El docking contra 6PT0 (referencia WIN) colapsa HU-308 y HU-433 al **mismo centroide conformacional** (distancia 1.7646 norm en Phase F/H) pese a contactos microswitch diferentes (Trp258 5.15 vs 6.47 Å en 6PT0, Phase H).

---

## 5. Micronetwork — veredicto INDETERMINATE

Fuente: `results/conformational/micronetwork_modes_report.md` @ rama `feat/micronetwork-falsification-test`.

**Pregunta:** ¿HU-308 y HU-433 presentan microdescriptores locales reproduciblemente diferentes?

**Veredicto:** **`INDETERMINATE`**

| Estado receptor | Veredicto par | Hallazgo |
|-----------------|---------------|----------|
| **6PT0** | `IDENTICAL_LOCAL_MODES` | Δdist_Trp258 = 1.32 Å pero solo 1 componente > 0.3 Å (criterio DISTINCT requiere ≥2) |
| **6KPF** | `DISTINCT_LOCAL_MODES` | 2 componentes > 0.3 Å (Trp258, Ser285) |

**Interpretación (Nivel 2 epistemológico):** la divergencia del par enantiomérico es **dependiente del molde conformacional**. 6KPF **detecta** la divergencia; 6PT0 la **enmascara**. No promover DISTINCT en 6KPF como ley general del par; la discrepancia 6PT0/6KPF = **plasticidad de estado**, no fallo técnico aislado.

Descriptor congelado: `LOCAL_MICROSWITCH_VECTOR = [dist_Trp258, dist_Phe183, dist_Ser285, torsion_Trp258]`.

---

## 6. Phase H — veredicto ordinal INDETERMINATE

Fuente: `results/conformational/fase_h_ordinal_functional_report.md`.

**H1 veredicto:** `INDETERMINATE` — proyección conformacional insuficiente para separar tiers TOTAL/PARTIAL/INVERSE (1 proyección obtenida; se requieren ≥3).

**Mecanismo sugerido (no demostrado como ley):** orientación/conformación del ligando sobre el toggle switch Trp258 modula eficacia más que la distancia al centroide macro — coherente con Ganzoni *et al.* 2026 sobre continuo funcional vía Trp258^6.48.

---

## 7. Implicaciones para el programa (sin cómputo)

1. **No** reclamar que HU-433 es «mejor agonista» por Ki superior.
2. **No** usar docking 6PT0 como predictor determinista de tier Gi.
3. Próximo paso **solo encuadrado** (no ejecutar): ensayo Gi comparable HU-433 con normalización CP55,940 **o** MD μs con muestreo Trp258 — requiere orden PI explícita post-congelación.
4. Ver límites metodológicos en [`DOCKING_LIMITS_AND_GOVERNANCE.md`](DOCKING_LIMITS_AND_GOVERNANCE.md).

---

## 8. Trazabilidad

| Artefacto | Ruta |
|-----------|------|
| Phase H ordinal | `results/conformational/fase_h_ordinal_functional_report.md` |
| Micronetwork | `results/conformational/micronetwork_modes_report.md` |
| Falsificación previa | `results/conformational/micronetwork_falsification_report.md` |
| Calibración multistate | `docs/cb2_multistate_calibration_synthesis.md` |
| Phase E lit-activo FAIL | `results/docking/screening_patents_thcv_fase_e.md` |
| Atlas 8GUS | [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md) |

---

*Fin documento par HU-308/HU-433. Consolidación epistemológica — no autoriza inferencia funcional beyond auditado.*

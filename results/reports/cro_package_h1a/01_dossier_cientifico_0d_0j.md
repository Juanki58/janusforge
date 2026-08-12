# Dossier científico 0D–0J (CRO / PI) — Qiu-14

> **1 página.** Consolidación read-only. Sin nuevos cálculos.  
> **Fuentes:** integración 0D–0G, matriz 0I, visual QC 0J, plan 0K.  
> **Fecha paquete:** 2026-08-12

---

## 1. Demostrado / cerrado (cadena QC)

| Ítem | Estado |
|------|--------|
| Identidad 2D Qiu **14 / 15 / 20 / 24** (SMILES/InChI vs figuras+SI) | **PASS 4/4** (0D) |
| Prep PDBQT + auditoría bruta Qiu | **PASS 4/4** (0E) |
| Docking CB2 6PT0 ejecutado (config bloqueada) | **PASS 4/4** con observación log↔PDBQT en **15/20** (0F) |
| Análisis geométrico poses escritas | **PASS 4/4** (0G) |
| Integración 0D–0G / matriz 0I / auditoría 0H | **PASS WITH OBSERVATIONS** |
| Visual QC best poses (MODEL 1) vs claims 0G/0H | **0J = PASS** (6/6 checklist) |

**Qiu-14 (ancla H1):** chemotype *o*-morfolinofenil + CONH–1-adamantilo; SMILES 0D verificado; ocupación ortostérica-like CB2 en MODEL 1; Ad −x / N1-het +z; visual QC confirma orientación.

**Observaciones conservadas (no fallan QC de ejecución):** desajuste log/PDBQT por `energy_range` en 15/20; 0 H-bonds geometry-OK (proximidades polares ≠ H-bonds); PDF Elsevier completo no obtenido (0D vía CDN/SI).

---

## 2. Solo inferencia computacional (no actividad)

- Scores **Vina** (p.ej. Qiu-14 ≈ −9.9 kcal/mol) = salida de docking, **≠** Ki/IC₅₀/EC₅₀.  
- Co-ocupación de caja / Jaccard / Δcentroid / overlays 0J.  
- Correspondencias espaciales feature↔residuo (farmacóforo geométrico D2↔Qiu).  
- D2_20/06 *canonical_like* vs D2_22 *feature_swap* (geometría only).  
- Hipótesis literaria S173/S285 **sin** medida propia.

**Axioma:** pose-comparable ≠ mismo farmacóforo ≠ misma farmacología.

---

## 3. Aún no probado (wet)

| Claim | Estado |
|-------|--------|
| Agonismo CB2 de Qiu-14 **en panel propio** | **Unproven** → objetivo **H1-a** |
| Antagonismo CB1 / perfil Janus operativo | **Unproven** → H1-b tras H1-a PASS |
| Actividad / Janus / transferencia en análogos D2 | **Unproven** (H2/H3; fuera de este RFQ) |
| Utilidad antifibrótica monomolecular | **Unproven** |
| NCE Janusforge patentable | **No reclamable** hasta wet + counsel (ver 05) |

Literatura Qiu (Yin–Yang) = **motivación PUBLISHED**, no PASS janusforge. Ki/IC₅₀/EC₅₀ de tablas Qiu **no recuperados en repo** → no inventar umbrales.

---

## 4. Rol de Qiu-14

**Qiu-14 = vehículo de validación publicado**, no invención ni NCE Janusforge. Sirve para calibrar el ensayo CB2-first (H1-a). Copias directas = prior art científico (control), no producto.

---

## 5. Decisión de programa (cerrada)

**H1-a:** funcional **hCB2** con Qiu-14 → Go/No-Go.  
**Sin** más docking/MD/SAR en esta fase.  
Si H1-a PASS → plan H1-b (CB1). Si KILL → stop ancla Qiu-14 (QC luego pivot).

# Qiu 2023 — Integración QC 0D–0G

> **Alcance:** integración / QC de resultados **ya generados** (0D→0G). Sin docking, sin Vina, sin regeneración PDBQT, sin nuevos cálculos de farmacóforo, sin SAR ni interpretación farmacológica.
>
> **Fecha:** 2026-08-12
>
> **Fuentes (evidencia):**  
> [`qiu_0d_structure_verification.md`](qiu_0d_structure_verification.md) · [`qiu_0e_pdbqt_preparation.md`](qiu_0e_pdbqt_preparation.md) · [`qiu_0e_raw_pdbqt_audit.md`](qiu_0e_raw_pdbqt_audit.md) · [`qiu_0f_docking_protocol.md`](qiu_0f_docking_protocol.md) · [`qiu_0f_docking_qc.md`](qiu_0f_docking_qc.md) · [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md) · [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md) · [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md)

---

## 1. Resumen ejecutivo

| Paso | Objetivo | Estado | Evidencia | Observaciones |
|------|----------|--------|-----------|---------------|
| **0D** | Verificación estructural 2D (SMILES/InChI) Qiu 14/15/20/24 | **PASS 4/4** | `qiu_0d_structure_verification.md` | Estructuras YES; sin PDBQT/docking |
| **0E** | Preparación PDBQT + auditoría bruta | **PASS 4/4** | `qiu_0e_pdbqt_preparation.md`, `qiu_0e_raw_pdbqt_audit.md` | SMILES exactos vs 0D; carga formal 0; discrepancias no-fallo (stereo InChI, H polar, Σq≈0) |
| **0F** | Docking CB2 6PT0 ejecutado (protocolo bloqueado) | **PASS 4/4** (con observación) | `qiu_0f_docking_protocol.md`, `qiu_0f_docking_qc.md` | rc=0 ×4; **15 y 20:** log reporta 1 pose más que MODELs en PDBQT (`energy_range`) |
| **0G** | Análisis geométrico de poses escritas | **PASS 4/4** | `qiu_0g_pose_analysis.md` | Región de unión comparable; scores = Vina only |
| **Farmacóforo geom.** | Mapa feature↔residuo D2↔Qiu (best poses) | **COMPLETE** | `qiu_0g_vs_d1_pharmacophore_geometry.md` | Correspondencias parciales; D2_22 orientación intercambiada; no elevar D2_22 por Vina |

**Veredicto global de la cadena:** **PASS WITH OBSERVATIONS** (ver §7).

---

## 2. Cadena de trazabilidad

Para cada compuesto **14 / 15 / 20 / 24**:

```
0D (SMILES verificado)
  → 0E (PDBQT ligando; REMARK SMILES = SMILES 0D)
    → 0F (Vina CB2 6PT0; out PDBQT + log)
      → 0G (análisis de MODELs escritos en out PDBQT)
        → [contexto] comparación D1 + farmacóforo geométrico (best poses)
```

| Cpd | 0D | 0E ligando | 0F out | 0G |
|-----|----|------------|--------|-----|
| 14 | PASS | `results/docking/qiu_0e/compound_14_lig.pdbqt` | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` | PASS |
| 15 | PASS | `results/docking/qiu_0e/compound_15_lig.pdbqt` | `results/docking/qiu_0f/compound_15_cb2_out.pdbqt` | PASS |
| 20 | PASS | `results/docking/qiu_0e/compound_20_lig.pdbqt` | `results/docking/qiu_0f/compound_20_cb2_out.pdbqt` | PASS |
| 24 | PASS | `results/docking/qiu_0e/compound_24_lig.pdbqt` | `results/docking/qiu_0f/compound_24_cb2_out.pdbqt` | PASS |

Comprobación read-only de existencia (2026-08-12): **8/8 rutas True** (4×0E + 4×0F).

### Puntos de trazabilidad imperfecta (documentados, no “resueltos”)

1. **0D:** PDF Elsevier/SSRN no obtenido; verificación apoyada en figuras CDN + SI (`mmc1`) — suficiente para 2D inequívoco según 0D, pero no es el PDF completo.
2. **0E→0D stereo:** InChIKey de conectividad coincide; capa estereo absoluta aparece en round-trip 3D Meeko (no en 0D stereo-omitted).
3. **0F→0G (15, 20):** modos presentes en el **log** pero **no** escritos en el PDBQT de salida (ventana `energy_range` por defecto del motor) — 0G analiza solo MODELs escritos.
4. **0E protonación:** aminas terciarias conservadas neutras “as drawn”; fracción protonada a pH fisiológico no explorada.
5. **Comparación D1 / farmacóforo:** pipelines de prep D1 vs Qiu 0E/0F pueden diferir; mismo receptor PDBQT.

---

## 3. QC de estructuras

| Cpd | SMILES 0D | Correspondencia 0E | PDBQT (0E) | n_atoms / carga | QC bruto 0E | Estado |
|-----|-----------|--------------------|------------|-----------------|-------------|--------|
| **14** | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | REMARK SMILES exacto; InChIKey conectividad `QQXQVTJJXRACOB`; chemotype o-morph + CONH-Ad | `results/docking/qiu_0e/compound_14_lig.pdbqt` | 38 / formal 0 (Σq≈+0.002) | PASS | **PASS** |
| **15** | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1` | REMARK SMILES exacto; InChIKey `ZVVBFOFPAAUAGH`; m-morph + CONH-Ad | `results/docking/qiu_0e/compound_15_lig.pdbqt` | 38 / formal 0 (Σq≈+0.002) | PASS | **PASS** |
| **20** | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1` | REMARK SMILES exacto; InChIKey `ZWCGYXUFIUXGBQ`; o-Me-piperazine + CONH-Ad | `results/docking/qiu_0e/compound_20_lig.pdbqt` | 39 / formal 0 (Σq≈+0.002) | PASS | **PASS** |
| **24** | `Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | REMARK SMILES exacto; InChIKey `RAQAMHLYXWAFRF`; o-morph + CONH-CH₂-Ad | `results/docking/qiu_0e/compound_24_lig.pdbqt` | 39 / formal 0 (Σq=0.000) | PASS | **PASS** |

**0D prior:** PASS 4/4. **0E prior (prep + audit):** PASS 4/4. Sin mismatches de SMILES / regioisómero / carga que fallen QC.

---

## 4. QC del docking

Configuración bloqueada (idéntica ×4; fuente: protocolo + QC 0F):

| Campo | Valor |
|-------|-------|
| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` |
| Box | center 98.379 / 109.559 / 123.801; size **22** × 22 × 22 |
| exhaustiveness | **8** |
| num_modes | 9 |
| seed | **42** |
| energy_range | omitido (default del motor) |
| Motor | AutoDock Vina **1.2.7** |

| Cpd | rc | Poses (log) | Poses escritas (PDBQT MODEL) | Mejor score (kcal/mol) | Config vs protocolo | Observaciones |
|-----|----|-------------|------------------------------|------------------------|---------------------|---------------|
| 14 | 0 | 9 | 9 | −9.919 | YES | Sin errores |
| 15 | 0 | 9 | **8** | −11.201 | YES | **Log reporta 1 pose más que la escrita en PDBQT** (`energy_range`) |
| 20 | 0 | 6 | **5** | −9.986 | YES | **Log reporta 1 pose más que la escrita**; además &lt;9 modos distintos en log |
| 24 | 0 | 9 | 9 | −11.606 | YES | Sin errores |

**Scores = números Vina observados; NO afinidad experimental.**

**0F prior:** PASS 4/4 con la observación de conteo log/PDBQT en 15 y 20 — se conserva aquí sin reinterpretar ni “arreglar”.

---

## 5. QC del análisis geométrico

### 5.1 Pose analysis Qiu (0G)

**`0G = PASS 4/4`** para compuestos Qiu 14 / 15 / 20 / 24 (poses escritas; región de unión comparable; sin H-bonds geometry-OK bajo criterio 0G).

### 5.2 Farmacóforo geométrico D2 ↔ Qiu (feature-by-feature)

Fuente obligatoria: [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md).  
Axioma explícito: **pose-comparable ≠ mismo farmacóforo ≠ misma farmacología**.

#### Correspondencias espaciales recurrentes (inferencia estructural; cutoffs centroid ≤3.0 Å o shell Jaccard ≥0.25)

| Pareja hipotética (geometría) | spatial_ok |
|-------------------------------|------------|
| **pirrol D2 ↔ pirazol Qiu** | **12/12** |
| **aril-cetona ↔ amida** | **8/12** |
| **benzoílo ↔ adamantilo** | **8/12** |
| **C2-Ph ↔ C5-Ph** | **8/12** |
| **C5-Me ↔ C4-Me** | **8/12** |
| **N-bencilo ↔ N1-heterociclo** | **6/12** |

(Grupo aril-cetona / benzoílo / C2-Ph / C5-Me ↔ amida / Ad / C5-Ph / C4-Me: cada eje listado arriba a **8/12**, salvo N-bencilo↔N1-heterociclo a **6/12**.)

#### Mismatches / no-correspondencias indicadas

- **n1_benzyl_aryl ↔ n1_phenyl:** spatial_ok solo **1/12** — no tratar como elemento farmacofórico conservado cross-chemotype.
- Adamantilo / CONH–Ad / morfolina–piperazina: presentes en Qiu; **ausentes** en D2_20/06/22.
- Aril-cetona vs CONH–Ad: coincidencia espacial posible; **no** identidad química.
- **D2_22 orientación intercambiada** vs D2_20/06: en D2_20/06, `benzoyl_aryl` solapa Ad/amida Qiu (shell THR114/ILE110/ILE186); en D2_22, `benzoyl_aryl` se acerca a n1_heterocycle/c5_phenyl Qiu mientras `n1_benzyl_pCl` se acerca a adamantilo — *feature swap* (solo geometría).
- **Advertencia:** no elevar **D2_22** por score Vina (lead histórico; overlap mid-pack; Vina más negativo ≠ más “Qiu-like”).

#### Separación epistémica

| Nivel | Contenido permitido aquí |
|-------|--------------------------|
| **Observación** | Coordenadas, REMARK Vina, hits SMARTS, distancias a cutoffs fijos, conteos spatial_ok |
| **Inferencia** | Flags spatial_ok / shell Jaccard; “orientación intercambiada” de D2_22 |
| **NO se puede concluir** | Actividad, afinidad experimental, selectividad, mecanismo, SAR, “mismo farmacóforo” o “misma farmacología” a partir de pose-comparable |

---

## 6. Discrepancias / limitaciones

Enumeración (sin resolución artificial):

1. **15 — log vs PDBQT:** log 9 modos / PDBQT 8 MODELs (+1 fuera de ventana `energy_range` por defecto).
2. **20 — log vs PDBQT:** log 6 modos / PDBQT 5 MODELs (+1 fuera de ventana); además &lt;`num_modes=9` modos distintos en log.
3. **0G / farmacóforo** usan solo poses **escritas** → el paisaje energético más allá de esas poses queda desconocido.
4. Stereo InChIKey 0E round-trip vs 0D stereo-omitted (conectividad OK).
5. PDBQT Meeko: solo H polar; fórmula completa vía Meeko→RDKit.
6. Σq parcial ≈ +0.002 (14/15/20) — redondeo Gasteiger; carga formal 0.
7. Protonación fisiológica de aminas terciarias no explorada (neutras as drawn).
8. Receptor estático único (6PT0 agonista); sin MD/ensamble.
9. **Vina score ≠ afinidad experimental.**
10. Cutoffs de contacto/correspondencia (4.0 Å; 3.0 Å / Jaccard 0.25) son heurísticos.
11. Chemotipos distintos Qiu vs URB447/D2 → no hay transferencia de Ad a un set atómico D2.
12. PDF fuente Qiu no obtenido; 0D apoyado en CDN figuras + SI.
13. Pipelines prep D1 vs Qiu pueden diferir en comparación cross-serie.

---

## 7. Veredicto global

**PASS WITH OBSERVATIONS**

Motivo breve: la cadena 0D→0E→0F→0G cierra **PASS 4/4** en cada paso para Qiu 14/15/20/24, con artefactos presentes y config 0F coherente; permanece la observación documentada y no cerrada de **desajuste log/PDBQT por `energy_range` en compuestos 15 y 20**, más las limitaciones geométricas/farmacóforo (incl. D2_22) que no invalidan el QC de ejecución pero impiden un PASS limpio de la cadena integrada.

---

## Cierre

Este informe **no autoriza** SAR, conclusiones farmacológicas, ni nuevos cálculos (docking, PDBQT, farmacóforo). Solo integra evidencia ya generada.

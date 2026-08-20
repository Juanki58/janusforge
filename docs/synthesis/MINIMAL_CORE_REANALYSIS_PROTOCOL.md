# Protocolo cerrado — reanálisis READ-ONLY del núcleo mínimo CB2→Gαi

**Fecha:** 2026-08-20  
**Rama:** `feat/cb2-minimal-gi-core-reanalysis`  
**Modo:** `READ_ONLY / PUBLIC_DATA_REANALYSIS`  
**Estado:** Pre-registrado **antes** de cómputo de métricas de red / leave-one-out.

### Gobernanza (obligatoria)

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
CONTRACT_v1.0: ARCHIVED_HISTORICAL
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
```

Regla central: **ningún** criterio / peso / conjunto de nodos / umbral se modifica tras ver resultados para favorecer un outcome.  
La palabra **switch** **no** se usa como conclusión confirmada.  
No Fase I. No diseño molecular. No docking. No retuning Contract v1.0.

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[INTERNAL_REANALYSIS]** | Cómputo Janusforge sobre objetos públicos recuperados |
| **[PRIMARY_LITERATURE]** | Afirmación del paper fuente |
| **[COMPUTATIONAL_LITERATURE]** | Resultado computacional publicado (no re-ejecutado) |
| **[SUPPORTED_INTERPRETATION]** | Inferencia acotada a datos en mano |
| **[HYPOTHESIS]** | No demostrada aquí |
| **[CONTRADICTORY_EVIDENCE]** | Conflicto abierto preservado |
| **[INDETERMINATE]** | Bloqueado / irreproducible / datos incompletos |

---

## 1. Preguntas (fijas)

**Primaria:** ¿Puede la red de comunicación CB2 asociada a Gαi reducirse a un conjunto pequeño de nodos cuya función sea robusta a remoción de nodos?

**Secundaria:** ¿Ese conjunto mínimo es arquitectónicamente distinto en CB1?

---

## 2. Fuentes permitidas (identidad)

### A — Morales-Pastor et al. 2025

- **Cita:** Morales-Pastor, A. et al. *Nat Commun* **16**, 5265 (2025).
- **DOI:** `10.1038/s41467-025-60003-0`
- **PMID:** `40500255`
- **PMC:** `PMC12159191`
- **MD:** GPCRmd publication `1540` — `https://gpcrmd.org/dynadb/publications/1540/`
- **Código:** `https://github.com/GPCRmd/prefcoup_cb2r` ; Zenodo `10.5281/zenodo.15270434`
- **Sistema:** CB2R + agonista HU-210; mutantes PrefCoup Gαi2 (**14**) / Coup Gαi2_βarr1 (**20**) + WT; PDB de soporte **6KPC**, **5ZTY**, **6KPF**.

### B — Dutta & Shukla 2023 (MSM / VAMPnets) — **no** Li 2023

- **Cita:** Dutta, S. & Shukla, D. *Commun Biol* **6**, 485 (2023).
- **DOI:** `10.1038/s42003-023-04868-1`
- **PMC:** `PMC10163236`
- **Código:** `https://github.com/ShuklaGroup/Cannabinoid_activation`
- **Box (traj/MSM):** URL publicada en Data availability del paper.
- **Nota:** Li et al. 2023 (`10.1038/s41467-023-37112-9`) = cryo-EM únicamente; **no** es la fuente MSM/VAMPnets.

### C — PDB solo como soporte estructural

No inventar métricas nuevas ni sustituir trayectorias faltantes con docking.

---

## 3. Objeto grafo (pre-registrado)

```
ortostérico → red de comunicación (LigACN/ACN) → TM5/TM6/TM7 → interfaz intracelular → región asociada a Gαi
```

- **Nodos / aristas:** solo entidades presentes en el dataset fuente recuperado.
- **Objeto primario si Supp Data 3 está disponible:** matriz de **degeneracy / information transmission** (frecuencia en 100 caminos más cortos bolsillo→sitio intracelular) — métrica primaria del paper.
- **No** añadir residuos porque “parezcan importantes”.

---

## 4. Métricas (lista cerrada — no shopping post hoc)

1. **information_transmission (degeneracy)** — primaria (paper)
2. degree  
3. betweenness  
4. closeness  
5. shortest-path participation  
6. orthosteric ↔ intracellular connectivity (binaria / nº caminos)  
7. path redundancy  

Sin mezclar métricas incompatibles sin normalización explícita pre-registrada (aquí: no se introduce normalización nueva).

---

## 5. Definición de «núcleo mínimo» (antes de resultados)

**Candidate core** = subconjunto mínimo de nodos cuya **remoción** rompe de forma reproducible la conectividad **ortostérico ↔ región asociada a Gαi** en el grafo LigACN publicado.

### Procedimiento fijo (A→E)

- **A** Candidatos: nodos con transmission > 0 en WT LigACN **o** unión (paper) de alta transmisión ∩ alta conectividad — **sin** reordenar tras ver LOO.
- **B** Leave-one-out: remover cada nodo candidato individualmente; registrar pérdida de conectividad S↔T.
- **C** Pérdida de conectividad: `connected(S,T)` pasa de True→False, o nº de caminos simples acotados cae a 0 (definición operativa: `networkx.has_path` tras remoción).
- **D** Remoción iterativa **solo** si A–C están fijados; tamaño de core **no** se optimiza tras ver resultados.
- **E** Robustez: réplicas/mutantes en Supp Data 3 si matrices disponibles; leave-one-replica-out **solo** si contactos por réplica recuperados.

### Sets S (ortostérico) y T (intracelular / Gαi)

Pre-registro:

- **S:** nodo ligando publicado en la matriz (`8D0:1` si presente) **más** sus vecinos con weight>0 en WT degeneracy — derivados **solo** del objeto publicado.
- **T:** lista de sinks del paper (sitio de acoplamiento intracelular). **Si la lista exacta no es recuperable del SI/código sin inferencia ad hoc → bloquear búsqueda de core y emitir `INDETERMINATE`.**

No inventar T desde “TM intracellular halves” si el paper no aporta la lista en datos recuperados.

---

## 6. Veredictos (etiquetas exactas)

| Código | Uso |
|--------|-----|
| `CORE_FOUND` | Subconjunto reducido rompe S↔T de forma reproducible bajo procedimiento A–E |
| `NETWORK_DISTRIBUTED` | No hay núcleo separable; redundancia impide ruptura por remoción mínima pre-registrada |
| `CB2_SPECIFIC_CORE` | `CORE_FOUND` **y** patrón CB1 distinto, no artefacto de una sola representación, soportado por datos públicos |
| `INDETERMINATE` | Datos esenciales faltantes / representación no reproducible / conflicto irresoluble / comparación CB1 inválida |

**CB1_COMPARISON** (solo **después** de cerrar CB2): `DISTINCT` | `SIMILAR` | `INDETERMINATE`

Prohibido: FAIL, SUCCESS, VALIDATED SWITCH.

---

## 7. Orden de ejecución (obligatorio)

1. Escribir este pre-registro (+ `results/network_core/preregistration.md`).
2. Data audit → `data_audit.json` + `data_audit.md` (checksums, versiones, confirmación receptor/ligando).
3. Análisis **solo** si datos recuperables; si no → stubs + `FINAL_VERDICT=INDETERMINATE` + blocker exacto.
4. Énfasis del informe: **recuperación / provenance / reproducibilidad PRIMERO**; métricas/core/veredicto **después**.
5. **DETENER EJECUCIÓN.** Sin siguiente fase.

---

## 8. Alineación proyecto (sin reabrir umbrales)

**[INTERNAL_REANALYSIS / OBSERVACIÓN_PROPIA previa]** Phase G GENERALIZES; Phase H INDETERMINATE; micronetwork INDETERMINATE.  
**[PRIMARY_LITERATURE]** LigACN no se reduce a Trp258^6.48 (Morales-Pastor 2025).  
Contradicciones abiertas HU-433 / AM630 / Trp258 permanecen **ABIERTA** — no armonizar.

---

*Fin pre-registro. Cualquier cómputo de red posterior a esta fecha debe citar este archivo como locked.*

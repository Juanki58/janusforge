# Experiment — EXTERNAL: Mnpotra 2014 CB2–Gi crosslinking vs modern complex structures

**Fecha pre-registro:** 2026-10-19  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — definiciones y reglas de veredicto locked **antes** del call estructural.  
**Scope:** **`EXTERNAL_CB2_GI_CROSSLINK_2014`** — nota bibliográfica + comparación estructural de parejas de entrecruzamiento CB2↔Gαi1 sobre PDBs CB2–Gi locales.  
**PI authorization:** YES (decisión PI 2026-10-19: lead crosslinking 2014 primero; tráfico 2025 como confusor; probes/GRAB diferidos).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Extraer parejas XL publicadas (secuencia + química) | Tratar XL como mapa de distancias **intramoleculares** de CB2 |
| Medir Cα–Cα CB2↔Gαi en complejos públicos locales | Claim funcional Gi; “XL prueba hubs Janusforge”; cerrar P3 |
| Contrastar con panel atlas CB2–Gi | Reabrir P2; avanzar P5; docking / de novo; Tier B MD |
| Veredicto `EXT_CB2_GI_XL_STRUCTURAL_*` | Inventar mapa de residuos Abrol si el numerado es ambiguo |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P5_MEMBRANE                     = HYPOTHESIS_READY; NOT advanced   # unchanged
P3_EFFECTOR                     = BLOCKED                          # unchanged
Gi_FUNCTIONAL_CLAIM             = FORBIDDEN
XL_MEASURES                     = INTERMOLECULAR_PROXIMITY_ONLY
HUB_CLAIM_FROM_XL               = FORBIDDEN
EXT_CB2_GI_XL_STRUCTURAL_*      = NEW (this experiment)
```

**Explicit non-claim (locked):**

> El entrecruzamiento químico reporta **proximidad intermolecular** CB2↔Gαi compatible con la geometría del reactivo.  
> **No** es una restricción de trayectoria alostérica intramolecular, **no** demuestra hubs Janusforge, y **no** cierra P3.

**Pregunta discriminante (locked):**

> ¿Las tres parejas XL de Mnpotra 2014 caen dentro de las ventanas Cα–Cα del paper en el panel moderno CB2–Gi (cryo/X-ray local), o hay tensión geométrica / residuos no mapeables (`INDETERMINATE`)?

---

## Bibliographic note (locked a priori)

| Field | Value |
|-------|-------|
| Citation | Mnpotra et al., *J. Biol. Chem.* 289:20259–20272 (2014) |
| DOI | [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916) |
| PMID | 24855641 |
| PMC | [PMC4106340](https://pmc.ncbi.nlm.nih.gov/articles/PMC4106340/) |
| Method | HgCl2 (Cys–Cys) + DSS (Lys–Lys); LC-MS/MS / ESI-MS/MS |
| MD in paper | Usa XL como **validación**, no como restraint de fuerza — no convertir MD 2014 en evidencia de ruta alostérica Janusforge |

### Experimental XL pairs (sequence numbers authoritative)

| Pair ID | CB2 | Gαi1 | Chemistry | Cα–Cα window (paper) |
|---------|-----|------|-----------|----------------------|
| `C134_C351` | Cys134 (BW label **C3.53** abstract / **C3.54** Results) | Cys351 (α5, i-3) | HgCl2 | **7–10 Å** |
| `K245_K349` | Lys245 **K6.35** | Lys349 (α5, i-5) | DSS | **≤24.2 Å** |
| `K215_K317` | Lys215 **K5.64** | Lys317 (α4β6) | DSS | **≤24.2 Å** |

**Pro139** (ICL2) ↔ bolsillo hidrofóbico Gαi (Val34, Leu194, Phe196, Phe336, Thr340, Ile343, Ile344): contacto de **registro MD** del paper — se reporta aparte; **no** es XL experimental.

---

## Structures (locked)

### Primary panel (cryo/X-ray CB2–Gi locales)

`6PT0`, `6KPF`, `8GUR`, `8GUS`, `8GUQ`, `8GUT`, `8X3L` under `data/external/cb2_landmark_expanded/`.

### Negative / no-Gi controls

`5ZTY`, `6KPC`, `9U7L` (local file sin Gi) → call esperado `N/A_NO_GI`.

### Secondary (optional; fail-closed)

Abrol/Heo avg frames Gi — **solo si** cadenas/residuos Gαi son identificables sin inventar offset. Si numeración fusionada ambigua → `NO_GAI_MAP` / no fuerza veredicto primario.

---

## Metrics (locked)

Por estructura con Gi mapeable, para cada pareja XL:

1. Localizar Cα CB2 y Cα Gαi por número de secuencia del paper.  
2. Distancia Cα–Cα (Å).  
3. Call: `WITHIN` (en ventana), `BORDERLINE` (margen pequeña; Cys: ±2–3 Å fuera de 7–10 como el start pose 10.6 Å del paper), `OUT`, `MISSING`.

Pro139: distancia mínima Cα a residuos del bolsillo Gαi listados arriba (informativo).

---

## Aggregate verdict rules (locked)

Evaluar **solo** el panel primario (≥3 estructuras OK):

| Call | Criterio |
|------|----------|
| **`EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED`** | Las 3 parejas con fracción `WITHIN` ≥0.70 |
| **`EXT_CB2_GI_XL_STRUCTURAL_PARTIAL`** | Lys–Lys ≥0.70 WITHIN y Cys WITHIN/BORDERLINE combinado ≥0.70, o mezcla sin mayoría OUT |
| **`EXT_CB2_GI_XL_STRUCTURAL_TENSION`** | ≥1 pareja con OUT en >50% del panel primario |
| **`EXT_CB2_GI_XL_STRUCTURAL_INDETERMINATE`** | <3 estructuras primarias mapeables |

Secondary annotation (no override): Abrol `NO_GAI_MAP` si aplica.

---

## Outputs (locked)

| Artefacto | Path |
|-----------|------|
| Pre-reg (este) | `docs/synthesis/EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md` |
| Report | `results/network_core/ext_cb2_gi_crosslink_2014.md` |
| Machine | `results/network_core/ext_cb2_gi_crosslink_2014.json` |
| Helper | `scripts/network_core/ext_cb2_gi_crosslink_2014.py` |

---

## Fail-closed

- No inventar distancias intramoleculares CB2 desde XL.  
- No promover compatibilidad geométrica a mecanismo Gi o hubs.  
- No mapear Abrol con offset ad hoc.  
- No reopen P2; no advance P5.

---

## Run

```text
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/ext_cb2_gi_crosslink_2014.py
```

---

*Fin pre-registro. EXTERNAL discrimination-only.*

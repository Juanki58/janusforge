# Experiment — EXTERNAL: ESMDynamic soft proxy on human CB2 sequence

**Fecha pre-registro:** 2026-09-12  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ver mapas / overlap / veredictos.  
**Scope:** **`EXTERNAL_ESMDYNAMIC`** — aplicar (o recuperar predicciones publicadas de) **ESMDynamic** (Kleiman, Feng, Xue, Shukla; Nat Commun, DOI [10.1038/s41467-026-76361-2](https://doi.org/10.1038/s41467-026-76361-2)) a la secuencia **UniProt P34972** (CB2 humano) como **proxy suave** de fluctuación de contactos dinámicos.  
**PI authorization:** YES — proceder **sin** esperar filelist Dutta/Shukla (“avancemos porque sinceramente no confío nada en que nos conteste nadie”).

---

## Epistemology (HARD LOCK)

| Allowed | Forbidden |
|---------|-----------|
| Proxy **AI/secuencia** de contactos dinámicos / alta varianza predicha | Sustituir probabilidades de contacto **por macroestado MSM** |
| Overlap descriptivo con seis hubs LigACN (índices UniProt) | Reabrir P2 como `CONVERGENT` |
| Soft compare vs priors `EXT_APO_PILOT_*` / `EXT_PDB_CONTACTS_STATE_DEPENDENT` | Afirmar mecanismo Gi / docking / de novo / retune hubs |
| Etiquetas `EXT_ESMDYNAMIC_*` **provisionales / soft** | Validación experimental de ESMDynamic en CB2 en este lab |
| Documentar blocker → `INDETERMINATE_UNAVAILABLE` + alternativa EXTERNAL sin autores | Fingir alineación traj↔MSM filelist |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C                = ABORTED                          # unchanged
EXT_MSM_STATE_CONTACTS          = INDETERMINATE_NO_ALIGNMENT       # unchanged; no fake filelist
EXT_APO_PILOT_* / EXT_PDB_*     = PRIOR (soft compare only)
EXT_ESMDYNAMIC_*                = NEW (provisional soft proxy)
```

**Explicit non-claims:**

1. ESMDynamic **≠** MSM-state contact probabilities.  
2. Resultado **no** reabre P2 ni arquitectura A/B/C.  
3. **No** claim de mecanismo Gi.  
4. No hay validación experimental de ESMDynamic sobre CB2 en este laboratorio; límites pre-registrados.  
5. Soft compare con pilots/PDB es **clase narrativa**, no promoción de ensemble.

---

## Questions (locked)

1. ¿Es factible obtener predicciones ESMDynamic para P34972 en este entorno (inferencia local / Docker / predicciones proteoma publicadas)?
2. Si sí: ¿qué fracciones de edges de alta `dynamic_prob` (y/o baja ocupación con alta dinámica) involucran los seis hubs LigACN vs null residual?
3. ¿El perfil hub-centric de “contactos dinámicos predichos” es compatible, en sentido **soft**, con priors `EXT_PDB_CONTACTS_STATE_DEPENDENT` vs `EXT_APO_PILOT_CONTACTS_INDETERMINATE`?
4. Si la corrida falla temprano (GPU/pesos/licencia/Docker): ¿queda documentado `EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE` y se ejecuta la alternativa EXTERNAL sin autores (TM6/toggle en `CB2_APO.zip` por filename active/inactive)?

---

## Data / software (locked a priori)

| Item | Value |
|------|-------|
| Sequence | UniProt **P34972** (misma cadena ya usada en pilots MSM/PDB del repo) |
| Hubs (UniProt indices) | ALA79, ALA83, LEU287, ASN291, ASN295, ARG302 |
| Offset note | UniProt↔topo MD típico ~−20 en construct Dutta; **este experimento usa índices UniProt** (secuencia completa). No re-mapear hubs post hoc. |
| Paper | DOI [10.1038/s41467-026-76361-2](https://doi.org/10.1038/s41467-026-76361-2) |
| Code | [ShuklaGroup/esmdynamic](https://github.com/ShuklaGroup/esmdynamic) (MIT) |
| Weights / proteome | Illinois Data Bank [10.13012/B2IDB-3773897_V2](https://doi.org/10.13012/B2IDB-3773897_V2) |
| Preferred temperature for primary metrics | **320 K** (recomendación autores; otras T = sensibilidad anotada) |
| Contact geometry in ESMDynamic | Cα-based dynamic contacts (definición del paper/modelo) — **≠** VdW+0.5 Å del pipeline P1 |

**Preferencia de obtención (orden):**

1. Inferencia `run_esmdynamic` con pesos oficiales si el entorno lo permite.  
2. Predicción ya publicada del human proteome para el ID UniProt/CNR2 si el shard es descargable sin archivar decenas de GB.  
3. Si (1)–(2) fallan temprano → `INDETERMINATE_UNAVAILABLE` + **alternativa** (abajo).  
4. Next-best local (solo si documentado): cabeza de contactos ESM liviana ya en repo — **no** preferido frente a ESMDynamic real.

Pesos / checkpoints / tar.xz grandes → **gitignore**; no commit.

---

## Metrics (locked a priori)

Primary analysis temperature: **320 K**.

| Symbol | Definition |
|--------|------------|
| \(D_{ij}\) | `dynamic_prob` predicted at 320 K |
| \(F_{ij}\) | `frequency_pred` (occupancy) at 320 K |
| \(E_{\mathrm{dyn}}(\tau_d)\) | undirected pairs with \(D_{ij} \ge \tau_d\), \(\|i-j\| \ge 6\) |
| \(E_{\mathrm{switch}}(\tau_d,\tau_f)\) | \(D_{ij} \ge \tau_d\) **and** \(F_{ij} \le \tau_f\) (high dynamics, not always-on) |
| Hub-touching edge | pair where **at least one** endpoint ∈ hub UniProt set \(H\) |
| `hub_edge_frac_dyn` | \|{e ∈ \(E_{\mathrm{dyn}}\): hub-touching}\| / \|E_dyn\| |
| `hub_degree_dyn[h]` | degree of hub \(h\) in \(E_{\mathrm{dyn}}\) |
| Enrichment | compare `hub_edge_frac_dyn` vs expectation under random residue degree-matched null (**n_null = 200**, seed `20260912`) |

**Locked thresholds:**

| Parameter | Value |
|-----------|-------|
| \(\tau_d\) (primary) | **0.5** (mismo umbral binario del paper para `dynamic_pred`) |
| \(\tau_d\) (stringent report) | **0.7** (anotación) |
| \(\tau_f\) (switch filter) | **0.7** (ocupación no “siempre on”) |
| Seq separation | \|i−j\| ≥ 6 |
| Null | exact \|H\|=6 residue labels redrawn from non-hub residues with same AA type when possible; else uniform residues with degree in graph |

---

## Verdict rules (provisional soft)

| Label | A priori rule |
|-------|----------------|
| `EXT_ESMDYNAMIC_HUB_ENRICHED` | Primary \(E_{\mathrm{dyn}}(0.5)\) hub-edge fraction significantly > null (empirical p ≤ 0.05, upper tail) **and** ≥ 4/6 hubs have degree ≥ 1 |
| `EXT_ESMDYNAMIC_HUB_NOT_ENRICHED` | p > 0.05 **or** < 4/6 hubs touch any dyn edge; clean negative |
| `EXT_ESMDYNAMIC_INDETERMINATE` | Maps obtained but sparse/empty \(E_{\mathrm{dyn}}\), hub map fail, or null underpowered |
| `EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE` | Cannot run / download model or proteome shard in this session |

**Soft compare (annotation only; never upgrades P2):**

| Label | Rule |
|-------|------|
| `EXT_ESMDYNAMIC_SOFT_COMPAT_PDB_B` | Narrative: high predicted dynamics around hubs / switching edges present — **compatible with** state-dependence story of PDB snapshot B (**not** evidence of MSM states) |
| `EXT_ESMDYNAMIC_SOFT_COMPAT_PILOT_INDET` | Diffuse / non-hub-centric dynamics — closer in spirit to filename-pilot INDETERMINATE |
| `EXT_ESMDYNAMIC_SOFT_COMPARE_NA` | UNAVAILABLE / INDETERMINATE without usable map |

Never write `P2_CONVERGENT` from this experiment.

---

## Failure modes (pre-registered)

| Failure | Action |
|---------|--------|
| Docker daemon down / no CUDA toolkit match | Document; try proteome shard or CPU/`--low_memory`; else UNAVAILABLE |
| VRAM OOM (GTX 1060 6 GB expected risk) | `--low_memory` / CPU; if still fail → UNAVAILABLE |
| Weights / openfold / torch install fails | Document blocker → UNAVAILABLE |
| Proteome archive too large to fetch shard | UNAVAILABLE (do not fake partial maps) |
| Sequence length / truncation mismatch vs UniProt | Flag `SEQ_MISMATCH`; do not retune hubs |

---

## Fallback EXTERNAL (same session if ESMDynamic fails early)

**Name:** `EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME`  
**Data:** local `CB2_APO.zip` / cached `_pilot_sample` + topology already in repo.  
**Stratification:** filename `*_inactive_*` vs `*_active_*` (**start-label proxy only** — **≠** MSM macrostate; explicit in report).  
**Features (locked):** all 24 Cα–Cα pairs from `x8_reduced_featurization_msm.py` `REDUCED_CA_PAIRS` (UniProt P34972 indices → topo via NW; expect ~−20).  
**Primary toggle subset (a priori):** pairs #1–3, #5, #10–11 (TM3–TM6 IC / Trp6.48–NPxxY corridor):  
`(131,245), (131,240), (131,258), (211,258), (258,291), (258,295)`.  
**Sampling:** prefer existing `_pilot_sample` (5+5) or primary 1+1 pilots; frame stride such that ≤200 frames/traj; seed `20260912`.  
**Per-feature stats:** mean±std (Å) per filename label; Cohen's d (inactive→active); two-sided Mann–Whitney U on pooled frames (descriptive; frames not independent).  

| Label | A priori rule |
|-------|----------------|
| `EXT_APO_TM6_TOGGLE_SEPARATED` | ≥4/6 primary pairs have \|d\| ≥ 0.8 **and** same sign pattern expected for activation on ≥3 of {131–245, 131–240, 131–258} (active mean **larger** IC opening) |
| `EXT_APO_TM6_TOGGLE_OVERLAP` | <2/6 primary pairs reach \|d\| ≥ 0.8 |
| `EXT_APO_TM6_TOGGLE_INDETERMINATE` | else, or hub/topo map fail, or insufficient frames |
| Soft | Never MSM; never P2 CONVERGENT; filename ≠ metastable state |

**Verdicts:** `EXT_APO_TM6_TOGGLE_*` only; soft; does **not** invent MSM alignment.

---

## Outputs

| Path | Content |
|------|---------|
| `docs/synthesis/EXPERIMENT_CB2_ESMDYNAMIC.md` | This pre-registration |
| `scripts/network_core/cb2_esmdynamic.py` | Runner / analyzer |
| `results/network_core/cb2_esmdynamic.{md,json}` | Report + machine payload + SHA |
| Optional fallback | `results/network_core/cb2_apo_tm6_toggle.{md,json}` |

Do **not** commit model weights, `*.pt` hub caches, or proteome `*.tar.xz`.

---

## CLI (intended)

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_esmdynamic.py
# if UNAVAILABLE early:
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_apo_tm6_toggle.py
```

---

*Fin pre-registro. No editar umbrales ni lista de hubs después de ver mapas o p-valores.*

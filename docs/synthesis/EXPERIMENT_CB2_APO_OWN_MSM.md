# Experiment — EXTERNAL: CB2_APO **own** MSM → contacts / π by **our** states

**Fecha pre-registro:** 2026-09-12  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ver ITS / contactos / veredictos.  
**Scope:** **`EXTERNAL_OWN_MSM_CB2_APO`** — construir **nuestro** mapa (featurize → tICA/cluster → MSM ligero) sobre trajs apo Dutta depositadas **locales**, luego contactos VdW+0.5 y π **por nuestros estados**.  
**PI authorization:** YES — proposal confirmed (“Build **our own** map on local CB2_APO”).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Reanálisis **EXTERNAL** de trajs apo Dutta locales (`CB2_APO.zip`) | Reabrir P2 GPCRmd Morales-Pastor como `CONVERGENT` |
| Estados **nuestros** (`OWN_S0…`) con contactos / π | Alinear / fingir identidad con Dutta I1–I4 o pickles Final_MSM |
| Soft A/B/C a nivel de mapa de contactos (umbrales EXT) | Claims Gi / docking / de novo / hub hunt P1 |
| Escala piloto → scale-up documentado | Desempaquetar los **142 GB** de una vez |
| Etiquetas `EXT_OWN_MSM_*` | Sustituir P2 o promover a arquitectura ensemble CB2 |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C                = ABORTED                          # unchanged
EXT_MSM_STATE_CONTACTS          = INDETERMINATE_NO_ALIGNMENT       # Dutta labels; unchanged
EXT_OWN_MSM_*                   = NEW (this experiment; our states only)
DUTTA_I1_I4                     = NOT_OUR_STATES                   # no fake pickle alignment
DOCKING / Gi                    = STOP
```

**Explicit non-claims:**

1. Nuestros macroestados **≠** Dutta I1–I4 / Inactive / Active (etiquetas filename `*_inactive_*` / `*_active_*` son **muestreo estratificado**, no labels MSM).  
2. Este experimento **no** reabre P2 ni decide A/B/C estructural de ensemble.  
3. **No** Gi coupling; **no** docking.  
4. Piloto con N limitado puede quedar `EXT_OWN_MSM_PILOT_*` / `INSUFFICIENT_SAMPLING` sin scale-up automático.

---

## Questions (locked)

1. Con featurización X8-like fija y N piloto registrado, ¿el ITS / CK soft es `CONVERGENT`, `MARGINAL`, o `NON_CONVERGENT`?
2. Si Stage-0 pasa (≥ `MARGINAL`): ¿cuántos macroestados PCCA+ aislables y qué π / poblaciones de frames?
3. ¿Los mapas de contacto VdW+0.5 por **nuestros** estados caen en STABLE / STATE_DEPENDENT / DIFFUSE / INDETERMINATE (umbrales abajo)?
4. Si Stage-0 falla: ¿abortamos contactos limpiamente con `EXT_OWN_MSM_INSUFFICIENT_SAMPLING` o `EXT_OWN_MSM_NON_CONVERGENT` (sin inventar A/B/C)?

---

## Data (locked)

```
ZIP  = data/external/dutta_shukla_2023/trajectories/CB2_APO.zip
DIR  = data/external/dutta_shukla_2023/trajectories/CB2_APO/
TOP  = CB2-APO_inactive_pr_1-strip.prmtop
CACHE= .../CB2_APO/_cache_own_msm/     # stratified extract + feature cache ONLY
```

| Item | Rule |
|------|------|
| Zip | **Do not** unpack entire archive |
| Extract | Stream/member extract stratified inactive/active basenames into `CACHE` |
| Topology | Shared Amber strip; expect **4566** atoms |
| Frame chunks | Published `pr_*_frame_*` NetCDFs (~600 frames each, typical) |
| Dutta pickles | **Not** used for assignment or alignment |

DOI deposit: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

---

## Sampling plan (locked a priori)

### Pilot (primary run)

| Parameter | Value |
|-----------|--------|
| `N_PER_STATE` | **50** inactive + **50** active = **100** trajs |
| Stratification | Evenly spaced indices over sorted zip member lists per filename class (`_inactive_` / `_active_`); seed `20260912` for any fill-in |
| Expected frames | ~100 × 600 ≈ **60 000** (order-of-magnitude; document actual) |
| Max disk (cache) | **≤ 8 GB** under `_cache_own_msm/` (features + extracted nc) |
| Max walltime (pilot) | **≤ 4 h** wall-clock on local CPU |
| Parallel | CPU workers for featurization / contact accumulation where helpful |

Filename `inactive`/`active` = **starting-structure class in the deposit**, **not** our MSM states.

### Scale-up (only if pilot ITS is usable and PI asks)

| Gate | Action |
|------|--------|
| Pilot `CONVERGENT` or clearly `MARGINAL` with finite ITS ≥3 lags | Optional scale to **N=200** (100+100) under same featurization / hyperparameters |
| Pilot `NON_CONVERGENT` / pathological | **Stop**; verdict `EXT_OWN_MSM_INSUFFICIENT_SAMPLING` or `NON_CONVERGENT`; document path to larger N as **human decision**, not auto-run |

Do **not** retune featurization after seeing ITS.

---

## Featurization (FIXED a priori — X8 set)

Reuse the **24 Cα–Cα distances** from `EXPERIMENT_X8_REDUCED_FEATURIZATION.md` (UniProt P34972 indices). At runtime, map UniProt → topology `resid` via sequence alignment (same rule as APO pilot contacts; typical ~−20 offset). **Pairs are fixed before results**; no post-hoc pair add/drop.

| # | UniProt pair | Role (short) |
|---|--------------|--------------|
| 1–24 | Same table as X8 | Activation-relevant TM / toggle / NPxxY / hub corridor |

```text
n_features = 24
distance_unit = Å
selection = protein Cα at mapped topo resids
```

If any registered UniProt residue fails AA check after alignment → `EXT_OWN_MSM_INDETERMINATE` (featurization blocked).

---

## Clustering / MSM (locked; deeptime in `janus_p1`)

```text
TICA_LAG_FRAMES     = 5
TICA_DIM            = 5
N_MICROSTATES       = 50          # modest ↑ vs P2/X8 (25) given ~60k frames; FIXED a priori
KMEANS_MAX_ITER     = 500
KMEANS_SEED         = 20260912
ITS_LAGS_FRAMES     = (1, 2, 5, 10, 15, 20, 25, 30, 40, 50)
N_ITS               = 8
FRAME_DT_NS         = 0.1         # document as assumed; Dutta chunks often denser than GPCRmd 1 ns/frame — report MDA dt
ITS_FLAT_REL_TOL    = 0.25
ITS_MARGINAL_REL_TOL= 0.50
```

Pipeline: distances → **deeptime** TICA → K-means → ITS grid → same `assess_its_convergence` philosophy as `p2_msm_builder.py` → MSM at recommended lag → PCCA+ (spectral gap, max 8 macros).

**Soft CK gate (secondary):** at recommended lag τ, compare \(T(2\tau)\) vs \(T(\tau)^2\) (largest connected set, padded/aligned by state symbols). Soft pass if relative Frobenius error \(\le 0.35\) when both models fit; else `CK_SOFT_FAIL` (annotates; does **not** alone invent biology). If models cannot be compared → `CK_SOFT_NA`.

**Do not invent PyEMMA** if absent — deeptime only.

---

## Soft gates → Stage-0 outcome

| ITS verdict | Soft CK | Stage-0 label | Contacts? |
|-------------|---------|---------------|-----------|
| `CONVERGENT` | pass or NA | `EXT_OWN_MSM_INTERPRETABLE` | Yes |
| `MARGINAL` | pass | `EXT_OWN_MSM_MARGINAL` | Yes (provisional) |
| `MARGINAL` | fail | `EXT_OWN_MSM_MARGINAL_CK_WEAK` | Yes but tag provisional |
| `NON_CONVERGENT` | any | `EXT_OWN_MSM_NON_CONVERGENT` | **Abort** contacts |
| Pathological / <3 finite ITS | any | `EXT_OWN_MSM_INSUFFICIENT_SAMPLING` | **Abort** |
| Smoke / zip / map fail | — | `EXT_OWN_MSM_INDETERMINATE` | **Abort** |

Primary PI-facing lean when aborting Stage-0: **`EXT_OWN_MSM_INSUFFICIENT_SAMPLING`** if sampling/pathology; else keep `NON_CONVERGENT`.

---

## Per-state contacts + π (only if Stage-0 allows)

Contact definition = P1 / APO pilot (locked):

```text
geometry: |AB| < RvdW(A)+RvdW(B)+0.5 Å  (non-H)
exclude_sequential_protein: True
selection: protein
p_ij_edge_threshold: 0.1
```

- Accumulate over frames assigned to each **our** macrostate `OWN_Sk`.
- Cap: ≤ **200** frames / macro (uniform subsample, seed `20260912`) for walltime.
- Report π from PCCA coarse stationary probability + empirical frame fractions.
- Soft contact-map class across macros (pairwise mean Jaccard / mean frac private):

| Label | Rule (same spirit as EXT APO pilot) |
|-------|-------------------------------------|
| `EXT_OWN_MSM_CONTACTS_STABLE` | mean pairwise Jaccard ≥ 0.80 **and** mean frac_private < 0.15 |
| `EXT_OWN_MSM_CONTACTS_STATE_DEPENDENT` | not STABLE; mean frac_private ≥ 0.15 |
| `EXT_OWN_MSM_CONTACTS_DIFFUSE` | not STABLE; mean frac_private < 0.15 **and** mean Jaccard < 0.55 |
| `EXT_OWN_MSM_CONTACTS_INDETERMINATE` | else / <2 macros with edges |

Never label macros I1–I4.

---

## Failure modes (abort cleanly)

| Code | Trigger |
|------|---------|
| `EXT_OWN_MSM_INDETERMINATE` | Missing zip/topo, atom mismatch, hub/pair map fail, software missing |
| `EXT_OWN_MSM_INSUFFICIENT_SAMPLING` | Pathological ITS / too few usable lags / empty connected sets |
| `EXT_OWN_MSM_NON_CONVERGENT` | ITS `NON_CONVERGENT` without being purely “insufficient points” |
| `EXT_OWN_MSM_CACHE_LIMIT` | Would exceed disk/walltime budget mid-extract → stop with partial inventory |

On abort: write JSON/MD with verdict + diagnostics; **no** fabricated contact architecture.

---

## Forbidden interpretations

- Do **not** claim our states are Dutta’s.  
- Do **not** reopen P2 GPCRmd as CONVERGENT.  
- Do **not** claim Gi mechanism or dock ligands.  
- Do **not** unpack full zip.  
- Do **not** retune X8 pairs or N_MICROSTATES after seeing results.

---

## Outputs

| Path | Content |
|------|---------|
| `docs/synthesis/EXPERIMENT_CB2_APO_OWN_MSM.md` | This pre-registration |
| `scripts/network_core/cb2_apo_own_msm.py` | Runner |
| `results/msm_model/cb2_apo_own_msm_report.{md,json}` | MSM / ITS / π / verdicts |
| `results/msm_model/cb2_apo_own_msm_its.png` | ITS plot |
| `results/network_core/cb2_apo_own_msm_contacts.{md,json}` | Contacts section (if Stage-0 allows; else stub abort) |

Do **not** commit `.zip` / `.nc` / `.prmtop` / large feature caches under `_cache_own_msm/`.

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_apo_own_msm.py
# optional:
#   --n-per-state 50
#   --max-workers 4
#   --skip-extract   # reuse existing cache members
```

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales / pares / N_MICROSTATES después de ver resultados.*

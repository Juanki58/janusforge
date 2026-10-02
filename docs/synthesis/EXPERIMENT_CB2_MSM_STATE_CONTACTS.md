# Experiment — EXTERNAL: CB2 MSM metastable-state contact probabilities

**Fecha pre-registro:** 2026-09-12  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el análisis de contactos.  
**Scope:** **`EXTERNAL_MSM_STATE_CONTACTS`** — frecuencias de contacto VdW+0.5 Å **por macroestado MSM** (inactive, I1–I4, active) usando trayectorias CB2_APO + pickles Final_MSM.  
**PI authorization:** YES (“adelante”).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Contact / contact-probability maps **por metaestable Dutta** (si hay alineación traj↔MSM) | Reabrir P2 GPCRmd como `CONVERGENT` |
| Soft compare vs `EXT_PDB_CONTACTS_STATE_DEPENDENT` / SNAPSHOT_B y vs pilot filename | Afirmar arquitectura A/B/C de ensemble / mecanismo Gi |
| Mapear seis hubs LigACN (descriptivo; offset UniProt→topo ~−20) | Resucitar P1 hub hunt; retunar lista de hubs |
| Etiquetas `EXT_MSM_STATE_CONTACTS_*` | Docking, de novo; tratar filename `inactive`/`active` como macroestado MSM |

```text
P2_MSM_TRANSITIONS     = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C       = ABORTED                          # unchanged
EXT_STRUCTURAL_ABC     = SNAPSHOT_ONLY (prior PDB; soft compare only)
EXT_APO_PILOT_*        = PRIOR (filename pilots; NOT MSM states)
EXT_MSM_STATE_CONTACTS_* = NEW
```

**Explicit upgrade:** filename `*_inactive_*` / `*_active_*` en el zip = etiqueta de **arranque de simulación**, **≠** asignación MSM. Este experimento sustituye ese proxy **solo si** existe clave de alineación traj↔lista MSM.

---

## Questions (locked)

1. ¿Los pickles Final_MSM + zip permiten mapear cada `.nc` (o cada frame) a un macroestado {inactive, I1, I2, I3, I4, active}?
2. Si sí: ¿las frecuencias de contacto / edge sets a umbral difieren entre macroestados (STABLE / STATE_DEPENDENT / INDETERMINATE)?
3. ¿Jaccard pairwise entre macroestados y grados de los seis hubs LigACN (descriptivo)?
4. Soft compare: ¿compatible con prior PDB SNAPSHOT_B / `STATE_DEPENDENT` y distinto del pilot filename?
5. Bonus: ¿cuáles son las ocupaciones estacionarias / empíricas π̂ de los 6 macroestados?

---

## Data (locked)

```
ZIP  = data/external/dutta_shukla_2023/trajectories/CB2_APO.zip   # ~142 GB; extract on demand ONLY
TOP  = data/external/dutta_shukla_2023/trajectories/CB2_APO/CB2-APO_inactive_pr_1-strip.prmtop
MSM  = data/external/dutta_shukla_2023/msm/
       CB2_state_prob.pkl
       CB2_msm_feature_final_clustering.pkl
CACHE= data/external/dutta_shukla_2023/trajectories/CB2_APO/_cache_msm_states/
```

DOI: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).  
Code labels: [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) `Main_Figure_6/CB2-APO_vampnet_states_TPT.py`.

**Do not** unpack the full zip. Prefer streaming from zip or extract selected members into `CACHE`, then optional cleanup of `.nc` after processing. Gitignore covers `*.zip` / `*.nc` / `*.prmtop`.

---

## 1. MSM micro / macro → biological labels (a priori)

### Objects

| File | Role |
|------|------|
| `CB2_state_prob.pkl` | `list` len ~4972; each `ndarray (T, 6) float32` soft membership over **6 metastable** states |
| `CB2_msm_feature_final_clustering.pkl` | `list` len ~4972; each `ndarray (T,) int32` **microstate** indices (alignment / integrity only) |

**Hard macrostate per frame:** `k = argmax(state_prob[t])` ∈ {0…5}.

### Column → Dutta label (LOCKED from authors’ code)

From `CB2-APO_vampnet_states_TPT.py`:

```python
labels = ['I1', 'I2', 'I3', 'Inactive', 'I4', 'Active']
```

Confirmed by `CB2_APO_vampnet_binding_pocket.py` / feature bar script:

```python
states = ['3', '0', '1', '2', '4', '5']   # pickle column indices
labels = ['Inactive', 'I1', 'I2', 'I3', 'I4', 'Active']
```

| argmax index | Macro label (this experiment) | Path-order key |
|-------------:|-------------------------------|----------------|
| 0 | I1 | I1 |
| 1 | I2 | I2 |
| 2 | I3 | I3 |
| 3 | Inactive | inactive |
| 4 | I4 | I4 |
| 5 | Active | active |

**Path order for reporting** (paper / Fig. 6 narrative, same as PDB experiment):

```text
inactive → I1 → I2 → I3 → I4 → active
```

**Uncertainty documented:** population π̂ from prior kinetic compare used numeric indices 0…5 without renaming; this experiment **renames** via the authors’ `labels` list above. If a future deposit contradicts that list, flag `LABEL_MAP_CONFLICT` and do not retune after seeing contact results.

**Microstates:** not used for contact stratification (too many; no biological names).

---

## 2. Contact definition (LOCKED — same as P1 / APO pilot)

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
exclude_sequential_protein: True
selection: "protein"
p_ij_edge_threshold: 0.1          # primary edge set (P1 / pilot)
p_ij_report_threshold_high: 0.5   # secondary edge set for “stable contacts”
VdW radii: H 1.20, C 1.70, N 1.55, O 1.52, S 1.80, P 1.80, F 1.47, CL 1.75, BR 1.85, I 1.98
```

No change vs P1/pilot — continuity for soft compare. Chemotype angles / water bridges not reimplemented.

**Per-macrostate rule:** accumulate binary contacts only on frames with hard label = that macrostate → \(p_{ij}^{(s)}\) = fraction of those frames; undirected edge if \(p_{ij}^{(s)} \ge \tau\).

**Optional π-weighted global** (annotation only; does not drive primary verdict):  
\(p_{ij}^{\pi} = \sum_s \hat\pi_s\, p_{ij}^{(s)}\) with \(\hat\pi\) = hard occupancy over all MSM frames.

---

## 3. Sampling plan (a priori)

### Gate 0 — traj ↔ MSM alignment (HARD STOP)

Before any contact computation, the runner **must** establish a bijection (or documented surjection) from MSM list index `i` → zip member `.nc` (and frame index alignment of length `T_i`).

**Accepted keys (any one sufficient):**

1. Explicit filename / path list of length `n_traj` co-deposited with Final_MSM, **or**
2. Deterministic reconstruction of the authors’ load order that **reproduces** known invariants (e.g. per-traj `T` sequence matches unzipped frame counts **in that exact order**), **or**
3. Other cryptographic / metadata key published by authors that uniquely identifies each list element.

**Not accepted (do not fake):**

- Assuming lex / natural / zip-member order equals MSM list order without validation.
- Using filename `inactive`/`active` as MSM macrostate.
- Matching only by dominant hard state of whole traj (conflates start-label with MSM).
- Dropping the off-by-one (4972 vs 4971) without identifying the missing/extra traj.

**If Gate 0 fails → stop immediately:**

```text
EXT_MSM_STATE_CONTACTS = INDETERMINATE_NO_ALIGNMENT
```

Report the missing mapping key; still emit π̂ table from pickles (bonus); **do not** invent frame–state contacts.

### If Gate 0 passes — stratified extract

| Parameter | Locked value |
|-----------|--------------|
| Pilot subsample (first registered run) | **N = 5 trajs per macrostate** (majority hard-label ≥ 0.9 of frames), seed `20260912` |
| Frames per traj | All frames whose hard label equals the target macrostate (cap **200 frames/traj** if needed for runtime) |
| Scale-up | If disk/time allow and pilot is not INDETERMINATE for sampling reasons, increase N (document N in results) |
| Cache | Extract selected `.nc` under `CACHE`; delete after processing when safe |
| Disk | Never unpack full zip |

---

## 4. Metrics (locked a priori)

Let \(E_s(\tau)\) = undirected edge set for macrostate \(s\) at threshold \(\tau \in \{0.1, 0.5\}\).

| Metric | Definition |
|--------|------------|
| `n_edges[s, τ]` | \|E_s(τ)\| |
| `jaccard[s,t, τ]` | \|E_s ∩ E_t\| / \|E_s ∪ E_t\| |
| `mean_jaccard(τ)` | mean over unordered pairs s\<t |
| `frac_private[s, τ]` | \|E_s \ ⋃_{t≠s} E_t\| / max(\|E_s\|, 1) — or pairwise private vs complement as in pilot when K=2 |
| `mean_frac_private(τ)` | mean over s of fraction of edges not in the intersection-of-all / not shared with median peer — **primary:** mean pairwise `frac_private` analog: for each unordered pair, mean of \|E_s\E_t\|/\|E_s\|; then average over pairs (same spirit as PDB/pilot) |
| `hub_degree[s, hub]` | degree of mapped LigACN hub in \(E_s(0.1)\) |
| `pi_hard[k]`, `pi_soft[k]` | hard occupancy / mean soft prob (bonus) |

**Hub map:** UniProt P34972 → topology resid via NW alignment; expect ~−20 offset; accept only if AA matches; else `HUB_MAP_FAIL`.

---

## 5. Verdict thresholds (aligned with prior experiments)

Primary thresholds use **τ = 0.1** (P1/pilot). Path-order states = six macro labels.

| Label | A priori rule |
|-------|----------------|
| `EXT_MSM_STATE_CONTACTS_STABLE` | `mean_jaccard ≥ 0.80` **and** `mean_frac_private < 0.15` |
| `EXT_MSM_STATE_CONTACTS_STATE_DEPENDENT` | Not STABLE; **and** `mean_frac_private ≥ 0.15` |
| `EXT_MSM_STATE_CONTACTS_DIFFUSE` | Not STABLE; **and** `mean_frac_private < 0.15` **and** `mean_jaccard < 0.55` |
| `EXT_MSM_STATE_CONTACTS_INDETERMINATE` | None of the above cleanly **or** insufficient frames/trajs after Gate 0 |
| `EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT` | Gate 0 failed |

**Soft compare (annotation only):**

| Label | Rule |
|-------|------|
| `EXT_MSM_SOFT_AGREE_PDB_B` | Primary = `STATE_DEPENDENT` (same class as PDB snapshot B) |
| `EXT_MSM_SOFT_DISAGREE_PDB_B` | Primary ∈ {STABLE, DIFFUSE} with clean class |
| `EXT_MSM_SOFT_COMPARE_NA` | NO_ALIGNMENT / smoke failure / INDETERMINATE without class |
| `EXT_MSM_UPGRADES_FILENAME_PILOT` | Always true when Gate 0 passes (MSM labels replace filename proxy) |
| `EXT_MSM_FILENAME_NEQ_MSM_STATE` | Always true (epistemic reminder) |

Never promote to P2 `CONVERGENT`.

---

## 6. Forbidden interpretations

- No Gi coupling / docking / de novo.  
- No P2 CONVERGENT reopen.  
- No treating filename inactive/active as MSM macrostates.  
- No fabricated traj index ↔ file mapping.  
- Pilot subsample N is provisional; document N.

---

## Outputs

| Path | Content |
|------|---------|
| `docs/synthesis/EXPERIMENT_CB2_MSM_STATE_CONTACTS.md` | This pre-registration |
| `scripts/network_core/cb2_msm_state_contacts.py` | Runner (Gate 0 → optional contacts) |
| `results/network_core/cb2_msm_state_contacts.md` | Human report + verdicts + π |
| `results/network_core/cb2_msm_state_contacts.json` | Machine payload |

Do **not** commit `.nc` / `.prmtop` / `.zip` / cache extracts.

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_msm_state_contacts.py
# optional if Gate 0 ever passes:
#   --n-per-state 5 --frame-cap 200 --cleanup-cache
```

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales después de ver resultados de contactos.*

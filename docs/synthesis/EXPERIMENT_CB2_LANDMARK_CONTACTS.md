# Experiment — EXTERNAL: CB2 geometric landmark contact maps

**Fecha pre-registro:** 2026-09-13  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script / ver contactos / veredictos.  
**Scope:** **`EXTERNAL_LANDMARK_GEOMETRIC`** — asignar cada frame de traj APO al **nearest** de los 6 PDBs representantes Dutta (o pesos soft), luego contact maps / contact probs **por landmark**.  
**PI authorization:** YES (“adelante” para landmark perspective).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Etiquetado **geométrico** por proximidad (RMSD Cα) a 6 refs PDB | MSM cinético; pickles Final_MSM; Dutta I1–I4 como estados MSM |
| Contactos VdW+0.5 agregados por landmark | Reabrir P2 GPCRmd como `CONVERGENT` |
| Soft compare vs prior `EXT_PDB_CONTACTS_STATE_DEPENDENT` | Afirmar identidad metastable MSM; mecanismo Gi |
| Etiquetas `EXT_LANDMARK_*` | Docking / de novo; resucitar P1 hub hunt |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C                = ABORTED                          # unchanged
EXT_PDB_CONTACTS_*              = STATE_DEPENDENT (snapshot prior) # unchanged; compare only
EXT_APO_PILOT_*                 = INDETERMINATE (prior)            # unchanged
EXT_OWN_MSM_*                   = NON_CONVERGENT (prior)           # unchanged
EXT_LANDMARK_*                  = NEW (this experiment)
DUTTA_I1_I4_PICKLES             = NOT_USED
Gi / docking                    = STOP
```

**Explicit non-claim (locked):**

> **Geometric proximity ≠ MSM metastable identity.**  
> Un frame cercano en RMSD a `CB2_ref_*_I2_b.pdb` **no** es el macroestado cinético “I2” del paper. Las etiquetas landmark son **nombres de refs estructurales**, no estados de Markov.

---

## Questions (locked)

1. ¿Los Cα del topo Amber strip y de los 6 PDBs landmark se pueden alinear 1:1 (secuencia + conteo) sin inventar mapping? Si no → `EXT_LANDMARK_BLOCKED_NUMBERING` y stop.
2. Tras asignación hard (argmin RMSD), ¿los mapas de contacto VdW+0.5 por landmark caen en STABLE / STATE_DEPENDENT / DIFFUSE / INDETERMINATE?
3. ¿Jaccard entre landmarks y turnover path inactive→…→active son compatibles (soft) con el prior snapshot `EXT_PDB_CONTACTS_STATE_DEPENDENT`?
4. (Opcional, sensibilidad) ¿Soft weights `softmax(−RMSD/τ)` cambian el veredicto primario? No retunar τ tras ver resultados.

---

## Data (locked)

```
PDB_DIR = data/external/dutta_shukla_2023/main_figure_6/
  CB2_ref_inactive_3_b.pdb      → landmark: inactive
  CB2_ref_inactive_I1_b.pdb     → I1
  CB2_ref_inactive_I2_b.pdb     → I2
  CB2_ref_inactive_I3_b.pdb     → I3
  CB2_ref_inactive_I4_b.pdb     → I4
  CB2_ref_inactive_active_b.pdb → active
ZIP     = data/external/dutta_shukla_2023/trajectories/CB2_APO.zip
DIR     = data/external/dutta_shukla_2023/trajectories/CB2_APO/
TOP     = CB2-APO_inactive_pr_1-strip.prmtop
CACHE   = .../CB2_APO/_cache_landmark_contacts/   # stratified .nc extract ONLY
```

| Item | Rule |
|------|------|
| Zip | **Do not** unpack entire archive (~142 GB) |
| Extract | Stream member extract stratified into `CACHE` |
| Topology | Shared Amber strip; expect **4566** atoms |
| Landmarks | 6 published Fig. 6 refs; SHA256 via `MANIFEST.json` if present |
| Dutta MSM pickles | **Not** opened |

DOI: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

**Path order (filenames / Fig. 6 — landmark names only):**

```text
inactive → I1 → I2 → I3 → I4 → active
```

---

## Gate 0 — numbering / alignment (MUST pass before mass run)

### Atom selection for RMSD (locked)

```text
selection: protein and name CA
fit:      Kabsch / MDAnalysis.analysis.rms.RMSD-equivalent
          (superpose traj frame Cα onto landmark Cα, then RMSD)
```

### Residue correspondence (locked a priori)

1. Extract protein sequences (exclude ACE/NME) from **topology** and from **each landmark PDB**.
2. Align each PDB sequence to topo sequence (Needleman–Wunsch; same as prior APO scripts).
3. Build the **intersection** of matched Cα residue pairs (identical AA in alignment; prefer shared construct resid when resid equal).
4. **Pass criteria (all required):**
   - Alignment identity topo↔each PDB ≥ **0.98**
   - Number of matched Cα pairs ≥ **250** (CB2 TM construct ~280 aa; allow small termini gaps)
   - Matched Cα count **identical** across all 6 landmarks (same index set used for all RMSDs)
   - Document median `(topo_resid − uniprot)` and `(pdb_resid − uniprot)`; prior expectation **≈ −20**
5. **Fail → stop immediately** with `EXT_LANDMARK_BLOCKED_NUMBERING` (or `BLOCKED_ALIGNMENT` / `BLOCKED_ATOMCOUNT`). Report what mapping would be needed. **Do not invent** resid offsets or pad atoms.

Contact-map residue labels use **topology-native** `RESNAME:resid` (ACE/NME excluded). Landmarks are only geometric refs for assignment — their PDB resid numbers are not used as edge labels.

---

## Assignment (locked a priori)

### Hard (primary verdicts)

```text
landmark(frame) = argmin_{k in 6} RMSD(frame_Cα_matched, landmark_k_Cα_matched)
```

### Soft (sensitivity only; does not drive primary verdict)

```text
w_k(frame) = softmax(−RMSD_k / τ)
τ = 2.0 Å   # fixed a priori; report; do not retune
```

Report soft-weighted contact probs as secondary; if soft primary-class differs from hard, annotate `EXT_LANDMARK_SOFT_SENSITIVITY` without changing hard verdict.

---

## Sampling (locked a priori)

| Parameter | Value |
|-----------|--------|
| `N_PER_STATE` | **50** inactive + **50** active = **100** trajs (filename class in deposit) |
| Stratification | Evenly spaced indices over sorted zip member lists (`_inactive_` / `_active_`); seed `20260913` for fill-in |
| Frame use | All frames in each extracted `.nc` (document actual n_frames) |
| Max disk | **≤ 8 GB** under `_cache_landmark_contacts/` |
| Max walltime | **≤ 6 h** wall-clock local **CPU** |
| Scale-up | Only if hard verdict is clean STABLE or STATE_DEPENDENT **and** PI asks; not auto |

Filename `inactive`/`active` = **deposit starting-structure class**, **not** landmark assignment and **not** MSM states.

Reuse existing `_cache_own_msm/` / other caches **only if** member basenames match the stratified set for this seed/N; otherwise extract into `_cache_landmark_contacts/`. Prefer on-demand extract; do not commit `.nc` / `.zip`.

---

## Contact definition (LOCKED — reuse P1 / PDB / pilot)

Primary (verdicts):

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
exclude_sequential_protein: True   # drop |resid_i − resid_j| == 1
selection: "protein"
p_ij_edge_threshold: 0.1           # edge if frame-fraction among frames hard-assigned to landmark ≥ 0.1
VdW radii: H 1.20, C 1.70, N 1.55, O 1.52, S 1.80, P 1.80, F 1.47, CL 1.75, BR 1.85, I 1.98
```

**Per-landmark rule:** accumulate binary contacts only on frames with `hard_assign == landmark`; \(p_{ij}^{(k)}\) = fraction within that landmark’s frames; edge if \(p_{ij}^{(k)} \ge 0.1\). Landmarks with **&lt; 100 frames** → mark `LOW_N` for that landmark; if **&lt; 3 landmarks** have ≥100 frames → primary `EXT_LANDMARK_INDETERMINATE` (insufficient occupancy).

**Secondary (sensitivity):** Cα–Cα &lt; 8.0 Å, `|Δresid| ≥ 2`, same \(p_{ij}\) thr; report mean Jaccard vs primary; do not retune.

---

## Metrics (locked a priori)

Let \(E_k\) = undirected edge set of landmark \(k\) after \(p_{ij}\) thr.  
Order \(s\) = inactive→I1→I2→I3→I4→active.

| Metric | Definition |
|--------|------------|
| `n_frames[k]`, `frac_frames[k]` | Hard-assign occupancy |
| `n_edges[k]` | \|E_k\| |
| `jaccard[k,t]` | \|E_k ∩ E_t\| / \|E_k ∪ E_t\| |
| `mean_jaccard` | mean over unordered pairs k&lt;t among landmarks with ≥100 frames |
| `min_jaccard`, `max_jaccard` | extremes |
| `frac_core` | \|⋂ E_k\| / \|⋃ E_k\| over occupied landmarks |
| `frac_state_specific` | mean_k \|{e ∈ E_k : e ∉ E_t ∀ t≠k}\| / max(\|E_k\|,1) |
| `path_turnover_frac` | mean along path (\|appear\|+\|disappear\|)/\|E_s ∪ E_{s+1}\| (skip missing LOW_N steps) |
| `mean_rmsd_to_assigned` | mean RMSD(frame, hard landmark) |
| `soft_entropy_mean` | mean_k Shannon entropy of soft weights (nats) |

**Substantial difference:** `mean_jaccard < 0.80` **or** `path_turnover_frac ≥ 0.20` → `DIFFERS_SUBSTANTIALLY`; else `SIMILAR_OVERALL`.

---

## Verdicts (thresholds locked)

| Label | A priori rule |
|-------|----------------|
| `EXT_LANDMARK_CONTACTS_STABLE` | `mean_jaccard ≥ 0.80` **and** `frac_core ≥ 0.60` |
| `EXT_LANDMARK_CONTACTS_STATE_DEPENDENT` | Not STABLE; **and** (`frac_state_specific ≥ 0.15` **or** `path_turnover_frac ≥ 0.20`) |
| `EXT_LANDMARK_CONTACTS_DIFFUSE` | Not STABLE; **and** `frac_state_specific < 0.15` **and** `mean_jaccard < 0.55` |
| `EXT_LANDMARK_CONTACTS_INDETERMINATE` | None of the above cleanly; or insufficient occupancy |
| `EXT_LANDMARK_BLOCKED_NUMBERING` | Gate 0 fail (numbering / alignment / atom match) |
| `EXT_LANDMARK_BLOCKED_DATA` | Missing zip/prmtop/PDBs / extract failure |

**Soft compare to prior PDB snapshot (annotation only):**

| Label | Rule |
|-------|------|
| `EXT_LANDMARK_SOFT_AGREE_PDB_B` | Primary = `STATE_DEPENDENT` (same soft class as `EXT_PDB_CONTACTS_STATE_DEPENDENT`) |
| `EXT_LANDMARK_SOFT_DISAGREE_PDB_B` | Primary is STABLE / DIFFUSE / INDETERMINATE (not blocked) |
| `EXT_LANDMARK_SOFT_COMPARE_NA` | Blocked / no primary contacts |

Always emit: `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `TRUE`.

Never promote to P2 `CONVERGENT` / ensemble architecture / Gi.

---

## Forbidden interpretations

- Do **not** claim that landmark labels are Dutta MSM I1–I4.  
- Do **not** reopen P2 or own-MSM as CONVERGENT from this result.  
- Do **not** claim Gi coupling.  
- Do **not** dock or design ligands.  
- Do **not** fake residue mapping if Gate 0 fails.

---

## Outputs

| Path | Content |
|------|---------|
| `docs/synthesis/EXPERIMENT_CB2_LANDMARK_CONTACTS.md` | This pre-registration |
| `scripts/network_core/cb2_landmark_contacts.py` | Runner (CPU; zip on demand) |
| `results/network_core/cb2_landmark_contacts.md` | Human report + verdicts (ES/EN key fields) |
| `results/network_core/cb2_landmark_contacts.json` | Machine payload |

Do **not** commit `.nc` / `.prmtop` / `.zip` / cache extracts.

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_landmark_contacts.py
# optional:
#   --n-per-state 50
#   --skip-extract   # reuse CACHE if manifest matches
#   --tau 2.0
```

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales después de ver resultados.*

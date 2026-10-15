# Experiment — EXTERNAL: CB2 expanded geometric landmark contact maps

**Fecha pre-registro:** 2026-09-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script / ver contactos / veredictos.  
**Scope:** **`EXTERNAL_LANDMARK_EXPANDED`** — mismos contactos VdW+0.5 y asignación hard por RMSD Cα que `EXT_LANDMARK_*`, pero con panel de landmarks **más allá de los 6 PDBs Dutta Fig. 6** (cryo-EM / cristal CB2 + Dutta-6).  
**PI authorization:** YES (“adelante” a la top recommendation de [`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md) §4.1).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Etiquetado **geométrico** por proximidad (RMSD Cα) a landmarks estructurales públicos | MSM cinético; pickles Final_MSM; Dutta I1–I4 como estados MSM |
| Contactos VdW+0.5 agregados por landmark | Reabrir P2 GPCRmd como `CONVERGENT` |
| Soft compare vs prior Dutta-6 `EXT_LANDMARK_CONTACTS_STABLE` (Jaccard≈0.82) y vs PDB snapshot B | Afirmar identidad metastable MSM; mecanismo Gi |
| Etiquetas `EXT_LANDMARK_EXPANDED_*` | Docking / de novo; resucitar P1 hub hunt |
| Drop per-PDB si Gate0 falla (con razón) y continuar | Inventar offsets resid / pad atoms |

```text
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C                = ABORTED                          # unchanged
EXT_LANDMARK_CONTACTS_*         = STABLE (prior Dutta-6; soft compare only)
EXT_PDB_CONTACTS_*              = STATE_DEPENDENT (snapshot prior) # soft compare only
EXT_LANDMARK_EXPANDED_*         = NEW (this experiment)
DUTTA_I1_I4_PICKLES             = NOT_USED
Gi / docking                    = STOP
```

**Explicit non-claim (locked):**

> **Geometric proximity ≠ MSM metastable identity.**  
> Un frame cercano en RMSD a un PDB cryo/cristal **no** es un macroestado cinético. Las etiquetas landmark son **nombres de refs estructurales** (acceso PDB o Fig. 6), no estados de Markov.  
> Este experimento **no** reabre P2 y **no** afirma acoplamiento Gi.

**Pregunta discriminante (locked):**

> ¿La estabilidad de mapa de contactos (`STABLE` bajo Dutta-6 geométrico) es propiedad del **camino inactive→active de Fig. 6**, o se mantiene / rompe al cruzar **diversidad de ligando / PAM / construct** del panel público?

---

## Questions (locked)

1. ¿Cada PDB candidato alinea Cα vs topo Amber strip (vía UniProt P34972) con identity ≥ 0.98 y ≥ 250 Cα emparejados? Si un PDB falla → **drop con razón** y continuar; si el set que pasa Gate0 tiene &lt; 3 landmarks → `EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING`.
2. Tras asignación hard (argmin RMSD) sobre el set Gate0-pass, ¿los mapas VdW+0.5 caen en STABLE / STATE_DEPENDENT / DIFFUSE / INDETERMINATE?
3. Soft: ¿`mean_jaccard` del panel expandido es compatible con el prior Dutta-6 (~0.82 STABLE)? ¿Coincide en clase soft con PDB snapshot B (`STATE_DEPENDENT`)?
4. (Sensibilidad) Soft weights `softmax(−RMSD/τ)`, τ=2.0 Å fijo; no retunar tras ver resultados.

---

## Data (locked)

### A) Dutta Fig. 6 (baseline, mismos 6 archivos)

```
PDB_DIR_DUTTA = data/external/dutta_shukla_2023/main_figure_6/
  CB2_ref_inactive_3_b.pdb      → landmark: dutta_inactive
  CB2_ref_inactive_I1_b.pdb     → dutta_I1
  CB2_ref_inactive_I2_b.pdb     → dutta_I2
  CB2_ref_inactive_I3_b.pdb     → dutta_I3
  CB2_ref_inactive_I4_b.pdb     → dutta_I4
  CB2_ref_inactive_active_b.pdb → dutta_active
```

### B) Panel público expandido (candidatos; drop si Gate0 falla)

| Accession | Estado / ligando (lit.) | Fuente |
|-----------|-------------------------|--------|
| **5ZTY** | Inactivo / antagonista AM10257 | RCSB/PDBe |
| **6KPC** | Activo (cristal) E3R | RCSB/PDBe |
| **6KPF** | Activo + Gi AM12033-class | RCSB/PDBe |
| **6PT0** | Activo + Gi WIN 55,212-2 | RCSB/PDBe |
| **8GUR** | Activo + Gi CP55,940 | RCSB/PDBe |
| **8GUS** | Activo + Gi HU-308 | RCSB/PDBe |
| **8GUQ** | Activo + Gi Olorinab (βarr-biased) | RCSB/PDBe |
| **8GUT** | Activo + Gi LEI-102 | RCSB/PDBe |
| **8X3L** | Activo + G (entropy-driven) | RCSB/PDBe |
| **9U7L** | Activo + PAM Ec21a + CP55,940 | RCSB/PDBe (si disponible) |

```
PDB_DIR_EXPANDED = data/external/cb2_landmark_expanded/
  MANIFEST.json   # accession, path, sha256, state/ligand, download URL, gate0 status (post-run)
ZIP     = data/external/dutta_shukla_2023/trajectories/CB2_APO.zip
DIR     = data/external/dutta_shukla_2023/trajectories/CB2_APO/
TOP     = CB2-APO_inactive_pr_1-strip.prmtop
CACHE   = .../CB2_APO/_cache_landmark_expanded/   # stratified .nc extract ONLY
```

| Item | Rule |
|------|------|
| Zip | **Do not** unpack entire archive (~142 GB) |
| Extract | Stream member extract stratified into `CACHE` (reuse `_cache_landmark_contacts` / `_cache_own_msm` if basenames match) |
| Topology | Shared Amber strip; expect **4566** atoms |
| RCSB PDBs | Download biological assembly / asymmetric unit as available; select **CB2 chain only** for Cα; ligands/Gi/waters ignored for RMSD |
| Atom count | Dutta refs may match strip atom count; **RCSB PDBs must NOT** be required to match 4566 atoms |
| Dutta MSM pickles | **Not** opened |

DOI anclas: Dutta [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1); atlas [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md).

---

## Gate 0 — numbering / alignment (MUST pass per landmark; drop failures)

### Atom selection for RMSD (locked)

```text
selection: protein and name CA  (CB2 chain only for multi-chain RCSB)
fit:      Kabsch (superpose traj frame Cα onto landmark Cα, then RMSD)
index:    shared UniProt P34972 positions with CA in BOTH topo and landmark
```

### Residue correspondence (locked a priori)

1. Extract protein sequence (exclude ACE/NME; for RCSB exclude non-standard polymer residues without AA map) from **topology** and from **each landmark** (best-matching CB2 chain by NW identity to UniProt).
2. Align each sequence to UniProt P34972 (Needleman–Wunsch).
3. Build matched Cα pairs via **shared UniProt positions** (identical AA in both alignments).
4. **Pass criteria (per landmark):**
   - Alignment identity of landmark seq vs UniProt (aligned columns) ≥ **0.90** *or* vs topo overlapping construct ≥ **0.98** (Dutta refs expected under the latter)
   - Number of matched Cα pairs (topo↔this landmark via UniProt) ≥ **250**
   - Document median `(topo_resid − uniprot)` and `(pdb_resid − uniprot)`
5. **Common index set** = intersection of UniProt positions across **all Gate0-passing** landmarks. Require `|common| ≥ 250`. If not → drop the landmark(s) with smallest private match set until common ≥ 250 or &lt; 3 landmarks remain.
6. **Fail a landmark → drop with reason** (`alignment_identity`, `insufficient_matched_ca`, `no_cb2_chain`, `download_missing`, …). **Do not invent** resid offsets.
7. If **&lt; 3** landmarks pass → stop with `EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING`.

Contact-map residue labels use **topology-native** `RESNAME:resid`. Landmarks are geometric refs only.

---

## Assignment (locked a priori)

### Hard (primary verdicts)

```text
landmark(frame) = argmin_{k in Gate0_pass} RMSD(frame_Cα_common, landmark_k_Cα_common)
```

### Soft (sensitivity only; does not drive primary verdict)

```text
w_k(frame) = softmax(−RMSD_k / τ)
τ = 2.0 Å   # fixed a priori; report; do not retune
```

---

## Sampling (locked a priori)

| Parameter | Value |
|-----------|--------|
| `N_PER_STATE` | **50** inactive + **50** active = **100** trajs (same style as Dutta-6 landmark run) |
| Stratification | Evenly spaced indices over sorted zip member lists (`_inactive_` / `_active_`); seed `20260913` |
| Frame use | All frames in each extracted `.nc` |
| Max disk | **≤ 8 GB** under `_cache_landmark_expanded/` |
| Max walltime | **≤ 6 h** wall-clock local **CPU** |

Filename `inactive`/`active` = **deposit starting-structure class**, **not** landmark assignment and **not** MSM states.

Prefer reuse of existing cache NC files when basenames match; do not commit `.nc` / `.zip`.

---

## Contact definition (LOCKED — identical to prior landmark / P1)

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
exclude_sequential_protein: True
selection: "protein"
p_ij_edge_threshold: 0.1
```

**Per-landmark rule:** accumulate on frames with `hard_assign == landmark`; edge if \(p_{ij}^{(k)} \ge 0.1\). Landmarks with **&lt; 100 frames** → `LOW_N`; if **&lt; 3** landmarks have ≥100 frames → primary `EXT_LANDMARK_EXPANDED_INDETERMINATE`.

**Secondary:** Cα–Cα &lt; 8.0 Å, `|Δresid| ≥ 2`; report mean Jaccard vs primary; do not retune.

---

## Metrics (locked a priori)

Let \(E_k\) = undirected edge set of landmark \(k\) after \(p_{ij}\) thr.  
Occupied = Gate0-pass landmarks with ≥100 frames.

| Metric | Definition |
|--------|------------|
| `n_frames[k]`, `frac_frames[k]` | Hard-assign occupancy |
| `n_edges[k]` | \|E_k\| |
| `jaccard[k,t]` | \|E_k ∩ E_t\| / \|E_k ∪ E_t\| |
| `mean_jaccard` | mean over unordered pairs k&lt;t among occupied |
| `min_jaccard`, `max_jaccard` | extremes |
| `frac_core` | \|⋂ E_k\| / \|⋃ E_k\| over occupied |
| `frac_state_specific` | mean_k \|{e ∈ E_k : e ∉ E_t ∀ t≠k}\| / max(\|E_k\|,1) |
| `path_turnover_frac` | **Only** if all 6 Dutta landmarks are Gate0-pass **and** occupied: mean along `dutta_inactive→…→dutta_active` (same formula as prior). Else `null` / skip path rule for primary. |
| `mean_rmsd_to_assigned` | mean RMSD(frame, hard landmark) |
| `soft_entropy_mean` | mean Shannon entropy of soft weights (nats) |
| `delta_mean_j_vs_dutta6_prior` | `mean_jaccard − 0.8214` (prior published run; soft annotate) |

**Substantial difference (maps):** `mean_jaccard < 0.80` **or** (if path defined) `path_turnover_frac ≥ 0.20` → `DIFFERS_SUBSTANTIALLY`; else `SIMILAR_OVERALL`.

---

## Verdicts (thresholds locked)

| Label | A priori rule |
|-------|----------------|
| `EXT_LANDMARK_EXPANDED_STABLE` | `mean_jaccard ≥ 0.80` **and** `frac_core ≥ 0.60` |
| `EXT_LANDMARK_EXPANDED_STATE_DEPENDENT` | Not STABLE; **and** (`frac_state_specific ≥ 0.15` **or** (path defined and `path_turnover_frac ≥ 0.20`)) |
| `EXT_LANDMARK_EXPANDED_DIFFUSE` | Not STABLE; **and** `frac_state_specific < 0.15` **and** `mean_jaccard < 0.55` |
| `EXT_LANDMARK_EXPANDED_INDETERMINATE` | None of the above cleanly; or insufficient occupancy |
| `EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING` | &lt; 3 landmarks pass Gate 0 |
| `EXT_LANDMARK_EXPANDED_BLOCKED_DATA` | Missing zip/prmtop / extract failure |

**Soft compare to prior Dutta-6 STABLE (annotation only):**

| Label | Rule |
|-------|------|
| `EXT_LANDMARK_EXPANDED_SOFT_AGREE_DUTTA6_STABLE` | Primary = `EXT_LANDMARK_EXPANDED_STABLE` |
| `EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_DUTTA6_STABLE` | Primary is a non-blocked contacts class other than STABLE |
| `EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6_NA` | Blocked / no primary |

**Soft compare to prior PDB snapshot B (annotation only):**

| Label | Rule |
|-------|------|
| `EXT_LANDMARK_EXPANDED_SOFT_AGREE_PDB_B` | Primary = `…_STATE_DEPENDENT` |
| `EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_PDB_B` | Primary is STABLE / DIFFUSE / INDETERMINATE (not blocked) |
| `EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB_NA` | Blocked / no primary |

Always emit: `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `TRUE`.

Never promote to P2 `CONVERGENT` / ensemble architecture / Gi.

---

## Forbidden interpretations

- Do **not** claim landmark labels are Dutta MSM I1–I4 or cryo “activation states” as kinetic.  
- Do **not** reopen P2.  
- Do **not** claim Gi coupling from contact stability.  
- Do **not** dock or design ligands.  
- Do **not** fake residue mapping if Gate 0 fails for a PDB — drop and document.

---

## Outputs

| Path | Content |
|------|---------|
| `docs/synthesis/EXPERIMENT_CB2_LANDMARK_EXPANDED.md` | This pre-registration |
| `scripts/network_core/cb2_landmark_expanded.py` | Runner (CPU; zip on demand; Gate0 drop) |
| `data/external/cb2_landmark_expanded/MANIFEST.json` | Accessions, SHAs, state/ligand, Gate0 drop reasons |
| `results/network_core/cb2_landmark_expanded.md` | Human report + verdicts |
| `results/network_core/cb2_landmark_expanded.json` | Machine payload |

Do **not** commit `.nc` / `.prmtop` / `.zip` / cache extracts. **Do** commit downloaded landmark PDBs/CIF under `data/external/cb2_landmark_expanded/` if size reasonable (or document download URLs + SHA if too large — prefer committing structures).

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_landmark_expanded.py
# optional:
#   --n-per-state 50
#   --skip-extract
#   --tau 2.0
#   --download-only   # fetch PDBs + MANIFEST, no traj analysis
```

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales después de ver resultados.*

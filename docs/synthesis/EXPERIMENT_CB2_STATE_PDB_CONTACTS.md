# Experiment — EXTERNAL: Dutta CB2 state-representative PDB contact maps

**Fecha pre-registro:** 2026-09-11  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script.  
**Scope:** **`EXTERNAL_STRUCTURAL_SNAPSHOT`** — comparación de contactos entre los 6 PDBs representantes de estado publicados por Dutta & Shukla 2023.  
**PI authorization:** YES (“adelante”).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Soft probe A/B/C **solo a nivel de contact-map** entre 6 snapshots estáticos | Reabrir P2 GPCRmd como `CONVERGENT` |
| Describir aparición/desaparición de contactos a lo largo del orden inactive→…→active | Ensemble / persistencia dinámica / redes de comunicación por estado |
| Describir participación de los 6 hubs LigACN estáticos (descriptivo) | Resucitar P1 como caza de hubs; retunar la lista de hubs |
| Etiquetas `EXT_*` de snapshots externos | Docking, de novo, mecanismo Gi, afirmar arquitectura A/B/C definitiva |

**Un PDB por estado ≠ ensemble.** Cualquier solapamiento alto/bajo es evidencia de snapshots publicados, no de estabilidad cinética ni de redes P2.

```text
P2_MSM_TRANSITIONS     = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C       = ABORTED                          # unchanged
EXT_STRUCTURAL_ABC     = SNAPSHOT_ONLY (nuanced; see verdicts)
```

---

## Questions (locked)

1. ¿Los mapas de contacto heavy-atom difieren de forma sustancial entre los 6 estados?
2. ¿Solapamiento de aristas entre estados? (>80% → A-like estable; bajo / state-specific → B-like; difuso → C-like) — umbrales abajo.
3. ¿Qué contactos aparecen/desaparecen a lo largo de inactive→I1→I2→I3→I4→active (orden por filenames / Fig. 6)?
4. ¿Los seis hubs LigACN estáticos participan de forma distinta entre PDBs? (**descriptivo only**).

---

## Data (locked)

```
DIR = data/external/dutta_shukla_2023/main_figure_6/
CB2_ref_inactive_3_b.pdb      → state key: inactive
CB2_ref_inactive_I1_b.pdb     → I1
CB2_ref_inactive_I2_b.pdb     → I2
CB2_ref_inactive_I3_b.pdb     → I3
CB2_ref_inactive_I4_b.pdb     → I4
CB2_ref_inactive_active_b.pdb → active
MANIFEST.json                 # SHA256 verify before analysis
```

**Path order (paper / filenames — NOT the MSM pickle label order `I1,I2,I3,Inactive,I4,Active` from `CB2-APO_vampnet_states_TPT.py`):**

```text
inactive → I1 → I2 → I3 → I4 → active
```

**Optional (not required for verdicts):** `data/external/dutta_shukla_2023/msm/CB2_state_prob.pkl` for soft populations as annotation only — **no weighting of contacts** in the primary analysis (single PDB ≠ ensemble; weighting would overclaim).

DOI: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

---

## Contact definition (LOCKED — reuse P1; do not invent after results)

Primary (verdicts):

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
exclude_sequential_protein: True   # drop |resid_i − resid_j| == 1
selection: "protein"               # apo refs; no 8D0 ligand in these PDBs
VdW radii: H 1.20, C 1.70, N 1.55, O 1.52, S 1.80, P 1.80, F 1.47, CL 1.75, BR 1.85, I 1.98
```

Same limitation as P1: chemotype angles / water bridges not reimplemented.

**Static snapshot rule:** a residue-pair edge exists if ≥1 heavy-atom pair satisfies the VdW envelope in that PDB (binary). No `p_ij` threshold (N_frames=1).

**Secondary (sensitivity only; does not drive verdict):** Cα–Cα contact if ‖CA_i − CA_j‖ < 8.0 Å, exclude `|Δresid| < 2`. Report mean Jaccard vs primary; do not retune.

**Residue labels:** `RESNAME:resid` using **PDB-native** residue numbers in each file (ACE/NME excluded from graphs).

---

## Hub mapping (locked a priori — descriptive Q4)

Fixed LigACN set (project numbering, identical to P1 / dual-validation):

| Hub | Project label | Expected AA |
|-----|---------------|-------------|
| ALA79 | `ALA:79` | ALA |
| ALA83 | `ALA:83` | ALA |
| LEU287 | `LEU:287` | LEU |
| ASN291 | `ASN:291` | ASN |
| ASN295 | `ASN:295` | ASN |
| ARG302 | `ARG:302` | ARG |

**Mapping into Dutta PDBs:** align protein sequence of each PDB (excluding ACE/NME) to UniProt **P34972**; take UniProt indices `{79,83,287,291,295,302}` → PDB `resid`. Accept hub node only if aligned PDB residue has the **expected AA**; otherwise mark `HUB_MAP_FAIL` for that hub (still list aligned AA/resid for transparency). No post-hoc hub substitution.

Metrics per mapped hub (descriptive): degree in the primary contact graph; set of neighbor labels; Jaccard of hub-incident edge sets across the 6 states.

---

## Metrics (locked a priori)

Let \(E_s\) = undirected edge set of state \(s\) (primary contacts).

| Metric | Definition |
|--------|------------|
| `n_edges[s]` | \|E_s\| |
| `jaccard[s,t]` | \|E_s ∩ E_t\| / \|E_s ∪ E_t\| (0 if both empty) |
| `mean_jaccard` | mean of `jaccard[s,t]` over all unordered pairs s\<t |
| `min_jaccard`, `max_jaccard` | extremes of pairwise matrix |
| `frac_core` | \|⋂_s E_s\| / \|⋃_s E_s\| |
| `n_state_specific[s]` | \|{e ∈ E_s : e ∉ E_t ∀ t≠s}\| |
| `frac_state_specific` | mean_s `n_state_specific[s] / max(\|E_s\|,1)` |
| `path_appear[k]` | edges in E_{s_{k+1}} \ E_{s_k} along path order |
| `path_disappear[k]` | edges in E_{s_k} \ E_{s_{k+1}} |
| `path_turnover_frac` | mean_k (\|appear\|+\|disappear\|) / \|E_{s_k} ∪ E_{s_{k+1}}\| |

**Substantial difference (Q1):** `mean_jaccard < 0.80` **or** `path_turnover_frac ≥ 0.20` → maps differ substantially (`DIFFERS_SUBSTANTIALLY`); else `SIMILAR_OVERALL`.

---

## Soft A/B/C at contact-map level (thresholds locked)

| Label | A priori rule |
|-------|----------------|
| `EXT_PDB_CONTACTS_STABLE` | `mean_jaccard ≥ 0.80` **and** `frac_core ≥ 0.60` (A-like shared contact core) |
| `EXT_PDB_CONTACTS_STATE_DEPENDENT` | Not STABLE; **and** (`frac_state_specific ≥ 0.15` **or** `path_turnover_frac ≥ 0.20`) (B-like state-specific / path turnover) |
| `EXT_PDB_CONTACTS_DIFFUSE` | Not STABLE; **and** `frac_state_specific < 0.15` **and** `mean_jaccard < 0.55` (C-like low overlap without strong state-private edges) |
| `EXT_PDB_CONTACTS_INDETERMINATE` | None of the above cleanly |

**Nuanced structural tag (always snapshot-scoped):**

| Label | Rule |
|-------|------|
| `EXT_STRUCTURAL_ABC_SNAPSHOT_A` | Primary verdict `STABLE` |
| `EXT_STRUCTURAL_ABC_SNAPSHOT_B` | Primary verdict `STATE_DEPENDENT` |
| `EXT_STRUCTURAL_ABC_SNAPSHOT_C` | Primary verdict `DIFFUSE` |
| `EXT_STRUCTURAL_ABC_SNAPSHOT_INDETERMINATE` | Primary `INDETERMINATE` |

Never promote these to P2 `CONVERGENT` / ensemble architecture.

---

## Forbidden interpretations

- Do **not** claim Gi coupling mechanism.  
- Do **not** reopen P1 hub hunt or change the six-hub list.  
- Do **not** treat one PDB per state as MSM ensemble evidence.  
- Do **not** claim P2 Gate-1 CONVERGENT.  
- Do **not** dock or design ligands from this result.

---

## Outputs

| Path | Content |
|------|---------|
| `scripts/network_core/cb2_state_pdb_contacts.py` | Runner |
| `results/network_core/cb2_state_pdb_contacts.md` | Human report + verdicts (ES/EN key fields) |
| `results/network_core/cb2_state_pdb_contacts.json` | Machine payload |
| `results/network_core/cb2_state_pdb_contacts_overlap.png` | Pairwise Jaccard heatmap (optional) |

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_state_pdb_contacts.py
```

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales después de ver resultados.*

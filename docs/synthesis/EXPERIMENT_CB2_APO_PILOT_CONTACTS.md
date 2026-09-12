# Experiment — EXTERNAL: CB2_APO trajectory pilot contact maps

**Fecha pre-registro:** 2026-09-12  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — este documento se escribe **antes** de ejecutar el script.  
**Scope:** **`EXTERNAL_APO_TRAJ_PILOT`** — contactos VdW+0.5 Å sobre **1 traj inactive + 1 traj active** (pilots locales) + topología Amber compartida.  
**PI authorization:** YES (“ok” → open pilots + prmtop + contact pilot).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Pilot EXTERNAL de mapas de contacto inactive vs active | Reabrir P2 GPCRmd como `CONVERGENT` |
| Soft compare descriptivo vs `EXT_PDB_CONTACTS_STATE_DEPENDENT` / snapshot B | Afirmar arquitectura A/B/C de ensemble / mecanismo Gi |
| Mapear seis hubs LigACN vía UniProt P34972 (descriptivo) | Resucitar P1 hub hunt; retunar lista de hubs |
| Etiquetas `EXT_APO_PILOT_*` | Docking, de novo, claims de persistencia de red completa CB2_APO |

**Single/few trajs ≠ full ensemble.** Los pilots son chunks publicados (`pr_*_frame_*`); **no** representan el MSM ni las ~4971 trayectorias del zip.

```text
P2_MSM_TRANSITIONS     = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_NETWORK_A_B_C       = ABORTED                          # unchanged
EXT_STRUCTURAL_ABC     = SNAPSHOT_ONLY (prior PDB; unchanged by this pilot)
EXT_APO_PILOT_*        = NEW (pilot-scoped only)
```

---

## Questions (locked)

1. ¿Abren prmtop + cada `.nc` con 4566 átomos y n_frames usable?
2. ¿Los mapas de contacto (persistencia P1) difieren entre inactive vs active pilot?
3. ¿Jaccard inactive∩active / inactive∪active cae en régimen STABLE / STATE_DEPENDENT / DIFFUSE / INDETERMINATE (umbrales abajo)?
4. ¿Los seis hubs LigACN resuelven en la topología (map UniProt) y qué grados tienen (descriptivo)?
5. Soft compare: ¿el veredicto pilot es compatible con el prior `EXT_PDB_CONTACTS_STATE_DEPENDENT` / `EXT_STRUCTURAL_ABC_SNAPSHOT_B`?

---

## Data (locked)

```
DIR  = data/external/dutta_shukla_2023/trajectories/CB2_APO/
TOP  = CB2-APO_inactive_pr_1-strip.prmtop
INACT= CB2-APO_inactive_pr_9_frame_99-strip.nc
ACT  = CB2-APO_active_pr_10_frame_28-strip.nc
ZIP  = data/external/dutta_shukla_2023/trajectories/CB2_APO.zip   # ~142 GB; do NOT unpack all
```

| Role | File | Expect (smoke) |
|------|------|----------------|
| Topology | `…prmtop` | Amber strip; shared for both nc |
| Inactive pilot | `…inactive_pr_9_frame_99-strip.nc` | 4566 atoms; n_frames documented at run |
| Active pilot | `…active_pr_10_frame_28-strip.nc` | same atom count |

DOI: [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1).

**Optional robustness (only if primary pilot is ambiguous or PI wants thicker N):** extract a **small stratified sample** (5 inactive + 5 active `.nc`) from the local zip **without** unpacking the archive; re-run aggregate persistence. Not required to close the pilot.

---

## Contact definition (LOCKED — reuse P1 / PDB experiment)

Primary (verdicts):

```text
name: getcontacts_vdw_envelope_plus_alloviz_filters
geometry: |AB| < Rvdw(A)+Rvdw(B)+0.5 Å  (non-H atoms)
slack_A: 0.5
exclude_sequential_protein: True   # drop |resid_i − resid_j| == 1
selection: "protein"               # apo; no 8D0
p_ij_edge_threshold: 0.1           # edge if frame-fraction ≥ 0.1 (P1)
VdW radii: H 1.20, C 1.70, N 1.55, O 1.52, S 1.80, P 1.80, F 1.47, CL 1.75, BR 1.85, I 1.98
```

Same limitation as P1: chemotype angles / water bridges not reimplemented.

**Multi-frame rule:** accumulate binary contacts per frame → \(p_{ij}\) = fraction of frames; undirected edge if \(p_{ij} \ge 0.1\).

**Secondary (sensitivity only; does not drive verdict):** Cα–Cα contact if ‖CA_i − CA_j‖ < 8.0 Å in ≥10% of frames, exclude `|Δresid| < 2`. Report Jaccard vs primary; do not retune.

**Residue labels:** `RESNAME:resid` using **topology-native** residue numbers (ACE/NME excluded from graphs / hub AA checks).

---

## Hub mapping (locked a priori — descriptive Q4)

Fixed LigACN set (project numbering = UniProt P34972 indices):

| Hub | Project label | Expected AA |
|-----|---------------|-------------|
| ALA79 | `ALA:79` | ALA |
| ALA83 | `ALA:83` | ALA |
| LEU287 | `LEU:287` | LEU |
| ASN291 | `ASN:291` | ASN |
| ASN295 | `ASN:295` | ASN |
| ARG302 | `ARG:302` | ARG |

**Mapping into APO topology:** align protein sequence (excluding ACE/NME) to UniProt **P34972**; take UniProt indices → topology `resid`. Accept hub only if aligned residue has expected AA (1-letter); else `HUB_MAP_FAIL`. No post-hoc hub substitution. Prior PDB refs used the same construct (expect ~−20 resid offset vs UniProt if N-term truncated).

Metrics (descriptive): degree in primary contact graph; Jaccard of hub-incident edge sets inactive vs active.

---

## Metrics (locked a priori)

Let \(E_s\) = undirected edge set of state \(s \in \{\mathrm{inactive}, \mathrm{active}\}\) after \(p_{ij}\) threshold.

| Metric | Definition |
|--------|------------|
| `n_edges[s]` | \|E_s\| |
| `jaccard_inactive_active` | \|E_i ∩ E_a\| / \|E_i ∪ E_a\| |
| `frac_private[s]` | \|E_s \ E_{other}\| / max(\|E_s\|, 1) |
| `mean_frac_private` | mean of `frac_private` over both states |
| `n_frames[s]`, `n_atoms` | smoke fields |

**Substantial difference (Q2):** `jaccard_inactive_active < 0.80` → `DIFFERS_SUBSTANTIALLY`; else `SIMILAR_OVERALL`.

---

## Soft A/B/C at contact-map level (thresholds locked — pilot scope)

| Label | A priori rule |
|-------|----------------|
| `EXT_APO_PILOT_CONTACTS_STABLE` | `jaccard ≥ 0.80` **and** `mean_frac_private < 0.15` |
| `EXT_APO_PILOT_CONTACTS_STATE_DEPENDENT` | Not STABLE; **and** `mean_frac_private ≥ 0.15` |
| `EXT_APO_PILOT_CONTACTS_DIFFUSE` | Not STABLE; **and** `mean_frac_private < 0.15` **and** `jaccard < 0.55` |
| `EXT_APO_PILOT_CONTACTS_INDETERMINATE` | None of the above cleanly |

**Soft compare to prior PDB (annotation only):**

| Label | Rule |
|-------|------|
| `EXT_APO_PILOT_SOFT_AGREE_PDB_B` | Primary = `STATE_DEPENDENT` (same soft class as `EXT_PDB_CONTACTS_STATE_DEPENDENT` / snapshot B) |
| `EXT_APO_PILOT_SOFT_DISAGREE_PDB_B` | Primary ≠ `STATE_DEPENDENT` |
| `EXT_APO_PILOT_SOFT_COMPARE_NA` | Smoke/data failure |

**Always emit (epistemic):**

| Label | Rule |
|-------|------|
| `EXT_APO_PILOT_SINGLE_TRAJ_LIMIT` | Always true for this primary run (1 nc / state) |
| `EXT_APO_PILOT_NEEDS_MORE_TRAJS` | Recommend stratified ≥5+5 from zip if robustness required (default: **yes** after pilot) |

Never promote pilot tags to P2 `CONVERGENT` / ensemble architecture.

---

## Forbidden interpretations

- Do **not** claim Gi coupling mechanism.  
- Do **not** reopen P1 hub hunt or change the six-hub list.  
- Do **not** treat 1–2 traj chunks as MSM / full CB2_APO ensemble.  
- Do **not** claim P2 Gate-1 CONVERGENT.  
- Do **not** dock or design ligands from this result.

---

## Outputs

| Path | Content |
|------|---------|
| `scripts/network_core/cb2_apo_pilot_contacts.py` | Runner (+ smoke-open) |
| `results/network_core/cb2_apo_pilot_contacts.md` | Human report + verdicts |
| `results/network_core/cb2_apo_pilot_contacts.json` | Machine payload |

Do **not** commit `.nc` / `.prmtop` / `.zip`.

---

## CLI

```bash
.\.micromamba\micromamba.exe run -n janus_p1 python scripts/network_core/cb2_apo_pilot_contacts.py
```

Optional later: `--extract-sample 5` to pull 5+5 from zip (not part of primary locked run unless invoked).

---

*Fin pre-registro. Ejecutar solo tras presencia de este archivo; no editar umbrales después de ver resultados.*

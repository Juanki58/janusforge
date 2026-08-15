# Qiu 0F — Docking protocol preparation (NOT EXECUTED)

> **Scope:** preparation only. No Vina run, no PDBQT generation, no receptor/ligand modification, no minimization, no pose/SAR interpretation.
>
> **0E status:** `0E = PASS 4/4 (closed)` — validated ligands left read-only (audit: [`qiu_0e_raw_pdbqt_audit.md`](qiu_0e_raw_pdbqt_audit.md)).
>
> **0F status:** `0F = READY / NOT EXECUTED`
>
> Date: 2026-08-12

---

## Accidental / partial outputs

- No `results/docking/qiu_0f/` directory present.
- No `vina` process running at protocol lock time.
- **No docking outputs exist for 0F.** Nothing to discard.

---

## A) Receptor + justification (from project files)

### Candidates found under `data/targets/cb2/`

| File | Role |
|------|------|
| `data/targets/cb2/6PT0_rec.pdbqt` | Prepared receptor PDBQT (docking input) |
| `data/targets/cb2/6PT0.pdb` | Raw PDB download |
| `data/targets/cb2/6PT0_clean.pdb` | Cleaned protein |
| `data/targets/cb2/6PT0_ligand.pdb` | Co-crystallized ligand extract (WI5) |
| `data/targets/cb2/6PT0_rec.box.pdb` / `.txt` | Box sidecar from prep |
| `data/targets/cb2/box.json` | Versioned box + receptor pointer |

Config also notes contrast structure **5ZTY** (antagonist-bound) in comments only — **no 5ZTY receptor PDBQT is present** in this repo; not a runnable candidate.

### Locked receptor (matches project protocol)

| Field | Value | Source |
|-------|-------|--------|
| Target | CB2 (primary for 0F; user-authorized) | This 0F prep scope |
| PDB ID | **6PT0** | `configs/cb1_cb2.yaml` → `targets.cb2.pdb` |
| Conformation / state | Agonist-bound / active-state Cryo-EM CB2–Gi with agonist WIN 55,212-2 | `configs/cb1_cb2.yaml` → `targets.cb2.pdb_notes`; `docking.cb2_structure_mode: agonist` |
| Co-crystal ligand | WI5 (WIN 55,212-2), chain R, resseq 401 | `data/targets/cb2/box.json` |
| Receptor PDBQT | **`data/targets/cb2/6PT0_rec.pdbqt`** | `configs/cb1_cb2.yaml` → `targets.cb2.receptor_pdbqt` and `docking.cb2.receptor`; `box.json` → `receptor_pdbqt`; `configs/docking_boxes_generated.yaml` |

**Why this one (not arbitrary):** every versioned docking path in janusforge points to 6PT0 agonist-state CB2 (`cb1_cb2.yaml`, `docking_boxes_generated.yaml`, `box.json`, Qiu Batch 1 gate summary). No alternate CB2 docking PDBQT exists in-tree.

**Historical dual-gate note (not executed in 0F):** Qiu Batch 1 and other gates dock **both** CB1 5TGZ + CB2 6PT0. User 0F authorization is CB2 receptor/conformation. This protocol locks **CB2-only**. CB1 is documented below for reference but **commands are CB2-only and NOT EXECUTED**.

Path existence (read-only check, 2026-08-12): **EXISTS** — `data/targets/cb2/6PT0_rec.pdbqt`.

---

## B) Full docking parameters (locked from versioned files)

### Box (CB2) — identical sources agree

| Parameter | Value | Sources (all agree) |
|-----------|-------|---------------------|
| `center_x` | **98.379** | `data/targets/cb2/box.json`; `data/targets/cb2/6PT0_rec.box.txt`; `configs/cb1_cb2.yaml` → `docking.cb2.box`; `configs/docking_boxes_generated.yaml` |
| `center_y` | **109.559** | same |
| `center_z` | **123.801** | same |
| `size_x` | **22.0** | same |
| `size_y` | **22.0** | same |
| `size_z` | **22.0** | same |
| Box origin | Co-crystallized ligand centroid (WI5) | `box.json` → `source`; `docking_boxes_generated.yaml` → `box_source` |

### Engine / search params from `configs/cb1_cb2.yaml` → `docking`

| Parameter | Locked value | Source |
|-----------|--------------|--------|
| `exhaustiveness` | **8** | `configs/cb1_cb2.yaml` → `docking.exhaustiveness` (also default in `src/screening/docking.py`) |
| `num_modes` | **9** | `configs/cb1_cb2.yaml` → `docking.num_modes` |
| `seed` | **42** | `configs/cb1_cb2.yaml` → `docking.seed` |
| `energy_range` | **not set** | Absent from `configs/cb1_cb2.yaml` and from `src/screening/docking.py` CLI args → **do not pass**; Vina built-in default applies at execution time |
| `cpu` / threads | **not set** in project config | Qiu Batch 1 logs show `CPU: 0` (Vina auto); **do not invent** a thread count |
| Scoring function | Vina (engine default) | Batch 1 logs: `Scoring function : vina` |

### Exhaustiveness historical note (not an alternate lock)

- Qiu Batch 1 gate summary documents **`exhaustiveness=10`** with `seed=42` ([`qiu_pyrazole_batch1_gate_summary.md`](qiu_pyrazole_batch1_gate_summary.md); also visible in `results/docking/qiu_pyrazole_batch1/cb2/QIU_14_vina.log`).
- That value is a **CLI override**, not the versioned YAML default.
- **0F locks `exhaustiveness=8`** from `configs/cb1_cb2.yaml` (versioned project protocol). If a future execution must reproduce Batch 1 settings exactly, change must be an explicit amendment to this protocol before any run.

### Uniformity confirmation

All four compounds (14 / 15 / 20 / 24) will use **the same**:

- receptor PDBQT (`6PT0_rec.pdbqt`)
- box (center + size above)
- exhaustiveness / num_modes / seed
- engine binary + version
- command template (ligand path only differs)

No per-compound parameter variation.

### Planned output directory (when executed later)

`results/docking/qiu_0f/` — **not created in this prep step.**

---

## C) Docking engine + version (version check only; no docking)

| Field | Value |
|-------|-------|
| Engine | AutoDock Vina |
| Version (checked) | **AutoDock Vina v1.2.7** |
| Check command | `..\molforge\tools\vina.exe --version` (version-only; no docking) |
| Binary path (config) | `configs/cb1_cb2.yaml` → `docking.vina_binary: ../molforge/tools/vina.exe` |
| Resolved path | `C:\Users\juanc\projects\molforge\tools\vina.exe` (**EXISTS**) |
| Local `tools/vina.exe` | **ABSENT** — runner falls back via config / `resolve_vina` to molforge path ([`tools/README.md`](../../tools/README.md)) |

Wrapper reference (not executed): `src/screening/docking.py` → `dock_ligand` / `resolve_vina`; retrospective runner `scripts/run_retrospective_dock.py`.

---

## D) Paths — ligands (read-only) + receptor

### Ligands — validated 0E PDBQTs (DO NOT modify / overwrite)

| Compound | Path | Exists |
|----------|------|--------|
| 14 | `results/docking/qiu_0e/compound_14_lig.pdbqt` | YES |
| 15 | `results/docking/qiu_0e/compound_15_lig.pdbqt` | YES |
| 20 | `results/docking/qiu_0e/compound_20_lig.pdbqt` | YES |
| 24 | `results/docking/qiu_0e/compound_24_lig.pdbqt` | YES |

### Receptor

| Path | Exists |
|------|--------|
| `data/targets/cb2/6PT0_rec.pdbqt` | YES |

---

## E) Exact pending commands — **NOT EXECUTED**

Working directory: repo root `C:\Users\juanc\projects\janusforge`.

Create output dir only at execution time (not now):

```bat
mkdir results\docking\qiu_0f
```

### Compound 14 — NOT EXECUTED

```bat
..\molforge\tools\vina.exe --receptor data\targets\cb2\6PT0_rec.pdbqt --ligand results\docking\qiu_0e\compound_14_lig.pdbqt --out results\docking\qiu_0f\compound_14_cb2_out.pdbqt --center_x 98.379 --center_y 109.559 --center_z 123.801 --size_x 22.0 --size_y 22.0 --size_z 22.0 --exhaustiveness 8 --num_modes 9 --seed 42 > results\docking\qiu_0f\compound_14_cb2.log 2>&1
```

### Compound 15 — NOT EXECUTED

```bat
..\molforge\tools\vina.exe --receptor data\targets\cb2\6PT0_rec.pdbqt --ligand results\docking\qiu_0e\compound_15_lig.pdbqt --out results\docking\qiu_0f\compound_15_cb2_out.pdbqt --center_x 98.379 --center_y 109.559 --center_z 123.801 --size_x 22.0 --size_y 22.0 --size_z 22.0 --exhaustiveness 8 --num_modes 9 --seed 42 > results\docking\qiu_0f\compound_15_cb2.log 2>&1
```

### Compound 20 — NOT EXECUTED

```bat
..\molforge\tools\vina.exe --receptor data\targets\cb2\6PT0_rec.pdbqt --ligand results\docking\qiu_0e\compound_20_lig.pdbqt --out results\docking\qiu_0f\compound_20_cb2_out.pdbqt --center_x 98.379 --center_y 109.559 --center_z 123.801 --size_x 22.0 --size_y 22.0 --size_z 22.0 --exhaustiveness 8 --num_modes 9 --seed 42 > results\docking\qiu_0f\compound_20_cb2.log 2>&1
```

### Compound 24 — NOT EXECUTED

```bat
..\molforge\tools\vina.exe --receptor data\targets\cb2\6PT0_rec.pdbqt --ligand results\docking\qiu_0e\compound_24_lig.pdbqt --out results\docking\qiu_0f\compound_24_cb2_out.pdbqt --center_x 98.379 --center_y 109.559 --center_z 123.801 --size_x 22.0 --size_y 22.0 --size_z 22.0 --exhaustiveness 8 --num_modes 9 --seed 42 > results\docking\qiu_0f\compound_24_cb2.log 2>&1
```

**Status of all four commands: NOT EXECUTED.**

---

## F) Post-execution QC checklist (for later run; not performed now)

After a future authorized execution, QC only (no ranking / no SAR narrative):

1. **Completion:** all 4 compounds finished (`compound_{14,15,20,24}_cb2_out.pdbqt` + matching `.log` present).
2. **Exit success:** Vina return code 0 (or log shows completed mode table without fatal error) for each.
3. **n poses:** each out PDBQT contains expected modes (up to `num_modes=9`; report actual count).
4. **Scores:** best affinity parsed numerically per compound; store in CSV/JSON for QC — **no winner declaration**.
5. **No errors:** logs free of crash / missing-receptor / empty-output failures.
6. **Pose validity:** finite coordinates; pose atom counts consistent with input ligand PDBQT; poses in/near locked box.
7. **Config match:** each log reports same receptor path, grid center/size, exhaustiveness=8, seed=42 (and engine version consistent with lock).
8. **Ligand integrity:** input 0E PDBQTs unchanged (timestamps/hashes vs 0E audit).
9. **Verdict rule:** `0F = PASS 4/4` if all QC checks pass; else `0F = NEEDS REVIEW (X/4)`.
10. **Explicit:** interpretation deferred; no compound ranking.

---

## G) Verdict

**`0F = READY / NOT EXECUTED`**

Critical items resolved from versioned project files:

- CB2 receptor/conformation unambiguous: **6PT0** → `6PT0_rec.pdbqt`
- Box unambiguous across `box.json` / `.box.txt` / YAML
- Params locked from `configs/cb1_cb2.yaml` (exhaustiveness=8, num_modes=9, seed=42)
- `energy_range` intentionally unset (not in project protocol)
- Engine available: AutoDock Vina **v1.2.7**
- All four ligand paths + receptor path exist
- Commands prepared and marked **NOT EXECUTED**

No docking was run under this preparation step.

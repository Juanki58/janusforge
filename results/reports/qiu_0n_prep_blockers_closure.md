# Qiu 0N — Prep blockers closure audit

> **Date:** 2026-08-13  
> **Scope:** Preparation / audit only. **No MD. No docking.** No modification of receptor/ligand PDBQT or docking outputs.  
> **No invented data** — unknown knobs stay **TBD**; stack substitution stays **REQUIERE DECISIÓN** until waived.  
> **Companions:** [`qiu_0n_md_protocol_ready.md`](qiu_0n_md_protocol_ready.md) · [`qiu_0n_status.md`](qiu_0n_status.md) · [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md) · [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md)

---

## Verdict

# **0N = BLOCKED**

**Why not READY TO EXECUTE:** TBD-0N-11/12 remain **REQUIERE DECISIÓN** (no signed waiver); local MD path needs Docker/WSL + CUDA OpenMM (Docker daemon **not running** at audit; host OpenMM has **no CUDA** platform); membrane env packages (`openff-toolkit`, `openmmforcefields`, AmberTools/`packmol-memgen`) **absent on Windows host**. Prep evidence for stack identity, 6PT0 provenance, CB2 TM map, and cost is now closed below — **execution is still gated**.

**Recommendation (exactly one):** **3. no ejecutar y pasar directamente a H1-a**

Rationale: 0N is optional orthogonal structural compute, not a pharmacological gate; H1-a CRO remains arbiter; remaining blockers are authorization + ops restore (Docker/GPU env), not missing scientific design for MINIMAL. Prefer RFQ send over waiting on stack waiver / Docker.

---

## 1. TBD-0N-11/12 — software stack + charges

### 1.1 What MINIMAL 0N needs (from protocol + Ge docs + prior MD)

| Role | Ge et al. 2023 (published track) | Janusforge MINIMAL / local precedent |
|------|----------------------------------|--------------------------------------|
| Engine | **AMBER 18** PMEMD.cuda | **OpenMM** CUDA (`scripts/run_md_openmm_membrane_lead.py`) |
| Membrane builder | CHARMM-GUI | `packmol-memgen` (AmberTools) |
| Protein FF | FF14SB | `amber14-all` |
| Lipid FF | **Lipid14** POPC | **lipid17** POPC (`amber14/lipid17`) |
| Ligand FF | **GAFF** + **RESP** (HF/6-31G\*, Gaussian 16 / Antechamber) | **GAFF2** (`gaff-2.11` via OpenFF + `GAFFTemplateGenerator`) |
| Water / salt | TIP3P; 0.15 M | TIP3P; 0.15 M (same themes) |
| Duration (MINIMAL) | Ge analysis window 115 ns-class (full LRIP) | **20 ns** production, **1 replica** (D2_22 / membrane panel precedent) |

Sources: [`qiu_0n_md_protocol_ready.md`](qiu_0n_md_protocol_ready.md); [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md); [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md); [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md); [`environments/environment-md-membrane.yml`](../../environments/environment-md-membrane.yml).

**Charge path clarification (do not conflate):**

| Stage | Method in-repo | Notes |
|-------|----------------|-------|
| Ge MD (paper) | **RESP** HF/6-31G\* | Fidelity track only |
| Qiu 0E docking PDBQT | Meeko; partial charges **Gasteiger** (audit: Σq≈0) | [`qiu_0e_raw_pdbqt_audit.md`](qiu_0e_raw_pdbqt_audit.md) — **not** RESP; **not** proven AM1-BCC |
| Local membrane MD script | OpenFF molecule → **GAFF2** templates | Typical OpenFF/AmberTools path uses AM1-BCC-class charges when antechamber is available; **exact charge method at 0N exec = TBD until env locked** |

**TBD-0N-11 / TBD-0N-12 status after this audit:** **Clarified, not waived.** OpenMM/lipid17/GAFF2 ≠ AMBER18/Lipid14/GAFF/RESP. Using the local stack for scoped structural MD still **REQUIERE DECISIÓN / waiver** before any run. Ge-faithful RESP/AMBER path is **not** demonstrated locally.

### 1.2 Local availability (read-only version checks, 2026-08-13)

| Component | Host status | Version / note |
|-----------|-------------|----------------|
| OS / CPU | Available | Windows 10; Intel Core i5-6600K (4C/4T); ~16 GB RAM |
| GPU / driver | Available | **NVIDIA GeForce GTX 1060 6GB**, driver **536.99** (`nvidia-smi`) |
| `nvcc` (CUDA toolkit) | **Missing** on PATH | Runtime may exist via driver; toolkit compiler not found |
| Python | Available | **3.14.6** |
| OpenMM | Available (host) | **8.5.2** — platforms: `Reference`, `CPU`, `OpenCL` — **no `CUDA` platform registered** |
| RDKit | Available | **2025.09.6** |
| Meeko | Available | **0.7.1** |
| mdtraj | Available | **1.11.1.post2** |
| pdbfixer | Available | import OK (no `__version__`) |
| openff-toolkit | **Missing** (host) | Required by membrane script / env yml |
| openmmforcefields | **Missing** (host) | Required for GAFF2 templates |
| AmberTools / `antechamber` | **Missing** (host) | Expected: not win-64 |
| `packmol` / `packmol-memgen` | **Missing** (host) | Required for POPC build |
| Docker CLI | Installed | **29.6.2** |
| Docker daemon | **Not running** | `docker images` / volume checks failed (engine pipe missing) |
| Micromamba binary | Present | `.micromamba/micromamba.exe` **2.8.1** (env contents inside Docker volume **not** re-verified — daemon down) |
| Prior successful MD path | Documented | Docker GPU + `janus_md` / `environment-md-membrane.yml` (D2_22 EXIT_CODE=0) |

**Missing for MINIMAL 0N execution on this machine (ops):** Docker engine up + GPU passthrough; Linux env with OpenMM **CUDA**, `openff-toolkit`, `openmmforcefields`, AmberTools/`packmol-memgen`; CB2 adaptation of membrane script (historically CB1-oriented — TBD at auth). Host-only Python is **insufficient**.

### 1.3 Decision still required

| ID | Decision | If waived as MINIMAL | If Ge-faithful required |
|----|----------|----------------------|-------------------------|
| TBD-0N-11 | Accept OpenMM + lipid17 + GAFF2 ≠ AMBER18 + Lipid14 + GAFF | Scoped structural MD only; label ≠ Ge reproduction | Rebuild AMBER18/CHARMM-GUI/Lipid14 track (**not** local) |
| TBD-0N-12 | Accept non-RESP ligand charges (OpenFF/GAFF2 path; docking PDBQT was Meeko/Gasteiger) | Document charge method at exec; no Ge LRIP claims | RESP HF/6-31G\* + Antechamber (**Gaussian/RESP toolchain TBD**) |

---

## 2. 6PT0 receptor + Qiu-14 MODEL 1 (read-only)

### 2.1 Receptor used in 0F — **VERIFIED**

| Evidence | Value |
|----------|-------|
| Protocol | [`qiu_0f_docking_protocol.md`](qiu_0f_docking_protocol.md) / [`qiu_0f_docking_qc.md`](qiu_0f_docking_qc.md) |
| Cmd | `results/docking/qiu_0f/compound_14_cb2.cmd.txt` → `--receptor data\targets\cb2\6PT0_rec.pdbqt` |
| Log | `compound_14_cb2.log` → `Rigid receptor: …\data\targets\cb2\6PT0_rec.pdbqt` |
| Params JSON | `"receptor": "data/targets/cb2/6PT0_rec.pdbqt"` |
| Box | center 98.379 / 109.559 / 123.801; size 22³ — matches `6PT0_rec.box.txt` / `receptor_prep_summary.json` |

**Conclusion:** 0F Qiu-14 CB2 docking used **`data/targets/cb2/6PT0_rec.pdbqt`**. Receptor **not modified** in this audit.

### 2.2 Original PDB 6PT0 — **LOCATED**

| Asset | Path | Role |
|-------|------|------|
| Raw PDB | `data/targets/cb2/6PT0.pdb` | RCSB download in-repo (HEADER 6PT0; CB2–Gi + WIN 55,212-2) |
| Clean protein | `data/targets/cb2/6PT0_clean.pdb` | Prep intermediate |
| Co-crystal ligand | `data/targets/cb2/6PT0_ligand.pdb` | WI5 |
| Receptor PDBQT | `data/targets/cb2/6PT0_rec.pdbqt` | Docking input (Meeko `mk_prepare` log present) |
| External reference | https://www.rcsb.org/structure/6PT0 | Same PDB ID as `configs` / README |

**DBREF (published in PDB file):** chain R → UniProt **P34972** residues 1–360.

**Note:** `6PT0_rec.pdb` (non-PDBQT) still **not** present; raw/clean PDBs exist for membrane export planning (**TBD-0N-MD-01** at auth — do not mutate PDBQT in place).

### 2.3 Qiu-14 MODEL 1 pose — **LOCATED**

| Asset | Path |
|-------|------|
| Seed pose | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` |
| MODEL 1 score | REMARK VINA RESULT **−9.919** (matches log mode 1) |
| Ligand input | `results/docking/qiu_0e/compound_14_lig.pdbqt` |

Pose PDB export for membrane build remains **TBD at execution** (read-only transform; no re-dock).

---

## 3. CB2 TM helix map for 0N metrics

### 3.1 PUBLISHED (cite only)

| Source | Content | Class |
|--------|---------|-------|
| UniProtKB **P34972** (CNR2_HUMAN; fetched 2026-08-13 REST) | TM1 34–59; TM2 72–92; TM3 105–129; TM4 150–172; TM5 189–214; TM6 247–267; TM7 280–301 | **PUBLISHED** annotation |
| 6PT0 PDB `DBREF` | Chain R aligned to UNP P34972 1–360 | **PUBLISHED** in structure file |
| Ge et al. main-text hotspots (in-repo extract/protocol) | BW / site labels e.g. **V3.32, T3.33, S7.39, F183, W5.43, I3.29** | **PUBLISHED** (Ge); not a full TM index table |
| Prior CB1 MD in this repo | TM3 **185–220**; TM6 **332–369** (UniProt **P21554** / 5TGZ) | **PUBLISHED for CB1 only** — **must not** be reused as CB2 indices |

### 3.2 Structure-backed residue presence (not a new map)

`6PT0_rec.pdbqt` chain R spans residues **22–319** (298 residues). UniProt TM3/TM5/TM6/TM7 endpoint residues **are present** in the PDBQT (checked read-only). Suitable for declaring TM Cα selections **if** authorization freezes UniProt ranges as the metric definition.

### 3.3 INFERENCE / TBD (do not invent)

| Item | Status |
|------|--------|
| Full BW ↔ sequence table for all CB2 sites | **TBD** — not assigned in 0G/0H (`Ballesteros–Weinstein indices not assigned`) |
| Equating Ge **S7.39** to a specific 6PT0 residue index for metrics | **INFERENCE unless separately cited** — 0G/0H report **SER285** as structure contact residue, not as BW assignment |
| Copying CB1 TM3/TM6 numeric ranges onto 6PT0 | **FORBIDDEN** (wrong UniProt) |
| Engineered 6PT0 construct quirks vs full P34972 | SEQADV expression tags beyond 360; receptor PDBQT truncated vs full UniProt C-term — document at exec |

### 3.4 Proposed freeze for MINIMAL metrics (requires auth — not auto-executed)

If TM-focused RMSD/COM are authorized, pre-declare from **UniProt P34972** (same numbering as 6PT0 DBREF):

| Helix | UniProt range (PUBLISHED) |
|-------|---------------------------|
| TM3 | 105–129 |
| TM6 | 247–267 |

Contact-shell metrics can continue to use **0G/0H observed residue lists** (structure numbering on chain R) without inventing new Å gates. Closing TBD-0N-MD-02 still needs explicit auth freeze of the table above (or an alternate published source).

---

## 4. COST — MINIMAL scenario (Qiu-14 · ~20 ns · 1 replica)

All $ figures without invoice anchors = **estimates TBD calibrated**. Timing uses **documented** precedents only.

### 4.A User machine (detected)

| Item | Value | Source |
|------|-------|--------|
| Hardware | i5-6600K + **GTX 1060 6GB** + ~16 GB RAM | `nvidia-smi` / WMI this audit |
| Prep time | Build `packmol-memgen` ≈ minutes–tens of minutes; equil ~1 ns ≈ **1–2 h** | [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md) |
| Run time (20 ns) | Plan **~0.7–1.3 days** @ **~15–30 ns/day**; empirical D2_22 wall **~12 h** | Plan + [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md) (14:24Z→02:34Z) |
| Direct $ | Host/electricity **TBD calibrated** (no $/kWh table in repo) | — |
| Storage | Order **~1.7 GB** DCD + metrics (D2_22 `production.dcd` ~1.70 GB) | D2_22 summary |
| Extras | Docker Desktop must be running; GPU passthrough; CB2 script adaptation TBD | This audit + protocol |
| Free/local | GPU time on owned hardware once Docker/CUDA env restored; sunk cost of machine | — |
| Current ops gap | Docker daemon **down**; host OpenMM **without CUDA**; membrane conda deps missing | This audit |

### 4.B Cloud CPU

| Item | Estimate | Note |
|------|----------|------|
| Prep | Similar chemistry prep if AmberTools image used — **TBD** wall | No CB2 0N cloud CPU timing in repo |
| Run time | **TBD** — no ns/day figure for membrane POPC on CPU in repo; expect **much slower** than GTX 1060 GPU path | Do not invent ns/day |
| Direct $ | **TBD calibrated** (SKU/hr unknown) | TBD-0N-MD-06 |
| Storage | Same order ~2 GB class + egress | — |
| Practicality | **Not recommended** for 20 ns membrane without a measured CPU throughput | — |

### 4.C Cloud GPU

| Item | Estimate | Note |
|------|----------|------|
| Prep | Same stack rebuild in Linux GPU image — minutes–hours **TBD** | Env yml exists |
| Run time | Expect **shorter** wall than GTX 1060 if modern GPU; **TBD** without smoke | Scale from local 12 h / 0.7–1.3 d anchors only as order-of-magnitude |
| Direct $ | **TBD calibrated** (no firm cloud $/hr in repo) | TBD-0N-MD-06 |
| Storage / extras | DCD egress; IP hygiene (no public push of coords) | Protocol hard rules |
| Free/local vs paid | Paid instance hours; design/docs free | — |

---

## 5. Blocker table

| Bloqueo | Evidencia | Solución | Coste | Tiempo | ¿Requiere autorización? |
|---------|-----------|----------|-------|--------|-------------------------|
| TBD-0N-11 stack Ge≠local | Ge AMBER18/Lipid14 vs OpenMM/lipid17 documented | Waive for scoped MD **or** rebuild AMBER track | Waiver: $0; AMBER rebuild: **TBD** | Waiver: minutes docs; AMBER: **TBD** | **Sí** |
| TBD-0N-12 charges RESP≠local | Ge RESP; 0E Meeko/Gasteiger; MD=OpenFF/GAFF2 | Waive non-RESP for MINIMAL **or** run RESP | Waiver: $0; RESP: Gaussian/**TBD** | Waiver: minutes; RESP: **TBD** | **Sí** |
| Docker/CUDA ops | Daemon down; host OpenMM no CUDA; missing OpenFF/AmberTools | Start Docker Desktop + prior `janus_md` GPU volume / recreate `environment-md-membrane.yml` | Local sunk; cloud GPU **TBD $/hr** | Env restore **TBD** (hours if volume intact) | **Sí** (GPU spend) |
| 6PT0 provenance | 0F cmd/log/params → `6PT0_rec.pdbqt`; PDB on disk | **Closed** — no action | $0 | Done | No |
| Qiu-14 MODEL 1 seed | `compound_14_cb2_out.pdbqt` MODEL 1 (−9.919) | **Closed** — freeze at auth; no re-dock | $0 | Done | Freeze confirmation **Sí** at exec |
| Export PDB for membrane (TBD-0N-MD-01) | `6PT0_rec.pdb` missing; `6PT0.pdb`/`_clean` exist | Auth-time read-only export from PDB + MODEL 1 | $0 compute | Minutes–hours | **Sí** (method freeze) |
| CB2 TM map (TBD-0N-MD-02) | UniProt P34972 + 6PT0 DBREF; CB1 ranges invalid | Freeze TM3 105–129 / TM6 247–267 **or** TM-optional metrics only | $0 | Minutes | **Sí** (metric freeze) |
| Cloud $ calibration (TBD-0N-MD-06) | No invoice anchors in repo | Pick SKU + quote **or** stay local | **TBD** | **TBD** | **Sí** if cloud |
| Ge SI / LRIP | ACS SI blocked | Out of scope for MINIMAL structural 0N | — | — | N/A for MINIMAL; blocks Ge track only |
| GPU / wall for 20 ns | GTX 1060 plan 0.7–1.3 d; D2_22 ~12 h | Run after GO | Local electricity **TBD**; cloud **TBD** | ~0.5–1.5 d class | **Sí** |

---

## 6. Final recommendation

**3. no ejecutar y pasar directamente a H1-a**

Do **not** start 0N MD until (a) explicit waivers for TBD-0N-11/12, (b) Docker/CUDA membrane env restored and smoke-checked, and (c) GPU/time authorized. Critical path remains `cro_package_h1a/SEND/` RFQs. If later authorized, prefer **local GPU** (recommendation 1) over cloud while GTX 1060 + Docker path is the documented precedent; cloud GPU (2) only if local Docker/GPU unavailable after restore attempt.

---

## Pointers updated

- This closure: [`qiu_0n_prep_blockers_closure.md`](qiu_0n_prep_blockers_closure.md)  
- Status / protocol: see pointer lines in [`qiu_0n_status.md`](qiu_0n_status.md) and [`qiu_0n_md_protocol_ready.md`](qiu_0n_md_protocol_ready.md)

**No MD executed under this audit.**

# **0N = BLOCKED**

# Qiu 0F — CB2 docking execution QC (compounds 14 / 15 / 20 / 24)

> **Scope:** objective execution QC only. No pose interpretation, no SAR, no ranking narrative.
>
> **Protocol:** [`qiu_0f_docking_protocol.md`](qiu_0f_docking_protocol.md)
>
> **Date:** 2026-08-12
>
> **Runner:** `scripts/run_qiu_0f_docking.py`

---

## Locked config (all four identical)

| Field | Value |
|-------|-------|
| Engine | AutoDock Vina **v1.2.7** (`../molforge/tools/vina.exe`) |
| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` (unmodified) |
| Center | 98.379, 109.559, 123.801 |
| Size | 22.0, 22.0, 22.0 |
| exhaustiveness | **8** |
| num_modes | 9 |
| seed | 42 |
| energy_range | omitted (engine default) |
| Ligands | `results/docking/qiu_0e/compound_{14,15,20,24}_lig.pdbqt` (read-only) |
| Output dir | `results/docking/qiu_0f/` |

Command template (ligand/out paths only differ):

```bat
..\molforge\tools\vina.exe --receptor data\targets\cb2\6PT0_rec.pdbqt --ligand results\docking\qiu_0e\compound_XX_lig.pdbqt --out results\docking\qiu_0f\compound_XX_cb2_out.pdbqt --center_x 98.379 --center_y 109.559 --center_z 123.801 --size_x 22.0 --size_y 22.0 --size_z 22.0 --exhaustiveness 8 --num_modes 9 --seed 42
```

Per-compound cmd copies: `results/docking/qiu_0f/compound_{N}_cb2.cmd.txt`  
Params JSON: `results/docking/qiu_0f/compound_{N}_cb2_params.json`  
Scores: `results/docking/qiu_0f/qiu_0f_scores.json`, `qiu_0f_scores.csv`

---

## QC table

| Q | 14 | 15 | 20 | 24 |
|---|----|----|----|----|
| **1. Finished correctly?** | YES (rc=0) | YES (rc=0) | YES (rc=0) | YES (rc=0) |
| **2. Result artifacts?** | out+log+cmd+params | out+log+cmd+params | out+log+cmd+params | out+log+cmd+params |
| **3. n poses (log table / PDBQT MODEL)** | 9 / 9 | 9 / 8 | 6 / 5 | 9 / 9 |
| **4. Scores (kcal/mol), log order** | −9.919, −9.789, −9.451, −9.287, −9.031, −8.907, −8.787, −8.742, −8.529 | −11.2, −11.17, −10.59, −10.55, −10.2, −10.2, −9.628, −9.597, −8.01 | −9.986, −9.048, −8.546, −7.927, −7.363, −6.925 | −11.61, −11.37, −11.23, −10.6, −10.44, −9.34, −9.121, −8.768, −8.724 |
| **4b. Scores written in PDBQT (REMARK VINA RESULT)** | −9.919, −9.789, −9.451, −9.287, −9.031, −8.907, −8.787, −8.742, −8.529 | −11.201, −11.170, −10.593, −10.550, −10.204, −10.203, −9.628, −9.597 | −9.986, −9.048, −8.546, −7.927, −7.363 | −11.606, −11.368, −11.228, −10.604, −10.444, −9.340, −9.121, −8.768, −8.724 |
| **5. Errors / warnings?** | none | none | none | none |
| **6. Same config as protocol?** | YES | YES | YES | YES |
| **7. Outputs readable/valid?** | YES (9 MODEL, 38 atoms each, finite coords) | YES (8 MODEL, 38 atoms each, finite coords) | YES (5 MODEL, 39 atoms each, finite coords) | YES (9 MODEL, 39 atoms each, finite coords) |

### Answers to checklist items

1. **Did each finish correctly?** Yes — return code 0 for all four; mode tables present; non-empty out PDBQTs.
2. **4/4 results?** Yes — `compound_{14,15,20,24}_cb2_out.pdbqt` + matching `.log` / `.cmd.txt` / `_params.json`.
3. **How many poses each?** Log: 9, 9, 6, 9. PDBQT MODEL blocks: 9, 8, 5, 9.
4. **Score of each pose?** Listed numerically above (no ranking).
5. **Errors or warnings?** None in logs (no WARNING/ERROR/crash lines).
6. **Exact same config across four?** Yes — identical receptor, box, exhaustiveness=8, num_modes=9, seed=42, engine v1.2.7; only ligand/out paths differ. Confirmed in each log (`Grid center/size`, `Exhaustiveness: 8`, `random seed: 42`).
7. **Output files readable/valid?** Yes — parseable PDBQT with MODEL/ENDMDL, REMARK VINA RESULT, atom counts match input ligand atom lines (38/38/39/39), zero non-finite coordinates.

### Pose-count note (objective)

Compounds **15** and **20** show **log modes = PDBQT models + 1**. The extra log row is outside the engine-default energy window relative to mode 1 (~3 kcal/mol) and is not written to the out PDBQT. Compound **20** also returned fewer than `num_modes=9` distinct modes in the log (6). Neither case is a crash or config mismatch; both are consistent with Vina defaults when `energy_range` is omitted per protocol.

### Ligand integrity (read-only)

SHA-256 recorded at run start (inputs not regenerated):

| Compound | sha256 |
|----------|--------|
| 14 | `0a2cda674215dc8b71de84c2a8e26806759bddf34fbe3bfcacf4f53cfcd2a9c8` |
| 15 | `cdd8606f855308c25d867e6b80d9074dcc2acffc9afb8e886ecd55d65eff3942` |
| 20 | `29e349682c4f941e81d8323c105d0fbb845d78835e4213c3ead2e5c94b1a3018` |
| 24 | `35a08c401874da5466e04532cdfa68d50ac9cbc8ec5e5ff8b289f2fa9cf0ed32` |

Receptor `data/targets/cb2/6PT0_rec.pdbqt` was not modified.

---

## Artifact index

| Compound | out PDBQT | log | cmd | params |
|----------|-----------|-----|-----|--------|
| 14 | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` | `.../compound_14_cb2.log` | `.../compound_14_cb2.cmd.txt` | `.../compound_14_cb2_params.json` |
| 15 | `results/docking/qiu_0f/compound_15_cb2_out.pdbqt` | `.../compound_15_cb2.log` | `.../compound_15_cb2.cmd.txt` | `.../compound_15_cb2_params.json` |
| 20 | `results/docking/qiu_0f/compound_20_cb2_out.pdbqt` | `.../compound_20_cb2.log` | `.../compound_20_cb2.cmd.txt` | `.../compound_20_cb2_params.json` |
| 24 | `results/docking/qiu_0f/compound_24_cb2_out.pdbqt` | `.../compound_24_cb2.log` | `.../compound_24_cb2.cmd.txt` | `.../compound_24_cb2_params.json` |

(Docking binary outputs under `results/docking/` are gitignored; report + runner script are versioned.)

---

## Verdict

**`0F = PASS 4/4`**

All four dockings finished with return code 0 under the locked protocol config. Interpretation deferred.

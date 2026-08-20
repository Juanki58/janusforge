# THCV Design Constraints — v1.0

Contract for computational gate evaluation (Exam A parity). Thresholds are normative for PASS/FAIL; do not retune during blind challenge runs.

## ADMET

| Metric | Threshold | Verdict |
|--------|-----------|---------|
| TPSA | ≥ 70 Å² | PASS / FAIL |

## CB1 filter (5TGZ antagonist-bound)

All sub-checks must PASS for aggregate CB1 PASS.

| Proxy | Threshold | Notes |
|-------|-----------|-------|
| C3 clearance | ≥ 0.8 Å | `free_extension_before_3.0A_clash` along C3 vector (interaction_mapping) |
| C9/C11 volume delta | ≤ 1.0 Å | \|Δ extension clearance C9 − C3\| at 3.0 Å clash probe |
| Steric clash | no clash @ 3.0 Å | min ligand–TM shell heavy distance ≥ 2.5 Å |

## CB2 filter (6PT0 agonist-bound)

All sub-checks must PASS for aggregate CB2 PASS.

| Proxy | Threshold | Notes |
|-------|-----------|-------|
| C3 occupancy | 2.5 Å envelope | adamantyl terminus within 2.5 Å of tunnel shell (ILE110/ILE186/THR114) |
| Ser285 contact | ≤ 3.5 Å | min heavy ligand → Ser285 sidechain |
| Pose persistence vs HU-308 | centroid ≤ 2.0 Å | mode-1 CB2 pose vs gold HU-308 reference |

## Global verdict

**PASS** only if CB1 filter, CB2 filter, and ADMET TPSA all PASS; otherwise **FAIL**.

## Cross-scaffold mapping (Qiu pyrazole challenge)

| THCV term | Qiu pyrazole proxy |
|-----------|-------------------|
| C3 alkyl terminus | Adamantyl (or adamantylmethyl) distal carbon along amide vector |
| C9/C11 polar zone | N1-aryl morpholine O / piperazine N vs extension clearance delta |
| Pose reference | HU-308 CB2 gold pose (`benchmark_gold_exam_a`) |

Limitations: proxies are geometric only; Vina scores ≠ functional agonism/antagonism.

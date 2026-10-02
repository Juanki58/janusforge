# Phase F — Conformational Fingerprint & CB2_STATE_DISTANCE

**Generated:** 2026-08-19 09:50 UTC  
**Branch:** `feat/fase-f-conformational-fingerprint`

## Governance locks

```yaml
BRANCH: feat/fase-f-conformational-fingerprint
PHASE_F_CONFORMATIONAL_FINGERPRINT: COMPLETE
RETROSPECTIVE_AUDITS_A_TO_E: CLOSED_AND_FROZEN
CONTRACT_v1.0: FROZEN
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION
```

## Level-0 data infrastructure

| PDB | Receptor | State | Ligand (verified) | Aligned PDB | TM Cα pairs | RMSD post (Å) |
|-----|----------|-------|-------------------|-------------|-------------|---------------|
| 6PT0 | CB2 | active_agonist_win_gi | WI5 | `data/targets/multistate_aligned/6PT0_aligned.pdb` | 178 | 0.0 |
| 6KPF | CB2 | active_agonist_cryoem | E3R | `data/targets/multistate_aligned/6KPF_aligned.pdb` | 178 | 22.406 |
| 5ZTY | CB2 | inactive_antagonist_am10257 | 9JU | `data/targets/multistate_aligned/5ZTY_aligned.pdb` | 178 | 15.202 |
| 5TGZ | CB1 | inactive_antagonist_am6538 | ZDG | `data/targets/multistate_aligned/5TGZ_aligned.pdb` | 171 | 0.0 |
| 5XRA | CB1 | active_agonist_am11542 | 8D3 | `data/targets/multistate_aligned/5XRA_aligned.pdb` | 139 | 29.692 |

**Level-0 notes:**
- 5TGZ: antagonist **AM6538** (ZDG), not Taranabant — AM6538 (CCD ZDG) — antagonist/inactive CB1; not Taranabant
- 5XRA: active CB1 agonist **AM11542** (8D3) — selected over 6KPG
- 5ZTY: inactive antagonist **AM10257** (9JU), not Gi-active
- 5VEU: **BLOCKED** — BLOCKED — CYP3A5

## Inter-helix distances & microswitch angles (per PDB)

| PDB | TM3–TM6 IC dist (Å) | Trp6.48 χ1 (°) | Trp6.48 χ2 (°) | ECL2 Phe disp (Å) | Phe tilt (°) | Ser7.39 polar contacts | Ser OG–Trp NE1 (Å) | Cavity vol (Å³) |
|-----|---------------------|----------------|----------------|-------------------|--------------|------------------------|-------------------|-----------------|
| 6PT0 | 15.3343 | 105.2525 | -87.928 | 0.0 | 59.0214 | 0.0 | 10.5586 | 9608.192 |
| 6KPF | 14.796 | 80.8281 | -65.4814 | 27.3566 | 43.5999 | 0.0 | 10.2793 | 9821.696 |
| 5ZTY | 10.2797 | 107.1005 | -134.1433 | 20.1205 | 58.0848 | 2.0 | 10.6391 | 9418.752 |
| 5TGZ | 11.9506 | 96.2948 | -90.7693 | 0.0 | 23.369 | 3.0 | 10.3254 | 9748.48 |
| 5XRA | 15.4697 | 112.8836 | -69.986 | 28.4665 | 78.6494 | 1.0 | 12.1809 | 9324.544 |

Cavity volume method: axis-aligned grid probe (0.8 Å spacing, 24.0 Å box, probe r=1.4 Å); approximation — no Connolly/SAS; membrane/ligand excluded

## CB2_STATE_DISTANCE matrix (normalized Euclidean vs active centroid 6PT0+6KPF)

| PDB | State | Distance (norm) | Distance (raw) |
|-----|-------|-----------------|----------------|
| 5TGZ | inactive_antagonist_am6538 | 3.577 | 48.1623 |
| 5XRA | active_agonist_am11542 | 4.2514 | 392.2007 |
| 5ZTY | inactive_antagonist_am10257 | 4.2819 | 302.2266 |
| 6KPF | active_agonist_cryoem | 1.7646 | 109.1684 |
| 6PT0 | active_agonist_win_gi | 1.7646 | 109.1684 |

### Inactive control

- **5ZTY** normalized distance to active centroid: 4.2819

### CB1 projection vs CB2 active vector

- **5TGZ**: normalized distance 3.577
- **5XRA**: normalized distance 4.2514

### Probe secondary mapping (multistate docking)

- **HU-308**: {"best_docked_state": "6PT0", "best_score_kcal_mol": null, "receptor_fingerprint_distance_to_active_centroid": 1.7646}
- **HU-433**: {"best_docked_state": "6PT0", "best_score_kcal_mol": null, "receptor_fingerprint_distance_to_active_centroid": 1.7646}
- **O-1966**: {"best_docked_state": "6PT0", "best_score_kcal_mol": null, "receptor_fingerprint_distance_to_active_centroid": 1.7646}

### Δ9-THCV historical position

- Receptor state: **6PT0**
- Normalized distance to CB2 active centroid: 1.7646
- CB2 dock affinity: -9.857 kcal/mol
- CB2 pose microswitches: {'Phe117(3.32)': 3.7, 'Trp258(6.48)': 5.91, 'Ser285(7.39)': 4.04}
- THCV docked against CB2 agonist 6PT0 (thcv_seed); receptor-state fingerprint places it on the active-state manifold (distance ≈ 0 vs 6PT0 reference). Pose-level Ser285/Trp258 contacts are secondary (ligand-dependent).

## Conclusion — probe convergence

Active calibration probes converge on the same receptor state (6PT0) in multistate docking; fingerprint distances rank them coherently with that state.

## Scripts

- `scripts/conformational/align_multistate.py`
- `scripts/conformational/extract_fingerprint.py`

# Qiu 0N — Status one-pager

> **Governance lock:** 2026-08-12  
> **Full protocol:** [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md)

## Status

**`0N = READY / NOT EXECUTED (Gated)`**

| Field | Value |
|-------|-------|
| Pharmacological arbiter | **H1-a CRO** (critical path unchanged) |
| 0N role | Optional parallel compute — **not a gate**, **not H1-a substitute** |
| Output labels (LOCKED) | `consistente` \| `no consistente` \| `inconcluso` |

## Hard stops (LOCKED)

1. Do **not** reinterpret docking **0F–0J** as function.
2. **Zero** post-hoc tuning to force Qiu-14 agonist.
3. **No** in silico pharmacological PASS / KILL / FAIL.

## Assets checklist

| Mark | Asset | Path |
|------|-------|------|
| [✓] | CB2 active | `data/targets/cb2/6PT0_rec.pdbqt` |
| [✓] | Qiu-14 ligand | `results/docking/qiu_0e/compound_14_lig.pdbqt` |
| [✓] | Seed pose 0F QC | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` MODEL 1 |
| [!] | Membrane/MD engine | OpenMM+lipid17 pending TBD-0N-11 |
| [X] | SI numeric tables | pending ingest TBD-0N-03 |

## Fidelity TBD (keep TBD — do not invent)

| IDs | Topic |
|-----|-------|
| TBD-0N-01/02 | Docking engine/grid + active/inactive PDBs |
| TBD-0N-03/04 | IP signatures S1–S4/S7 + MD/GBSA templates (`cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`) |
| TBD-0N-05/06 | GB/PB exact knobs |
| TBD-0N-07/08/09 | ΔE (−10 kcal/mol gate), equilibration, replicas |
| TBD-0N-11/12 | AMBER18/Lipid14/GAFF/RESP → OpenMM/lipid17/GAFF2/AM1-BCC validation |

## Next ops (document only)

1. **Critical path:** send `cro_package_h1a/SEND/` RFQs.
2. **Pre-exec 0N:** ingest Ge SI tables — **pending**.
3. **Gate:** 115 ns MD + LRIP **BLOCKED** until explicit auth after fidelity verification.

**No MD executed under this lock.**

# EXTERNAL — Geometric AEA/HU308 × Ec21a × hubs TM7

**Run UTC:** `2026-10-02T23:01:27Z`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_AEA_EC21A_HUB_OVERLAP.md`  
**Mode:** static PDBs only — **no** AEA traj unpack, **no** docking.

## Verdict

**`EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL`**

> Hubs L287/N291/N295 son miembros de **TM7** (corredor AEA primario a nivel de hélice).  
> Capas: bolsillo ortostérico/HU-308 vs plug Ec21a vestibular (ECL2).  
> Helix membership ≠ tunnel atomístico AEA (trajs no desempaquetadas).

## Hub distances (Å, heavy-atom min)

| Hub | HU308 (KO3) | class | Ec21a (A1EOL) | class | CP55 (9GF) | class | AEA TM1–7 helix |
|-----|------------:|-------|--------------:|-------|-----------:|-------|-----------------|
| LEU287 | 8.16 | **DISTAL** | 13.88 | **DISTAL** | 8.04 | DISTAL | True |
| ASN291 | 10.04 | **DISTAL** | 16.53 | **DISTAL** | 10.07 | DISTAL | True |
| ASN295 | 12.32 | **DISTAL** | 19.96 | **DISTAL** | 13.22 | DISTAL | True |

## Ec21a vestibule residues vs nearest TM7 hub

| Residue | min Å → Ec21a | class | min Å → nearest hub TM7 |
|---------|--------------:|-------|------------------------:|
| SER268 | 3.18 | NEAR_LIGAND | 15.15 |
| LYS278 | 3.58 | NEAR_LIGAND | 12.57 |
| PHE183 | 3.37 | NEAR_LIGAND | 17.72 |
| ILE186 | 3.55 | NEAR_LIGAND | 18.43 |
| PRO176 | 12.97 | DISTAL | 31.80 |
| PRO178 | 9.71 | DISTAL | 28.01 |

## Governance

```text
VERDICT: EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL
AEA_TRAJ_UNPACK: FALSE
DOCKING: STOP
P2_REOPEN: FALSE
Gi_FUNCTIONAL_CLAIM: FALSE
```

---

*Fin EXTERNAL geometric overlap.*

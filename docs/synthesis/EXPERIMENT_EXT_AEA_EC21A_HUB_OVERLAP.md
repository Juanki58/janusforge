# Experiment — EXTERNAL: Geometric AEA/HU308 × Ec21a plug × hubs TM7

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — static PDB/coords only.  
**Scope:** **`EXTERNAL_AEA_EC21A_HUB_OVERLAP`** — intersección geométrica de corredores AEA (TM1–7 + TM5–6 CB2 lit.), sitio HU-308 (8GUS), plug Ec21a (9U7L), hubs TM7 L287/N291/N295.  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Distancias mínimas heavy-atom / Cα en PDBs locales | Docking / de novo / unpack AEA 85 GB |
| Helix-level membership TM1–7 / TM5–6 (rangos locked) | Inventar residuos AEA no publicados en repo |
| Veredicto `EXT_AEA_EC21A_HUB_OVERLAP_*` | Gi efficacy; P2 reopen; DEER |

```text
TRAJECTORIES_AEA = NOT_UNPACKED
P2 = CLOSED unchanged
docking = STOP
EXT_AEA_EC21A_HUB_OVERLAP_* = NEW
```

**Pregunta discriminante:**

> ¿Los hubs TM7 caen en la vecindad geométrica del corredor de entrada AEA / bolsillo HU-308 **y/o** del plug Ec21a, o son capas espacialmente separadas en estructuras estáticas?

---

## Locked objects

| Object | Source | Residues / ligands |
|--------|--------|--------------------|
| Hubs TM7 | dual-test | L287, N291, N295 |
| HU-308 complex | PDB **8GUS** (local) | ligand KO3 + CB2 chain R |
| Ec21a + CP55 | PDB **9U7L** CIF→chain R | A1EOL (Ec21a), 9GF (CP55) |
| Ec21a vestibule residues (Wang lit.) | atlas / switch map | S268, K278, F183, I186, P176, P178 |
| AEA primary path | P4-lite CLOSED_IN_LIT | helix shells **TM1∪TM7** (ranges below) |
| AEA alternate CB2 | P4-lite | helix shells **TM5∪TM6** |

### TM residue ranges (UniProt P34972; locked a priori, helix-level)

| Helix | Inclusive resid |
|-------|-----------------|
| TM1 | 27–51 |
| TM5 | 185–217 |
| TM6 | 230–260 |
| TM7 | 270–300 |

**Non-claim:** helix membership ≠ published atomistic AEA tunnel residue list (trajs not unpacked).

### Distance thresholds (locked)

| Class | Criterion |
|-------|-----------|
| `NEAR_LIGAND` | min heavy-atom hub↔ligand < **5.0 Å** |
| `SHELL` | min heavy-atom hub↔ligand < **8.0 Å** |
| `DISTAL` | ≥ 8.0 Å |
| `HELIX_MEMBER` | hub resid ∈ helix range |

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_AEA_EC21A_HUB_OVERLAP_STRONG`** | ≥2 hubs NEAR_LIGAND to HU308 **and** ≥1 hub NEAR/SHELL to Ec21a |
| **`EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL`** | Hubs HELIX_MEMBER of TM7/AEA-primary **and** Ec21a vestibule DISTAL from hubs (layered) **or** mixed NEAR/DISTAL |
| **`EXT_AEA_EC21A_HUB_OVERLAP_ABSENT`** | All hubs DISTAL to both ligands and not useful helix members |
| **`EXT_AEA_EC21A_HUB_OVERLAP_INDETERMINATE`** | PDBs missing / unreadable |

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_AEA_EC21A_HUB_OVERLAP.md` |
| Report | `results/network_core/ext_aea_ec21a_hub_overlap.md` |
| JSON | `results/network_core/ext_aea_ec21a_hub_overlap.json` |
| Script | `scripts/network_core/ext_aea_ec21a_hub_overlap.py` |

---

*Fin pre-registro. Static coords only.*

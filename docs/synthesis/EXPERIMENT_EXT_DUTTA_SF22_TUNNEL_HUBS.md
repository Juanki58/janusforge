# Experiment — EXTERNAL: Dutta Supp Fig. 22 tunnel membership vs hubs

**Fecha pre-registro:** 2026-10-02  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION` — SI figure + main-text only.  
**Scope:** **`EXTERNAL_DUTTA_SF22_TUNNEL_HUBS`** — ¿los seis hubs caen en tunnels/pipelines de Supp Fig. 22 (CB2)?  
**PI authorization:** YES (blanket advance).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Lectura SI caption + main text pipelines | Inventar lista de residuos por tunnel desde la figura |
| Helix-level inference **labeled as weak** | Tratar SF22 como Gate-1 / P2 CONVERGENT |
| Veredicto `EXT_DUTTA_SF22_TUNNEL_HUB_*` | Unpack trajs; docking |

```text
P2 = CLOSED (INSUFFICIENT_SAMPLING) unchanged
EXT_P4LITE claim2 (pipelines CB2 no state-stratified) = prior CLOSED_IN_LIT
EXT_DUTTA_SF22_TUNNEL_HUB_* = NEW
```

**Pregunta discriminante:**

> ¿Hay membership residue-level de hubs en los six tunnels de SF22, o solo afirmación cualitativa EC→IC sin roster?

---

## Source set

| Source | Path / DOI |
|--------|------------|
| Dutta & Shukla 2023 | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| SI PDF | `results/network_core/_raw_downloads/42003_2023_4868_MOESM1_ESM.pdf` |
| Hubs | ALA79, ALA83, LEU287, ASN291, ASN295, ARG302 |

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_DUTTA_SF22_TUNNEL_HUB_MEMBERSHIP`** | SI/text da lista de residuos por tunnel que incluye ≥3 hubs |
| **`EXT_DUTTA_SF22_TUNNEL_HUB_QUALITATIVE_ONLY`** | Pipelines EC→IC / no state split CLOSED_IN_LIT; **sin** roster residue-level → hubs membership INDETERMINATE |
| **`EXT_DUTTA_SF22_TUNNEL_HUB_INDETERMINATE`** | SI no disponible |

**Prefer QUALITATIVE_ONLY / INDETERMINATE over inventing residues from a figure.**

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_DUTTA_SF22_TUNNEL_HUBS.md` |
| Report | `results/network_core/ext_dutta_sf22_tunnel_hubs.md` |
| JSON | `results/network_core/ext_dutta_sf22_tunnel_hubs.json` |
| Script | `scripts/network_core/ext_dutta_sf22_tunnel_hubs.py` |

---

*Fin pre-registro.*

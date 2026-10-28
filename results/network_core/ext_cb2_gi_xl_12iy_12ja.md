# EXTERNAL — Mnpotra 2014 XL pairs on 12IY / 12JA (protocol extension)

**Run UTC:** `2026-10-19T13:33:49Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md`
**Protocol:** identical to `EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014` (Cα–Cα windows locked).

## Verdict

**Primary:** `EXT_CB2_GI_XL_12IY_12JA_PARTIAL`

> 12JA (Gi complex): all three XL pairs WITHIN Mnpotra windows; 12IY is locally refined receptor-only (no Gi) — XL intermolecular map N/A for 12IY

## Plain-language answer

**12JA** (CB2–Gi + '1029) se evalúa con las tres parejas XL de Mnpotra 2014. **12IY** es un depósito de refinamiento local **solo receptor** (sin Gi) → el mapa intermolecular CB2↔Gi **no aplica** (`N/A_NO_GI`). Apéndice **12IZ** = complejo Gi de la misma serie '5249. Compatibilidad geométrica ≠ claim funcional Gi ni hubs.

## Locked XL windows (unchanged)

| Pair | Chemistry | Cα–Cα window |
|------|-----------|--------------|
| C134–C351 | HgCl2 | 7–10 Å |
| K245–K349 | DSS | ≤24.2 Å |
| K215–K317 | DSS | ≤24.2 Å |

## PI panel (12IY, 12JA)

| Structure | Role | C134–C351 | K245–K349 | K215–K317 | Call |
|-----------|------|-----------|-----------|-----------|------|
| 12IY | Locally refined CB2 + agonist '5249 (Rachman 202… | — / `N/A_NO_GI` | — / `N/A_NO_GI` | — / `N/A_NO_GI` | `NO_GI_COMPLEX` |
| 12JA | CB2–Gi + agonist '1029 (Rachman 2026)… | 7.87 / `WITHIN` | 16.14 / `WITHIN` | 23.34 / `WITHIN` | `ALL_WITHIN` |

## Appendix — 12IZ (Gi counterpart of '5249 series)

| Structure | C134–C351 | K245–K349 | K215–K317 | Call |
|-----------|-----------|-----------|-----------|------|
| 12IZ | 7.89 / `WITHIN` | 15.62 / `WITHIN` | 21.61 / `WITHIN` | `ALL_WITHIN` |

Pro139 pocket min (12JA): 6.69 Å → ILE343:A (MD registering; not XL).
Pro139 pocket min (12IZ): 6.30 Å → ILE343:A.

## Epistemic limits

- XL = intermolecular CB2↔Gi proximity, not intramolecular CB2 distances
- Geometric compatibility ≠ Gi functional proof; ≠ Janusforge hubs; ≠ P3
- 12IY receptor-only deposit does not support XL mapping (honest N/A_NO_GI)
- P2 not reopened; P5 not advanced; no docking; no Tier B MD

## Governance

```text
VERDICT: EXT_CB2_GI_XL_12IY_12JA_PARTIAL
PROTOCOL: SAME_AS_EXT_CB2_GI_CROSSLINK_2014
XL_MEASURES: INTERMOLECULAR_CB2_Gi_PROXIMITY
HUB_CLAIM: FALSE
P3_CLAIM: FALSE
P2_REOPEN: FALSE
P5_ADVANCE: FALSE
DOCKING: FALSE
TIER_B_MD: FALSE
```

## References

1. Mnpotra et al. *JBC* 2014 — [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916)
2. Rachman et al. *J. Med. Chem.* 2026 — [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PDB **12IY**, **12JA**, **12IZ**
3. Parent compare — [`ext_cb2_gi_crosslink_2014.md`](ext_cb2_gi_crosslink_2014.md)

---

*Fin. EXTERNAL discrimination-only.*

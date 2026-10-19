# EXTERNAL — Mnpotra 2014 CB2-Gi crosslinking vs modern complex structures

**Run UTC:** `2026-10-19T13:26:08Z`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md`
**Scope:** EXTERNAL structural comparison only — **intermolecular proximity**, not intramolecular CB2 map.

## Verdict

**Primary:** `EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED`

> All three XL pairs WITHIN in >=70% of primary cryo/X-ray CB2-Gi panel

## Plain-language answer

Las tres parejas de entrecruzamiento CB2<->Gai1 de Mnpotra 2014 se contrastan con estructuras modernas CB2-Gi (panel cryo/X-ray local). Lo que se mide es distancia Ca-Ca **entre receptor y Gi**, bajo ventanas quimicas del paper (HgCl2 Cys-Cys ~7-10 A; DSS Lys-Lys <=24.2 A). Esto **no** demuestra hubs Janusforge ni cierra P3.

## Bibliographic note (locked)

| Field | Value |
|-------|-------|
| Paper | Mnpotra et al., *J. Biol. Chem.* 2014 |
| DOI | [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916) |
| PMID | 24855641 |
| PMC | [PMC4106340](https://pmc.ncbi.nlm.nih.gov/articles/PMC4106340/) |
| What XL measures | Intermolecular CB2<->Gai1 proximity compatible with crosslinker geometry |
| What XL does **not** measure | Intramolecular CB2 distances; allosteric path; hub identity |

### Experimental pairs (sequence numbers authoritative)

| Pair | CB2 | Gai1 | Chemistry | Ca-Ca window (paper) |
|------|-----|------|-----------|----------------------|
| C134-C351 | C3.53/C3.54(134) | Cys351 a5 i-3 | HgCl2 | 7-10 A |
| K245-K349 | K6.35(245) | Lys349 a5 i-5 | DSS | <=24.2 A |
| K215-K317 | K5.64(215) | Lys317 a4b6 | DSS | <=24.2 A |

Ballesteros label for Cys134 is **C3.53 in the abstract** and **C3.54 in the Results body** — sequence number **134** is used for mapping. Pro139-Gai hydrophobic pocket is an **MD registering contact**, reported separately, not as XL.

## Primary panel (cryo/X-ray CB2-Gi)

| Structure | C134-C351 (A / call) | K245-K349 (A / call) | K215-K317 (A / call) | Structure call |
|-----------|----------------------|----------------------|----------------------|----------------|
| 6PT0 | 8.25 / `WITHIN` | 16.26 / `WITHIN` | 21.93 / `WITHIN` | `ALL_WITHIN` |
| 6KPF | 7.97 / `WITHIN` | 15.73 / `WITHIN` | 21.62 / `WITHIN` | `ALL_WITHIN` |
| 8GUR | 7.83 / `WITHIN` | 15.51 / `WITHIN` | 22.09 / `WITHIN` | `ALL_WITHIN` |
| 8GUS | 7.85 / `WITHIN` | 15.53 / `WITHIN` | 21.99 / `WITHIN` | `ALL_WITHIN` |
| 8GUQ | 8.28 / `WITHIN` | 16.17 / `WITHIN` | 22.07 / `WITHIN` | `ALL_WITHIN` |
| 8GUT | 7.80 / `WITHIN` | 15.48 / `WITHIN` | 21.73 / `WITHIN` | `ALL_WITHIN` |
| 8X3L | 7.65 / `WITHIN` | 15.77 / `WITHIN` | 23.20 / `WITHIN` | `ALL_WITHIN` |

### Pair tallies (primary panel)

| Pair | WITHIN | BORDERLINE | OUT | MISSING | WITHIN frac |
|------|--------|------------|-----|---------|-------------|
| C134_C351 | 7 | 0 | 0 | 0 | 1.00 |
| K245_K349 | 7 | 0 | 0 | 0 | 1.00 |
| K215_K317 | 7 | 0 | 0 | 0 | 1.00 |

## Pro139 pocket (MD registering; not XL)

| Structure | min Ca-Ca to pocket (A) | nearest Gai residue |
|-----------|-------------------------|---------------------|
| 6PT0 | 6.36 | ILE343:A |
| 6KPF | 6.17 | ILE343:A |
| 8GUR | 6.60 | ILE343:A |
| 8GUS | 6.39 | ILE343:A |
| 8GUQ | 5.95 | ILE343:A |
| 8GUT | 6.25 | ILE343:A |
| 8X3L | 6.56 | ILE343:A |

## Secondary / negative controls

| Structure | Role | Result |
|-----------|------|--------|
| 9U7L | PAM complex; Gi absent in local file | `N/A_NO_GI` (expected) |
| 5ZTY | inactive crystal — no Gi | `N/A_NO_GI` (expected) |
| 6KPC | active crystal — no Gi | `N/A_NO_GI` (expected) |
| Abrol_Gi_Empty | Abrol/Heo avg frame Gi-Empty (MD model, not cryo) | `NO_GAI_MAP` — single chain X, fused numbering; Gai XL sites not identifiable without invented offset |
| Abrol_Gi_GDP | Abrol/Heo avg frame Gi-GDP (MD model, not cryo) | `NO_GAI_MAP` — same fused-chain limit; left INDETERMINATE (fail-closed) |

## Epistemic limits (locked)

- XL = intermolecular CB2<->Gi proximity under crosslinking chemistry, not intramolecular CB2 distances
- Geometric compatibility != proof of Janusforge hubs or P3 effector mechanism
- Pro139 pocket proximity is MD registering contact from Mnpotra, not an experimental XL
- Abrol avg frames are secondary (MD models), not primary cryo evidence
- P2 not reopened; P5 not advanced; no docking/de novo; no Tier B MD

## Governance

```text
VERDICT: EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED
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
2. Local structures — [`CB2_STRUCTURE_ATLAS.md`](../../docs/synthesis/CB2_STRUCTURE_ATLAS.md)
3. Abrol avg frames — Heo & Abrol [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100) (secondary only)

---

*Fin. EXTERNAL discrimination-only.*

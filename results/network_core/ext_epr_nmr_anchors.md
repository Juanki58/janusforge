# EXTERNAL — EPR/NMR anchors checklist vs repo predictions

**Run UTC:** `2026-09-22T05:00:00Z` (documentation checklist; no MD)  
**Branch:** `feat/cb2-hubs-functional-topology-test`  
**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_EPR_NMR_ANCHORS.md`  
**Scope:** EXTERNAL qualitative anchors only — **no restraints**, **no Gi claim**, **P2 unchanged**.

## Verdict

**Primary:** `EXT_EPR_NMR_ANCHORS_PARTIAL_AGREE`  
**Secondary:** `DEER_CB2 = ABSENT`

> ICL3 flexibility and TM7 order/ligand-sensitivity agree directionally with Phase F/G + static hubs.  
> A270C (EC tip TM6) has **no** prior Phase F/G site prediction.  
> No DEER distance map exists to restrain MD.

## Plain-language answer

Las anclas CW-EPR / DNP-NMR **no** contradicen el repo: ICL3 se ve flexible (EPR + NMR) y el repo no la trata como hub rígido; TM7 (M293) se ve ordenado y ligando-sensible, cerca de hubs estáticos NPxxY. Falta predicción propia para A270 EC. **No hay DEER CB2** → no inventar restraints.

## Site checklist

| Site | Lit. observation | Repo prior | Call |
|------|------------------|------------|------|
| ICL3 center (≈H217–G225; EPR) | High label mobility (C2/C1 ↑) | Phase F/G: IC TM3–TM6 opens inactive→active (5ZTY ~10.3 Å → 6PT0/6KPF ~15 Å); 5ZTY construct removes IL3; **no hub in ICL3 core**; hubs inventory ≠ ICL3 skeleton | **AGREE** (flex / non-hub) |
| A270C TM6 EC tip (EPR) | More mobile with CP-55,940 vs SR-144,528 | Phase F/G fingerprint = IC + toggle W258 + ECL2 Phe — **A270 not in prior feature set** | **NO_PRIOR_PRED** |
| M237 ICL3 (DNP-NMR) | Broad conformational space across ligands | Same ICL3 flex prior as above; soft landmark STABLE is **contact-map** geometric, not ICL3 rigidity claim | **AGREE** |
| M293 TM7 (DNP-NMR) | More restricted; ligand-sensitive; near NPxxY | Hubs LEU287 / ASN291 / ASN295 on TM7; `STATIC_BOTTLENECKS`; `EXT_HUBS_IN_LIGACNTOP` | **AGREE** |
| DEER IL3 / TM6 (proposed) | **Not published** as CB2 distance map | — | **ABSENT_RESTRAINT** |

### Hub proximity (UniProt P34972; inventory only)

| Anchor residue | Nearest frozen hub(s) | Note |
|----------------|----------------------|------|
| M237 (ICL3) | ARG302 (H8) via published LigACNtop edge ARG302↔THR246 neighborhood | ICL3 itself **not** a hub |
| M293 (TM7) | ASN291 / ASN295 / LEU287 | Direct TM7 hub corridor |
| A270 (TM6 EC) | None of the six hubs | EC tip outside hub set |
| G225 / IL3 center | None of the six hubs | Loop |

## Phase F/G numbers used (already in repo)

| PDB | TM3–TM6 IC (Å) | Role |
|-----|----------------|------|
| 5ZTY | 10.28 | inactive |
| 6KPF | 14.80 | active |
| 6PT0 | 15.33 | active |
| 8GUR (Phase G blind) | ~active manifold | GENERALIZES |

Sources: `results/conformational/fase_f_conformational_fingerprint.md`, `fase_g_generalization_report.md`.

## Where future DEER would discriminate (conditional)

If own sampling existed and A/B/C were reopenable: DEER pairs spanning **IC TM3–TM6** (activation opening) vs **ICL3-local** mobility would test whether geometric `RED_ESTABLE`-like contact maps coexist with large ICL3 fluctuations — a discrimination Phase F/G soft maps **cannot** settle alone. **Not authorized here; no distances invented.**

## Governance

```text
VERDICT: EXT_EPR_NMR_ANCHORS_PARTIAL_AGREE
DEER_CB2: ABSENT
RESTRAINTS_ADDED: FALSE
P2_REOPEN: FALSE
Gi_CLAIM: FALSE
```

## References

1. Yeliseev et al. *BBA Biomembranes* 2021 — [10.1016/j.bbamem.2021.183603](https://doi.org/10.1016/j.bbamem.2021.183603)  
2. Yeliseev et al. *Sci. Rep.* 2021 (cholesterol context) — [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6)  
3. DNP-MAS NMR *ACS Omega* 2023 — [10.1021/acsomega.3c04681](https://doi.org/10.1021/acsomega.3c04681)  

---

*Fin checklist. EXTERNAL only.*

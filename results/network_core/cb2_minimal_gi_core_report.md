# CB2 → Gαi minimal communication-core reanalysis

**Branch:** `feat/cb2-minimal-gi-core-reanalysis`  
**Access date:** 2026-08-20T12:15:33Z  
**FINAL_VERDICT:** `INDETERMINATE`  
**CB1_COMPARISON:** `INDETERMINATE`

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
CONTRACT_v1.0: ARCHIVED_HISTORICAL
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
```

---

## 0. Recovery / provenance / reproducibility (LEAD)

Interpretability of any CB2→Gi “minimal core” depends on this section. **Recovery is incomplete.**

### Datasets recovered

See `data_audit.md` / `data_audit.json` for full checksums. Headline:

| File | Bytes | SHA256 (prefix) | Maps to |
|------|------:|-----------------|--------|
| `41467_2025_60003_MOESM1_ESM.pdf` | 4 670 882 | `4ec13634…` | SI PDF |
| `41467_2025_60003_MOESM2_ESM.pdf` | 34 257 | `2937da83…` | Description of Additional Supplementary Files (Supp Data 1–4) |
| `41467_2025_60003_MOESM3_ESM.xlsx` | 56 748 | `f296cb13…` | Supp Data 1 |
| `41467_2025_60003_MOESM4_ESM.xlsx` | 5 133 984 | `04a7d0c0…` | Supp Data 2 contacts |
| `41467_2025_60003_MOESM5_ESM.xlsx` | 970 304 | `ff53ec7b…` | Supp Data 3 degeneracy |
| Zenodo `prefcoup_cb2r-v.1.0.0.zip` | 4 513 | `e1c6d030…` | code stub release |
| GitHub notebooks (4) | see audit | see audit | analysis logic |
| PMC + GPCRmd HTML + API trees | see audit | see audit | identity / mapping |

### Provenance

- **[PRIMARY_LITERATURE]** Morales-Pastor 2025 DOI `10.1038/s41467-025-60003-0`, PMID `40500255`; GPCRmd/1540; GitHub `GPCRmd/prefcoup_cb2r`.
- **[PRIMARY_LITERATURE]** Dutta & Shukla 2023 DOI `10.1038/s42003-023-04868-1` (MSM/VAMPnets; **not** Li 2023); Box ID `jzooa0o27z1w9ha0h6va3i51ir7l38j4`.
- Access date UTC: `2026-08-20T12:15:33Z`; provenance recovery update same day.
- Official SI inventory (MOESM2): **SI + Supplementary Data 1–4 only**. Prior **MOESM6** chase **STRICKEN**.
- Sink Set T: **EXTRACTED** — Arg131(3×50), Asp240(6×30), Ser303(8×47), Ser69(2×39) from Methods.
- See `provenance_recovery_log.md`.

### Reproduced vs not

- **Reproduced (partial):** load Supp Data 1–3; MOESM2 PDF; Sink Set T from Methods; confirm WT LigACN degeneracy object (100×100, 117 positive edges); ligand node `8D0:1` with neighbors SER:285, PHE:87; descriptive centrality on published matrix.
- **Not reproduced:** trajectory-level ACN rebuild; local Supp Data 4 bytes; CB1 comparable LigACN; Box MSM / GPCRmd traj binaries (ENLACE_REGISTRADO only).

**[INDETERMINATE]** Sink Set T recovered; without traj-level replication a minimal-core claim would still be over-claiming → `BLOCKED_PENDING_PROVENANCE`.

---

## 1. Exact question

Can the CB2 Gαi-associated communication network be reduced to a small node set robust to node removal? Secondary: is that set architecturally distinct in CB1?

## 2. Primary sources

Morales-Pastor 2025 (ACN/LigACN/mutagenesis); Dutta & Shukla 2023 (MSM/VAMPnets for CB1/CB2 landscape — comparison substrate only if graph-comparable objects exist).

## 3. Dataset + checksums

See §0 and `data_audit.json`.

## 4. Reconstruction method

Pre-registered in `MINIMAL_CORE_REANALYSIS_PROTOCOL.md`. Script: `scripts/network/reconstruct_cb2_minimal_gi_core.py` — fail-closed; builds descriptive graph from WT degeneracy only; **does not** execute candidate-core search when T missing.

## 5. Node / edge definition

Nodes/edges = labels and positive degeneracy weights in published `WT_degeneracy` (Supp Data 3). No residues added.

## 6. Metrics

Pre-registered list. Computed descriptively only (`cb2_network_metrics.json`). Primary paper metric (degeneracy/transmission) preserved as edge weight.

Status: `DESCRIPTIVE_ONLY`.  
S proxy: `['8D0:1', 'PHE:87', 'SER:285']`.  
T: **unrecovered** → LOO / core search **NOT_EXECUTED**.

## 7. Node-removal results

**[INDETERMINATE]** Not executed (blocker: traj/Box not local; Sink Set T now EXTRACTED).

## 8. Candidate core

`cb2_candidate_core.json`: `candidate_core = null`. No CORE_FOUND claim.

## 9. Robustness

Not applicable beyond confirming 36 degeneracy sheets exist on disk; replica-level LOO not run (would require unjustified T and/or traj rebuild).

## 10. CB1 comparison

`CB1_COMPARISON = INDETERMINATE` (`cb1_comparison.json`). No CB1 LigACN graph recovered; CB2 core search not closed with CORE_FOUND/NETWORK_DISTRIBUTED.

## 11. Limitations

MOESM2 recovered; Sink Set T EXTRACTED; MOESM6 chase stricken. Remaining: no local GPCRmd traj / Box MSM binaries; Supp Data 4 bytes not local; Zenodo zip too small to replace author private `data/` trees.

## 12. Literature conflicts (preserved open)

**[CONTRADICTORY_EVIDENCE]** Project prior: Phase G GENERALIZES / H INDETERMINATE / micronetwork INDETERMINATE; literature distributed LigACN not reducible to Trp258. Not harmonized here.

## 13. Final verdict

**`FINAL_VERDICT = INDETERMINATE`**

Reason: Sink Set T is EXTRACTED, but traj replication / Box MSM / CB1 graph remain unavailable locally (`BLOCKED_PENDING_PROVENANCE`). Descriptive inspection of the published WT LigACN object is consistent with a **non-singleton** transmission network **[SUPPORTED_INTERPRETATION / PRIMARY_LITERATURE]** but is **not** sufficient under locked rules to assign `NETWORK_DISTRIBUTED` or `CORE_FOUND`.

**STOP.** No Phase I. No molecule suggestions. Human scientific review next.

# Qiu 0J — Visual QC of best CB2 poses (vs 0G/0H)

> **Scope:** visual confirmation of **existing** best poses (MODEL 1) only. No re-docking; no Vina; no PDBQT / receptor edits; no SAR / pharmacological claims.
>
> **Date:** 2026-08-12
>
> **User path:** 0I → **visual QC (0J)** → validation decision (dual CB1 / MD / wet / stop). **No MD. No dual-CB1 in this step.**
>
> **Upstream (read-only):** [`qiu_0h_pose_audit.md`](qiu_0h_pose_audit.md) · [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md) · [`qiu_0i_evidence_matrix.md`](qiu_0i_evidence_matrix.md) · [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md)
>
> **Script (reproducible snapshots):** `scripts/generate_qiu_0j_visual_qc.py`
>
> **Artifacts:** [`qiu_0j_visual_qc/`](qiu_0j_visual_qc/)

---

## Methods

### Poses inspected (strict)

| Set | Path | MODEL |
|-----|------|-------|
| Qiu 14 / 15 / 20 / 24 | `results/docking/qiu_0f/compound_{N}_cb2_out.pdbqt` | **1** (also lowest Vina REMARK among written models) |
| D2_20 / D2_06 / D2_22 | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | **1** |
| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` chain R | — |

No new docking calculations. Snapshots are viewing artifacts only.

### How viewed

1. **Janusforge Visor** available at `http://127.0.0.1:8765` (`app/main.py` / FastAPI + 3Dmol.js) — health OK during session; used as the project viewer for interactive inspection of the same PDBQT paths.
2. **Reproducible static evidence** via `scripts/generate_qiu_0j_visual_qc.py`:
   - Per-compound **XZ / XY** matplotlib projections with pocket heavy atoms (≤11 Å), region residues, and feature centroids.
   - Overlay PNGs for 14↔20, 14/15/20↔24, D2 canonical vs Qiu 14, D2_22 feature_swap.
   - Interactive **3Dmol.js HTML** per compound (feature spheres + TYR25 sticks) under `qiu_0j_visual_qc/`.
3. **Visual read** of the PNG overlays/panels (primary checklist evidence). Coordinate axes / TYR25 distances cross-checked against 0H metrics (observation layer).

### Epistemic rules

| Label | Meaning in 0J |
|-------|----------------|
| **Observación** | What is visible / measurable in MODEL 1 coordinates and snapshots |
| **Interpretación** | Structural orientation notes only (occupation, rotation, feature map) — **not** activity |
| **H-bonds** | **Do not rescue.** 0H: 0 geometry-OK H-bonds for all 7 poses. Polar proximities remain proximities |

---

## Artifact index

| File | Role |
|------|------|
| [`qiu_0j_visual_qc/index.html`](qiu_0j_visual_qc/index.html) | Artifact index |
| [`qiu_0j_visual_qc/qiu_*_model1.png`](qiu_0j_visual_qc/) | Per-Qiu XZ/XY panels |
| [`qiu_0j_visual_qc/janus_d2_*_model1.png`](qiu_0j_visual_qc/) | Per-D2 XZ/XY panels |
| [`qiu_0j_visual_qc/*_model1.html`](qiu_0j_visual_qc/) | 3Dmol interactive views |
| [`qiu_0j_visual_qc/overlay_qiu_14_20_xz.png`](qiu_0j_visual_qc/overlay_qiu_14_20_xz.png) | 14 vs 20 occupation |
| [`qiu_0j_visual_qc/overlay_qiu_14_15_20_24_xz.png`](qiu_0j_visual_qc/overlay_qiu_14_15_20_24_xz.png) | N1-het rotation vs 14/15/20 |
| [`qiu_0j_visual_qc/overlay_d2_canonical_vs_qiu14_xz.png`](qiu_0j_visual_qc/overlay_d2_canonical_vs_qiu14_xz.png) | D2_20/06 vs Qiu Ad/N1-het map |
| [`qiu_0j_visual_qc/overlay_d2_22_feature_swap_xz.png`](qiu_0j_visual_qc/overlay_d2_22_feature_swap_xz.png) | D2_22 swap vs Qiu/D2_20 |
| [`qiu_0j_visual_qc/qiu_0j_visual_qc_metrics.json`](qiu_0j_visual_qc/qiu_0j_visual_qc_metrics.json) | Feature centroids / axes (observation) |

---

## Checklist (visual QC)

| # | Claim (from 0G/0H) | Status | Visual rationale (Observación) |
|---|--------------------|--------|--------------------------------|
| 1 | Qiu **14/20**: similar occupation | **CONFIRMED** | Overlay XZ: atom clouds nearly coincident; Ad centroids overlap (~94.3–94.4, z~121.7–121.8); N1-het both **+z** (~100.2–100.3, z~129). Δcentroid 14↔20 tiny (0H/metrics). |
| 2 | Qiu **15**: TYR25 proximity/contact | **CONFIRMED** | MODEL 1 panel: N1-*m*-morpholine extends toward TYR25 (red square). min heavy **3.021 Å** ≤ 4.0 Å contact cutoff. **Not** a geometry-OK H-bond (0H: polar proximity O···TYR25 O). |
| 3 | Qiu **24**: N1-heterocycle rotation (+x vs 14/15/20) | **CONFIRMED** | Overlay: Ad still −x cluster with 14/15/20; N1-het of 24 at ~**(103.0, 123.8)** vs 14/15/20 at z~129–131 / x~100. Dominant axis **+x** (vs **+z**). |
| 4 | D2_20 / D2_06: **canonical_like** vs Qiu Ad/N1-het map | **CONFIRMED** | Overlay vs Qiu 14: `benzoyl_aryl` co-localizes with Ad (−x / low-z); `n1_benzyl_aryl` with N1-het (+z). Axes: Bz **−x**, NBn **+z** (matches 0H). |
| 5 | D2_22: **feature_swap** orientation | **CONFIRMED** | Overlay: D2_22 `n1_benzyl_aryl` in Ad/Bz pocket; `benzoyl_aryl` in N1-het pocket — reversed vs D2_20 / Qiu 14. Axes: Bz **+z**, NBn **+y**. |
| 6 | No geometry-OK H-bonds reinterpreted as present | **CONFIRMED** | Visual QC does not draw H-bond dashed lines. Metrics retain `h0_hbonds_geometry_ok = 0`. Polar proximities (e.g. THR114/TYR25) not relabeled as H-bonds. |

### Per-compound snapshot notes

| Compound | MODEL | Vina REMARK (score-only) | Key visual note | Status |
|----------|-------|--------------------------|-----------------|--------|
| Qiu_14 | 1 | −9.919 | Ad −x; N1-het +z; TYR25 **outside** 4 Å (5.041) | occupation OK |
| Qiu_15 | 1 | −11.201 | Same Ad/−x map; N1-het higher +z; TYR25 **in** shell (3.021) | TYR25 contact OK |
| Qiu_20 | 1 | −9.986 | Near-superposable to 14 | similar to 14 OK |
| Qiu_24 | 1 | −11.606 | Ad −x retained; N1-morph **+x** rotation | rotation OK |
| JANUS_D2_20 | 1 | −11.656 | Bz↔Ad / NBn↔N1-het spatial pairing | canonical_like OK |
| JANUS_D2_06 | 1 | −12.03 | Same pairing as D2_20 | canonical_like OK |
| JANUS_D2_22 | 1 | −12.35 | Features swapped vs Qiu/D2_20 map; mid co-occupation only | feature_swap OK |

*Vina numbers are docking scores only — not affinity.*

---

## Discrepancies vs 0G / 0H text

| Topic | Finding |
|-------|---------|
| Orientations / axes | **No discrepancy.** Visual axes match 0H summary (Ad −x; N1-het +z except 24 +x; D2_20/06 canonical; D2_22 swap). |
| Qiu 15 TYR25 | **Aligned.** Contact ≤4.0 Å visible as proximity; 0G/0H wording “contact / shell” is correct. Must **not** be read as H-bond. |
| Qiu 14/20 similarity | **Aligned.** Overlay confirms near-identical occupation claimed in 0G Jaccard / 0H. |
| Qiu 24 rotation | **Aligned.** Clear +x displacement of N1-het vs 14/15/20 while Ad stays put. |
| H-bonds | **Aligned / enforced.** 0H “none geometry-OK” stands; 0J does not elevate polar proximities. |
| Chemotype mismatch | **Preserved observation.** Visual feature map is spatial only (Ad≠benzoyl chemically). |
| 15/20 log↔PDBQT | **Out of visual scope** (modes not in PDBQT). Unchanged from 0F/0I; MODEL 1 of written poses used. |
| Interactive browser capture | Static PNG/HTML + Visor health used; automated browser MCP tab session was flaky — does not change geometric conclusions from projections + metrics. |

---

## Verdict

All six checklist items are **CONFIRMED** against MODEL 1 snapshots and 0H coordinates. No contradiction that would reopen docking or force a NEEDS REVIEW on pose identity/orientation.

**`0J = PASS`**

*(Optional soft note — not a fail: polar O···TYR25/THR114 remain **proximities**, not H-bonds; chemotype mismatch and D2_22 swap remain documented observations from 0H/0I.)*

---

## Closing — next validation decision (user)

0J does **not** start the next step. Choose explicitly:

1. **Dual CB1** (5TGZ) docking/comparison — only if authorized  
2. **MD / ensemble** on selected written poses — only if authorized  
3. **Wet / binding assay** planning — experimental validation  
4. **Stop / pivot** — no further compute on this branch  

No SAR. No pharmacological conclusion from visual co-occupation. Shared pocket occupation ≠ same pharmacophore ≠ same pharmacology.

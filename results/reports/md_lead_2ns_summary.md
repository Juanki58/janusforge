# MD 2 ns — JANUS_H1_02c vs Δ9-THCV on CB1 inactive (5TGZ)

> **Public report:** no SMILES, no coordinates. Trajectories / CSV / DCD / PDB stay local under `results/md/` (gitignored).  
> Script: [`scripts/run_md_openmm_lead.py`](../../scripts/run_md_openmm_lead.py) · plan: [`md_lead_plan.md`](md_lead_plan.md) · env: [`environments/environment-md.yml`](../../environments/environment-md.yml)

## Setup (executed)

| Item | Value |
|------|--------|
| Receptor | 5TGZ CB1 chimera, flavodoxin insert stripped (keep UniProt 99–306 + 332–414) |
| Ligands | JANUS_H1_02c, delta9-THCV (Vina MODEL 1 poses) |
| FF | Protein `amber14-all` + TIP3P; ligand **GAFF2** (`gaff-2.11` via OpenFF + openmmforcefields) |
| Box | Cubic TIP3P, padding ~1 nm, neutralize + **0.15 M NaCl** |
| Protocol | Min 5000 → NVT/NPT equil ~100 ps → **NPT production 2.0 ns**, 300 K, 1 atm, seed 42 |
| Platform | OpenMM **CUDA** (GTX 1060 6GB in Linux Docker; ~57–59 ns/day) |
| Wall time | **~1 h 49 min** for both ligands (incl. build/min/equil) |
| Frames | 200 / ligand (10 ps report interval over 2 ns) |

**Host note:** AmberTools is unavailable on win-64 conda-forge. Run used portable micromamba env `janus_md` inside Docker (`mambaorg/micromamba`) with GPU passthrough.

## Metrics (production)

| Metric | JANUS_H1_02c | delta9-THCV | Lead vs THCV |
|--------|-------------:|------------:|--------------|
| TM6 Cα RMSD mean ± sd (Å) | **0.83 ± 0.19** | 1.32 ± 0.24 | Lead quieter (~0.5 Å lower) |
| TM6 Cα RMSD final (Å) | 0.66 | 1.58 | Lead more settled |
| TM3–TM6 COM mean ± sd (Å) | 13.49 ± 0.25 | **12.57 ± 0.21** | THCV slightly tighter / lower mean |
| Phenolic H-bond persistence (%) | 55.5 | **100.0** | THCV more persistent |
| n(TM3 Cα) / n(TM6 Cα) | 36 / 38 | 36 / 38 | Same selection |

TM ranges (UniProt / GPCRdb): TM3 185–220; TM6 332–369. RMSD vs minimized frame 0 of each trajectory.

## Critical verdict — does the “ratchet” hold under thermal noise?

**Mixed / weak support. Do not claim a thermal ratchet from this run alone.**

1. **TM6 dynamics** favor the lead: lower mean and final Cα RMSD than THCV over 2 ns in the inactive well — consistent with a quieter TM6 when the 1′-methyl lead occupies the pose.
2. **TM3–TM6 separation** does **not** favor a more restricted lead: mean COM distance is *higher* for H1_02c (13.5 vs 12.6 Å) with comparable fluctuation. The lead is not “pinching” TM3–TM6 relative to THCV here.
3. **Phenolic H-bond** persistence is **worse** for the lead (55% vs 100% for THCV) under the flexible OH→protein acceptor criterion (3.5 Å). That undercuts a simple “locked phenol” ratchet story on this timescale.

**Bottom line:** short NPT MD in water suggests the lead keeps TM6 a bit quieter than THCV, but does **not** show a more restricted TM3–TM6 geometry or a more persistent phenolic contact. Geometric “ratchet vs THCV” remains a docking-era hypothesis, not a thermal-MD confirmation.

## Limitations (must read)

1. **No explicit membrane** — protein+ligand in TIP3P only; TM helices can breathe/deform unphysically vs bilayer MD.
2. **2 ns is short** — probes local stability of the docked inactive pose, not agonism, activation path, or Janus α.
3. **Vina pose ≠ bound ensemble** — starting coordinates are docking proxies.
4. **5TGZ chimera** (mutations + stripped flavodoxin; ICL3 gap) ≠ full native CB1.
5. Phenolic H-bond detection is geometry-only (any protein O/N acceptor); not residue-locked (e.g. S7.39).
6. Single seed (42); no replicate trajectories.

## Local artifacts (gitignored)

- Aggregate CSV: `results/md/janus_h1_02c_vs_thcv_5tgz.csv`
- Per ligand: `results/md/<id>/production.dcd`, `minimized.pdb`, `production.log`, `metrics_summary.json`, `frame_metrics.csv`

## Siguiente = membrane MD (A1+A3)

Escalón aprobado: **POPC explícita + 20 ns**, panel **H1_02c vs THCV vs THC**, go/no-go hacia ensayo in vitro u Opción D (URB447/Yin-Yang). Protocolo: [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md). Script: `scripts/run_md_openmm_membrane_lead.py`.

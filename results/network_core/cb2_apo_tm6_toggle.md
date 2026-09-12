# EXTERNAL fallback — CB2_APO TM6/toggle (filename inactive vs active)

**Generated (UTC):** `2026-09-12T14:00:55.157482+00:00`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs\synthesis\EXPERIMENT_CB2_ESMDYNAMIC.md`
**Run mode:** `sample25`
**Experiment:** `EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME_N25`

## Epistemology

- Filename `inactive`/`active` = **start-label proxy only** — **≠** MSM macrostate.
- Fallback after `EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE`.
- Does **not** reopen P2 CONVERGENT; no Gi; no fake filelist alignment.

## Verdicts

- **`EXT_APO_TM6_TOGGLE_INDETERMINATE`**
- Soft vs PDB state-dependence narrative: `EXT_APO_TM6_SOFT_NOT_CLEAR_STATE_DEPENDENT`
- Soft vs prior N=5 INDETERMINATE: `PRIOR_N5_INDETERMINATE_STABLE`
- Soft vs Dutta conserved/unconserved narrative: `SOFT_COMPAT_DUTTA_MIXED_CONSERVED_UNCONSERVED — partial signal (3/6 |d|≥0.8; IC open 1/3); matches expectation that filename inactive/active is a coarse proxy for a mixed conserved/unconserved activation-feature story`
- Filename ≠ MSM: `True`
- P2 unchanged: `CLOSED_INSUFFICIENT_SAMPLING`

## Sampling

- N_traj inactive/active: **25** / **25**
- Frames pooled inactive/active: `5000` / `5000`
- Seed: `20260912`; frame_cap: `200`
- Zip extract ok: `True`; cache `data\external\dutta_shukla_2023\trajectories\CB2_APO\_tm6_sample25`
- Zip pools inactive/active: `{'inactive': 2598, 'active': 2373}`
- Bytes written this run: `1555197864`; reused existing: `0`

## Mapping

- Alignment identity: `1.0000`
- Median topo−UniProt offset: `-20`
- Note: UniProt P34972 → topo resid; expect ~-20 on Dutta construct

## Primary toggle summary

- |d|≥0.8 among primary 6: **3**/6
- IC opening (active>inactive & |d|≥0.8): **1**/3

## Primary features

| role | UniProt | topo | mean_in | mean_act | Δ | d |
|---|---|---|---:|---:|---:|---:|
| Arg3.50-Lys6.35 | [131, 245] | [111, 213] | 10.64 | 15.04 | 4.40 | 4.01 |
| Arg3.50-Asp6.30 | [131, 240] | [111, 208] | 13.36 | 12.96 | -0.39 | -0.18 |
| Arg3.50-Trp6.48 | [131, 258] | [111, 226] | 22.18 | 20.86 | -1.32 | -1.73 |
| Pro5.50-Trp6.48 | [211, 258] | [191, 226] | 23.00 | 20.89 | -2.10 | -2.52 |
| Trp6.48-Asn7.45 | [258, 291] | [226, 259] | 7.51 | 7.38 | -0.13 | -0.12 |
| Trp6.48-Asn7.49 | [258, 295] | [226, 263] | 12.14 | 12.07 | -0.06 | -0.07 |

## N-term / TM2–NPxxY (descriptive only)

- `Ala2.53-Asn7.45` UniProt=[83, 291] d=0.01 Δ=0.00 Å |d|≥0.8=False
- `Ala2.49-Asn7.45` UniProt=[79, 291] d=0.06 Δ=0.03 Å |d|≥0.8=False

## Hub-adjacent distances (descriptive)

- `Trp6.48-Asn7.45` UniProt=[258, 291] d=-0.12 Δ=-0.13 Å
- `Trp6.48-Asn7.49` UniProt=[258, 295] d=-0.07 Δ=-0.06 Å
- `Lys6.35-Asn7.45` UniProt=[245, 291] d=0.61 Δ=0.62 Å
- `Asp6.30-Asn7.49` UniProt=[240, 295] d=0.88 Δ=1.61 Å
- `TM6Cterm-Asn7.49` UniProt=[264, 295] d=-0.02 Δ=-0.01 Å
- `Arg3.50-Asn7.49` UniProt=[131, 295] d=-2.06 Δ=-2.28 Å
- `Arg3.50-Asn7.45` UniProt=[131, 291] d=-1.94 Δ=-1.93 Å
- `Ala2.53-Asn7.45` UniProt=[83, 291] d=0.01 Δ=0.00 Å
- `Ala2.49-Asn7.45` UniProt=[79, 291] d=0.06 Δ=0.03 Å
- `Leu7.41-Asn7.49` UniProt=[287, 295] d=-0.25 Δ=-0.19 Å
- `Arg8.46-Asn7.49` UniProt=[302, 295] d=-1.62 Δ=-1.32 Å

## PI summary (ES)

TM6/toggle filename inactive vs active, N_traj=25+25 (mode=sample25): **EXT_APO_TM6_TOGGLE_INDETERMINATE** — primary |d|≥0.8: 3/6; apertura IC (active>inactive y |d|≥0.8): 1/3. vs N=5 prior: PRIOR_N5_INDETERMINATE_STABLE. Etiqueta de arranque ≠ macroestado MSM; no reabre P2; sin filelist inventado; no Gi.

## Forbidden claims

- No MSM substitute; no P2 CONVERGENT; no Gi; filename ≠ metastable state.

## Artifact SHA256

- `cb2_apo_tm6_toggle.json`: `426f9afe59510fd9cf8559e450541ac5580867761d14f765f829b7fc80a36f56`
- prereg `EXPERIMENT_CB2_ESMDYNAMIC.md`: `08b1afbef984d08d420398fe7bc2648fb5123dddcff8789cdc3ada092a87fbf0`
- script `cb2_apo_tm6_toggle.py`: `d352d779261ec185eb67c1b164082acf7cab9ee32cbd103eac73cf6861f858e5`

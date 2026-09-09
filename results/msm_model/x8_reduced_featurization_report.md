# X8 — Reduced featurization MSM (Gate-1 diagnosis)

**Generated (UTC):** 2026-09-09T20:08:59.485003+00:00
**Pre-registration:** `docs\synthesis\EXPERIMENT_X8_REDUCED_FEATURIZATION.md`
**X8 verdict:** `X8_SAMPLING_LIMITED`

## Scope

- Same 1995 frames / 5 WT replicas as P2 baseline.
- Reduced featurization only; **no** A/B/C architecture claim.
- P2 remains **CLOSED (INSUFFICIENT_SAMPLING)** regardless of X8.

## Baseline (`2dcff23`)

- Features: **15753** TM Cα pairwise
- ITS: **`NON_CONVERGENT`**
- Connected states/lag: `[25, 25, 8, 1, 8, 1, 8, 1, 1, 1]`

## Reduced features

- **n = 24** Cα–Cα distances (fixed a priori)

- 1. `131–245` (Arg3.50-Lys6.35)
- 2. `131–240` (Arg3.50-Asp6.30)
- 3. `131–258` (Arg3.50-Trp6.48)
- 4. `128–245` (Tyr3.47region-Lys6.35)
- 5. `211–258` (Pro5.50-Trp6.48)
- 6. `207–258` (TM5mid-Trp6.48)
- 7. `215–245` (TM5IC-Lys6.35)
- 8. `215–240` (TM5IC-Asp6.30)
- 9. `201–258` (TM5mid2-Trp6.48)
- 10. `258–291` (Trp6.48-Asn7.45)
- 11. `258–295` (Trp6.48-Asn7.49)
- 12. `258–285` (Trp6.48-Ser7.39)
- 13. `245–291` (Lys6.35-Asn7.45)
- 14. `240–295` (Asp6.30-Asn7.49)
- 15. `264–295` (TM6Cterm-Asn7.49)
- 16. `131–295` (Arg3.50-Asn7.49)
- 17. `131–291` (Arg3.50-Asn7.45)
- 18. `83–291` (Ala2.53-Asn7.45)
- 19. `79–291` (Ala2.49-Asn7.45)
- 20. `87–285` (Phe87-Ser285)
- 21. `183–258` (PheECL2-Trp6.48)
- 22. `268–285` (Ser6.58-Ser7.39)
- 23. `287–295` (Leu7.41-Asn7.49)
- 24. `302–295` (Arg8.46-Asn7.49)

## Hyperparameters

- tICA lag=5, dim=5
- K-means microstates=25, seed=20260821
- ITS lags=[1, 2, 5, 10, 15, 20, 25, 30, 40, 50]

## ITS assessment

- Verdict: **`NON_CONVERGENT`**
- Reason: slowest ITS relative change late-vs-mid thirds = 0.674 (flat≤0.25, marginal≤0.5)
- n_finite_slowest: 10
- connected_states_per_lag: `[25, 25, 25, 25, 25, 25, 25, 25, 25, 25]`
- slowest_rel_change: 0.6741694642440774

## Material improvement checklist

- cond1 finite ITS ≥3: **True**
- cond2 no majority collapse: **True**
- cond3 flattening: **False** (fails flattening clause (verdict=NON_CONVERGENT, pathological=False, rel=0.6741694642440774))
- materially_improves: **False**

## Verdict

**`X8_SAMPLING_LIMITED`**

- Provisional P2 lean (unchanged gate): `P2_INSUFFICIENT_SAMPLING`

## Artifacts

- `results\msm_model\x8_implied_timescales.png`
- `results\msm_model\x8_implied_timescales.json`
- `results/msm_model/x8_reduced_featurization_report.json`


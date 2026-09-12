# Data request — Dutta & Shukla 2023 MSM (DRAFT)

**Status:** `FINAL_MSM_RECOVERED` + local `CB2_APO.zip` — Gate 0 for MSM-state contacts is **`EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT`** (2026-09-12). Email still needed for **traj↔MSM filelist** (not for re-download of 142 GB).

**Action:** draft only — **do NOT email** from automation  
**Date:** 2026-08-21 (updated 2026-09-12)  
**Branch:** `feat/cb2-hubs-functional-topology-test`  
**P2 role (reformulated):** Dutta & Shukla is **NOT** required to run P2. Real P2 uses **own MSM** on 5 WT GPCRmd Morales-Pastor trajs. Final_MSM pickles are **READY for optional external comparison when PI authorizes** (never a fitting template; different K is allowed). Frame-level contacts **per Dutta macrostate** remain blocked without an ordered filelist.

---

## Citation / endpoints (locked)

| Item | Value |
|------|--------|
| Paper | Dutta, S. & Shukla, D. *Commun Biol* **6**, 485 (2023) |
| DOI | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| PMC | [PMC10163236](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10163236/) |
| Code | [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) (`0fe83dc`) |
| Box (Data availability) | `https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4` (ID `jzooa0o27z1w9ha0h6va3i51ir7l38j4`) |
| Traj share (README) | `https://uofi.box.com/s/xl7tpf345rt8tikjaidfa8rm7gy2wrpj` (`CB2_APO`) |
| Prior recovery | One-shot 2026-08-21 — all Box host/README mirrors **404**; see `results/network_core/traj_recovery_attempt.md` |
| Reprobe 2026-09-10 | Listing **HTTP 200**; scripted download **403 bandwidth**; user browser later recovered full `Final_MSM` quartet |
| CB2_APO zip (local) | `data/external/dutta_shukla_2023/trajectories/CB2_APO.zip` (~153 GB on disk; **4971** `.nc` + prmtop + helpers `list`, `mv_short_file`) |

**Local landing path:** `data/external/dutta_shukla_2023/msm/` + `MANIFEST.json` · traj zip + `trajectories/CB2_APO/` · shallow code clone `trajectories/../_code_Cannabinoid_activation/` (optional local mirror of GitHub)

---

## GitHub audit (2026-09-12) — does **not** unlock alignment

Shallow clone of [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) + recovery tree JSON under `data/external/_recovery_2026-08-21/`:

| Finding | Detail |
|---------|--------|
| Repo contents | Figure/table scripts + Initial_Coordinates PDBs/prmtops + README Box links. **No** MSM construction notebook, **no** traj loader, **no** `filelist` / path list of length ~4972. |
| How pickles are used | e.g. `Main_Figure_6/CB2-APO_vampnet_states_TPT.py` does `pickle.load(...CB2_state_prob.pkl)` / `CB2_msm_feature_final_clustering.pkl` and concatenates list elements — **anonymous index order**, never maps index → `.nc` name. |
| Labels only | Same script locks macro labels `['I1','I2','I3','Inactive','I4','Active']` (column order). Useful for naming; **not** for traj alignment. |
| Zip helper `CB2_APO/list` | **5** leftover short-traj names from `mv_short_file` shell snippet — **not** the MSM load order. |
| Sister repos (recovery) | `Dutta_Shukla_Cannabinoid_2023a`, `Dutta_Shukla_EndoCannabinoid_2025` — no CB2_APO filelist either. |

**Verdict:** GitHub **does not** reconstruct traj↔index mapping. Do **not** assume lex / zip-member / natural sort equals MSM list order.

### Dry-run counts (no fake alignment)

| Object | Count |
|--------|------:|
| `CB2_state_prob.pkl` / clustering list length | **4972** |
| `.nc` members in `CB2_APO.zip` | **4971** |
| Δ | **+1 MSM list entry** vs zip |
| Multiset of per-traj lengths `T` | Matches zip NetCDF byte-size → `T` map **except** one extra MSM traj with **`T = 360`** (MSM has 2 such; zip has 1) |
| Common sort orders vs MSM `T` sequence | Prefix match ≪ 4971; **fail** Gate 0 (see `results/network_core/cb2_msm_state_contacts.*`) |

---

## Need (remaining) — precise author ask

We already hold Final_MSM + the full CB2_APO trajectory zip. **Ask only for the alignment key:**

1. **Preferred:** plain-text (or pickle/JSON) **ordered filelist** of length **4972** — one Amber NetCDF basename per line — in the **exact order** of `CB2_state_prob.pkl` / `CB2_msm_feature_final_clustering.pkl` list indices `0…4971`.
2. **Or:** identification of the **extra** MSM trajectory (the second `T=360` entry, or whichever index is not in the public zip) **plus** the ordered list of the **4971** deposited `.nc` files.
3. **Or:** the original load script / glob that built that list (deterministic, runnable against the Box folder layout).

Optional nicety: confirm whether any short trajs were moved aside (`mv_short_file` / `shorter_traj`) and whether those appear in the MSM list.

**Not needed from authors for this Gate:** re-upload of the 142 GB zip (we have it); re-send of Final_MSM pickles.

---

## Email template (copy for human send)

**To:** corresponding author(s) as listed on the paper  
**Subject:** Request for CB2 apo MSM trajectory filelist — Commun Biol 2023 (DOI 10.1038/s42003-023-04868-1)

Dear Dr. Dutta and Dr. Shukla,

We are independently reanalyzing published CB2 conformational dynamics from your *Communications Biology* paper (DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)).

We already have locally: (i) the `Final_MSM` objects `CB2_state_prob.pkl` and `CB2_msm_feature_final_clustering.pkl` (each a Python `list` of length **4972**), and (ii) the Box `CB2_APO` trajectory archive (**4971** Amber NetCDF `*-strip.nc` files). Your GitHub repository [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) is available and clarifies metastable-state label order, but it does **not** include the trajectory path list or MSM-building loader, so we cannot map list index `i` → `.nc` filename. The public zip is also short by one trajectory relative to the pickle lists (multiset of per-traj lengths matches except one extra MSM entry with length **360**).

Would you be willing to share a small text file (or equivalent) with the **ordered filenames** used when those pickles were written—ideally 4972 lines aligned to the pickle list indices—or otherwise identify the missing/extra trajectory and the load order for the 4971 deposited files? We do **not** need another copy of the large trajectory archive.

We would use this only for academic reanalysis of state-dependent contact patterns under your published MSM labels (no redistribution beyond our research group without your permission). Happy to cite the paper and acknowledge your help.

Thank you very much for your time and for making the analysis reproducible.

Best regards,  
[NAME]  
[AFFILIATION]  
[EMAIL]

---

## Governance

```
STATUS: FINAL_MSM_RECOVERED + CB2_APO_ZIP_LOCAL
AUTO_EMAIL: FORBIDDEN
INFINITE_PUBLIC_SEARCH: STOP
GITHUB_UNLOCKS_ALIGNMENT: NO (audited 2026-09-12)
EXTERNAL_COMPARISON: READY_WHEN_PI_AUTHORIZES (pickle-level OK)
EXT_MSM_STATE_CONTACTS: INDETERMINATE_NO_ALIGNMENT (need filelist)
P2_REAL_MSM_COMPUTE: NOT_GATED_BY_DUTTA (own Morales-Pastor MSM)
P5_EXECUTION: NOT_OPENED_BY_THIS_REQUEST
TRAJECTORIES: ZIP_LOCAL (4971 nc); ALIGNMENT_KEY: MISSING
```

*Fin — ask authors for ordered filelist (or extra-traj ID); do not re-download 142 GB; do not fake lex/zip order.*

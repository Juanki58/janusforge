# Email draft — Dutta & Shukla CB2 apo MSM filelist (READY TO SEND)

**Status:** DRAFT — **do NOT send from automation**. Human send only.  
**Date:** 2026-09-22  
**Language:** EN (matches prior [`DATA_REQUEST_DUTTA_SHUKLA_MSM.md`](../synthesis/DATA_REQUEST_DUTTA_SHUKLA_MSM.md) template)  
**Related:** Gate 0 `EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT`  
**Branch:** `feat/cb2-hubs-functional-topology-test`

---

## Send checklist (human)

- [ ] Confirm corresponding author emails from the paper PDF / journal site  
- [ ] Fill `[NAME] / [AFFILIATION] / [EMAIL]` below  
- [ ] Optional: attach a one-line note that we do **not** need another 142 GB copy  
- [ ] Send manually (Outlook / institutional mail)  
- [ ] Log date sent in `DATA_REQUEST_DUTTA_SHUKLA_MSM.md` when done  

**AUTO_EMAIL:** FORBIDDEN

---

## To / Subject

**To:** corresponding author(s) as listed on Dutta & Shukla, *Commun Biol* 2023  
**Subject:** Request for CB2 apo MSM trajectory filelist — Commun Biol 2023 (DOI 10.1038/s42003-023-04868-1)

---

## Body (copy-paste)

Dear Dr. Dutta and Dr. Shukla,

We are independently reanalyzing published CB2 conformational dynamics from your *Communications Biology* paper (DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)).

We already have locally:

1. the `Final_MSM` objects `CB2_state_prob.pkl` and `CB2_msm_feature_final_clustering.pkl` (each a Python `list` of length **4972**), and  
2. the Box `CB2_APO` trajectory archive (**4971** Amber NetCDF `*-strip.nc` files).

Your GitHub repository [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) clarifies metastable-state label order, but it does **not** include the trajectory path list or the MSM-building loader, so we cannot map list index `i` → `.nc` filename. The public zip is also short by one trajectory relative to the pickle lists (the multiset of per-traj lengths matches except one extra MSM entry with length **360**). We are **not** assuming lexicographic or zip-member order equals the MSM list order.

Would you be willing to share a small text file (or equivalent) with the **ordered filenames** used when those pickles were written—ideally **4972** lines aligned to the pickle list indices—or otherwise identify the missing/extra trajectory and the load order for the **4971** deposited files? We do **not** need another copy of the large trajectory archive.

We would use this only for academic reanalysis of state-dependent contact patterns under your published MSM labels (no redistribution beyond our research group without your permission). Happy to cite the paper and acknowledge your help.

Thank you very much for your time and for making the analysis reproducible.

Best regards,  
[NAME]  
[AFFILIATION]  
[EMAIL]

---

## Spanish note for PI (not for authors)

Este borrador está listo para envío humano. **No** se ha enviado automáticamente. Desbloquea EXTERNAL contactos por metaestable Dutta; **no** reabre P2 Gate-1 ni sustituye muestreo propio Tier B.

---

*Fin draft. Mirror of synthesis DATA_REQUEST email block; communications copy for send workflow.*

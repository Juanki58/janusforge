#!/usr/bin/env python3
"""Build local Option D panel (URB447 + published Yin-Yang + THCV/THC refs).

Only published/public structures + optional local ex-lead H1_02c.
Writes gitignored CSV under data/libraries/option_d_batch1*.csv — do not print SMILES.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data/libraries/quimioma_semillas.csv"
BATCH3 = ROOT / "data/libraries/h1_h5_batch3.csv"
OUT = ROOT / "data/libraries/option_d_batch1.csv"
OUT_FULL = ROOT / "data/libraries/option_d_batch1_full.csv"
OUT_META = ROOT / "data/libraries/option_d_batch1_meta.json"

# Published Janus / Yin-Yang (PubChem / ChEBI / GtoPdb; not Qiu 2023 — no reliable public SMILES)
PUBLISHED = [
    {
        "name": "AM1710",
        "common_name": "AM1710",
        "role": "yin_yang_published",
        "hypothesis": "YY_AM1710",
        "smiles": "CCCCCCC(C)(C)C1=CC(=C2C(=C1)OC(=O)C3=C2C=C(C=C3)OC)O",
        "notes": "PubChem CID 11268660; Dhopeshwarkar 2017 Janus (CB2 ago / CB1 inverse ago low-potency)",
        "key_ref": "Dhopeshwarkar 2017; Khanolkar 2007",
        "doi_or_url": "https://doi.org/10.1124/jpet.116.236539",
    },
    {
        "name": "GW405833",
        "common_name": "GW405833",
        "role": "yin_yang_published",
        "hypothesis": "YY_GW405833",
        "smiles": "CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4",
        "notes": "PubChem CID 9911463; Dhopeshwarkar 2017 Janus",
        "key_ref": "Dhopeshwarkar 2017",
        "doi_or_url": "https://doi.org/10.1124/jpet.116.236539",
    },
]


def _row_from_seed(df: pd.DataFrame, name: str, role: str | None = None, hyp: str = "") -> dict:
    r = df[df["name"] == name]
    if r.empty:
        raise ValueError(f"Missing {name} in {SEED}")
    x = r.iloc[0]
    return {
        "name": str(x["name"]),
        "common_name": str(x.get("common_name", name)),
        "role": role or str(x["role"]),
        "hypothesis": hyp or str(x.get("role", "")),
        "smiles": str(x["smiles"]),
        "notes": str(x.get("notes", "")),
        "key_ref": str(x.get("key_ref", "")),
        "doi_or_url": str(x.get("doi_or_url", "")),
    }


def main() -> int:
    seeds = pd.read_csv(SEED)
    rows: list[dict] = []

    # Synthetic seed / design comparator
    urb = _row_from_seed(seeds, "URB447", role="design_comparator", hyp="URB447_seed")
    urb["notes"] = (
        "PubChem CID 25195055; LoVerme 2009; Track D synthetic seed / design comparator"
    )
    rows.append(urb)

    rows.extend(PUBLISHED)

    # Refs
    rows.append(_row_from_seed(seeds, "delta9-THCV", hyp="REF"))
    rows.append(_row_from_seed(seeds, "delta9-THC", hyp="REF"))

    # Optional ex-lead phytocannabinoid (local only; from Batch 3 panel)
    if BATCH3.exists():
        b3 = pd.read_csv(BATCH3)
        hit = b3[b3["name"] == "JANUS_H1_02c"]
        if not hit.empty:
            x = hit.iloc[0]
            rows.append(
                {
                    "name": "JANUS_H1_02c",
                    "common_name": "ex-lead phytocannabinoid",
                    "role": "ex_lead_phytocannabinoid",
                    "hypothesis": "H1_02c_exlead",
                    "smiles": str(x["smiles"]),
                    "notes": "Optional Batch3 ex-lead; Track1 membrane MD NO-GO; local only",
                    "key_ref": "h1_h5_batch3 / md_membrane_20ns_summary",
                    "doi_or_url": "",
                }
            )

    full = pd.DataFrame(rows)
    # Qiu 2023: literature-only (no SMILES in panel — no reliable public structure dump)
    meta = {
        "batch": "option_d_batch1",
        "n_rows": len(full),
        "roles": full["role"].value_counts().to_dict(),
        "qiu_2023": {
            "included": False,
            "reason": "No reliable public SMILES/CID for Qiu Bioorg Chem 2023 Yin-Yang lead; cite DOI only",
            "doi": "https://doi.org/10.1016/j.bioorg.2023.106377",
        },
        "sources": {
            "URB447": "data/libraries/quimioma_semillas.csv",
            "AM1710": "PubChem CID 11268660",
            "GW405833": "PubChem CID 9911463",
            "delta9-THCV": "quimioma_semillas.csv",
            "delta9-THC": "quimioma_semillas.csv",
            "JANUS_H1_02c": "h1_h5_batch3.csv (optional local)",
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel = full[["name", "common_name", "smiles", "role"]].copy()
    panel.to_csv(OUT, index=False)
    full.to_csv(OUT_FULL, index=False)
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Status without structures
    print(f"Wrote {OUT} ({len(panel)} ligands)")
    print(f"Roles: {meta['roles']}")
    print(f"Qiu 2023 in panel: {meta['qiu_2023']['included']} ({meta['qiu_2023']['reason']})")
    for name, role in zip(full["name"], full["role"], strict=True):
        print(f"  {name}\t{role}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

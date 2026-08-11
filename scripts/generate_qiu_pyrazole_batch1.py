#!/usr/bin/env python3
"""Build local Qiu pyrazole Batch-1 panel (LOCAL / gitignored).

Compound 14 (Qiu et al. 2023 Yin-Yang): SMILES reconstructed from published
structural descriptors (mapa / paper text) — NOT a PubChem CID deposit.
No ChEMBL document dump found for DOI 10.1016/j.bioorg.2023.106377.

Writes gitignored CSVs under data/libraries/qiu_pyrazole_batch1*.csv.
IP: do not print/commit/push SMILES of design candidates.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data/libraries/quimioma_semillas.csv"
OUT = ROOT / "data/libraries/qiu_pyrazole_batch1.csv"
OUT_FULL = ROOT / "data/libraries/qiu_pyrazole_batch1_full.csv"
OUT_META = ROOT / "data/libraries/qiu_pyrazole_batch1_meta.json"

# Published Yin-Yang refs (same as option_d_batch1; PubChem CIDs)
GW405833_SMILES = "CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4"
AM1710_SMILES = "CCCCCCC(C)(C)C1=CC(=C2C(=C1)OC(=O)C3=C2C=C(C=C3)OC)O"

# Qiu Compound 14 — reconstructed from published descriptors:
# N1-(2-morpholinophenyl), C3-adamantan-1-yl, C4-methyl, C5-phenyl
# Confidence: medium (no PubChem CID / ChEMBL deposit; not SI-validated here).
QIU14_SMILES = "Cc1c(-c2ccccc2)n(-c2ccccc2N2CCOCC2)nc1C12CC3CC(CC(C3)C1)C2"
QIU14_CONFIDENCE = "reconstructed_published_descriptors_no_pubchem_cid"


def _load_seed(name: str) -> str:
    df = pd.read_csv(SEED)
    hit = df[df["name"] == name]
    if hit.empty:
        raise KeyError(f"{name} not in {SEED}")
    return str(hit.iloc[0]["smiles"])


def _canon(smiles: str) -> str | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Exception:  # noqa: BLE001
        return None
    return Chem.MolToSmiles(mol, isomericSmiles=True)


def _row(
    name: str,
    common: str,
    smiles: str | None,
    role: str,
    hypothesis: str,
    notes: str,
    key_ref: str = "",
    doi: str = "",
) -> dict:
    ok = bool(smiles)
    mw = formula = None
    if smiles:
        m = Chem.MolFromSmiles(smiles)
        if m is not None:
            mw = round(Descriptors.MolWt(m), 2)
            formula = rdMolDescriptors.CalcMolFormula(m)
    return {
        "name": name,
        "common_name": common,
        "smiles": smiles or "",
        "role": role,
        "hypothesis": hypothesis,
        "smiles_valid": ok,
        "mw": mw,
        "formula": formula or "",
        "notes": notes,
        "key_ref": key_ref,
        "doi_or_url": doi,
    }


def _qiu_analogs() -> list[dict]:
    """Minimal documented variants around reconstructed Compound 14 (IDs QIU_*)."""
    # Base and ortho→para/meta/none morpholine; aryl / cage edits
    specs = [
        (
            "QIU_14",
            "Compound14_reconstructed",
            QIU14_SMILES,
            "yin_yang_published",
            "QIU14_ortho_morpholine",
            (
                "Qiu 2023 Compound 14 reconstructed: N1-(2-morpholinophenyl), "
                "C3-adamantan-1-yl, C4-Me, C5-Ph. "
                f"smiles_source={QIU14_CONFIDENCE}. Ki/IC50 table not recovered."
            ),
            "Qiu et al. 2023",
            "https://doi.org/10.1016/j.bioorg.2023.106377",
        ),
        (
            "QIU_01",
            "para_morpholine",
            "Cc1c(-c2ccccc2)n(-c2ccc(N3CCOCC3)cc2)nc1C12CC3CC(CC(C3)C1)C2",
            "design_candidate",
            "QIU_para_morpholine_negctrl",
            "Minimal: morpholine para (vs ortho) — negative control for S173/S285 hypothesis.",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_02",
            "meta_morpholine",
            "Cc1c(-c2ccccc2)n(-c2cccc(N3CCOCC3)c2)nc1C12CC3CC(CC(C3)C1)C2",
            "design_candidate",
            "QIU_meta_morpholine",
            "Minimal: morpholine meta on N1-phenyl.",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_03",
            "N1_phenyl_no_morpholine",
            "Cc1c(-c2ccccc2)n(-c2ccccc2)nc1C12CC3CC(CC(C3)C1)C2",
            "design_candidate",
            "QIU_no_morpholine",
            "Minimal: drop morpholine (N1-phenyl) — tests polar arm necessity in Vina proxy.",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_04",
            "C5_pCl_phenyl",
            "Cc1c(-c2ccc(Cl)cc2)n(-c2ccccc2N2CCOCC2)nc1C12CC3CC(CC(C3)C1)C2",
            "design_candidate",
            "QIU_C5_pCl",
            "Minimal: C5 p-Cl-phenyl (rimonabant-like aryl) keep ortho-morpholine + adamantyl.",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_05",
            "C4_desmethyl",
            "c1ccc(-c2cc(C34CC5CC(CC(C5)C3)C4)nn2-c2ccccc2N2CCOCC2)cc1",
            "design_candidate",
            "QIU_C4_H",
            "Minimal: C4-H (desmethyl) vs C4-Me.",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_06",
            "ortho_piperidine",
            "Cc1c(-c2ccccc2)n(-c2ccccc2N2CCCCC2)nc1C12CC3CC(CC(C3)C1)C2",
            "design_candidate",
            "QIU_ortho_piperidine",
            "Minimal: ortho-piperidine bioisostere of morpholine (lose ether O H-bond acceptor).",
            "local QIU_* SAR",
            "",
        ),
        (
            "QIU_07",
            "C3_cyclohexyl",
            "Cc1c(-c2ccccc2)n(-c2ccccc2N2CCOCC2)nc1C1CCCCC1",
            "design_candidate",
            "QIU_C3_cyclohexyl",
            "Minimal: C3-cyclohexyl instead of adamantyl (smaller hydrophobic cage).",
            "local QIU_* SAR",
            "",
        ),
    ]
    rows = []
    for name, common, smi, role, hyp, notes, ref, doi in specs:
        canon = _canon(smi)
        rows.append(_row(name, common, canon, role, hyp, notes, ref, doi))
    return rows


def main() -> int:
    rows: list[dict] = []
    rows.extend(_qiu_analogs())

    # Published refs already in chemome / prior Option D panels
    rows.append(
        _row(
            "URB447",
            "URB447",
            _canon(_load_seed("URB447")),
            "design_comparator",
            "URB447_seed",
            "PubChem CID 25195055; LoVerme 2009; dual-rank anchor for this gate.",
            "LoVerme 2009",
            "https://doi.org/10.1016/j.bmcl.2008.12.059",
        )
    )
    rows.append(
        _row(
            "GW405833",
            "GW405833",
            _canon(GW405833_SMILES),
            "yin_yang_published",
            "YY_GW405833",
            "PubChem CID 9911463; Dhopeshwarkar 2017 Janus.",
            "Dhopeshwarkar 2017",
            "https://doi.org/10.1124/jpet.116.236539",
        )
    )
    rows.append(
        _row(
            "AM1710",
            "AM1710",
            _canon(AM1710_SMILES),
            "yin_yang_published",
            "YY_AM1710",
            "PubChem CID 11268660; Dhopeshwarkar 2017 Janus.",
            "Dhopeshwarkar 2017",
            "https://doi.org/10.1124/jpet.116.236539",
        )
    )
    rows.append(
        _row(
            "delta9-THCV",
            "THCV",
            _canon(_load_seed("delta9-THCV")),
            "seed",
            "REF",
            "Optional phytocannabinoid ref; not primary gate for this batch.",
            "Pertwee / quimioma",
            "",
        )
    )
    rows.append(
        _row(
            "delta9-THC",
            "THC",
            _canon(_load_seed("delta9-THC")),
            "anti_seed",
            "REF",
            "Anti-seed for gap vs THC.",
            "Pertwee / quimioma",
            "",
        )
    )

    df = pd.DataFrame(rows)
    bad = df[~df["smiles_valid"]]
    if not bad.empty:
        print("BLOQUEO: invalid SMILES:", bad["name"].tolist())
        return 2

    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Slim docking CSV
    slim_cols = ["name", "common_name", "smiles", "role", "hypothesis"]
    df[slim_cols].to_csv(OUT, index=False)
    df.to_csv(OUT_FULL, index=False)

    meta = {
        "batch": "qiu_pyrazole_batch1",
        "n_rows": int(len(df)),
        "qiu14_smiles_confidence": QIU14_CONFIDENCE,
        "qiu14_pubchem_cid": None,
        "qiu14_chembl_document": None,
        "qiu14_ki_ic50": "not_recovered_from_open_sources",
        "doi": "https://doi.org/10.1016/j.bioorg.2023.106377",
        "structure_descriptors": {
            "core": "1H-pyrazole",
            "N1": "2-morpholinophenyl",
            "C3": "adamantan-1-yl (direct)",
            "C4": "methyl",
            "C5": "phenyl",
        },
        "ids": df["name"].tolist(),
        "note": (
            "SMILES local/gitignored. Public reports: IDs + scores only. "
            "MD/OpenMM paused — docking CPU only."
        ),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"OK {len(df)} ligands -> {OUT}")
    print(f"Full: {OUT_FULL}")
    print(f"Meta: {OUT_META}")
    print(f"QIU_14 confidence: {QIU14_CONFIDENCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

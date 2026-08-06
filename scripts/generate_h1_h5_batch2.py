#!/usr/bin/env python3
"""Generate Track-1 Batch-2 panel: H1×H2 hybrids + 1′ volume (LOCAL / gitignored).

Builds on Batch-1 lesson: only JANUS_H1_02 (1′-Me on THCV) passed the hard gate
marginally; H2 acids/esters weakened CB1. Batch 2 asks whether combining 1′
branching with THCVA-like A-ring COOH (or ester) helps, and whether larger 1′
volume on neutral THCV improves further.

Writes only under gitignored paths (default: data/libraries/h1_h5_batch2.csv).
IP: do not commit/push the output CSV or derived SDF/PDBQT.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SEED_CSV = ROOT / "data/libraries/quimioma_semillas.csv"
DEFAULT_OUT = ROOT / "data/libraries/h1_h5_batch2.csv"
DEFAULT_META = ROOT / "data/libraries/h1_h5_batch2_meta.json"
DEFAULT_FULL = ROOT / "data/libraries/h1_h5_batch2_full.csv"

# Aromatic carbon bearing a linear n-propyl side chain (THCV / THCVA).
_PROPYL_SMARTS = "[c:1][CH2:2][CH2:3][CH3:4]"


def _load_seed(name: str) -> tuple[str, Chem.Mol]:
    df = pd.read_csv(SEED_CSV)
    hit = df[df["name"] == name]
    if hit.empty:
        raise KeyError(f"{name} not in {SEED_CSV}")
    smiles = str(hit.iloc[0]["smiles"])
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid template SMILES for {name}")
    return smiles, mol


def _canonicalize(mol: Chem.Mol | None) -> str | None:
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Exception:  # noqa: BLE001
        return None
    if any(a.GetAtomicNum() == 0 for a in mol.GetAtoms()):
        return None
    return Chem.MolToSmiles(mol, isomericSmiles=True)


def _attach_chain_to_aromatic(mol: Chem.Mol, chain_smiles: str) -> Chem.Mol | None:
    """Replace Ar–CH2–CH2–CH3 with Ar–(chain); chain root bonds to aromatic C."""
    qry = Chem.MolFromSmarts(_PROPYL_SMARTS)
    if qry is None:
        return None
    matches = mol.GetSubstructMatches(qry)
    if not matches:
        return None
    match = matches[0]
    ar_idx, *propyl_idxs = match

    chain = Chem.MolFromSmiles(chain_smiles)
    if chain is None or chain.GetNumAtoms() < 1:
        return None

    rw = Chem.RWMol(Chem.Mol(mol))
    for idx in sorted(propyl_idxs, reverse=True):
        rw.RemoveAtom(idx)

    offset = sum(1 for i in propyl_idxs if i < ar_idx)
    ar_idx_new = ar_idx - offset

    combo = Chem.RWMol(Chem.CombineMols(rw, chain))
    n_core = rw.GetNumAtoms()
    chain_root = n_core
    combo.AddBond(ar_idx_new, chain_root, Chem.BondType.SINGLE)
    try:
        Chem.SanitizeMol(combo)
    except Exception:  # noqa: BLE001
        return None
    return combo.GetMol()


def _build_methyl_ester(acid: Chem.Mol | None) -> Chem.Mol | None:
    """COOH → COOCH3 on THCVA-like acids."""
    if acid is None:
        return None
    rxn = AllChem.ReactionFromSmarts("[C:1](=[O:2])[OH]>>[C:1](=[O:2])OC")
    if rxn is None or not acid.HasSubstructMatch(Chem.MolFromSmarts("C(=O)[OH]")):
        return None
    outs = rxn.RunReactants((acid,))
    for tup in outs:
        for m in tup:
            smi = _canonicalize(m)
            if smi:
                return Chem.MolFromSmiles(smi)
    return None


def _row(
    name: str,
    common: str,
    smiles: str | None,
    role: str,
    hypothesis: str,
    notes: str,
    valid: bool,
) -> dict:
    return {
        "name": name,
        "common_name": common,
        "smiles": smiles or "",
        "role": role,
        "hypothesis": hypothesis,
        "smiles_valid": bool(valid and smiles),
        "notes": notes,
    }


def build_panel() -> tuple[pd.DataFrame, dict]:
    thcv_smi, thcv = _load_seed("delta9-THCV")
    thc_smi, _thc = _load_seed("delta9-THC")
    _thcva_smi, thcva = _load_seed("THCVA")

    # Pre-build parents so ester steps are honest (fail closed if acid fails).
    h1h2_01 = _attach_chain_to_aromatic(thcva, "C(C)CC")  # 1'-Me-THCVA
    h1h2_03 = _attach_chain_to_aromatic(thcva, "C(CC)CC")  # 1'-Et-THCVA

    builders = [
        (
            "JANUS_H1H2_01",
            "1'-Me-THCVA",
            "H1xH2 1'-Me-THCVA",
            "Hybrid: 1'-methyl on THCVA scaffold (A-ring COOH retained). "
            "Stereo at 1' unspecified (rac-like). Tests whether COOH kills CB1 "
            "even when 1'-Me helped on neutral THCV.",
            lambda: h1h2_01,
        ),
        (
            "JANUS_H1_03",
            "THCV-1'-Et",
            "H1 1'-Et",
            "1'-ethyl volume on neutral THCV (Ar–CH(Et)CH2CH3); stereo at 1' "
            "unspecified. Larger benzylic branch than Batch-1 JANUS_H1_02.",
            lambda: _attach_chain_to_aromatic(thcv, "C(CC)CC"),
        ),
        (
            "JANUS_H1_04",
            "THCV-1'-cPr",
            "H1 1'-cPr",
            "1'-cyclopropyl on neutral THCV: Ar–CH(cPr)CH2CH3 (closest valid to "
            "1'-cPr on C3 chain; not Ar–cPr alone). Stereo at 1' unspecified.",
            lambda: _attach_chain_to_aromatic(thcv, "C(C1CC1)CC"),
        ),
        (
            "JANUS_H1H2_02",
            "1'-Me-THCVA-OMe",
            "H1xH2 1'-Me-ester",
            "H1×H2 ester: methyl ester of JANUS_H1H2_01 (COOH→COOMe). "
            "Viable if parent acid builds; stereo at 1' unspecified.",
            lambda: _build_methyl_ester(h1h2_01),
        ),
        (
            "JANUS_H1H2_03",
            "1'-Et-THCVA",
            "H1xH2 1'-Et-THCVA",
            "Optional hybrid: 1'-ethyl + THCVA A-ring COOH. Stereo at 1' "
            "unspecified. Asks if larger H1 volume rescues acid CB1 weakness.",
            lambda: h1h2_03,
        ),
        (
            "JANUS_H1H2_04",
            "1'-Et-THCVA-OMe",
            "H1xH2 1'-Et-ester",
            "Optional: methyl ester of JANUS_H1H2_03. Stereo at 1' unspecified.",
            lambda: _build_methyl_ester(h1h2_03),
        ),
    ]

    rows: list[dict] = []
    meta_candidates: list[dict] = []

    rows.append(
        _row(
            "delta9-THCV",
            "THCV",
            thcv_smi,
            "seed",
            "REF",
            "Gate reference seed from quimioma_semillas.csv",
            True,
        )
    )
    rows.append(
        _row(
            "delta9-THC",
            "THC",
            thc_smi,
            "anti_seed",
            "REF",
            "Gate reference anti-seed from quimioma_semillas.csv",
            True,
        )
    )

    for name, common, hyp, notes, fn in builders:
        mol = None
        try:
            mol = fn()
        except Exception:  # noqa: BLE001
            mol = None
        smi = _canonicalize(mol) if mol is not None else None
        if smi and Chem.MolFromSmiles(smi) is None:
            smi = None
        valid = smi is not None
        rows.append(_row(name, common, smi, "design_candidate", hyp, notes, valid))
        meta_candidates.append(
            {
                "name": name,
                "hypothesis": hyp,
                "smiles_valid": valid,
                "notes": notes,
            }
        )

    df = pd.DataFrame(rows)
    panel = df[["name", "common_name", "smiles", "role"]].copy()
    meta = {
        "batch": "h1_h5_batch2",
        "design_focus": "H1xH2 hybrids + 1' volume (ethyl, cyclopropyl) on THCV",
        "batch1_lesson": (
            "Only JANUS_H1_02 (1'-Me) passed hard gate marginally; "
            "H2 acids/esters weakened CB1 dual."
        ),
        "template_sources": {
            "THCV": "delta9-THCV from data/libraries/quimioma_semillas.csv",
            "THCVA": "THCVA from data/libraries/quimioma_semillas.csv (PubChem CID 59444416)",
            "THC": "delta9-THC from data/libraries/quimioma_semillas.csv",
        },
        "n_candidates": int((df["role"] == "design_candidate").sum()),
        "n_valid_candidates": int(
            ((df["role"] == "design_candidate") & df["smiles_valid"]).sum()
        ),
        "candidates": meta_candidates,
        "isomer_notes": {
            "JANUS_H1H2_01": "1'-Me-THCVA; stereo at 1' unspecified",
            "JANUS_H1_03": "1'-Et-THCV Ar–CH(Et)CH2CH3; stereo at 1' unspecified",
            "JANUS_H1_04": "1'-cPr-THCV Ar–CH(cPr)CH2CH3; stereo at 1' unspecified",
            "JANUS_H1H2_02": "Methyl ester of H1H2_01; stereo at 1' unspecified",
            "JANUS_H1H2_03": "1'-Et-THCVA; stereo at 1' unspecified",
            "JANUS_H1H2_04": "Methyl ester of H1H2_03; stereo at 1' unspecified",
        },
        "ip_note": "Output paths are gitignored; do not commit SMILES tables of new analogs.",
    }
    return panel, {"panel": panel, "full": df, "meta": meta}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--meta", type=Path, default=DEFAULT_META)
    ap.add_argument("--full-out", type=Path, default=DEFAULT_FULL)
    args = ap.parse_args()

    panel, bundle = build_panel()
    full: pd.DataFrame = bundle["full"]
    meta: dict = bundle["meta"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.out, index=False)
    full.to_csv(args.full_out, index=False)
    args.meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    n_ok = int(full["smiles_valid"].sum())
    n_tot = len(full)
    print(f"Wrote panel: {args.out} ({len(panel)} rows)")
    print(f"Wrote full:  {args.full_out}")
    print(f"Wrote meta:  {args.meta}")
    print(f"Valid SMILES: {n_ok}/{n_tot}")
    for _, r in full.iterrows():
        flag = "OK" if r["smiles_valid"] else "FAIL"
        print(f"  [{flag}] {r['name']} ({r['role']}) hyp={r['hypothesis']}")
    print("SMILES omitted from console (IP policy).")
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    raise SystemExit(main())

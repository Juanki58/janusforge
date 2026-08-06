#!/usr/bin/env python3
"""Generate Track-1 Batch-1 H1–H5 candidate panel (LOCAL / gitignored output).

Builds SMILES by RDKit edits on THCV / THCVA templates from quimioma_semillas.csv.
Writes only under gitignored paths (default: data/libraries/h1_h5_batch1.csv).

IP: do not commit/push the output CSV or derived SDF/PDBQT. Public GitHub must not
receive concrete new-analog SMILES tables.
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
DEFAULT_OUT = ROOT / "data/libraries/h1_h5_batch1.csv"
DEFAULT_META = ROOT / "data/libraries/h1_h5_batch1_meta.json"

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
    # Drop residual dummy atoms if any
    if any(a.GetAtomicNum() == 0 for a in mol.GetAtoms()):
        return None
    return Chem.MolToSmiles(mol, isomericSmiles=True)


def _attach_chain_to_aromatic(mol: Chem.Mol, chain_smiles: str) -> Chem.Mol | None:
    """Replace Ar–CH2–CH2–CH3 with Ar–(chain), where chain_smiles is rooted at the
    atom that bonds to the aromatic carbon (no dummy atoms).

    Examples of chain_smiles:
      'CCCC'   → n-butyl
      'C(C)CC' → 1-methylpropyl (1'-Me)
      'CCCF'   → 3-fluoropropyl (ω-F)
    """
    qry = Chem.MolFromSmarts(_PROPYL_SMARTS)
    if qry is None:
        return None
    matches = mol.GetSubstructMatches(qry)
    if not matches:
        return None
    # Prefer match on the resorcinol ring (carbon ortho/meta pattern with O neighbors)
    match = matches[0]
    ar_idx, *propyl_idxs = match

    chain = Chem.MolFromSmiles(chain_smiles)
    if chain is None or chain.GetNumAtoms() < 1:
        return None

    rw = Chem.RWMol(Chem.Mol(mol))
    # Delete propyl carbons from highest index so indices remain valid
    for idx in sorted(propyl_idxs, reverse=True):
        rw.RemoveAtom(idx)

    # Remap aromatic index after deletions
    offset = sum(1 for i in propyl_idxs if i < ar_idx)
    ar_idx_new = ar_idx - offset

    combo = Chem.RWMol(Chem.CombineMols(rw, chain))
    # Attachment: aromatic atom in first fragment; chain root = first atom of chain
    n_core = rw.GetNumAtoms()
    chain_root = n_core  # first atom of appended chain
    combo.AddBond(ar_idx_new, chain_root, Chem.BondType.SINGLE)
    try:
        Chem.SanitizeMol(combo)
    except Exception:  # noqa: BLE001
        return None
    return combo.GetMol()


def _build_butyl_homolog(thcv: Chem.Mol) -> Chem.Mol | None:
    """H1: C4 (butyl) homolog — Ar–CH2–CH2–CH2–CH3."""
    return _attach_chain_to_aromatic(thcv, "CCCC")


def _build_1prime_methyl(thcv: Chem.Mol) -> Chem.Mol | None:
    """H1: 1'-methyl branch → Ar–CH(CH3)–CH2–CH3.

    Isomer choice: unspecified stereo at 1' (rac-like). Documented in meta.
    """
    return _attach_chain_to_aromatic(thcv, "C(C)CC")


def _build_omega_fluoro(thcv: Chem.Mol) -> Chem.Mol | None:
    """H3: terminal fluoro on propyl = 3'-F (ω-F).

    Honesty: cannabinoid '5\"' numbering is pentyl-centric; on THCV (C3)
    the terminal carbon is 3'. Hypothesis tag keeps 5''-fluoro by analogy
    to THC C5' terminus; chemically this is 3'-fluoro-THCV.
    """
    return _attach_chain_to_aromatic(thcv, "CCCF")


def _build_methyl_ester(thcva: Chem.Mol) -> Chem.Mol | None:
    """H2: THCVA → methyl ester (COOH → COOCH3)."""
    rxn = AllChem.ReactionFromSmarts("[C:1](=[O:2])[OH]>>[C:1](=[O:2])OC")
    if rxn is None or not thcva.HasSubstructMatch(Chem.MolFromSmarts("C(=O)[OH]")):
        return None
    outs = rxn.RunReactants((thcva,))
    for tup in outs:
        for m in tup:
            smi = _canonicalize(m)
            if smi:
                return Chem.MolFromSmiles(smi)
    return None


def _build_delta9_saturated(thcv: Chem.Mol) -> Chem.Mol | None:
    """H4: saturate the cyclohexene Δ9 olefin (9,10-dihydro-THCV proxy).

    Stereo at the new sp3 centers left unspecified (honest ambiguity).
    """
    rxn = AllChem.ReactionFromSmarts("[C;R;!$(c):1]=[C;R;!$(c):2]>>[C:1]-[C:2]")
    if rxn is None:
        return None
    if not thcv.HasSubstructMatch(Chem.MolFromSmarts("[C;R]=[C;R]")):
        return None
    outs = rxn.RunReactants((thcv,))
    for tup in outs:
        for m in tup:
            smi = _canonicalize(m)
            if smi:
                out = Chem.MolFromSmiles(smi)
                # Must have lost the alicyclic alkene
                if out and not out.HasSubstructMatch(Chem.MolFromSmarts("[C;R]=[C;R]")):
                    return out
    return None


def _build_phenol_omethyl(thcv: Chem.Mol) -> Chem.Mol | None:
    """H5-lite: phenolic O-methyl (mask Ar–OH). Not a true N-heterocycle URB447 import."""
    rxn = AllChem.ReactionFromSmarts("[c:1][OH]>>[c:1]OC")
    if rxn is None:
        return None
    outs = rxn.RunReactants((thcv,))
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
    thcva_smi, thcva = _load_seed("THCVA")

    builders = [
        (
            "JANUS_H1_01",
            "THCV-C4 / CBDB-like",
            "H1",
            "C4 butyl homolog of THCV scaffold (not C5 THC / C7 THCP)",
            lambda: _build_butyl_homolog(thcv),
        ),
        (
            "JANUS_H1_02",
            "THCV-1'-Me",
            "H1",
            "1'-methyl branch on propyl; stereo at 1' unspecified (rac-like choice)",
            lambda: _build_1prime_methyl(thcv),
        ),
        (
            "JANUS_H2_01",
            "THCVA",
            "H2",
            "Δ9-THCVA reused from quimioma / PubChem CID 59444416",
            lambda: Chem.MolFromSmiles(thcva_smi),
        ),
        (
            "JANUS_H2_02",
            "THCVA-OMe",
            "H2",
            "Methyl ester of THCVA (COOH→COOMe)",
            lambda: _build_methyl_ester(thcva),
        ),
        (
            "JANUS_H3_01",
            "3'-F-THCV (ω-F; H3-labeled 5'' by analogy)",
            "H3",
            "Terminal fluoro on C3 chain = chemically 3'-F; '5''-F' is pentyl-analogy label only",
            lambda: _build_omega_fluoro(thcv),
        ),
        (
            "JANUS_H4_01",
            "9,10-dihydro-THCV",
            "H4",
            "Δ9 saturated (anti-flip rigidity proxy); new stereocenters unspecified",
            lambda: _build_delta9_saturated(thcv),
        ),
        (
            "JANUS_H5_01",
            "THCV-OMe (phenol)",
            "H5",
            "Phenolic O-methyl mask — H5-lite polarity; NOT a claimed URB447 N-heterocycle transplant",
            lambda: _build_phenol_omethyl(thcv),
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
        mol = fn()
        smi = _canonicalize(mol) if mol is not None else None
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
        "batch": "h1_h5_batch1",
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
            "JANUS_H1_02": "1'-methyl: Ar–CH(CH3)CH2CH3; stereo at 1' left unspecified",
            "JANUS_H3_01": "Chemically 3'-fluoro-THCV; hypothesis tag 5''-F is pentyl-numbering analogy",
            "JANUS_H4_01": "Δ9 reduction; C9/C10 stereo unspecified",
        },
        "ip_note": "Output paths are gitignored; do not commit SMILES tables of new analogs.",
    }
    return panel, {"panel": panel, "full": df, "meta": meta}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--meta", type=Path, default=DEFAULT_META)
    ap.add_argument(
        "--full-out",
        type=Path,
        default=ROOT / "data/libraries/h1_h5_batch1_full.csv",
        help="Local QC table with hypothesis/validity (gitignored).",
    )
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

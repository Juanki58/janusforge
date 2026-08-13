#!/usr/bin/env python3
"""Generate Track-1 Batch-3 panel: refine JANUS_H1_02 / 1′-Me (LOCAL / gitignored).

Batch 1–2 lesson: only JANUS_H1_02 (1′-Me on THCV) passed the hard gate
marginally; A-ring COOH/COOMe kill CB1; larger 1′ volume (Et/cPr) did not help.
Batch 3 keeps 1′-Me fixed and samples lipophilic-chain / periphery edits
without free acids.

Writes only under gitignored paths (default: data/libraries/h1_h5_batch3.csv).
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
DEFAULT_OUT = ROOT / "data/libraries/h1_h5_batch3.csv"
DEFAULT_META = ROOT / "data/libraries/h1_h5_batch3_meta.json"
DEFAULT_FULL = ROOT / "data/libraries/h1_h5_batch3_full.csv"

# Aromatic carbon bearing a linear n-propyl side chain (THCV).
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


def _build_1prime_methyl(thcv: Chem.Mol) -> Chem.Mol | None:
    """Batch-1 control: Ar–CH(CH3)–CH2–CH3 (1′-Me)."""
    return _attach_chain_to_aromatic(thcv, "C(C)CC")


def _phenol_oalkyl(mol: Chem.Mol | None, alkyl_smarts: str) -> Chem.Mol | None:
    """Phenolic O-alkylation (Ar–OH → Ar–OR). Non-acid periphery.

    alkyl_smarts examples: 'C' → OMe, 'CC' → OEt (appended after O in product).
    """
    if mol is None:
        return None
    rxn = AllChem.ReactionFromSmarts(f"[c:1][OH]>>[c:1]O{alkyl_smarts}")
    if rxn is None:
        return None
    outs = rxn.RunReactants((mol,))
    for tup in outs:
        for m in tup:
            smi = _canonicalize(m)
            if smi:
                return Chem.MolFromSmiles(smi)
    return None


def _phenol_omethyl(mol: Chem.Mol | None) -> Chem.Mol | None:
    return _phenol_oalkyl(mol, "C")


def _phenol_oethyl(mol: Chem.Mol | None) -> Chem.Mol | None:
    return _phenol_oalkyl(mol, "CC")


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

    # Fixed 1′-Me parent (Batch-1 JANUS_H1_02) reused as control + edit base.
    h1_02 = _build_1prime_methyl(thcv)

    builders = [
        (
            "JANUS_H1_02",
            "THCV-1'-Me (Batch1 control)",
            "H1_02 control",
            "Positive control: Batch-1 1'-methyl on THCV (Ar–CH(CH3)CH2CH3). "
            "Stereo at 1' unspecified (rac-like). Regenerated for same-run gate.",
            lambda: h1_02,
        ),
        (
            "JANUS_H1_02a",
            "1'-Me + ω-F chain",
            "H1_02a ω-F",
            "1'-Me retained; chain = Ar–CH(CH3)CH2CH2F (ω-F on C3-like chain). "
            "Stereo at 1' unspecified. Lipophilic terminus fluorination; no acid.",
            lambda: _attach_chain_to_aromatic(thcv, "C(C)CCF"),
        ),
        (
            "JANUS_H1_02b",
            "1'-Me + phenol OMe",
            "H1_02b ether",
            "1'-Me parent + small periphery ether: phenolic O-methyl (Ar–OH→Ar–OMe). "
            "Soft TPSA; NOT A-ring COOH/COOMe. Stereo at 1' unspecified.",
            lambda: _phenol_omethyl(h1_02),
        ),
        (
            "JANUS_H1_02c",
            "1'-Me + chain CF3 terminus",
            "H1_02c chain bioisostere",
            "1'-Me retained; non-polar chain bioisostere Ar–CH(CH3)CH2CF3 "
            "(CF3 terminus vs alkyl). Stereo at 1' unspecified. No free acid.",
            lambda: _attach_chain_to_aromatic(thcv, "C(C)CC(F)(F)F"),
        ),
        (
            "JANUS_H1_02d",
            "1'-Me + F on methyl branch",
            "H1_02d strategic F",
            "Strategic F on chain: Ar–CH(CH2F)CH2CH3 (fluoromethyl at 1'-branch). "
            "Ring Ar–F ortho-phenol was not a clean unique match on this scaffold; "
            "chain F keeps 1' branching + non-acid polarity. Stereo at 1' unspecified.",
            lambda: _attach_chain_to_aromatic(thcv, "C(CF)CC"),
        ),
        (
            "JANUS_H1_02e",
            "1'-Me + phenol OEt",
            "H1_02e phenol bioisostere",
            "1'-Me + phenol→OEt (ethyl ether bioisostere of phenol H-bond donor). "
            "Avoids -COOH; stereo at 1' unspecified.",
            lambda: _phenol_oethyl(h1_02),
        ),
        (
            "JANUS_H1_02f",
            "1'-Me + short C2 homolog",
            "H1_02f short chain",
            "Optional coherent: 1'-Me on shorter chain Ar–CH(CH3)CH3 (isopropyl-like). "
            "Tests whether shorter lipophilic arm helps with 1'-Me fixed. "
            "Stereo at 1' unspecified.",
            lambda: _attach_chain_to_aromatic(thcv, "C(C)C"),
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
        # Control kept as design_candidate so it appears in n_cand / can PASS
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
        "batch": "h1_h5_batch3",
        "design_focus": (
            "Refine JANUS_H1_02 (1'-Me fixed): ω-F / short chain / CF3 terminus, "
            "small ethers, strategic Ar–F, phenol bioisosteres — no free COOH/COOMe"
        ),
        "batch12_lesson": (
            "Only JANUS_H1_02 passed hard gate marginally; A-ring acids/esters "
            "kill CB1; 1' Et/cPr volume did not clear gap vs THC."
        ),
        "template_sources": {
            "THCV": "delta9-THCV from data/libraries/quimioma_semillas.csv",
            "THC": "delta9-THC from data/libraries/quimioma_semillas.csv",
        },
        "n_candidates": int((df["role"] == "design_candidate").sum()),
        "n_valid_candidates": int(
            ((df["role"] == "design_candidate") & df["smiles_valid"]).sum()
        ),
        "candidates": meta_candidates,
        "isomer_notes": {
            "JANUS_H1_02": "1'-Me Ar–CH(CH3)CH2CH3; stereo at 1' unspecified (rac-like)",
            "JANUS_H1_02a": "1'-Me + ω-F Ar–CH(CH3)CH2CH2F; stereo at 1' unspecified",
            "JANUS_H1_02b": "1'-Me + ArOMe; stereo at 1' unspecified",
            "JANUS_H1_02c": "1'-Me + CF3 terminus Ar–CH(CH3)CH2CF3; stereo at 1' unspecified",
            "JANUS_H1_02d": (
                "Ar–CH(CH2F)CH2CH3; stereo at 1' unspecified "
                "(chain F; Ar–F ortho-phenol skipped — no clean unique match)"
            ),
            "JANUS_H1_02e": "1'-Me + ArOEt; stereo at 1' unspecified",
            "JANUS_H1_02f": "1'-Me short Ar–CH(CH3)CH3; stereo at 1' unspecified",
        },
        "forbidden": "No free -COOH / -COOMe on A-ring (Batch-2 lesson).",
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
        hyp = str(r["hypothesis"]).replace("\u03c9", "omega")
        print(f"  [{flag}] {r['name']} ({r['role']}) hyp={hyp}")
    print("SMILES omitted from console (IP policy).")
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    raise SystemExit(main())

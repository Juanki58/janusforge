#!/usr/bin/env python3
"""Build local Option D Batch-2 panel: URB447 minimal SAR + refs (LOCAL / gitignored).

Around URB447 (quimioma seed) generate ~15–40 small-substituent analogs with
publishable IDs (JANUS_D2_XX). Refs: URB447, GW405833, delta9-THCV, delta9-THC.

Writes gitignored CSVs under data/libraries/option_d_batch2*.csv.
IP: do not print/commit/push SMILES of design candidates.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data/libraries/quimioma_semillas.csv"
OUT = ROOT / "data/libraries/option_d_batch2.csv"
OUT_FULL = ROOT / "data/libraries/option_d_batch2_full.csv"
OUT_META = ROOT / "data/libraries/option_d_batch2_meta.json"

# Published Yin-Yang PASS ref from Batch 1 (PubChem CID 9911463)
GW405833_SMILES = "CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4"


def _load_seed(name: str) -> tuple[str, Chem.Mol]:
    df = pd.read_csv(SEED)
    hit = df[df["name"] == name]
    if hit.empty:
        raise KeyError(f"{name} not in {SEED}")
    smiles = str(hit.iloc[0]["smiles"])
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES for {name}")
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


def _replace_once(mol: Chem.Mol, smarts_from: str, smarts_to: str) -> Chem.Mol | None:
    qry = Chem.MolFromSmarts(smarts_from)
    repl = Chem.MolFromSmiles(smarts_to)
    if qry is None or repl is None:
        return None
    products = AllChem.ReplaceSubstructs(mol, qry, repl, replaceAll=False)
    if not products:
        return None
    return products[0]


def _rxn_first(mol: Chem.Mol, smarts: str) -> Chem.Mol | None:
    rxn = AllChem.ReactionFromSmarts(smarts)
    if rxn is None:
        return None
    outs = rxn.RunReactants((mol,))
    for tup in outs:
        for m in tup:
            smi = _canonicalize(m)
            if smi:
                return Chem.MolFromSmiles(smi)
    return None


def _c5_targets(mol: Chem.Mol) -> list[tuple[int, int]]:
    """Pyrrole C5 (aromatic C next to N) bearing a terminal methyl → (c_idx, me_idx)."""
    targets: list[tuple[int, int]] = []
    for a in mol.GetAtoms():
        if not (a.GetIsAromatic() and a.IsInRingSize(5) and a.GetAtomicNum() == 6):
            continue
        if not any(n.GetAtomicNum() == 7 for n in a.GetNeighbors()):
            continue
        mes = [
            n
            for n in a.GetNeighbors()
            if n.GetAtomicNum() == 6
            and n.GetDegree() == 1
            and not n.GetIsAromatic()
        ]
        if len(mes) == 1:
            targets.append((a.GetIdx(), mes[0].GetIdx()))
    return targets


def _edit_c5(mol: Chem.Mol, fragment_smiles: str | None) -> Chem.Mol | None:
    """Replace C5–Me with C5–fragment (fragment root = attachment). None → desmethyl."""
    targets = _c5_targets(mol)
    if not targets:
        return None
    c_idx, me_idx = targets[0]
    rw = Chem.RWMol(Chem.Mol(mol))
    rw.RemoveAtom(me_idx)
    if me_idx < c_idx:
        c_idx -= 1
    if fragment_smiles is None:
        try:
            Chem.SanitizeMol(rw)
        except Exception:  # noqa: BLE001
            return None
        return rw.GetMol()
    frag = Chem.MolFromSmiles(fragment_smiles)
    if frag is None:
        return None
    combo = Chem.RWMol(Chem.CombineMols(rw, frag))
    combo.AddBond(c_idx, rw.GetNumAtoms(), Chem.BondType.SINGLE)
    try:
        Chem.SanitizeMol(combo)
    except Exception:  # noqa: BLE001
        return None
    return combo.GetMol()


def _row(
    name: str,
    common: str,
    smiles: str | None,
    role: str,
    hypothesis: str,
    notes: str,
) -> dict:
    ok = bool(smiles)
    return {
        "name": name,
        "common_name": common,
        "smiles": smiles or "",
        "role": role,
        "hypothesis": hypothesis,
        "smiles_valid": ok,
        "notes": notes,
        "key_ref": "option_d_batch2 URB447 SAR (local)",
        "doi_or_url": "",
    }


def build_analogs(urb: Chem.Mol) -> list[dict]:
    """Minimal substituent edits; IDs only in public reports."""
    specs: list[tuple[str, str, str, Chem.Mol | None]] = []

    # --- N-benzyl para-halo / isosteres (Cl of URB447) ---
    para_swaps = [
        ("JANUS_D2_01", "NBn_pF", "[Cl]", "F", "para-F N-benzyl"),
        ("JANUS_D2_02", "NBn_pBr", "[Cl]", "Br", "para-Br N-benzyl"),
        ("JANUS_D2_03", "NBn_pMe", "[Cl]", "C", "para-Me N-benzyl"),
        ("JANUS_D2_04", "NBn_pOMe", "[Cl]", "OC", "para-OMe N-benzyl"),
        ("JANUS_D2_05", "NBn_pCF3", "[Cl]", "C(F)(F)F", "para-CF3 N-benzyl"),
        ("JANUS_D2_06", "NBn_pCN", "[Cl]", "C#N", "para-CN N-benzyl"),
        ("JANUS_D2_07", "NBn_H", "[Cl]", "[H]", "des-Cl N-benzyl"),
    ]
    for name, hyp, fr, to, note in para_swaps:
        if to == "[H]":
            m = _rxn_first(urb, "[c:1][Cl]>>[c:1][H]")
        else:
            m = _replace_once(urb, fr, to)
            m = Chem.MolFromSmiles(_canonicalize(m) or "") if m is not None else None
        specs.append((name, hyp, note, m))

    # meta-Cl / ortho-Cl isomers via rebuild from URB SMILES edits (reaction)
    # Move Cl: para→meta and para→ortho on N-benzyl ring
    m_meta = _rxn_first(
        urb,
        "[n:1][CH2:2][c:3]1[c:4][c:5][c:6]([Cl])[c:7][c:8]1>>"
        "[n:1][CH2:2][c:3]1[c:4][c:5]([Cl])[c:6][c:7][c:8]1",
    )
    specs.append(("JANUS_D2_08", "NBn_mCl", "meta-Cl N-benzyl isomer", m_meta))

    m_ortho = _rxn_first(
        urb,
        "[n:1][CH2:2][c:3]1[c:4][c:5][c:6]([Cl])[c:7][c:8]1>>"
        "[n:1][CH2:2][c:3]1[c:4]([Cl])[c:5][c:6][c:7][c:8]1",
    )
    specs.append(("JANUS_D2_09", "NBn_oCl", "ortho-Cl N-benzyl isomer", m_ortho))

    # N-benzyl → N-phenethyl (one-carbon linker)
    m_pe = _rxn_first(
        urb,
        "[n:1][CH2:2][c:3]>>[n:1][CH2][CH2][c:3]",
    )
    specs.append(("JANUS_D2_10", "N_phenethyl", "N-phenethyl linker (+CH2)", m_pe))

    # --- C5-methyl edits (pyrrole α-Me) via RWMol ---
    for name, hyp, frag, note in [
        ("JANUS_D2_11", "C5_Et", "CC", "C5-Me→Et"),
        ("JANUS_D2_12", "C5_nPr", "CCC", "C5-Me→nPr"),
        ("JANUS_D2_13", "C5_iPr", "C(C)C", "C5-Me→iPr"),
        ("JANUS_D2_14", "C5_H", None, "C5-desmethyl"),
        ("JANUS_D2_15", "C5_CF3", "C(F)(F)F", "C5-Me→CF3"),
    ]:
        specs.append((name, hyp, note, _edit_c5(urb, frag)))

    # --- C3-amino edits ---
    specs.append(
        (
            "JANUS_D2_16",
            "NHMe",
            "C3-NH2→NHMe",
            _rxn_first(urb, "[c:1][NH2]>>[c:1][NH]C"),
        )
    )
    specs.append(
        (
            "JANUS_D2_17",
            "NMe2",
            "C3-NH2→NMe2",
            _rxn_first(urb, "[c:1][NH2]>>[c:1]N(C)C"),
        )
    )

    # --- Benzoyl (C4) para-substitutions ---
    benzoyl_para = [
        ("JANUS_D2_18", "Bz_pF", "F", "benzoyl para-F"),
        ("JANUS_D2_19", "Bz_pCl", "Cl", "benzoyl para-Cl"),
        ("JANUS_D2_20", "Bz_pMe", "C", "benzoyl para-Me"),
        ("JANUS_D2_21", "Bz_pOMe", "OC", "benzoyl para-OMe"),
        ("JANUS_D2_22", "Bz_pCF3", "C(F)(F)F", "benzoyl para-CF3"),
    ]
    for name, hyp, sub, note in benzoyl_para:
        m = _rxn_first(
            urb,
            f"[C:1](=O)[c:2]1[c:3][c:4][c:5][c:6][c:7]1>>"
            f"[C:1](=O)[c:2]1[c:3][c:4][c:5]({sub})[c:6][c:7]1",
        )
        specs.append((name, hyp, note, m))

    # --- C2-phenyl para-substitutions ---
    c2_para = [
        ("JANUS_D2_23", "C2Ph_pF", "F", "C2-Ph para-F"),
        ("JANUS_D2_24", "C2Ph_pCl", "Cl", "C2-Ph para-Cl"),
        ("JANUS_D2_25", "C2Ph_pMe", "C", "C2-Ph para-Me"),
        ("JANUS_D2_26", "C2Ph_pOMe", "OC", "C2-Ph para-OMe"),
    ]
    for name, hyp, sub, note in c2_para:
        m = _rxn_first(
            urb,
            f"[n;r5:10][c;r5:1]([c:2]1[c:3][c:4][c:5][c:6][c:7]1)>>"
            f"[n;r5:10][c;r5:1]([c:2]1[c:3][c:4][c:5]({sub})[c:6][c:7]1)",
        )
        specs.append((name, hyp, note, m))

    # Dual minimal combos (selected)
    base_pf = _replace_once(urb, "[Cl]", "F")
    if base_pf is not None:
        smi = _canonicalize(base_pf)
        base_pf = Chem.MolFromSmiles(smi) if smi else None
    m_pf_et = _edit_c5(base_pf, "CC") if base_pf is not None else None
    specs.append(("JANUS_D2_27", "NBn_pF_C5Et", "combo para-F + C5-Et", m_pf_et))

    m_pme_nhme = None
    base_pme = _replace_once(urb, "[Cl]", "C")
    if base_pme is not None:
        smi = _canonicalize(base_pme)
        if smi:
            base_pme = Chem.MolFromSmiles(smi)
            m_pme_nhme = _rxn_first(base_pme, "[c:1][NH2]>>[c:1][NH]C")
    specs.append(
        ("JANUS_D2_28", "NBn_pMe_NHMe", "combo para-Me + NHMe", m_pme_nhme)
    )

    m_bzf_pf = None
    if base_pf is not None:
        m_bzf_pf = _rxn_first(
            base_pf,
            "[C:1](=O)[c:2]1[c:3][c:4][c:5][c:6][c:7]1>>"
            "[C:1](=O)[c:2]1[c:3][c:4][c:5](F)[c:6][c:7]1",
        )
    specs.append(
        ("JANUS_D2_29", "NBn_pF_Bz_pF", "combo para-F NBn + benzoyl para-F", m_bzf_pf)
    )

    specs.append(
        ("JANUS_D2_30", "C5_CH2OH", "C5-Me→CH2OH (polar tip)", _edit_c5(urb, "CO"))
    )

    # Extra small SAR to fill panel (~15–40)
    specs.append(
        (
            "JANUS_D2_31",
            "NBn_pF_NHMe",
            "combo para-F + NHMe",
            _rxn_first(base_pf, "[c:1][NH2]>>[c:1][NH]C") if base_pf else None,
        )
    )
    m_bz_pf = _rxn_first(
        urb,
        "[C:1](=O)[c:2]1[c:3][c:4][c:5][c:6][c:7]1>>"
        "[C:1](=O)[c:2]1[c:3][c:4][c:5](F)[c:6][c:7]1",
    )
    specs.append(
        (
            "JANUS_D2_32",
            "Bz_pF_C5Et",
            "combo benzoyl para-F + C5-Et",
            _edit_c5(m_bz_pf, "CC") if m_bz_pf is not None else None,
        )
    )

    rows: list[dict] = []
    seen: set[str] = set()
    urb_can = _canonicalize(urb)
    if urb_can:
        seen.add(urb_can)

    for name, hyp, note, mol in specs:
        smi = _canonicalize(mol) if mol is not None else None
        if smi and smi in seen:
            smi = None  # duplicate of parent or prior
        if smi:
            seen.add(smi)
        rows.append(
            _row(
                name,
                f"URB447 analog {hyp}",
                smi,
                "design_candidate",
                hyp,
                note,
            )
        )
    return rows


def main() -> int:
    urb_smi, urb = _load_seed("URB447")
    thcv_smi, _ = _load_seed("delta9-THCV")
    thc_smi, _ = _load_seed("delta9-THC")

    rows: list[dict] = []

    # Seed + published PASS ref + natural refs
    rows.append(
        _row(
            "URB447",
            "URB447",
            urb_smi,
            "design_comparator",
            "URB447_seed",
            "Track D seed; PubChem CID 25195055; LoVerme 2009",
        )
    )
    rows.append(
        _row(
            "GW405833",
            "GW405833",
            GW405833_SMILES,
            "yin_yang_published",
            "YY_GW405833",
            "Batch1 PASS published Yin-Yang; PubChem CID 9911463",
        )
    )
    rows.append(
        _row(
            "delta9-THCV",
            "Δ9-THCV",
            thcv_smi,
            "seed",
            "REF",
            "Gate reference (dual_THCV)",
        )
    )
    rows.append(
        _row(
            "delta9-THC",
            "Δ9-THC",
            thc_smi,
            "anti_seed",
            "REF",
            "Gate reference (dual_THC)",
        )
    )

    analogs = build_analogs(urb)
    rows.extend(analogs)

    full = pd.DataFrame(rows)
    valid_analogs = full[
        (full["role"] == "design_candidate") & full["smiles_valid"]
    ]
    n_valid = int(valid_analogs["smiles_valid"].sum())
    n_fail_build = int(
        ((full["role"] == "design_candidate") & ~full["smiles_valid"]).sum()
    )

    # Drop invalid SMILES from docking panel (keep in full for audit)
    panel = full[full["smiles_valid"]][["name", "common_name", "smiles", "role"]].copy()

    meta = {
        "batch": "option_d_batch2",
        "n_panel_rows": int(len(panel)),
        "n_design_valid": n_valid,
        "n_design_build_fail": n_fail_build,
        "n_refs": 4,
        "roles": panel["role"].value_counts().to_dict(),
        "phase": "light_docking_only",
        "md": "deferred",
        "sources": {
            "URB447": "data/libraries/quimioma_semillas.csv",
            "GW405833": "PubChem CID 9911463",
            "delta9-THCV": "quimioma_semillas.csv",
            "delta9-THC": "quimioma_semillas.csv",
            "analogs": "RDKit edits from URB447 (local only)",
        },
        "ids": panel["name"].tolist(),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT, index=False)
    full.to_csv(OUT_FULL, index=False)
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Status without structures
    print(f"Wrote {OUT} ({len(panel)} ligands; {n_valid} design analogs valid)")
    print(f"Build fails (dropped): {n_fail_build}")
    print(f"Roles: {meta['roles']}")
    for name, role, ok in zip(full["name"], full["role"], full["smiles_valid"], strict=True):
        flag = "ok" if ok else "FAIL_BUILD"
        print(f"  {name}\t{role}\t{flag}")
    return 0 if n_valid >= 15 else 1


if __name__ == "__main__":
    raise SystemExit(main())

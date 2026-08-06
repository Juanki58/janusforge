#!/usr/bin/env python3
"""CSV panel → SDF + PDBQT ligands (pH 7.4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chemistry.prepare_ligands import PROTONATION_NOTE, load_panel_csv, smiles_to_pdbqt


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--csv",
        type=Path,
        default=ROOT / "data/libraries/quimioma_semillas.csv",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "data/processed/panel_ligands",
    )
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--seed", type=int, default=0xF00D)
    args = ap.parse_args()

    df = load_panel_csv(args.csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    print(PROTONATION_NOTE)
    for _, r in df.iterrows():
        name = str(r["name"])
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:80]
        smiles = str(r["smiles"])
        pdbqt = args.out_dir / f"{safe}.pdbqt"
        sdf = args.out_dir / f"{safe}.sdf"
        print(f"  prepare {name} ...", flush=True)
        try:
            meta = smiles_to_pdbqt(
                smiles,
                pdbqt,
                name=name,
                seed=args.seed,
                ph=args.ph,
                sdf_path=sdf,
            )
            meta["role"] = str(r.get("role", ""))
            meta["common_name"] = str(r.get("common_name", ""))
            meta["error"] = None
        except Exception as exc:  # noqa: BLE001
            meta = {
                "name": name,
                "smiles_input": smiles,
                "error": str(exc)[:300],
                "role": str(r.get("role", "")),
            }
            print(f"    FAIL: {exc}", flush=True)
        rows.append(meta)

    meta_path = args.out_dir / "panel_ligands_meta.json"
    meta_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    ok = sum(1 for x in rows if not x.get("error"))
    print(f"OK {ok}/{len(rows)} -> {args.out_dir}")
    print(f"Meta: {meta_path}")
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

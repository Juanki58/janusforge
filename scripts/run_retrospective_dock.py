#!/usr/bin/env python3
"""Dual Vina docking of the 11-compound quimioma panel on CB1 (5TGZ) and CB2 (6PT0)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chemistry.prepare_ligands import load_panel_csv
from src.screening.docking import dock_ligand, resolve_vina


def _load_box(target_key: str, cfg: dict) -> tuple[Path, dict]:
    """Prefer data/targets/<key>/box.json; fallback to config docking.<key>."""
    box_json = ROOT / "data" / "targets" / target_key / "box.json"
    if box_json.exists():
        meta = json.loads(box_json.read_text(encoding="utf-8"))
        rec = Path(meta["receptor_pdbqt"])
        if not rec.is_absolute():
            rec = ROOT / rec
        box = {
            "center_x": meta["center_x"],
            "center_y": meta["center_y"],
            "center_z": meta["center_z"],
            "size_x": meta["size_x"],
            "size_y": meta["size_y"],
            "size_z": meta["size_z"],
        }
        return rec, box

    dock = cfg.get("docking", {})
    t = dock.get(target_key, {})
    if not t.get("receptor") or not t.get("box"):
        raise FileNotFoundError(
            f"Sin box/receptor para {target_key}. Ejecuta scripts/prepare_receptors.py"
        )
    rec = Path(t["receptor"])
    if not rec.is_absolute():
        rec = ROOT / rec
    return rec, dict(t["box"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=ROOT / "configs/cb1_cb2.yaml")
    ap.add_argument(
        "--csv",
        type=Path,
        default=ROOT / "data/libraries/quimioma_semillas.csv",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results/docking/retrospective_panel",
    )
    ap.add_argument("--exhaustiveness", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument(
        "--ligand-dir",
        type=Path,
        default=None,
        help="Optional prebuilt PDBQT cache (default: data/processed/panel_ligands).",
    )
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    dock_cfg = cfg.get("docking", {})
    exhaustiveness = int(
        args.exhaustiveness
        if args.exhaustiveness is not None
        else dock_cfg.get("exhaustiveness", 8)
    )
    num_modes = int(dock_cfg.get("num_modes", 9))
    seed = int(args.seed if args.seed is not None else dock_cfg.get("seed", 42))
    ph = float(dock_cfg.get("ph", 7.4))
    vina_bin = dock_cfg.get("vina_binary")

    try:
        vina = resolve_vina(vina_bin, root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    df = load_panel_csv(args.csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    targets = {}
    for key in ("cb1", "cb2"):
        rec, box = _load_box(key, cfg)
        if not rec.exists():
            print(f"BLOQUEO: receptor ausente {rec}")
            return 2
        targets[key] = {"receptor": rec, "box": box, "work": args.out_dir / key}

    print(f"Vina: {vina}")
    print(f"exhaustiveness={exhaustiveness} seed={seed} num_modes={num_modes} ph={ph}")

    rows = []
    ligand_cache = (
        args.ligand_dir
        if args.ligand_dir is not None
        else ROOT / "data/processed/panel_ligands"
    )
    for i, r in df.iterrows():
        name = str(r["name"])
        smiles = str(r["smiles"])
        role = str(r.get("role", ""))
        common = str(r.get("common_name", ""))
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:80]
        reuse = ligand_cache / f"{safe}.pdbqt"
        row = {
            "name": name,
            "common_name": common,
            "role": role,
            "smiles": smiles,
        }
        for key, meta in targets.items():
            print(f"[{key}] {name} ...", flush=True)
            res = dock_ligand(
                smiles=smiles,
                name=name,
                receptor=meta["receptor"],
                box=meta["box"],
                work_dir=meta["work"],
                vina_path=vina,
                exhaustiveness=exhaustiveness,
                num_modes=num_modes,
                seed=seed,
                ph=ph,
                reuse_ligand_pdbqt=reuse if reuse.exists() else None,
            )
            row[f"{key}_vina"] = res.get("vina_affinity")
            row[f"{key}_error"] = res.get("dock_error")
            row[f"{key}_docked_pdbqt"] = res.get("docked_pdbqt")
            print(f"  {key}_vina={row[f'{key}_vina']} err={row[f'{key}_error']}")
        rows.append(row)
        # checkpoint
        out_csv = args.out_dir / "retrospective_scores.csv"
        pd.DataFrame(rows).to_csv(out_csv, index=False)

    out_csv = args.out_dir / "retrospective_scores.csv"
    out_json = args.out_dir / "retrospective_scores.json"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Scores: {out_csv}")

    n_ok = sum(
        1
        for r in rows
        if r.get("cb1_vina") is not None and r.get("cb2_vina") is not None
    )
    print(f"Docked OK: {n_ok}/{len(rows)}")
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

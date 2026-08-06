#!/usr/bin/env python3
"""Download and prepare CB1 (5TGZ) / CB2 (6PT0) receptors + docking boxes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.screening.receptors import prepare_target


def _load_cfg(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs/cb1_cb2.yaml",
    )
    args = ap.parse_args()
    cfg = _load_cfg(args.config)
    dock = cfg.get("docking", {})
    size = float(dock.get("box_size", 22.0))
    box_size = (size, size, size)

    results = {}
    for key in ("cb1", "cb2"):
        tcfg = cfg["targets"][key]
        pdb_id = str(tcfg["pdb"])
        out_dir = ROOT / "data" / "targets" / key
        lig = tcfg.get("ligand_resname")
        chains = tcfg.get("chains")
        print(f"=== {key.upper()} {pdb_id} ===", flush=True)
        try:
            box = prepare_target(
                pdb_id=pdb_id,
                out_dir=out_dir,
                ligand_resname=lig,
                box_size=box_size,
                chains=chains,
            )
            results[key] = box
            print(
                f"  ligand={box['ligand_resname']} chain={box['ligand_chain']} "
                f"resseq={box['ligand_resseq']} atoms={box['ligand_natoms']}"
            )
            print(
                f"  center=({box['center_x']}, {box['center_y']}, {box['center_z']}) "
                f"size={box['size_x']}"
            )
            print(f"  receptor={box['receptor_pdbqt']}")
        except Exception as exc:  # noqa: BLE001
            results[key] = {"error": str(exc)}
            print(f"  FAIL: {exc}", flush=True)

    summary = ROOT / "data" / "targets" / "receptor_prep_summary.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Summary: {summary}")

    # Patch config docking boxes in-memory dump for transparency
    boxes_yaml = ROOT / "configs" / "docking_boxes_generated.yaml"
    dump = {}
    for key, box in results.items():
        if "error" in box:
            dump[key] = box
        else:
            rec = Path(box["receptor_pdbqt"])
            try:
                rec_s = str(rec.relative_to(ROOT)).replace("\\", "/")
            except ValueError:
                rec_s = str(rec)
            dump[key] = {
                "pdb": box["pdb_id"],
                "receptor_pdbqt": rec_s,
                "box": {
                    "center_x": box["center_x"],
                    "center_y": box["center_y"],
                    "center_z": box["center_z"],
                    "size_x": box["size_x"],
                    "size_y": box["size_y"],
                    "size_z": box["size_z"],
                },
                "ligand_resname": box["ligand_resname"],
                "box_source": box["source"],
            }
    boxes_yaml.write_text(
        "# Generado por scripts/prepare_receptors.py — no editar a mano\n"
        + yaml.safe_dump(dump, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Boxes YAML: {boxes_yaml}")

    failed = [k for k, v in results.items() if "error" in v]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

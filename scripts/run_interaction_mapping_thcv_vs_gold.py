#!/usr/bin/env python3
"""Run THCV vs gold spatial sub-pocket interaction mapping (analysis only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.interaction_mapping import run_interaction_mapping  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out-md",
        type=Path,
        default=ROOT / "results/docking/interaction_mapping_thcv_vs_gold.md",
    )
    ap.add_argument(
        "--out-json",
        type=Path,
        default=ROOT / "results/docking/interaction_mapping_thcv_vs_gold_distances.json",
    )
    args = ap.parse_args()

    payload = run_interaction_mapping(root=ROOT, out_md=args.out_md, out_json=args.out_json)
    print(f"Report: {args.out_md}")
    print(f"JSON: {args.out_json}")

    c3 = payload["cb2_thcv_vs_hu308"]["c3_alkyl_subpocket"]
    print(
        "Key vectors - C3 residual (CB2): "
        f"{c3.get('residual_free_volume_along_c3_vector_A')} A; "
        "C9-HU hydroxymethyl: "
        f"{payload['cb2_thcv_vs_hu308']['c9_c11_zone'].get('c9_methyl_to_hu_hydroxymethyl_O_A')} A"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

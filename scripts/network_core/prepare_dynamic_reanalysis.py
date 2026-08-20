#!/usr/bin/env python3
"""Gate dynamic reanalysis paths; write BLOCKED status if traj/MSM missing.

Thin wrapper around dynamic_pipeline.write_blocked_status.
Protocol: docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import dynamic_pipeline as dp  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    _ = argv
    st = dp.write_blocked_status()
    print(f"[prepare_dynamic_reanalysis] status={st['status']}")
    print(f"[prepare_dynamic_reanalysis] verdict={st['verdict']}")
    print(f"[prepare_dynamic_reanalysis] wrote {dp.STATUS_PATH}")
    for key, info in st["path_check"]["paths"].items():
        flag = "READY" if info["ready"] else "MISSING"
        print(f"  [{flag}] {key}: {info['path']}")
    if st["blocked"]:
        print(
            "[prepare_dynamic_reanalysis] BLOCKED_PENDING_TRAJECTORIES — "
            "fail closed (INDETERMINATE). Run synthetic self-tests via "
            "dynamic_pipeline.py --self-test"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

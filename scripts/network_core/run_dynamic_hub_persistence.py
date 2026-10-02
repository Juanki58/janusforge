#!/usr/bin/env python3
"""P1 technical entry — dynamic hub persistence (blocked without real traj).

Default: refresh BLOCKED status. Optional --self-test runs synthetic null suite.
Never analyzes real .xtc here until paths exist and methodology stays frozen.
Never label outcomes as "switch".

Protocol: docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import dynamic_pipeline as dp  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="P1 entry: status gate + optional synthetic self-tests"
    )
    parser.add_argument(
        "--status-only",
        action="store_true",
        help="Only write dynamic_reanalysis_status.json",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run synthetic null / dual-network / microstate self-tests",
    )
    args = parser.parse_args(argv)

    if not args.status_only and not args.self_test:
        args.status_only = True

    rc = 0
    st = dp.write_blocked_status()
    print(f"[run_dynamic_hub_persistence] status={st['status']}")
    print(f"[run_dynamic_hub_persistence] verdict={st['verdict']}")
    print(f"[run_dynamic_hub_persistence] wrote {dp.STATUS_PATH}")
    print(
        "[run_dynamic_hub_persistence] roadmap: P1 (hubs both nets) -> "
        "P2 (microstate routes) -> P3 (Gi enrichment)"
    )
    if st.get("blocked"):
        print(
            "[run_dynamic_hub_persistence] BLOCKED_PENDING_TRAJECTORIES / "
            "INDETERMINATE — exit 0 (fail closed)."
        )

    if args.self_test:
        print("[run_dynamic_hub_persistence] synthetic self-tests ...")
        payload = dp.run_self_tests()
        for t in payload["tests"]:
            flag = "PASS" if t["passed"] else "FAIL"
            print(f"  [{flag}] {t['name']}")
        if not payload["all_passed"]:
            rc = 1

    return rc


if __name__ == "__main__":
    sys.exit(main())

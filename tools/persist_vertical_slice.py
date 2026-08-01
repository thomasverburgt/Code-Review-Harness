#!/usr/bin/env python3
"""Persist, verify, and replay deterministic vertical-slice executions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import ArtifactLedger, LedgerError
from validate_vertical_slice import FIXTURE_DIR, ROOT, WORKFLOW


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--clearance", default="internal")
    subparsers = parser.add_subparsers(dest="command", required=True)
    persist = subparsers.add_parser("persist")
    persist.add_argument("--run-dir", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--execution-id", required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--execution-id", required=True)
    replay.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = ArtifactLedger(args.ledger_dir, args.clearance)
    try:
        if args.command == "persist":
            artifacts = sorted(FIXTURE_DIR.glob("*.artifact.json"))
            result = ledger.persist_execution(args.run_dir, artifacts, WORKFLOW)
        elif args.command == "verify":
            result = ledger.verify_execution(args.execution_id)
        else:
            result = ledger.replay(args.execution_id, args.output_dir)
    except LedgerError as exc:
        print(json.dumps({"status": "failed", "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

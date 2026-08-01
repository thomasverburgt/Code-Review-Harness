#!/usr/bin/env python3
"""Build or verify the governed legacy-retirement readiness manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "migration" / "retirement-readiness.json"
TRAINING = ROOT / "training" / "agentic-system-curriculum"


def stats(relative: str) -> dict:
    path = ROOT / relative
    files = [item for item in path.rglob("*") if item.is_file()] if path.is_dir() else []
    return {
        "path": relative,
        "exists": path.exists(),
        "file_count": len(files),
        "bytes": sum(item.stat().st_size for item in files),
    }


def manifest() -> dict:
    gates = {
        "compatibility_release_observed": False,
        "gx10_full_regression_passed": False,
        "external_training_archive_selected": False,
        "archive_hash_verification_passed": False,
        "legacy_removal_human_approved": False,
    }
    training_candidates = [
        "training/agentic-system-curriculum/qa-libreoffice",
        "training/agentic-system-curriculum/revised/qa-final",
        "training/agentic-system-curriculum/revised/renders",
        "training/agentic-system-curriculum/condensed/qa",
        "training/agentic-system-curriculum/condensed/qa2",
        "training/agentic-system-curriculum/condensed/qa3",
        "training/agentic-system-curriculum/condensed/renders",
    ]
    return {
        "manifest_version": "1.0.0",
        "decision": "ADR-0032",
        "removal_authorized": all(gates.values()),
        "gates": gates,
        "candidates": {
            "python_compatibility_paths": {
                "paths": ["tools", "src/code_harness/_legacy.py"],
                "state": "retain_compatibility_release_required",
                "rollback": "continue direct tools invocation and package legacy delegation",
            },
            "training_transient_or_archive_paths": {
                "paths": [stats(path) for path in training_candidates],
                "state": "retain_external_archive_not_selected",
                "rollback": "retain current Git paths and release manifests",
            },
            "legacy_evidence_paths": {
                "catalog": "evidence/legacy-catalog.json",
                "state": "retain_immutable_in_place",
                "rollback": "not applicable; no physical migration is authorized",
            },
            "git_unreachable_objects": {
                "state": "local_maintenance_only",
                "tracked_change": False,
                "procedure": "git gc; verify git fsck and reachable history",
            },
        },
    }


def rendered() -> str:
    return json.dumps(manifest(), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = rendered()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != value:
            print("Retirement readiness manifest is stale.")
            return 1
        data = json.loads(value)
        if data["removal_authorized"] and not all(data["gates"].values()):
            print("Retirement readiness authority is inconsistent.")
            return 1
        print("Retirement readiness manifest verified; removal remains gated.")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(value, encoding="utf-8", newline="\n")
    print("Retirement readiness manifest written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


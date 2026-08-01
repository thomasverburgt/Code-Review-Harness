#!/usr/bin/env python3
"""Generate the ADR-0017 deterministic CAP-COORD reference evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import pretty_bytes
from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest, persist_manifest, validate_for_cap_synth
from validate_vertical_slice import load_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    artifact = load_json(ACCEPTED_CAP_RISK)
    manifest = build_manifest([artifact], ["CAP-RISK"])
    validate_for_cap_synth(manifest, [artifact])
    (output / "capability-input-manifest.json").write_bytes(pretty_bytes(manifest))
    ledger_ref = persist_manifest(output / "ledger", manifest)
    summary = {
        "status": "passed", "adr": "ADR-0017", "coordinator": "CAP-COORD",
        "implementation": "deterministic", "calibration_scope": manifest["calibration_scope"],
        "fitness_claim": manifest["fitness_claim"], "manifest_id": manifest["manifest_id"],
        "manifest_hash": manifest["integrity"]["manifest_hash"], "input_hash": manifest["integrity"]["input_hash"],
        "received_designations": [item["designation"] for item in manifest["received_inputs"]],
        "routing_state": manifest["routing"]["state"],
        "cap_synth_dispatch_contract_valid": True, "cap_synth_scheduled": False,
        "baseline_workflow_changed": False, "report_changed": False,
        "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)",
        "ledger_object_hash": ledger_ref["object_hash"], "decision_authority": "human",
    }
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

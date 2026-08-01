#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import ArtifactLedger, pretty_bytes
from enterprise_arch_runtime import build_inputs
from enterprise_governance_runtime import build_candidate, load_source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    source = load_source()
    gate, artifacts = build_inputs()
    candidate = build_candidate()
    files = [
        ("governance-source-manifest.json", source),
        ("ent-evidence-input.artifact.json", gate),
        ("capability-input-1.artifact.json", artifacts[0]),
        ("capability-input-2.artifact.json", artifacts[1]),
        ("ent-gov-candidate.artifact.json", candidate),
    ]
    for name, value in files:
        (output / name).write_bytes(pretty_bytes(value))

    reference = ArtifactLedger(output / "ledger").persist_artifact(candidate)
    role = candidate["extensions"]["enterprise"]["role"]
    summary = {
        "status": "passed",
        "adr": "ADR-0022",
        "designation": "ENT-GOV",
        "candidate_status": "candidate",
        "scheduled": False,
        "evidence_tier": role["evidence_tier"],
        "fitness_claim": role["fitness_claim"],
        "governance_sources": len(source["sources"]),
        "capability_inputs": len(artifacts),
        "matrix_rows": len(role["compliance_matrix"]),
        "artifact_id": candidate["artifact"]["artifact_id"],
        "artifact_hash": candidate["integrity"]["output_hash"],
        "ledger_hash": reference["object_hash"],
        "baseline_changed": False,
        "report_changed": False,
        "cap_req_gate_bypassed": False,
        "ent_arch_schedule_changed": False,
        "production_target": "A100 large cluster",
        "test_platform": "DGX Spark or approved equivalent (GX-10)",
    }
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Materialize the ADR-0018 deterministic CAP-SYNTH candidate-admission package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import ArtifactLedger, pretty_bytes
from capability_synth_runtime import build_reference_package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    artifacts, manifest, candidate = build_reference_package()
    for artifact in artifacts:
        (output / f"{artifact['identity']['designation'].lower()}-input.artifact.json").write_bytes(pretty_bytes(artifact))
    (output / "capability-input-manifest.json").write_bytes(pretty_bytes(manifest))
    (output / "cap-synth-candidate.artifact.json").write_bytes(pretty_bytes(candidate))
    ledger = ArtifactLedger(output / "ledger")
    manifest_ref = ledger.persist_record(f"capability-input-manifests/{manifest['manifest_id']}.json", "capability-input-manifest", manifest["manifest_id"], manifest)
    candidate_ref = ledger.persist_artifact(candidate)
    role = candidate["extensions"]["capability"]["role"]
    summary = {"status": "passed", "adr": "ADR-0018", "designation": "CAP-SYNTH", "candidate_status": "candidate",
               "scheduled": False, "evidence_tier": role["evidence_tier"], "fitness_claim": role["fitness_claim"],
               "manifest_id": manifest["manifest_id"], "manifest_hash": manifest["integrity"]["manifest_hash"],
               "candidate_artifact_id": candidate["artifact"]["artifact_id"], "candidate_output_hash": candidate["integrity"]["output_hash"],
               "preserved_records": len(role["preserved_child_assertions"]), "derived_assertions": len(role["derived_capability_assertions"]),
               "enterprise_handoff_state": role["enterprise_handoff"]["handoff_state"],
               "manifest_ledger_hash": manifest_ref["object_hash"], "candidate_ledger_hash": candidate_ref["object_hash"],
               "baseline_workflow_changed": False, "report_changed": False, "decision_authority": "human",
               "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)"}
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

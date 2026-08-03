#!/usr/bin/env python3
"""Materialize the ADR-0034 deterministic accepted-live comparison package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from accepted_live_capability_synth_runtime import build_accepted_live_package
from artifact_ledger import ArtifactLedger, pretty_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    artifacts, eligibility, manifest, candidate, compatibility, review = build_accepted_live_package()
    for artifact in artifacts:
        (output / f"{artifact['identity']['designation'].lower()}-input.artifact.json").write_bytes(pretty_bytes(artifact))
    records = {"requirements-eligibility-record.json": eligibility, "capability-input-manifest.json": manifest,
               "cap-synth-candidate.artifact.json": candidate, "enterprise-compatibility.json": compatibility,
               "semantic-review-packet.json": review}
    for name, value in records.items():
        (output / name).write_bytes(pretty_bytes(value))
    ledger = ArtifactLedger(output / "ledger")
    candidate_ref = ledger.persist_artifact(candidate)
    manifest_ref = ledger.persist_record(f"capability-input-manifests/{manifest['manifest_id']}.json",
                                         "capability-input-manifest", manifest["manifest_id"], manifest)
    review_ref = ledger.persist_record(f"capability-synthesis-reviews/{review['packet_id']}.json",
                                       "capability-synthesis-review", review["packet_id"], review)
    role = candidate["extensions"]["capability"]["role"]
    summary = {"status": "passed", "adr": "ADR-0034", "designation": "CAP-SYNTH",
               "package_kind": "deterministic_reference_comparison", "scheduled": False,
               "semantic_acceptance": "awaiting_project_owner_review", "evidence_tier": role["evidence_tier"],
               "fitness_claim": role["fitness_claim"], "candidate_artifact_id": candidate["artifact"]["artifact_id"],
               "candidate_output_hash": candidate["integrity"]["output_hash"], "manifest_id": manifest["manifest_id"],
               "manifest_hash": manifest["integrity"]["manifest_hash"], "eligibility_id": eligibility["eligibility_id"],
               "eligibility_hash": eligibility["record_hash"], "semantic_review_packet_id": review["packet_id"],
               "semantic_review_packet_hash": review["packet_hash"], "candidate_ledger_hash": candidate_ref["object_hash"],
               "manifest_ledger_hash": manifest_ref["object_hash"], "review_ledger_hash": review_ref["object_hash"],
               "baseline_route": "CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK", "baseline_changed": False,
               "report_changed": False, "deployment_effect": "none", "production_target": "A100 large cluster",
               "test_platform": "DGX Spark or approved equivalent (GX-10)"}
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

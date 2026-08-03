#!/usr/bin/env python3
"""Materialize the ADR-0036 deterministic ENT-GOV package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from accepted_live_enterprise_governance_runtime import build_package
from artifact_ledger import ArtifactLedger, pretty_bytes


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    source, eligibility, governance, evidence, gate, manifest, candidate, compatibility, review = build_package()
    records = {"cap-synth-input.artifact.json": source, "cap-synth-eligibility.json": eligibility, "owner-governance-source-manifest.json": governance,
        "governance-evidence-binding-manifest.json": evidence,
        "ent-evidence-gate.artifact.json": gate, "enterprise-governance-input-manifest.json": manifest, "ent-gov-candidate.artifact.json": candidate,
        "downstream-compatibility.json": compatibility, "semantic-review-packet.json": review}
    for name, value in records.items(): (output / name).write_bytes(pretty_bytes(value))
    ledger = ArtifactLedger(output / "ledger"); refs = [ledger.persist_artifact(gate), ledger.persist_artifact(candidate),
        ledger.persist_record(f"governance-sources/{governance['manifest_id']}.json", "governance-source-manifest", governance["manifest_id"], governance),
        ledger.persist_record(f"governance-evidence/{evidence['manifest_id']}.json", "governance-evidence-binding", evidence["manifest_id"], evidence),
        ledger.persist_record(f"enterprise-governance-inputs/{manifest['manifest_id']}.json", "enterprise-governance-input", manifest["manifest_id"], manifest),
        ledger.persist_record(f"enterprise-governance-reviews/{review['packet_id']}.json", "enterprise-governance-review", review["packet_id"], review)]
    row = candidate["extensions"]["enterprise"]["role"]["compliance_matrix"][0]
    summary = {"status": "passed", "adr": "ADR-0036", "package_kind": "deterministic_reference_comparison",
        "candidate_id": candidate["artifact"]["artifact_id"], "candidate_hash": candidate["integrity"]["output_hash"],
        "source_manifest_id": governance["manifest_id"], "source_manifest_hash": governance["manifest_hash"],
        "input_manifest_id": manifest["manifest_id"], "input_manifest_hash": manifest["manifest_hash"],
        "semantic_review_packet_id": review["packet_id"], "semantic_review_packet_hash": review["packet_hash"],
        "matrix_state": row["state"], "semantic_acceptance": "awaiting_project_owner_review", "anti_double_counting": manifest["anti_double_counting"],
        "cap_synth_scheduled": False, "ent_gov_scheduled": False, "report_effect": "none", "deployment_effect": "none",
        "ledger_hashes": [item["object_hash"] for item in refs], "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)"}
    (output / "summary.json").write_bytes(pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())

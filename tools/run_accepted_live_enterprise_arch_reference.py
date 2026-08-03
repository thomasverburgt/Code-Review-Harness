#!/usr/bin/env python3
"""Materialize the ADR-0035 deterministic ENT-ARCH evaluation package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from accepted_live_enterprise_arch_runtime import build_package
from artifact_ledger import ArtifactLedger, pretty_bytes


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    source, eligibility, gate, manifest, candidate, compatibility, review = build_package()
    records = {"cap-synth-input.artifact.json": source, "cap-synth-eligibility.json": eligibility,
               "ent-evidence-gate.artifact.json": gate, "enterprise-architecture-input-manifest.json": manifest,
               "ent-arch-candidate.artifact.json": candidate, "downstream-compatibility.json": compatibility,
               "semantic-review-packet.json": review}
    for name, value in records.items(): (output / name).write_bytes(pretty_bytes(value))
    ledger = ArtifactLedger(output / "ledger")
    refs = [ledger.persist_artifact(gate), ledger.persist_artifact(candidate),
            ledger.persist_record(f"enterprise-architecture-inputs/{manifest['manifest_id']}.json", "enterprise-architecture-input", manifest["manifest_id"], manifest),
            ledger.persist_record(f"enterprise-architecture-reviews/{review['packet_id']}.json", "enterprise-architecture-review", review["packet_id"], review)]
    role = candidate["extensions"]["enterprise"]["role"]
    summary = {"status": "passed", "adr": "ADR-0035", "package_kind": "deterministic_reference_comparison",
               "candidate_id": candidate["artifact"]["artifact_id"], "candidate_hash": candidate["integrity"]["output_hash"],
               "evidence_tier": role["evidence_tier"], "fitness_claim": role["fitness_claim"],
               "input_manifest_id": manifest["manifest_id"], "input_manifest_hash": manifest["manifest_hash"],
               "semantic_review_packet_id": review["packet_id"], "semantic_review_packet_hash": review["packet_hash"],
               "semantic_acceptance": "awaiting_project_owner_review", "anti_double_counting": manifest["anti_double_counting"],
               "cap_synth_scheduled": False, "ent_arch_scheduled": False, "report_effect": "none", "deployment_effect": "none",
               "baseline_route": "CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK", "ledger_hashes": [item["object_hash"] for item in refs],
               "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)"}
    (output / "summary.json").write_bytes(pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())

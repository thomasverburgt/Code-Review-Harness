#!/usr/bin/env python3
"""Materialize ADR-0033 project-owner finalization and CAP-REQ eligibility."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import ArtifactLedger, atomic_write, pretty_bytes
from requirements_acceptance_runtime import build_owner_finalization, derive_eligibility
from validate_vertical_slice import ROOT, load_json


DEFAULT_PACKET = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json"
DEFAULT_RESPONSE = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0020/human-response/requirements-acceptance-response.json"
DEFAULT_OUTPUT = ROOT / "fixtures/cap-req-admission/evidence/2026-08-02/adr0033/project-owner-finalization-corrected"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--response", type=Path, default=DEFAULT_RESPONSE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    packet = load_json(args.packet.resolve())
    response = load_json(args.response.resolve())
    finalization = build_owner_finalization(packet, response)
    eligibility = derive_eligibility(packet, response, finalization)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    ledger = ArtifactLedger(output / "ledger")
    finalization_ref = ledger.persist_record(
        f"project-owner-finalizations/{finalization['finalization_id']}.json",
        "project-owner-finalization",
        finalization["finalization_id"],
        finalization,
        retention_class="architecture-evidence",
    )
    eligibility_ref = ledger.persist_record(
        f"requirements-eligibility/{eligibility['eligibility_id']}.json",
        "requirements-eligibility",
        eligibility["eligibility_id"],
        eligibility,
        retention_class="architecture-evidence",
    )
    atomic_write(output / "project-owner-finalization.json", pretty_bytes(finalization))
    atomic_write(output / "requirements-eligibility-record.json", pretty_bytes(eligibility))
    summary = {
        "adr": "ADR-0033",
        "status": "owner_finalized",
        "project_owner": "thomasverburgt",
        "second_verifier_required": False,
        "response_id": response["response_id"],
        "response_hash": response["response_hash"],
        "finalization_id": finalization["finalization_id"],
        "finalization_hash": finalization["finalization_hash"],
        "eligibility_id": eligibility["eligibility_id"],
        "eligibility_hash": eligibility["record_hash"],
        "eligibility_state": eligibility["state"],
        "cap_synth_scheduled": False,
        "production_target": "A100 large cluster",
        "test_platform": "DGX Spark or approved equivalent (GX-10)",
        "ledger_refs": [finalization_ref, eligibility_ref],
    }
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

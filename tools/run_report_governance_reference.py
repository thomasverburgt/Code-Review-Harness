#!/usr/bin/env python3
"""Materialize the accepted ADR-0012 reference record chain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import ArtifactLedger, pretty_bytes
from report_governance_runtime import ReportGovernanceService, build_report_package
from validate_vertical_slice import ROOT, load_json


ARTIFACT_PATHS = [
    ROOT / "fixtures/vertical-risk-slice/evidence/canonical-spec-secrets-2026-07-31/accepted-spec-secrets.artifact.json",
    ROOT / "fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/accepted-prod-sec.artifact.json",
    ROOT / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-cap-risk.artifact.json",
    ROOT / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-ent-evidence.artifact.json",
    ROOT / "fixtures/vertical-risk-slice/evidence/canonical-ent-sysrisk-2026-07-31/accepted-ent-sysrisk.artifact.json",
]


def actor(subject: str, role: str) -> dict:
    return {"actor_type": "human", "subject_id": subject, "authority_role": role,
            "authentication_provider": "fixture-idp", "assurance_level": "fixture-mfa",
            "session_id": f"SESSION-{subject}"}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pretty_bytes(value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    service = ReportGovernanceService(ArtifactLedger(output / "ledger"))
    package = build_report_package([load_json(path) for path in ARTIFACT_PATHS], "2026-07-31T16:00:00Z")
    service.persist_package(package)
    review, review_bytes = service.create_review_export(package, "2026-07-31T16:01:00Z")
    admin = actor("ADMIN-GOVERNANCE-001", "governance-records-administrator")
    verifier = actor("ADMIN-GOVERNANCE-VERIFY-001", "governance-records-verifier")
    approval = service.record_distribution_approval(
        package, review,
        {"authority_role": "senior-leadership-distribution-authority", "authority_name": "Senior Leadership Review Board"},
        {"source_type": "signed_leadership_memorandum", "source_reference": "MEMO-DIST-001", "source_hash": "sha256:" + "1" * 64},
        admin, ["authorized human experts"], ["controlled distribution"],
        "2026-07-31T16:05:00Z", "2026-07-31T16:06:00Z")
    distribution_verification = service.verify_record(approval, "distribution_approval", verifier, True, True,
                                                      "2026-07-31T16:07:00Z")
    approved_export, approved_bytes = service.create_approved_export(package, approval, distribution_verification,
                                                                     "2026-07-31T16:08:00Z")
    risk_id = next(item["report_item_id"] for item in package["report_items"] if item["kind"] == "risk")
    decision = service.record_external_decision(
        package, approved_export, [risk_id], "risk_disposition",
        {"authority_role": "enterprise-risk-acceptance-authority", "authority_name": "Enterprise Risk Board"},
        {"source_type": "signed_expert_decision", "source_reference": "ERB-DECISION-001", "source_hash": "sha256:" + "2" * 64},
        admin, "accepted", "External experts accepted the documented risk.", ["Track the associated CAPA."],
        "2026-07-31T17:00:00Z", "2026-07-31T17:05:00Z")
    decision_verification = service.verify_record(decision, "external_decision", verifier, True, True,
                                                  "2026-07-31T17:06:00Z")
    reconciliation = service.reconciliation_view(package, [decision], [decision_verification])
    records = {
        "report-package.json": package, "review-export-record.json": review,
        "distribution-approval-attestation.json": approval,
        "distribution-verification.json": distribution_verification,
        "approved-export-record.json": approved_export,
        "external-decision-attestation.json": decision,
        "external-decision-verification.json": decision_verification,
        "reconciliation-view.json": reconciliation,
    }
    for name, value in records.items():
        write_json(output / name, value)
    (output / review["file_name"]).write_bytes(review_bytes)
    (output / approved_export["file_name"]).write_bytes(approved_bytes)
    summary = {"status": "passed", "report_package_id": package["report_package_id"],
               "report_item_count": len(package["report_items"]),
               "review_distribution_state": review["distribution_state"],
               "approved_distribution_state": approved_export["distribution_state"],
               "external_decision_state": decision_verification["verification_state"],
               "effects": [approval["effect"], decision["effect"], decision_verification["effect"]]}
    write_json(output / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

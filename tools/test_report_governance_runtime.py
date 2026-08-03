#!/usr/bin/env python3
"""Conformance tests for ADR-0012 governance and ADR-0033 owner finalization."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from artifact_ledger import ArtifactLedger, content_hash
from report_governance_runtime import ReportGovernanceError, ReportGovernanceService, build_report_package
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


class ReportGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.ledger = ArtifactLedger(Path(self.temp.name) / "ledger")
        self.service = ReportGovernanceService(self.ledger)
        self.sources = [load_json(path) for path in ARTIFACT_PATHS]
        self.package = build_report_package(self.sources, "2026-07-31T16:00:00Z")
        self.service.persist_package(self.package)
        self.review, self.review_bytes = self.service.create_review_export(self.package, "2026-07-31T16:01:00Z")
        self.admin = actor("ADMIN-GOVERNANCE-001", "governance-records-administrator")
        self.verifier = actor("ADMIN-GOVERNANCE-VERIFY-001", "governance-records-verifier")
        self.owner = actor("HUMAN-PROJECT-OWNER-001", "project-owner")
        self.owner["assurance_level"] = "repository-owner-attestation"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def distribution_approval(self) -> dict:
        return self.service.record_distribution_approval(
            self.package, self.review,
            {"authority_role": "senior-leadership-distribution-authority",
             "authority_name": "Senior Leadership Review Board"},
            {"source_type": "signed_leadership_memorandum", "source_reference": "MEMO-DIST-001",
             "source_hash": "sha256:" + "1" * 64},
            self.admin, ["authorized human experts"], ["controlled distribution"],
            "2026-07-31T16:05:00Z", "2026-07-31T16:06:00Z")

    def approved_export(self) -> tuple[dict, dict]:
        approval = self.distribution_approval()
        verification = self.service.verify_record(approval, "distribution_approval", self.verifier,
                                                  True, True, "2026-07-31T16:07:00Z")
        export, _ = self.service.create_approved_export(self.package, approval, verification,
                                                       "2026-07-31T16:08:00Z")
        return export, approval

    def test_report_is_deterministic_complete_and_unmodified(self) -> None:
        replay = build_report_package(self.sources, "2026-07-31T16:00:00Z")
        self.assertEqual(self.package, replay)
        self.assertEqual(self.package["technical_state"], "technically_validated")
        self.assertTrue({"finding", "risk", "capa", "recommendation"}.issubset(
            {item["kind"] for item in self.package["report_items"]}))
        self.assertTrue(self.package["evidence_items"])
        self.assertEqual(len(self.package["source_contexts"]), len(self.sources))
        self.assertTrue(all("methodology" in context for context in self.package["source_contexts"]))
        self.assertEqual(len(self.package["report_items"]), len({i["report_item_id"] for i in self.package["report_items"]}))
        self.assertEqual(self.sources, [load_json(path) for path in ARTIFACT_PATHS])

    def test_review_copy_cannot_be_used_as_approved_distribution(self) -> None:
        self.assertEqual(self.review["distribution_state"], "not_approved_for_distribution")
        self.assertIn(b"NOT APPROVED FOR DISTRIBUTION", self.review_bytes)
        approval = self.distribution_approval()
        rejected = self.service.verify_record(approval, "distribution_approval", self.verifier,
                                              False, True, "2026-07-31T16:07:00Z")
        with self.assertRaises(ReportGovernanceError):
            self.service.create_approved_export(self.package, approval, rejected, "2026-07-31T16:08:00Z")

    def test_distribution_requires_separate_authority_recorder_and_verifier(self) -> None:
        approval = self.distribution_approval()
        self.assertNotEqual(approval["approved_by"]["authority_role"], approval["recorded_by"]["authority_role"])
        with self.assertRaises(ReportGovernanceError):
            self.service.verify_record(approval, "distribution_approval", self.admin,
                                       True, True, "2026-07-31T16:07:00Z")
        verification = self.service.verify_record(approval, "distribution_approval", self.verifier,
                                                  True, True, "2026-07-31T16:07:00Z")
        export, approved_bytes = self.service.create_approved_export(self.package, approval, verification,
                                                                    "2026-07-31T16:08:00Z")
        self.assertEqual(export["distribution_state"], "approved_for_distribution")
        self.assertIn(b"APPROVED FOR DISTRIBUTION", approved_bytes)
        self.assertNotEqual(export["file_hash"], self.review["file_hash"])

    def test_project_owner_can_finalize_distribution_without_second_verifier(self) -> None:
        approval = self.distribution_approval()
        finalization = self.service.finalize_record(
            approval, "distribution_approval", self.owner, True, True, "2026-08-02")
        export, approved_bytes = self.service.create_approved_export(
            self.package, approval, finalization, "2026-08-02T12:00:00Z")
        self.assertEqual(finalization["finalization_state"], "finalized")
        self.assertEqual(export["distribution_state"], "approved_for_distribution")
        self.assertIn(b"APPROVED FOR DISTRIBUTION", approved_bytes)

    def test_external_decision_is_exact_record_only_and_independently_verified(self) -> None:
        export, _ = self.approved_export()
        package_before = copy.deepcopy(self.package)
        item_id = next(i["report_item_id"] for i in self.package["report_items"] if i["kind"] == "risk")
        decision = self.service.record_external_decision(
            self.package, export, [item_id], "risk_disposition",
            {"authority_role": "enterprise-risk-acceptance-authority", "authority_name": "Enterprise Risk Board"},
            {"source_type": "signed_expert_decision", "source_reference": "ERB-DECISION-001",
             "source_hash": "sha256:" + "2" * 64}, self.admin, "accepted",
            "External experts accepted the documented risk.", ["Track the associated CAPA."],
            "2026-07-31T17:00:00Z", "2026-07-31T17:05:00Z")
        self.assertEqual(decision["effect"], "record_only")
        self.assertFalse(decision["original_report_mutated"])
        self.assertEqual(decision["attestation_state"], "recorded_pending_project_owner_finalization")
        pending = self.service.reconciliation_view(self.package, [decision], [])
        self.assertEqual(next(v for v in pending if v["report_item"]["report_item_id"] == item_id)
                         ["external_decisions"][0]["administrative_state"], "recorded_pending_project_owner_finalization")
        verification = self.service.verify_record(decision, "external_decision", self.verifier,
                                                  True, True, "2026-07-31T17:06:00Z")
        reconciled = self.service.reconciliation_view(self.package, [decision], [verification])
        self.assertEqual(next(v for v in reconciled if v["report_item"]["report_item_id"] == item_id)
                         ["external_decisions"][0]["administrative_state"], "verified")
        self.assertEqual(self.package, package_before)

    def test_external_decision_fails_closed_and_is_immutable(self) -> None:
        export, _ = self.approved_export()
        args = dict(package=self.package, approved_export=export,
                    report_item_ids=[self.package["report_items"][0]["report_item_id"]],
                    decision_type="risk_disposition",
                    decided_by={"authority_role": "enterprise-risk-acceptance-authority", "authority_name": "Enterprise Risk Board"},
                    decision_source={"source_type": "signed_expert_decision", "source_reference": "ERB-DECISION-002", "source_hash": "sha256:" + "3" * 64},
                    recorded_by=self.admin, disposition="accepted", rationale="Recorded from signed source.",
                    conditions=[], decided_at="2026-07-31T18:00:00Z", recorded_at="2026-07-31T18:05:00Z")
        first = self.service.record_external_decision(**args)
        self.assertEqual(first, self.service.record_external_decision(**args))
        changed = dict(args, rationale="Changed after recording.")
        with self.assertRaises(ReportGovernanceError):
            self.service.record_external_decision(**changed)
        with self.assertRaises(ReportGovernanceError):
            self.service.record_external_decision(**dict(args, report_item_ids=["RISK:NOT-IN-REPORT"]))
        bad_source = dict(args["decision_source"], source_hash="unhashed")
        with self.assertRaises(ReportGovernanceError):
            self.service.record_external_decision(**dict(args, decision_source=bad_source))
        with self.assertRaises(ReportGovernanceError):
            self.service.record_external_decision(**dict(args, decided_by={"authority_role": "governance-records-administrator", "authority_name": "Admin"}))
        with self.assertRaises(ReportGovernanceError):
            self.service.verify_record(first, "unsupported", self.verifier, True, True, "2026-07-31T18:06:00Z")


if __name__ == "__main__":
    unittest.main(verbosity=2)

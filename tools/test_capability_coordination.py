#!/usr/bin/env python3
"""ADR-0017 deterministic coordination and fail-closed dispatch tests."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from artifact_ledger import content_hash
from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest, persist_manifest, validate_for_cap_synth
from validate_vertical_slice import ROOT, ValidationFailure, load_json


BASELINE = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"
REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"


def rehash(artifact: dict) -> dict:
    artifact["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(artifact)
    return artifact


class CapabilityCoordinationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = load_json(ACCEPTED_CAP_RISK)
        self.manifest = build_manifest([self.artifact], ["CAP-RISK"])

    def test_single_domain_manifest_is_deterministic_mechanical_and_traceable(self) -> None:
        self.assertEqual(self.manifest, build_manifest([self.artifact], ["CAP-RISK"]))
        self.assertEqual(self.manifest["calibration_scope"], "single_domain_mechanical_calibration")
        self.assertEqual(self.manifest["fitness_claim"], "mechanical_coordination_only")
        self.assertEqual(self.manifest["routing"], {"state": "ready_for_cap_synth", "synthesis_dispatch_permitted": True, "consumer": "CAP-SYNTH"})
        records = {(item["record_kind"], item["record_id"]) for item in self.manifest["traceability"]}
        self.assertEqual(records, {("finding", "FINDING-001"), ("risk", "RISK-001"), ("decision_request", "DC-001")})

    def test_dispatch_requires_exact_manifest_and_exact_immutable_artifacts(self) -> None:
        validate_for_cap_synth(self.manifest, [self.artifact])
        mutated_manifest = copy.deepcopy(self.manifest)
        mutated_manifest["routing"]["state"] = "blocked"
        with self.assertRaises(ValidationFailure):
            validate_for_cap_synth(mutated_manifest, [self.artifact])
        mutated_artifact = copy.deepcopy(self.artifact)
        mutated_artifact["findings"][0]["statement"] = "changed after coordination"
        with self.assertRaises(ValidationFailure):
            validate_for_cap_synth(self.manifest, [mutated_artifact])

    def test_missing_input_blocks_and_partial_authorization_does_not_dispatch(self) -> None:
        blocked = build_manifest([self.artifact], ["CAP-RISK", "CAP-REQ"], calibration_scope="declared_multi_domain")
        self.assertEqual(blocked["routing"]["state"], "blocked")
        self.assertFalse(blocked["routing"]["synthesis_dispatch_permitted"])
        authorization = {"authorization_id": "PARTIAL-001", "missing_designations": ["CAP-REQ"],
                         "authority_role": "capability-review-authority", "limitations": ["inventory only; no synthesis"],
                         "expires_at": "2026-08-02T18:00:00Z"}
        incomplete = build_manifest([self.artifact], ["CAP-RISK", "CAP-REQ"], partial_input_authorization=authorization,
                                    calibration_scope="declared_multi_domain")
        self.assertEqual(incomplete["routing"]["state"], "incomplete_authorized")
        self.assertFalse(incomplete["routing"]["synthesis_dispatch_permitted"])
        with self.assertRaises(ValidationFailure):
            validate_for_cap_synth(incomplete, [self.artifact])

    def test_extra_duplicate_stale_and_incompatible_inputs_fail_closed(self) -> None:
        extra = copy.deepcopy(self.artifact)
        extra["identity"]["designation"] = "CAP-REQ"
        extra["identity"]["agent_uuid"] = "9a82a407-38f6-4abe-9ef8-49f0fd256e67"
        extra["artifact"]["artifact_id"] = "17000000-0000-4000-8000-000000000001"
        rehash(extra)
        with self.assertRaises(ValidationFailure):
            build_manifest([self.artifact, extra], ["CAP-RISK"])
        with self.assertRaises(ValidationFailure):
            build_manifest([self.artifact, self.artifact], ["CAP-RISK"])
        with self.assertRaises(ValidationFailure):
            build_manifest([self.artifact], ["CAP-RISK"], freshness={"CAP-RISK": "stale"})
        with self.assertRaises(ValidationFailure):
            build_manifest([self.artifact], ["CAP-RISK"], compatibility={"CAP-RISK": "incompatible"})

    def test_mutated_or_incomplete_artifact_fails_before_manifest(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["findings"][0]["statement"] = "unauthorized mutation"
        with self.assertRaises(ValidationFailure):
            build_manifest([mutated], ["CAP-RISK"])
        incomplete = copy.deepcopy(self.artifact)
        incomplete["artifact"]["lifecycle_state"] = "incomplete_input"
        rehash(incomplete)
        with self.assertRaises(ValidationFailure):
            build_manifest([incomplete], ["CAP-RISK"])
        with self.assertRaises(ValidationFailure):
            build_manifest([self.artifact], ["CAP-RISK"], calibration_scope="declared_multi_domain")

    def test_conflicts_are_preserved_without_semantic_resolution(self) -> None:
        conflicted = copy.deepcopy(self.artifact)
        conflicted["conflicts"] = [{"conflict_id": "CONFLICT-001", "statement": "Two reviewers disagree.", "evidence_refs": ["UDS-0001"]}]
        rehash(conflicted)
        manifest = build_manifest([conflicted], ["CAP-RISK"])
        self.assertEqual(manifest["preserved_conflicts"][0]["statement"], "Two reviewers disagree.")
        self.assertIn(("conflict", "CONFLICT-001"), {(item["record_kind"], item["record_id"]) for item in manifest["traceability"]})

    def test_manifest_persists_as_immutable_ledger_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = persist_manifest(Path(directory), self.manifest)
            second = persist_manifest(Path(directory), self.manifest)
            self.assertEqual(first, second)

    def test_increment_does_not_modify_baseline_report_or_schedule_cap_synth(self) -> None:
        before = (BASELINE.read_bytes(), REPORT.read_bytes())
        build_manifest([self.artifact], ["CAP-RISK"])
        self.assertEqual(before, (BASELINE.read_bytes(), REPORT.read_bytes()))
        workflow = load_json(BASELINE)
        self.assertNotIn("CAP-SYNTH", {node["designation"] for node in workflow["nodes"]})
        spec = (ROOT / "agents/capability/capability-coordinator.md").read_text(encoding="utf-8")
        self.assertIn("no model prompt", spec)
        self.assertNotIn("BEGIN CAP-COORD PROMPT", spec)


if __name__ == "__main__":
    unittest.main(verbosity=2)

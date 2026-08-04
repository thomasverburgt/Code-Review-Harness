#!/usr/bin/env python3
"""Tests for the ADR-0039 specialist human-shadow calibration boundary."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from artifact_ledger import content_hash
from run_specialist_shadow_calibration_reference import (
    AGENT_UUID,
    CONTROL_REVOKED_AT,
    CREATED_AT,
    GENERATED_AT,
    IMMUTABLE_REVISION,
    PRODUCT_ID,
    REPOSITORY_URI,
    build_candidate,
    build_locator,
    build_manifest,
    build_response,
    generate,
)
from specialist_shadow_calibration_runtime import (
    ROOT,
    SpecialistShadowCalibrationError,
    build_control_record,
    build_metrics,
    build_review_packet,
    canonical_file_hash,
    focus_material,
    seal_hash,
    validate_candidate_artifact,
    validate_control_record,
    validate_manifest,
    validate_metrics,
    validate_review_response,
)


class SpecialistShadowCalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = build_manifest()
        self.candidate = build_candidate(self.manifest)
        self.locators = [
            build_locator("EVIDENCE-DEPS-BUILD-001", 2, 'requires = ["setuptools"]', "build-system"),
            build_locator("EVIDENCE-DEPS-DOCS-001", 15, 'docs = ["python-docx==1.2.0"]', "project.optional-dependencies"),
        ]
        self.packet = build_review_packet(self.manifest, self.candidate, self.locators, GENERATED_AT)

    def test_reference_packet_is_exact_reviewable_and_comparison_only(self) -> None:
        self.assertEqual(self.packet["reviewability_state"], "ready_for_human_shadow_review")
        self.assertEqual(len(self.packet["items"]), 5)
        self.assertIn("general_engineering_intern", self.packet["permitted_reviewer_tracks"])
        self.assertEqual(self.packet["candidate_artifact_hash"], content_hash(self.candidate))
        self.assertTrue(self.packet["lifecycle"]["comparison_only"])
        for name in ("scheduled", "product_fan_in_eligible", "report_eligible", "deployment_authorized", "a100_production_authorized"):
            self.assertFalse(self.packet["lifecycle"][name])
        self.assertTrue(all(item["locators"] for item in self.packet["items"]))

    def test_focus_binding_tampering_fails_closed(self) -> None:
        tampered = copy.deepcopy(self.manifest)
        tampered["focus_binding"]["compiled_prompt_focus_hash"] = "sha256:" + "1" * 64
        tampered = seal_hash(tampered, "manifest_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "focus binding"):
            validate_manifest(tampered)

    def test_missing_locator_blocks_review_and_response(self) -> None:
        blocked = build_review_packet(self.manifest, self.candidate, [], GENERATED_AT)
        self.assertEqual(blocked["reviewability_state"], "blocked_missing_locator")
        self.assertTrue(blocked["blocking_issues"])
        response = copy.deepcopy(build_response(self.packet))
        response["packet_id"] = blocked["packet_id"]
        response["packet_hash"] = blocked["packet_hash"]
        response = seal_hash(response, "response_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "blocked packet"):
            validate_review_response(blocked, response)

    def test_unauthorized_candidate_effects_and_consumers_fail_closed(self) -> None:
        scheduled = copy.deepcopy(self.candidate)
        scheduled["execution"]["scheduled"] = True
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "comparison-only"):
            validate_candidate_artifact(self.manifest, scheduled)
        consumer = copy.deepcopy(self.candidate)
        consumer["consumers"] = ["PROD-SEC"]
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "unauthorized downstream consumer"):
            validate_candidate_artifact(self.manifest, consumer)

    def test_raw_restricted_marker_is_rejected(self) -> None:
        unsafe = copy.deepcopy(self.candidate)
        unsafe["observations"][0]["fact"] = "BEGIN PRIVATE KEY"
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "prohibited raw restricted content"):
            validate_candidate_artifact(self.manifest, unsafe)

    def test_restricted_evidence_cannot_route_to_general_intern(self) -> None:
        restricted = copy.deepcopy(self.manifest)
        restricted["evidence_population"][0]["classification"] = "restricted"
        restricted = seal_hash(restricted, "manifest_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "restricted evidence"):
            validate_manifest(restricted)

    def test_review_requires_exact_item_coverage_and_authorized_access(self) -> None:
        response = build_response(self.packet)
        missing = copy.deepcopy(response)
        missing["item_reviews"] = missing["item_reviews"][:-1]
        missing = seal_hash(missing, "response_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "every packet item"):
            validate_review_response(self.packet, missing)
        unauthorized = copy.deepcopy(response)
        unauthorized["reviewer"]["authorized_classifications"] = ["internal"]
        unauthorized = seal_hash(unauthorized, "response_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "lacks the packet classification"):
            validate_review_response(self.packet, unauthorized)

    def test_metrics_are_derived_and_never_establish_correctness(self) -> None:
        response = build_response(self.packet)
        metrics = build_metrics(self.packet, [response], CONTROL_REVOKED_AT)
        validate_metrics(self.packet, [response], metrics)
        self.assertFalse(metrics["correctness_established"])
        self.assertEqual(metrics["item_count"], 5)
        self.assertEqual(metrics["review_count"], 1)
        self.assertEqual(sum(metrics["disposition_counts"].values()), 5)
        self.assertEqual(metrics["review_duration_seconds"]["total"], 1800.0)

    def test_project_owner_enable_and_revoke_are_bounded(self) -> None:
        enable = build_control_record(self.manifest, "enable_calibration", CREATED_AT, "thomasverburgt", "ADR-0039")
        revoke = build_control_record(self.manifest, "revoke_calibration", CONTROL_REVOKED_AT, "thomasverburgt", "ADR-0039 rollback")
        validate_control_record(self.manifest, enable)
        validate_control_record(self.manifest, revoke)
        self.assertTrue(enable["effects"]["dispatch_enabled"])
        self.assertFalse(revoke["effects"]["dispatch_enabled"])
        for record in (enable, revoke):
            for name in ("scheduled", "product_fan_in_eligible", "report_eligible", "deployment_authorized", "a100_production_authorized"):
                self.assertFalse(record["effects"][name])

    def test_all_registered_specialists_have_exact_focus_sources(self) -> None:
        registry = json.loads((ROOT / "agents" / "agent-identities.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "agents" / "focus-profiles" / "catalog.json").read_text(encoding="utf-8"))
        specialists = {item["designation"]: item for item in registry["agents"] if item["layer"] == "specialist"}
        profiles = {item["designation"]: item for item in catalog["profiles"] if item["layer"] == "specialist"}
        self.assertEqual(set(specialists), set(profiles))
        self.assertEqual(len(specialists), 22)
        for designation, agent in specialists.items():
            entry = profiles[designation]
            profile_path = ROOT / entry["path"]
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            source_path = ROOT / profile["source"]["specification"]
            self.assertEqual(entry["agent_uuid"], agent["agent_uuid"])
            self.assertEqual(entry["sha256"], canonical_file_hash(profile_path))
            self.assertEqual(profile["source"]["specification_sha256"], canonical_file_hash(source_path))
            self.assertTrue(focus_material(profile))
            self.assertTrue(profile["prompt_binding"]["compression_protected_elements"])

    def test_reference_generation_persists_immutable_rollback_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "gold"
            summary = generate(output)
            self.assertEqual(summary["status"], "persisted_and_revoked")
            self.assertEqual(summary["record_count"], 9)
            self.assertTrue((output / "ledger" / "objects" / "sha256").is_dir())
            self.assertTrue((output / "control-revoke.json").is_file())
            self.assertTrue((output / "human-shadow-review-packet.md").is_file())
            for name in ("scheduled", "product_fan_in_eligible", "deployment_authorized", "a100_production_authorized"):
                self.assertFalse(summary[name])


if __name__ == "__main__":
    unittest.main()

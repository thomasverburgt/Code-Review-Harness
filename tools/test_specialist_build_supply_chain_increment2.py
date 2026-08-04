#!/usr/bin/env python3
"""Regression and fail-closed tests for ADR-0039 Increment 2."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from run_specialist_build_supply_chain_increment2 import CONFIG, GENERATED_AT, build_candidate, build_manifest, generate, locator
from specialist_shadow_calibration_runtime import SpecialistShadowCalibrationError, build_review_packet, seal_hash, validate_candidate_artifact, validate_manifest


class SpecialistBuildSupplyChainIncrement2Tests(unittest.TestCase):
    def test_all_candidates_are_distinct_reviewable_deferred_and_non_authoritative(self) -> None:
        packet_ids = set()
        for designation, cfg in CONFIG.items():
            manifest = build_manifest(designation)
            candidate = build_candidate(manifest)
            packet = build_review_packet(manifest, candidate, [locator(item) for item in cfg["evidence"]], GENERATED_AT)
            packet_ids.add(packet["packet_id"])
            self.assertEqual(candidate["extensions"]["specialist"]["role"]["designation"], designation)
            self.assertEqual(packet["reviewability_state"], "ready_for_human_shadow_review")
            self.assertFalse(packet["lifecycle"]["scheduled"])
            self.assertFalse(packet["lifecycle"]["product_fan_in_eligible"])
            self.assertFalse(packet["lifecycle"]["report_eligible"])
            self.assertFalse(packet["lifecycle"]["deployment_authorized"])
            self.assertFalse(packet["lifecycle"]["a100_production_authorized"])
        self.assertEqual(len(packet_ids), 3)

    def test_execution_binding_mutation_fails_closed(self) -> None:
        manifest = build_manifest("SPEC-CONTAINER")
        manifest["execution_bindings"]["prompt"]["hash"] = "sha256:" + "1" * 64
        manifest = seal_hash(manifest, "manifest_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "Increment 2 specialist-candidate files"):
            validate_manifest(manifest)

    def test_container_source_cannot_claim_deployment_readiness(self) -> None:
        manifest = build_manifest("SPEC-CONTAINER")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["images"][0]["deployment_readiness"] = "demonstrated"
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "verified artifact, scan, and runtime evidence"):
            validate_candidate_artifact(manifest, candidate)

    def test_cicd_configuration_cannot_claim_effective_gate(self) -> None:
        manifest = build_manifest("SPEC-CICD")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["pipelines"][0]["gate_effectiveness"] = "demonstrated"
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "configuration alone"):
            validate_candidate_artifact(manifest, candidate)

    def test_cicd_configuration_cannot_create_repeatability_measure(self) -> None:
        manifest = build_manifest("SPEC-CICD")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["measures"]["repeatability"] = 1.0
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "completed admitted runs"):
            validate_candidate_artifact(manifest, candidate)

    def test_iac_source_cannot_claim_observed_state(self) -> None:
        manifest = build_manifest("SPEC-IAC")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["modules"][0]["observed_state"] = "matches_desired"
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "observed state requires"):
            validate_candidate_artifact(manifest, candidate)

    def test_iac_source_cannot_claim_idempotency_confidence(self) -> None:
        manifest = build_manifest("SPEC-IAC")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["measures"]["idempotency_confidence"] = 0.9
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "apply evidence"):
            validate_candidate_artifact(manifest, candidate)

    def test_role_evidence_cannot_escape_manifest(self) -> None:
        manifest = build_manifest("SPEC-IAC")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["modules"][0]["evidence_refs"] = ["INVENTED-EVIDENCE"]
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "outside the manifest"):
            validate_candidate_artifact(manifest, candidate)

    def test_generation_is_deterministic_and_review_stays_deferred(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = generate(Path(first)); two = generate(Path(second))
            self.assertEqual(one, two)
            self.assertTrue(one["human_review_deferred"])
            self.assertEqual(one["state"], "candidate_packets_retained_human_review_deferred")
            for cfg in CONFIG.values():
                left = Path(first) / cfg["slug"] / "human-shadow-review-packet.json"
                right = Path(second) / cfg["slug"] / "human-shadow-review-packet.json"
                self.assertEqual(left.read_bytes(), right.read_bytes())


if __name__ == "__main__":
    unittest.main()

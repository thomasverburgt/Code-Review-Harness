#!/usr/bin/env python3
"""Regression and fail-closed tests for ADR-0039 Increment 1."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from run_specialist_static_evidence_increment1 import CONFIG, GENERATED_AT, build_candidate, build_manifest, generate, locator
from specialist_shadow_calibration_runtime import (
    SpecialistShadowCalibrationError, build_review_packet, seal_hash,
    validate_candidate_artifact, validate_manifest,
)


class SpecialistStaticEvidenceIncrement1Tests(unittest.TestCase):
    def test_all_three_candidates_are_distinct_reviewable_and_non_authoritative(self) -> None:
        packets = {}
        for designation, cfg in CONFIG.items():
            manifest = build_manifest(designation)
            candidate = build_candidate(manifest)
            packet = build_review_packet(manifest, candidate, [locator(item) for item in cfg["evidence"]], GENERATED_AT)
            packets[designation] = packet
            self.assertEqual(packet["reviewability_state"], "ready_for_human_shadow_review")
            self.assertEqual(len(packet["items"]), 4)
            self.assertEqual(candidate["extensions"]["specialist"]["role"]["designation"], designation)
            self.assertEqual(candidate["consumers"], ["human-shadow-review-only"])
            self.assertFalse(packet["lifecycle"]["scheduled"])
            self.assertFalse(packet["lifecycle"]["product_fan_in_eligible"])
            self.assertFalse(packet["lifecycle"]["report_eligible"])
            self.assertFalse(packet["lifecycle"]["deployment_authorized"])
            self.assertFalse(packet["lifecycle"]["a100_production_authorized"])
        self.assertEqual(len({packet["packet_id"] for packet in packets.values()}), 3)
        questions = {CONFIG[name]["finding"] for name in packets}
        self.assertEqual(len(questions), 3)

    def test_execution_binding_mutation_fails_before_dispatch(self) -> None:
        manifest = build_manifest("SPEC-DEPS")
        manifest["execution_bindings"]["rubric"]["hash"] = "sha256:" + "1" * 64
        manifest = seal_hash(manifest, "manifest_hash")
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "controlled Increment 1 files"):
            validate_manifest(manifest)

    def test_role_schema_rejects_cross_domain_and_extra_fields(self) -> None:
        manifest = build_manifest("SPEC-SBOM")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["quality_gate"] = {"gate_state": "passed"}
        with self.assertRaises(Exception):
            validate_candidate_artifact(manifest, candidate)

    def test_role_evidence_cannot_escape_manifest(self) -> None:
        manifest = build_manifest("SPEC-DEPS")
        candidate = build_candidate(manifest)
        candidate["extensions"]["specialist"]["role"]["graph_nodes"][0]["evidence_refs"] = ["INVENTED-EVIDENCE"]
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "outside the manifest"):
            validate_candidate_artifact(manifest, candidate)

    def test_lint_cannot_pass_without_completed_execution(self) -> None:
        manifest = build_manifest("SPEC-LINT")
        candidate = build_candidate(manifest)
        role = candidate["extensions"]["specialist"]["role"]
        role["quality_gate"]["gate_state"] = "passed"
        role["quality_gate"]["observed_result"] = "zero errors"
        with self.assertRaisesRegex(SpecialistShadowCalibrationError, "cannot be decided"):
            validate_candidate_artifact(manifest, candidate)

    def test_declared_inventory_does_not_become_resolved_sbom(self) -> None:
        manifest = build_manifest("SPEC-SBOM")
        candidate = build_candidate(manifest)
        role = candidate["extensions"]["specialist"]["role"]
        self.assertEqual(role["generation_method"]["method"], "declared_manifest_projection")
        self.assertEqual(role["coverage"]["resolved_components"], 0)
        self.assertEqual(role["coverage"]["artifacts_scanned"], 0)
        self.assertIsNone(role["measures"]["sbom_completeness"])

    def test_dependency_measures_remain_unknown_without_resolved_graph(self) -> None:
        manifest = build_manifest("SPEC-DEPS")
        candidate = build_candidate(manifest)
        role = candidate["extensions"]["specialist"]["role"]
        self.assertFalse(role["coverage"]["resolved_graph_available"])
        self.assertTrue(all(role["measures"][name] is None for name in ("circular_count", "orphan_count", "duplicate_library_count", "abandoned_exposure_count", "critical_path_concentration")))
        self.assertEqual(role["measures"]["graph_trend"], "not_measurable")

    def test_generation_is_deterministic_and_does_not_touch_zip(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = generate(Path(first)); two = generate(Path(second))
            self.assertEqual(one, two)
            for designation, cfg in CONFIG.items():
                left = Path(first) / cfg["slug"] / "human-shadow-review-packet.json"
                right = Path(second) / cfg["slug"] / "human-shadow-review-packet.json"
                self.assertEqual(left.read_bytes(), right.read_bytes())


if __name__ == "__main__":
    unittest.main()

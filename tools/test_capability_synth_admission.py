#!/usr/bin/env python3
"""ADR-0018 evidence-tier, lineage, authority, and immutability tests."""

from __future__ import annotations

import copy
import hashlib
import unittest

from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest
from capability_synth_runtime import BASELINE, assemble_model_candidate, build_candidate, build_reference_package, rehash_artifact, validate_candidate
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json, validate_workflow_instance


REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
PROMPT = ROOT / "appendices/prompt-templates/candidates/cap-synth/design-0.1.0.prompt.txt"
PROMPT_MANIFEST = ROOT / "appendices/prompt-templates/candidates/manifest.json"
CANDIDATE_WORKFLOW = ROOT / "appendices/candidate-workflows/cap-synth-calibration.workflow.json"


class CapabilitySynthAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifacts, self.manifest, self.candidate = build_reference_package()

    def test_reference_is_deterministic_multi_domain_fixture_only(self) -> None:
        self.assertEqual((self.artifacts, self.manifest, self.candidate), build_reference_package())
        role = self.candidate["extensions"]["capability"]["role"]
        self.assertEqual(role["evidence_tier"], "adjudicated_multi_domain_contract_fixture")
        self.assertEqual(role["fitness_claim"], "contract_fixture_only")
        self.assertEqual(role["enterprise_handoff"]["handoff_state"], "comparison_only")
        self.assertEqual(set(role["synthesis_basis"]["expected_designations"]), {"CAP-REQ", "CAP-RISK"})

    def test_prompt_registry_schema_and_candidate_workflow_are_exact(self) -> None:
        prompts = load_json(PROMPT_MANIFEST)["prompts"]["CAP-SYNTH"]
        self.assertEqual(hashlib.sha256(PROMPT.read_bytes()).hexdigest(), prompts["sha256"])
        assert_schema(self.candidate["extensions"]["capability"]["role"], "cap-synth-role.schema.json", "CAP-SYNTH role")
        registry = load_json(ROOT / "agents/agent-identities.json")
        by_designation = {item["designation"]: item for item in registry["agents"]}
        validate_workflow_instance(load_json(CANDIDATE_WORKFLOW), by_designation, "CAP-SYNTH candidate workflow")
        self.assertEqual(by_designation["CAP-SYNTH"]["status"], "candidate")

    def test_manifest_and_child_mutation_fail_closed(self) -> None:
        changed_manifest = copy.deepcopy(self.manifest); changed_manifest["capability_id"] = "CHANGED"
        with self.assertRaises(ValidationFailure): validate_candidate(self.candidate, changed_manifest, self.artifacts)
        changed_children = copy.deepcopy(self.artifacts); changed_children[1]["findings"][0]["statement"] = "changed"
        with self.assertRaises(ValidationFailure): validate_candidate(self.candidate, self.manifest, changed_children)

    def test_preservation_is_exact_and_invented_lineage_fails(self) -> None:
        role = self.candidate["extensions"]["capability"]["role"]
        expected = {(item["source_artifact_id"], item["record_id"], tuple(item["evidence_refs"])) for item in self.manifest["traceability"]}
        actual = {(item["source_artifact_id"], item["source_record_id"], tuple(item["evidence_refs"])) for item in role["preserved_child_assertions"]}
        self.assertEqual(expected, actual)
        invented = copy.deepcopy(self.candidate)
        invented["extensions"]["capability"]["role"]["derived_capability_assertions"][0]["contributing_record_ids"][0] = "INVENTED"
        rehash_artifact(invented)
        with self.assertRaises(ValidationFailure): validate_candidate(invented, self.manifest, self.artifacts)

    def test_evidence_tier_cannot_be_promoted(self) -> None:
        elevated = copy.deepcopy(self.candidate)
        elevated["extensions"]["capability"]["role"]["fitness_claim"] = "multi_domain_candidate_calibration"
        rehash_artifact(elevated)
        with self.assertRaises(ValidationFailure): validate_candidate(elevated, self.manifest, self.artifacts)

    def test_one_domain_live_input_is_protocol_smoke_only(self) -> None:
        artifact = load_json(ACCEPTED_CAP_RISK)
        manifest = build_manifest([artifact], ["CAP-RISK"])
        candidate = build_candidate(manifest, [artifact], "accepted_live_input_calibration")
        role = candidate["extensions"]["capability"]["role"]
        self.assertEqual(role["fitness_claim"], "protocol_lineage_smoke_only")
        self.assertEqual(role["derived_capability_assertions"], [])
        projected = assemble_model_candidate(role, manifest, [artifact])
        self.assertEqual(projected["execution"]["model"], "qwen3-32b")

    def test_authority_and_handoff_changes_fail_closed(self) -> None:
        authority = copy.deepcopy(self.candidate); authority["extensions"]["capability"]["role"]["decision_authority"] = "agent"
        rehash_artifact(authority)
        with self.assertRaises(ValidationFailure): validate_candidate(authority, self.manifest, self.artifacts)
        handoff = copy.deepcopy(self.candidate); handoff["extensions"]["capability"]["role"]["enterprise_handoff"]["artifact_id"] = "18000000-0000-4000-8000-000000000099"
        rehash_artifact(handoff)
        with self.assertRaises(ValidationFailure): validate_candidate(handoff, self.manifest, self.artifacts)

    def test_candidate_does_not_change_baseline_or_report(self) -> None:
        before = (BASELINE.read_bytes(), REPORT.read_bytes()); build_reference_package()
        self.assertEqual(before, (BASELINE.read_bytes(), REPORT.read_bytes()))
        self.assertNotIn("CAP-SYNTH", {node["designation"] for node in load_json(BASELINE)["nodes"]})
        self.assertEqual(self.candidate["consumers"], ["ENT-ARCH-CANDIDATE-COMPARISON",
                                                       "ENT-GOV-CANDIDATE-COMPARISON",
                                                       "ENT-STRAT-CANDIDATE-COMPARISON"])


if __name__ == "__main__": unittest.main(verbosity=2)

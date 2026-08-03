#!/usr/bin/env python3
"""ADR-0034 exact admission, semantics, compatibility, and rollback tests."""

from __future__ import annotations

import copy
import unittest

from accepted_live_capability_synth_runtime import build_accepted_live_package
from capability_coordination_runtime import validate_for_cap_synth
from capability_synth_runtime import assemble_model_candidate, validate_candidate
from requirements_acceptance_runtime import derive_eligibility
from accepted_live_capability_synth_runtime import FINALIZATION, PACKET, RESPONSE
from validate_vertical_slice import ROOT, ValidationFailure, load_json, validate_workflow_instance


class AcceptedLiveCapabilitySynthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = build_accepted_live_package()
        self.artifacts, self.eligibility, self.manifest, self.candidate, self.compatibility, self.review = self.package

    def test_package_is_deterministic_exact_and_unscheduled(self) -> None:
        self.assertEqual(self.package, build_accepted_live_package())
        self.assertEqual(self.manifest["expected_designations"], ["CAP-REQ", "CAP-RISK"])
        self.assertEqual(self.manifest["missing_designations"], [])
        self.assertFalse(self.review["scheduling_authorized"])
        role = self.candidate["extensions"]["capability"]["role"]
        self.assertEqual(role["evidence_tier"], "accepted_live_multi_domain_candidate_evaluation")
        self.assertEqual(role["fitness_claim"], "multi_domain_candidate_evaluation")
        registry = {item["designation"]: item for item in load_json(ROOT / "agents/agent-identities.json")["agents"]}
        workflow = load_json(ROOT / "appendices/candidate-workflows/cap-synth-accepted-live-multi-domain-evaluation.workflow.json")
        validate_workflow_instance(workflow, registry, "ADR-0034 CAP-SYNTH workflow")
        self.assertEqual(workflow["human_gates"][0]["authority_role"], "project-owner")

    def test_eligibility_is_exact_and_revocation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.eligibility)
        mutated["record_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure):
            build_accepted_live_package(eligibility_override=mutated)
        revoked = derive_eligibility(load_json(PACKET), load_json(RESPONSE), load_json(FINALIZATION), revoked=True)
        with self.assertRaises(ValidationFailure):
            build_accepted_live_package(eligibility_override=revoked)

    def test_manifest_authorization_and_artifacts_are_exact(self) -> None:
        validate_for_cap_synth(self.manifest, self.artifacts)
        mutated = copy.deepcopy(self.manifest)
        mutated["accepted_input_authorizations"][0]["artifact_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure):
            validate_for_cap_synth(mutated, self.artifacts)

    def test_zero_requirements_remains_unassessable_with_real_lineage(self) -> None:
        cap_req = next(x for x in self.artifacts if x["identity"]["designation"] == "CAP-REQ")
        role = self.candidate["extensions"]["capability"]["role"]
        self.assertEqual(cap_req["extensions"]["capability"]["role"]["requirement_records"], [])
        self.assertIsNone(cap_req["extensions"]["capability"]["role"]["coverage"]["fraction"])
        derived = role["derived_capability_assertions"]
        self.assertTrue(derived)
        self.assertEqual(len(derived[0]["contributing_artifact_ids"]), 2)
        self.assertIn("cannot be evaluated", derived[0]["statement"])
        validate_candidate(self.candidate, self.manifest, self.artifacts)

    def test_enterprise_compatibility_is_comparison_only_and_honest(self) -> None:
        states = {x["designation"]: x["state"] for x in self.compatibility["results"]}
        self.assertEqual(states["ENT-ARCH"], "direct_comparison_compatible")
        self.assertEqual(states["ENT-GOV"], "direct_comparison_compatible")
        self.assertEqual(states["ENT-STRAT"], "compatible_via_tiered_posture_wrapper")
        self.assertEqual(states["ENT-SYNTH"], "not_direct_enterprise_domain_agents_required")
        self.assertFalse(self.compatibility["enterprise_scheduled"])

    def test_model_projection_preserves_harness_boundary(self) -> None:
        role = copy.deepcopy(self.candidate["extensions"]["capability"]["role"])
        role["derived_capability_assertions"][0]["assertion_id"] = "MODEL-DERIVED-001"
        projected = assemble_model_candidate(role, self.manifest, self.artifacts,
                                             evidence_tier="accepted_live_multi_domain_candidate_evaluation")
        validate_candidate(projected, self.manifest, self.artifacts)
        self.assertEqual(projected["decision_authority"], "human")
        self.assertEqual(projected["extensions"]["capability"]["role"]["enterprise_handoff"]["handoff_state"], "comparison_only")
        self.assertEqual(projected["extensions"]["capability"]["role"]["enterprise_handoff"]["derived_assertion_ids"],
                         ["MODEL-DERIVED-001"])
        broken = copy.deepcopy(projected)
        broken["extensions"]["capability"]["role"]["enterprise_handoff"]["derived_assertion_ids"] = ["STALE-ID"]
        from capability_synth_runtime import rehash_artifact
        rehash_artifact(broken)
        with self.assertRaises(ValidationFailure):
            validate_candidate(broken, self.manifest, self.artifacts)


if __name__ == "__main__":
    unittest.main(verbosity=2)

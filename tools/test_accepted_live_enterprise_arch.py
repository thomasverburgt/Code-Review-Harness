#!/usr/bin/env python3
"""ADR-0035 eligibility, anti-double-counting, scope, and rollback tests."""

from __future__ import annotations

import copy
import unittest

from accepted_live_enterprise_arch_runtime import BASELINE, REPORT, build_package, validate_candidate, validate_input_manifest
from capability_synth_semantic_acceptance_runtime import build_records, derive_eligibility
from enterprise_arch_runtime import rehash
from validate_vertical_slice import ROOT, ValidationFailure, load_json, validate_workflow_instance


class AcceptedLiveEnterpriseArchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = build_package()
        self.source, self.eligibility, self.gate, self.manifest, self.candidate, self.compatibility, self.review = self.package

    def test_package_is_deterministic_exact_and_unscheduled(self) -> None:
        self.assertEqual(self.package, build_package())
        role = self.candidate["extensions"]["enterprise"]["role"]
        self.assertEqual(role["evidence_tier"], "accepted_live_multi_domain_single_capability_evaluation")
        self.assertEqual(role["fitness_claim"], "single_capability_architecture_evaluation")
        self.assertFalse(self.review["cap_synth_scheduled"]); self.assertFalse(self.review["ent_arch_scheduled"])

    def test_candidate_workflow_is_registered_and_owner_gated(self) -> None:
        registry = {item["designation"]: item for item in load_json(ROOT / "agents/agent-identities.json")["agents"]}
        workflow = load_json(ROOT / "appendices/candidate-workflows/ent-arch-accepted-live-multi-domain-evaluation.workflow.json")
        validate_workflow_instance(workflow, registry, "ADR-0035 ENT-ARCH workflow")
        self.assertEqual(workflow["human_gates"][0]["authority_role"], "project-owner")

    def test_parent_only_admission_prevents_double_counting(self) -> None:
        self.assertEqual(self.manifest["admitted_capability_artifact_ids"], [self.source["artifact"]["artifact_id"]])
        self.assertEqual(set(self.manifest["excluded_child_artifact_ids"]), set(self.source["artifact"]["links"]["children"]))
        changed = copy.deepcopy(self.manifest)
        changed["admitted_capability_artifact_ids"].append(self.source["artifact"]["links"]["children"][0])
        with self.assertRaises(ValidationFailure): validate_input_manifest(changed, self.gate, self.source, self.eligibility)

    def test_gate_names_cap_synth_not_inherited_cap_risk(self) -> None:
        facts = [item["fact"] for item in self.gate["observations"]]
        self.assertEqual(len(facts), 1)
        self.assertIn("CAP-SYNTH", facts[0])
        self.assertNotIn("CAP-RISK artifact", facts[0])

    def test_missing_mutated_or_revoked_eligibility_fails_closed(self) -> None:
        changed = copy.deepcopy(self.eligibility); changed["record_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure): build_package(eligibility_override=changed)
        disposition, finalization, _ = build_records(); revoked = derive_eligibility(disposition, finalization, revoked=True)
        with self.assertRaises(ValidationFailure): build_package(eligibility_override=revoked)

    def test_single_capability_scope_suppresses_unsupported_claims(self) -> None:
        role = self.candidate["extensions"]["enterprise"]["role"]
        self.assertEqual(role["architecture_coherence"]["state"], "insufficient_evidence")
        self.assertEqual(role["dependency_topology"], []); self.assertEqual(role["shared_service_concentration"], []); self.assertEqual(role["failure_propagation"], [])
        overclaim = copy.deepcopy(self.candidate)
        overclaim["extensions"]["enterprise"]["role"]["architecture_coherence"]["state"] = "coherent"
        rehash(overclaim)
        with self.assertRaises(ValidationFailure): validate_candidate(overclaim, self.gate, self.source)

    def test_model_projection_remains_harness_owned_and_exact(self) -> None:
        role = copy.deepcopy(self.candidate["extensions"]["enterprise"]["role"])
        role["architecture_debt"] = copy.deepcopy(role["architecture_findings"])
        role["capa_options"] = [{"unsupported": "model suggestion"}]
        projected = build_package(role)[4]
        validate_candidate(projected, self.gate, self.source)
        self.assertEqual(projected["extensions"]["enterprise"]["role"]["manifest_binding"], role["manifest_binding"])
        self.assertEqual(projected["extensions"]["enterprise"]["role"]["architecture_debt"], [])
        self.assertEqual(projected["extensions"]["enterprise"]["role"]["capa_options"], [])
        self.assertEqual(projected["decision_authority"], "human")

    def test_child_decision_ids_are_source_qualified_and_unique(self) -> None:
        role = copy.deepcopy(self.candidate["extensions"]["enterprise"]["role"])
        role["decision_requests"] = [
            {"record_id": "DC-001", "statement": "Declare authoritative requirements for the bounded slice to enable traceability."},
            {"record_id": "DC-001", "statement": "Classify the redacted credential-like value as confirmed secret, likely secret, or benign/nonsecret to resolve the risk."},
        ]
        projected = build_package(role)[4]
        identifiers = [item["record_id"] for item in projected["extensions"]["enterprise"]["role"]["decision_requests"]]
        self.assertEqual(identifiers, [
            "6beec632-8baf-5a58-a4ce-fa14784d8435:DC-001",
            "a5ada795-db2f-5625-aed9-1b619411be17:DC-001",
        ])
        self.assertEqual(len(identifiers), len(set(identifiers)))

        flattened = copy.deepcopy(projected)
        flattened["extensions"]["enterprise"]["role"]["decision_requests"][0]["record_id"] = "DC-001"
        rehash(flattened)
        with self.assertRaises(ValidationFailure): validate_candidate(flattened, self.gate, self.source)

    def test_rollback_and_authoritative_files_are_unchanged(self) -> None:
        before = (BASELINE.read_bytes(), REPORT.read_bytes()); build_package()
        self.assertEqual(before, (BASELINE.read_bytes(), REPORT.read_bytes()))
        self.assertNotIn("ENT-ARCH", {node["designation"] for node in load_json(BASELINE)["nodes"]})


if __name__ == "__main__": unittest.main(verbosity=2)

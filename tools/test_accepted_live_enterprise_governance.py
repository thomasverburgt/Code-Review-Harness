#!/usr/bin/env python3
"""ADR-0036 source, eligibility, scope, authority, and rollback tests."""

from __future__ import annotations

import copy
import unittest

from accepted_live_enterprise_governance_runtime import REPORT, build_package, validate_candidate, validate_evidence_manifest, validate_input_manifest, validate_owner_source
from capability_synth_semantic_acceptance_runtime import build_records, derive_eligibility
from enterprise_arch_runtime import BASELINE, rehash
from validate_vertical_slice import ROOT, ValidationFailure, load_json


class AcceptedLiveEnterpriseGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = build_package(); self.source, self.eligibility, self.governance, self.evidence, self.gate, self.manifest, self.candidate, self.compatibility, self.review = self.package

    def test_package_is_deterministic_owner_declared_and_unscheduled(self) -> None:
        self.assertEqual(self.package, build_package()); self.assertEqual(self.governance["declared_by"]["authority_name"], "thomasverburgt")
        role = self.candidate["extensions"]["enterprise"]["role"]
        self.assertEqual(role["evidence_tier"], "accepted_live_multi_domain_single_capability_governance_evaluation")
        self.assertFalse(self.review["cap_synth_scheduled"]); self.assertFalse(self.review["ent_gov_scheduled"])

    def test_owner_source_exact_authority_obligation_and_locator(self) -> None:
        validate_owner_source(self.governance); source = self.governance["sources"][0]
        self.assertEqual(self.governance["declared_by"]["subject_id"], "HUMAN-PROJECT-OWNER-001")
        self.assertEqual(self.governance["declared_by"]["authority_registry"]["registry_version"], "0.7.0")
        self.assertEqual(source["path"], "GOVERNANCE.md"); self.assertEqual((source["line_start"], source["line_end"]), (13, 13))
        self.assertEqual(source["obligations"][0]["obligation_id"], "GOV-AGENT-AUTH-001")

    def test_parent_only_admission_prevents_double_counting(self) -> None:
        self.assertEqual(self.manifest["admitted_capability_artifact_ids"], [self.source["artifact"]["artifact_id"]])
        changed = copy.deepcopy(self.manifest); changed["admitted_capability_artifact_ids"].append(self.source["artifact"]["links"]["children"][0])
        with self.assertRaises(ValidationFailure): validate_input_manifest(changed, self.gate, self.source, self.eligibility, self.governance, self.evidence)

    def test_evidence_binding_resolves_exact_fields_and_excludes_unrelated_derivation(self) -> None:
        validate_evidence_manifest(self.evidence, self.source, self.eligibility)
        pointers = {item["json_pointer"] for item in self.evidence["records"]}
        self.assertIn("/decision_authority", pointers)
        self.assertIn("/cap_synth_scheduled", pointers)
        refs = self.candidate["extensions"]["enterprise"]["role"]["compliance_matrix"][0]["evidence_refs"]
        self.assertEqual(refs, [item["locator_id"] for item in self.evidence["records"]])
        self.assertNotIn("DERIVED-001", refs)

    def test_mutated_source_or_revoked_eligibility_fails_closed(self) -> None:
        changed = copy.deepcopy(self.governance); changed["declared_by"]["authority_name"] = "Fixture Authority"
        with self.assertRaises(ValidationFailure): build_package(governance_override=changed)
        disposition, finalization, _ = build_records(); revoked = derive_eligibility(disposition, finalization, revoked=True)
        with self.assertRaises(ValidationFailure): build_package(eligibility_override=revoked)

    def test_matrix_preserves_missingness_and_rejects_invention(self) -> None:
        role = self.candidate["extensions"]["enterprise"]["role"]; self.assertEqual(len(role["compliance_matrix"]), 1)
        self.assertEqual(role["compliance_matrix"][0]["state"], "insufficient_evidence")
        overclaim = copy.deepcopy(self.candidate); overclaim["extensions"]["enterprise"]["role"]["compliance_matrix"][0]["state"] = "compliant"; rehash(overclaim)
        with self.assertRaises(ValidationFailure): validate_candidate(overclaim, self.gate, self.source, self.eligibility, self.governance, self.evidence, self.manifest)

    def test_model_cannot_create_exception_approval_maturity_or_capa(self) -> None:
        role = copy.deepcopy(self.candidate["extensions"]["enterprise"]["role"]); role["exception_register"] = [{"invented": True}]; role["approval_dependencies"] = [{"invented": True}]
        role["governance_maturity"] = {"state": "assessed", "advisory_only": True, "rationale": "invented"}; role["capa_options"] = [{"invented": True}]
        role["compliance_matrix"][0]["rationale"] = "Unrelated requirements and credential rationale."
        role["compliance_matrix"][0]["evidence_refs"] = ["a5ada795-db2f-5625-aed9-1b619411be17:RISK-001"]
        projected = build_package(role, raw_response_sha256="1" * 64)[6]; projected_role = projected["extensions"]["enterprise"]["role"]
        self.assertEqual(projected_role["exception_register"], []); self.assertEqual(projected_role["approval_dependencies"], []); self.assertEqual(projected_role["capa_options"], [])
        self.assertEqual(projected_role["governance_maturity"]["state"], "insufficient_evidence")
        self.assertIn("agent prohibition", projected_role["compliance_matrix"][0]["rationale"])
        self.assertEqual(projected_role["compliance_matrix"][0]["evidence_refs"], [item["locator_id"] for item in self.evidence["records"]])
        self.assertEqual(projected["execution"]["generation_mode"], "model_response_with_harness_owned_governance_projection")
        self.assertEqual(projected["extensions"]["enterprise"]["confidence_reconciliation"]["method"], "confidence_in_bounded_evidence_insufficiency_not_compliance")

    def test_authoritative_files_and_schedules_are_unchanged(self) -> None:
        before = (BASELINE.read_bytes(), REPORT.read_bytes()); build_package(); self.assertEqual(before, (BASELINE.read_bytes(), REPORT.read_bytes()))
        self.assertNotIn("ENT-GOV", {node["designation"] for node in load_json(BASELINE)["nodes"]})


if __name__ == "__main__": unittest.main(verbosity=2)

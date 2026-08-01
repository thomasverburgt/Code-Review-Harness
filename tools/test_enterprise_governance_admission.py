#!/usr/bin/env python3
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from artifact_ledger import ArtifactLedger, content_hash
from enterprise_arch_runtime import build_inputs
from enterprise_governance_runtime import (
    BASELINE,
    build_candidate,
    load_source,
    persist_candidate,
    validate_candidate,
    validate_source,
)
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
ADR20 = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json"


class EnterpriseGovernanceAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = load_source()
        self.gate, self.artifacts = build_inputs()
        self.candidate = build_candidate()

    def test_source_manifest_schema_hash_locator_and_authority(self):
        assert_schema(self.source, "governance-source-manifest.schema.json", "source")
        validate_source(self.source)
        authority = load_json(ROOT / "appendices/governance/decision-authorities-0.1.0.json")
        record = next(x for x in authority["authorities"] if x["authority_role"] == "governance-source-owner")
        self.assertIn("declare_governance_source_and_applicability", record["allowed_actions"])

    def test_registry_truth_and_candidate_identity(self):
        registry = load_json(ROOT / "agents/agent-identities.json")
        states = {x["designation"]: x["status"] for x in registry["agents"] if x["layer"] == "enterprise"}
        self.assertEqual(states["ENT-EVIDENCE"], "baseline")
        self.assertEqual(states["ENT-SYSRISK"], "baseline")
        self.assertEqual(states["ENT-ARCH"], "candidate")
        self.assertEqual(states["ENT-GOV"], "candidate")
        self.assertIn(states["ENT-STRAT"], {"planned", "candidate"})
        self.assertIn(states["ENT-SYNTH"], {"planned", "candidate"})
        self.assertTrue(all(states[x] == "planned" for x in states if x not in {"ENT-EVIDENCE", "ENT-SYSRISK", "ENT-ARCH", "ENT-GOV", "ENT-STRAT", "ENT-SYNTH"}))

    def test_deterministic_exact_source_gate_and_capability_binding(self):
        self.assertEqual(self.candidate, build_candidate())
        binding = self.candidate["extensions"]["enterprise"]["role"]["manifest_binding"]
        self.assertEqual(binding["governance_manifest_hash"], content_hash(self.source))
        self.assertEqual(binding["gate_artifact_hash"], content_hash(self.gate))
        self.assertEqual(binding["capability_artifact_hashes"], [content_hash(x) for x in self.artifacts])

    def test_matrix_is_complete_cross_product_and_missing_evidence_is_unknown(self):
        role = self.candidate["extensions"]["enterprise"]["role"]
        eligible = sum(len(x["obligations"]) for x in self.source["sources"] if x["classification"] == "authoritative" and x["lifecycle_state"] == "active" and x["applicability"]["determination"] == "applicable")
        self.assertEqual(len(role["compliance_matrix"]), eligible * len(self.artifacts))
        self.assertTrue(all(x["state"] == "insufficient_evidence" for x in role["compliance_matrix"]))
        self.assertTrue(all(x["evidence_refs"] == [] for x in role["compliance_matrix"]))

    def test_role_and_workflow_schemas(self):
        role = self.candidate["extensions"]["enterprise"]["role"]
        assert_schema(role, "ent-gov-role.schema.json", "ENT-GOV role")
        workflow = load_json(ROOT / "appendices/candidate-workflows/ent-gov-calibration.workflow.json")
        self.assertEqual(workflow["nodes"][0]["designation"], "ENT-GOV")

    def test_mutated_source_classification_applicability_or_hash_fails_closed(self):
        mutations = []
        for field, value in [("classification", "advisory"), ("content_hash", "sha256:" + "0" * 64)]:
            source = copy.deepcopy(self.source)
            source["sources"][0][field] = value
            mutations.append(source)
        source = copy.deepcopy(self.source)
        source["sources"][0]["applicability"]["determination"] = "not_applicable"
        mutations.append(source)
        for source in mutations:
            with self.assertRaises(ValidationFailure):
                validate_source(source)

    def test_missing_extra_matrix_rows_and_invented_human_record_fail_closed(self):
        candidates = []
        missing = copy.deepcopy(self.candidate)
        missing["extensions"]["enterprise"]["role"]["compliance_matrix"].pop()
        candidates.append(missing)
        extra = copy.deepcopy(self.candidate)
        extra["extensions"]["enterprise"]["role"]["compliance_matrix"].append(copy.deepcopy(extra["extensions"]["enterprise"]["role"]["compliance_matrix"][0]))
        candidates.append(extra)
        invented = copy.deepcopy(self.candidate)
        invented["extensions"]["enterprise"]["role"]["exception_register"].append({"exception_id": "invented"})
        candidates.append(invented)
        for candidate in candidates:
            with self.assertRaises(ValidationFailure):
                validate_candidate(candidate, self.gate, self.artifacts, self.source)

    def test_live_single_capability_is_source_protocol_only(self):
        gate, artifacts = build_inputs(live=True)
        candidate = build_candidate(live=True)
        role = candidate["extensions"]["enterprise"]["role"]
        self.assertEqual(role["fitness_claim"], "source_protocol_lineage_smoke_only")
        validate_candidate(candidate, gate, artifacts, self.source, live=True)

    def test_authority_boundary_and_persistence(self):
        role = self.candidate["extensions"]["enterprise"]["role"]
        self.assertEqual(role["decision_authority"], "human")
        self.assertFalse(role["downstream_handoff"]["scheduled"])
        self.assertEqual(role["unsupported_claims"], [])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = persist_candidate(root, self.candidate)
            self.assertEqual(ArtifactLedger(root).get_object(reference["object_hash"]), self.candidate)
            self.assertEqual(reference, persist_candidate(root, self.candidate))

    def test_baseline_report_adr20_and_ent_arch_schedule_unchanged(self):
        paths = [BASELINE, REPORT, ADR20]
        before = [path.read_bytes() for path in paths]
        build_candidate()
        self.assertEqual(before, [path.read_bytes() for path in paths])
        scheduled = {node["designation"] for node in load_json(BASELINE)["nodes"]}
        self.assertNotIn("ENT-GOV", scheduled)
        self.assertNotIn("ENT-ARCH", scheduled)


if __name__ == "__main__":
    unittest.main(verbosity=2)

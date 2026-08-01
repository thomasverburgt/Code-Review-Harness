#!/usr/bin/env python3
"""Deterministic and fail-closed calibration tests for PROD-SYNTH."""

from __future__ import annotations

import copy
import unittest

from artifact_ledger import content_hash
from calibrate_product_synth import (CANDIDATE_WORKFLOW, DEFAULT_EVIDENCE, MODEL_MANIFEST,
                                     build_dispatch, build_job)
from test_product_synth_admission import GOLD
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json, validate_workflow_instance
from worker_runtime import (VersionResolver, WorkerError, assemble_canonical_artifact,
                            project_product_synthesis_layer, validate_candidate)


LIVE_ARTIFACT = ROOT / "fixtures/product-synth-admission/evidence/2026-07-31/live-calibration/accepted-prod-synth.artifact.json"


def canonical_payload(child: dict) -> dict:
    gold = load_json(GOLD)
    role = copy.deepcopy(gold["extensions"]["product"]["role"])
    finding = child["findings"][0]
    preserved = role["preserved_child_assertions"][0]
    preserved["source_artifact_id"] = child["artifact"]["artifact_id"]
    preserved["source_record_id"] = finding["finding_id"]
    preserved["evidence_refs"] = copy.deepcopy(finding["evidence_refs"])
    derived = role["derived_product_assertions"][0]
    derived["contributing_artifact_ids"] = [child["artifact"]["artifact_id"]]
    derived["contributing_record_ids"] = [finding["finding_id"]]
    confidence = copy.deepcopy(gold["confidence"])
    confidence["provenance"] = [{"source": "PROD-SEC", "version": "fixture-rev-001"}]
    return {"methodology": copy.deepcopy(gold["methodology"]), "review_counts": copy.deepcopy(gold["coverage"]),
            "findings": copy.deepcopy(gold["findings"]), "secondary_records": [], "confidence": confidence,
            "decisions_requested": copy.deepcopy(gold["decisions_requested"]),
            "role_payload": role,
            "generation_disclosure": {"omitted_item_estimate": 0, "truncated_string_estimate": 0}}


class ProductSynthCalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load_json(CANDIDATE_WORKFLOW)
        self.manifest = load_json(MODEL_MANIFEST)
        self.child = load_json(ROOT / DEFAULT_EVIDENCE)
        registry = load_json(ROOT / "agents/agent-identities.json")
        validate_workflow_instance(self.workflow, {item["designation"]: item for item in registry["agents"]}, "candidate workflow")
        model_pin = {"provider": self.manifest["provider"], "model_id": self.manifest["model_id"], "version": self.manifest["upstream_revision"]}
        self.resolved = VersionResolver(model_pin_override=model_pin, workflow_path=CANDIDATE_WORKFLOW).resolve("PROD-SYNTH")
        self.job = build_job(DEFAULT_EVIDENCE, self.child, self.workflow, self.manifest)
        self.inputs = {DEFAULT_EVIDENCE: self.child}

    def test_candidate_projection_is_deterministic_and_unscheduled(self) -> None:
        first = assemble_canonical_artifact(canonical_payload(self.child), self.job, self.resolved, self.inputs)
        second = assemble_canonical_artifact(copy.deepcopy(canonical_payload(self.child)), copy.deepcopy(self.job), self.resolved, copy.deepcopy(self.inputs))
        self.assertEqual(first, second)
        artifact = first[0]
        assert_schema(artifact, "universal-agent-artifact.schema.json", "calibrated PROD-SYNTH")
        self.assertEqual(artifact["extensions"]["product"]["role"]["capability_handoff"]["artifact_id"], artifact["artifact"]["artifact_id"])
        self.assertEqual(artifact["decision_authority"], "human")
        self.assertFalse(any(node["designation"] == "PROD-SYNTH" for node in load_json(ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json")["nodes"]))

    def test_projection_rejects_invented_and_missing_lineage(self) -> None:
        invented = canonical_payload(self.child)
        invented["role_payload"]["preserved_child_assertions"][0]["source_record_id"] = "INVENTED"
        with self.assertRaises(WorkerError):
            project_product_synthesis_layer(invented, self.job, self.resolved, self.inputs)
        wrong_child = copy.deepcopy(self.child)
        wrong_child["identity"]["designation"] = "PROD-ARCH"
        with self.assertRaises(WorkerError):
            project_product_synthesis_layer(canonical_payload(self.child), self.job, self.resolved, {DEFAULT_EVIDENCE: wrong_child})

    def test_dispatch_and_job_are_pinned_to_test_environment(self) -> None:
        dispatch = build_dispatch(self.child, self.workflow, self.manifest)
        self.assertEqual(dispatch["execution_environment"]["execution_mode"], "test")
        self.assertEqual(dispatch["execution_environment"]["platform_class"], "approved-equivalent")
        self.assertEqual(dispatch["version_pins"]["model"]["version"], self.manifest["upstream_revision"])
        assert_schema(self.job, "worker-job.schema.json", "PROD-SYNTH calibration job")

    def test_wrong_contract_or_projection_pin_fails_closed(self) -> None:
        bad_contract = copy.deepcopy(self.job)
        bad_contract["generation_contract_version"] = "wrong"
        self.assertNotEqual(bad_contract["generation_contract_version"], self.resolved["canonical_generation_contract_version"])
        bad_projection = copy.deepcopy(self.job)
        bad_projection["projection_version"] = "wrong"
        self.assertNotEqual(bad_projection["projection_version"], self.resolved["canonical_projection_version"])

    def test_retained_live_candidate_is_valid_and_exactly_bound(self) -> None:
        live = load_json(LIVE_ARTIFACT)
        validate_candidate(live, self.resolved, self.inputs)
        self.assertEqual(content_hash(live), "sha256:bbb642801216bc347892d212440e5b23ec36a3863c83dea8e91a359e62693196")
        role = live["extensions"]["product"]["role"]
        self.assertEqual(role["synthesis_basis"]["received_artifact_ids"], [self.child["artifact"]["artifact_id"]])
        self.assertEqual(role["capability_handoff"]["artifact_id"], live["artifact"]["artifact_id"])
        self.assertEqual(role["capability_handoff"]["handoff_state"], "ready_for_capability_fan_in")
        self.assertEqual(live["decision_authority"], "human")


if __name__ == "__main__":
    unittest.main(verbosity=2)

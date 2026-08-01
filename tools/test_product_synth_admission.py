#!/usr/bin/env python3
"""Candidate-admission and downstream-compatibility tests for PROD-SYNTH."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest

from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


GOLD = ROOT / "fixtures/product-synth-admission/gold/prod-synth.artifact.json"
NEGATIVE = ROOT / "fixtures/product-synth-admission/negative/cases.json"
PROD_SEC = ROOT / "fixtures/vertical-risk-slice/gold/prod-sec.artifact.json"
CAP_RISK = ROOT / "fixtures/vertical-risk-slice/gold/cap-risk.artifact.json"
REGISTRY = ROOT / "agents/agent-identities.json"
WORKFLOW = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"
PROMPT_MANIFEST = ROOT / "appendices/prompt-templates/candidates/manifest.json"


class ProductSynthAdmissionError(Exception):
    pass


def validate_prompt_manifest(entry: dict) -> None:
    if entry.get("status") != "candidate":
        raise ProductSynthAdmissionError("PROD-SYNTH prompt is not a candidate")
    prompt = ROOT / entry["path"]
    if hashlib.sha256(prompt.read_bytes()).hexdigest() != entry.get("sha256"):
        raise ProductSynthAdmissionError("PROD-SYNTH prompt hash mismatch")


def validate_candidate(artifact: dict, workflow: dict | None = None) -> None:
    assert_schema(artifact, "universal-agent-artifact.schema.json", "PROD-SYNTH candidate")
    extension = artifact["extensions"]["product"]
    assert_schema(extension, "product-extension.schema.json", "PROD-SYNTH product extension")
    assert_schema(extension["role"], "prod-synth-role.schema.json", "PROD-SYNTH role extension")
    registry = load_json(REGISTRY)
    identity = next(item for item in registry["agents"] if item["designation"] == "PROD-SYNTH")
    if identity["status"] != "candidate" or artifact["identity"]["agent_uuid"] != identity["agent_uuid"]:
        raise ProductSynthAdmissionError("PROD-SYNTH identity is not the registered candidate")
    if artifact["decision_authority"] != "human" or extension["role"]["decision_authority"] != "human":
        raise ProductSynthAdmissionError("PROD-SYNTH cannot claim decision authority")
    if extension["release_readiness_input"].get("is_release_decision") is not False:
        raise ProductSynthAdmissionError("release-readiness input cannot become a release decision")
    inputs = {item["artifact_id"] for item in artifact["inputs"]}
    children = set(artifact["artifact"]["links"]["children"])
    inventory = {item["artifact_id"] for item in extension["specialist_artifact_inventory"] if item.get("state") == "valid_present"}
    received = set(extension["role"]["synthesis_basis"]["received_artifact_ids"])
    if not inputs or inputs != children or inputs != inventory or inputs != received:
        raise ProductSynthAdmissionError("input, child-link, inventory, and synthesis-basis lineage must match exactly")
    for assertion in extension["role"]["preserved_child_assertions"]:
        if assertion["source_artifact_id"] not in inputs:
            raise ProductSynthAdmissionError("preserved assertion cites an undeclared child")
    for assertion in extension["role"]["derived_product_assertions"]:
        if not set(assertion["contributing_artifact_ids"]).issubset(inputs):
            raise ProductSynthAdmissionError("derived assertion cites an undeclared child")
    handoff = extension["role"]["capability_handoff"]
    if handoff["artifact_id"] != artifact["artifact"]["artifact_id"] or handoff["product_id"] != extension["product_id"]:
        raise ProductSynthAdmissionError("capability handoff is not bound to the candidate artifact")
    preserved_findings = {item["source_record_id"] for item in extension["role"]["preserved_child_assertions"] if item["record_kind"] == "finding"}
    preserved_evidence = {ref for item in extension["role"]["preserved_child_assertions"] for ref in item["evidence_refs"]}
    if not set(handoff["preserved_finding_ids"]).issubset(preserved_findings) or not set(handoff["preserved_evidence_refs"]).issubset(preserved_evidence):
        raise ProductSynthAdmissionError("capability handoff drops or invents preserved finding lineage")
    scheduled = workflow or load_json(WORKFLOW)
    if any(node["designation"] == "PROD-SYNTH" for node in scheduled["nodes"]):
        raise ProductSynthAdmissionError("candidate PROD-SYNTH cannot be scheduled before promotion")


class ProductSynthAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gold = load_json(GOLD)

    def test_gold_candidate_and_prompt_integrity(self) -> None:
        validate_candidate(self.gold)
        manifest = load_json(PROMPT_MANIFEST)["prompts"]["PROD-SYNTH"]
        validate_prompt_manifest(manifest)

    def test_child_finding_and_evidence_survive_capability_handoff(self) -> None:
        validate_candidate(self.gold)
        child = load_json(PROD_SEC)
        finding = child["findings"][0]
        handoff = self.gold["extensions"]["product"]["role"]["capability_handoff"]
        self.assertIn(finding["finding_id"], handoff["preserved_finding_ids"])
        self.assertTrue(set(finding["evidence_refs"]).issubset(handoff["preserved_evidence_refs"]))
        adapted = load_json(CAP_RISK)
        adapted["artifact"]["links"]["children"] = [self.gold["artifact"]["artifact_id"]]
        adapted["inputs"] = [{"artifact_id": self.gold["artifact"]["artifact_id"], "hash": self.gold["integrity"]["output_hash"], "compatibility": "compatible", "freshness": "fresh"}]
        adapted["extensions"]["capability"]["role"]["risk_provenance"][0]["artifact_ids"] = [self.gold["artifact"]["artifact_id"]]
        assert_schema(adapted, "universal-agent-artifact.schema.json", "adapted CAP-RISK artifact")
        assert_schema(adapted["extensions"]["capability"], "capability-extension.schema.json", "adapted capability extension")
        assert_schema(adapted["extensions"]["capability"]["role"], "cap-risk-role.schema.json", "adapted CAP-RISK role")

    def test_negative_admission_cases_fail_closed(self) -> None:
        cases = load_json(NEGATIVE)["cases"]
        executed = set()
        for case in cases:
            candidate = copy.deepcopy(self.gold)
            workflow = None
            case_id = case["case_id"]
            if case_id == "wrong-identity":
                candidate["identity"]["agent_uuid"] = "00000000-0000-4000-8000-000000000000"
            elif case_id == "missing-required-child":
                candidate["inputs"] = []
            elif case_id == "invented-lineage":
                candidate["extensions"]["product"]["role"]["derived_product_assertions"][0]["contributing_artifact_ids"] = ["77777777-7777-4777-8777-777777777777"]
            elif case_id == "release-authority-claim":
                candidate["extensions"]["product"]["release_readiness_input"]["is_release_decision"] = True
            elif case_id == "agent-decision-authority":
                candidate["decision_authority"] = "agent"
            elif case_id == "prompt-hash-mismatch":
                manifest = copy.deepcopy(load_json(PROMPT_MANIFEST)["prompts"]["PROD-SYNTH"])
                manifest["sha256"] = "0" * 64
                with self.assertRaises(ProductSynthAdmissionError):
                    validate_prompt_manifest(manifest)
                executed.add(case_id)
                continue
            elif case_id == "premature-workflow-scheduling":
                workflow = load_json(WORKFLOW)
                workflow["nodes"].append({"designation": "PROD-SYNTH"})
            else:
                self.fail(f"unimplemented negative case {case_id}")
            with self.assertRaises((ProductSynthAdmissionError, ValidationFailure, KeyError)):
                validate_candidate(candidate, workflow)
            executed.add(case_id)
        self.assertEqual(executed, {item["case_id"] for item in cases})

    def test_replay_is_deterministic_and_source_children_are_immutable(self) -> None:
        before = json.dumps(load_json(PROD_SEC), sort_keys=True)
        self.assertEqual(self.gold, load_json(GOLD))
        validate_candidate(self.gold)
        self.assertEqual(before, json.dumps(load_json(PROD_SEC), sort_keys=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)

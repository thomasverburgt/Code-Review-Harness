#!/usr/bin/env python3
"""Gold and negative tests for the deterministic vertical-risk slice."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from validate_vertical_slice import (
    REGISTRY,
    ROOT,
    ValidationFailure,
    load_gold_payloads,
    load_json,
    validate_artifact_payloads,
    validate_state_machines,
    validate_workflow,
    validate_workflow_instance,
)
from run_vertical_slice import run


CASES = ROOT / "fixtures" / "vertical-risk-slice" / "negative" / "cases.json"


def mutate(case_id: str, workflow: dict[str, Any], artifacts: dict[str, dict[str, Any]], decision: dict[str, Any]) -> None:
    nodes = {node["node_id"]: node for node in workflow["nodes"]}
    if case_id == "workflow_uuid_mismatch":
        nodes["spec-secrets"]["agent_uuid"] = "00000000-0000-4000-8000-000000000000"
    elif case_id == "workflow_cycle":
        workflow["edges"].append({"from": "ent-sysrisk", "to": "spec-secrets", "artifact_type": "invalid-cycle", "required": True})
        nodes["ent-sysrisk"]["consumers"].append("spec-secrets")
        nodes["spec-secrets"]["required_inputs"].append("ent-sysrisk")
    elif case_id == "undeclared_dependency":
        nodes["prod-sec"]["required_inputs"].append("cap-risk")
    elif case_id == "missing_required_artifact":
        artifacts.pop("PROD-SEC")
    elif case_id == "bad_lineage_hash":
        artifacts["PROD-SEC"]["inputs"][0]["hash"] = "sha256:incorrect"
    elif case_id == "missing_layer_field":
        del artifacts["PROD-SEC"]["extensions"]["product"]["product_id"]
    elif case_id == "stale_input":
        artifacts["PROD-SEC"]["inputs"][0]["freshness"] = "stale"
    elif case_id == "unauthorized_incomplete_input":
        artifacts["CAP-RISK"]["artifact"]["lifecycle_state"] = "incomplete_input"
    elif case_id == "contract_version_mismatch":
        artifacts["SPEC-SECRETS"]["identity"]["contract_version"] = "9.9.9"
    elif case_id == "artifact_uuid_mismatch":
        artifacts["SPEC-SECRETS"]["identity"]["agent_uuid"] = "00000000-0000-4000-8000-000000000000"
    elif case_id == "decision_authority_violation":
        decision["decision_authority"] = "agent"
    elif case_id == "incomplete_capa":
        del artifacts["SPEC-SECRETS"]["findings"][0]["capa"]["validation_method"]
    elif case_id == "restricted_secret_leakage":
        artifacts["SPEC-SECRETS"]["execution"]["secret_value"] = "BEGIN PRIVATE KEY"
    elif case_id == "unlinked_final_decision":
        decision["triggering_artifacts"] = ["00000000-0000-4000-8000-000000000000"]
    elif case_id == "role_designation_mismatch":
        artifacts["CAP-RISK"]["extensions"]["capability"]["role"]["designation"] = "ENT-SYSRISK"
    else:
        raise RuntimeError(f"unknown negative case {case_id}")


def main() -> int:
    registry = load_json(REGISTRY)
    registry_by_designation = {agent["designation"]: agent for agent in registry["agents"]}
    base_workflow = validate_workflow(registry_by_designation)
    validate_state_machines()
    base_artifacts, base_decision = load_gold_payloads()
    validate_artifact_payloads(base_workflow, registry_by_designation, base_artifacts, base_decision)

    suite = load_json(CASES)
    passed = 0
    failures: list[str] = []
    for case in suite["cases"]:
        workflow = copy.deepcopy(base_workflow)
        artifacts = copy.deepcopy(base_artifacts)
        decision = copy.deepcopy(base_decision)
        mutate(case["case_id"], workflow, artifacts, decision)
        try:
            validate_workflow_instance(workflow, registry_by_designation, case["case_id"])
            validate_artifact_payloads(workflow, registry_by_designation, artifacts, decision)
        except ValidationFailure as exc:
            if case["expected_reason"].lower() in str(exc).lower():
                passed += 1
            else:
                failures.append(f"{case['case_id']}: wrong failure: {exc}")
        else:
            failures.append(f"{case['case_id']}: mutation was incorrectly accepted")
    if failures:
        print("vertical slice tests FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    expected_scenarios = {
        "gold": ("complete", 0, 0, 0),
        "authorized_incomplete_input": ("incomplete_input", 3, 0, 0),
        "retry_then_success": ("complete", 0, 1, 0),
        "timeout_failure": ("failed", 0, 0, 1),
        "superseded_failure": ("failed", 0, 0, 0),
    }
    with tempfile.TemporaryDirectory(prefix="vertical-slice-tests-") as temp:
        base = Path(temp)
        for scenario, expected in expected_scenarios.items():
            summary = run(base / scenario, "90000000-0000-4000-8000-000000000001", "2026-07-31T15:00:00Z", scenario)
            actual = (summary["status"], summary["partial_inputs"], summary["retries"], summary["timeouts"])
            if actual != expected:
                print(f"scenario {scenario} expected {expected} but got {actual}", file=sys.stderr)
                return 1
        run_one = base / "replay-one"
        run_two = base / "replay-two"
        run(run_one, "90000000-0000-4000-8000-000000000001", "2026-07-31T15:00:00Z", "gold")
        run(run_two, "90000000-0000-4000-8000-000000000001", "2026-07-31T15:00:00Z", "gold")
        one_files = {str(path.relative_to(run_one)): path.read_bytes() for path in run_one.rglob("*") if path.is_file()}
        two_files = {str(path.relative_to(run_two)): path.read_bytes() for path in run_two.rglob("*") if path.is_file()}
        if one_files != two_files:
            print("deterministic replay outputs differ", file=sys.stderr)
            return 1
    print(json.dumps({"gold": "passed", "negative_cases": len(suite["cases"]), "negative_cases_passed": passed, "runtime_scenarios": len(expected_scenarios), "deterministic_replay": "passed", "suite": suite["fixture_suite_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

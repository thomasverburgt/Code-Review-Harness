#!/usr/bin/env python3
"""Deterministic reference runner for WF-VERTICAL-RISK-001.

This runner simulates the orchestration controls around pre-adjudicated agent
artifacts. It does not invoke a model and does not make engineering decisions.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import uuid
from pathlib import Path
from typing import Any

from validate_vertical_slice import (
    FIXTURE_DIR,
    REGISTRY,
    ROOT,
    assert_schema,
    load_json,
    validate_artifacts,
    validate_artifact_payloads,
    validate_state_machines,
    validate_workflow,
)


DEFAULT_EXECUTION_ID = "90000000-0000-4000-8000-000000000001"
DEFAULT_STARTED_AT = "2026-07-31T15:00:00Z"
NAMESPACE = uuid.UUID("90000000-0000-4000-8000-000000000000")
DEFAULT_EXECUTION_ENVIRONMENT = {
    "execution_mode": "test",
    "platform_designation": "NVIDIA-DGX-SPARK-REFERENCE",
    "platform_class": "dgx-spark",
    "approval_reference": "ADR-0008",
    "accelerator_runtime": "pinned-by-test-platform-manifest",
    "container_image": "code-review-harness-reference:0.1.0",
    "model_or_workload_scale": "deterministic-fixture-no-model",
    "limitations": ["Reference runner simulates orchestration and does not measure A100 capacity"],
    "environment_policy_version": "ADR-0008",
}


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def topological_order(workflow: dict[str, Any]) -> list[str]:
    node_ids = [node["node_id"] for node in workflow["nodes"]]
    incoming = {node_id: 0 for node_id in node_ids}
    adjacency = {node_id: [] for node_id in node_ids}
    for edge in workflow["edges"]:
        incoming[edge["to"]] += 1
        adjacency[edge["from"]].append(edge["to"])
    ready = sorted(node_id for node_id, count in incoming.items() if count == 0)
    ordered: list[str] = []
    while ready:
        node_id = ready.pop(0)
        ordered.append(node_id)
        for target in sorted(adjacency[node_id]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    if len(ordered) != len(node_ids):
        raise RuntimeError("workflow graph is cyclic")
    return ordered


def make_audit_event(sequence: int, execution_id: str, controller: str, event_type: str,
                     subject_id: str, before: str | None, after: str, reason: str,
                     refs: list[str], timestamp: str) -> dict[str, Any]:
    event = {
        "event_id": stable_uuid(execution_id, "audit", str(sequence), controller, subject_id),
        "sequence": sequence,
        "workflow_id": "WF-VERTICAL-RISK-001",
        "execution_id": execution_id,
        "controller": controller,
        "event_type": event_type,
        "subject_id": subject_id,
        "state_before": before,
        "state_after": after,
        "reason_code": reason,
        "input_refs": refs,
        "timestamp": timestamp,
    }
    assert_schema(event, "audit-event.schema.json", f"audit event {sequence}")
    return event


def artifact_files() -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    for path in FIXTURE_DIR.glob("*.artifact.json"):
        value = load_json(path)
        artifacts[value["identity"]["designation"]] = value
    return artifacts


def run(output_dir: Path, execution_id: str, started_at: str, scenario: str = "gold") -> dict[str, Any]:
    registry = load_json(REGISTRY)
    registry_by_designation = {agent["designation"]: agent for agent in registry["agents"]}
    workflow = validate_workflow(registry_by_designation)
    validate_state_machines()
    validate_artifacts(workflow, registry_by_designation)

    nodes = {node["node_id"]: node for node in workflow["nodes"]}
    order = topological_order(workflow)
    artifacts = artifact_files()
    authorized_partial_designations: set[str] = set()
    if scenario == "authorized_incomplete_input":
        authorized_partial_designations = {"CAP-RISK", "ENT-EVIDENCE", "ENT-SYSRISK"}
        for designation in authorized_partial_designations:
            artifacts[designation]["artifact"]["lifecycle_state"] = "incomplete_input"
    decision = load_json(FIXTURE_DIR / "human-decision-request.json")
    validate_artifact_payloads(workflow, registry_by_designation, artifacts, decision, authorized_partial_designations)
    artifact_by_node = {node_id: artifacts[nodes[node_id]["designation"]] for node_id in order}
    incoming_edges = {node_id: [] for node_id in order}
    for edge in workflow["edges"]:
        incoming_edges[edge["to"]].append(edge)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    audit: list[dict[str, Any]] = []
    sequence = 0
    audit.append(make_audit_event(sequence, execution_id, "ORCH-SCHED", "workflow_validated", workflow["workflow_id"], "received", "scheduled", "SCHEDULE_READY", [workflow["workflow_id"]], started_at))
    sequence += 1

    schedule = {
        "workflow_id": workflow["workflow_id"],
        "workflow_version": workflow["workflow_version"],
        "policy_version": workflow["policy_version"],
        "execution_id": execution_id,
        "ordered_nodes": order,
        "dependency_state": "acyclic_and_declared",
        "status": "scheduled",
        "execution_environment": copy.deepcopy(DEFAULT_EXECUTION_ENVIRONMENT),
    }
    write_json(output_dir / "schedule.json", schedule)

    if scenario in {"timeout_failure", "superseded_failure"}:
        if scenario == "timeout_failure":
            controller, reason, subject = "ORCH-FANOUT", "DISPATCH_TIMEOUT", "spec-secrets"
        else:
            controller, reason, subject = "ORCH-FANIN", "SUPERSESSION_INVALID", "cap-risk"
        audit.append(make_audit_event(sequence, execution_id, controller, "execution_failed", subject, "validating", "failed", reason, [subject], started_at))
        summary = {"workflow_id": workflow["workflow_id"], "execution_id": execution_id, "status": "failed", "scenario": scenario, "reason_code": reason, "nodes_scheduled": len(order), "nodes_routed": 0, "gate_failures": 1, "partial_inputs": 0, "retries": 0, "timeouts": 1 if scenario == "timeout_failure" else 0, "escalations": 1, "audit_events": len(audit), "human_decision_requests": 0}
        write_json(output_dir / "audit-events.json", audit)
        write_json(output_dir / "summary.json", summary)
        return summary

    routed: list[dict[str, Any]] = []
    for node_id in order:
        node = nodes[node_id]
        artifact = artifact_by_node[node_id]
        input_manifest: list[dict[str, Any]] = []
        if not incoming_edges[node_id]:
            input_manifest.append({
                "artifact_id": "SOURCE-EVIDENCE-001", "artifact_type": "source-evidence",
                "hash": "sha256:fixture-evidence-001", "schema": "fixture-source-evidence",
                "producer_designation": "HUMAN-FIXTURE-AUTHORITY", "lifecycle_state": "complete",
                "freshness_state": "fresh", "required": True
            })
        for edge in sorted(incoming_edges[node_id], key=lambda item: item["from"]):
            source_artifact = artifact_by_node[edge["from"]]
            input_manifest.append({
                "artifact_id": source_artifact["artifact"]["artifact_id"],
                "artifact_type": edge["artifact_type"],
                "hash": source_artifact["integrity"]["output_hash"],
                "schema": nodes[edge["from"]]["output_schema"],
                "producer_designation": nodes[edge["from"]]["designation"],
                "lifecycle_state": source_artifact["artifact"]["lifecycle_state"],
                "freshness_state": "fresh",
                "required": edge["required"]
            })
        partial_authorization = None
        if node["designation"] in authorized_partial_designations:
            partial_authorization = {"authorization_id": "PARTIAL-AUTH-001", "authority_role": "fixture-review-authority", "missing_inputs": ["runtime identity-service recovery evidence"], "limitations": ["Risk posture cannot establish recovery effectiveness"], "expires_at": "2026-08-01T00:00:00Z"}
        envelope = {
            "dispatch_id": stable_uuid(execution_id, "dispatch", node_id),
            "workflow_id": workflow["workflow_id"],
            "workflow_version": workflow["workflow_version"],
            "execution_id": execution_id,
            "node_id": node_id,
            "agent": {"agent_uuid": node["agent_uuid"], "designation": node["designation"], "contract_version": registry_by_designation[node["designation"]]["contract_version"]},
            "scope": artifact["scope"],
            "input_manifest": input_manifest,
            "version_pins": workflow["version_pins"],
            "execution_environment": copy.deepcopy(DEFAULT_EXECUTION_ENVIRONMENT),
            "expected_output": {"universal_schema": "universal-agent-artifact.schema.json", "layer": node["layer"], "layer_schema": node["output_schema"], "role_schema": node["role_schema"], "consumers": node["consumers"]},
            "partial_input_authorization": partial_authorization,
            "created_at": started_at
        }
        assert_schema(envelope, "dispatch-envelope.schema.json", f"dispatch {node_id}")
        write_json(output_dir / "dispatch" / f"{node_id}.json", envelope)
        if scenario == "retry_then_success" and node_id == "prod-sec":
            audit.append(make_audit_event(sequence, execution_id, "ORCH-FANOUT", "dispatch_retry_scheduled", node_id, "dispatching", "retry_wait", "DISPATCH_RETRY_SCHEDULED", [envelope["dispatch_id"]], started_at))
            sequence += 1
            audit.append(make_audit_event(sequence, execution_id, "ORCH-FANOUT", "dispatch_retry_started", node_id, "retry_wait", "dispatching", "DISPATCH_RETRY_STARTED", [envelope["dispatch_id"]], started_at))
            sequence += 1
        audit.append(make_audit_event(sequence, execution_id, "ORCH-FANOUT", "node_dispatched", node_id, "ready", "dispatched", "DISPATCH_COMPLETE", [envelope["dispatch_id"]], started_at))
        sequence += 1

        checks = [
            {"check": name, "state": "passed", "details": "Validated by deterministic reference runner"}
            for name in ("identity", "schema", "integrity", "lineage", "freshness", "completeness", "conflict_preservation", "capa", "authority", "routing")
        ]
        partial_node = node["designation"] in authorized_partial_designations
        gate = {
            "gate_result_id": stable_uuid(execution_id, "gate", node_id),
            "workflow_id": workflow["workflow_id"],
            "execution_id": execution_id,
            "node_id": node_id,
            "artifact_id": artifact["artifact"]["artifact_id"],
            "checks": checks,
            "gate_state": "passed_incomplete_input" if partial_node else "passed",
            "confidence_effect": {"delta": -0.1 if partial_node else 0.0, "reason": "Authorized partial input propagated" if partial_node else "All required checks passed"},
            "partial_input_authorization": partial_authorization,
            "escalations": [],
            "evaluated_at": started_at
        }
        assert_schema(gate, "gate-result.schema.json", f"gate {node_id}")
        write_json(output_dir / "gates" / f"{node_id}.json", gate)
        audit.append(make_audit_event(sequence, execution_id, "ORCH-FANIN", "artifact_routed", node_id, "validating_identity", "routed", "ROUTING_COMPLETE", [artifact["artifact"]["artifact_id"], gate["gate_result_id"]], started_at))
        sequence += 1
        routed.append({"node_id": node_id, "artifact_id": artifact["artifact"]["artifact_id"], "consumers": node["consumers"], "immutable": True})

    assert_schema(decision, "human-decision-request.schema.json", "human decision request")
    write_json(output_dir / "human-decision-request.json", decision)
    routing = {"workflow_id": workflow["workflow_id"], "execution_id": execution_id, "routing_results": routed, "human_gate": workflow["human_gates"][0], "decision_request": decision["decision_context_id"]}
    write_json(output_dir / "routing.json", routing)
    write_json(output_dir / "audit-events.json", audit)
    partial_count = len(authorized_partial_designations)
    summary = {"workflow_id": workflow["workflow_id"], "execution_id": execution_id, "status": "incomplete_input" if partial_count else "complete", "scenario": scenario, "nodes_scheduled": len(order), "nodes_routed": len(routed), "gate_failures": 0, "partial_inputs": partial_count, "retries": 1 if scenario == "retry_then_success" else 0, "timeouts": 0, "escalations": 0, "audit_events": len(audit), "human_decision_requests": 1}
    write_json(output_dir / "summary.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--execution-id", default=DEFAULT_EXECUTION_ID)
    parser.add_argument("--started-at", default=DEFAULT_STARTED_AT)
    parser.add_argument("--scenario", choices=["gold", "authorized_incomplete_input", "retry_then_success", "timeout_failure", "superseded_failure"], default="gold")
    parser.add_argument("--ledger-dir", type=Path, help="Persist the completed run to the immutable reference ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run(args.output_dir.resolve(), args.execution_id, args.started_at, args.scenario)
    if args.ledger_dir:
        from artifact_ledger import ArtifactLedger

        ledger = ArtifactLedger(args.ledger_dir.resolve())
        persistence = ledger.persist_execution(args.output_dir.resolve(), sorted(FIXTURE_DIR.glob("*.artifact.json")),
                                               ROOT / "appendices" / "example-workflows" / "vertical-risk-slice.workflow.json")
        summary = {**summary, "persistence": persistence}
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

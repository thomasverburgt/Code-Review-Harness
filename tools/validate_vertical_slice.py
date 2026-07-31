#!/usr/bin/env python3
"""Zero-dependency validator for the executable vertical-risk reference slice."""

from __future__ import annotations

import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "appendices" / "schemas"
WORKFLOW = ROOT / "appendices" / "example-workflows" / "vertical-risk-slice.workflow.json"
FIXTURE_DIR = ROOT / "fixtures" / "vertical-risk-slice" / "gold"
REGISTRY = ROOT / "agents" / "agent-identities.json"
STATE_DIR = ROOT / "orchestration" / "state-machines"


class ValidationFailure(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationFailure(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def resolve_pointer(schema: dict[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise ValidationFailure(f"unsupported non-local $ref: {reference}")
    value: Any = schema
    for part in reference[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[part]
    return value


def type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return False


def validate_format(value: str, format_name: str, path: str) -> list[str]:
    errors: list[str] = []
    try:
        if format_name == "uuid":
            uuid.UUID(value)
        elif format_name == "date-time":
            datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        errors.append(f"{path}: invalid {format_name}: {value!r}")
    return errors


def validate_instance(value: Any, rule: dict[str, Any], root_schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    if "$ref" in rule:
        return validate_instance(value, resolve_pointer(root_schema, rule["$ref"]), root_schema, path)
    for subrule in rule.get("allOf", []):
        errors.extend(validate_instance(value, subrule, root_schema, path))
    if "const" in rule and value != rule["const"]:
        errors.append(f"{path}: expected constant {rule['const']!r}, got {value!r}")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {rule['enum']!r}")
    expected = rule.get("type")
    if expected is not None:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(type_matches(value, choice) for choice in choices):
            errors.append(f"{path}: expected type {choices}, got {type(value).__name__}")
            return errors
    if isinstance(value, dict):
        required = rule.get("required", [])
        for name in required:
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")
        if len(value) < rule.get("minProperties", 0):
            errors.append(f"{path}: too few properties")
        properties = rule.get("properties", {})
        for name, child in value.items():
            child_path = f"{path}.{name}"
            if name in properties:
                errors.extend(validate_instance(child, properties[name], root_schema, child_path))
            else:
                additional = rule.get("additionalProperties", True)
                if additional is False:
                    errors.append(f"{child_path}: additional property is prohibited")
                elif isinstance(additional, dict):
                    errors.extend(validate_instance(child, additional, root_schema, child_path))
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if rule.get("uniqueItems"):
            canonical = [json.dumps(item, sort_keys=True) for item in value]
            if len(canonical) != len(set(canonical)):
                errors.append(f"{path}: items are not unique")
        item_rule = rule.get("items")
        if isinstance(item_rule, dict):
            for index, child in enumerate(value):
                errors.extend(validate_instance(child, item_rule, root_schema, f"{path}[{index}]"))
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            errors.append(f"{path}: value {value!r} does not match {rule['pattern']!r}")
        if "format" in rule:
            errors.extend(validate_format(value, rule["format"], path))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in rule and value < rule["minimum"]:
            errors.append(f"{path}: value below minimum")
        if "maximum" in rule and value > rule["maximum"]:
            errors.append(f"{path}: value above maximum")
    return errors


def assert_schema(instance: Any, schema_name: str, label: str) -> None:
    schema = load_json(SCHEMAS / schema_name)
    errors = validate_instance(instance, schema, schema)
    if errors:
        formatted = "\n  - ".join(errors)
        raise ValidationFailure(f"{label} failed {schema_name}:\n  - {formatted}")


def validate_workflow_instance(workflow: dict[str, Any], registry_by_designation: dict[str, dict[str, Any]], label: str = "workflow") -> dict[str, Any]:
    assert_schema(workflow, "workflow-definition.schema.json", label)
    nodes = {node["node_id"]: node for node in workflow["nodes"]}
    if len(nodes) != len(workflow["nodes"]):
        raise ValidationFailure("workflow contains duplicate node_id values")
    for node in nodes.values():
        registered = registry_by_designation.get(node["designation"])
        if registered is None:
            raise ValidationFailure(f"unregistered workflow agent {node['designation']}")
        if registered["agent_uuid"] != node["agent_uuid"] or registered["layer"] != node["layer"]:
            raise ValidationFailure(f"identity mismatch for {node['designation']}")
        for schema_name in (node["output_schema"], node["role_schema"]):
            if not (SCHEMAS / schema_name).is_file():
                raise ValidationFailure(f"missing schema {schema_name} for {node['node_id']}")
    adjacency = {node_id: [] for node_id in nodes}
    incoming = {node_id: set() for node_id in nodes}
    for edge in workflow["edges"]:
        if edge["from"] not in nodes or edge["to"] not in nodes:
            raise ValidationFailure(f"edge references unknown node: {edge}")
        adjacency[edge["from"]].append(edge["to"])
        incoming[edge["to"]].add(edge["from"])
        if edge["to"] not in nodes[edge["from"]]["consumers"]:
            raise ValidationFailure(f"edge consumer is undeclared: {edge}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise ValidationFailure(f"workflow graph contains a cycle at {node_id}")
        if node_id in visited:
            return
        visiting.add(node_id)
        for target in adjacency[node_id]:
            visit(target)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)
    for node_id, node in nodes.items():
        declared_nodes = {value for value in node["required_inputs"] if value in nodes}
        if declared_nodes != incoming[node_id]:
            raise ValidationFailure(f"required_inputs/edge mismatch for {node_id}: declared={sorted(declared_nodes)} incoming={sorted(incoming[node_id])}")
    for gate in workflow["human_gates"]:
        if gate["after_node"] not in nodes:
            raise ValidationFailure(f"human gate references unknown node: {gate['after_node']}")
    return workflow


def validate_workflow(registry_by_designation: dict[str, dict[str, Any]]) -> dict[str, Any]:
    workflow = load_json(WORKFLOW)
    return validate_workflow_instance(workflow, registry_by_designation, str(WORKFLOW.relative_to(ROOT)))


def validate_state_machines() -> None:
    for path in sorted(STATE_DIR.glob("*.json")):
        instance = load_json(path)
        assert_schema(instance, "orchestration-state-machine.schema.json", str(path.relative_to(ROOT)))
        states = set(instance["states"])
        if instance["initial_state"] not in states or not set(instance["terminal_states"]).issubset(states):
            raise ValidationFailure(f"{path.relative_to(ROOT)}: initial or terminal state is undeclared")
        for transition in instance["transitions"]:
            if transition["from"] not in states or transition["to"] not in states:
                raise ValidationFailure(f"{path.relative_to(ROOT)}: transition references undeclared state")


def validate_artifact_payloads(workflow: dict[str, Any], registry_by_designation: dict[str, dict[str, Any]], artifacts_by_designation: dict[str, dict[str, Any]], decision: dict[str, Any], authorized_partial_designations: set[str] | None = None, replacement_designation: str | None = None, external_input_designations: set[str] | None = None) -> None:
    authorized_partial_designations = authorized_partial_designations or set()
    external_input_designations = external_input_designations or set()
    artifacts_by_id: dict[str, dict[str, Any]] = {}
    layer_schema = {"specialist": "specialist-extension.schema.json", "product": "product-extension.schema.json", "capability": "capability-extension.schema.json", "enterprise": "enterprise-extension.schema.json"}
    role_schema = {node["designation"]: node["role_schema"] for node in workflow["nodes"]}
    for designation, artifact in artifacts_by_designation.items():
        label = f"artifact {designation}"
        assert_schema(artifact, "universal-agent-artifact.schema.json", label)
        actual_designation = artifact["identity"]["designation"]
        if actual_designation != designation:
            raise ValidationFailure(f"{label}: map key/designation mismatch")
        registered = registry_by_designation.get(designation)
        if registered is None or registered["agent_uuid"] != artifact["identity"]["agent_uuid"]:
            raise ValidationFailure(f"{label}: artifact identity does not match registry")
        if registered["contract_version"] != artifact["identity"]["contract_version"]:
            raise ValidationFailure(f"{label}: contract version does not match registry")
        layer = registered["layer"]
        extension = artifact.get("extensions", {}).get(layer)
        if extension is None:
            raise ValidationFailure(f"{label}: missing extensions.{layer}")
        assert_schema(extension, layer_schema[layer], f"{label} extensions.{layer}")
        assert_schema(extension["role"], role_schema[designation], f"{label} role")
        if extension["role"].get("designation") != designation:
            raise ValidationFailure(f"{label}: role designation mismatch")
        artifacts_by_id[artifact["artifact"]["artifact_id"]] = artifact
        lifecycle = artifact["artifact"]["lifecycle_state"]
        if lifecycle == "incomplete_input" and designation in authorized_partial_designations:
            pass
        elif lifecycle != "complete":
            raise ValidationFailure(f"{label}: gold execution requires complete lifecycle without partial authorization")
        for item in artifact.get("inputs", []):
            if item.get("freshness") == "stale":
                raise ValidationFailure(f"{label}: stale input is not authorized")
        for finding in artifact.get("findings", []):
            capa = finding.get("capa")
            if not isinstance(capa, dict):
                raise ValidationFailure(f"{label}: finding {finding.get('finding_id')} lacks CAPA")
            required_capa = {"corrective_action", "preventive_action", "owner_role", "target_horizon", "implementation_level", "validation_method"}
            if not required_capa.issubset(capa):
                raise ValidationFailure(f"{label}: finding {finding.get('finding_id')} has incomplete CAPA")
        serialized = json.dumps(artifact)
        if "BEGIN PRIVATE KEY" in serialized or '"secret_value"' in serialized:
            raise ValidationFailure(f"{label}: restricted secret material is present")
    expected_designations = {node["designation"] for node in workflow["nodes"]}
    if set(artifacts_by_designation) != expected_designations:
        raise ValidationFailure(f"fixture artifact set mismatch: expected={sorted(expected_designations)} actual={sorted(artifacts_by_designation)}")
    node_by_id = {node["node_id"]: node for node in workflow["nodes"]}
    for edge in workflow["edges"]:
        source_designation = node_by_id[edge["from"]]["designation"]
        target_designation = node_by_id[edge["to"]]["designation"]
        if source_designation in authorized_partial_designations and target_designation not in authorized_partial_designations:
            raise ValidationFailure(f"partial input from {source_designation} was not preserved by {target_designation}")
    for edge in workflow["edges"]:
        if node_by_id[edge["from"]]["designation"] == replacement_designation:
            continue
        if node_by_id[edge["to"]]["designation"] in external_input_designations:
            continue
        source = artifacts_by_designation[node_by_id[edge["from"]]["designation"]]
        target = artifacts_by_designation[node_by_id[edge["to"]]["designation"]]
        source_id = source["artifact"]["artifact_id"]
        source_hash = source["integrity"]["output_hash"]
        matching = [item for item in target["inputs"] if item.get("artifact_id") == source_id]
        if not matching or matching[0].get("hash") != source_hash:
            raise ValidationFailure(f"fixture lineage/hash mismatch for edge {edge['from']} -> {edge['to']}")
        if source_id not in target["artifact"]["links"]["children"]:
            raise ValidationFailure(f"target child link missing for edge {edge['from']} -> {edge['to']}")
    assert_schema(decision, "human-decision-request.schema.json", "gold human decision request")
    final_id = artifacts_by_designation["ENT-SYSRISK"]["artifact"]["artifact_id"]
    if replacement_designation != "ENT-SYSRISK" and final_id not in decision["triggering_artifacts"]:
        raise ValidationFailure("human decision request does not reference final ENT-SYSRISK artifact")


def load_gold_payloads() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    manifest = load_json(FIXTURE_DIR / "input-manifest.json")
    artifacts: dict[str, dict[str, Any]] = {}
    for name in manifest["artifacts"]:
        if not name.endswith(".artifact.json"):
            continue
        artifact = load_json(FIXTURE_DIR / name)
        artifacts[artifact["identity"]["designation"]] = artifact
    return artifacts, load_json(FIXTURE_DIR / "human-decision-request.json")


def validate_artifacts(workflow: dict[str, Any], registry_by_designation: dict[str, dict[str, Any]]) -> None:
    artifacts, decision = load_gold_payloads()
    validate_artifact_payloads(workflow, registry_by_designation, artifacts, decision)


def main() -> int:
    try:
        registry = load_json(REGISTRY)
        registry_by_designation = {agent["designation"]: agent for agent in registry["agents"]}
        workflow = validate_workflow(registry_by_designation)
        validate_state_machines()
        validate_artifacts(workflow, registry_by_designation)
    except ValidationFailure as exc:
        print(f"vertical slice validation FAILED: {exc}", file=sys.stderr)
        return 1
    print("vertical slice validation passed: workflow=1; nodes=5; state_machines=3; gold_artifacts=5; human_decision_requests=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

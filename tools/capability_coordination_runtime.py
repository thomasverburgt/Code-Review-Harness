#!/usr/bin/env python3
"""Deterministic CAP-COORD validation, inventory, traceability, and routing."""

from __future__ import annotations

import copy
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


COORDINATOR_UUID = "38d55885-5785-4da7-b4a7-94ca65e652e5"
COORDINATOR_NAMESPACE = uuid.UUID("17000000-0000-4000-8000-000000000000")
GENERATED_AT = "2026-08-01T18:00:00Z"
ACCEPTED_CAP_RISK = ROOT / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-cap-risk.artifact.json"


def _stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(COORDINATOR_NAMESPACE, "|".join(parts)))


def _artifact_hash_is_valid(artifact: dict[str, Any]) -> bool:
    material = copy.deepcopy(artifact)
    expected = material.get("integrity", {}).get("output_hash")
    if not isinstance(expected, str):
        return False
    material["integrity"]["output_hash"] = None
    return content_hash(material) == expected


def _validate_artifact(artifact: dict[str, Any], registry: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    try:
        assert_schema(artifact, "universal-agent-artifact.schema.json", "capability coordinator input")
        designation = artifact["identity"]["designation"]
        identity = registry.get(designation)
        if not identity or identity["layer"] != "capability" or identity["agent_uuid"] != artifact["identity"]["agent_uuid"]:
            raise ValidationFailure(f"unregistered or mismatched capability identity: {designation}")
        if artifact["artifact"]["lifecycle_state"] != "complete":
            raise ValidationFailure(f"input {designation} is not complete")
        if artifact["integrity"]["schema_validation"] != "passed":
            raise ValidationFailure(f"input {designation} reports failed schema validation")
        if not _artifact_hash_is_valid(artifact):
            raise ValidationFailure(f"input {designation} failed output-hash verification")
        if designation == "CAP-RISK":
            assert_schema(artifact["extensions"]["capability"], "capability-extension.schema.json", "CAP-RISK capability extension")
            assert_schema(artifact["extensions"]["capability"]["role"], "cap-risk-role.schema.json", "CAP-RISK role")
        return designation, identity
    except (KeyError, TypeError) as exc:
        raise ValidationFailure(f"malformed capability coordinator input: {exc}") from exc


def _traceability(artifact: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_id = artifact["artifact"]["artifact_id"]
    records: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for finding in artifact.get("findings", []):
        records.append({"source_artifact_id": source_id, "record_kind": "finding", "record_id": finding["finding_id"],
                        "evidence_refs": sorted(finding.get("evidence_refs", []))})
    role = artifact.get("extensions", {}).get("capability", {}).get("role", {})
    for risk in role.get("risk_register", []):
        records.append({"source_artifact_id": source_id, "record_kind": "risk", "record_id": risk["risk_id"],
                        "evidence_refs": sorted(risk.get("contributing_artifacts", []))})
    for index, conflict in enumerate(artifact.get("conflicts", []), start=1):
        conflict_id = conflict.get("conflict_id") or f"CONFLICT-{index:03d}"
        preserved = {"source_artifact_id": source_id, "conflict_id": conflict_id,
                     "statement": conflict.get("statement", ""), "evidence_refs": sorted(conflict.get("evidence_refs", []))}
        conflicts.append(preserved)
        records.append({"source_artifact_id": source_id, "record_kind": "conflict", "record_id": conflict_id,
                        "evidence_refs": preserved["evidence_refs"]})
    for decision in artifact.get("decisions_requested", []):
        records.append({"source_artifact_id": source_id, "record_kind": "decision_request",
                        "record_id": decision["decision_context_id"], "evidence_refs": sorted(decision.get("evidence_refs", []))})
    return records, conflicts


def build_manifest(artifacts: list[dict[str, Any]], expected_designations: list[str], *,
                   capability_id: str = "CAPABILITY-IDENTITY-ACCESS",
                   freshness: dict[str, str] | None = None, compatibility: dict[str, str] | None = None,
                   partial_input_authorization: dict[str, Any] | None = None,
                   calibration_scope: str = "single_domain_mechanical_calibration") -> dict[str, Any]:
    if not expected_designations or len(expected_designations) != len(set(expected_designations)):
        raise ValidationFailure("expected capability designations must be non-empty and unique")
    if any(not item.startswith("CAP-") for item in expected_designations):
        raise ValidationFailure("expected input set contains a non-capability designation")
    if calibration_scope == "single_domain_mechanical_calibration" and len(expected_designations) != 1:
        raise ValidationFailure("single-domain calibration requires exactly one expected designation")
    if calibration_scope == "declared_multi_domain" and len(expected_designations) < 2:
        raise ValidationFailure("multi-domain coordination requires at least two expected designations")
    if calibration_scope not in {"single_domain_mechanical_calibration", "declared_multi_domain"}:
        raise ValidationFailure("unsupported capability coordination calibration scope")
    registry_doc = load_json(ROOT / "agents/agent-identities.json")
    registry = {item["designation"]: item for item in registry_doc["agents"]}
    fresh_map = freshness or {}
    compatible_map = compatibility or {}
    by_designation: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        designation, _ = _validate_artifact(artifact, registry)
        if designation in by_designation:
            raise ValidationFailure(f"duplicate capability input: {designation}")
        by_designation[designation] = artifact
    expected = sorted(expected_designations)
    received_designations = sorted(by_designation)
    missing = sorted(set(expected) - set(received_designations))
    extra = sorted(set(received_designations) - set(expected))
    if extra:
        raise ValidationFailure(f"undeclared capability inputs: {', '.join(extra)}")
    for designation in received_designations:
        if fresh_map.get(designation, "fresh") != "fresh":
            raise ValidationFailure(f"stale capability input: {designation}")
        if compatible_map.get(designation, "compatible") != "compatible":
            raise ValidationFailure(f"incompatible capability input: {designation}")
    if partial_input_authorization is not None:
        required = {"authorization_id", "missing_designations", "authority_role", "limitations", "expires_at"}
        if set(partial_input_authorization) != required:
            raise ValidationFailure("partial-input authorization has an invalid field set")
        if sorted(partial_input_authorization["missing_designations"]) != missing or not missing:
            raise ValidationFailure("partial-input authorization does not match the missing designation set")
        expiry = datetime.fromisoformat(partial_input_authorization["expires_at"].replace("Z", "+00:00"))
        generated = datetime.fromisoformat(GENERATED_AT.replace("Z", "+00:00"))
        if expiry <= generated or not partial_input_authorization["limitations"]:
            raise ValidationFailure("partial-input authorization is expired or unbounded")
    received_inputs: list[dict[str, Any]] = []
    traceability: list[dict[str, Any]] = []
    preserved_conflicts: list[dict[str, Any]] = []
    for designation in received_designations:
        artifact = by_designation[designation]
        received_inputs.append({"designation": designation, "artifact_id": artifact["artifact"]["artifact_id"],
                                "artifact_type": artifact["artifact"]["artifact_type"],
                                "output_hash": artifact["integrity"]["output_hash"],
                                "lifecycle_state": artifact["artifact"]["lifecycle_state"],
                                "freshness": "fresh", "compatibility": "compatible"})
        records, conflicts = _traceability(artifact)
        traceability.extend(records)
        preserved_conflicts.extend(conflicts)
    if missing and partial_input_authorization:
        route_state = "incomplete_authorized"
    elif missing:
        route_state = "blocked"
    else:
        route_state = "ready_for_cap_synth"
    manifest_id = _stable_uuid(capability_id, *expected, *[item["output_hash"] for item in received_inputs])
    manifest: dict[str, Any] = {
        "manifest_id": manifest_id, "manifest_version": "1.0.0", "generated_at": GENERATED_AT,
        "coordinator": {"agent_uuid": COORDINATOR_UUID, "designation": "CAP-COORD", "implementation": "deterministic"},
        "capability_id": capability_id, "calibration_scope": calibration_scope,
        "fitness_claim": "mechanical_coordination_only", "expected_designations": expected,
        "received_inputs": received_inputs, "missing_designations": missing, "extra_designations": [],
        "validation": {"identity": "passed", "schema": "passed", "integrity": "passed", "freshness": "passed",
                       "compatibility": "passed", "conflict_preservation": "passed"},
        "review_completeness": {"expected": len(expected), "valid": len(received_inputs),
                                "fraction": len(received_inputs) / len(expected)},
        "preserved_conflicts": sorted(preserved_conflicts, key=lambda item: (item["source_artifact_id"], item["conflict_id"])),
        "traceability": sorted(traceability, key=lambda item: (item["source_artifact_id"], item["record_kind"], item["record_id"])),
        "partial_input_authorization": copy.deepcopy(partial_input_authorization),
        "routing": {"state": route_state, "synthesis_dispatch_permitted": route_state == "ready_for_cap_synth", "consumer": "CAP-SYNTH"},
        "decision_authority": "human", "effect": "validation_and_routing_only",
        "integrity": {"input_hash": content_hash(received_inputs), "manifest_hash": "sha256:" + "0" * 64},
    }
    material = copy.deepcopy(manifest)
    material["integrity"]["manifest_hash"] = None
    manifest["integrity"]["manifest_hash"] = content_hash(material)
    assert_schema(manifest, "capability-input-manifest.schema.json", "capability input manifest")
    return manifest


def validate_for_cap_synth(manifest: dict[str, Any], artifacts: list[dict[str, Any]]) -> None:
    assert_schema(manifest, "capability-input-manifest.schema.json", "CAP-SYNTH dispatch manifest")
    material = copy.deepcopy(manifest)
    expected_hash = material["integrity"]["manifest_hash"]
    material["integrity"]["manifest_hash"] = None
    if content_hash(material) != expected_hash:
        raise ValidationFailure("CAP-SYNTH manifest hash mismatch")
    route = manifest["routing"]
    if route["state"] != "ready_for_cap_synth" or not route["synthesis_dispatch_permitted"]:
        raise ValidationFailure("CAP-SYNTH dispatch is not permitted")
    if manifest["missing_designations"] or manifest["extra_designations"] or manifest["partial_input_authorization"] is not None:
        raise ValidationFailure("CAP-SYNTH requires an exact complete input set")
    registry_doc = load_json(ROOT / "agents/agent-identities.json")
    registry = {item["designation"]: item for item in registry_doc["agents"]}
    for artifact in artifacts:
        _validate_artifact(artifact, registry)
    actual = sorted((item["identity"]["designation"], item["artifact"]["artifact_id"], item["integrity"]["output_hash"]) for item in artifacts)
    declared = sorted((item["designation"], item["artifact_id"], item["output_hash"]) for item in manifest["received_inputs"])
    if actual != declared:
        raise ValidationFailure("CAP-SYNTH artifacts do not match the coordinator manifest")
    if content_hash(manifest["received_inputs"]) != manifest["integrity"]["input_hash"]:
        raise ValidationFailure("CAP-SYNTH manifest input hash mismatch")


def persist_manifest(ledger_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    return ArtifactLedger(ledger_root).persist_record(
        f"capability-input-manifests/{manifest['manifest_id']}.json", "capability-input-manifest",
        manifest["manifest_id"], manifest, retention_class="architecture-evidence")

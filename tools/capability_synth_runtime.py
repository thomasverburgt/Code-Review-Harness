#!/usr/bin/env python3
"""ADR-0018 deterministic CAP-SYNTH candidate projection and admission controls."""

from __future__ import annotations

import copy
import uuid
from typing import Any

from artifact_ledger import content_hash
from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest, validate_for_cap_synth
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


NAMESPACE = uuid.UUID("18000000-0000-4000-8000-000000000000")
CAP_SYNTH_UUID = "ca95161d-d7dc-40b0-b233-fda505b18afe"
CREATED_AT = "2026-08-01T20:00:00Z"
BASELINE = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def rehash_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(artifact)
    return artifact


def build_adjudicated_inputs() -> list[dict[str, Any]]:
    risk = load_json(ACCEPTED_CAP_RISK)
    requirement = copy.deepcopy(risk)
    requirement["identity"] = {"agent_uuid": "9a82a407-38f6-4abe-9ef8-49f0fd256e67", "designation": "CAP-REQ",
                               "display_name": "Requirements Traceability Reviewer", "agent_version": "fixture-0.1.0", "contract_version": "1.0.0"}
    requirement["artifact"] = {"artifact_id": stable_uuid("adjudicated-cap-req"), "artifact_type": "capability-requirements-posture",
                               "created_at": CREATED_AT, "lifecycle_state": "complete", "links": {"parents": [], "children": [], "peers": []}}
    requirement["methodology"] = {"method": "adjudicated contract fixture", "limitations": ["Not accepted live operational evidence"]}
    requirement["observations"] = [{"observation_id": "OBS-REQ-001", "fact": "The security classification decision remains a requirement dependency.", "evidence_refs": ["UDS-0001"]}]
    requirement["assessments"] = [{"assessment_id": "ASM-REQ-001", "rationale": "Requirement closure depends on the unresolved classification.", "confidence": 0.9}]
    requirement["findings"] = [{"finding_id": "FINDING-REQ-001", "statement": "Requirement verification is incomplete while the credential-like value remains unclassified.",
                                "evidence_refs": ["UDS-0001"], "root_cause": "process_or_governance_gap", "impact": "Requirement closure cannot be demonstrated.",
                                "capa": {"corrective_action": "Record the authoritative classification.", "preventive_action": "Bind classification records to requirement verification.",
                                         "owner_role": "requirements_engineer", "target_horizon": "short_term", "implementation_level": "process_level", "validation_method": "independent requirements review"}}]
    requirement["patterns"], requirement["insights"], requirement["conflicts"] = [], [], []
    requirement["confidence"] = {"evidence": 0.95, "assessment": 0.9, "review": 1.0, "decision": None,
                                 "provenance": [{"source": "adjudicated fixture", "version": "0.1.0"}]}
    requirement["decisions_requested"] = [{"decision_context_id": "DC-REQ-001", "question": "Is the requirement satisfied after authoritative classification?", "required_authority": "requirements-acceptance-authority"}]
    requirement["consumers"] = ["CAP-SYNTH-CANDIDATE"]
    requirement["extensions"]["capability"]["requirement_traceability"] = {"state": "incomplete", "requirement_ids": ["REQ-001"]}
    requirement["extensions"]["capability"]["role"] = {"designation": "CAP-REQ", "fixture_status": "adjudicated_multi_domain_contract_fixture", "requirement_ids": ["REQ-001"]}
    requirement["integrity"] = {"input_hash": content_hash(["UDS-0001"]), "output_hash": None, "attestation_ref": None,
                                "retention_class": "fixture", "schema_validation": "passed"}
    rehash_artifact(requirement)
    assert_schema(requirement, "universal-agent-artifact.schema.json", "adjudicated CAP-REQ fixture")
    assert_schema(requirement["extensions"]["capability"], "capability-extension.schema.json", "adjudicated CAP-REQ extension")
    return [risk, requirement]


def _record_index(artifacts: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for artifact in artifacts:
        artifact_id = artifact["artifact"]["artifact_id"]
        for field, key, kind in (("observations", "observation_id", "observation"), ("assessments", "assessment_id", "assessment"),
                                 ("findings", "finding_id", "finding"), ("patterns", "pattern_id", "pattern"),
                                 ("insights", "insight_id", "insight"), ("conflicts", "conflict_id", "conflict"),
                                 ("decisions_requested", "decision_context_id", "decision_request")):
            for record in artifact.get(field, []):
                index[(artifact_id, record[key])] = {"kind": kind, "evidence_refs": sorted(record.get("evidence_refs", []))}
        for risk in artifact.get("extensions", {}).get("capability", {}).get("role", {}).get("risk_register", []):
            index[(artifact_id, risk["risk_id"])] = {"kind": "risk", "evidence_refs": sorted(risk.get("contributing_artifacts", []))}
    return index


def build_candidate(manifest: dict[str, Any], artifacts: list[dict[str, Any]], evidence_tier: str) -> dict[str, Any]:
    validate_for_cap_synth(manifest, artifacts)
    artifact_ids = sorted(item["artifact"]["artifact_id"] for item in artifacts)
    record_index = _record_index(artifacts)
    trace_keys = sorted((item["source_artifact_id"], item["record_id"]) for item in manifest["traceability"])
    preserved = [{"source_artifact_id": source_id, "source_record_id": record_id,
                  "record_kind": record_index[(source_id, record_id)]["kind"],
                  "evidence_refs": record_index[(source_id, record_id)]["evidence_refs"],
                  "preservation_state": "preserved_without_rewrite"} for source_id, record_id in trace_keys]
    is_multi = len(manifest["expected_designations"]) >= 2
    if evidence_tier == "adjudicated_multi_domain_contract_fixture" and not is_multi:
        raise ValidationFailure("adjudicated multi-domain tier requires at least two domains")
    if evidence_tier not in {"adjudicated_multi_domain_contract_fixture", "accepted_live_input_calibration"}:
        raise ValidationFailure("unsupported CAP-SYNTH evidence tier")
    fitness = "contract_fixture_only" if evidence_tier.startswith("adjudicated") else ("multi_domain_candidate_calibration" if is_multi else "protocol_lineage_smoke_only")
    derived = []
    if is_multi:
        finding_ids = [item["source_record_id"] for item in preserved if item["record_kind"] == "finding"]
        derived = [{"assertion_id": "DERIVED-CAPSYNTH-001", "statement": "Risk disposition and requirement closure depend on the same unresolved classification decision.",
                    "contributing_artifact_ids": artifact_ids, "contributing_record_ids": sorted(finding_ids)[:2],
                    "derivation_logic": "The preserved risk and requirement findings cite the same source evidence and unresolved classification context.",
                    "assumptions": ["The fixture source binding remains current"], "alternatives": ["Authoritative classification may resolve both records"],
                    "confidence": 0.85, "uncertainty": ["No authoritative classification decision is present"]}]
    candidate_id = stable_uuid(manifest["manifest_id"], evidence_tier, "candidate")
    confidence_inputs = [item.get("confidence", {}).get("assessment") for item in artifacts]
    role = {
        "designation": "CAP-SYNTH", "evidence_tier": evidence_tier, "fitness_claim": fitness,
        "synthesis_basis": {"coordinator_manifest_id": manifest["manifest_id"], "coordinator_manifest_hash": manifest["integrity"]["manifest_hash"],
                            "expected_designations": manifest["expected_designations"], "received_artifact_ids": artifact_ids, "completeness_state": "complete"},
        "preserved_child_assertions": preserved, "derived_capability_assertions": derived,
        "capability_posture": {"state": "human_decision_required", "rationale": "Preserved inputs contain unresolved decision requests.",
                                "limitations": ["Candidate comparison only", "Evidence tier does not authorize scheduling"], "advisory_only": True},
        "confidence_reconciliation": {"method": "preserve_inputs_and_bounded_minimum", "inputs": confidence_inputs,
                                      "result": min(value for value in confidence_inputs if isinstance(value, (int, float))),
                                      "uncertainty": ["Unlike domain confidence values are not averaged"]},
        "enterprise_handoff": {"capability_id": manifest["capability_id"], "artifact_id": candidate_id,
                               "preserved_record_ids": sorted(item["source_record_id"] for item in preserved),
                               "derived_assertion_ids": [item["assertion_id"] for item in derived],
                               "unresolved_conflict_ids": sorted(item["conflict_id"] for item in manifest["preserved_conflicts"]),
                               "decision_request_ids": sorted(item["source_record_id"] for item in preserved if item["record_kind"] == "decision_request"),
                               "intended_consumers": ["ENT-SYNTH-CANDIDATE-COMPARISON"], "handoff_state": "comparison_only"},
        "decision_authority": "human",
    }
    candidate = {
        "identity": {"agent_uuid": CAP_SYNTH_UUID, "designation": "CAP-SYNTH", "display_name": "Capability Synthesis Lead", "agent_version": "design-0.1.0", "contract_version": "1.0.0"},
        "artifact": {"artifact_id": candidate_id, "artifact_type": "capability-synthesis-posture", "created_at": CREATED_AT, "lifecycle_state": "complete", "links": {"parents": [], "children": artifact_ids, "peers": []}},
        "execution": {"execution_id": stable_uuid(candidate_id, "execution"), "model": "deterministic-reference-agent", "prompt_version": "design-0.1.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}, "evidence_tier": evidence_tier},
        "scope": {"capability_id": manifest["capability_id"], "decision_context": "candidate_admission", "included": manifest["expected_designations"], "excluded": ["baseline scheduling", "reports", "governance", "deployment"]},
        "inputs": [{"artifact_id": item["artifact_id"], "hash": item["output_hash"], "compatibility": "compatible", "freshness": "fresh"} for item in manifest["received_inputs"]],
        "methodology": {"method": "preserve-correlate-project", "limitations": role["capability_posture"]["limitations"]},
        "coverage": {"eligible": len(artifacts), "reviewed": len(artifacts), "omitted": 0, "inaccessible": 0, "unknown": 0, "negative_evidence": 0},
        "observations": [], "assessments": [], "findings": [], "patterns": [],
        "insights": [{"insight_id": "INSIGHT-CAPSYNTH-001", "statement": "Candidate evidence tier constrains all fitness claims.", "evidence_refs": [manifest["manifest_id"]]}],
        "conflicts": copy.deepcopy(manifest["preserved_conflicts"]),
        "confidence": {"evidence": 1.0, "assessment": role["confidence_reconciliation"]["result"], "review": 1.0, "decision": None,
                       "provenance": [{"artifact_id": item["artifact"]["artifact_id"], "confidence": item.get("confidence", {}).get("assessment")} for item in artifacts]},
        "decisions_requested": [{"decision_context_id": "DECISION-CAPSYNTH-001", "question": "Should this candidate proceed to a later promotion review after accepted live multi-domain evidence exists?", "required_authority": "project-maintainer"}],
        "consumers": ["ENT-SYNTH-CANDIDATE-COMPARISON"], "decision_authority": "human",
        "integrity": {"input_hash": content_hash({"manifest_hash": manifest["integrity"]["manifest_hash"], "inputs": manifest["received_inputs"]}),
                      "output_hash": None, "attestation_ref": None, "retention_class": "candidate-test", "schema_validation": "passed"},
        "extensions": {"capability": {"capability_id": manifest["capability_id"], "participating_products": ["PRODUCT-ALPHA"],
            "mission_thread": {}, "requirement_traceability": {}, "cross_product_interface_state": {}, "human_centered_systems_evaluation": {},
            "mission_effectiveness_evidence": [], "operational_readiness": {"state": "human_decision_required"},
            "capability_risk_posture": {"state": "undisposed", "decision_authority": "human"},
            "technical_confidence_rollup": role["confidence_reconciliation"], "capability_confidence_score": role["confidence_reconciliation"]["result"],
            "decision_conflicts": copy.deepcopy(manifest["preserved_conflicts"]), "enterprise_escalations": copy.deepcopy(candidate_decisions(role)), "role": role}}
    }
    rehash_artifact(candidate)
    validate_candidate(candidate, manifest, artifacts)
    return candidate


def candidate_decisions(role: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"escalation_id": item, "authority": "human"} for item in role["enterprise_handoff"]["decision_request_ids"]]


def validate_candidate(candidate: dict[str, Any], manifest: dict[str, Any], artifacts: list[dict[str, Any]]) -> None:
    validate_for_cap_synth(manifest, artifacts)
    assert_schema(candidate, "universal-agent-artifact.schema.json", "CAP-SYNTH candidate")
    extension = candidate["extensions"]["capability"]
    assert_schema(extension, "capability-extension.schema.json", "CAP-SYNTH capability extension")
    role = extension["role"]
    assert_schema(role, "cap-synth-role.schema.json", "CAP-SYNTH role")
    if candidate["identity"]["agent_uuid"] != CAP_SYNTH_UUID or candidate["identity"]["designation"] != "CAP-SYNTH":
        raise ValidationFailure("CAP-SYNTH identity mismatch")
    material = copy.deepcopy(candidate); expected_hash = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != expected_hash:
        raise ValidationFailure("CAP-SYNTH output hash mismatch")
    artifact_ids = {item["artifact"]["artifact_id"] for item in artifacts}
    if set(candidate["artifact"]["links"]["children"]) != artifact_ids or set(role["synthesis_basis"]["received_artifact_ids"]) != artifact_ids:
        raise ValidationFailure("CAP-SYNTH child lineage mismatch")
    if role["synthesis_basis"]["coordinator_manifest_id"] != manifest["manifest_id"] or role["synthesis_basis"]["coordinator_manifest_hash"] != manifest["integrity"]["manifest_hash"]:
        raise ValidationFailure("CAP-SYNTH coordinator binding mismatch")
    expected_records = {(item["source_artifact_id"], item["record_id"]): tuple(item["evidence_refs"]) for item in manifest["traceability"]}
    actual_records = {(item["source_artifact_id"], item["source_record_id"]): tuple(item["evidence_refs"]) for item in role["preserved_child_assertions"]}
    if actual_records != expected_records:
        raise ValidationFailure("CAP-SYNTH did not exactly preserve coordinator traceability")
    preserved_ids = {item["source_record_id"] for item in role["preserved_child_assertions"]}
    for derived in role["derived_capability_assertions"]:
        if not set(derived["contributing_artifact_ids"]).issubset(artifact_ids) or not set(derived["contributing_record_ids"]).issubset(preserved_ids):
            raise ValidationFailure("CAP-SYNTH derived assertion contains invented lineage")
    tier, fitness = role["evidence_tier"], role["fitness_claim"]
    if tier == "adjudicated_multi_domain_contract_fixture" and (len(artifacts) < 2 or fitness != "contract_fixture_only"):
        raise ValidationFailure("CAP-SYNTH fixture tier fitness mismatch")
    if tier == "accepted_live_input_calibration" and len(artifacts) == 1 and fitness != "protocol_lineage_smoke_only":
        raise ValidationFailure("single-domain live evidence cannot claim multi-domain fitness")
    if role["enterprise_handoff"]["artifact_id"] != candidate["artifact"]["artifact_id"] or role["enterprise_handoff"]["handoff_state"] != "comparison_only":
        raise ValidationFailure("CAP-SYNTH enterprise handoff is not comparison-only and exact")
    if candidate["decision_authority"] != "human" or role["decision_authority"] != "human":
        raise ValidationFailure("CAP-SYNTH decision authority must remain human")
    baseline = load_json(BASELINE)
    if any(node["designation"] == "CAP-SYNTH" for node in baseline["nodes"]):
        raise ValidationFailure("CAP-SYNTH candidate cannot be scheduled in the baseline workflow")


def assemble_model_candidate(model_role: dict[str, Any], manifest: dict[str, Any], artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    """Project only model-owned analytical fields into a harness-owned live-smoke envelope."""
    base = build_candidate(manifest, artifacts, "accepted_live_input_calibration")
    role = base["extensions"]["capability"]["role"]
    for field in ("preserved_child_assertions", "derived_capability_assertions", "capability_posture", "confidence_reconciliation"):
        if field not in model_role:
            raise ValidationFailure(f"CAP-SYNTH model payload omitted {field}")
        role[field] = copy.deepcopy(model_role[field])
    if len(artifacts) == 1 and role["derived_capability_assertions"]:
        raise ValidationFailure("single-domain model calibration cannot emit a cross-domain derivation")
    base["extensions"]["capability"]["technical_confidence_rollup"] = copy.deepcopy(role["confidence_reconciliation"])
    base["extensions"]["capability"]["capability_confidence_score"] = role["confidence_reconciliation"]["result"]
    base["confidence"]["assessment"] = role["confidence_reconciliation"]["result"]
    base["execution"]["model"] = "qwen3-32b"
    rehash_artifact(base)
    validate_candidate(base, manifest, artifacts)
    return base


def build_reference_package() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    artifacts = build_adjudicated_inputs()
    manifest = build_manifest(artifacts, ["CAP-RISK", "CAP-REQ"], calibration_scope="declared_multi_domain")
    candidate = build_candidate(manifest, artifacts, "adjudicated_multi_domain_contract_fixture")
    return artifacts, manifest, candidate

#!/usr/bin/env python3
"""ADR-0035 exact CAP-SYNTH-to-ENT-ARCH isolated evaluation runtime."""

from __future__ import annotations

import copy
import uuid
from typing import Any

from artifact_ledger import content_hash
from capability_synth_runtime import validate_candidate as validate_cap_synth
from capability_synth_semantic_acceptance_runtime import build_records as build_semantic_records
from enterprise_arch_runtime import BASELINE, ENT_EVIDENCE, rehash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


CAP_SYNTH_RUN = ROOT / "fixtures/capability-synth-admission/evidence/2026-08-02/adr0034/gx10-live-evaluation/successful-run"
CAP_SYNTH = CAP_SYNTH_RUN / "cap-synth-model-candidate.artifact.json"
CAP_SYNTH_MANIFEST = CAP_SYNTH_RUN / "capability-input-manifest.json"
CAP_RISK = CAP_SYNTH_RUN / "cap-risk-input.artifact.json"
CAP_REQ = CAP_SYNTH_RUN / "cap-req-input.artifact.json"
ELIGIBILITY = ROOT / "fixtures/capability-synth-admission/evidence/2026-08-02/adr0034/project-owner-semantic-disposition/enterprise-evaluation-eligibility.json"
REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
NAMESPACE = uuid.UUID("35000000-0000-4000-8000-000000000000")
GENERATED_AT = "2026-08-02T08:00:00Z"


def sid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def _hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value)
    material[field] = None
    value[field] = content_hash(material)
    return value


def load_exact_input(*, eligibility_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate, manifest = load_json(CAP_SYNTH), load_json(CAP_SYNTH_MANIFEST)
    children = [load_json(CAP_RISK), load_json(CAP_REQ)]
    validate_cap_synth(candidate, manifest, children)
    eligibility = copy.deepcopy(eligibility_override) if eligibility_override is not None else load_json(ELIGIBILITY)
    expected = build_semantic_records()[2]
    if eligibility != expected:
        raise ValidationFailure("ENT-ARCH input does not have the exact owner-finalized CAP-SYNTH eligibility")
    if eligibility["state"] != "eligible_for_enterprise_candidate_evaluation" or eligibility["rollback_state"] != "active":
        raise ValidationFailure("CAP-SYNTH enterprise-evaluation eligibility is absent or revoked")
    if (eligibility["candidate_id"], eligibility["candidate_hash"]) != (
            candidate["artifact"]["artifact_id"], candidate["integrity"]["output_hash"]):
        raise ValidationFailure("CAP-SYNTH eligibility candidate binding mismatch")
    return candidate, eligibility


def build_gate(candidate: dict[str, Any]) -> dict[str, Any]:
    gate = copy.deepcopy(load_json(ENT_EVIDENCE))
    candidate_id = candidate["artifact"]["artifact_id"]
    capability_id = candidate["extensions"]["capability"]["capability_id"]
    gate["artifact"]["artifact_id"] = sid("ent-evidence", candidate_id)
    gate["artifact"]["links"]["children"] = [candidate_id]
    gate["scope"]["participating_capabilities"] = [capability_id]
    gate["inputs"] = [{"artifact_id": candidate_id, "hash": candidate["integrity"]["output_hash"],
                       "compatibility": "compatible", "freshness": "fresh"}]
    gate["coverage"].update({"eligible": 1, "reviewed": 1, "omitted": 0, "inaccessible": 0, "unknown": 0})
    extension = gate["extensions"]["enterprise"]
    extension["participating_capabilities"] = [capability_id]
    extension["capability_input_manifest"] = [{"artifact_id": candidate_id, "state": "valid"}]
    extension["enterprise_traceability_manifest"] = {"artifact_ids": [candidate_id],
                                                        "excluded_child_artifact_ids": sorted(candidate["artifact"]["links"]["children"])}
    extension["role"]["validated_input_manifest"] = [{"artifact_id": candidate_id, "state": "valid"}]
    extension["role"]["completeness"] = {"required": 1, "valid": 1, "fraction": 1.0}
    extension["role"]["duplicate_or_superseded_inputs"] = []
    gate["observations"] = [{
        "observation_id": "OBS-ENTEVID-ADR35-001",
        "fact": "The declared CAP-SYNTH artifact is present, traceable, fresh, compatible, and admitted once for single-capability enterprise architecture evaluation.",
        "evidence_refs": [candidate_id],
    }]
    gate["integrity"]["input_hash"] = content_hash([candidate["integrity"]["output_hash"]])
    rehash(gate)
    assert_schema(gate, "universal-agent-artifact.schema.json", "ADR-0035 ENT-EVIDENCE gate")
    assert_schema(extension, "enterprise-extension.schema.json", "ADR-0035 ENT-EVIDENCE extension")
    assert_schema(extension["role"], "ent-evidence-role.schema.json", "ADR-0035 ENT-EVIDENCE role")
    return gate


def build_input_manifest(gate: dict[str, Any], candidate: dict[str, Any], eligibility: dict[str, Any]) -> dict[str, Any]:
    child_ids = sorted(candidate["artifact"]["links"]["children"])
    value = {
        "manifest_id": sid("input-manifest", candidate["artifact"]["artifact_id"], eligibility["record_hash"]),
        "manifest_version": "1.0.0", "generated_at": GENERATED_AT,
        "ent_evidence_gate": {"id": gate["artifact"]["artifact_id"], "hash": content_hash(gate)},
        "cap_synth_candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
        "cap_synth_eligibility": {"id": eligibility["eligibility_id"], "hash": eligibility["record_hash"]},
        "admitted_capability_artifact_ids": [candidate["artifact"]["artifact_id"]],
        "excluded_child_artifact_ids": child_ids,
        "anti_double_counting": "parent_only_children_retained_as_lineage",
        "evidence_tier": "accepted_live_multi_domain_single_capability_evaluation",
        "effect": "evaluation_input_only", "manifest_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "manifest_hash")
    assert_schema(value, "enterprise-architecture-evaluation-input.schema.json", "ADR-0035 input manifest")
    return value


def allowed_record_ids(candidate: dict[str, Any]) -> set[str]:
    role = candidate["extensions"]["capability"]["role"]
    preserved = role["preserved_child_assertions"]
    return ({item["source_record_id"] for item in preserved}
            | set(role["enterprise_handoff"]["preserved_record_ids"])
            | {ref for item in preserved for ref in item["evidence_refs"]}
            | {item["assertion_id"] for item in role["derived_capability_assertions"]})


def source_decision_map(candidate: dict[str, Any]) -> dict[str, str]:
    role = candidate["extensions"]["capability"]["role"]
    statements = [statement for assertion in role["derived_capability_assertions"] for statement in assertion["alternatives"]]
    qualified_ids = role["enterprise_handoff"]["decision_request_ids"]
    if len(statements) != len(qualified_ids) or len(set(qualified_ids)) != len(qualified_ids):
        raise ValidationFailure("ADR-0035 source decision lineage is incomplete or ambiguous")
    return dict(zip(statements, qualified_ids))


def qualify_decision_requests(role: dict[str, Any], candidate: dict[str, Any]) -> None:
    mapping = source_decision_map(candidate)
    for request in role["decision_requests"]:
        statement = request.get("statement") or request.get("question")
        identifier_key = "record_id" if "record_id" in request else "decision_context_id"
        if statement in mapping:
            request[identifier_key] = mapping[statement]
        elif str(request.get(identifier_key, "")).startswith("DC-"):
            raise ValidationFailure("ADR-0035 cannot retain an unqualified child decision identifier")


def deterministic_role(gate: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    candidate_id, gate_hash = candidate["artifact"]["artifact_id"], content_hash(gate)
    source = {"record_id": "ARCH-VIEW-ADR35-001",
              "statement": "The semantically accepted capability posture is unassessable; the bounded evidence does not support an architecture-coherence conclusion.",
              "source_artifact_ids": [candidate_id], "evidence_refs": ["DERIVED-001", "FINDING-REQ-GAP-001", "RISK-001"],
              "confidence": 0.85,
              "uncertainty": "Confidence concerns the unassessability conclusion, not architecture readiness or coherence."}
    return {
        "designation": "ENT-ARCH", "evidence_tier": "accepted_live_multi_domain_single_capability_evaluation",
        "fitness_claim": "single_capability_architecture_evaluation",
        "manifest_binding": {"gate_artifact_id": gate["artifact"]["artifact_id"], "gate_artifact_hash": gate_hash,
                             "capability_artifact_ids": [candidate_id], "capability_artifact_hashes": [content_hash(candidate)],
                             "binding_state": "exact"},
        "system_of_systems_views": [source],
        "architecture_coherence": {"state": "insufficient_evidence",
                                   "rationale": "One accepted multi-domain capability posture is unassessable and cannot establish system-of-systems coherence.",
                                   "source_artifact_ids": [candidate_id], "confidence": 0.85,
                                   "uncertainty": "No second operational capability or approved architecture source is present."},
        "dependency_topology": [], "shared_service_concentration": [], "failure_propagation": [],
        "target_state_alignment": {"state": "not_assessed", "reason": "No approved target-state source was supplied."},
        "transition_architecture": {"state": "not_assessed", "reason": "No approved transition architecture was supplied."},
        "architecture_debt": [], "architecture_findings": [{**source, "record_id": "ARCH-FINDING-ADR35-001"}],
        "capa_options": [],
        "decision_requests": [{"decision_context_id": "ARCH-DECISION-ADR35-001",
                               "question": "Is additional accepted architecture evidence required before architecture coherence can be evaluated?",
                               "required_authority": "project-owner"}],
        "unsupported_claims": [],
        "downstream_handoff": {"consumers": ["ENT-ARCHSTRAT-CANDIDATE", "ENT-TECHDEBT-CANDIDATE",
                                               "ENT-MODERNIZE-CANDIDATE", "ENT-SYNTH-CANDIDATE"],
                               "handoff_state": "comparison_only", "scheduled": False},
        "decision_authority": "human",
    }


def build_candidate(gate: dict[str, Any], source: dict[str, Any], model_role: dict[str, Any] | None = None) -> dict[str, Any]:
    expected = deterministic_role(gate, source)
    role = copy.deepcopy(expected if model_role is None else model_role)
    for key in ("designation", "evidence_tier", "fitness_claim", "manifest_binding", "dependency_topology",
                "shared_service_concentration", "failure_propagation", "target_state_alignment",
                "transition_architecture", "architecture_debt", "capa_options", "unsupported_claims",
                "downstream_handoff", "decision_authority"):
        role[key] = copy.deepcopy(expected[key])
    qualify_decision_requests(role, source)
    artifact_id = sid("ent-arch-candidate", source["integrity"]["output_hash"])
    capability_id = source["extensions"]["capability"]["capability_id"]
    candidate = {
        "identity": {"agent_uuid": "6f74e6ca-2ae2-4415-8f99-be1aef2bc94a", "designation": "ENT-ARCH",
                     "display_name": "Systems Architecture Reviewer", "agent_version": "design-0.1.0", "contract_version": "1.0.0"},
        "artifact": {"artifact_id": artifact_id, "artifact_type": "enterprise-architecture-posture",
                     "created_at": GENERATED_AT, "lifecycle_state": "complete",
                     "links": {"parents": [], "children": [gate["artifact"]["artifact_id"], source["artifact"]["artifact_id"]], "peers": []}},
        "execution": {"execution_id": sid(artifact_id, "execution"), "model": "qwen3-32b" if model_role is not None else "deterministic-reference-agent",
                      "prompt_version": "design-0.1.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0},
                      "evidence_tier": role["evidence_tier"]},
        "scope": {"enterprise_scope_id": "ENTERPRISE-FIXTURE-001", "participating_capabilities": [capability_id],
                  "assessment_period": "2026-08-02", "decision_context": "accepted_live_single_capability_architecture_evaluation"},
        "inputs": [{"artifact_id": gate["artifact"]["artifact_id"], "hash": content_hash(gate), "compatibility": "compatible", "freshness": "fresh"},
                   {"artifact_id": source["artifact"]["artifact_id"], "hash": content_hash(source), "compatibility": "compatible", "freshness": "fresh"}],
        "methodology": {"method": "eligibility-gated single-capability architecture evaluation",
                        "limitations": ["One capability only", "No cross-capability or target-state inference", "Comparison only"]},
        "coverage": {"eligible": 1, "reviewed": 1, "omitted": 0, "inaccessible": 0, "unknown": 0, "negative_evidence": 0},
        "observations": [], "assessments": [], "findings": [], "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 1.0, "assessment": role["architecture_coherence"]["confidence"], "review": 1.0, "decision": None,
                       "provenance": [{"artifact_id": source["artifact"]["artifact_id"], "confidence": source["confidence"]["assessment"]}]},
        "decisions_requested": copy.deepcopy(role["decision_requests"]),
        "consumers": role["downstream_handoff"]["consumers"], "decision_authority": "human",
        "integrity": {"input_hash": content_hash({"gate": content_hash(gate), "source": content_hash(source)}), "output_hash": None,
                      "attestation_ref": None, "retention_class": "candidate-test", "schema_validation": "passed"},
        "extensions": {"enterprise": {"enterprise_scope": {"enterprise_scope_id": "ENTERPRISE-FIXTURE-001", "assessment_period": "2026-08-02"},
            "participating_capabilities": [capability_id],
            "capability_input_manifest": [{"artifact_id": source["artifact"]["artifact_id"], "content_hash": content_hash(source), "state": "valid"}],
            "cross_capability_correlations": role["system_of_systems_views"], "enterprise_assertions": role["architecture_findings"],
            "systemic_dependencies": [], "enterprise_unknowns": [{"statement": role["architecture_coherence"]["uncertainty"]}],
            "unresolved_disagreements": [], "confidence_reconciliation": {"method": "preserve source confidence as confidence in unassessability",
                                                                            "result": role["architecture_coherence"]["confidence"]},
            "human_decision_requests": role["decision_requests"],
            "enterprise_traceability_manifest": {"gate_artifact_id": gate["artifact"]["artifact_id"],
                                                   "artifact_ids": [source["artifact"]["artifact_id"]],
                                                   "excluded_child_artifact_ids": sorted(source["artifact"]["links"]["children"])},
            "role": role}},
    }
    rehash(candidate)
    validate_candidate(candidate, gate, source)
    return candidate


def validate_input_manifest(manifest: dict[str, Any], gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any]) -> None:
    assert_schema(manifest, "enterprise-architecture-evaluation-input.schema.json", "ADR-0035 input manifest")
    if content_hash({**manifest, "manifest_hash": None}) != manifest["manifest_hash"]:
        raise ValidationFailure("ADR-0035 input manifest hash mismatch")
    if manifest["admitted_capability_artifact_ids"] != [source["artifact"]["artifact_id"]]:
        raise ValidationFailure("ADR-0035 parent-child double counting or substitution detected")
    if set(manifest["excluded_child_artifact_ids"]) != set(source["artifact"]["links"]["children"]):
        raise ValidationFailure("ADR-0035 excluded-child lineage mismatch")
    if (manifest["ent_evidence_gate"]["id"], manifest["ent_evidence_gate"]["hash"]) != (gate["artifact"]["artifact_id"], content_hash(gate)):
        raise ValidationFailure("ADR-0035 ENT-EVIDENCE gate binding mismatch")
    if (manifest["cap_synth_eligibility"]["id"], manifest["cap_synth_eligibility"]["hash"]) != (eligibility["eligibility_id"], eligibility["record_hash"]):
        raise ValidationFailure("ADR-0035 eligibility binding mismatch")


def validate_candidate(candidate: dict[str, Any], gate: dict[str, Any], source: dict[str, Any]) -> None:
    assert_schema(candidate, "universal-agent-artifact.schema.json", "ADR-0035 ENT-ARCH candidate")
    extension = candidate["extensions"]["enterprise"]
    assert_schema(extension, "enterprise-extension.schema.json", "ADR-0035 ENT-ARCH extension")
    role = extension["role"]
    assert_schema(role, "ent-arch-role.schema.json", "ADR-0035 ENT-ARCH role")
    material = copy.deepcopy(candidate); expected_hash = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != expected_hash:
        raise ValidationFailure("ADR-0035 ENT-ARCH output hash mismatch")
    binding = role["manifest_binding"]
    if (binding["gate_artifact_id"], binding["gate_artifact_hash"], binding["capability_artifact_ids"], binding["capability_artifact_hashes"]) != (
            gate["artifact"]["artifact_id"], content_hash(gate), [source["artifact"]["artifact_id"]], [content_hash(source)]):
        raise ValidationFailure("ADR-0035 ENT-ARCH exact input binding mismatch")
    if role["evidence_tier"] != "accepted_live_multi_domain_single_capability_evaluation" or role["fitness_claim"] != "single_capability_architecture_evaluation":
        raise ValidationFailure("ADR-0035 ENT-ARCH evidence tier mismatch")
    if role["dependency_topology"] or role["shared_service_concentration"] or role["failure_propagation"] or role["architecture_debt"] or role["capa_options"]:
        raise ValidationFailure("single-capability evidence cannot support topology, concentration, propagation, debt, or CAPA claims")
    if role["architecture_coherence"]["state"] != "insufficient_evidence" or role["target_state_alignment"].get("state") != "not_assessed" or role["transition_architecture"].get("state") != "not_assessed":
        raise ValidationFailure("ADR-0035 candidate overclaims architecture coherence, target state, or transition state")
    allowed = allowed_record_ids(source)
    for group in (role["system_of_systems_views"], role["architecture_debt"], role["architecture_findings"]):
        for item in group:
            if item["source_artifact_ids"] != [source["artifact"]["artifact_id"]] or not set(item["evidence_refs"]).issubset(allowed):
                raise ValidationFailure("ADR-0035 ENT-ARCH invented source or evidence lineage")
    decision_map = source_decision_map(source)
    qualified_ids = set(decision_map.values())
    seen: set[str] = set()
    for request in role["decision_requests"]:
        statement = request.get("statement") or request.get("question")
        identifier = request.get("record_id") or request.get("decision_context_id")
        if not identifier or identifier in seen:
            raise ValidationFailure("ADR-0035 decision identifiers must be present and unique")
        seen.add(identifier)
        if statement in decision_map and identifier != decision_map[statement]:
            raise ValidationFailure("ADR-0035 child decision identifier lost source qualification")
        if identifier in qualified_ids and statement not in decision_map:
            raise ValidationFailure("ADR-0035 qualified decision identifier is bound to the wrong statement")
        if identifier.startswith("DC-"):
            raise ValidationFailure("ADR-0035 bare child decision identifier is ambiguous")
    if role["unsupported_claims"] or role["downstream_handoff"]["scheduled"] or role["downstream_handoff"]["handoff_state"] != "comparison_only" or candidate["decision_authority"] != "human":
        raise ValidationFailure("ADR-0035 ENT-ARCH authority boundary violated")
    if any(node["designation"] == "ENT-ARCH" for node in load_json(BASELINE)["nodes"]):
        raise ValidationFailure("ADR-0035 cannot schedule ENT-ARCH in the baseline")


def build_review_packet(candidate: dict[str, Any], manifest: dict[str, Any], eligibility: dict[str, Any]) -> dict[str, Any]:
    value = {
        "packet_id": sid(candidate["artifact"]["artifact_id"], "semantic-review"), "packet_version": "1.0.0", "generated_at": GENERATED_AT,
        "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
        "input_manifest": {"id": manifest["manifest_id"], "hash": manifest["manifest_hash"]},
        "cap_synth_eligibility": {"id": eligibility["eligibility_id"], "hash": eligibility["record_hash"]},
        "review_dimensions": ["source_semantics", "anti_double_counting", "single_capability_scope", "unsupported_claim_suppression",
                              "confidence_and_uncertainty", "downstream_handoff", "authority_boundary", "rollback"],
        "review_state": "awaiting_human_semantic_review", "required_authority": "project-owner", "effect": "review_request_only",
        "cap_synth_scheduled": False, "ent_arch_scheduled": False, "report_effect": "none", "deployment_effect": "none",
        "packet_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "packet_hash")
    assert_schema(value, "enterprise-architecture-semantic-review-packet.schema.json", "ADR-0035 semantic review packet")
    return value


def build_compatibility(candidate: dict[str, Any]) -> dict[str, Any]:
    return {"record_id": sid(candidate["artifact"]["artifact_id"], "compatibility"), "generated_at": GENERATED_AT,
            "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
            "results": [{"consumer": "ENT-SYNTH", "state": "compatible_via_tiered_enterprise_domain_wrapper"},
                        {"consumer": "ENT-ARCHSTRAT", "state": "candidate_interface_only_unscheduled"},
                        {"consumer": "ENT-TECHDEBT", "state": "planned_interface_only"},
                        {"consumer": "ENT-MODERNIZE", "state": "planned_interface_only"}],
            "effect": "comparison_only", "scheduled": False}


def build_package(model_role: dict[str, Any] | None = None, *, eligibility_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], ...]:
    source, eligibility = load_exact_input(eligibility_override=eligibility_override)
    gate = build_gate(source)
    manifest = build_input_manifest(gate, source, eligibility)
    candidate = build_candidate(gate, source, model_role)
    review = build_review_packet(candidate, manifest, eligibility)
    return source, eligibility, gate, manifest, candidate, build_compatibility(candidate), review

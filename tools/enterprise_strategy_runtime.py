#!/usr/bin/env python3
"""ADR-0023 deterministic ENT-STRAT candidate projection and admission controls."""
from __future__ import annotations

import copy
import uuid
from pathlib import Path
from typing import Any

from artifact_ledger import ArtifactLedger, content_hash
from enterprise_arch_runtime import build_inputs
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

OBJECTIVES = ROOT / "fixtures/enterprise-strategy-admission/input/strategic-objective-manifest.json"
METHOD = ROOT / "fixtures/enterprise-strategy-admission/input/strategic-scoring-method-manifest.json"
AUTHORITY = ROOT / "appendices/governance/decision-authorities-0.1.0.json"
BASELINE = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"
NAMESPACE = uuid.UUID("23000000-0000-4000-8000-000000000000")
CREATED_AT = "2026-08-01T23:59:00Z"


def stable_id(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def rehash(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(artifact)
    return artifact


def _registered(role: str, action: str, scope: str) -> bool:
    record = next((x for x in load_json(AUTHORITY)["authorities"] if x["authority_role"] == role), None)
    return bool(record and record["authority_kind"] == "expert_decision_authority" and action in record["allowed_actions"] and scope in record["scope_ids"])


def validate_manifests(objectives: dict[str, Any], method: dict[str, Any]) -> None:
    assert_schema(objectives, "strategic-objective-manifest.schema.json", "strategic objective manifest")
    assert_schema(method, "strategic-scoring-method-manifest.schema.json", "strategic scoring method")
    objective_copy = copy.deepcopy(objectives)
    objective_hash = objective_copy["manifest_hash"]
    objective_copy["manifest_hash"] = None
    method_copy = copy.deepcopy(method)
    method_hash = method_copy["method_hash"]
    method_copy["method_hash"] = None
    if content_hash(objective_copy) != objective_hash or content_hash(method_copy) != method_hash:
        raise ValidationFailure("strategic manifest hash mismatch")
    if objectives["scope_id"] != method["scope_id"]:
        raise ValidationFailure("strategic manifest scope mismatch")
    if not _registered("enterprise-strategy-authority", "declare_strategic_objectives", objectives["scope_id"]):
        raise ValidationFailure("strategic objective authority is not registered")
    if not _registered("scoring-method-owner", "declare_strategic_scoring_method", method["scope_id"]):
        raise ValidationFailure("strategic scoring authority is not registered")
    measures = [m["measure_id"] for o in objectives["objectives"] for m in o["measures"]]
    if len(measures) != len(set(measures)) or set(measures) != set(method["weights"]):
        raise ValidationFailure("scoring weights do not exactly cover objective measures")
    if abs(sum(method["weights"].values()) - 1.0) > 1e-9:
        raise ValidationFailure("scoring weights must sum to one")


def load_manifests() -> tuple[dict[str, Any], dict[str, Any]]:
    objectives, method = load_json(OBJECTIVES), load_json(METHOD)
    validate_manifests(objectives, method)
    return objectives, method


def strategic_inputs(live: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    gate, artifacts = build_inputs(live)
    if live:
        observations = [{
            "artifact_id": artifacts[0]["artifact"]["artifact_id"],
            "artifact_hash": content_hash(artifacts[0]),
            "designation": artifacts[0]["identity"]["designation"],
            "evidence_tier": "accepted_live",
            "measure_values": {"MEASURE-ALIGNMENT": 0.6},
            "confidence": 0.7,
        }]
    else:
        observations = [
            {"artifact_id": artifacts[0]["artifact"]["artifact_id"], "artifact_hash": content_hash(artifacts[0]), "designation": "ENT-ARCH-FIXTURE", "evidence_tier": "adjudicated_fixture", "measure_values": {"MEASURE-ALIGNMENT": 0.7}, "confidence": 0.8},
            {"artifact_id": artifacts[1]["artifact"]["artifact_id"], "artifact_hash": content_hash(artifacts[1]), "designation": "ENT-GOV-FIXTURE", "evidence_tier": "adjudicated_fixture", "measure_values": {"MEASURE-RESILIENCE": 0.4}, "confidence": 0.75},
        ]
    return gate, artifacts, observations


def role_template(gate: dict[str, Any], artifacts: list[dict[str, Any]], observations: list[dict[str, Any]], objectives: dict[str, Any], method: dict[str, Any], live: bool = False) -> dict[str, Any]:
    values: dict[str, dict[str, Any]] = {}
    for observation in observations:
        for measure_id, value in observation["measure_values"].items():
            values[measure_id] = {"value": value, "artifact_id": observation["artifact_id"], "confidence": observation["confidence"], "evidence_tier": observation["evidence_tier"]}
    scorecards, distributions, missing = [], [], []
    for objective in objectives["objectives"]:
        components = []
        for measure in objective["measures"]:
            observed = values.get(measure["measure_id"])
            component = {"measure_id": measure["measure_id"], "direction": measure["direction"], "weight": method["weights"][measure["measure_id"]], "normalized_value": observed["value"] if observed else None, "source_artifact_ids": [observed["artifact_id"]] if observed else [], "source_evidence_tier": observed["evidence_tier"] if observed else "unavailable", "confidence": observed["confidence"] if observed else None, "state": "observed" if observed else "missing"}
            components.append(component)
            if not observed:
                missing.append({"objective_id": objective["objective_id"], "measure_id": measure["measure_id"], "effect": "Composite and complete objective confidence remain unavailable; no imputation performed."})
        scorecards.append({"objective_id": objective["objective_id"], "outcome": objective["outcome"], "components": components, "state": "complete_components_composite_prohibited" if all(x["state"] == "observed" for x in components) else "insufficient_evidence", "composite_score": None})
        observed_values = [x["normalized_value"] for x in components if x["normalized_value"] is not None]
        distributions.append({"objective_id": objective["objective_id"], "component_min": min(observed_values) if observed_values else None, "component_max": max(observed_values) if observed_values else None, "composite": None, "false_precision_avoided": True})
    return {
        "designation": "ENT-STRAT",
        "evidence_tier": "accepted_live_single_domain_protocol_smoke" if live else "adjudicated_multi_domain_scoring_fixture",
        "fitness_claim": "objective_method_protocol_lineage_smoke_only" if live else "scoring_contract_mechanics_only",
        "manifest_binding": {"gate_artifact_id": gate["artifact"]["artifact_id"], "gate_artifact_hash": content_hash(gate), "posture_artifact_ids": [x["artifact_id"] for x in observations], "posture_artifact_hashes": [x["artifact_hash"] for x in observations], "objective_manifest_id": objectives["manifest_id"], "objective_manifest_hash": content_hash(objectives), "scoring_method_id": method["method_id"], "scoring_method_hash": content_hash(method), "binding_state": "exact"},
        "input_evidence_tiers": [{"artifact_id": x["artifact_id"], "designation": x["designation"], "evidence_tier": x["evidence_tier"]} for x in observations],
        "objective_scorecards": scorecards,
        "normalization_method": method["normalization"],
        "weighting_model": copy.deepcopy(method["weights"]),
        "confidence_distributions": distributions,
        "sensitivity_analysis": [{"objective_id": x["objective_id"], "authorized_weight_delta": method["sensitivity"]["weight_delta"], "result": "not_calculated_composite_prohibited"} for x in objectives["objectives"]],
        "missing_data_effects": missing,
        "disagreement_register": [],
        "threshold_context": None,
        "strategic_confidence_posture": {"state": "insufficient_evidence", "advisory_only": True, "rationale": "Composite scoring is human-prohibited and live multi-domain evidence is not available."},
        "composite_score": None,
        "decision_requests": [],
        "unsupported_claims": [],
        "downstream_handoff": {"consumers": ["ENT-SYNTH-CANDIDATE", "ENT-PORTFOLIO-CANDIDATE"], "handoff_state": "comparison_only", "scheduled": False},
        "decision_authority": "human",
    }


def build_candidate(model_role: dict[str, Any] | None = None, live: bool = False, objectives_override: dict[str, Any] | None = None, method_override: dict[str, Any] | None = None) -> dict[str, Any]:
    default_objectives, default_method = load_manifests()
    objectives = copy.deepcopy(objectives_override or default_objectives)
    method = copy.deepcopy(method_override or default_method)
    validate_manifests(objectives, method)
    gate, artifacts, observations = strategic_inputs(live)
    role = role_template(gate, artifacts, observations, objectives, method, live)
    artifact_id = stable_id("live" if live else "fixture", "artifact")
    capabilities = [x["extensions"]["capability"]["capability_id"] for x in artifacts]
    candidate = {
        "identity": {"agent_uuid": "0275dcd7-ef2d-4535-8b3b-0e6da66ebff6", "designation": "ENT-STRAT", "display_name": "Strategic Scoring Agent", "agent_version": "design-0.1.0", "contract_version": "1.0.0"},
        "artifact": {"artifact_id": artifact_id, "artifact_type": "enterprise-strategic-confidence", "created_at": CREATED_AT, "lifecycle_state": "complete", "links": {"parents": [], "children": [gate["artifact"]["artifact_id"]] + [x["artifact_id"] for x in observations], "peers": []}},
        "execution": {"execution_id": stable_id(artifact_id, "execution"), "model": "qwen3-32b" if model_role is not None else "deterministic-reference-agent", "prompt_version": "design-0.1.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}},
        "scope": {"enterprise_scope_id": objectives["scope_id"], "participating_capabilities": capabilities, "assessment_period": "2026-08-01", "decision_context": "candidate_calibration"},
        "inputs": [{"artifact_id": gate["artifact"]["artifact_id"], "hash": content_hash(gate), "compatibility": "compatible", "freshness": "fresh"}] + [{"artifact_id": x["artifact_id"], "hash": x["artifact_hash"], "compatibility": "compatible", "freshness": "fresh"} for x in observations] + [{"reference": "strategic-objective-manifest", "hash": content_hash(objectives), "compatibility": "compatible", "freshness": "fresh"}, {"reference": "strategic-scoring-method-manifest", "hash": content_hash(method), "compatibility": "compatible", "freshness": "fresh"}],
        "methodology": {"method": "human-controlled strategic objective and scoring method projection", "limitations": ["Candidate-only evidence", "No strategy or decision authority"]},
        "coverage": {"eligible": sum(len(x["measures"]) for x in objectives["objectives"]), "reviewed": sum(1 for x in role["objective_scorecards"] for y in x["components"] if y["state"] == "observed"), "omitted": 0, "inaccessible": 0, "unknown": len(role["missing_data_effects"]), "negative_evidence": 0},
        "observations": [], "assessments": [], "findings": [], "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 0.7, "assessment": 1.0, "review": 1.0, "decision": None, "provenance": [{"source": "human-controlled strategic manifests", "version": "1.0.0"}]},
        "decisions_requested": [], "consumers": role["downstream_handoff"]["consumers"], "decision_authority": "human",
        "integrity": {"input_hash": content_hash({"gate": content_hash(gate), "postures": [x["artifact_hash"] for x in observations], "objectives": content_hash(objectives), "method": content_hash(method)}), "output_hash": None, "attestation_ref": None, "retention_class": "candidate-test", "schema_validation": "passed"},
        "extensions": {"enterprise": {"enterprise_scope": {"enterprise_scope_id": objectives["scope_id"], "assessment_period": "2026-08-01"}, "participating_capabilities": capabilities, "capability_input_manifest": [{"artifact_id": x["artifact_id"], "content_hash": x["artifact_hash"], "state": x["evidence_tier"]} for x in observations], "cross_capability_correlations": [], "enterprise_assertions": role["objective_scorecards"], "systemic_dependencies": [], "enterprise_unknowns": role["missing_data_effects"], "unresolved_disagreements": [], "confidence_reconciliation": {"method": method["confidence"], "result": None}, "human_decision_requests": [], "enterprise_traceability_manifest": role["manifest_binding"], "role": role}}
    }
    rehash(candidate)
    validate_candidate(candidate, gate, artifacts, observations, objectives, method, live)
    return candidate


def validate_candidate(candidate: dict[str, Any], gate: dict[str, Any], artifacts: list[dict[str, Any]], observations: list[dict[str, Any]], objectives: dict[str, Any], method: dict[str, Any], live: bool = False) -> None:
    validate_manifests(objectives, method)
    assert_schema(candidate, "universal-agent-artifact.schema.json", "ENT-STRAT candidate")
    extension = candidate["extensions"]["enterprise"]
    assert_schema(extension, "enterprise-extension.schema.json", "ENT-STRAT extension")
    role = extension["role"]
    assert_schema(role, "ent-strat-role.schema.json", "ENT-STRAT role")
    material = copy.deepcopy(candidate)
    output_hash = material["integrity"]["output_hash"]
    material["integrity"]["output_hash"] = None
    if content_hash(material) != output_hash:
        raise ValidationFailure("ENT-STRAT output hash mismatch")
    expected = role_template(gate, artifacts, observations, objectives, method, live)
    if role != expected:
        raise ValidationFailure("ENT-STRAT deterministic projection, tier, missingness, or authority mismatch")
    if live and role["fitness_claim"] != "objective_method_protocol_lineage_smoke_only":
        raise ValidationFailure("single-domain strategic result overclaims fitness")
    if any(node["designation"] == "ENT-STRAT" for node in load_json(BASELINE)["nodes"]):
        raise ValidationFailure("ENT-STRAT candidate cannot be baseline scheduled")


def persist_candidate(root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    return ArtifactLedger(root).persist_artifact(candidate)

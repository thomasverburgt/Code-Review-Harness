#!/usr/bin/env python3
"""ADR-0034 exact accepted-live CAP-REQ/CAP-RISK admission and review records."""

from __future__ import annotations

import copy
import uuid
from typing import Any

from artifact_ledger import content_hash
from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest
from capability_req_runtime import validate_candidate as validate_cap_req
from capability_synth_runtime import assemble_model_candidate, build_candidate
from requirements_acceptance_runtime import derive_eligibility, load_live_artifact, validate_owner_finalization
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


PACKET = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json"
RESPONSE = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0020/human-response/requirements-acceptance-response.json"
FINALIZATION = ROOT / "fixtures/cap-req-admission/evidence/2026-08-02/adr0033/project-owner-finalization-corrected/project-owner-finalization.json"
ELIGIBILITY = ROOT / "fixtures/cap-req-admission/evidence/2026-08-02/adr0033/project-owner-finalization-corrected/requirements-eligibility-record.json"
NAMESPACE = uuid.UUID("34000000-0000-4000-8000-000000000000")
GENERATED_AT = "2026-08-02T06:00:00Z"


def _hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value)
    material[field] = None
    value[field] = content_hash(material)
    return value


def load_accepted_live_inputs(*, eligibility_override: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    packet, response, finalization = load_json(PACKET), load_json(RESPONSE), load_json(FINALIZATION)
    eligibility = copy.deepcopy(eligibility_override) if eligibility_override is not None else load_json(ELIGIBILITY)
    validate_owner_finalization(packet, response, finalization)
    expected = derive_eligibility(packet, response, finalization)
    if eligibility != expected:
        raise ValidationFailure("CAP-REQ eligibility is not the exact derived owner-finalized record")
    if eligibility["state"] != "eligible_for_accepted_capability_input" or eligibility["rollback_state"] != "active":
        raise ValidationFailure("CAP-REQ eligibility is absent, inactive, or revoked")
    cap_req = load_live_artifact()
    validate_cap_req(cap_req)
    if (eligibility["artifact_id"], eligibility["artifact_hash"]) != (
            cap_req["artifact"]["artifact_id"], content_hash(cap_req)):
        raise ValidationFailure("CAP-REQ artifact does not match its eligibility record")
    cap_risk = load_json(ACCEPTED_CAP_RISK)
    return [cap_risk, cap_req], eligibility


def build_enterprise_compatibility(candidate: dict[str, Any]) -> dict[str, Any]:
    artifact_id, artifact_hash = candidate["artifact"]["artifact_id"], candidate["integrity"]["output_hash"]
    return {
        "record_id": str(uuid.uuid5(NAMESPACE, artifact_id + ":enterprise-compatibility")),
        "record_version": "1.0.0", "generated_at": GENERATED_AT,
        "candidate": {"id": artifact_id, "hash": artifact_hash},
        "results": [
            {"designation": "ENT-ARCH", "required_input": "CAPABILITY-ARTIFACTS", "state": "direct_comparison_compatible"},
            {"designation": "ENT-GOV", "required_input": "CAPABILITY-ARTIFACTS", "state": "direct_comparison_compatible"},
            {"designation": "ENT-STRAT", "required_input": "TIERED-POSTURE-INPUTS", "state": "compatible_via_tiered_posture_wrapper"},
            {"designation": "ENT-SYNTH", "required_input": "TIERED-ENTERPRISE-DOMAIN-ARTIFACTS", "state": "not_direct_enterprise_domain_agents_required"},
        ],
        "effect": "comparison_only", "enterprise_scheduled": False, "decision_authority": "human",
    }


def build_semantic_review_packet(candidate: dict[str, Any], manifest: dict[str, Any],
                                 eligibility: dict[str, Any]) -> dict[str, Any]:
    packet = {
        "packet_id": str(uuid.uuid5(NAMESPACE, candidate["artifact"]["artifact_id"] + ":semantic-review")),
        "packet_version": "1.0.0", "generated_at": GENERATED_AT,
        "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
        "coordinator_manifest": {"id": manifest["manifest_id"], "hash": manifest["integrity"]["manifest_hash"]},
        "cap_req_eligibility": {"id": eligibility["eligibility_id"], "hash": eligibility["record_hash"]},
        "input_artifacts": [{"designation": item["designation"], "artifact_id": item["artifact_id"],
                             "artifact_hash": item["output_hash"]} for item in manifest["received_inputs"]],
        "review_dimensions": ["child_assertion_preservation", "cross_domain_derivation",
                              "conflict_and_unknown_preservation", "evidence_sufficiency",
                              "confidence_reconciliation", "enterprise_handoff", "authority_boundary", "rollback"],
        "review_state": "awaiting_human_semantic_review", "required_authority": "project-owner",
        "effect": "review_request_only", "scheduling_authorized": False, "production_effect": "none",
        "packet_hash": "sha256:" + "0" * 64,
    }
    _hashed(packet, "packet_hash")
    assert_schema(packet, "capability-synthesis-semantic-review-packet.schema.json", "CAP-SYNTH semantic review packet")
    return packet


def build_accepted_live_package(model_role: dict[str, Any] | None = None,
                                *, eligibility_override: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    artifacts, eligibility = load_accepted_live_inputs(eligibility_override=eligibility_override)
    cap_req = next(item for item in artifacts if item["identity"]["designation"] == "CAP-REQ")
    authorization = [{"designation": "CAP-REQ", "artifact_id": cap_req["artifact"]["artifact_id"],
                      "artifact_hash": cap_req["integrity"]["output_hash"],
                      "eligibility_record_id": eligibility["eligibility_id"],
                      "eligibility_record_hash": eligibility["record_hash"],
                      "authority_basis": "project_owner_finalized_eligibility"}]
    manifest = build_manifest(artifacts, ["CAP-RISK", "CAP-REQ"], calibration_scope="declared_multi_domain",
                              accepted_input_authorizations=authorization)
    candidate = (build_candidate(manifest, artifacts, "accepted_live_multi_domain_candidate_evaluation")
                 if model_role is None else assemble_model_candidate(
                     model_role, manifest, artifacts, evidence_tier="accepted_live_multi_domain_candidate_evaluation"))
    compatibility = build_enterprise_compatibility(candidate)
    review = build_semantic_review_packet(candidate, manifest, eligibility)
    return artifacts, eligibility, manifest, candidate, compatibility, review

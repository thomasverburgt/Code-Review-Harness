#!/usr/bin/env python3
"""Record the corrected ADR-0037 project-owner semantic disposition."""
from __future__ import annotations
import copy, uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

RUN = ROOT / "fixtures/enterprise-strategy-admission/evidence/2026-08-02/adr0037/corrected-gx10-live-evaluation"
SUPERSESSION = ROOT / "fixtures/enterprise-strategy-admission/evidence/2026-08-02/adr0037/corrected-candidate-supersession.json"
REGISTRY = ROOT / "appendices/governance/decision-authorities-0.1.0.json"
NS = uuid.UUID("37000000-0000-4000-8000-000000000002")
DECIDED = "2026-08-02T15:00:00Z"
DERIVED = "2026-08-02T15:01:00Z"
BOUNDARIES = [
    "single_capability_evidence_scope",
    "finding_locator_coverage_missing_from_admitted_cap_synth",
    "no_composite_score_authorized",
    "comparison_only_no_strategy_investment_or_scheduling_authority",
    "deterministic_harness_projection_with_raw_response_retained",
]
SOURCE_CONTEXT = [
    "cap_synth_declared_requirements_absence_remains_unresolved_source_context",
    "cap_synth_redacted_credential_like_value_remains_unclassified_source_context",
    "cap_synth_later_promotion_review_request_remains_human_owned",
    "locator_coverage_requires_admitted_findings_with_resolvable_file_and_location_bindings",
]

def hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value); material[field] = None; value[field] = content_hash(material); return value

def owner() -> None:
    registry = load_json(REGISTRY)
    authority = next(x for x in registry["authorities"] if x["authority_role"] == "project-owner")
    if "finalize_governance_record" not in authority["allowed_actions"] or "HUMAN-PROJECT-OWNER-001" not in authority["human_subject_ids"] or "CODE-HARNESS-PROJECT-001" not in authority["scope_ids"]:
        raise ValidationFailure("project-owner authority or corrected project scope absent")

def load_exact_review():
    packet = load_json(RUN / "semantic-review-packet.json")
    candidate = load_json(RUN / "ent-strat-model-candidate.artifact.json")
    raw = load_json(RUN / "raw-response.json")
    supersession = load_json(SUPERSESSION)
    assert_schema(packet, "enterprise-strategy-semantic-review-packet.schema.json", "corrected ADR-0037 packet")
    material = copy.deepcopy(candidate); candidate_hash = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != candidate_hash or raw != candidate["extensions"]["enterprise"]["role"]:
        raise ValidationFailure("corrected ADR-0037 candidate or raw projection mismatch")
    if content_hash({**packet, "packet_hash": None}) != packet["packet_hash"] or (packet["candidate"]["id"], packet["candidate"]["hash"]) != (candidate["artifact"]["artifact_id"], candidate_hash):
        raise ValidationFailure("corrected ADR-0037 packet binding mismatch")
    if (supersession["successor_artifact_id"], supersession["successor_object_hash"]) != (candidate["artifact"]["artifact_id"], candidate_hash):
        raise ValidationFailure("corrected candidate supersession mismatch")
    return packet, candidate, supersession

def build_disposition():
    packet, candidate, supersession = load_exact_review(); owner()
    value = {
        "disposition_id": str(uuid.uuid5(NS, packet["packet_id"] + ":accept-corrected")), "packet_id": packet["packet_id"], "packet_hash": packet["packet_hash"],
        "candidate_id": candidate["artifact"]["artifact_id"], "candidate_hash": candidate["integrity"]["output_hash"], "supersession_id": supersession["supersession_id"], "decided_at": DECIDED,
        "decided_by": {"authority_role": "project-owner", "authority_name": "thomasverburgt", "subject_id": "HUMAN-PROJECT-OWNER-001"}, "disposition": "accept_corrected_candidate_as_semantically_faithful",
        "reviewed_dimensions": packet["review_dimensions"], "semantic_judgment": {"statement": "Accept corrected ENT-STRAT as semantically faithful and continue.", "strategy_posture": "insufficient_evidence", "effect": "semantic_acceptance_of_corrected_candidate"},
        "remaining_boundaries": BOUNDARIES, "source_context_recommendations": SOURCE_CONTEXT, "decision_authority": "project_owner", "effect": "semantic_acceptance_record_only", "scheduling_authorized": False, "report_effect": "none", "deployment_effect": "none", "disposition_hash": "sha256:" + "0" * 64,
    }
    hashed(value, "disposition_hash"); assert_schema(value, "enterprise-strategy-corrected-semantic-disposition.schema.json", "corrected ADR-0037 disposition"); return value

def validate_disposition(value):
    packet, candidate, supersession = load_exact_review(); assert_schema(value, "enterprise-strategy-corrected-semantic-disposition.schema.json", "corrected ADR-0037 disposition")
    if (value["packet_id"], value["packet_hash"], value["candidate_id"], value["candidate_hash"], value["supersession_id"]) != (packet["packet_id"], packet["packet_hash"], candidate["artifact"]["artifact_id"], candidate["integrity"]["output_hash"], supersession["supersession_id"]) or content_hash({**value, "disposition_hash": None}) != value["disposition_hash"]:
        raise ValidationFailure("corrected ADR-0037 disposition mismatch")

def build_finalization(disposition):
    validate_disposition(disposition)
    value = {"finalization_id": str(uuid.uuid5(NS, disposition["disposition_id"] + ":finalization")), "target_record_type": "enterprise_strategy_semantic_disposition", "target_record_id": disposition["disposition_id"], "target_record_hash": disposition["disposition_hash"], "finalized_on": "2026-08-02", "finalized_by": {"authority_role": "project-owner", "authority_name": "thomasverburgt", "subject_id": "HUMAN-PROJECT-OWNER-001"}, "checks": {"source_binding": True, "authority_binding": True, "record_integrity": True, "scope_binding": True}, "finalization_state": "finalized", "decision_authority": "project_owner", "effect": "record_only", "finalization_hash": "sha256:" + "0" * 64}
    hashed(value, "finalization_hash"); assert_schema(value, "project-owner-finalization.schema.json", "corrected ADR-0037 finalization"); return value

def derive_eligibility(disposition, finalization, revoked=False):
    validate_disposition(disposition); assert_schema(finalization, "project-owner-finalization.schema.json", "corrected ADR-0037 finalization")
    active = not revoked and finalization["target_record_hash"] == disposition["disposition_hash"] and finalization["finalization_state"] == "finalized"
    value = {"eligibility_id": str(uuid.uuid5(NS, disposition["disposition_id"] + (":revoked" if revoked else ":active"))), "candidate_id": disposition["candidate_id"], "candidate_hash": disposition["candidate_hash"], "packet_id": disposition["packet_id"], "packet_hash": disposition["packet_hash"], "disposition_id": disposition["disposition_id"], "disposition_hash": disposition["disposition_hash"], "finalization_id": finalization["finalization_id"], "finalization_hash": finalization["finalization_hash"], "supersession_id": disposition["supersession_id"], "derived_at": DERIVED, "state": "eligible_for_enterprise_synthesis_candidate_evaluation" if active else "not_eligible", "rollback_state": "active" if active else "revoked", "reason": "project_owner_accepted_corrected_candidate_as_semantically_faithful" if active else "eligibility_revoked", "limitations_carried_forward": BOUNDARIES, "source_context_carried_forward": SOURCE_CONTEXT, "decision_authority": "derived_from_project_owner_finalization", "effect": "enterprise_synthesis_evaluation_eligibility_only", "ent_strat_scheduled": False, "ent_synth_scheduled": False, "report_effect": "none", "deployment_effect": "none", "record_hash": "sha256:" + "0" * 64}
    hashed(value, "record_hash"); assert_schema(value, "enterprise-strategy-corrected-semantic-eligibility.schema.json", "corrected ADR-0037 eligibility"); return value

def build_records():
    disposition = build_disposition(); finalization = build_finalization(disposition); return disposition, finalization, derive_eligibility(disposition, finalization)

def persist_records(root: Path, disposition, finalization, eligibility):
    ledger = ArtifactLedger(root)
    return [ledger.persist_record(f"enterprise-strategy-dispositions/{disposition['disposition_id']}.json", "enterprise-strategy-disposition", disposition["disposition_id"], disposition), ledger.persist_record(f"project-owner-finalizations/{finalization['finalization_id']}.json", "project-owner-finalization", finalization["finalization_id"], finalization), ledger.persist_record(f"enterprise-strategy-eligibility/{eligibility['eligibility_id']}.json", "enterprise-strategy-eligibility", eligibility["eligibility_id"], eligibility)]

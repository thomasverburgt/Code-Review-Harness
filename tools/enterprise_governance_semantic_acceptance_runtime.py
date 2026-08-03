#!/usr/bin/env python3
"""Record and derive the ADR-0036 project-owner ENT-GOV semantic disposition."""

from __future__ import annotations

import copy
import uuid
from pathlib import Path
from typing import Any

from accepted_live_enterprise_governance_runtime import validate_candidate
from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json


RUN = ROOT / "fixtures/enterprise-governance-admission/evidence/2026-08-02/adr0036/gx10-live-evaluation/revised-flow-run"
PACKET = RUN / "semantic-review-packet.json"
CANDIDATE = RUN / "ent-gov-model-candidate.artifact.json"
GATE = RUN / "ent-evidence-gate.artifact.json"
SOURCE = RUN / "cap-synth-input.artifact.json"
ELIGIBILITY = RUN / "cap-synth-eligibility.json"
GOVERNANCE = RUN / "owner-governance-source-manifest.json"
EVIDENCE = RUN / "governance-evidence-binding-manifest.json"
INPUT_MANIFEST = RUN / "enterprise-governance-input-manifest.json"
AUTHORITY_REGISTRY = ROOT / "appendices/governance/decision-authorities-0.1.0.json"
NAMESPACE = uuid.UUID("36000000-0000-4000-8000-000000000001")
DECIDED_AT = "2026-08-02T11:00:00Z"
DERIVED_AT = "2026-08-02T11:01:00Z"


def _hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value)
    material[field] = None
    value[field] = content_hash(material)
    return value


def _owner_can_finalize() -> None:
    registry = load_json(AUTHORITY_REGISTRY)
    assert_schema(registry, "decision-authority-registry.schema.json", "decision authority registry")
    owner = next((item for item in registry["authorities"] if item["authority_role"] == "project-owner"), None)
    if not owner or "finalize_governance_record" not in owner["allowed_actions"] or "HUMAN-PROJECT-OWNER-001" not in owner["human_subject_ids"]:
        raise ValidationFailure("project owner lacks governance-record finalization authority")


def load_exact_review() -> tuple[dict[str, Any], dict[str, Any]]:
    packet, candidate = load_json(PACKET), load_json(CANDIDATE)
    gate, source, eligibility = load_json(GATE), load_json(SOURCE), load_json(ELIGIBILITY)
    governance, evidence, input_manifest = load_json(GOVERNANCE), load_json(EVIDENCE), load_json(INPUT_MANIFEST)
    assert_schema(packet, "enterprise-governance-semantic-review-packet.schema.json", "ENT-GOV semantic packet")
    if content_hash({**packet, "packet_hash": None}) != packet["packet_hash"]:
        raise ValidationFailure("ENT-GOV semantic packet hash mismatch")
    validate_candidate(candidate, gate, source, eligibility, governance, evidence, input_manifest)
    if (packet["candidate"]["id"], packet["candidate"]["hash"]) != (
            candidate["artifact"]["artifact_id"], candidate["integrity"]["output_hash"]):
        raise ValidationFailure("ENT-GOV semantic packet candidate binding mismatch")
    return packet, candidate


def build_disposition() -> dict[str, Any]:
    packet, candidate = load_exact_review()
    _owner_can_finalize()
    value = {
        "disposition_id": str(uuid.uuid5(NAMESPACE, packet["packet_id"] + ":semantically-faithful")),
        "packet_id": packet["packet_id"], "packet_hash": packet["packet_hash"],
        "candidate_id": candidate["artifact"]["artifact_id"], "candidate_hash": candidate["integrity"]["output_hash"],
        "decided_at": DECIDED_AT,
        "decided_by": {"authority_role": "project-owner", "authority_name": "thomasverburgt", "subject_id": "HUMAN-PROJECT-OWNER-001"},
        "disposition": "accept_semantically_faithful", "reviewed_dimensions": packet["review_dimensions"],
        "semantic_judgment": {"statement": "Revised packet checks out.", "governance_posture": "insufficient_evidence", "confidence_interpretation": "confidence_in_bounded_evidence_insufficiency_not_compliance"},
        "acknowledged_boundaries": {"single_capability_only": True, "no_enterprise_governance_maturity_claim": True, "no_compliance_determination": True, "no_exception_or_approval_authority": True, "no_policy_change": True, "comparison_only": True},
        "decision_authority": "project_owner", "effect": "semantic_acceptance_record_only", "scheduling_authorized": False,
        "report_effect": "none", "deployment_effect": "none", "disposition_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "disposition_hash")
    assert_schema(value, "enterprise-governance-semantic-disposition.schema.json", "ENT-GOV semantic disposition")
    return value


def validate_disposition(disposition: dict[str, Any]) -> None:
    packet, candidate = load_exact_review()
    assert_schema(disposition, "enterprise-governance-semantic-disposition.schema.json", "ENT-GOV semantic disposition")
    expected = (packet["packet_id"], packet["packet_hash"], candidate["artifact"]["artifact_id"], candidate["integrity"]["output_hash"])
    actual = (disposition["packet_id"], disposition["packet_hash"], disposition["candidate_id"], disposition["candidate_hash"])
    if actual != expected or content_hash({**disposition, "disposition_hash": None}) != disposition["disposition_hash"]:
        raise ValidationFailure("ENT-GOV semantic disposition binding or hash mismatch")
    _owner_can_finalize()


def build_finalization(disposition: dict[str, Any]) -> dict[str, Any]:
    validate_disposition(disposition)
    value = {
        "finalization_id": str(uuid.uuid5(NAMESPACE, disposition["disposition_id"] + ":finalization")),
        "target_record_type": "enterprise_governance_semantic_disposition", "target_record_id": disposition["disposition_id"],
        "target_record_hash": disposition["disposition_hash"], "finalized_on": "2026-08-02",
        "finalized_by": {"authority_role": "project-owner", "authority_name": "thomasverburgt", "subject_id": "HUMAN-PROJECT-OWNER-001"},
        "checks": {"source_binding": True, "authority_binding": True, "record_integrity": True, "scope_binding": True},
        "finalization_state": "finalized", "decision_authority": "project_owner", "effect": "record_only",
        "finalization_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "finalization_hash")
    assert_schema(value, "project-owner-finalization.schema.json", "ENT-GOV semantic finalization")
    return value


def validate_finalization(disposition: dict[str, Any], finalization: dict[str, Any]) -> None:
    validate_disposition(disposition)
    assert_schema(finalization, "project-owner-finalization.schema.json", "ENT-GOV semantic finalization")
    if (finalization["target_record_type"], finalization["target_record_id"], finalization["target_record_hash"]) != ("enterprise_governance_semantic_disposition", disposition["disposition_id"], disposition["disposition_hash"]):
        raise ValidationFailure("ENT-GOV semantic finalization binding mismatch")
    if content_hash({**finalization, "finalization_hash": None}) != finalization["finalization_hash"] or finalization["finalization_state"] != "finalized" or not all(finalization["checks"].values()):
        raise ValidationFailure("ENT-GOV semantic finalization did not pass")


def derive_eligibility(disposition: dict[str, Any], finalization: dict[str, Any], *, revoked: bool = False) -> dict[str, Any]:
    validate_finalization(disposition, finalization)
    eligible = disposition["disposition"] == "accept_semantically_faithful" and not revoked
    value = {
        "eligibility_id": str(uuid.uuid5(NAMESPACE, disposition["disposition_id"] + (":revoked" if revoked else ":active"))),
        "candidate_id": disposition["candidate_id"], "candidate_hash": disposition["candidate_hash"],
        "packet_id": disposition["packet_id"], "packet_hash": disposition["packet_hash"],
        "disposition_id": disposition["disposition_id"], "disposition_hash": disposition["disposition_hash"],
        "finalization_id": finalization["finalization_id"], "finalization_hash": finalization["finalization_hash"],
        "derived_at": DERIVED_AT, "state": "eligible_for_enterprise_synthesis_candidate_evaluation" if eligible else "not_eligible",
        "rollback_state": "revoked" if revoked else "active", "reason": "project_owner_accepted_semantically_faithful" if eligible else "eligibility_revoked",
        "decision_authority": "derived_from_project_owner_finalization", "effect": "enterprise_synthesis_evaluation_eligibility_only",
        "ent_gov_scheduled": False, "ent_synth_scheduled": False, "report_effect": "none", "deployment_effect": "none", "record_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "record_hash")
    assert_schema(value, "enterprise-governance-semantic-eligibility.schema.json", "ENT-GOV semantic eligibility")
    return value


def build_records() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    disposition = build_disposition()
    finalization = build_finalization(disposition)
    return disposition, finalization, derive_eligibility(disposition, finalization)


def persist_records(root: Path, disposition: dict[str, Any], finalization: dict[str, Any], eligibility: dict[str, Any]) -> list[dict[str, Any]]:
    ledger = ArtifactLedger(root)
    return [
        ledger.persist_record(f"enterprise-governance-dispositions/{disposition['disposition_id']}.json", "enterprise-governance-disposition", disposition["disposition_id"], disposition),
        ledger.persist_record(f"project-owner-finalizations/{finalization['finalization_id']}.json", "project-owner-finalization", finalization["finalization_id"], finalization),
        ledger.persist_record(f"enterprise-governance-eligibility/{eligibility['eligibility_id']}.json", "enterprise-governance-eligibility", eligibility["eligibility_id"], eligibility),
    ]

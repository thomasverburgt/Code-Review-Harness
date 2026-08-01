#!/usr/bin/env python3
"""ADR-0020 immutable CAP-REQ human-acceptance boundary."""
from __future__ import annotations
import copy, io, json, tarfile, uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger, content_hash
from capability_req_runtime import inputs, validate_candidate
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

LIVE_ARCHIVE = ROOT / "fixtures/cap-req-admission/evidence/2026-08-01/adr0019/gx10-live-calibration.tar.gz"
LIVE_ARTIFACT_MEMBER = "adr19-cap-req-live/cap-req-candidate.artifact.json"
AUTHORITY_REGISTRY = ROOT / "appendices/governance/decision-authorities-0.1.0.json"
STATE_MACHINE = ROOT / "orchestration/state-machines/requirements-acceptance.state-machine.json"
GENERATED_AT = "2026-08-01T23:00:00Z"
DERIVED_AT = "2026-08-01T23:30:00Z"
NAMESPACE = uuid.UUID("20000000-0000-4000-8000-000000000000")
DISPOSITIONS = ["accept_review_as_complete", "supply_authoritative_requirements", "require_scope_correction", "reject_artifact", "insufficient_evidence"]

def _hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(value); result[field] = None; value[field] = content_hash(result); return value

def load_live_artifact() -> dict[str, Any]:
    with tarfile.open(LIVE_ARCHIVE, "r:gz") as archive:
        stream = archive.extractfile(LIVE_ARTIFACT_MEMBER)
        if stream is None: raise ValidationFailure("retained live CAP-REQ artifact is missing")
        artifact = json.load(io.TextIOWrapper(stream, encoding="utf-8"))
    validate_candidate(artifact)
    return artifact

def _authority(role: str, kind: str, action: str, scope: str) -> None:
    registry = load_json(AUTHORITY_REGISTRY)
    assert_schema(registry, "decision-authority-registry.schema.json", "authority registry")
    found = next((x for x in registry["authorities"] if x["authority_role"] == role), None)
    if not found or found["authority_kind"] != kind or action not in found["allowed_actions"] or scope not in found["scope_ids"]:
        raise ValidationFailure(f"unauthorized requirements acceptance role: {role}")

def build_packet() -> dict[str, Any]:
    artifact = load_live_artifact(); source, locator, _ = inputs(); role = artifact["extensions"]["capability"]["role"]
    if source["declared_requirement_population"] or role["requirement_records"] or role["coverage"]["fraction"] is not None:
        raise ValidationFailure("requirements acceptance packet requires honest zero-population semantics")
    execution = artifact["execution"]
    packet = {"packet_id":str(uuid.uuid5(NAMESPACE, artifact["artifact"]["artifact_id"])),"packet_version":"1.0.0","generated_at":GENERATED_AT,
      "cap_req_artifact":{"artifact_id":artifact["artifact"]["artifact_id"],"output_hash":artifact["integrity"]["output_hash"],"content_hash":content_hash(artifact),"lifecycle_state":artifact["artifact"]["lifecycle_state"],"acceptance_state":role["acceptance_state"]},
      "source_manifest":{"content_hash":content_hash(source),"scope_id":source["scope_id"],"immutable_revision":source["immutable_revision"],"declared_requirement_count":0,"interpretation_boundary":source["interpretation_boundary"]},
      "evidence_locator":{"locator_id":locator["locator_id"],"locator_hash":locator["locator_hash"],"repository_uri":locator["repository_uri"],"immutable_revision":locator["immutable_revision"],"path":locator["path"],"line_start":locator["line_start"],"line_end":locator["line_end"],"line_fingerprint":locator["line_fingerprint"]},
      "execution_pins":{"model":execution["model"],"prompt_version":execution["prompt_version"],"rubric_version":execution["rubric_version"],"projection_version":"capability-requirements-analytical-projection-1.0.0","toolchain_version":execution["toolchain_version"]},
      "review_facts":{"requirement_records":0,"satisfaction_claim_present":False,"satisfaction_rate":None,"traceability_gap_ids":["GAP-REQ-001"],"human_decision_request_ids":["DC-REQ-001"],"interpretation":"zero_declared_requirements_is_unassessable_not_satisfied"},
      "available_dispositions":DISPOSITIONS,"required_authority":"requirements-acceptance-authority","decision_authority":"human","effect":"review_request_only","eligibility_state":"blocked_pending_human_requirements_acceptance",
      "isolation":{"baseline_workflow_changed":False,"report_package_changed":False,"cap_synth_scheduled":False,"deployment_effect":"none"},"packet_hash":"sha256:"+"0"*64}
    _hashed(packet, "packet_hash"); assert_schema(packet,"requirements-acceptance-packet.schema.json","requirements acceptance packet"); return packet

def validate_response(packet: dict[str, Any], response: dict[str, Any]) -> None:
    assert_schema(response,"requirements-acceptance-response.schema.json","requirements acceptance response")
    if response["packet_id"] != packet["packet_id"] or response["packet_hash"] != packet["packet_hash"]: raise ValidationFailure("response packet binding mismatch")
    artifact = packet["cap_req_artifact"]
    if response["artifact_id"] != artifact["artifact_id"] or response["artifact_hash"] != artifact["content_hash"]: raise ValidationFailure("response artifact binding mismatch")
    if content_hash({**response,"response_hash":None}) != response["response_hash"]: raise ValidationFailure("response hash mismatch")
    _authority(response["decided_by"]["authority_role"],"expert_decision_authority","accept_capability_requirements_review",packet["source_manifest"]["scope_id"])

def build_verification(packet: dict[str, Any], response: dict[str, Any], verifier_name: str="Independent Governance Verifier") -> dict[str, Any]:
    validate_response(packet,response); _authority("governance-records-verifier","records_verifier","verify_external_decision","ENTERPRISE-FIXTURE-001")
    if verifier_name == response["decided_by"]["authority_name"]: raise ValidationFailure("requirements decision-maker cannot verify the same record")
    value={"verification_id":str(uuid.uuid5(NAMESPACE,response["response_id"]+":verification")),"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"response_id":response["response_id"],"response_hash":response["response_hash"],"verified_at":DERIVED_AT,"verified_by":{"authority_role":"governance-records-verifier","authority_name":verifier_name},"checks":{"packet_binding":True,"artifact_binding":True,"authority":True,"record_integrity":True},"status":"verified","decision_authority":"human","effect":"record_only","verification_hash":"sha256:"+"0"*64}
    _hashed(value,"verification_hash"); assert_schema(value,"requirements-acceptance-verification.schema.json","requirements acceptance verification"); return value

def validate_verification(packet: dict[str, Any], response: dict[str, Any], verification: dict[str, Any]) -> None:
    validate_response(packet,response); assert_schema(verification,"requirements-acceptance-verification.schema.json","requirements acceptance verification")
    expected=(packet["packet_id"],packet["packet_hash"],response["response_id"],response["response_hash"])
    actual=(verification["packet_id"],verification["packet_hash"],verification["response_id"],verification["response_hash"])
    if actual != expected or content_hash({**verification,"verification_hash":None}) != verification["verification_hash"]: raise ValidationFailure("verification binding or hash mismatch")
    if verification["status"] != "verified" or not all(verification["checks"].values()): raise ValidationFailure("requirements acceptance verification did not pass")
    if verification["verified_by"]["authority_name"] == response["decided_by"]["authority_name"]: raise ValidationFailure("requirements acceptance verification is not independent")

def derive_eligibility(packet: dict[str, Any], response: dict[str, Any], verification: dict[str, Any], revoked: bool=False) -> dict[str, Any]:
    validate_verification(packet,response,verification)
    eligible=response["disposition"]=="accept_review_as_complete" and not revoked
    reason="verified_human_acceptance" if eligible else "eligibility_revoked" if revoked else "human_disposition_does_not_accept_review"
    value={"eligibility_id":str(uuid.uuid5(NAMESPACE,response["response_id"]+(':revoked' if revoked else ':active'))),"artifact_id":packet["cap_req_artifact"]["artifact_id"],"artifact_hash":packet["cap_req_artifact"]["content_hash"],"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"response_id":response["response_id"],"response_hash":response["response_hash"],"verification_id":verification["verification_id"],"verification_hash":verification["verification_hash"],"derived_at":DERIVED_AT,"basis_disposition":response["disposition"],"state":"eligible_for_accepted_capability_input" if eligible else "not_eligible","rollback_state":"revoked" if revoked else "active","reason":reason,"decision_authority":"derived_from_verified_human_record","effect":"eligibility_record_only","cap_synth_scheduled":False,"record_hash":"sha256:"+"0"*64}
    _hashed(value,"record_hash"); assert_schema(value,"requirements-eligibility-record.schema.json","requirements eligibility record"); return value

def render_review(packet: dict[str, Any]) -> str:
    a=packet["cap_req_artifact"]; s=packet["source_manifest"]; loc=packet["evidence_locator"]
    return f"""# CAP-REQ Human Acceptance Review Packet

Packet: `{packet['packet_id']}`  
Packet hash: `{packet['packet_hash']}`

**ACCEPTED CAPABILITY INPUT USE IS BLOCKED — HUMAN REQUIREMENTS ACCEPTANCE REQUIRED**

## Exact artifact and source

- Live CAP-REQ artifact: `{a['artifact_id']}`
- Artifact content hash: `{a['content_hash']}`
- Source-manifest hash: `{s['content_hash']}`
- Declared authoritative requirements: **0**
- Source location: `{loc['repository_uri']}@{loc['immutable_revision']}` → `{loc['path']}:{loc['line_start']}`
- Locator hash: `{loc['locator_hash']}`

## Required interpretation

Zero declared requirements means satisfaction is **unassessable**, not satisfied. The artifact contains zero requirement records and no satisfaction rate. `GAP-REQ-001` and `DC-REQ-001` remain open.

## Human disposition

Required authority: `requirements-acceptance-authority`

Allowed dispositions: {', '.join(f'`{x}`' for x in DISPOSITIONS)}.

Acceptance means only that this bounded review may become an accepted CAP-REQ input after independent verification. It does not establish requirement satisfaction, capability readiness, risk acceptance, scheduling, report distribution, deployment, or A100 production approval. CAP-SYNTH remains unscheduled.

## Rollback

Derived eligibility can be revoked without altering this packet or the immutable response and verification history. Missing, invalid, rejected, or revoked records fail closed.
"""

def persist_packet(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    return ArtifactLedger(root).persist_record(f"requirements-acceptance/{packet['packet_id']}.json","requirements-acceptance-request",packet["packet_id"],packet,retention_class="architecture-evidence")

#!/usr/bin/env python3
"""Immutable, record-only semantic adjudication support for ADR-0016."""
from __future__ import annotations
import copy, io, json, tarfile, uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

BASELINE = ROOT / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-cap-risk.artifact.json"
LIVE_ARCHIVE = ROOT / "fixtures/product-synth-admission/evidence/2026-07-31/shadow-comparison-adr0015/gx10-live-shadow-success.tar.gz"
LIVE_ARTIFACT_MEMBER = "adr15-shadow-live-output-20260731c/accepted-shadow-cap-risk.artifact.json"
LIVE_COMPARISON_MEMBER = "adr15-shadow-live-output-20260731c/live-shadow-comparison.json"
GENERATED_AT = "2026-08-01T15:00:00Z"
NAMESPACE = uuid.UUID("16000000-0000-4000-8000-000000000000")
DISPOSITIONS = ["accept_preserved_meaning", "accept_beneficial_enrichment", "require_normalization", "reject_semantic_drift", "insufficient_evidence"]

DELTA_SPECS = [
    ("assessments", "/assessments/0/rationale", "potentially_substantive", "Does the changed likelihood wording preserve the accepted assessment meaning?", "Changes the rationale presented to capability-risk reviewers."),
    ("conflicts", "/conflicts", "substantive", "Should the shadow-added DC-001 question be retained as an explicit capability conflict?", "Changes whether downstream reports and reviewers see an unresolved conflict."),
    ("risk_register", "/extensions/capability/role/risk_register/0/risk_category", "substantive", "Is security_exposure an acceptable replacement for secrets_exposure?", "Changes risk taxonomy, aggregation, filtering, and trend analysis."),
    ("risk_register", "/extensions/capability/role/risk_register/0/dependency_chain", "potentially_substantive", "Is adding PRODUCT-ALPHA to the dependency chain supported and useful?", "Changes dependency and blast-radius reasoning."),
    ("risk_register", "/extensions/capability/role/risk_register/0/likelihood_basis", "potentially_substantive", "Does the likelihood-basis wording preserve uncertainty?", "May change perceived evidentiary strength."),
    ("risk_register", "/extensions/capability/role/risk_register/0/mission_effect", "substantive", "Does the generalized sensitive-information mission effect preserve the accepted unauthorized-access meaning?", "Changes mission consequence communicated to leadership."),
    ("risk_register", "/extensions/capability/role/risk_register/0/treatment_options/0", "substantive", "Are the shadow treatment wording, sequencing, evidence, and verification changes acceptable?", "Changes the action package human experts may consider."),
]

def load_archive_json(member: str) -> dict[str, Any]:
    with tarfile.open(LIVE_ARCHIVE, "r:gz") as archive:
        stream = archive.extractfile(member)
        if stream is None: raise ValidationFailure(f"missing retained archive member: {member}")
        return json.load(io.TextIOWrapper(stream, encoding="utf-8"))

def resolve_pointer(value: Any, pointer: str) -> Any:
    current = value
    for token in pointer.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return copy.deepcopy(current)

def build_packet() -> dict[str, Any]:
    baseline, shadow = load_json(BASELINE), load_archive_json(LIVE_ARTIFACT_MEMBER)
    comparison = load_archive_json(LIVE_COMPARISON_MEMBER)
    if comparison["overall_state"] != "blocked" or comparison["authority_effect"] != "comparison_only":
        raise ValidationFailure("semantic adjudication requires a blocked comparison-only source")
    if content_hash(baseline) != comparison["baseline_cap_risk"]["content_hash"] or content_hash(shadow) != comparison["shadow_cap_risk"]["content_hash"]:
        raise ValidationFailure("adjudication source artifact hash mismatch")
    dimensions = comparison["semantics"]["dimensions"]
    differing = sorted(name for name, state in dimensions.items() if state == "different")
    preserved = sorted(name for name, state in dimensions.items() if state == "equivalent")
    deltas = []
    for dimension, pointer, materiality, question, consequence in DELTA_SPECS:
        left, right = resolve_pointer(baseline, pointer), resolve_pointer(shadow, pointer)
        if left == right: raise ValidationFailure(f"declared semantic delta is not different: {pointer}")
        deltas.append({"delta_id": str(uuid.uuid5(NAMESPACE, pointer)), "dimension": dimension, "json_pointer": pointer,
                       "baseline_value": left, "shadow_value": right, "materiality": materiality,
                       "review_question": question, "downstream_consequence": consequence,
                       "available_dispositions": DISPOSITIONS, "default_if_unresolved": "block_cutover"})
    if set(differing) != {item["dimension"] for item in deltas}:
        raise ValidationFailure("adjudication packet does not cover every differing comparison dimension")
    packet = {"packet_id": str(uuid.uuid5(NAMESPACE, comparison["comparison_id"])), "packet_version": "1.0.0",
        "generated_at": GENERATED_AT,
        "source_comparison": {"record_id": comparison["comparison_id"], "content_hash": content_hash(comparison)},
        "baseline_artifact": {"record_id": baseline["artifact"]["artifact_id"], "content_hash": content_hash(baseline)},
        "shadow_artifact": {"record_id": shadow["artifact"]["artifact_id"], "content_hash": content_hash(shadow)},
        "preserved_dimensions": preserved, "differing_dimensions": differing, "deltas": deltas,
        "required_decision_authority": "enterprise-risk-acceptance-authority", "decision_authority": "human",
        "effect": "review_request_only", "cutover_state": "blocked_pending_human_adjudication",
        "isolation": {"baseline_workflow_changed": False, "report_package_changed": False, "deployment_effect": "none"},
        "packet_hash": "sha256:" + "0" * 64}
    material = copy.deepcopy(packet); material["packet_hash"] = None
    packet["packet_hash"] = content_hash(material)
    assert_schema(packet, "semantic-adjudication-packet.schema.json", "semantic adjudication packet")
    return packet

def validate_response(packet: dict[str, Any], response: dict[str, Any]) -> None:
    assert_schema(response, "semantic-adjudication-response.schema.json", "semantic adjudication response")
    if response["packet_id"] != packet["packet_id"] or response["packet_hash"] != packet["packet_hash"]:
        raise ValidationFailure("adjudication response is not bound to the exact packet")
    expected, actual = {item["delta_id"] for item in packet["deltas"]}, [item["delta_id"] for item in response["delta_decisions"]]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValidationFailure("adjudication response must decide every delta exactly once")
    dispositions = {item["disposition"] for item in response["delta_decisions"]}
    expected_recommendation = ("reject_cutover" if "reject_semantic_drift" in dispositions else
        "insufficient_evidence" if "insufficient_evidence" in dispositions else
        "normalization_required" if "require_normalization" in dispositions else "eligible_for_cutover_review")
    if response["overall_recommendation"] != expected_recommendation:
        raise ValidationFailure("overall recommendation is inconsistent with delta dispositions")

def render_review(packet: dict[str, Any]) -> str:
    lines = ["# PROD-SYNTH Shadow Semantic Adjudication Packet", "",
        f"Packet: `{packet['packet_id']}`", f"Packet hash: `{packet['packet_hash']}`", "",
        "**CUTOVER BLOCKED — HUMAN ADJUDICATION REQUIRED**", "",
        "Preserved dimensions: " + ", ".join(packet["preserved_dimensions"]),
        "Differing dimensions: " + ", ".join(packet["differing_dimensions"]), ""]
    for index, delta in enumerate(packet["deltas"], 1):
        lines.extend([f"## {index}. {delta['dimension']} — `{delta['json_pointer']}`", "",
            delta["review_question"], "", f"Materiality: `{delta['materiality']}`", "",
            "Baseline:", "```json", json.dumps(delta["baseline_value"], indent=2, sort_keys=True), "```", "",
            "Shadow:", "```json", json.dumps(delta["shadow_value"], indent=2, sort_keys=True), "```", "",
            "Downstream consequence: " + delta["downstream_consequence"], "",
            "Allowed dispositions: " + ", ".join(f"`{item}`" for item in DISPOSITIONS), "",
            "If unresolved: `block_cutover`", ""])
    lines.extend(["## Authority and effect", "", "The enterprise risk acceptance authority decides semantic meaning outside the harness. Any recorded response remains record-only. A separate later ADR is required for workflow cutover.", ""])
    return "\n".join(lines)

def persist_packet(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    return ArtifactLedger(root).persist_record(f"semantic-adjudication/{packet['packet_id']}.json", "semantic-adjudication-request",
        packet["packet_id"], packet, retention_class="architecture-evidence")

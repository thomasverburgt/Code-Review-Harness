#!/usr/bin/env python3
"""ADR-0038 exact accepted-domain ENT-SYNTH candidate controls."""
from __future__ import annotations
import copy, uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

NS = uuid.UUID("38000000-0000-4000-8000-000000000001")
CREATED = "2026-08-02T16:00:00Z"
BASELINE = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"
REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
REPORT_MACHINE = ROOT / "orchestration/state-machines/report-governance.state-machine.json"
SOURCES = {
    "ENT-SYSRISK": (ROOT / "fixtures/vertical-risk-slice/evidence/canonical-ent-sysrisk-2026-07-31/accepted-ent-sysrisk.artifact.json", None),
    "ENT-ARCH": (ROOT / "fixtures/enterprise-arch-admission/evidence/2026-08-02/adr0035/gx10-live-evaluation/corrected-run/ent-arch-model-candidate.artifact.json", ROOT / "fixtures/enterprise-arch-admission/evidence/2026-08-02/adr0035/project-owner-semantic-disposition/enterprise-synthesis-evaluation-eligibility.json"),
    "ENT-GOV": (ROOT / "fixtures/enterprise-governance-admission/evidence/2026-08-02/adr0036/gx10-live-evaluation/revised-flow-run/ent-gov-model-candidate.artifact.json", ROOT / "fixtures/enterprise-governance-admission/evidence/2026-08-02/adr0036/project-owner-semantic-disposition/enterprise-synthesis-evaluation-eligibility.json"),
    "ENT-STRAT": (ROOT / "fixtures/enterprise-strategy-admission/evidence/2026-08-02/adr0037/corrected-gx10-live-evaluation/ent-strat-model-candidate.artifact.json", ROOT / "fixtures/enterprise-strategy-admission/evidence/2026-08-02/adr0037/corrected-project-owner-semantic-disposition/enterprise-synthesis-evaluation-eligibility.json"),
}
EXPECTED = list(SOURCES)

def sid(*parts: str) -> str: return str(uuid.uuid5(NS, "|".join(parts)))
def hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value); material[field] = None; value[field] = content_hash(material); return value
def artifact_hash(artifact: dict[str, Any]) -> str:
    material = copy.deepcopy(artifact); expected = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != expected: raise ValidationFailure(f"artifact integrity mismatch: {artifact['identity']['designation']}")
    return expected
def record_hash(record: dict[str, Any]) -> str:
    expected = record["record_hash"]; material = copy.deepcopy(record); material["record_hash"] = None
    if content_hash(material) != expected: raise ValidationFailure("eligibility record integrity mismatch")
    return expected

def load_sources():
    artifacts, eligibilities = [], {}
    for designation, (artifact_path, eligibility_path) in SOURCES.items():
        artifact = load_json(artifact_path); ah = artifact_hash(artifact)
        if artifact["identity"]["designation"] != designation: raise ValidationFailure("domain designation mismatch")
        artifacts.append(artifact)
        if eligibility_path:
            eligibility = load_json(eligibility_path); record_hash(eligibility)
            if eligibility["candidate_id"] != artifact["artifact"]["artifact_id"] or eligibility["candidate_hash"] != ah or eligibility["state"] != "eligible_for_enterprise_synthesis_candidate_evaluation" or eligibility["rollback_state"] != "active":
                raise ValidationFailure(f"inactive or mismatched {designation} eligibility")
            eligibilities[designation] = eligibility
    return artifacts, eligibilities

def build_gate(artifacts=None, eligibilities=None):
    if artifacts is None or eligibilities is None: artifacts, eligibilities = load_sources()
    admitted = []
    for artifact in artifacts:
        designation = artifact["identity"]["designation"]; eligibility = eligibilities.get(designation)
        if eligibility and (eligibility["state"] != "eligible_for_enterprise_synthesis_candidate_evaluation" or eligibility["rollback_state"] != "active"):
            raise ValidationFailure(f"revoked or inactive {designation} eligibility")
        admitted.append({"designation": designation, "artifact_id": artifact["artifact"]["artifact_id"], "artifact_hash": artifact_hash(artifact), "eligibility_id": eligibility["eligibility_id"] if eligibility else None, "eligibility_hash": eligibility["record_hash"] if eligibility else None})
    value = {"gate_id": sid("accepted-live", "gate"), "gate_version": "1.0.0", "created_at": CREATED, "scope_id": "CODE-HARNESS-PROJECT-001", "expected_designations": EXPECTED, "admitted_inputs": admitted, "excluded_lineage": ["CAP-SYNTH", "CAP-REQ", "CAP-RISK", "PROD-*", "SPEC-*"], "gate_state": "admitted_for_candidate_evaluation", "scheduling_authorized": False, "report_effect": "none", "deployment_effect": "none", "gate_hash": "sha256:" + "0" * 64}
    hashed(value, "gate_hash"); validate_gate(value, artifacts, eligibilities); return value

def validate_gate(gate, artifacts, eligibilities):
    assert_schema(gate, "enterprise-synthesis-evidence-gate.schema.json", "ADR-0038 gate")
    if content_hash({**gate, "gate_hash": None}) != gate["gate_hash"]: raise ValidationFailure("gate hash mismatch")
    if [x["designation"] for x in gate["admitted_inputs"]] != EXPECTED or len({x["artifact_id"] for x in gate["admitted_inputs"]}) != 4: raise ValidationFailure("missing, duplicate, or reordered domain")
    for admitted, artifact in zip(gate["admitted_inputs"], artifacts):
        designation = artifact["identity"]["designation"]; eligibility = eligibilities.get(designation)
        expected = (designation, artifact["artifact"]["artifact_id"], artifact_hash(artifact), eligibility["eligibility_id"] if eligibility else None, eligibility["record_hash"] if eligibility else None)
        actual = (admitted["designation"], admitted["artifact_id"], admitted["artifact_hash"], admitted["eligibility_id"], admitted["eligibility_hash"])
        if actual != expected: raise ValidationFailure("gate source or eligibility substitution")

def build_manifest(gate=None, artifacts=None, eligibilities=None):
    if artifacts is None or eligibilities is None: artifacts, eligibilities = load_sources()
    gate = gate or build_gate(artifacts, eligibilities); inputs = []
    for artifact in artifacts:
        designation = artifact["identity"]["designation"]; eligibility = eligibilities.get(designation)
        artifact_limitations = artifact.get("methodology", {}).get("limitations", [])
        eligibility_limitations = eligibility.get("limitations_carried_forward", []) if eligibility else []
        limitations = list(dict.fromkeys(artifact_limitations + eligibility_limitations))
        inputs.append({"artifact_id": artifact["artifact"]["artifact_id"], "content_hash": artifact_hash(artifact), "designation": designation, "schema_version": "1.0.0", "freshness": "fresh", "compatibility": "compatible", "evidence_tier": "accepted_live", "authority_owner": "human domain authority", "permitted_use": "authoritative_domain_reference", "eligibility_id": eligibility["eligibility_id"] if eligibility else None, "eligibility_hash": eligibility["record_hash"] if eligibility else None, "limitations_carried_forward": limitations, "source_context_carried_forward": eligibility.get("source_context_carried_forward", []) if eligibility else []})
    value = {"manifest_id": sid(gate["gate_hash"], "input-manifest"), "manifest_version": "1.0.0", "created_at": CREATED, "scope_id": "CODE-HARNESS-PROJECT-001", "gate_artifact_id": gate["gate_id"], "gate_artifact_hash": gate["gate_hash"], "inputs": inputs, "manifest_hash": "sha256:" + "0" * 64}
    hashed(value, "manifest_hash"); validate_manifest(value, gate, artifacts, eligibilities); return value

def validate_manifest(manifest, gate, artifacts, eligibilities):
    assert_schema(manifest, "enterprise-synthesis-input-manifest.schema.json", "ADR-0038 manifest"); validate_gate(gate, artifacts, eligibilities)
    if content_hash({**manifest, "manifest_hash": None}) != manifest["manifest_hash"] or (manifest["gate_artifact_id"], manifest["gate_artifact_hash"]) != (gate["gate_id"], gate["gate_hash"]): raise ValidationFailure("manifest integrity or gate binding mismatch")
    expected = [(x["artifact_id"], x["artifact_hash"], x["designation"], x["eligibility_id"], x["eligibility_hash"]) for x in gate["admitted_inputs"]]
    actual = [(x["artifact_id"], x["content_hash"], x["designation"], x.get("eligibility_id"), x.get("eligibility_hash")) for x in manifest["inputs"]]
    if actual != expected or any(x["evidence_tier"] != "accepted_live" or x["permitted_use"] != "authoritative_domain_reference" for x in manifest["inputs"]): raise ValidationFailure("manifest domain set, eligibility, or tier mismatch")

def source_record_ids(value: Any) -> list[str]:
    found: set[str] = set()
    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, item in node.items():
                if key.endswith("_id") and isinstance(item, str) and key not in {"artifact_id", "agent_uuid"}: found.add(item)
                walk(item)
        elif isinstance(node, list):
            for item in node: walk(item)
    walk(value); return sorted(found)

def build_role(gate, artifacts, manifest):
    snapshots, summaries, contributions, decisions, disagreements = [], [], [], [], []
    for artifact, admitted in zip(artifacts, manifest["inputs"]):
        designation = admitted["designation"]; role = artifact["extensions"]["enterprise"]["role"]; role_hash = content_hash(role)
        snapshots.append({"artifact_id": admitted["artifact_id"], "artifact_hash": admitted["content_hash"], "designation": designation, "source_role_hash": role_hash, "preservation_state": "preserved_by_exact_content_address", "preserved_record_ids": source_record_ids(role)})
        summaries.append({"designation": designation, "artifact_id": admitted["artifact_id"], "source_role_hash": role_hash, "summary_type": "direct_domain_preservation", "limitations": admitted.get("limitations_carried_forward", []), "source_context": admitted.get("source_context_carried_forward", []), "authority_changed": False})
        contributions.append({"synthesis_assertion_id": f"SYNTH-{designation}", "statement": "The exact domain output is admitted at its accepted-live tier without semantic rewrite.", "source_artifact_ids": [admitted["artifact_id"]], "source_role_hashes": [role_hash], "transformation": "direct_summary", "uncertainty": "Domain conclusions retain their original scope, missingness, confidence meaning, and human authority."})
        for request in role.get("decision_requests", []): decisions.append({"decision_request_id": f"{admitted['artifact_id']}:{request.get('decision_request_id', request.get('decision_context_id', request.get('request_id', request.get('record_id', 'UNQUALIFIED'))))}", "source_artifact_id": admitted["artifact_id"], "source_designation": designation, "preserved_request": request, "decision_authority": "human"})
        for item in role.get("unresolved_disagreements", role.get("disagreement_register", [])): disagreements.append({"source_artifact_id": admitted["artifact_id"], "source_designation": designation, "preserved_disagreement": item})
    return {"designation": "ENT-SYNTH", "evidence_tier": "accepted_live_bounded_enterprise_domain_synthesis_evaluation", "fitness_claim": "bounded_code_harness_domain_synthesis_evaluation", "manifest_binding": {"gate_artifact_id": gate["gate_id"], "gate_artifact_hash": gate["gate_hash"], "synthesis_manifest_id": manifest["manifest_id"], "synthesis_manifest_hash": manifest["manifest_hash"], "domain_artifact_ids": [x["artifact_id"] for x in manifest["inputs"]], "domain_artifact_hashes": [x["content_hash"] for x in manifest["inputs"]], "eligibility_ids": [x["eligibility_id"] for x in manifest["inputs"] if x.get("eligibility_id")], "eligibility_hashes": [x["eligibility_hash"] for x in manifest["inputs"] if x.get("eligibility_hash")], "binding_state": "exact"}, "input_evidence_tiers": [{"artifact_id": x["artifact_id"], "designation": x["designation"], "evidence_tier": x["evidence_tier"], "permitted_use": x["permitted_use"]} for x in manifest["inputs"]], "source_assertion_snapshots": snapshots, "enterprise_posture_summary": {"state": "bounded_domain_set_preserved_human_review_required", "advisory_only": True, "statement": "Four accepted-live domain outputs are preserved without domain approval, conflict resolution, confidence averaging, or enterprise readiness claims."}, "domain_summaries": summaries, "contribution_map": contributions, "terminology_normalizations": [], "derived_correlations": [], "unresolved_disagreements": disagreements, "completeness": {"expected_designations": EXPECTED, "received_designations": [x["designation"] for x in manifest["inputs"]], "complete_set": True, "authoritative_live_complete": True, "scope_limit": "bounded_code_harness_single_capability_domain_set", "capability_or_child_double_counted": False}, "report_boundary": {"report_package_modified": False, "distribution_state_machine_modified": False, "publication_authorized": False, "decision_recording_authorized": False}, "decision_requests": decisions, "unsupported_claims": [], "downstream_handoff": {"consumers": ["REPORT-PACKAGER-CANDIDATE", "ENT-PORTFOLIO-CANDIDATE"], "handoff_state": "comparison_only", "scheduled": False}, "decision_authority": "human"}

def build_candidate(raw_hash=None):
    artifacts, eligibilities = load_sources(); gate = build_gate(artifacts, eligibilities); manifest = build_manifest(gate, artifacts, eligibilities); role = build_role(gate, artifacts, manifest); aid = sid(manifest["manifest_hash"], content_hash(role), "accepted-live-projection-1.0.0", "candidate")
    value = {"identity": {"agent_uuid": "a4911647-648f-43fd-a51a-ed60d0d9bdf9", "designation": "ENT-SYNTH", "display_name": "Enterprise Synthesis Agent", "agent_version": "design-0.1.0", "contract_version": "1.0.0"}, "artifact": {"artifact_id": aid, "artifact_type": "enterprise-synthesis-posture", "created_at": CREATED, "lifecycle_state": "complete", "links": {"parents": [], "children": [gate["gate_id"]] + [x["artifact"]["artifact_id"] for x in artifacts], "peers": []}}, "execution": {"execution_id": sid(aid, "execution"), "generation_mode": "model_response_with_harness_owned_synthesis_projection" if raw_hash else "deterministic_reference_projection", "model": "qwen3-32b" if raw_hash else "deterministic-reference-agent", "prompt_version": "design-0.1.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}, "raw_model_response_sha256": raw_hash, "harness_owned_fields": ["identity", "exact_bindings", "eligibility_enforcement", "domain_preservation", "limitation_and_source_context_propagation", "completeness", "report_boundary", "authority_boundary", "downstream_state"]}, "scope": {"enterprise_scope_id": "CODE-HARNESS-PROJECT-001", "participating_capabilities": ["CAPABILITY-IDENTITY-ACCESS"], "assessment_period": "2026-08-02", "decision_context": "accepted_live_bounded_enterprise_domain_synthesis_evaluation"}, "inputs": [{"reference": "enterprise-synthesis-evidence-gate", "hash": gate["gate_hash"], "compatibility": "compatible", "freshness": "fresh"}] + [{"artifact_id": x["artifact"]["artifact_id"], "hash": artifact_hash(x), "compatibility": "compatible", "freshness": "fresh"} for x in artifacts] + [{"reference": "enterprise-synthesis-input-manifest", "hash": manifest["manifest_hash"], "compatibility": "compatible", "freshness": "fresh"}], "methodology": {"method": "exact tier-preserving domain synthesis", "limitations": ["Bounded Code Harness domain set", "Single participating capability", "Comparison only", "Not a report, distribution, domain approval, deployment, or scheduling decision", "Raw model output retained separately when present"]}, "coverage": {"eligible": 4, "reviewed": 4, "omitted": 0, "inaccessible": 0, "unknown": 0, "negative_evidence": 0}, "observations": [], "assessments": [], "findings": [], "patterns": [], "insights": [], "conflicts": [], "confidence": {"evidence": 1.0, "assessment": 1.0, "review": 1.0, "decision": None, "provenance": [{"source": "deterministic exact-input and preservation checks", "version": "1.0.0"}]}, "decisions_requested": role["decision_requests"], "consumers": role["downstream_handoff"]["consumers"], "decision_authority": "human", "integrity": {"input_hash": content_hash({"gate": gate["gate_hash"], "manifest": manifest["manifest_hash"]}), "output_hash": None, "attestation_ref": None, "retention_class": "candidate-test", "schema_validation": "passed"}, "extensions": {"enterprise": {"enterprise_scope": {"enterprise_scope_id": "CODE-HARNESS-PROJECT-001", "assessment_period": "2026-08-02"}, "participating_capabilities": ["CAPABILITY-IDENTITY-ACCESS"], "capability_input_manifest": manifest["inputs"], "cross_capability_correlations": [], "enterprise_assertions": role["contribution_map"], "systemic_dependencies": [], "enterprise_unknowns": [x for item in manifest["inputs"] for x in item.get("source_context_carried_forward", [])], "unresolved_disagreements": role["unresolved_disagreements"], "confidence_reconciliation": {"method": "preserve_domain_confidence_without_averaging", "result": None}, "human_decision_requests": role["decision_requests"], "enterprise_traceability_manifest": role["manifest_binding"], "role": role}}}
    value["extensions"]["enterprise"]["enterprise_unknowns"] = [
        {"source_designation": item["designation"], "context": context, "treatment": "preserved_source_context_not_scoring_input"}
        for item in manifest["inputs"] for context in item.get("source_context_carried_forward", [])
    ]
    material = copy.deepcopy(value); material["integrity"]["output_hash"] = None; value["integrity"]["output_hash"] = content_hash(material)
    validate_candidate(value, gate, artifacts, eligibilities, manifest); return value

def validate_candidate(candidate, gate, artifacts, eligibilities, manifest):
    validate_manifest(manifest, gate, artifacts, eligibilities); assert_schema(candidate, "universal-agent-artifact.schema.json", "ADR-0038 candidate"); assert_schema(candidate["extensions"]["enterprise"], "enterprise-extension.schema.json", "ADR-0038 enterprise extension"); assert_schema(candidate["extensions"]["enterprise"]["role"], "ent-synth-role.schema.json", "ADR-0038 role")
    material = copy.deepcopy(candidate); expected = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != expected or candidate["extensions"]["enterprise"]["role"] != build_role(gate, artifacts, manifest): raise ValidationFailure("candidate mutation or projection mismatch")
    if any(x["designation"] == "ENT-SYNTH" for x in load_json(BASELINE)["nodes"]): raise ValidationFailure("ENT-SYNTH unexpectedly scheduled")

def build_packet(candidate, manifest):
    value = {"packet_id": sid(candidate["artifact"]["artifact_id"], "semantic-review"), "packet_version": "1.0.0", "generated_at": CREATED, "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]}, "input_manifest": {"id": manifest["manifest_id"], "hash": manifest["manifest_hash"]}, "projection_provenance": {"generation_mode": candidate["execution"]["generation_mode"], "raw_model_response_sha256": candidate["execution"]["raw_model_response_sha256"], "harness_owned_fields": candidate["execution"]["harness_owned_fields"]}, "review_dimensions": ["domain_source_fidelity", "eligibility_and_supersession", "limitation_and_source_context_preservation", "confidence_meaning", "missingness", "unresolved_decisions", "authority_boundary", "report_boundary", "rollback"], "review_state": "awaiting_human_semantic_review", "required_authority": "project-owner", "effect": "review_request_only", "ent_synth_scheduled": False, "report_effect": "none", "deployment_effect": "none", "packet_hash": "sha256:" + "0" * 64}
    hashed(value, "packet_hash"); assert_schema(value, "enterprise-synthesis-semantic-review-packet.schema.json", "ADR-0038 review packet"); return value

def build_package(raw_hash=None):
    artifacts, eligibilities = load_sources(); gate = build_gate(artifacts, eligibilities); manifest = build_manifest(gate, artifacts, eligibilities); candidate = build_candidate(raw_hash); return gate, manifest, candidate, build_packet(candidate, manifest)
def persist_candidate(root: Path, candidate): return ArtifactLedger(root).persist_artifact(candidate)

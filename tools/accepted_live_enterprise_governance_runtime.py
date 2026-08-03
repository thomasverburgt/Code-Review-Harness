#!/usr/bin/env python3
"""ADR-0036 exact CAP-SYNTH and owner-source ENT-GOV evaluation runtime."""

from __future__ import annotations

import copy
import hashlib
import uuid
from typing import Any

from accepted_live_enterprise_arch_runtime import build_gate as build_cap_synth_gate, load_exact_input
from artifact_ledger import content_hash
from canonical_content import canonical_file_bytes
from enterprise_arch_runtime import BASELINE, rehash
from enterprise_governance_runtime import GOVERNANCE, validate_source
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json, validate_workflow_instance


REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
AUTHORITY_REGISTRY = ROOT / "appendices/governance/decision-authorities-0.1.0.json"
AUTHORITY_SNAPSHOTS = ROOT / "appendices/governance/snapshots"
NAMESPACE = uuid.UUID("36000000-0000-4000-8000-000000000000")
GENERATED_AT = "2026-08-02T10:00:00Z"
SOURCE_REVISION = "ab84b15d3c6bd6ba2c594c9a01457df8474d623e"
OBLIGATION = "Automated agents may analyze, recommend, draft, test, and identify conflicts. They do not approve pull requests, accept risk, change requirements, grant exceptions, or exercise project authority."


def sid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "|".join(parts)))


def _hashed(value: dict[str, Any], field: str) -> dict[str, Any]:
    material = copy.deepcopy(value); material[field] = None
    value[field] = content_hash(material)
    return value


def build_owner_source_manifest() -> dict[str, Any]:
    source_id = "GOVSRC-HARNESS-OWNER-001"
    registry = load_json(AUTHORITY_SNAPSHOTS / "decision-authorities-0.7.0.json")
    value = {
        "manifest_id": sid("owner-governance-source", SOURCE_REVISION), "manifest_version": "1.0.0",
        "created_at": GENERATED_AT, "scope_id": "ENTERPRISE-FIXTURE-001",
        "declared_by": {"authority_role": "governance-source-owner", "authority_name": "thomasverburgt",
                        "subject_id": "HUMAN-PROJECT-OWNER-001",
                        "authority_registry": {"registry_id": registry["registry_id"], "registry_version": registry["registry_version"],
                                               "registry_hash": content_hash(registry)}},
        "sources": [{"source_id": source_id, "classification": "authoritative", "source_type": "repository_governance",
            "authority": "thomasverburgt, project owner", "repository_uri": "https://github.com/thomasverburgt/Code-Review-Harness.git",
            "immutable_revision": SOURCE_REVISION, "path": "GOVERNANCE.md", "line_start": 13, "line_end": 13,
            "line_fingerprint": "sha256:" + hashlib.sha256(OBLIGATION.encode()).hexdigest(),
            "content_hash": "sha256:" + hashlib.sha256(canonical_file_bytes(GOVERNANCE)).hexdigest(),
            "version": f"repository-revision-{SOURCE_REVISION[:12]}", "effective_date": "2026-08-02", "lifecycle_state": "active",
            "scope": ["ENTERPRISE-FIXTURE-001", "CAPABILITY-IDENTITY-ACCESS"],
            "applicability": {"determination": "applicable", "authority_role": "governance-source-owner",
                              "determination_id": "GOVAPP-ADR36-001",
                              "rationale": "The project governance authority boundary applies to automated agents evaluating this harness capability."},
            "obligations": [{"obligation_id": "GOV-AGENT-AUTH-001", "statement": OBLIGATION, "obligation_class": "required",
                             "required_evidence": ["human decision authority", "advisory-only posture", "unscheduled downstream handoff", "no risk acceptance", "no requirements change", "no exception grant"]}],
            "required_approvals": ["project-owner"], "exception_process": "A material exception requires a later explicit ADR and authorized human decision.",
            "retention_rule": "retain with ADR-0036 evaluation evidence", "conflicts": []}],
        "exception_records": [], "approval_records": [], "manifest_hash": "sha256:" + "0" * 64,
    }
    _hashed(value, "manifest_hash")
    validate_owner_source(value)
    return value


def validate_owner_source(source: dict[str, Any]) -> None:
    validate_source(source)
    declared_version = source["declared_by"]["authority_registry"]["registry_version"]
    current = load_json(AUTHORITY_REGISTRY)
    registry_path = AUTHORITY_REGISTRY if current["registry_version"] == declared_version else AUTHORITY_SNAPSHOTS / f"decision-authorities-{declared_version}.json"
    registry = load_json(registry_path)
    if content_hash(registry) != source["declared_by"]["authority_registry"]["registry_hash"]:
        raise ValidationFailure("ADR-0036 declared authority-registry snapshot hash mismatch")
    expected_declarer = {"authority_role": "governance-source-owner", "authority_name": "thomasverburgt",
                         "subject_id": "HUMAN-PROJECT-OWNER-001",
                         "authority_registry": {"registry_id": registry["registry_id"], "registry_version": registry["registry_version"],
                                                "registry_hash": content_hash(registry)}}
    if source["declared_by"] != expected_declarer:
        raise ValidationFailure("ADR-0036 governance source was not declared by the project owner")
    owner = next(item for item in registry["authorities"] if item["authority_role"] == "governance-source-owner")
    if "HUMAN-PROJECT-OWNER-001" not in owner["human_subject_ids"]:
        raise ValidationFailure("ADR-0036 project owner is not registered as governance-source-owner")
    entry = source["sources"][0]
    if entry["immutable_revision"] != SOURCE_REVISION or entry["line_start"] != 13 or entry["line_end"] != 13 or entry["obligations"][0]["statement"] != OBLIGATION:
        raise ValidationFailure("ADR-0036 owner source declaration is not exact")


def _pointer(value: Any, pointer: str) -> Any:
    current = value
    for token in pointer.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def build_evidence_manifest(source: dict[str, Any], eligibility: dict[str, Any]) -> dict[str, Any]:
    source_id = source["artifact"]["artifact_id"]
    records = [
        {"locator_id": "GOV-EVID-CAPSYNTH-DECISION-AUTHORITY", "source_kind": "capability_artifact", "source_id": source_id,
         "source_hash": content_hash(source), "json_pointer": "/decision_authority", "expected_value": "human", "purpose": "Proves the artifact preserves human decision authority."},
        {"locator_id": "GOV-EVID-CAPSYNTH-ADVISORY-ONLY", "source_kind": "capability_artifact", "source_id": source_id,
         "source_hash": content_hash(source), "json_pointer": "/extensions/capability/role/capability_posture/advisory_only", "expected_value": True, "purpose": "Proves the synthesized posture is advisory only."},
        {"locator_id": "GOV-EVID-CAPSYNTH-COMPARISON-HANDOFF", "source_kind": "capability_artifact", "source_id": source_id,
         "source_hash": content_hash(source), "json_pointer": "/extensions/capability/role/enterprise_handoff/handoff_state", "expected_value": "comparison_only", "purpose": "Proves the enterprise handoff is comparison only."},
        {"locator_id": "GOV-EVID-CAPSYNTH-UNSCHEDULED", "source_kind": "eligibility_record", "source_id": eligibility["eligibility_id"],
         "source_hash": content_hash(eligibility), "json_pointer": "/cap_synth_scheduled", "expected_value": False, "purpose": "Proves semantic eligibility did not schedule CAP-SYNTH."},
    ]
    value = {"manifest_id": sid("evidence-binding", source_id, eligibility["record_hash"]), "manifest_version": "1.0.0",
             "generated_at": GENERATED_AT, "records": records, "manifest_hash": "sha256:" + "0" * 64}
    _hashed(value, "manifest_hash"); validate_evidence_manifest(value, source, eligibility); return value


def validate_evidence_manifest(value: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any]) -> None:
    assert_schema(value, "enterprise-governance-evidence-binding.schema.json", "ADR-0036 evidence binding")
    if content_hash({**value, "manifest_hash": None}) != value["manifest_hash"]:
        raise ValidationFailure("ADR-0036 evidence binding hash mismatch")
    expected_sources = {"capability_artifact": (source["artifact"]["artifact_id"], content_hash(source), source),
                        "eligibility_record": (eligibility["eligibility_id"], content_hash(eligibility), eligibility)}
    if len(value["records"]) != 4 or len({item["locator_id"] for item in value["records"]}) != 4:
        raise ValidationFailure("ADR-0036 evidence binding is incomplete or duplicated")
    for item in value["records"]:
        expected_id, expected_hash, document = expected_sources[item["source_kind"]]
        if (item["source_id"], item["source_hash"]) != (expected_id, expected_hash) or _pointer(document, item["json_pointer"]) != item["expected_value"]:
            raise ValidationFailure("ADR-0036 evidence locator binding mismatch")


def build_gate(source: dict[str, Any]) -> dict[str, Any]:
    gate = build_cap_synth_gate(source)
    gate["observations"] = [{"observation_id": "OBS-ENTEVID-ADR36-001",
        "fact": "The declared CAP-SYNTH artifact is present, traceable, fresh, compatible, and admitted once for single-capability enterprise governance evaluation.",
        "evidence_refs": [source["artifact"]["artifact_id"]]}]
    rehash(gate)
    return gate


def build_input_manifest(gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    value = {"manifest_id": sid("input", source["artifact"]["artifact_id"], governance["manifest_hash"]), "manifest_version": "1.0.0",
        "generated_at": GENERATED_AT, "ent_evidence_gate": {"id": gate["artifact"]["artifact_id"], "hash": content_hash(gate)},
        "cap_synth_candidate": {"id": source["artifact"]["artifact_id"], "hash": source["integrity"]["output_hash"]},
        "cap_synth_eligibility": {"id": eligibility["eligibility_id"], "hash": eligibility["record_hash"]},
        "governance_source_manifest": {"id": governance["manifest_id"], "hash": content_hash(governance)},
        "governance_evidence_manifest": {"id": evidence["manifest_id"], "hash": content_hash(evidence)},
        "admitted_capability_artifact_ids": [source["artifact"]["artifact_id"]],
        "excluded_child_artifact_ids": sorted(source["artifact"]["links"]["children"]),
        "anti_double_counting": "parent_only_children_retained_as_lineage",
        "evidence_tier": "accepted_live_multi_domain_single_capability_governance_evaluation",
        "effect": "evaluation_input_only", "manifest_hash": "sha256:" + "0" * 64}
    _hashed(value, "manifest_hash")
    validate_input_manifest(value, gate, source, eligibility, governance, evidence)
    return value


def validate_input_manifest(value: dict[str, Any], gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any]) -> None:
    assert_schema(value, "enterprise-governance-evaluation-input.schema.json", "ADR-0036 input manifest")
    if content_hash({**value, "manifest_hash": None}) != value["manifest_hash"]:
        raise ValidationFailure("ADR-0036 input manifest hash mismatch")
    if value["admitted_capability_artifact_ids"] != [source["artifact"]["artifact_id"]] or set(value["excluded_child_artifact_ids"]) != set(source["artifact"]["links"]["children"]):
        raise ValidationFailure("ADR-0036 parent-child double counting or substitution")
    expected = (gate["artifact"]["artifact_id"], content_hash(gate), eligibility["eligibility_id"], eligibility["record_hash"], governance["manifest_id"], content_hash(governance), evidence["manifest_id"], content_hash(evidence))
    actual = (value["ent_evidence_gate"]["id"], value["ent_evidence_gate"]["hash"], value["cap_synth_eligibility"]["id"], value["cap_synth_eligibility"]["hash"], value["governance_source_manifest"]["id"], value["governance_source_manifest"]["hash"], value["governance_evidence_manifest"]["id"], value["governance_evidence_manifest"]["hash"])
    if actual != expected:
        raise ValidationFailure("ADR-0036 exact input binding mismatch")


def allowed_evidence_refs(source: dict[str, Any]) -> set[str]:
    role = source["extensions"]["capability"]["role"]
    return ({source["artifact"]["artifact_id"]} | set(role["enterprise_handoff"]["preserved_record_ids"])
            | {item["assertion_id"] for item in role["derived_capability_assertions"]}
            | {ref for item in role["preserved_child_assertions"] for ref in item["evidence_refs"]})


def deterministic_role(gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any], input_manifest: dict[str, Any]) -> dict[str, Any]:
    aid = source["artifact"]["artifact_id"]; entry = governance["sources"][0]; obligation = entry["obligations"][0]
    baseline = {"source_id": entry["source_id"], "obligation_id": obligation["obligation_id"], "classification": "authoritative",
                "applicability": "applicable", "source_locator": "GOVERNANCE.md:13", "source_hash": entry["content_hash"]}
    row = {"row_id": f"ROW-{obligation['obligation_id']}-{aid[:8]}", "source_id": entry["source_id"], "obligation_id": obligation["obligation_id"],
           "capability_artifact_id": aid, "state": "insufficient_evidence",
           "rationale": "CAP-SYNTH preserves human decision authority, advisory-only posture, and an unscheduled comparison handoff, but the bounded artifact does not prove enforcement of every repository agent prohibition.",
           "evidence_refs": [item["locator_id"] for item in evidence["records"]], "applicability_determination_id": entry["applicability"]["determination_id"],
           "confidence": 0.85, "uncertainty": "No execution-control evidence proves that all agent instances cannot approve pull requests, change requirements, grant exceptions, or exercise project authority."}
    return {"designation": "ENT-GOV", "evidence_tier": "accepted_live_multi_domain_single_capability_governance_evaluation",
        "fitness_claim": "single_capability_governance_evaluation",
        "manifest_binding": {"gate_artifact_id": gate["artifact"]["artifact_id"], "gate_artifact_hash": content_hash(gate),
            "capability_artifact_ids": [aid], "capability_artifact_hashes": [content_hash(source)],
            "governance_manifest_id": governance["manifest_id"], "governance_manifest_hash": content_hash(governance),
            "cap_synth_eligibility_id": eligibility["eligibility_id"], "cap_synth_eligibility_hash": eligibility["record_hash"],
            "governance_evidence_manifest_id": evidence["manifest_id"], "governance_evidence_manifest_hash": content_hash(evidence),
            "evaluation_input_manifest_id": input_manifest["manifest_id"], "evaluation_input_manifest_hash": input_manifest["manifest_hash"],
            "binding_state": "exact"},
        "governance_baseline": [baseline], "compliance_matrix": [row], "governance_inconsistencies": [],
        "exception_register": [], "approval_dependencies": [], "governance_conflicts": [],
        "governance_maturity": {"state": "insufficient_evidence", "advisory_only": True, "rationale": "One capability and one obligation cannot establish enterprise governance maturity."},
        "capa_options": [], "decision_requests": [], "unsupported_claims": [],
        "downstream_handoff": {"consumers": ["ENT-STRAT-CANDIDATE", "ENT-SYNTH-CANDIDATE"], "handoff_state": "comparison_only", "scheduled": False},
        "decision_authority": "human"}


def build_candidate(gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any], input_manifest: dict[str, Any], model_role: dict[str, Any] | None = None, raw_response_sha256: str | None = None) -> dict[str, Any]:
    expected = deterministic_role(gate, source, eligibility, governance, evidence, input_manifest); role = copy.deepcopy(expected if model_role is None else model_role)
    for key in ("designation", "evidence_tier", "fitness_claim", "manifest_binding", "governance_baseline", "compliance_matrix",
                "governance_inconsistencies", "exception_register", "approval_dependencies", "governance_conflicts",
                "governance_maturity", "capa_options", "unsupported_claims", "downstream_handoff", "decision_authority"):
        role[key] = copy.deepcopy(expected[key])
    aid = sid("candidate", source["integrity"]["output_hash"], governance["manifest_hash"]); capability_id = source["extensions"]["capability"]["capability_id"]
    harness_fields = ["governance_baseline", "compliance_matrix", "governance_inconsistencies", "exception_register", "approval_dependencies", "governance_conflicts", "governance_maturity", "capa_options", "authority_boundary"]
    if model_role is not None and raw_response_sha256 is None: raw_response_sha256 = content_hash(model_role).split(":", 1)[1]
    generation_mode = "deterministic_reference_projection" if model_role is None else "model_response_with_harness_owned_governance_projection"
    candidate = {"identity": {"agent_uuid": "bc12d42a-6837-4084-a419-3d5a14618714", "designation": "ENT-GOV", "display_name": "Enterprise Governance Reviewer", "agent_version": "design-0.1.0", "contract_version": "1.0.0"},
        "artifact": {"artifact_id": aid, "artifact_type": "enterprise-governance-posture", "created_at": GENERATED_AT, "lifecycle_state": "complete", "links": {"parents": [], "children": [gate["artifact"]["artifact_id"], source["artifact"]["artifact_id"]], "peers": []}},
        "execution": {"execution_id": sid(aid, "execution"), "model": "qwen3-32b" if model_role is not None else "deterministic-reference-agent", "prompt_version": "design-0.1.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}, "evidence_tier": role["evidence_tier"], "generation_mode": generation_mode, "raw_model_response_sha256": raw_response_sha256, "harness_owned_fields": harness_fields},
        "scope": {"enterprise_scope_id": governance["scope_id"], "participating_capabilities": [capability_id], "assessment_period": "2026-08-02", "decision_context": "accepted_live_single_capability_governance_evaluation"},
        "inputs": [{"artifact_id": gate["artifact"]["artifact_id"], "hash": content_hash(gate), "compatibility": "compatible", "freshness": "fresh"}, {"artifact_id": source["artifact"]["artifact_id"], "hash": content_hash(source), "compatibility": "compatible", "freshness": "fresh"}, {"reference": "cap-synth-eligibility", "hash": content_hash(eligibility), "compatibility": "compatible", "freshness": "fresh"}, {"reference": "governance-source-manifest", "hash": content_hash(governance), "compatibility": "compatible", "freshness": "fresh"}, {"reference": "governance-evidence-manifest", "hash": content_hash(evidence), "compatibility": "compatible", "freshness": "fresh"}, {"reference": "enterprise-governance-input-manifest", "hash": content_hash(input_manifest), "compatibility": "compatible", "freshness": "fresh"}],
        "methodology": {"method": "owner-source and eligibility gated governance evaluation", "limitations": ["One capability only", "No legal or compliance approval", "Comparison only", "The obligation row and authority boundary are deterministic harness projections; raw model output is retained separately."]},
        "coverage": {"eligible": 1, "reviewed": 1, "omitted": 0, "inaccessible": 0, "unknown": 1, "negative_evidence": 0},
        "observations": [], "assessments": [], "findings": [], "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 1.0, "assessment": role["compliance_matrix"][0]["confidence"], "review": 1.0, "decision": None, "provenance": [{"artifact_id": source["artifact"]["artifact_id"], "confidence": source["confidence"]["assessment"]}]},
        "decisions_requested": copy.deepcopy(role["decision_requests"]), "consumers": role["downstream_handoff"]["consumers"], "decision_authority": "human",
        "integrity": {"input_hash": content_hash({"gate": content_hash(gate), "source": content_hash(source), "governance": content_hash(governance)}), "output_hash": None, "attestation_ref": None, "retention_class": "candidate-test", "schema_validation": "passed"},
        "extensions": {"enterprise": {"enterprise_scope": {"enterprise_scope_id": governance["scope_id"], "assessment_period": "2026-08-02"}, "participating_capabilities": [capability_id],
            "capability_input_manifest": [{"artifact_id": source["artifact"]["artifact_id"], "content_hash": content_hash(source), "state": "valid"}],
            "cross_capability_correlations": role["governance_inconsistencies"], "enterprise_assertions": role["compliance_matrix"], "systemic_dependencies": [],
            "enterprise_unknowns": [{"statement": item["uncertainty"]} for item in role["compliance_matrix"]], "unresolved_disagreements": role["governance_conflicts"],
            "confidence_reconciliation": {"method": "confidence_in_bounded_evidence_insufficiency_not_compliance", "result": role["compliance_matrix"][0]["confidence"]},
            "human_decision_requests": role["decision_requests"], "enterprise_traceability_manifest": {"gate_artifact_id": gate["artifact"]["artifact_id"], "artifact_ids": [source["artifact"]["artifact_id"]], "cap_synth_eligibility_id": eligibility["eligibility_id"], "governance_manifest_id": governance["manifest_id"], "governance_evidence_manifest_id": evidence["manifest_id"], "evaluation_input_manifest_id": input_manifest["manifest_id"], "excluded_child_artifact_ids": sorted(source["artifact"]["links"]["children"])}, "role": role}}}
    rehash(candidate); validate_candidate(candidate, gate, source, eligibility, governance, evidence, input_manifest); return candidate


def validate_candidate(candidate: dict[str, Any], gate: dict[str, Any], source: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any], input_manifest: dict[str, Any]) -> None:
    validate_owner_source(governance); validate_evidence_manifest(evidence, source, eligibility); validate_input_manifest(input_manifest, gate, source, eligibility, governance, evidence); assert_schema(candidate, "universal-agent-artifact.schema.json", "ADR-0036 ENT-GOV candidate")
    extension = candidate["extensions"]["enterprise"]; assert_schema(extension, "enterprise-extension.schema.json", "ADR-0036 ENT-GOV extension")
    role = extension["role"]; assert_schema(role, "ent-gov-role.schema.json", "ADR-0036 ENT-GOV role")
    material = copy.deepcopy(candidate); expected_hash = material["integrity"]["output_hash"]; material["integrity"]["output_hash"] = None
    if content_hash(material) != expected_hash: raise ValidationFailure("ADR-0036 ENT-GOV output hash mismatch")
    binding = role["manifest_binding"]
    expected_binding = (gate["artifact"]["artifact_id"], content_hash(gate), [source["artifact"]["artifact_id"]], [content_hash(source)], governance["manifest_id"], content_hash(governance), eligibility["eligibility_id"], eligibility["record_hash"], evidence["manifest_id"], content_hash(evidence), input_manifest["manifest_id"], input_manifest["manifest_hash"])
    actual_binding = (binding["gate_artifact_id"], binding["gate_artifact_hash"], binding["capability_artifact_ids"], binding["capability_artifact_hashes"], binding["governance_manifest_id"], binding["governance_manifest_hash"], binding.get("cap_synth_eligibility_id"), binding.get("cap_synth_eligibility_hash"), binding.get("governance_evidence_manifest_id"), binding.get("governance_evidence_manifest_hash"), binding.get("evaluation_input_manifest_id"), binding.get("evaluation_input_manifest_hash"))
    if actual_binding != expected_binding: raise ValidationFailure("ADR-0036 ENT-GOV exact input binding mismatch")
    if role["evidence_tier"] != "accepted_live_multi_domain_single_capability_governance_evaluation" or role["fitness_claim"] != "single_capability_governance_evaluation": raise ValidationFailure("ADR-0036 evidence tier mismatch")
    expected_role = deterministic_role(gate, source, eligibility, governance, evidence, input_manifest); rows = role["compliance_matrix"]
    if rows != expected_role["compliance_matrix"]:
        raise ValidationFailure("ADR-0036 governance matrix is incomplete or invented")
    if rows[0]["state"] != "insufficient_evidence" or set(rows[0]["evidence_refs"]) != {item["locator_id"] for item in evidence["records"]}:
        raise ValidationFailure("ADR-0036 governance evidence or missingness semantics violated")
    if role["governance_baseline"] != expected_role["governance_baseline"] or role["governance_inconsistencies"] or role["governance_conflicts"] or role["exception_register"] or role["approval_dependencies"] or role["governance_maturity"]["state"] != "insufficient_evidence" or role["capa_options"]:
        raise ValidationFailure("ADR-0036 invented governance authority or overclaimed maturity")
    if role["unsupported_claims"] or role["downstream_handoff"]["scheduled"] or role["downstream_handoff"]["handoff_state"] != "comparison_only" or candidate["decision_authority"] != "human":
        raise ValidationFailure("ADR-0036 authority boundary violated")
    if candidate["extensions"]["enterprise"]["confidence_reconciliation"]["method"] != "confidence_in_bounded_evidence_insufficiency_not_compliance":
        raise ValidationFailure("ADR-0036 confidence interpretation is ambiguous")
    execution = candidate["execution"]
    if execution.get("generation_mode") not in {"deterministic_reference_projection", "model_response_with_harness_owned_governance_projection"} or execution.get("harness_owned_fields") != ["governance_baseline", "compliance_matrix", "governance_inconsistencies", "exception_register", "approval_dependencies", "governance_conflicts", "governance_maturity", "capa_options", "authority_boundary"]:
        raise ValidationFailure("ADR-0036 projection provenance is incomplete")
    raw_hash = execution.get("raw_model_response_sha256")
    if execution["generation_mode"] == "model_response_with_harness_owned_governance_projection" and (not isinstance(raw_hash, str) or len(raw_hash) != 64 or any(ch not in "0123456789abcdef" for ch in raw_hash)):
        raise ValidationFailure("ADR-0036 raw model response provenance is missing")
    if any(node["designation"] == "ENT-GOV" for node in load_json(BASELINE)["nodes"]): raise ValidationFailure("ADR-0036 cannot schedule ENT-GOV")


def build_review_packet(candidate: dict[str, Any], input_manifest: dict[str, Any], eligibility: dict[str, Any], governance: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    value = {"packet_id": sid(candidate["artifact"]["artifact_id"], "semantic-review"), "packet_version": "1.0.0", "generated_at": GENERATED_AT,
        "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
        "input_manifest": {"id": input_manifest["manifest_id"], "hash": input_manifest["manifest_hash"]},
        "cap_synth_eligibility": {"id": eligibility["eligibility_id"], "hash": eligibility["record_hash"]},
        "governance_source_manifest": {"id": governance["manifest_id"], "hash": content_hash(governance)},
        "governance_evidence_manifest": {"id": evidence["manifest_id"], "hash": content_hash(evidence)},
        "projection_provenance": {"generation_mode": candidate["execution"]["generation_mode"],
                                  "raw_model_response_sha256": candidate["execution"]["raw_model_response_sha256"],
                                  "harness_owned_fields": candidate["execution"]["harness_owned_fields"]},
        "review_dimensions": ["source_authority", "obligation_preservation", "applicability", "capability_evidence", "missingness", "confidence_and_uncertainty", "authority_boundary", "rollback"],
        "review_state": "awaiting_human_semantic_review", "required_authority": "project-owner", "effect": "review_request_only",
        "cap_synth_scheduled": False, "ent_gov_scheduled": False, "report_effect": "none", "deployment_effect": "none", "packet_hash": "sha256:" + "0" * 64}
    _hashed(value, "packet_hash"); assert_schema(value, "enterprise-governance-semantic-review-packet.schema.json", "ADR-0036 review packet"); return value


def build_compatibility(candidate: dict[str, Any]) -> dict[str, Any]:
    return {"record_id": sid(candidate["artifact"]["artifact_id"], "compatibility"), "generated_at": GENERATED_AT,
        "candidate": {"id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"]},
        "results": [{"consumer": "ENT-SYNTH", "state": "compatible_via_tiered_enterprise_domain_wrapper"}, {"consumer": "ENT-STRAT", "state": "candidate_interface_only_unscheduled"}], "effect": "comparison_only", "scheduled": False}


def build_package(model_role: dict[str, Any] | None = None, *, raw_response_sha256: str | None = None, eligibility_override: dict[str, Any] | None = None, governance_override: dict[str, Any] | None = None, evidence_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], ...]:
    source, eligibility = load_exact_input(eligibility_override=eligibility_override); governance = copy.deepcopy(governance_override) if governance_override is not None else build_owner_source_manifest()
    validate_owner_source(governance); evidence = copy.deepcopy(evidence_override) if evidence_override is not None else build_evidence_manifest(source, eligibility); validate_evidence_manifest(evidence, source, eligibility)
    gate = build_gate(source); manifest = build_input_manifest(gate, source, eligibility, governance, evidence)
    candidate = build_candidate(gate, source, eligibility, governance, evidence, manifest, model_role, raw_response_sha256); review = build_review_packet(candidate, manifest, eligibility, governance, evidence)
    workflow = load_json(ROOT / "appendices/candidate-workflows/ent-gov-accepted-live-multi-domain-evaluation.workflow.json")
    registry = {item["designation"]: item for item in load_json(ROOT / "agents/agent-identities.json")["agents"]}; validate_workflow_instance(workflow, registry, "ADR-0036 workflow")
    return source, eligibility, governance, evidence, gate, manifest, candidate, build_compatibility(candidate), review

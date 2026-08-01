#!/usr/bin/env python3
"""ADR-0019 deterministic CAP-REQ candidate projection and admission controls."""
from __future__ import annotations
import copy, uuid
from typing import Any
from artifact_ledger import content_hash
from capability_coordination_runtime import build_manifest
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

NAMESPACE=uuid.UUID("19000000-0000-4000-8000-000000000000")
SOURCE=ROOT/"fixtures/cap-req-admission/input/requirements-source-manifest.json"
LOCATORS=ROOT/"fixtures/vertical-risk-slice/evidence/evidence-locator-increment4-2026-07-31/reference-run/evidence-locator.json"
PRODUCT=ROOT/"fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/accepted-prod-sec.artifact.json"
BASELINE=ROOT/"appendices/example-workflows/vertical-risk-slice.workflow.json"
REPORT=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
CREATED_AT="2026-08-01T22:00:00Z"
def sid(*p:str)->str:return str(uuid.uuid5(NAMESPACE,"|".join(p)))
def rehash(a:dict[str,Any])->dict[str,Any]:
    a["integrity"]["output_hash"]=None;a["integrity"]["output_hash"]=content_hash(a);return a

def inputs()->tuple[dict[str,Any],dict[str,Any],dict[str,Any]]:
    source=load_json(SOURCE); product=load_json(PRODUCT)
    locator=next((x for x in load_json(LOCATORS) if x["locator_id"]==source["evidence_locator"]["locator_id"]),None)
    if not locator or any(locator[k]!=source["evidence_locator"][k] for k in ("locator_id","evidence_id","path","line_start","line_end","line_fingerprint","locator_hash")):
        raise ValidationFailure("CAP-REQ source manifest locator mismatch")
    if source["mutation_performed"] or not source["immutable_revision"]: raise ValidationFailure("CAP-REQ source is mutable")
    return source,locator,product

def role_template(source:dict[str,Any],locator:dict[str,Any])->dict[str,Any]:
    return {"designation":"CAP-REQ","evidence_tier":"accepted_live_input_calibration","declared_population":{"source_manifest_hash":content_hash(source),"count":0,"population_state":"none_declared_for_slice"},"requirement_records":[],"traceability_gaps":[{"gap_id":"GAP-REQ-001","statement":"No authoritative requirement is declared for the bounded evidence slice; satisfaction cannot be assessed.","evidence_locator_ids":[locator["locator_id"]],"state":"unresolvable_without_declared_requirement"}],"coverage":{"declared":0,"reviewed":0,"satisfied":0,"partially_satisfied":0,"unsatisfied":0,"unknown":0,"not_reviewed":0,"fraction":None},"unsupported_claims":[],"acceptance_state":"pending_human_requirements_acceptance","decision_requests":[{"decision_context_id":"DC-REQ-001","question":"What authoritative requirement source, if any, governs this evidence slice?","required_authority":"requirements-acceptance-authority"}],"decision_authority":"human"}

def build_candidate(model_role:dict[str,Any]|None=None)->dict[str,Any]:
    source,locator,product=inputs(); role=role_template(source,locator)
    if model_role is not None:
        for f in ("requirement_records","traceability_gaps","unsupported_claims","decision_requests"):
            if f not in model_role: raise ValidationFailure(f"CAP-REQ model payload omitted {f}")
            role[f]=copy.deepcopy(model_role[f])
    aid=sid(content_hash(source),product["artifact"]["artifact_id"],"candidate")
    candidate={"identity":{"agent_uuid":"9a82a407-38f6-4abe-9ef8-49f0fd256e67","designation":"CAP-REQ","display_name":"Requirements Traceability Reviewer","agent_version":"design-0.1.0","contract_version":"1.0.0"},"artifact":{"artifact_id":aid,"artifact_type":"capability-requirements-posture","created_at":CREATED_AT,"lifecycle_state":"complete","links":{"parents":[],"children":[product["artifact"]["artifact_id"]],"peers":[]}},"execution":{"execution_id":sid(aid,"execution"),"model":"qwen3-32b" if model_role is not None else "deterministic-reference-agent","prompt_version":"design-0.1.0","rubric_version":"0.1.0","toolchain_version":"0.1.0","settings":{"temperature":0}},"scope":{"capability_id":"CAPABILITY-IDENTITY-ACCESS","source_revision":source["immutable_revision"],"decision_context":"candidate_calibration","included":[source["scope_id"]],"excluded":["inferred requirements","contractual acceptance","CAP-SYNTH scheduling"]},"inputs":[{"artifact_id":product["artifact"]["artifact_id"],"hash":product["integrity"]["output_hash"],"compatibility":"compatible","freshness":"fresh"},{"reference":"requirements-source-manifest","hash":content_hash(source),"compatibility":"compatible","freshness":"fresh"},{"reference":locator["locator_id"],"hash":locator["locator_hash"],"compatibility":"compatible","freshness":"fresh"}],"methodology":{"method":"declared-population requirements traceability review","limitations":["No authoritative requirement is declared for this bounded slice"]},"coverage":{"eligible":0,"reviewed":0,"omitted":0,"inaccessible":0,"unknown":0,"negative_evidence":0},"observations":[{"observation_id":"OBS-REQ-001","fact":"The bounded source manifest declares zero authoritative requirements.","evidence_refs":[locator["locator_id"]]}],"assessments":[{"assessment_id":"ASM-REQ-001","rationale":"Requirement satisfaction is not assessable without a declared requirement.","confidence":1.0}],"findings":[{"finding_id":"FINDING-REQ-GAP-001","statement":"Requirement traceability is unavailable because no authoritative requirement is declared for the bounded slice.","evidence_refs":[locator["locator_id"]],"root_cause":"process_or_governance_gap","impact":"No requirement satisfaction claim can be made.","capa":{"corrective_action":"Identify and bind the authoritative requirement source or record that none applies.","preventive_action":"Require immutable requirement-source manifests before traceability review.","owner_role":"requirements_engineer","target_horizon":"short_term","implementation_level":"process_level","validation_method":"independent requirements-authority review"}}],"patterns":[],"insights":[],"conflicts":[],"confidence":{"evidence":1.0,"assessment":1.0,"review":1.0,"decision":None,"provenance":[{"source":"requirements source manifest","version":"1.0.0"}]},"decisions_requested":copy.deepcopy(role["decision_requests"]),"consumers":["CAP-COORD-CANDIDATE"],"decision_authority":"human","integrity":{"input_hash":content_hash({"source":source,"locator_hash":locator["locator_hash"],"product_hash":product["integrity"]["output_hash"]}),"output_hash":None,"attestation_ref":None,"retention_class":"candidate-test","schema_validation":"passed"},"extensions":{"capability":{"capability_id":"CAPABILITY-IDENTITY-ACCESS","participating_products":["PRODUCT-ALPHA"],"mission_thread":{},"requirement_traceability":{"state":"unassessable_no_declared_requirement","gap_ids":["GAP-REQ-001"]},"cross_product_interface_state":{},"human_centered_systems_evaluation":{},"mission_effectiveness_evidence":[],"operational_readiness":{"state":"unknown"},"capability_risk_posture":{"state":"not_assessed","decision_authority":"human"},"technical_confidence_rollup":{"method":"declared population integrity","result":1.0},"capability_confidence_score":1.0,"decision_conflicts":[],"enterprise_escalations":[{"escalation_id":"DC-REQ-001","authority":"requirements-acceptance-authority"}],"role":role}}}
    rehash(candidate);validate_candidate(candidate);return candidate

def validate_candidate(c:dict[str,Any])->None:
    source,locator,product=inputs();assert_schema(c,"universal-agent-artifact.schema.json","CAP-REQ candidate");ext=c["extensions"]["capability"];assert_schema(ext,"capability-extension.schema.json","CAP-REQ extension");role=ext["role"];assert_schema(role,"cap-req-role.schema.json","CAP-REQ role")
    material=copy.deepcopy(c);h=material["integrity"]["output_hash"];material["integrity"]["output_hash"]=None
    if content_hash(material)!=h:raise ValidationFailure("CAP-REQ output hash mismatch")
    if role["declared_population"]!={"source_manifest_hash":content_hash(source),"count":0,"population_state":"none_declared_for_slice"}:raise ValidationFailure("CAP-REQ declared population mismatch")
    if role["requirement_records"]:raise ValidationFailure("CAP-REQ invented a requirement from an empty population")
    zeros={"declared":0,"reviewed":0,"satisfied":0,"partially_satisfied":0,"unsatisfied":0,"unknown":0,"not_reviewed":0,"fraction":None}
    if role["coverage"]!=zeros:raise ValidationFailure("CAP-REQ zero-population coverage is dishonest")
    if len(role["traceability_gaps"])!=1 or role["traceability_gaps"][0]["evidence_locator_ids"]!=[locator["locator_id"]]:raise ValidationFailure("CAP-REQ locator gap mismatch")
    if any(x["required_authority"]!="requirements-acceptance-authority" for x in role["decision_requests"]):raise ValidationFailure("CAP-REQ decision authority mismatch")
    if c["artifact"]["links"]["children"]!=[product["artifact"]["artifact_id"]] or c["decision_authority"]!="human":raise ValidationFailure("CAP-REQ lineage or authority mismatch")
    if any(n["designation"] in {"CAP-REQ","CAP-SYNTH"} for n in load_json(BASELINE)["nodes"]):raise ValidationFailure("candidate capability roles cannot be baseline scheduled")
    manifest=build_manifest([c],["CAP-REQ"])
    if manifest["routing"]["state"]!="ready_for_cap_synth":raise ValidationFailure("CAP-REQ candidate is not CAP-COORD compatible")

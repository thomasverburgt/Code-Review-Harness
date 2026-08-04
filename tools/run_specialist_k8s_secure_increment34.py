#!/usr/bin/env python3
"""Build deterministic ADR-0039 Increment 3 and 4 candidates; human review stays deferred."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import run_specialist_build_supply_chain_increment2 as base
from specialist_shadow_calibration_runtime import ROOT, seal_hash, validate_manifest

DEFAULT_OUTPUT = ROOT / "fixtures" / "specialist-k8s-secure-increment34" / "gold"
CONFIG = {
 "SPEC-K8S-WORKLOAD":{"slug":"spec-k8s-workload","display":"Kubernetes Workload Security Reviewer","domain":"kubernetes_workload_security","increment":3,"evidence":[
  ("EVIDENCE-K8S-WORKLOAD-SA-001","src/test/app-admin.yaml",43,"      serviceAccountName: httpbin","service account","sha256:4f77066037aaab25f70d45bc109122338f0d883b00746090e5565f9b5ede4ba3","configuration"),
  ("EVIDENCE-K8S-WORKLOAD-SC-001","src/test/app-admin.yaml",58,"            allowPrivilegeEscalation: false","container security context","sha256:4f77066037aaab25f70d45bc109122338f0d883b00746090e5565f9b5ede4ba3","configuration")],
  "observation":"The admitted workload manifest names a service account and declares a container security context that disables privilege escalation, runs non-root, and drops capabilities.","finding":"The source manifest declares workload hardening, but no admission result, effective policy, pod status, runtime identity, or execution evidence is admitted.","corrective":"Retain admission decisions and immutable runtime observations for the exact rendered workload.","preventive":"Continuously verify rendered workload identity and least-privilege controls against admission and runtime evidence.","unknown":"Admission enforcement, mutation, effective namespace policy, runtime identity, and deployable readiness are not demonstrated by source configuration alone."},
 "SPEC-K8S-PLATFORM":{"slug":"spec-k8s-platform","display":"Kubernetes Platform Security Reviewer","domain":"kubernetes_platform_security","increment":3,"evidence":[
  ("EVIDENCE-K8S-PLATFORM-NETPOL-001",".github/test-infra/aws/eks/cluster.tf",160,"        enableNetworkPolicy = \"true\"","EKS VPC CNI configuration","sha256:f1fea85dcf05b2511c21ad8b31ac9138a478df956dc2a206f914df51d80e87f3","iac")],
  "observation":"The admitted EKS desired state enables the VPC CNI network-policy option.","finding":"No live cluster state, policy inventory, enforcement test, tenant boundary test, control-plane observation, or failure evidence is admitted.","corrective":"Retain live configuration and negative/positive enforcement tests for the exact cluster revision.","preventive":"Continuously reconcile platform desired state with observed controls and tenant-isolation tests.","unknown":"Actual installation, enforcement, coverage, tenant isolation, drift, and platform effectiveness remain unknown from IaC desired state alone."},
 "SPEC-COMMS":{"slug":"spec-comms","display":"Workload Communication Security Reviewer","domain":"communication_trust_paths","increment":3,"evidence":[
  ("EVIDENCE-COMMS-MTLS-STRICT-001","src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml",12,"    mode: STRICT","default mTLS posture","sha256:997d1e3c370b888254bb016f1158d241717d7e10ec57b487a77823bf15bff232","configuration"),
  ("EVIDENCE-COMMS-MTLS-EXCEPTION-001","src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml",19,"      mode: PERMISSIVE","port 10250 exception","sha256:997d1e3c370b888254bb016f1158d241717d7e10ec57b487a77823bf15bff232","configuration"),
  ("EVIDENCE-COMMS-UDP-BOUNDARY-001","src/pepr/operator/crd/sources/package/v1alpha1.ts",185,"UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.","UDP protocol contract","sha256:f4ba8a9ea016ce84b42843eca7bcc0d501c5ee7734387f9fd7adba781a06dbd4","git_source"),
  ("EVIDENCE-COMMS-TOPOLOGY-001","src/test/app-admin-package.yaml",17,"        - name: httpbin","bounded service topology","sha256:813beed77a5a843c83869037cc21c957c22b074db3a6a380816438d86e91813a","configuration")],
  "observation":"The topology declares an exposed httpbin service and egress, while communication policy declares STRICT mTLS with a port-specific PERMISSIVE exception and documents that UDP bypasses Istio mTLS and AuthorizationPolicy.","finding":"No rendered route set, identity binding, authorization result, traffic test, telemetry, or failure-path evidence is admitted.","corrective":"Retain the rendered topology plus authenticated positive and unauthorized negative traffic tests for every declared path and exception.","preventive":"Continuously compare declared topology, protocol exceptions, authorization policy, certificates, and observed traffic paths.","unknown":"Effective identity, encryption, authorization, exposure, lateral-movement resistance, and failure behavior are not demonstrated without runtime traffic evidence."},
 "SPEC-SECURE-CODE":{"slug":"spec-secure-code","display":"Secure Coding Reviewer","domain":"secure_implementation","increment":4,"evidence":[
  ("EVIDENCE-SECURE-CODE-SANITIZE-001","src/pepr/operator/crd/validators/package-validator.ts",74,"    const sanitizedName = sanitizeResourceName(customGateway.name);","custom gateway input sanitization","sha256:f7a0a04a7bd520cc0e68844eb2a7954bb472f25f9afacbe09e359cad11320c24","git_source"),
  ("EVIDENCE-SECURE-CODE-UDP-VALIDATION-001","src/pepr/operator/crd/validators/package-validator.ts",88,"    if (expose.protocol === \"UDP\") {","UDP incompatible-field validation","sha256:f7a0a04a7bd520cc0e68844eb2a7954bb472f25f9afacbe09e359cad11320c24","git_source")],
  "observation":"The admitted validator sanitizes a custom gateway name and rejects fields incompatible with UDP exposure.","finding":"The bounded source shows positive validation controls, but their completeness, bypass resistance, error behavior, and exploitability context are not established by admitted tests or execution.","corrective":"Retain focused positive, negative, boundary, and bypass tests for the exact validator revision.","preventive":"Map trust-boundary inputs to validation requirements and continuously test failure and bypass paths.","unknown":"Population coverage, generated-code boundaries, bypass behavior, execution-path reachability, and exploitability remain unknown."},
 "SPEC-SECRETS":{"slug":"spec-secrets","display":"Secrets Reviewer","domain":"secrets_revalidation","increment":4,"evidence":[
  ("UDS-0001","docs/getting-started/local-demo/integrate-your-package.mdx",153,"matched value omitted","redacted credential-like detector candidate","sha256:ea1f7e607a6f1afd442316db9ce06f270926fa321e07b8a488de4d45684eda99","external_record")],
  "observation":"The accepted retained route records one redacted credential-like detector candidate with a source path, line, and fingerprint; the matched value is omitted.","finding":"The admitted redacted evidence supports only unresolved_credential_like_value and does not establish a confirmed exposure or benign classification.","corrective":"A restricted qualified reviewer may classify the redacted candidate using separately authorized evidence without distributing the value.","preventive":"Keep detection, classification, rotation, and exposure confirmation separate and irreversibly redact review exports.","unknown":"Secret classification, validity, ownership, age, storage policy, and blast radius remain unknown; no raw value is admitted."}
}

def role_payload(designation:str, refs:list[str])->dict[str,Any]:
 cfg=CONFIG[designation]; unknown={"unknown_id":f"UNKNOWN-{designation.removeprefix('SPEC-')}-001","statement":cfg["unknown"],"missing_evidence":[],"evidence_refs":refs}
 if designation=="SPEC-K8S-WORKLOAD":
  unknown["missing_evidence"]=["admission records","effective policy","runtime pod and identity evidence"]
  return {"designation":designation,"workloads":[{"workload_id":"WORKLOAD-HTTPBIN","service_account":"httpbin","security_context":"least_privilege_declared","resource_controls":"declared","admission_effectiveness":"configured_not_demonstrated","runtime_effectiveness":"not_observed","deployment_readiness":"unable_to_determine","evidence_refs":refs}],"coverage":{"manifests_reviewed":1,"admission_records_reviewed":0,"runtime_records_reviewed":0},"unknowns":[unknown],"authority_boundary":"workload_configuration_only_no_platform_runtime_release_or_product_approval"}
 if designation=="SPEC-K8S-PLATFORM":
  unknown["missing_evidence"]=["live cluster state","enforcement tests","tenant isolation tests"]
  return {"designation":designation,"platform_controls":[{"control_id":"EKS-VPC-CNI-NETWORK-POLICY","desired_state":"declared","observed_state":"not_observed","enforcement_effectiveness":"configured_not_demonstrated","tenant_isolation_confidence":None,"evidence_refs":refs}],"coverage":{"platform_definitions_reviewed":1,"live_clusters_reviewed":0,"enforcement_tests_reviewed":0},"unknowns":[unknown],"authority_boundary":"shared_platform_desired_state_only_no_workload_runtime_release_or_product_approval"}
 if designation=="SPEC-COMMS":
  unknown["missing_evidence"]=["rendered topology","identity and authorization results","traffic tests and telemetry"]
  return {"designation":designation,"topology":{"artifact_ref":refs[3],"completeness":"bounded_declared"},"trust_paths":[{"path_id":"METRICS-API-DEFAULT","protocol":"TCP","mtls_posture":"strict_declared","authorization_coverage":"configured_not_demonstrated","runtime_effectiveness":"not_observed","evidence_refs":[refs[0],refs[3]]},{"path_id":"METRICS-API-10250","protocol":"TCP/10250","mtls_posture":"permissive_exception_declared","authorization_coverage":"unknown","runtime_effectiveness":"not_observed","evidence_refs":[refs[1],refs[3]]},{"path_id":"UDP-EXPOSE","protocol":"UDP","mtls_posture":"not_declared","authorization_coverage":"not_protected_by_declared_control","runtime_effectiveness":"not_observed","evidence_refs":[refs[2],refs[3]]}],"coverage":{"topology_artifacts_reviewed":1,"routes_reviewed":3,"traffic_tests_reviewed":0},"unknowns":[unknown],"authority_boundary":"communication_trust_paths_only_no_platform_workload_release_or_product_approval"}
 if designation=="SPEC-SECURE-CODE":
  unknown["missing_evidence"]=["security tests","execution traces","bypass and exploit evidence"]
  return {"designation":designation,"code_assessments":[{"assessment_id":"CODE-VALIDATION-001","pattern":"input sanitization and protocol-specific incompatible-field rejection","assessment_state":"positive_control_observed","exploitability":"not_assessed","test_support":"not_admitted","evidence_refs":refs}],"coverage":{"source_files_reviewed":1,"security_tests_reviewed":0,"execution_traces_reviewed":0},"unknowns":[unknown],"authority_boundary":"implementation_quality_only_no_architecture_supply_chain_release_or_product_approval"}
 return {"designation":"SPEC-SECRETS","secret_observations":[{"observation_id":"OBS-001","secret_type":"credential-like value","evidence_state":"unresolved_credential_like_value","exposure_location":"docs/getting-started/local-demo/integrate-your-package.mdx:153","owner_role":None,"rotation_policy":None,"age_or_expiry":None,"approved_storage_reference":None,"blast_radius":{},"regulatory_or_policy_impact":[],"evidence_refs":refs,"exposure_root_cause":None}],"measures":{"eligible_coverage":1.0,"confirmed_exposure_count":0,"managed_secret_adoption":None,"rotation_compliance":None,"unresolved_detection_rate":1.0}}

_original_build_manifest=base.build_manifest
_original_locator=base.locator
def build_manifest(designation:str)->dict[str,Any]:
 value=_original_build_manifest(designation)
 value["environment"]["environment_policy_version"]=f"increment-{CONFIG[designation]['increment']}.0.0"
 if designation=="SPEC-SECRETS":
  for item in value["evidence_population"]:
   item.update({"classification":"internal","safe_for_human_review":True,"allowed_reviewer_tracks":["restricted_domain_reviewer","qualified_subject_matter_expert"]})
 value=seal_hash(value,"manifest_hash"); validate_manifest(value); return value

def locator(evidence):
 value=_original_locator(evidence)
 if evidence[0]=="UDS-0001":
  value["redaction"]={"applied":True,"method":"irreversible_value_omission","raw_value_included":False}
  value["line_fingerprint"]="sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca"
  value["access"]={"classification":"internal","constraints":["restricted or qualified reviewer only","raw value access not admitted"],"reviewer_instructions":["Compare this locator with the retained redacted detector record; do not request or reproduce the matched value in the review packet."]}
  value["reproduction_steps"]=["Open the retained redacted calibration slice.","Match evidence ID UDS-0001, source path, line 153, and the detector fingerprint.","Verify that the matched value remains omitted."]
  value=seal_hash(value,"locator_hash")
 return value

def configure() -> None:
 base.CONFIG=CONFIG; base.role_payload=role_payload; base.build_manifest=build_manifest; base.locator=locator
 base.CREATED_AT="2026-08-03T22:00:00Z"; base.GENERATED_AT="2026-08-03T22:05:00Z"
 base.INCREMENT_KEY="increment-34"; base.INCREMENT_LABEL="Increments 3 and 4"
 base.ENVIRONMENT_POLICY_VERSION="increment-3.0.0"; base.LOCATOR_COLLECTOR="increment-34-deterministic-reference"
 base.INCREMENT_SUMMARY=[3,4]

def main()->int:
 configure()
 parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT); args=parser.parse_args()
 summary=base.generate(args.output.resolve()); summary["suite"]="adr0039-increment34-kubernetes-secure-specialists"; summary["human_review_deferred"]=True
 base.atomic_write(args.output.resolve()/"summary.json",base.pretty_bytes(summary))
 print(json.dumps(summary,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())

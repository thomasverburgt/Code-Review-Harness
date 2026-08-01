#!/usr/bin/env python3
"""ADR-0025 fail-closed readiness gate for enterprise shadow integration."""
from __future__ import annotations
import copy,hashlib,uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger,content_hash
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
BASELINE=ROOT/"appendices/example-workflows/vertical-risk-slice.workflow.json";REPORT=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json";NAMESPACE=uuid.UUID("25000000-0000-4000-8000-000000000000");GENERATED_AT="2026-08-02T00:30:00Z"
SOURCES=[
 ("ADR0016-SEMANTIC-ADJUDICATION","external_human_decision","enterprise-risk-acceptance-authority","fixtures/product-synth-admission/evidence/2026-08-01/semantic-adjudication-adr0016/reference-run/semantic-adjudication-packet.json","review_request_only","pending_external_decision","The semantic adjudication packet has no verified external response."),
 ("ADR0020-REQUIREMENTS-ACCEPTANCE","external_human_decision","requirements-acceptance-authority","fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json","review_request_only","pending_external_decision","The requirements acceptance packet has no verified external response."),
 ("ENT-ARCH-LIVE-MULTI-DOMAIN","live_domain_acceptance","architecture-domain-acceptance-authority","fixtures/enterprise-arch-admission/evidence/2026-08-01/adr0021/gx10-live-calibration.tar.gz","protocol_smoke_only","missing_accepted_live_evidence","Retained live evidence proves single-capability protocol handling only."),
 ("ENT-GOV-LIVE-MULTI-DOMAIN","live_domain_acceptance","governance-source-owner","fixtures/enterprise-governance-admission/evidence/2026-08-01/adr0022/gx10-live-calibration.tar.gz","protocol_smoke_only","missing_accepted_live_evidence","Retained live evidence proves single-capability source protocol handling only."),
 ("ENT-STRAT-LIVE-MULTI-DOMAIN","live_domain_acceptance","enterprise-strategy-authority","fixtures/enterprise-strategy-admission/evidence/2026-08-01/adr0023/gx10-live-calibration.tar.gz","protocol_smoke_only","missing_accepted_live_evidence","Retained live evidence proves single-domain objective and method protocol handling only."),
 ("ENT-SYNTH-LIVE-MULTI-DOMAIN","live_domain_acceptance","enterprise-synthesis-acceptance-authority","fixtures/enterprise-synthesis-admission/evidence/2026-08-01/adr0024/gx10-live-calibration.tar.gz","protocol_smoke_only","missing_accepted_live_evidence","Retained live evidence is mixed-tier protocol calibration, not accepted enterprise synthesis."),]
def file_hash(path:Path)->str:return "sha256:"+hashlib.sha256(path.read_bytes()).hexdigest()
def build_manifest()->dict[str,Any]:
 ps=[]
 for pid,cat,auth,rel,tier,state,rationale in SOURCES:
  p=ROOT/rel
  if not p.is_file():raise ValidationFailure(f"readiness prerequisite source missing: {rel}")
  ps.append({"prerequisite_id":pid,"category":cat,"required_authority":auth,"source_path":rel.replace('\\','/'),"source_hash":file_hash(p),"evidence_tier":tier,"state":state,"satisfies_readiness":False,"rationale":rationale})
 m={"manifest_id":str(uuid.uuid5(NAMESPACE,"enterprise-shadow-readiness")),"manifest_version":"1.0.0","generated_at":GENERATED_AT,"scope_id":"ENTERPRISE-FIXTURE-001","prerequisites":ps,"overall_state":"blocked","shadow_scheduled":False,"baseline_route":"ENT-EVIDENCE -> ENT-SYSRISK","rollback":{"disable_candidate_discovery":True,"discard_derived_shadow_state":True,"retain_evidence":True,"baseline_unchanged":True},"decision_authority":"human","manifest_hash":"sha256:"+"0"*64};x=copy.deepcopy(m);x["manifest_hash"]=None;m["manifest_hash"]=content_hash(x);validate_manifest(m);return m
def validate_manifest(m:dict[str,Any])->None:
 assert_schema(m,"enterprise-shadow-readiness-manifest.schema.json","enterprise shadow readiness manifest");x=copy.deepcopy(m);h=x["manifest_hash"];x["manifest_hash"]=None
 if content_hash(x)!=h:raise ValidationFailure("readiness manifest hash mismatch")
 expected={x[0] for x in SOURCES};actual=[x["prerequisite_id"] for x in m["prerequisites"]]
 if len(actual)!=len(set(actual)) or set(actual)!=expected:raise ValidationFailure("readiness prerequisite set mismatch")
 for p in m["prerequisites"]:
  if file_hash(ROOT/p["source_path"])!=p["source_hash"]:raise ValidationFailure("readiness source hash mismatch")
  if p["evidence_tier"]!="accepted_live_multi_domain" and p["satisfies_readiness"]:raise ValidationFailure("non-accepted evidence promoted into readiness")
 ready=all(p["state"]=="accepted_and_verified" and p["evidence_tier"]=="accepted_live_multi_domain" and p["satisfies_readiness"] for p in m["prerequisites"])
 if (m["overall_state"]=="ready_for_shadow_authorization_review")!=ready or m["shadow_scheduled"]:raise ValidationFailure("readiness state or scheduling mismatch")
 if any(n["designation"] in {"ENT-ARCH","ENT-GOV","ENT-STRAT","ENT-SYNTH"} for n in load_json(BASELINE)["nodes"]):raise ValidationFailure("enterprise candidate is unexpectedly scheduled")
def persist_manifest(root:Path,m:dict[str,Any])->dict[str,Any]:return ArtifactLedger(root).persist_record(f"enterprise-shadow-readiness/{m['manifest_id']}.json","enterprise-shadow-readiness",m["manifest_id"],m,retention_class="architecture-evidence")

#!/usr/bin/env python3
"""ADR-0026 authority-separated readiness action dossier."""
from __future__ import annotations
import copy,uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger,content_hash
from enterprise_shadow_readiness_runtime import BASELINE,REPORT,build_manifest,file_hash
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
NAMESPACE=uuid.UUID("26000000-0000-4000-8000-000000000000");GENERATED_AT="2026-08-02T00:45:00Z"
EXISTING={
 "ADR0016-SEMANTIC-ADJUDICATION":("fixtures/product-synth-admission/evidence/2026-08-01/semantic-adjudication-adr0016/reference-run/semantic-adjudication-packet.json","packet_id","packet_hash"),
 "ADR0020-REQUIREMENTS-ACCEPTANCE":("fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json","packet_id","packet_hash"),}
DOMAIN={"ENT-ARCH-LIVE-MULTI-DOMAIN":"ENT-ARCH","ENT-GOV-LIVE-MULTI-DOMAIN":"ENT-GOV","ENT-STRAT-LIVE-MULTI-DOMAIN":"ENT-STRAT","ENT-SYNTH-LIVE-MULTI-DOMAIN":"ENT-SYNTH"}
def hashed(v:dict[str,Any],field:str)->dict[str,Any]:x=copy.deepcopy(v);x[field]=None;v[field]=content_hash(x);return v
def build_domain_packet(readiness:dict[str,Any],p:dict[str,Any])->dict[str,Any]:
 designation=DOMAIN[p["prerequisite_id"]];v={"packet_id":str(uuid.uuid5(NAMESPACE,p["prerequisite_id"])),"packet_version":"1.0.0","generated_at":GENERATED_AT,"readiness_manifest_id":readiness["manifest_id"],"readiness_manifest_hash":readiness["manifest_hash"],"prerequisite_id":p["prerequisite_id"],"designation":designation,"required_authority":p["required_authority"],"current_evidence":{"path":p["source_path"],"content_hash":p["source_hash"],"evidence_tier":"protocol_smoke_only"},"review_state":"not_ready_for_review","missing_requirements":["accepted-live multi-domain input set","independent human semantic evaluation","exact accepted evidence and evaluator-authority bindings"],"accepted_response_allowed":False,"decision_authority":"human","effect":"evidence_gap_notice_only","packet_hash":"sha256:"+"0"*64};hashed(v,"packet_hash");assert_schema(v,"domain-acceptance-packet.schema.json",designation+" packet");return v
def build_dossier()->tuple[dict[str,Any],dict[str,dict[str,Any]]]:
 readiness=build_manifest();packets={};entries=[]
 for p in readiness["prerequisites"]:
  pid=p["prerequisite_id"]
  if pid in EXISTING:
   rel,idf,hf=EXISTING[pid];packet=load_json(ROOT/rel)
   if file_hash(ROOT/rel)!=p["source_hash"]:raise ValidationFailure("existing review packet readiness hash mismatch")
   entry={"prerequisite_id":pid,"required_authority":p["required_authority"],"action_state":"awaiting_external_response","packet_type":"existing_review_packet","packet_id":packet[idf],"packet_hash":packet[hf],"packet_path":rel,"response_must_be_atomic":True,"independent_verification_required":True,"satisfies_readiness":False}
  else:
   packet=build_domain_packet(readiness,p);packets[pid]=packet;rel=f"domain-packets/{p['prerequisite_id'].lower()}.json";entry={"prerequisite_id":pid,"required_authority":p["required_authority"],"action_state":"not_ready_for_review","packet_type":"domain_evidence_gap_packet","packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"packet_path":rel,"response_must_be_atomic":True,"independent_verification_required":True,"satisfies_readiness":False}
  entries.append(entry)
 summary={"total":len(entries),"awaiting_external_response":sum(x["action_state"]=="awaiting_external_response" for x in entries),"not_ready_for_review":sum(x["action_state"]=="not_ready_for_review" for x in entries),"satisfied":0};d={"dossier_id":str(uuid.uuid5(NAMESPACE,readiness["manifest_id"])),"dossier_version":"1.0.0","generated_at":GENERATED_AT,"readiness_manifest_id":readiness["manifest_id"],"readiness_manifest_hash":readiness["manifest_hash"],"entries":entries,"summary":summary,"dossier_approval_allowed":False,"shadow_scheduled":False,"baseline_unchanged":True,"decision_authority":"separate_named_human_authority_per_entry","dossier_hash":"sha256:"+"0"*64};hashed(d,"dossier_hash");validate_dossier(d,packets);return d,packets
def validate_dossier(d:dict[str,Any],packets:dict[str,dict[str,Any]])->None:
 assert_schema(d,"human-readiness-action-dossier.schema.json","human readiness dossier");x=copy.deepcopy(d);h=x["dossier_hash"];x["dossier_hash"]=None
 if content_hash(x)!=h:raise ValidationFailure("dossier hash mismatch")
 readiness=build_manifest()
 if (d["readiness_manifest_id"],d["readiness_manifest_hash"])!=(readiness["manifest_id"],readiness["manifest_hash"]):raise ValidationFailure("dossier readiness binding mismatch")
 expected={x["prerequisite_id"] for x in readiness["prerequisites"]};actual=[x["prerequisite_id"] for x in d["entries"]]
 if len(actual)!=len(set(actual)) or set(actual)!=expected:raise ValidationFailure("dossier entry set mismatch")
 for e in d["entries"]:
  if e["satisfies_readiness"] or not e["response_must_be_atomic"] or not e["independent_verification_required"]:raise ValidationFailure("dossier inferred or bundled authority")
  if e["prerequisite_id"] in DOMAIN:
   p=packets.get(e["prerequisite_id"])
   if not p or p["packet_hash"]!=e["packet_hash"] or p["accepted_response_allowed"]:raise ValidationFailure("domain evidence-gap packet mismatch or premature response")
 if d["summary"]!={"total":6,"awaiting_external_response":2,"not_ready_for_review":4,"satisfied":0}:raise ValidationFailure("dossier summary mismatch")
def render_dossier(d:dict[str,Any])->str:
 lines=["# Enterprise Shadow Readiness — Human Action Dossier","",f"Dossier: `{d['dossier_id']}`  ",f"Dossier hash: `{d['dossier_hash']}`","","**SHADOW INTEGRATION BLOCKED — DOSSIER APPROVAL IS NOT PERMITTED**","",f"Two entries await external responses; four are not ready for review because accepted-live multi-domain evidence is missing.",""]
 for e in d["entries"]:lines += [f"## {e['prerequisite_id']}","",f"- State: `{e['action_state']}`",f"- Required authority: `{e['required_authority']}`",f"- Packet: `{e['packet_path']}`",f"- Packet hash: `{e['packet_hash']}`",f"- Independent verification required: yes",""]
 lines += ["A response applies only to its named entry. No batch signature, dossier approval, project-maintainer statement, or administrative action satisfies another authority's prerequisite.",""];return "\n".join(lines)
def persist_dossier(root:Path,d:dict[str,Any])->dict[str,Any]:return ArtifactLedger(root).persist_record(f"human-readiness-dossier/{d['dossier_id']}.json","human-readiness-action-dossier",d["dossier_id"],d,retention_class="architecture-evidence")

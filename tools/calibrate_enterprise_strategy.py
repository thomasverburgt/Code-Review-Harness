#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from artifact_ledger import atomic_write,pretty_bytes
from enterprise_strategy_runtime import build_candidate,load_manifests,role_template,strategic_inputs
from validate_vertical_slice import ROOT,load_json
from worker_runtime import VLLMAdapter,inline_local_refs,prepare_guided_schema
PROMPT=ROOT/"appendices/prompt-templates/candidates/ent-strat/design-0.1.0.prompt.txt";SCHEMA=ROOT/"appendices/schemas/ent-strat-role.schema.json";MODEL=ROOT/"appendices/model-manifests/gx10-qwen3-32b-ent-strat-calibration-0.1.0.json"
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--base-url",default="http://127.0.0.1:8000");p.add_argument("--api-key-env",default="VLLM_API_KEY");p.add_argument("--timeout-seconds",type=int,default=900);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);objectives,method=load_manifests();gate,arts,obs=strategic_inputs(live=True);required=role_template(gate,arts,obs,objectives,method,live=True);schema=prepare_guided_schema(inline_local_refs(load_json(SCHEMA)),3,256);m=load_json(MODEL);context={"designation":"ENT-STRAT","generation_contract":schema,"strategic_objective_manifest":objectives,"strategic_scoring_method_manifest":method,"evidence_gate":{"artifact_id":gate["artifact"]["artifact_id"],"content_hash":required["manifest_binding"]["gate_artifact_hash"]},"tiered_posture_inputs":obs,"required_result":required};ad=VLLMAdapter(a.base_url,m["model_id"],api_key_env=a.api_key_env,max_tokens=m["max_output_tokens"],disable_thinking=True,use_json_schema=True,guided_array_max_items=m["guided_array_max_items"]);s={"suite":"ent-strat-live-single-domain-objective-method-protocol-calibration","designation":"ENT-STRAT","candidate_status":"candidate","scheduled":False,"evidence_tier":required["evidence_tier"],"fitness_claim":required["fitness_claim"],"composite_score":None,"report_changed":False,"ent_arch_schedule_changed":False,"ent_gov_schedule_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)","passed":False}
 try:
  payload,usage=ad.generate(PROMPT.read_text(encoding="utf-8"),context,a.timeout_seconds)
  if ad.last_response_content is not None:raw=ad.last_response_content.encode();atomic_write(o/"raw-response.json",raw);s["raw_response_sha256"]=hashlib.sha256(raw).hexdigest()
  c=build_candidate(payload,live=True);atomic_write(o/"ent-strat-live-candidate.artifact.json",pretty_bytes(c));atomic_write(o/"strategic-objective-manifest.json",pretty_bytes(objectives));atomic_write(o/"strategic-scoring-method-manifest.json",pretty_bytes(method));s.update({"passed":True,"status":"complete","artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"usage":usage})
 except Exception as e:s.update({"status":"failed_closed","error_type":type(e).__name__,"error":str(e)[:1000]})
 atomic_write(o/"summary.json",pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0 if s["passed"] else 1
if __name__=="__main__":raise SystemExit(main())

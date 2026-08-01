#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from artifact_ledger import atomic_write,pretty_bytes
from enterprise_synthesis_runtime import build_candidate,role_template,synthesis_inputs
from validate_vertical_slice import ROOT,load_json
from worker_runtime import VLLMAdapter,inline_local_refs,prepare_guided_schema
PROMPT=ROOT/"appendices/prompt-templates/candidates/ent-synth/design-0.1.0.prompt.txt";SCHEMA=ROOT/"appendices/schemas/ent-synth-role.schema.json";MODEL=ROOT/"appendices/model-manifests/gx10-qwen3-32b-ent-synth-calibration-0.1.0.json"
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--base-url",default="http://127.0.0.1:8000");p.add_argument("--api-key-env",default="VLLM_API_KEY");p.add_argument("--timeout-seconds",type=int,default=900);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);g,arts,m=synthesis_inputs(live=True);required=role_template(g,arts,m,live=True);schema=prepare_guided_schema(inline_local_refs(load_json(SCHEMA)),4,256);mm=load_json(MODEL);ctx={"designation":"ENT-SYNTH","generation_contract":schema,"synthesis_input_manifest":m,"required_result":required};ad=VLLMAdapter(a.base_url,mm["model_id"],api_key_env=a.api_key_env,max_tokens=mm["max_output_tokens"],disable_thinking=True,use_json_schema=True,guided_array_max_items=mm["guided_array_max_items"]);s={"suite":"ent-synth-live-mixed-tier-protocol-calibration","designation":"ENT-SYNTH","candidate_status":"candidate","scheduled":False,"evidence_tier":required["evidence_tier"],"fitness_claim":required["fitness_claim"],"report_changed":False,"distribution_state_changed":False,"passed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"}
 try:
  payload,usage=ad.generate(PROMPT.read_text(encoding="utf-8"),ctx,a.timeout_seconds)
  if ad.last_response_content is not None:raw=ad.last_response_content.encode();atomic_write(o/"raw-response.json",raw);s["raw_response_sha256"]=hashlib.sha256(raw).hexdigest()
  c=build_candidate(payload,live=True);atomic_write(o/"ent-synth-live-candidate.artifact.json",pretty_bytes(c));atomic_write(o/"synthesis-input-manifest.json",pretty_bytes(m));s.update({"passed":True,"status":"complete","artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"usage":usage})
 except Exception as e:s.update({"status":"failed_closed","error_type":type(e).__name__,"error":str(e)[:1000]})
 atomic_write(o/"summary.json",pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0 if s["passed"] else 1
if __name__=="__main__":raise SystemExit(main())

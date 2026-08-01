#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from artifact_ledger import atomic_write,pretty_bytes
from capability_req_runtime import SOURCE,build_candidate,inputs,role_template
from validate_vertical_slice import ROOT,load_json
from worker_runtime import VLLMAdapter,inline_local_refs,prepare_guided_schema
PROMPT=ROOT/"appendices/prompt-templates/candidates/cap-req/design-0.1.0.prompt.txt";SCHEMA=ROOT/"appendices/schemas/cap-req-role.schema.json";MODEL=ROOT/"appendices/model-manifests/gx10-qwen3-32b-cap-req-calibration-0.1.0.json"
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--base-url",default="http://127.0.0.1:8000");p.add_argument("--api-key-env",default="VLLM_API_KEY");p.add_argument("--timeout-seconds",type=int,default=900);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);source,locator,product=inputs();schema=prepare_guided_schema(inline_local_refs(load_json(SCHEMA)),3,256);m=load_json(MODEL);ctx={"designation":"CAP-REQ","generation_contract":schema,"requirements_source_manifest":source,"evidence_locator":locator,"product_artifact":{"artifact_id":product["artifact"]["artifact_id"],"finding_ids":[x["finding_id"] for x in product["findings"]]},"required_result":{"requirement_records":[],"coverage":{"declared":0,"reviewed":0,"satisfied":0,"partially_satisfied":0,"unsatisfied":0,"unknown":0,"not_reviewed":0,"fraction":None},"acceptance_state":"pending_human_requirements_acceptance"}};ad=VLLMAdapter(a.base_url,m["model_id"],api_key_env=a.api_key_env,max_tokens=m["max_output_tokens"],disable_thinking=True,use_json_schema=True,guided_array_max_items=m["guided_array_max_items"]);s={"suite":"cap-req-live-zero-declared-population-calibration","designation":"CAP-REQ","candidate_status":"candidate","scheduled":False,"acceptance_state":"pending_human_requirements_acceptance","cap_synth_scheduled":False,"report_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)","passed":False}
 try:
  payload,usage=ad.generate(PROMPT.read_text(encoding="utf-8"),ctx,a.timeout_seconds)
  if ad.last_response_content is not None:raw=ad.last_response_content.encode();atomic_write(o/"raw-response.json",raw);s["raw_response_sha256"]=hashlib.sha256(raw).hexdigest()
  c=build_candidate(payload);atomic_write(o/"cap-req-candidate.artifact.json",pretty_bytes(c));atomic_write(o/"requirements-source-manifest.json",pretty_bytes(source));s.update({"passed":True,"status":"complete","artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"declared_requirements":0,"requirement_records":0,"usage":usage})
 except Exception as e:s.update({"status":"failed_closed","error_type":type(e).__name__,"error":str(e)[:1000]})
 atomic_write(o/"summary.json",pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0 if s["passed"] else 1
if __name__=="__main__":raise SystemExit(main())

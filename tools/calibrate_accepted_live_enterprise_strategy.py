#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from accepted_live_enterprise_strategy_runtime import build_package
from artifact_ledger import atomic_write,pretty_bytes
from validate_vertical_slice import ROOT,load_json
from worker_runtime import VLLMAdapter,inline_local_refs,prepare_guided_schema
PROMPT=ROOT/"appendices/prompt-templates/candidates/ent-strat/design-0.1.0.prompt.txt";SCHEMA=ROOT/"appendices/schemas/ent-strat-role.schema.json";MODEL=ROOT/"appendices/model-manifests/gx10-qwen3-32b-ent-strat-multi-domain-evaluation-0.1.0.json"
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--base-url",default="http://127.0.0.1:8000");p.add_argument("--api-key-env",default="VLLM_API_KEY");p.add_argument("--timeout-seconds",type=int,default=900);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True)
 cap,elig,obj,method,evidence,gate,inp,det,_=build_package();schema=prepare_guided_schema(inline_local_refs(load_json(SCHEMA)),8,512);context={"designation":"ENT-STRAT","generation_contract":schema,"project_strategic_objectives":obj,"project_scoring_method":method,"strategy_evidence_bindings":evidence,"cap_synth":{"artifact_id":cap["artifact"]["artifact_id"],"role":cap["extensions"]["capability"]["role"]},"required_result":det["extensions"]["enterprise"]["role"],"constraints":["single capability only","missing locator coverage remains missing","no imputation or composite","comparison only and unscheduled"]};m=load_json(MODEL);ad=VLLMAdapter(a.base_url,m["model_id"],api_key_env=a.api_key_env,max_tokens=m["max_output_tokens"],disable_thinking=True,use_json_schema=True,guided_array_max_items=m["guided_array_max_items"]);s={"suite":"ent-strat-accepted-live-multi-domain-single-capability-evaluation","passed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)","cap_synth_scheduled":False,"ent_strat_scheduled":False,"report_effect":"none","deployment_effect":"none"}
 try:
  payload,usage=ad.generate(PROMPT.read_text(encoding="utf-8"),context,a.timeout_seconds);raw=ad.last_response_content.encode("utf-8");atomic_write(o/"raw-response.json",raw);rh=hashlib.sha256(raw).hexdigest();cap,elig,obj,method,evidence,gate,inp,c,packet=build_package(rh)
  for n,v in (("cap-synth-input.artifact.json",cap),("cap-synth-eligibility.json",elig),("project-strategic-objective-manifest.json",obj),("project-strategic-scoring-method-manifest.json",method),("strategy-evidence-binding-manifest.json",evidence),("ent-evidence-gate.artifact.json",gate),("enterprise-strategy-input-manifest.json",inp),("ent-strat-model-candidate.artifact.json",c),("semantic-review-packet.json",packet)):atomic_write(o/n,pretty_bytes(v))
  s.update({"passed":True,"status":"complete","raw_response_sha256":rh,"artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"semantic_review_packet_id":packet["packet_id"],"semantic_review_packet_hash":packet["packet_hash"],"state":"insufficient_evidence","usage":usage})
 except Exception as e:s.update({"status":"failed_closed","error_type":type(e).__name__,"error":str(e)[:1000]})
 atomic_write(o/"summary.json",pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0 if s["passed"] else 1
if __name__=="__main__":raise SystemExit(main())

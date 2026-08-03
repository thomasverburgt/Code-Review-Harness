#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from artifact_ledger import atomic_write, pretty_bytes
from accepted_live_enterprise_synthesis_runtime import build_candidate, build_gate, build_manifest, build_packet, build_role, load_sources
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema
PROMPT=ROOT/"appendices/prompt-templates/candidates/ent-synth/design-0.1.0.prompt.txt"
SCHEMA=ROOT/"appendices/schemas/ent-synth-role.schema.json"
MODEL=ROOT/"appendices/model-manifests/gx10-qwen3-32b-ent-synth-bounded-domain-evaluation-0.1.0.json"
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,required=True);parser.add_argument("--base-url",default="http://127.0.0.1:8000");parser.add_argument("--api-key-env",default="VLLM_API_KEY");parser.add_argument("--timeout-seconds",type=int,default=900);args=parser.parse_args();output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    artifacts,eligibilities=load_sources();gate=build_gate(artifacts,eligibilities);manifest=build_manifest(gate,artifacts,eligibilities);required=build_role(gate,artifacts,manifest);model=load_json(MODEL);schema=prepare_guided_schema(inline_local_refs(load_json(SCHEMA)),model["guided_array_max_items"],model["guided_string_max_length"])
    context={"designation":"ENT-SYNTH","generation_contract":schema,"exact_input_manifest":manifest,"required_result":required,"instruction":"Return required_result exactly. Do not summarize, omit, normalize, correlate, or add fields."}
    adapter=VLLMAdapter(args.base_url,model["model_id"],api_key_env=args.api_key_env,max_tokens=model["max_output_tokens"],disable_thinking=True,use_json_schema=True,guided_array_max_items=model["guided_array_max_items"])
    summary={"suite":"ent-synth-accepted-live-bounded-domain-evaluation","designation":"ENT-SYNTH","candidate_status":"candidate","scheduled":False,"passed":False,"report_effect":"none","deployment_effect":"none","production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"}
    try:
        payload,usage=adapter.generate(PROMPT.read_text(encoding="utf-8"),context,args.timeout_seconds)
        if payload!=required:raise ValueError("raw ENT-SYNTH response does not exactly preserve the required bounded role")
        raw=adapter.last_response_content.encode();raw_hash=hashlib.sha256(raw).hexdigest();candidate=build_candidate(raw_hash);packet=build_packet(candidate,manifest)
        atomic_write(output/"raw-response.json",raw)
        for name,value in (("ent-synthesis-evidence-gate.json",gate),("enterprise-synthesis-input-manifest.json",manifest),("ent-synth-model-candidate.artifact.json",candidate),("semantic-review-packet.json",packet)):atomic_write(output/name,pretty_bytes(value))
        summary.update({"passed":True,"status":"complete","artifact_id":candidate["artifact"]["artifact_id"],"artifact_hash":candidate["integrity"]["output_hash"],"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"raw_response_sha256":raw_hash,"usage":usage})
    except Exception as error:summary.update({"status":"failed_closed","error_type":type(error).__name__,"error":str(error)[:1000]})
    atomic_write(output/"summary.json",pretty_bytes(summary));print(json.dumps(summary,sort_keys=True));return 0 if summary["passed"] else 1
if __name__=="__main__":raise SystemExit(main())

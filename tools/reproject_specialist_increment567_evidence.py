#!/usr/bin/env python3
"""Re-envelope retained Increment 5-7 raw model role payloads without re-inference."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from artifact_ledger import atomic_write, content_hash, pretty_bytes
import run_specialist_increment567 as increment
from specialist_shadow_calibration_runtime import build_review_packet, stable_uuid, validate_candidate_artifact

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--run",type=Path,required=True); a=p.parse_args(); root=a.run.resolve(); increment.configure(); old=json.loads((root/"summary.json").read_text()); usage={x["designation"]:x["usage"] for x in old["results"]}; results=[]
    for designation,cfg in increment.CONFIG.items():
        target=root/cfg["slug"]; raw=(target/"raw-response.json").read_bytes(); payload=json.loads(raw); raw_hash="sha256:"+hashlib.sha256(raw).hexdigest(); manifest=increment.build_manifest(designation); candidate=increment.base.build_candidate(manifest); candidate["extensions"]["specialist"]["role"]=payload; candidate["execution"].update({"model":"qwen3-32b","generation_mode":"model_role_payload_deterministic_universal_projection"}); candidate["artifact"]["artifact_id"]=stable_uuid(manifest["manifest_id"],raw_hash,"model-candidate"); candidate["integrity"]["output_hash"]=content_hash(payload); validate_candidate_artifact(manifest,candidate); locators=[increment.locator(item) for item in cfg["evidence"]]; packet=build_review_packet(manifest,candidate,locators,increment.base.GENERATED_AT)
        for name,value in (("input-manifest.json",manifest),("model-candidate.artifact.json",candidate),("evidence-locators.json",locators),("human-shadow-review-packet.json",packet)): atomic_write(target/name,pretty_bytes(value))
        result={"designation":designation,"suite":"adr0039-increment567-live-calibration","passed":True,"candidate_status":"candidate","semantic_acceptance":"human_review_deferred","human_review_deferred":True,"scheduled":False,"product_fan_in_eligible":False,"report_eligible":False,"deployment_authorized":False,"a100_production_authorized":False,"test_platform":"GX-10 / approved DGX Spark-equivalent","status":"complete","raw_response_hash":raw_hash,"artifact_id":candidate["artifact"]["artifact_id"],"artifact_hash":content_hash(candidate),"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"usage":usage[designation]}; atomic_write(target/"summary.json",pretty_bytes(result)); results.append(result)
    summary={"suite":"adr0039-increment567-all-specialists","passed":True,"results":results,"human_review_deferred":True,"scheduled":False,"product_fan_in_eligible":False,"report_eligible":False,"deployment_authorized":False,"a100_production_authorized":False}; atomic_write(root/"summary.json",pretty_bytes(summary)); print(json.dumps({"reprojected":len(results),"passed":True},sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())

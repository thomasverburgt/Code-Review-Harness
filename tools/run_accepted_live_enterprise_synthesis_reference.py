#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from artifact_ledger import pretty_bytes
from accepted_live_enterprise_synthesis_runtime import build_package, persist_candidate
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); output=args.output.resolve(); output.mkdir(parents=True,exist_ok=True)
    gate,manifest,candidate,packet=build_package()
    for name,value in (("ent-synthesis-evidence-gate.json",gate),("enterprise-synthesis-input-manifest.json",manifest),("ent-synth-candidate.artifact.json",candidate),("semantic-review-packet.json",packet)):(output/name).write_bytes(pretty_bytes(value))
    ref=persist_candidate(output/"ledger",candidate); summary={"status":"passed","adr":"ADR-0038","artifact_id":candidate["artifact"]["artifact_id"],"artifact_hash":candidate["integrity"]["output_hash"],"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"domain_inputs":4,"ent_synth_scheduled":False,"report_effect":"none","deployment_effect":"none","production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)","ledger_hash":ref["object_hash"]};(output/"summary.json").write_bytes(pretty_bytes(summary));print(json.dumps(summary,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

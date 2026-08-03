#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from accepted_live_enterprise_strategy_runtime import build_package
from artifact_ledger import ArtifactLedger,pretty_bytes
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True)
 cap,elig,obj,method,evidence,gate,inp,c,packet=build_package();items=(("cap-synth-input.artifact.json",cap),("cap-synth-eligibility.json",elig),("project-strategic-objective-manifest.json",obj),("project-strategic-scoring-method-manifest.json",method),("strategy-evidence-binding-manifest.json",evidence),("ent-evidence-gate.artifact.json",gate),("enterprise-strategy-input-manifest.json",inp),("ent-strat-candidate.artifact.json",c),("semantic-review-packet.json",packet))
 for n,v in items:(o/n).write_bytes(pretty_bytes(v))
 ref=ArtifactLedger(o/"ledger").persist_artifact(c);s={"status":"passed","adr":"ADR-0037","artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"state":"insufficient_evidence","cap_synth_scheduled":False,"ent_strat_scheduled":False,"report_effect":"none","deployment_effect":"none","ledger_hash":ref["object_hash"]};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

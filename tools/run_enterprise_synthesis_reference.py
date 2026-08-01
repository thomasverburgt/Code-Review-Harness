#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import ArtifactLedger,pretty_bytes
from enterprise_synthesis_runtime import build_candidate,synthesis_inputs
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);g,arts,m=synthesis_inputs();c=build_candidate();
 for n,v in [("synthesis-input-manifest.json",m),("ent-evidence-input.artifact.json",g),("ent-synth-candidate.artifact.json",c)]:(o/n).write_bytes(pretty_bytes(v))
 ref=ArtifactLedger(o/"ledger").persist_artifact(c);r=c["extensions"]["enterprise"]["role"];s={"status":"passed","adr":"ADR-0024","designation":"ENT-SYNTH","candidate_status":"candidate","scheduled":False,"evidence_tier":r["evidence_tier"],"fitness_claim":r["fitness_claim"],"domain_inputs":len(arts),"artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"ledger_hash":ref["object_hash"],"report_changed":False,"distribution_state_changed":False,"candidate_schedules_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

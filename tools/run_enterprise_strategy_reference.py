#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import ArtifactLedger,pretty_bytes
from enterprise_strategy_runtime import build_candidate,load_manifests,strategic_inputs
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);objectives,method=load_manifests();gate,arts,obs=strategic_inputs();c=build_candidate()
 for name,value in [("strategic-objective-manifest.json",objectives),("strategic-scoring-method-manifest.json",method),("ent-evidence-input.artifact.json",gate),("ent-strat-candidate.artifact.json",c)]:(o/name).write_bytes(pretty_bytes(value))
 ref=ArtifactLedger(o/"ledger").persist_artifact(c);r=c["extensions"]["enterprise"]["role"];s={"status":"passed","adr":"ADR-0023","designation":"ENT-STRAT","candidate_status":"candidate","scheduled":False,"evidence_tier":r["evidence_tier"],"fitness_claim":r["fitness_claim"],"posture_inputs":len(obs),"composite_score":None,"artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"ledger_hash":ref["object_hash"],"baseline_changed":False,"report_changed":False,"ent_arch_schedule_changed":False,"ent_gov_schedule_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

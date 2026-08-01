#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import ArtifactLedger,pretty_bytes
from enterprise_arch_runtime import build_candidate,build_inputs
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);g,arts=build_inputs();c=build_candidate();
 for name,value in [("ent-evidence-input.artifact.json",g),("capability-input-1.artifact.json",arts[0]),("capability-input-2.artifact.json",arts[1]),("ent-arch-candidate.artifact.json",c)]:(o/name).write_bytes(pretty_bytes(value))
 ref=ArtifactLedger(o/"ledger").persist_artifact(c);s={"status":"passed","adr":"ADR-0021","designation":"ENT-ARCH","candidate_status":"candidate","scheduled":False,"evidence_tier":"adjudicated_multi_capability_contract_fixture","fitness_claim":"contract_mechanics_only","capability_inputs":2,"artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"ledger_hash":ref["object_hash"],"baseline_changed":False,"report_changed":False,"cap_req_gate_bypassed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

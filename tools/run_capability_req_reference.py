#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import ArtifactLedger,pretty_bytes
from capability_req_runtime import SOURCE,build_candidate,inputs
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);source,locator,product=inputs();c=build_candidate();
 for name,value in (("requirements-source-manifest.json",source),("evidence-locator.json",locator),("prod-sec-input.artifact.json",product),("cap-req-candidate.artifact.json",c)):(o/name).write_bytes(pretty_bytes(value))
 ref=ArtifactLedger(o/"ledger").persist_artifact(c);s={"status":"passed","adr":"ADR-0019","designation":"CAP-REQ","candidate_status":"candidate","scheduled":False,"declared_requirements":0,"requirement_records":0,"traceability_gap":"GAP-REQ-001","acceptance_state":"pending_human_requirements_acceptance","artifact_id":c["artifact"]["artifact_id"],"artifact_hash":c["integrity"]["output_hash"],"ledger_hash":ref["object_hash"],"cap_coord_compatible":True,"cap_synth_scheduled":False,"report_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

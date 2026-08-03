#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from artifact_ledger import pretty_bytes
from enterprise_synthesis_semantic_acceptance_runtime import build_records,persist_records
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);d,f,e=build_records()
 for n,v in (("semantic-disposition.json",d),("project-owner-finalization.json",f),("enterprise-shadow-integration-eligibility.json",e)):(o/n).write_bytes(pretty_bytes(v))
 refs=persist_records(o/"ledger",d,f,e);s={"status":"owner_finalized","adr":"ADR-0038","disposition":d["disposition"],"disposition_id":d["disposition_id"],"disposition_hash":d["disposition_hash"],"finalization_id":f["finalization_id"],"finalization_hash":f["finalization_hash"],"eligibility_id":e["eligibility_id"],"eligibility_hash":e["record_hash"],"eligibility_state":e["state"],"boundaries_carried_forward":e["boundaries_carried_forward"],"ent_synth_scheduled":False,"report_effect":"none","deployment_effect":"none","ledger_hashes":[x["object_hash"] for x in refs]};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

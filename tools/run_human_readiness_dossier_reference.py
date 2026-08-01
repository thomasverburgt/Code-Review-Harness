#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import pretty_bytes
from human_readiness_dossier_runtime import build_dossier,persist_dossier,render_dossier
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);d,packets=build_dossier();(o/"human-readiness-action-dossier.json").write_bytes(pretty_bytes(d));(o/"human-readiness-action-dossier.md").write_text(render_dossier(d),encoding="utf-8")
 for pid,v in packets.items():path=o/"domain-packets"/(pid.lower()+".json");path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(pretty_bytes(v))
 ref=persist_dossier(o/"ledger",d);s={"status":"blocked_actionable","adr":"ADR-0026","entries":6,"awaiting_external_response":2,"not_ready_for_review":4,"satisfied":0,"dossier_id":d["dossier_id"],"dossier_hash":d["dossier_hash"],"ledger_hash":ref["object_hash"],"shadow_scheduled":False,"baseline_changed":False,"report_changed":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)"};(o/"summary.json").write_bytes(pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

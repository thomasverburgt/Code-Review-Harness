#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from artifact_ledger import atomic_write,pretty_bytes
from requirements_acceptance_runtime import build_packet,persist_packet,render_review
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args();o=a.output.resolve();o.mkdir(parents=True,exist_ok=True);packet=build_packet();ref=persist_packet(o/"ledger",packet);atomic_write(o/"requirements-acceptance-packet.json",pretty_bytes(packet));atomic_write(o/"requirements-acceptance-review.md",render_review(packet).encode("utf-8"));s={"status":"awaiting_external_requirements_acceptance","adr":"ADR-0020","packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"artifact_id":packet["cap_req_artifact"]["artifact_id"],"artifact_hash":packet["cap_req_artifact"]["content_hash"],"required_authority":packet["required_authority"],"effect":packet["effect"],"eligibility_state":packet["eligibility_state"],"cap_synth_scheduled":False,"production_target":"A100 large cluster","test_platform":"DGX Spark or approved equivalent (GX-10)","ledger_ref":ref};atomic_write(o/"summary.json",pretty_bytes(s));print(json.dumps(s,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

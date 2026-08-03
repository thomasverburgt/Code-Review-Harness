#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from artifact_ledger import atomic_write, pretty_bytes
from accepted_live_enterprise_synthesis_runtime import build_candidate, build_manifest, build_packet
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--run",type=Path,required=True);args=parser.parse_args();run=args.run.resolve();raw_path=run/"raw-response.json";raw_bytes=raw_path.read_bytes();raw=json.loads(raw_bytes);candidate=build_candidate(hashlib.sha256(raw_bytes).hexdigest())
    if raw!=candidate["extensions"]["enterprise"]["role"]:raise ValueError("retained raw response no longer equals the authoritative role projection")
    manifest=build_manifest();packet=build_packet(candidate,manifest)
    atomic_write(run/"ent-synth-model-candidate.artifact.json",pretty_bytes(candidate));atomic_write(run/"semantic-review-packet.json",pretty_bytes(packet))
    summary=json.loads((run/"summary.json").read_text());summary.update({"artifact_id":candidate["artifact"]["artifact_id"],"artifact_hash":candidate["integrity"]["output_hash"],"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"reprojected_from_retained_raw":True,"raw_response_sha256":hashlib.sha256(raw_bytes).hexdigest()});atomic_write(run/"summary.json",pretty_bytes(summary));print(json.dumps(summary,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())

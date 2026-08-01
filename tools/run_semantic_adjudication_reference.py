#!/usr/bin/env python3
"""Materialize the proposed ADR-0016 semantic review packet."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from artifact_ledger import atomic_write, pretty_bytes
from semantic_adjudication_runtime import build_packet, persist_packet, render_review

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    packet = build_packet(); ref = persist_packet(output / "ledger", packet)
    atomic_write(output / "semantic-adjudication-packet.json", pretty_bytes(packet))
    atomic_write(output / "semantic-adjudication-review.md", render_review(packet).encode("utf-8"))
    summary = {"status": "awaiting_human_adjudication", "packet_id": packet["packet_id"], "packet_hash": packet["packet_hash"],
               "delta_count": len(packet["deltas"]), "required_decision_authority": packet["required_decision_authority"],
               "effect": packet["effect"], "cutover_state": packet["cutover_state"], "ledger_ref": ref}
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())

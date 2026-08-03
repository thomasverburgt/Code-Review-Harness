#!/usr/bin/env python3
"""Materialize the exact ADR-0035 project-owner semantic disposition records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_ledger import pretty_bytes
from enterprise_arch_semantic_acceptance_runtime import build_records, persist_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    disposition, finalization, eligibility = build_records()
    for name, value in (("semantic-disposition.json", disposition), ("project-owner-finalization.json", finalization),
                        ("enterprise-synthesis-evaluation-eligibility.json", eligibility)):
        (output / name).write_bytes(pretty_bytes(value))
    refs = persist_records(output / "ledger", disposition, finalization, eligibility)
    summary = {"status": "owner_finalized", "adr": "ADR-0035", "disposition": disposition["disposition"],
               "disposition_id": disposition["disposition_id"], "disposition_hash": disposition["disposition_hash"],
               "finalization_id": finalization["finalization_id"], "finalization_hash": finalization["finalization_hash"],
               "eligibility_id": eligibility["eligibility_id"], "eligibility_hash": eligibility["record_hash"],
               "eligibility_state": eligibility["state"], "ent_arch_scheduled": False, "ent_synth_scheduled": False,
               "report_effect": "none", "deployment_effect": "none", "ledger_hashes": [item["object_hash"] for item in refs]}
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

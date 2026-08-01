#!/usr/bin/env python3
"""Materialize the deterministic PROD-SYNTH candidate-admission reference package."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from artifact_ledger import pretty_bytes
from test_product_synth_admission import CAP_RISK, GOLD, PROD_SEC, validate_candidate
from validate_vertical_slice import assert_schema, load_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    candidate = load_json(GOLD)
    child = load_json(PROD_SEC)
    validate_candidate(candidate)
    handoff = candidate["extensions"]["product"]["role"]["capability_handoff"]
    finding = child["findings"][0]
    adapted = copy.deepcopy(load_json(CAP_RISK))
    adapted["artifact"]["links"]["children"] = [candidate["artifact"]["artifact_id"]]
    adapted["inputs"] = [{"artifact_id": candidate["artifact"]["artifact_id"], "hash": candidate["integrity"]["output_hash"], "compatibility": "compatible", "freshness": "fresh"}]
    adapted["extensions"]["capability"]["role"]["risk_provenance"][0]["artifact_ids"] = [candidate["artifact"]["artifact_id"]]
    assert_schema(adapted, "universal-agent-artifact.schema.json", "adapted CAP-RISK artifact")
    assert_schema(adapted["extensions"]["capability"], "capability-extension.schema.json", "adapted capability extension")
    assert_schema(adapted["extensions"]["capability"]["role"], "cap-risk-role.schema.json", "adapted CAP-RISK role")
    (output / "prod-synth-candidate.artifact.json").write_bytes(pretty_bytes(candidate))
    (output / "cap-risk-compatible-handoff.artifact.json").write_bytes(pretty_bytes(adapted))
    summary = {"status": "passed", "candidate_status": "candidate", "scheduled": False,
               "prod_synth_artifact_id": candidate["artifact"]["artifact_id"],
               "child_artifact_id": child["artifact"]["artifact_id"],
               "preserved_finding_id": finding["finding_id"],
               "preserved_evidence_refs": finding["evidence_refs"],
               "handoff_state": handoff["handoff_state"],
               "capability_consumer": "CAP-RISK", "decision_authority": candidate["decision_authority"],
               "baseline_workflow_changed": False}
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


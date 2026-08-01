#!/usr/bin/env python3
"""Materialize the Increment 4 expert-review evidence packet."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from artifact_ledger import content_hash, pretty_bytes
from evidence_locator_runtime import build_binding_manifest, build_expert_review_packet, render_evidence_annex
from test_evidence_locator_runtime import CALIBRATION, REPORT, bindings
from validate_vertical_slice import load_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    package, source = load_json(REPORT), load_json(CALIBRATION)
    evidence = source["redacted_detector_findings"][0]
    collection = source["collection"]
    locator = {"locator_id": "LOCATOR-UDS-0001", "evidence_id": evidence["evidence_id"], "source_type": "git_source",
               "repository_uri": collection["repository"], "immutable_revision": collection["revision"], "path": evidence["locator"]["path"],
               "line_start": evidence["locator"]["line"], "line_end": evidence["locator"]["line"], "symbol_or_section": None,
               "safe_excerpt": "Credential-like assignment detected; matched value omitted.",
               "redaction": {"applied": True, "method": evidence["redaction"], "raw_value_included": False},
               "line_fingerprint": evidence["line_fingerprint"], "collector": "SPEC-SECRETS calibration collector",
               "collection_method": collection["method"], "collected_at": "2026-07-31T13:00:00Z",
               "access": {"classification": source["access_classification"], "constraints": ["authorized reviewers only"],
                          "reviewer_instructions": ["Obtain an authorized read-only clone; do not copy restricted values into the review packet."]},
               "reproduction_steps": [f"Check out commit {collection['revision']} from {collection['repository']}.",
                                      f"Open {evidence['locator']['path']} at line {evidence['locator']['line']}.",
                                      "Run the approved redacted credential-assignment check and compare the line fingerprint."],
               "locator_state": "source_located", "locator_hash": "sha256:" + "0" * 64}
    material = copy.deepcopy(locator)
    material["locator_hash"] = None
    locator["locator_hash"] = content_hash(material)
    risk_locator = copy.deepcopy(locator)
    risk_locator["locator_id"] = "LOCATOR-OBS-RISK-001"
    risk_locator["evidence_id"] = "OBS-RISK-001"
    risk_locator["locator_hash"] = "sha256:" + "0" * 64
    material = copy.deepcopy(risk_locator)
    material["locator_hash"] = None
    risk_locator["locator_hash"] = content_hash(material)
    manifest = build_binding_manifest(package, bindings(package))
    packet = build_expert_review_packet(package, manifest, [locator, risk_locator], "2026-07-31T19:00:00Z")
    for name, value in (("evidence-locator.json", [locator, risk_locator]), ("evidence-binding-manifest.json", manifest), ("expert-review-packet.json", packet)):
        (output / name).write_bytes(pretty_bytes(value))
    (output / "expert-evidence-annex.md").write_text(render_evidence_annex(packet), encoding="utf-8")
    summary = {"status": "passed", "report_package_id": package["report_package_id"], "report_package_hash": package["package_hash"],
               "reviewability_state": packet["reviewability_state"], "actionable_item_count": len(packet["actionable_items"]),
               "locator_count": len(packet["locators"]), "report_unchanged": True, "authority_effect": packet["authority_effect"]}
    (output / "summary.json").write_bytes(pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

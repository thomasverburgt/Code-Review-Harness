#!/usr/bin/env python3
"""Materialize deterministic ADR-0015 shadow comparison evidence."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from artifact_ledger import atomic_write, pretty_bytes
from shadow_product_synth_runtime import assert_no_publication_target, build_shadow_cap_risk, compare_paths, persist_shadow
from validate_vertical_slice import ROOT, load_json

BASELINE = ROOT / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-cap-risk.artifact.json"
PROD_SYNTH = ROOT / "fixtures/product-synth-admission/evidence/2026-07-31/live-calibration/accepted-prod-synth.artifact.json"
BASELINE_WORKFLOW = ROOT / "appendices/example-workflows/vertical-risk-slice.workflow.json"
REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"

def file_sha(path: Path) -> str: return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--platform", default="local-deterministic-reference")
    args = parser.parse_args(); output = args.output.resolve(); assert_no_publication_target(output); output.mkdir(parents=True, exist_ok=True)
    workflow_before, report_before = file_sha(BASELINE_WORKFLOW), file_sha(REPORT)
    baseline, product = load_json(BASELINE), load_json(PROD_SYNTH)
    shadow = build_shadow_cap_risk(baseline, product); comparison = compare_paths(baseline, product, shadow, platform=args.platform)
    refs = persist_shadow(output / "ledger-shadow", shadow, comparison)
    atomic_write(output / "shadow-cap-risk.artifact.json", pretty_bytes(shadow)); atomic_write(output / "shadow-path-comparison.json", pretty_bytes(comparison))
    summary = {"status": "passed" if comparison["overall_state"] != "blocked" else "blocked", "workflow_id": comparison["workflow_id"],
               "comparison_id": comparison["comparison_id"], "shadow_cap_risk_artifact_id": shadow["artifact"]["artifact_id"],
               "semantic_state": comparison["overall_state"], "authority_effect": "comparison_only", "ledger_namespace": "shadow/adr-0015",
               "baseline_workflow_hash_before": workflow_before, "baseline_workflow_hash_after": file_sha(BASELINE_WORKFLOW),
               "report_hash_before": report_before, "report_hash_after": file_sha(REPORT), "ledger_refs": refs}
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"] == "passed" else 1

if __name__ == "__main__": raise SystemExit(main())

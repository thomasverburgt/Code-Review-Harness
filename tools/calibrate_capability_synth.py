#!/usr/bin/env python3
"""Run isolated CAP-SYNTH live protocol/lineage calibration on accepted CAP-RISK."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from artifact_ledger import atomic_write, pretty_bytes
from capability_coordination_runtime import ACCEPTED_CAP_RISK, build_manifest
from capability_synth_runtime import assemble_model_candidate
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema


PROMPT = ROOT / "appendices/prompt-templates/candidates/cap-synth/design-0.1.0.prompt.txt"
ROLE_SCHEMA = ROOT / "appendices/schemas/cap-synth-role.schema.json"
MODEL_MANIFEST = ROOT / "appendices/model-manifests/gx10-qwen3-32b-cap-synth-calibration-0.1.0.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    artifact = load_json(ACCEPTED_CAP_RISK)
    manifest = build_manifest([artifact], ["CAP-RISK"])
    schema = prepare_guided_schema(inline_local_refs(load_json(ROLE_SCHEMA)), 4, 256)
    required_preserved = [{"source_artifact_id": item["source_artifact_id"], "source_record_id": item["record_id"],
                           "record_kind": item["record_kind"], "evidence_refs": item["evidence_refs"],
                           "preservation_state": "preserved_without_rewrite"} for item in manifest["traceability"]]
    context = {"designation": "CAP-SYNTH", "evidence_tier": "accepted_live_input_calibration",
               "fitness_claim": "protocol_lineage_smoke_only", "generation_contract": schema,
               "coordinator_manifest": manifest, "required_preserved_assertions": required_preserved,
               "constraints": ["derived_capability_assertions must be empty because only one domain is present",
                               "copy required_preserved_assertions exactly", "comparison only", "human authority"]}
    model = load_json(MODEL_MANIFEST)
    adapter = VLLMAdapter(args.base_url, model["model_id"], api_key_env=args.api_key_env,
                          max_tokens=model["max_output_tokens"], disable_thinking=True, use_json_schema=True,
                          guided_array_max_items=model["guided_array_max_items"])
    summary = {"suite": "cap-synth-live-single-domain-protocol-calibration", "designation": "CAP-SYNTH",
               "candidate_status": "candidate", "scheduled": False, "evidence_tier": "accepted_live_input_calibration",
               "fitness_claim": "protocol_lineage_smoke_only", "baseline_workflow_changed": False,
               "report_changed": False, "production_target": "A100 large cluster",
               "test_platform": "DGX Spark or approved equivalent (GX-10)", "passed": False}
    try:
        payload, usage = adapter.generate(PROMPT.read_text(encoding="utf-8"), context, args.timeout_seconds)
        if adapter.last_response_content is not None:
            raw = adapter.last_response_content.encode("utf-8")
            atomic_write(output / "raw-response.json", raw)
            summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        candidate = assemble_model_candidate(payload, manifest, [artifact])
        atomic_write(output / "accepted-cap-synth-smoke.artifact.json", pretty_bytes(candidate))
        atomic_write(output / "capability-input-manifest.json", pretty_bytes(manifest))
        summary.update({"passed": True, "status": "complete", "artifact_id": candidate["artifact"]["artifact_id"],
                        "artifact_hash": candidate["integrity"]["output_hash"], "usage": usage})
    except Exception as exc:
        summary.update({"status": "failed_closed", "error_type": type(exc).__name__, "error": str(exc)[:1000]})
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

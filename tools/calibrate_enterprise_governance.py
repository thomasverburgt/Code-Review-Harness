#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from artifact_ledger import atomic_write, pretty_bytes
from enterprise_arch_runtime import build_inputs
from enterprise_governance_runtime import build_candidate, load_source, role_template
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema

PROMPT = ROOT / "appendices/prompt-templates/candidates/ent-gov/design-0.1.0.prompt.txt"
SCHEMA = ROOT / "appendices/schemas/ent-gov-role.schema.json"
MODEL = ROOT / "appendices/model-manifests/gx10-qwen3-32b-ent-gov-calibration-0.1.0.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    source = load_source()
    gate, artifacts = build_inputs(live=True)
    required = role_template(gate, artifacts, source, live=True)
    schema = prepare_guided_schema(inline_local_refs(load_json(SCHEMA)), 3, 256)
    model = load_json(MODEL)
    context = {
        "designation": "ENT-GOV",
        "generation_contract": schema,
        "governance_source_manifest": source,
        "ent_evidence_manifest": {
            "artifact_id": gate["artifact"]["artifact_id"],
            "content_hash": required["manifest_binding"]["gate_artifact_hash"],
        },
        "capability_artifacts": [
            {
                "artifact_id": artifact["artifact"]["artifact_id"],
                "content_hash": digest,
                "capability_id": artifact["extensions"]["capability"]["capability_id"],
                "finding_ids": [finding["finding_id"] for finding in artifact["findings"]],
            }
            for artifact, digest in zip(
                artifacts, required["manifest_binding"]["capability_artifact_hashes"]
            )
        ],
        "required_result": required,
    }
    adapter = VLLMAdapter(
        args.base_url,
        model["model_id"],
        api_key_env=args.api_key_env,
        max_tokens=model["max_output_tokens"],
        disable_thinking=True,
        use_json_schema=True,
        guided_array_max_items=model["guided_array_max_items"],
    )
    summary = {
        "suite": "ent-gov-live-single-capability-source-protocol-calibration",
        "designation": "ENT-GOV",
        "candidate_status": "candidate",
        "scheduled": False,
        "evidence_tier": required["evidence_tier"],
        "fitness_claim": required["fitness_claim"],
        "report_changed": False,
        "cap_req_gate_bypassed": False,
        "ent_arch_schedule_changed": False,
        "production_target": "A100 large cluster",
        "test_platform": "DGX Spark or approved equivalent (GX-10)",
        "passed": False,
    }
    try:
        payload, usage = adapter.generate(
            PROMPT.read_text(encoding="utf-8"), context, args.timeout_seconds
        )
        if adapter.last_response_content is not None:
            raw = adapter.last_response_content.encode()
            atomic_write(output / "raw-response.json", raw)
            summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        candidate = build_candidate(payload, live=True)
        atomic_write(output / "ent-gov-live-candidate.artifact.json", pretty_bytes(candidate))
        atomic_write(output / "governance-source-manifest.json", pretty_bytes(source))
        atomic_write(output / "ent-evidence-input.artifact.json", pretty_bytes(gate))
        summary.update(
            {
                "passed": True,
                "status": "complete",
                "artifact_id": candidate["artifact"]["artifact_id"],
                "artifact_hash": candidate["integrity"]["output_hash"],
                "matrix_rows": len(
                    candidate["extensions"]["enterprise"]["role"]["compliance_matrix"]
                ),
                "usage": usage,
            }
        )
    except Exception as exc:
        summary.update(
            {
                "status": "failed_closed",
                "error_type": type(exc).__name__,
                "error": str(exc)[:1000],
            }
        )
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

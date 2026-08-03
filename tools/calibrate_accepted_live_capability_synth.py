#!/usr/bin/env python3
"""Run ADR-0034 isolated Qwen3-32B accepted-live multi-domain evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from accepted_live_capability_synth_runtime import build_accepted_live_package, build_enterprise_compatibility, build_semantic_review_packet
from artifact_ledger import atomic_write, pretty_bytes
from capability_synth_runtime import assemble_model_candidate
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema


PROMPT = ROOT / "appendices/prompt-templates/candidates/cap-synth/design-0.1.0.prompt.txt"
ROLE_SCHEMA = ROOT / "appendices/schemas/cap-synth-role.schema.json"
MODEL_MANIFEST = ROOT / "appendices/model-manifests/gx10-qwen3-32b-cap-synth-multi-domain-evaluation-0.1.0.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    artifacts, eligibility, manifest, deterministic, _, _ = build_accepted_live_package()
    schema = prepare_guided_schema(inline_local_refs(load_json(ROLE_SCHEMA)), 16, 512)
    required_preserved = deterministic["extensions"]["capability"]["role"]["preserved_child_assertions"]
    context = {
        "designation": "CAP-SYNTH", "evidence_tier": "accepted_live_multi_domain_candidate_evaluation",
        "fitness_claim": "multi_domain_candidate_evaluation", "generation_contract": schema,
        "coordinator_manifest": manifest, "input_artifacts": artifacts,
        "cap_req_eligibility": eligibility, "required_preserved_assertions": required_preserved,
        "constraints": ["copy required_preserved_assertions exactly",
                        "emit at least one derived assertion citing both real input artifact IDs and at least two real preserved record IDs",
                        "zero declared requirements remains unassessable and must never be represented as satisfied or covered",
                        "preserve conflicts, unknowns, decision requests, evidence references, and confidence provenance",
                        "enterprise handoff is comparison only", "decision authority remains human",
                        "do not authorize scheduling, reports, deployment, or A100 production"],
    }
    model = load_json(MODEL_MANIFEST)
    adapter = VLLMAdapter(args.base_url, model["model_id"], api_key_env=args.api_key_env,
                          max_tokens=model["max_output_tokens"], disable_thinking=True, use_json_schema=True,
                          guided_array_max_items=model["guided_array_max_items"])
    summary = {"suite": "cap-synth-accepted-live-multi-domain-evaluation", "designation": "CAP-SYNTH",
               "candidate_status": "candidate", "scheduled": False,
               "semantic_acceptance": "awaiting_project_owner_review",
               "evidence_tier": "accepted_live_multi_domain_candidate_evaluation",
               "fitness_claim": "multi_domain_candidate_evaluation", "baseline_workflow_changed": False,
               "report_changed": False, "deployment_effect": "none", "production_target": "A100 large cluster",
               "test_platform": "DGX Spark or approved equivalent (GX-10)", "passed": False}
    try:
        payload, usage = adapter.generate(PROMPT.read_text(encoding="utf-8"), context, args.timeout_seconds)
        if adapter.last_response_content is not None:
            raw = adapter.last_response_content.encode("utf-8")
            atomic_write(output / "raw-response.json", raw)
            summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        candidate = assemble_model_candidate(payload, manifest, artifacts,
                                             evidence_tier="accepted_live_multi_domain_candidate_evaluation")
        compatibility = build_enterprise_compatibility(candidate)
        review = build_semantic_review_packet(candidate, manifest, eligibility)
        for artifact in artifacts:
            atomic_write(output / f"{artifact['identity']['designation'].lower()}-input.artifact.json", pretty_bytes(artifact))
        for name, value in (("requirements-eligibility-record.json", eligibility),
                            ("capability-input-manifest.json", manifest),
                            ("cap-synth-model-candidate.artifact.json", candidate),
                            ("enterprise-compatibility.json", compatibility),
                            ("semantic-review-packet.json", review)):
            atomic_write(output / name, pretty_bytes(value))
        summary.update({"passed": True, "status": "complete", "artifact_id": candidate["artifact"]["artifact_id"],
                        "artifact_hash": candidate["integrity"]["output_hash"],
                        "semantic_review_packet_id": review["packet_id"],
                        "semantic_review_packet_hash": review["packet_hash"], "usage": usage})
    except Exception as exc:
        summary.update({"status": "failed_closed", "error_type": type(exc).__name__, "error": str(exc)[:1000]})
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

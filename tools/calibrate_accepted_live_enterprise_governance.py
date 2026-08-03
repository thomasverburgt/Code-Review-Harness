#!/usr/bin/env python3
"""Run ADR-0036 isolated Qwen3-32B ENT-GOV evaluation on GX-10."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from accepted_live_enterprise_governance_runtime import build_candidate, build_compatibility, build_package, build_review_packet
from artifact_ledger import atomic_write, pretty_bytes
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema


PROMPT = ROOT / "appendices/prompt-templates/candidates/ent-gov/design-0.1.0.prompt.txt"
SCHEMA = ROOT / "appendices/schemas/ent-gov-role.schema.json"
MODEL = ROOT / "appendices/model-manifests/gx10-qwen3-32b-ent-gov-multi-domain-evaluation-0.1.0.json"


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000"); parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--raw-response", type=Path, help="Reproject a retained model role without invoking the model")
    parser.add_argument("--timeout-seconds", type=int, default=900); args = parser.parse_args(); output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    source, eligibility, governance, evidence, gate, manifest, deterministic, _, _ = build_package(); expected = deterministic["extensions"]["enterprise"]["role"]
    schema = prepare_guided_schema(inline_local_refs(load_json(SCHEMA)), 8, 512)
    context = {"designation": "ENT-GOV", "evidence_tier": expected["evidence_tier"], "fitness_claim": expected["fitness_claim"], "generation_contract": schema,
        "required_manifest_binding": expected["manifest_binding"], "required_governance_baseline": expected["governance_baseline"],
        "owner_governance_source_manifest": governance, "governance_evidence_binding_manifest": evidence,
        "cap_synth_input": {"artifact_id": source["artifact"]["artifact_id"],
            "capability_id": source["extensions"]["capability"]["capability_id"], "role": source["extensions"]["capability"]["role"]},
        "anti_double_counting": manifest,
        "constraints": ["CAP-SYNTH is the only capability input", "CAP-RISK and CAP-REQ children are lineage only", "exactly one compliance row is required",
            "the row must remain insufficient_evidence", "cite only locator IDs in the governance evidence binding manifest", "do not invent exceptions or approvals",
            "governance maturity must remain insufficient_evidence and advisory only", "comparison only; no scheduling, compliance approval, exception, report, deployment, or production authority"]}
    model = load_json(MODEL); adapter = VLLMAdapter(args.base_url, model["model_id"], api_key_env=args.api_key_env, max_tokens=model["max_output_tokens"], disable_thinking=True, use_json_schema=True, guided_array_max_items=model["guided_array_max_items"])
    summary = {"suite": "ent-gov-accepted-live-multi-domain-single-capability-evaluation", "designation": "ENT-GOV", "candidate_status": "candidate",
        "semantic_acceptance": "awaiting_project_owner_review", "evidence_tier": expected["evidence_tier"], "fitness_claim": expected["fitness_claim"],
        "anti_double_counting": manifest["anti_double_counting"], "cap_synth_scheduled": False, "ent_gov_scheduled": False,
        "report_effect": "none", "deployment_effect": "none", "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)", "passed": False}
    try:
        if args.raw_response is not None:
            raw = args.raw_response.read_bytes(); payload = json.loads(raw.decode("utf-8")); usage = {"mode": "retained_response_reprojection", "model_invoked": False}
            atomic_write(output / "raw-response.json", raw); summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        else:
            payload, usage = adapter.generate(PROMPT.read_text(encoding="utf-8"), context, args.timeout_seconds)
            if adapter.last_response_content is not None:
                raw = adapter.last_response_content.encode("utf-8"); atomic_write(output / "raw-response.json", raw); summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        candidate = build_candidate(gate, source, eligibility, governance, evidence, manifest, payload, summary["raw_response_sha256"]); compatibility = build_compatibility(candidate); review = build_review_packet(candidate, manifest, eligibility, governance, evidence)
        for name, value in (("cap-synth-input.artifact.json", source), ("cap-synth-eligibility.json", eligibility), ("owner-governance-source-manifest.json", governance), ("governance-evidence-binding-manifest.json", evidence),
            ("ent-evidence-gate.artifact.json", gate), ("enterprise-governance-input-manifest.json", manifest), ("ent-gov-model-candidate.artifact.json", candidate),
            ("downstream-compatibility.json", compatibility), ("semantic-review-packet.json", review)): atomic_write(output / name, pretty_bytes(value))
        summary.update({"passed": True, "status": "complete", "artifact_id": candidate["artifact"]["artifact_id"], "artifact_hash": candidate["integrity"]["output_hash"],
            "semantic_review_packet_id": review["packet_id"], "semantic_review_packet_hash": review["packet_hash"], "matrix_state": candidate["extensions"]["enterprise"]["role"]["compliance_matrix"][0]["state"], "usage": usage})
    except Exception as exc: summary.update({"status": "failed_closed", "error_type": type(exc).__name__, "error": str(exc)[:1000]})
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True)); return 0 if summary["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())

#!/usr/bin/env python3
"""Run ADR-0035 isolated Qwen3-32B ENT-ARCH evaluation on GX-10."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from accepted_live_enterprise_arch_runtime import build_candidate, build_compatibility, build_package, build_review_packet
from artifact_ledger import atomic_write, pretty_bytes
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema


PROMPT = ROOT / "appendices/prompt-templates/candidates/ent-arch/design-0.1.0.prompt.txt"
SCHEMA = ROOT / "appendices/schemas/ent-arch-role.schema.json"
MODEL = ROOT / "appendices/model-manifests/gx10-qwen3-32b-ent-arch-multi-domain-evaluation-0.1.0.json"


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000"); parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--raw-response", type=Path, help="Reproject a retained model role without invoking the model")
    parser.add_argument("--timeout-seconds", type=int, default=900); args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    source, eligibility, gate, manifest, deterministic, _, _ = build_package()
    schema = prepare_guided_schema(inline_local_refs(load_json(SCHEMA)), 12, 512)
    expected = deterministic["extensions"]["enterprise"]["role"]
    source_role = source["extensions"]["capability"]["role"]
    context = {"designation": "ENT-ARCH", "evidence_tier": expected["evidence_tier"], "fitness_claim": expected["fitness_claim"],
               "generation_contract": schema, "required_manifest_binding": expected["manifest_binding"],
               "ent_evidence_gate": {"artifact_id": gate["artifact"]["artifact_id"], "content_hash": expected["manifest_binding"]["gate_artifact_hash"]},
               "cap_synth_input": {"artifact_id": source["artifact"]["artifact_id"], "content_hash": expected["manifest_binding"]["capability_artifact_hashes"][0],
                                    "capability_id": source["extensions"]["capability"]["capability_id"],
                                    "posture": source_role["capability_posture"],
                                    "derived_assertions": source_role["derived_capability_assertions"],
                                    "preserved_assertions": source_role["preserved_child_assertions"]},
               "anti_double_counting": manifest,
               "constraints": ["CAP-SYNTH is the only admitted capability artifact",
                               "its CAP-RISK and CAP-REQ children are lineage only and must not be counted as independent inputs",
                               "architecture_coherence.state must be insufficient_evidence",
                               "dependency_topology, shared_service_concentration, failure_propagation, architecture_debt, and unsupported_claims must be empty",
                               "target_state_alignment.state and transition_architecture.state must be not_assessed",
                               "every sourced record must cite only the CAP-SYNTH artifact and real preserved or derived record IDs",
                               "confidence concerns unassessability, not readiness or coherence",
                               "comparison only; no scheduling, report, deployment, risk acceptance, or requirements satisfaction"]}
    model = load_json(MODEL)
    adapter = VLLMAdapter(args.base_url, model["model_id"], api_key_env=args.api_key_env,
                          max_tokens=model["max_output_tokens"], disable_thinking=True, use_json_schema=True,
                          guided_array_max_items=model["guided_array_max_items"])
    summary = {"suite": "ent-arch-accepted-live-multi-domain-single-capability-evaluation", "designation": "ENT-ARCH",
               "candidate_status": "candidate", "semantic_acceptance": "awaiting_project_owner_review",
               "evidence_tier": expected["evidence_tier"], "fitness_claim": expected["fitness_claim"],
               "anti_double_counting": manifest["anti_double_counting"], "cap_synth_scheduled": False,
               "ent_arch_scheduled": False, "report_effect": "none", "deployment_effect": "none",
               "production_target": "A100 large cluster", "test_platform": "DGX Spark or approved equivalent (GX-10)", "passed": False}
    try:
        if args.raw_response is not None:
            raw = args.raw_response.read_bytes()
            payload = json.loads(raw.decode("utf-8"))
            usage = {"mode": "retained_response_reprojection", "model_invoked": False}
            atomic_write(output / "raw-response.json", raw)
            summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        else:
            payload, usage = adapter.generate(PROMPT.read_text(encoding="utf-8"), context, args.timeout_seconds)
            if adapter.last_response_content is not None:
                raw = adapter.last_response_content.encode("utf-8"); atomic_write(output / "raw-response.json", raw)
                summary["raw_response_sha256"] = hashlib.sha256(raw).hexdigest()
        candidate = build_candidate(gate, source, payload); compatibility = build_compatibility(candidate)
        review = build_review_packet(candidate, manifest, eligibility)
        for name, value in (("cap-synth-input.artifact.json", source), ("cap-synth-eligibility.json", eligibility),
                            ("ent-evidence-gate.artifact.json", gate), ("enterprise-architecture-input-manifest.json", manifest),
                            ("ent-arch-model-candidate.artifact.json", candidate), ("downstream-compatibility.json", compatibility),
                            ("semantic-review-packet.json", review)):
            atomic_write(output / name, pretty_bytes(value))
        summary.update({"passed": True, "status": "complete", "artifact_id": candidate["artifact"]["artifact_id"],
                        "artifact_hash": candidate["integrity"]["output_hash"], "semantic_review_packet_id": review["packet_id"],
                        "semantic_review_packet_hash": review["packet_hash"], "usage": usage})
    except Exception as exc:
        summary.update({"status": "failed_closed", "error_type": type(exc).__name__, "error": str(exc)[:1000]})
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True)); return 0 if summary["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())

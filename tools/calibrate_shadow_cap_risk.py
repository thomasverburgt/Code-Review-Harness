#!/usr/bin/env python3
"""Run model-backed CAP-RISK against the accepted PROD-SYNTH shadow child."""
from __future__ import annotations
import argparse, hashlib, json, shutil, uuid
from pathlib import Path
from artifact_ledger import ArtifactLedger, atomic_write, pretty_bytes
from run_shadow_product_synth_reference import BASELINE
from shadow_product_synth_runtime import compare_paths
from validate_vertical_slice import ROOT, assert_schema, load_json
from worker_runtime import FileQueue, VLLMAdapter, VersionResolver, Worker

WORKFLOW_PATH = ROOT / "appendices/candidate-workflows/prod-synth-cap-risk-shadow.workflow.json"
MODEL_MANIFEST = ROOT / "appendices/model-manifests/gx10-qwen3-32b-cap-risk-calibration-0.1.0.json"
DEFAULT_EVIDENCE = "fixtures/product-synth-admission/evidence/2026-07-31/live-calibration/accepted-prod-synth.artifact.json"
EXECUTION_ID = "99500000-0000-4000-8000-000000000001"
CREATED_AT = "2026-07-31T23:00:00Z"
NAMESPACE = uuid.UUID("99500000-0000-4000-8000-000000000000")

def digest(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def build_job(path: str, child: dict, workflow: dict, manifest: dict) -> dict:
    node = next(item for item in workflow["nodes"] if item["designation"] == "CAP-RISK")
    model = {"provider": manifest["provider"], "model_id": manifest["model_id"], "version": manifest["upstream_revision"]}
    dispatch = {"dispatch_id": str(uuid.uuid5(NAMESPACE, "dispatch")), "workflow_id": workflow["workflow_id"],
        "workflow_version": workflow["workflow_version"], "execution_id": EXECUTION_ID, "node_id": node["node_id"],
        "agent": {"agent_uuid": node["agent_uuid"], "designation": "CAP-RISK", "contract_version": "1.0.0"},
        "scope": {"capability_id": "CAPABILITY-IDENTITY-ACCESS", "participating_products": [child["scope"]["product_id"]],
                  "source_revision": child["scope"]["source_revision"], "included": ["accepted PROD-SYNTH shadow child"],
                  "excluded": ["authoritative baseline, report publication, governance, and deployment"], "decision_context": "shadow_comparison"},
        "input_manifest": [{"artifact_id": child["artifact"]["artifact_id"], "artifact_type": child["artifact"]["artifact_type"],
                            "hash": child["integrity"]["output_hash"], "schema": "universal-agent-artifact.schema.json",
                            "producer_designation": "PROD-SYNTH", "lifecycle_state": child["artifact"]["lifecycle_state"],
                            "freshness_state": "fresh", "required": True}],
        "version_pins": {**workflow["version_pins"], "model": model},
        "execution_environment": {"execution_mode": "test", "platform_designation": "GX-10", "platform_class": "approved-equivalent",
            "approval_reference": "ADR-0008", "accelerator_runtime": "NVIDIA GB10/CUDA test runtime",
            "container_image": manifest["container_image"], "model_or_workload_scale": manifest["upstream_model"],
            "limitations": ["Test results do not represent measured A100 production capacity"], "environment_policy_version": "ADR-0008"},
        "expected_output": {"universal_schema": "universal-agent-artifact.schema.json", "layer": "capability",
            "layer_schema": node["output_schema"], "role_schema": node["role_schema"], "consumers": node["consumers"]},
        "partial_input_authorization": None, "created_at": CREATED_AT}
    assert_schema(dispatch, "dispatch-envelope.schema.json", "shadow CAP-RISK dispatch")
    job = {"job_id": str(uuid.uuid5(NAMESPACE, "live-job")), "idempotency_key": f"{EXECUTION_ID}:cap-risk-shadow:live",
        "execution_id": EXECUTION_ID, "node_id": node["node_id"], "designation": "CAP-RISK", "dispatch": dispatch,
        "evidence_paths": [path], "allowed_evidence_paths": [path], "max_attempts": 1, "timeout_seconds": 900,
        "created_at": CREATED_AT, "generation_mode": manifest["generation_mode"],
        "generation_contract_version": manifest["generation_contract_version"], "assembler_version": manifest["assembler_version"],
        "projection_version": manifest["projection_version"]}
    assert_schema(job, "worker-job.schema.json", "shadow CAP-RISK job")
    return job

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, required=True); parser.add_argument("--base-url", default="http://127.0.0.1:8000"); parser.add_argument("--api-key-env", default="VLLM_API_KEY"); parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args(); output = args.output_dir.resolve()
    if output.exists(): shutil.rmtree(output)
    output.mkdir(parents=True)
    workflow, manifest, child = load_json(WORKFLOW_PATH), load_json(MODEL_MANIFEST), load_json(ROOT / DEFAULT_EVIDENCE)
    job = build_job(DEFAULT_EVIDENCE, child, workflow, manifest); job["timeout_seconds"] = args.timeout_seconds
    model = {"provider": manifest["provider"], "model_id": manifest["model_id"], "version": manifest["upstream_revision"]}
    adapter = VLLMAdapter(args.base_url, manifest["model_id"], api_key_env=args.api_key_env, max_tokens=manifest["max_output_tokens"],
                          disable_thinking=True, use_json_schema=True, guided_array_max_items=manifest["guided_array_max_items"])
    queue = FileQueue(output / "queue"); queue.enqueue(job)
    result = Worker(queue, output / "workers", adapter, "WORKER-GX10-CAP-RISK-SHADOW-001", ArtifactLedger(output / "ledger-shadow"),
                    VersionResolver(model_pin_override=model, workflow_path=WORKFLOW_PATH)).process_next()
    if result is None: raise RuntimeError("shadow worker returned no result")
    worker_dir = output / "workers" / job["job_id"]; telemetry = load_json(worker_dir / "telemetry.json")
    comparison_state = None
    if result["status"] == "complete":
        artifact = load_json(worker_dir / "artifact.json")
        comparison = compare_paths(load_json(BASELINE), child, artifact, product_ms=264198,
                                   risk_ms=telemetry["wall_duration_ms"], platform="GX-10-DGX-Spark-equivalent")
        atomic_write(output / "accepted-shadow-cap-risk.artifact.json", pretty_bytes(artifact))
        atomic_write(output / "live-shadow-comparison.json", pretty_bytes(comparison)); comparison_state = comparison["overall_state"]
    summary = {"suite": "live-shadow-cap-risk", "status": result["status"], "error": result["error"],
        "artifact_hash": result["artifact_hash"], "comparison_state": comparison_state, "authority_effect": "comparison_only",
        "baseline_workflow_changed": False, "report_package_changed": False, "input_tokens": telemetry["input_tokens"],
        "output_tokens": telemetry["output_tokens"], "wall_duration_ms": telemetry["wall_duration_ms"],
        "model_manifest_sha256": digest(MODEL_MANIFEST.read_bytes()), "credential_exported": False}
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True))
    return 0 if result["status"] == "complete" else 1

if __name__ == "__main__": raise SystemExit(main())

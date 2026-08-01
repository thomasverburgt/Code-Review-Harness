#!/usr/bin/env python3
"""Run the unscheduled PROD-SYNTH candidate through the live contract-gated worker."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from pathlib import Path

from artifact_ledger import ArtifactLedger, atomic_write, pretty_bytes
from validate_vertical_slice import ROOT, assert_schema, load_json
from worker_runtime import FileQueue, VLLMAdapter, VersionResolver, Worker


CANDIDATE_WORKFLOW = ROOT / "appendices/candidate-workflows/prod-synth-calibration.workflow.json"
MODEL_MANIFEST = ROOT / "appendices/model-manifests/gx10-qwen3-32b-prod-synth-calibration-0.1.0.json"
DEFAULT_EVIDENCE = "fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/accepted-prod-sec.artifact.json"
EXECUTION_ID = "99000000-0000-4000-8000-000000000001"
CREATED_AT = "2026-07-31T21:00:00Z"
NAMESPACE = uuid.UUID("99000000-0000-4000-8000-000000000000")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def build_dispatch(child: dict, workflow: dict, manifest: dict) -> dict:
    node = workflow["nodes"][0]
    model_pin = {"provider": manifest["provider"], "model_id": manifest["model_id"], "version": manifest["upstream_revision"]}
    dispatch = {
        "dispatch_id": str(uuid.uuid5(NAMESPACE, "prod-synth-dispatch")),
        "workflow_id": workflow["workflow_id"], "workflow_version": workflow["workflow_version"],
        "execution_id": EXECUTION_ID, "node_id": node["node_id"],
        "agent": {"agent_uuid": node["agent_uuid"], "designation": node["designation"], "contract_version": "1.0.0"},
        "scope": {"product_id": child["scope"]["product_id"], "source_revision": child["scope"]["source_revision"],
                  "included": ["immutable PROD-SEC candidate-calibration child"], "excluded": ["other product domains by calibration policy"],
                  "decision_context": "candidate_calibration"},
        "input_manifest": [{"artifact_id": child["artifact"]["artifact_id"], "artifact_type": child["artifact"]["artifact_type"],
                            "hash": child["integrity"]["output_hash"], "schema": "universal-agent-artifact.schema.json",
                            "producer_designation": child["identity"]["designation"], "lifecycle_state": child["artifact"]["lifecycle_state"],
                            "freshness_state": "fresh", "required": True}],
        "version_pins": {**workflow["version_pins"], "model": model_pin},
        "execution_environment": {"execution_mode": "test", "platform_designation": "GX-10",
                                  "platform_class": "approved-equivalent", "approval_reference": "ADR-0008",
                                  "accelerator_runtime": "NVIDIA GB10/CUDA test runtime",
                                  "container_image": manifest["container_image"], "model_or_workload_scale": manifest["upstream_model"],
                                  "limitations": ["Test results do not represent measured A100 production capacity"],
                                  "environment_policy_version": "ADR-0008"},
        "expected_output": {"universal_schema": "universal-agent-artifact.schema.json", "layer": "product",
                            "layer_schema": node["output_schema"], "role_schema": node["role_schema"],
                            "consumers": node["consumers"]},
        "partial_input_authorization": None, "created_at": CREATED_AT,
    }
    assert_schema(dispatch, "dispatch-envelope.schema.json", "PROD-SYNTH calibration dispatch")
    return dispatch


def build_job(evidence_path: str, child: dict, workflow: dict, manifest: dict) -> dict:
    dispatch = build_dispatch(child, workflow, manifest)
    job = {"job_id": str(uuid.uuid5(NAMESPACE, "prod-synth-live-calibration")),
           "idempotency_key": f"{EXECUTION_ID}:prod-synth-candidate:live-calibration", "execution_id": EXECUTION_ID,
           "node_id": "prod-synth-candidate", "designation": "PROD-SYNTH", "dispatch": dispatch,
           "evidence_paths": [evidence_path], "allowed_evidence_paths": [evidence_path], "max_attempts": 1,
           "timeout_seconds": 900, "created_at": CREATED_AT, "generation_mode": manifest["generation_mode"],
           "generation_contract_version": manifest["generation_contract_version"],
           "assembler_version": manifest["assembler_version"], "projection_version": manifest["projection_version"]}
    assert_schema(job, "worker-job.schema.json", "PROD-SYNTH calibration job")
    return job


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--evidence-path", default=DEFAULT_EVIDENCE)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    workflow, manifest = load_json(CANDIDATE_WORKFLOW), load_json(MODEL_MANIFEST)
    child = load_json(ROOT / args.evidence_path)
    job = build_job(args.evidence_path, child, workflow, manifest)
    job["timeout_seconds"] = args.timeout_seconds
    model_pin = {"provider": manifest["provider"], "model_id": manifest["model_id"], "version": manifest["upstream_revision"]}
    resolver = VersionResolver(model_pin_override=model_pin, workflow_path=CANDIDATE_WORKFLOW)
    queue = FileQueue(output / "queue")
    queue.enqueue(job)
    adapter = VLLMAdapter(args.base_url, manifest["model_id"], api_key_env=args.api_key_env,
                          max_tokens=manifest["max_output_tokens"], disable_thinking=True, use_json_schema=True,
                          guided_array_max_items=manifest["guided_array_max_items"])
    result = Worker(queue, output / "workers", adapter, worker_id="WORKER-GX10-PROD-SYNTH-001",
                    ledger=ArtifactLedger(output / "ledger"), resolver=resolver).process_next()
    if result is None:
        raise RuntimeError("PROD-SYNTH worker returned no result")
    raw_hash = None
    if adapter.last_response_content is not None:
        raw = adapter.last_response_content.encode("utf-8")
        raw_hash = sha256_bytes(raw)
        atomic_write(output / "raw-response.txt", raw)
    worker_dir = output / "workers" / job["job_id"]
    telemetry = load_json(worker_dir / "telemetry.json")
    if result["status"] == "complete":
        artifact = load_json(worker_dir / "artifact.json")
        atomic_write(output / "accepted-prod-synth.artifact.json", pretty_bytes(artifact))
    summary = {"suite": "prod-synth-live-candidate-calibration", "designation": "PROD-SYNTH",
               "candidate_status": "candidate", "scheduled": False, "baseline_workflow_changed": False,
               "model_manifest": str(MODEL_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
               "model_manifest_sha256": sha256_bytes(MODEL_MANIFEST.read_bytes()),
               "status": result["status"], "error": result["error"], "artifact_hash": result["artifact_hash"],
               "raw_response_sha256": raw_hash, "input_tokens": telemetry["input_tokens"],
               "output_tokens": telemetry["output_tokens"], "wall_duration_ms": telemetry["wall_duration_ms"],
               "credential_exported": False, "passed": result["status"] == "complete"}
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


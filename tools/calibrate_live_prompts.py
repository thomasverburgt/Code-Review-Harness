#!/usr/bin/env python3
"""Run the four candidate prompts through the contract-gated live worker path."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from pathlib import Path

from artifact_ledger import ArtifactLedger, atomic_write, pretty_bytes
from run_vertical_slice import DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, run
from validate_vertical_slice import ROOT, load_json
from worker_runtime import FileQueue, VLLMAdapter, VersionResolver, Worker


DESIGNATIONS = ("SPEC-SECRETS", "PROD-SEC", "CAP-RISK", "ENT-SYSRISK")
NODES = {"SPEC-SECRETS": "spec-secrets", "PROD-SEC": "prod-sec", "CAP-RISK": "cap-risk", "ENT-SYSRISK": "ent-sysrisk"}
EVIDENCE = {
    "SPEC-SECRETS": ["fixtures/vertical-risk-slice/gold/input-manifest.json"],
    "PROD-SEC": ["fixtures/vertical-risk-slice/gold/spec-secrets.artifact.json"],
    "CAP-RISK": ["fixtures/vertical-risk-slice/gold/prod-sec.artifact.json"],
    "ENT-SYSRISK": [
        "fixtures/vertical-risk-slice/gold/cap-risk.artifact.json",
        "fixtures/vertical-risk-slice/gold/ent-evidence.artifact.json",
    ],
}
MODEL_MANIFEST = ROOT / "appendices" / "model-manifests" / "gx10-qwen3-32b-calibration-0.1.0.json"
NAMESPACE = uuid.UUID("95000000-0000-4000-8000-000000000000")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--model-manifest", type=Path, default=MODEL_MANIFEST)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--spec-evidence-path", default=EVIDENCE["SPEC-SECRETS"][0])
    parser.add_argument("--prod-evidence-path", default=EVIDENCE["PROD-SEC"][0])
    parser.add_argument("--cap-evidence-path", default=EVIDENCE["CAP-RISK"][0])
    parser.add_argument("--ent-cap-evidence-path", default=EVIDENCE["ENT-SYSRISK"][0])
    parser.add_argument("--ent-gate-evidence-path", default=EVIDENCE["ENT-SYSRISK"][1])
    parser.add_argument("--designation", action="append", choices=DESIGNATIONS,
                        help="Run only the selected designation; repeat to select multiple roles")
    args = parser.parse_args()

    output = args.output_dir.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    reference_run = output / "reference-run"
    run(reference_run, DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, "gold")

    manifest_path = args.model_manifest
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = load_json(manifest_path)
    model_pin = {"provider": manifest["provider"], "model_id": manifest["model_id"], "version": manifest["upstream_revision"]}
    resolver = VersionResolver(model_pin_override=model_pin)
    ledger = ArtifactLedger(output / "ledger")
    results = []
    evidence_by_designation = dict(EVIDENCE)
    evidence_by_designation["SPEC-SECRETS"] = [args.spec_evidence_path]
    evidence_by_designation["PROD-SEC"] = [args.prod_evidence_path]
    evidence_by_designation["CAP-RISK"] = [args.cap_evidence_path]
    evidence_by_designation["ENT-SYSRISK"] = [args.ent_cap_evidence_path, args.ent_gate_evidence_path]

    selected_designations = tuple(args.designation) if args.designation else DESIGNATIONS
    allowed_designations = tuple(manifest.get("scope_designations", DESIGNATIONS))
    unsupported = sorted(set(selected_designations) - set(allowed_designations))
    if unsupported:
        raise ValueError(
            f"model manifest generation topology is not approved for: {', '.join(unsupported)}; "
            f"approved scope: {', '.join(allowed_designations)}"
        )
    for designation in selected_designations:
        node = NODES[designation]
        dispatch = load_json(reference_run / "dispatch" / f"{node}.json")
        dispatch["version_pins"]["model"] = model_pin
        dispatch["execution_environment"]["model_or_workload_scale"] = manifest["upstream_model"]
        suffix = f"live-calibration-{designation.lower()}"
        job_id = str(uuid.uuid5(NAMESPACE, suffix))
        job = {
            "job_id": job_id,
            "idempotency_key": f"{DEFAULT_EXECUTION_ID}:{node}:{suffix}",
            "execution_id": DEFAULT_EXECUTION_ID,
            "node_id": node,
            "designation": designation,
            "dispatch": dispatch,
            "evidence_paths": evidence_by_designation[designation],
            "allowed_evidence_paths": evidence_by_designation[designation],
            "max_attempts": 1,
            "timeout_seconds": args.timeout_seconds,
            "created_at": DEFAULT_STARTED_AT,
            "generation_mode": manifest["generation_mode"],
            "generation_contract_version": manifest["generation_contract_version"],
            "assembler_version": manifest["assembler_version"],
        }
        if manifest.get("projection_version"):
            job["projection_version"] = manifest["projection_version"]
        queue = FileQueue(output / "queue")
        queue.enqueue(job)
        adapter = VLLMAdapter(
            args.base_url,
            manifest["model_id"],
            api_key_env=args.api_key_env,
            max_tokens=manifest["max_output_tokens"],
            disable_thinking=True,
            use_json_schema=True,
            guided_array_max_items=manifest["guided_array_max_items"],
        )
        result = Worker(queue, output / "workers", adapter, worker_id="WORKER-GX10-CALIBRATION-001",
                        ledger=ledger, resolver=resolver).process_next()
        if result is None:
            raise RuntimeError(f"worker returned no result for {designation}")
        raw = adapter.last_response_content
        raw_hash = None
        if raw is not None:
            raw_bytes = raw.encode("utf-8")
            raw_hash = sha256_bytes(raw_bytes)
            atomic_write(output / "workers" / job_id / "raw-response.txt", raw_bytes)
        telemetry = load_json(output / "workers" / job_id / "telemetry.json")
        results.append({
            "designation": designation,
            "status": result["status"],
            "error": result["error"],
            "artifact_hash": result["artifact_hash"],
            "raw_response_sha256": raw_hash,
            "input_tokens": telemetry["input_tokens"],
            "output_tokens": telemetry["output_tokens"],
            "wall_duration_ms": telemetry["wall_duration_ms"],
        })

    summary = {
        "suite": "live-prompt-calibration",
        "model_manifest": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "model_manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "credential_exported": False,
        "selected_designations": list(selected_designations),
        "results": results,
        "passed": all(item["status"] == "complete" for item in results),
    }
    atomic_write(output / "summary.json", pretty_bytes(summary))
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

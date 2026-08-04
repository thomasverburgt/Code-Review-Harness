#!/usr/bin/env python3
"""Run isolated GX-10 Qwen3-32B calibration for ADR-0039 Increment 1."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
from pathlib import Path

from artifact_ledger import atomic_write, content_hash, pretty_bytes
from run_specialist_static_evidence_increment1 import CONFIG, GENERATED_AT, build_candidate, build_manifest, locator
from specialist_shadow_calibration_runtime import build_review_packet, stable_uuid, validate_candidate_artifact
from validate_vertical_slice import ROOT, load_json
from worker_runtime import VLLMAdapter, inline_local_refs, prepare_guided_schema


def safe_error_text(exc: Exception, api_key_env: str) -> str:
    message = str(exc)
    secret = os.environ.get(api_key_env)
    if secret:
        message = message.replace(secret, "[REDACTED]").replace(secret.strip(), "[REDACTED]")
    message = re.sub(r"(?i)Bearer\s+[^'\"\s]+", "Bearer [REDACTED]", message)
    return message[:1000]


def run_role(designation: str, output: Path, base_url: str, api_key_env: str, timeout: int) -> dict:
    cfg = CONFIG[designation]
    manifest = build_manifest(designation)
    deterministic = build_candidate(manifest)
    schema_path = ROOT / f"appendices/schemas/{cfg['slug']}-role.schema.json"
    model_path = ROOT / f"appendices/model-manifests/gx10-qwen3-32b-{cfg['slug']}-calibration-0.1.0.json"
    prompt_path = ROOT / f"appendices/prompt-templates/candidates/{cfg['slug']}/design-0.2.0.prompt.txt"
    schema = prepare_guided_schema(inline_local_refs(load_json(schema_path)), 12, 512)
    evidence = [{
        "evidence_id": evidence_id, "path": path, "line": line, "section": section,
        "safe_excerpt": text, "content_hash": next(item["content_hash"] for item in manifest["evidence_population"] if item["evidence_id"] == evidence_id),
    } for evidence_id, path, line, text, section in cfg["evidence"]]
    context = {
        "designation": designation,
        "generation_contract": schema,
        "authoritative_focus_binding": manifest["focus_binding"],
        "immutable_repository": manifest["repository"],
        "admitted_evidence": evidence,
        "required_result_shape_and_bounded_facts": deterministic["extensions"]["specialist"]["role"],
        "constraints": [
            "Return only the strict role payload.",
            "Use only admitted evidence IDs and preserve missing evidence as unknown.",
            "Do not infer a resolved graph, complete SBOM, or completed lint execution.",
            "Keep the role comparison-only, unscheduled, downstream-ineligible, and human-authority bounded.",
        ],
    }
    model = load_json(model_path)
    adapter = VLLMAdapter(base_url, model["model_id"], api_key_env=api_key_env,
                          max_tokens=model["max_output_tokens"], disable_thinking=True,
                          use_json_schema=True, guided_array_max_items=12)
    target = output / cfg["slug"]
    target.mkdir(parents=True, exist_ok=True)
    summary = {"designation": designation, "suite": "adr0039-increment1-specialist-static-evidence-live-calibration",
               "passed": False, "candidate_status": "candidate", "semantic_acceptance": "awaiting_human_review",
               "scheduled": False, "product_fan_in_eligible": False, "report_eligible": False,
               "deployment_authorized": False, "a100_production_authorized": False,
               "test_platform": "GX-10 / approved DGX Spark-equivalent"}
    try:
        payload, usage = adapter.generate(prompt_path.read_text(encoding="utf-8"), context, timeout)
        raw = (adapter.last_response_content or json.dumps(payload, sort_keys=True)).encode("utf-8")
        raw_hash = "sha256:" + hashlib.sha256(raw).hexdigest()
        atomic_write(target / "raw-response.json", raw)
        candidate = copy.deepcopy(deterministic)
        candidate["extensions"]["specialist"]["role"] = payload
        candidate["execution"]["model"] = model["model_id"]
        candidate["execution"]["generation_mode"] = "model_role_payload_deterministic_universal_projection"
        candidate["artifact"]["artifact_id"] = stable_uuid(manifest["manifest_id"], raw_hash, "model-candidate")
        candidate["integrity"]["output_hash"] = content_hash(payload)
        validate_candidate_artifact(manifest, candidate)
        locators = [locator(item) for item in cfg["evidence"]]
        packet = build_review_packet(manifest, candidate, locators, GENERATED_AT)
        for name, value in (("input-manifest.json", manifest), ("model-candidate.artifact.json", candidate),
                            ("evidence-locators.json", locators), ("human-shadow-review-packet.json", packet)):
            atomic_write(target / name, pretty_bytes(value))
        summary.update({"passed": True, "status": "complete", "raw_response_hash": raw_hash,
                        "artifact_id": candidate["artifact"]["artifact_id"], "artifact_hash": content_hash(candidate),
                        "packet_id": packet["packet_id"], "packet_hash": packet["packet_hash"], "usage": usage})
    except Exception as exc:
        if adapter.last_response_content is not None:
            atomic_write(target / "raw-response.json", adapter.last_response_content.encode("utf-8"))
        summary.update({"status": "failed_closed", "error_type": type(exc).__name__, "error": safe_error_text(exc, api_key_env)})
    atomic_write(target / "summary.json", pretty_bytes(summary))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key-env", default="VLLM_API_KEY")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    results = [run_role(name, output, args.base_url, args.api_key_env, args.timeout_seconds) for name in CONFIG]
    summary = {"suite": "adr0039-increment1-all-static-evidence-specialists", "passed": all(item["passed"] for item in results),
               "results": results, "scheduled": False, "product_fan_in_eligible": False,
               "report_eligible": False, "deployment_authorized": False, "a100_production_authorized": False}
    atomic_write(output / "summary.json", pretty_bytes(summary)); print(json.dumps(summary, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())

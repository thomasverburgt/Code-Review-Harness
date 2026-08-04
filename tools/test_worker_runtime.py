#!/usr/bin/env python3
"""Increment 2 conformance tests; run only on DGX Spark or approved equivalent."""

from __future__ import annotations

import copy
import json
import os
import tempfile
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from run_vertical_slice import DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, run
from artifact_ledger import ArtifactLedger, LedgerError
from build_enterprise_evidence_gate import build_enterprise_evidence_artifact
from worker_runtime import (ANALYTICAL_FIELDS, ASSEMBLER_VERSION, CANONICAL_ASSEMBLER_VERSION,
                            CAPABILITY_CANONICAL_GENERATION_CONTRACT_VERSION,
                            CAPABILITY_CANONICAL_PROJECTION_VERSION,
                            CANONICAL_GENERATION_CONTRACT_VERSION, CANONICAL_PROJECTION_VERSION,
                            GENERATION_CONTRACT_VERSION, PRODUCT_CANONICAL_GENERATION_CONTRACT_VERSION,
                            PRODUCT_CANONICAL_PROJECTION_VERSION,
                            ENTERPRISE_CANONICAL_GENERATION_CONTRACT_VERSION,
                            ENTERPRISE_CANONICAL_PROJECTION_VERSION, FileQueue,
                            FixtureModelAdapter, LeastPrivilegeEvidenceAdapter, ModelAdapter,
                            RetryableAdapterError, VLLMAdapter, VersionResolver, Worker, WorkerError,
                            assemble_artifact, assemble_canonical_artifact, compose_output_schema,
                            prepare_guided_schema, stable_uuid, validate_candidate)


EVIDENCE = {
    "SPEC-SECRETS": ["fixtures/vertical-risk-slice/gold/input-manifest.json"],
    "PROD-SEC": ["fixtures/vertical-risk-slice/gold/spec-secrets.artifact.json"],
    "CAP-RISK": ["fixtures/vertical-risk-slice/gold/prod-sec.artifact.json"],
    "ENT-SYSRISK": [
        "fixtures/vertical-risk-slice/gold/cap-risk.artifact.json",
        "fixtures/vertical-risk-slice/gold/ent-evidence.artifact.json",
    ],
}
NODES = {"SPEC-SECRETS": "spec-secrets", "PROD-SEC": "prod-sec", "CAP-RISK": "cap-risk", "ENT-SYSRISK": "ent-sysrisk"}


class InvalidAuthorityAdapter(FixtureModelAdapter):
    def generate(self, prompt, context, timeout_seconds):
        artifact, usage = super().generate(prompt, context, timeout_seconds)
        artifact["decision_authority"] = "agent"
        return artifact, usage


class FlakyAdapter(FixtureModelAdapter):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt, context, timeout_seconds):
        self.calls += 1
        if self.calls == 1:
            raise RetryableAdapterError("synthetic transient model failure")
        return super().generate(prompt, context, timeout_seconds)


class AlwaysTimeoutAdapter(FixtureModelAdapter):
    def generate(self, prompt, context, timeout_seconds):
        raise RetryableAdapterError("synthetic adapter timeout")


class CountingAdapter(FixtureModelAdapter):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt, context, timeout_seconds):
        self.calls += 1
        return super().generate(prompt, context, timeout_seconds)


class FixtureRolePayloadAdapter(FixtureModelAdapter):
    def generate(self, prompt, context, timeout_seconds):
        artifact, usage = super().generate(prompt, context, timeout_seconds)
        layer = {"SPEC-SECRETS": "specialist", "PROD-SEC": "product", "CAP-RISK": "capability", "ENT-SYSRISK": "enterprise"}[context["designation"]]
        payload = {field: copy.deepcopy(artifact[field]) for field in ANALYTICAL_FIELDS}
        payload["layer_payload"] = copy.deepcopy(artifact["extensions"][layer])
        payload["generation_disclosure"] = {"array_max_items": 3, "string_max_length": 256, "limit_applied": False, "omitted_item_estimate": 0, "truncated_string_estimate": 0}
        return payload, usage


class HarnessFieldOverrideAdapter(FixtureRolePayloadAdapter):
    def generate(self, prompt, context, timeout_seconds):
        payload, usage = super().generate(prompt, context, timeout_seconds)
        payload["identity"] = {"designation": "ATTACKER"}
        return payload, usage


class TruncatedRolePayloadAdapter(FixtureRolePayloadAdapter):
    def generate(self, prompt, context, timeout_seconds):
        payload, usage = super().generate(prompt, context, timeout_seconds)
        payload["generation_disclosure"] = {"array_max_items": 3, "string_max_length": 256, "limit_applied": True, "omitted_item_estimate": 1, "truncated_string_estimate": 0}
        return payload, usage


class FixtureCanonicalPayloadAdapter(FixtureModelAdapter):
    def generate(self, prompt, context, timeout_seconds):
        artifact, usage = super().generate(prompt, context, timeout_seconds)
        confidence = copy.deepcopy(artifact["confidence"])
        confidence["provenance"] = [
            {"source": item.get("source", item.get("artifact_id", "fixture")),
             "version": item.get("version", "fixture-0.1.0")}
            for item in confidence["provenance"]
        ]
        secondary = []
        for kind, field, key in (("pattern", "patterns", "pattern_id"),
                                 ("insight", "insights", "insight_id"),
                                 ("conflict", "conflicts", "conflict_id")):
            for item in artifact[field]:
                secondary.append({"kind": kind, "record_id": item[key],
                                  "statement": item.get("statement", item.get("rationale", kind)),
                                  "evidence_refs": copy.deepcopy(item.get("evidence_refs", []))})
        payload = {
            "methodology": copy.deepcopy(artifact["methodology"]),
            "review_counts": copy.deepcopy(artifact["coverage"]),
            "findings": copy.deepcopy(artifact["findings"]),
            "secondary_records": secondary,
            "confidence": confidence,
            "decisions_requested": copy.deepcopy(artifact["decisions_requested"]),
        }
        layer = {"SPEC-SECRETS": "specialist", "PROD-SEC": "product", "CAP-RISK": "capability",
                 "ENT-SYSRISK": "enterprise"}[context["designation"]]
        payload["role_payload"] = copy.deepcopy(artifact["extensions"][layer]["role"])
        if context["designation"] == "CAP-RISK":
            extension = artifact["extensions"]["capability"]
            payload["layer_context"] = {field: copy.deepcopy(extension[field]) for field in (
                "mission_thread", "requirement_traceability", "cross_product_interface_state",
                "human_centered_systems_evaluation", "mission_effectiveness_evidence", "operational_readiness")}
        if context["designation"] == "ENT-SYSRISK":
            extension = artifact["extensions"]["enterprise"]
            payload["layer_context"] = {field: copy.deepcopy(extension[field]) for field in (
                "enterprise_scope", "cross_capability_correlations", "enterprise_assertions",
                "systemic_dependencies")}
        payload["generation_disclosure"] = {"omitted_item_estimate": 0, "truncated_string_estimate": 0}
        return payload, usage


class TruncatedCanonicalPayloadAdapter(FixtureCanonicalPayloadAdapter):
    def generate(self, prompt, context, timeout_seconds):
        payload, usage = super().generate(prompt, context, timeout_seconds)
        payload["generation_disclosure"]["omitted_item_estimate"] = 1
        return payload, usage


class CanonicalHarnessFieldOverrideAdapter(FixtureCanonicalPayloadAdapter):
    def generate(self, prompt, context, timeout_seconds):
        payload, usage = super().generate(prompt, context, timeout_seconds)
        payload["inputs"] = [{"artifact_id": "attacker-controlled"}]
        return payload, usage


class MockVLLMHandler(BaseHTTPRequestHandler):
    artifact: dict = {}

    def do_POST(self):
        if self.path != "/v1/chat/completions" or self.headers.get("Authorization") != "Bearer conformance-test-key":
            self.send_response(401)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length).decode("utf-8"))
        assert request["model"] == "qwen3-32b"
        payload = {
            "choices": [{"message": {"content": json.dumps(self.artifact)}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200},
        }
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def job_for(run_dir: Path, designation: str, suffix: str = "baseline", max_attempts: int = 2,
            role_payload: bool = False, canonical_payload: bool = False) -> dict:
    node = NODES[designation]
    dispatch = json.loads((run_dir / "dispatch" / f"{node}.json").read_text(encoding="utf-8"))
    job_id = str(uuid.uuid5(uuid.UUID("94000000-0000-4000-8000-000000000000"), f"{designation}|{suffix}"))
    job = {
        "job_id": job_id,
        "idempotency_key": f"{DEFAULT_EXECUTION_ID}:{node}:{suffix}",
        "execution_id": DEFAULT_EXECUTION_ID,
        "node_id": node,
        "designation": designation,
        "dispatch": dispatch,
        "evidence_paths": EVIDENCE[designation],
        "allowed_evidence_paths": EVIDENCE[designation],
        "max_attempts": max_attempts,
        "timeout_seconds": 30,
        "created_at": DEFAULT_STARTED_AT,
    }
    if role_payload:
        job.update({
            "generation_mode": "role_payload_v1",
            "generation_contract_version": GENERATION_CONTRACT_VERSION,
            "assembler_version": ASSEMBLER_VERSION,
        })
    if canonical_payload:
        generation_version = {"SPEC-SECRETS": CANONICAL_GENERATION_CONTRACT_VERSION,
                              "PROD-SEC": PRODUCT_CANONICAL_GENERATION_CONTRACT_VERSION,
                              "CAP-RISK": CAPABILITY_CANONICAL_GENERATION_CONTRACT_VERSION,
                              "ENT-SYSRISK": ENTERPRISE_CANONICAL_GENERATION_CONTRACT_VERSION}[designation]
        projection_version = {"SPEC-SECRETS": CANONICAL_PROJECTION_VERSION,
                              "PROD-SEC": PRODUCT_CANONICAL_PROJECTION_VERSION,
                              "CAP-RISK": CAPABILITY_CANONICAL_PROJECTION_VERSION,
                              "ENT-SYSRISK": ENTERPRISE_CANONICAL_PROJECTION_VERSION}[designation]
        job.update({
            "generation_mode": "canonical_payload_v1",
            "generation_contract_version": generation_version,
            "assembler_version": CANONICAL_ASSEMBLER_VERSION,
            "projection_version": projection_version,
        })
    return job


def process(base: Path, run_dir: Path, designation: str, suffix: str, adapter: ModelAdapter,
            max_attempts: int = 2, cancel: bool = False, ledger: ArtifactLedger | None = None,
            role_payload: bool = False, canonical_payload: bool = False) -> tuple[dict, Path, FileQueue]:
    queue = FileQueue(base / f"queue-{suffix}")
    output = base / f"output-{suffix}"
    job = job_for(run_dir, designation, suffix, max_attempts, role_payload, canonical_payload)
    first = queue.enqueue(job)
    second = queue.enqueue(copy.deepcopy(job))
    assert first == second
    if cancel:
        queue.request_cancellation(job["job_id"], "conformance cancellation")
    result = Worker(queue, output, adapter, ledger=ledger).process_next()
    assert result is not None
    return result, output / job["job_id"], queue


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="worker-runtime-tests-") as temp_name:
        base = Path(temp_name)
        run_dir = base / "reference-run"
        run(run_dir, DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, "gold")

        replaced = []
        ledger = ArtifactLedger(base / "worker-ledger")
        resolved_spec = VersionResolver().resolve("SPEC-SECRETS")
        composed = compose_output_schema(resolved_spec["output_contract"], "specialist")
        assert composed["properties"]["extensions"]["required"] == ["specialist"]
        assert composed["properties"]["extensions"]["properties"]["specialist"]["properties"]["role"]["properties"]["designation"]["const"] == "SPEC-SECRETS"
        guided = prepare_guided_schema(composed, 3)
        guided_text = json.dumps(guided)
        assert "uniqueItems" not in guided_text
        assert '"maxItems": 3' in guided_text
        for designation in NODES:
            result, job_dir, queue = process(base, run_dir, designation, f"replace-{designation.lower()}", FixtureModelAdapter(), ledger=ledger)
            assert result["status"] == "complete"
            assert result["artifact_path"] == "artifact.json"
            assert (job_dir / "artifact.json").is_file() and (job_dir / "gate.json").is_file()
            telemetry = json.loads((job_dir / "telemetry.json").read_text(encoding="utf-8"))
            assert telemetry["job_id"] == result["job_id"]
            assert telemetry["execution_id"] == DEFAULT_EXECUTION_ID
            assert telemetry["dispatch_id"] == job_for(run_dir, designation, f"replace-{designation.lower()}")["dispatch"]["dispatch_id"]
            assert Worker(queue, job_dir.parent, FixtureModelAdapter()).process_next() is None
            replaced.append(designation)

        assembled_replaced = []
        for designation in NODES:
            suffix = f"assembled-{designation.lower()}"
            result, job_dir, _ = process(base, run_dir, designation, suffix, FixtureRolePayloadAdapter(),
                                         ledger=ledger, role_payload=True)
            assert result["status"] == "complete", result
            assert result["payload_path"] == "payload.json" and result["assembly_path"] == "assembly.json"
            assert (job_dir / "artifact.json").is_file() and (job_dir / "assembly.json").is_file()
            telemetry = json.loads((job_dir / "telemetry.json").read_text(encoding="utf-8"))
            assert telemetry["generation_mode"] == "role_payload_v1"
            assembled_replaced.append(designation)

        canonical, canonical_dir, _ = process(base, run_dir, "SPEC-SECRETS", "canonical-spec-secrets",
                                               FixtureCanonicalPayloadAdapter(), ledger=ledger,
                                               canonical_payload=True)
        assert canonical["status"] == "complete", canonical
        canonical_artifact = json.loads((canonical_dir / "artifact.json").read_text(encoding="utf-8"))
        canonical_assembly = json.loads((canonical_dir / "assembly.json").read_text(encoding="utf-8"))
        assert canonical_artifact["extensions"]["specialist"]["role"]["designation"] == "SPEC-SECRETS"
        assert canonical_artifact["extensions"]["specialist"]["domain_findings"] == [{"finding_id": "FINDING-SECRET-001"}]
        assert canonical_assembly["projection_version"] == CANONICAL_PROJECTION_VERSION

        canonical_product, canonical_product_dir, _ = process(
            base, run_dir, "PROD-SEC", "canonical-prod-sec", FixtureCanonicalPayloadAdapter(),
            ledger=ledger, canonical_payload=True)
        assert canonical_product["status"] == "complete", canonical_product
        product_artifact = json.loads((canonical_product_dir / "artifact.json").read_text(encoding="utf-8"))
        product_assembly = json.loads((canonical_product_dir / "assembly.json").read_text(encoding="utf-8"))
        assert product_artifact["extensions"]["product"]["role"]["designation"] == "PROD-SEC"
        assert product_artifact["extensions"]["product"]["specialist_artifact_inventory"][0]["designation"] == "SPEC-SECRETS"
        assert product_artifact["extensions"]["product"]["release_readiness_input"]["is_release_decision"] is False
        assert product_assembly["projection_version"] == PRODUCT_CANONICAL_PROJECTION_VERSION

        product_job = job_for(run_dir, "PROD-SEC", "canonical-product-replay", canonical_payload=True)
        product_resolved = VersionResolver().resolve("PROD-SEC")
        product_source = {path: json.loads((Path(__file__).parents[1] / path).read_text(encoding="utf-8"))
                          for path in EVIDENCE["PROD-SEC"]}
        product_payload, _ = FixtureCanonicalPayloadAdapter().generate(
            product_resolved["prompt_text"], {"designation": "PROD-SEC"}, 30)
        product_once = assemble_canonical_artifact(product_payload, product_job, product_resolved, product_source)
        product_twice = assemble_canonical_artifact(copy.deepcopy(product_payload), copy.deepcopy(product_job),
                                                    product_resolved, copy.deepcopy(product_source))
        assert product_once == product_twice

        accepted_spec_path = Path(__file__).parents[1] / "fixtures/vertical-risk-slice/evidence/canonical-spec-secrets-2026-07-31/accepted-spec-secrets.artifact.json"
        accepted_spec = json.loads(accepted_spec_path.read_text(encoding="utf-8"))
        accepted_product, _ = assemble_canonical_artifact(
            copy.deepcopy(product_payload), product_job, product_resolved,
            {str(accepted_spec_path): accepted_spec})
        validate_candidate(accepted_product, product_resolved, {str(accepted_spec_path): accepted_spec})
        assert accepted_product["inputs"][0]["artifact_id"] == accepted_spec["artifact"]["artifact_id"]

        canonical_override, canonical_override_dir, _ = process(
            base, run_dir, "PROD-SEC", "canonical-product-harness-override",
            CanonicalHarnessFieldOverrideAdapter(), ledger=ledger, canonical_payload=True)
        assert canonical_override["status"] == "failed" and canonical_override["artifact_path"] is None
        assert canonical_override["payload_path"] == "payload.json"
        assert not (canonical_override_dir / "artifact.json").exists()

        canonical_capability, canonical_capability_dir, _ = process(
            base, run_dir, "CAP-RISK", "canonical-cap-risk", FixtureCanonicalPayloadAdapter(),
            ledger=ledger, canonical_payload=True)
        assert canonical_capability["status"] == "complete", canonical_capability
        capability_artifact = json.loads((canonical_capability_dir / "artifact.json").read_text(encoding="utf-8"))
        capability_assembly = json.loads((canonical_capability_dir / "assembly.json").read_text(encoding="utf-8"))
        capability_layer = capability_artifact["extensions"]["capability"]
        assert capability_layer["role"]["designation"] == "CAP-RISK"
        assert capability_layer["capability_risk_posture"]["decision_authority"] == "human"
        assert capability_layer["capability_confidence_score"] == capability_artifact["confidence"]["assessment"]
        assert capability_assembly["projection_version"] == CAPABILITY_CANONICAL_PROJECTION_VERSION

        cap_job = job_for(run_dir, "CAP-RISK", "canonical-capability-replay", canonical_payload=True)
        cap_resolved = VersionResolver().resolve("CAP-RISK")
        cap_payload, _ = FixtureCanonicalPayloadAdapter().generate(cap_resolved["prompt_text"],
                                                                   {"designation": "CAP-RISK"}, 30)
        accepted_product_path = Path(__file__).parents[1] / "fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/accepted-prod-sec.artifact.json"
        accepted_product = json.loads(accepted_product_path.read_text(encoding="utf-8"))
        for risk in cap_payload["role_payload"]["risk_register"]:
            risk["contributing_artifacts"] = [accepted_product["artifact"]["artifact_id"]]
        cap_inputs = {str(accepted_product_path): accepted_product}
        cap_once = assemble_canonical_artifact(cap_payload, cap_job, cap_resolved, cap_inputs)
        cap_twice = assemble_canonical_artifact(copy.deepcopy(cap_payload), copy.deepcopy(cap_job),
                                                cap_resolved, copy.deepcopy(cap_inputs))
        assert cap_once == cap_twice
        validate_candidate(cap_once[0], cap_resolved, cap_inputs)
        assert cap_once[0]["inputs"][0]["artifact_id"] == accepted_product["artifact"]["artifact_id"]

        accepted_cap_path = Path(__file__).parents[1] / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-cap-risk.artifact.json"
        accepted_gate_path = Path(__file__).parents[1] / "fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/accepted-ent-evidence.artifact.json"
        accepted_cap = json.loads(accepted_cap_path.read_text(encoding="utf-8"))
        accepted_gate = json.loads(accepted_gate_path.read_text(encoding="utf-8"))
        rebuilt_gate = build_enterprise_evidence_artifact(copy.deepcopy(accepted_cap))
        assert rebuilt_gate == accepted_gate
        assert accepted_gate["inputs"][0]["artifact_id"] == accepted_cap["artifact"]["artifact_id"]
        assert accepted_gate["inputs"][0]["hash"] == accepted_cap["integrity"]["output_hash"]
        assert accepted_gate["extensions"]["enterprise"]["role"]["gate_state"] == "passed"

        canonical_enterprise, canonical_enterprise_dir, _ = process(
            base, run_dir, "ENT-SYSRISK", "canonical-ent-sysrisk", FixtureCanonicalPayloadAdapter(),
            ledger=ledger, canonical_payload=True)
        assert canonical_enterprise["status"] == "complete", canonical_enterprise
        enterprise_artifact = json.loads((canonical_enterprise_dir / "artifact.json").read_text(encoding="utf-8"))
        enterprise_assembly = json.loads((canonical_enterprise_dir / "assembly.json").read_text(encoding="utf-8"))
        enterprise_layer = enterprise_artifact["extensions"]["enterprise"]
        assert enterprise_layer["role"]["designation"] == "ENT-SYSRISK"
        assert enterprise_layer["role"]["decision_authority"] == "human"
        assert enterprise_artifact["decision_authority"] == "human"
        assert enterprise_assembly["projection_version"] == ENTERPRISE_CANONICAL_PROJECTION_VERSION

        ent_job = job_for(run_dir, "ENT-SYSRISK", "canonical-enterprise-replay", canonical_payload=True)
        ent_resolved = VersionResolver().resolve("ENT-SYSRISK")
        ent_payload, _ = FixtureCanonicalPayloadAdapter().generate(ent_resolved["prompt_text"],
                                                                   {"designation": "ENT-SYSRISK"}, 30)
        ent_inputs = {str(accepted_cap_path): accepted_cap, str(accepted_gate_path): accepted_gate}
        ent_once = assemble_canonical_artifact(ent_payload, ent_job, ent_resolved, ent_inputs)
        ent_twice = assemble_canonical_artifact(copy.deepcopy(ent_payload), copy.deepcopy(ent_job),
                                                ent_resolved, copy.deepcopy(ent_inputs))
        assert ent_once == ent_twice
        validate_candidate(ent_once[0], ent_resolved, ent_inputs)
        assert {item["artifact_id"] for item in ent_once[0]["inputs"]} == {
            accepted_cap["artifact"]["artifact_id"], accepted_gate["artifact"]["artifact_id"]}
        assert ent_once[0]["extensions"]["enterprise"]["capability_input_manifest"][0] == {
            "artifact_id": accepted_cap["artifact"]["artifact_id"],
            "gate_artifact_id": accepted_gate["artifact"]["artifact_id"], "state": "valid"}

        canonical_limited, canonical_limited_dir, _ = process(
            base, run_dir, "SPEC-SECRETS", "canonical-spec-secrets-limited",
            TruncatedCanonicalPayloadAdapter(), ledger=ledger, canonical_payload=True)
        assert canonical_limited["status"] == "failed" and canonical_limited["artifact_path"] is None
        limited_assembly = json.loads((canonical_limited_dir / "assembly.json").read_text(encoding="utf-8"))
        assert limited_assembly["generation_disclosure"]["limit_applied"] is True

        canonical_job = job_for(run_dir, "SPEC-SECRETS", "canonical-replay", canonical_payload=True)
        canonical_resolved = VersionResolver().resolve("SPEC-SECRETS")
        canonical_source = {path: json.loads((Path(__file__).parents[1] / path).read_text(encoding="utf-8"))
                            for path in EVIDENCE["SPEC-SECRETS"]}
        canonical_gold = json.loads((Path(__file__).parents[1] / "fixtures/vertical-risk-slice/gold/spec-secrets.artifact.json").read_text(encoding="utf-8"))
        canonical_payload = {"methodology": copy.deepcopy(canonical_gold["methodology"]),
                             "review_counts": copy.deepcopy(canonical_gold["coverage"]),
                             "findings": copy.deepcopy(canonical_gold["findings"]),
                             "secondary_records": [],
                             "confidence": copy.deepcopy(canonical_gold["confidence"]),
                             "decisions_requested": copy.deepcopy(canonical_gold["decisions_requested"])}
        canonical_payload["role_payload"] = copy.deepcopy(canonical_gold["extensions"]["specialist"]["role"])
        canonical_payload["generation_disclosure"] = {"omitted_item_estimate": 0,
                                                       "truncated_string_estimate": 0}
        projected_once = assemble_canonical_artifact(canonical_payload, canonical_job, canonical_resolved, canonical_source)
        projected_twice = assemble_canonical_artifact(copy.deepcopy(canonical_payload), copy.deepcopy(canonical_job),
                                                       canonical_resolved, copy.deepcopy(canonical_source))
        assert projected_once == projected_twice

        designation = "PROD-SEC"
        replay_job = job_for(run_dir, designation, "assembly-replay", role_payload=True)
        resolved = VersionResolver().resolve(designation)
        source_values = {path: json.loads((Path(__file__).parents[1] / path).read_text(encoding="utf-8")) for path in EVIDENCE[designation]}
        gold_product = json.loads((Path(__file__).parents[1] / "fixtures/vertical-risk-slice/gold/prod-sec.artifact.json").read_text(encoding="utf-8"))
        payload = {field: copy.deepcopy(gold_product[field]) for field in ANALYTICAL_FIELDS}
        payload["layer_payload"] = copy.deepcopy(gold_product["extensions"]["product"])
        payload["generation_disclosure"] = {"array_max_items": 3, "string_max_length": 256, "limit_applied": False, "omitted_item_estimate": 0, "truncated_string_estimate": 0}
        first_artifact, first_assembly = assemble_artifact(payload, replay_job, resolved, source_values)
        second_artifact, second_assembly = assemble_artifact(copy.deepcopy(payload), copy.deepcopy(replay_job), resolved, copy.deepcopy(source_values))
        assert first_artifact == second_artifact and first_assembly == second_assembly

        override, override_dir, _ = process(base, run_dir, "SPEC-SECRETS", "harness-field-override",
                                            HarnessFieldOverrideAdapter(), ledger=ledger, role_payload=True)
        assert override["status"] == "failed" and override["artifact_path"] is None
        assert override["payload_path"] == "payload.json" and not (override_dir / "artifact.json").exists()

        truncated, truncated_dir, _ = process(base, run_dir, "PROD-SEC", "truncated-role-payload",
                                               TruncatedRolePayloadAdapter(), ledger=ledger, role_payload=True)
        assert truncated["status"] == "failed" and truncated["artifact_path"] is None
        assert truncated["assembly_path"] == "assembly.json" and not (truncated_dir / "artifact.json").exists()

        spec_id = json.loads((base / "output-replace-spec-secrets" / job_for(run_dir, "SPEC-SECRETS", "replace-spec-secrets")["job_id"] / "artifact.json").read_text(encoding="utf-8"))["artifact"]["artifact_id"]
        assert ledger.get_index("artifact", spec_id)["object_hash"].startswith("sha256:")

        invalid, invalid_dir, _ = process(base, run_dir, "PROD-SEC", "invalid-output", InvalidAuthorityAdapter(), ledger=ledger)
        assert invalid["status"] == "failed" and invalid["artifact_path"] is None
        assert not (invalid_dir / "artifact.json").exists(), "invalid model output bypassed fan-in"

        flaky_adapter = FlakyAdapter()
        retried, retry_dir, _ = process(base, run_dir, "CAP-RISK", "retry", flaky_adapter, max_attempts=2)
        assert retried["status"] == "complete" and retried["attempt_count"] == 2 and flaky_adapter.calls == 2
        assert len(list(retry_dir.glob("artifact.json"))) == 1

        timed_out, timeout_dir, _ = process(base, run_dir, "SPEC-SECRETS", "timeout", AlwaysTimeoutAdapter(), max_attempts=2)
        assert timed_out["status"] == "failed" and timed_out["attempt_count"] == 2
        timeout_telemetry = json.loads((timeout_dir / "telemetry.json").read_text(encoding="utf-8"))
        assert len(timeout_telemetry["attempts"]) == 2

        counting = CountingAdapter()
        cancelled, cancel_dir, _ = process(base, run_dir, "ENT-SYSRISK", "cancel", counting, cancel=True)
        assert cancelled["status"] == "cancelled" and counting.calls == 0 and not (cancel_dir / "artifact.json").exists()

        denied = LeastPrivilegeEvidenceAdapter([EVIDENCE["SPEC-SECRETS"][0]])
        try:
            denied.read_json("fixtures/vertical-risk-slice/gold/prod-sec.artifact.json")
        except WorkerError as exc:
            assert "access denied" in str(exc)
        else:
            raise AssertionError("least-privilege evidence adapter allowed an undeclared path")

        missing_key_name = "CODE_HARNESS_TEST_MISSING_VLLM_KEY"
        os.environ.pop(missing_key_name, None)
        try:
            VLLMAdapter("http://127.0.0.1:8000", "qwen3-32b", missing_key_name).generate("prompt", {}, 1)
        except WorkerError as exc:
            assert "credential" in str(exc)
        else:
            raise AssertionError("vLLM adapter allowed an unauthenticated call")

        MockVLLMHandler.artifact = json.loads((Path(__file__).resolve().parents[1] / EVIDENCE["PROD-SEC"][0]).read_text(encoding="utf-8"))
        server = ThreadingHTTPServer(("127.0.0.1", 0), MockVLLMHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        # Environment injection may carry surrounding transport whitespace on Windows-to-Linux handoff.
        # The adapter must strip it before constructing the authorization header.
        os.environ["CODE_HARNESS_TEST_VLLM_KEY"] = " conformance-test-key\r"
        try:
            live_adapter = VLLMAdapter(f"http://127.0.0.1:{server.server_port}", "qwen3-32b", "CODE_HARNESS_TEST_VLLM_KEY")
            live_result, _, _ = process(base, run_dir, "SPEC-SECRETS", "vllm-protocol", live_adapter)
            assert live_result["status"] == "complete"
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            os.environ.pop("CODE_HARNESS_TEST_VLLM_KEY", None)

        queue = FileQueue(base / "idempotency-conflict")
        original = job_for(run_dir, "SPEC-SECRETS", "idempotency-conflict")
        queue.enqueue(original)
        changed = copy.deepcopy(original)
        changed["timeout_seconds"] = 31
        try:
            queue.enqueue(changed)
        except WorkerError as exc:
            assert "idempotency" in str(exc)
        else:
            raise AssertionError("idempotency-key content mutation was accepted")

        print(json.dumps({
            "suite": "worker-runtime-conformance",
            "one_node_replacements": replaced,
            "assembled_one_node_replacements": assembled_replaced,
            "deterministic_assembly_replay": "passed",
            "canonical_projection_replay": "passed",
            "canonical_product_projection": "passed",
            "canonical_product_projection_replay": "passed",
            "canonical_product_live_upstream_lineage": "passed",
            "canonical_capability_projection": "passed",
            "canonical_capability_projection_replay": "passed",
            "canonical_capability_live_upstream_lineage": "passed",
            "deterministic_enterprise_evidence_gate": "passed",
            "canonical_enterprise_projection": "passed",
            "canonical_enterprise_projection_replay": "passed",
            "canonical_enterprise_live_upstream_lineage": "passed",
            "canonical_worker_derived_limit": "passed",
            "harness_field_override_rejected": True,
            "cardinality_truncation_failed_closed": True,
            "fan_in_bypass_rejected": True,
            "retry_idempotency": "passed",
            "timeout": "passed",
            "cancellation": "passed",
            "least_privilege_tools": "passed",
            "telemetry_lineage": "passed",
            "vllm_auth_gate": "passed",
            "vllm_protocol": "passed",
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

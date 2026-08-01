#!/usr/bin/env python3
"""Reference worker, queue, version resolver, adapters, fan-in, and telemetry."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from artifact_ledger import ArtifactLedger, atomic_write, content_hash, pretty_bytes
from validate_vertical_slice import (FIXTURE_DIR, REGISTRY, ROOT, WORKFLOW, ValidationFailure, assert_schema,
                                     load_json, validate_artifact_payloads, validate_instance, validate_workflow)


PROMPT_MANIFEST = ROOT / "appendices" / "prompt-templates" / "candidates" / "manifest.json"
RUBRIC = ROOT / "appendices" / "rubrics" / "fixture-0.1.0.json"
TOOLCHAIN = ROOT / "appendices" / "tool-manifests" / "reference-toolchain-0.1.0.json"
GOLD = ROOT / "fixtures" / "vertical-risk-slice" / "gold"
WORKER_NAMESPACE = uuid.UUID("93000000-0000-4000-8000-000000000000")
GENERATION_CONTRACT_VERSION = "role-payload-1.3.0"
ASSEMBLER_VERSION = "deterministic-envelope-1.0.0"
CANONICAL_GENERATION_CONTRACT_VERSION = "canonical-role-payload-1.2.0"
CANONICAL_ASSEMBLER_VERSION = "deterministic-envelope-1.1.0"
CANONICAL_PROJECTION_VERSION = "specialist-analytical-projection-1.0.0"
CANONICAL_PROJECTION_MANIFEST = ROOT / "appendices" / "projection-manifests" / "specialist-analytical-projection-1.0.0.json"
PRODUCT_CANONICAL_GENERATION_CONTRACT_VERSION = "canonical-product-payload-1.0.0"
PRODUCT_CANONICAL_PROJECTION_VERSION = "product-analytical-projection-1.0.0"
PRODUCT_CANONICAL_PROJECTION_MANIFEST = ROOT / "appendices" / "projection-manifests" / "product-analytical-projection-1.0.0.json"
PRODUCT_SYNTH_CANONICAL_GENERATION_CONTRACT_VERSION = "canonical-product-synthesis-payload-1.0.0"
PRODUCT_SYNTH_CANONICAL_PROJECTION_VERSION = "product-synthesis-analytical-projection-1.0.0"
PRODUCT_SYNTH_CANONICAL_PROJECTION_MANIFEST = ROOT / "appendices" / "projection-manifests" / "product-synthesis-analytical-projection-1.0.0.json"
CAPABILITY_CANONICAL_GENERATION_CONTRACT_VERSION = "canonical-capability-risk-payload-1.0.0"
CAPABILITY_CANONICAL_PROJECTION_VERSION = "capability-risk-analytical-projection-1.0.0"
CAPABILITY_CANONICAL_PROJECTION_MANIFEST = ROOT / "appendices" / "projection-manifests" / "capability-risk-analytical-projection-1.0.0.json"
ENTERPRISE_CANONICAL_GENERATION_CONTRACT_VERSION = "canonical-enterprise-systemic-risk-payload-1.0.0"
ENTERPRISE_CANONICAL_PROJECTION_VERSION = "enterprise-systemic-risk-analytical-projection-1.0.0"
ENTERPRISE_CANONICAL_PROJECTION_MANIFEST = ROOT / "appendices" / "projection-manifests" / "enterprise-systemic-risk-analytical-projection-1.0.0.json"
GENERATION_ARRAY_MAX_ITEMS = 3
GENERATION_STRING_MAX_LENGTH = 256
ANALYTICAL_FIELDS = (
    "methodology", "coverage", "observations", "assessments", "findings", "patterns",
    "insights", "conflicts", "confidence", "decisions_requested",
)
ARTIFACT_TYPES = {
    "SPEC-SECRETS": "specialist-secrets-review",
    "PROD-SEC": "product-security-posture",
    "PROD-SYNTH": "product-engineering-posture",
    "CAP-RISK": "capability-risk-posture",
    "ENT-SYSRISK": "enterprise-systemic-risk-posture",
}


class WorkerError(Exception):
    pass


class RetryableAdapterError(WorkerError):
    pass


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(WORKER_NAMESPACE, "|".join(parts)))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VersionResolver:
    def __init__(self, model_pin_override: dict[str, Any] | None = None,
                 workflow_path: Path | None = None) -> None:
        self.workflow = load_json(workflow_path or WORKFLOW)
        self.registry = load_json(REGISTRY)
        self.prompt_manifest = load_json(PROMPT_MANIFEST)
        self.rubric = load_json(RUBRIC)
        self.toolchain = load_json(TOOLCHAIN)
        self.model_pin_override = copy.deepcopy(model_pin_override)

    def resolve(self, designation: str) -> dict[str, Any]:
        pins = self.workflow["version_pins"]
        if designation not in self.prompt_manifest["prompts"]:
            raise WorkerError(f"no candidate prompt registered for {designation}")
        prompt = self.prompt_manifest["prompts"][designation]
        expected_prompt = pins["prompts"].get(designation)
        if expected_prompt != self.prompt_manifest["prompt_version"]:
            raise WorkerError(f"prompt version mismatch for {designation}")
        prompt_path = ROOT / prompt["path"]
        if sha256_file(prompt_path) != prompt["sha256"]:
            raise WorkerError(f"prompt integrity mismatch for {designation}")
        if pins["rubrics"].get(designation) != self.rubric["version"]:
            raise WorkerError(f"rubric version mismatch for {designation}")
        if pins["toolchain"]["version"] != self.toolchain["version"]:
            raise WorkerError("toolchain version mismatch")
        agent = next((item for item in self.registry["agents"] if item["designation"] == designation), None)
        node = next((item for item in self.workflow["nodes"] if item["designation"] == designation), None)
        if not agent or not node:
            raise WorkerError(f"unregistered worker designation: {designation}")
        resolved = {
            "designation": designation,
            "agent": agent,
            "node": node,
            "prompt_version": expected_prompt,
            "prompt_path": prompt["path"],
            "prompt_sha256": prompt["sha256"],
            "prompt_text": prompt_path.read_text(encoding="utf-8"),
            "rubric_version": self.rubric["version"],
            "rubric_sha256": sha256_file(RUBRIC),
            "toolchain_version": self.toolchain["version"],
            "toolchain_sha256": sha256_file(TOOLCHAIN),
            "model": self.model_pin_override or pins["model"],
            "output_contract": {
                "universal": load_json(ROOT / "appendices" / "schemas" / "universal-agent-artifact.schema.json"),
                "layer": load_json(ROOT / "appendices" / "schemas" / node["output_schema"]),
                "role": load_json(ROOT / "appendices" / "schemas" / node["role_schema"]),
            },
            "rubric": self.rubric,
            "toolchain": self.toolchain,
            "workflow_id": self.workflow["workflow_id"],
            "workflow_version": self.workflow["workflow_version"],
        }
        resolved["generation_contract"] = build_generation_schema(resolved)
        resolved["generation_contract_version"] = GENERATION_CONTRACT_VERSION
        resolved["generation_contract_sha256"] = content_hash(resolved["generation_contract"])
        resolved["assembler_version"] = ASSEMBLER_VERSION
        if designation in {"SPEC-SECRETS", "PROD-SEC", "PROD-SYNTH", "CAP-RISK", "ENT-SYSRISK"}:
            resolved["canonical_generation_contract"] = build_canonical_generation_schema(resolved)
            resolved["canonical_generation_contract_version"] = {
                "SPEC-SECRETS": CANONICAL_GENERATION_CONTRACT_VERSION,
                "PROD-SEC": PRODUCT_CANONICAL_GENERATION_CONTRACT_VERSION,
                "PROD-SYNTH": PRODUCT_SYNTH_CANONICAL_GENERATION_CONTRACT_VERSION,
                "CAP-RISK": CAPABILITY_CANONICAL_GENERATION_CONTRACT_VERSION,
                "ENT-SYSRISK": ENTERPRISE_CANONICAL_GENERATION_CONTRACT_VERSION,
            }[designation]
            resolved["canonical_generation_contract_sha256"] = content_hash(resolved["canonical_generation_contract"])
            resolved["canonical_assembler_version"] = CANONICAL_ASSEMBLER_VERSION
            projection_path = {
                "SPEC-SECRETS": CANONICAL_PROJECTION_MANIFEST,
                "PROD-SEC": PRODUCT_CANONICAL_PROJECTION_MANIFEST,
                "PROD-SYNTH": PRODUCT_SYNTH_CANONICAL_PROJECTION_MANIFEST,
                "CAP-RISK": CAPABILITY_CANONICAL_PROJECTION_MANIFEST,
                "ENT-SYSRISK": ENTERPRISE_CANONICAL_PROJECTION_MANIFEST,
            }[designation]
            resolved["canonical_projection_version"] = {
                "SPEC-SECRETS": CANONICAL_PROJECTION_VERSION,
                "PROD-SEC": PRODUCT_CANONICAL_PROJECTION_VERSION,
                "PROD-SYNTH": PRODUCT_SYNTH_CANONICAL_PROJECTION_VERSION,
                "CAP-RISK": CAPABILITY_CANONICAL_PROJECTION_VERSION,
                "ENT-SYSRISK": ENTERPRISE_CANONICAL_PROJECTION_VERSION,
            }[designation]
            resolved["canonical_projection_sha256"] = "sha256:" + sha256_file(projection_path)
        return resolved


class LeastPrivilegeEvidenceAdapter:
    def __init__(self, allowed_paths: list[str]) -> None:
        self.allowed = {(ROOT / path).resolve() for path in allowed_paths}

    def read_json(self, relative_path: str) -> Any:
        path = (ROOT / relative_path).resolve()
        if path not in self.allowed:
            raise WorkerError(f"evidence access denied: {relative_path}")
        if ROOT not in path.parents or not path.is_file():
            raise WorkerError(f"evidence path invalid or missing: {relative_path}")
        return load_json(path)


class ModelAdapter:
    provider = "abstract"
    model_id = "abstract"

    def generate(self, prompt: str, context: dict[str, Any], timeout_seconds: int) -> tuple[dict[str, Any], dict[str, Any]]:
        raise NotImplementedError


class FixtureModelAdapter(ModelAdapter):
    provider = "fixture"
    model_id = "deterministic-reference-agent"
    FILES = {
        "SPEC-SECRETS": "spec-secrets.artifact.json",
        "PROD-SEC": "prod-sec.artifact.json",
        "CAP-RISK": "cap-risk.artifact.json",
        "ENT-SYSRISK": "ent-sysrisk.artifact.json",
    }

    def generate(self, prompt: str, context: dict[str, Any], timeout_seconds: int) -> tuple[dict[str, Any], dict[str, Any]]:
        designation = context["designation"]
        if not prompt.startswith(f"BEGIN {designation} PROMPT") or not prompt.rstrip().endswith(f"END {designation} PROMPT"):
            raise WorkerError("candidate prompt copy boundary is invalid")
        artifact = copy.deepcopy(load_json(GOLD / self.FILES[designation]))
        return artifact, {"input_tokens": len(prompt.split()), "output_tokens": len(json.dumps(artifact).split()), "cost_usd": 0.0}


class VLLMAdapter(ModelAdapter):
    provider = "vllm-openai-compatible"

    def __init__(self, base_url: str, model_id: str, api_key_env: str = "VLLM_API_KEY",
                 max_tokens: int | None = None, disable_thinking: bool = False,
                 use_json_schema: bool = False, guided_array_max_items: int | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.model_id = model_id
        self.api_key_env = api_key_env
        self.max_tokens = max_tokens
        self.disable_thinking = disable_thinking
        self.use_json_schema = use_json_schema
        self.guided_array_max_items = guided_array_max_items
        self.last_response_content: str | None = None

    def generate(self, prompt: str, context: dict[str, Any], timeout_seconds: int) -> tuple[dict[str, Any], dict[str, Any]]:
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise WorkerError(f"required model credential environment variable is unavailable: {self.api_key_env}")
        response_format: dict[str, Any] = {"type": "json_object"}
        if self.use_json_schema:
            inference_schema = context.get("generation_contract")
            if inference_schema is None:
                inference_schema = compose_output_schema(context["required_output_contract"], context["resolved_layer"])
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": f"{context['designation'].lower().replace('-', '_')}_artifact",
                    "schema": prepare_guided_schema(inference_schema, self.guided_array_max_items),
                    "strict": True,
                },
            }
        request_body = {
            "model": self.model_id,
            "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": json.dumps(context, sort_keys=True)}],
            "temperature": 0,
            "response_format": response_format,
        }
        if self.max_tokens is not None:
            request_body["max_tokens"] = self.max_tokens
        if self.disable_thinking:
            request_body["chat_template_kwargs"] = {"enable_thinking": False}
        request = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(request_body).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read(1000).decode("utf-8", errors="replace").replace("\r", " ").replace("\n", " ")
            if exc.code in {408, 429, 500, 502, 503, 504}:
                raise RetryableAdapterError(f"vLLM retryable HTTP status {exc.code}: {detail}") from exc
            raise WorkerError(f"vLLM rejected request with HTTP status {exc.code}: {detail}") from exc
        except (TimeoutError, urllib.error.URLError) as exc:
            raise RetryableAdapterError(f"vLLM transport failure: {exc}") from exc
        content = payload["choices"][0]["message"]["content"]
        self.last_response_content = content
        artifact = json.loads(content)
        usage = payload.get("usage", {})
        return artifact, {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
            "cost_usd": 0.0,
        }


class FileQueue:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def enqueue(self, job: dict[str, Any]) -> dict[str, Any]:
        assert_schema(job, "worker-job.schema.json", "worker job")
        job_hash = content_hash(job)
        key = hashlib.sha256(job["idempotency_key"].encode("utf-8")).hexdigest()
        index = self.root / "idempotency" / f"{key}.json"
        binding = {"idempotency_key": job["idempotency_key"], "job_id": job["job_id"], "job_hash": job_hash}
        if index.exists():
            existing = json.loads(index.read_text(encoding="utf-8"))
            if existing != binding:
                raise WorkerError("idempotency-key reuse with different job content")
            return existing
        target = self.root / "pending" / f"{job['job_id']}.json"
        atomic_write(target, pretty_bytes(job))
        atomic_write(index, pretty_bytes(binding))
        return binding

    def request_cancellation(self, job_id: str, reason: str) -> None:
        record = {"job_id": job_id, "reason": reason}
        path = self.root / "cancellations" / f"{job_id}.json"
        if path.exists() and json.loads(path.read_text(encoding="utf-8")) != record:
            raise WorkerError("cancellation record mutation rejected")
        if not path.exists():
            atomic_write(path, pretty_bytes(record))

    def is_cancelled(self, job_id: str) -> bool:
        return (self.root / "cancellations" / f"{job_id}.json").exists()

    def lease_next(self, worker_id: str) -> tuple[dict[str, Any], Path] | None:
        for path in sorted((self.root / "pending").glob("*.json")) if (self.root / "pending").exists() else []:
            leased = self.root / "leased" / worker_id / path.name
            leased.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.replace(path, leased)
            except FileNotFoundError:
                continue
            return json.loads(leased.read_text(encoding="utf-8")), leased
        return None

    def finish(self, leased_path: Path, status: str) -> None:
        target = self.root / status / leased_path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(leased_path, target)


def inline_local_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """Inline local $defs references so a role schema can be embedded safely."""
    source = copy.deepcopy(schema)
    definitions = source.get("$defs", {})

    def visit(value: Any) -> Any:
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str) and reference.startswith("#/$defs/"):
                name = reference.removeprefix("#/$defs/")
                if name not in definitions:
                    raise WorkerError(f"unresolved local schema reference: {reference}")
                return visit(copy.deepcopy(definitions[name]))
            return {key: visit(item) for key, item in value.items() if key not in {"$schema", "$id", "$defs"}}
        if isinstance(value, list):
            return [visit(item) for item in value]
        return value

    return visit(source)


def compose_output_schema(contract: dict[str, Any], layer: str) -> dict[str, Any]:
    """Compose universal, layer, and role schemas into one inference boundary."""
    universal = inline_local_refs(contract["universal"])
    layer_schema = inline_local_refs(contract["layer"])
    role_schema = inline_local_refs(contract["role"])
    layer_schema.setdefault("properties", {})["role"] = role_schema
    universal["properties"]["extensions"] = {
        "type": "object",
        "additionalProperties": False,
        "required": [layer],
        "properties": {layer: layer_schema},
    }
    return universal


def build_generation_schema(resolved: dict[str, Any]) -> dict[str, Any]:
    """Build the compact analytical payload contract used by role_payload_v1."""
    universal = inline_local_refs(resolved["output_contract"]["universal"])
    layer_schema = inline_local_refs(resolved["output_contract"]["layer"])
    layer_schema.setdefault("properties", {})["role"] = inline_local_refs(resolved["output_contract"]["role"])
    properties = {field: copy.deepcopy(universal["properties"][field]) for field in ANALYTICAL_FIELDS}
    properties["layer_payload"] = layer_schema
    properties["generation_disclosure"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["array_max_items", "string_max_length", "limit_applied", "omitted_item_estimate", "truncated_string_estimate"],
        "properties": {
            "array_max_items": {"const": GENERATION_ARRAY_MAX_ITEMS},
            "string_max_length": {"const": GENERATION_STRING_MAX_LENGTH},
            "limit_applied": {"type": "boolean"},
            "omitted_item_estimate": {"type": ["integer", "null"], "minimum": 0},
            "truncated_string_estimate": {"type": ["integer", "null"], "minimum": 0},
        },
    }
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{resolved['designation']} analytical generation payload",
        "type": "object",
        "additionalProperties": False,
        "required": [*ANALYTICAL_FIELDS, "layer_payload", "generation_disclosure"],
        "properties": properties,
    }
    return prepare_guided_schema(schema, GENERATION_ARRAY_MAX_ITEMS, GENERATION_STRING_MAX_LENGTH)


def build_canonical_generation_schema(resolved: dict[str, Any]) -> dict[str, Any]:
    """Build one canonical analytical form without the duplicative layer extension."""
    if resolved["designation"] not in {"SPEC-SECRETS", "PROD-SEC", "PROD-SYNTH", "CAP-RISK", "ENT-SYSRISK"}:
        raise WorkerError("canonical analytical projection is unavailable for this designation")
    root_causes = ["design_flaw", "implementation_defect", "configuration_error", "process_or_governance_gap",
                   "dependency_or_supplier_issue", "insufficient_observability", "external_constraint", "unknown"]
    properties = {
        "methodology": {"type": "object", "additionalProperties": False, "required": ["method", "limitations"],
                        "properties": {"method": {"type": "string", "minLength": 1},
                                       "limitations": {"type": "array", "items": {"type": "string"}}}},
        "review_counts": {"type": "object", "additionalProperties": False,
                          "required": ["eligible", "reviewed", "omitted", "inaccessible", "unknown", "negative_evidence"],
                          "properties": {key: {"type": "integer", "minimum": 0} for key in
                                         ("eligible", "reviewed", "omitted", "inaccessible", "unknown", "negative_evidence")}},
        "findings": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                     "required": ["finding_id", "statement", "evidence_refs", "root_cause", "impact", "capa"],
                     "properties": {
                         "finding_id": {"type": "string", "minLength": 1}, "statement": {"type": "string", "minLength": 1},
                         "evidence_refs": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                         "root_cause": {"enum": root_causes}, "impact": {"type": "string", "minLength": 1},
                         "capa": {"type": "object", "additionalProperties": False,
                                  "required": ["corrective_action", "preventive_action", "owner_role", "target_horizon", "implementation_level", "validation_method"],
                                  "properties": {key: {"type": "string", "minLength": 1} for key in
                                                 ("corrective_action", "preventive_action", "owner_role", "target_horizon", "implementation_level", "validation_method")},
                                  },
                     }}},
        "secondary_records": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                              "required": ["kind", "record_id", "statement", "evidence_refs"],
                              "properties": {"kind": {"enum": ["pattern", "insight", "conflict"]},
                                             "record_id": {"type": "string", "minLength": 1},
                                             "statement": {"type": "string", "minLength": 1},
                                             "evidence_refs": {"type": "array", "items": {"type": "string"}}}}},
        "confidence": {"type": "object", "additionalProperties": False,
                       "required": ["evidence", "assessment", "review", "decision", "provenance"],
                       "properties": {"evidence": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                                      "assessment": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                                      "review": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                                      "decision": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                                      "provenance": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                     "required": ["source", "version"],
                                                     "properties": {"source": {"type": "string", "minLength": 1},
                                                                    "version": {"type": "string", "minLength": 1}}}}}},
        "decisions_requested": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                "required": ["decision_context_id", "question", "required_authority"],
                                "properties": {"decision_context_id": {"type": "string", "minLength": 1},
                                               "question": {"type": "string", "minLength": 1},
                                               "required_authority": {"type": "string", "minLength": 1}}}},
        "role_payload": inline_local_refs(resolved["output_contract"]["role"]),
    }
    required = ["methodology", "review_counts", "findings", "secondary_records", "confidence",
                "decisions_requested", "role_payload", "generation_disclosure"]
    if resolved["designation"] == "CAP-RISK":
        properties["layer_context"] = {
            "type": "object", "additionalProperties": False,
            "required": ["mission_thread", "requirement_traceability", "cross_product_interface_state",
                         "human_centered_systems_evaluation", "mission_effectiveness_evidence", "operational_readiness"],
            "properties": {
                "mission_thread": {"type": "object"},
                "requirement_traceability": {"type": "object"},
                "cross_product_interface_state": {"type": "object"},
                "human_centered_systems_evaluation": {"type": "object"},
                "mission_effectiveness_evidence": {"type": "array", "items": {"type": "object"}},
                "operational_readiness": {"type": "object"},
            },
        }
        required.insert(-2, "layer_context")
    if resolved["designation"] == "ENT-SYSRISK":
        properties["layer_context"] = {
            "type": "object", "additionalProperties": False,
            "required": ["enterprise_scope", "cross_capability_correlations", "enterprise_assertions",
                         "systemic_dependencies"],
            "properties": {
                "enterprise_scope": {"type": "object"},
                "cross_capability_correlations": {"type": "array", "items": {"type": "object"}},
                "enterprise_assertions": {"type": "array", "items": {"type": "object"}},
                "systemic_dependencies": {"type": "array", "items": {"type": "object"}},
            },
        }
        required.insert(-2, "layer_context")
    properties["generation_disclosure"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["omitted_item_estimate", "truncated_string_estimate"],
        "properties": {
            "omitted_item_estimate": {"type": "integer", "minimum": 0},
            "truncated_string_estimate": {"type": "integer", "minimum": 0},
        },
    }
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{resolved['designation']} canonical analytical generation payload",
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }
    return prepare_guided_schema(schema, GENERATION_ARRAY_MAX_ITEMS, GENERATION_STRING_MAX_LENGTH)


def project_specialist_layer(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any]) -> dict[str, Any]:
    """Project the specialist extension from one canonical analysis without semantic invention."""
    manifest = load_json(CANONICAL_PROJECTION_MANIFEST)
    if manifest["projection_version"] != CANONICAL_PROJECTION_VERSION:
        raise WorkerError("canonical projection manifest version mismatch")
    scope = job["dispatch"].get("scope", {})
    coverage = payload["review_counts"]
    role_observations = payload["role_payload"]["secret_observations"]
    observations = [{"observation_id": item["observation_id"],
                     "fact": f"{item['evidence_state']}: {item['secret_type']} at {item['exposure_location']}.",
                     "evidence_refs": copy.deepcopy(item["evidence_refs"])} for item in role_observations]
    assessments = [{"assessment_id": f"ASM-{item['observation_id']}",
                    "rationale": f"Classification is {item['evidence_state']} based on the cited redacted evidence.",
                    "confidence": payload["confidence"].get("assessment")} for item in role_observations]
    secondary = payload["secondary_records"]

    payload["coverage"] = copy.deepcopy(coverage)
    payload["observations"] = observations
    payload["assessments"] = assessments
    payload["patterns"] = [{"pattern_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "pattern"]
    payload["insights"] = [{"insight_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "insight"]
    payload["conflicts"] = [{"conflict_id": item["record_id"], "statement": item["statement"],
                             "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                            for item in secondary if item["kind"] == "conflict"]

    def references(records: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
        return [{key: record[key]} for record in records if isinstance(record, dict) and key in record]

    return {
        "product_id": scope.get("product_id", "unknown"),
        "domain_scope": {"domain": "secrets", "source_revision": scope.get("source_revision", "unknown")},
        "eligible_population": {
            "eligible": coverage.get("eligible"),
            "reviewed": coverage.get("reviewed"),
            "omitted": coverage.get("omitted"),
            "inaccessible": coverage.get("inaccessible"),
            "unknown": coverage.get("unknown"),
        },
        "domain_observations": references(payload["observations"], "observation_id"),
        "domain_assessments": references(payload["assessments"], "assessment_id"),
        "domain_findings": references(payload["findings"], "finding_id"),
        "domain_patterns": references(payload["patterns"], "pattern_id"),
        "domain_unknowns": copy.deepcopy(payload["conflicts"]),
        "domain_coverage": copy.deepcopy(coverage),
        "domain_confidence": {
            "evidence": payload["confidence"].get("evidence"),
            "assessment": payload["confidence"].get("assessment"),
            "review": payload["confidence"].get("review"),
        },
        "product_consumers": copy.deepcopy(resolved["node"].get("consumers", [])),
        "role": copy.deepcopy(payload["role_payload"]),
    }


def project_product_layer(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                          input_values: dict[str, Any]) -> dict[str, Any]:
    """Project the product extension from canonical synthesis and immutable specialist inputs."""
    manifest = load_json(PRODUCT_CANONICAL_PROJECTION_MANIFEST)
    if manifest["projection_version"] != PRODUCT_CANONICAL_PROJECTION_VERSION:
        raise WorkerError("product canonical projection manifest version mismatch")
    role = payload["role_payload"]
    correlations = role["security_domain_correlations"]
    paths = role["attack_path_hypotheses"]
    payload["coverage"] = copy.deepcopy(payload["review_counts"])
    payload["observations"] = [
        {"observation_id": f"OBS-{item['record_id']}", "fact": item["rationale"],
         "evidence_refs": [*item["contributing_artifact_ids"], *item["contributing_evidence_ids"]]}
        for item in correlations
    ]
    payload["assessments"] = [
        {"assessment_id": f"ASM-{item['record_id']}", "rationale": item["rationale"],
         "confidence": item.get("confidence")}
        for item in paths
    ]
    secondary = payload["secondary_records"]
    payload["patterns"] = [{"pattern_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "pattern"]
    payload["insights"] = [{"insight_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "insight"]
    payload["conflicts"] = [{"conflict_id": item["record_id"], "statement": item["statement"],
                             "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                            for item in secondary if item["kind"] == "conflict"]
    inventory = []
    for value in input_values.values():
        if isinstance(value, dict) and isinstance(value.get("artifact"), dict):
            inventory.append({"artifact_id": value["artifact"]["artifact_id"],
                              "designation": value.get("identity", {}).get("designation", "UNKNOWN"),
                              "state": "valid_present"})
    required = len(resolved["node"].get("required_inputs", []))
    valid = len(inventory)
    evidence_score = payload["confidence"].get("evidence")
    evidence_state = "unknown" if evidence_score is None else ("high" if evidence_score >= 0.8 else "limited")
    decisions = payload["decisions_requested"]
    return {
        "product_id": job["dispatch"].get("scope", {}).get("product_id", "unknown"),
        "specialist_artifact_inventory": inventory,
        "input_completeness": {"required": required, "valid": valid,
                               "fraction": (valid / required if required else 1.0)},
        "cross_domain_correlations": [{"record_id": item["record_id"]} for item in correlations],
        "unresolved_conflicts": copy.deepcopy(payload["conflicts"]),
        "product_findings": [{"finding_id": item["finding_id"]} for item in payload["findings"]],
        "product_patterns": [{"pattern_id": item["pattern_id"]} for item in payload["patterns"]],
        "product_risk_posture": {**copy.deepcopy(role["security_posture"]), "decision_authority": "human"},
        "technical_confidence": payload["confidence"].get("assessment"),
        "coverage": {"required_domains": required, "reviewed_domains": valid},
        "evidence_quality": {"state": evidence_state, "score": evidence_score},
        "release_readiness_input": {"state": ("blocked_pending_human_decision" if decisions else "advisory_no_decision_requested"),
                                    "is_release_decision": False},
        "escalations": [{"escalation_id": item["decision_context_id"],
                         "authority": item["required_authority"]} for item in decisions],
        "role": copy.deepcopy(role),
    }


def project_product_synthesis_layer(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                                    input_values: dict[str, Any]) -> dict[str, Any]:
    """Project PROD-SYNTH while retaining child meaning and owning all lineage fields."""
    manifest = load_json(PRODUCT_SYNTH_CANONICAL_PROJECTION_MANIFEST)
    if manifest["projection_version"] != PRODUCT_SYNTH_CANONICAL_PROJECTION_VERSION:
        raise WorkerError("product-synthesis canonical projection manifest version mismatch")
    children = [value for value in input_values.values()
                if isinstance(value, dict) and isinstance(value.get("artifact"), dict)]
    if len(children) != 1 or children[0].get("identity", {}).get("designation") != "PROD-SEC":
        raise WorkerError("PROD-SYNTH calibration requires exactly one immutable PROD-SEC child")
    child = children[0]
    child_id = child["artifact"]["artifact_id"]
    if child.get("artifact", {}).get("lifecycle_state") != "complete":
        raise WorkerError("PROD-SYNTH child must be complete")
    record_map: dict[str, dict[str, Any]] = {}
    for field, key in (("observations", "observation_id"), ("assessments", "assessment_id"),
                       ("findings", "finding_id"), ("patterns", "pattern_id"),
                       ("insights", "insight_id"), ("conflicts", "conflict_id"),
                       ("decisions_requested", "decision_context_id")):
        for record in child.get(field, []):
            if key in record:
                record_map[record[key]] = record
    role = copy.deepcopy(payload["role_payload"])
    preserved_ids: set[str] = set()
    preserved_finding_ids: set[str] = set()
    preserved_evidence_refs: set[str] = set()
    for assertion in role["preserved_child_assertions"]:
        if assertion["source_artifact_id"] != child_id or assertion["source_record_id"] not in record_map:
            raise WorkerError("PROD-SYNTH preserved assertion does not resolve to the declared child")
        source = record_map[assertion["source_record_id"]]
        source_refs = set(source.get("evidence_refs", []))
        if not set(assertion["evidence_refs"]).issubset(source_refs):
            raise WorkerError("PROD-SYNTH preserved assertion changed child evidence references")
        preserved_ids.add(assertion["source_record_id"])
        preserved_evidence_refs.update(assertion["evidence_refs"])
        if assertion["record_kind"] == "finding":
            preserved_finding_ids.add(assertion["source_record_id"])
    for assertion in role["derived_product_assertions"]:
        if set(assertion["contributing_artifact_ids"]) != {child_id}:
            raise WorkerError("PROD-SYNTH derived assertion contains invented artifact lineage")
        if not set(assertion["contributing_record_ids"]).issubset(preserved_ids):
            raise WorkerError("PROD-SYNTH derived assertion cites an unpreserved child record")
    allowed_refs = {child_id, *record_map.keys(), *preserved_evidence_refs}
    for finding in payload["findings"]:
        if not set(finding["evidence_refs"]).issubset(allowed_refs):
            raise WorkerError("PROD-SYNTH finding contains invented evidence lineage")
    input_confidence = child.get("confidence", {}).get("assessment")
    confidence_inputs = [input_confidence] if isinstance(input_confidence, (int, float)) else []
    result_confidence = payload["confidence"].get("assessment")
    artifact_id = stable_uuid(job["job_id"], "assembled-artifact")
    product_id = job["dispatch"].get("scope", {}).get("product_id", "unknown")
    decisions = payload["decisions_requested"]
    role["synthesis_basis"] = {"required_designations": ["PROD-SEC"], "received_artifact_ids": [child_id],
                               "completeness_state": "complete", "partial_input_authorization": None}
    role["confidence_reconciliation"] = {"method": "preserve_child_and_canonical_assessment",
                                         "input_values": confidence_inputs or [result_confidence or 0.0],
                                         "result": result_confidence,
                                         "uncertainty": copy.deepcopy(role["confidence_reconciliation"].get("uncertainty", []))}
    role["capability_handoff"] = {"product_id": product_id, "artifact_id": artifact_id,
                                  "preserved_finding_ids": sorted(preserved_finding_ids),
                                  "preserved_evidence_refs": sorted(preserved_evidence_refs),
                                  "unresolved_conflict_ids": sorted(item["record_id"] for item in payload["secondary_records"] if item["kind"] == "conflict"),
                                  "escalation_ids": sorted(item["decision_context_id"] for item in decisions),
                                  "intended_consumers": copy.deepcopy(resolved["node"]["consumers"]),
                                  "handoff_state": "ready_for_capability_fan_in"}
    role["decision_authority"] = "human"
    payload["coverage"] = copy.deepcopy(payload["review_counts"])
    payload["observations"] = [{"observation_id": f"OBS-PRESERVED-{index:03d}",
                                "fact": f"Preserved {item['record_kind']} {item['source_record_id']} from child {child_id}.",
                                "evidence_refs": [child_id, *item["evidence_refs"]]}
                               for index, item in enumerate(role["preserved_child_assertions"], 1)]
    payload["assessments"] = [{"assessment_id": item["assertion_id"], "rationale": item["correlation_logic"],
                               "confidence": item["confidence"]} for item in role["derived_product_assertions"]]
    secondary = payload["secondary_records"]
    payload["patterns"] = [{"pattern_id": item["record_id"], "statement": item["statement"], "evidence_refs": item["evidence_refs"]}
                           for item in secondary if item["kind"] == "pattern"]
    payload["insights"] = [{"insight_id": item["record_id"], "statement": item["statement"], "evidence_refs": item["evidence_refs"]}
                           for item in secondary if item["kind"] == "insight"]
    payload["conflicts"] = [{"conflict_id": item["record_id"], "statement": item["statement"], "evidence_refs": item["evidence_refs"]}
                            for item in secondary if item["kind"] == "conflict"]
    evidence_score = payload["confidence"].get("evidence")
    return {
        "product_id": product_id,
        "specialist_artifact_inventory": [{"artifact_id": child_id, "designation": "PROD-SEC", "state": "valid_present"}],
        "input_completeness": {"required": 1, "valid": 1, "fraction": 1.0, "policy": "PROD-SYNTH-CALIBRATION-0.1.0"},
        "cross_domain_correlations": [{"assertion_id": item["assertion_id"], "contributing_artifact_ids": item["contributing_artifact_ids"]}
                                      for item in role["derived_product_assertions"]],
        "unresolved_conflicts": copy.deepcopy(payload["conflicts"]),
        "product_findings": [{"finding_id": item["finding_id"]} for item in payload["findings"]],
        "product_patterns": [{"pattern_id": item["pattern_id"]} for item in payload["patterns"]],
        "product_risk_posture": {"state": role["engineering_posture"]["state"], "advisory_only": True,
                                 "decision_authority": "human"},
        "technical_confidence": result_confidence,
        "coverage": {"required_domains": 1, "reviewed_domains": 1, "candidate_calibration": True},
        "evidence_quality": {"state": "high" if isinstance(evidence_score, (int, float)) and evidence_score >= 0.8 else "limited",
                             "score": evidence_score},
        "release_readiness_input": {"state": "human_review_required" if decisions else "advisory_no_decision_requested",
                                    "is_release_decision": False},
        "escalations": [{"escalation_id": item["decision_context_id"], "authority": item["required_authority"]}
                        for item in decisions],
        "role": role,
    }


def project_capability_risk_layer(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                                  input_values: dict[str, Any]) -> dict[str, Any]:
    """Project capability context and risk rollups without making a risk disposition."""
    manifest = load_json(CAPABILITY_CANONICAL_PROJECTION_MANIFEST)
    if manifest["projection_version"] != CAPABILITY_CANONICAL_PROJECTION_VERSION:
        raise WorkerError("capability-risk canonical projection manifest version mismatch")
    role = payload["role_payload"]
    risks = role["risk_register"]
    context = payload["layer_context"]
    payload["coverage"] = copy.deepcopy(payload["review_counts"])
    payload["observations"] = [
        {"observation_id": f"OBS-{risk['risk_id']}", "fact": risk["risk_statement"],
         "evidence_refs": copy.deepcopy(risk["contributing_artifacts"])} for risk in risks
    ]
    payload["assessments"] = [
        {"assessment_id": f"ASM-{risk['risk_id']}",
         "rationale": f"{risk['likelihood_basis']} {risk['impact_basis']}",
         "confidence": risk.get("confidence")} for risk in risks
    ]
    secondary = payload["secondary_records"]
    payload["patterns"] = [{"pattern_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "pattern"]
    payload["insights"] = [{"insight_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "insight"]
    payload["conflicts"] = [{"conflict_id": item["record_id"], "statement": item["statement"],
                             "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                            for item in secondary if item["kind"] == "conflict"]
    input_confidences = []
    for value in input_values.values():
        if isinstance(value, dict):
            score = value.get("confidence", {}).get("assessment")
            if isinstance(score, (int, float)):
                input_confidences.append(score)
    result_confidence = payload["confidence"].get("assessment")
    scope = job["dispatch"].get("scope", {})
    participating = scope.get("participating_products") or [
        value.get("scope", {}).get("product_id") for value in input_values.values()
        if isinstance(value, dict) and value.get("scope", {}).get("product_id")
    ]
    readiness_state = context["operational_readiness"].get("state", "unknown")
    return {
        "capability_id": scope.get("capability_id", "unknown"),
        "participating_products": participating,
        "mission_thread": copy.deepcopy(context["mission_thread"]),
        "requirement_traceability": copy.deepcopy(context["requirement_traceability"]),
        "cross_product_interface_state": copy.deepcopy(context["cross_product_interface_state"]),
        "human_centered_systems_evaluation": copy.deepcopy(context["human_centered_systems_evaluation"]),
        "mission_effectiveness_evidence": copy.deepcopy(context["mission_effectiveness_evidence"]),
        "operational_readiness": copy.deepcopy(context["operational_readiness"]),
        "capability_risk_posture": {"state": readiness_state, "risk_ids": [risk["risk_id"] for risk in risks],
                                    "decision_authority": "human"},
        "technical_confidence_rollup": {"method": "preserve_inputs_and_canonical_assessment",
                                        "inputs": input_confidences, "result": result_confidence},
        "capability_confidence_score": result_confidence,
        "decision_conflicts": copy.deepcopy(payload["conflicts"]),
        "enterprise_escalations": copy.deepcopy(role["escalation_flags"]),
        "role": copy.deepcopy(role),
    }


def project_enterprise_systemic_risk_layer(payload: dict[str, Any], job: dict[str, Any],
                                            resolved: dict[str, Any],
                                            input_values: dict[str, Any]) -> dict[str, Any]:
    """Project enterprise risk context while preserving the human disposition boundary."""
    manifest = load_json(ENTERPRISE_CANONICAL_PROJECTION_MANIFEST)
    if manifest["projection_version"] != ENTERPRISE_CANONICAL_PROJECTION_VERSION:
        raise WorkerError("enterprise systemic-risk canonical projection manifest version mismatch")
    role = payload["role_payload"]
    risks = role["systemic_risk_register"]
    context = payload["layer_context"]
    payload["coverage"] = copy.deepcopy(payload["review_counts"])
    payload["observations"] = [
        {"observation_id": f"OBS-{risk['enterprise_risk_id']}", "fact": risk["risk_statement"],
         "evidence_refs": copy.deepcopy(risk["evidence_refs"])} for risk in risks
    ]
    payload["assessments"] = [
        {"assessment_id": f"ASM-{risk['enterprise_risk_id']}",
         "rationale": f"{risk['probability_basis']} {risk['consequence_basis']}",
         "confidence": payload["confidence"].get("assessment")} for risk in risks
    ]
    secondary = payload["secondary_records"]
    payload["patterns"] = [{"pattern_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "pattern"]
    payload["insights"] = [{"insight_id": item["record_id"], "statement": item["statement"],
                            "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                           for item in secondary if item["kind"] == "insight"]
    payload["conflicts"] = [{"conflict_id": item["record_id"], "statement": item["statement"],
                             "evidence_refs": copy.deepcopy(item["evidence_refs"])}
                            for item in secondary if item["kind"] == "conflict"]

    cap_inputs = [value for value in input_values.values()
                  if isinstance(value, dict) and value.get("identity", {}).get("designation") == "CAP-RISK"]
    gate_inputs = [value for value in input_values.values()
                   if isinstance(value, dict) and value.get("identity", {}).get("designation") == "ENT-EVIDENCE"]
    if len(cap_inputs) != 1 or len(gate_inputs) != 1:
        raise WorkerError("ENT-SYSRISK canonical projection requires exactly one CAP-RISK and one ENT-EVIDENCE input")
    capability, gate = cap_inputs[0], gate_inputs[0]
    cap_id = capability["artifact"]["artifact_id"]
    gate_id = gate["artifact"]["artifact_id"]
    capability_id = capability.get("scope", {}).get("capability_id", "unknown")
    input_confidences = [value.get("confidence", {}).get("assessment") for value in (capability, gate)]
    result_confidence = payload["confidence"].get("assessment")
    risk_ids = [risk["enterprise_risk_id"] for risk in risks]
    contributing_risk_ids = sorted({risk_id for risk in risks for risk_id in risk["contributing_risk_ids"]})
    unknowns = sorted({unknown for risk in risks for unknown in risk["unknowns"]})
    decisions = payload["decisions_requested"]
    return {
        "enterprise_scope": copy.deepcopy(context["enterprise_scope"]),
        "participating_capabilities": [capability_id],
        "capability_input_manifest": [{"artifact_id": cap_id, "gate_artifact_id": gate_id, "state": "valid"}],
        "cross_capability_correlations": copy.deepcopy(context["cross_capability_correlations"]),
        "enterprise_assertions": copy.deepcopy(context["enterprise_assertions"]),
        "systemic_dependencies": copy.deepcopy(context["systemic_dependencies"]),
        "enterprise_unknowns": [{"unknown_id": f"UNKNOWN-ENT-{index:03d}", "statement": item}
                                for index, item in enumerate(unknowns, 1)],
        "unresolved_disagreements": copy.deepcopy(payload["conflicts"]),
        "confidence_reconciliation": {"method": "preserve_inputs_and_canonical_assessment",
                                      "inputs": input_confidences, "result": result_confidence,
                                      "uncertainty": unknowns},
        "human_decision_requests": [{"decision_context_id": item["decision_context_id"],
                                     "authority": item["required_authority"]} for item in decisions],
        "enterprise_traceability_manifest": {"artifact_ids": [cap_id, gate_id],
                                             "risk_ids": [*contributing_risk_ids, *risk_ids]},
        "role": copy.deepcopy(role),
    }


def project_canonical_layer(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                            input_values: dict[str, Any]) -> dict[str, Any]:
    if resolved["designation"] == "SPEC-SECRETS":
        return project_specialist_layer(payload, job, resolved)
    if resolved["designation"] == "PROD-SEC":
        return project_product_layer(payload, job, resolved, input_values)
    if resolved["designation"] == "PROD-SYNTH":
        return project_product_synthesis_layer(payload, job, resolved, input_values)
    if resolved["designation"] == "CAP-RISK":
        return project_capability_risk_layer(payload, job, resolved, input_values)
    if resolved["designation"] == "ENT-SYSRISK":
        return project_enterprise_systemic_risk_layer(payload, job, resolved, input_values)
    raise WorkerError("canonical projection is unavailable for this designation")


def validate_generation_payload(payload: dict[str, Any], resolved: dict[str, Any]) -> None:
    schema = resolved["generation_contract"]
    errors = validate_instance(payload, schema, schema)
    if errors:
        formatted = "\n  - ".join(errors)
        raise ValidationFailure(f"generation payload {resolved['designation']} failed {GENERATION_CONTRACT_VERSION}:\n  - {formatted}")


def assemble_artifact(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                      input_values: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Deterministically assemble harness-owned fields around an analytical payload."""
    validate_generation_payload(payload, resolved)
    designation = resolved["designation"]
    layer = resolved["node"]["layer"]
    inputs = []
    child_ids = []
    for value in input_values.values():
        if isinstance(value, dict) and isinstance(value.get("artifact"), dict) and isinstance(value.get("integrity"), dict):
            artifact_id = value["artifact"]["artifact_id"]
            child_ids.append(artifact_id)
            inputs.append({
                "artifact_id": artifact_id,
                "hash": value["integrity"]["output_hash"],
                "compatibility": "compatible",
                "freshness": "fresh",
            })
    if not inputs:
        inputs = copy.deepcopy(job["dispatch"].get("input_manifest", []))
    artifact_id = stable_uuid(job["job_id"], "assembled-artifact")
    disclosure = copy.deepcopy(payload["generation_disclosure"])
    coverage = copy.deepcopy(payload["coverage"])
    coverage["generation_limit"] = disclosure
    artifact = {
        "identity": {
            "agent_uuid": resolved["agent"]["agent_uuid"],
            "designation": designation,
            "display_name": resolved["agent"]["display_name"],
            "agent_version": resolved["agent"].get("agent_version", "1.0.0"),
            "contract_version": resolved["agent"]["contract_version"],
        },
        "artifact": {
            "artifact_id": artifact_id,
            "artifact_type": ARTIFACT_TYPES[designation],
            "created_at": job["created_at"],
            "lifecycle_state": "incomplete_input" if disclosure["limit_applied"] else "complete",
            "links": {"parents": [], "children": child_ids, "peers": []},
        },
        "execution": {
            "execution_id": job["execution_id"],
            "model": resolved["model"]["model_id"],
            "prompt_version": resolved["prompt_version"],
            "rubric_version": resolved["rubric_version"],
            "toolchain_version": resolved["toolchain_version"],
            "settings": {"temperature": 0},
            "generation_mode": "role_payload_v1",
            "generation_contract_version": resolved["generation_contract_version"],
            "assembler_version": resolved["assembler_version"],
        },
        "scope": copy.deepcopy(job["dispatch"].get("scope", {})),
        "inputs": inputs,
        **{field: copy.deepcopy(payload[field]) for field in ANALYTICAL_FIELDS if field != "coverage"},
        "coverage": coverage,
        "consumers": copy.deepcopy(resolved["node"].get("consumers", [])),
        "decision_authority": "human",
        "integrity": {
            "input_hash": content_hash(inputs),
            "output_hash": "sha256:" + "0" * 64,
            "attestation_ref": None,
            "retention_class": "internal-test",
            "schema_validation": "passed",
        },
        "extensions": {layer: copy.deepcopy(payload["layer_payload"])},
    }
    hash_material = copy.deepcopy(artifact)
    hash_material["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(hash_material)
    assembly = {
        "assembly_id": stable_uuid(job["job_id"], "assembly"),
        "job_id": job["job_id"],
        "designation": designation,
        "generation_mode": "role_payload_v1",
        "generation_contract_version": resolved["generation_contract_version"],
        "generation_contract_sha256": resolved["generation_contract_sha256"],
        "assembler_version": resolved["assembler_version"],
        "projection_version": "none",
        "projection_sha256": content_hash({"projection": "none"}),
        "payload_hash": content_hash(payload),
        "artifact_id": artifact_id,
        "artifact_hash": content_hash(artifact),
        "generation_disclosure": disclosure,
        "assembled_at": job["created_at"],
    }
    assert_schema(assembly, "assembly-record.schema.json", "assembly record")
    return artifact, assembly


def assemble_canonical_artifact(payload: dict[str, Any], job: dict[str, Any], resolved: dict[str, Any],
                                input_values: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Assemble a final artifact and deterministically project its registered layer."""
    schema = resolved.get("canonical_generation_contract")
    if schema is None:
        raise WorkerError("canonical analytical projection is unavailable for this designation")
    errors = validate_instance(payload, schema, schema)
    if errors:
        formatted = "\n  - ".join(errors)
        raise ValidationFailure(
            f"generation payload {resolved['designation']} failed {CANONICAL_GENERATION_CONTRACT_VERSION}:\n  - {formatted}"
        )
    inputs = []
    child_ids = []
    for value in input_values.values():
        if isinstance(value, dict) and isinstance(value.get("artifact"), dict) and isinstance(value.get("integrity"), dict):
            artifact_id = value["artifact"]["artifact_id"]
            child_ids.append(artifact_id)
            inputs.append({"artifact_id": artifact_id, "hash": value["integrity"]["output_hash"],
                           "compatibility": "compatible", "freshness": "fresh"})
    if not inputs:
        inputs = copy.deepcopy(job["dispatch"].get("input_manifest", []))
    disclosed_counts = payload["generation_disclosure"]
    disclosure = {"array_max_items": GENERATION_ARRAY_MAX_ITEMS,
                  "string_max_length": GENERATION_STRING_MAX_LENGTH,
                  "limit_applied": (disclosed_counts["omitted_item_estimate"] > 0 or
                                    disclosed_counts["truncated_string_estimate"] > 0),
                  "omitted_item_estimate": disclosed_counts["omitted_item_estimate"],
                  "truncated_string_estimate": disclosed_counts["truncated_string_estimate"]}
    projected_payload = copy.deepcopy(payload)
    layer_payload = project_canonical_layer(projected_payload, job, resolved, input_values)
    coverage = copy.deepcopy(projected_payload["coverage"])
    coverage["generation_limit"] = disclosure
    artifact_id = stable_uuid(job["job_id"], "assembled-artifact")
    artifact = {
        "identity": {
            "agent_uuid": resolved["agent"]["agent_uuid"], "designation": resolved["designation"],
            "display_name": resolved["agent"]["display_name"],
            "agent_version": resolved["agent"].get("agent_version", "1.0.0"),
            "contract_version": resolved["agent"]["contract_version"],
        },
        "artifact": {"artifact_id": artifact_id, "artifact_type": ARTIFACT_TYPES[resolved["designation"]],
                     "created_at": job["created_at"],
                     "lifecycle_state": "incomplete_input" if disclosure["limit_applied"] else "complete",
                     "links": {"parents": [], "children": child_ids, "peers": []}},
        "execution": {"execution_id": job["execution_id"], "model": resolved["model"]["model_id"],
                      "prompt_version": resolved["prompt_version"], "rubric_version": resolved["rubric_version"],
                      "toolchain_version": resolved["toolchain_version"], "settings": {"temperature": 0},
                      "generation_mode": "canonical_payload_v1",
                      "generation_contract_version": resolved["canonical_generation_contract_version"],
                      "assembler_version": resolved["canonical_assembler_version"],
                      "projection_version": resolved["canonical_projection_version"]},
        "scope": copy.deepcopy(job["dispatch"].get("scope", {})), "inputs": inputs,
        **{field: copy.deepcopy(projected_payload[field]) for field in ANALYTICAL_FIELDS if field != "coverage"},
        "coverage": coverage, "consumers": copy.deepcopy(resolved["node"].get("consumers", [])),
        "decision_authority": "human",
        "integrity": {"input_hash": content_hash(inputs), "output_hash": "sha256:" + "0" * 64,
                      "attestation_ref": None, "retention_class": "internal-test", "schema_validation": "passed"},
        "extensions": {resolved["node"]["layer"]: layer_payload},
    }
    hash_material = copy.deepcopy(artifact)
    hash_material["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(hash_material)
    assembly = {
        "assembly_id": stable_uuid(job["job_id"], "assembly"), "job_id": job["job_id"],
        "designation": resolved["designation"], "generation_mode": "canonical_payload_v1",
        "generation_contract_version": resolved["canonical_generation_contract_version"],
        "generation_contract_sha256": resolved["canonical_generation_contract_sha256"],
        "assembler_version": resolved["canonical_assembler_version"],
        "projection_version": resolved["canonical_projection_version"],
        "projection_sha256": resolved["canonical_projection_sha256"],
        "payload_hash": content_hash(payload), "artifact_id": artifact_id,
        "artifact_hash": content_hash(artifact), "generation_disclosure": disclosure,
        "assembled_at": job["created_at"],
    }
    assert_schema(assembly, "assembly-record.schema.json", "assembly record")
    return artifact, assembly


def prepare_guided_schema(schema: dict[str, Any], array_max_items: int | None = None,
                          string_max_length: int | None = None) -> dict[str, Any]:
    """Adapt a validation schema to the vLLM grammar subset without changing validation."""
    def visit(value: Any) -> Any:
        if isinstance(value, dict):
            result = {key: visit(item) for key, item in value.items() if key != "uniqueItems"}
            declared_type = result.get("type")
            if array_max_items is not None and declared_type == "array":
                result["maxItems"] = min(result.get("maxItems", array_max_items), array_max_items)
            if string_max_length is not None and declared_type == "string":
                result["maxLength"] = min(result.get("maxLength", string_max_length), string_max_length)
            return result
        if isinstance(value, list):
            return [visit(item) for item in value]
        return value
    return visit(copy.deepcopy(schema))


def validate_candidate(candidate: dict[str, Any], resolved: dict[str, Any],
                       input_values: dict[str, Any] | None = None) -> None:
    designation = resolved["designation"]
    assert_schema(candidate, "universal-agent-artifact.schema.json", f"worker artifact {designation}")
    layer = resolved["node"]["layer"]
    assert_schema(candidate["extensions"][layer], resolved["node"]["output_schema"], f"worker layer {designation}")
    assert_schema(candidate["extensions"][layer]["role"], resolved["node"]["role_schema"], f"worker role {designation}")
    if candidate["identity"]["agent_uuid"] != resolved["agent"]["agent_uuid"]:
        raise ValidationFailure("worker artifact agent UUID mismatch")
    if candidate["identity"]["designation"] != designation:
        raise ValidationFailure("worker artifact designation mismatch")
    if candidate["identity"]["contract_version"] != resolved["agent"]["contract_version"]:
        raise ValidationFailure("worker artifact contract version mismatch")
    if candidate["execution"].get("prompt_version") != resolved["prompt_version"]:
        raise ValidationFailure("worker artifact prompt version mismatch")
    if candidate["execution"].get("rubric_version") != resolved["rubric_version"]:
        raise ValidationFailure("worker artifact rubric version mismatch")
    if candidate["execution"].get("toolchain_version") != resolved["toolchain_version"]:
        raise ValidationFailure("worker artifact toolchain version mismatch")
    if candidate["execution"].get("model") != resolved["model"]["model_id"]:
        raise ValidationFailure("worker artifact model pin mismatch")
    if designation == "PROD-SYNTH":
        if resolved["agent"].get("status") != "candidate":
            raise ValidationFailure("PROD-SYNTH calibration requires candidate identity status")
        baseline = load_json(WORKFLOW)
        if any(node["designation"] == "PROD-SYNTH" for node in baseline["nodes"]):
            raise ValidationFailure("PROD-SYNTH candidate cannot be scheduled in the baseline workflow")
        values = [value for value in (input_values or {}).values()
                  if isinstance(value, dict) and isinstance(value.get("artifact"), dict)]
        if len(values) != 1 or values[0].get("identity", {}).get("designation") != "PROD-SEC":
            raise ValidationFailure("PROD-SYNTH candidate requires exactly one PROD-SEC calibration child")
        child_id = values[0]["artifact"]["artifact_id"]
        extension = candidate["extensions"]["product"]
        role = extension["role"]
        input_ids = {item["artifact_id"] for item in candidate["inputs"]}
        inventory_ids = {item["artifact_id"] for item in extension["specialist_artifact_inventory"]}
        if input_ids != {child_id} or inventory_ids != {child_id} or set(role["synthesis_basis"]["received_artifact_ids"]) != {child_id}:
            raise ValidationFailure("PROD-SYNTH candidate lineage does not match the immutable child")
        if role["capability_handoff"]["artifact_id"] != candidate["artifact"]["artifact_id"]:
            raise ValidationFailure("PROD-SYNTH capability handoff is not bound to the assembled artifact")
        if extension["release_readiness_input"].get("is_release_decision") is not False:
            raise ValidationFailure("PROD-SYNTH cannot emit a release decision")
        return
    if designation == "CAP-RISK" and resolved.get("workflow_id") == "WF-PROD-SYNTH-CAP-RISK-SHADOW-001":
        values = [value for value in (input_values or {}).values()
                  if isinstance(value, dict) and isinstance(value.get("artifact"), dict)]
        if len(values) != 1 or values[0].get("identity", {}).get("designation") != "PROD-SYNTH":
            raise ValidationFailure("shadow CAP-RISK requires exactly one PROD-SYNTH child")
        child_id = values[0]["artifact"]["artifact_id"]
        if candidate["artifact"]["links"]["children"] != [child_id] or {item["artifact_id"] for item in candidate["inputs"]} != {child_id}:
            raise ValidationFailure("shadow CAP-RISK exact child lineage mismatch")
        role = candidate["extensions"]["capability"]["role"]
        cited = {artifact_id for risk in role["risk_register"] for artifact_id in risk["contributing_artifacts"]}
        cited.update(record["source_artifact_id"] for record in role["risk_provenance"] if record.get("source_artifact_id"))
        if not cited or cited != {child_id}:
            raise ValidationFailure("shadow CAP-RISK risk lineage must cite only its PROD-SYNTH child")
        if candidate["decision_authority"] != "human" or role["decision_authority"] != "human":
            raise ValidationFailure("shadow CAP-RISK cannot claim decision authority")
        if candidate["consumers"] != ["SHADOW-COMPARISON"]:
            raise ValidationFailure("shadow CAP-RISK cannot route outside comparison")
        if any(node["designation"] == "PROD-SYNTH" for node in load_json(WORKFLOW)["nodes"]):
            raise ValidationFailure("shadow execution cannot mutate baseline scheduling")
        return
    registry = load_json(REGISTRY)
    registry_by_designation = {item["designation"]: item for item in registry["agents"]}
    workflow = validate_workflow(registry_by_designation)
    artifacts = {}
    external_input_designations: set[str] = set()
    for path in FIXTURE_DIR.glob("*.artifact.json"):
        value = load_json(path)
        artifacts[value["identity"]["designation"]] = value
    for value in (input_values or {}).values():
        if isinstance(value, dict) and isinstance(value.get("identity"), dict) and isinstance(value.get("artifact"), dict):
            input_designation = value["identity"].get("designation")
            if input_designation:
                artifacts[input_designation] = value
                external_input_designations.add(input_designation)
    artifacts[designation] = candidate
    decision = load_json(FIXTURE_DIR / "human-decision-request.json")
    validate_artifact_payloads(workflow, registry_by_designation, artifacts, decision,
                               replacement_designation=designation,
                               external_input_designations=external_input_designations)


class Worker:
    def __init__(self, queue: FileQueue, output_root: Path, adapter: ModelAdapter, worker_id: str = "WORKER-REFERENCE-001",
                 ledger: ArtifactLedger | None = None, resolver: VersionResolver | None = None) -> None:
        self.queue = queue
        self.output_root = output_root.resolve()
        self.adapter = adapter
        self.worker_id = worker_id
        self.ledger = ledger
        self.resolver = resolver or VersionResolver()

    def process_next(self) -> dict[str, Any] | None:
        leased = self.queue.lease_next(self.worker_id)
        if not leased:
            return None
        job, leased_path = leased
        result_path = self.output_root / job["job_id"] / "result.json"
        if result_path.exists():
            self.queue.finish(leased_path, "completed")
            return json.loads(result_path.read_text(encoding="utf-8"))
        start_wall = time.time_ns()
        start_cpu = time.process_time_ns()
        attempts: list[dict[str, Any]] = []
        status = "failed"
        error = None
        candidate = None
        model_output = None
        generated_payload = None
        assembly = None
        gate = None
        usage = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
        resolved = self.resolver.resolve(job["designation"])
        generation_mode = job.get("generation_mode", "full_artifact")
        configuration_error = None
        if generation_mode == "role_payload_v1":
            generation_contract_version = job.get("generation_contract_version", "")
            assembler_version = job.get("assembler_version", "")
            if generation_contract_version != resolved["generation_contract_version"]:
                configuration_error = "generation contract version mismatch"
            if assembler_version != resolved["assembler_version"]:
                configuration_error = "assembler version mismatch"
            generation_contract_sha256 = resolved["generation_contract_sha256"]
            projection_version = "none"
            projection_sha256 = content_hash({"projection": "none"})
        elif generation_mode == "canonical_payload_v1":
            if "canonical_generation_contract" not in resolved:
                configuration_error = "canonical payload mode is unavailable for this designation"
            generation_contract_version = job.get("generation_contract_version", "")
            assembler_version = job.get("assembler_version", "")
            projection_version = job.get("projection_version", "")
            if generation_contract_version != resolved.get("canonical_generation_contract_version"):
                configuration_error = "canonical generation contract version mismatch"
            if assembler_version != resolved.get("canonical_assembler_version"):
                configuration_error = "canonical assembler version mismatch"
            if projection_version != resolved.get("canonical_projection_version"):
                configuration_error = "canonical projection version mismatch"
            generation_contract_sha256 = resolved.get("canonical_generation_contract_sha256", content_hash({}))
            projection_sha256 = resolved.get("canonical_projection_sha256", content_hash({}))
        else:
            generation_contract_version = "full-artifact-1.0.0"
            assembler_version = "none"
            generation_contract_sha256 = content_hash(
                compose_output_schema(resolved["output_contract"], resolved["node"]["layer"])
            )
            projection_version = "none"
            projection_sha256 = content_hash({"projection": "none"})
        try:
            if configuration_error:
                raise WorkerError(configuration_error)
            if self.queue.is_cancelled(job["job_id"]):
                status = "cancelled"
                raise WorkerError("job cancellation requested before model invocation")
            evidence = LeastPrivilegeEvidenceAdapter(job["allowed_evidence_paths"])
            inputs = {path: evidence.read_json(path) for path in job["evidence_paths"]}
            exact_reference_bindings = []
            for path, value in inputs.items():
                if isinstance(value, dict) and isinstance(value.get("artifact"), dict) and isinstance(value.get("integrity"), dict):
                    exact_reference_bindings.append({
                        "source_path": path,
                        "designation": value.get("identity", {}).get("designation"),
                        "artifact_id": value["artifact"].get("artifact_id"),
                        "output_hash": value["integrity"].get("output_hash"),
                    })
            for attempt in range(1, job["max_attempts"] + 1):
                try:
                    model_context = {
                        "designation": job["designation"],
                        "dispatch": job["dispatch"],
                        "evidence": inputs,
                        "rubric": resolved["rubric"],
                        "toolchain": resolved["toolchain"],
                        "resolved_model": resolved["model"],
                        "resolved_layer": resolved["node"]["layer"],
                        "exact_reference_bindings": exact_reference_bindings,
                        "generation_mode": generation_mode,
                    }
                    if generation_mode in {"role_payload_v1", "canonical_payload_v1"}:
                        generation_contract = (resolved["generation_contract"] if generation_mode == "role_payload_v1"
                                               else resolved["canonical_generation_contract"])
                        disclosure_instruction = (
                            "Report nonnegative omitted_item_estimate and truncated_string_estimate in generation_disclosure. "
                            "The worker—not the model—derives lifecycle limit_applied from whether either count is positive."
                            if generation_mode == "canonical_payload_v1" else
                            "Set generation_disclosure.limit_applied=true and estimate omitted items or truncated strings if any relevant content cannot be returned; "
                            "such output is retained but fails closed as incomplete_input until explicitly authorized."
                        )
                        model_context.update({
                            "generation_contract": generation_contract,
                            "generation_contract_version": generation_contract_version,
                            "task_instruction": (
                                "Return exactly one JSON analytical payload conforming to generation_contract; this runtime boundary replaces the prompt's final publication format for this invocation. "
                                "Do not emit identity, artifact, execution, scope, inputs, consumers, decision_authority, integrity, routing, hashes, or Markdown. "
                                "The worker owns and deterministically assembles those fields. Preserve uncertainty, conflicts, coverage limits, CAPA content, and human decision boundaries in the analytical fields. "
                                f"Every array is limited to {GENERATION_ARRAY_MAX_ITEMS} items and every string to {GENERATION_STRING_MAX_LENGTH} characters for this calibration contract. "
                                + disclosure_instruction
                            ),
                        })
                    else:
                        model_context.update({
                            "required_output_contract": resolved["output_contract"],
                            "layer_payload_required_keys": resolved["output_contract"]["layer"].get("required", []),
                            "role_payload_required_keys": resolved["output_contract"]["role"].get("required", []),
                            "task_instruction": (
                                "Return exactly one JSON object conforming to the required output contract; do not use Markdown fences or commentary. "
                                f"Place the role-specific payload only at extensions.{resolved['node']['layer']}.role and include exactly its schema-defined fields. "
                                "Do not put gate, validation, completeness, confidence, or universal artifact fields inside the role payload. "
                                "Copy every supplied exact_reference_binding artifact_id and output_hash verbatim into the corresponding inputs entry, "
                                "and copy the artifact_id into artifact.links.children; never calculate or substitute these immutable references."
                            ),
                        })
                    if job["designation"] == "PROD-SYNTH":
                        preservable = []
                        for value in inputs.values():
                            if not isinstance(value, dict) or not isinstance(value.get("artifact"), dict):
                                continue
                            source_artifact_id = value["artifact"].get("artifact_id")
                            for field, key, kind in (
                                ("observations", "observation_id", "observation"),
                                ("assessments", "assessment_id", "assessment"),
                                ("findings", "finding_id", "finding"),
                                ("patterns", "pattern_id", "pattern"),
                                ("insights", "insight_id", "insight"),
                                ("conflicts", "conflict_id", "conflict"),
                                ("decisions_requested", "decision_context_id", "decision_request"),
                            ):
                                for record in value.get(field, []):
                                    preservable.append({"source_artifact_id": source_artifact_id,
                                                        "source_record_id": record.get(key),
                                                        "record_kind": kind,
                                                        "evidence_refs": copy.deepcopy(record.get("evidence_refs", []))})
                        model_context["preservable_record_bindings"] = preservable
                        model_context["task_instruction"] += (
                            " For PROD-SYNTH, preserved_child_assertions and every derived contributing_record_id "
                            "must copy source_artifact_id, source_record_id, record_kind, and evidence_refs only from "
                            "preservable_record_bindings. Role-internal correlation or hypothesis IDs are not universal "
                            "child records and must not be represented as preserved assertions or contributing_record_ids."
                        )
                    model_output, usage = self.adapter.generate(
                        resolved["prompt_text"],
                        model_context,
                        job["timeout_seconds"],
                    )
                    attempts.append({"attempt": attempt, "state": "model_completed"})
                    break
                except RetryableAdapterError as exc:
                    attempts.append({"attempt": attempt, "state": "retryable_failure", "reason": str(exc)})
                    if attempt == job["max_attempts"]:
                        raise
            if model_output is None:
                raise WorkerError("model adapter produced no artifact")
            if generation_mode == "role_payload_v1":
                generated_payload = model_output
                candidate, assembly = assemble_artifact(generated_payload, job, resolved, inputs)
            elif generation_mode == "canonical_payload_v1":
                generated_payload = model_output
                candidate, assembly = assemble_canonical_artifact(generated_payload, job, resolved, inputs)
            else:
                candidate = model_output
            validate_candidate(candidate, resolved, inputs)
            gate = {
                "gate_result_id": stable_uuid(job["job_id"], "gate"),
                "workflow_id": resolved["workflow_id"],
                "execution_id": job["execution_id"],
                "node_id": job["node_id"],
                "artifact_id": candidate["artifact"]["artifact_id"],
                "checks": [{"check": name, "state": "passed", "details": "Validated after model adapter output"}
                           for name in ("identity", "schema", "integrity", "lineage", "freshness", "completeness", "conflict_preservation", "capa", "authority", "routing")],
                "gate_state": "passed",
                "confidence_effect": {"delta": 0.0, "reason": "Worker output passed fan-in"},
                "partial_input_authorization": None,
                "escalations": [],
                "evaluated_at": job["created_at"],
            }
            assert_schema(gate, "gate-result.schema.json", "worker gate")
            status = "complete"
        except Exception as exc:
            error = str(exc)
            if status != "cancelled":
                status = "failed"

        telemetry = {
            "telemetry_id": stable_uuid(job["job_id"], "telemetry"),
            "job_id": job["job_id"],
            "execution_id": job["execution_id"],
            "dispatch_id": job["dispatch"]["dispatch_id"],
            "node_id": job["node_id"],
            "designation": job["designation"],
            "worker_id": self.worker_id,
            "model_provider": self.adapter.provider,
            "model_id": self.adapter.model_id,
            "prompt_version": resolved["prompt_version"],
            "prompt_sha256": resolved["prompt_sha256"],
            "rubric_version": resolved["rubric_version"],
            "toolchain_version": resolved["toolchain_version"],
            "generation_mode": generation_mode,
            "generation_contract_version": generation_contract_version,
            "generation_contract_sha256": generation_contract_sha256,
            "assembler_version": assembler_version,
            "projection_version": projection_version,
            "projection_sha256": projection_sha256,
            "attempts": attempts,
            "wall_duration_ms": max(0, (time.time_ns() - start_wall) // 1_000_000),
            "cpu_duration_ms": max(0, (time.process_time_ns() - start_cpu) // 1_000_000),
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "cost_usd": usage["cost_usd"],
            "status": status,
        }
        assert_schema(telemetry, "execution-telemetry.schema.json", "worker telemetry")
        job_dir = self.output_root / job["job_id"]
        artifact_path = None
        artifact_hash = None
        gate_path = None
        payload_path = None
        assembly_path = None
        if generated_payload is not None:
            payload_path = "payload.json"
            atomic_write(job_dir / payload_path, pretty_bytes(generated_payload))
        if assembly is not None:
            assembly_path = "assembly.json"
            atomic_write(job_dir / assembly_path, pretty_bytes(assembly))
            if self.ledger:
                self.ledger.persist_record(f"worker-assemblies/{assembly['assembly_id']}.json", "worker-assembly",
                                           assembly["assembly_id"], assembly)
        if status == "complete" and candidate is not None and gate is not None:
            artifact_path = "artifact.json"
            gate_path = "gate.json"
            artifact_hash = content_hash(candidate)
            atomic_write(job_dir / artifact_path, pretty_bytes(candidate))
            atomic_write(job_dir / gate_path, pretty_bytes(gate))
            if self.ledger:
                artifact_ref = self.ledger.persist_artifact(candidate)
                if artifact_ref["object_hash"] != artifact_hash:
                    raise WorkerError("ledger and worker artifact hashes disagree")
                self.ledger.persist_record(f"worker-gates/{gate['gate_result_id']}.json", "worker-gate",
                                           gate["gate_result_id"], gate)
        atomic_write(job_dir / "telemetry.json", pretty_bytes(telemetry))
        if self.ledger:
            self.ledger.persist_record(f"worker-telemetry/{telemetry['telemetry_id']}.json", "worker-telemetry",
                                       telemetry["telemetry_id"], telemetry)
        result = {
            "job_id": job["job_id"],
            "execution_id": job["execution_id"],
            "node_id": job["node_id"],
            "designation": job["designation"],
            "status": status,
            "attempt_count": len(attempts),
            "artifact_path": artifact_path,
            "artifact_hash": artifact_hash,
            "gate_path": gate_path,
            "telemetry_path": "telemetry.json",
            "payload_path": payload_path,
            "assembly_path": assembly_path,
            "error": error,
        }
        assert_schema(result, "worker-result.schema.json", "worker result")
        atomic_write(result_path, pretty_bytes(result))
        if self.ledger:
            self.ledger.persist_record(f"worker-results/{job['job_id']}.json", "worker-result", job["job_id"], result)
        self.queue.finish(leased_path, "completed" if status == "complete" else status)
        return result

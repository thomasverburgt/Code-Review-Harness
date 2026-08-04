#!/usr/bin/env python3
"""Common ADR-0039 specialist candidate and human shadow calibration boundary."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from artifact_ledger import ArtifactLedger, content_hash
from canonical_content import canonical_file_bytes
from evidence_locator_runtime import validate_locator
from validate_vertical_slice import ROOT, assert_schema, load_json


CALIBRATION_NAMESPACE = uuid.UUID("a4000000-0000-4000-8000-000000000000")
REGISTRY_PATH = ROOT / "agents" / "agent-identities.json"
FOCUS_CATALOG_PATH = ROOT / "agents" / "focus-profiles" / "catalog.json"
DISPOSITIONS = [
    "supported",
    "partially_supported",
    "unsupported",
    "duplicate",
    "outside_specialist_scope",
    "unable_to_determine",
]
REVIEWER_TRACKS = {
    "general_engineering_intern",
    "restricted_domain_reviewer",
    "qualified_subject_matter_expert",
}
CLASSIFICATION_ORDER = {"public": 0, "internal": 1, "restricted": 2}
RAW_RESTRICTED_PATTERNS = (
    "BEGIN PRIVATE KEY",
    '"secret_value"',
    '"raw_value"',
    "ghp_",
)
STATIC_ROLE_BINDINGS = {
    "SPEC-DEPS": {
        "prompt": ("SPEC-DEPS-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-deps/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-DEPS-ROLE", "1.0.0", "appendices/schemas/spec-deps-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-DEPS-CANDIDATE", "0.1.0", "appendices/rubrics/spec-deps-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-DEPS-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-deps-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-DEPS-STATIC-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-deps-static-evidence-0.1.0.json"),
    },
    "SPEC-SBOM": {
        "prompt": ("SPEC-SBOM-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-sbom/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-SBOM-ROLE", "1.0.0", "appendices/schemas/spec-sbom-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-SBOM-CANDIDATE", "0.1.0", "appendices/rubrics/spec-sbom-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-SBOM-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-sbom-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-SBOM-STATIC-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-sbom-static-evidence-0.1.0.json"),
    },
    "SPEC-LINT": {
        "prompt": ("SPEC-LINT-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-lint/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-LINT-ROLE", "1.0.0", "appendices/schemas/spec-lint-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-LINT-CANDIDATE", "0.1.0", "appendices/rubrics/spec-lint-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-LINT-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-lint-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-LINT-STATIC-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-lint-static-evidence-0.1.0.json"),
    },
    "SPEC-CONTAINER": {
        "prompt": ("SPEC-CONTAINER-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-container/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-CONTAINER-ROLE", "1.0.0", "appendices/schemas/spec-container-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-CONTAINER-CANDIDATE", "0.1.0", "appendices/rubrics/spec-container-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-CONTAINER-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-container-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-CONTAINER-BUILD-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-container-build-evidence-0.1.0.json"),
    },
    "SPEC-CICD": {
        "prompt": ("SPEC-CICD-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-cicd/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-CICD-ROLE", "1.0.0", "appendices/schemas/spec-cicd-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-CICD-CANDIDATE", "0.1.0", "appendices/rubrics/spec-cicd-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-CICD-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-cicd-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-CICD-BUILD-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-cicd-build-evidence-0.1.0.json"),
    },
    "SPEC-IAC": {
        "prompt": ("SPEC-IAC-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-iac/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-IAC-ROLE", "1.0.0", "appendices/schemas/spec-iac-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-IAC-CANDIDATE", "0.1.0", "appendices/rubrics/spec-iac-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-IAC-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-iac-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-IAC-BUILD-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-iac-build-evidence-0.1.0.json"),
    },
    "SPEC-K8S-WORKLOAD": {
        "prompt": ("SPEC-K8S-WORKLOAD-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-k8s-workload/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-K8S-WORKLOAD-ROLE", "1.0.0", "appendices/schemas/spec-k8s-workload-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-K8S-WORKLOAD-CANDIDATE", "0.1.0", "appendices/rubrics/spec-k8s-workload-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-K8S-WORKLOAD-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-k8s-workload-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-K8S-WORKLOAD-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-k8s-workload-evidence-0.1.0.json"),
    },
    "SPEC-K8S-PLATFORM": {
        "prompt": ("SPEC-K8S-PLATFORM-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-k8s-platform/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-K8S-PLATFORM-ROLE", "1.0.0", "appendices/schemas/spec-k8s-platform-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-K8S-PLATFORM-CANDIDATE", "0.1.0", "appendices/rubrics/spec-k8s-platform-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-K8S-PLATFORM-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-k8s-platform-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-K8S-PLATFORM-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-k8s-platform-evidence-0.1.0.json"),
    },
    "SPEC-COMMS": {
        "prompt": ("SPEC-COMMS-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-comms/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-COMMS-ROLE", "1.0.0", "appendices/schemas/spec-comms-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-COMMS-CANDIDATE", "0.1.0", "appendices/rubrics/spec-comms-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-COMMS-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-comms-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-COMMS-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-comms-evidence-0.1.0.json"),
    },
    "SPEC-SECURE-CODE": {
        "prompt": ("SPEC-SECURE-CODE-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-secure-code/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-SECURE-CODE-ROLE", "1.0.0", "appendices/schemas/spec-secure-code-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-SECURE-CODE-CANDIDATE", "0.1.0", "appendices/rubrics/spec-secure-code-candidate-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-SECURE-CODE-CALIBRATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-secure-code-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-SECURE-CODE-EVIDENCE", "0.1.0", "appendices/tool-manifests/spec-secure-code-evidence-0.1.0.json"),
    },
    "SPEC-SECRETS": {
        "prompt": ("SPEC-SECRETS-CANDIDATE-PROMPT", "design-0.2.0", "appendices/prompt-templates/candidates/spec-secrets/design-0.2.0.prompt.txt"),
        "role_schema": ("SPEC-SECRETS-ROLE", "1.0.0", "appendices/schemas/spec-secrets-role.schema.json"),
        "rubric": ("RUBRIC-SPEC-SECRETS-REVALIDATION", "0.1.0", "appendices/rubrics/spec-secrets-revalidation-0.1.0.json"),
        "model_manifest": ("GX10-QWEN3-32B-SPEC-SECRETS-REVALIDATION", "0.1.0", "appendices/model-manifests/gx10-qwen3-32b-spec-secrets-calibration-0.1.0.json"),
        "tool_policy": ("TOOLCHAIN-SPEC-SECRETS-REVALIDATION", "0.1.0", "appendices/tool-manifests/spec-secrets-revalidation-0.1.0.json"),
    },
}
_INCREMENT_567_SLUGS = {
    "SPEC-ARCH":"spec-arch", "SPEC-INTEROP":"spec-interop", "SPEC-DATA":"spec-data",
    "SPEC-DIAGRAM":"spec-diagram", "SPEC-IO":"spec-io", "SPEC-OBS":"spec-obs",
    "SPEC-PERF":"spec-perf", "SPEC-FMECA":"spec-fmeca", "SPEC-RESEARCH":"spec-research",
    "SPEC-RISK":"spec-risk", "SPEC-SECURITY":"spec-security",
}
for _designation, _slug in _INCREMENT_567_SLUGS.items():
    STATIC_ROLE_BINDINGS[_designation] = {
        "prompt": (f"{_designation}-CANDIDATE-PROMPT", "design-0.2.0", f"appendices/prompt-templates/candidates/{_slug}/design-0.2.0.prompt.txt"),
        "role_schema": (f"{_designation}-ROLE", "1.0.0", f"appendices/schemas/{_slug}-role.schema.json"),
        "rubric": (f"RUBRIC-{_designation}-CANDIDATE", "0.1.0", f"appendices/rubrics/{_slug}-candidate-0.1.0.json"),
        "model_manifest": (f"GX10-QWEN3-32B-{_designation}-CALIBRATION", "0.1.0", f"appendices/model-manifests/gx10-qwen3-32b-{_slug}-calibration-0.1.0.json"),
        "tool_policy": (f"TOOLCHAIN-{_designation}-EVIDENCE", "0.1.0", f"appendices/tool-manifests/{_slug}-evidence-0.1.0.json"),
    }
ROLE_SCHEMAS = {
    "SPEC-DEPS": "spec-deps-role.schema.json", "SPEC-SBOM": "spec-sbom-role.schema.json",
    "SPEC-LINT": "spec-lint-role.schema.json", "SPEC-CONTAINER": "spec-container-role.schema.json",
    "SPEC-CICD": "spec-cicd-role.schema.json", "SPEC-IAC": "spec-iac-role.schema.json",
    "SPEC-K8S-WORKLOAD": "spec-k8s-workload-role.schema.json", "SPEC-K8S-PLATFORM": "spec-k8s-platform-role.schema.json",
    "SPEC-COMMS": "spec-comms-role.schema.json", "SPEC-SECURE-CODE": "spec-secure-code-role.schema.json",
    "SPEC-SECRETS": "spec-secrets-role.schema.json",
}
ROLE_SCHEMAS.update({_designation: f"{_slug}-role.schema.json" for _designation, _slug in _INCREMENT_567_SLUGS.items()})


class SpecialistShadowCalibrationError(Exception):
    """Raised when a candidate, review packet, response, or metric fails closed."""


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(CALIBRATION_NAMESPACE, "|".join(parts)))


def canonical_file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(canonical_file_bytes(path)).hexdigest()


def seal_hash(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result[field] = None
    result[field] = content_hash(result)
    return result


def verify_hash(value: dict[str, Any], field: str, label: str) -> None:
    material = copy.deepcopy(value)
    material[field] = None
    if value[field] != content_hash(material):
        raise SpecialistShadowCalibrationError(f"{label} hash does not match canonical content")


def safe_repository_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def focus_material(profile: dict[str, Any]) -> dict[str, Any]:
    sections = profile["prompt_binding"]["required_sections"]
    return {name: profile["focus"][name] for name in sections}


def controlled_execution_bindings(designation: str) -> dict[str, dict[str, str]]:
    if designation not in STATIC_ROLE_BINDINGS:
        raise SpecialistShadowCalibrationError(f"{designation} has no controlled specialist-candidate execution binding")
    result = {}
    for kind, (binding_id, version, relative_path) in STATIC_ROLE_BINDINGS[designation].items():
        path = ROOT / relative_path
        if not path.is_file():
            raise SpecialistShadowCalibrationError(f"controlled {kind} file is missing for {designation}")
        result[kind] = {"id": binding_id, "version": version, "hash": canonical_file_hash(path)}
    return result


def _unsafe_serialized(value: Any) -> str | None:
    serialized = json.dumps(value, sort_keys=True)
    for marker in RAW_RESTRICTED_PATTERNS:
        if marker in serialized:
            return marker
    if re.search(r"AKIA[0-9A-Z]{16}", serialized):
        return "AWS access-key pattern"
    return None


def _registry_agent(designation: str) -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    match = next((item for item in registry["agents"] if item["designation"] == designation), None)
    if match is None or match["layer"] != "specialist":
        raise SpecialistShadowCalibrationError(f"{designation} is not a registered specialist")
    return match


def _focus_entry(designation: str) -> tuple[dict[str, Any], dict[str, Any], Path]:
    catalog = load_json(FOCUS_CATALOG_PATH)
    entry = next((item for item in catalog["profiles"] if item["designation"] == designation), None)
    if entry is None:
        raise SpecialistShadowCalibrationError(f"{designation} has no registered focus profile")
    path = ROOT / entry["path"]
    profile = load_json(path)
    if canonical_file_hash(path) != entry["sha256"]:
        raise SpecialistShadowCalibrationError(f"{designation} focus profile file hash is stale")
    return entry, profile, path


def validate_manifest(manifest: dict[str, Any]) -> None:
    assert_schema(manifest, "specialist-candidate-input-manifest.schema.json", "specialist candidate input manifest")
    verify_hash(manifest, "manifest_hash", "specialist candidate input manifest")
    candidate = manifest["candidate"]
    designation = candidate["designation"]
    agent = _registry_agent(designation)
    if candidate["agent_uuid"] != agent["agent_uuid"] or candidate["contract_version"] != agent["contract_version"]:
        raise SpecialistShadowCalibrationError("candidate identity or contract does not match the registry")

    entry, profile, _profile_path = _focus_entry(designation)
    binding = manifest["focus_binding"]
    expected_binding = {
        "profile_id": entry["profile_id"],
        "profile_version": entry["profile_version"],
        "profile_hash": entry["sha256"],
        "source_specification": profile["source"]["specification"],
        "source_specification_hash": profile["source"]["specification_sha256"],
        "compiled_prompt_focus_hash": content_hash(focus_material(profile)),
        "compression_protected_elements": profile["prompt_binding"]["compression_protected_elements"],
    }
    if binding != expected_binding:
        raise SpecialistShadowCalibrationError("focus binding does not exactly match the controlled profile")
    if profile["agent"]["agent_uuid"] != agent["agent_uuid"] or profile["agent"]["designation"] != designation:
        raise SpecialistShadowCalibrationError("focus profile identity does not match the candidate")
    source_path = ROOT / profile["source"]["specification"]
    if not source_path.is_file() or canonical_file_hash(source_path) != profile["source"]["specification_sha256"]:
        raise SpecialistShadowCalibrationError("focus profile source specification is missing or stale")
    controlled_increment = manifest["environment"]["environment_policy_version"] in {"increment-1.0.0", "increment-2.0.0", "increment-3.0.0", "increment-4.0.0", "increment-5.0.0", "increment-6.0.0", "increment-7.0.0"}
    if controlled_increment and designation in STATIC_ROLE_BINDINGS and manifest["execution_bindings"] != controlled_execution_bindings(designation):
        raise SpecialistShadowCalibrationError("execution bindings do not match the exact controlled Increment 1 files or Increment 2 specialist-candidate files")

    evidence_ids: set[str] = set()
    for evidence in manifest["evidence_population"]:
        if evidence["evidence_id"] in evidence_ids:
            raise SpecialistShadowCalibrationError("evidence population contains duplicate evidence IDs")
        evidence_ids.add(evidence["evidence_id"])
        if not safe_repository_path(evidence["path"]):
            raise SpecialistShadowCalibrationError("evidence path must be a safe repository-relative POSIX path")
        tracks = set(evidence["allowed_reviewer_tracks"])
        if not tracks.issubset(REVIEWER_TRACKS):
            raise SpecialistShadowCalibrationError("evidence contains an unsupported reviewer track")
        if evidence["classification"] == "restricted" and "general_engineering_intern" in tracks:
            raise SpecialistShadowCalibrationError("restricted evidence cannot be assigned to the general intern track")
        if not evidence["safe_for_human_review"] and "general_engineering_intern" in tracks:
            raise SpecialistShadowCalibrationError("unsafe evidence cannot be assigned to the general intern track")


def build_control_record(
    manifest: dict[str, Any], action: str, decided_at: str, authority_name: str, authority_source: str
) -> dict[str, Any]:
    validate_manifest(manifest)
    if action not in {"enable_calibration", "revoke_calibration"}:
        raise SpecialistShadowCalibrationError(f"unsupported calibration control action: {action}")
    enabled = action == "enable_calibration"
    value = {
        "control_id": stable_uuid(manifest["manifest_id"], manifest["manifest_hash"], action, decided_at),
        "control_version": "1.0.0",
        "manifest_id": manifest["manifest_id"],
        "manifest_hash": manifest["manifest_hash"],
        "designation": manifest["candidate"]["designation"],
        "action": action,
        "decided_at": decided_at,
        "decided_by": {"authority_role": "project_owner", "authority_name": authority_name},
        "authority_source": authority_source,
        "effects": {
            "candidate_discovery_enabled": enabled,
            "dispatch_enabled": enabled,
            "packet_export_enabled": enabled,
            "scheduled": False,
            "product_fan_in_eligible": False,
            "report_eligible": False,
            "deployment_authorized": False,
            "a100_production_authorized": False,
        },
        "authority_effect": "candidate_calibration_control_only",
        "control_hash": "sha256:" + "0" * 64,
    }
    value = seal_hash(value, "control_hash")
    validate_control_record(manifest, value)
    return value


def validate_control_record(manifest: dict[str, Any], record: dict[str, Any]) -> None:
    validate_manifest(manifest)
    assert_schema(record, "specialist-candidate-control-record.schema.json", "specialist candidate control record")
    verify_hash(record, "control_hash", "specialist candidate control record")
    if (record["manifest_id"], record["manifest_hash"], record["designation"]) != (
        manifest["manifest_id"], manifest["manifest_hash"], manifest["candidate"]["designation"]
    ):
        raise SpecialistShadowCalibrationError("control record does not bind the exact candidate manifest")
    enabled = record["action"] == "enable_calibration"
    actual = record["effects"]
    if any(actual[name] != enabled for name in ("candidate_discovery_enabled", "dispatch_enabled", "packet_export_enabled")):
        raise SpecialistShadowCalibrationError("control effects do not match the requested action")


def validate_candidate_artifact(manifest: dict[str, Any], candidate: dict[str, Any]) -> None:
    validate_manifest(manifest)
    assert_schema(candidate, "universal-agent-artifact.schema.json", "specialist shadow candidate")
    assert_schema(candidate["extensions"]["specialist"], "specialist-extension.schema.json", "specialist shadow candidate extension")
    expected = manifest["candidate"]
    identity = candidate["identity"]
    if (identity["agent_uuid"], identity["designation"], identity["agent_version"], identity["contract_version"]) != (
        expected["agent_uuid"], expected["designation"], expected["agent_version"], expected["contract_version"]
    ):
        raise SpecialistShadowCalibrationError("candidate artifact identity does not match the exact input manifest")
    if candidate["extensions"]["specialist"]["product_id"] != expected["product_id"]:
        raise SpecialistShadowCalibrationError("candidate product scope does not match the manifest")
    role = candidate["extensions"]["specialist"]["role"]
    controlled_increment = manifest["environment"]["environment_policy_version"] in {"increment-1.0.0", "increment-2.0.0", "increment-3.0.0", "increment-4.0.0", "increment-5.0.0", "increment-6.0.0", "increment-7.0.0"}
    if controlled_increment and expected["designation"] in ROLE_SCHEMAS:
        assert_schema(role, ROLE_SCHEMAS[expected["designation"]], f"{expected['designation']} role payload")
        if role["designation"] != expected["designation"]:
            raise SpecialistShadowCalibrationError("candidate role designation does not match its identity")
        admitted = {item["evidence_id"] for item in manifest["evidence_population"]}
        referenced: set[str] = set()
        def collect(value: Any) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == "evidence_refs" and isinstance(child, list):
                        referenced.update(child)
                    else:
                        collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
        collect(role)
        if not referenced or not referenced.issubset(admitted):
            raise SpecialistShadowCalibrationError("role payload evidence references are missing or outside the manifest")
        if expected["designation"] == "SPEC-LINT":
            completed = any(item["completed"] and item["exit_code"] is not None for item in role["executions"])
            if role["quality_gate"]["gate_state"] in {"passed", "failed"} and not completed:
                raise SpecialistShadowCalibrationError("lint quality gate cannot be decided without a completed admitted execution")
        if expected["designation"] == "SPEC-CONTAINER":
            if any(item["deployment_readiness"] == "demonstrated" for item in role["images"]):
                required = all(item["signature_or_attestation"] == "verified" and item["artifact_provenance"] == "verified" for item in role["images"])
                if not required or role["coverage"]["built_images_scanned"] == 0 or role["coverage"]["runtime_configs_reviewed"] == 0:
                    raise SpecialistShadowCalibrationError("container deployment readiness requires verified artifact, scan, and runtime evidence")
        if expected["designation"] == "SPEC-CICD":
            if role["coverage"]["completed_runs_reviewed"] == 0:
                if role["measures"]["repeatability"] is not None or role["measures"]["effective_gate_rate"] is not None:
                    raise SpecialistShadowCalibrationError("pipeline effectiveness cannot be measured without completed admitted runs")
                if any(item["gate_effectiveness"] == "demonstrated" for item in role["pipelines"]):
                    raise SpecialistShadowCalibrationError("pipeline gate effectiveness cannot be demonstrated from configuration alone")
        if expected["designation"] == "SPEC-IAC":
            if role["coverage"]["plans_reviewed"] == 0 and any(item["observed_state"] != "not_observed" for item in role["modules"]):
                raise SpecialistShadowCalibrationError("IaC observed state requires admitted plan, apply, or runtime evidence")
            if role["coverage"]["applies_reviewed"] == 0 and role["measures"]["idempotency_confidence"] is not None:
                raise SpecialistShadowCalibrationError("IaC idempotency confidence requires admitted apply evidence")
        if expected["designation"] == "SPEC-K8S-WORKLOAD" and role["coverage"]["runtime_records_reviewed"] == 0:
            if any(item["runtime_effectiveness"] == "demonstrated" or item["deployment_readiness"] == "demonstrated" for item in role["workloads"]):
                raise SpecialistShadowCalibrationError("workload runtime effectiveness or readiness requires admitted runtime evidence")
            if role["coverage"]["admission_records_reviewed"] == 0 and any(item["admission_effectiveness"] == "demonstrated" for item in role["workloads"]):
                raise SpecialistShadowCalibrationError("workload admission effectiveness requires admitted admission evidence")
        if expected["designation"] == "SPEC-K8S-PLATFORM" and role["coverage"]["live_clusters_reviewed"] == 0:
            if any(item["enforcement_effectiveness"] == "demonstrated" or item["tenant_isolation_confidence"] is not None for item in role["platform_controls"]):
                raise SpecialistShadowCalibrationError("platform effectiveness and tenant isolation cannot be inferred from desired state alone")
        if expected["designation"] == "SPEC-COMMS":
            if not role["topology"]["artifact_ref"]:
                raise SpecialistShadowCalibrationError("communications assessment requires a topology artifact")
            if role["coverage"]["traffic_tests_reviewed"] == 0 and any(item["runtime_effectiveness"] == "demonstrated" for item in role["trust_paths"]):
                raise SpecialistShadowCalibrationError("communication runtime effectiveness requires admitted traffic evidence")
        if expected["designation"] == "SPEC-SECURE-CODE":
            if role["coverage"]["security_tests_reviewed"] == 0 and any(item["assessment_state"] == "confirmed_weakness" or item["exploitability"] == "demonstrated" for item in role["code_assessments"]):
                raise SpecialistShadowCalibrationError("confirmed secure-code weakness or exploitability requires admitted security-test evidence")
        if expected["designation"] == "SPEC-SECRETS":
            if any("general_engineering_intern" in item["allowed_reviewer_tracks"] for item in manifest["evidence_population"]):
                raise SpecialistShadowCalibrationError("SPEC-SECRETS revalidation cannot use the general intern track")
            if any(item["evidence_state"] == "confirmed_secret" for item in role["secret_observations"]):
                raise SpecialistShadowCalibrationError("redacted unresolved evidence cannot be promoted to confirmed secret during revalidation")
        if expected["designation"] in _INCREMENT_567_SLUGS:
            coverage = role["coverage"]
            if coverage["tests_reviewed"] == 0 and coverage["runtime_records_reviewed"] == 0 and any(item["effectiveness"] == "demonstrated" for item in role["domain_records"]):
                raise SpecialistShadowCalibrationError("static, design, external, or retained-candidate evidence cannot demonstrate effectiveness")
            if expected["designation"] in {"SPEC-DIAGRAM", "SPEC-IO", "SPEC-RESEARCH", "SPEC-RISK", "SPEC-SECURITY"}:
                maturity = ROOT / "appendices" / "maturity-manifests" / f"{_INCREMENT_567_SLUGS[expected['designation']]}-bounded-calibration-0.1.0.json"
                if not maturity.is_file() or load_json(maturity)["result"] != "sufficient_for_bounded_candidate_calibration":
                    raise SpecialistShadowCalibrationError("seed-status specialist lacks a passing bounded-calibration maturity record")
    if candidate["artifact"]["lifecycle_state"] != "complete":
        raise SpecialistShadowCalibrationError("only structurally complete candidates may enter human shadow review")
    if candidate["scope"].get("decision_context") != "specialist_human_shadow_calibration":
        raise SpecialistShadowCalibrationError("candidate decision context is not human shadow calibration")
    execution = candidate["execution"]
    required_execution = {
        "comparison_only": True,
        "scheduled": False,
        "product_fan_in_eligible": False,
        "deployment_authorized": False,
        "a100_production_authorized": False,
    }
    for name, expected_value in required_execution.items():
        if execution.get(name) != expected_value:
            raise SpecialistShadowCalibrationError(f"candidate execution violates comparison-only control: {name}")
    if candidate["consumers"] != ["human-shadow-review-only"]:
        raise SpecialistShadowCalibrationError("specialist candidate has an unauthorized downstream consumer")
    if candidate["integrity"]["retention_class"] != "specialist-human-shadow-calibration":
        raise SpecialistShadowCalibrationError("candidate retention class is not specialist human shadow calibration")
    marker = _unsafe_serialized(candidate)
    if marker:
        raise SpecialistShadowCalibrationError(f"candidate contains prohibited raw restricted content: {marker}")


def candidate_items(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    default_confidence = candidate["confidence"].get("assessment")
    items: list[dict[str, Any]] = []
    for record in candidate["observations"]:
        items.append({
            "source_record_id": record["observation_id"], "kind": "observation",
            "statement": record.get("fact") or record.get("statement"),
            "confidence": record.get("confidence", candidate["confidence"].get("evidence")),
            "confidence_meaning": "confidence in the attributable observation within the declared evidence population",
            "evidence_refs": record.get("evidence_refs", []),
        })
    for record in candidate["findings"]:
        items.append({
            "source_record_id": record["finding_id"], "kind": "finding", "statement": record["statement"],
            "confidence": record.get("confidence", default_confidence),
            "confidence_meaning": "assessment confidence for this bounded specialist finding, not decision confidence",
            "evidence_refs": record.get("evidence_refs", []),
        })
        capa = record.get("capa")
        if isinstance(capa, dict) and capa.get("corrective_action"):
            items.append({
                "source_record_id": f"{record['finding_id']}:CAPA", "kind": "recommendation",
                "statement": capa["corrective_action"], "confidence": record.get("confidence", default_confidence),
                "confidence_meaning": "confidence that the recommendation addresses the bounded finding; implementation remains human-owned",
                "evidence_refs": record.get("evidence_refs", []),
            })
    for record in candidate["patterns"]:
        items.append({
            "source_record_id": record["pattern_id"], "kind": "pattern", "statement": record["statement"],
            "confidence": record.get("confidence", default_confidence),
            "confidence_meaning": "confidence in a candidate positive pattern, not approval or effectiveness",
            "evidence_refs": record.get("evidence_refs", []),
        })
    for record in candidate["extensions"]["specialist"].get("domain_unknowns", []):
        items.append({
            "source_record_id": record["unknown_id"], "kind": "unknown", "statement": record["statement"],
            "confidence": record.get("confidence"),
            "confidence_meaning": "confidence in the stated evidence limitation; no missing value is imputed",
            "evidence_refs": record.get("evidence_refs", []),
        })
    if not items:
        raise SpecialistShadowCalibrationError("candidate has no human-reviewable records")
    for item in items:
        if not item["statement"] or not item["evidence_refs"]:
            raise SpecialistShadowCalibrationError(f"candidate item {item['source_record_id']} lacks a statement or evidence reference")
    return items


def _locator_summary(locator: dict[str, Any]) -> dict[str, Any]:
    return {
        "locator_id": locator["locator_id"],
        "locator_hash": locator["locator_hash"],
        "evidence_id": locator["evidence_id"],
        "repository_uri": locator["repository_uri"],
        "immutable_revision": locator["immutable_revision"],
        "path": locator["path"],
        "line_start": locator["line_start"],
        "line_end": locator["line_end"],
        "symbol_or_section": locator["symbol_or_section"],
        "safe_excerpt": locator["safe_excerpt"],
        "line_fingerprint": locator["line_fingerprint"],
        "classification": locator["access"]["classification"],
        "redaction_applied": locator["redaction"]["applied"],
        "raw_value_included": locator["redaction"]["raw_value_included"],
        "reproduction_steps": locator["reproduction_steps"],
        "locator_state": locator["locator_state"],
    }


def build_review_packet(
    manifest: dict[str, Any], candidate: dict[str, Any], locators: list[dict[str, Any]], generated_at: str
) -> dict[str, Any]:
    validate_candidate_artifact(manifest, candidate)
    for locator in locators:
        validate_locator(locator)
        if locator["repository_uri"] != manifest["repository"]["repository_uri"] or locator["immutable_revision"] != manifest["repository"]["immutable_revision"]:
            raise SpecialistShadowCalibrationError("locator repository or revision does not match the input manifest")
    locator_map: dict[str, list[dict[str, Any]]] = {}
    for locator in locators:
        locator_map.setdefault(locator["evidence_id"], []).append(locator)
    evidence_map = {item["evidence_id"]: item for item in manifest["evidence_population"]}
    packet_items: list[dict[str, Any]] = []
    packet_tracks = set(REVIEWER_TRACKS)
    classifications: list[str] = []
    blocking: list[str] = []

    for index, item in enumerate(candidate_items(candidate), start=1):
        unknown_refs = set(item["evidence_refs"]) - set(evidence_map)
        if unknown_refs:
            raise SpecialistShadowCalibrationError(f"candidate item references evidence outside the manifest: {sorted(unknown_refs)}")
        item_locators = [locator for evidence_id in item["evidence_refs"] for locator in locator_map.get(evidence_id, [])]
        tracks = set(REVIEWER_TRACKS)
        unsafe = False
        for evidence_id in item["evidence_refs"]:
            evidence = evidence_map[evidence_id]
            tracks &= set(evidence["allowed_reviewer_tracks"])
            classifications.append(evidence["classification"])
            unsafe = unsafe or not evidence["safe_for_human_review"]
        packet_tracks &= tracks
        if unsafe:
            state = "blocked_unsafe_content"
        elif not tracks:
            state = "blocked_access"
        elif not item_locators:
            state = "blocked_missing_locator"
        elif any(locator["locator_state"] == "source_inaccessible" for locator in item_locators):
            state = "blocked_access"
        elif any(locator["locator_state"] != "source_located" for locator in item_locators):
            state = "blocked_unverified_locator"
        else:
            state = "ready"
        if state != "ready":
            blocking.append(f"{item['source_record_id']}:{state}")
        packet_items.append({
            "item_id": f"ITEM-{index:04d}",
            **item,
            "locators": [_locator_summary(locator) for locator in item_locators],
            "reviewability": state,
            "allowed_dispositions": DISPOSITIONS,
        })

    if not packet_tracks:
        blocking.append("packet:no_common_authorized_reviewer_track")
    if any("blocked_unsafe_content" in value for value in blocking):
        reviewability = "blocked_unsafe_content"
    elif any("blocked_access" in value for value in blocking) or not packet_tracks:
        reviewability = "blocked_access"
    elif any("blocked_missing_locator" in value for value in blocking):
        reviewability = "blocked_missing_locator"
    elif any("blocked_unverified_locator" in value for value in blocking):
        reviewability = "blocked_unverified_locator"
    else:
        reviewability = "ready_for_human_shadow_review"
    classification = max(classifications, key=CLASSIFICATION_ORDER.get) if classifications else "public"
    packet = {
        "packet_id": stable_uuid(manifest["manifest_id"], manifest["manifest_hash"], candidate["artifact"]["artifact_id"], content_hash(candidate), "human-shadow-review"),
        "packet_version": "1.0.0",
        "generated_at": generated_at,
        "candidate": {
            "agent_uuid": manifest["candidate"]["agent_uuid"],
            "designation": manifest["candidate"]["designation"],
            "product_id": manifest["candidate"]["product_id"],
        },
        "input_manifest_id": manifest["manifest_id"],
        "input_manifest_hash": manifest["manifest_hash"],
        "candidate_artifact_id": candidate["artifact"]["artifact_id"],
        "candidate_artifact_hash": content_hash(candidate),
        "focus_binding": {name: manifest["focus_binding"][name] for name in ("profile_id", "profile_version", "profile_hash")},
        "reviewability_state": reviewability,
        "classification": classification,
        "permitted_reviewer_tracks": sorted(packet_tracks),
        "items": packet_items,
        "blocking_issues": sorted(set(blocking)),
        "lifecycle": {
            "comparison_only": True,
            "scheduled": False,
            "product_fan_in_eligible": False,
            "report_eligible": False,
            "deployment_authorized": False,
            "a100_production_authorized": False,
        },
        "authority_effect": "review_support_only",
        "packet_hash": "sha256:" + "0" * 64,
    }
    packet = seal_hash(packet, "packet_hash")
    validate_review_packet(manifest, candidate, packet)
    return packet


def validate_review_packet(manifest: dict[str, Any], candidate: dict[str, Any], packet: dict[str, Any]) -> None:
    validate_candidate_artifact(manifest, candidate)
    assert_schema(packet, "specialist-shadow-review-packet.schema.json", "specialist shadow review packet")
    verify_hash(packet, "packet_hash", "specialist shadow review packet")
    exact = (
        packet["input_manifest_id"] == manifest["manifest_id"]
        and packet["input_manifest_hash"] == manifest["manifest_hash"]
        and packet["candidate_artifact_id"] == candidate["artifact"]["artifact_id"]
        and packet["candidate_artifact_hash"] == content_hash(candidate)
    )
    if not exact:
        raise SpecialistShadowCalibrationError("review packet does not bind the exact manifest and candidate")
    item_ids = [item["item_id"] for item in packet["items"]]
    source_ids = [item["source_record_id"] for item in packet["items"]]
    if len(item_ids) != len(set(item_ids)) or len(source_ids) != len(set(source_ids)):
        raise SpecialistShadowCalibrationError("review packet contains duplicate item or source record IDs")
    if packet["classification"] == "restricted" and "general_engineering_intern" in packet["permitted_reviewer_tracks"]:
        raise SpecialistShadowCalibrationError("restricted packet cannot be delivered to the general intern track")
    ready = packet["reviewability_state"] == "ready_for_human_shadow_review"
    if ready and (packet["blocking_issues"] or any(item["reviewability"] != "ready" for item in packet["items"])):
        raise SpecialistShadowCalibrationError("ready packet contains blocking issues")
    if not ready and not packet["blocking_issues"]:
        raise SpecialistShadowCalibrationError("blocked packet does not explain its blocking issues")
    marker = _unsafe_serialized(packet)
    if marker:
        raise SpecialistShadowCalibrationError(f"review packet contains prohibited raw restricted content: {marker}")


def build_review_response(
    packet: dict[str, Any], reviewer: dict[str, Any], item_reviews: list[dict[str, Any]],
    overall_usability: dict[str, Any], evidence_requests: list[str], started_at: str, completed_at: str,
) -> dict[str, Any]:
    value = {
        "response_id": stable_uuid(packet["packet_id"], packet["packet_hash"], reviewer["reviewer_id"], completed_at),
        "response_version": "1.0.0",
        "packet_id": packet["packet_id"],
        "packet_hash": packet["packet_hash"],
        "reviewer": reviewer,
        "started_at": started_at,
        "completed_at": completed_at,
        "item_reviews": item_reviews,
        "overall_usability": overall_usability,
        "evidence_requests": evidence_requests,
        "classification": "non_authoritative_human_review",
        "non_authoritative_acknowledged": True,
        "decision_authority": "human",
        "authority_effect": "calibration_evidence_only",
        "response_hash": "sha256:" + "0" * 64,
    }
    value = seal_hash(value, "response_hash")
    validate_review_response(packet, value)
    return value


def validate_review_response(packet: dict[str, Any], response: dict[str, Any]) -> None:
    assert_schema(packet, "specialist-shadow-review-packet.schema.json", "specialist shadow review packet")
    verify_hash(packet, "packet_hash", "specialist shadow review packet")
    if packet["reviewability_state"] != "ready_for_human_shadow_review":
        raise SpecialistShadowCalibrationError("a blocked packet cannot receive a completed human review")
    assert_schema(response, "specialist-shadow-review-response.schema.json", "specialist shadow review response")
    verify_hash(response, "response_hash", "specialist shadow review response")
    if response["packet_id"] != packet["packet_id"] or response["packet_hash"] != packet["packet_hash"]:
        raise SpecialistShadowCalibrationError("review response does not bind the exact packet")
    track = response["reviewer"]["reviewer_track"]
    if track not in packet["permitted_reviewer_tracks"]:
        raise SpecialistShadowCalibrationError("reviewer track is not authorized for this packet")
    if packet["classification"] not in response["reviewer"]["authorized_classifications"]:
        raise SpecialistShadowCalibrationError("reviewer lacks the packet classification")
    expected = {item["item_id"] for item in packet["items"]}
    actual = [item["item_id"] for item in response["item_reviews"]]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise SpecialistShadowCalibrationError("review response must disposition every packet item exactly once")
    allowed = {item["item_id"]: set(item["allowed_dispositions"]) for item in packet["items"]}
    for item in response["item_reviews"]:
        if item["disposition"] not in allowed[item["item_id"]]:
            raise SpecialistShadowCalibrationError("review response contains a disposition not allowed by the packet")
    started = datetime.fromisoformat(response["started_at"].replace("Z", "+00:00"))
    completed = datetime.fromisoformat(response["completed_at"].replace("Z", "+00:00"))
    if completed < started:
        raise SpecialistShadowCalibrationError("review completion precedes review start")


def build_metrics(packet: dict[str, Any], responses: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    if not responses:
        raise SpecialistShadowCalibrationError("metrics require at least one review response")
    for response in responses:
        validate_review_response(packet, response)
    response_ids = [item["response_id"] for item in responses]
    if len(response_ids) != len(set(response_ids)):
        raise SpecialistShadowCalibrationError("metrics cannot double count a review response")
    dispositions = Counter(item["disposition"] for response in responses for item in response["item_reviews"])
    locators = Counter(item["locator_correctness"] for response in responses for item in response["item_reviews"])
    total_items = sum(dispositions.values())
    durations = []
    for response in responses:
        started = datetime.fromisoformat(response["started_at"].replace("Z", "+00:00"))
        completed = datetime.fromisoformat(response["completed_at"].replace("Z", "+00:00"))
        durations.append((completed - started).total_seconds())
    rates = {
        "support": dispositions["supported"] / total_items,
        "partial_support": dispositions["partially_supported"] / total_items,
        "unsupported": dispositions["unsupported"] / total_items,
        "duplicate": dispositions["duplicate"] / total_items,
        "scope_violation": dispositions["outside_specialist_scope"] / total_items,
        "unresolved": dispositions["unable_to_determine"] / total_items,
        "locator_success": locators["correct"] / total_items,
    }
    value = {
        "metrics_id": stable_uuid(packet["packet_id"], packet["packet_hash"], *sorted(response_ids), "metrics"),
        "metrics_version": "1.0.0",
        "generated_at": generated_at,
        "packet_id": packet["packet_id"],
        "packet_hash": packet["packet_hash"],
        "response_bindings": [
            {"response_id": response["response_id"], "response_hash": response["response_hash"]}
            for response in sorted(responses, key=lambda item: item["response_id"])
        ],
        "item_count": len(packet["items"]),
        "review_count": len(responses),
        "disposition_counts": {name: dispositions[name] for name in DISPOSITIONS},
        "locator_counts": {name: locators[name] for name in ("correct", "partially_correct", "incorrect", "not_verified")},
        "rates": rates,
        "review_duration_seconds": {
            "total": sum(durations),
            "minimum": min(durations),
            "maximum": max(durations),
            "mean": sum(durations) / len(durations),
        },
        "correctness_established": False,
        "authority_effect": "calibration_measurement_only",
        "metrics_hash": "sha256:" + "0" * 64,
    }
    value = seal_hash(value, "metrics_hash")
    validate_metrics(packet, responses, value)
    return value


def validate_metrics(packet: dict[str, Any], responses: list[dict[str, Any]], metrics: dict[str, Any]) -> None:
    for response in responses:
        validate_review_response(packet, response)
    assert_schema(metrics, "specialist-shadow-review-metrics.schema.json", "specialist shadow review metrics")
    verify_hash(metrics, "metrics_hash", "specialist shadow review metrics")
    if metrics["packet_id"] != packet["packet_id"] or metrics["packet_hash"] != packet["packet_hash"]:
        raise SpecialistShadowCalibrationError("metrics do not bind the exact packet")
    expected = {(item["response_id"], item["response_hash"]) for item in responses}
    actual = {(item["response_id"], item["response_hash"]) for item in metrics["response_bindings"]}
    if actual != expected:
        raise SpecialistShadowCalibrationError("metrics do not bind the exact review responses")
    total_dispositions = sum(metrics["disposition_counts"].values())
    if total_dispositions != metrics["item_count"] * metrics["review_count"]:
        raise SpecialistShadowCalibrationError("metrics disposition population is inconsistent")


def persist_calibration(
    ledger_root: Path, manifest: dict[str, Any], enable: dict[str, Any], candidate: dict[str, Any],
    locators: list[dict[str, Any]], packet: dict[str, Any], responses: list[dict[str, Any]],
    metrics: dict[str, Any], revoke: dict[str, Any],
) -> dict[str, Any]:
    validate_control_record(manifest, enable)
    validate_review_packet(manifest, candidate, packet)
    for response in responses:
        validate_review_response(packet, response)
    validate_metrics(packet, responses, metrics)
    validate_control_record(manifest, revoke)
    ledger = ArtifactLedger(ledger_root, clearance="internal")
    references = [
        ledger.persist_record("specialist-shadow/input-manifest.json", "specialist-shadow-input", manifest["manifest_id"], manifest, retention_class="specialist-human-shadow-calibration"),
        ledger.persist_record("specialist-shadow/control-enable.json", "specialist-shadow-control", enable["control_id"], enable, retention_class="specialist-human-shadow-calibration"),
        ledger.persist_artifact(candidate),
    ]
    for locator in locators:
        references.append(ledger.persist_record(
            f"specialist-shadow/locators/{locator['locator_id']}.json", "evidence-locator", locator["locator_id"], locator,
            classification="internal", retention_class="specialist-human-shadow-calibration",
        ))
    references.append(ledger.persist_record("specialist-shadow/review-packet.json", "specialist-shadow-packet", packet["packet_id"], packet, retention_class="specialist-human-shadow-calibration"))
    for response in responses:
        references.append(ledger.persist_record(
            f"specialist-shadow/responses/{response['response_id']}.json", "specialist-shadow-response", response["response_id"], response,
            retention_class="specialist-human-shadow-calibration",
        ))
    references.append(ledger.persist_record("specialist-shadow/metrics.json", "specialist-shadow-metrics", metrics["metrics_id"], metrics, retention_class="specialist-human-shadow-calibration"))
    references.append(ledger.persist_record("specialist-shadow/control-revoke.json", "specialist-shadow-control", revoke["control_id"], revoke, retention_class="specialist-human-shadow-calibration"))
    return {
        "status": "persisted_and_revoked",
        "record_count": len(references),
        "packet_id": packet["packet_id"],
        "metrics_id": metrics["metrics_id"],
        "final_control_id": revoke["control_id"],
        "scheduled": False,
        "product_fan_in_eligible": False,
        "deployment_authorized": False,
        "a100_production_authorized": False,
    }

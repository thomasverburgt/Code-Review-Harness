#!/usr/bin/env python3
"""Build deterministic ADR-0039 Increment 2 candidates and deferred-review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from artifact_ledger import atomic_write, content_hash, pretty_bytes
from specialist_shadow_calibration_runtime import (
    ROOT, build_control_record, build_review_packet, controlled_execution_bindings,
    focus_material, seal_hash, stable_uuid, validate_candidate_artifact, validate_manifest,
)

REPOSITORY_URI = "https://github.com/defenseunicorns/uds-core.git"
REVISION = "329ade01852f9e570d31cb7b19d9979152938c17"
PRODUCT_ID = "UDS-CORE-SPECIALIST-CALIBRATION-001"
CREATED_AT = "2026-08-03T20:00:00Z"
GENERATED_AT = "2026-08-03T20:05:00Z"
DEFAULT_OUTPUT = ROOT / "fixtures" / "specialist-build-supply-chain-increment2" / "gold"
INCREMENT_KEY = "increment-2"
INCREMENT_LABEL = "Increment 2"
ENVIRONMENT_POLICY_VERSION = "increment-2.0.0"
LOCATOR_COLLECTOR = "increment-2-deterministic-reference"
INCREMENT_SUMMARY = 2

# Evidence tuples: ID, repository path, line, exact safe excerpt, section, full-file hash, source type.
CONFIG = {
    "SPEC-CONTAINER": {
        "slug": "spec-container", "display": "Container and Image Security Reviewer", "domain": "container_image_posture",
        "evidence": [
            ("EVIDENCE-CONTAINER-BASE-001", "scripts/keycloak-crl-airgap/Dockerfile", 4, "FROM scratch", "base image", "sha256:68d294b60ad036736ed6a8074d438f16adef6c805e51c813ed81b1a722f771b4", "configuration"),
            ("EVIDENCE-CONTAINER-COPY-001", "scripts/keycloak-crl-airgap/Dockerfile", 5, "COPY stage/ /", "composition", "sha256:68d294b60ad036736ed6a8074d438f16adef6c805e51c813ed81b1a722f771b4", "configuration"),
        ],
        "observation": "The admitted container definition uses a scratch base and copies a staged filesystem into the image.",
        "finding": "The source definition does not identify a built digest, verified signature or attestation, provenance record, scan result, or declared runtime user.",
        "corrective": "Retain the built image digest, provenance, signature verification, composition scan, and runtime security-context evidence for this image.",
        "preventive": "Gate image promotion on immutable identity, verified provenance, scan retention, and least-privilege runtime declarations.",
        "unknown": "Built contents, registry trust, signing, provenance, vulnerability exposure, runtime identity, startup behavior, and deployment readiness are not demonstrated by the admitted Dockerfile alone.",
    },
    "SPEC-CICD": {
        "slug": "spec-cicd", "display": "CI/CD Pipeline Reviewer", "domain": "delivery_pipeline_posture",
        "evidence": [
            ("EVIDENCE-CICD-RELEASE-PERM-001", ".github/workflows/tag-and-release.yaml", 21, "    permissions: write-all", "tag-new-version permissions", "sha256:b0e38ef39b2396cc1b21e5655059e14381fd2833d94e8e6bc69e1880e8928097", "configuration"),
            ("EVIDENCE-CICD-PUBLISH-PERM-001", ".github/workflows/publish.yaml", 30, "    permissions:", "publish job permissions", "sha256:1f47488f2872d8e0d5037df954be9062bb8cbf764e5e31aacf7af393a4cdcaa3", "configuration"),
            ("EVIDENCE-CICD-ACTION-PIN-001", ".github/workflows/tag-and-release.yaml", 30, "        uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0", "release action pin", "sha256:b0e38ef39b2396cc1b21e5655059e14381fd2833d94e8e6bc69e1880e8928097", "configuration"),
        ],
        "observation": "The release workflow pins release-please to an immutable commit while its tag job declares write-all permissions; the called publish workflow defines job-scoped permissions.",
        "finding": "No completed pipeline run, produced artifact identity, attestation, promotion decision, failure recovery, or rollback event is admitted for this calibration slice.",
        "corrective": "Review and narrow the tag job permissions, then retain linked run, artifact, provenance, gate, promotion, and rollback evidence.",
        "preventive": "Continuously test least privilege and bind every release decision to immutable workflow, run, artifact, attestation, and rollback records.",
        "unknown": "Secret scope, runner isolation, actual permission use, repeatability, gate effectiveness, artifact provenance, promotion governance, and recovery behavior remain unknown without execution records.",
    },
    "SPEC-IAC": {
        "slug": "spec-iac", "display": "Infrastructure-as-Code Reviewer", "domain": "infrastructure_desired_state",
        "evidence": [
            ("EVIDENCE-IAC-MODULE-001", ".github/test-infra/aws/eks/main.tf", 34, "  source                    = \"../modules/kms\"", "generate_kms module source", "sha256:6645013085794585353406bb41480c0ac7ac18dddd1d60984dfb831ec5aa784f", "iac"),
            ("EVIDENCE-IAC-BACKEND-001", ".github/test-infra/aws/eks/versions.tf", 16, "  backend \"s3\" {", "Terraform backend", "sha256:758fd3a64791ca409cd88e19129af3942fd4220bb590f995a126c5592825f275", "iac"),
            ("EVIDENCE-IAC-VERSION-001", ".github/test-infra/aws/eks/versions.tf", 21, "      version = \"~> 6.0\"", "AWS provider constraint", "sha256:758fd3a64791ca409cd88e19129af3942fd4220bb590f995a126c5592825f275", "iac"),
        ],
        "observation": "The admitted EKS IaC declares a local KMS module, an S3 backend, and a constrained AWS provider version.",
        "finding": "No plan, apply, state safeguard verification, drift result, policy result, idempotency test, failure recovery, or rollback evidence is admitted.",
        "corrective": "Retain immutable module provenance plus redacted backend-control, plan, policy, apply, drift, idempotency, failure, and recovery evidence.",
        "preventive": "Require content-addressed plans, policy results, protected remote state, drift checks, and tested recovery before infrastructure change approval.",
        "unknown": "Resource coverage, ownership, backend locking and encryption, observed state, policy conformance, drift, idempotency, failure behavior, recovery, and blast radius remain unknown.",
    },
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def focus_binding(designation: str) -> dict[str, Any]:
    catalog = load(ROOT / "agents" / "focus-profiles" / "catalog.json")
    entry = next(item for item in catalog["profiles"] if item["designation"] == designation)
    profile = load(ROOT / entry["path"])
    return {
        "profile_id": entry["profile_id"], "profile_version": entry["profile_version"], "profile_hash": entry["sha256"],
        "source_specification": profile["source"]["specification"], "source_specification_hash": profile["source"]["specification_sha256"],
        "compiled_prompt_focus_hash": content_hash(focus_material(profile)),
        "compression_protected_elements": profile["prompt_binding"]["compression_protected_elements"],
    }


def agent(designation: str) -> dict[str, Any]:
    return next(item for item in load(ROOT / "agents" / "agent-identities.json")["agents"] if item["designation"] == designation)


def build_manifest(designation: str) -> dict[str, Any]:
    cfg, identity = CONFIG[designation], agent(designation)
    evidence = [{
        "evidence_id": evidence_id, "source_type": source_type, "path": path, "content_hash": file_hash,
        "classification": "public", "admitted": True, "safe_for_human_review": True,
        "allowed_reviewer_tracks": ["general_engineering_intern", "qualified_subject_matter_expert", "restricted_domain_reviewer"],
        "purpose": f"Review {designation} evidence in {section}.",
    } for evidence_id, path, _line, _text, section, file_hash, source_type in cfg["evidence"]]
    value = {
        "manifest_id": stable_uuid(designation, PRODUCT_ID, REVISION, f"{INCREMENT_KEY}-input"), "manifest_version": "1.0.0", "created_at": CREATED_AT,
        "candidate": {"agent_uuid": identity["agent_uuid"], "designation": designation, "agent_version": "design-0.2.0", "contract_version": identity["contract_version"], "product_id": PRODUCT_ID},
        "repository": {"repository_uri": REPOSITORY_URI, "immutable_revision": REVISION, "read_only": True, "modification_prohibited": True},
        "evidence_population": evidence, "focus_binding": focus_binding(designation), "execution_bindings": controlled_execution_bindings(designation),
        "environment": {"execution_mode": "specialist_human_shadow_calibration", "platform_class": "dgx_spark_or_equivalent", "environment_policy_version": ENVIRONMENT_POLICY_VERSION},
        "lifecycle": {"comparison_only": True, "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False, "retention_class": "specialist-human-shadow-calibration"},
        "manifest_hash": "sha256:" + "0" * 64,
    }
    value = seal_hash(value, "manifest_hash")
    validate_manifest(value)
    return value


def role_payload(designation: str, refs: list[str]) -> dict[str, Any]:
    cfg = CONFIG[designation]
    unknown = {"unknown_id": f"UNKNOWN-{designation.removeprefix('SPEC-')}-001", "statement": cfg["unknown"], "missing_evidence": [], "evidence_refs": refs}
    if designation == "SPEC-CONTAINER":
        unknown["missing_evidence"] = ["built image digest", "signature and provenance", "scan result", "runtime configuration"]
        return {"designation": designation, "images": [{"image_id": "IMAGE-KEYCLOAK-CRL-AIRGAP", "image_reference": None, "digest": None, "base_image": "scratch", "composition": "staged filesystem copied into scratch image", "registry_trust": "not_assessed", "signature_or_attestation": "not_observed", "artifact_provenance": "not_observed", "patch_lifecycle": "not_applicable_scratch_base", "runtime_user": "not_declared", "hardening_maturity": "not_demonstrated", "deployment_readiness": "unable_to_determine", "evidence_refs": refs}], "coverage": {"dockerfiles_reviewed": 1, "image_manifests_reviewed": 0, "built_images_scanned": 0, "signatures_verified": 0, "runtime_configs_reviewed": 0}, "measures": {"signed_image_rate": None, "supported_base_image_rate": None, "patch_currency": None, "reproducibility": "not_measurable", "runtime_assumption_coverage": None, "readiness_gap_count": 5}, "unknowns": [unknown], "authority_boundary": "image_and_artifact_assessment_only_no_live_cluster_release_or_product_approval"}
    if designation == "SPEC-CICD":
        unknown["missing_evidence"] = ["completed run records", "artifact identities and attestations", "gate outcomes", "rollback events"]
        return {"designation": designation, "pipelines": [
            {"pipeline_id": "PIPELINE-TAG-RELEASE", "pipeline_definition": ".github/workflows/tag-and-release.yaml", "pipeline_stage": "release", "trigger": "push to main or release branch", "permissions": "broad_write_observed", "action_pinning": "immutable_commit", "build_integrity": "partially_declared", "artifact_provenance": "not_observed", "promotion_flow": "explicit", "gate_effectiveness": "configured_not_demonstrated", "determinism": "partially_constrained", "resumability": "not_assessed", "rollback_evidence": "not_observed", "auditability": "partial", "evidence_refs": [refs[0], refs[2]]},
            {"pipeline_id": "PIPELINE-PUBLISH", "pipeline_definition": ".github/workflows/publish.yaml", "pipeline_stage": "publish", "trigger": "reusable workflow call", "permissions": "least_privilege_observed", "action_pinning": "not_assessed", "build_integrity": "partially_declared", "artifact_provenance": "not_observed", "promotion_flow": "explicit", "gate_effectiveness": "configured_not_demonstrated", "determinism": "not_demonstrated", "resumability": "not_assessed", "rollback_evidence": "not_observed", "auditability": "partial", "evidence_refs": [refs[1]]}],
            "coverage": {"pipeline_definitions_reviewed": 2, "completed_runs_reviewed": 0, "artifacts_verified": 0, "promotion_events_reviewed": 0, "rollback_events_reviewed": 0}, "measures": {"repeatability": None, "provenanced_artifact_coverage": None, "verification_gap_count": 6, "effective_gate_rate": None, "nondeterminism_rate": None, "recovery_maturity": "not_measurable"}, "unknowns": [unknown], "authority_boundary": "pipeline_evidence_only_no_release_risk_acceptance_or_product_approval"}
    unknown["missing_evidence"] = ["plans and applies", "state safeguards", "policy and drift results", "failure and recovery tests"]
    return {"designation": designation, "modules": [{"module_id": "IAC-EKS-KMS", "module": "generate_kms", "infrastructure_layer_owner": None, "module_maturity": "not_declared", "desired_state": "declared", "observed_state": "not_observed", "expected_state": "partial", "idempotency": "not_assessed", "policy_inheritance": "not_assessed", "dependency_order": "implicit", "partial_deployment_failure_mode": "not_assessed", "recovery_consideration": "not_observed", "change_blast_radius_prediction": "not_assessed", "evidence_refs": [refs[0]]}], "state_management": {"backend": "remote", "locking": "not_observed", "encryption": "not_observed", "access_control": "not_observed", "evidence_refs": [refs[1]]}, "coverage": {"iac_files_reviewed": 2, "modules_reviewed": 1, "plans_reviewed": 0, "applies_reviewed": 0, "drift_checks_reviewed": 0, "rollback_tests_reviewed": 0}, "measures": {"managed_resource_coverage": None, "policy_conformance": None, "drift_detection_readiness": "not_measurable", "idempotency_confidence": None, "partial_deployment_recovery_coverage": None, "ownership_clarity": None}, "unknowns": [unknown], "authority_boundary": "desired_state_assessment_only_no_runtime_health_deployment_or_product_approval"}


def build_candidate(manifest: dict[str, Any]) -> dict[str, Any]:
    designation = manifest["candidate"]["designation"]
    cfg, identity = CONFIG[designation], agent(designation)
    refs = [item["evidence_id"] for item in manifest["evidence_population"]]
    unknown = {"unknown_id": f"UNKNOWN-{designation.removeprefix('SPEC-')}-001", "statement": cfg["unknown"], "confidence": 1.0, "evidence_refs": refs}
    candidate = {
        "identity": {"agent_uuid": identity["agent_uuid"], "designation": designation, "display_name": cfg["display"], "agent_version": "design-0.2.0", "contract_version": identity["contract_version"]},
        "artifact": {"artifact_id": stable_uuid(manifest["manifest_id"], manifest["manifest_hash"], "candidate"), "artifact_type": f"{cfg['slug']}-shadow-candidate", "created_at": GENERATED_AT, "lifecycle_state": "complete", "links": {"parents": [manifest["manifest_id"]], "children": [], "peers": []}},
        "execution": {"execution_id": stable_uuid(manifest["manifest_id"], "execution"), "model": "deterministic-reference-agent", "prompt_version": "design-0.2.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}, "comparison_only": True, "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False, "input_manifest_id": manifest["manifest_id"], "focus_binding": manifest["focus_binding"], "execution_bindings": manifest["execution_bindings"]},
        "scope": {"product_id": PRODUCT_ID, "source_revision": REVISION, "included": sorted({item["path"] for item in manifest["evidence_population"]}), "excluded": [], "decision_context": "specialist_human_shadow_calibration"},
        "inputs": [{"evidence_id": item["evidence_id"], "reference": f"{REPOSITORY_URI}@{REVISION}:{item['path']}", "hash": item["content_hash"], "freshness": "immutable revision"} for item in manifest["evidence_population"]],
        "methodology": {"method": f"bounded deterministic {cfg['domain']} projection", "focus_profile_id": manifest["focus_binding"]["profile_id"], "limitations": [cfg["unknown"], "No external network, registry, pipeline execution, cloud, or runtime evidence was admitted.", "Human review is deferred and all output remains non-authoritative."]},
        "coverage": {"eligible": len(refs), "reviewed": len(refs), "omitted": 0, "inaccessible": 0, "unknown": 1, "negative_evidence": 0},
        "observations": [{"observation_id": f"OBS-{designation.removeprefix('SPEC-')}-001", "fact": cfg["observation"], "confidence": 1.0, "evidence_refs": refs}],
        "assessments": [{"assessment_id": f"ASM-{designation.removeprefix('SPEC-')}-001", "rationale": cfg["finding"], "confidence": 0.98, "evidence_refs": refs}],
        "findings": [{"finding_id": f"FINDING-{designation.removeprefix('SPEC-')}-001", "statement": cfg["finding"], "severity": "low", "confidence": 0.98, "evidence_refs": refs, "root_cause": "missing_execution_or_artifact_evidence", "impact": "The bounded specialist question cannot be fully answered from source definitions alone.", "capa": {"corrective_action": cfg["corrective"], "preventive_action": cfg["preventive"], "owner_role": "project-maintainer", "target_horizon": "before candidate completion", "implementation_level": "product", "validation_method": "Repeat the bounded review with immutable artifact and execution evidence."}}],
        "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 1.0, "assessment": 0.98, "review": None, "decision": None, "provenance": [{"source": f"ADR-0039 {INCREMENT_LABEL} deterministic projection", "version": "1.0.0"}]},
        "decisions_requested": [{"decision_context_id": f"DECISION-{designation.removeprefix('SPEC-')}-001", "question": "Should the requested evidence be added for continued candidate calibration?", "required_authority": "project_owner"}],
        "consumers": ["human-shadow-review-only"], "decision_authority": "human",
        "integrity": {"input_hash": manifest["manifest_hash"], "output_hash": content_hash({"manifest": manifest["manifest_hash"], "designation": designation}), "attestation_ref": None, "retention_class": "specialist-human-shadow-calibration", "schema_validation": "passed"},
        "extensions": {"specialist": {"product_id": PRODUCT_ID, "domain_scope": {"domain": cfg["domain"], "revision": REVISION}, "eligible_population": {"evidence_records": len(refs)}, "domain_observations": [{"observation_id": f"OBS-{designation.removeprefix('SPEC-')}-001"}], "domain_assessments": [{"assessment_id": f"ASM-{designation.removeprefix('SPEC-')}-001"}], "domain_findings": [{"finding_id": f"FINDING-{designation.removeprefix('SPEC-')}-001"}], "domain_patterns": [], "domain_unknowns": [unknown], "domain_coverage": {"reviewed_fraction": 1.0}, "domain_confidence": {"evidence": 1.0, "assessment": 0.98}, "product_consumers": ["human-shadow-review-only"], "role": role_payload(designation, refs)}}
    }
    validate_candidate_artifact(manifest, candidate)
    return candidate


def locator(evidence: tuple[str, str, int, str, str, str, str]) -> dict[str, Any]:
    evidence_id, path, line, excerpt, section, _file_hash, source_type = evidence
    value = {"locator_id": stable_uuid(evidence_id, REVISION, path, str(line)), "evidence_id": evidence_id, "source_type": source_type, "repository_uri": REPOSITORY_URI, "immutable_revision": REVISION, "path": path, "line_start": line, "line_end": line, "symbol_or_section": section, "safe_excerpt": excerpt, "redaction": {"applied": False, "method": "none_required_public_source", "raw_value_included": False}, "line_fingerprint": "sha256:" + hashlib.sha256((excerpt + "\n").encode()).hexdigest(), "collector": LOCATOR_COLLECTOR, "collection_method": "exact immutable source line", "collected_at": GENERATED_AT, "access": {"classification": "public", "constraints": ["read-only immutable revision"], "reviewer_instructions": ["Compare the exact revision, path, line, excerpt, and fingerprint after consolidated review begins."]}, "reproduction_steps": [f"Open {REPOSITORY_URI} at {REVISION}.", f"Inspect {path} line {line}.", "Compare the safe excerpt and fingerprint."], "locator_state": "source_located", "locator_hash": "sha256:" + "0" * 64}
    return seal_hash(value, "locator_hash")


def render_packet(packet: dict[str, Any]) -> str:
    lines = [f"# {packet['candidate']['designation']} Deferred Human Shadow Review Packet", "", f"Reviewability: **{packet['reviewability_state']}**", "", "Retained for consolidated end-of-program human review. Comparison-only; no admission, scheduling, report, deployment, or A100 authority.", ""]
    for item in packet["items"]:
        lines += [f"## {item['item_id']} - {item['kind']}", "", item["statement"], ""]
        for loc in item["locators"]:
            lines += [f"- `{loc['path']}` line {loc['line_start']}: `{loc['safe_excerpt']}`", f"- Revision: `{loc['immutable_revision']}`", ""]
    return "\n".join(lines)


def generate(output: Path) -> dict[str, Any]:
    summary = {"increment": INCREMENT_SUMMARY, "state": "candidate_packets_retained_human_review_deferred", "source_repository": REPOSITORY_URI, "source_revision": REVISION, "candidates": [], "human_review_deferred": True, "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False}
    for designation, cfg in CONFIG.items():
        manifest = build_manifest(designation)
        candidate = build_candidate(manifest)
        locators = [locator(item) for item in cfg["evidence"]]
        control = build_control_record(manifest, "enable_calibration", CREATED_AT, "thomasverburgt", f"ADR-0039 {INCREMENT_LABEL} project-owner authorization")
        packet = build_review_packet(manifest, candidate, locators, GENERATED_AT)
        target = output / cfg["slug"]
        for name, value in (("input-manifest.json", manifest), ("control-enable.json", control), ("candidate.artifact.json", candidate), ("evidence-locators.json", locators), ("human-shadow-review-packet.json", packet)):
            atomic_write(target / name, pretty_bytes(value))
        atomic_write(target / "human-shadow-review-packet.md", (render_packet(packet) + "\n").encode())
        summary["candidates"].append({"designation": designation, "manifest_id": manifest["manifest_id"], "artifact_id": candidate["artifact"]["artifact_id"], "packet_id": packet["packet_id"], "reviewability": packet["reviewability_state"], "review_state": "deferred", "item_count": len(packet["items"])})
    atomic_write(output / "summary.json", pretty_bytes(summary))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(generate(args.output.resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

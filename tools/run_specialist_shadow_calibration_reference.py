#!/usr/bin/env python3
"""Generate the deterministic ADR-0039 Increment 0 reference package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from artifact_ledger import atomic_write, content_hash, pretty_bytes
from specialist_shadow_calibration_runtime import (
    ROOT,
    build_control_record,
    build_metrics,
    build_review_packet,
    build_review_response,
    canonical_file_hash,
    focus_material,
    persist_calibration,
    seal_hash,
    stable_uuid,
    validate_candidate_artifact,
    validate_manifest,
)


DESIGNATION = "SPEC-DEPS"
AGENT_UUID = "7e7d7710-885a-47c6-af0f-339ed9dad525"
REPOSITORY_URI = "https://github.com/thomasverburgt/Code-Review-Harness.git"
IMMUTABLE_REVISION = "ada870cc7fc557a417f4215c8e60fbf3bee367d9"
PRODUCT_ID = "CODE-HARNESS-PROJECT-001"
CREATED_AT = "2026-08-03T15:00:00Z"
GENERATED_AT = "2026-08-03T15:05:00Z"
REVIEW_STARTED_AT = "2026-08-03T15:10:00Z"
REVIEW_COMPLETED_AT = "2026-08-03T15:40:00Z"
CONTROL_REVOKED_AT = "2026-08-03T15:45:00Z"
DEFAULT_OUTPUT = ROOT / "fixtures" / "specialist-shadow-calibration" / "gold"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def binding(binding_id: str) -> dict[str, str]:
    version = "increment-0.1.0"
    return {"id": binding_id, "version": version, "hash": content_hash({"id": binding_id, "version": version})}


def build_manifest() -> dict[str, Any]:
    catalog = load_json(ROOT / "agents" / "focus-profiles" / "catalog.json")
    entry = next(item for item in catalog["profiles"] if item["designation"] == DESIGNATION)
    profile = load_json(ROOT / entry["path"])
    evidence_hash = canonical_file_hash(ROOT / "pyproject.toml")
    manifest = {
        "manifest_id": stable_uuid(DESIGNATION, PRODUCT_ID, IMMUTABLE_REVISION, "input-manifest"),
        "manifest_version": "1.0.0",
        "created_at": CREATED_AT,
        "candidate": {
            "agent_uuid": AGENT_UUID,
            "designation": DESIGNATION,
            "agent_version": "design-0.1.0",
            "contract_version": "1.0.0",
            "product_id": PRODUCT_ID,
        },
        "repository": {
            "repository_uri": REPOSITORY_URI,
            "immutable_revision": IMMUTABLE_REVISION,
            "read_only": True,
            "modification_prohibited": True,
        },
        "evidence_population": [
            {
                "evidence_id": "EVIDENCE-DEPS-BUILD-001",
                "source_type": "configuration",
                "path": "pyproject.toml",
                "content_hash": evidence_hash,
                "classification": "public",
                "admitted": True,
                "safe_for_human_review": True,
                "allowed_reviewer_tracks": [
                    "general_engineering_intern",
                    "qualified_subject_matter_expert",
                    "restricted_domain_reviewer",
                ],
                "purpose": "Review the declared build-system dependency constraint.",
            },
            {
                "evidence_id": "EVIDENCE-DEPS-DOCS-001",
                "source_type": "configuration",
                "path": "pyproject.toml",
                "content_hash": evidence_hash,
                "classification": "public",
                "admitted": True,
                "safe_for_human_review": True,
                "allowed_reviewer_tracks": [
                    "general_engineering_intern",
                    "qualified_subject_matter_expert",
                    "restricted_domain_reviewer",
                ],
                "purpose": "Review the optional documentation dependency declaration.",
            },
        ],
        "focus_binding": {
            "profile_id": entry["profile_id"],
            "profile_version": entry["profile_version"],
            "profile_hash": entry["sha256"],
            "source_specification": profile["source"]["specification"],
            "source_specification_hash": profile["source"]["specification_sha256"],
            "compiled_prompt_focus_hash": content_hash(focus_material(profile)),
            "compression_protected_elements": profile["prompt_binding"]["compression_protected_elements"],
        },
        "execution_bindings": {
            "prompt": binding("SPECIALIST-SHADOW-PROMPT-SPEC-DEPS"),
            "role_schema": binding("SPECIALIST-EXTENSION"),
            "rubric": binding("SPECIALIST-SHADOW-RUBRIC-SPEC-DEPS"),
            "model_manifest": binding("DETERMINISTIC-REFERENCE-MODEL"),
            "tool_policy": binding("READ-ONLY-EVIDENCE-TOOLS"),
        },
        "environment": {
            "execution_mode": "specialist_human_shadow_calibration",
            "platform_class": "dgx_spark_or_equivalent",
            "environment_policy_version": "1.0.0",
        },
        "lifecycle": {
            "comparison_only": True,
            "scheduled": False,
            "product_fan_in_eligible": False,
            "deployment_authorized": False,
            "a100_production_authorized": False,
            "retention_class": "specialist-human-shadow-calibration",
        },
        "manifest_hash": "sha256:" + "0" * 64,
    }
    manifest = seal_hash(manifest, "manifest_hash")
    validate_manifest(manifest)
    return manifest


def build_candidate(manifest: dict[str, Any]) -> dict[str, Any]:
    candidate = {
        "identity": {
            "agent_uuid": AGENT_UUID,
            "designation": DESIGNATION,
            "display_name": "Dependency Reviewer",
            "agent_version": "design-0.1.0",
            "contract_version": "1.0.0",
        },
        "artifact": {
            "artifact_id": stable_uuid(manifest["manifest_id"], manifest["manifest_hash"], "candidate-artifact"),
            "artifact_type": "specialist-dependency-shadow-candidate",
            "created_at": GENERATED_AT,
            "lifecycle_state": "complete",
            "links": {"parents": [manifest["manifest_id"]], "children": [], "peers": []},
        },
        "execution": {
            "execution_id": stable_uuid(manifest["manifest_id"], "execution"),
            "model": "deterministic-reference-agent",
            "prompt_version": "increment-0.1.0",
            "rubric_version": "increment-0.1.0",
            "toolchain_version": "increment-0.1.0",
            "settings": {"temperature": 0},
            "comparison_only": True,
            "scheduled": False,
            "product_fan_in_eligible": False,
            "deployment_authorized": False,
            "a100_production_authorized": False,
            "input_manifest_id": manifest["manifest_id"],
            "focus_binding": manifest["focus_binding"],
        },
        "scope": {
            "product_id": PRODUCT_ID,
            "source_revision": IMMUTABLE_REVISION,
            "included": ["pyproject.toml"],
            "excluded": [],
            "decision_context": "specialist_human_shadow_calibration",
        },
        "inputs": [
            {
                "evidence_id": item["evidence_id"],
                "reference": f"{REPOSITORY_URI}@{IMMUTABLE_REVISION}:{item['path']}",
                "hash": item["content_hash"],
                "freshness": "immutable reference fixture",
            }
            for item in manifest["evidence_population"]
        ],
        "methodology": {
            "method": "Bounded deterministic inspection of declared dependency entries",
            "focus_profile_id": manifest["focus_binding"]["profile_id"],
            "limitations": [
                "The fixture does not resolve the transitive dependency graph.",
                "The fixture does not establish vulnerability, license, or runtime supportability status.",
                "Human shadow dispositions are calibration evidence and do not establish correctness.",
            ],
        },
        "coverage": {"eligible": 2, "reviewed": 2, "omitted": 0, "inaccessible": 0, "unknown": 0, "negative_evidence": 0},
        "observations": [
            {
                "observation_id": "OBS-DEPS-001",
                "fact": "The build system declares setuptools as a required build dependency.",
                "confidence": 1.0,
                "evidence_refs": ["EVIDENCE-DEPS-BUILD-001"],
            }
        ],
        "assessments": [
            {
                "assessment_id": "ASM-DEPS-001",
                "rationale": "An unconstrained build dependency can resolve differently across clean build environments.",
                "confidence": 0.94,
                "evidence_refs": ["EVIDENCE-DEPS-BUILD-001"],
            }
        ],
        "findings": [
            {
                "finding_id": "FINDING-DEPS-001",
                "statement": "The setuptools build-system dependency is declared without a version constraint.",
                "severity": "low",
                "confidence": 0.98,
                "evidence_refs": ["EVIDENCE-DEPS-BUILD-001"],
                "root_cause": "dependency_constraint_not_declared",
                "impact": "Clean builds may select different supported setuptools releases over time.",
                "capa": {
                    "corrective_action": "Declare a tested setuptools compatibility range in build-system.requires.",
                    "preventive_action": "Exercise clean-build reproducibility in CI when dependency constraints change.",
                    "owner_role": "build-maintainer",
                    "target_horizon": "before candidate admission",
                    "implementation_level": "product",
                    "validation_method": "Rebuild in a clean environment and compare the resolved build tool version and artifact hash.",
                },
            }
        ],
        "patterns": [
            {
                "pattern_id": "PATTERN-DEPS-001",
                "statement": "The optional documentation dependency uses an exact python-docx version pin.",
                "confidence": 1.0,
                "evidence_refs": ["EVIDENCE-DEPS-DOCS-001"],
            }
        ],
        "insights": [],
        "conflicts": [],
        "confidence": {
            "evidence": 1.0,
            "assessment": 0.98,
            "review": None,
            "decision": None,
            "provenance": [{"source": "deterministic Increment 0 reference fixture", "version": "1.0.0"}],
        },
        "decisions_requested": [
            {
                "decision_context_id": "DECISION-DEPS-001",
                "question": "Should the project define and test a setuptools compatibility range?",
                "required_authority": "project_owner",
            }
        ],
        "consumers": ["human-shadow-review-only"],
        "decision_authority": "human",
        "integrity": {
            "input_hash": manifest["manifest_hash"],
            "output_hash": content_hash({"manifest_hash": manifest["manifest_hash"], "designation": DESIGNATION, "fixture": "reference"}),
            "attestation_ref": None,
            "retention_class": "specialist-human-shadow-calibration",
            "schema_validation": "passed",
        },
        "extensions": {
            "specialist": {
                "product_id": PRODUCT_ID,
                "domain_scope": {"domain": "dependency_health", "revision": IMMUTABLE_REVISION},
                "eligible_population": {"files": 1, "dependency_entries": 2},
                "domain_observations": [{"observation_id": "OBS-DEPS-001"}],
                "domain_assessments": [{"assessment_id": "ASM-DEPS-001"}],
                "domain_findings": [{"finding_id": "FINDING-DEPS-001"}],
                "domain_patterns": [{"pattern_id": "PATTERN-DEPS-001"}],
                "domain_unknowns": [
                    {
                        "unknown_id": "UNKNOWN-DEPS-001",
                        "statement": "Transitive dependency health is unknown because no resolved dependency graph was admitted.",
                        "confidence": 1.0,
                        "evidence_refs": ["EVIDENCE-DEPS-BUILD-001"],
                    }
                ],
                "domain_coverage": {"declared_entries_reviewed_fraction": 1.0, "transitive_graph_reviewed": False},
                "domain_confidence": {"evidence": 1.0, "assessment": 0.98},
                "product_consumers": ["human-shadow-review-only"],
                "role": {
                    "designation": DESIGNATION,
                    "focus_profile_id": manifest["focus_binding"]["profile_id"],
                    "dependency_observations": ["OBS-DEPS-001", "FINDING-DEPS-001", "PATTERN-DEPS-001"],
                },
            }
        },
    }
    validate_candidate_artifact(manifest, candidate)
    return candidate


def fingerprint(line: str) -> str:
    return "sha256:" + hashlib.sha256((line + "\n").encode("utf-8")).hexdigest()


def build_locator(evidence_id: str, line_number: int, line: str, section: str) -> dict[str, Any]:
    locator = {
        "locator_id": stable_uuid(evidence_id, IMMUTABLE_REVISION, "pyproject.toml", str(line_number)),
        "evidence_id": evidence_id,
        "source_type": "configuration",
        "repository_uri": REPOSITORY_URI,
        "immutable_revision": IMMUTABLE_REVISION,
        "path": "pyproject.toml",
        "line_start": line_number,
        "line_end": line_number,
        "symbol_or_section": section,
        "safe_excerpt": line,
        "redaction": {"applied": False, "method": "none_required_public_source", "raw_value_included": False},
        "line_fingerprint": fingerprint(line),
        "collector": "deterministic-increment-0-reference",
        "collection_method": "exact immutable source line",
        "collected_at": GENERATED_AT,
        "access": {
            "classification": "public",
            "constraints": ["Read-only review of the immutable revision."],
            "reviewer_instructions": ["Open the immutable revision and compare the exact path, line, excerpt, and fingerprint."],
        },
        "reproduction_steps": [
            f"Open {REPOSITORY_URI} at commit {IMMUTABLE_REVISION}.",
            f"Open pyproject.toml and inspect line {line_number} in section {section}.",
            "Compare the line with the safe excerpt and SHA-256 line fingerprint.",
        ],
        "locator_state": "source_located",
        "locator_hash": "sha256:" + "0" * 64,
    }
    return seal_hash(locator, "locator_hash")


def build_response(packet: dict[str, Any]) -> dict[str, Any]:
    reviews = []
    for item in packet["items"]:
        reviews.append({
            "item_id": item["item_id"],
            "disposition": "supported",
            "rationale": "The bounded statement is supported by the cited immutable source line; broader dependency health remains unproven.",
            "locator_correctness": "correct",
            "severity_reasonableness": "reasonable" if item["kind"] == "finding" else "not_applicable",
            "recommendation_reasonableness": "reasonable" if item["kind"] == "recommendation" else "not_applicable",
            "missing_evidence": ["Resolved transitive dependency graph"] if item["kind"] == "unknown" else [],
        })
    return build_review_response(
        packet,
        reviewer={
            "reviewer_id": "FIXTURE-INTERN-001",
            "reviewer_track": "general_engineering_intern",
            "experience_level": "intern",
            "domain_qualifications": ["Python package manifest reading"],
            "authorized_classifications": ["public"],
            "conflict_of_interest": None,
        },
        item_reviews=reviews,
        overall_usability={
            "rating": 4,
            "rationale": "The packet is reviewable because every item identifies an exact source file and immutable location.",
            "would_request_more_evidence": True,
        },
        evidence_requests=["Provide a resolved dependency graph before assessing transitive dependency health."],
        started_at=REVIEW_STARTED_AT,
        completed_at=REVIEW_COMPLETED_AT,
    )


def render_packet(packet: dict[str, Any]) -> str:
    lines = [
        "# Specialist Human Shadow Review Packet",
        "",
        f"Candidate: `{packet['candidate']['designation']}`",
        f"Packet: `{packet['packet_id']}`",
        f"Reviewability: **{packet['reviewability_state']}**",
        f"Classification: `{packet['classification']}`",
        "",
        "This packet supports comparison-only human calibration. It does not approve a finding, admit an agent, alter a product report, or authorize deployment.",
        "",
    ]
    for item in packet["items"]:
        lines.extend([f"## {item['item_id']} — {item['kind']}", "", item["statement"], "", f"Source record: `{item['source_record_id']}`", f"Reviewability: `{item['reviewability']}`", ""])
        for locator in item["locators"]:
            lines.extend([
                f"- Evidence: `{locator['evidence_id']}`",
                f"- Repository: `{locator['repository_uri']}`",
                f"- Revision: `{locator['immutable_revision']}`",
                f"- File: `{locator['path']}` (line {locator['line_start']})",
                f"- Safe excerpt: `{locator['safe_excerpt']}`",
                f"- Fingerprint: `{locator['line_fingerprint']}`",
                "",
            ])
    return "\n".join(lines)


def generate(output: Path) -> dict[str, Any]:
    manifest = build_manifest()
    candidate = build_candidate(manifest)
    locators = [
        build_locator("EVIDENCE-DEPS-BUILD-001", 2, 'requires = ["setuptools"]', "build-system"),
        build_locator("EVIDENCE-DEPS-DOCS-001", 15, 'docs = ["python-docx==1.2.0"]', "project.optional-dependencies"),
    ]
    packet = build_review_packet(manifest, candidate, locators, GENERATED_AT)
    response = build_response(packet)
    metrics = build_metrics(packet, [response], CONTROL_REVOKED_AT)
    enable = build_control_record(manifest, "enable_calibration", CREATED_AT, "thomasverburgt", "ADR-0039")
    revoke = build_control_record(manifest, "revoke_calibration", CONTROL_REVOKED_AT, "thomasverburgt", "ADR-0039 rollback demonstration")
    summary = persist_calibration(output / "ledger", manifest, enable, candidate, locators, packet, [response], metrics, revoke)
    files = {
        "input-manifest.json": manifest,
        "control-enable.json": enable,
        "candidate.artifact.json": candidate,
        "evidence-locators.json": locators,
        "human-shadow-review-packet.json": packet,
        "human-shadow-review-response.json": response,
        "human-shadow-review-metrics.json": metrics,
        "control-revoke.json": revoke,
        "summary.json": summary,
    }
    for name, value in files.items():
        atomic_write(output / name, pretty_bytes(value))
    atomic_write(output / "human-shadow-review-packet.md", (render_packet(packet) + "\n").encode("utf-8"))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = generate(args.output.resolve())
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

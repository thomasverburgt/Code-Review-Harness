#!/usr/bin/env python3
"""Build deterministic ADR-0039 Increment 1 candidates and human-review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from artifact_ledger import atomic_write, content_hash, pretty_bytes
from specialist_shadow_calibration_runtime import (
    ROOT, build_control_record, build_review_packet, canonical_file_hash,
    controlled_execution_bindings, focus_material, seal_hash, stable_uuid,
    validate_candidate_artifact, validate_manifest,
)

REPOSITORY_URI = "https://github.com/thomasverburgt/Code-Review-Harness.git"
REVISION = "ada870cc7fc557a417f4215c8e60fbf3bee367d9"
PRODUCT_ID = "CODE-HARNESS-PROJECT-001"
CREATED_AT = "2026-08-03T17:00:00Z"
GENERATED_AT = "2026-08-03T17:05:00Z"
DEFAULT_OUTPUT = ROOT / "fixtures" / "specialist-static-evidence-increment1" / "gold"

CONFIG = {
    "SPEC-DEPS": {
        "slug": "spec-deps", "display": "Dependency Reviewer", "domain": "dependency_health",
        "evidence": [
            ("EVIDENCE-DEPS-BUILD-001", "pyproject.toml", 2, 'requires = ["setuptools"]', "build-system"),
            ("EVIDENCE-DEPS-DOCS-001", "pyproject.toml", 15, 'docs = ["python-docx==1.2.0"]', "project.optional-dependencies"),
        ],
        "observation": "The declared manifest contains one unconstrained build dependency and one exactly pinned optional documentation dependency.",
        "finding": "The setuptools build-system dependency is declared without a version constraint.",
        "corrective": "Declare and test a setuptools compatibility range.",
        "preventive": "Record the resolved build-tool version during clean-build reproducibility checks.",
        "unknown": "Transitive dependency health, runtime loading, maintenance, licensing, and replacement risk are not measurable from the admitted manifest alone.",
    },
    "SPEC-SBOM": {
        "slug": "spec-sbom", "display": "Software Composition and SBOM Reviewer", "domain": "software_inventory",
        "evidence": [
            ("EVIDENCE-SBOM-BUILD-001", "pyproject.toml", 2, 'requires = ["setuptools"]', "build-system"),
            ("EVIDENCE-SBOM-DOCS-001", "pyproject.toml", 15, 'docs = ["python-docx==1.2.0"]', "project.optional-dependencies"),
        ],
        "observation": "The manifest declares setuptools and python-docx components for the bounded source population.",
        "finding": "The admitted evidence contains declarations but no resolved, artifact-derived, or signed SBOM inventory.",
        "corrective": "Generate a content-addressed SBOM from the resolved build and retain its method and source population.",
        "preventive": "Compare SBOM identity and component drift for each candidate artifact.",
        "unknown": "Transitive components, artifact contents, suppliers, package identifiers, and runtime inventory are unknown.",
    },
    "SPEC-LINT": {
        "slug": "spec-lint", "display": "Linter and Code Quality Reviewer", "domain": "defined_quality_rules",
        "evidence": [
            ("EVIDENCE-LINT-ENTRY-001", "pyproject.toml", 18, 'harness-check = "code_harness.cli:check_repository"', "project.scripts"),
            ("EVIDENCE-LINT-RULE-001", "tools/check_repository_structure.py", 38, "def check_utf8_and_mojibake(errors: list[str]) -> None:", "check_utf8_and_mojibake"),
        ],
        "observation": "The project declares a repository-check command and implements a text-integrity rule function.",
        "finding": "No completed checker execution result is admitted for this candidate evidence population.",
        "corrective": "Execute the pinned checker against the immutable revision and retain its source population, exit code, and output.",
        "preventive": "Require a content-addressed quality-rule execution record for every candidate revision.",
        "unknown": "Rule execution coverage, violations, suppressions, false positives, complexity, and trend are unknown without a completed result.",
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
    registry = load(ROOT / "agents" / "agent-identities.json")
    return next(item for item in registry["agents"] if item["designation"] == designation)


def build_manifest(designation: str) -> dict[str, Any]:
    cfg, identity = CONFIG[designation], agent(designation)
    evidence = []
    for evidence_id, path, _line, _text, section in cfg["evidence"]:
        evidence.append({
            "evidence_id": evidence_id, "source_type": "configuration" if path == "pyproject.toml" else "git_source",
            "path": path, "content_hash": canonical_file_hash(ROOT / path), "classification": "public", "admitted": True,
            "safe_for_human_review": True,
            "allowed_reviewer_tracks": ["general_engineering_intern", "qualified_subject_matter_expert", "restricted_domain_reviewer"],
            "purpose": f"Review {designation} evidence in {section}.",
        })
    value = {
        "manifest_id": stable_uuid(designation, PRODUCT_ID, REVISION, "increment-1-input"), "manifest_version": "1.0.0", "created_at": CREATED_AT,
        "candidate": {"agent_uuid": identity["agent_uuid"], "designation": designation, "agent_version": "design-0.2.0", "contract_version": identity["contract_version"], "product_id": PRODUCT_ID},
        "repository": {"repository_uri": REPOSITORY_URI, "immutable_revision": REVISION, "read_only": True, "modification_prohibited": True},
        "evidence_population": evidence, "focus_binding": focus_binding(designation), "execution_bindings": controlled_execution_bindings(designation),
        "environment": {"execution_mode": "specialist_human_shadow_calibration", "platform_class": "dgx_spark_or_equivalent", "environment_policy_version": "increment-1.0.0"},
        "lifecycle": {"comparison_only": True, "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False, "retention_class": "specialist-human-shadow-calibration"},
        "manifest_hash": "sha256:" + "0" * 64,
    }
    value = seal_hash(value, "manifest_hash"); validate_manifest(value); return value


def role_payload(designation: str, refs: list[str]) -> dict[str, Any]:
    if designation == "SPEC-DEPS":
        return {"designation": designation, "graph_nodes": [
            {"node_id": "DEP-SETUPTOOLS", "component_name": "setuptools", "version": None, "dependency_intent": "tooling", "ownership_or_stewardship": None, "critical_path_tags": ["build"], "version_drift": "unconstrained", "maintenance_signal": "not_assessed", "license_risk": "not_assessed", "replacement_complexity": "not_assessed", "stability_trajectory": "not_assessed", "evidence_refs": [refs[0]]},
            {"node_id": "DEP-PYTHON-DOCX", "component_name": "python-docx", "version": "1.2.0", "dependency_intent": "tooling", "ownership_or_stewardship": None, "critical_path_tags": ["documentation"], "version_drift": "constrained", "maintenance_signal": "not_assessed", "license_risk": "not_assessed", "replacement_complexity": "not_assessed", "stability_trajectory": "not_assessed", "evidence_refs": [refs[1]]}],
            "graph_edges": [{"edge_id": "EDGE-BUILD-SETUPTOOLS", "from_node": PRODUCT_ID, "to_node": "DEP-SETUPTOOLS", "coupling_type": "build", "circularity": "not_assessed", "orphan_status": "not_assessed", "evidence_refs": [refs[0]]}],
            "coverage": {"declared_nodes": 2, "reviewed_nodes": 2, "resolved_graph_available": False, "runtime_loading_reviewed": False},
            "measures": {"circular_count": None, "orphan_count": None, "duplicate_library_count": None, "abandoned_exposure_count": None, "critical_path_concentration": None, "graph_trend": "not_measurable"},
            "unknowns": [{"unknown_id": "UNKNOWN-DEPS-001", "statement": CONFIG[designation]["unknown"], "missing_evidence": ["resolved graph", "runtime loading evidence"], "evidence_refs": [refs[0]]}],
            "authority_boundary": "dependency_assessment_only_no_vulnerability_release_or_product_approval"}
    if designation == "SPEC-SBOM":
        return {"designation": designation, "generation_method": {"method": "declared_manifest_projection", "tool": "harness deterministic manifest projector", "tool_version": "0.1.0", "format": "internal_projection", "generated_at": GENERATED_AT, "source_population": ["pyproject.toml"], "evidence_refs": refs},
            "components": [
                {"component_id": "COMP-SETUPTOOLS", "component_name": "setuptools", "version": None, "purl_or_cpe": None, "supplier": None, "license": None, "component_criticality": "not_assessed", "source_of_inventory": "pyproject.toml:build-system.requires", "build_system": "setuptools.build_meta", "package_manager": "Python build-system declaration", "first_seen": None, "last_seen": None, "lineage": "direct", "inventory_completeness": "partial", "inventory_drift": "not_comparable", "dependency_confidence": 1.0, "evidence_refs": [refs[0]]},
                {"component_id": "COMP-PYTHON-DOCX", "component_name": "python-docx", "version": "1.2.0", "purl_or_cpe": None, "supplier": None, "license": None, "component_criticality": "not_assessed", "source_of_inventory": "pyproject.toml:project.optional-dependencies.docs", "build_system": None, "package_manager": "Python project declaration", "first_seen": None, "last_seen": None, "lineage": "direct", "inventory_completeness": "partial", "inventory_drift": "not_comparable", "dependency_confidence": 1.0, "evidence_refs": [refs[1]]}],
            "changes": [], "coverage": {"declared_components": 2, "identified_components": 2, "resolved_components": 0, "artifacts_scanned": 0, "runtime_components_reviewed": 0},
            "measures": {"inventory_coverage": None, "identification_confidence": 1.0, "sbom_completeness": None, "unexplained_drift_count": None, "critical_component_coverage": None},
            "unknowns": [{"unknown_id": "UNKNOWN-SBOM-001", "statement": CONFIG[designation]["unknown"], "missing_evidence": ["resolved SBOM", "artifact scan"], "evidence_refs": refs}],
            "authority_boundary": "inventory_evidence_only_no_vulnerability_release_or_governance_decision"}
    return {"designation": designation, "rule_set": {"rule_set_id": "REPOSITORY-STRUCTURE-CHECK", "rule_version": None, "languages_or_frameworks": ["Python", "repository metadata"], "configuration_refs": ["pyproject.toml:project.scripts.harness-check"], "evidence_refs": refs},
        "executions": [], "violations": [], "suppressions": [],
        "quality_gate": {"defined": True, "threshold": "zero structural check errors", "observed_result": None, "gate_state": "not_executed", "authority_effect": "quality_signal_only"},
        "measures": {"eligible_files": 0, "reviewed_files": 0, "violation_count": 0, "suppression_count": 0, "autofixable_count": 0, "complexity_trend": "not_measurable"},
        "unknowns": [{"unknown_id": "UNKNOWN-LINT-001", "statement": CONFIG[designation]["unknown"], "missing_evidence": ["completed checker execution record"], "evidence_refs": refs}],
        "authority_boundary": "defined_quality_rule_assessment_only_no_architecture_security_or_release_approval"}


def build_candidate(manifest: dict[str, Any]) -> dict[str, Any]:
    designation, cfg, identity = manifest["candidate"]["designation"], CONFIG[manifest["candidate"]["designation"]], agent(manifest["candidate"]["designation"])
    refs = [item["evidence_id"] for item in manifest["evidence_population"]]
    unknown = {"unknown_id": f"UNKNOWN-{designation.removeprefix('SPEC-')}-001", "statement": cfg["unknown"], "confidence": 1.0, "evidence_refs": refs}
    candidate = {
        "identity": {"agent_uuid": identity["agent_uuid"], "designation": designation, "display_name": cfg["display"], "agent_version": "design-0.2.0", "contract_version": identity["contract_version"]},
        "artifact": {"artifact_id": stable_uuid(manifest["manifest_id"], manifest["manifest_hash"], "candidate"), "artifact_type": f"{cfg['slug']}-shadow-candidate", "created_at": GENERATED_AT, "lifecycle_state": "complete", "links": {"parents": [manifest["manifest_id"]], "children": [], "peers": []}},
        "execution": {"execution_id": stable_uuid(manifest["manifest_id"], "execution"), "model": "deterministic-reference-agent", "prompt_version": "design-0.2.0", "rubric_version": "0.1.0", "toolchain_version": "0.1.0", "settings": {"temperature": 0}, "comparison_only": True, "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False, "input_manifest_id": manifest["manifest_id"], "focus_binding": manifest["focus_binding"], "execution_bindings": manifest["execution_bindings"]},
        "scope": {"product_id": PRODUCT_ID, "source_revision": REVISION, "included": sorted({item["path"] for item in manifest["evidence_population"]}), "excluded": [], "decision_context": "specialist_human_shadow_calibration"},
        "inputs": [{"evidence_id": item["evidence_id"], "reference": f"{REPOSITORY_URI}@{REVISION}:{item['path']}", "hash": item["content_hash"], "freshness": "immutable revision"} for item in manifest["evidence_population"]],
        "methodology": {"method": f"bounded deterministic {cfg['domain']} projection", "focus_profile_id": manifest["focus_binding"]["profile_id"], "limitations": [cfg["unknown"], "No external network evidence was admitted.", "Human review remains non-authoritative calibration evidence."]},
        "coverage": {"eligible": len(refs), "reviewed": len(refs), "omitted": 0, "inaccessible": 0, "unknown": 1, "negative_evidence": 0},
        "observations": [{"observation_id": f"OBS-{designation.removeprefix('SPEC-')}-001", "fact": cfg["observation"], "confidence": 1.0, "evidence_refs": refs}],
        "assessments": [{"assessment_id": f"ASM-{designation.removeprefix('SPEC-')}-001", "rationale": cfg["finding"], "confidence": 0.98, "evidence_refs": refs}],
        "findings": [{"finding_id": f"FINDING-{designation.removeprefix('SPEC-')}-001", "statement": cfg["finding"], "severity": "low", "confidence": 0.98, "evidence_refs": refs, "root_cause": "missing_or_incomplete_declared_evidence", "impact": "The bounded specialist question cannot be fully answered from the admitted population.", "capa": {"corrective_action": cfg["corrective"], "preventive_action": cfg["preventive"], "owner_role": "project-maintainer", "target_horizon": "before candidate completion", "implementation_level": "product", "validation_method": "Repeat the review against the newly admitted immutable evidence."}}],
        "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 1.0, "assessment": 0.98, "review": None, "decision": None, "provenance": [{"source": "ADR-0039 Increment 1 deterministic projection", "version": "1.0.0"}]},
        "decisions_requested": [{"decision_context_id": f"DECISION-{designation.removeprefix('SPEC-')}-001", "question": "Should the requested evidence be added for continued candidate calibration?", "required_authority": "project_owner"}],
        "consumers": ["human-shadow-review-only"], "decision_authority": "human",
        "integrity": {"input_hash": manifest["manifest_hash"], "output_hash": content_hash({"manifest": manifest["manifest_hash"], "designation": designation}), "attestation_ref": None, "retention_class": "specialist-human-shadow-calibration", "schema_validation": "passed"},
        "extensions": {"specialist": {"product_id": PRODUCT_ID, "domain_scope": {"domain": cfg["domain"], "revision": REVISION}, "eligible_population": {"evidence_records": len(refs)}, "domain_observations": [{"observation_id": f"OBS-{designation.removeprefix('SPEC-')}-001"}], "domain_assessments": [{"assessment_id": f"ASM-{designation.removeprefix('SPEC-')}-001"}], "domain_findings": [{"finding_id": f"FINDING-{designation.removeprefix('SPEC-')}-001"}], "domain_patterns": [], "domain_unknowns": [unknown], "domain_coverage": {"reviewed_fraction": 1.0}, "domain_confidence": {"evidence": 1.0, "assessment": 0.98}, "product_consumers": ["human-shadow-review-only"], "role": role_payload(designation, refs)}}
    }
    validate_candidate_artifact(manifest, candidate); return candidate


def locator(evidence: tuple[str, str, int, str, str]) -> dict[str, Any]:
    evidence_id, path, line, text, section = evidence
    value = {"locator_id": stable_uuid(evidence_id, REVISION, path, str(line)), "evidence_id": evidence_id, "source_type": "configuration" if path == "pyproject.toml" else "git_source", "repository_uri": REPOSITORY_URI, "immutable_revision": REVISION, "path": path, "line_start": line, "line_end": line, "symbol_or_section": section, "safe_excerpt": text, "redaction": {"applied": False, "method": "none_required_public_source", "raw_value_included": False}, "line_fingerprint": "sha256:" + hashlib.sha256((text + "\n").encode()).hexdigest(), "collector": "increment-1-deterministic-reference", "collection_method": "exact immutable source line", "collected_at": GENERATED_AT, "access": {"classification": "public", "constraints": ["read-only immutable revision"], "reviewer_instructions": ["Compare the exact revision, path, line, excerpt, and fingerprint."]}, "reproduction_steps": [f"Open {REPOSITORY_URI} at {REVISION}.", f"Inspect {path} line {line}.", "Compare the safe excerpt and fingerprint."], "locator_state": "source_located", "locator_hash": "sha256:" + "0" * 64}
    return seal_hash(value, "locator_hash")


def render_packet(packet: dict[str, Any]) -> str:
    lines = [f"# {packet['candidate']['designation']} Human Shadow Review Packet", "", f"Reviewability: **{packet['reviewability_state']}**", "", "Comparison-only calibration; no admission, scheduling, report, deployment, or A100 authority.", ""]
    for item in packet["items"]:
        lines += [f"## {item['item_id']} — {item['kind']}", "", item["statement"], ""]
        for loc in item["locators"]: lines += [f"- `{loc['path']}` line {loc['line_start']}: `{loc['safe_excerpt']}`", f"- Revision: `{loc['immutable_revision']}`", ""]
    return "\n".join(lines)


def generate(output: Path) -> dict[str, Any]:
    summary = {"increment": 1, "state": "packets_ready_for_non_authoritative_human_review", "candidates": [], "scheduled": False, "product_fan_in_eligible": False, "deployment_authorized": False, "a100_production_authorized": False}
    for designation, cfg in CONFIG.items():
        manifest = build_manifest(designation); candidate = build_candidate(manifest); locators = [locator(item) for item in cfg["evidence"]]
        control = build_control_record(manifest, "enable_calibration", CREATED_AT, "thomasverburgt", "ADR-0039 Increment 1 authorization")
        packet = build_review_packet(manifest, candidate, locators, GENERATED_AT)
        target = output / cfg["slug"]
        for name, value in (("input-manifest.json", manifest), ("control-enable.json", control), ("candidate.artifact.json", candidate), ("evidence-locators.json", locators), ("human-shadow-review-packet.json", packet)):
            atomic_write(target / name, pretty_bytes(value))
        atomic_write(target / "human-shadow-review-packet.md", (render_packet(packet) + "\n").encode())
        summary["candidates"].append({"designation": designation, "manifest_id": manifest["manifest_id"], "artifact_id": candidate["artifact"]["artifact_id"], "packet_id": packet["packet_id"], "reviewability": packet["reviewability_state"], "item_count": len(packet["items"])})
    atomic_write(output / "summary.json", pretty_bytes(summary)); return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT); args = parser.parse_args()
    print(json.dumps(generate(args.output.resolve()), indent=2, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())

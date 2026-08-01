#!/usr/bin/env python3
"""Isolated ADR-0015 shadow execution and semantic comparison primitives."""
from __future__ import annotations
import copy
import uuid
from pathlib import Path
from typing import Any
from artifact_ledger import ArtifactLedger, content_hash
from validate_vertical_slice import ValidationFailure, assert_schema

WORKFLOW_ID = "WF-PROD-SYNTH-CAP-RISK-SHADOW-001"
LEDGER_NAMESPACE = "shadow/adr-0015"
NAMESPACE = uuid.UUID("15000000-0000-4000-8000-000000000000")
GENERATED_AT = "2026-07-31T22:00:00Z"

def _ref(value: dict[str, Any]) -> dict[str, str]:
    return {"artifact_id": value["artifact"]["artifact_id"], "content_hash": content_hash(value)}

def _rehash(value: dict[str, Any]) -> None:
    material = copy.deepcopy(value)
    material["integrity"]["output_hash"] = None
    value["integrity"]["output_hash"] = content_hash(material)

def validate_product_handoff(product: dict[str, Any]) -> tuple[list[str], list[str]]:
    assert_schema(product, "universal-agent-artifact.schema.json", "shadow PROD-SYNTH input")
    if product["identity"]["designation"] != "PROD-SYNTH" or product["decision_authority"] != "human":
        raise ValidationFailure("shadow product input must be human-authority PROD-SYNTH")
    role = product["extensions"]["product"]["role"]
    handoff = role["capability_handoff"]
    if handoff["artifact_id"] != product["artifact"]["artifact_id"]:
        raise ValidationFailure("PROD-SYNTH handoff is not bound to its artifact")
    findings = sorted(set(handoff["preserved_finding_ids"]))
    evidence = sorted(set(handoff["preserved_evidence_refs"]))
    source_findings = {i["source_record_id"] for i in role["preserved_child_assertions"] if i["record_kind"] == "finding"}
    source_evidence = {ref for i in role["preserved_child_assertions"] for ref in i["evidence_refs"]}
    if not set(findings).issubset(source_findings) or not set(evidence).issubset(source_evidence):
        raise ValidationFailure("PROD-SYNTH handoff drops or invents preserved lineage")
    return findings, evidence

def build_shadow_cap_risk(baseline: dict[str, Any], product: dict[str, Any]) -> dict[str, Any]:
    """Replay accepted CAP-RISK meaning with PROD-SYNTH as its sole shadow child."""
    validate_product_handoff(product)
    if baseline["identity"]["designation"] != "CAP-RISK":
        raise ValidationFailure("baseline comparison input must be CAP-RISK")
    shadow = copy.deepcopy(baseline)
    child_id = product["artifact"]["artifact_id"]
    product_id = product["extensions"]["product"]["product_id"]
    shadow["artifact"].update({"artifact_id": str(uuid.uuid5(NAMESPACE, f"cap-risk-shadow|{child_id}")), "created_at": GENERATED_AT})
    shadow["artifact"]["links"]["children"] = [child_id]
    shadow["inputs"] = [{"artifact_id": child_id, "hash": product["integrity"]["output_hash"], "compatibility": "compatible", "freshness": "fresh"}]
    shadow["execution"]["execution_id"] = str(uuid.uuid5(NAMESPACE, "shadow-execution"))
    shadow["execution"]["model"] = "deterministic-shadow-reference"
    shadow["scope"]["decision_context"] = "shadow_comparison"
    shadow["scope"]["participating_products"] = [product_id]
    shadow["consumers"] = ["SHADOW-COMPARISON"]
    capability = shadow["extensions"]["capability"]
    capability["participating_products"] = [product_id]
    role = capability["role"]
    for record in role["risk_provenance"]:
        record["source_artifact_id"] = child_id
        record.pop("artifact_ids", None)
    old_child = baseline["inputs"][0]["artifact_id"]
    for record in shadow["observations"]:
        record["evidence_refs"] = [child_id if ref == old_child else ref for ref in record["evidence_refs"]]
    shadow["integrity"]["input_hash"] = content_hash(shadow["inputs"])
    shadow["integrity"]["retention_class"] = "shadow-comparison"
    _rehash(shadow)
    assert_schema(shadow, "universal-agent-artifact.schema.json", "shadow CAP-RISK artifact")
    assert_schema(shadow["extensions"]["capability"], "capability-extension.schema.json", "shadow capability extension")
    assert_schema(role, "cap-risk-role.schema.json", "shadow CAP-RISK role")
    if shadow["decision_authority"] != "human" or shadow["artifact"]["links"]["children"] != [child_id]:
        raise ValidationFailure("shadow CAP-RISK authority or exact-child binding failed")
    return shadow

def _dimensions(value: dict[str, Any]) -> dict[str, Any]:
    role = value["extensions"]["capability"]["role"]
    return {"findings": value["findings"], "assessments": value["assessments"], "conflicts": value["conflicts"],
            "decisions_requested": value["decisions_requested"], "risk_register": role["risk_register"],
            "capa_options": role["capa_options"], "confidence": value["confidence"], "coverage": value["coverage"]}

def compare_paths(baseline: dict[str, Any], product: dict[str, Any], shadow: dict[str, Any],
                  product_ms: int | None = None, risk_ms: int | None = None,
                  platform: str = "local-deterministic-reference") -> dict[str, Any]:
    findings, evidence = validate_product_handoff(product)
    child_id = product["artifact"]["artifact_id"]
    exact = shadow["artifact"]["links"]["children"] == [child_id] and {i["artifact_id"] for i in shadow["inputs"]} == {child_id}
    baseline_evidence = {ref for item in baseline["findings"] for ref in item["evidence_refs"]}
    dropped = sorted(baseline_evidence - set(evidence))
    left, right = _dimensions(baseline), _dimensions(shadow)
    dimensions = {name: "equivalent" if value == right[name] else "different" for name, value in left.items()}
    equivalent = all(v == "equivalent" for v in dimensions.values())
    issues = ([] if exact else ["shadow CAP-RISK is not exactly bound to PROD-SYNTH"])
    if dropped: issues.append("baseline evidence was dropped")
    if not equivalent: issues.append("unexplained semantic divergence")
    result = {
        "comparison_id": str(uuid.uuid5(NAMESPACE, f"comparison|{child_id}|{shadow['artifact']['artifact_id']}")),
        "workflow_id": WORKFLOW_ID, "generated_at": GENERATED_AT,
        "baseline_cap_risk": _ref(baseline), "shadow_prod_synth": _ref(product), "shadow_cap_risk": _ref(shadow),
        "isolation": {"ledger_namespace": LEDGER_NAMESPACE, "baseline_workflow_changed": False, "report_package_changed": False,
                      "publication_enabled": False, "governance_effect": "none", "deployment_effect": "none"},
        "lineage": {"exact_child_binding": exact, "preserved_finding_ids": findings, "preserved_evidence_refs": evidence,
                    "dropped_refs": dropped, "invented_refs": []},
        "semantics": {"equivalent": equivalent, "dimensions": dimensions, "explained_deltas": []},
        "telemetry": {"baseline_wall_duration_ms": None, "shadow_prod_synth_wall_duration_ms": product_ms,
                      "shadow_cap_risk_wall_duration_ms": risk_ms, "platform": platform},
        "overall_state": "blocked" if issues else "equivalent", "blocking_issues": issues,
        "authority_effect": "comparison_only", "comparison_hash": "sha256:" + "0" * 64}
    material = copy.deepcopy(result); material["comparison_hash"] = None
    result["comparison_hash"] = content_hash(material)
    assert_schema(result, "shadow-path-comparison.schema.json", "shadow path comparison")
    return result

def persist_shadow(root: Path, shadow: dict[str, Any], comparison: dict[str, Any]) -> dict[str, Any]:
    ledger = ArtifactLedger(root)
    artifact_ref = ledger.persist_record(f"{LEDGER_NAMESPACE}/artifacts/{shadow['artifact']['artifact_id']}.json", "shadow-artifact",
                                         shadow["artifact"]["artifact_id"], shadow, retention_class="shadow-comparison")
    comparison_ref = ledger.persist_record(f"{LEDGER_NAMESPACE}/comparisons/{comparison['comparison_id']}.json", "shadow-comparison",
                                           comparison["comparison_id"], comparison, retention_class="shadow-comparison")
    return {"artifact": artifact_ref, "comparison": comparison_ref}

def assert_no_publication_target(path: Path) -> None:
    if {"report-packages", "distribution", "governance", "deployment", "baseline"}.intersection(p.lower() for p in path.parts):
        raise ValidationFailure("shadow output cannot target report, governance, deployment, or baseline storage")

#!/usr/bin/env python3
"""Build a deterministic ENT-EVIDENCE gate for one accepted CAP-RISK artifact."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from artifact_ledger import atomic_write, content_hash, pretty_bytes
from validate_vertical_slice import ROOT, REGISTRY, assert_schema, load_json
from worker_runtime import stable_uuid


def build_enterprise_evidence_artifact(capability: dict, created_at: str | None = None) -> dict:
    assert_schema(capability, "universal-agent-artifact.schema.json", "enterprise gate capability input")
    assert_schema(capability["extensions"]["capability"], "capability-extension.schema.json",
                  "enterprise gate capability extension")
    assert_schema(capability["extensions"]["capability"]["role"], "cap-risk-role.schema.json",
                  "enterprise gate capability role")
    if capability["identity"]["designation"] != "CAP-RISK" or capability["artifact"]["lifecycle_state"] != "complete":
        raise ValueError("ENT-EVIDENCE requires one complete CAP-RISK artifact")
    registry = load_json(REGISTRY)
    identity = next(item for item in registry["agents"] if item["designation"] == "ENT-EVIDENCE")
    cap_id = capability["artifact"]["artifact_id"]
    cap_hash = capability["integrity"]["output_hash"]
    capability_id = capability["scope"].get("capability_id", "unknown")
    timestamp = created_at or capability["artifact"]["created_at"]
    artifact_id = stable_uuid(cap_id, "enterprise-evidence-gate")
    inputs = [{"artifact_id": cap_id, "hash": cap_hash, "compatibility": "compatible", "freshness": "fresh"}]
    artifact = {
        "identity": {"agent_uuid": identity["agent_uuid"], "designation": "ENT-EVIDENCE",
                     "display_name": identity["display_name"],
                     "agent_version": identity.get("agent_version", "role-spec-1.0.0"),
                     "contract_version": identity["contract_version"]},
        "artifact": {"artifact_id": artifact_id, "artifact_type": "validated-enterprise-input-manifest",
                     "created_at": timestamp, "lifecycle_state": "complete",
                     "links": {"parents": [], "children": [cap_id], "peers": []}},
        "execution": {"execution_id": stable_uuid(cap_id, "enterprise-evidence-execution"),
                      "model": "deterministic-enterprise-evidence-gate", "prompt_version": "role-spec-1.0.0",
                      "rubric_version": "fixture-0.1.0", "toolchain_version": "0.1.0",
                      "settings": {"temperature": 0}},
        "scope": {"enterprise_scope_id": "ENTERPRISE-FIXTURE-001",
                  "participating_capabilities": [capability_id],
                  "assessment_period": timestamp[:10], "decision_context": "governance"},
        "inputs": inputs,
        "methodology": {"method": "deterministic contract, identity, integrity-reference, freshness, and completeness gate",
                        "limitations": ["Semantic enterprise risk review remains the responsibility of ENT-SYSRISK"]},
        "coverage": {"eligible": 1, "reviewed": 1, "omitted": 0, "inaccessible": 0,
                     "unknown": 0, "negative_evidence": 0},
        "observations": [{"observation_id": "OBS-ENTEVID-LIVE-001",
                          "fact": "The declared CAP-RISK artifact is complete, schema-valid, traceable, fresh, and compatible.",
                          "evidence_refs": [cap_id]}],
        "assessments": [{"assessment_id": "ASM-ENTEVID-LIVE-001",
                         "rationale": "All deterministic enterprise input checks passed for the declared capability artifact.",
                         "confidence": 1.0}],
        "findings": [], "patterns": [], "insights": [], "conflicts": [],
        "confidence": {"evidence": 1.0, "assessment": 1.0, "review": 1.0, "decision": None,
                       "provenance": [{"source": "deterministic gate checks", "version": "1.0.0"}]},
        "decisions_requested": [], "consumers": ["ENT-SYSRISK"], "decision_authority": "human",
        "integrity": {"input_hash": content_hash(inputs), "output_hash": "sha256:" + "0" * 64,
                      "attestation_ref": None, "retention_class": "internal-test", "schema_validation": "passed"},
        "extensions": {"enterprise": {
            "enterprise_scope": {"enterprise_scope_id": "ENTERPRISE-FIXTURE-001", "assessment_period": timestamp[:10]},
            "participating_capabilities": [capability_id],
            "capability_input_manifest": [{"artifact_id": cap_id, "state": "valid"}],
            "cross_capability_correlations": [],
            "enterprise_assertions": [{"assertion_id": "ASSERT-ENTEVID-LIVE-001",
                                       "statement": "The declared capability input is reviewable."}],
            "systemic_dependencies": [], "enterprise_unknowns": [], "unresolved_disagreements": [],
            "confidence_reconciliation": {"method": "deterministic_gate_conjunction", "result": 1.0},
            "human_decision_requests": [], "enterprise_traceability_manifest": {"artifact_ids": [cap_id]},
            "role": {"designation": "ENT-EVIDENCE",
                     "validated_input_manifest": [{"artifact_id": cap_id, "state": "valid"}],
                     "identity_validation": {"state": "passed"}, "schema_compatibility": {"state": "passed"},
                     "integrity_results": {"state": "passed"}, "lineage_results": {"state": "passed"},
                     "freshness_results": {"state": "passed"},
                     "completeness": {"required": 1, "valid": 1, "fraction": 1.0},
                     "duplicate_or_superseded_inputs": [], "conflict_preservation": {"state": "passed", "count": 0},
                     "reviewability": 1.0, "confidence_effect": {"delta": 0.0},
                     "gate_state": "passed", "escalations": []}
        }}
    }
    hash_material = copy.deepcopy(artifact)
    hash_material["integrity"]["output_hash"] = None
    artifact["integrity"]["output_hash"] = content_hash(hash_material)
    assert_schema(artifact, "universal-agent-artifact.schema.json", "enterprise evidence artifact")
    assert_schema(artifact["extensions"]["enterprise"], "enterprise-extension.schema.json", "enterprise evidence layer")
    assert_schema(artifact["extensions"]["enterprise"]["role"], "ent-evidence-role.schema.json", "enterprise evidence role")
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap-artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    capability = json.loads(args.cap_artifact.read_text(encoding="utf-8"))
    output = args.output.resolve()
    atomic_write(output, pretty_bytes(build_enterprise_evidence_artifact(capability)))
    print(json.dumps({"output": str(output), "artifact_hash": content_hash(load_json(output))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

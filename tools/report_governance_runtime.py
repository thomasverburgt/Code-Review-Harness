#!/usr/bin/env python3
"""Immutable report export and external-decision reconciliation reference boundary."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any

from artifact_ledger import ArtifactLedger, LedgerError, canonical_bytes, content_hash
from validate_vertical_slice import ROOT, assert_schema, load_json


AUTHORITY_REGISTRY = ROOT / "appendices" / "governance" / "decision-authorities-0.1.0.json"
GOVERNANCE_NAMESPACE = uuid.UUID("97000000-0000-4000-8000-000000000000")


class ReportGovernanceError(Exception):
    pass


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(GOVERNANCE_NAMESPACE, "|".join(parts)))


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def require_sha256(value: str, label: str) -> None:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
        raise ReportGovernanceError(f"{label} is not a canonical SHA-256 reference")


def build_report_package(artifacts: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    if not artifacts:
        raise ReportGovernanceError("report package requires source artifacts")
    seen: set[str] = set()
    sources = []
    source_contexts = []
    items = []
    evidence_items = []
    evidence_refs: set[str] = set()
    all_conflicts = []
    uncertainty_values: set[str] = set()
    final = artifacts[-1]
    for artifact in artifacts:
        assert_schema(artifact, "universal-agent-artifact.schema.json", "report source artifact")
        artifact_id = artifact["artifact"]["artifact_id"]
        if artifact_id in seen:
            raise ReportGovernanceError("report package contains a duplicate source artifact")
        seen.add(artifact_id)
        if artifact["artifact"]["lifecycle_state"] != "complete":
            raise ReportGovernanceError("distribution report cannot hide incomplete source input")
        sources.append({"artifact_id": artifact_id, "output_hash": artifact["integrity"]["output_hash"],
                        "designation": artifact["identity"]["designation"],
                        "artifact_type": artifact["artifact"]["artifact_type"]})
        source_contexts.append({"artifact_id": artifact_id,
                                "confidence": copy.deepcopy(artifact.get("confidence", {})),
                                "coverage": copy.deepcopy(artifact.get("coverage", {})),
                                "conflicts": copy.deepcopy(artifact.get("conflicts", [])),
                                "methodology": copy.deepcopy(artifact.get("methodology", {}))})
        all_conflicts.extend(copy.deepcopy(artifact.get("conflicts", [])))
        for finding in artifact.get("findings", []):
            finding_id = finding["finding_id"]
            items.append({"report_item_id": f"FINDING:{artifact['identity']['designation']}:{finding_id}", "kind": "finding",
                          "source_artifact_id": artifact_id, "source_record_id": finding_id,
                          "statement": finding["statement"], "evidence_refs": copy.deepcopy(finding.get("evidence_refs", [])),
                          "details": copy.deepcopy(finding), "advisory": True})
            evidence_refs.update(finding.get("evidence_refs", []))
        for observation in artifact.get("observations", []):
            evidence_refs.update(observation.get("evidence_refs", []))
            evidence_items.append({"evidence_item_id": f"EVIDENCE:{artifact['identity']['designation']}:{observation['observation_id']}",
                                   "source_artifact_id": artifact_id,
                                   "source_record_id": observation["observation_id"],
                                   "statement": observation["fact"],
                                   "evidence_refs": copy.deepcopy(observation.get("evidence_refs", []))})

    extension = final.get("extensions", {}).get("enterprise", {})
    role = extension.get("role", {})
    for risk in role.get("systemic_risk_register", []):
        risk_id = risk["enterprise_risk_id"]
        items.append({"report_item_id": f"RISK:{risk_id}", "kind": "risk",
                      "source_artifact_id": final["artifact"]["artifact_id"], "source_record_id": risk_id,
                      "statement": risk["risk_statement"], "evidence_refs": copy.deepcopy(risk.get("evidence_refs", [])),
                      "details": copy.deepcopy(risk), "advisory": True})
        evidence_refs.update(risk.get("evidence_refs", []))
        uncertainty_values.update(risk.get("unknowns", []))
    for index, capa in enumerate(role.get("enterprise_risk_capas", []), 1):
        capa_id = capa.get("capa_id") or stable_uuid(final["artifact"]["artifact_id"], "capa", str(index))
        items.append({"report_item_id": f"CAPA:{capa_id}", "kind": "capa",
                      "source_artifact_id": final["artifact"]["artifact_id"], "source_record_id": capa_id,
                      "statement": f"{capa['corrective_action']} {capa['preventive_action']}",
                      "evidence_refs": [], "details": copy.deepcopy(capa), "advisory": True})
    for index, option in enumerate(role.get("advisory_treatment_options", []), 1):
        record_id = option.get("option_id") or stable_uuid(final["artifact"]["artifact_id"], "recommendation", str(index))
        statement = (option.get("description") or option.get("target_condition") or
                     option.get("proposed_control") or "Advisory treatment option")
        items.append({"report_item_id": f"RECOMMENDATION:{record_id}", "kind": "recommendation",
                      "source_artifact_id": final["artifact"]["artifact_id"], "source_record_id": record_id,
                      "statement": statement, "evidence_refs": [], "details": copy.deepcopy(option), "advisory": True})
    if not items:
        raise ReportGovernanceError("report package contains no decision-support items")
    scope_id = final.get("scope", {}).get("enterprise_scope_id", "unknown")
    package_id = stable_uuid("WF-VERTICAL-RISK-001", *[item["artifact_id"] for item in sources])
    uncertainty_values.update(item.get("statement") for item in extension.get("enterprise_unknowns", [])
                              if isinstance(item, dict) and item.get("statement"))
    package = {
        "report_package_id": package_id, "report_version": "1.0.0",
        "workflow_id": "WF-VERTICAL-RISK-001", "enterprise_scope_id": scope_id,
        "generated_at": generated_at, "source_artifacts": sources, "source_contexts": source_contexts,
        "report_items": items, "evidence_items": evidence_items,
        "evidence_refs": sorted(evidence_refs), "confidence": copy.deepcopy(final.get("confidence", {})),
        "coverage": copy.deepcopy(final.get("coverage", {})), "conflicts": all_conflicts,
        "uncertainties": sorted(uncertainty_values), "technical_state": "technically_validated", "package_hash": "sha256:" + "0" * 64,
    }
    material = copy.deepcopy(package)
    material["package_hash"] = None
    package["package_hash"] = content_hash(material)
    assert_schema(package, "review-report-package.schema.json", "review report package")
    return package


class ReportGovernanceService:
    def __init__(self, ledger: ArtifactLedger, registry: dict[str, Any] | None = None) -> None:
        self.ledger = ledger
        self.registry = copy.deepcopy(registry or load_json(AUTHORITY_REGISTRY))
        assert_schema(self.registry, "decision-authority-registry.schema.json", "report governance authority registry")
        self.authorities = {item["authority_role"]: item for item in self.registry["authorities"]}
        if len(self.authorities) != len(self.registry["authorities"]):
            raise ReportGovernanceError("authority registry contains duplicate roles")

    def _authority(self, role: str, kind: str, action: str, scope_id: str,
                   subject_id: str | None = None, assurance: str | None = None,
                   decision_type: str | None = None) -> dict[str, Any]:
        entry = self.authorities.get(role)
        if entry is None or entry["authority_kind"] != kind:
            raise ReportGovernanceError(f"role {role} is not registered as {kind}")
        if action not in entry["allowed_actions"]:
            raise ReportGovernanceError(f"role {role} cannot perform {action}")
        if scope_id not in entry["scope_ids"] and "*" not in entry["scope_ids"]:
            raise ReportGovernanceError(f"role {role} is out of scope for {scope_id}")
        if subject_id is not None and subject_id not in entry["human_subject_ids"]:
            raise ReportGovernanceError(f"subject {subject_id} is not registered for {role}")
        if assurance is not None and assurance not in entry["assurance_levels"]:
            raise ReportGovernanceError(f"assurance level is insufficient for {role}")
        if decision_type is not None and decision_type not in entry["decision_types"]:
            raise ReportGovernanceError(f"role {role} cannot decide {decision_type}")
        return entry

    @staticmethod
    def _validate_actor(actor: dict[str, Any], expected_role: str) -> None:
        required = {"actor_type", "subject_id", "authority_role", "authentication_provider", "assurance_level", "session_id"}
        if set(actor) != required or actor.get("actor_type") != "human" or actor.get("authority_role") != expected_role:
            raise ReportGovernanceError("authenticated actor binding is invalid")

    @staticmethod
    def _validate_external_source(source: dict[str, Any]) -> None:
        required = {"source_type", "source_reference", "source_hash"}
        if set(source) != required or not source["source_reference"]:
            raise ReportGovernanceError("external decision source is incomplete")
        require_sha256(source["source_hash"], "external decision source hash")

    @staticmethod
    def _validate_external_authority(authority: dict[str, Any]) -> None:
        if set(authority) != {"authority_role", "authority_name"} or not authority.get("authority_name"):
            raise ReportGovernanceError("external authority binding is invalid")

    def persist_package(self, package: dict[str, Any]) -> dict[str, Any]:
        assert_schema(package, "review-report-package.schema.json", "review report package")
        return self.ledger.persist_record(f"report-packages/{package['report_package_id']}.json", "report-package",
                                          package["report_package_id"], package, retention_class="governance-report")

    def create_review_export(self, package: dict[str, Any], created_at: str) -> tuple[dict[str, Any], bytes]:
        content = canonical_bytes({"distribution_notice": "NOT APPROVED FOR DISTRIBUTION",
                                   "report_package": package})
        export_id = stable_uuid(package["report_package_id"], "leadership-review-export")
        record = {"export_id": export_id, "report_package_id": package["report_package_id"],
                  "report_package_hash": package["package_hash"],
                  "export_purpose": "leadership_distribution_review",
                  "distribution_state": "not_approved_for_distribution",
                  "file_name": f"{package['report_package_id']}-leadership-review.json",
                  "media_type": "application/json", "file_hash": sha256_bytes(content),
                  "created_at": created_at, "distribution_approval_record_id": None}
        assert_schema(record, "report-export-record.schema.json", "leadership review export")
        self.ledger.persist_record(f"report-exports/{export_id}.json", "report-export", export_id, record,
                                   retention_class="governance-report")
        return record, content

    def record_distribution_approval(self, package: dict[str, Any], review_export: dict[str, Any],
                                     approved_by: dict[str, Any], approval_source: dict[str, Any],
                                     recorded_by: dict[str, Any], intended_recipients: list[str],
                                     limitations: list[str], approved_at: str, recorded_at: str) -> dict[str, Any]:
        if review_export["report_package_hash"] != package["package_hash"] or review_export["distribution_state"] != "not_approved_for_distribution":
            raise ReportGovernanceError("distribution approval is not bound to the controlled review export")
        self._validate_external_source(approval_source)
        self._validate_external_authority(approved_by)
        scope = package["enterprise_scope_id"]
        self._authority(approved_by.get("authority_role", ""), "distribution_authority",
                        "approve_report_distribution", scope)
        self._validate_actor(recorded_by, "governance-records-administrator")
        self._authority(recorded_by["authority_role"], "records_administrator", "record_distribution_approval",
                        scope, recorded_by["subject_id"], recorded_by["assurance_level"])
        record_id = stable_uuid(package["report_package_id"], review_export["export_id"], approval_source["source_hash"])
        record = {"distribution_approval_record_id": record_id,
                  "report_package_id": package["report_package_id"], "report_package_hash": package["package_hash"],
                  "review_export_id": review_export["export_id"], "approved_by": copy.deepcopy(approved_by),
                  "approval_source": copy.deepcopy(approval_source), "recorded_by": copy.deepcopy(recorded_by),
                  "intended_recipients": copy.deepcopy(intended_recipients),
                  "distribution_limitations": copy.deepcopy(limitations), "approved_at": approved_at,
                  "recorded_at": recorded_at, "attestation_state": "recorded_pending_verification",
                  "effect": "record_only"}
        assert_schema(record, "distribution-approval-attestation.schema.json", "distribution approval attestation")
        self._persist_immutable("distribution-approval", record_id, record)
        return record

    def verify_record(self, target: dict[str, Any], target_type: str, verified_by: dict[str, Any],
                      source_passed: bool, authority_passed: bool, verified_at: str) -> dict[str, Any]:
        if target_type not in {"distribution_approval", "external_decision"}:
            raise ReportGovernanceError("unsupported governance verification target type")
        assert_schema(target, ("distribution-approval-attestation.schema.json" if target_type == "distribution_approval"
                               else "external-decision-attestation.schema.json"), "governance verification target")
        id_field = ("distribution_approval_record_id" if target_type == "distribution_approval"
                    else "external_decision_record_id")
        target_id = target[id_field]
        self._validate_actor(verified_by, "governance-records-verifier")
        scope = self._scope_for_record(target)
        action = "verify_distribution_approval" if target_type == "distribution_approval" else "verify_external_decision"
        self._authority(verified_by["authority_role"], "records_verifier", action, scope,
                        verified_by["subject_id"], verified_by["assurance_level"])
        if verified_by["subject_id"] == target["recorded_by"]["subject_id"]:
            raise ReportGovernanceError("records verifier must differ from the administrative recorder")
        target_hash = content_hash(target)
        verification_id = stable_uuid(target_id, target_hash, "verification")
        passed = source_passed and authority_passed
        verification = {"verification_record_id": verification_id, "target_record_id": target_id,
                        "target_record_hash": target_hash, "target_record_type": target_type,
                        "verified_by": copy.deepcopy(verified_by),
                        "source_binding_state": "passed" if source_passed else "failed",
                        "authority_binding_state": "passed" if authority_passed else "failed",
                        "verification_state": "verified" if passed else "rejected",
                        "verified_at": verified_at, "effect": "record_only"}
        assert_schema(verification, "governance-record-verification.schema.json", "governance verification")
        self._persist_immutable("governance-verification", verification_id, verification)
        self.ledger.put_index("verification-by-target", target_id,
                              {"target_record_id": target_id, "verification_record_id": verification_id,
                               "verification_hash": content_hash(verification)})
        return verification

    def create_approved_export(self, package: dict[str, Any], approval: dict[str, Any],
                               verification: dict[str, Any], created_at: str) -> tuple[dict[str, Any], bytes]:
        if (approval["report_package_id"] != package["report_package_id"] or
                approval["report_package_hash"] != package["package_hash"] or
                verification["target_record_id"] != approval["distribution_approval_record_id"] or
                verification["target_record_hash"] != content_hash(approval) or
                verification["verification_state"] != "verified"):
            raise ReportGovernanceError("approved export requires a verified distribution attestation")
        content = canonical_bytes({"distribution_notice": "APPROVED FOR DISTRIBUTION",
                                   "distribution_approval_record_id": approval["distribution_approval_record_id"],
                                   "report_package": package})
        export_id = stable_uuid(package["report_package_id"], approval["distribution_approval_record_id"], "approved-export")
        record = {"export_id": export_id, "report_package_id": package["report_package_id"],
                  "report_package_hash": package["package_hash"], "export_purpose": "approved_distribution",
                  "distribution_state": "approved_for_distribution",
                  "file_name": f"{package['report_package_id']}-approved-distribution.json",
                  "media_type": "application/json", "file_hash": sha256_bytes(content),
                  "created_at": created_at,
                  "distribution_approval_record_id": approval["distribution_approval_record_id"]}
        assert_schema(record, "report-export-record.schema.json", "approved distribution export")
        self._persist_immutable("report-export", export_id, record)
        return record, content

    def record_external_decision(self, package: dict[str, Any], approved_export: dict[str, Any],
                                 report_item_ids: list[str], decision_type: str,
                                 decided_by: dict[str, Any], decision_source: dict[str, Any],
                                 recorded_by: dict[str, Any], disposition: str, rationale: str,
                                 conditions: list[str], decided_at: str, recorded_at: str) -> dict[str, Any]:
        if approved_export["distribution_state"] != "approved_for_distribution" or approved_export["report_package_hash"] != package["package_hash"]:
            raise ReportGovernanceError("external decision is not bound to an approved report export")
        valid_items = {item["report_item_id"] for item in package["report_items"]}
        if not report_item_ids or any(item not in valid_items for item in report_item_ids):
            raise ReportGovernanceError("external decision references an item not present in the distributed report")
        self._validate_external_source(decision_source)
        self._validate_external_authority(decided_by)
        scope = package["enterprise_scope_id"]
        self._authority(decided_by.get("authority_role", ""), "expert_decision_authority",
                        "make_external_decision", scope, decision_type=decision_type)
        self._validate_actor(recorded_by, "governance-records-administrator")
        self._authority(recorded_by["authority_role"], "records_administrator", "record_external_decision",
                        scope, recorded_by["subject_id"], recorded_by["assurance_level"])
        record_id = stable_uuid(package["report_package_id"], decision_source["source_hash"],
                                decision_type, *sorted(report_item_ids))
        record = {"external_decision_record_id": record_id, "report_package_id": package["report_package_id"],
                  "report_package_hash": package["package_hash"], "report_item_ids": sorted(report_item_ids),
                  "decision_type": decision_type, "decided_by": copy.deepcopy(decided_by),
                  "decision_source": copy.deepcopy(decision_source), "recorded_by": copy.deepcopy(recorded_by),
                  "disposition": disposition, "rationale_summary": rationale,
                  "conditions": copy.deepcopy(conditions), "decided_at": decided_at, "recorded_at": recorded_at,
                  "attestation_state": "recorded_pending_verification", "effect": "record_only",
                  "original_report_mutated": False}
        assert_schema(record, "external-decision-attestation.schema.json", "external decision attestation")
        self._persist_immutable("external-decision", record_id, record)
        return record

    def reconciliation_view(self, package: dict[str, Any], decisions: list[dict[str, Any]],
                            verifications: list[dict[str, Any]]) -> list[dict[str, Any]]:
        verified = {item["target_record_id"]: item for item in verifications}
        by_item: dict[str, list[dict[str, Any]]] = {}
        for decision in decisions:
            check = verified.get(decision["external_decision_record_id"])
            state = (check["verification_state"] if check else "recorded_pending_verification")
            for item_id in decision["report_item_ids"]:
                by_item.setdefault(item_id, []).append({"external_decision_record_id": decision["external_decision_record_id"],
                                                        "disposition": decision["disposition"],
                                                        "administrative_state": state,
                                                        "decided_by": copy.deepcopy(decision["decided_by"]),
                                                        "recorded_by": copy.deepcopy(decision["recorded_by"])})
        return [{"report_item": copy.deepcopy(item), "external_decisions": by_item.get(item["report_item_id"], []),
                 "report_item_mutated": False} for item in package["report_items"]]

    def _scope_for_record(self, record: dict[str, Any]) -> str:
        ref = self.ledger.get_index("report-package", record["report_package_id"])
        package = self.ledger.get_object(ref["object_hash"])
        return package["enterprise_scope_id"]

    def _persist_immutable(self, family: str, record_id: str, value: dict[str, Any]) -> None:
        try:
            existing_ref = self.ledger.get_index(family, record_id)
        except LedgerError as exc:
            if "not found" not in str(exc):
                raise
        else:
            if self.ledger.get_object(existing_ref["object_hash"]) != value:
                raise ReportGovernanceError(f"immutable {family} mutation rejected")
            return
        self.ledger.persist_record(f"{family}/{record_id}.json", family, record_id, value,
                                   retention_class="governance-record")

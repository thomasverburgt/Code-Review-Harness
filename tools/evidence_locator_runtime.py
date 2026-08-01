#!/usr/bin/env python3
"""Reproducible evidence localization and expert-review packet boundary."""

from __future__ import annotations

import copy
import uuid
from pathlib import PurePosixPath
from typing import Any

from artifact_ledger import content_hash
from validate_vertical_slice import assert_schema


EVIDENCE_NAMESPACE = uuid.UUID("98000000-0000-4000-8000-000000000000")


class EvidenceLocatorError(Exception):
    pass


def stable_uuid(*parts: str) -> str:
    return str(uuid.uuid5(EVIDENCE_NAMESPACE, "|".join(parts)))


def _verified_hash(value: dict[str, Any], field: str, label: str) -> None:
    material = copy.deepcopy(value)
    material[field] = None
    if value[field] != content_hash(material):
        raise EvidenceLocatorError(f"{label} hash does not match canonical content")


def validate_locator(locator: dict[str, Any]) -> None:
    assert_schema(locator, "evidence-locator.schema.json", "evidence locator")
    path = PurePosixPath(locator["path"])
    if path.is_absolute() or ".." in path.parts or "\\" in locator["path"]:
        raise EvidenceLocatorError("evidence locator path must be a safe repository-relative POSIX path")
    start, end = locator["line_start"], locator["line_end"]
    if (start is None) != (end is None) or (start is not None and end < start):
        raise EvidenceLocatorError("evidence locator line range is incomplete or reversed")
    if start is None and not locator["symbol_or_section"]:
        raise EvidenceLocatorError("evidence locator requires a line range or named section")
    if locator["locator_state"] == "source_located" and start is None and not locator["symbol_or_section"]:
        raise EvidenceLocatorError("source_located evidence is not precisely localized")
    if locator["redaction"]["raw_value_included"]:
        raise EvidenceLocatorError("raw restricted values are prohibited in evidence locators")
    _verified_hash(locator, "locator_hash", "evidence locator")


def build_binding_manifest(package: dict[str, Any], bindings: list[dict[str, Any]]) -> dict[str, Any]:
    report_ids = {item["report_item_id"] for item in package["report_items"]}
    bound_ids = [item["report_item_id"] for item in bindings]
    if len(bound_ids) != len(set(bound_ids)) or set(bound_ids) != report_ids:
        raise EvidenceLocatorError("binding manifest must bind every report item exactly once")
    for binding in bindings:
        report_item = next(item for item in package["report_items"] if item["report_item_id"] == binding["report_item_id"])
        if report_item["evidence_refs"] and binding["binding_basis"] != "direct_report_reference":
            raise EvidenceLocatorError("direct report evidence must retain its direct binding basis")
        if report_item["evidence_refs"] and sorted(report_item["evidence_refs"]) != sorted(binding["evidence_refs"]):
            raise EvidenceLocatorError("binding manifest changed a direct report evidence reference")
    manifest = {
        "manifest_id": stable_uuid(package["report_package_id"], package["package_hash"], "evidence-bindings"),
        "report_package_id": package["report_package_id"],
        "report_package_hash": package["package_hash"],
        "bindings": sorted(copy.deepcopy(bindings), key=lambda item: item["report_item_id"]),
        "manifest_hash": "sha256:" + "0" * 64,
    }
    material = copy.deepcopy(manifest)
    material["manifest_hash"] = None
    manifest["manifest_hash"] = content_hash(material)
    assert_schema(manifest, "evidence-binding-manifest.schema.json", "evidence binding manifest")
    return manifest


def build_expert_review_packet(package: dict[str, Any], manifest: dict[str, Any],
                               locators: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    assert_schema(package, "review-report-package.schema.json", "review report package")
    assert_schema(manifest, "evidence-binding-manifest.schema.json", "evidence binding manifest")
    _verified_hash(manifest, "manifest_hash", "evidence binding manifest")
    if manifest["report_package_id"] != package["report_package_id"] or manifest["report_package_hash"] != package["package_hash"]:
        raise EvidenceLocatorError("binding manifest is not bound to the exact report package")
    by_evidence: dict[str, list[dict[str, Any]]] = {}
    locator_ids: set[str] = set()
    for locator in locators:
        validate_locator(locator)
        if locator["locator_id"] in locator_ids:
            raise EvidenceLocatorError("duplicate evidence locator ID")
        locator_ids.add(locator["locator_id"])
        by_evidence.setdefault(locator["evidence_id"], []).append(locator)
    bindings = {item["report_item_id"]: item for item in manifest["bindings"]}
    actionable, issues, used = [], [], {}
    missing = False
    unverified = False
    for report_item in package["report_items"]:
        binding = bindings[report_item["report_item_id"]]
        resolved = [locator for ref in binding["evidence_refs"] for locator in by_evidence.get(ref, [])]
        if not resolved:
            reviewability = "blocked_missing_locator"
            missing = True
            issues.append(f"{report_item['report_item_id']}: no locator resolves {binding['evidence_refs']}")
        elif any(locator["locator_state"] != "source_located" for locator in resolved):
            reviewability = "blocked_unverified_locator"
            unverified = True
            issues.append(f"{report_item['report_item_id']}: locator is not source_located")
        else:
            reviewability = "ready"
        for locator in resolved:
            used[locator["locator_id"]] = locator
        actionable.append({"report_item_id": report_item["report_item_id"], "kind": report_item["kind"],
                           "statement": report_item["statement"], "evidence_refs": copy.deepcopy(binding["evidence_refs"]),
                           "locator_ids": sorted({item["locator_id"] for item in resolved}), "reviewability": reviewability})
    state = "blocked_missing_locator" if missing else ("blocked_unverified_locator" if unverified else "ready_for_expert_review")
    summary_fields = ["locator_id", "evidence_id", "repository_uri", "immutable_revision", "path", "line_start", "line_end",
                      "symbol_or_section", "safe_excerpt", "line_fingerprint", "access", "reproduction_steps", "locator_state", "locator_hash"]
    packet = {"packet_id": stable_uuid(package["report_package_id"], manifest["manifest_hash"], "expert-review-packet"),
              "packet_version": "1.0.0", "report_package_id": package["report_package_id"],
              "report_package_hash": package["package_hash"], "binding_manifest_id": manifest["manifest_id"],
              "binding_manifest_hash": manifest["manifest_hash"], "generated_at": generated_at,
              "reviewability_state": state, "actionable_items": actionable,
              "locators": [{field: copy.deepcopy(item[field]) for field in summary_fields} for item in sorted(used.values(), key=lambda value: value["locator_id"])],
              "blocking_issues": sorted(issues), "authority_effect": "review_support_only", "packet_hash": "sha256:" + "0" * 64}
    material = copy.deepcopy(packet)
    material["packet_hash"] = None
    packet["packet_hash"] = content_hash(material)
    assert_schema(packet, "expert-review-packet.schema.json", "expert review packet")
    return packet


def render_evidence_annex(packet: dict[str, Any]) -> str:
    assert_schema(packet, "expert-review-packet.schema.json", "expert review packet")
    lines = ["# Expert Evidence Annex", "", f"Report package: `{packet['report_package_id']}`",
             f"Report hash: `{packet['report_package_hash']}`", f"Reviewability: **{packet['reviewability_state']}**", "",
             "This annex supports human review only. It does not approve distribution, decide a finding, accept risk, or authorize a change.", ""]
    locator_by_id = {item["locator_id"]: item for item in packet["locators"]}
    for item in packet["actionable_items"]:
        lines.extend([f"## {item['report_item_id']}", "", item["statement"], "", f"Reviewability: `{item['reviewability']}`", ""])
        for locator_id in item["locator_ids"]:
            loc = locator_by_id[locator_id]
            position = f"lines {loc['line_start']}-{loc['line_end']}" if loc["line_start"] is not None else f"section {loc['symbol_or_section']}"
            lines.extend([f"- Evidence: `{loc['evidence_id']}`", f"- Repository: `{loc['repository_uri']}`",
                          f"- Immutable revision: `{loc['immutable_revision']}`", f"- File: `{loc['path']}` ({position})",
                          f"- Safe excerpt: {loc['safe_excerpt']}", f"- Fingerprint: `{loc['line_fingerprint']}`",
                          "- Reviewer reproduction:"] + [f"  {index}. {step}" for index, step in enumerate(loc["reproduction_steps"], 1)] + [""])
    if packet["blocking_issues"]:
        lines.extend(["## Blocking issues", ""] + [f"- {issue}" for issue in packet["blocking_issues"]] + [""])
    return "\n".join(lines)


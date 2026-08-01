#!/usr/bin/env python3
"""Conformance tests for reproducible evidence localization."""

from __future__ import annotations

import copy
import unittest

from artifact_ledger import content_hash
from evidence_locator_runtime import (EvidenceLocatorError, build_binding_manifest,
                                      build_expert_review_packet, render_evidence_annex, validate_locator)
from validate_vertical_slice import ROOT, load_json


REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
CALIBRATION = ROOT / "fixtures/vertical-risk-slice/evidence/live-prompt-calibration-2026-07-31/uds-core-spec-secrets-calibration-slice.json"


def locator(state: str = "source_located", evidence_id: str = "UDS-0001") -> dict:
    source = load_json(CALIBRATION)
    evidence = source["redacted_detector_findings"][0]
    collection = source["collection"]
    value = {"locator_id": f"LOCATOR-{evidence_id}", "evidence_id": evidence_id, "source_type": "git_source",
             "repository_uri": collection["repository"], "immutable_revision": collection["revision"],
             "path": evidence["locator"]["path"], "line_start": evidence["locator"]["line"],
             "line_end": evidence["locator"]["line"], "symbol_or_section": None,
             "safe_excerpt": "Credential-like assignment detected; matched value omitted.",
             "redaction": {"applied": True, "method": evidence["redaction"], "raw_value_included": False},
             "line_fingerprint": evidence["line_fingerprint"], "collector": "SPEC-SECRETS calibration collector",
             "collection_method": collection["method"], "collected_at": "2026-07-31T13:00:00Z",
             "access": {"classification": source["access_classification"], "constraints": ["authorized reviewers only"],
                        "reviewer_instructions": ["Obtain an authorized read-only clone; do not copy restricted values into the review packet."]},
             "reproduction_steps": [f"Check out commit {collection['revision']} from {collection['repository']}.",
                                    f"Open {evidence['locator']['path']} at line {evidence['locator']['line']}.",
                                    "Run the approved redacted credential-assignment check and compare the line fingerprint."],
             "locator_state": state, "locator_hash": "sha256:" + "0" * 64}
    material = copy.deepcopy(value)
    material["locator_hash"] = None
    value["locator_hash"] = content_hash(material)
    return value


def bindings(package: dict) -> list[dict]:
    return [{"report_item_id": item["report_item_id"], "evidence_refs": item["evidence_refs"] or ["UDS-0001"],
             "binding_basis": "direct_report_reference" if item["evidence_refs"] else "explicit_derived_item_binding"}
            for item in package["report_items"]]


class EvidenceLocatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = load_json(REPORT)
        self.package_before = copy.deepcopy(self.package)
        self.manifest = build_binding_manifest(self.package, bindings(self.package))

    def test_ready_packet_is_deterministic_exact_and_report_immutable(self) -> None:
        locators = [locator(), locator(evidence_id="OBS-RISK-001")]
        packet = build_expert_review_packet(self.package, self.manifest, locators, "2026-07-31T19:00:00Z")
        self.assertEqual(packet, build_expert_review_packet(self.package, self.manifest, locators, "2026-07-31T19:00:00Z"))
        self.assertEqual(packet["reviewability_state"], "ready_for_expert_review")
        self.assertTrue(all(item["reviewability"] == "ready" for item in packet["actionable_items"]))
        self.assertEqual(self.package, self.package_before)
        self.assertEqual(self.package["package_hash"], "sha256:430233c423d65642bdebde1d9217517d7023bc2ddcc5dbbf89ebe361d9ceeb4a")
        annex = render_evidence_annex(packet)
        self.assertIn("docs/getting-started/local-demo/integrate-your-package.mdx", annex)
        self.assertIn("329ade01852f9e570d31cb7b19d9979152938c17", annex)

    def test_missing_and_unverified_locators_fail_closed(self) -> None:
        self.assertEqual(build_expert_review_packet(self.package, self.manifest, [], "2026-07-31T19:00:00Z")["reviewability_state"], "blocked_missing_locator")
        unverified = [locator("source_locator_unverified"), locator("source_locator_unverified", "OBS-RISK-001")]
        self.assertEqual(build_expert_review_packet(self.package, self.manifest, unverified, "2026-07-31T19:00:00Z")["reviewability_state"], "blocked_unverified_locator")

    def test_unsafe_or_mutated_locator_is_rejected(self) -> None:
        for change in ({"path": "../secret"}, {"immutable_revision": "main"}, {"line_end": 1}):
            candidate = locator()
            candidate.update(change)
            with self.assertRaises(Exception):
                validate_locator(candidate)
        candidate = locator()
        candidate["safe_excerpt"] = "changed after hashing"
        with self.assertRaises(EvidenceLocatorError):
            validate_locator(candidate)

    def test_binding_is_exact_and_complete(self) -> None:
        with self.assertRaises(EvidenceLocatorError):
            build_binding_manifest(self.package, bindings(self.package)[:-1])
        changed = bindings(self.package)
        changed[0]["evidence_refs"] = ["OTHER"]
        with self.assertRaises(EvidenceLocatorError):
            build_binding_manifest(self.package, changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)

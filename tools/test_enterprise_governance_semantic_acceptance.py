#!/usr/bin/env python3
"""ADR-0036 project-owner semantic-disposition tests."""

from __future__ import annotations

import copy
import unittest

from enterprise_arch_runtime import BASELINE
from enterprise_governance_semantic_acceptance_runtime import build_records, derive_eligibility, load_exact_review, validate_disposition
from validate_vertical_slice import ROOT, ValidationFailure, load_json


class EnterpriseGovernanceSemanticAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.disposition, self.finalization, self.eligibility = build_records()

    def test_exact_revised_candidate_is_owner_finalized(self) -> None:
        packet, candidate = load_exact_review()
        self.assertEqual(candidate["integrity"]["output_hash"], "sha256:ee04f21b04d026cecfc6040568812b32a39c833f8d2b4910ff91e6844aa6d370")
        self.assertEqual(packet["packet_hash"], "sha256:869f86a26c52085e3b8ad7df6e04519499cc984a61eed046ac92b635d1d3cc07")
        self.assertEqual(self.disposition["disposition"], "accept_semantically_faithful")
        self.assertEqual(self.disposition["decided_by"]["authority_name"], "thomasverburgt")

    def test_eligibility_is_synthesis_evaluation_only_and_unscheduled(self) -> None:
        self.assertEqual(self.eligibility["state"], "eligible_for_enterprise_synthesis_candidate_evaluation")
        self.assertFalse(self.eligibility["ent_gov_scheduled"])
        self.assertFalse(self.eligibility["ent_synth_scheduled"])

    def test_mutation_and_revocation_fail_closed(self) -> None:
        changed = copy.deepcopy(self.disposition)
        changed["candidate_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure):
            validate_disposition(changed)
        revoked = derive_eligibility(self.disposition, self.finalization, revoked=True)
        self.assertEqual(revoked["state"], "not_eligible")
        self.assertEqual(revoked["rollback_state"], "revoked")

    def test_authoritative_baseline_and_report_are_unchanged(self) -> None:
        report = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
        before = (BASELINE.read_bytes(), report.read_bytes())
        build_records()
        self.assertEqual(before, (BASELINE.read_bytes(), report.read_bytes()))
        self.assertNotIn("ENT-GOV", {node["designation"] for node in load_json(BASELINE)["nodes"]})


if __name__ == "__main__":
    unittest.main(verbosity=2)

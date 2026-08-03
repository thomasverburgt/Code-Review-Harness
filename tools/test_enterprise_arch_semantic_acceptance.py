#!/usr/bin/env python3
"""ADR-0035 project-owner semantic-disposition tests."""

from __future__ import annotations

import copy
import unittest

from enterprise_arch_runtime import BASELINE
from enterprise_arch_semantic_acceptance_runtime import build_records, derive_eligibility, load_exact_review, validate_disposition
from validate_vertical_slice import ROOT, ValidationFailure, load_json


class EnterpriseArchSemanticAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.disposition, self.finalization, self.eligibility = build_records()

    def test_exact_corrected_candidate_is_owner_finalized(self) -> None:
        packet, candidate = load_exact_review()
        self.assertEqual(candidate["integrity"]["output_hash"], "sha256:321186b8016dde5dee6f4948d5254397a011e6796b0c63ae5bebf49ab2d3faab")
        self.assertEqual(packet["packet_hash"], "sha256:170b55b2ff03a9e4ca034f52f3eedec3a2cb3c9d948146bb0eafb5c6db8126e5")
        self.assertEqual(self.disposition["disposition"], "accept_semantically_faithful")
        self.assertEqual(self.disposition["decided_by"]["authority_name"], "thomasverburgt")

    def test_eligibility_is_synthesis_evaluation_only_and_unscheduled(self) -> None:
        self.assertEqual(self.eligibility["state"], "eligible_for_enterprise_synthesis_candidate_evaluation")
        self.assertFalse(self.eligibility["ent_arch_scheduled"])
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
        self.assertNotIn("ENT-ARCH", {node["designation"] for node in load_json(BASELINE)["nodes"]})


if __name__ == "__main__":
    unittest.main(verbosity=2)

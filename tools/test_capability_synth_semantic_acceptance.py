#!/usr/bin/env python3
"""ADR-0034 project-owner semantic disposition tests."""

from __future__ import annotations

import copy
import unittest

from capability_synth_semantic_acceptance_runtime import build_records, derive_eligibility, validate_disposition, validate_finalization
from validate_vertical_slice import ValidationFailure


class CapabilitySynthSemanticAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.disposition, self.finalization, self.eligibility = build_records()

    def test_exact_owner_disposition_is_deterministic_and_limited(self) -> None:
        self.assertEqual((self.disposition, self.finalization, self.eligibility), build_records())
        self.assertEqual(self.disposition["semantic_judgment"]["statement"], "It is semantically faithful.")
        self.assertEqual(self.disposition["semantic_judgment"]["capability_posture"], "unassessable")
        self.assertFalse(self.disposition["scheduling_authorized"])
        self.assertEqual(self.eligibility["state"], "eligible_for_enterprise_candidate_evaluation")
        self.assertFalse(self.eligibility["cap_synth_scheduled"])
        self.assertFalse(self.eligibility["enterprise_scheduled"])

    def test_packet_candidate_and_hash_mutations_fail_closed(self) -> None:
        for field in ("packet_hash", "candidate_hash", "disposition_hash"):
            changed = copy.deepcopy(self.disposition)
            changed[field] = "sha256:" + "0" * 64
            with self.assertRaises(ValidationFailure):
                validate_disposition(changed)

    def test_finalization_mutation_fails_closed(self) -> None:
        changed = copy.deepcopy(self.finalization)
        changed["target_record_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure):
            validate_finalization(self.disposition, changed)

    def test_revocation_is_deterministic_and_never_schedules(self) -> None:
        revoked = derive_eligibility(self.disposition, self.finalization, revoked=True)
        self.assertEqual(revoked["state"], "not_eligible")
        self.assertEqual(revoked["rollback_state"], "revoked")
        self.assertFalse(revoked["cap_synth_scheduled"])
        self.assertFalse(revoked["enterprise_scheduled"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

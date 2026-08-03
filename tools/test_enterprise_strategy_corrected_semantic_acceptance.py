import copy, unittest
from enterprise_strategy_corrected_semantic_acceptance_runtime import build_records, derive_eligibility, validate_disposition
from validate_vertical_slice import ValidationFailure

class Tests(unittest.TestCase):
    def setUp(self): self.disposition, self.finalization, self.eligibility = build_records()
    def test_corrected_candidate_is_exactly_accepted(self):
        self.assertEqual(self.disposition["candidate_id"], "dd5598c9-628a-5f24-b974-9f2a53512119")
        self.assertEqual(self.disposition["disposition"], "accept_corrected_candidate_as_semantically_faithful")
    def test_remaining_context_is_carried_without_scheduling(self):
        self.assertIn("finding_locator_coverage_missing_from_admitted_cap_synth", self.eligibility["limitations_carried_forward"])
        self.assertIn("cap_synth_later_promotion_review_request_remains_human_owned", self.eligibility["source_context_carried_forward"])
        self.assertFalse(self.eligibility["ent_strat_scheduled"]); self.assertFalse(self.eligibility["ent_synth_scheduled"])
    def test_mutation_and_revocation_fail_closed(self):
        changed = copy.deepcopy(self.disposition); changed["candidate_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure): validate_disposition(changed)
        self.assertEqual(derive_eligibility(self.disposition, self.finalization, True)["state"], "not_eligible")

if __name__ == "__main__": unittest.main()

import copy, unittest
from accepted_live_enterprise_synthesis_runtime import BASELINE, REPORT, REPORT_MACHINE, build_package, load_sources, validate_candidate, validate_gate, validate_manifest
from validate_vertical_slice import ValidationFailure, load_json
class Tests(unittest.TestCase):
    def setUp(self): self.artifacts,self.eligibilities=load_sources();self.gate,self.manifest,self.candidate,self.packet=build_package()
    def test_exact_domain_set_and_active_eligibility(self):
        self.assertEqual([x["designation"] for x in self.gate["admitted_inputs"]],["ENT-SYSRISK","ENT-ARCH","ENT-GOV","ENT-STRAT"]);self.assertTrue(all(x["eligibility_id"] for x in self.gate["admitted_inputs"][1:]));self.assertIsNone(self.gate["admitted_inputs"][0]["eligibility_id"])
    def test_corrected_strat_context_preserved(self):
        strat=next(x for x in self.manifest["inputs"] if x["designation"]=="ENT-STRAT");self.assertIn("finding_locator_coverage_missing_from_admitted_cap_synth",strat["limitations_carried_forward"]);self.assertIn("cap_synth_later_promotion_review_request_remains_human_owned",strat["source_context_carried_forward"])
    def test_every_domain_summary_carries_declared_limitations(self):
        summaries={x["designation"]:x for x in self.candidate["extensions"]["enterprise"]["role"]["domain_summaries"]};self.assertTrue(all(summaries[x]["limitations"] for x in ("ENT-SYSRISK","ENT-ARCH","ENT-GOV","ENT-STRAT")));self.assertIn("No legal or compliance approval",summaries["ENT-GOV"]["limitations"]);self.assertIn("No cross-capability or target-state inference",summaries["ENT-ARCH"]["limitations"])
    def test_complete_without_double_counting(self):
        completeness=self.candidate["extensions"]["enterprise"]["role"]["completeness"];self.assertTrue(completeness["authoritative_live_complete"]);self.assertFalse(completeness["capability_or_child_double_counted"])
    def test_preserved_decision_ids_are_child_qualified_and_unique(self):
        decisions=self.candidate["extensions"]["enterprise"]["role"]["decision_requests"];ids=[x["decision_request_id"] for x in decisions];self.assertEqual(len(ids),len(set(ids)));self.assertTrue(all("UNQUALIFIED" not in x for x in ids));self.assertTrue(all(x["preserved_request"]["record_id"] in x["decision_request_id"] for x in decisions))
    def test_fail_closed_mutations(self):
        gate=copy.deepcopy(self.gate);gate["admitted_inputs"].pop()
        with self.assertRaises(ValidationFailure):validate_gate(gate,self.artifacts,self.eligibilities)
        manifest=copy.deepcopy(self.manifest);manifest["inputs"][3]["eligibility_hash"]="sha256:"+"0"*64
        with self.assertRaises(ValidationFailure):validate_manifest(manifest,self.gate,self.artifacts,self.eligibilities)
        candidate=copy.deepcopy(self.candidate);candidate["extensions"]["enterprise"]["role"]["report_boundary"]["publication_authorized"]=True
        with self.assertRaises(ValidationFailure):validate_candidate(candidate,self.gate,self.artifacts,self.eligibilities,self.manifest)
    def test_rollback_revocation_fails_closed(self):
        eligibility=copy.deepcopy(self.eligibilities["ENT-STRAT"]);eligibility["rollback_state"]="revoked";eligibility["state"]="not_eligible"
        with self.assertRaises(ValidationFailure):
            from accepted_live_enterprise_synthesis_runtime import build_gate
            build_gate(self.artifacts,{**self.eligibilities,"ENT-STRAT":eligibility})
    def test_report_baseline_and_scheduling_unchanged(self):
        before=[p.read_bytes() for p in (BASELINE,REPORT,REPORT_MACHINE)];build_package();self.assertEqual(before,[p.read_bytes() for p in (BASELINE,REPORT,REPORT_MACHINE)]);self.assertNotIn("ENT-SYNTH",{x["designation"] for x in load_json(BASELINE)["nodes"]})
if __name__=="__main__":unittest.main()

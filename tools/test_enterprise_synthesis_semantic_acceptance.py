import copy,unittest
from enterprise_synthesis_semantic_acceptance_runtime import build_records,derive_eligibility,validate_disposition
from validate_vertical_slice import ValidationFailure
class Tests(unittest.TestCase):
 def setUp(self):self.d,self.f,self.e=build_records()
 def test_exact_final_candidate_accepted(self):self.assertEqual(self.d["candidate_id"],"ca22ea90-b911-565a-931f-9a6f39ca265c");self.assertEqual(self.d["disposition"],"accept_semantically_faithful_for_bounded_integration_evaluation")
 def test_only_bounded_integration_eligibility(self):self.assertEqual(self.e["state"],"eligible_for_enterprise_shadow_integration_evaluation");self.assertFalse(self.e["ent_synth_scheduled"]);self.assertEqual(self.e["report_effect"],"none")
 def test_mutation_and_revocation_fail_closed(self):
  x=copy.deepcopy(self.d);x["candidate_hash"]="sha256:"+"0"*64
  with self.assertRaises(ValidationFailure):validate_disposition(x)
  self.assertEqual(derive_eligibility(self.d,self.f,True)["state"],"not_eligible")
if __name__=="__main__":unittest.main()

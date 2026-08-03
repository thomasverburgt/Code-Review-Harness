import copy,unittest
from enterprise_strategy_semantic_acceptance_runtime import build_records,derive_eligibility,validate_disposition
from validate_vertical_slice import ValidationFailure
class Tests(unittest.TestCase):
 def setUp(self):self.d,self.f,self.e=build_records()
 def test_exact_owner_accept_as_is(self):self.assertEqual(self.d["disposition"],"accept_as_is_with_acknowledged_limitations");self.assertEqual(len(self.d["acknowledged_limitations"]),4)
 def test_eligibility_carries_limitations_and_does_not_schedule(self):self.assertEqual(self.e["state"],"eligible_for_enterprise_synthesis_candidate_evaluation");self.assertEqual(self.e["limitations_carried_forward"],self.d["acknowledged_limitations"]);self.assertFalse(self.e["ent_strat_scheduled"]);self.assertFalse(self.e["ent_synth_scheduled"])
 def test_mutation_and_revocation_fail_closed(self):
  x=copy.deepcopy(self.d);x["candidate_hash"]="sha256:"+"0"*64
  with self.assertRaises(ValidationFailure):validate_disposition(x)
  self.assertEqual(derive_eligibility(self.d,self.f,True)["state"],"not_eligible")
if __name__=="__main__":unittest.main()

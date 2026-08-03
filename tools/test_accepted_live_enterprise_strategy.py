import copy,unittest
from accepted_live_enterprise_strategy_runtime import build_candidate,build_package,build_sources,validate_sources
from enterprise_arch_runtime import BASELINE
from validate_vertical_slice import ROOT,ValidationFailure,load_json
class Tests(unittest.TestCase):
 def setUp(self):self.p=build_package();self.c=self.p[-2]
 def test_exact_sources_and_owner(self):
  o,m=build_sources();validate_sources(o,m);self.assertEqual(o["declared_by"]["subject_id"],"HUMAN-PROJECT-OWNER-001");self.assertEqual(o["declared_by"]["authority_registry"]["registry_version"],"0.9.0");self.assertEqual(o["scope_id"],"CODE-HARNESS-PROJECT-001")
 def test_bounded_missingness(self):
  r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(r["fitness_claim"],"single_capability_project_strategy_evaluation");self.assertEqual(r["objective_scorecards"][0]["state"],"insufficient_evidence");self.assertIsNone(r["composite_score"]);self.assertEqual(r["objective_scorecards"][0]["components"][1]["state"],"missing")
 def test_exact_locators(self):self.assertEqual(self.c["extensions"]["enterprise"]["role"]["objective_scorecards"][0]["components"][0]["evidence_refs"],["STRAT-EVID-HUMAN-AUTHORITY","STRAT-EVID-ADVISORY-ONLY"])
 def test_mapping_confidence_and_distribution_are_declared(self):
  _,m=build_sources();r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(r["objective_scorecards"][0]["components"][0]["mapping_rule_id"],"MAP-HUMAN-AUTHORITY-001");self.assertEqual(r["strategic_confidence_posture"]["confidence_derivation"],m["confidence_derivation"]);self.assertEqual(r["confidence_distributions"][0]["basis"],"observed_components_only_not_objective_completeness")
 def test_raw_hash_and_projection_disclosed(self):
  c=build_candidate("a"*64);self.assertEqual(c["execution"]["generation_mode"],"model_response_with_harness_owned_strategy_projection");self.assertTrue(c["execution"]["harness_owned_fields"])
 def test_source_mutation_and_bad_raw_fail(self):
  o,m=build_sources();o=copy.deepcopy(o);o["objectives"][0]["outcome"]="invented"
  with self.assertRaises(ValidationFailure):validate_sources(o,m)
  with self.assertRaises(ValidationFailure):build_candidate("bad")
 def test_historical_registry_snapshot(self):
  import sys;sys.path.insert(0,"tools");from artifact_ledger import content_hash
  expected={"0.7.0":"sha256:eb503882b2886f2966c80cfa30914b1b616bfba6ca96baf417962f0f1e28cc72","0.8.0":"sha256:6bfd43e8c308d8075bee0bd92521288ca082a269679c2430d64b787bf8822631"}
  for version,digest in expected.items():self.assertEqual(content_hash(load_json(ROOT/f"appendices/governance/snapshots/decision-authorities-{version}.json")),digest)
 def test_protected_state(self):
  report=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json";b=(BASELINE.read_bytes(),report.read_bytes());build_package();self.assertEqual(b,(BASELINE.read_bytes(),report.read_bytes()));self.assertNotIn("ENT-STRAT",{n["designation"] for n in load_json(BASELINE)["nodes"]})
if __name__=="__main__":unittest.main()

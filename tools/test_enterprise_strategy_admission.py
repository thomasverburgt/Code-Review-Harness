#!/usr/bin/env python3
from __future__ import annotations
import copy,tempfile,unittest
from pathlib import Path
from artifact_ledger import ArtifactLedger,content_hash
from enterprise_strategy_runtime import BASELINE,build_candidate,load_manifests,persist_candidate,strategic_inputs,validate_candidate,validate_manifests
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
REPORT=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json";ADR20=ROOT/"fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json"
class EnterpriseStrategyAdmissionTests(unittest.TestCase):
 def setUp(self):self.objectives,self.method=load_manifests();self.gate,self.arts,self.obs=strategic_inputs();self.c=build_candidate()
 def test_registry_truth(self):
  states={x["designation"]:x["status"] for x in load_json(ROOT/"agents/agent-identities.json")["agents"] if x["layer"]=="enterprise"};self.assertEqual(states["ENT-STRAT"],"candidate");self.assertEqual(states["ENT-ARCH"],"candidate");self.assertEqual(states["ENT-GOV"],"candidate");self.assertEqual(states["ENT-EVIDENCE"],"baseline");self.assertEqual(states["ENT-SYSRISK"],"baseline")
 def test_manifest_hash_scope_authority_and_exact_measure_coverage(self):validate_manifests(self.objectives,self.method);self.assertEqual(set(self.method["weights"]),{m["measure_id"] for o in self.objectives["objectives"] for m in o["measures"]});self.assertAlmostEqual(sum(self.method["weights"].values()),1.0)
 def test_deterministic_exact_binding(self):self.assertEqual(self.c,build_candidate());b=self.c["extensions"]["enterprise"]["role"]["manifest_binding"];self.assertEqual(b["gate_artifact_hash"],content_hash(self.gate));self.assertEqual(b["posture_artifact_hashes"],[x["artifact_hash"] for x in self.obs]);self.assertEqual(b["objective_manifest_hash"],content_hash(self.objectives));self.assertEqual(b["scoring_method_hash"],content_hash(self.method))
 def test_no_composite_false_precision_or_imputation(self):
  r=self.c["extensions"]["enterprise"]["role"];self.assertIsNone(r["composite_score"]);self.assertIsNone(r["threshold_context"]);self.assertTrue(all(x["composite"] is None and x["false_precision_avoided"] for x in r["confidence_distributions"]));self.assertEqual(r["normalization_method"],self.method["normalization"]);self.assertEqual(r["weighting_model"],self.method["weights"])
 def test_schema_and_workflow(self):assert_schema(self.c["extensions"]["enterprise"]["role"],"ent-strat-role.schema.json","role");self.assertEqual(load_json(ROOT/"appendices/candidate-workflows/ent-strat-calibration.workflow.json")["nodes"][0]["designation"],"ENT-STRAT")
 def test_mutated_objective_weight_or_authority_fails_closed(self):
  cases=[];o=copy.deepcopy(self.objectives);o["objectives"][0]["outcome"]="invented";cases.append((o,self.method));m=copy.deepcopy(self.method);m["weights"]["MEASURE-ALIGNMENT"]=0.5;cases.append((self.objectives,m));o=copy.deepcopy(self.objectives);o["declared_by"]["authority_role"]="scoring-method-owner";cases.append((o,self.method))
  for o,m in cases:
   with self.assertRaises(ValidationFailure):validate_manifests(o,m)
 def test_tier_promotion_composite_or_missingness_mutation_fails_closed(self):
  cases=[]
  for mutate in (lambda r:r["input_evidence_tiers"][0].update(evidence_tier="accepted_live"),lambda r:r.update(composite_score=0.9),lambda r:r["objective_scorecards"][0]["components"][0].update(normalized_value=0.99)):
   c=copy.deepcopy(self.c);mutate(c["extensions"]["enterprise"]["role"]);cases.append(c)
  for c in cases:
   with self.assertRaises(ValidationFailure):validate_candidate(c,self.gate,self.arts,self.obs,self.objectives,self.method)
 def test_live_is_incomplete_protocol_only(self):
  g,a,o=strategic_inputs(live=True);c=build_candidate(live=True);r=c["extensions"]["enterprise"]["role"];self.assertEqual(r["fitness_claim"],"objective_method_protocol_lineage_smoke_only");self.assertIsNone(r["composite_score"]);self.assertEqual(len(r["missing_data_effects"]),1);validate_candidate(c,g,a,o,self.objectives,self.method,live=True)
 def test_authority_boundary_and_immutable_persistence(self):
  r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(r["decision_authority"],"human");self.assertFalse(r["downstream_handoff"]["scheduled"]);self.assertEqual(r["unsupported_claims"],[])
  with tempfile.TemporaryDirectory() as d:root=Path(d);ref=persist_candidate(root,self.c);self.assertEqual(ArtifactLedger(root).get_object(ref["object_hash"]),self.c);self.assertEqual(ref,persist_candidate(root,self.c))
 def test_protected_state_unchanged(self):
  paths=[BASELINE,REPORT,ADR20];before=[p.read_bytes() for p in paths];build_candidate();self.assertEqual(before,[p.read_bytes() for p in paths]);scheduled={x["designation"] for x in load_json(BASELINE)["nodes"]};self.assertFalse({"ENT-ARCH","ENT-GOV","ENT-STRAT"}&scheduled)
if __name__=="__main__":unittest.main(verbosity=2)

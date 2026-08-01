#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,unittest
from capability_req_runtime import BASELINE,REPORT,SOURCE,build_candidate,inputs,rehash,validate_candidate
from validate_vertical_slice import ROOT,ValidationFailure,load_json,validate_workflow_instance
PROMPT=ROOT/"appendices/prompt-templates/candidates/cap-req/design-0.1.0.prompt.txt"; PM=ROOT/"appendices/prompt-templates/candidates/manifest.json"; WF=ROOT/"appendices/candidate-workflows/cap-req-calibration.workflow.json"
class CapabilityReqAdmissionTests(unittest.TestCase):
 def setUp(self):self.c=build_candidate();self.role=self.c["extensions"]["capability"]["role"]
 def test_deterministic_complete_review_does_not_claim_satisfaction(self):
  self.assertEqual(self.c,build_candidate());self.assertEqual(self.c["artifact"]["lifecycle_state"],"complete");self.assertEqual(self.role["requirement_records"],[]);self.assertIsNone(self.role["coverage"]["fraction"]);self.assertEqual(self.role["acceptance_state"],"pending_human_requirements_acceptance")
 def test_prompt_registry_workflow_and_candidate_identity(self):
  self.assertEqual(hashlib.sha256(PROMPT.read_bytes()).hexdigest(),load_json(PM)["prompts"]["CAP-REQ"]["sha256"]);reg=load_json(ROOT/"agents/agent-identities.json");by={x["designation"]:x for x in reg["agents"]};validate_workflow_instance(load_json(WF),by,"CAP-REQ workflow");self.assertEqual(by["CAP-REQ"]["status"],"candidate")
 def test_locator_and_source_manifest_are_exact_immutable(self):
  s,l,_=inputs();self.assertFalse(s["mutation_performed"]);self.assertEqual(l["locator_hash"],s["evidence_locator"]["locator_hash"]);bad=copy.deepcopy(s);bad["evidence_locator"]["line_start"]=152
  from unittest.mock import patch
  with patch("capability_req_runtime.load_json",side_effect=lambda p: bad if p==SOURCE else load_json(p)):
   with self.assertRaises(ValidationFailure):inputs()
 def test_invented_requirement_fails_closed(self):
  x=copy.deepcopy(self.c);x["extensions"]["capability"]["role"]["requirement_records"]=[{"requirement_id":"INVENTED","source_locator":"LOCATOR-UDS-0001","text_hash":"sha256:"+"0"*64,"satisfaction_state":"satisfied","evidence_refs":[],"rationale":"invented","confidence":1.0}];rehash(x)
  with self.assertRaises(ValidationFailure):validate_candidate(x)
 def test_false_denominator_or_acceptance_fails_closed(self):
  x=copy.deepcopy(self.c);x["extensions"]["capability"]["role"]["coverage"]["fraction"]=1.0;rehash(x)
  with self.assertRaises(ValidationFailure):validate_candidate(x)
  y=copy.deepcopy(self.c);y["extensions"]["capability"]["role"]["acceptance_state"]="accepted";rehash(y)
  with self.assertRaises(ValidationFailure):validate_candidate(y)
 def test_missing_or_changed_gap_fails_closed(self):
  x=copy.deepcopy(self.c);x["extensions"]["capability"]["role"]["traceability_gaps"]=[];rehash(x)
  with self.assertRaises(ValidationFailure):validate_candidate(x)
 def test_model_projection_keeps_harness_owned_empty_population(self):
  model=copy.deepcopy(self.role);projected=build_candidate(model);self.assertEqual(projected["execution"]["model"],"qwen3-32b");self.assertEqual(projected["extensions"]["capability"]["role"]["declared_population"],self.role["declared_population"])
 def test_baseline_report_and_uds_source_remain_unchanged(self):
  before=(BASELINE.read_bytes(),REPORT.read_bytes(),SOURCE.read_bytes());build_candidate();self.assertEqual(before,(BASELINE.read_bytes(),REPORT.read_bytes(),SOURCE.read_bytes()));self.assertNotIn("CAP-SYNTH",{n["designation"] for n in load_json(BASELINE)["nodes"]})
if __name__=="__main__":unittest.main(verbosity=2)

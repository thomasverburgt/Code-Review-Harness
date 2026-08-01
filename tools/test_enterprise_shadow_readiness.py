#!/usr/bin/env python3
from __future__ import annotations
import copy,tempfile,unittest
from pathlib import Path
from artifact_ledger import ArtifactLedger
from enterprise_shadow_readiness_runtime import BASELINE,REPORT,SOURCES,build_manifest,persist_manifest,validate_manifest
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
class EnterpriseShadowReadinessTests(unittest.TestCase):
 def setUp(self):self.m=build_manifest()
 def test_manifest_is_deterministic_schema_valid_and_blocked(self):self.assertEqual(self.m,build_manifest());assert_schema(self.m,"enterprise-shadow-readiness-manifest.schema.json","readiness");self.assertEqual(self.m["overall_state"],"blocked");self.assertFalse(self.m["shadow_scheduled"])
 def test_every_required_prerequisite_is_explicit(self):self.assertEqual({x["prerequisite_id"] for x in self.m["prerequisites"]},{x[0] for x in SOURCES});self.assertEqual(len(self.m["prerequisites"]),6)
 def test_human_gates_remain_pending(self):
  p={x["prerequisite_id"]:x for x in self.m["prerequisites"]};self.assertEqual(p["ADR0016-SEMANTIC-ADJUDICATION"]["state"],"pending_external_decision");self.assertEqual(p["ADR0020-REQUIREMENTS-ACCEPTANCE"]["state"],"pending_external_decision")
 def test_protocol_evidence_never_satisfies_readiness(self):self.assertTrue(all(not x["satisfies_readiness"] for x in self.m["prerequisites"]));self.assertTrue(all(x["evidence_tier"]!="accepted_live_multi_domain" for x in self.m["prerequisites"]))
 def test_missing_duplicate_mutated_or_promoted_fails_closed(self):
  cases=[]
  for f in (lambda m:m["prerequisites"].pop(),lambda m:m["prerequisites"].append(copy.deepcopy(m["prerequisites"][0])),lambda m:m["prerequisites"][2].update(satisfies_readiness=True),lambda m:m.update(overall_state="ready_for_shadow_authorization_review")):
   m=copy.deepcopy(self.m);f(m);cases.append(m)
  for m in cases:
   with self.assertRaises(ValidationFailure):validate_manifest(m)
 def test_rollback_is_complete_and_baseline_route_preserved(self):self.assertTrue(all(self.m["rollback"].values()));self.assertEqual(self.m["baseline_route"],"ENT-EVIDENCE -> ENT-SYSRISK")
 def test_persistence_is_immutable(self):
  with tempfile.TemporaryDirectory() as d:root=Path(d);ref=persist_manifest(root,self.m);self.assertEqual(ArtifactLedger(root).get_object(ref["object_hash"]),self.m);self.assertEqual(ref,persist_manifest(root,self.m))
 def test_baseline_report_and_candidate_schedules_unchanged(self):
  before=[BASELINE.read_bytes(),REPORT.read_bytes()];build_manifest();self.assertEqual(before,[BASELINE.read_bytes(),REPORT.read_bytes()]);scheduled={x["designation"] for x in load_json(BASELINE)["nodes"]};self.assertFalse({"ENT-ARCH","ENT-GOV","ENT-STRAT","ENT-SYNTH"}&scheduled)
if __name__=="__main__":unittest.main(verbosity=2)

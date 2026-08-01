#!/usr/bin/env python3
from __future__ import annotations
import copy,tempfile,unittest
from pathlib import Path
from artifact_ledger import ArtifactLedger,content_hash
from enterprise_synthesis_runtime import BASELINE,REPORT,REPORT_MACHINE,build_candidate,persist_candidate,synthesis_inputs,validate_candidate,validate_manifest
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
class EnterpriseSynthesisAdmissionTests(unittest.TestCase):
 def setUp(self):self.g,self.arts,self.m=synthesis_inputs();self.c=build_candidate()
 def test_registry_truth(self):
  s={x["designation"]:x["status"] for x in load_json(ROOT/"agents/agent-identities.json")["agents"] if x["layer"]=="enterprise"};self.assertEqual(s["ENT-SYNTH"],"candidate");self.assertEqual(s["ENT-EVIDENCE"],"baseline");self.assertEqual(s["ENT-SYSRISK"],"baseline")
 def test_manifest_exact_hash_order_and_tiers(self):validate_manifest(self.m,self.g,self.arts);self.assertEqual([x["artifact_id"] for x in self.m["inputs"]],[x["artifact"]["artifact_id"] for x in self.arts]);self.assertTrue(all(x["permitted_use"]=="comparison_only" for x in self.m["inputs"]))
 def test_deterministic_exact_provenance(self):self.assertEqual(self.c,build_candidate());r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(len(r["contribution_map"]),4);self.assertTrue(all(x["preserved"] for x in r["source_assertion_snapshots"]))
 def test_schema_workflow_and_completeness(self):assert_schema(self.c["extensions"]["enterprise"]["role"],"ent-synth-role.schema.json","role");self.assertTrue(self.c["extensions"]["enterprise"]["role"]["completeness"]["complete_set"]);self.assertEqual(load_json(ROOT/"appendices/candidate-workflows/ent-synth-calibration.workflow.json")["nodes"][0]["designation"],"ENT-SYNTH")
 def test_mutated_missing_extra_duplicate_or_promoted_manifest_fails(self):
  cases=[]
  for f in (lambda m:m["inputs"].pop(),lambda m:m["inputs"].append(copy.deepcopy(m["inputs"][0])),lambda m:m["inputs"][0].update(evidence_tier="accepted_live",permitted_use="authoritative_domain_reference"),lambda m:m["inputs"][0].update(content_hash="sha256:"+"0"*64)):
   m=copy.deepcopy(self.m);f(m);cases.append(m)
  for m in cases:
   with self.assertRaises(ValidationFailure):validate_manifest(m,self.g,self.arts)
 def test_domain_rewrite_tier_promotion_and_report_authority_fail(self):
  cases=[]
  for f in (lambda r:r["source_assertion_snapshots"][0].update(preserved=False),lambda r:r["input_evidence_tiers"][0].update(evidence_tier="accepted_live"),lambda r:r["report_boundary"].update(publication_authorized=True)):
   c=copy.deepcopy(self.c);f(c["extensions"]["enterprise"]["role"]);cases.append(c)
  for c in cases:
   with self.assertRaises(ValidationFailure):validate_candidate(c,self.g,self.arts,self.m)
 def test_live_mixed_tier_protocol_only(self):
  g,a,m=synthesis_inputs(live=True);c=build_candidate(live=True);r=c["extensions"]["enterprise"]["role"];self.assertEqual(r["fitness_claim"],"mixed_tier_protocol_lineage_smoke_only");self.assertFalse(r["completeness"]["authoritative_live_complete"]);self.assertEqual([x["evidence_tier"] for x in r["input_evidence_tiers"]].count("accepted_live"),1);validate_candidate(c,g,a,m,live=True)
 def test_authority_and_handoff(self):r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(r["decision_authority"],"human");self.assertFalse(r["downstream_handoff"]["scheduled"]);self.assertEqual(r["unsupported_claims"],[])
 def test_persistence(self):
  with tempfile.TemporaryDirectory() as d:root=Path(d);ref=persist_candidate(root,self.c);self.assertEqual(ArtifactLedger(root).get_object(ref["object_hash"]),self.c);self.assertEqual(ref,persist_candidate(root,self.c))
 def test_report_distribution_baseline_and_candidates_unchanged(self):
  paths=[REPORT,REPORT_MACHINE,BASELINE];before=[p.read_bytes() for p in paths];build_candidate();self.assertEqual(before,[p.read_bytes() for p in paths]);self.assertNotIn("ENT-SYNTH",{x["designation"] for x in load_json(BASELINE)["nodes"]})
if __name__=="__main__":unittest.main(verbosity=2)

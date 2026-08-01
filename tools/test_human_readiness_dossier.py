#!/usr/bin/env python3
from __future__ import annotations
import copy,tempfile,unittest
from pathlib import Path
from artifact_ledger import ArtifactLedger
from enterprise_shadow_readiness_runtime import BASELINE,REPORT
from human_readiness_dossier_runtime import DOMAIN,build_dossier,persist_dossier,render_dossier,validate_dossier
from validate_vertical_slice import ValidationFailure,assert_schema,load_json
class HumanReadinessDossierTests(unittest.TestCase):
 def setUp(self):self.d,self.p=build_dossier()
 def test_deterministic_schema_and_exact_summary(self):self.assertEqual((self.d,self.p),build_dossier());assert_schema(self.d,"human-readiness-action-dossier.schema.json","dossier");self.assertEqual(self.d["summary"],{"total":6,"awaiting_external_response":2,"not_ready_for_review":4,"satisfied":0})
 def test_existing_packets_await_separate_external_responses(self):
  entries={x["prerequisite_id"]:x for x in self.d["entries"]};self.assertEqual(entries["ADR0016-SEMANTIC-ADJUDICATION"]["action_state"],"awaiting_external_response");self.assertEqual(entries["ADR0020-REQUIREMENTS-ACCEPTANCE"]["action_state"],"awaiting_external_response");self.assertNotEqual(entries["ADR0016-SEMANTIC-ADJUDICATION"]["required_authority"],entries["ADR0020-REQUIREMENTS-ACCEPTANCE"]["required_authority"])
 def test_domain_packets_are_not_ready_and_cannot_accept_response(self):self.assertEqual(set(self.p),set(DOMAIN));self.assertTrue(all(x["review_state"]=="not_ready_for_review" and not x["accepted_response_allowed"] for x in self.p.values()))
 def test_no_dossier_or_batch_authority(self):self.assertFalse(self.d["dossier_approval_allowed"]);self.assertEqual(self.d["decision_authority"],"separate_named_human_authority_per_entry");self.assertTrue(all(x["response_must_be_atomic"] and x["independent_verification_required"] for x in self.d["entries"]))
 def test_missing_duplicate_mutated_or_inferred_satisfaction_fails(self):
  cases=[]
  for f in (lambda d:d["entries"].pop(),lambda d:d["entries"].append(copy.deepcopy(d["entries"][0])),lambda d:d["entries"][0].update(satisfies_readiness=True),lambda d:d.update(readiness_manifest_hash="sha256:"+"0"*64)):
   d=copy.deepcopy(self.d);f(d);cases.append(d)
  for d in cases:
   with self.assertRaises(ValidationFailure):validate_dossier(d,self.p)
 def test_premature_domain_response_fails(self):
  packets=copy.deepcopy(self.p);next(iter(packets.values()))["accepted_response_allowed"]=True
  with self.assertRaises(ValidationFailure):validate_dossier(self.d,packets)
 def test_human_render_names_block_and_atomic_authority(self):text=render_dossier(self.d);self.assertIn("SHADOW INTEGRATION BLOCKED",text);self.assertIn("No batch signature",text);self.assertIn("not_ready_for_review",text)
 def test_persistence_and_protected_state(self):
  before=[BASELINE.read_bytes(),REPORT.read_bytes()]
  with tempfile.TemporaryDirectory() as d:root=Path(d);ref=persist_dossier(root,self.d);self.assertEqual(ArtifactLedger(root).get_object(ref["object_hash"]),self.d);self.assertEqual(ref,persist_dossier(root,self.d))
  self.assertEqual(before,[BASELINE.read_bytes(),REPORT.read_bytes()]);self.assertFalse(self.d["shadow_scheduled"])
if __name__=="__main__":unittest.main(verbosity=2)

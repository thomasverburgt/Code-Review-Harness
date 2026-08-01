#!/usr/bin/env python3
from __future__ import annotations
import copy,tempfile,unittest
from artifact_ledger import ArtifactLedger,content_hash
from enterprise_arch_runtime import BASELINE,build_candidate,build_inputs,persist_candidate,role_template,validate_candidate
from validate_vertical_slice import ROOT,ValidationFailure,assert_schema,load_json
REPORT=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
ADR20=ROOT/"fixtures/cap-req-admission/evidence/2026-08-01/adr0020/reference-run/requirements-acceptance-packet.json"
class EnterpriseArchAdmissionTests(unittest.TestCase):
 def setUp(self):self.gate,self.arts=build_inputs();self.c=build_candidate()
 def test_registry_truth_and_candidate_identity(self):
  reg=load_json(ROOT/"agents/agent-identities.json");states={x["designation"]:x["status"] for x in reg["agents"] if x["layer"]=="enterprise"};self.assertEqual(states["ENT-EVIDENCE"],"baseline");self.assertEqual(states["ENT-SYSRISK"],"baseline");self.assertEqual(states["ENT-ARCH"],"candidate");self.assertIn(states["ENT-GOV"],{"planned","candidate"});self.assertIn(states["ENT-STRAT"],{"planned","candidate"});self.assertIn(states["ENT-SYNTH"],{"planned","candidate"});self.assertTrue(all(states[x]=="planned" for x in states if x not in {"ENT-EVIDENCE","ENT-SYSRISK","ENT-ARCH","ENT-GOV","ENT-STRAT","ENT-SYNTH"}))
 def test_deterministic_fixture_candidate_exact_binding(self):
  self.assertEqual(self.c,build_candidate());b=self.c["extensions"]["enterprise"]["role"]["manifest_binding"];self.assertEqual(b["capability_artifact_ids"],[a["artifact"]["artifact_id"] for a in self.arts]);self.assertEqual(b["capability_artifact_hashes"],[content_hash(a) for a in self.arts]);self.assertEqual(b["gate_artifact_hash"],content_hash(self.gate))
 def test_layer_role_and_workflow_schemas(self):
  assert_schema(self.c["extensions"]["enterprise"],"enterprise-extension.schema.json","enterprise extension");assert_schema(self.c["extensions"]["enterprise"]["role"],"ent-arch-role.schema.json","ENT-ARCH role");wf=load_json(ROOT/"appendices/candidate-workflows/ent-arch-calibration.workflow.json");self.assertEqual(wf["nodes"][0]["designation"],"ENT-ARCH")
 def test_missing_extra_mutated_or_invented_inputs_fail_closed(self):
  missing=copy.deepcopy(self.c);missing["extensions"]["enterprise"]["role"]["manifest_binding"]["capability_artifact_ids"].pop()
  extra=copy.deepcopy(self.c);extra["extensions"]["enterprise"]["role"]["manifest_binding"]["capability_artifact_ids"].append("11111111-1111-4111-8111-111111111111")
  invented=copy.deepcopy(self.c);invented["extensions"]["enterprise"]["role"]["architecture_findings"][0]["source_artifact_ids"]=["11111111-1111-4111-8111-111111111111"]
  mutated=copy.deepcopy(self.arts);mutated[0]["findings"][0]["statement"]="mutated"
  for c,g,a in [(missing,self.gate,self.arts),(extra,self.gate,self.arts),(invented,self.gate,self.arts),(self.c,self.gate,mutated)]:
   with self.assertRaises(ValidationFailure):validate_candidate(c,g,a)
 def test_live_single_capability_is_protocol_only(self):
  g,a=build_inputs(live=True);c=build_candidate(live=True);r=c["extensions"]["enterprise"]["role"];self.assertEqual(r["fitness_claim"],"protocol_lineage_smoke_only");self.assertEqual(r["dependency_topology"],[]);validate_candidate(c,g,a,live=True)
  over=copy.deepcopy(c);over["extensions"]["enterprise"]["role"]["fitness_claim"]="contract_mechanics_only"
  with self.assertRaises(ValidationFailure):validate_candidate(over,g,a,live=True)
 def test_authority_and_downstream_are_comparison_only(self):
  r=self.c["extensions"]["enterprise"]["role"];self.assertEqual(r["decision_authority"],"human");self.assertEqual(r["downstream_handoff"]["handoff_state"],"comparison_only");self.assertFalse(r["downstream_handoff"]["scheduled"]);self.assertEqual(r["unsupported_claims"],[])
 def test_persistence_is_immutable(self):
  with tempfile.TemporaryDirectory() as d:
   ref=persist_candidate(__import__('pathlib').Path(d),self.c);ledger=ArtifactLedger(__import__('pathlib').Path(d));self.assertEqual(ledger.get_object(ref["object_hash"]),self.c);self.assertEqual(ref,persist_candidate(__import__('pathlib').Path(d),self.c))
 def test_baseline_report_and_cap_req_gate_unchanged(self):
  paths=[BASELINE,REPORT,ADR20];before=[p.read_bytes() for p in paths];build_candidate();self.assertEqual(before,[p.read_bytes() for p in paths]);self.assertFalse(any(n["designation"]=="ENT-ARCH" for n in load_json(BASELINE)["nodes"]))
if __name__=="__main__":unittest.main(verbosity=2)

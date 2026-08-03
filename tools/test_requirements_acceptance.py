#!/usr/bin/env python3
"""ADR-0020/0033 packet, project-owner finalization, eligibility, and rollback tests."""
from __future__ import annotations
import copy, uuid, unittest
from artifact_ledger import content_hash
from requirements_acceptance_runtime import (AUTHORITY_REGISTRY, DISPOSITIONS, LIVE_ARCHIVE, STATE_MACHINE,
 build_owner_finalization, build_packet, build_verification, derive_eligibility, load_live_artifact,
 render_review, validate_owner_finalization, validate_response, validate_verification)
from validate_vertical_slice import ROOT, ValidationFailure, assert_schema, load_json

BASELINE=ROOT/"appendices/example-workflows/vertical-risk-slice.workflow.json"
REPORT=ROOT/"fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"
SOURCE=ROOT/"fixtures/cap-req-admission/input/requirements-source-manifest.json"
NS=uuid.UUID("20000000-0000-4000-8000-000000000000")

def response_for(packet:dict, disposition:str="accept_review_as_complete", authority_name:str="Requirements Review Board")->dict:
 r={"response_id":str(uuid.uuid5(NS,"fixture-response:"+disposition)),"packet_id":packet["packet_id"],"packet_hash":packet["packet_hash"],"artifact_id":packet["cap_req_artifact"]["artifact_id"],"artifact_hash":packet["cap_req_artifact"]["content_hash"],"decided_at":"2026-08-01T23:15:00Z","decided_by":{"authority_role":"requirements-acceptance-authority","authority_name":authority_name},"disposition":disposition,"rationale":"Fixture human requirements-authority rationale.","authoritative_source_hash":"sha256:"+"1"*64,"decision_authority":"human","effect":"record_only","response_hash":"sha256:"+"0"*64}
 r["response_hash"]=content_hash({**r,"response_hash":None});return r

class RequirementsAcceptanceTests(unittest.TestCase):
 def setUp(self)->None:self.packet=build_packet()
 def test_packet_is_deterministic_and_binds_live_artifact(self)->None:
  self.assertEqual(self.packet,build_packet());live=load_live_artifact();self.assertEqual(self.packet["cap_req_artifact"]["content_hash"],content_hash(live));self.assertEqual(self.packet["cap_req_artifact"]["output_hash"],live["integrity"]["output_hash"]);self.assertEqual(self.packet["execution_pins"]["model"],"qwen3-32b")
 def test_zero_population_is_unassessable_and_review_is_blocked(self)->None:
  facts=self.packet["review_facts"];self.assertEqual(facts["requirement_records"],0);self.assertIsNone(facts["satisfaction_rate"]);self.assertFalse(facts["satisfaction_claim_present"]);review=render_review(self.packet);self.assertIn("unassessable",review);self.assertIn("CAP-SYNTH remains unscheduled",review);self.assertNotIn("requirements are satisfied",review.lower())
 def test_valid_external_response_is_exact_and_record_only(self)->None:
  r=response_for(self.packet);validate_response(self.packet,r);self.assertEqual(r["effect"],"record_only");self.assertEqual(r["decided_by"]["authority_role"],"requirements-acceptance-authority")
 def test_missing_mutated_unauthorized_or_stale_response_fails(self)->None:
  cases=[]
  missing=response_for(self.packet);missing.pop("rationale");cases.append(missing)
  mutated=response_for(self.packet);mutated["packet_hash"]="sha256:"+"0"*64;cases.append(mutated)
  unauthorized=response_for(self.packet);unauthorized["decided_by"]["authority_role"]="project-maintainer";cases.append(unauthorized)
  stale=response_for(self.packet);stale["artifact_hash"]="sha256:"+"2"*64;stale["response_hash"]=content_hash({**stale,"response_hash":None});cases.append(stale)
  bad_hash=response_for(self.packet);bad_hash["rationale"]="mutated after signing";cases.append(bad_hash)
  for value in cases:
   with self.subTest(value=value):
    with self.assertRaises(ValidationFailure):validate_response(self.packet,value)
 def test_project_owner_finalization_is_exact_and_needs_no_second_person(self)->None:
  r=response_for(self.packet,authority_name="thomasverburgt");f=build_owner_finalization(self.packet,r);validate_owner_finalization(self.packet,r,f);self.assertEqual(f["finalization_state"],"finalized");self.assertEqual(f["finalized_by"]["authority_name"],r["decided_by"]["authority_name"])
  bad=copy.deepcopy(f);bad["target_record_hash"]="sha256:"+"3"*64
  with self.assertRaises(ValidationFailure):validate_owner_finalization(self.packet,r,bad)
 def test_legacy_independent_verification_remains_replayable_but_is_not_required(self)->None:
  r=response_for(self.packet);v=build_verification(self.packet,r);validate_verification(self.packet,r,v);self.assertEqual(v["status"],"verified")
 def test_only_owner_finalized_acceptance_yields_eligibility(self)->None:
  for disposition in DISPOSITIONS:
   r=response_for(self.packet,disposition);f=build_owner_finalization(self.packet,r);e=derive_eligibility(self.packet,r,f)
   expected="eligible_for_accepted_capability_input" if disposition=="accept_review_as_complete" else "not_eligible"
   self.assertEqual(e["state"],expected);self.assertFalse(e["cap_synth_scheduled"]);self.assertEqual(e["effect"],"eligibility_record_only")
 def test_rollback_revokes_without_mutating_history(self)->None:
  r=response_for(self.packet);f=build_owner_finalization(self.packet,r);before=(copy.deepcopy(self.packet),copy.deepcopy(r),copy.deepcopy(f));active=derive_eligibility(self.packet,r,f);revoked=derive_eligibility(self.packet,r,f,revoked=True);self.assertEqual(active["state"],"eligible_for_accepted_capability_input");self.assertEqual(revoked["state"],"not_eligible");self.assertEqual(revoked["rollback_state"],"revoked");self.assertEqual(before,(self.packet,r,f))
 def test_generation_does_not_mutate_operational_inputs(self)->None:
  paths=[BASELINE,REPORT,SOURCE,LIVE_ARCHIVE];before=[p.read_bytes() for p in paths];build_packet();self.assertEqual(before,[p.read_bytes() for p in paths]);self.assertFalse(self.packet["isolation"]["cap_synth_scheduled"])
 def test_authority_registry_and_state_machine_are_closed(self)->None:
  registry=load_json(AUTHORITY_REGISTRY);assert_schema(registry,"decision-authority-registry.schema.json","authority registry");role=next(x for x in registry["authorities"] if x["authority_role"]=="requirements-acceptance-authority");self.assertEqual(role["authority_kind"],"expert_decision_authority");owner=next(x for x in registry["authorities"] if x["authority_role"]=="project-owner");self.assertIn("HUMAN-PROJECT-OWNER-001",owner["human_subject_ids"])
  machine=load_json(STATE_MACHINE);assert_schema(machine,"requirements-acceptance-state-machine.schema.json","requirements acceptance state machine");states=set(machine["states"]);self.assertIn(machine["initial_state"],states);self.assertTrue(set(machine["terminal_states"]).issubset(states));self.assertTrue(all(t["from"] in states and t["to"] in states for t in machine["transitions"]));self.assertEqual(machine["effects"]["scheduling"],"none")

if __name__=="__main__":unittest.main(verbosity=2)

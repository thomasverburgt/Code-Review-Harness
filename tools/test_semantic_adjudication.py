#!/usr/bin/env python3
"""ADR-0016 packet completeness, authority, immutability, and response tests."""
from __future__ import annotations
import copy, uuid, unittest
from artifact_ledger import content_hash
from semantic_adjudication_runtime import (BASELINE, DISPOSITIONS, build_packet, load_archive_json,
                                            resolve_pointer, render_review, validate_response,
                                            LIVE_ARTIFACT_MEMBER)
from validate_vertical_slice import ROOT, ValidationFailure, load_json

REPORT = ROOT / "fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/reference-run/report-package.json"

def response_for(packet: dict, disposition: str = "accept_preserved_meaning") -> dict:
    decisions = [{"delta_id": item["delta_id"], "disposition": disposition, "rationale": "Fixture human rationale."} for item in packet["deltas"]]
    recommendation = {"accept_preserved_meaning": "eligible_for_cutover_review", "accept_beneficial_enrichment": "eligible_for_cutover_review",
                      "require_normalization": "normalization_required", "reject_semantic_drift": "reject_cutover",
                      "insufficient_evidence": "insufficient_evidence"}[disposition]
    return {"adjudication_id": str(uuid.uuid5(uuid.UUID("16000000-0000-4000-8000-000000000000"), "fixture-response")),
        "packet_id": packet["packet_id"], "packet_hash": packet["packet_hash"], "decided_at": "2026-08-01T16:00:00Z",
        "decided_by": {"authority_role": "enterprise-risk-acceptance-authority", "authority_name": "Enterprise Risk Board"},
        "delta_decisions": decisions, "overall_recommendation": recommendation,
        "authoritative_source_hash": "sha256:" + "1" * 64, "decision_authority": "human", "effect": "record_only"}

class SemanticAdjudicationTests(unittest.TestCase):
    def setUp(self) -> None: self.packet = build_packet()

    def test_packet_is_deterministic_exact_and_cutover_blocked(self) -> None:
        self.assertEqual(self.packet, build_packet())
        self.assertEqual(self.packet["differing_dimensions"], ["assessments", "conflicts", "risk_register"])
        self.assertEqual(self.packet["cutover_state"], "blocked_pending_human_adjudication")
        self.assertEqual(self.packet["effect"], "review_request_only")
        shadow = load_archive_json(LIVE_ARTIFACT_MEMBER)
        self.assertEqual(self.packet["shadow_artifact"]["content_hash"], content_hash(shadow))

    def test_every_delta_resolves_to_exact_different_values(self) -> None:
        import json
        baseline = json.loads(BASELINE.read_text(encoding="utf-8")); shadow = load_archive_json(LIVE_ARTIFACT_MEMBER)
        for delta in self.packet["deltas"]:
            self.assertEqual(delta["baseline_value"], resolve_pointer(baseline, delta["json_pointer"]))
            self.assertEqual(delta["shadow_value"], resolve_pointer(shadow, delta["json_pointer"]))
            self.assertNotEqual(delta["baseline_value"], delta["shadow_value"])
            self.assertEqual(delta["available_dispositions"], DISPOSITIONS)

    def test_complete_human_response_is_record_only(self) -> None:
        response = response_for(self.packet)
        validate_response(self.packet, response)
        self.assertEqual(response["effect"], "record_only")
        self.assertEqual(response["decided_by"]["authority_role"], "enterprise-risk-acceptance-authority")

    def test_missing_mutated_or_unauthorized_response_fails_closed(self) -> None:
        missing = response_for(self.packet); missing["delta_decisions"].pop()
        with self.assertRaises(ValidationFailure): validate_response(self.packet, missing)
        mutated = response_for(self.packet); mutated["packet_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValidationFailure): validate_response(self.packet, mutated)
        unauthorized = response_for(self.packet); unauthorized["decided_by"]["authority_role"] = "governance-records-administrator"
        with self.assertRaises(ValidationFailure): validate_response(self.packet, unauthorized)
        inconsistent = response_for(self.packet, "require_normalization"); inconsistent["overall_recommendation"] = "eligible_for_cutover_review"
        with self.assertRaises(ValidationFailure): validate_response(self.packet, inconsistent)

    def test_packet_and_review_cannot_authorize_cutover(self) -> None:
        review = render_review(self.packet)
        self.assertIn("CUTOVER BLOCKED", review)
        self.assertIn("separate later ADR", review)
        self.assertNotIn("APPROVED FOR DISTRIBUTION", review)

    def test_generation_leaves_baseline_and_report_unchanged(self) -> None:
        before = (BASELINE.read_bytes(), REPORT.read_bytes()); build_packet()
        self.assertEqual(before, (BASELINE.read_bytes(), REPORT.read_bytes()))

    def test_state_machine_is_closed_and_record_only(self) -> None:
        machine = load_json(ROOT / "orchestration/state-machines/semantic-adjudication.state-machine.json")
        states = set(machine["states"])
        self.assertIn(machine["initial_state"], states)
        self.assertTrue(set(machine["terminal_states"]).issubset(states))
        for transition in machine["transitions"]:
            self.assertIn(transition["from"], states)
            self.assertIn(transition["to"], states)
        self.assertEqual(machine["effects"]["all_states"], "record_only")
        self.assertEqual(machine["effects"]["cutover_authority"], "none")

if __name__ == "__main__": unittest.main(verbosity=2)

#!/usr/bin/env python3
"""ADR-0015 shadow integration, isolation, divergence, and rollback tests."""
from __future__ import annotations
import copy, unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from shadow_product_synth_runtime import (assert_no_publication_target, build_shadow_cap_risk,
                                          compare_paths, persist_shadow, validate_product_handoff)
from run_shadow_product_synth_reference import BASELINE, BASELINE_WORKFLOW, PROD_SYNTH, REPORT
from validate_vertical_slice import ROOT, ValidationFailure, load_json, validate_workflow_instance

SHADOW_WORKFLOW = ROOT / "appendices/candidate-workflows/prod-synth-cap-risk-shadow.workflow.json"

class ShadowProductSynthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline, self.product = load_json(BASELINE), load_json(PROD_SYNTH)
        self.shadow = build_shadow_cap_risk(self.baseline, self.product)

    def test_workflow_valid_and_baseline_unscheduled(self) -> None:
        registry = {i["designation"]: i for i in load_json(ROOT / "agents/agent-identities.json")["agents"]}
        validate_workflow_instance(load_json(SHADOW_WORKFLOW), registry, "ADR-0015 shadow workflow")
        self.assertFalse(any(n["designation"] == "PROD-SYNTH" for n in load_json(BASELINE_WORKFLOW)["nodes"]))

    def test_replay_deterministic_and_semantically_equivalent(self) -> None:
        self.assertEqual(self.shadow, build_shadow_cap_risk(copy.deepcopy(self.baseline), copy.deepcopy(self.product)))
        result = compare_paths(self.baseline, self.product, self.shadow)
        self.assertEqual(result["overall_state"], "equivalent")
        self.assertTrue(result["lineage"]["exact_child_binding"])
        self.assertEqual(result["authority_effect"], "comparison_only")

    def test_dropped_lineage_and_semantic_divergence_block(self) -> None:
        bad = copy.deepcopy(self.product)
        bad["extensions"]["product"]["role"]["capability_handoff"]["preserved_evidence_refs"] = []
        self.assertEqual(compare_paths(self.baseline, bad, build_shadow_cap_risk(self.baseline, bad))["overall_state"], "blocked")
        divergent = copy.deepcopy(self.shadow)
        divergent["extensions"]["capability"]["role"]["risk_register"][0]["priority"] = "low"
        self.assertEqual(compare_paths(self.baseline, self.product, divergent)["overall_state"], "blocked")

    def test_invented_lineage_fails_closed(self) -> None:
        invented = copy.deepcopy(self.product)
        invented["extensions"]["product"]["role"]["capability_handoff"]["preserved_evidence_refs"].append("INVENTED")
        with self.assertRaises(ValidationFailure): validate_product_handoff(invented)

    def test_storage_separate_and_publication_rejected(self) -> None:
        ledger = MagicMock()
        ledger.persist_record.side_effect = [{"family": "shadow-artifact"}, {"family": "shadow-comparison"}]
        with patch("shadow_product_synth_runtime.ArtifactLedger", return_value=ledger):
            persist_shadow(Path("isolated-shadow-ledger"), self.shadow, compare_paths(self.baseline, self.product, self.shadow))
        self.assertEqual([call.args[1] for call in ledger.persist_record.call_args_list], ["shadow-artifact", "shadow-comparison"])
        with self.assertRaises(ValidationFailure): assert_no_publication_target(Path("output/report-packages"))

    def test_rollback_leaves_authoritative_bytes_unchanged(self) -> None:
        before = (BASELINE.read_bytes(), BASELINE_WORKFLOW.read_bytes(), REPORT.read_bytes())
        compare_paths(self.baseline, self.product, self.shadow)
        self.assertEqual(before, (BASELINE.read_bytes(), BASELINE_WORKFLOW.read_bytes(), REPORT.read_bytes()))

if __name__ == "__main__": unittest.main(verbosity=2)

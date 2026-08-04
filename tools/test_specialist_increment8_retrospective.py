#!/usr/bin/env python3
"""Validate the ADR-0039 all-specialist comparison and final-state register."""
from __future__ import annotations
from build_specialist_increment8_retrospective import OUTPUT, build, load

def main() -> int:
    summary=build(); register=load(OUTPUT/"final-state-register.json"); comparison=load(OUTPUT/"all-agent-comparison.json")
    assert summary["passed"] and summary["registered_agents"] == 22 and summary["gx10_passed"] == 22
    assert len(register["states"]) == 22 and len({x["designation"] for x in register["states"]}) == 22
    assert all(x["final_state"] == "blocked_on_evidence" and not x["candidate_complete"] for x in register["states"])
    assert all(x["lifecycle"]["comparison_only"] and not any(v for k,v in x["lifecycle"].items() if k != "comparison_only") for x in register["states"])
    assert comparison["usage"]["input_tokens"] == 53369 and comparison["usage"]["output_tokens"] == 8641
    assert comparison["human_metrics"]["state"] == "not_yet_observable" and comparison["coverage"]["human_responses"] == 0
    print({"suite":"adr0039-increment8-retrospective","agents":22,"machine_preparation":"passed","human_review":"pending","unsafe_lifecycle_states":0}); return 0
if __name__ == "__main__": raise SystemExit(main())

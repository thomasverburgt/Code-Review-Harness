#!/usr/bin/env python3
"""Positive and fail-closed tests for ADR-0039 Increments 5-7."""
from __future__ import annotations
import copy, json, tempfile
from pathlib import Path
from run_specialist_increment567 import CONFIG, base, configure
from specialist_shadow_calibration_runtime import SpecialistShadowCalibrationError, validate_candidate_artifact

def main() -> int:
    configure()
    with tempfile.TemporaryDirectory() as td:
        summary=base.generate(Path(td)); assert len(summary["candidates"]) == 11
        rejected=0
        for designation,cfg in CONFIG.items():
            folder=Path(td)/cfg["slug"]; manifest=json.loads((folder/"input-manifest.json").read_text()); candidate=json.loads((folder/"candidate.artifact.json").read_text())
            validate_candidate_artifact(manifest,candidate)
            unsafe=copy.deepcopy(candidate); unsafe["extensions"]["specialist"]["role"]["domain_records"][0]["effectiveness"]="demonstrated"
            try: validate_candidate_artifact(manifest,unsafe)
            except SpecialistShadowCalibrationError: rejected += 1
            else: raise AssertionError(f"unsupported effectiveness accepted for {designation}")
        assert rejected == 11
    print({"suite":"adr0039-increment567-specialists","positive_candidates":11,"negative_mutations_rejected":11,"human_review_deferred":True}); return 0
if __name__ == "__main__": raise SystemExit(main())

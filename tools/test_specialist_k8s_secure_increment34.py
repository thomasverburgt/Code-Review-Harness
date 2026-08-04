#!/usr/bin/env python3
"""Positive and fail-closed tests for ADR-0039 Increments 3 and 4."""
from __future__ import annotations
import copy
import tempfile
from pathlib import Path
from run_specialist_k8s_secure_increment34 import CONFIG, base, configure
from specialist_shadow_calibration_runtime import SpecialistShadowCalibrationError, validate_candidate_artifact

def rejected(manifest, candidate, mutate):
 value=copy.deepcopy(candidate); mutate(value)
 try: validate_candidate_artifact(manifest,value)
 except SpecialistShadowCalibrationError: return
 raise AssertionError("unsafe mutation was accepted")

def main()->int:
 configure()
 with tempfile.TemporaryDirectory() as td:
  summary=base.generate(Path(td)); assert len(summary["candidates"])==5
  for designation,cfg in CONFIG.items():
   folder=Path(td)/cfg["slug"]
   import json
   manifest=json.loads((folder/"input-manifest.json").read_text()); candidate=json.loads((folder/"candidate.artifact.json").read_text())
   validate_candidate_artifact(manifest,candidate)
   if designation=="SPEC-K8S-WORKLOAD": rejected(manifest,candidate,lambda v:v["extensions"]["specialist"]["role"]["workloads"][0].update(runtime_effectiveness="demonstrated"))
   if designation=="SPEC-K8S-PLATFORM": rejected(manifest,candidate,lambda v:v["extensions"]["specialist"]["role"]["platform_controls"][0].update(tenant_isolation_confidence=0.9))
   if designation=="SPEC-COMMS": rejected(manifest,candidate,lambda v:v["extensions"]["specialist"]["role"]["trust_paths"][0].update(runtime_effectiveness="demonstrated"))
   if designation=="SPEC-SECURE-CODE": rejected(manifest,candidate,lambda v:v["extensions"]["specialist"]["role"]["code_assessments"][0].update(exploitability="demonstrated"))
   if designation=="SPEC-SECRETS": rejected(manifest,candidate,lambda v:v["extensions"]["specialist"]["role"]["secret_observations"][0].update(evidence_state="confirmed_secret"))
 print({"suite":"adr0039-increment34-specialists","positive_candidates":5,"negative_mutations_rejected":5,"human_review_deferred":True})
 return 0
if __name__=="__main__": raise SystemExit(main())

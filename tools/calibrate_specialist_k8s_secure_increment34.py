#!/usr/bin/env python3
"""Run isolated GX-10 Qwen3-32B calibration for ADR-0039 Increments 3 and 4."""
from __future__ import annotations
import calibrate_specialist_build_supply_chain_increment2 as calibration
import run_specialist_k8s_secure_increment34 as increment

increment.configure()
calibration.CONFIG = increment.CONFIG
calibration.build_manifest = increment.build_manifest
calibration.build_candidate = increment.base.build_candidate
calibration.locator = increment.base.locator
calibration.GENERATED_AT = increment.base.GENERATED_AT
calibration.ROLE_SUITE = "adr0039-increment34-kubernetes-secure-live-calibration"
calibration.ALL_SUITE = "adr0039-increment34-all-kubernetes-secure-specialists"

if __name__ == "__main__":
    raise SystemExit(calibration.main())

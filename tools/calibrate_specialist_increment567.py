#!/usr/bin/env python3
"""Run isolated GX-10 Qwen3-32B calibration for ADR-0039 Increments 5-7."""
from __future__ import annotations
import calibrate_specialist_build_supply_chain_increment2 as calibration
import run_specialist_increment567 as increment

increment.configure()
calibration.CONFIG = increment.CONFIG
calibration.build_manifest = increment.build_manifest
calibration.build_candidate = increment.base.build_candidate
calibration.locator = increment.base.locator
calibration.GENERATED_AT = increment.base.GENERATED_AT
calibration.ROLE_SUITE = "adr0039-increment567-live-calibration"
calibration.ALL_SUITE = "adr0039-increment567-all-specialists"
if __name__ == "__main__": raise SystemExit(calibration.main())

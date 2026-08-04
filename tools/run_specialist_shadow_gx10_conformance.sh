#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${1:-${ROOT}/_runs/specialist-shadow-calibration-gx10}"
mkdir -p "${OUTPUT}"
TRANSCRIPT="${OUTPUT}/gx10-conformance.txt"
exec > >(tee "${TRANSCRIPT}") 2>&1

echo "ADR-0039 Increment 0 GX-10 conformance"
echo "started_at=$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
echo "hostname=$(hostname)"
echo "architecture=$(uname -m)"
echo "kernel=$(uname -sr)"
echo "python=$(python3 --version 2>&1)"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader

cd "${ROOT}"
sha256sum \
  tools/specialist_shadow_calibration_runtime.py \
  tools/run_specialist_shadow_calibration_reference.py \
  tools/test_specialist_shadow_calibration.py \
  contracts/specialist-human-shadow-calibration-contract.md \
  orchestration/state-machines/specialist-human-shadow-calibration.state-machine.json

python3 tools/run_specialist_shadow_calibration_reference.py --output "${OUTPUT}/reference-run"
python3 tools/test_specialist_shadow_calibration.py -v
python3 tools/check_repository_structure.py
python3 tools/validate_vertical_slice.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/build_artifact_catalogs.py --check

tar -czf "${OUTPUT}/reference-run.tar.gz" -C "${OUTPUT}" reference-run
sha256sum "${OUTPUT}/reference-run.tar.gz"
echo "completed_at=$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
echo "result=pass"

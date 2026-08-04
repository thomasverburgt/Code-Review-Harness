#!/usr/bin/env python3
"""Audit the complete ADR-0039 specialist calibration against prompt library 0.2.0."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "appendices/prompt-templates/candidates/manifest-design-0.2.0.json"
CALIBRATION = (
    ROOT
    / "fixtures/specialist-calibration-0.2.0/evidence/2026-08-04/adr0039/gx10-live-run-001"
)
REQUIRED = {
    "evidence-locators.json",
    "human-shadow-review-packet.json",
    "input-manifest.json",
    "model-candidate.artifact.json",
    "raw-response.json",
    "summary.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = load(MANIFEST)
    assert manifest["prompt_version"] == "design-0.2.0"
    expected = manifest["prompts"]
    observed: set[str] = set()
    input_tokens = 0
    output_tokens = 0

    for run_dir in sorted(path for path in CALIBRATION.iterdir() if path.is_dir()):
        missing = REQUIRED - {path.name for path in run_dir.iterdir() if path.is_file()}
        assert not missing, f"{run_dir.name}: missing {sorted(missing)}"

        candidate = load(run_dir / "model-candidate.artifact.json")
        summary = load(run_dir / "summary.json")
        designation = candidate["identity"]["designation"]
        assert designation in expected, f"unexpected designation: {designation}"
        assert designation not in observed, f"duplicate designation: {designation}"
        observed.add(designation)

        prompt_entry = expected[designation]
        prompt_path = ROOT / prompt_entry["path"]
        prompt_hash = sha256(prompt_path)
        binding = candidate["execution"]["execution_bindings"]["prompt"]
        assert prompt_hash == prompt_entry["sha256"], f"{designation}: manifest hash mismatch"
        assert binding["hash"] == f"sha256:{prompt_hash}", f"{designation}: bound prompt hash mismatch"
        assert binding["version"] == "design-0.2.0"
        assert candidate["identity"]["agent_version"] == "design-0.2.0"
        assert candidate["execution"]["prompt_version"] == "design-0.2.0"
        assert summary["passed"] is True
        assert summary["status"] == "complete"
        assert summary["deployment_authorized"] is False
        assert summary["report_eligible"] is False

        usage = summary.get("usage", {})
        input_tokens += int(usage.get("input_tokens", 0))
        output_tokens += int(usage.get("output_tokens", 0))

    assert observed == set(expected), f"coverage mismatch: {sorted(set(expected) - observed)}"
    print(
        json.dumps(
            {
                "validated_agents": len(observed),
                "prompt_version": "design-0.2.0",
                "all_passed": True,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

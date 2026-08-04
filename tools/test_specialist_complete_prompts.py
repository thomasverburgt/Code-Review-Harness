#!/usr/bin/env python3
"""Validate the complete design-0.2.0 specialist prompt set."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "appendices/prompt-templates/candidates/manifest-design-0.2.0.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "agents/focus-profiles/catalog.json").read_text(encoding="utf-8"))
    profiles = {item["designation"]: json.loads((ROOT / item["path"]).read_text(encoding="utf-8")) for item in catalog["profiles"] if item["designation"].startswith("SPEC-")}
    assert manifest["prompt_version"] == "design-0.2.0"
    assert set(manifest["prompts"]) == set(profiles)
    for designation, entry in manifest["prompts"].items():
        data = (ROOT / entry["path"]).read_bytes()
        text = data.decode("utf-8")
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        assert text.startswith(f"BEGIN {designation} PROMPT")
        assert text.rstrip().endswith(f"END {designation} PROMPT")
        assert not re.search(r"\bintern\b", text, re.IGNORECASE)
        for number in range(1, 19):
            assert re.search(rf"(?m)^{number}\. ", text), (designation, number)
        for value in profiles[designation]["focus"]["dimensions"]:
            assert value in text, (designation, value)
        for value in profiles[designation]["focus"]["evidence_priorities"]:
            assert value in text, (designation, value)
        assert "Runtime environment control" in text
        assert "decision_authority: human" in text
        assert "incomplete_input" in text and "failed" in text and "superseded" in text
        assert "observations" in text and "assessments" in text and "findings" in text
        assert "patterns" in text and "insights" in text and "conflicts" in text
        assert "DGX Spark" in text and "A100" in text
    print(json.dumps({"validated": len(manifest["prompts"]), "version": manifest["prompt_version"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

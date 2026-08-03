#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from tools.validate_vertical_slice import assert_schema


ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "agents" / "focus-profiles"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AgentFocusProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load(ROOT / "agents" / "agent-identities.json")
        cls.catalog = load(PROFILE_DIR / "catalog.json")

    def test_generated_profiles_are_current(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_agent_focus_profiles.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_catalog_and_profiles_validate(self):
        assert_schema(self.catalog, "agent-focus-profile-catalog.schema.json", "focus profile catalog")
        for entry in self.catalog["profiles"]:
            assert_schema(load(ROOT / entry["path"]), "agent-focus-profile.schema.json", entry["designation"])

    def test_registry_has_exactly_one_profile_per_agent(self):
        registry = {item["designation"]: item for item in self.registry["agents"]}
        catalog = {item["designation"]: item for item in self.catalog["profiles"]}
        self.assertEqual(set(registry), set(catalog))
        self.assertEqual(len(catalog), len(self.catalog["profiles"]))
        for designation, agent in registry.items():
            entry = catalog[designation]
            profile_path = ROOT / entry["path"]
            profile = load(profile_path)
            self.assertEqual(profile["profile_id"], f"FOCUS-{designation}")
            self.assertEqual(profile["agent"]["agent_uuid"], agent["agent_uuid"])
            self.assertEqual(profile["agent"]["display_name"], agent["display_name"])
            self.assertEqual(profile["agent"]["layer"], agent["layer"])
            self.assertEqual(profile["agent"]["contract_version"], agent["contract_version"])
            self.assertEqual(profile["lifecycle"]["agent_status"], agent["status"])
            self.assertTrue(profile["focus"]["authoritative_questions"][0].endswith("?"))
            actual = "sha256:" + hashlib.sha256(profile_path.read_bytes()).hexdigest()
            self.assertEqual(entry["sha256"], actual)

    def test_profile_sources_are_exact_and_current(self):
        for entry in self.catalog["profiles"]:
            profile = load(ROOT / entry["path"])
            source = ROOT / profile["source"]["specification"]
            self.assertTrue(source.is_file())
            actual = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertEqual(profile["source"]["specification_sha256"], actual)
            self.assertEqual(profile["source"]["identity_registry_version"], self.registry["registry_version"])

    def test_prompt_focus_is_compression_protected_and_fail_closed(self):
        protected = {"authoritative_questions", "dimensions", "evidence_priorities", "prohibited_conclusions", "rubric_checks", "evidence locators", "active limitations", "human authority boundaries"}
        for entry in self.catalog["profiles"]:
            profile = load(ROOT / entry["path"])
            binding = profile["prompt_binding"]
            self.assertEqual(set(binding["compression_protected_elements"]), protected)
            self.assertEqual(binding["missing_profile_effect"], "fail_closed_before_dispatch")
            self.assertEqual(binding["hash_mismatch_effect"], "fail_closed_before_dispatch")

    def test_deterministic_gates_do_not_claim_semantic_authority(self):
        for designation in ("CAP-COORD", "ENT-EVIDENCE"):
            profile = load(PROFILE_DIR / f"{designation.lower()}.json")
            combined = " ".join(profile["focus"]["prohibited_conclusions"])
            self.assertIn("Do not", combined)
            self.assertTrue("assessment" in combined or "conclusion" in combined)


if __name__ == "__main__":
    unittest.main()

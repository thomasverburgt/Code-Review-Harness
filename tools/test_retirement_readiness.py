from __future__ import annotations

import subprocess
import unittest

from tools.build_retirement_readiness import ROOT, manifest


class RetirementReadinessDeterminismTests(unittest.TestCase):
    def test_training_inventory_counts_only_tracked_repository_files(self) -> None:
        data = manifest()
        for entry in data["candidates"]["training_and_qa_paths"]["paths"]:
            result = subprocess.run(
                ["git", "ls-files", "-z", "--", entry["path"]],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            tracked = [value for value in result.stdout.split("\0") if value]
            self.assertEqual(entry["file_count"], len(tracked))


if __name__ == "__main__":
    unittest.main()

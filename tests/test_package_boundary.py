from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class PackageBoundaryTests(unittest.TestCase):
    def test_ledger_api_is_available(self):
        from code_harness.artifact_ledger import ArtifactLedger, LedgerError

        self.assertTrue(callable(ArtifactLedger))
        self.assertTrue(issubclass(LedgerError, Exception))

    def test_representative_runtime_apis_are_available(self):
        from code_harness.worker_runtime import Worker
        from code_harness.report_governance_runtime import build_report_package

        self.assertTrue(callable(Worker))
        self.assertTrue(callable(build_report_package))

    def test_package_clis_match_direct_validation(self):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(SRC)
        result = subprocess.run(
            [sys.executable, "-c", "from code_harness.cli import check_repository, validate_vertical; raise SystemExit(check_repository() or validate_vertical())"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)


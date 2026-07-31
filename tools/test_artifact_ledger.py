#!/usr/bin/env python3
"""Conformance tests for the filesystem reference artifact ledger.

Run this suite only on the approved DGX Spark or equivalent test platform.
"""

from __future__ import annotations

import copy
import json
import tempfile
import uuid
from pathlib import Path

from artifact_ledger import ArtifactLedger, LedgerError, pretty_bytes
from run_vertical_slice import DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, run
from validate_vertical_slice import FIXTURE_DIR, WORKFLOW, assert_schema


def expect_failure(operation, expected: str) -> None:
    try:
        operation()
    except LedgerError as exc:
        if expected.lower() not in str(exc).lower():
            raise AssertionError(f"expected {expected!r}, got {exc!r}") from exc
    else:
        raise AssertionError(f"operation unexpectedly succeeded; expected {expected!r}")


def json_tree(root: Path) -> dict[str, object]:
    return {path.relative_to(root).as_posix(): json.loads(path.read_text(encoding="utf-8"))
            for path in root.rglob("*.json")}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="artifact-ledger-tests-") as temp_name:
        base = Path(temp_name)
        run_dir = base / "run"
        ledger_dir = base / "ledger"
        replay_dir = base / "replay"
        run(run_dir, DEFAULT_EXECUTION_ID, DEFAULT_STARTED_AT, "gold")
        ledger = ArtifactLedger(ledger_dir)
        source_artifacts = sorted(FIXTURE_DIR.glob("*.artifact.json"))

        first = ledger.persist_execution(run_dir, source_artifacts, WORKFLOW)
        second = ledger.persist_execution(run_dir, source_artifacts, WORKFLOW)
        assert first == second, "idempotent persistence changed its result"
        verified = ledger.verify_execution(DEFAULT_EXECUTION_ID)
        assert verified["status"] == "verified"
        assert_schema(ledger.load_manifest(DEFAULT_EXECUTION_ID), "execution-ledger-manifest.schema.json", "ledger manifest")

        replayed = ledger.replay(DEFAULT_EXECUTION_ID, replay_dir)
        assert replayed["status"] == "replayed"
        original = json_tree(run_dir)
        retained_run = {path: value for path, value in json_tree(replay_dir).items()
                        if not path.startswith("artifacts/") and path != "workflow.json"}
        assert original == retained_run, "replayed run records changed identifiers or meaning"

        summary_path = run_dir / "summary.json"
        original_summary = summary_path.read_bytes()
        mutated = json.loads(original_summary)
        mutated["status"] = "failed"
        summary_path.write_bytes(pretty_bytes(mutated))
        expect_failure(lambda: ledger.persist_execution(run_dir, source_artifacts, WORKFLOW), "mutation")
        summary_path.write_bytes(original_summary)

        spec = json.loads((FIXTURE_DIR / "spec-secrets.artifact.json").read_text(encoding="utf-8"))
        previous_id = spec["artifact"]["artifact_id"]
        successor = copy.deepcopy(spec)
        successor_id = str(uuid.uuid5(uuid.UUID("92000000-0000-4000-8000-000000000000"), previous_id))
        successor["artifact"]["artifact_id"] = successor_id
        successor["artifact"]["links"]["parents"] = [previous_id]
        ledger.persist_artifact(successor)
        supersession = ledger.record_supersession(previous_id, successor_id, "fixture-maintainer",
                                                  "2026-07-31T18:00:00Z", "validated successor fixture")
        supersession_record = {key: value for key, value in supersession.items() if key != "record_object_hash"}
        assert_schema(supersession_record, "supersession-record.schema.json", "supersession record")
        assert ledger.get_object(supersession["previous_object_hash"])["artifact"]["artifact_id"] == previous_id
        assert ledger.get_object(supersession["successor_object_hash"])["artifact"]["artifact_id"] == successor_id
        expect_failure(lambda: ledger.record_supersession(previous_id, previous_id, "fixture-maintainer",
                                                          "2026-07-31T18:00:00Z", "invalid"), "cannot supersede itself")

        manifest = ledger.load_manifest(DEFAULT_EXECUTION_ID)
        summary_ref = next(ref for ref in manifest["records"] if ref["logical_path"] == "summary.json")
        object_path = ledger._object_path(summary_ref["object_hash"])
        original_object = object_path.read_bytes()
        object_path.write_bytes(b"{}\n")
        expect_failure(lambda: ledger.verify_execution(DEFAULT_EXECUTION_ID), "integrity")
        object_path.write_bytes(original_object)

        events = json.loads((run_dir / "audit-events.json").read_text(encoding="utf-8"))
        expect_failure(lambda: ledger._build_audit_chain(list(reversed(events)), DEFAULT_EXECUTION_ID), "ordered")
        expect_failure(lambda: ledger._record_ref("restricted.json", "test", "restricted", {"x": 1},
                                                  classification="restricted"), "access denied")

        print(json.dumps({
            "suite": "artifact-ledger-conformance",
            "persistence": "passed",
            "idempotency": "passed",
            "integrity": "passed",
            "replay": "passed",
            "supersession": "passed",
            "access_control": "passed",
            "audit_chain": "passed",
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

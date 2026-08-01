#!/usr/bin/env python3
"""Build redacted, read-only repository evidence for secrets prompt calibration."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PATTERNS = (
    ("private-key-header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("credential-assignment", re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|client[_-]?secret)\b\s*[:=]\s*[^\s${}\[\]]{8,}")),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/-]{16,}={0,2}")),
)
MAX_FILE_BYTES = 1_000_000
MAX_INVENTORY_ITEMS = 40
MAX_FINDINGS = 100


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_dir.resolve()
    output = args.output.resolve()
    revision = git(repo, "rev-parse", "HEAD")
    remote = git(repo, "remote", "get-url", "origin")
    tracked = git(repo, "ls-files", "-z").split("\0")
    tracked = sorted(path for path in tracked if path)
    inventory = []
    findings = []
    scanned_files = 0
    omitted_large_or_binary = 0
    for relative in tracked:
        path = repo / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if len(inventory) < MAX_INVENTORY_ITEMS:
            inventory.append({"path": relative, "bytes": len(data), "sha256": digest})
        if len(data) > MAX_FILE_BYTES or b"\0" in data:
            omitted_large_or_binary += 1
            continue
        scanned_files += 1
        text = data.decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for detector, pattern in PATTERNS:
                if pattern.search(line) and len(findings) < MAX_FINDINGS:
                    findings.append({
                        "evidence_id": f"UDS-{len(findings) + 1:04d}",
                        "detector": detector,
                        "locator": {"path": relative, "line": line_number},
                        "redaction": "matched value omitted",
                        "line_fingerprint": "sha256:" + hashlib.sha256(line.encode("utf-8")).hexdigest(),
                    })
    manifest = {
        "manifest_version": "1.0.0",
        "collection": {
            "method": "read-only shallow Git clone plus offline redacted heuristic scan",
            "collected_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "repository": remote,
            "revision": revision,
            "mutation_performed": False,
            "credential_validation_performed": False,
        },
        "eligible_population": {
            "tracked_files": len(tracked),
            "scanned_text_files": scanned_files,
            "omitted_large_or_binary_files": omitted_large_or_binary,
            "history_depth": "shallow current revision only",
            "runtime_and_external_secret_stores": "not assessed",
        },
        "inventory_sample": inventory,
        "inventory_sample_limit": MAX_INVENTORY_ITEMS,
        "redacted_detector_findings": findings,
        "finding_limit": MAX_FINDINGS,
        "limitations": [
            "Heuristic calibration evidence is not a production secret scanner result.",
            "No Git history, live credential validation, runtime configuration, external store, or downstream artifact was examined.",
            "Matched values and source-line content are deliberately excluded.",
        ],
        "access_classification": "internal-test-redacted",
        "reliability": "calibration-only",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"revision": revision, "tracked_files": len(tracked), "scanned_text_files": scanned_files,
                      "redacted_findings": len(findings), "output": str(output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

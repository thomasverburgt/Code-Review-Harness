#!/usr/bin/env python3
"""Build or verify deterministic manifests for controlled binary releases."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "training" / "agentic-system-curriculum"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(path: Path, generator: str, lifecycle: str = "release_candidate") -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "generator": generator,
        "lifecycle": lifecycle,
    }


def deliverables_manifest() -> tuple[Path, dict]:
    base = ROOT / "deliverables"
    generators = {
        "SPEC-SECRETS-Prompt-Design-and-Methodology.docx": "document_builders/build_spec_secrets_prompt_design.py",
        "PROD-SEC-Prompt-Design-and-Methodology.docx": "document_builders/build_prod_sec_prompt_design.py",
        "CAP-RISK-Prompt-Design-and-Methodology.docx": "document_builders/build_cap_risk_prompt_design.py",
        "ENT-SYSRISK-Prompt-Design-and-Methodology.docx": "document_builders/build_ent_sysrisk_prompt_design.py",
    }
    artifacts = [entry(base / name, generator) for name, generator in sorted(generators.items())]
    return base / "release-manifest.json", {
        "manifest_version": "1.0.0",
        "collection": "prompt-design-deliverables",
        "state": "design_candidate",
        "binary_policy": "legacy_git_until_verified_lfs_migration",
        "artifacts": artifacts,
    }


def training_manifest(variant: str) -> tuple[Path, dict]:
    base = TRAINING / variant
    if variant == "revised":
        artifacts = [entry(base / "Code-Review-Harness-Agentic-System-Curriculum.docx", "training/agentic-system-curriculum/revised/build/build_handbook.py")]
        artifacts.extend(entry(path, "training/agentic-system-curriculum/revised/build/build_decks.mjs") for path in sorted((base / "slides").glob("*.pptx")))
        transient = ["qa-final", "renders", "slides/*.inspect.ndjson"]
        collection = "agentic-system-curriculum-full"
    else:
        artifacts = [entry(base / "Code-Review-Harness-Agentic-System-Curriculum-Condensed.docx", "training/agentic-system-curriculum/revised/build/build_condensed_handbook.py")]
        artifacts.extend(entry(path, "training/agentic-system-curriculum/revised/build/build_condensed_decks.mjs") for path in sorted((base / "slides").glob("*.pptx")))
        artifacts.extend(entry(path, "training/agentic-system-curriculum/revised/build/build_reference_primers.py") for path in sorted((base / "handouts").glob("*.docx")))
        transient = ["qa", "qa2", "qa3", "renders", "slides/*.inspect.ndjson"]
        collection = "agentic-system-curriculum-condensed"
    artifacts.append(entry(base / "QA-Release-Report.md", "human_visual_review", "qa_record"))
    return base / "release-manifest.json", {
        "manifest_version": "1.0.0",
        "collection": collection,
        "state": "qa_passed_release_candidate",
        "binary_policy": "legacy_git_until_verified_lfs_migration",
        "transient_or_external_archive_candidates": transient,
        "artifacts": sorted(artifacts, key=lambda item: item["path"]),
    }


def manifests() -> list[tuple[Path, dict]]:
    return [deliverables_manifest(), training_manifest("revised"), training_manifest("condensed")]


def canonical(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when a committed manifest is stale")
    args = parser.parse_args()
    stale: list[str] = []
    for path, data in manifests():
        rendered = canonical(data)
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.write_text(rendered, encoding="utf-8", newline="\n")
    if stale:
        print("Stale release manifests:")
        for path in stale:
            print(f"- {path}")
        return 1
    print("Release manifests verified." if args.check else "Release manifests written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


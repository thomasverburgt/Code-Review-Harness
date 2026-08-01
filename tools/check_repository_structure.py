#!/usr/bin/env python3
"""Zero-dependency checks for repository navigation and controlled registries."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".ps1", ".sh"}
SKIP_PARTS = {".git", "_docx_work", "_runs", "__pycache__"}
# Construct markers from code points so the checker does not contain the
# sequences it is intended to reject.
MOJIBAKE = (
    "".join(map(chr, (226, 8364, 339))),
    "".join(map(chr, (226, 8364, 157))),
    "".join(map(chr, (226, 8364, 8482))),
    "".join(map(chr, (226, 8364, 8221))),
)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def files(suffixes: set[str]):
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in suffixes and not SKIP_PARTS.intersection(path.parts):
            yield path


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_utf8_and_mojibake(errors: list[str]) -> None:
    for path in files(TEXT_SUFFIXES):
        # Retained evidence may preserve the encoding emitted by its source
        # environment. It is immutable and is validated by its evidence hash.
        if "evidence" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative(path)}: invalid UTF-8: {exc}")
            continue
        for marker in MOJIBAKE:
            if marker in text:
                errors.append(f"{relative(path)}: suspected mojibake marker {marker!r}")
                break


def check_markdown_links(errors: list[str]) -> None:
    for path in files({".md"}):
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            elif " " in target:
                target = target.split(" ", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{relative(path)}: local link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"{relative(path)}: missing local link target: {raw_target}")


def check_agent_registry(errors: list[str]) -> None:
    registry_path = ROOT / "agents" / "agent-identities.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    seen_ids: set[str] = set()
    seen_designations: set[str] = set()
    for agent in registry["agents"]:
        agent_id = agent["agent_uuid"]
        designation = agent["designation"]
        if agent_id in seen_ids:
            errors.append(f"agents/agent-identities.json: duplicate UUID {agent_id}")
        if designation in seen_designations:
            errors.append(f"agents/agent-identities.json: duplicate designation {designation}")
        seen_ids.add(agent_id)
        seen_designations.add(designation)
        specification = ROOT / "agents" / agent["specification"]
        if not specification.is_file():
            errors.append(f"agents/agent-identities.json: {designation} missing specification {relative(specification)}")


def check_prompt_manifest(errors: list[str]) -> None:
    manifest_path = ROOT / "appendices" / "prompt-templates" / "candidates" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for designation, entry in manifest["prompts"].items():
        prompt = ROOT / entry["path"]
        source = ROOT / entry["source"]
        if not prompt.is_file():
            errors.append(f"candidate prompt {designation}: missing {entry['path']}")
            continue
        if not source.is_file():
            errors.append(f"candidate prompt {designation}: missing source {entry['source']}")
        actual = hashlib.sha256(prompt.read_bytes()).hexdigest()
        if actual != entry["sha256"]:
            errors.append(f"candidate prompt {designation}: SHA-256 mismatch")


def check_schema_catalog(errors: list[str]) -> None:
    schema_dir = ROOT / "appendices" / "schemas"
    catalog = (schema_dir / "README.md").read_text(encoding="utf-8")
    seen_ids: dict[str, str] = {}
    for path in sorted(schema_dir.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative(path)}: invalid JSON: {exc}")
            continue
        if path.name not in catalog:
            errors.append(f"appendices/schemas/README.md: missing catalog entry for {path.name}")
        schema_id = schema.get("$id")
        if schema_id:
            if schema_id in seen_ids:
                errors.append(f"duplicate schema $id {schema_id}: {seen_ids[schema_id]} and {path.name}")
            seen_ids[schema_id] = path.name


def check_release_manifests(errors: list[str]) -> None:
    for manifest_path in (
        ROOT / "deliverables" / "release-manifest.json",
        ROOT / "training" / "agentic-system-curriculum" / "revised" / "release-manifest.json",
        ROOT / "training" / "agentic-system-curriculum" / "condensed" / "release-manifest.json",
    ):
        if not manifest_path.is_file():
            errors.append(f"missing release manifest: {relative(manifest_path)}")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for artifact in manifest.get("artifacts", []):
            path = ROOT / artifact["path"]
            if not path.is_file():
                errors.append(f"{relative(manifest_path)}: missing artifact {artifact['path']}")
                continue
            if path.stat().st_size != artifact["bytes"]:
                errors.append(f"{relative(manifest_path)}: size mismatch for {artifact['path']}")
            if hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
                errors.append(f"{relative(manifest_path)}: SHA-256 mismatch for {artifact['path']}")
            generator = artifact.get("generator")
            if generator not in {"human_visual_review"} and not (ROOT / generator).is_file():
                errors.append(f"{relative(manifest_path)}: missing generator {generator}")


def check_artifact_catalog_paths(errors: list[str]) -> None:
    catalog_path = ROOT / "evidence" / "legacy-catalog.json"
    mapping_path = ROOT / "evidence" / "legacy-path-map.json"
    shared_path = ROOT / "fixtures" / "shared" / "content-addressed-index.json"
    for path in (catalog_path, mapping_path, shared_path, ROOT / "fixtures" / "catalog.json"):
        if not path.is_file():
            errors.append(f"missing artifact catalog: {relative(path)}")
            return
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    for package in catalog["packages"]:
        if not (ROOT / package["legacy_root"]).is_dir():
            errors.append(f"{relative(catalog_path)}: missing legacy root {package['legacy_root']}")
    shared = json.loads(shared_path.read_text(encoding="utf-8"))
    for item in shared["objects"]:
        paths = [
            item["canonical_source"],
            *item.get("reusable_fixture_copies", []),
            *item.get("immutable_evidence_copies", []),
        ]
        for value in paths:
            path = ROOT / value
            if not path.is_file():
                errors.append(f"{relative(shared_path)}: missing fixture path {value}")
            elif f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}" != item["object_id"]:
                errors.append(f"{relative(shared_path)}: hash mismatch for {value}")


def main() -> int:
    errors: list[str] = []
    check_utf8_and_mojibake(errors)
    check_markdown_links(errors)
    check_agent_registry(errors)
    check_prompt_manifest(errors)
    check_schema_catalog(errors)
    check_release_manifests(errors)
    check_artifact_catalog_paths(errors)
    if errors:
        print("Repository structural checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository structural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

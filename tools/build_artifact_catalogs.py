#!/usr/bin/env python3
"""Build deterministic fixture and legacy-evidence catalogs."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

try:
    from .canonical_content import canonical_file_bytes, catalog_size
except ImportError:
    from canonical_content import canonical_file_bytes, catalog_size


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
EVIDENCE = ROOT / "evidence"
EXCLUDED_FIXTURE_OUTPUTS = {
    FIXTURES / "catalog.json",
    FIXTURES / "shared" / "content-addressed-index.json",
}


def canonical(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_file_bytes(path)).hexdigest()


def scenario_roots() -> list[Path]:
    return sorted(
        (path for path in FIXTURES.iterdir() if path.is_dir() and path.name != "shared"),
        key=lambda path: path.name,
    )


def stable_files(root: Path) -> list[Path]:
    """Sort with POSIX relative strings instead of platform-specific Path ordering."""
    return sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def is_evidence(path: Path) -> bool:
    return "evidence" in path.relative_to(FIXTURES).parts


def fixture_catalog() -> tuple[Path, dict]:
    scenarios = []
    for root in scenario_roots():
        all_files = stable_files(root)
        evidence_files = [path for path in all_files if is_evidence(path)]
        reusable_files = [path for path in all_files if not is_evidence(path)]
        scenarios.append({
            "scenario": root.name,
            "root": root.relative_to(ROOT).as_posix(),
            "reusable_file_count": len(reusable_files),
            "legacy_evidence_file_count": len(evidence_files),
            "total_bytes": sum(catalog_size(path) for path in all_files),
        })
    return FIXTURES / "catalog.json", {
        "catalog_version": "1.0.0",
        "authority": "derived_index_only",
        "canonical_fixture_root": "fixtures",
        "canonical_future_evidence_root": "evidence",
        "scenarios": scenarios,
    }


def duplicate_groups() -> list[tuple[str, int, list[Path]]]:
    groups: dict[tuple[str, int], list[Path]] = defaultdict(list)
    for root in scenario_roots():
        for path in stable_files(root):
            if path in EXCLUDED_FIXTURE_OUTPUTS or path.name == ".gitkeep":
                continue
            groups[(sha256(path), catalog_size(path))].append(path)
    return [
        (digest, size, paths)
        for (digest, size), paths in sorted(groups.items())
        if len(paths) > 1
    ]


def shared_fixture_index() -> tuple[Path, dict]:
    objects = []
    for digest, size, paths in duplicate_groups():
        reusable = sorted(
            (path for path in paths if not is_evidence(path)),
            key=lambda path: path.relative_to(ROOT).as_posix(),
        )
        retained = sorted(
            (path for path in paths if is_evidence(path)),
            key=lambda path: path.relative_to(ROOT).as_posix(),
        )
        reusable_paths = [path.relative_to(ROOT).as_posix() for path in reusable]
        retained_paths = [path.relative_to(ROOT).as_posix() for path in retained]
        object_path = FIXTURES / "shared" / "objects" / "sha256" / digest[:2] / digest
        objects.append({
            "object_id": f"sha256:{digest}",
            "bytes": size,
            "canonical_source": object_path.relative_to(ROOT).as_posix(),
            "reusable_fixture_copies": reusable_paths,
            "immutable_evidence_copies": retained_paths,
            "migration_state": "shared_object_materialized_copies_retained",
        })
    return FIXTURES / "shared" / "content-addressed-index.json", {
        "index_version": "1.0.0",
        "authority": "derived_reuse_index_only",
        "objects": objects,
    }


def inventory(root: Path) -> tuple[str, int, int]:
    entries = []
    total = 0
    for path in stable_files(root):
        size = catalog_size(path)
        total += size
        entries.append({
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256(path),
            "bytes": size,
        })
    digest = hashlib.sha256(canonical(entries).encode("utf-8")).hexdigest()
    return digest, len(entries), total


def legacy_evidence_roots() -> list[tuple[str, Path]]:
    roots = []
    for scenario in scenario_roots():
        evidence_root = scenario / "evidence"
        if evidence_root.is_dir():
            roots.append((scenario.name, evidence_root))
    return roots


def legacy_catalog() -> tuple[Path, dict]:
    packages = []
    for scenario, root in legacy_evidence_roots():
        digest, count, total = inventory(root)
        packages.append({
            "scenario": scenario,
            "legacy_root": root.relative_to(ROOT).as_posix(),
            "inventory_sha256": f"sha256:{digest}",
            "file_count": count,
            "total_bytes": total,
            "retention": "immutable_in_place",
            "migration_state": "indexed_in_place",
        })
    return EVIDENCE / "legacy-catalog.json", {
        "catalog_version": "1.0.0",
        "authority": "derived_inventory_only",
        "packages": packages,
    }


def legacy_path_map() -> tuple[Path, dict]:
    mappings = []
    for scenario, root in legacy_evidence_roots():
        mappings.append({
            "legacy_root": root.relative_to(ROOT).as_posix(),
            "canonical_future_prefix": f"evidence/YYYY-MM-DD/adrNNNN/{scenario}/<run-id>",
            "treatment": "indexed_in_place",
            "remove_legacy": False,
        })
    return EVIDENCE / "legacy-path-map.json", {
        "map_version": "1.0.0",
        "decision": "ADR-0029",
        "mappings": mappings,
    }


def outputs() -> list[tuple[Path, dict]]:
    return [fixture_catalog(), shared_fixture_index(), legacy_catalog(), legacy_path_map()]


def materialize_shared_objects(check: bool) -> list[str]:
    stale = []
    for digest, _size, paths in duplicate_groups():
        object_path = FIXTURES / "shared" / "objects" / "sha256" / digest[:2] / digest
        if check:
            if not object_path.is_file() or sha256(object_path) != digest:
                stale.append(object_path.relative_to(ROOT).as_posix())
        else:
            rendered = canonical_file_bytes(paths[0])
            object_path.parent.mkdir(parents=True, exist_ok=True)
            if not object_path.is_file() or object_path.read_bytes() != rendered:
                object_path.write_bytes(rendered)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = materialize_shared_objects(args.check)
    for path, data in outputs():
        rendered = canonical(data)
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                path.write_text(rendered, encoding="utf-8", newline="\n")
    if stale:
        print("Stale artifact catalogs:")
        for path in stale:
            print(f"- {path}")
        return 1
    print("Artifact catalogs verified." if args.check else "Artifact catalogs written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

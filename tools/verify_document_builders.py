#!/usr/bin/env python3
"""Rebuild prompt-design DOCX files and compare their package contents."""

from __future__ import annotations

import importlib
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_runs" / "document-builder-verification"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BUILDERS = {
    "SPEC-SECRETS-Prompt-Design-and-Methodology.docx": "document_builders.build_spec_secrets_prompt_design",
    "PROD-SEC-Prompt-Design-and-Methodology.docx": "document_builders.build_prod_sec_prompt_design",
    "CAP-RISK-Prompt-Design-and-Methodology.docx": "document_builders.build_cap_risk_prompt_design",
    "ENT-SYSRISK-Prompt-Design-and-Methodology.docx": "document_builders.build_ent_sysrisk_prompt_design",
}


def normalized_member(name: str, data: bytes) -> bytes:
    if name == "docProps/core.xml":
        data = re.sub(
            rb"<dcterms:modified[^>]*>.*?</dcterms:modified>",
            b"<dcterms:modified>normalized</dcterms:modified>",
            data,
        )
    return data


def package(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"corrupt DOCX package: {path}")
        return {name: normalized_member(name, archive.read(name)) for name in archive.namelist()}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for filename, module_name in BUILDERS.items():
        module = importlib.import_module(module_name)
        generated = OUTPUT / filename
        module.OUT = generated
        module.build_document()
        expected = ROOT / "deliverables" / filename
        expected_members = package(expected)
        generated_members = package(generated)
        if expected_members != generated_members:
            changed = sorted(
                name for name in expected_members.keys() | generated_members.keys()
                if expected_members.get(name) != generated_members.get(name)
            )
            failures.append(f"{filename}: differing package members: {', '.join(changed)}")
    if failures:
        print("Document builder verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Document builders reproduced {len(BUILDERS)} controlled deliverables.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

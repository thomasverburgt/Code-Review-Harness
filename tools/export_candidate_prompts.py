#!/usr/bin/env python3
"""Extract the approved copy boundary from the four prompt-design DOCX files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "appendices" / "prompt-templates" / "candidates"
SOURCES = {
    "SPEC-SECRETS": ROOT / "deliverables" / "SPEC-SECRETS-Prompt-Design-and-Methodology.docx",
    "PROD-SEC": ROOT / "deliverables" / "PROD-SEC-Prompt-Design-and-Methodology.docx",
    "CAP-RISK": ROOT / "deliverables" / "CAP-RISK-Prompt-Design-and-Methodology.docx",
    "ENT-SYSRISK": ROOT / "deliverables" / "ENT-SYSRISK-Prompt-Design-and-Methodology.docx",
}


def extract(designation: str, source: Path) -> str:
    begin = f"BEGIN {designation} PROMPT"
    end = f"END {designation} PROMPT"
    lines: list[str] = []
    active = False
    for paragraph in Document(source).paragraphs:
        text = paragraph.text.strip()
        if text == begin:
            active = True
        if active and text:
            lines.append(text)
        if text == end:
            break
    if not lines or lines[0] != begin or lines[-1] != end:
        raise RuntimeError(f"copy boundary not found for {designation}")
    return "\n\n".join(lines) + "\n"


def main() -> int:
    manifest = {"manifest_version": "1.0.0", "prompt_version": "design-0.1.0", "prompts": {}}
    for designation, source in SOURCES.items():
        text = extract(designation, source)
        target = OUT / designation.lower() / "design-0.1.0.prompt.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        manifest["prompts"][designation] = {
            "path": target.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "source": source.relative_to(ROOT).as_posix(),
            "status": "candidate",
        }
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

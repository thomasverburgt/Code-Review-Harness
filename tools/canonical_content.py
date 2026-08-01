from __future__ import annotations

from pathlib import Path


CANONICAL_TEXT_SUFFIXES = {".json", ".md", ".txt", ".yaml", ".yml"}


def canonical_file_bytes(path: Path) -> bytes:
    """Return stable catalog bytes across LF and CRLF worktrees."""
    data = path.read_bytes()
    if path.suffix.lower() not in CANONICAL_TEXT_SUFFIXES or b"\x00" in data:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def catalog_size(path: Path) -> int:
    return len(canonical_file_bytes(path))

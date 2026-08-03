from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.build_artifact_catalogs import sha256, stable_files
from tools.canonical_content import canonical_file_bytes, catalog_size


class ArtifactCatalogCanonicalizationTests(unittest.TestCase):
    def test_text_identity_is_stable_across_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.md"
            crlf = root / "crlf.md"
            lf.write_bytes(b"first\nsecond\n")
            crlf.write_bytes(b"first\r\nsecond\r\n")

            self.assertEqual(canonical_file_bytes(lf), canonical_file_bytes(crlf))
            self.assertEqual(catalog_size(lf), catalog_size(crlf))
            self.assertEqual(sha256(lf), sha256(crlf))

    def test_binary_content_is_not_normalized_by_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "capture.txt"
            original = b"\x00first\r\nsecond\r\n"
            path.write_bytes(original)

            self.assertEqual(canonical_file_bytes(path), original)

    def test_gitkeep_identity_is_stable_across_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf" / ".gitkeep"
            crlf = root / "crlf" / ".gitkeep"
            lf.parent.mkdir()
            crlf.parent.mkdir()
            lf.write_bytes(b"placeholder\n")
            crlf.write_bytes(b"placeholder\r\n")

            self.assertEqual(canonical_file_bytes(lf), canonical_file_bytes(crlf))
            self.assertEqual(catalog_size(lf), catalog_size(crlf))
            self.assertEqual(sha256(lf), sha256(crlf))

    def test_file_order_uses_platform_independent_posix_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("z/item.json", "B/item.json", "a/item.json"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")

            self.assertEqual(
                [path.relative_to(root).as_posix() for path in stable_files(root)],
                ["B/item.json", "a/item.json", "z/item.json"],
            )


if __name__ == "__main__":
    unittest.main()

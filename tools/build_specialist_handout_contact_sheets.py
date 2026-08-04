#!/usr/bin/env python3
"""Build readable contact sheets for page-by-page specialist handout QA."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
QA_ROOT = ROOT / "_runs/handout-qa-020-20260804"
PAGES_ROOT = QA_ROOT / "pages"
SHEETS_ROOT = QA_ROOT / "contact-sheets"
PAGES_PER_SHEET = 9
COLS = 3
THUMB_W = 380
THUMB_H = 492
LABEL_H = 28
MARGIN = 20


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if not match:
        raise ValueError(f"page number missing from {path}")
    return int(match.group(1))


def main() -> int:
    SHEETS_ROOT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    inventory: dict[str, dict] = {}

    for document_dir in sorted(path for path in PAGES_ROOT.iterdir() if path.is_dir()):
        pages = sorted(document_dir.glob("*.png"), key=page_number)
        assert pages, f"no rendered pages for {document_dir.name}"
        sheet_paths: list[str] = []
        for start in range(0, len(pages), PAGES_PER_SHEET):
            batch = pages[start : start + PAGES_PER_SHEET]
            rows = (len(batch) + COLS - 1) // COLS
            canvas = Image.new(
                "RGB",
                (MARGIN * 2 + COLS * THUMB_W, MARGIN * 2 + rows * (THUMB_H + LABEL_H) + LABEL_H),
                "#d9dde3",
            )
            draw = ImageDraw.Draw(canvas)
            title = f"{document_dir.name} | pages {page_number(batch[0])}-{page_number(batch[-1])}"
            draw.text((MARGIN, 8), title, fill="black", font=font)
            for offset, page_path in enumerate(batch):
                with Image.open(page_path) as source:
                    image = source.convert("RGB")
                    image.thumbnail((THUMB_W - 8, THUMB_H - 8), Image.Resampling.LANCZOS)
                col = offset % COLS
                row = offset // COLS
                x = MARGIN + col * THUMB_W + (THUMB_W - image.width) // 2
                y = MARGIN + LABEL_H + row * (THUMB_H + LABEL_H)
                canvas.paste(image, (x, y))
                draw.text(
                    (MARGIN + col * THUMB_W + 4, y + THUMB_H - 18),
                    f"page {page_number(page_path)}",
                    fill="black",
                    font=font,
                )
            output = SHEETS_ROOT / f"{document_dir.name}-{start // PAGES_PER_SHEET + 1:02d}.png"
            canvas.save(output)
            sheet_paths.append(str(output.relative_to(ROOT)).replace("\\", "/"))
        inventory[document_dir.name] = {"pages": len(pages), "contact_sheets": sheet_paths}

    (QA_ROOT / "render-inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"documents": len(inventory), "pages": sum(item["pages"] for item in inventory.values()), "contact_sheets": sum(len(item["contact_sheets"]) for item in inventory.values())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

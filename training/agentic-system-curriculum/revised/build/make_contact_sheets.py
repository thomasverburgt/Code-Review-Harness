from pathlib import Path
from PIL import Image, ImageDraw


SOURCE = Path(__file__).resolve().parents[1] / "qa-final" / "handbook"
OUTPUT = SOURCE / "contact-sheets"
OUTPUT.mkdir(parents=True, exist_ok=True)

pages = sorted(SOURCE.glob("page-*.png"))
for sheet_index in range(0, len(pages), 4):
    group = pages[sheet_index : sheet_index + 4]
    opened = [Image.open(path).convert("RGB") for path in group]
    width = max(image.width for image in opened)
    height = max(image.height for image in opened)
    canvas = Image.new("RGB", (width * 2, height * 2), "#D9DEE5")
    draw = ImageDraw.Draw(canvas)
    for index, (path, image) in enumerate(zip(group, opened)):
        x = (index % 2) * width
        y = (index // 2) * height
        canvas.paste(image, (x, y))
        draw.rectangle((x, y, x + 120, y + 30), fill="#FFFFFF")
        draw.text((x + 8, y + 7), path.stem, fill="#17212B")
    output = OUTPUT / f"sheet-{sheet_index // 4 + 1:02}.png"
    canvas.save(output, optimize=True)
    print(output)

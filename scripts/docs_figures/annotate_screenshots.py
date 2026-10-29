"""Draw the labels on the landing page's screenshots of the launch.

    python scripts/docs_figures/annotate_screenshots.py <raw folder>

<raw folder> holds the raw screenshots named as in SCREENSHOTS, taken by the
browser test tool at 1456 x 828 pixels: GitHub's "Create a new codespace"
page, the two building screens (building-a.png, building-b.png, put side by
side), the trust dialog (trust.png, copied as it is), and the VS Code window
of a new Codespace just after Tutorial 1 opened and at the end of its run.
Writes the figures to
docs/start/figures/. The boxes are in pixels of
those captures; retake a screenshot at the same size if the layout changes,
and move its boxes here.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# raw name -> (output name, crop, boxes). The crop (left, top, right, bottom)
# is applied first and the boxes are in the cropped image; None keeps it all.
# A box is (label, left, top, right, bottom); an empty label draws the box
# alone. Numbered as docs/index.md lists them.
SCREENSHOTS = {
    # Cropped below GitHub's header, which shows the account's avatar.
    "create.png": ("launch-create.png", (0, 66, 1512, 600), [("", 783, 439, 997, 495)]),
    "trust.png": ("launch-trust.png", None, []),
    # The end of the run: the report heading, the results line and the zip in the explorer.
    "done.png": ("launch-done.png", None, []),
    # The explorer, the notebook text, the first step's status line.
    "running.png": ("launch-running.png", None, [("1", 50, 38, 342, 198), ("2", 384, 222, 1442, 378), ("3", 352, 400, 1442, 628)]),
}
COLOR = (227, 66, 52)
WIDTH = 4
RADIUS = 22


def font(size):
    for name in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def annotate(src, out, crop, boxes):
    image = Image.open(src).convert("RGB")
    if crop:
        image = image.crop(crop)
    draw = ImageDraw.Draw(image)
    label_font = font(28)
    for label, left, top, right, bottom in boxes:
        draw.rounded_rectangle((left, top, right, bottom), radius=8, outline=COLOR, width=WIDTH)
        if label:
            # On the box's top-left corner, so it covers border rather than content.
            cx, cy = left, top
            draw.ellipse((cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS), fill=COLOR)
            draw.text((cx, cy), label, fill="white", font=label_font, anchor="mm")
    image.save(out, optimize=True)
    print(f"wrote {out}")


def side_by_side(left, right, out, gap=24):
    """Two captures next to each other on white, for the two building screens."""
    a, b = Image.open(left).convert("RGB"), Image.open(right).convert("RGB")
    height = max(a.height, b.height)
    image = Image.new("RGB", (a.width + gap + b.width, height), "white")
    image.paste(a, (0, 0))
    image.paste(b, (a.width + gap, 0))
    image.save(out, optimize=True)
    print(f"wrote {out}")


def main():
    raw = Path(sys.argv[1])
    figures = Path(__file__).resolve().parents[2] / "docs/start/figures"
    # GitHub's "Setting up your codespace" page, then VS Code connecting.
    if (raw / "building-a.png").exists() and (raw / "building-b.png").exists():
        side_by_side(raw / "building-a.png", raw / "building-b.png", figures / "launch-building.png")
    for name, (out, crop, boxes) in SCREENSHOTS.items():
        if (raw / name).exists():
            annotate(raw / name, figures / out, crop, boxes)
        else:
            print(f"no {raw / name}, skipped")


if __name__ == "__main__":
    main()

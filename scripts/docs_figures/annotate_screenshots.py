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

# (raw name, output name, crop, scale, boxes). The crop (left, top, right,
# bottom) is applied first, then the scale, and the boxes are in the result;
# None keeps the whole capture. A box is (label, left, top, right, bottom); an
# empty label draws the box alone. Numbered as docs/index.md lists them.
SCREENSHOTS = [
    # Cropped below GitHub's header, which shows the account's avatar.
    ("create.png", "launch-create.png", (0, 66, 1512, 600), 1, [("", 783, 439, 997, 495)]),
    # The pages a returning user sees instead: "Resume codespace" (both buttons boxed),
    # then the options page after "Create a new one". Cropped below GitHub's header.
    ("resume.png", "launch-resume.png", (0, 66, 1456, 650), 1, [("1", 505, 516, 648, 552), ("2", 767, 516, 950, 552)]),
    ("options.png", "launch-options.png", (0, 66, 1456, 560), 1, [("", 937, 432, 1093, 468)]),
    ("trust.png", "launch-trust.png", None, 1, []),
    # The browser's clipboard prompt on the first right-click in the explorer (Chrome), taken by hand.
    ("clipboard.png", "clipboard-prompt.png", None, 1, [("", 548, 400, 834, 470)]),
    # The end of the run: the report heading, the results line, the zip in the explorer.
    ("done.png", "launch-done.png", None, 1, [("1", 400, 68, 800, 124), ("2", 406, 488, 1030, 540), ("3", 56, 200, 250, 230)]),
    # The top of the window: the explorer, the notebook's tab and its toolbar, with Run All boxed.
    ("done.png", "run-all.png", (0, 0, 1512, 130), 1, [("", 546, 36, 630, 68)]),
    ("running.png", "launch-running.png", None, 1, [("1", 50, 38, 342, 198), ("2", 384, 222, 1442, 378), ("3", 352, 400, 1442, 628)]),
]
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


def annotate(src, out, crop, scale, boxes):
    image = Image.open(src).convert("RGB")
    if crop:
        image = image.crop(crop)
    if scale != 1:
        image = image.resize((image.width * scale, image.height * scale), Image.LANCZOS)
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
    for name, out, crop, scale, boxes in SCREENSHOTS:
        if (raw / name).exists():
            annotate(raw / name, figures / out, crop, scale, boxes)
        else:
            print(f"no {raw / name}, skipped")


if __name__ == "__main__":
    main()

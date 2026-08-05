#!/usr/bin/env python3
"""Bytter ut foto med grå plassholdere i samme størrelse/format.

Logoer, ikoner og favicons beholdes (KEEP_PATTERNS). Kjøres fra repo-roten.
Originalene røres ikke andre steder enn wp-content/uploads.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
UPLOADS = ROOT / "wp-content" / "uploads"

KEEP_PATTERNS = re.compile(
    r"(logo|Logo|LOGO|Totalkontroll|download|bvnlogo|cropped-|favicon|icon)"
)
EXTS = {".png", ".jpg", ".jpeg", ".webp"}

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"


def make_placeholder(path: Path) -> None:
    with Image.open(path) as im:
        w, h = im.size
        fmt = im.format  # PNG / JPEG / WEBP

    ph = Image.new("RGB", (w, h), (229, 231, 235))  # lys grå
    d = ImageDraw.Draw(ph)
    d.rectangle([0, 0, w - 1, h - 1], outline=(156, 163, 175), width=max(1, w // 400))
    # diagonale hjelpelinjer så flaten tydelig leses som plassholder
    d.line([0, 0, w, h], fill=(209, 213, 219), width=max(1, w // 500))
    d.line([w, 0, 0, h], fill=(209, 213, 219), width=max(1, w // 500))

    label = f"BILDE KOMMER\n{path.stem}\n{w} x {h}"
    size = max(12, min(w, h) // 12)
    try:
        font = ImageFont.truetype(FONT_PATH, size)
    except OSError:
        font = ImageFont.load_default()
    d.multiline_text((w / 2, h / 2), label, fill=(75, 85, 99), font=font,
                     anchor="mm", align="center", spacing=size // 3)

    if fmt == "JPEG":
        ph.save(path, "JPEG", quality=70)
    elif fmt == "WEBP":
        ph.save(path, "WEBP", quality=70)
    else:
        ph.save(path, "PNG", optimize=True)


def main() -> None:
    replaced, kept = 0, 0
    for path in sorted(UPLOADS.rglob("*")):
        if path.suffix.lower() not in EXTS or not path.is_file():
            continue
        if KEEP_PATTERNS.search(path.name):
            kept += 1
            continue
        try:
            make_placeholder(path)
            replaced += 1
        except Exception as e:  # korrupt fil e.l. — meld fra, ikke stopp
            print(f"FEIL {path}: {e}", file=sys.stderr)
    print(f"Byttet ut {replaced} foto, beholdt {kept} logoer/ikoner.")


if __name__ == "__main__":
    main()

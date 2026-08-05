#!/usr/bin/env python3
"""Matcher leverte bilder mot bildeplassene via perseptuell hash og legger dem inn.

For hver bildeplass i wp-content/uploads sammenlignes nedlastet original
(scratch/originaler) mot filene i bildemappen på delingen. Beste treff under
terskelen legges inn: basefil i originalens dimensjoner + alle -WxH-varianter
som finnes i repoet (cover-crop). Umatchede plasser beholder plassholderen.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parent.parent
ORIG = Path(sys.argv[1])       # mappe med nedlastede originaler (flate _-navn)
LEVERT = Path(sys.argv[2])     # bildemappen på delingen
TERSKEL = 40                   # av 256 bits

SKIP = re.compile(r"(logo|totalkontroll|download|bvnlogo|cropped|favicon|icon)", re.I)
VARIANT = re.compile(r"-(\d+)x(\d+)$")


def ahash(path, size=16):
    try:
        im = Image.open(path).convert("L").resize((size, size), Image.LANCZOS)
    except Exception:
        return None
    px = list(im.getdata())
    avg = sum(px) / len(px)
    return sum(1 << i for i, p in enumerate(px) if p > avg)


def dist(a, b):
    return bin(a ^ b).count("1")


levert = [p for p in LEVERT.rglob("*") if p.suffix.lower() in (".png", ".webp", ".jpg", ".jpeg")]
lhash = {p: ahash(p) for p in levert}

slots = []
for p in sorted((REPO / "wp-content" / "uploads").rglob("*")):
    if p.suffix.lower() not in (".png", ".webp", ".jpg") or SKIP.search(p.name):
        continue
    if VARIANT.search(p.stem):
        continue
    slots.append(p)

matched, unmatched_slots = {}, []
for slot in slots:
    okey = str(slot.relative_to(REPO)).replace("/", "_")
    ofile = ORIG / okey
    oh = ahash(ofile) if ofile.exists() else None
    if oh is None:
        unmatched_slots.append((slot, "original mangler"))
        continue
    best, bestd = None, 999
    for p, h in lhash.items():
        if h is None:
            continue
        d = dist(oh, h)
        if d < bestd:
            best, bestd = p, d
    if best is not None and bestd <= TERSKEL:
        matched[slot] = (best, bestd)
    else:
        unmatched_slots.append((slot, f"beste avstand {bestd}"))

used = set()


def save(im, path):
    fmt = {".png": "PNG", ".webp": "WEBP", ".jpg": "JPEG"}[path.suffix.lower()]
    im = im.convert("RGB") if fmt in ("JPEG", "WEBP") else im
    kw = {"quality": 82} if fmt == "WEBP" else {"quality": 85} if fmt == "JPEG" else {"optimize": True}
    im.save(path, fmt, **kw)


for slot, (src, d) in sorted(matched.items()):
    used.add(src)
    okey = str(slot.relative_to(REPO)).replace("/", "_")
    with Image.open(ORIG / okey) as o:
        base_size = o.size
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        base = ImageOps.fit(im, base_size, Image.LANCZOS)
        save(base, slot)
        for var in slot.parent.glob(f"{slot.stem}-*"):
            m = VARIANT.search(var.stem)
            if not m or var.stem[: -len(m.group(0))] != slot.stem:
                continue
            w, h = int(m.group(1)), int(m.group(2))
            save(ImageOps.fit(im, (w, h), Image.LANCZOS), var)
    print(f"INN  {slot.relative_to(REPO)}  <-  {src.relative_to(LEVERT)}  (avstand {d})")

print("\n--- Plasser uten treff (beholder plassholder) ---")
for slot, why in unmatched_slots:
    print(f"MANGLER  {slot.relative_to(REPO)}  ({why})")

print("\n--- Leverte bilder som ikke ble brukt ---")
for p in sorted(set(levert) - used):
    print(f"UBRUKT  {p.relative_to(LEVERT)}")

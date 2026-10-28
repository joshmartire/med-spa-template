#!/usr/bin/env python3
"""Generates the favicons, logo.png (for schema) and the default social-share image from the brand config.
Needs Pillow, fontTools and brotli:  pip install pillow fonttools brotli
Runs automatically from build.py."""
import json, os, io, math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
ACC_HEX, F2_HEX, F3_HEX = CFG.get("accent", "#f4b8c4"), CFG.get("field_2", "#c8d8c3"), CFG.get("field_3", "#6b1f37")
ACC, F2, F3 = hexrgb(ACC_HEX), hexrgb(F2_HEX), hexrgb(F3_HEX)
INK, PAPER = (28, 21, 23), (247, 241, 239)
LOGO_FILE = (CFG.get("logo") or "").strip()
NAME = CFG["business_name"]


def font(name, size):
    f = TTFont(os.path.join(ROOT, "assets", "fonts", name))
    f.flavor = None
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)


def mark(d, cx, cy, s):
    """Peony mark: five round petals around a deep centre (s = overall size)."""
    k = s / 40
    for a in range(-90, 270, 72):
        x, y = cx + 10 * k * math.cos(math.radians(a)), cy + 10 * k * math.sin(math.radians(a))
        d.ellipse([x - 9 * k, y - 9 * k, x + 9 * k, y + 9 * k], fill=ACC)
    d.ellipse([cx - 8 * k, cy - 8 * k, cx + 8 * k, cy + 8 * k], fill=F3)
    d.ellipse([cx - 3.2 * k, cy - 3.2 * k, cx + 3.2 * k, cy + 3.2 * k], fill=PAPER)


# favicon.svg
petals = "".join(f'<circle cx="{20 + 10 * math.cos(math.radians(a)):.1f}" cy="{20 + 10 * math.sin(math.radians(a)):.1f}" r="9" fill="{ACC_HEX}"/>' for a in range(-90, 270, 72))
open(os.path.join(IMG, "favicon.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="9" fill="#1c1517"/>'
    f'<g transform="translate(2 2) scale(.9)">{petals}<circle cx="20" cy="20" r="8" fill="{F3_HEX}"/><circle cx="20" cy="20" r="3.2" fill="#f7f1ef"/></g></svg>')

for size, fname in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    S = size * 4
    im = Image.new("RGB", (S, S), INK); d = ImageDraw.Draw(im)
    mark(d, S / 2, S / 2, S * 0.86)
    im.resize((size, size), Image.LANCZOS).save(os.path.join(IMG, fname))

# logo.png (schema): the client's logo when supplied, otherwise mark + name on porcelain
if LOGO_FILE:
    src = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    src = src.crop(src.getchannel("A").getbbox() or (0, 0, src.width, src.height))
    if src.width > 1200:
        src = src.resize((1200, round(src.height * 1200 / src.width)), Image.LANCZOS)
    src.save(os.path.join(IMG, "logo.png"))
else:
    f = font("b800.woff2", 120)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = tmp.textlength(NAME.lower(), font=f)
    im = Image.new("RGB", (int(w) + 360, 300), PAPER); d = ImageDraw.Draw(im)
    mark(d, 150, 150, 230)
    d.text((290, 150), NAME.lower(), font=f, fill=INK, anchor="lm")
    im.save(os.path.join(IMG, "logo.png"))

# og-default.png 1200x630: a flat poster. Accent field, the claim in heavy lower case, the peony bloom on the deep field.
W, H = 1200, 630
im = Image.new("RGB", (W, H), ACC); d = ImageDraw.Draw(im)
d.rounded_rectangle([760, 40, 1160, 590], 40, fill=F3)
cx, cy = 960, 300
for r, n, pr, col, st in ((120, 9, 72, ACC, 10), (70, 8, 56, F3, 30), (0, 1, 66, ACC, 0), (36, 6, 30, F3, 0)):
    for i in range(n):
        t = math.radians(st + i * 360 / n)
        x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        d.ellipse([x - pr, y - pr, x + pr, y + pr], fill=col)
d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=PAPER)
claim = (CFG.get("hero_claim") or NAME).lower()
words = claim.split(" ")
lines, cur = [], ""
big = font("b800.woff2", 118)
for wd in words:
    test = (cur + " " + wd).strip()
    if d.textlength(test, font=big) > 660 and cur:
        lines.append(cur); cur = wd
    else:
        cur = test
lines.append(cur)
y = 80
for ln in lines[:3]:
    d.text((60, y), ln, font=big, fill=INK); y += 112
d.text((62, 470), NAME, font=font("b800.woff2", 44), fill=INK)
d.text((62, 530), f"Injectables · Skin · Laser · {CFG['region_label']}", font=font("b500.woff2", 30), fill=INK)
im.save(os.path.join(IMG, "og-default.png"), optimize=True)
print("Images written to assets/img/")

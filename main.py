#!/usr/bin/env python3
"""Sum up 21 November 2026 world news in one image.

Deterministic, offline: no network, no random, no timestamps in the image.
Run: python3 main.py  -> writes /output/entry.png when /output exists,
otherwise ./output/entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

STORIES = [
    ("1", "KYIV / POLAND", "Russia fires 400+ drones and 110 missiles at Ukraine; missiles land in Poland",
     "At least 8 killed in Kyiv. Bridges and rail hit. Warsaw calls it a deliberate provocation."),
    ("2", "MARKETS", "AI sell-off pushes S&P 500 into correction",
     "S&P 500 -3.7%. Nasdaq -5.28%. Nikkei -5.06%. Tech rout wipes out Nasdaq's 2026 gains."),
    ("3", "THE HAGUE", "World Court: Myanmar committed genocide against the Rohingya",
     "The International Court of Justice finds Myanmar responsible for genocide, a first for a state."),
    ("4", "HEALTH", "Pancreatic cancer pill shows major progress in trial",
     "Daraxonrasib made tumours undetectable on scans in 1 in 12 patients."),
    ("5", "BRUSSELS", "UK and EU sign biggest post-Brexit deals",
     "Three agreements on food exports, carbon markets and youth mobility."),
    ("6", "ANTALYA", "COP31 climate talks run past deadline over fossil fuels",
     "Nearly 200 nations fail to agree. Summit goes into overtime."),
]

def main():
    img = Image.new("RGB", (W, H), (248, 246, 240))
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 150], fill=(12, 28, 58))
    d.rectangle([0, 150, W, 158], fill=(200, 40, 40))
    d.text((48, 28), "THE WORLD IN ONE DAY", font=font(BOLD, 52), fill=(255, 255, 255))
    d.text((48, 96), "Saturday 21 November 2026  |  Six stories that defined the day", font=font(REG, 26), fill=(200, 210, 225))
    # Stories: two columns x three rows
    x0, y0 = 48, 190
    cw, ch, gx, gy = 452, 250, 32, 24
    for i, (num, kicker, head, body) in enumerate(STORIES):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        d.rectangle([x, y, x + cw, y + ch], fill=(255, 255, 255), outline=(180, 180, 175), width=2)
        d.rectangle([x, y, x + 64, y + 64], fill=(200, 40, 40))
        d.text((x + 20, y + 12), num, font=font(BOLD, 36), fill=(255, 255, 255))
        d.text((x + 80, y + 16), kicker, font=font(BOLD, 20), fill=(200, 40, 40))
        lines = wrap(d, head, font(BOLD, 26), cw - 32)
        yy = y + 76
        for ln in lines[:3]:
            d.text((x + 16, yy), ln, font=font(BOLD, 26), fill=(12, 28, 58))
            yy += 32
        blines = wrap(d, body, font(REG, 21), cw - 32)
        for ln in blines[:3]:
            d.text((x + 16, yy + 6), ln, font=font(REG, 21), fill=(60, 60, 60))
            yy += 27
    # Footer
    d.text((48, 986), "Sources: AP, NYT, France 24, CBS, El Pais  |  One image, 21 Nov 2026", font=font(REG, 20), fill=(90, 90, 90))
    outdir = "/output" if os.path.isdir("/output") else "output"
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out)

if __name__ == "__main__":
    main()

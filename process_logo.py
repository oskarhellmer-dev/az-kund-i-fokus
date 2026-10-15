#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bearbetar kundens logga: tar bort vit bakgrund, delar ikon/text, gör favicon, samplar färger."""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/clawd/.hermes/profiles/az-kund-i-fokus/image_cache/img_a7617526fd7a.jpg"
OUT = os.path.join(ROOT, "bilder")
ASSETS = os.path.join(ROOT, "assets")

def white_to_alpha(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    mn = a.min(axis=2)
    alpha = 1.0 - mn / 255.0                      # 0 = vit bakgrund
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb = (a - (1.0 - alpha)[:, :, None] * 255.0) / np.where(alpha[:, :, None] == 0, 1, alpha[:, :, None])
    rgb = np.clip(rgb, 0, 255)
    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")

im = Image.open(SRC).convert("RGB")
arr = np.asarray(im.convert("L"))
ys, xs = np.where(arr < 240)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
pad = 14
crop = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))
logo = white_to_alpha(crop)
logo.save(f"{OUT}/logo.png")
print("logo.png", logo.size)

# ikon och text möts utan tomt band -> splitta vid rad-minimum i mittenregionen
alpha = np.asarray(logo)[:, :, 3]
rows = (alpha > 40).sum(axis=1)
lo, hi = int(logo.height * 0.68), int(logo.height * 0.90)
split = lo + int(np.argmin(rows[lo:hi]))
print("split vid y", split, "av", logo.height, "| radvärde", int(rows[split]))
mark = logo.crop((0, 0, logo.width, split))
textpart = logo.crop((0, split, logo.width, logo.height))
# trimma mark
ma = np.asarray(mark)[:, :, 3]
my, mx = np.where(ma > 25)
mark = mark.crop((mx.min(), my.min(), mx.max() + 1, my.max() + 1))
mark.save(f"{OUT}/logo-mark.png")
print("logo-mark.png", mark.size)
textpart.save(f"{OUT}/logo-text.png")
print("logo-text.png", textpart.size)

# favicon: kvadratisk mark på genomskinlig botten
side = max(mark.size) + 40
fav = Image.new("RGBA", (side, side), (0, 0, 0, 0))
fav.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2), mark)
fav.resize((512, 512), Image.LANCZOS).save(f"{ASSETS}/favicon.png")
print("favicon.png 512x512")

# sampla varumärkesfärger (blå + grön)
rgb = np.asarray(logo).astype(np.int16)[:, :, :3]
al = np.asarray(logo)[:, :, 3]
m = al > 200
r, g, b = rgb[:, :, 0][m], rgb[:, :, 1][m], rgb[:, :, 2][m]
blue = (b > r + 30) & (b > g)
green = (g > r + 30) & (g > b)
def hexof(rr, gg, bb):
    return "#%02X%02X%02X" % (int(rr), int(gg), int(bb))
print("BLÅ  medel:", hexof(r[blue].mean(), g[blue].mean(), b[blue].mean()))
print("GRÖN medel:", hexof(r[green].mean(), g[green].mean(), b[green].mean()))

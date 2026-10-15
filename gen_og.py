#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OG-bild (varumärkt, 1200x630) + bearbetar Adrians riktiga foton till om-oss."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "bilder")
CACHE = "/home/clawd/.hermes/profiles/az-kund-i-fokus/image_cache"

def font(sz, bold=False):
    cands = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []) + [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
    for c in cands:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, sz)
            except: pass
    return ImageFont.load_default()

# ---- OG-bild ----
def make_og():
    base = Image.open(f"{OUT}/hero-1200.webp").convert("RGB")
    # beskära till 1200x630 (band från mitten)
    w,h = base.size
    target = 1200/630
    if w/h > target:
        nw=int(h*target); base=base.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else:
        nh=int(w/target); y=int((h-nh)*0.35); base=base.crop((0,y,w,y+nh))
    base = base.resize((1200,630), Image.LANCZOS)
    # mörk gradient nedtill för läsbarhet
    grad = Image.new("L",(1,630))
    for y in range(630):
        grad.putpixel((0,y), int(210*max(0,(y-150)/480)))
    grad = grad.resize((1200,630))
    dark = Image.new("RGB",(1200,630),(6,40,35))
    base = Image.composite(dark, base, grad.filter(ImageFilter.GaussianBlur(2)))
    d = ImageDraw.Draw(base)
    # riktiga loggan på vit rundad platta
    logo = Image.open(f"{OUT}/logo.png").convert("RGBA")
    lw = 320; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    cx, cy = 56, 52
    chip = Image.new("RGBA", (logo.width + 40, logo.height + 32), (255, 255, 255, 235))
    chip.putalpha(255)
    chip = chip.resize(chip.size)
    base.paste(chip, (cx, cy), chip)
    base.paste(logo, (cx + 20, cy + 16), logo)
    # text
    f1 = font(64, True); f2 = font(30)
    d = ImageDraw.Draw(base)
    d.text((56, 480), "A.Z & Kund i Fokus", font=f1, fill="white", anchor="lm")
    d.text((58, 540), "Städfirma i Dalsland  ·  RUT-avdrag  ·  kundifokus.se", font=f2, fill=(200,222,242), anchor="lm")
    base.save(f"{OUT}/og-kundifokus.jpg","JPEG",quality=88,optimize=True,progressive=True)
    print("OK  og-kundifokus.jpg")

# ---- Riktiga foton -> om-oss ----
def process_real(src, name, aspect=4/3):
    im = Image.open(src).convert("RGB")
    w,h = im.size
    if w/h > aspect:
        nw=int(h*aspect); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else:
        nh=int(w/aspect); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    base = 1000
    im = im.resize((base,int(base/aspect)), Image.LANCZOS)
    for tw in (1000,600,400):
        im.resize((tw,int(tw/aspect)), Image.LANCZOS).save(f"{OUT}/{name}-{tw}.webp","WEBP",quality=82,method=6)
    im.resize((800,int(800/aspect)), Image.LANCZOS).save(f"{OUT}/{name}.jpg","JPEG",quality=84,optimize=True,progressive=True)
    print(f"OK  {name}")

if __name__ == "__main__":
    make_og()
    process_real(f"{CACHE}/img_6ae22633eebe.jpg", "om-oss-1")
    process_real(f"{CACHE}/img_4cbd7a5754cf.jpg", "om-oss-2")

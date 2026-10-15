#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genererar sajtbilder via fal.ai Seedream v4 -> responsiva WebP + JPG.
Kör:  set -a; . /home/clawd/.hermes/fal.env; set +a; python3 gen_imgs.py
"""
import os, sys, json, urllib.request
from io import BytesIO
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder")
MODEL = "fal-ai/bytedance/seedream/v4/text-to-image"
KEY = os.environ.get("FAL_KEY")

BASE = ("candid unstyled documentary interior photograph, real everyday Swedish home, "
        "soft natural daylight from a side window, muted natural colors, shot on 35mm film, "
        "gentle film grain, slightly imperfect and homely, no people, no faces, no text, "
        "no watermark, no logos, no brand marks")

# name, prompt, aspect(w/h), widths, base_w
JOBS = [
 ("hero", "a bright tidy Scandinavian living room just cleaned, warm natural wood floor shining, a simple linen sofa with cushions, a green plant by the window, sunlight streaming across the floor, calm airy and inviting", 4/5, [1200,800], 1200),
 ("hemstadning", "a small bright modern bathroom freshly cleaned, white glossy tiles, glass shower, neatly folded white towels on a rail, soft daylight, spotless and fresh", 8/5, [1200,800,400], 1200),
 ("flyttstadning", "an empty bright apartment room after move-out cleaning, bare clean floorboards, two cardboard moving boxes by the wall, sunlight through a bare window, absolutely spotless", 8/5, [1200,800,400], 1200),
 ("kontorsstadning", "a small modern office freshly cleaned, tidy desks with a closed laptop, ergonomic chairs, potted plants, bright morning light, calm and organised", 8/5, [1200,800,400], 1200),
 ("fritidshus-airbnb", "a cosy Swedish summer cottage bedroom prepared for guests, crisp white linens on the bed, neatly folded guest towels, light wooden walls, soft daylight through a small window", 8/5, [1200,800,400], 1200),
 ("byggstad-storstadning", "a newly renovated empty room after final cleaning, fresh light paint on the walls, spotless clean floor, a wooden step ladder and folded drop cloths neatly in one corner, bright daylight", 8/5, [1200,800,400], 1200),
]

def gen(prompt, w, h):
    body = json.dumps({"prompt": prompt + ", " + BASE, "image_size": {"width": w, "height": h}, "num_images": 1}).encode()
    req = urllib.request.Request(f"https://fal.run/{MODEL}", data=body,
        headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=240))
    return r["images"][0]["url"]

def crop_resize(im, aspect, base_w):
    w, h = im.size
    if w/h > aspect:
        nw = int(h*aspect); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
    else:
        nh = int(w/aspect); y=(h-nh)//2; im=im.crop((0,y,w,y+nh))
    H = int(base_w/aspect)
    return im.resize((base_w, H), Image.LANCZOS)

def emit(name, im, widths, base_w, aspect):
    for tw in widths:
        th = int(tw/aspect)
        im.resize((tw,th), Image.LANCZOS).save(f"{OUT}/{name}-{tw}.webp","WEBP",quality=82,method=6)
    # jpg fallback = mellersta/största bredd, 16:10 -> 800x500 style
    jw = widths[-1]
    im.resize((jw,int(jw/aspect)), Image.LANCZOS).save(f"{OUT}/{name}.jpg","JPEG",quality=84,optimize=True,progressive=True)

def main():
    if not KEY:
        print("FAL_KEY saknas"); sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    for name, prompt, aspect, widths, bw in JOBS:
        try:
            gw, gh = 1280, int(1280/aspect)
            url = gen(prompt, gw, gh)
            raw = urllib.request.urlopen(url, timeout=180).read()
            im = Image.open(BytesIO(raw)).convert("RGB")
            im = crop_resize(im, aspect, bw)
            emit(name, im, widths, bw, aspect)
            print(f"OK  {name}  ({im.size[0]}x{im.size[1]})")
        except Exception as e:
            print(f"ERR {name}: {e}")
    print("Klart.")

if __name__ == "__main__":
    main()

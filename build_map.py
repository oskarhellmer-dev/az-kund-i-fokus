#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger statiska kartbilder (OpenStreetMap-plattor, ingen tredjeparts-JS/cookies).
- bilder/karta-omrade.webp : serviceområdet med ortsnamn (Åmål/Bengtsfors/Säffle/Mellerud/Ed)
- bilder/karta-adress.webp  : Fengersfors på gatunivå ("hitta hit")
Kör: python3 build_map.py
"""
import os, math, time, urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "bilder")
UA = "kundifokus-site/1.0 (+https://kundifokus.se; contact adrianna.zawada.kundifokus@gmail.com)"

TOWNS = {
    "Fengersfors": (58.9949, 12.4640),
    "Åmål":        (58.9838, 12.6127),
    "Bengtsfors":  (59.0327, 12.2191),
    "Säffle":      (59.1167, 12.8500),
    "Mellerud":    (58.7167, 12.4667),
    "Ed":          (58.9126, 11.9340),
    "Årjäng":      (59.3892, 12.1328),
    "Grums":       (59.3531, 13.1060),
    "Arvika":      (59.6546, 12.5896),
    "Karlstad":    (59.3793, 13.5036),
    "Forshaga":    (59.5286, 13.4820),
    "Vänersborg":  (58.3807, 12.3234),
    "Trollhättan": (58.2837, 12.2887),
    "Uddevalla":   (58.3497, 11.9412),
}

def deg2num(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y

def num2deg(x, y, z):
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon

def font(sz, bold=True):
    c = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []
    c += ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in c:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def fetch(z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            return Image.open(BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB")
        except Exception as e:
            if attempt == 2: raise
            time.sleep(1.5)

def build(center_lat, center_lon, z, w, h, markers, path, marker_main=None,
          radius_km=None, radius_center=None):
    cx, cy = deg2num(center_lat, center_lon, z)
    px, py = cx * 256, cy * 256
    left, top = px - w / 2, py - h / 2
    tx0, ty0 = int(left // 256), int(top // 256)
    tx1, ty1 = int((left + w) // 256), int((top + h) // 256)
    canvas = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), (240, 240, 240))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            canvas.paste(fetch(z, tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
            time.sleep(0.05)
    img = canvas.crop((int(left - tx0 * 256), int(top - ty0 * 256),
                       int(left - tx0 * 256) + w, int(top - ty0 * 256) + h))
    d = ImageDraw.Draw(img, "RGBA")
    fx = lambda lat, lon: (deg2num(lat, lon, z)[0] * 256 - left, deg2num(lat, lon, z)[1] * 256 - top)
    # radie (nåbarhetscirkel)
    if radius_km and radius_center:
        mpp = 156543.03392 * math.cos(math.radians(center_lat)) / (2 ** z)
        rpx = radius_km * 1000.0 / mpp
        RX, RY = fx(*radius_center)
        d.ellipse([RX - rpx, RY - rpx, RX + rpx, RY + rpx],
                  outline=(11, 95, 180, 150), width=4)
    for name, (lat, lon) in markers.items():
        X, Y = fx(lat, lon)
        if not (-40 < X < w + 40 and -40 < Y < h + 40):
            continue
        main = (name == marker_main)
        r = 9 if main else 6
        d.ellipse([X - r, Y - r, X + r, Y + r], fill=(11, 95, 180) if main else (88, 174, 1),
                  outline="white", width=3)
        f = font(26 if main else 22)
        bb = d.textbbox((0, 0), name, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.rectangle([X + 12, Y - th - 8, X + 16 + tw, Y + 6], fill=(255, 255, 255, 255))
        d.text((X + 14 - bb[0], Y - th - 6 - bb[1]), name, font=f, fill=(20, 32, 30))
    # attribution (krävs av OSM)
    f = font(15, False)
    txt = "© OpenStreetMap contributors"
    bb = d.textbbox((0, 0), txt, font=f)
    d.rectangle([w - (bb[2] - bb[0]) - 14, h - 24, w, h], fill=(255, 255, 255))
    d.text((w - (bb[2] - bb[0]) - 8, h - 21), txt, font=f, fill=(80, 90, 88))
    for tw_ in (1200, 800, 400):
        img.resize((tw_, int(h * tw_ / w)), Image.LANCZOS).save(f"{OUT}/{path}-{tw_}.webp", "WEBP", quality=82, method=6)
    img.resize((800, int(h * 800 / w)), Image.LANCZOS).save(f"{OUT}/{path}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    print(f"OK {path} {w}x{h}")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # områdeskarta (visar serviceområdet + radie på ca 10 mil)
    build(58.9949, 12.4640, 8, 900, 780, TOWNS, "karta-omrade",
          marker_main="Fengersfors", radius_km=100, radius_center=(58.9949, 12.4640))
    # adresskarta (Fengersfors på gatunivå)
    build(58.9949, 12.4640, 15, 1200, 560, {"Fengersfors": (58.9949, 12.4640)}, "karta-adress", marker_main="Fengersfors")
    print("Klart.")

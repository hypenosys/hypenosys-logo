#!/usr/bin/env python3
"""Regenerate Hypenosys brand files from the approved, compressed SVG sources."""
import base64
import gzip
import io
import json
from pathlib import Path

import cairosvg
from PIL import Image

root = Path(__file__).resolve().parent.parent
payload = (root / "source/brand-v2.svg.json.gz.b64").read_text().strip()
sources = json.loads(gzip.decompress(base64.b64decode(payload)))
for name, svg in sources.items():
    (root / "source" / name).write_text(svg, encoding="utf-8")

(root / "logo_simple.svg").write_text(sources["hypenosys_wordmark.svg"], encoding="utf-8")
(root / "logo_icon.svg").write_text(sources["hypenosys_icon.svg"], encoding="utf-8")
(root / "favicon.svg").write_text(sources["hypenosys_favicon.svg"], encoding="utf-8")

def raster(name, size):
    raw = cairosvg.svg2png(bytestring=sources[name].encode(), output_width=size, output_height=size if name != "hypenosys_wordmark.svg" else size // 2)
    return Image.open(io.BytesIO(raw)).convert("RGBA")

def save(name, source, size):
    raster(source, size).save(root / name)

save("favicon-16x16.png", "hypenosys_favicon.svg", 16)
save("favicon-32x32.png", "hypenosys_favicon.svg", 32)
save("android-chrome-192x192.png", "hypenosys_favicon.svg", 192)
save("android-chrome-512x512.png", "hypenosys_favicon.svg", 512)
save("apple-touch-icon.png", "hypenosys_icon.svg", 180)
(root / "previews").mkdir(exist_ok=True)
save("previews/wordmark-1024.png", "hypenosys_wordmark.svg", 1024)
save("previews/icon-512.png", "hypenosys_icon.svg", 512)
save("previews/avatar-1024.png", "hypenosys_icon.svg", 1024)

icons = [raster("hypenosys_favicon.svg", n) for n in (16, 32, 48, 64)]
icons[-1].save(root / "favicon.ico", format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64)])
for file in ["favicon.ico","favicon-16x16.png","favicon-32x32.png","android-chrome-192x192.png","android-chrome-512x512.png","apple-touch-icon.png"]:
    with Image.open(root / file) as im:
        im.verify()
print("Validated brand assets")

#!/usr/bin/env python3
"""Generate WebP assets and patch homepage HTML/CSS for PageSpeed."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
CSS = HOME / "woa-home.css"

# Max width by usage hint (path substring)
RULES: list[tuple[str, int, int]] = [
    ("custom-tattoos-las-vegas-epic-snake", 1200, 78),  # hero texture + gallery
    ("professional-tattoo-artist-work-of-art", 900, 80),
    ("img_0279", 800, 82),
    ("img_0280", 800, 82),
    ("img_0131", 800, 82),
    ("artist-portfolio", 640, 82),
    ("masterpiece-wall", 640, 82),
    ("master-body-piercer", 640, 82),
    ("best-tattoo-las-vegas-custom-sleeve", 1600, 80),  # LCP hero
    ("vibrant-color-sunflower", 1600, 80),
    ("black-and-grey-artistry-dynamic-snake", 900, 82),
    ("realism-tattoos-grim-reaper", 600, 82),
    ("flying-dove", 600, 82),
    ("luxury-jewelry", 800, 82),
    ("floral-and-roman", 600, 82),
    ("butterfly", 600, 82),
    ("nightmare-before", 600, 82),
]
DEFAULT_MAX_W = 800
DEFAULT_Q = 82
TEXTURE_MAX_W = 480
TEXTURE_Q = 60


def rule_for(path: str) -> tuple[int, int]:
    low = path.lower()
    for needle, w, q in RULES:
        if needle in low:
            return w, q
    return DEFAULT_MAX_W, DEFAULT_Q


def resize_and_webp(src: Path, dest: Path, max_w: int, quality: int) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB") if im.mode in ("RGBA", "P") else im
        w, h = im.size
        if w > max_w:
            nh = max(1, int(h * max_w / w))
            im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
            w, h = im.size
        if im.mode == "RGBA":
            im.save(dest.with_suffix(".webp"), "WEBP", quality=quality, method=6)
        else:
            im.save(dest.with_suffix(".webp"), "WEBP", quality=quality, method=6)
    return w, h


def collect_src_paths(html: str) -> list[str]:
    return sorted(set(re.findall(r'src="(/[^"?]+\.(?:png|jpe?g))"', html, re.I)))


def webp_path_for(url_path: str) -> Path:
    return (ROOT / url_path.lstrip("/")).with_suffix(".webp")


def patch_html_images(html: str, dims: dict[str, tuple[int, int]]) -> str:
    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        src = m.group(1)
        webp = src.rsplit(".", 1)[0] + ".webp"
        w, h = dims.get(src, (0, 0))
        if 'type="image/webp"' in tag:
            return tag
        # Build picture wrapper
        inner = tag.replace(f'src="{src}"', f'src="{src}"')
        if w and h and "width=" not in tag:
            inner = inner.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
        picture = (
            f'<picture><source srcset="{webp}" type="image/webp"/>'
            f'{inner}</picture>'
        )
        return picture

    return re.sub(
        r'<img\s[^>]*src="(/[^"]+\.(?:png|jpe?g))"[^>]*>',
        repl,
        html,
        flags=re.I,
    )


def main() -> None:
    html = CODE.read_text(encoding="utf-8")
    paths = collect_src_paths(html)
    dims: dict[str, tuple[int, int]] = {}
    made = 0

    for url in paths:
        src = ROOT / url.lstrip("/")
        if not src.is_file() or src.stat().st_size < 100:
            print(f"skip missing/empty: {url}")
            continue
        max_w, q = rule_for(url)
        dest = webp_path_for(url)
        if dest.is_file() and dest.stat().st_mtime >= src.stat().st_mtime:
            with Image.open(dest) as im:
                dims[url] = im.size
            continue
        w, h = resize_and_webp(src, dest, max_w, q)
        dims[url] = (w, h)
        kb = dest.stat().st_size // 1024
        print(f"webp {kb:4} KiB  {dest.relative_to(ROOT)}  ({w}x{h})")
        made += 1

    # Tiny texture for CSS background (was 10MB PNG)
    snake = HOME / "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png"
    tex = HOME / "custom-tattoos-las-vegas-epic-snake-texture.webp"
    if snake.is_file():
        resize_and_webp(snake, tex, TEXTURE_MAX_W, TEXTURE_Q)
        print(f"texture webp {tex.stat().st_size // 1024} KiB")

    html2 = patch_html_images(html, dims)
    if html2 != html:
        CODE.write_text(html2, encoding="utf-8")
        print("updated code.html with <picture> + dimensions")

    css = CSS.read_text(encoding="utf-8")
    old_bg = "/home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png"
    new_bg = "/home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-texture.webp"
    if old_bg in css:
        CSS.write_text(css.replace(old_bg, new_bg), encoding="utf-8")
        print("updated woa-home.css texture background")

    print(f"done ({made} new webp files)")


if __name__ == "__main__":
    main()

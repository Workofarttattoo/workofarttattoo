#!/usr/bin/env python3
"""Bake upright hero carousel images (no EXIF sideways) + sync HTML dimensions."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
HOME_HTML = HOME / "code.html"
ROOT_HTML = ROOT / "code.html"

# Keep in sync with set_hero_carousel.py
CAROUSEL_STEMS = (
    "home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas",
    "home_work_of_art_tattoo_piercing/client-portfolio/skull-hourglass-forearm-realism-fresh-las-vegas",
    "home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skeleton-reaper-hand-realism-las-vegas",
    "home_work_of_art_tattoo_piercing/client-portfolio/black-grey-eagle-shoulder-realism-las-vegas",
)

TARGET_W = 1200
TARGET_H = 1600


def upright_portrait(im: Image.Image) -> Image.Image:
    """Bake EXIF only — do not auto-rotate landscape tattoo masters."""
    return ImageOps.exif_transpose(im)


def fit_portrait_card(im: Image.Image) -> Image.Image:
    im = upright_portrait(im)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    return ImageOps.fit(
        im,
        (TARGET_W, TARGET_H),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.45),
    )


def normalize_carousel_file(path: Path) -> tuple[int, int] | None:
    if not path.is_file():
        return None
    out = fit_portrait_card(Image.open(path))
    out.save(path, "PNG", optimize=True)
    webp = path.with_suffix(".webp")
    out.save(webp, "WEBP", quality=84, method=6)
    return out.size


def patch_html_dims(html: str, rel_src: str, w: int, h: int) -> str:
    esc = re.escape(rel_src)

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        tag = re.sub(r'\s*width="[^"]*"', "", tag)
        tag = re.sub(r'\s*height="[^"]*"', "", tag)
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    return re.sub(
        rf'<img\s[^>]*\ssrc="/{esc}"[^>]*>',
        repl,
        html,
        flags=re.I,
    )


def resolve_png(stem: str) -> Path | None:
    for base in (HOME, ROOT):
        candidate = base / f"{stem}.png"
        if candidate.is_file():
            return candidate
    alt = ROOT / stem
    if alt.is_file():
        return alt
    return None


def rel_src(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    dims: dict[str, tuple[int, int]] = {}
    for stem in CAROUSEL_STEMS:
        png = resolve_png(stem)
        if not png:
            print(f"[skip] missing {stem}.png")
            continue
        size = normalize_carousel_file(png)
        if size:
            rel = rel_src(png)
            dims[rel] = size
            print(f"[carousel] {rel} → {size[0]}×{size[1]}")

    for path in (HOME_HTML, ROOT_HTML):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        for rel, (w, h) in dims.items():
            html = patch_html_dims(html, rel, w, h)
        path.write_text(html, encoding="utf-8")
        print(f"[html] {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

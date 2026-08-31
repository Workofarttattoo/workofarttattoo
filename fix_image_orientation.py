#!/usr/bin/env python3
"""Bake EXIF orientation and repair Stitch page-screenshot assets used as photos.

Some exports are full-page PNG captures (~300×1600). In portrait cards they read as
sideways or broken. This script:
  1. Applies ImageOps.exif_transpose so camera orientation is baked in.
  2. Detects page-screenshot aspect ratios and crops the hero portrait band.
  3. Regenerates sibling .webp files and updates width/height in static HTML.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# Page capture: narrow width, very tall (Stitch mobile export).
SCREENSHOT_MAX_W = 600
SCREENSHOT_MIN_ASPECT = 3.0
# Full-page capture exported at high width but extreme height (e.g. 2560×14000).
TALL_PAGE_MIN_HEIGHT = 5000
TALL_PAGE_MIN_ASPECT = 4.0

# Hero band on Stitch artist/guide pages (portrait column, upper half).
CROP_TOP_FRAC = 0.38
CROP_LEFT_FRAC = 0.35
CARD_ASPECT = 3 / 4
CARD_MAX_W = 800

# Never crop CSS background textures, wide hero masters, or artist portraits.
SKIP_CROP_STEMS = ("texture", "katelyn-cole-master", "no-duplicates")


def is_page_screenshot(width: int, height: int) -> bool:
    if width <= 0 or height <= 0:
        return False
    if width < SCREENSHOT_MAX_W and (height / width) >= SCREENSHOT_MIN_ASPECT:
        return True
    return height >= TALL_PAGE_MIN_HEIGHT and (height / width) >= TALL_PAGE_MIN_ASPECT


def crop_hero_portrait(im: Image.Image) -> Image.Image:
    w, h = im.size
    box = (int(w * CROP_LEFT_FRAC), 0, w, int(h * CROP_TOP_FRAC))
    cropped = im.crop(box)
    cw, ch = cropped.size
    if cw < 2 or ch < 2:
        return im
    cur = cw / ch
    if cur > CARD_ASPECT:
        new_w = max(1, int(ch * CARD_ASPECT))
        x0 = (cw - new_w) // 2
        cropped = cropped.crop((x0, 0, x0 + new_w, ch))
    else:
        new_h = max(1, int(cw / CARD_ASPECT))
        y0 = (ch - new_h) // 2
        cropped = cropped.crop((0, y0, cw, y0 + new_h))
    out_w = CARD_MAX_W
    out_h = max(1, int(out_w / CARD_ASPECT))
    return cropped.resize((out_w, out_h), Image.Resampling.LANCZOS)


def normalize_image(path: Path, *, dry_run: bool = False) -> tuple[bool, str]:
    with Image.open(path) as raw:
        im = ImageOps.exif_transpose(raw)
        changed = im.size != raw.size
        action = "exif"

        if is_page_screenshot(*im.size) and not any(s in path.stem for s in SKIP_CROP_STEMS):
            fixed = crop_hero_portrait(im)
            if fixed.size != im.size:
                im = fixed
                action = "crop"
                changed = True

        if not changed:
            return False, "ok"

        if dry_run:
            return True, action

        if path.suffix.lower() == ".webp":
            im.save(path, "WEBP", quality=82, method=6)
        elif path.suffix.lower() in {".jpg", ".jpeg"}:
            im.save(path, "JPEG", quality=88, optimize=True)
        else:
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
            im.save(path, "PNG", optimize=True)
        return True, action


def save_webp_companion(path: Path, *, dry_run: bool = False) -> bool:
    webp = path.with_suffix(".webp")
    if path.suffix.lower() == ".webp":
        return False
    if dry_run:
        return webp.exists() or path.exists()
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "P"):
            im.save(webp, "WEBP", quality=82, method=6)
        else:
            rgb = im.convert("RGB")
            rgb.save(webp, "WEBP", quality=82, method=6)
    return True


def iter_images(folder: Path) -> list[Path]:
    out: list[Path] = []
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMAGE_EXTS:
            continue
        if any(part.startswith(".") for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def patch_html_dimensions(html_path: Path, dims: dict[str, tuple[int, int]], *, dry_run: bool) -> bool:
    text = html_path.read_text(encoding="utf-8")
    orig = text

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        src = m.group(1)
        size = dims.get(src)
        if not size:
            return tag
        w, h = size
        tag = re.sub(r'\s*width="[^"]*"', "", tag)
        tag = re.sub(r'\s*height="[^"]*"', "", tag)
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    text = re.sub(
        r'<img\s[^>]*\ssrc="(/[^"?#]+\.(?:png|jpe?g|webp))"[^>]*>',
        repl,
        text,
        flags=re.I,
    )
    if text == orig:
        return False
    if not dry_run:
        html_path.write_text(text, encoding="utf-8")
    return True


def build_dims_map() -> dict[str, tuple[int, int]]:
    dims: dict[str, tuple[int, int]] = {}
    for p in iter_images(ROOT):
        rel = "/" + p.relative_to(ROOT).as_posix()
        try:
            with Image.open(p) as im:
                dims[rel] = im.size
        except OSError:
            continue
    return dims


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write files")
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Only refresh width/height attributes in code.html files",
    )
    args = parser.parse_args()

    if not args.html_only:
        fixed = 0
        for path in iter_images(ROOT):
            if path.suffix.lower() == ".webp" and path.with_suffix(".png").is_file():
                continue
            try:
                changed, action = normalize_image(path, dry_run=args.dry_run)
            except OSError as exc:
                print(f"[skip] {path.relative_to(ROOT)}: {exc}")
                continue
            if not changed:
                continue
            fixed += 1
            label = "would fix" if args.dry_run else "fixed"
            print(f"[{label}:{action}] {path.relative_to(ROOT)}")
            if not args.dry_run and path.suffix.lower() != ".webp":
                save_webp_companion(path)

        print(f"images {label if args.dry_run else 'updated'}: {fixed}")

    dims = build_dims_map()
    html_count = 0
    for html in ROOT.rglob("code.html"):
        if patch_html_dimensions(html, dims, dry_run=args.dry_run):
            html_count += 1
            print(f"[html] {html.relative_to(ROOT)}")
    for html in ROOT.glob("artists_build/*.html"):
        if patch_html_dimensions(html, dims, dry_run=args.dry_run):
            html_count += 1
            print(f"[html] {html.relative_to(ROOT)}")
    for html in (ROOT / "code.html",):
        if html.is_file() and patch_html_dimensions(html, dims, dry_run=args.dry_run):
            html_count += 1
            print(f"[html] {html.relative_to(ROOT)}")

    print(f"html files touched: {html_count}")


if __name__ == "__main__":
    main()

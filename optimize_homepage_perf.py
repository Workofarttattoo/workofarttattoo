#!/usr/bin/env python3
"""Generate WebP assets and patch homepage HTML/CSS for PageSpeed."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"
CSS = HOME / "woa-home.css"

RULES: list[tuple[str, int, int]] = [
    ("work-of-art-studio-banner", 1200, 78),
    ("custom-tattoos-las-vegas-epic-snake", 1200, 78),
    ("client-portfolio", 800, 78),
    ("professional-tattoo-artist-work-of-art", 900, 80),
    ("artist-portfolio", 640, 82),
    ("masterpiece-wall", 640, 82),
    ("professional-piercer", 640, 82),
]
DEFAULT_MAX_W = 800
DEFAULT_Q = 78
TEXTURE_MAX_W = 480
TEXTURE_Q = 55
THUMB_MAX_W = 400
THUMB_Q = 72
HERO_MOBILE_W = 800
HERO_DESKTOP_W = 1200


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
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")
        w, h = im.size
        if w > max_w:
            nh = max(1, int(h * max_w / w))
            im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
            w, h = im.size
        im.save(dest, "WEBP", quality=quality, method=6)
    return w, h


def variant_path(src: Path, suffix: str) -> Path:
    return src.with_name(f"{src.stem}{suffix}.webp")


def ensure_webp_variants(src: Path, url: str) -> dict[str, str]:
    """Return url-path -> variant path map for srcset (400w thumb + main webp)."""
    if not src.is_file():
        return {}
    max_w, q = rule_for(url)
    main = src.with_suffix(".webp")
    if not main.is_file() or main.stat().st_mtime < src.stat().st_mtime:
        resize_and_webp(src, main, max_w, q)
        print(f"webp {main.stat().st_size // 1024:4} KiB  {main.relative_to(ROOT)}")

    variants: dict[str, str] = {max_w: f"/{main.relative_to(ROOT).as_posix()}"}

    thumb = variant_path(src, "-400")
    if not thumb.is_file() or thumb.stat().st_mtime < src.stat().st_mtime:
        resize_and_webp(src, thumb, THUMB_MAX_W, THUMB_Q)
        print(f"thumb {thumb.stat().st_size // 1024:4} KiB  {thumb.relative_to(ROOT)}")
    variants[THUMB_MAX_W] = f"/{thumb.relative_to(ROOT).as_posix()}"
    return variants


def ensure_hero_banner_variants() -> dict[int, str]:
    src = HOME / "work-of-art-studio-banner-las-vegas.png"
    if not src.is_file():
        return {}
    out: dict[int, str] = {}
    for width, suffix, quality in (
        (HERO_MOBILE_W, "-800", 76),
        (HERO_DESKTOP_W, "-1200", 78),
    ):
        dest = variant_path(src, suffix)
        if not dest.is_file() or dest.stat().st_mtime < src.stat().st_mtime:
            resize_and_webp(src, dest, width, quality)
            print(f"hero {dest.stat().st_size // 1024:4} KiB  {dest.relative_to(ROOT)}")
        out[width] = f"/{dest.relative_to(ROOT).as_posix()}"
    full = src.with_suffix(".webp")
    if not full.is_file() or full.stat().st_mtime < src.stat().st_mtime:
        resize_and_webp(src, full, 1600, 78)
    out[1600] = f"/{full.relative_to(ROOT).as_posix()}"
    return out


def collect_src_paths(html: str) -> list[str]:
    return sorted(set(re.findall(r'src="(/[^"?]+\.(?:png|jpe?g))"', html, re.I)))


def srcset_for(variants: dict[int, str]) -> str:
    return ", ".join(f"{url} {width}w" for width, url in sorted(variants.items()))


def patch_picture_srcsets(html: str, srcsets: dict[str, dict[int, str]], sizes: dict[str, str]) -> str:
    for src, variants in srcsets.items():
        if not variants or THUMB_MAX_W not in variants:
            continue
        webp = variants[max(variants)]
        thumb = variants[THUMB_MAX_W]
        srcset = f"{thumb} {THUMB_MAX_W}w, {webp} {max(variants)}w"
        size_attr = sizes.get(src, "(max-width: 768px) 50vw, 350px")
        old = f'<source srcset="{webp}" type="image/webp"/>'
        new = f'<source srcset="{srcset}" sizes="{size_attr}" type="image/webp"/>'
        if old in html:
            html = html.replace(old, new)
    return html


def patch_hero_banner(html: str, hero_variants: dict[int, str]) -> str:
    if not hero_variants:
        return html
    srcset = srcset_for(hero_variants)
    banner_webp = "/home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.webp"
    banner_800 = "/home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas-800.webp"
    old_src = (
        'src="/home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.png"'
    )
    html = html.replace(old_src, f'src="{banner_webp}"', 1)
    old = (
        '<source srcset="/home_work_of_art_tattoo_piercing/work-of-art-studio-banner-las-vegas.webp" '
        'type="image/webp"/>'
    )
    new = f'<source srcset="{srcset}" sizes="100vw" type="image/webp"/>'
    if old in html:
        return html.replace(old, new, 1)
    # Already patched — refresh srcset if hero variants changed
    html = re.sub(
        r'<source srcset="/home_work_of_art_tattoo_piercing/work-of-art-studio-banner[^"]+" sizes="100vw" type="image/webp"/>',
        new,
        html,
        count=1,
    )
    if banner_800 in html or banner_webp in html:
        return html
    return html


def main() -> None:
    html = CODE.read_text(encoding="utf-8")
    paths = collect_src_paths(html)
    srcsets: dict[str, dict[int, str]] = {}
    sizes: dict[str, str] = {}

    for url in paths:
        src = ROOT / url.lstrip("/")
        if not src.is_file() or src.stat().st_size < 100:
            print(f"skip missing/empty: {url}")
            continue
        if "work-of-art-studio-banner" in url:
            continue
        variants = ensure_webp_variants(src, url)
        if variants:
            srcsets[url] = variants
            if "client-portfolio" in url or "cover-up-tattoos" in url or "healed" in url:
                sizes[url] = "(max-width: 768px) 50vw, 350px"
            elif "las-vegas-tattoo-healing-guide" in url or "healed_tattoo" in url or "studio_gallery" in url:
                sizes[url] = "(max-width: 768px) 33vw, 301px"

    snake = HOME / "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png"
    tex = HOME / "custom-tattoos-las-vegas-epic-snake-texture.webp"
    if snake.is_file():
        resize_and_webp(snake, tex, TEXTURE_MAX_W, TEXTURE_Q)
        print(f"texture webp {tex.stat().st_size // 1024} KiB")

    hero_variants = ensure_hero_banner_variants()
    html2 = patch_hero_banner(html, hero_variants)
    html2 = patch_picture_srcsets(html2, srcsets, sizes)

    if html2 != html:
        CODE.write_text(html2, encoding="utf-8")
        ROOT_CODE.write_text(html2, encoding="utf-8")
        print("updated homepage HTML with responsive srcset")

    css = CSS.read_text(encoding="utf-8")
    old_bg = "/home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-black-and-grey-realism.png"
    new_bg = "/home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-texture.webp"
    if old_bg in css:
        CSS.write_text(css.replace(old_bg, new_bg), encoding="utf-8")
        print("updated woa-home.css texture background")

    print("done")


if __name__ == "__main__":
    main()

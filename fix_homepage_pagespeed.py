#!/usr/bin/env python3
"""Homepage PageSpeed: static Tailwind, doctype, defer icon font, drop duplicate CSS."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
TARGETS = [HOME / "code.html", ROOT / "code.html"]

TAILWIND_CDN_RE = re.compile(
    r'<script src="https://cdn\.tailwindcss\.com[^"]*"></script>\s*',
    re.I,
)
TAILWIND_CONFIG_RE = re.compile(
    r'<script id="tailwind-config">[\s\S]*?</script>\s*',
    re.I,
)
TAILWIND_LINK = (
    '<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>'
)
DUPLICATE_SPARKLE_LINK = (
    '<link href="/home_work_of_art_tattoo_piercing/woa-sparkle.css" rel="stylesheet"/>'
)
MEDUSA_TEXTURE_PNG = (
    "/home_work_of_art_tattoo_piercing/client-portfolio/"
    "black-grey-medusa-snakehair-realism-las-vegas.png"
)
SNAKE_TEXTURE_WEBP = (
    "/home_work_of_art_tattoo_piercing/custom-tattoos-las-vegas-epic-snake-texture.webp"
)
MATERIAL_SYMBOLS_RE = re.compile(
    r'<link href="(https://fonts\.googleapis\.com/css2\?family=Material\+Symbols\+Outlined[^"]*)" rel="stylesheet"/>',
    re.I,
)
INK_TEXTURE_INLINE_RE = re.compile(
    r"(\.ink-texture\s*\{[^}]*background-image:\s*)url\([^)]+\)",
    re.I,
)


def async_stylesheet_link(href: str) -> str:
    return (
        f'<link rel="preload" as="style" href="{href}" '
        f'onload="this.onload=null;this.rel=\'stylesheet\'"/>'
        f'<noscript><link href="{href}" rel="stylesheet"/></noscript>'
    )


def patch_html(html: str) -> tuple[str, bool]:
    changed = False
    out = html

    if not out.lstrip().lower().startswith("<!doctype html>"):
        out = "<!DOCTYPE html>\n" + out.lstrip()
        changed = True

    if TAILWIND_CDN_RE.search(out):
        out = TAILWIND_CDN_RE.sub("", out, count=1)
        changed = True

    if TAILWIND_CONFIG_RE.search(out):
        out = TAILWIND_CONFIG_RE.sub("", out, count=1)
        changed = True

    if TAILWIND_LINK not in out:
        anchor = '<meta charset="utf-8"/>'
        if anchor in out:
            out = out.replace(anchor, anchor + "\n" + TAILWIND_LINK, 1)
            changed = True

    if "fonts.googleapis.com" in out and 'rel="preconnect" href="https://fonts.googleapis.com"' not in out:
        preconnect = (
            '<link rel="preconnect" href="https://fonts.googleapis.com"/>'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>'
        )
        font_link = out.find('<link href="https://fonts.googleapis.com/css2?')
        if font_link >= 0:
            out = out[:font_link] + preconnect + out[font_link:]
            changed = True

    if DUPLICATE_SPARKLE_LINK in out and "woa-home.css" in out:
        out = out.replace(DUPLICATE_SPARKLE_LINK, "")
        changed = True

    if MEDUSA_TEXTURE_PNG in out:
        out = out.replace(MEDUSA_TEXTURE_PNG, SNAKE_TEXTURE_WEBP)
        changed = True

    if INK_TEXTURE_INLINE_RE.search(out):
        out = INK_TEXTURE_INLINE_RE.sub(
            rf"\1url({SNAKE_TEXTURE_WEBP})",
            out,
            count=1,
        )
        changed = True

    def defer_symbols(m: re.Match[str]) -> str:
        return async_stylesheet_link(m.group(1))

    new_out, n = MATERIAL_SYMBOLS_RE.subn(defer_symbols, out, count=1)
    if n:
        out = new_out
        changed = True

    # Stats row used h4 under h2 — use styled paragraphs for heading order.
    for old, new in (
        ('<h4 class="text-secondary font-headline-md">2</h4>', '<p class="text-secondary font-headline-md m-0" role="presentation">2</p>'),
        ('<h4 class="text-secondary font-headline-md">7+</h4>', '<p class="text-secondary font-headline-md m-0" role="presentation">7+</p>'),
    ):
        if old in out:
            out = out.replace(old, new, 1)
            changed = True

    return out, changed


def main() -> int:
    n = 0
    for path in TARGETS:
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated, ok = patch_html(raw)
        if ok:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            n += 1
        else:
            print(f"[skip] {path.relative_to(ROOT)}")
    print(f"done — updated {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

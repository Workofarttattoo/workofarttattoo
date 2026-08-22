#!/usr/bin/env python3
"""Link woa-typography.css + Google fonts on static HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TYPO_CSS = "/home_work_of_art_tattoo_piercing/woa-typography.css"
FONT_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Cinzel:wght@500;600;700"
    "&family=UnifrakturMaguntia"
    "&family=Hanken+Grotesk:wght@400;500;600"
    "&display=swap"
)
SKIP_PARTS = frozenset(
    {
        "skipped_upload_build",
        "artists_raw",
        "reviews_vault_100_verified_masterpieces",
        ".git",
        "__pycache__",
    }
)


def patch_html(html: str) -> tuple[str, bool]:
    changed = False
    if TYPO_CSS not in html:
        block = (
            f'<link href="{FONT_HREF}" rel="stylesheet"/>\n'
            f'<link href="{TYPO_CSS}" rel="stylesheet"/>'
        )
        if '<link href="/home_work_of_art_tattoo_piercing/woa-home.css"' in html:
            html = html.replace(
                '<link href="/home_work_of_art_tattoo_piercing/woa-home.css" rel="stylesheet"/>',
                '<link href="/home_work_of_art_tattoo_piercing/woa-home.css" rel="stylesheet"/>\n'
                + block,
                1,
            )
            changed = True
        elif '<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css"' in html:
            html = html.replace(
                '<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>',
                '<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>\n'
                + block,
                1,
            )
            changed = True
        elif "family=Playfair+Display" in html:
            html = re.sub(
                r'<link href="https://fonts\.googleapis\.com/css2\?'
                r'family=Playfair\+Display[^"]*"[^/]*/>',
                block,
                html,
                count=1,
            )
            changed = TYPO_CSS in html

    if 'class="woa-hero-copy' in html and "woa-text-on-photo" not in html:
        html = html.replace('class="woa-hero-copy ', 'class="woa-hero-copy woa-text-on-photo ', 1)
        changed = True

    # Drop legacy Playfair-only link when typography bundle is present
    if TYPO_CSS in html:
        html = re.sub(
            r'<link href="https://fonts\.googleapis\.com/css2\?'
            r'family=Playfair\+Display[^"]*"[^/]*/>\s*',
            "",
            html,
            count=1,
        )

    return html, changed


def iter_html_pages() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(ROOT.glob("*/code.html")):
        if path.parent.name in SKIP_PARTS:
            continue
        paths.append(path)
    for path in sorted((ROOT / "artists_build").glob("*.html")):
        paths.append(path)
    root_home = ROOT / "code.html"
    if root_home.is_file():
        paths.append(root_home)
    return paths


def main() -> int:
    n = 0
    for path in iter_html_pages():
        raw = path.read_text(encoding="utf-8")
        new_html, ok = patch_html(raw)
        if ok:
            path.write_text(new_html, encoding="utf-8")
            print(f"typography {path.relative_to(ROOT)}")
            n += 1
    print(f"done — updated {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

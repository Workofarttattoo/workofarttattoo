#!/usr/bin/env python3
"""Hero: interview top-right on desktop; carousel zoomed out (full tattoo visible)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
HERO_PANEL_RE = re.compile(
    r'<div class="woa-hero-video-panel[^"]*"[^>]*>\s*'
    r"<!-- WOA_HERO_LEAD_START -->[\s\S]*?<!-- WOA_HERO_LEAD_END -->\s*"
    r"</div>\s*",
    re.MULTILINE,
)


def patch_hero(html: str) -> str:
    # Carousel: show full artwork (not cropped)
    hero = re.search(r'id="hero"[\s\S]*?id="hero-carousel"[\s\S]*?</div>\s*</div>', html)
    if hero:
        block = hero.group(0)
        block = block.replace("object-cover", "object-contain")
        html = html[: hero.start()] + block + html[hero.end() :]

    # Float interview top-right (outside the background grid)
    panel_match = HERO_PANEL_RE.search(html)
    if panel_match and "woa-hero-interview-topright" not in html:
        panel_block = panel_match.group(0)
        html = HERO_PANEL_RE.sub("", html, count=1)
        lead = re.search(
            r"<!-- WOA_HERO_LEAD_START -->[\s\S]*?<!-- WOA_HERO_LEAD_END -->",
            panel_block,
        )
        if lead:
            floated = (
                '<div class="woa-hero-interview-topright woa-hero-video-panel relative z-[25] '
                'border border-outline-variant/40 bg-background/95 backdrop-blur-md shadow-2xl">\n'
                f"{lead.group(0)}\n</div>\n"
            )
            html = html.replace(
                '</div>\n</div>\n<div class="woa-hero-copy',
                "</div>\n</div>\n" + floated + '<div class="woa-hero-copy',
                1,
            )

    # Single-column media grid (carousel full width; interview is absolute)
    html = html.replace(
        'class="woa-hero-media-grid absolute inset-0 z-0 grid grid-cols-1 lg:grid-cols-[1fr_minmax(300px,38vw)] grid-rows-[minmax(44vh,50vh)_1fr] lg:grid-rows-1"',
        'class="woa-hero-media-grid absolute inset-0 z-0 grid grid-cols-1 grid-rows-1"',
        1,
    )

    if 'woa-hero-copy woa-text-on-photo' not in html:
        html = html.replace('class="woa-hero-copy ', 'class="woa-hero-copy woa-text-on-photo ', 1)

    # Discount / offer promo
    html = html.replace(
        'class="w-full shadow-2xl border border-outline-variant/20 transition-transform duration-500 group-hover:scale-[1.02]" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/pink-rose',
        'class="w-full max-h-[min(70vh,520px)] object-contain object-center mx-auto bg-[#0a0a0a] shadow-2xl border border-outline-variant/20 transition-transform duration-500 group-hover:scale-[1.02]" loading="lazy" src="/home_work_of_art_tattoo_piercing/client-portfolio/pink-rose',
        1,
    )

    return html


def main() -> int:
    if not CODE.is_file():
        raise SystemExit(f"Missing {CODE}")
    html = CODE.read_text(encoding="utf-8")
    CODE.write_text(patch_hero(html), encoding="utf-8")
    root_copy = ROOT / "code.html"
    if root_copy.is_file():
        root_copy.write_text(CODE.read_text(encoding="utf-8"), encoding="utf-8")
    print("[ok] hero: interview top-right, carousel object-contain, panther slide")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

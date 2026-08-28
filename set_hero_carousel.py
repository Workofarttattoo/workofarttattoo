#!/usr/bin/env python3
"""Rebuild homepage hero carousel slides (source of truth for order + assets)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"

from import_landing_portfolio_images import SHOWCASE_STEMS

CAROUSEL_SLIDES: list[tuple[str, str, bool]] = [
    (
        f"home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[0]}",
        "Norse Odin and Viking ship black and grey sleeve — Work of Art Tattoo Las Vegas",
        True,
    ),
    (
        f"home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[1]}",
        "Black and grey warrior profile shoulder realism — Work of Art Tattoo Las Vegas",
        False,
    ),
    (
        f"home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[2]}",
        "Veiled woman statue black and grey realism — Work of Art Tattoo Las Vegas",
        False,
    ),
    (
        f"home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[3]}",
        "All-seeing eye triangle forearm realism — Work of Art Tattoo Las Vegas",
        False,
    ),
]


def slide_html(path_stem: str, alt: str, *, active: bool, eager: bool) -> str:
    base = f"/{path_stem}"
    active_cls = " is-active" if active else ""
    load = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    return f"""<div class="carousel-item relative min-w-full h-full woa-hero-slide{active_cls}">
<picture><source srcset="{base}.webp" type="image/webp"/><img alt="{alt}" class="w-full h-full object-contain object-center" decoding="async" height="1600" loading="{load}"{fetch} src="{base}.png" width="1200"/></picture>
</div>"""


def build_track() -> str:
    parts = [
        slide_html(stem, alt, active=(i == 0), eager=(i == 0))
        for i, (stem, alt, _e) in enumerate(CAROUSEL_SLIDES)
    ]
    return "\n".join(parts)


def patch_html(html: str) -> str:
    track = build_track()
    html = re.sub(
        r'(<div class="carousel-track[^"]*"[^>]*id="hero-carousel"[^>]*>)([\s\S]*?)(</div>\s*<div class="absolute inset-0 bg-gradient-to-r)',
        rf"\1\n{track}\n\3",
        html,
        count=1,
    )
    # Preload first carousel slide (lion thigh)
    first_webp = f"/{CAROUSEL_SLIDES[0][0]}.webp"
    html = re.sub(
        r'<link as="image"[^>]*rel="preload"[^>]*/>',
        f'<link as="image" fetchpriority="high" href="{first_webp}" rel="preload" type="image/webp"/>',
        html,
        count=1,
    )
    return html


def main() -> int:
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        path.write_text(patch_html(path.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"[carousel] rebuilt {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

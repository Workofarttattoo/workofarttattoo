#!/usr/bin/env python3
"""Homepage: scroll-depth B&G ink plates + tighter section rhythm."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"

INK_MARKER_START = "<!-- WOA_INK_FIELD_START -->"
INK_MARKER_END = "<!-- WOA_INK_FIELD_END -->"

# Highly detailed evil black & grey work — spread down the page
INK_PLATES: list[tuple[str, str, str]] = [
    (
        "woa-ink-plate--lion-thigh",
        "18%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-realism-thigh-client-photo-las-vegas.webp",
    ),
    (
        "woa-ink-plate--hourglass",
        "32%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/skull-hourglass-forearm-realism-fresh-las-vegas.webp",
    ),
    (
        "woa-ink-plate--eagle",
        "46%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-eagle-shoulder-realism-las-vegas.webp",
    ),
    (
        "woa-ink-plate--skull-candle",
        "58%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas.webp",
    ),
    (
        "woa-ink-plate--ravens",
        "82%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skeleton-reaper-hand-realism-las-vegas.webp",
    ),
    (
        "woa-ink-plate--thorns",
        "93%",
        "/cover_up_tattoos_las_vegas_master_authority_guide/healed-realism-seraphim-eye-wings-tattoo.webp",
    ),
]


def _plate_exists(url: str) -> bool:
    rel = url.lstrip("/")
    return (ROOT / rel).is_file()


def build_ink_field_html() -> str:
    plates: list[str] = []
    for cls, top, url in INK_PLATES:
        if not _plate_exists(url):
            continue
        plates.append(
            f'<div class="woa-ink-plate {cls}" style="--ink-top:{top};--ink-url:url(\'{url}\');"></div>'
        )
    inner = "\n".join(plates)
    return f"""{INK_MARKER_START}
<div class="woa-ink-field" aria-hidden="true">
{inner}
</div>
{INK_MARKER_END}"""


def patch_html(html: str) -> str:
    block = build_ink_field_html()
    if INK_MARKER_START in html:
        html = re.sub(
            rf"{re.escape(INK_MARKER_START)}[\s\S]*?{re.escape(INK_MARKER_END)}",
            block,
            html,
            count=1,
        )
    elif '<main class="relative z-10">' in html:
        html = html.replace(
            '<main class="relative z-10">',
            f'<main class="relative z-10 woa-home-main">\n{block}',
            1,
        )
    else:
        return html

    html = html.replace(
        'class="relative min-h-screen flex flex-col',
        'class="relative min-h-[88vh] flex flex-col',
        1,
    )
    html = html.replace(
        'class="py-24 px-margin-mobile',
        'class="py-12 md:py-16 px-margin-mobile',
        1,
    )
    return html


def main() -> int:
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        html = patch_html(path.read_text(encoding="utf-8"))
        path.write_text(html, encoding="utf-8")
        print(f"[atmosphere] {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

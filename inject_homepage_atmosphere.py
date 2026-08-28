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

from import_landing_portfolio_images import SHOWCASE_STEMS

INK_PLATES: list[tuple[str, str, str]] = [
    (
        "woa-ink-plate--odin-sleeve",
        "18%",
        f"/home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[0]}.webp",
    ),
    (
        "woa-ink-plate--warrior",
        "32%",
        f"/home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[1]}.webp",
    ),
    (
        "woa-ink-plate--veiled",
        "46%",
        f"/home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[2]}.webp",
    ),
    (
        "woa-ink-plate--eye",
        "58%",
        f"/home_work_of_art_tattoo_piercing/client-portfolio/{SHOWCASE_STEMS[3]}.webp",
    ),
    (
        "woa-ink-plate--angel",
        "82%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/falling-angel-black-grey-realism-las-vegas.webp",
    ),
    (
        "woa-ink-plate--eagle-memorial",
        "93%",
        "/home_work_of_art_tattoo_piercing/client-portfolio/eagle-memorial-color-leg-tattoo-las-vegas.webp",
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

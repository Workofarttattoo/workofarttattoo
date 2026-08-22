#!/usr/bin/env python3
"""Embed matching studio video clips into guide pages."""

from __future__ import annotations

import re
from pathlib import Path

from woa_guide_videos import GUIDE_VIDEOS, video_section

ROOT = Path(__file__).resolve().parent
MARKER = 'data-woa-guide-video="1"'


def strip_video(html_text: str) -> str:
    return re.sub(
        rf'<section[^>]*{re.escape(MARKER)}[^>]*>.*?</section>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )


def inject(html_text: str, slug: str) -> str:
    block = video_section(slug)
    if not block:
        return html_text
    html_text = strip_video(html_text)
    for pattern in (
        r'(<section[^>]*\bid="faq"[^>]*>)',
        r'(<section[^>]*\bid="book"[^>]*>)',
    ):
        match = re.search(pattern, html_text)
        if match:
            pos = match.start()
            return html_text[:pos] + block + "\n" + html_text[pos:]
    if "</main>" in html_text:
        return html_text.replace("</main>", block + "\n</main>", 1)
    return html_text


def main() -> int:
    n = 0
    for slug in GUIDE_VIDEOS:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            print(f"[skip] {slug}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject(raw, slug)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {slug}")
            n += 1
    print(f"Done: video embeds on {n} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

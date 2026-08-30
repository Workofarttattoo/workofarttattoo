#!/usr/bin/env python3
"""Apply real Instagram and Facebook URLs; drop placeholder TikTok links."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import (
    HREF_FACEBOOK_STUDIO,
    HREF_INSTAGRAM_JOSHUA,
    HREF_INSTAGRAM_JOSHUA_HANDLE,
    HREF_INSTAGRAM_KATELYN,
    HREF_INSTAGRAM_KATELYN_HANDLE,
    HREF_INSTAGRAM_STUDIO,
    HREF_INSTAGRAM_TERALYN,
    HREF_INSTAGRAM_TERALYN_HANDLE,
    ROOT_A,
)
from woa_external_attribution import with_preset

ROOT = ROOT_A
SKIP_DIRS = frozenset({"artists_raw", ".git", "__pycache__", "node_modules"})
SKIP_FILES = frozenset({"skipped_pages_clipboard.html"})

EXTERNAL = ' rel="noopener noreferrer" target="_blank"'

SOCIAL_UTM: dict[str, str] = {
    HREF_INSTAGRAM_STUDIO: with_preset(HREF_INSTAGRAM_STUDIO, "instagram_studio"),
    HREF_INSTAGRAM_JOSHUA: with_preset(HREF_INSTAGRAM_JOSHUA, "instagram_joshua"),
    HREF_INSTAGRAM_KATELYN: with_preset(HREF_INSTAGRAM_KATELYN, "instagram_katelyn"),
    HREF_INSTAGRAM_TERALYN: with_preset(HREF_INSTAGRAM_TERALYN, "instagram_teralyn"),
    HREF_FACEBOOK_STUDIO: with_preset(HREF_FACEBOOK_STUDIO, "facebook_studio"),
}

REPLACEMENTS: list[tuple[str, str]] = [
    (
        'href="#">Instagram</a>',
        f'href="{SOCIAL_UTM[HREF_INSTAGRAM_STUDIO]}"{EXTERNAL}>Instagram</a>',
    ),
    (
        'href="#">Instagram Portfolio</a>',
        f'href="{SOCIAL_UTM[HREF_INSTAGRAM_STUDIO]}"{EXTERNAL}>Instagram @{HREF_INSTAGRAM_JOSHUA_HANDLE}</a>',
    ),
    (
        'href="https://instagram.com" target="_blank">Follow on Instagram</a>',
        f'href="{SOCIAL_UTM[HREF_INSTAGRAM_STUDIO]}"{EXTERNAL}>Follow on Instagram</a>',
    ),
    (
        'href="#">Facebook</a>',
        f'href="{SOCIAL_UTM[HREF_FACEBOOK_STUDIO]}"{EXTERNAL}>Facebook</a>',
    ),
]

TIKTOK_LINE = re.compile(
    r'\s*<a[^>]*href="#"[^>]*>TikTok</a>\s*\n?',
    re.IGNORECASE,
)

CONTACT_US = (
    'href="#">Contact Us</a>',
    f'href="tel:+17252241240">(725) 224-1240</a>',
)


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES or "skipped_upload_build" in path.parts:
            continue
        out.append(path)
    return out


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    text = re.sub(
        r'href="https://www\.instagram\.com/stabislifee/"([^>]*)>Instagram\s*@stabislifee\s*\(Joshua\)</a>',
        f'href="{SOCIAL_UTM[HREF_INSTAGRAM_JOSHUA]}"\\1>Instagram @{HREF_INSTAGRAM_JOSHUA_HANDLE} (Joshua)</a>',
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'href="https://www\.instagram\.com/stabislifee/"([^>]*)>Instagram\s*\(Joshua\)</a>',
        f'href="{SOCIAL_UTM[HREF_INSTAGRAM_JOSHUA]}"\\1>Instagram (Joshua)</a>',
        text,
        flags=re.IGNORECASE,
    )

    if path.name == "joshua-cole.html":
        text = text.replace(
            'href="#">Instagram Portfolio</a>',
            f'href="{SOCIAL_UTM[HREF_INSTAGRAM_JOSHUA]}"{EXTERNAL}>Instagram @{HREF_INSTAGRAM_JOSHUA_HANDLE}</a>',
        )

    for old, new in REPLACEMENTS:
        if path.name == "joshua-cole.html" and "Instagram Portfolio" in old:
            continue
        if path.name == "katelyn-cole.html" and "Instagram</a>" in old and "Portfolio" not in old:
            text = text.replace(
                'href="#">Instagram</a>',
                f'href="{SOCIAL_UTM[HREF_INSTAGRAM_KATELYN]}"{EXTERNAL}>Instagram @{HREF_INSTAGRAM_KATELYN_HANDLE}</a>',
            )
            continue
        text = text.replace(old, new)

    for base_url, utm_url in SOCIAL_UTM.items():
        text = text.replace(f'href="{base_url}"', f'href="{utm_url}"')

    text = TIKTOK_LINE.sub("\n", text)
    text = text.replace(CONTACT_US[0], CONTACT_US[1])

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = [p for p in iter_html_files() if process(p)]
    for p in changed:
        print(p.relative_to(ROOT))
    print(f"---\nUpdated {len(changed)} files")


if __name__ == "__main__":
    main()

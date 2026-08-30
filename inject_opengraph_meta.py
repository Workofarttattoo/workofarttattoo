#!/usr/bin/env python3
"""Inject canonical, Open Graph, and Twitter meta tags into static HTML pages."""

from __future__ import annotations

import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://workofarttattoo.com"
DEFAULT_OG_IMAGE = (
    f"{SITE}/best_fine_line_tattoos_in_vegas_ultimate_authority_guide/"
    "best-tattoo-las-vegas-custom-sleeve-by-master-artist.webp"
)
ARTIST_OG = (
    f"{SITE}/joshua_cole_masterpiece_wall_consistently_unique/"
    "joshua-cole-masterpiece-wall-consistently-unique-las-vegas.webp"
)

HTML_FILES: list[Path] = []
for path in ROOT.rglob("code.html"):
    if "skipped" in path.parts or "node_modules" in path.parts:
        continue
    HTML_FILES.append(path)
for path in (ROOT / "artists_build").glob("*.html"):
    HTML_FILES.append(path)


def canonical_for(path: Path) -> str:
    if path.parent.name == "artists_build":
        return f"{SITE}/artists/{path.stem}/"
    if path.name == "code.html":
        slug = path.parent.name
        if slug.startswith("home_work_of_art"):
            return f"{SITE}/"
        return f"{SITE}/{slug}/"
    return SITE + "/"


def og_image_for(path: Path) -> str:
    if path.parent.name == "artists_build" and path.stem == "joshua-cole":
        return ARTIST_OG
    return DEFAULT_OG_IMAGE


def parse_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html, re.I)
    return m.group(1).strip() if m else "Work of Art Tattoo & Piercing | Las Vegas"


def parse_description(html: str) -> str:
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']',
            html,
            re.I,
        )
    if m:
        return m.group(1).strip()
    return "Las Vegas tattoo shop and piercing studio on E. Tropicana — Work of Art."


def build_tags(title: str, desc: str, url: str, image: str) -> str:
    t, d = escape(unescape(title)), escape(unescape(desc))
    return f"""<link rel="canonical" href="{url}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{t}"/>
<meta property="og:description" content="{d}"/>
<meta property="og:image" content="{image}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:site_name" content="Work of Art Tattoo &amp; Piercing"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{t}"/>
<meta name="twitter:description" content="{d}"/>
<meta name="twitter:image" content="{image}"/>
"""


def inject(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if 'property="og:title"' in html or "property='og:title'" in html:
        return False
    title = parse_title(html)
    desc = parse_description(html)
    url = canonical_for(path)
    image = og_image_for(path)
    block = build_tags(title, desc, url, image)
    m = re.search(
        r'(<meta[^>]+name=["\']description["\'][^>]*>)',
        html,
        re.I,
    )
    if m:
        html = html[: m.end()] + "\n" + block + html[m.end() :]
    else:
        m2 = re.search(r"(<title>[^<]+</title>)", html, re.I)
        if not m2:
            return False
        html = html[: m2.end()] + "\n" + block + html[m2.end() :]
    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for path in sorted(HTML_FILES):
        if inject(path):
            print(f"og: {path.relative_to(ROOT)}")
            n += 1
    print(f"Updated {n} file(s)")


if __name__ == "__main__":
    main()

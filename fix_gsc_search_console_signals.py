#!/usr/bin/env python3
"""Search Console follow-up fixes for reel links and local piercing intent."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REEL_SCHEMA_MARKER = 'data-woa-reel-list-schema="1"'
LOCAL_INTENT_MARKER = "WOA_LOCAL_PIERCING_INTENT_START"
SITE = "https://www.workofarttattoo.com"
IMAGE_LICENSE_URL = f"{SITE}/image-license/"
IMAGE_CREDIT_TEXT = "Work of Art Tattoo & Piercing"
IMAGE_COPYRIGHT_NOTICE = "Copyright Work of Art Tattoo & Piercing. All rights reserved."

REELS = [
    ("Joshua Cole - professional studio interview", "https://www.instagram.com/p/DDiX988y0tR/"),
    ("Client interview - Las Vegas studio", "https://www.instagram.com/p/DTZRprYgQ3G/"),
    ("Joshua Cole - painting in the studio", "https://www.instagram.com/reel/C8vPwacP1du/"),
    ("Joshua Cole - seminars and advanced training", "https://www.instagram.com/reel/Cpp18lXgU3P/"),
    ("Minor ear piercing - how Katelyn does it", "https://www.instagram.com/reel/Cs1_Oc4gEx1/"),
    ("Katelyn Cole - piercing in the studio", "https://www.instagram.com/reel/C78fY1quCVF/"),
    ("Jewelry and placement - studio reel", "https://www.instagram.com/reel/C0nNwUkRHz6/"),
    ("Ear curation - studio reel", "https://www.instagram.com/reel/C4fOsY7OSTq/"),
    ("Piercing session - studio reel", "https://www.instagram.com/reel/C3GjVCdLUQ9/"),
]

REEL_ITEMLIST_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "@id": f"{SITE}/studio_videos/#instagram-reel-library",
    "name": "Work of Art Tattoo & Piercing Instagram reel library",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": idx,
            "name": name,
            "url": url,
        }
        for idx, (name, url) in enumerate(REELS, start=1)
    ],
}

FEATURED_EMBED = """<div class="woa-ig-cell woa-featured-embed" data-woa-featured-video-embed="1">
<iframe title="Joshua Cole professional studio interview on Instagram" src="https://www.instagram.com/reel/DDiX988y0tR/embed/" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" allowfullscreen></iframe>
</div>"""

LOCAL_PIERCING_BLOCK = f"""<!-- {LOCAL_INTENT_MARKER} -->
<section class="py-10 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" id="piercing-hours">
<div class="max-w-4xl mx-auto space-y-4 text-center">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Piercing appointments daily</span>
<h2 class="font-headline-md text-on-surface text-2xl">Piercing shop hours in Las Vegas: 12pm - 12am daily</h2>
<p class="font-body-md text-on-surface-variant">Work of Art Tattoo &amp; Piercing is on E. Tropicana near the Strip with piercing appointments, walk-in availability when the schedule allows, and booking support by phone at <a class="text-secondary underline hover:no-underline" href="tel:+17252241240">(725) 224-1240</a>.</p>
<p><a class="inline-flex items-center justify-center gap-2 bg-secondary text-on-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest border-2 border-secondary" href="/appointments/">Book piercing appointment</a></p>
</div>
</section>
<!-- WOA_LOCAL_PIERCING_INTENT_END -->"""


def insert_before_body(html: str, block: str, marker: str) -> tuple[str, bool]:
    if marker in html:
        return html, False
    idx = html.rfind("</body>")
    if idx < 0:
        return html, False
    return html[:idx] + block + "\n" + html[idx:], True


def upsert_marked_script(html: str, block: str, marker: str) -> tuple[str, bool]:
    if marker not in html:
        return insert_before_body(html, block, marker)
    pattern = re.compile(
        rf'<script\s+{re.escape(marker)}\s+type="application/ld\+json">.*?</script>',
        re.S,
    )
    new_html, count = pattern.subn(block, html, count=1)
    return new_html, bool(count and new_html != html)


def script_block(marker: str, data: object) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'<script {marker} type="application/ld+json">\n{payload}\n</script>'


def normalize_marked_jsonld(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    new_html = html.replace('type="application/ld+json">\\n{', 'type="application/ld+json">\n{')
    new_html = new_html.replace('}\\n</script>', '}\n</script>')
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def sync_reel_schema(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    changed = False
    legacy_marker = 'data-woa-' + 'video-schema="1"'
    legacy_pattern = re.compile(
        rf'<script\s+{re.escape(legacy_marker)}\s+type="application/ld\+json">.*?</script>\s*',
        re.S,
    )
    html, removed = legacy_pattern.subn("", html)
    changed = changed or bool(removed)
    if path.name == "code.html" and path.parent.name == "studio_videos":
        html, ok = upsert_marked_script(
            html,
            script_block(REEL_SCHEMA_MARKER, REEL_ITEMLIST_SCHEMA),
            REEL_SCHEMA_MARKER,
        )
        changed = changed or ok
    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def add_embed(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if "data-woa-featured-video-embed" in html:
        return False
    if path.parent.name == "studio_videos":
        needle = '</div>\n<div class="woa-video-grid">'
        if needle in html:
            html = html.replace(
                needle,
                '</div>\n<div class="max-w-[420px] mx-auto w-full">\n'
                f"{FEATURED_EMBED}\n"
                '</div>\n<div class="woa-video-grid">',
                1,
            )
            path.write_text(html, encoding="utf-8")
            return True
    pattern = re.compile(
        r'<div class="woa-interview-player max-w-\[420px\] mx-auto w-full">\s*'
        r'<article class="woa-video-card">',
        re.MULTILINE,
    )
    replacement = (
        '<div class="woa-interview-player max-w-[420px] mx-auto w-full">\n'
        f"{FEATURED_EMBED}\n"
        '<article class="woa-video-card">'
    )
    new_html, count = pattern.subn(replacement, html, count=1)
    if count:
        path.write_text(new_html, encoding="utf-8")
    return bool(count)


def add_local_intent(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if LOCAL_INTENT_MARKER in html:
        return False
    anchor = "</main>"
    idx = html.find(anchor)
    if idx < 0:
        return False
    html = html[:idx] + LOCAL_PIERCING_BLOCK + "\n" + html[idx:]
    path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    changed: list[str] = []
    for rel in [
        "code.html",
        "home_work_of_art_tattoo_piercing/code.html",
        "studio_videos/code.html",
    ]:
        path = ROOT / rel
        if add_embed(path) | sync_reel_schema(path) | normalize_marked_jsonld(path):
            changed.append(rel)

    for rel in [
        "piercing-guide-las-vegas/code.html",
        "best_piercing_shop_las_vegas_updated_jewelry_standards/code.html",
        "official_location_hours_contact/code.html",
    ]:
        path = ROOT / rel
        if add_local_intent(path):
            changed.append(rel)

    for rel in changed:
        print(f"[ok] {rel}")
    print(f"Done: {len(changed)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

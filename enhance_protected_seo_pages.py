#!/usr/bin/env python3
"""Surgical SEO growth patches for protected high-traffic pages (no URL changes)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIN_SCIENCE_SLUG = "skin_science_tattoo_dermatology_authority_guide"
SKIN_QUICK_MARKER = 'data-woa-skin-science-quick="1"'
ARTIST_RELATED_MARKER = 'data-woa-artist-related-guides="1"'

SKIN_QUICK_BLOCK = """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-skin-science-quick="1">
<strong>Quick answer:</strong> Tattoo ink stays in the <em>dermis</em> — the stable layer below your constantly shedding epidermis. Healthy skin, realistic placement, and desert aftercare all affect how crisp a tattoo looks years later. This hub explains the biology in plain language; it is studio education, not medical advice.
</p>
<nav aria-label="On this page" class="border border-outline-variant/30 bg-surface-container-low p-5 my-6" data-woa-skin-science-toc="1">
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary mb-3">On this page</p>
<ol class="font-body-md text-on-surface-variant space-y-1.5 list-decimal pl-5">
<li><a class="text-secondary underline hover:no-underline" href="#skin-layers">Skin layers — where ink lives</a></li>
<li><a class="text-secondary underline hover:no-underline" href="#why-permanent">Why tattoos stay permanent</a></li>
<li><a class="text-secondary underline hover:no-underline" href="#conditions">Skin conditions &amp; tattoo planning</a></li>
<li><a class="text-secondary underline hover:no-underline" href="#healing-aging">Healing, aging &amp; aftercare</a></li>
</ol>
</nav>
"""

JOSHUA_RELATED = """
<nav aria-label="Joshua Cole specialty guides" class="border border-outline-variant/30 bg-surface-container-low p-6 my-10" data-woa-artist-related-guides="1">
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary mb-3">Joshua's specialty guides</p>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Black &amp; grey realism in Las Vegas</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up tattoo planning</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/skin_science_tattoo_dermatology_authority_guide/">Skin science for tattoo collectors</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">Healed tattoo gallery</a></li>
</ul>
</nav>
"""

KATELYN_RELATED = """
<nav aria-label="Katelyn Cole piercing guides" class="border border-outline-variant/30 bg-surface-container-low p-6 my-10" data-woa-artist-related-guides="1">
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary mb-3">Katelyn's piercing guides</p>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Complete piercing guide</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/ear_piercing_guide_las_vegas/">Ear piercing guide</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/best_piercing_shop_las_vegas_updated_jewelry_standards/">Piercing shop &amp; jewelry standards</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/piercing_aftercare_guide_las_vegas/">Piercing aftercare</a></li>
</ul>
</nav>
"""

COVER_UP_PHOTO_NOTE = (
    '<p class="font-body-sm text-on-surface-variant text-sm mt-3">'
    "Attach reference photos in your appointment request message, or email them after you submit the form — "
    "Joshua reviews every cover-up consult with the actual tattoo in view."
    "</p>"
)


def patch_skin_science(html: str) -> str:
    if SKIN_QUICK_MARKER in html:
        return html
    needle = '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Skin Science for Tattoo Collectors</h1>'
    if needle not in html:
        return html
    html = html.replace(needle, needle + SKIN_QUICK_BLOCK, 1)
    html = html.replace(
        '<h2 class="font-headline-md text-on-surface text-2xl">Skin layers — where ink lives</h2>',
        '<h2 class="font-headline-md text-on-surface text-2xl" id="skin-layers">Skin layers — where ink lives</h2>',
        1,
    )
    html = html.replace(
        '<h2 class="font-headline-md text-on-surface text-2xl">Why tattoos stay permanent</h2>',
        '<h2 class="font-headline-md text-on-surface text-2xl" id="why-permanent">Why tattoos stay permanent</h2>',
        1,
    )
    for old, new in (
        (
            '<h2 class="font-headline-md text-on-surface text-2xl">Skin conditions',
            '<h2 class="font-headline-md text-on-surface text-2xl" id="conditions">Skin conditions',
        ),
        (
            '<h2 class="font-headline-md text-on-surface text-2xl">Healing',
            '<h2 class="font-headline-md text-on-surface text-2xl" id="healing-aging">Healing',
        ),
    ):
        if old in html:
            html = html.replace(old, new, 1)
    return html


def patch_artist_page(path: Path, block: str) -> str:
    html = path.read_text(encoding="utf-8")
    if ARTIST_RELATED_MARKER in html:
        return html
    if "</main>" in html:
        updated = html.replace("</main>", block + "\n</main>", 1)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            return updated
    return html


def patch_cover_up_photo_note(html: str) -> str:
    if "Joshua reviews every cover-up consult" in html:
        return html
    anchor = 'href="/appointments/">Send Joshua a Photo</a>'
    if anchor not in html:
        return html
    return html.replace(anchor, anchor + COVER_UP_PHOTO_NOTE, 1)


def main() -> int:
    changed = 0

    skin_path = ROOT / SKIN_SCIENCE_SLUG / "code.html"
    if skin_path.is_file():
        raw = skin_path.read_text(encoding="utf-8")
        updated = patch_skin_science(raw)
        if updated != raw:
            skin_path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] skin science scanability: {SKIN_SCIENCE_SLUG}")

    cover_path = ROOT / "cover-up-tattoos-las-vegas" / "code.html"
    if cover_path.is_file():
        raw = cover_path.read_text(encoding="utf-8")
        updated = patch_cover_up_photo_note(raw)
        if updated != raw:
            cover_path.write_text(updated, encoding="utf-8")
            changed += 1
            print("[ok] cover-up photo workflow note")

    for rel, block in (
        ("artists_build/joshua-cole.html", JOSHUA_RELATED),
        ("artists/katelyn-cole/code.html", KATELYN_RELATED),
        ("artists_build/katelyn-cole.html", KATELYN_RELATED),
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = patch_artist_page(path, block)
        if after != before:
            changed += 1
            print(f"[ok] artist related guides: {rel}")

    print(f"Done: {changed} protected page patch(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

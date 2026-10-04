#!/usr/bin/env python3
"""Patch healed timelines in place. Does not rebuild pages from the desert template."""

from __future__ import annotations

import re
from pathlib import Path

from build_healed_gallery_pages import _stage_photos, entry_card
from build_real_client_timeline_page import GALLERY, STUDIO, img, missing_stage, stage_card
from enhance_artist_entity_pages import timeline_section
from woa_healed_gallery import COLLECTIONS, HEALED_CATALOG, HUB_SLUG

ROOT = Path(__file__).resolve().parent
ARTICLE_RE = re.compile(
    r'<article class="woa-healed-case[^"]*" id="([^"]+)">.*?</article>',
    re.DOTALL,
)
TIMELINE_RE = re.compile(
    r'<section\b[^>]*data-woa-healed-timeline="([^"]+)"[^>]*>.*?</section>',
    re.DOTALL,
)
PHOTOS_RE = re.compile(
    r'(<section class="space-y-4" id="photos">)(.*?)(</section>)',
    re.DOTALL,
)
EMPTY_PHOTO = (
    '<p class="font-body-md text-on-surface-variant italic border border-outline-variant/30 '
    'bg-surface-container-low p-5">Studio photo for this style and stage is not yet documented. '
    'See our <a class="text-secondary underline" href="/healed_tattoo_gallery_las_vegas/">healed gallery</a> '
    'and <a class="text-secondary underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a> '
    "for available proof.</p>"
)
EMPTY_PHOTO_NEXT = (
    '<p class="font-body-md text-on-surface-variant italic border border-outline-variant/30 '
    'bg-surface-container-low p-5" data-woa-request-healed="1">Studio photo for this style and stage is not on file. '
    'See the <a class="text-secondary underline" href="/healed_tattoo_gallery_las_vegas/">healed gallery</a> '
    'and <a class="text-secondary underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a> '
    'for photos we do have. '
    '<a class="text-secondary underline" href="sms:+17252241240">Text (725) 224-1240</a> '
    'or use the <a class="text-secondary underline" href="/appointments/">appointments form</a> '
    "to request a healed photo.</p>"
)
FOLLOW_UP = (
    '<aside class="mt-4 border border-outline-variant/40 bg-surface-container-low p-5 space-y-2" data-woa-request-healed="1">'
    '<p class="font-body-md text-on-surface">Send a later healed photo</p>'
    '<p class="font-body-md text-on-surface-variant">A studio photo is on this page. '
    'Text <a class="text-secondary underline" href="sms:+17252241240">(725) 224-1240</a> '
    'or use the <a class="text-secondary underline" href="/appointments/">appointments form</a> '
    "to send a later follow-up. There is no upload form.</p></aside>"
)


def patch_healed_articles() -> None:
    by_id = {entry.entry_id: entry for entry in HEALED_CATALOG}
    slugs = [HUB_SLUG] + [slug for slug, _title, _intro in COLLECTIONS.values()]
    for slug in slugs:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            print(f"[skip] missing {slug}/code.html")
            continue
        raw = path.read_text(encoding="utf-8")
        if "<<<<<<<" in raw:
            print(f"[skip-conflict] {slug}")
            continue

        def repl(match: re.Match[str], page_slug: str = slug) -> str:
            entry_id = match.group(1)
            entry = by_id.get(entry_id)
            if entry is None:
                return match.group(0)
            return entry_card(entry, source_path=f"/{page_slug}/#{entry_id}")

        updated, count = ARTICLE_RE.subn(repl, raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {slug}/code.html ({count} timeline card(s))")
        else:
            print(f"[skip] {slug}/code.html no healed cards")


def patch_artist_timelines() -> None:
    targets = (
        (ROOT / "artists_build" / "joshua-cole.html", "joshua"),
        (ROOT / "artists" / "joshua-cole" / "code.html", "joshua"),
        (ROOT / "artists_build" / "katelyn-cole.html", "katelyn"),
        (ROOT / "artists" / "katelyn-cole" / "code.html", "katelyn"),
    )
    for path, key in targets:
        if not path.is_file():
            print(f"[skip] missing {path.relative_to(ROOT)}")
            continue
        raw = path.read_text(encoding="utf-8")
        if "<<<<<<<" in raw:
            print(f"[skip-conflict] {path.relative_to(ROOT)}")
            continue
        section = timeline_section((), key).strip()
        if TIMELINE_RE.search(raw):
            updated = TIMELINE_RE.sub(section, raw, count=1)
        else:
            updated = raw.replace("</main>", section + "\n</main>", 1)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")


def patch_healing_photos() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("code.html")):
        if not any("healing_database" in part for part in path.parts) and path.parent.name not in {
            "las-vegas-tattoo-healing-guide",
            "tattoo_healing_before_after_real_results",
        }:
            continue
        raw = path.read_text(encoding="utf-8")
        if "<<<<<<<" in raw:
            continue
        updated = raw.replace(EMPTY_PHOTO, EMPTY_PHOTO_NEXT)

        def repl(match: re.Match[str]) -> str:
            body = match.group(2)
            if "data-woa-request-healed" in body:
                return match.group(0)
            if "<picture>" not in body:
                return match.group(0)
            return match.group(1) + body + FOLLOW_UP + match.group(3)

        updated = PHOTOS_RE.sub(repl, updated, count=1)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"[ok] healing photo CTA on {changed} page(s)")


def patch_real_client() -> None:
    path = ROOT / "real_client_tattoo_timeline_las_vegas" / "code.html"
    raw = path.read_text(encoding="utf-8")
    fresh = stage_card(
        "Fresh",
        "Stage label already used on this photo: Fresh (day 0). Cross, eye, and skull mapped with soft grey wash; highlights left open.",
        f'<figure class="border border-outline-variant/30 overflow-hidden">{img("cross-eye-skull-forearm-stack-5bc3d948", STUDIO, "Fresh cross eye skull forearm tattoo Joshua Cole Las Vegas")}</figure>',
    )
    year = stage_card(
        "3+ months",
        "Stage label already used on this photo: Healed (1 year). Full forearm stack still reads clearly. No touch-up before this documentation.",
        f'<figure class="border border-outline-variant/30 overflow-hidden">{img("healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas", GALLERY, "One year healed cross eye skull forearm Joshua Cole")}</figure>',
    )
    grid = f"""<h2 class="font-headline-md text-on-surface text-2xl text-center">Fresh → about 4 weeks → 3+ months</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6" data-woa-heal-stages="1">
{fresh}
{missing_stage("About 4 weeks")}
{year}
</div>
<aside class="border border-outline-variant/40 bg-surface p-6 space-y-3" data-woa-request-healed="1">
<h3 class="font-headline-md text-on-surface text-xl">Request a healed photo</h3>
<p class="font-body-md text-on-surface-variant">The one-year photo is on file. About 4 weeks is not. Text or email a later photo — there is no upload form.</p>
<p class="font-body-md"><a class="text-secondary underline" href="sms:+17252241240">Text (725) 224-1240</a> · <a class="text-secondary underline" href="#" data-woa-email-us="1">Email us now</a> · <a class="text-secondary underline" href="/appointments/">Appointments form</a></p>
</aside>"""
    updated = raw.replace(
        "Real Client Timeline — One Tattoo, Every Stage",
        "Real Client Timeline — Fresh and 1 Year Healed",
    )
    updated = updated.replace(
        "This page documents one real tattoo from day one through later healed stages so you can see realistic peeling, line settling, and color changes — not idealized day-of photos alone.",
        "This page shows the fresh session and the one-year healed photo of one forearm tattoo. About 4 weeks is not on file, so that stage has no photo.",
    )
    start = updated.find(
        '<h2 class="font-headline-md text-on-surface text-2xl text-center">Fresh →'
    )
    end = updated.find(
        "We add stages as we photograph the same client — this is a living reference, not a one-time SEO page.</p>"
    )
    if start == -1 or end == -1:
        print("[skip] real client timeline markers missing")
        return
    end = end + len(
        "We add stages as we photograph the same client — this is a living reference, not a one-time SEO page.</p>"
    )
    updated = updated[:start] + grid + updated[end:]
    path.write_text(updated, encoding="utf-8")
    print("[ok] real_client_tattoo_timeline_las_vegas/code.html")


def report() -> None:
    print("--- healed context ---")
    for entry in HEALED_CATALOG:
        _photos, has_healed = _stage_photos(entry)
        kind = "healed context" if has_healed else "request CTA"
        print(f"  {entry.entry_id}: {kind}")


def main() -> int:
    patch_healed_articles()
    patch_artist_timelines()
    patch_healing_photos()
    patch_real_client()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

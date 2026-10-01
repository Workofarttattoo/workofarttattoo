#!/usr/bin/env python3
"""Add EEAT authority sections, healed timelines, and topic-specific links on artist pages."""

from __future__ import annotations

import re
from pathlib import Path

from woa_healed_gallery import HEALED_CATALOG
from woa_healed_timeline_template import file_exists, timeline_html
from woa_healed_timelines import (
    JOSHUA_CASE_STUDIES,
    KATELYN_CASE_STUDIES,
    CaseStudy,
)

JOSHUA_TIMELINE_IDS = (
    "roaring-lion-thigh-fresh-healed",
    "cross-eye-skull-forearm-1-year",
    "eagle-memorial-calf",
    "lion-thigh",
    "phoenix-cover-up-hand",
    "davy-jones-pirates-calf",
    "steampunk-clock-forearm",
    "skull-hourglass-forearm",
    "all-seeing-eye-triangle-fresh",
)

ROOT = Path(__file__).resolve().parent
EEAT_MARKER = 'data-woa-artist-eeat="'
TIMELINE_MARKER = 'data-woa-healed-timeline="'
FOOTER_MARKERS = ("<!-- Footer -->", "<footer", "</main>")


def _case_study_html(study: CaseStudy) -> str:
    img_block = ""
    if study.image_stem:
        webp = f"/{study.image_dir}/{study.image_stem}.webp"
        png = f"/{study.image_dir}/{study.image_stem}.png"
        if study.image_dir.startswith("cover"):
            png = webp
        img_block = f"""
<div class="md:col-span-5">
<picture>
<source srcset="{webp}" type="image/webp"/>
<img alt="{study.title} — Work of Art Las Vegas" class="w-full h-auto object-cover border border-outline-variant/30" decoding="async" loading="lazy" src="{png}"/>
</picture>
</div>"""
    stages = "".join(
        f"<li><strong>{s.label}:</strong> {s.note}</li>" for s in study.stages
    )
    guide = ""
    if study.guide_href:
        guide = f'<p class="font-body-md pt-2"><a class="text-secondary underline" href="{study.guide_href}">Related guide</a></p>'
    return f"""
<article class="grid grid-cols-1 md:grid-cols-12 gap-8 border border-outline-variant/30 p-6 md:p-8 bg-surface">
{img_block}
<div class="{'md:col-span-7' if img_block else 'md:col-span-12'} space-y-3">
<h3 class="font-headline-md text-on-surface">{study.title}</h3>
<p class="font-body-md text-on-surface-variant">{study.artist} · {study.placement} · {study.sessions}</p>
<p class="font-body-md text-on-surface-variant">{study.summary}</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{stages}</ul>
{guide}
</div>
</article>"""


def _joshua_timeline_cards() -> str:
    from build_healed_gallery_pages import entry_card

    by_id = {entry.entry_id: entry for entry in HEALED_CATALOG}
    cards = []
    for entry_id in JOSHUA_TIMELINE_IDS:
        entry = by_id.get(entry_id)
        if entry is None:
            continue
        cards.append(
            entry_card(entry, source_path=f"/artists/joshua-cole/#{entry_id}")
        )
    return "".join(cards)


def _katelyn_timeline_card() -> str:
    folder = "studio_gallery"
    stem = "ear-curation-work-eb7d2939"
    webp_ok, png_ok = file_exists(folder, stem)
    photos = []
    if webp_ok or png_ok:
        photos.append(
            (
                "fresh",
                folder,
                stem,
                "In-studio documentation",
                "Ear curation in studio — Katelyn Cole, Work of Art Las Vegas",
            )
        )
    stages = timeline_html(
        photos,
        has_healed=False,
        source_path="/artists/katelyn-cole/#ear-curation",
    )
    return f"""
<article class="woa-healed-case py-12 border-b border-outline-variant/20" id="ear-curation">
<div class="space-y-4">
<h3 class="font-headline-md text-on-surface">Ear curation — helix and flat</h3>
<p class="font-body-md text-on-surface-variant">Katelyn Cole · left ear · planning visit and install. The in-studio photo is not a healed follow-up.</p>
{stages}
</div>
</article>"""


def timeline_section(studies: tuple[CaseStudy, ...], artist_key: str) -> str:
    if artist_key == "joshua":
        cards = _joshua_timeline_cards()
        intro = (
            "Fresh, about 4 weeks, and 3+ months. A photo is shown only when that file is on disk. "
            "Pieces without a healed photo include a request path."
        )
    elif artist_key == "katelyn":
        cards = _katelyn_timeline_card()
        intro = (
            "Piercing photos stay labeled as in-studio documentation unless a healed photo is already on file."
        )
    else:
        cards = "".join(_case_study_html(s) for s in studies)
        intro = "Documented studio work — not stock before/after collages."
    return f"""
<section class="py-16 px-margin-mobile md:px-margin-desktop bg-surface border-y border-outline-variant/20" {TIMELINE_MARKER}{artist_key}">
<div class="max-w-4xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Healed timelines &amp; client stories</h2>
<p class="font-body-md text-on-surface-variant">{intro}</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="/start_here/">Start Here</a> · <a class="text-secondary underline" href="/appointments/">Book an appointment</a> · <a class="text-secondary underline" href="/geo_hub_ai_source_of_truth_work_of_art/">Studio source profile</a></p>
<div class="space-y-8">{cards}</div>
</div>
</section>
"""


JOSHUA_EEAT = """
<section class="py-16 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-artist-eeat="joshua">
<div class="max-w-4xl mx-auto space-y-10">
<h2 class="font-headline-lg text-on-surface">Joshua Cole — Artist Profile</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-10">
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">Experience</h3>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li>20+ years tattooing; studio lead at Work of Art</li>
<li>Trains resident artists and maintains alumni guest network</li>
<li>Black &amp; grey realism, portraits, sleeves, cover-up redesigns</li>
<li>Color realism, surrealistic work, and select fine-line projects</li>
</ul>
</div>
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">How he works</h3>
<p class="font-body-md text-on-surface-variant">Consult-first custom work from reference and anatomy — not flash. Sterile setup, session mapping, and desert-climate aftercare are part of every booking.</p>
<p class="font-body-md text-on-surface-variant">Machines, needles, and grey-wash systems are chosen per piece for smooth saturation and healed readability.</p>
</div>
</div>
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">Start here</h3>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Realism tattoos in Las Vegas</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up planning</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/appointments/">Book a consult with Joshua</a></li>
</ul>
</div>
</div>
</section>
"""

KATELYN_EEAT = """
<section class="py-16 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-artist-eeat="katelyn">
<div class="max-w-4xl mx-auto space-y-10">
<h2 class="font-headline-lg text-on-surface">Katelyn Cole — Piercer Profile</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-10">
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">Specialties</h3>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
<li>Ear curation and constellation piercing</li>
<li>Starter jewelry fit and downsizing planning</li>
<li>Clean placement process and aftercare education</li>
<li>Healed piercing troubleshooting and jewelry upgrades</li>
</ul>
</div>
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">Safety &amp; standards</h3>
<p class="font-body-md text-on-surface-variant">Every appointment includes placement planning, jewelry matched to anatomy, and written aftercare for Las Vegas heat and travel schedules. We keep the language factual until owner-verified credential and material documentation is added.</p>
</div>
</div>
<div class="space-y-4">
<h3 class="font-label-caps text-secondary uppercase tracking-widest text-sm">Start here</h3>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline hover:no-underline" href="/best_piercing_shop_las_vegas_updated_jewelry_standards/">Piercing shop &amp; jewelry standards</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/studio_videos/">Studio piercing videos</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/appointments/">Book piercing consult</a></li>
</ul>
</div>
</div>
</section>
"""


def fix_katelyn_breadcrumb(html: str) -> str:
    return html.replace(
        '"item": "https://www.workofarttattoo.com/piercing"',
        '"item": "https://www.workofarttattoo.com/best_piercing_shop_las_vegas_updated_jewelry_standards/"',
    ).replace(
        '"name": "Piercing",',
        '"name": "Piercing Guide",',
    )


def inject_sections(html: str, combined: str) -> str:
    html = re.sub(
        r'<section[^>]*data-woa-artist-eeat="[^"]*"[^>]*>.*?</section>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<section[^>]*data-woa-healed-timeline="[^"]*"[^>]*>.*?</section>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    for foot in FOOTER_MARKERS:
        if foot in html:
            return html.replace(foot, combined + "\n" + foot, 1)
    return html.replace("</body>", combined + "\n</body>", 1)


def main() -> int:
    pairs = (
        (ROOT / "artists_build" / "joshua-cole.html", JOSHUA_EEAT, JOSHUA_CASE_STUDIES, "joshua"),
        (ROOT / "artists_build" / "katelyn-cole.html", KATELYN_EEAT, KATELYN_CASE_STUDIES, "katelyn"),
    )
    for path, eeat, studies, key in pairs:
        if not path.is_file():
            print(f"[skip] {path.name}")
            continue
        raw = path.read_text(encoding="utf-8")
        combined = eeat + timeline_section(studies, key)
        updated = inject_sections(raw, combined)
        if path.stem == "katelyn-cole":
            updated = fix_katelyn_breadcrumb(updated)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

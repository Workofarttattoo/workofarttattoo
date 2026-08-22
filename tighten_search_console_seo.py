#!/usr/bin/env python3
"""Targeted SEO tightening from Search Console query data."""

from __future__ import annotations

from pathlib import Path

from woa_nav_config import STUDIO_PHONE_PARENS


HOME_TITLE_OLD = "Work of Art Tattoo &amp; Piercing | Las Vegas | Walk-Ins on E. Tropicana"
HOME_TITLE_NEW = "Tattoo and Piercing Shop Near the Strip | Work of Art Las Vegas"
HOME_DESC_OLD = (
    "Warm, no-attitude tattoo &amp; piercing on E. Tropicana — free consultations, "
    "walk-ins welcome. Joshua, Katelyn &amp; Teralyn in-studio. Questions encouraged. "
    f"{STUDIO_PHONE_PARENS}."
)
HOME_DESC_NEW = (
    "Tattoo and piercing shop near the Las Vegas Strip on E. Tropicana. "
    "Walk-ins welcome, free consults, cover-up tattoos, "
    "fine-line tattoos with Teralyn, and piercing with Katelyn."
)

PIERCING_BOOKING_BLOCK = """<section class="py-10 px-margin-mobile md:px-margin-desktop bg-surface-container/40 border-y border-outline-variant/20" data-woa-piercing-booking-boost="1">
<div class="max-w-4xl mx-auto space-y-5 text-center">
<span class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Piercing walk-ins and appointments</span>
<h2 class="font-headline-md text-on-surface text-2xl">Same-day piercing near the Strip</h2>
<p class="font-body-md text-on-surface-variant">Work of Art Tattoo &amp; Piercing is on E. Tropicana, minutes from the Strip. Walk-ins are welcome when the schedule allows; booking ahead is the best way to reserve time with Katelyn Cole for ear, facial, oral, and body piercing.</p>
<div class="flex flex-col sm:flex-row gap-3 justify-center">
<a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest" href="/appointments/">Book piercing appointment</a>
<a class="inline-flex items-center justify-center border border-outline px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary" href="tel:+17252241240">Call for walk-in availability</a>
</div>
<p class="font-body-md text-on-surface-variant text-sm"><a class="text-secondary underline" href="/artists/katelyn-cole/">Female piercer in Las Vegas: Katelyn Cole</a> · <a class="text-secondary underline" href="/piercing_jewelry_guide_las_vegas/">Piercing jewelry guide</a> · <a class="text-secondary underline" href="/official_location_hours_contact/">Hours and location</a></p>
</div>
</section>
"""

HOME_BOOST_BLOCK = """<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container/30 border-y border-outline-variant/20" data-woa-home-query-boost="1">
<div class="max-w-5xl mx-auto grid gap-8 md:grid-cols-3">
<div class="space-y-3">
<span class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Near the Strip</span>
<h2 class="font-headline-md text-on-surface text-2xl">Tattoo and piercing shop near the Strip</h2>
<p class="font-body-md text-on-surface-variant">Work of Art Tattoo &amp; Piercing is on E. Tropicana, minutes from the Las Vegas Strip, with tattoo consults, piercing appointments, and walk-in availability when the schedule allows.</p>
<a class="text-secondary underline font-body-md" href="/official_location_hours_contact/">See hours and location</a>
</div>
<div class="space-y-3">
<span class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Piercing</span>
<h2 class="font-headline-md text-on-surface text-2xl">Piercing walk-ins and appointments</h2>
<p class="font-body-md text-on-surface-variant">Book with Katelyn Cole for calm, anatomy-first ear, facial, oral, and body piercing. Walk-ins are welcome when there is room in the day.</p>
<a class="text-secondary underline font-body-md" href="/appointments/">Book piercing online</a>
</div>
<div class="space-y-3">
<span class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Cover-ups</span>
<h2 class="font-headline-md text-on-surface text-2xl">Cover-up tattoo consults</h2>
<p class="font-body-md text-on-surface-variant">Joshua Cole plans cover-up tattoos around healed results, contrast, scar camouflage, and realistic session strategy.</p>
<a class="text-secondary underline font-body-md" href="/cover-up-tattoos-las-vegas/">Explore cover-up tattoos</a>
</div>
</div>
</section>
"""

COVERUP_BOOST_BLOCK = """<section class="py-10 px-margin-mobile md:px-margin-desktop bg-background border-t border-outline-variant/20" data-woa-coverup-authority-boost="1">
<div class="max-w-4xl mx-auto space-y-5">
<span class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Cover-up authority</span>
<h2 class="font-headline-md text-on-surface text-2xl">Cover-up tattoo artist near the Las Vegas Strip</h2>
<p class="font-body-md text-on-surface-variant">Search demand is already showing for cover up tattoo artist Las Vegas, tattoo cover up Las Vegas, and best tattoo cover up artist near me. This page connects those searches to Joshua Cole's consult process, healed proof, pricing expectations, and realism portfolio.</p>
<div class="grid gap-4 sm:grid-cols-2">
<a class="block border border-outline-variant/30 bg-surface-container/40 p-4 hover:border-secondary transition-colors" href="/healed_cover_up_tattoos_las_vegas/"><h3 class="font-headline-md text-on-surface text-lg">Healed cover-up proof</h3><p class="font-body-md text-on-surface-variant text-sm mt-2">See healed cover-up and rework examples before booking.</p></a>
<a class="block border border-outline-variant/30 bg-surface-container/40 p-4 hover:border-secondary transition-colors" href="/realism-tattoos-las-vegas/"><h3 class="font-headline-md text-on-surface text-lg">Realism tattoo portfolio</h3><p class="font-body-md text-on-surface-variant text-sm mt-2">Compare the black and grey realism style often used for strong cover-ups.</p></a>
</div>
<p><a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-4 min-h-[48px] font-label-caps text-[11px] uppercase tracking-widest" href="/appointments/">Book cover-up consultation</a></p>
</div>
</section>
"""


def replace_all(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def insert_once_before_main_close(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    idx = text.find("</main>")
    if idx < 0:
        raise ValueError("missing </main>")
    return text[:idx] + block + text[idx:]


def update_home(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = replace_all(
        text,
        [
            (HOME_TITLE_OLD, HOME_TITLE_NEW),
            (HOME_DESC_OLD, HOME_DESC_NEW),
        ],
    )
    text = insert_once_before_main_close(text, "data-woa-home-query-boost", HOME_BOOST_BLOCK)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return text != original


def update_piercing_page(path: Path, *, title: str | None = None, desc: str | None = None) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    if title:
        text = replace_title_like(text, title)
    if desc:
        text = replace_description_like(text, desc)
    text = insert_once_before_main_close(text, "data-woa-piercing-booking-boost", PIERCING_BOOKING_BLOCK)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return text != original


def replace_title_like(text: str, title: str) -> str:
    import re

    old_title = re.search(r"<title>.*?</title>", text, re.S)
    if old_title:
        old = old_title.group(0)[7:-8]
        text = text.replace(old, title)
    return text


def replace_description_like(text: str, desc: str) -> str:
    import re

    match = re.search(r'<meta content="[^"]*" name="description"/>', text)
    if not match:
        return text
    old_desc = match.group(0).split('content="', 1)[1].split('" name=', 1)[0]
    text = text.replace(old_desc, desc)
    return text


def update_katelyn(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = replace_all(
        text,
        [
            ("Ear Piercing Las Vegas | Katelyn Cole | Work of Art", "Female Piercer Las Vegas | Katelyn Cole | Work of Art"),
            (
                "Katelyn Cole — master piercer at Work of Art Las Vegas. Ear curation, implant-grade titanium, APP-aligned technique. Book a consult.",
                "Katelyn Cole is a female piercer in Las Vegas at Work of Art near the Strip. Ear curation, implant-grade titanium, calm consults, and anatomy-first piercing.",
            ),
            (
                "Katelyn Cole — Ear Piercing in Las Vegas",
                "Katelyn Cole — Female Piercer in Las Vegas",
            ),
            (
                "Work of Art's dedicated piercing specialist. Katelyn Cole combines medical-grade safety with high-fashion jewelry design — anatomical ear curation, facial and body piercing, and luxury implant-grade jewelry.",
                "Work of Art's dedicated piercing specialist and a female piercer in Las Vegas. Katelyn Cole combines medical-grade safety with high-fashion jewelry design - anatomical ear curation, facial and body piercing, calm consults, and luxury implant-grade jewelry.",
            ),
        ],
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
    return text != original


def update_coverup(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = replace_all(
        text,
        [
            ("Tattoo Cover-Ups — Joshua Cole | Work of Art Las Vegas | Work of Art", "Cover Up Tattoo Artist Las Vegas | Joshua Cole | Work of Art"),
            (
                "Tattoo cover up, scar camouflage, real studio portfolio photos, pricing, and free consult — minutes from the Strip. Work of Art Tattoo &amp; Piercing, Las…",
                "Cover up tattoo artist in Las Vegas near the Strip. Joshua Cole plans cover-ups, scar camouflage, healed proof, pricing, and free consults at Work of Art.",
            ),
        ],
    )
    text = insert_once_before_main_close(text, "data-woa-coverup-authority-boost", COVERUP_BOOST_BLOCK)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return text != original


def main() -> int:
    updates: list[str] = []
    for p in [Path("code.html"), Path("home_work_of_art_tattoo_piercing/code.html")]:
        if update_home(p):
            updates.append(str(p))

    piercing_updates = {
        "piercing-guide-las-vegas/code.html": (
            "Piercing Las Vegas | Walk-Ins Near the Strip | Work of Art",
            "Piercing in Las Vegas near the Strip with Katelyn Cole. Ear, facial, oral, and body piercing guides, walk-ins when available, and online booking.",
        ),
        "ear_piercing_guide_las_vegas/code.html": (
            "Ear Piercing Las Vegas | Female Piercer Near the Strip | Work of Art",
            "Ear piercing in Las Vegas near the Strip with Katelyn Cole. Helix, conch, tragus, lobe, curated ears, walk-ins when available, and booking online.",
        ),
        "facial_piercing_guide_las_vegas/code.html": (
            "Facial Piercing Las Vegas | Walk-Ins Near the Strip | Work of Art",
            "Facial piercing in Las Vegas near the Strip: nostril, septum consults, bridge, eyebrow, anatomy checks, walk-ins when available, and booking online.",
        ),
        "body_piercing_guide_las_vegas/code.html": (
            "Body Piercing Las Vegas | Consults Near the Strip | Work of Art",
            "Body piercing in Las Vegas near the Strip with private consults, anatomy checks, implant-grade jewelry, walk-ins when available, and online booking.",
        ),
        "best_piercing_shop_las_vegas_updated_jewelry_standards/code.html": (
            "Tattoo and Piercing Shop Near the Strip Las Vegas | Work of Art",
            "Tattoo and piercing shop near the Las Vegas Strip on E. Tropicana. Implant-grade jewelry, sterile piercing, walk-ins when available, and online booking.",
        ),
    }
    for file, (title, desc) in piercing_updates.items():
        if update_piercing_page(Path(file), title=title, desc=desc):
            updates.append(file)

    if update_katelyn(Path("artists_build/katelyn-cole.html")):
        updates.append("artists_build/katelyn-cole.html")
    if update_coverup(Path("cover-up-tattoos-las-vegas/code.html")):
        updates.append("cover-up-tattoos-las-vegas/code.html")

    print("\n".join(updates))
    print(f"updated={len(updates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

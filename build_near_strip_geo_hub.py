#!/usr/bin/env python3
"""Build the canonical near-Strip visitor geo hub."""

from __future__ import annotations

import html
from pathlib import Path

from woa_entity_schema import guide_article_graph, schema_script
from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_PHONE_DISPLAY

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
SLUG = "tattoo_shop_near_the_strip_nap_corrected"
TITLE = "Tattoo & Piercing Studio Near the Las Vegas Strip"
DESCRIPTION = (
    "Visitor guide for reaching Work of Art Tattoo & Piercing from the Strip, MGM, "
    "The Sphere, Allegiant Stadium, and Harry Reid International Airport."
)

HEAD_LINKS = """<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>
<link href="/home_work_of_art_tattoo_piercing/woa-typography.css" rel="stylesheet"/>"""

IMAGES = (
    (
        "/home_work_of_art_tattoo_piercing/client-portfolio/color-realism-wolf-red-forearm-las-vegas.webp",
        "Color realism tattoo from Work of Art in Las Vegas",
    ),
    (
        "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas.webp",
        "Black and grey tattoo from Work of Art in Las Vegas",
    ),
    (
        "/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp",
        "Curated ear piercings from Work of Art in Las Vegas",
    ),
)

SECTIONS = (
    (
        "Direct Answer",
        (
            "Work of Art Tattoo & Piercing is a real studio on E. Tropicana for visitors staying near the Las Vegas Strip who want a planned tattoo or piercing appointment instead of a rushed casino-corridor decision.",
            "Use the studio address in maps, plan around shows, flights, alcohol, pools, and sun, and choose the artist by portfolio rather than by the nearest storefront.",
        ),
    ),
    (
        "Strip Areas This Hub Serves",
        (
            "MGM Grand, Park MGM, New York-New York, and T-Mobile Arena visitors should use the south Strip/MGM guide for event and show-day planning.",
            "The Sphere, Venetian, Wynn, Encore, Fashion Show, and Convention Center visitors should use the Sphere guide for north Strip and event-corridor planning.",
            "Mandalay Bay, Luxor, and Allegiant Stadium visitors should use the Allegiant guide when stadium traffic shapes the day.",
            "Harry Reid International Airport visitors should use the airport guide when flights, rental cars, and luggage timing matter.",
        ),
    ),
    (
        "Why Leave The Strip For A Tattoo Or Piercing",
        (
            "A dedicated studio gives you artist portfolios, placement discussion, sober decision-making, and aftercare time.",
            "Joshua Cole fits realism, black and grey, blackwork, cover-ups, sleeves, portraits, and color realistic imagery.",
            "Teralyn fits piercing plus fine line floral work, script, flash, detailed smaller tattoos, and custom drawings by commission.",
            "Katelyn Cole and Teralyn offer piercing services for clients who want calm placement and jewelry-fit discussion.",
        ),
    ),
    (
        "Las Vegas Visitor Aftercare",
        (
            "Fresh tattoos and piercings should stay out of hotel pools, hot tubs, and heavy direct sun.",
            "Plan clothing around the placement before walking the Strip, sitting through a show, carrying bags, or flying home.",
            "Do not book tattoo or piercing work after drinking. If the trip inspires an idea late at night, save the reference and book a clear appointment window.",
        ),
    ),
    (
        "Getting Here Without Guesswork",
        (
            f"Use the canonical studio address: {STUDIO_ADDRESS_SINGLE_LINE}.",
            "Rideshare pickup and resort valet pins can send drivers to the wrong place; enter the studio address directly.",
            "Travel times and fares change with events, conventions, rideshare demand, and hotel pickup zones, so check your map app before leaving.",
        ),
    ),
)

RELATED = (
    ("MGM Grand visitor guide", "/tattoo_shop_near_mgm_grand_las_vegas/"),
    ("The Sphere visitor guide", "/tattoo_shop_near_the_sphere_las_vegas/"),
    ("Allegiant Stadium visitor guide", "/tattoo_shop_near_allegiant_stadium_las_vegas/"),
    ("Harry Reid airport visitor guide", "/tattoo_shop_near_las_vegas_airport/"),
    ("Paradise locality guide", "/tattoo_shop_paradise_nevada/"),
    ("Henderson guide", "/tattoo_shop_serving_henderson_nevada/"),
    ("Spring Valley guide", "/tattoo_shop_spring_valley_las_vegas/"),
    ("Appointments", "/appointments/"),
)


def list_section(title: str, rows: tuple[str, ...]) -> str:
    items = "".join(
        f"<li class=\"font-body-md text-on-surface-variant\">{html.escape(row)}</li>"
        for row in rows
    )
    return f"""<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">{html.escape(title)}</h2>
<ul class="space-y-2 list-disc pl-5 marker:text-secondary">{items}</ul>
</section>"""


def image_grid() -> str:
    cards = "".join(
        f"""<figure class="space-y-3">
<img alt="{html.escape(alt)}" class="aspect-[4/5] w-full object-cover border border-outline-variant/30 bg-surface-container" decoding="async" loading="lazy" src="{html.escape(src)}"/>
<figcaption class="font-body-sm text-on-surface-variant">{html.escape(alt)}</figcaption>
</figure>"""
        for src, alt in IMAGES
    )
    return f"""<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-xl">Original Work From The Studio</h2>
<p class="font-body-md text-on-surface-variant">The Strip hub uses Work of Art tattoo and piercing imagery, not stock photos or fake satellite-office visuals.</p>
<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">{cards}</div>
</section>"""


def main() -> int:
    graph = guide_article_graph(slug=SLUG, title=TITLE, description=DESCRIPTION)
    sections = "\n".join(list_section(title, rows) for title, rows in SECTIONS)
    related = "".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}">{html.escape(label)}</a></li>'
        for label, href in RELATED
    )
    html_doc = f"""<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{TITLE} | Work of Art</title>
<meta content="{DESCRIPTION}" name="description"/>
<link href="{SITE}/{SLUG}/" rel="canonical"/>
<meta content="{SITE}/{SLUG}/" property="og:url"/>
<meta content="{TITLE} | Work of Art" property="og:title"/>
<meta content="{DESCRIPTION}" property="og:description"/>
<meta content="{TITLE} | Work of Art" name="twitter:title"/>
<meta content="{DESCRIPTION}" name="twitter:description"/>
{HEAD_LINKS}
{schema_script(graph)}
</head>
<body class="bg-background text-on-surface antialiased">
<nav class="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-md border-b border-outline-variant/30 flex justify-between items-center px-6 py-4">
<a class="font-headline-md text-secondary uppercase tracking-widest" href="/">Work of Art</a>
<a class="bg-secondary text-on-secondary px-6 py-3 font-label-caps text-label-caps uppercase tracking-widest" href="/appointments/">Book Now</a>
</nav>
<main class="pt-28 pb-24 px-6 max-w-3xl mx-auto space-y-10">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px]">Visitor geo hub · Las Vegas Strip</p>
<h1 class="font-headline-lg text-on-surface">{TITLE}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">You're welcome here — questions included. This hub helps Strip visitors plan a real tattoo or piercing appointment at Work of Art without relying on thin neighborhood doorway pages.</p>
{sections}
{image_grid()}
<div class="border border-outline-variant/30 p-6 bg-surface-container-low space-y-3">
<p class="font-label-caps text-secondary uppercase tracking-widest text-sm">Studio NAP</p>
<p class="font-body-md text-on-surface">{html.escape(STUDIO_ADDRESS_SINGLE_LINE)}</p>
<p class="font-body-md text-on-surface-variant">Check the official location page before planning around shows, flights, work shifts, or event traffic.</p>
<p class="font-body-md"><a class="text-secondary underline hover:no-underline" href="tel:+17252241240">{STUDIO_PHONE_DISPLAY}</a> · <a class="text-secondary underline hover:no-underline" href="/appointments/">Book appointment</a></p>
</div>
<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">Related Visitor Guides</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{related}</ul>
</section>
</main>
</body></html>
"""
    out_dir = ROOT / SLUG
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "code.html").write_text(html_doc, encoding="utf-8")
    print(f"[ok] {SLUG}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

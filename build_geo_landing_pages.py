#!/usr/bin/env python3
"""Build geo-intent landing pages — unique directions, parking, and local context per place."""

from __future__ import annotations

import html
from pathlib import Path

from woa_entity_schema import guide_article_graph, schema_script
from woa_geo_pages import GeoPage, indexable_geo_pages
from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_PHONE_DISPLAY

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"

HEAD_LINKS = """<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>
<link href="/home_work_of_art_tattoo_piercing/woa-typography.css" rel="stylesheet"/>"""

GEO_VISUALS: dict[str, tuple[tuple[str, str], ...]] = {
    "tattoo_shop_near_mgm_grand_las_vegas": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/color-realism-wolf-red-forearm-las-vegas.webp", "Color realism tattoo example for south Strip visitors"),
        ("/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-portrait-script-text-lower-arm-las-vegas.webp", "Black and grey portrait and script tattoo example"),
    ),
    "tattoo_shop_near_allegiant_stadium_las_vegas": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas.webp", "Black and grey realism tattoo example for event-weekend planning"),
    ),
    "tattoo_shop_near_las_vegas_airport": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/color-realism-wolf-red-forearm-las-vegas.webp", "Fresh tattoo example with travel-day aftercare planning"),
        ("/studio_gallery/nostril-stud-on-smiling-client-dd626b1d.webp", "Nostril piercing example for visitors planning around flights"),
    ),
    "tattoo_shop_near_the_sphere_las_vegas": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-portrait-script-text-lower-arm-las-vegas.webp", "Detailed tattoo example for Sphere and north Strip visitors"),
    ),
    "tattoo_shop_paradise_nevada": (
        ("/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp", "Curated ear piercing example from the Paradise-area studio"),
        ("/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas.webp", "Tattoo example from the E. Tropicana studio"),
    ),
    "tattoo_shop_spring_valley_las_vegas": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-skull-hood-candle-realism-las-vegas.webp", "Black and grey tattoo example for west-valley collectors"),
    ),
    "tattoo_shop_serving_henderson_nevada": (
        ("/home_work_of_art_tattoo_piercing/client-portfolio/color-realism-wolf-red-forearm-las-vegas.webp", "Color realism tattoo example for Henderson collectors"),
        ("/studio_gallery/flat-and-conch-cartilage-studs-c317138a.webp", "Cartilage piercing placement example for repeat clients"),
    ),
}

GEO_META_DESCRIPTIONS: dict[str, str] = {
    "tattoo_shop_near_mgm_grand_las_vegas": "From MGM Grand, route east on Tropicana to 2375 E. Tropicana Ave, Suite 3; use the studio address instead of a casino valet pin.",
    "tattoo_shop_near_allegiant_stadium_las_vegas": "From Allegiant Stadium or Mandalay Bay, plan the Tropicana ride before event traffic and arrive sober with time for setup.",
    "tattoo_shop_near_las_vegas_airport": "From Harry Reid terminals, stay on the Tropicana route toward 2375 E. Tropicana Ave and leave room for flight timing.",
    "tattoo_shop_near_the_sphere_las_vegas": "From The Sphere, Venetian, Wynn, or the north Strip, rideshare to 2375 E. Tropicana Ave before show traffic builds.",
    "tattoo_shop_paradise_nevada": "Paradise clients can find Work of Art on E. Tropicana between Maryland Parkway and Eastern, with one real studio address.",
    "tattoo_shop_spring_valley_las_vegas": "From Spring Valley, compare Tropicana, Flamingo, and I-215 before leaving; use the studio lot at 2375 E. Tropicana Ave.",
    "tattoo_shop_serving_henderson_nevada": "Henderson clients can plan the Tropicana studio drive around Green Valley, Eastern, or I-215 depending on session timing.",
}

CTA_LABELS = (
    "Book your free consult",
    "Check today's availability",
    "Start your consult",
    "See if we have room this week",
)

UNIQUE_SECTIONS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "tattoo_shop_near_mgm_grand_las_vegas": (
        (
            "MGM and south Strip planning",
            (
                "Book before drinking, club plans, or late show plans. A good Vegas tattoo decision needs a clear head and time for placement changes.",
                "If your group is staying near MGM Grand, Park MGM, or New York-New York, nominate one sober ride plan before the appointment.",
                "Small script, fine line, or flash may fit a short trip. Realism, cover-ups, and sleeves usually need a consult-first plan.",
            ),
        ),
        (
            "Pool, sun, and show timing",
            (
                "Fresh tattoos and fresh piercings do not belong in hotel pools or hot tubs.",
                "South Strip days often involve long walks and sun. Ask about placement if clothing, bags, or show outfits will rub the fresh area.",
                "If the tattoo is tied to a trip memory, it still deserves the same planning as a local appointment.",
            ),
        ),
    ),
    "tattoo_shop_near_allegiant_stadium_las_vegas": (
        (
            "Stadium event logistics",
            (
                "Game days and concert nights can make short map distances feel unpredictable. Keep the tattoo appointment separate from stadium entry or exit timing.",
                "Plan clothing around the placement. Jerseys, waistbands, shoulder straps, and long walks can irritate fresh work.",
                "If you want a Raiders, concert, or trip tattoo, bring references before the event starts rather than after alcohol.",
            ),
        ),
        (
            "South Strip crossover",
            (
                "Mandalay Bay, Luxor, Excalibur, and Allegiant visitors often have similar route and aftercare concerns.",
                "A quick idea can still be custom-drawn when the scope is realistic. Larger pieces should be scheduled as a consult and tattoo plan.",
                "Piercing clients should consider headphones, helmets, hats, and sleep position before choosing placement on an event weekend.",
            ),
        ),
    ),
    "tattoo_shop_near_las_vegas_airport": (
        (
            "Airport-day decisions",
            (
                "Do not book tattoo or piercing work so close to a flight that cleaning, bandaging, or comfort gets rushed.",
                "Bring flight timing, hotel timing, and rental-car timing into the booking conversation.",
                "If you are flying after a session, ask about clothing, luggage straps, airplane dryness, and when to clean the area.",
            ),
        ),
        (
            "Visitor aftercare checklist",
            (
                "Pack loose clothing for the tattoo or piercing placement.",
                "Avoid pool, hot tub, and heavy sun plans after fresh work.",
                "Use the official appointment page for current availability instead of assuming walk-in space during travel days.",
            ),
        ),
    ),
    "tattoo_shop_near_the_sphere_las_vegas": (
        (
            "Sphere and north Strip timing",
            (
                "The Sphere, Venetian, Wynn, and convention corridors create event traffic waves. Book the studio visit outside the tightest show window.",
                "A daytime consult before an evening show is usually calmer than trying to add a tattoo after doors close.",
                "Fine line, script, and small detailed pieces can fit a trip when the idea is already focused.",
            ),
        ),
        (
            "After-show reality check",
            (
                "We do not tattoo or pierce intoxicated clients.",
                "If a show inspired the design, save the references and book the next clear, unrushed opening.",
                "Fresh work needs clean aftercare, not a late-night crowd, hotel pool, or sun-heavy next day.",
            ),
        ),
    ),
    "tattoo_shop_paradise_nevada": (
        (
            "Why Paradise matters",
            (
                "Paradise is the actual locality for many Strip-adjacent addresses, including Work of Art's E. Tropicana studio address.",
                "This page exists to clarify the real studio location, not to claim a second storefront.",
                "Use it when maps, local search, or rideshare apps describe the area differently from the City of Las Vegas.",
            ),
        ),
        (
            "Local client use case",
            (
                "Paradise clients often need follow-up access for multi-session tattoos, healed checks, piercing questions, and jewelry-fit conversations.",
                "The studio roster is Joshua Cole, Katelyn Cole, and Teralyn.",
                "Visitors staying nearby should still plan around sobriety, sun, pools, and travel timing.",
            ),
        ),
    ),
    "tattoo_shop_spring_valley_las_vegas": (
        (
            "West-valley appointment planning",
            (
                "Spring Valley clients often reach us by Tropicana, Flamingo, Decatur, Jones, or I-215 depending on where they start.",
                "For sleeves and cover-ups, the value is artist continuity across sessions, not shaving a few minutes off the first drive.",
                "Bring healed photos, old tattoo photos, and reference images to make the consult worth the trip.",
            ),
        ),
        (
            "What belongs here",
            (
                "Joshua Cole fits realism, black and grey, blackwork, cover-ups, and color realistic imagery.",
                "Teralyn fits fine line floral work, script, detailed smaller tattoos, flash, and custom drawings by commission.",
                "Katelyn Cole handles piercing and ear curation when placement needs a longer plan.",
            ),
        ),
    ),
    "tattoo_shop_serving_henderson_nevada": (
        (
            "Henderson-to-Tropicana fit",
            (
                "This page stays indexed because Henderson clients often plan larger tattoos around artist fit and repeat sessions.",
                "Green Valley is consolidated here so Henderson searchers get one stronger page instead of thin neighborhood duplicates.",
                "Use the consult to discuss project sequence, not only a single appointment date.",
            ),
        ),
        (
            "When the drive is worth it",
            (
                "Large realism, sleeves, portraits, cover-ups, and detailed custom work benefit from a consistent artist relationship.",
                "Piercing clients should bring current jewelry and irritation questions rather than guessing from generic online advice.",
                "If the project is impulsive or budget-sensitive, start with questions before committing to the drive.",
            ),
        ),
    ),
}


def _list_section(title: str, items: tuple[str, ...]) -> str:
    rows = "".join(
        f"<li class=\"font-body-md text-on-surface-variant\">{html.escape(line)}</li>"
        for line in items
    )
    return f"""<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">{html.escape(title)}</h2>
<ul class="space-y-2 list-disc pl-5 marker:text-secondary">{rows}</ul>
</section>"""


def _directions_cta(page: GeoPage) -> str:
    label = CTA_LABELS[sum(ord(ch) for ch in page.slug) % len(CTA_LABELS)]
    return f"""<section class="border border-secondary/30 bg-surface-container-low p-6 space-y-3">
<p class="font-body-md text-on-surface-variant">Have the route figured out? Send the idea, placement, and timing before you make the drive.</p>
<a class="inline-flex bg-secondary text-on-secondary px-6 py-3 font-label-caps text-label-caps uppercase tracking-widest hover:opacity-90 transition-opacity" href="/appointments/">{html.escape(label)}</a>
</section>"""


def _unique_sections(page: GeoPage) -> str:
    sections = []
    for title, items in UNIQUE_SECTIONS.get(page.slug, ()):
        sections.append(_list_section(title, items))
    return "\n".join(sections)


def _proof_section(page: GeoPage) -> str:
    visuals = GEO_VISUALS.get(page.slug, ())
    if not visuals:
        return ""
    cards = "".join(
        f"""<figure class="space-y-3">
<img alt="{html.escape(alt)}" class="aspect-[4/5] w-full object-cover border border-outline-variant/30 bg-surface-container" decoding="async" loading="lazy" src="{html.escape(src)}"/>
<figcaption class="font-body-sm text-on-surface-variant">{html.escape(alt)}</figcaption>
</figure>"""
        for src, alt in visuals
    )
    return f"""<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-xl">Relevant studio visuals</h2>
<p class="font-body-md text-on-surface-variant">Every photo below is real client work from our Tropicana studio.</p>
<div class="grid grid-cols-1 sm:grid-cols-{min(len(visuals), 3)} gap-4">{cards}</div>
</section>"""


def page_html(page: GeoPage) -> str:
    meta = GEO_META_DESCRIPTIONS.get(
        page.slug,
        (
            f"Tattoo & piercing near {page.title.split(' Near ')[-1].split(' in ')[-1].split(' Serving ')[-1].rstrip('.')} — "
            f"{page.drive_time}. {STUDIO_ADDRESS_SINGLE_LINE}. Call {STUDIO_PHONE_DISPLAY}."
        ),
    )[:158]
    graph = guide_article_graph(slug=page.slug, title=page.title, description=meta)
    related = "".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}">'
        f"{html.escape(label)}</a></li>"
        for label, href in page.related_guides
    )
    return f"""<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{html.escape(page.title)} | Work of Art</title>
<meta content="{html.escape(meta)}" name="description"/>
<link href="{SITE}/{page.slug}/" rel="canonical"/>
<meta content="{SITE}/{page.slug}/" property="og:url"/>
<meta content="{html.escape(page.title)} | Work of Art" property="og:title"/>
<meta content="{html.escape(meta)}" property="og:description"/>
<meta content="{html.escape(page.title)} | Work of Art" name="twitter:title"/>
<meta content="{html.escape(meta)}" name="twitter:description"/>
{HEAD_LINKS}
{schema_script(graph)}
</head>
<body class="bg-background text-on-surface antialiased">
<nav class="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-md border-b border-outline-variant/30 flex justify-between items-center px-6 py-4">
<a class="font-headline-md text-secondary uppercase tracking-widest" href="/">Work of Art</a>
<a class="bg-secondary text-on-secondary px-6 py-3 font-label-caps text-label-caps uppercase tracking-widest" href="/appointments/">Book Now</a>
</nav>
<main class="pt-28 pb-24 px-6 max-w-3xl mx-auto space-y-10">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px]">Local guide · {html.escape(page.drive_time)}</p>
<h1 class="font-headline-lg text-on-surface">{html.escape(page.title)}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">{html.escape(page.intro)}</p>
<p class="font-body-md text-on-surface-variant border-l-4 border-secondary pl-4">{html.escape(page.audience_note)}</p>
{_list_section("Directions from your area", page.directions)}
{_directions_cta(page)}
{_list_section("Parking", page.parking)}
{_list_section("Why collectors choose Work of Art", page.why_choose)}
{_unique_sections(page)}
{_proof_section(page)}
<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">Nearby landmarks</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(page.landmarks[0])}</p>
</section>
<div class="border border-outline-variant/30 p-6 bg-surface-container-low space-y-3">
<p class="font-label-caps text-secondary uppercase tracking-widest text-sm">Studio NAP</p>
<p class="font-body-md text-on-surface">{html.escape(STUDIO_ADDRESS_SINGLE_LINE)}</p>
<p class="font-body-md text-on-surface-variant">Check the official location page before planning around shows, flights, work shifts, or event traffic.</p>
<p class="font-body-md"><a class="text-secondary underline hover:no-underline" href="tel:+17252241240">{STUDIO_PHONE_DISPLAY}</a> · <a class="text-secondary underline hover:no-underline" href="/appointments/">Book appointment</a></p>
</div>
<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">Related guides</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{related}
<li><a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua Cole — tattoo</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/katelyn-cole/">Katelyn Cole — piercing</a></li>
</ul>
</section>
</main>
</body></html>
"""


def main() -> int:
    pages = indexable_geo_pages()
    for page in pages:
        out_dir = ROOT / page.slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "code.html").write_text(page_html(page), encoding="utf-8")
        print(f"[ok] {page.slug}/")
    print(f"Done: {len(pages)} indexable geo landing page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

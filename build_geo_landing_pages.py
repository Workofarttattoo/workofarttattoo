#!/usr/bin/env python3
"""Build geo-intent landing pages — unique directions, parking, and local context per place."""

from __future__ import annotations

import html
from pathlib import Path

from woa_entity_schema import guide_article_graph, schema_script
from woa_geo_pages import GEO_PAGES, GeoPage
from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE, STUDIO_HOURS_SUMMARY, STUDIO_PHONE_DISPLAY

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"

HEAD_LINKS = """<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>
<link href="/home_work_of_art_tattoo_piercing/woa-typography.css" rel="stylesheet"/>"""


def _list_section(title: str, items: tuple[str, ...]) -> str:
    rows = "".join(
        f"<li class=\"font-body-md text-on-surface-variant\">{html.escape(line)}</li>"
        for line in items
    )
    return f"""<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">{html.escape(title)}</h2>
<ul class="space-y-2 list-disc pl-5 marker:text-secondary">{rows}</ul>
</section>"""


def page_html(page: GeoPage) -> str:
    meta = (
        f"Tattoo & piercing near {page.title.split(' Near ')[-1].split(' in ')[-1].split(' Serving ')[-1].rstrip('.')} — "
        f"{page.drive_time}. {STUDIO_ADDRESS_SINGLE_LINE}. Call {STUDIO_PHONE_DISPLAY}."
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
{_list_section("Parking", page.parking)}
{_list_section("Why collectors choose Work of Art", page.why_choose)}
<section class="space-y-3">
<h2 class="font-headline-md text-on-surface text-xl">Nearby landmarks</h2>
<p class="font-body-md text-on-surface-variant">{html.escape(page.landmarks[0])}</p>
</section>
<div class="border border-outline-variant/30 p-6 bg-surface-container-low space-y-3">
<p class="font-label-caps text-secondary uppercase tracking-widest text-sm">Studio NAP</p>
<p class="font-body-md text-on-surface">{html.escape(STUDIO_ADDRESS_SINGLE_LINE)}</p>
<p class="font-body-md text-on-surface-variant">{html.escape(STUDIO_HOURS_SUMMARY)}</p>
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
    for page in GEO_PAGES:
        out_dir = ROOT / page.slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "code.html").write_text(page_html(page), encoding="utf-8")
        print(f"[ok] {page.slug}/")
    print(f"Done: {len(GEO_PAGES)} geo landing page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

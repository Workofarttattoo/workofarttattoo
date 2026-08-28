#!/usr/bin/env python3
"""Build Real Client Timeline page — one tattoo, documented heal stages."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import expert_callout, reviewed_by_block
from woa_entity_schema import ID_JOSHUA, guide_article_graph, schema_script
from woa_expert_entity_blocks import joshua_entity_block
from woa_healed_gallery import GALLERY, STUDIO

ROOT = Path(__file__).resolve().parent
SLUG = "real_client_tattoo_timeline_las_vegas"
SITE = f"https://www.workofarttattoo.com/{SLUG}/"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
TITLE = "Real Client Tattoo Timeline — Fresh to 1 Year | Joshua Cole, Las Vegas"
DESCRIPTION = (
    "One forearm tattoo documented from fresh to one year — cross, eye, and skull black & grey realism "
    "by Joshua Cole. Real heal stages, desert aftercare, no filters. Work of Art Las Vegas."
)
BOOK = "/appointments/"
JOSHUA = "/artists/joshua-cole/"
HEALED_HUB = "/healed_tattoo_gallery_las_vegas/"
REALISM = "/realism_tattoos_las_vegas_master_authority_guide/"


def img(stem: str, folder: str, alt: str) -> str:
    webp = f"https://www.workofarttattoo.com/{folder}/{stem}.webp"
    png = f"https://www.workofarttattoo.com/{folder}/{stem}.png"
    return (
        f'<picture><source srcset="{webp}" type="image/webp"/>'
        f'<img alt="{html.escape(alt)}" class="w-full h-auto object-cover" loading="lazy" src="{png}"/></picture>'
    )


def stage_card(label: str, note: str, image_html: str, *, pending: bool = False) -> str:
    badge = (
        '<span class="font-label-caps text-[10px] uppercase tracking-widest text-on-surface-variant">Coming soon</span>'
        if pending
        else '<span class="font-label-caps text-[10px] uppercase tracking-widest text-secondary">Documented</span>'
    )
    media = image_html if image_html else '<p class="font-body-md text-on-surface-variant italic">Photo update in progress.</p>'
    return f"""<article class="border border-outline-variant/30 bg-surface-container-high overflow-hidden">
<div class="p-5 space-y-3 border-b border-outline-variant/20 flex justify-between items-start gap-4">
<h2 class="font-headline-md text-on-surface text-xl">{html.escape(label)}</h2>
{badge}
</div>
<div class="p-5 space-y-4">
{media}
<p class="font-body-md text-on-surface-variant">{html.escape(note)}</p>
</div>
</article>"""


def main_html() -> str:
    fresh_stem = "cross-eye-skull-forearm-stack-5bc3d948"
    healed_stem = "healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas"

    stages = stage_card(
        "Fresh — day 0",
        "Cross, eye, and skull mapped with soft grey wash; highlights left open. Single long session with Joshua Cole.",
        f'<figure class="border border-outline-variant/30 overflow-hidden">{img(fresh_stem, STUDIO, "Fresh cross eye skull forearm tattoo Joshua Cole Las Vegas")}</figure>',
    )
    two_weeks = stage_card(
        "2 weeks",
        "Peeling complete; grey steps separated without blowout. Client used desert aftercare — saline, no sun, no picking.",
        "",
        pending=True,
    )
    three_months = stage_card(
        "3 months",
        "Contrast settling; cross bevel and iris detail still crisp. Same client, studio check-in — no touch-up required.",
        "",
        pending=True,
    )
    one_year = stage_card(
        "1 year",
        "Full forearm stack from multiple angles — eyelash detail, skull teeth, and cross beveling still read clearly. No touch-up before documentation.",
        f'<figure class="border border-outline-variant/30 overflow-hidden">{img(healed_stem, GALLERY, "One year healed cross eye skull forearm Joshua Cole")}</figure>',
    )
    three_years = stage_card(
        "3 years",
        "Long-term documentation scheduled — this page updates as we publish multi-year healed photos of the same piece.",
        "",
        pending=True,
    )

    joshua_note = expert_callout(
        "Real client timeline",
        "I publish heal stages because day-zero photos lie — black and grey realism is judged at six months and beyond, especially in Vegas sun.",
        expert="joshua",
    )

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-8">
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="{HEALED_HUB}">← Healed tattoo gallery</a> · <a class="text-secondary underline" href="{REALISM}">Realism guide</a></p>
{reviewed_by_block(expert="joshua")}
{joshua_entity_block()}
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Real client proof · Joshua Cole</span>
<h1 class="font-headline-xl text-on-surface leading-tight">Real Client Timeline — One Tattoo, Every Stage</h1>
<p class="font-body-lg text-on-surface-variant">Cross, eye &amp; skull forearm stack — black &amp; grey realism by Joshua Cole at Work of Art Las Vegas. One client. One piece. Honest heal documentation — not stock photos.</p>
{joshua_note}
<div class="flex flex-wrap gap-3">
<a class="bg-secondary text-on-secondary px-8 py-4 font-label-caps tracking-widest" href="{BOOK}">Book realism consult</a>
<a class="border border-outline px-8 py-4 font-label-caps tracking-widest hover:border-secondary" href="{JOSHUA}">Joshua Cole portfolio</a>
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-4xl mx-auto space-y-8">
<h2 class="font-headline-md text-on-surface text-2xl text-center">Fresh → 2 weeks → 3 months → 1 year → 3 years</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
{stages}
{two_weeks}
{three_months}
{one_year}
{three_years}
</div>
<p class="font-body-md text-on-surface-variant text-center pt-4">We add stages as we photograph the same client — this is a living reference, not a one-time SEO page.</p>
</div>
</section>
</main>"""


def patch_meta(page: str) -> str:
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE)} | Work of Art</title>", page, count=1)
    page = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html.escape(DESCRIPTION)}" name="description"/>',
        page,
        count=1,
    )
    page = re.sub(
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{SITE}" rel="canonical"/>',
        page,
        count=1,
    )
    return page


def main() -> int:
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page)
    page = re.sub(r'<main class="relative pt-20">.*?</main>', main_html().strip(), page, count=1, flags=re.DOTALL)
    page = re.sub(r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*', "", page, flags=re.DOTALL)
    graph = guide_article_graph(slug=SLUG, title=TITLE, description=DESCRIPTION, author_id=ID_JOSHUA)
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    out = ROOT / SLUG
    out.mkdir(parents=True, exist_ok=True)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {SLUG}/code.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

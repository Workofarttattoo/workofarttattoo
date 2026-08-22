#!/usr/bin/env python3
"""Build piercing pillar pages — definitive topic hubs that link to cluster guides."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import reviewed_by_block
from woa_piercing_seo import BOOK, PHONE_DISPLAY, PHONE_TEL, hub_meta_description, pillar_meta, pillar_title
from woa_entity_schema import ID_KATELYN, guide_article_graph, schema_script
from woa_piercing_authority import (
    BOOK,
    HUB_SLUG,
    KATELYN_PAGE,
    PIERCING_CATALOG as _BASE,
    PiercingGuide,
    slug_for,
)
from woa_piercing_catalog_extra import PIERCING_CATALOG_EXTRA
from woa_piercing_pillars import (
    EAR_SLUGS,
    BODY_SLUGS,
    FACIAL_SLUGS,
    ORAL_SLUGS,
    PILLARS,
    SKIP_STANDALONE_CLUSTER,
    PiercingPillar,
)

PIERCING_CATALOG: tuple[PiercingGuide, ...] = _BASE + PIERCING_CATALOG_EXTRA

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OG = "/studio_gallery/ear-lobe-piercing-session-da19eec5"
BOOK_LINK = "/appointments/"


def clusters_for(pillar: PiercingPillar) -> list[PiercingGuide]:
    if pillar.cluster_filter == "none" or pillar.cluster_filter == "all":
        return []
    filters = {
        "ear": EAR_SLUGS,
        "facial": FACIAL_SLUGS,
        "oral": ORAL_SLUGS,
        "body": BODY_SLUGS,
    }
    allowed = filters.get(pillar.cluster_filter, set())
    return [
        g
        for g in PIERCING_CATALOG
        if g.slug_id in allowed
        and g.slug_id not in SKIP_STANDALONE_CLUSTER
        and g.offered
    ]


def cluster_cards(guides: list[PiercingGuide]) -> str:
    if not guides:
        return ""
    cards = "\n".join(
        f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-5 hover:border-secondary transition-colors" href="/{slug_for(g)}/">
<h3 class="font-headline-md text-on-surface text-base">{html.escape(g.name)}</h3>
<p class="font-body-md text-on-surface-variant text-sm mt-1">{html.escape(g.healing_time.split(';')[0])} · Pain {g.pain_score}/10</p>
</a>"""
        for g in guides
    )
    return f"""<section class="space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Placement guides</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">{cards}</div>
</section>"""


def related_pillar_links(pillar: PiercingPillar) -> str:
    items = "".join(
        f'<li><a class="text-secondary underline" href="{html.escape(href)}">{html.escape(label)}</a></li>'
        for label, href in pillar.related_pillars
    )
    return f"""<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Related guides</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{items}</ul>
</section>"""


def pillar_main(pillar: PiercingPillar) -> str:
    body = "".join(
        f'<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(p)}</p>'
        for p in pillar.body_paragraphs
    )
    clusters = cluster_cards(clusters_for(pillar))
    related = related_pillar_links(pillar)
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-8">
<p class="font-body-md text-on-surface-variant">
<a class="text-secondary underline" href="/{HUB_SLUG}/">Complete piercing guide</a>
</p>
{reviewed_by_block(expert="katelyn")}
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Pillar guide · Katelyn Cole</span>
<h1 class="font-headline-xl text-on-surface leading-tight">{html.escape(pillar.title)}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">{html.escape(pillar.intro)}</p>
{body}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-4xl mx-auto space-y-12">
{clusters}
{related}
<div class="flex flex-col sm:flex-row gap-4 pt-4">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest text-center" href="{BOOK}">Book piercing online</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest text-center hover:border-secondary" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
</div>
</div>
</section>
</main>"""


def patch_meta(page_html: str, slug: str, title: str, description: str) -> str:
    canon = f"{SITE}/{slug}/"
    page_html = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | Work of Art</title>", page_html, count=1)
    page_html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html.escape(description)}" name="description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{canon}" rel="canonical"/>',
        page_html,
        count=1,
    )
    return page_html


def patch_main(page_html: str, main: str) -> str:
    return re.sub(r'<main class="relative pt-20">.*?</main>', main.strip(), page_html, count=1, flags=re.DOTALL)


def write_pillar(pillar: PiercingPillar) -> None:
    if pillar.slug == HUB_SLUG:
        return
    seo_title = pillar_title(pillar.title)
    seo_desc = pillar_meta(pillar.title.split(" — ")[0].lower())
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, pillar.slug, seo_title, seo_desc)
    page = patch_main(page, pillar_main(pillar))
    page = re.sub(r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*', "", page, flags=re.DOTALL)
    graph = guide_article_graph(
        slug=pillar.slug,
        title=seo_title,
        description=seo_desc,
        author_id=ID_KATELYN,
    )
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    out = ROOT / pillar.slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {pillar.slug}/code.html")


def main() -> int:
    for pillar in PILLARS:
        write_pillar(pillar)
    built = sum(1 for p in PILLARS if p.slug != HUB_SLUG)
    print(f"Done: {built} piercing pillar page(s) (+ complete guide hub via build_piercing_authority_pages.py)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

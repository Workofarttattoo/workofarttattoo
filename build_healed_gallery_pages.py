#!/usr/bin/env python3
"""Build healed tattoo gallery hub + collection pages from woa_healed_gallery catalog."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_healed_gallery import (
    COLLECTIONS,
    HUB_SLUG,
    CollectionId,
    HealedEntry,
    ImageRef,
    entries_for,
    featured_entry,
    image_url,
    seo_alt,
)
from woa_entity_schema import guide_article_graph, schema_script

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"


def picture(ref: ImageRef, entry: HealedEntry, *, eager: bool = False) -> str:
    webp = image_url(ref, webp=True)
    png = image_url(ref, webp=False)
    alt = html.escape(seo_alt(entry, ref))
    loading = "eager" if eager else "lazy"
    return (
        f'<picture><source srcset="{webp}" type="image/webp"/>'
        f'<img alt="{alt}" class="w-full h-auto object-cover" decoding="async" height="800" '
        f'loading="{loading}" src="{png}" width="800"/></picture>'
    )


def entry_card(entry: HealedEntry, *, eager: bool = False) -> str:
    images = ""
    if entry.fresh and entry.healed and entry.fresh.stem != entry.healed.stem:
        images = f"""<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
<figure class="border border-outline-variant/30 bg-surface overflow-hidden">
{picture(entry.fresh, entry, eager=eager)}
<figcaption class="p-3 font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(entry.fresh.stage)}</figcaption>
</figure>
<figure class="border border-outline-variant/30 bg-surface overflow-hidden">
{picture(entry.healed, entry)}
<figcaption class="p-3 font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(entry.healed.stage)}</figcaption>
</figure>
</div>"""
    else:
        images = f"""<figure class="border border-outline-variant/30 bg-surface overflow-hidden max-w-2xl">
{picture(entry.healed, entry, eager=eager)}
<figcaption class="p-3 font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(entry.healed.stage)}</figcaption>
</figure>"""

    gallery_block = ""
    if entry.gallery:
        tiles = []
        for i, ref in enumerate(entry.gallery):
            tiles.append(
                f"""<figure class="border border-outline-variant/30 bg-surface overflow-hidden">
{picture(ref, entry, eager=eager and i == 0)}
<figcaption class="p-2 font-label-caps text-[9px] uppercase tracking-widest text-secondary">{html.escape(ref.stage)}</figcaption>
</figure>"""
            )
        gallery_block = f"""<div class="mt-8">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-4">Healed photo set — {html.escape(entry.healed_age)} ({len(entry.gallery)} angles)</p>
<div class="grid grid-cols-2 md:grid-cols-3 gap-3">
{"".join(tiles)}
</div>
</div>"""

    timeline = ""
    if entry.timeline:
        rows = "".join(
            f'<li><strong class="text-on-surface">{html.escape(label)}</strong> — {html.escape(note)}</li>'
            for label, note in entry.timeline
        )
        timeline = f"""<div class="mt-6">
<p class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-3">Healing timeline</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{rows}</ul>
</div>"""

    return f"""<article class="woa-healed-case py-12 border-b border-outline-variant/20 last:border-0" id="{html.escape(entry.entry_id)}">
<div class="space-y-6">
<div>
<h2 class="font-headline-md text-on-surface text-2xl mb-2">{html.escape(entry.title)} — {html.escape(entry.healed_age)} healed</h2>
<p class="font-body-md text-on-surface-variant max-w-3xl">{html.escape(entry.description)}</p>
</div>
{images}
{gallery_block}
<dl class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-4 font-body-md text-on-surface-variant mt-6">
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Artist</dt><dd class="text-on-surface">{html.escape(entry.artist)}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Placement</dt><dd>{html.escape(entry.placement)}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Sessions</dt><dd>{html.escape(entry.sessions)}</dd></div>
<div><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Touch-up</dt><dd>{html.escape(entry.touch_up)}</dd></div>
<div class="sm:col-span-2"><dt class="font-label-caps text-secondary uppercase tracking-widest text-[10px] mb-1">Aftercare notes</dt><dd>{html.escape(entry.aftercare_notes)}</dd></div>
</dl>
{timeline}
</div>
</article>"""


def hub_main() -> str:
    featured = featured_entry()
    featured_section = ""
    if featured:
        featured_section = f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-4xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">Featured · {html.escape(featured.healed_age)} healed</span>
{entry_card(featured, eager=True)}
</div>
</section>"""

    cards = []
    for cid, (slug, title, blurb) in COLLECTIONS.items():
        count = len(entries_for(cid))
        cards.append(
            f"""<a class="block bg-surface-container-high border border-outline-variant/30 p-8 hover:border-secondary transition-colors group" href="/{slug}/">
<span class="font-label-caps text-secondary uppercase tracking-widest text-[10px]">{count} documented piece{"s" if count != 1 else ""}</span>
<h2 class="font-headline-md text-on-surface text-xl mt-2 group-hover:text-secondary transition-colors">{html.escape(title)}</h2>
<p class="font-body-md text-on-surface-variant mt-3">{html.escape(blurb)}</p>
<span class="inline-block mt-4 font-label-caps text-[11px] uppercase tracking-widest text-secondary">View collection →</span>
</a>"""
        )
    grid = "\n".join(cards)
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Healed portfolio proof</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Healed tattoo gallery — Las Vegas studio results</h1>
<p class="font-body-lg text-on-surface-variant max-w-2xl">Most shops show only day-one photos. We document fresh and healed work so you can answer the questions that matter before you book: <em>Will fine line last? How does black and grey age? What does color look like after a year?</em></p>
<p class="font-body-md text-on-surface-variant">Every entry includes placement, session count, touch-up status, and aftercare context — not anonymous portfolio filler.</p>
</div>
</section>
{featured_section}
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-6xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Browse by style</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{grid}
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface">Planning your piece?</h2>
<p class="font-body-md text-on-surface-variant">Joshua Cole documents fresh and healed photos in-studio. Start with a consult — we walk through design, session length, and desert aftercare before you commit.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="/appointments/">Book consult</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors" href="/tattoo_healing_before_after_real_results/">Fresh vs healed guide</a>
</div>
<p class="font-body-md text-on-surface-variant pt-2"><a class="text-secondary underline" href="/joshua_oil_painting_black_grey_tattoo_aging_las_vegas/">Why oil painting training shapes how Joshua plans for long-term healing</a></p>
</div>
</section>
</main>"""


def collection_main(collection: CollectionId) -> str:
    slug, title, intro = COLLECTIONS[collection]
    items = entries_for(collection)
    cards = "\n".join(entry_card(e, eager=i == 0) for i, e in enumerate(items))
    other_links = []
    for cid, (other_slug, other_title, _b) in COLLECTIONS.items():
        if cid == collection:
            continue
        other_links.append(
            f'<li><a class="text-secondary underline hover:no-underline" href="/{other_slug}/">{html.escape(other_title)}</a></li>'
        )
    siblings = "\n".join(other_links)
    hero_img = items[0].healed if items else None
    hero = ""
    if hero_img:
        hero = f"""<section class="relative min-h-[40vh] flex items-end px-margin-mobile md:px-margin-desktop pb-12 overflow-hidden">
<div class="absolute inset-0 z-0 opacity-40">{picture(hero_img, items[0], eager=True)}</div>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-transparent"></div>
<div class="relative z-10 max-w-3xl pt-24">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block">Healed gallery</span>
<h1 class="font-headline-xl text-[36px] md:text-headline-lg text-on-surface leading-tight">{html.escape(title)}</h1>
<p class="font-body-lg text-on-surface-variant mt-4 max-w-2xl">{html.escape(intro)}</p>
</div>
</section>"""
    else:
        hero = f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop pt-28">
<h1 class="font-headline-xl text-on-surface">{html.escape(title)}</h1>
<p class="font-body-lg text-on-surface-variant mt-4 max-w-2xl">{html.escape(intro)}</p>
</section>"""

    return f"""<main class="relative pt-20">
{hero}
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl mx-auto">
<p class="font-body-md text-on-surface-variant mb-10"><a class="text-secondary underline" href="/{HUB_SLUG}/">← All healed collections</a></p>
{cards}
</div>
</section>
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto">
<h2 class="font-headline-md text-on-surface mb-4">More healed collections</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{siblings}</ul>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop text-center">
<div class="max-w-xl mx-auto space-y-4">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="/appointments/">Book a consult</a>
</div>
</section>
</main>"""


def patch_meta(page_html: str, slug: str, title: str, description: str, og_path: str) -> str:
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
    for prop in ("og:url",):
        page_html = re.sub(
            rf'<meta content="https://www.workofarttattoo.com/tattoo_healing[^"]*" property="{prop}"/>',
            f'<meta content="{canon}" property="{prop}"/>',
            page_html,
            count=1,
        )
    og_img = f"{SITE}{og_path}.webp"
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" property="og:image"/>',
        f'<meta content="{og_img}" property="og:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" property="og:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" property="og:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" property="og:description"/>',
        f'<meta content="{html.escape(description)}" property="og:description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" name="twitter:image"/>',
        f'<meta content="{og_img}" name="twitter:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Tattoo &amp; Piercing Aftercare in Desert Climate \| Work of Art" name="twitter:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" name="twitter:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="Vegas-specific healing:[^"]*" name="twitter:description"/>',
        f'<meta content="{html.escape(description)}" name="twitter:description"/>',
        page_html,
        count=1,
    )
    return page_html


def patch_main(page_html: str, main: str) -> str:
    return re.sub(
        r'<main class="relative pt-20">.*?</main>',
        main.strip(),
        page_html,
        count=1,
        flags=re.DOTALL,
    )


def inject_schema(page_html: str, slug: str, title: str, description: str) -> str:
    page_html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page_html,
        flags=re.DOTALL,
    )
    graph = guide_article_graph(slug=slug, title=title, description=description)
    return page_html.replace("</head>", schema_script(graph) + "\n</head>", 1)


def write_page(slug: str, main: str, title: str, description: str, og_path: str) -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    out_dir = ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, slug, title, description, og_path)
    page = patch_main(page, main)
    page = inject_schema(page, slug, title, description)
    (out_dir / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {slug}/code.html")


def main() -> int:
    hub_title = "Healed Tattoo Gallery"
    hub_desc = (
        "Fresh and healed tattoo documentation from Work of Art Las Vegas — black and grey, "
        "fine line, color, cover-ups, sleeves, and portraits with session and aftercare notes."
    )
    featured = featured_entry()
    hub_og = (
        image_url(featured.healed, webp=False).replace(".png", "")
        if featured
        else "/home_work_of_art_tattoo_piercing/client-portfolio/steampunk-clock-gears-rose-forearm-healed-las-vegas"
    )
    write_page(
        HUB_SLUG,
        hub_main(),
        hub_title,
        hub_desc,
        hub_og,
    )

    for cid, (slug, title, intro) in COLLECTIONS.items():
        items = entries_for(cid)
        og = image_url(items[0].healed, webp=False) if items else "/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.png"
        write_page(slug, collection_main(cid), title, intro[:155], og.replace(".png", ""))

    print(f"Done: hub + {len(COLLECTIONS)} collection page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

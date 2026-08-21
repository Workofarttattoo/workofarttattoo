#!/usr/bin/env python3
"""Build Healing Database hub, style hubs, universal timeline pages, and style×stage leaf pages."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import expert_callout, reviewed_by_block, toc_nav
from woa_entity_schema import ID_JOSHUA, faq_page_graph, guide_article_graph, schema_script
from woa_expert_entity_blocks import joshua_entity_block
from woa_healing_database import (
    AFTERCARE_GUIDE,
    BOOK,
    HEALED_HUB,
    HUB_FAQS,
    HUB_SLUG,
    REAL_CLIENT,
    STYLE_CATEGORIES,
    TIMELINE_STAGES,
    FaqItem,
    PhotoSlot,
    StageId,
    StyleCategory,
    StyleId,
    TimelineStage,
    all_leaf_slugs,
    image_path,
    leaf_slug,
    merge_stage_style_copy,
    photos_for,
    stage_by_id,
    style_by_id,
    style_hub_slug,
    universal_timeline_slug,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OG_DEFAULT = "/healed_tattoo_gallery_las_vegas/fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas"


def list_block(items: tuple[str, ...]) -> str:
    if not items:
        return ""
    rows = "".join(f"<li>{html.escape(s)}</li>" for s in items)
    return f'<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{rows}</ul>'


def faq_details(faqs: tuple[FaqItem, ...]) -> str:
    blocks = []
    for item in faqs:
        blocks.append(
            f"""<details class="border border-outline-variant/30 bg-surface-container-high p-5 group">
<summary class="font-headline-md text-on-surface cursor-pointer list-none">{html.escape(item.question)}</summary>
<p class="font-body-md text-on-surface-variant mt-4 leading-relaxed">{html.escape(item.answer)}</p>
</details>"""
        )
    return "\n".join(blocks)


def picture(slot: PhotoSlot, *, eager: bool = False) -> str:
    webp = image_path(slot.stem, slot.folder, webp=True)
    png = image_path(slot.stem, slot.folder, webp=False)
    loading = "eager" if eager else "lazy"
    return (
        f'<picture><source srcset="{webp}" type="image/webp"/>'
        f'<img alt="{html.escape(slot.alt)}" class="w-full h-auto object-cover" decoding="async" '
        f'height="800" loading="{loading}" src="{png}" width="800"/></picture>'
    )


def photo_gallery(slots: list[PhotoSlot], *, eager: bool = False) -> str:
    if not slots:
        return (
            '<p class="font-body-md text-on-surface-variant italic border border-outline-variant/30 '
            'bg-surface-container-low p-5">Studio photo for this style and stage is not yet documented. '
            f'See our <a class="text-secondary underline" href="{HEALED_HUB}">healed gallery</a> '
            f'and <a class="text-secondary underline" href="{REAL_CLIENT}">real client timeline</a> '
            "for available proof.</p>"
        )
    figures = []
    for i, slot in enumerate(slots):
        figures.append(
            f"""<figure class="border border-outline-variant/30 bg-surface overflow-hidden">
{picture(slot, eager=eager and i == 0)}
<figcaption class="p-3 font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(slot.caption)}</figcaption>
</figure>"""
        )
    grid = "grid-cols-1" if len(figures) == 1 else "grid-cols-1 sm:grid-cols-2"
    return f'<div class="grid {grid} gap-4">{"".join(figures)}</div>'


def timeline_nav(stage: TimelineStage, *, style: StyleCategory | None = None) -> str:
    links: list[tuple[str, str]] = []
    if stage.prev_stage:
        href = (
            f"/{leaf_slug(style.style_id, stage.prev_stage)}/"
            if style
            else f"/{universal_timeline_slug(stage.prev_stage)}/"
        )
        prev = stage_by_id(stage.prev_stage)
        links.append((f"← {prev.label}", href))
    if stage.next_stage:
        href = (
            f"/{leaf_slug(style.style_id, stage.next_stage)}/"
            if style
            else f"/{universal_timeline_slug(stage.next_stage)}/"
        )
        nxt = stage_by_id(stage.next_stage)
        links.append((f"{nxt.label} →", href))
    if not links:
        return ""
    row = " · ".join(
        f'<a class="text-secondary underline hover:no-underline" href="{html.escape(h)}">{html.escape(l)}</a>'
        for l, h in links
    )
    return f'<p class="font-body-md text-on-surface-variant pt-6">{row}</p>'


def related_links_block(*, style: StyleCategory | None = None, stage: TimelineStage | None = None) -> str:
    links = [
        ("Desert aftercare guide", AFTERCARE_GUIDE),
        ("Healed tattoo gallery", HEALED_HUB),
        ("Real client timeline", REAL_CLIENT),
        ("Book consult", BOOK),
    ]
    if style and style.healed_collection_slug:
        links.insert(2, (f"Healed {style.short_label.lower()} gallery", f"/{style.healed_collection_slug}/"))
    if style and style.style_guide_href:
        links.insert(1, ("Style authority guide", style.style_guide_href))
    if stage:
        links.insert(0, ("Healing Database hub", f"/{HUB_SLUG}/"))
    items = "".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}">'
        f"{html.escape(label)}</a></li>"
        for label, href in links
    )
    return f"""<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto">
<h2 class="font-headline-md text-on-surface text-xl mb-4">Related resources</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{items}</ul>
</div>
</section>"""


def stage_content_main(
    stage: TimelineStage,
    *,
    style: StyleCategory | None = None,
    title: str,
    description: str,
    breadcrumb: str,
) -> str:
    normal, watch, vegas = merge_stage_style_copy(stage, style)
    slots = photos_for(style.style_id if style else None, stage.stage_id)
    style_note = ""
    if style:
        style_note = f" · {html.escape(style.label)}"
    joshua = expert_callout(
        f"Healing at {stage.label}",
        (
            "I tell clients: week one looks rough on purpose — skin is rebuilding. "
            "We document heal stages so you compare to real photos, not anxiety."
        ),
        expert="joshua",
    )
    toc = toc_nav(
        (
            ("What to expect", "expect"),
            ("What's normal", "normal"),
            ("Watch for", "watch"),
            ("Call the studio", "studio"),
            ("See a doctor", "doctor"),
            ("Las Vegas notes", "vegas"),
            ("Studio photos", "photos"),
        )
    )
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
<p class="font-body-md text-on-surface-variant">{breadcrumb}</p>
{reviewed_by_block(expert="joshua")}
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Healing Database{style_note} · {html.escape(stage.day_range)}</span>
<h1 class="font-headline-xl text-on-surface leading-tight">{html.escape(title)}</h1>
<p class="font-body-lg text-on-surface-variant">{html.escape(description)}</p>
{toc}
{joshua}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-10">
<section class="space-y-3" id="expect">
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(stage.headline)}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(stage.intro)}</p>
</section>
<section class="space-y-3" id="normal">
<h2 class="font-headline-md text-on-surface text-2xl">What's normal</h2>
{list_block(normal)}
</section>
<section class="space-y-3" id="watch">
<h2 class="font-headline-md text-on-surface text-2xl">Watch for — not typical</h2>
{list_block(watch)}
</section>
<section class="space-y-3" id="studio">
<h2 class="font-headline-md text-on-surface text-2xl">Call Work of Art</h2>
{list_block(stage.call_studio)}
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="{BOOK}">Message or book</a> · (725) 224-1240</p>
</section>
<section class="space-y-3" id="doctor">
<h2 class="font-headline-md text-on-surface text-2xl">See a doctor</h2>
{list_block(stage.see_doctor)}
<p class="font-body-md text-on-surface-variant text-sm italic">We share general aftercare education — not medical advice.</p>
</section>
<section class="space-y-3" id="vegas">
<h2 class="font-headline-md text-on-surface text-2xl">Las Vegas desert notes</h2>
{list_block(vegas)}
</section>
<section class="space-y-4" id="photos">
<h2 class="font-headline-md text-on-surface text-2xl">Studio documentation</h2>
{photo_gallery(slots, eager=True)}
</section>
{timeline_nav(stage, style=style)}
</div>
</section>
{related_links_block(style=style, stage=stage)}
</main>"""


def hub_main() -> str:
    stage_cards = []
    for stage in TIMELINE_STAGES:
        slug = universal_timeline_slug(stage.stage_id)
        stage_cards.append(
            f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-5 hover:border-secondary transition-colors" href="/{slug}/">
<span class="font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(stage.day_range)}</span>
<h3 class="font-headline-md text-on-surface text-lg mt-1">{html.escape(stage.label)}</h3>
<p class="font-body-md text-on-surface-variant text-sm mt-2 line-clamp-2">{html.escape(stage.headline)}</p>
</a>"""
        )
    style_cards = []
    for style in STYLE_CATEGORIES:
        slug = style_hub_slug(style.style_id)
        style_cards.append(
            f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-6 hover:border-secondary transition-colors" href="/{slug}/">
<h3 class="font-headline-md text-on-surface text-xl">{html.escape(style.label)}</h3>
<p class="font-body-md text-on-surface-variant mt-3">{html.escape(style.description)}</p>
<span class="inline-block mt-4 font-label-caps text-[11px] uppercase tracking-widest text-secondary">12 timeline stages →</span>
</a>"""
        )
    featured = photos_for("black_grey", "day_1")[:1] + photos_for("black_grey", "month_3")[:1]
    featured_html = photo_gallery(featured, eager=True) if featured else ""

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
{reviewed_by_block(expert="joshua")}
{joshua_entity_block()}
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Healing encyclopedia</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Tattoo Healing Database — Timeline Encyclopedia</h1>
<p class="font-body-lg text-on-surface-variant max-w-2xl">You have healed photos. Now become the internet's healing encyclopedia — stage by stage, style by style. Day 1 through year 1, with Las Vegas desert notes and honest studio documentation where we have photographed the same client at that heal age.</p>
<p class="font-body-md text-on-surface-variant">84 style-specific pages plus universal timeline guides. Medical emergencies go to a clinician; aftercare timing and photo review come to us.</p>
<div class="flex flex-wrap gap-3 pt-2">
<a class="bg-secondary text-on-secondary px-8 py-4 font-label-caps tracking-widest" href="{BOOK}">Book consult</a>
<a class="border border-outline px-8 py-4 font-label-caps tracking-widest hover:border-secondary" href="{AFTERCARE_GUIDE}">Desert aftercare</a>
<a class="border border-outline px-8 py-4 font-label-caps tracking-widest hover:border-secondary" href="{HEALED_HUB}">Healed gallery</a>
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-4xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Featured proof — same client, two stages</h2>
{featured_html}
<p class="font-body-md text-on-surface-variant text-sm"><a class="text-secondary underline" href="{REAL_CLIENT}">Full cross/eye/skull client timeline (fresh → 1 year)</a></p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-6xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Universal timeline — all styles</h2>
<p class="font-body-md text-on-surface-variant max-w-2xl">General healing stages that apply to every tattoo. Start here if you are unsure which style bucket fits.</p>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
{"".join(stage_cards)}
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-6xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Browse by style — 12 stages each</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{"".join(style_cards)}
</div>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Common questions</h2>
<div class="space-y-3">{faq_details(HUB_FAQS)}</div>
</div>
</section>
</main>"""


def style_hub_main(style: StyleCategory) -> str:
    slug = style_hub_slug(style.style_id)
    stage_links = []
    for stage in TIMELINE_STAGES:
        leaf = leaf_slug(style.style_id, stage.stage_id)
        photo_count = len(photos_for(style.style_id, stage.stage_id))
        badge = f"{photo_count} photo{'s' if photo_count != 1 else ''}" if photo_count else "Education"
        stage_links.append(
            f"""<a class="flex justify-between items-start gap-4 border border-outline-variant/30 bg-surface-container-high p-4 hover:border-secondary transition-colors" href="/{leaf}/">
<div>
<span class="font-label-caps text-[10px] uppercase tracking-widest text-secondary">{html.escape(stage.day_range)}</span>
<h3 class="font-headline-md text-on-surface text-base mt-1">{html.escape(stage.label)}</h3>
</div>
<span class="font-label-caps text-[9px] uppercase tracking-widest text-on-surface-variant shrink-0">{badge}</span>
</a>"""
        )
    collection = ""
    if style.healed_collection_slug:
        collection = (
            f'<p class="font-body-md text-on-surface-variant">'
            f'<a class="text-secondary underline" href="/{style.healed_collection_slug}/">Healed {html.escape(style.short_label.lower())} gallery</a>'
            f" · documented client proof</p>"
        )
    guide = ""
    if style.style_guide_href:
        guide = f'<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="{style.style_guide_href}">Style authority guide</a></p>'

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="/{HUB_SLUG}/">← Healing Database</a></p>
{reviewed_by_block(expert="joshua")}
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Style hub</span>
<h1 class="font-headline-xl text-on-surface leading-tight">{html.escape(style.label)} Tattoo Healing — All Stages</h1>
<p class="font-body-lg text-on-surface-variant">{html.escape(style.description)}</p>
{collection}
{guide}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-3xl mx-auto space-y-4">
<h2 class="font-headline-md text-on-surface text-xl">Timeline — day 1 to year 1</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
{"".join(stage_links)}
</div>
<p class="font-body-md text-on-surface-variant text-sm pt-4">Universal stages (all styles): <a class="text-secondary underline" href="/{universal_timeline_slug("day_1")}/">start at day 1</a></p>
</div>
</section>
{related_links_block(style=style)}
</main>"""


def meta_for_hub() -> tuple[str, str]:
    title = "Tattoo Healing Database — Timeline Encyclopedia"
    desc = (
        "Day 1 through year 1 tattoo healing encyclopedia — black & grey, color, fine line, traditional, "
        "neo-traditional, cover-ups, and portraits. Las Vegas desert aftercare notes and honest studio photos."
    )
    return title, desc


def meta_for_style_hub(style: StyleCategory) -> tuple[str, str]:
    title = f"{style.label} Tattoo Healing Timeline — Las Vegas"
    desc = (
        f"How {style.short_label.lower()} tattoos heal day 1 to year 1 — what's normal, when to call the studio, "
        f"and desert-climate notes from Work of Art Las Vegas."
    )[:160]
    return title, desc


def meta_for_universal(stage: TimelineStage) -> tuple[str, str]:
    title = f"Tattoo Healing {stage.label} — What to Expect"
    desc = (
        f"{stage.headline}. Normal healing signs, red flags, and Las Vegas desert aftercare at "
        f"{stage.label.lower()} ({stage.day_range}). Work of Art Tattoo & Piercing."
    )[:160]
    return title, desc


def meta_for_leaf(style: StyleCategory, stage: TimelineStage) -> tuple[str, str]:
    title = f"{style.label} Tattoo Healing — {stage.label}"
    desc = (
        f"{style.short_label} tattoo at {stage.label.lower()} ({stage.day_range}): what's normal, "
        f"Vegas desert notes, and studio photos when documented. Work of Art Las Vegas."
    )[:160]
    return title, desc


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
        r'<link href="https://workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{canon}" rel="canonical"/>',
        page_html,
        count=1,
    )
    for prop in ("og:url",):
        page_html = re.sub(
            rf'<meta content="https://workofarttattoo.com/[^"]*" property="{prop}"/>',
            f'<meta content="{canon}" property="{prop}"/>',
            page_html,
            count=1,
        )
    og_img = f"{SITE}{og_path}.webp"
    page_html = re.sub(
        r'<meta content="https://workofarttattoo.com/[^"]*" property="og:image"/>',
        f'<meta content="{og_img}" property="og:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" property="og:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" property="og:description"/>',
        f'<meta content="{html.escape(description)}" property="og:description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="https://workofarttattoo.com/[^"]*" name="twitter:image"/>',
        f'<meta content="{og_img}" name="twitter:image"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" name="twitter:title"/>',
        f'<meta content="{html.escape(title)} | Work of Art" name="twitter:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" name="twitter:description"/>',
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


def inject_schema(page_html: str, slug: str, title: str, description: str, *, faqs: tuple[FaqItem, ...] = ()) -> str:
    page_html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page_html,
        flags=re.DOTALL,
    )
    if faqs:
        graph = faq_page_graph(slug=slug, title=title, faqs=[(f.question, f.answer) for f in faqs])
    else:
        graph = guide_article_graph(slug=slug, title=title, description=description, author_id=ID_JOSHUA)
    return page_html.replace("</head>", schema_script(graph) + "\n</head>", 1)


def write_page(
    slug: str,
    main: str,
    title: str,
    description: str,
    og_path: str,
    *,
    faqs: tuple[FaqItem, ...] = (),
) -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    out_dir = ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, slug, title, description, og_path)
    page = patch_main(page, main)
    page = inject_schema(page, slug, title, description, faqs=faqs)
    (out_dir / "code.html").write_text(page, encoding="utf-8")


def og_for_slots(slots: list[PhotoSlot]) -> str:
    if slots:
        return image_path(slots[0].stem, slots[0].folder, webp=False).replace(".png", "")
    return OG_DEFAULT


def main() -> int:
    hub_title, hub_desc = meta_for_hub()
    write_page(HUB_SLUG, hub_main(), hub_title, hub_desc, OG_DEFAULT, faqs=HUB_FAQS)
    print(f"[ok] {HUB_SLUG}/code.html")

    for style in STYLE_CATEGORIES:
        slug = style_hub_slug(style.style_id)
        title, desc = meta_for_style_hub(style)
        write_page(slug, style_hub_main(style), title, desc, OG_DEFAULT)
        print(f"[ok] {slug}/code.html")

    for stage in TIMELINE_STAGES:
        slug = universal_timeline_slug(stage.stage_id)
        title, desc = meta_for_universal(stage)
        breadcrumb = (
            f'<a class="text-secondary underline" href="/{HUB_SLUG}/">Healing Database</a> · Universal timeline'
        )
        main = stage_content_main(
            stage,
            title=title,
            description=desc,
            breadcrumb=breadcrumb,
        )
        slots = photos_for(None, stage.stage_id)
        write_page(slug, main, title, desc, og_for_slots(slots))
        print(f"[ok] {slug}/code.html")

    leaf_count = 0
    for style_id, stage_id, slug in all_leaf_slugs():
        style = style_by_id(style_id)
        stage = stage_by_id(stage_id)
        title, desc = meta_for_leaf(style, stage)
        breadcrumb = (
            f'<a class="text-secondary underline" href="/{HUB_SLUG}/">Healing Database</a> · '
            f'<a class="text-secondary underline" href="/{style_hub_slug(style_id)}/">{html.escape(style.label)}</a>'
        )
        main = stage_content_main(
            stage,
            style=style,
            title=title,
            description=desc,
            breadcrumb=breadcrumb,
        )
        slots = photos_for(style_id, stage_id)
        write_page(slug, main, title, desc, og_for_slots(slots))
        leaf_count += 1

    total = 1 + len(STYLE_CATEGORIES) + len(TIMELINE_STAGES) + leaf_count
    print(f"Done: {total} page(s) — hub + {len(STYLE_CATEGORIES)} style hubs + "
          f"{len(TIMELINE_STAGES)} universal + {leaf_count} leaf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

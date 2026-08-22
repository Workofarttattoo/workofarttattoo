#!/usr/bin/env python3
"""Build Skin Science hub + topic authority pages (Joshua Cole voice)."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import expert_callout, reviewed_by_block, toc_nav
from woa_entity_schema import ID_JOSHUA, guide_article_graph, schema_script
from woa_expert_entity_blocks import joshua_entity_block
from woa_skin_science import (
    BOOK,
    CATEGORY_LABELS,
    COVER_UP,
    DESERT_AFTERCARE,
    FINE_LINE,
    HEALED_HUB,
    HEALING_PROOF,
    HUB_INTRO,
    HUB_SLUG,
    HUB_TITLE,
    JOSHUA_PAGE,
    MEDICAL_DISCLAIMER,
    SKIN_SCIENCE_TOPICS,
    CategoryId,
    SkinScienceTopic,
    hub_meta_description,
    page_title,
    slug_for,
    topic_by_id,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OG_DEFAULT = "/healed_tattoo_gallery_las_vegas/fresh-all-seeing-eye-skull-elbow-joshua-cole-las-vegas"


def topics_for(category: CategoryId) -> list[SkinScienceTopic]:
    return [t for t in SKIN_SCIENCE_TOPICS if t.category == category]


def section_block(heading: str, bullets: tuple[str, ...], anchor: str = "") -> str:
    if not bullets:
        return ""
    aid = f' id="{html.escape(anchor)}"' if anchor else ""
    items = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
    slug_anchor = anchor or heading.lower().replace(" ", "-").replace("'", "")[:40]
    if not anchor:
        aid = f' id="{html.escape(slug_anchor)}"'
    return f"""<section class="space-y-4"{aid}>
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(heading)}</h2>
<ul class="font-body-md text-on-surface-variant space-y-3 list-disc pl-5">{items}</ul>
</section>"""


def medical_disclaimer_block() -> str:
    return f"""<aside class="border border-outline-variant/40 bg-surface-container-low p-6 my-6" data-woa-medical-disclaimer="1">
<p class="font-label-caps text-[10px] uppercase tracking-widest text-secondary mb-2">Medical disclaimer</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(MEDICAL_DISCLAIMER)}</p>
</aside>"""


def desert_section(bullets: tuple[str, ...]) -> str:
    if not bullets:
        return ""
    items = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
    return f"""<section class="space-y-4" id="desert-climate">
<h2 class="font-headline-md text-on-surface text-2xl">Las Vegas desert climate</h2>
<ul class="font-body-md text-on-surface-variant space-y-3 list-disc pl-5">{items}</ul>
<p class="font-body-md text-on-surface-variant text-sm">More: <a class="text-secondary underline" href="{DESERT_AFTERCARE}">Desert tattoo aftercare guide</a></p>
</section>"""


def faq_section(faqs: tuple[tuple[str, str], ...]) -> str:
    if not faqs:
        return ""
    rows = "".join(
        f"""<details class="border border-outline-variant/30 bg-surface-container-high p-5 group">
<summary class="font-headline-md text-on-surface cursor-pointer list-none flex justify-between items-center gap-4">
<span>{html.escape(q)}</span>
<span class="text-secondary font-label-caps text-xs">+</span>
</summary>
<p class="font-body-md text-on-surface-variant mt-4">{html.escape(a)}</p>
</details>"""
        for q, a in faqs
    )
    return f"""<section class="space-y-4" id="faq">
<h2 class="font-headline-md text-on-surface text-2xl">Common questions</h2>
{rows}
</section>"""


def related_section(topic: SkinScienceTopic) -> str:
    links: list[str] = []
    for rid in topic.related:
        rel = topic_by_id(rid)
        if rel:
            links.append(
                f'<li><a class="text-secondary underline hover:no-underline" href="/{slug_for(rel)}/">'
                f"{html.escape(rel.title)}</a></li>"
            )
    links.append(
        f'<li><a class="text-secondary underline hover:no-underline" href="/{HUB_SLUG}/">'
        "All skin science guides</a></li>"
    )
    return f"""<section class="space-y-4">
<h2 class="font-headline-md text-on-surface text-2xl">Related skin science</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">{"".join(links)}</ul>
</section>"""


def knowledge_graph_links() -> str:
    return f"""<section class="space-y-4 border border-outline-variant/30 bg-surface-container-low p-6">
<h2 class="font-headline-md text-on-surface text-xl">Connected studio guides</h2>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline" href="{DESERT_AFTERCARE}">Desert climate aftercare</a></li>
<li><a class="text-secondary underline" href="{HEALING_PROOF}">Fresh vs healed — real photos</a></li>
<li><a class="text-secondary underline" href="{HEALED_HUB}">Healed tattoo gallery</a></li>
<li><a class="text-secondary underline" href="{FINE_LINE}">Fine line tattoo guide</a></li>
<li><a class="text-secondary underline" href="{COVER_UP}">Cover-up tattoos</a></li>
<li><a class="text-secondary underline" href="{JOSHUA_PAGE}">Joshua Cole — artist page</a></li>
<li><a class="text-secondary underline" href="{BOOK}">Book a consult</a></li>
</ul>
</section>"""


def topic_card(topic: SkinScienceTopic) -> str:
    return f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-6 hover:border-secondary transition-colors group" href="/{slug_for(topic)}/">
<h3 class="font-headline-md text-on-surface text-lg group-hover:text-secondary transition-colors">{html.escape(topic.title)}</h3>
<p class="font-body-md text-on-surface-variant mt-3 line-clamp-3 text-sm">{html.escape(topic.intro[:160])}…</p>
<span class="inline-block mt-4 font-label-caps text-[11px] uppercase tracking-widest text-secondary">Read guide →</span>
</a>"""


def hub_main() -> str:
    category_blocks: list[str] = []
    for cat in ("layers", "permanence", "conditions"):
        items = topics_for(cat)
        if not items:
            continue
        cards = "\n".join(topic_card(t) for t in items)
        category_blocks.append(
            f"""<div class="space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">{html.escape(CATEGORY_LABELS[cat])}</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{cards}
</div>
</div>"""
        )
    grid = "\n\n".join(category_blocks)
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Skin science · Joshua Cole</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html.escape(HUB_TITLE)}</h1>
{reviewed_by_block(expert="joshua")}
{joshua_entity_block()}
<p class="font-body-lg text-on-surface-variant max-w-2xl leading-relaxed">{html.escape(HUB_INTRO)}</p>
<p class="font-body-md text-on-surface-variant">{html.escape(MEDICAL_DISCLAIMER)}</p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-6xl mx-auto space-y-14">
<h2 class="font-headline-md text-on-surface text-2xl">Explore by topic</h2>
{grid}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
{knowledge_graph_links()}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low text-center">
<div class="max-w-2xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface">Questions about your skin?</h2>
<p class="font-body-md text-on-surface-variant">Bring photos and medical history to a consult — we will tell you honestly if timing or placement needs adjustment.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="{BOOK}">Book consult</a>
<a class="border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors" href="{JOSHUA_PAGE}">Joshua's portfolio</a>
</div>
</div>
</section>
</main>"""


def topic_main(topic: SkinScienceTopic) -> str:
    toc_items: list[tuple[str, str]] = []
    for heading, _ in topic.sections:
        aid = heading.lower().replace(" ", "-").replace("'", "")[:40]
        toc_items.append((heading.split("—")[0].strip()[:28], aid))
    if topic.desert_bullets:
        toc_items.append(("Desert climate", "desert-climate"))
    if topic.faqs:
        toc_items.append(("FAQ", "faq"))
    toc_items.append(("Book", "book"))

    sections_html = "\n".join(
        section_block(h, bullets, anchor=h.lower().replace(" ", "-").replace("'", "")[:40])
        for h, bullets in topic.sections
    )

    expert = expert_callout(topic.title.split("—")[0].strip(), topic.joshua_quote, expert="joshua") if topic.joshua_quote else ""
    disclaimer = medical_disclaimer_block() if topic.medical else ""

    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-6">
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="/{HUB_SLUG}/">← Skin Science hub</a></p>
{reviewed_by_block(expert="joshua")}
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Skin science · {html.escape(CATEGORY_LABELS[topic.category])}</span>
<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">{html.escape(topic.title)}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed">{html.escape(topic.intro)}</p>
{disclaimer}
{toc_nav(tuple(toc_items))}
{expert}
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-3xl mx-auto space-y-12">
{sections_html}
{desert_section(topic.desert_bullets)}
{faq_section(topic.faqs)}
{related_section(topic)}
{knowledge_graph_links()}
<section class="space-y-4 pt-4" id="book">
<h2 class="font-headline-md text-on-surface text-2xl">Book a consult</h2>
<p class="font-body-md text-on-surface-variant">Joshua Cole tattoos at Work of Art on E. Tropicana — seven nights a week. Bring questions about your skin; we plan sessions around honest heal expectations.</p>
<div class="flex flex-col sm:flex-row gap-4 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest justify-center" href="{BOOK}">Book appointment</a>
<a class="inline-flex border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary transition-colors justify-center" href="{JOSHUA_PAGE}">Joshua's portfolio</a>
</div>
</section>
</div>
</section>
</main>"""


def patch_meta(page_html: str, slug: str, title: str, description: str) -> str:
    canon = f"{SITE}/{slug}/"
    og = f"{SITE}{OG_DEFAULT}.webp"
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
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/tattoo[^"]*" property="og:url"/>',
        f'<meta content="{canon}" property="og:url"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" property="og:image"/>',
        f'<meta content="{og}" property="og:image"/>',
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
        r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" name="twitter:image"/>',
        f'<meta content="{og}" name="twitter:image"/>',
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


def inject_schema(
    page_html: str,
    slug: str,
    title: str,
    description: str,
    faqs: list[tuple[str, str]] | None = None,
) -> str:
    page_html = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page_html,
        flags=re.DOTALL,
    )
    graph = guide_article_graph(
        slug=slug,
        title=title,
        description=description,
        author_id=ID_JOSHUA,
        faqs=faqs,
    )
    return page_html.replace("</head>", schema_script(graph) + "\n</head>", 1)


def write_page(
    slug: str,
    main: str,
    title: str,
    description: str,
    faqs: list[tuple[str, str]] | None = None,
) -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    out_dir = ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, slug, title, description)
    page = patch_main(page, main)
    page = inject_schema(page, slug, title, description, faqs)
    (out_dir / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {slug}/code.html")


def main() -> int:
    write_page(HUB_SLUG, hub_main(), HUB_TITLE, hub_meta_description())

    for topic in SKIN_SCIENCE_TOPICS:
        slug = slug_for(topic)
        title = page_title(topic)
        desc = topic.meta_description
        faqs = list(topic.faqs) if topic.faqs else None
        write_page(slug, topic_main(topic), title, desc, faqs)

    print(f"Done: hub + {len(SKIN_SCIENCE_TOPICS)} skin science topic page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

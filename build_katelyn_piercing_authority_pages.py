#!/usr/bin/env python3
"""Build Katelyn Cole piercing authority topic hub + pages."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import reviewed_by_block
from woa_entity_schema import ID_KATELYN, guide_article_graph, schema_script
from woa_katelyn_piercing_topics import (
    BOOK,
    DESERT,
    ENCYCLOPEDIA,
    HUB_INTRO,
    HUB_SLUG,
    HUB_TITLE,
    KATELYN_PAGE,
    KATELYN_TOPICS,
    KatelynTopic,
    slug_for,
    topic_by_id,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OG = "/studio_gallery/ear-lobe-piercing-session-da19eec5"


def patch_meta(page_html: str, slug: str, title: str, description: str) -> str:
    canon = f"{SITE}/{slug}/"
    page_html = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | Work of Art</title>", page_html, count=1)
    page_html = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{html.escape(description)}" name="description"/>', page_html, count=1)
    page_html = re.sub(r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>', f'<link href="{canon}" rel="canonical"/>', page_html, count=1)
    og = f"{SITE}{OG}.webp"
    page_html = re.sub(r'<meta content="https://www.workofarttattoo.com/how_much[^"]*" property="og:image"/>', f'<meta content="{og}" property="og:image"/>', page_html, count=1)
    page_html = re.sub(r'<meta content="https://www.workofarttattoo.com/tattoo_healing[^"]*" property="og:url"/>', f'<meta content="{canon}" property="og:url"/>', page_html, count=1)
    return page_html


def patch_main(page_html: str, main: str) -> str:
    return re.sub(r'<main class="relative pt-20">.*?</main>', main.strip(), page_html, count=1, flags=re.DOTALL)


def write_page(slug: str, main: str, title: str, desc: str, faqs: list[tuple[str, str]] | None = None) -> None:
    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, slug, title, desc)
    page = patch_main(page, main)
    page = re.sub(r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*', "", page, flags=re.DOTALL)
    graph = guide_article_graph(slug=slug, title=title, description=desc, author_id=ID_KATELYN, faqs=faqs)
    page = page.replace("</head>", schema_script(graph) + "\n</head>", 1)
    out = ROOT / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "code.html").write_text(page, encoding="utf-8")
    print(f"[ok] {slug}/code.html")


def hub_main() -> str:
    cards = []
    for t in KATELYN_TOPICS:
        cards.append(
            f"""<a class="block border border-outline-variant/30 bg-surface-container-high p-6 hover:border-secondary transition-colors" href="/{slug_for(t)}/">
<h3 class="font-headline-md text-on-surface text-lg">{html.escape(t.title)}</h3>
<p class="font-body-md text-on-surface-variant mt-2 text-sm line-clamp-2">{html.escape(t.intro[:140])}…</p>
</a>"""
        )
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-4xl space-y-6">
<span class="font-label-caps text-secondary uppercase tracking-[0.2em]">Katelyn Cole · master piercer</span>
<h1 class="font-headline-xl text-on-surface">{html.escape(HUB_TITLE)}</h1>
{reviewed_by_block(expert="katelyn")}
<p class="font-body-lg text-on-surface-variant">{html.escape(HUB_INTRO)}</p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline" href="{ENCYCLOPEDIA}">Piercing encyclopedia</a> · <a class="text-secondary underline" href="{DESERT}">Desert piercing aftercare</a> · <a class="text-secondary underline" href="/studio_videos/#katelyn-piercing">Videos</a></p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20">
<div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{"".join(cards)}
</div>
</section>
<section class="py-section-gap text-center">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps tracking-widest" href="{BOOK}">Book with Katelyn</a>
</section>
</main>"""


def topic_main(topic: KatelynTopic) -> str:
    sections = []
    for heading, bullets in topic.sections:
        items = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
        sections.append(
            f"""<section class="space-y-4"><h2 class="font-headline-md text-on-surface text-2xl">{html.escape(heading)}</h2>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">{items}</ul></section>"""
        )
    related = []
    for rid in topic.related:
        rt = topic_by_id(rid)
        if rt:
            related.append(f'<li><a class="text-secondary underline" href="/{slug_for(rt)}/">{html.escape(rt.title)}</a></li>')
    faq = ""
    if topic.faqs:
        faq = "<section class='space-y-4'><h2 class='font-headline-md text-on-surface text-2xl'>FAQ</h2>" + "".join(
            f"<p class='font-body-md text-on-surface-variant'><strong class='text-on-surface'>{html.escape(q)}</strong> {html.escape(a)}</p>"
            for q, a in topic.faqs
        ) + "</section>"
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background max-w-3xl mx-auto space-y-8">
<p><a class="text-secondary underline" href="/{HUB_SLUG}/">← Katelyn Cole piercing authority</a></p>
<h1 class="font-headline-xl text-on-surface">{html.escape(topic.title)}</h1>
<p class="font-body-lg text-on-surface-variant">{html.escape(topic.intro)}</p>
<p class="font-body-md text-on-surface-variant italic">— Katelyn Cole, master piercer, Work of Art Las Vegas</p>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop max-w-3xl mx-auto space-y-10">
{"".join(sections)}
{faq}
<section><h2 class="font-headline-md text-on-surface text-2xl mb-4">Related topics</h2><ul class="font-body-md text-on-surface-variant space-y-2">{"".join(related)}</ul></section>
<div class="flex gap-4 flex-wrap"><a class="bg-secondary text-on-secondary px-8 py-3 font-label-caps tracking-widest" href="{BOOK}">Book consult</a><a class="border border-outline px-8 py-3 font-label-caps tracking-widest" href="{KATELYN_PAGE}">Portfolio</a></div>
</section>
</main>"""


def main() -> int:
    write_page(HUB_SLUG, hub_main(), HUB_TITLE, HUB_INTRO[:155])
    for t in KATELYN_TOPICS:
        slug = slug_for(t)
        write_page(slug, topic_main(t), t.title, t.intro[:155], list(t.faqs) if t.faqs else None)
    print(f"Done: hub + {len(KATELYN_TOPICS)} Katelyn topic pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

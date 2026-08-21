#!/usr/bin/env python3
"""Build /knowledge/ hub and focused Q&A answer pages for AI + long-tail SEO."""

from __future__ import annotations

import html
import shutil
from pathlib import Path

from knowledge_qa_data import KNOWLEDGE_CATEGORIES, KNOWLEDGE_QA
from woa_entity_schema import faq_page_graph, schema_script

ROOT = Path(__file__).resolve().parent
KNOWLEDGE = ROOT / "knowledge"
SITE = "https://workofarttattoo.com"

HEAD_LINKS = """<link href="/home_work_of_art_tattoo_piercing/woa-tailwind.min.css" rel="stylesheet"/>
<link href="/home_work_of_art_tattoo_piercing/woa-typography.css" rel="stylesheet"/>"""


def qa_page_html(slug: str, question: str, answer: str, guide_slug: str) -> str:
    guide_href = f"/{guide_slug}/"
    guide_title = guide_slug.replace("_", " ").replace("authority guide", "").strip().title()
    graph = faq_page_graph(slug=f"knowledge/{slug}", title=question, faqs=[(question, answer)])
    return f"""<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{html.escape(question)} | Work of Art Knowledge</title>
<meta content="{html.escape(answer[:155])}" name="description"/>
<link href="{SITE}/knowledge/{slug}/" rel="canonical"/>
{HEAD_LINKS}
{schema_script(graph)}
</head>
<body class="bg-background text-on-surface antialiased">
<nav class="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-md border-b border-outline-variant/30 flex justify-between items-center px-6 py-4">
<a class="font-headline-md text-secondary uppercase tracking-widest" href="/">Work of Art</a>
<a class="bg-secondary text-on-secondary px-6 py-3 font-label-caps text-label-caps uppercase tracking-widest" href="/appointments/">Book Now</a>
</nav>
<main class="pt-28 pb-24 px-6 max-w-3xl mx-auto">
<p class="font-label-caps text-secondary uppercase tracking-widest text-sm mb-4"><a class="hover:underline" href="/knowledge/">Knowledge Base</a></p>
<h1 class="font-headline-lg text-on-surface mb-6">{html.escape(question)}</h1>
<p class="font-body-lg text-on-surface-variant leading-relaxed mb-8">{html.escape(answer)}</p>
<p class="font-body-md text-on-surface-variant mb-4"><strong class="text-on-surface">Related guide:</strong> <a class="text-secondary underline hover:no-underline" href="{guide_href}">{html.escape(guide_title)}</a></p>
<p class="font-body-md text-on-surface-variant"><a class="text-secondary underline hover:no-underline" href="/appointments/">Book a consult</a> · <a class="text-secondary underline hover:no-underline" href="/artists/">Meet our artists</a> · <a class="text-secondary underline hover:no-underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">Desert aftercare guide</a></p>
</main>
</body></html>
"""


def hub_sections_html() -> str:
    by_cat: dict[str, list[tuple[str, str, str]]] = {c: [] for c in KNOWLEDGE_CATEGORIES}
    for slug, category, question, answer, _guide in KNOWLEDGE_QA:
        by_cat.setdefault(category, []).append((slug, question, answer))

    sections: list[str] = []
    for category in KNOWLEDGE_CATEGORIES:
        items = by_cat.get(category, [])
        if not items:
            continue
        cards = []
        for slug, question, answer in items:
            snippet = answer if len(answer) <= 160 else answer[:157].rstrip() + "…"
            cards.append(
                f'<li class="border border-outline-variant/30 p-4 bg-surface-container-low hover:border-secondary/40 transition-colors">'
                f'<a class="block" href="/knowledge/{slug}/">'
                f'<h3 class="font-headline-md text-on-surface mb-1 text-[1.05rem]">{html.escape(question)}</h3>'
                f'<p class="font-body-md text-on-surface-variant text-sm">{html.escape(snippet)}</p>'
                f"</a></li>"
            )
        sections.append(
            f'<section class="mb-12"><h2 class="font-label-caps text-secondary uppercase tracking-widest text-sm mb-4">{html.escape(category)}</h2>'
            f'<ul class="space-y-3">{"".join(cards)}</ul></section>'
        )
    return "\n".join(sections)


def hub_html() -> str:
    faqs = [(q, a) for _s, _c, q, a, _g in KNOWLEDGE_QA[:12]]
    graph = faq_page_graph(
        slug="knowledge",
        title="Tattoo & Piercing Knowledge Base — Work of Art Las Vegas",
        faqs=faqs,
    )
    count = len(KNOWLEDGE_QA)
    return f"""<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Tattoo &amp; Piercing Knowledge Base | Work of Art Las Vegas</title>
<meta content="Factual answers on tattoo healing, pricing, placement, piercing, cover-ups, and choosing a Las Vegas studio — Work of Art Tattoo &amp; Piercing." name="description"/>
<link href="{SITE}/knowledge/" rel="canonical"/>
{HEAD_LINKS}
{schema_script(graph)}
</head>
<body class="bg-background text-on-surface antialiased">
<nav class="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-md border-b border-outline-variant/30 flex justify-between items-center px-6 py-4">
<a class="font-headline-md text-secondary uppercase tracking-widest" href="/">Work of Art</a>
<a class="bg-secondary text-on-secondary px-6 py-3 font-label-caps text-label-caps uppercase tracking-widest" href="/appointments/">Book Now</a>
</nav>
<main class="pt-28 pb-24 px-6 max-w-4xl mx-auto">
<h1 class="font-headline-lg text-on-surface mb-4">Knowledge Base</h1>
<p class="font-body-lg text-on-surface-variant mb-4">{count} direct answers on tattoo and piercing — written for clarity, not keyword stuffing. Each page covers one question. For long-form guides, see our <a class="text-secondary underline hover:no-underline" href="/#knowledge-base">Insider Guides vault</a>.</p>
<p class="font-body-md text-on-surface-variant mb-10">Medical questions beyond aftercare basics should go to a licensed clinician. We share studio practice and general industry facts — not personal medical advice.</p>
{hub_sections_html()}
</main>
</body></html>
"""


def cleanup_orphan_slugs(valid: set[str]) -> None:
    if not KNOWLEDGE.is_dir():
        return
    for child in KNOWLEDGE.iterdir():
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name not in valid and (child / "code.html").is_file():
            shutil.rmtree(child)
            print(f"[del] orphan knowledge/{child.name}/")


def main() -> int:
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    valid_slugs = {slug for slug, *_rest in KNOWLEDGE_QA}
    cleanup_orphan_slugs(valid_slugs)

    (KNOWLEDGE / "code.html").write_text(hub_html(), encoding="utf-8")
    print(f"[ok] knowledge/code.html ({len(KNOWLEDGE_QA)} topics)")

    for slug, _cat, question, answer, guide in KNOWLEDGE_QA:
        out_dir = KNOWLEDGE / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "code.html").write_text(
            qa_page_html(slug, question, answer, guide),
            encoding="utf-8",
        )
    print(f"[ok] {len(KNOWLEDGE_QA)} answer page(s) written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

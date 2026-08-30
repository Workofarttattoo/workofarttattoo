#!/usr/bin/env python3
"""Build /start_here/ — intent-based hub that routes visitors to the right guides."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_entity_schema import faq_page_graph, schema_script
from woa_start_here import (
    HREF_START_HERE,
    START_HERE_META,
    START_HERE_PATHS,
    START_HERE_SLUG,
    START_HERE_TITLE,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
TEMPLATE = ROOT / "tattoo_healing_in_desert_climate_expert_aftercare_guide" / "code.html"
OUT_DIR = ROOT / START_HERE_SLUG
BOOK = "/appointments/"


def path_card(path) -> str:
    link_items = "".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{html.escape(href)}" '
        f'data-woa-start-here-selection="{html.escape(path.anchor)}" data-woa-start-here-link-type="secondary">'
        f"{html.escape(label)}</a></li>"
        for label, href in path.links
    )
    return f"""<article class="woa-start-card border border-outline-variant/30 bg-surface-container-high p-6 md:p-8 flex flex-col gap-4" id="{html.escape(path.anchor)}">
<h2 class="font-headline-md text-on-surface text-xl md:text-2xl leading-snug">{html.escape(path.title)}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed flex-1">{html.escape(path.summary)}</p>
<a class="inline-flex self-start bg-secondary text-on-secondary px-8 py-3 font-label-caps text-label-caps tracking-widest hover:opacity-90 transition-opacity" href="{html.escape(path.primary_href)}" data-woa-start-here-selection="{html.escape(path.anchor)}" data-woa-start-here-link-type="primary">{html.escape(path.primary_label)}</a>
<ul class="font-body-md text-on-surface-variant space-y-1.5 list-none pt-2 border-t border-outline-variant/20">{link_items}</ul>
</article>"""


def jump_nav() -> str:
    items = "".join(
        f'<a class="woa-start-jump px-3 py-2 border border-outline-variant/40 text-on-surface-variant hover:border-secondary hover:text-secondary transition-colors text-sm whitespace-nowrap" '
        f'href="#{html.escape(p.anchor)}" data-woa-start-here-selection="{html.escape(p.anchor)}" data-woa-start-here-link-type="jump">{html.escape(p.title)}</a>'
        for p in START_HERE_PATHS
    )
    return f"""<nav aria-label="Jump to your situation" class="flex flex-wrap gap-2 justify-center mb-12">{items}</nav>"""


def intent_router() -> str:
    return f"""<nav aria-label="Choose your path" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mb-10">
<a class="flex flex-col items-center justify-center gap-2 border border-outline-variant/40 bg-surface-container-high px-4 py-5 hover:border-secondary transition-colors text-center" href="/appointments/" data-woa-start-here-selection="router-tattoo" data-woa-start-here-link-type="router">
<span class="material-symbols-outlined text-secondary text-2xl">brush</span>
<span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface">Tattoo</span>
</a>
<a class="flex flex-col items-center justify-center gap-2 border border-outline-variant/40 bg-surface-container-high px-4 py-5 hover:border-secondary transition-colors text-center" href="/piercing-guide-las-vegas/" data-woa-start-here-selection="router-piercing" data-woa-start-here-link-type="router">
<span class="material-symbols-outlined text-secondary text-2xl">diamond</span>
<span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface">Piercing</span>
</a>
<a class="flex flex-col items-center justify-center gap-2 border border-outline-variant/40 bg-surface-container-high px-4 py-5 hover:border-secondary transition-colors text-center" href="/cover-up-tattoos-las-vegas/" data-woa-start-here-selection="router-cover-up" data-woa-start-here-link-type="router">
<span class="material-symbols-outlined text-secondary text-2xl">layers</span>
<span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface">Cover-Up</span>
</a>
<a class="flex flex-col items-center justify-center gap-2 border border-outline-variant/40 bg-surface-container-high px-4 py-5 hover:border-secondary transition-colors text-center" href="/artists/" data-woa-start-here-selection="router-artists" data-woa-start-here-link-type="router">
<span class="material-symbols-outlined text-secondary text-2xl">groups</span>
<span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface">View Artists</span>
</a>
<a class="flex flex-col items-center justify-center gap-2 border border-secondary bg-secondary/10 px-4 py-5 hover:bg-secondary/20 transition-colors text-center sm:col-span-3 lg:col-span-1" href="{BOOK}" data-woa-start-here-selection="router-book" data-woa-start-here-link-type="router">
<span class="material-symbols-outlined text-secondary text-2xl">calendar_month</span>
<span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface">Book Now</span>
</a>
</nav>"""


def main_content() -> str:
    cards = "\n".join(path_card(p) for p in START_HERE_PATHS)
    return f"""<main class="relative pt-20">
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background">
<div class="max-w-5xl mx-auto">
<span class="font-label-caps text-secondary uppercase tracking-[0.2em] mb-4 block text-center">Work of Art · Las Vegas</span>
<h1 class="font-headline-xl text-on-surface text-center leading-tight mb-6">{html.escape(START_HERE_TITLE)}</h1>
{intent_router()}
<p class="font-body-md text-on-surface-variant text-center max-w-2xl mx-auto mb-8 leading-relaxed">
Pick the situation closest to yours — or jump straight to booking. Each path links to the guides we use in consults.
</p>
{jump_nav()}
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">{cards}</div>
<div class="mt-14 pt-10 border-t border-outline-variant/20 text-center space-y-4">
<p class="font-body-md text-on-surface-variant">Ready to book? <a class="text-secondary underline hover:no-underline" href="{BOOK}">Request an appointment</a> · <a class="text-secondary underline hover:no-underline" href="/official_location_hours_contact/">Hours &amp; directions</a></p>
<p class="font-body-md text-on-surface-variant text-sm">Browse everything: <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Piercing guides</a> · <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">Healed galleries</a> · <a class="text-secondary underline hover:no-underline" href="/knowledge/">Q&amp;A answers</a></p>
</div>
</div>
</section>
</main>"""


def patch_meta(page_html: str, title: str, description: str) -> str:
    canon = f"{SITE}/{START_HERE_SLUG}/"
    esc_title = html.escape(f"{title} | Work of Art Las Vegas")
    esc_desc = html.escape(description)
    page_html = re.sub(r"<title>.*?</title>", f"<title>{esc_title}</title>", page_html, count=1)
    page_html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{esc_desc}" name="description"/>',
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
        r'<meta content="https://www.workofarttattoo.com/[^"]*" property="og:url"/>',
        f'<meta content="{canon}" property="og:url"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{esc_title}" property="og:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" property="og:description"/>',
        f'<meta content="{esc_desc}" property="og:description"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" name="twitter:title"/>',
        f'<meta content="{esc_title}" name="twitter:title"/>',
        page_html,
        count=1,
    )
    page_html = re.sub(
        r'<meta content="[^"]*" name="twitter:description"/>',
        f'<meta content="{esc_desc}" name="twitter:description"/>',
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


def entity_graph() -> dict:
    faqs = [(p.title, p.summary) for p in START_HERE_PATHS]
    return faq_page_graph(
        slug=START_HERE_SLUG,
        title=f"{START_HERE_TITLE} — Work of Art Tattoo & Piercing Las Vegas",
        faqs=faqs,
    )


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    page = TEMPLATE.read_text(encoding="utf-8")
    page = patch_meta(page, START_HERE_TITLE, START_HERE_META)
    page = patch_main(page, main_content())
    page = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\+json">.*?</script>\s*',
        "",
        page,
        flags=re.DOTALL,
    )
    graph = entity_graph()
    insert = schema_script(graph)
    page = page.replace("</head>", f"{insert}\n</head>", 1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "code.html"
    out_path.write_text(page, encoding="utf-8")
    print(f"[ok] {START_HERE_SLUG}/code.html ({len(START_HERE_PATHS)} intent paths → {HREF_START_HERE})")

    # Template overwrite drops injected nav — re-apply desktop + mobile nav.
    from upgrade_site_navigation import upgrade_file

    if upgrade_file(out_path):
        print(f"[ok] navigation applied to {START_HERE_SLUG}/code.html")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

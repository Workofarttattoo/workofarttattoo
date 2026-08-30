#!/usr/bin/env python3
"""Inject tattoo FAQs + meta — no duplicate hero blocks on pages that already have Joshua's voice."""

from __future__ import annotations

import html
import re
from pathlib import Path

from woa_content_standards import expert_callout, reviewed_by_block
from woa_tattoo_seo import (
    BOOK,
    JOSHUA_PAGE,
    TATTOO_GUIDES,
    TattooGuideSEO,
    conversion_bar,
    meta_description,
    page_title,
    seo_faqs,
)

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
FAQ_MARKER = 'data-woa-tattoo-faq="1"'
SEO_MARKER = 'data-woa-tattoo-seo="1"'
SLEEVE_BRIDGE_MARKER = 'data-woa-sleeve-commercial-bridge="1"'


def strip_injected(html_text: str) -> str:
    html_text = re.sub(
        rf'<section[^>]*{re.escape(SEO_MARKER)}[^>]*>.*?</section>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    html_text = re.sub(
        rf'<section[^>]*{re.escape(FAQ_MARKER)}[^>]*>.*?</section>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<aside[^>]*data-woa-tattoo-cta="1"[^>]*>.*?</aside>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    html_text = re.sub(
        rf'<section[^>]*{re.escape(SLEEVE_BRIDGE_MARKER)}[^>]*>.*?</section>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    return html_text


def patch_meta(html_text: str, guide: TattooGuideSEO) -> str:
    title = page_title(guide)
    desc = meta_description(guide)
    full_title = f"{html.escape(title)} | Work of Art"
    esc_desc = html.escape(desc)

    html_text = re.sub(r"<title>.*?</title>", f"<title>{full_title}</title>", html_text, count=1)
    html_text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{esc_desc}" name="description"/>',
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{full_title}" property="og:title"/>',
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'<meta content="[^"]*" property="og:description"/>',
        f'<meta content="{esc_desc}" property="og:description"/>',
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'<meta content="[^"]*" name="twitter:title"/>',
        f'<meta content="{full_title}" name="twitter:title"/>',
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'<meta content="[^"]*" name="twitter:description"/>',
        f'<meta content="{esc_desc}" name="twitter:description"/>',
        html_text,
        count=1,
    )
    return html_text


def faq_section(guide: TattooGuideSEO, *, page_html: str) -> str:
    note = ""
    if "Joshua's Studio Notes" not in page_html:
        note = expert_callout(guide.style_label, guide.joshua_note, expert="joshua")

    rows = "".join(
        f"""<details class="border border-outline-variant/30 bg-surface-container-high p-5 group">
<summary class="font-headline-md text-on-surface cursor-pointer list-none flex justify-between gap-4">
<span>{html.escape(q)}</span>
<span class="text-secondary font-label-caps text-xs">+</span>
</summary>
<p class="font-body-md text-on-surface-variant mt-4">{html.escape(a)}</p>
</details>"""
        for q, a in seo_faqs(guide)
    )
    return f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" {FAQ_MARKER}>
<div class="max-w-3xl mx-auto space-y-6">
{reviewed_by_block(expert="joshua")}
{note}
<h2 class="font-headline-md text-on-surface text-2xl">Questions clients ask</h2>
{rows}
{conversion_bar(guide, compact=True)}
</div>
</section>"""


def inject_before_main_close(html_text: str, block: str) -> str:
    return html_text.replace("</main>", block + "\n</main>", 1)


def sleeve_commercial_bridge() -> str:
    return f"""<section class="py-10 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" {SLEEVE_BRIDGE_MARKER}>
<div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-8 items-center">
<div class="space-y-3">
<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-[10px]">Planning a sleeve in Las Vegas?</p>
<h2 class="font-headline-md text-on-surface text-2xl">Turn sleeve ideas into a real project plan</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">Use this guide to compare sleeve styles, then move into Joshua's large-scale portfolio, healed work, pricing expectations, and a consultation when you are ready to map flow, sessions, and budget.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 min-w-[min(100%,360px)]">
<a class="inline-flex border border-outline px-5 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary justify-center" href="{JOSHUA_PAGE}">Joshua's large-scale work</a>
<a class="inline-flex border border-outline px-5 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary justify-center" href="/healed_sleeve_tattoos_las_vegas/">Healed sleeve work</a>
<a class="inline-flex border border-outline px-5 py-3 font-label-caps text-[11px] uppercase tracking-widest hover:border-secondary justify-center" href="/how_much_do_tattoos_cost_in_las_vegas_authority_guide/">Project pricing</a>
<a class="inline-flex bg-secondary text-on-secondary px-5 py-3 font-label-caps text-[11px] uppercase tracking-widest justify-center" href="{BOOK}">Book consultation</a>
</div>
</div>
</section>"""


def inject_after_first_section(html_text: str, block: str) -> str:
    match = re.search(r"</section>", html_text, flags=re.IGNORECASE)
    if not match:
        return inject_before_main_close(html_text, block)
    return html_text[: match.end()] + "\n" + block + html_text[match.end():]


def inject_page(html_text: str, guide: TattooGuideSEO) -> str:
    html_text = strip_injected(html_text)
    html_text = patch_meta(html_text, guide)
    if guide.slug == "best_tattoo_styles_for_sleeves_large_scale_project_hub":
        html_text = inject_after_first_section(html_text, sleeve_commercial_bridge())
    html_text = inject_before_main_close(html_text, faq_section(guide, page_html=html_text))
    return html_text


def main() -> int:
    changed = 0
    for slug in TATTOO_GUIDES:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            print(f"[skip] missing {slug}/code.html")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject_page(raw, TATTOO_GUIDES[slug])
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {slug}")
    print(f"Done: tattoo voice + FAQ on {changed} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

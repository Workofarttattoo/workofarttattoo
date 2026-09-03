#!/usr/bin/env python3
"""Surgical GSC SEO sprint — priority pages only, no wholesale rewrites."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# --- Meta patches: (title, description) — surgical CTR/local intent only ---
META_PATCHES: dict[str, tuple[str, str]] = {
    "home_work_of_art_tattoo_piercing/code.html": (
        "Tattoo & Piercing Shop Las Vegas | Work of Art",
        "Las Vegas tattoo and piercing studio — custom tattoos, realism, cover-ups, fine line work, and professional body piercing. Walk-ins and appointments on E. Tropicana. (725) 224-1240.",
    ),
    "cover-up-tattoos-las-vegas/code.html": (
        "Cover-Up Tattoo Artist Las Vegas | Joshua Cole | Work of Art",
        "Cover-up tattoo artist in Las Vegas — Joshua Cole plans redesigns, scar work, and healed proof at Work of Art on E. Tropicana. Book a consult or send photos.",
    ),
    "tattoo_shop_near_the_strip_nap_corrected/code.html": (
        "Tattoo & Piercing Shop Near Me — Las Vegas Strip | Work of Art",
        "Tattoo and piercing shop minutes from the Las Vegas Strip — Work of Art on E. Tropicana. Custom tattoos, cover-ups, fine line, and professional piercing. Directions, artists, booking.",
    ),
}


def patch_title_desc(html: str, title: str, description: str) -> str:
    html = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1)
    html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{description}" name="description"/>',
        html,
        count=1,
    )
    for prop in ("og:title", "twitter:title"):
        html = re.sub(
            rf'<meta content="[^"]*" property="{prop}"/>',
            f'<meta content="{title}" property="{prop}"/>',
            html,
            count=1,
        )
        html = re.sub(
            rf'<meta content="[^"]*" name="{prop.replace("og:", "")}"/>',
            f'<meta content="{title}" name="{prop}"/>',
            html,
            count=1,
        )
    for prop in ("og:description", "twitter:description"):
        tag = "property" if prop.startswith("og:") else "name"
        html = re.sub(
            rf'<meta content="[^"]*" {tag}="{prop}"/>',
            f'<meta content="{description}" {tag}="{prop}"/>',
            html,
            count=1,
        )
    return html


def patch_homepage_local_link(html: str) -> str:
    needle = (
        '<p class="font-body-md text-on-surface-variant text-sm pt-1">'
        '<a aria-label="2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119"'
    )
    insert = (
        '<p class="font-body-md text-on-surface-variant text-sm">'
        'Looking for a tattoo and piercing shop near the Strip? '
        '<a class="text-secondary underline hover:no-underline" href="/tattoo_shop_near_the_strip_nap_corrected/">'
        'Directions from major resorts</a> · '
        '<a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">'
        'Professional piercing in Las Vegas</a> · '
        '<a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">'
        'Cover-up tattoos</a>'
        '</p>\n'
    )
    if "tattoo and piercing shop near the Strip" in html:
        return html
    if needle in html:
        return html.replace(needle, insert + needle, 1)
    return html


def patch_coverup_reviews(html: str) -> str:
    html = html.replace(
        "Embedded from verified Google-style feedback — same trust signals we show in-studio.",
        "In-studio client feedback — for verified Google reviews, see our reviews page.",
    )
    html = html.replace(
        '<span class="material-symbols-outlined text-on-surface-variant">google</span>',
        "",
    )
    # Strengthen outbound entity links near hero CTAs
    hero_cta = 'href="#studio-portfolio">VIEW REAL WORK</a>'
    realism_cta = 'href="/realism-tattoos-las-vegas/">BLACK &amp; GREY REALISM</a>'
    if realism_cta not in html and hero_cta in html:
        html = html.replace(
            '<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="#studio-portfolio">VIEW REAL WORK</a>',
            '<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="#studio-portfolio">VIEW REAL WORK</a>\n'
            '<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:border-secondary transition-all text-center" href="/realism-tattoos-las-vegas/">BLACK &amp; GREY REALISM</a>',
            1,
        )
    return html


def patch_joshua_specialty_links(html: str) -> str:
    block = """
<p class="font-body-md text-on-surface-variant mt-6 flex flex-wrap gap-x-4 gap-y-2">
<a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Black &amp; grey realism guide</a>
<a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up tattoos in Las Vegas</a>
<a class="text-secondary underline hover:no-underline" href="/fine_line_tattoos_las_vegas_master_authority_guide/">Fine line tattoos</a>
</p>"""
    marker = "<!-- Massive Image Wall Portfolio -->"
    if "Cover-up tattoos in Las Vegas" in html and marker in html:
        return html
    if marker in html:
        return html.replace(marker, block + "\n" + marker, 1)
    return html


def patch_realism_coverup_link(html: str) -> str:
    needle = 'href="/artists/joshua-cole/">Joshua Cole — realism portfolio</a>'
    extra = (
        ' · <a class="text-secondary underline" href="/cover-up-tattoos-las-vegas/">'
        "Cover-up tattoos in Las Vegas</a>"
        ' · <a class="text-secondary underline" href="/fine_line_tattoos_las_vegas_master_authority_guide/">'
        "Fine line tattoos</a>"
    )
    if "Cover-up tattoos in Las Vegas" in html:
        return html
    return html.replace(needle, needle + extra, 1)


def patch_strip_services_links(html: str) -> str:
    section = """
<section class="space-y-3" data-woa-strip-service-links="1">
<h2 class="font-headline-md text-on-surface text-xl">Tattoo &amp; Piercing Services</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">Work of Art is one studio for tattoos and professional piercing — choose by portfolio, not by the nearest mall kiosk.</p>
<ul class="font-body-md text-on-surface-variant space-y-2">
<li><a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up tattoos in Las Vegas</a> — Joshua Cole</li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Meet tattoo artist Joshua Cole</a> — realism, sleeves, portraits</li>
<li><a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Black and grey realism</a></li>
<li><a class="text-secondary underline hover:no-underline" href="/fine_line_tattoos_las_vegas_master_authority_guide/">Fine line tattoos</a> — Joshua Cole &amp; Teralyn</li>
<li><a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Professional piercing in Las Vegas</a> — Katelyn Cole</li>
<li><a class="text-secondary underline hover:no-underline" href="/artists/katelyn-cole/">Katelyn Cole — piercer</a></li>
</ul>
</section>
"""
    if 'data-woa-strip-service-links="1"' in html:
        return html
    anchor = '<section class="space-y-3">\n<h2 class="font-headline-md text-on-surface text-xl">Related Visitor Guides</h2>'
    if anchor in html:
        return html.replace(anchor, section + "\n" + anchor, 1)
    return html


def patch_fine_line_intent_order(html: str) -> str:
    """Move customer-facing blocks above technical article; replace dead form with booking CTA."""
    if 'data-woa-fine-line-intent-reordered="1"' in html:
        return html

    # Enhanced hero copy
    html = re.sub(
        r'(<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">\s*)Joshua Cole and Teralyn tattoo fine line.*?(\s*</p>)',
        r"\1Looking for clean, detailed fine line tattoo work in Las Vegas? Joshua Cole and Teralyn tattoo floral, script, stipple, and single-needle pieces at Work of Art — real portfolio photos below. Book a consult when you know placement and approximate size.\2",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Customer intent block after hero
    intent_block = """
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-b border-outline-variant/20" data-woa-fine-line-intent-reordered="1">
<div class="max-w-4xl mx-auto space-y-6">
<h2 class="font-headline-md text-on-surface text-2xl">Who does fine line tattoos here?</h2>
<p class="font-body-lg text-on-surface-variant leading-relaxed">Work of Art offers fine-line tattooing with <a class="text-secondary underline" href="/artists/joshua-cole/">Joshua Cole</a> and <a class="text-secondary underline" href="/artists/teralyn/">Teralyn</a>. Teralyn focuses on floral fine line, script, and custom drawings; Joshua handles select fine-line and stipple-heavy work alongside realism and cover-ups.</p>
<div class="flex flex-wrap gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase" href="/appointments/">Book fine line consult</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="/studio_gallery/">View portfolio</a>
<a class="inline-flex border border-outline px-8 py-3 font-label-caps text-[11px] tracking-widest uppercase hover:border-secondary" href="/healed_fine_line_tattoos_las_vegas/">Healed fine line gallery</a>
</div>
</div>
</section>
"""

    hero_end = "</section>\n<!-- Expanded Guide Content -->"
    if hero_end in html and 'data-woa-fine-line-intent-reordered="1"' not in html:
        html = html.replace(hero_end, "</section>\n" + intent_block + "\n<!-- Expanded Guide Content -->", 1)

    # Replace non-functional quote form with booking CTA
    form_pattern = re.compile(
        r"<!-- Instant Quote Form -->.*?</section>\s*",
        re.DOTALL,
    )
    booking_cta = """<!-- Book consult CTA -->
<section class="py-section-gap px-margin-mobile md:px-margin-desktop">
<div class="bg-surface p-8 md:p-12 border border-outline-variant max-w-3xl mx-auto text-center space-y-6">
<h2 class="font-headline-lg text-headline-lg">Book a fine line consult</h2>
<p class="font-body-lg text-on-surface-variant">Send placement, approximate size, and reference photos through our appointment form — we reply with artist fit and next steps.</p>
<div class="flex flex-col sm:flex-row gap-3 justify-center">
<a class="inline-flex bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps tracking-widest" href="/appointments/">Book appointment</a>
<a class="inline-flex border border-outline px-10 py-4 font-label-caps text-label-caps tracking-widest hover:border-secondary" href="tel:+17252241240">Call (725) 224-1240</a>
</div>
</div>
</section>
"""
    html = form_pattern.sub(booking_cta, html, count=1)

    # Mark technical article for readers who scroll
    html = html.replace(
        "<h2>The Physics of Single-Needle Precision</h2>",
        '<p class="font-label-caps text-secondary uppercase tracking-[0.2em] text-[10px] mb-4">Technical deep-dive</p>\n<h2 id="technical-deep-dive">The Physics of Single-Needle Precision</h2>',
        1,
    )

    # Move proof strip before article if article currently precedes it
    proof_match = re.search(
        r'(<section class="space-y-6 py-4" data-woa-guide-proof-strip="1".*?</section>)',
        html,
        re.DOTALL,
    )
    article_match = re.search(
        r"(<!-- Expanded Guide Content -->\s*<article class=\"article-content.*?</article>)",
        html,
        re.DOTALL,
    )
    if proof_match and article_match and proof_match.start() > article_match.start():
        proof = proof_match.group(1)
        html = html.replace(proof, "", 1)
        html = html.replace(
            "<!-- Expanded Guide Content -->",
            proof + "\n<!-- Expanded Guide Content -->",
            1,
        )

    return html


def sync_index(code_path: Path) -> None:
    index_path = code_path.parent / "index.html"
    if index_path.is_file() or code_path.parent.name in {
        "home_work_of_art_tattoo_piercing",
    }:
        index_path.write_text(code_path.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> int:
    changed: list[str] = []

    for rel, (title, desc) in META_PATCHES.items():
        path = ROOT / rel
        if not path.is_file():
            print(f"[skip] missing {rel}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_title_desc(raw, title, desc)
        if rel.startswith("home_work_of_art_tattoo_piercing"):
            updated = patch_homepage_local_link(updated)
        if "cover-up-tattoos-las-vegas" in rel:
            updated = patch_coverup_reviews(updated)
        if "tattoo_shop_near_the_strip" in rel:
            updated = patch_strip_services_links(updated)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            sync_index(path)
            changed.append(rel)
            print(f"[ok] meta/links: {rel}")

    for rel, fn in (
        ("artists/joshua-cole/code.html", patch_joshua_specialty_links),
        ("artists_build/joshua-cole.html", patch_joshua_specialty_links),
        ("realism-tattoos-las-vegas/code.html", patch_realism_coverup_link),
        ("fine_line_tattoos_las_vegas_master_authority_guide/code.html", patch_fine_line_intent_order),
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = fn(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            if "index.html" in str(path.parent) or path.parent.name.endswith("_guide"):
                sync_index(path)
            changed.append(rel)
            print(f"[ok] content: {rel}")

    # Root homepage mirror
    home = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    if home.is_file():
        for mirror in (ROOT / "code.html", ROOT / "index.html"):
            mirror.write_text(home.read_text(encoding="utf-8"), encoding="utf-8")

    for mirror in (
        ROOT / "cover-up-tattoos-las-vegas" / "index.html",
        ROOT / "fine_line_tattoos_las_vegas_master_authority_guide" / "index.html",
        ROOT / "realism-tattoos-las-vegas" / "index.html",
        ROOT / "tattoo_shop_near_the_strip_nap_corrected" / "index.html",
    ):
        code = mirror.parent / "code.html"
        if code.is_file() and mirror.parent.name in {p.parent.name for p in [ROOT / c for c in changed]}:
            mirror.write_text(code.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"[done] {len(changed)} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

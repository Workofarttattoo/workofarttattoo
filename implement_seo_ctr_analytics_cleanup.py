#!/usr/bin/env python3
"""Focused SEO CTR, ATF answers, meta fixes, legal noindex, and analytics dedupe."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PRIORITY_TITLES: dict[str, str] = {
    "epidermis_skin_science_las_vegas_authority_guide": "Epidermis & Tattoo Healing: What Happens to Ink",
    "healed_tattoo_gallery_las_vegas": "Healed Tattoo Gallery | Real Las Vegas Results",
    "how-to-choose-a-tattoo-artist": "How to Choose a Tattoo Artist in Las Vegas",
    "walk-in-tattoos-las-vegas": "Walk-In Tattoos Las Vegas | Same-Day Availability",
    "tattoo_shop_near_las_vegas_airport": "Tattoo & Piercing Shop Near Las Vegas Airport",
    "tattoo-aftercare-desert-climate": "Tattoo Aftercare in Las Vegas Desert Heat",
    "las-vegas-tattoo-healing-guide": "Fresh vs. Healed Tattoos: Las Vegas Healing Guide",
    "real_client_tattoo_timeline_las_vegas": "Tattoo Healing Timeline: Real Client Results",
    "tattoo_shop_near_the_strip_nap_corrected": "Tattoo & Piercing Shop Near Las Vegas Strip",
}

META_DESCRIPTION_FIXES: dict[str, str] = {
    "joshua_oil_painting_black_grey_tattoo_aging_las_vegas/code.html": (
        "How Joshua Cole's classical painting background shapes black-and-grey tattoo design in Las Vegas — "
        "choices that heal cleanly and read well for years at Work of Art on E. Tropicana."
    ),
    "knowledge/tattoo-second-skin-saniderm-how-long/code.html": (
        "How long to keep Saniderm or second skin on a fresh tattoo — typical wear windows, safe removal, "
        "and aftercare steps for Las Vegas clients at Work of Art Tattoo & Piercing."
    ),
    "tattoo_shop_near_the_strip_nap_corrected/code.html": (
        "Tattoo and piercing studio minutes from the Las Vegas Strip on E. Tropicana — custom tattoos, "
        "cover-ups, fine line, and professional piercing. Directions, artists, and booking."
    ),
    "artists/teralyn/code.html": (
        "Meet Teralyn at Work of Art Las Vegas — fine-line floral tattoos, script, custom drawings, "
        "walk-in flash, and piercing by request. Portfolio and booking at our Tropicana studio."
    ),
}

HOME_META_DESCRIPTION = (
    "Open daily noon–midnight. Visit Work of Art in Las Vegas for custom tattoos, cover-ups and "
    "professional piercings. Walk-ins welcome; book online."
)

ATF_ANSWER_BLOCKS: dict[str, str] = {
    "epidermis_skin_science_las_vegas_authority_guide": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">'
        "Tattoo needles pass through the constantly renewing epidermis to deposit pigment in the stable dermis beneath. "
        "During healing, that outer layer sheds — normal peeling and flaking, not a sign your tattoo is failing. "
        'Questions about aftercare? See our <a class="text-secondary underline hover:no-underline" href="/tattoo-aftercare-desert-climate/">desert aftercare guide</a> '
        'or <a class="text-secondary underline hover:no-underline" href="/appointments/">book a consult</a>.'
        "</p>"
    ),
    "knowledge/tattoo-on-ribs-recovery": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-6" data-woa-atf-answer="1">'
        "Rib tattoos are among the more intense placements most clients report, with surface healing often taking two to three weeks. "
        "Sleep on the opposite side, keep fabric from rubbing the area, and treat friction as the main recovery concern — not just pain on the table. "
        'Planning ribs or a large piece? '
        '<a class="text-secondary underline hover:no-underline" href="/appointments/">Check tattoo availability</a> '
        "before you commit to placement."
        "</p>"
    ),
    "healed_tattoo_gallery_las_vegas": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">'
        "This gallery shows tattoos after they have settled — not only fresh-from-the-chair photos — so you can judge long-term linework, "
        "grey saturation, and color contrast before you book. "
        'Ready to compare artists? '
        '<a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">How to choose a tattoo artist</a> '
        'and <a class="text-secondary underline hover:no-underline" href="/appointments/">request a consult</a>.'
        "</p>"
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">'
        "Tattoo pricing in Las Vegas depends on size, placement, artist, session length, and whether the piece is custom, cover-up, or walk-in flash — "
        "not a single menu price for every design. "
        "This page breaks down shop minimums, hourly rates, deposits, and what changes your quote. "
        '<a class="text-secondary underline hover:no-underline" href="/appointments/">Submit photos for a tattoo quote</a> '
        "when you are ready to plan."
        "</p>"
    ),
    "how-to-choose-a-tattoo-artist": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-8" data-woa-atf-answer="1">'
        "Choose an artist by comparing healed work in the style you want, studio hygiene, how they listen in consult, "
        "and whether their portfolio matches your idea — not follower counts or fresh-only Instagram posts. "
        'When you are ready, '
        '<a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">browse healed studio proof</a> '
        'and <a class="text-secondary underline hover:no-underline" href="/appointments/">book a consult</a>.'
        "</p>"
    ),
    "las-vegas-tattoo-healing-guide": (
        '<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-6" data-woa-atf-answer="1">'
        "Healing moves through fresh, peeling, settling, and fully healed stages over weeks to months — "
        "what you see at two weeks is not the final look. "
        'See our <a class="text-secondary underline hover:no-underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a> '
        "for stage-by-stage photos, or "
        '<a class="text-secondary underline hover:no-underline" href="/appointments/">ask about your piece in consult</a>.'
        "</p>"
    ),
}

LEGAL_NOINDEX_SLUGS = frozenset({"privacy-policy", "terms-of-service", "image-license"})

GTAG_BLOCK_RE = re.compile(
    r"<!-- Google tag \(gtag\.js\) -->[\s\S]*?gtag\('config', 'G-XLXNGGW7SX'\);\s*</script>\s*",
    re.IGNORECASE,
)
ATF_BLOCK_RE = re.compile(
    r'<p[^>]*data-woa-atf-answer="1"[^>]*>[\s\S]*?</p>',
    re.IGNORECASE,
)


def path_for(rel: str) -> Path:
    return ROOT / rel


def patch_title_and_social(html: str, title: str) -> str:
    html = re.sub(r"<title>[^<]*</title>", f"<title>{escape(title)}</title>", html, count=1)
    for prop in ("og:title", "twitter:title"):
        html = re.sub(
            rf'<meta content="[^"]*" property="{re.escape(prop)}"/>',
            f'<meta content="{escape(title)}" property="{prop}"/>',
            html,
            count=1,
        )
        tw = prop.replace("og:", "")
        html = re.sub(
            rf'<meta content="[^"]*" name="{re.escape(tw)}"/>',
            f'<meta content="{escape(title)}" name="{tw}"/>',
            html,
            count=1,
        )
    return html


def patch_description(html: str, description: str) -> str:
    esc = escape(description)
    html = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{esc}" name="description"/>',
        html,
        count=1,
    )
    for prop in ("og:description", "twitter:description"):
        tag = "property" if prop.startswith("og:") else "name"
        html = re.sub(
            rf'<meta content="[^"]*" {tag}="{re.escape(prop)}"/>',
            f'<meta content="{esc}" {tag}="{prop}"/>',
            html,
            count=1,
        )
    return html


def patch_robots_noindex(html: str) -> str:
    if re.search(r'<meta content="[^"]*noindex[^"]*" name="robots"/>', html, re.I):
        return html
    return re.sub(
        r'<meta content="[^"]*" name="robots"/>',
        '<meta content="noindex, follow" name="robots"/>',
        html,
        count=1,
    )


def patch_homepage_piercing(html: str) -> str:
    html = patch_description(html, HOME_META_DESCRIPTION)
    html = patch_title_and_social(html, "Tattoo & Piercing Shop Las Vegas | Work of Art")

    marker = 'data-woa-home-piercing-ctr="1"'
    if marker in html:
        return html

    old = """<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/10" id="piercing">
<div class="max-w-3xl mx-auto text-center space-y-4">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Professional Piercer</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Ear Curation &amp; Body piercing</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Katelyn Cole — ear piercing, helix piercing, starter jewelry, anatomical placement, and jewelry styling.</p>
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest" href="/artists/katelyn-cole/">Meet Katelyn</a>
</div>
</section>"""

    new = f"""<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/10" id="piercing">
<div class="max-w-3xl mx-auto text-center space-y-4" {marker}>
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Professional Piercer</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Ear Curation &amp; Body Piercing</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Katelyn Cole offers professional ear and body piercing in Las Vegas with implant-grade jewelry, anatomy-first placement, and walk-in availability when chairs allow. <strong class="text-on-surface">Walk-in piercings available daily from noon to midnight.</strong></p>
<div class="flex flex-col sm:flex-row flex-wrap justify-center gap-3 pt-2">
<a class="inline-flex bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest" href="/appointments/">Book Piercing Appointment</a>
<a class="inline-flex border border-secondary text-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest hover:bg-secondary/10 transition-colors" href="/piercing-guide-las-vegas/">Las Vegas Piercing Guide</a>
</div>
<a class="inline-block text-secondary underline font-body-md pt-2" href="/artists/katelyn-cole/">Meet Katelyn Cole</a>
</div>
</section>"""

    if old in html:
        return html.replace(old, new, 1)
    if "Walk-in piercings available daily from noon to midnight" in html:
        return html
    return html


def replace_atf_block(html: str, new_block: str) -> str:
    if 'data-woa-atf-answer="1"' in html:
        return ATF_BLOCK_RE.sub(new_block, html, count=1)
    return html


def inject_atf_after_h1(html: str, h1_fragment: str, block: str) -> str:
    if 'data-woa-atf-answer="1"' in html:
        return html
    idx = html.find(h1_fragment)
    if idx == -1:
        return html
    end = html.find("</h1>", idx)
    if end == -1:
        return html
    insert_at = end + len("</h1>")
    return html[:insert_at] + block + html[insert_at:]


def strip_duplicate_gtag(html: str) -> str:
    # Leave the direct GA4 tag in place. GTM-TZTQSQBB does not initialize G-XLXNGGW7SX.
    return html


def main() -> int:
    changed = 0

    for slug, title in PRIORITY_TITLES.items():
        path = ROOT / slug / "code.html"
        if not path.is_file():
            print(f"[skip] title {slug}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_title_and_social(raw, title)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[title] {slug}")

    for rel, desc in META_DESCRIPTION_FIXES.items():
        path = path_for(rel)
        if not path.is_file():
            print(f"[skip] meta {rel}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_description(raw, desc)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[meta] {rel}")

    home = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    if home.is_file():
        raw = home.read_text(encoding="utf-8")
        updated = patch_homepage_piercing(raw)
        if updated != raw:
            home.write_text(updated, encoding="utf-8")
            changed += 1
            print("[home] piercing section + meta")

    for slug, block in ATF_ANSWER_BLOCKS.items():
        path = ROOT / slug / "code.html" if not slug.startswith("knowledge/") else ROOT / slug / "code.html"
        if not path.is_file():
            print(f"[skip] atf {slug}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = replace_atf_block(raw, block)
        if slug == "how_much_do_tattoos_cost_in_las_vegas_authority_guide" and 'data-woa-atf-answer="1"' not in updated:
            updated = inject_atf_after_h1(
                updated,
                "How Much Do Tattoos Cost in Las Vegas?",
                block,
            )
        if slug == "how-to-choose-a-tattoo-artist" and 'data-woa-atf-answer="1"' not in updated:
            updated = inject_atf_after_h1(
                updated,
                "The Selection of a Masterpiece",
                block,
            )
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[atf] {slug}")

    for slug in LEGAL_NOINDEX_SLUGS:
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_robots_noindex(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[noindex] {slug}")

    for path in sorted(ROOT.rglob("code.html")):
        if any(p in path.parts for p in (".git", "skipped_upload_build", "artists_raw")):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        updated = strip_duplicate_gtag(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    artists_build = ROOT / "artists_build" / "teralyn.html"
    if artists_build.is_file():
        raw = artists_build.read_text(encoding="utf-8")
        updated = patch_description(strip_duplicate_gtag(raw), META_DESCRIPTION_FIXES["artists/teralyn/code.html"])
        if updated != raw:
            artists_build.write_text(updated, encoding="utf-8")
            changed += 1
            print("[meta] artists_build/teralyn.html")

    print(f"Done: {changed} file update(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

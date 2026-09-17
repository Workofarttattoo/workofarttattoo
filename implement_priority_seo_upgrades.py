#!/usr/bin/env python3
"""Priority SEO upgrades: ATF answer summaries, piercing hub, cover-up, contextual links."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ATF_MARKER = 'data-woa-atf-answer="1"'
PIERCING_HUB_MARKER = 'data-woa-piercing-hub-intro="1"'
COVER_UP_ATF_MARKER = 'data-woa-coverup-atf="1"'
CTX_MARKER = 'data-woa-priority-ctx="1"'

ATF_ANSWERS: dict[str, tuple[str, str]] = {
    "epidermis_skin_science_las_vegas_authority_guide": (
        '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">The Epidermis — Your Skin\'s Outer Shield</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">
Tattoo needles pass through the constantly renewing epidermis to deposit pigment in the stable dermis beneath it.
During healing, that outer layer sheds — normal peeling and flaking, not a sign your tattoo is failing.
</p>
""",
    ),
    "knowledge/tattoo-on-ribs-recovery": (
        '<h1 class="font-headline-lg text-on-surface mb-6">How painful are rib tattoos and how long do they take to heal?</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-6" data-woa-atf-answer="1">
Rib tattoos are among the more intense placements most clients report, with surface healing often taking two to three weeks.
Sleep on the opposite side, keep shirts from rubbing the area, and treat friction as the main recovery concern — not just pain on the table.
</p>
""",
    ),
    "healed_tattoo_gallery_las_vegas": (
        '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Healed tattoo gallery — Las Vegas studio results</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">
This gallery shows tattoos after they have settled — not only fresh-from-the-chair photos — so you can judge long-term linework, grey saturation, and color contrast before you book.
</p>
""",
    ),
    "how-to-choose-a-tattoo-artist": (
        '<h1 class="font-headline-xl text-headline-xl md:text-headline-xl leading-tight mb-8">The Selection of a Masterpiece</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-8" data-woa-atf-answer="1">
Choose an artist by comparing healed work in the style you want, studio hygiene, how they listen in consult, and whether their portfolio matches your idea — not follower counts or fresh-only Instagram posts.
</p>
""",
    ),
    "las-vegas-tattoo-healing-guide": (
        '<h1 class="font-headline-xl text-[40px] md:text-headline-xl text-on-surface mb-6 leading-tight">Fresh vs healed: what your tattoo will look like over time</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed mb-6" data-woa-atf-answer="1">
Healing moves through fresh, peeling, settling, and fully healed stages over weeks to months.
See our <a class="text-secondary underline hover:no-underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a> for what those stages actually look like on studio work.
</p>
""",
    ),
    "real_client_tattoo_timeline_las_vegas": (
        '<h1 class="font-headline-xl text-on-surface leading-tight">Real Client Timeline — One Tattoo, Every Stage</h1>',
        """
<p class="font-body-lg text-on-surface max-w-3xl leading-relaxed" data-woa-atf-answer="1">
This page documents one real tattoo from day one through later healed stages so you can see realistic peeling, line settling, and color changes — not idealized day-of photos alone.
</p>
""",
    ),
}

PIERCING_META = {
    "description": (
        "Explore professional piercing in Las Vegas with Katelyn Cole. Compare placements, jewelry, "
        "healing and anatomy considerations, then check availability."
    ),
}

PIERCING_HUB_INTRO = """
<div class="space-y-4" data-woa-piercing-hub-intro="1">
<p class="font-body-lg text-on-surface-variant max-w-3xl leading-relaxed">
<strong class="text-on-surface">Professional piercing in Las Vegas</strong> with Katelyn Cole — ear, helix, nose, and body work planned anatomy-first.
Starter jewelry sizing, jewelry-fit guidance, and walk-ins when availability permits at 2375 E. Tropicana Ave, Suite 3.
</p>
<p class="font-body-md text-on-surface-variant max-w-3xl">
Compare placements and healing timelines below, then
<a class="text-secondary underline hover:no-underline" href="/appointments/">check availability or book with Katelyn Cole</a>.
Studio hours and directions are on our
<a class="text-secondary underline hover:no-underline" href="/official_location_hours_contact/">location page</a>.
</p>
</div>
"""

COVER_UP_ATF_BLOCK = """
<p class="font-body-lg text-on-surface-variant max-w-2xl mb-6" data-woa-coverup-atf="1">
Whether a cover-up is possible depends on how dark the old ink is, its size, placement, scar tissue, and how flexible the new design can be — Joshua Cole assesses each piece in consult; not every tattoo can be covered.
<a class="text-secondary underline hover:no-underline" href="/healed_cover_up_tattoos_las_vegas/">Browse healed cover-up results</a>
before you book.
</p>
"""

# slug -> list of HTML snippets (injected once before </main> if marker absent)
CONTEXTUAL_LINK_BLOCKS: dict[str, list[str]] = {
    "dermis_skin_science_las_vegas_authority_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Ink sits below the epidermis — read our guide to <a class="text-secondary underline hover:no-underline" href="/epidermis_skin_science_las_vegas_authority_guide/">the epidermis and normal peeling during healing</a>.</p>',
    ],
    "skin_science_tattoo_dermatology_authority_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Start with <a class="text-secondary underline hover:no-underline" href="/epidermis_skin_science_las_vegas_authority_guide/">how the epidermis renews</a> and why peeling is expected after a session.</p>',
    ],
    "tattoo-aftercare-desert-climate": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">See the full <a class="text-secondary underline hover:no-underline" href="/las-vegas-tattoo-healing-guide/">tattoo healing stages</a> and our <a class="text-secondary underline hover:no-underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a> for desert healing in practice.</p>',
    ],
    "tattoo_pain_chart_placement_sensitivity_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Ribs rank high on the sensitivity chart — our <a class="text-secondary underline hover:no-underline" href="/knowledge/tattoo-on-ribs-recovery/">rib tattoo recovery guide</a> covers pain level, sleep, and surface-healing timing.</p>',
    ],
    "realism-tattoos-las-vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Compare <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed realism results</a> and read <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">how to choose a tattoo artist</a> before you commit to a large piece.</p>',
    ],
    "start_here": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">New collectors: <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">how to choose a tattoo artist</a> and <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed tattoo proof</a> from the studio.</p>',
    ],
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Budget matters, but so does vetting — use our <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">artist selection guide</a> alongside pricing.</p>',
    ],
    "walk-in-tattoos-las-vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Even walk-ins benefit from <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">choosing the right artist</a> and checking <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed work</a> first.</p>',
    ],
    "artists/joshua-cole": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Joshua specializes in <a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">cover-up tattoo planning</a> and <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed portfolio proof</a>.</p>',
    ],
    "artists/katelyn-cole": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Book <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">professional piercing in Las Vegas</a> — Katelyn\'s complete <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Las Vegas piercing guide</a> covers ear and body placements.</p>',
    ],
    "ear_piercing_guide_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">This ear guide is part of our full <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Las Vegas piercing guide</a> — anatomy-first planning with Katelyn Cole.</p>',
    ],
    "facial_piercing_guide_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Facial work links back to the studio <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">piercing hub</a> for jewelry standards and booking.</p>',
    ],
    "body_piercing_guide_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Body placements are indexed in our <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">ear and body piercing guide</a>.</p>',
    ],
    "piercing_jewelry_guide_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Jewelry-fit questions start on the <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">professional piercing hub</a> before you pick a placement.</p>',
    ],
    "piercing_aftercare_guide_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Aftercare pairs with placement choice — see the full <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">Las Vegas piercing guide</a> for starter jewelry and healing timelines.</p>',
    ],
    "official_location_hours_contact": [
        '<p class="font-body-md text-on-surface-variant" data-woo-priority-ctx="1">Visit for tattoos or <a class="text-secondary underline hover:no-underline" href="/piercing-guide-las-vegas/">professional piercing in Las Vegas</a> with Katelyn Cole — walk-ins when chairs allow.</p>'.replace(
            "data-woo-", "data-woa-"
        ),
    ],
    "healed_cover_up_tattoos_las_vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Ready to plan yours? Start with a <a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">cover-up consultation with Joshua Cole</a>.</p>',
    ],
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Track stages visually on our <a class="text-secondary underline hover:no-underline" href="/las-vegas-tattoo-healing-guide/">tattoo healing guide</a> and <a class="text-secondary underline hover:no-underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a>.</p>',
    ],
    "knowledge/tattoo-aging-and-fading-over-time": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Skin turnover starts in the <a class="text-secondary underline hover:no-underline" href="/epidermis_skin_science_las_vegas_authority_guide/">epidermis guide</a>; compare long-term results in the <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed tattoo gallery</a>.</p>',
    ],
    "fine_line_tattoos_las_vegas_master_authority_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Fine line demands healed proof — browse the <a class="text-secondary underline hover:no-underline" href="/healed_tattoo_gallery_las_vegas/">healed gallery</a> and <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">artist selection checklist</a>.</p>',
    ],
    "home_work_of_art_tattoo_piercing": [
        '<p class="font-body-md text-on-surface-variant text-sm" data-woa-priority-ctx="1">Planning ink? Review our <a class="text-secondary underline hover:no-underline" href="/las-vegas-tattoo-healing-guide/">tattoo healing guide</a>, <a class="text-secondary underline hover:no-underline" href="/real_client_tattoo_timeline_las_vegas/">real client timeline</a>, and <a class="text-secondary underline hover:no-underline" href="/epidermis_skin_science_las_vegas_authority_guide/">epidermis skin science</a> before your session.</p>',
    ],
    "knowledge/first-tattoo-tips-before-you-book": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Considering ribs or a sensitive spot? Read our <a class="text-secondary underline hover:no-underline" href="/knowledge/tattoo-on-ribs-recovery/">rib tattoo recovery guide</a> and <a class="text-secondary underline hover:no-underline" href="/how-to-choose-a-tattoo-artist/">how to choose a tattoo artist</a> first.</p>',
    ],
    "tattoo_pain_chart_placement_sensitivity_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Ribs sit high on the sensitivity chart — see <a class="text-secondary underline hover:no-underline" href="/knowledge/tattoo-on-ribs-recovery/">rib placement recovery</a> for sleep and healing timing.</p>',
    ],
    "why_tattoos_stay_forever_skin_science_las_vegas_authority_guide": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Ink passes through the <a class="text-secondary underline hover:no-underline" href="/epidermis_skin_science_las_vegas_authority_guide/">epidermis</a> into the dermis — that outer layer explains normal post-session peeling.</p>',
    ],
    "realism-tattoos-las-vegas": [
        '<p class="font-body-md text-on-surface-variant" data-woa-priority-ctx="1">Planning a cover-up or rework? Joshua Cole handles <a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">cover-up consults in Las Vegas</a> with healed proof in the gallery.</p>',
    ],
}


def path_for_slug(slug: str) -> Path:
    if slug.startswith("knowledge/"):
        return ROOT / slug / "code.html"
    if slug == "home_work_of_art_tattoo_piercing":
        return ROOT / slug / "code.html"
    if slug.startswith("artists/"):
        return ROOT / slug / "code.html"
    return ROOT / slug / "code.html"


def inject_after_h1(html: str, h1_needle: str, block: str, marker: str) -> str:
    if marker.split("=")[0].strip('"') in html and marker in html:
        return html
    if h1_needle not in html:
        return html
    return html.replace(h1_needle, h1_needle + block, 1)


def patch_meta_description(html: str, description: str) -> str:
    pattern = re.compile(
        r'(<meta content=")([^"]*)(" name="description"/>)',
        re.IGNORECASE,
    )
    if not pattern.search(html):
        return html
    return pattern.sub(rf"\1{description}\3", html, count=1)


def patch_og_twitter_descriptions(html: str, description: str) -> str:
    for prop in ("og:description", "twitter:description"):
        pattern = re.compile(
            rf'(<meta content=")([^"]*)(" (?:property|name)="{re.escape(prop)}"/>)',
            re.IGNORECASE,
        )
        html = pattern.sub(rf"\1{description}\3", html, count=1)
    return html


def patch_piercing_hub(html: str) -> str:
    html = patch_meta_description(html, PIERCING_META["description"])
    html = patch_og_twitter_descriptions(html, PIERCING_META["description"])
    if PIERCING_HUB_MARKER in html:
        return html
    needle = '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Piercing in Las Vegas — the Complete Guide to Ear, Nose &amp; Body Work</h1>'
    if needle not in html:
        return html
    return html.replace(needle, needle + PIERCING_HUB_INTRO, 1)


def patch_cover_up(html: str) -> str:
    if COVER_UP_ATF_MARKER not in html:
        needle = '<h1 class="font-headline-xl text-headline-xl mb-6 leading-none">Cover Up Tattoos <span class="text-secondary">Las Vegas</span></h1>'
        if needle in html:
            html = html.replace(needle, needle + COVER_UP_ATF_BLOCK, 1)
    # Above-the-fold healed gallery link in hero CTAs
    gallery_cta = 'href="/healed_cover_up_tattoos_las_vegas/"'
    if gallery_cta not in html:
        old = 'href="#studio-portfolio">VIEW REAL WORK</a>'
        new = 'href="/healed_cover_up_tattoos_las_vegas/">HEALED COVER-UP GALLERY</a>'
        if old in html:
            html = html.replace(old, new, 1)
    return html


def inject_contextual_blocks(html: str, blocks: list[str]) -> str:
    if CTX_MARKER in html:
        return html
    chunk = "\n".join(blocks)
    if "</main>" in html:
        return html.replace("</main>", chunk + "\n</main>", 1)
    return html


def main() -> int:
    changed = 0

    for slug, (h1, block) in ATF_ANSWERS.items():
        path = path_for_slug(slug)
        if not path.is_file():
            print(f"[skip] missing {slug}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject_after_h1(raw, h1, block, ATF_MARKER)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[atf] {slug}")

    for hub_slug in ("piercing-guide-las-vegas", "piercing_types_las_vegas_authority_hub"):
        path = path_for_slug(hub_slug)
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_piercing_hub(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[piercing] {hub_slug}")

    cover_path = path_for_slug("cover-up-tattoos-las-vegas")
    if cover_path.is_file():
        raw = cover_path.read_text(encoding="utf-8")
        updated = patch_cover_up(raw)
        if updated != raw:
            cover_path.write_text(updated, encoding="utf-8")
            changed += 1
            print("[cover-up] cover-up-tattoos-las-vegas")

    for slug, blocks in CONTEXTUAL_LINK_BLOCKS.items():
        path = path_for_slug(slug)
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = inject_contextual_blocks(raw, blocks)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ctx] {slug}")

    print(f"Done: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

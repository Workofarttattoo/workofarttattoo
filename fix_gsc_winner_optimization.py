#!/usr/bin/env python3
"""Surgical GSC winner optimization — CTR, images, internal links, snippets."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FINE_LINE = ROOT / "fine_line_tattoos_las_vegas_master_authority_guide" / "code.html"
BEST_FINE_LINE = ROOT / "best_fine_line_tattoos_in_vegas_ultimate_authority_guide" / "code.html"
PIERCING_GUIDE = ROOT / "piercing-guide-las-vegas" / "code.html"
STRIP_PAGE = ROOT / "tattoo_shop_near_the_strip_nap_corrected" / "code.html"
DERMIS = ROOT / "dermis_skin_science_las_vegas_authority_guide" / "code.html"
SCAR_TISSUE = ROOT / "scar_tissue_tattoo_skin_science_las_vegas_authority_guide" / "code.html"
KNOW_AGING = ROOT / "knowledge" / "tattoo-aging-and-fading-over-time" / "code.html"
KNOW_STYLE = ROOT / "knowledge" / "tattoo-style-matching-artist" / "code.html"
START_HERE = ROOT / "start_here" / "code.html"


def sub_all(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if old not in text:
            continue
        text = text.replace(old, new)
    return text


def inject_once(text: str, needle: str, insert: str) -> str:
    if insert.strip() in text or needle not in text:
        return text
    return text.replace(needle, insert + needle, 1)


def patch_fine_line() -> bool:
    if not FINE_LINE.is_file():
        return False
    raw = FINE_LINE.read_text(encoding="utf-8")
    text = raw

    title = "Fine Line Tattoos Las Vegas | Joshua Cole &amp; Teralyn | Work of Art"
    meta = (
        "Fine line tattoos in Las Vegas from Joshua Cole and Teralyn — real floral, "
        "script, and single-needle work. Book a consult at Work of Art on E. Tropicana."
    )
    og_img = "https://www.workofarttattoo.com/studio_gallery/beauty-script-roses-inner-forearm-195a396a.webp"

    text = sub_all(
        text,
        [
            (
                "<title>Fine Line Tattoos — Joshua Cole | Work of Art Las Vegas | Work of Art</title>",
                f"<title>{title}</title>",
            ),
            (
                'content="Fine Line Tattoos — Joshua Cole | Work of Art Las Vegas | Work of Art"',
                f'content="{title}"',
            ),
            (
                'content="Needle depth, ink load, artist selection, and aftercare for fine line work in desert heat. Work of Art Tattoo &amp; Piercing, Las Vegas — E. Tropicana."',
                f'content="{meta}"',
            ),
            (
                'content="https://www.workofarttattoo.com/fine_line_tattoos_las_vegas_master_authority_guide/realism-tattoos-grim-reaper-dark-art.webp"',
                f'content="{og_img}"',
            ),
            (
                "<h1 class=\"font-headline-xl text-headline-xl mb-6 leading-tight\">Fine line tattoos:<br/>needle depth, ink, and healing</h1>",
                '<h1 class="font-headline-xl text-headline-xl mb-6 leading-tight">Fine Line Tattoos in Las Vegas</h1>',
            ),
            (
                """<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
                    How single-needle work, ink depth, and aftercare actually affect fine line tattoos — explained in plain terms, with the technical details that matter for longevity.
                </p>""",
                """<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
                    Joshua Cole and Teralyn tattoo fine line, floral, script, and stipple work at Work of Art — real portfolio photos below, not stock art. Consultations and booking are open for delicate pieces that need to heal cleanly in desert heat.
                </p>""",
            ),
            (
                'src="https://lh3.googleusercontent.com/aida/ADBb0uij5pOKtUtXQr25aB5puRbqIi-Ji_RoXhr6ZE2-cdRjBJS3iEVTuYANMyjgbUU11QN7N1sbKe4wFSLHu7XaMRuT7_yHoHKFgoucDvgF6iG4KvB2BW4x1nKBLe6PBL9dJ6Oq4eHLGfXGYIa06j9h3BFLC2dDAVln9-nyhKwNIH2dpBgi3B9MmD9P_78WB0W1wgilXMKHE_OnpK8pQFK_9T4srinB20SnpQQVdAIOd4xaoix9cPQkwFd7bg4_EaJpGiiNQkLRak6jXQ"',
                'src="/studio_gallery/beauty-script-roses-inner-forearm-195a396a.webp"',
            ),
            (
                'alt="Tattoo artist workspace, Work of Art Tattoo &amp; Piercing, Las Vegas"',
                'alt="Fine line script and roses on inner forearm — Work of Art Tattoo, Las Vegas"',
            ),
            (
                "<p>Fine line tattooing gets treated like a purely aesthetic choice. In practice it is a technical discipline where the medium is living skin and the tool is a single point of steel — there is nowhere for a mistake to hide. At Work of Art, Joshua Cole treats fine line as a technical problem first — needle depth, ink load, and how skin heals in desert air.</p>",
                "<p>Fine line tattooing is a technical discipline — the medium is living skin and the tool is a single needle. At Work of Art, <a class=\"text-secondary underline\" href=\"/artists/joshua-cole/\">Joshua Cole</a> handles single-needle and stipple-heavy work; <a class=\"text-secondary underline\" href=\"/artists/teralyn/\">Teralyn</a> specializes in floral fine line and delicate script. The photos on this page are real studio work, not placeholders.</p>",
            ),
            (
                'src="https://lh3.googleusercontent.com/aida/ADBb0uipmb723pZnzPYAGxJCj2HD0RvjdHhvyrJ6ttHFu6WlTGbdZvXK8JwhgRrnyDzAzHCWzKypcWbVQQViLWV7Ikpqhl62Tf6g-vMYmpHgOk5PpfRdK5E-imuTdyE50ScBZxcuCDyF8c0WfDi37lMde89GAOcfw7N7Dj1NFavs5SvdXIcA9PSODN4nHtWYzGlLRfgsWP38cBwR-1lEpGz9p-tZzxhaNeHplv7fbSDF5y7t20nGrsEwoJQ61RhL"',
                'src="/studio_gallery/black-and-grey-rose-tattoo-design-a1784097.webp"',
            ),
            (
                'alt="Microscopic needle precision, Work of Art Tattoo &amp; Piercing, Las Vegas"',
                'alt="Stipple-shaded rose tattoo flash — pointillism fine line reference, Work of Art Las Vegas"',
            ),
            (
                'src="https://lh3.googleusercontent.com/aida/ADBb0ugzhUamW0a61RKYIoDLfKxVe7P7iO24iINB7jsdRajTIC7DFQ_MHn0ArkhBtKgP6VNa_4K1bH2H87UkulCD9HU9loD8I6QhHtt_Br884DSfZX3AXXAA-gNwAtzYBpiuQ00O26G9X7dcL1Ryc2XefKEeRKTub_K8DI-0jMUrA0mdsoT-uUjq3StHpFXNpjdawws-miM_CKF-CjpIv0IqGoQZyM2ZjFQ9UJs_pRMLL6AOHqR9znj3_DH0q72HXa4aeFrvqBJO78ML28Y"',
                'src="/studio_gallery/joshua-cole-fine-line-ankle-work-55a4538d.webp"',
            ),
            (
                'alt="Fine line healing detail, Work of Art Tattoo &amp; Piercing, Las Vegas"',
                'alt="Joshua Cole fine line ankle tattoo — healed spacing reference, Las Vegas"',
            ),
        ],
    )

    # Portfolio proof strip — replace non-fine-line skull images
    proof_old = """<figure class="space-y-2" id="proof-settled-heal">
<picture><source srcset="/healed_tattoo_gallery_las_vegas/healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas.webp" type="image/webp"/><img alt="Settled heal — Fine line — Work of Art Las Vegas" class="w-full aspect-square object-cover" decoding="async" height="400" loading="lazy" src="/healed_tattoo_gallery_las_vegas/healed-1-year-cross-eye-skull-outer-forearm-joshua-cole-las-vegas.png" width="400"/></picture>
<figcaption class="px-1 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block">Settled heal</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">Settled line-and-shade reference from healed studio documentation.</p>
</figcaption>
</figure>
<figure class="space-y-2" id="proof-fresh-redness">
<picture><source srcset="/healed_tattoo_gallery_las_vegas/fresh-all-seeing-eye-triangle-forearm-joshua-cole-las-vegas.webp" type="image/webp"/><img alt="Fresh redness — Fine line — Work of Art Las Vegas" class="w-full aspect-square object-cover" decoding="async" height="400" loading="lazy" src="/healed_tattoo_gallery_las_vegas/fresh-all-seeing-eye-triangle-forearm-joshua-cole-las-vegas.png" width="400"/></picture>
<figcaption class="px-1 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block">Fresh redness</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">Fresh tattoo surface detail shown later as healing context, not as the lead fine-line proof.</p>
</figcaption>
</figure>"""

    proof_new = """<figure class="space-y-2" id="proof-stipple-rose">
<picture><source srcset="/studio_gallery/black-and-grey-rose-tattoo-design-a1784097.webp" type="image/webp"/><img alt="Stipple-shaded rose tattoo design — fine line pointillism, Work of Art Las Vegas" class="w-full aspect-square object-cover" decoding="async" height="400" loading="lazy" src="/studio_gallery/black-and-grey-rose-tattoo-design-a1784097.png" width="400"/></picture>
<figcaption class="px-1 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block">Pointillism rose</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">Stipple-shaded rose flash — shows how single-needle density reads on skin.</p>
</figcaption>
</figure>
<figure class="space-y-2" id="proof-teralyn-floral">
<picture><source srcset="/artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas.webp" type="image/webp"/><img alt="Teralyn — fine line floral tattoo artist at Work of Art Las Vegas" class="w-full aspect-square object-cover object-top" decoding="async" height="400" loading="lazy" src="/artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas.jpg" width="400"/></picture>
<figcaption class="px-1 space-y-1">
<span class="font-label-caps text-secondary text-[10px] uppercase tracking-widest block">Teralyn — floral fine line</span>
<p class="font-body-md text-on-surface-variant text-sm leading-snug">More floral and script work on <a class="text-secondary underline" href="/artists/teralyn/">Teralyn's page</a> and <a class="text-secondary underline" href="https://www.instagram.com/mischiefmodifies/" rel="noopener noreferrer" target="_blank">@mischiefmodifies</a>.</p>
</figcaption>
</figure>"""

    text = text.replace(proof_old, proof_new)

    text = sub_all(
        text,
        [
            (
                "<p class=\"font-body-md text-on-surface-variant\">Real fine line from Joshua Cole's chair — fresh redness, peel stage, and settled heal photographed in-studio. Desert sun changes the timeline; these are honest reference frames.</p>",
                "<p class=\"font-body-md text-on-surface-variant\">Real fine line from Joshua Cole and Teralyn — ankle detail, floral script, stipple roses, and healed spacing photographed in-studio. Desert sun changes the timeline; these are honest reference frames.</p>",
            ),
            (
                'href="/artists/joshua-cole/">Joshua\'s portfolio</a></p>',
                'href="/artists/joshua-cole/">Joshua\'s portfolio</a> · <a class="text-secondary underline" href="/artists/teralyn/">Teralyn\'s fine line &amp; floral work</a></p>',
            ),
        ],
    )

    if text != raw:
        FINE_LINE.write_text(text, encoding="utf-8")
        return True
    return False


def patch_best_fine_line_supporting() -> bool:
    if not BEST_FINE_LINE.is_file():
        return False
    raw = BEST_FINE_LINE.read_text(encoding="utf-8")
    title = "How to Choose a Fine Line Tattoo Artist in Vegas | Work of Art"
    meta = (
        "Compare artists, healed clarity, and placement limits before booking fine line in Las Vegas. "
        "Start with our primary fine line service guide at Work of Art."
    )
    text = sub_all(
        raw,
        [
            (
                "<title>Fine Line Tattoos in Vegas — Joshua Cole | Work of Art Las Vegas | Work of Art</title>",
                f"<title>{title}</title>",
            ),
            (
                'content="Fine Line Tattoos in Vegas — Joshua Cole | Work of Art Las Vegas | Work of Art"',
                f'content="{title}"',
            ),
            (
                'content="Needle-light linework, healed clarity, and how to pick an artist for delicate script and micro-detail. Work of Art Tattoo &amp; Piercing, Las Vegas — E…"',
                f'content="{meta}"',
            ),
        ],
    )
    text = inject_once(
        text,
        '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl text-on-surface leading-tight">Fine Line Tattoos in Vegas</h1>',
        '<p class="font-body-md text-on-surface-variant mb-4 max-w-3xl"><strong class="text-on-surface">Primary service page:</strong> <a class="text-secondary underline hover:no-underline" href="/fine_line_tattoos_las_vegas_master_authority_guide/">Fine line tattoos in Las Vegas</a> — portfolio, artists, and booking.</p>\n',
    )
    if text != raw:
        BEST_FINE_LINE.write_text(text, encoding="utf-8")
        return True
    return False


def patch_piercing_snippets() -> int:
    changed = 0
    title = "Professional Piercing Las Vegas | Complete Guide | Work of Art"
    meta = (
        "Professional piercing in Las Vegas — ear curation, nose, and body work with Katelyn Cole. "
        "Placement guides, jewelry standards, and booking at Work of Art."
    )
    old_title = "Piercing Las Vegas | Complete Guide — Ear, Nose, Body &amp; Book Online | Work of Art"
    old_meta = (
        "All placement guides, jewelry standards, and Katelyn Cole's piercing hub. "
        "Work of Art Tattoo &amp; Piercing, Las Vegas — E. Tropicana."
    )
    if PIERCING_GUIDE.is_file():
        raw = PIERCING_GUIDE.read_text(encoding="utf-8")
        text = raw.replace(old_title, title).replace(old_meta, meta)
        if text != raw:
            PIERCING_GUIDE.write_text(text, encoding="utf-8")
            changed += 1

    strip_meta = (
        "Tattoo and piercing studio minutes from the Las Vegas Strip — professional ear, nose, "
        "and body piercing with Katelyn Cole. Directions from MGM, Sphere, and the airport."
    )
    strip_old = (
        "Directions to Work of Art at 2375 E. Tropicana Ave, Suite 3 — easy access from the Strip "
        "and airport. Work of Art Tattoo &amp; Piercing, Las Vegas — E…"
    )
    if STRIP_PAGE.is_file():
        raw = STRIP_PAGE.read_text(encoding="utf-8")
        text = raw.replace(strip_old, strip_meta)
        if text != raw:
            STRIP_PAGE.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def patch_internal_links() -> int:
    changed = 0
    link_specs: list[tuple[Path, str, str]] = [
        (
            DERMIS,
            "Scarred dermis: unpredictable pockets — see our scar tissue guide before cover-ups.",
            'Scarred dermis: unpredictable pockets — see our <a class="text-secondary underline" href="/scar_tissue_tattoo_skin_science_las_vegas_authority_guide/">scar tissue guide</a> before <a class="text-secondary underline" href="/cover-up-tattoos-las-vegas/">cover-up tattoo consultations</a>.',
        ),
        (
            SCAR_TISSUE,
            "<li>Scar tissue changes how ink sits — timing and technique matter more than on untouched skin.</li>",
            "<li>Scar tissue changes how ink sits — timing and technique matter more than on untouched skin. See our <a class=\"text-secondary underline\" href=\"/cover-up-tattoos-las-vegas/\">cover-up tattoo work</a> in Las Vegas when old ink or scars need correction.</li>",
        ),
        (
            KNOW_AGING,
            "<p>Fine lines soften over decades; bold lines spread wider but keep internal detail longer.</p>",
            "<p>Fine lines soften over decades; bold lines spread wider but keep internal detail longer. For <a class=\"text-secondary underline\" href=\"/fine_line_tattoos_las_vegas_master_authority_guide/\">fine line tattoos in Las Vegas</a>, placement and artist technique matter most.</p>",
        ),
        (
            KNOW_STYLE,
            "<p>Match the artist to the style you want healed — not just the flash that caught your eye on Instagram.</p>",
            "<p>Match the artist to the style you want healed — not just the flash that caught your eye on Instagram. Compare <a class=\"text-secondary underline\" href=\"/realism-tattoos-las-vegas/\">realism</a>, <a class=\"text-secondary underline\" href=\"/fine_line_tattoos_las_vegas_master_authority_guide/\">fine line</a>, and <a class=\"text-secondary underline\" href=\"/cover-up-tattoos-las-vegas/\">cover-up tattoo consultations</a> at Work of Art.</p>",
        ),
    ]
    for path, needle, insert in link_specs:
        if not path.is_file() or needle not in path.read_text(encoding="utf-8"):
            continue
        raw = path.read_text(encoding="utf-8")
        text = raw.replace(needle, insert, 1)
        if text != raw:
            path.write_text(text, encoding="utf-8")
            changed += 1

    if START_HERE.is_file():
        raw = START_HERE.read_text(encoding="utf-8")
        needle = 'href="/piercing-guide-las-vegas/">Complete piercing guide</a>'
        insert = 'href="/piercing-guide-las-vegas/">Professional piercing in Las Vegas</a>'
        if needle in raw and insert not in raw:
            START_HERE.write_text(raw.replace(needle, insert, 1), encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    flags = []
    if patch_fine_line():
        flags.append("fine_line")
    if patch_best_fine_line_supporting():
        flags.append("best_fine_line_support")
    n = patch_piercing_snippets()
    if n:
        flags.append(f"piercing_snippets({n})")
    n = patch_internal_links()
    if n:
        flags.append(f"internal_links({n})")
    print("GSC winner optimization:", ", ".join(flags) if flags else "no changes")


if __name__ == "__main__":
    main()

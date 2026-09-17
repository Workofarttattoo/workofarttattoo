#!/usr/bin/env python3
"""Sharpen Joshua / Katelyn / Teralyn entity positioning in key HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

JOSHUA_PIERCING_SECTION_RE = re.compile(
    r"<section class=\"py-24 relative z-10 bg-surface-container-low border-y border-outline-variant/10\">"
    r".*?"
    r"Piercing consults and jewelry planning</p>\s*</div>\s*</div>\s*</div>\s*</section>",
    re.DOTALL,
)

FOUNDER_SECTION_RE = re.compile(
    r"<!-- Founder Tech Projects -->.*?</section>\s*",
    re.DOTALL,
)

DEMOTED_PIERCING_SECTION = """
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-lowest relative z-10 border-t border-outline-variant/10" data-woa-joshua-piercing-secondary="1">
<div class="max-w-3xl mx-auto text-center space-y-4">
<span class="text-label-caps font-label-caps text-on-surface-variant uppercase tracking-[0.2em] block">Secondary note</span>
<h2 class="text-headline-md font-headline-md text-on-surface">Piercing at Work of Art</h2>
<p class="text-body-md text-on-surface-variant">Joshua Cole's primary work is black-and-grey realism tattooing. For professional piercing, ear curation, and jewelry fit, see <a class="text-secondary underline hover:no-underline" href="/artists/katelyn-cole/">Katelyn Cole</a> or <a class="text-secondary underline hover:no-underline" href="/artists/teralyn/">Teralyn</a>.</p>
</div>
</section>
"""

JOSHUA_HERO_FIRST_P = (
    "Joshua Cole is the studio lead and black-and-grey realism artist at Work of Art on E. "
    "Tropicana — portraits, wildlife, full sleeves, and complex cover-up/rework projects. "
    "He also accepts select fine-line and stipple-heavy work alongside his primary realism practice."
)

JOSHUA_SPECIALTY_LINKS = """<p class="font-body-md text-on-surface-variant mt-6 flex flex-wrap gap-x-4 gap-y-2">
<a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Joshua Cole — black and grey realism artist Las Vegas</a>
<a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up tattoo artist Joshua Cole</a>
<a class="text-secondary underline hover:no-underline" href="/healed_black_grey_tattoos_las_vegas/">Healed black &amp; grey gallery</a>
<a class="text-secondary underline hover:no-underline" href="/artists/teralyn/">Fine line with Teralyn</a>
</p>"""

ROSTER_THREE_RESIDENTS = (
    "Three in-studio residents today — Joshua Cole (studio lead, black-and-grey realism), "
    "Katelyn Cole (professional piercer), and Teralyn (fine-line tattoos and piercing; floral fine line, "
    "script, custom drawings, and detailed smaller tattoos). Tattoo and piercing consults book at "
    "2375 E. Tropicana Ave, Suite 3."
)
ROSTER_INLINE = (
    "Joshua Cole — studio lead, black-and-grey realism. Katelyn Cole — professional piercer. "
    "Teralyn — fine-line tattoos and piercing; floral fine line, script, custom drawings, and "
    "detailed smaller tattoos."
)
ROSTER_LEADS = (
    "Joshua Cole leads black-and-grey realism tattooing; Katelyn Cole is our professional piercer; "
    "Teralyn specializes in fine line, floral, script, and detailed smaller tattoos."
)

FINE_LINE_HERO_OLD = (
    "Looking for clean, detailed fine line tattoo work in Las Vegas? Joshua Cole and Teralyn "
    "tattoo floral, script, stipple, and single-needle pieces at Work of Art — real portfolio "
    "photos below. Book a consult when you know placement and approximate size."
)
FINE_LINE_HERO_NEW = (
    "Looking for clean, detailed fine line tattoo work in Las Vegas? Teralyn focuses on "
    "fine-line floral work, script, small detailed tattoos, and custom drawings at Work of Art. "
    "Studio lead Joshua Cole also accepts select fine-line and stipple-heavy projects alongside "
    "his primary black-and-grey realism work. Book a consult when you know placement and approximate size."
)

INTERNAL_LINK_BLOCKS: dict[str, str] = {
    "realism-tattoos-las-vegas": """
<p class="font-body-md text-on-surface-variant" data-woa-realism-joshua-link="1">
Planning a portrait, sleeve, or cover-up with Joshua Cole?
<a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua Cole — award-winning black and grey realism artist Las Vegas</a>
· <a class="text-secondary underline hover:no-underline" href="/healed_black_grey_tattoos_las_vegas/">Healed black &amp; grey proof</a>
</p>
""",
    "cover-up-tattoos-las-vegas": """
<p class="font-body-md text-on-surface-variant" data-woa-coverup-joshua-link="1">
Cover-up consults are led by
<a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua Cole — cover-up tattoo artist Las Vegas</a>
· <a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Black and grey realism guide</a>
</p>
""",
    "healed_black_grey_tattoos_las_vegas": """
<p class="font-body-md text-on-surface-variant" data-woa-healed-bg-joshua-link="1">
These healed results are primarily from
<a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">Joshua Cole — realism tattoo artist Las Vegas</a>
· <a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Realism tattoos guide</a>
</p>
""",
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": """
<p class="font-body-md text-on-surface-variant" data-woa-sleeve-joshua-link="1">
Large-scale sleeve planning with Joshua Cole:
<a class="text-secondary underline hover:no-underline" href="/artists/joshua-cole/">large-scale tattoo artist Joshua Cole</a>
· <a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Las Vegas Best Of realism tattoo artist</a>
</p>
""",
}


def patch_joshua_page(html: str) -> str:
    founder_match = FOUNDER_SECTION_RE.search(html)
    founder_block = founder_match.group(0) if founder_match else ""
    if founder_block:
        html = html.replace(founder_block, "", 1)

    html = JOSHUA_PIERCING_SECTION_RE.sub("", html, count=1)

    html = html.replace(
        "Joshua Cole builds custom black-and-grey work from consult through healed photos — "
        "portraits, wildlife, sleeves, and cover-ups at Work of Art on E. Tropicana.",
        JOSHUA_HERO_FIRST_P,
    )
    html = html.replace(
        "20+ Years Tattooing | Best of Las Vegas 2025 &amp; 2026 · BusinessRate.com",
        "Work of Art — Best of Las Vegas 2025 &amp; 2026 · BusinessRate.com",
    )
    old_links = """<p class="font-body-md text-on-surface-variant mt-6 flex flex-wrap gap-x-4 gap-y-2">
<a class="text-secondary underline hover:no-underline" href="/realism-tattoos-las-vegas/">Black &amp; grey realism guide</a>
<a class="text-secondary underline hover:no-underline" href="/cover-up-tattoos-las-vegas/">Cover-up tattoos in Las Vegas</a>
<a class="text-secondary underline hover:no-underline" href="/fine_line_tattoos_las_vegas_master_authority_guide/">Fine line tattoos</a>
</p>"""
    if old_links in html:
        html = html.replace(old_links, JOSHUA_SPECIALTY_LINKS, 1)

    if 'data-woa-joshua-piercing-secondary="1"' not in html:
        insert_before = "<!-- Footer -->"
        tail = DEMOTED_PIERCING_SECTION
        if founder_block:
            tail += founder_block
        if insert_before in html:
            html = html.replace(insert_before, tail + insert_before, 1)
        elif "</main>" in html:
            html = html.replace("</main>", tail + "</main>", 1)

    html = html.replace(
        "<li>Trained the in-studio team in piercing fundamentals</li>",
        "<li>Color realism, surrealistic work, and select fine-line projects</li>",
    )
    return html


def patch_fine_line_pages(html: str) -> str:
    html = html.replace(FINE_LINE_HERO_OLD, FINE_LINE_HERO_NEW)
    html = html.replace(
        "Joshua Cole specializes in fine line tattoos in vegas",
        "Teralyn specializes in fine line tattoos in Las Vegas",
    )
    html = html.replace(
        "Joshua Cole specializes in fine line",
        "Teralyn specializes in fine line",
    )
    return html


def patch_artists_index(html: str) -> str:
    html = html.replace(
        "Meet Joshua Cole, Katelyn Cole, and Teralyn at Work of Art in Las Vegas — custom tattoos, piercing, fineline floral work, script, and realism.",
        "Meet Joshua Cole (black-and-grey realism), Katelyn Cole (professional piercing), and Teralyn (fine-line tattoos) at Work of Art in Las Vegas.",
    )
    html = html.replace(
        "Joshua Cole (tattoo and piercing, studio lead), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fineline floral work, script, custom drawings by commission, and detailed smaller tattoos)",
        "Joshua Cole (studio lead, black-and-grey realism), Katelyn Cole (professional piercer), and Teralyn (fine-line tattoos and piercing; floral fine line, script, custom drawings by commission, and detailed smaller tattoos)",
    )
    return html


def inject_link_block(html: str, marker: str, block: str) -> str:
    if marker in html:
        return html
    if "<!-- Footer -->" in html:
        return html.replace("<!-- Footer -->", block + "\n<!-- Footer -->", 1)
    if "</main>" in html:
        return html.replace("</main>", block + "\n</main>", 1)
    return html


def patch_homepage(html: str) -> str:
    html = html.replace(
        "Our in-studio team includes Joshua Cole (tattoo and piercing, studio lead), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fineline floral, script, custom drawings by commission, and high-detail small tattoos). Book tattoo and piercing consults at our Tropicana studio.",
        "Our in-studio team includes Joshua Cole (studio lead, black-and-grey realism), Katelyn Cole (professional piercer), and Teralyn (fine-line tattoos and piercing; floral fine line, script, custom drawings by commission, and detailed smaller tattoos). Book tattoo and piercing consults at our Tropicana studio.",
    )
    html = html.replace(
        "Three in-studio residents today — Joshua Cole (tattoo artist and studio lead; also offers piercing), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fine line, floral, script, custom drawings, and detailed smaller tattoos). Tattoo and piercing consults book at 2375 E. Tropicana Ave, Suite 3.",
        ROSTER_THREE_RESIDENTS,
    )
    html = html.replace(
        "Joshua Cole — tattoo artist / studio lead; also offers piercing. Katelyn Cole — professional piercer. Teralyn — tattoo artist and piercer; fine line, floral, script, custom drawings, and detailed smaller tattoos.",
        ROSTER_INLINE,
    )
    html = html.replace(
        "Joshua Cole leads tattoo work and also offers piercing; Katelyn Cole is our professional piercer; Teralyn tattoos and pierces, including fine line, floral, script, and detailed smaller tattoos.",
        ROSTER_LEADS,
    )
    html = html.replace(
        "<span class=\"font-body-md text-[13px] text-on-surface-variant block mt-1\">Tattoo Artist / Studio Lead</span>",
        "<span class=\"font-body-md text-[13px] text-on-surface-variant block mt-1\">Black &amp; Grey Realism · Studio Lead</span>",
    )
    return html


def main() -> int:
    changed: list[str] = []

    joshua_path = ROOT / "artists" / "joshua-cole" / "code.html"
    if joshua_path.is_file():
        raw = joshua_path.read_text(encoding="utf-8")
        updated = patch_joshua_page(raw)
        if updated != raw:
            joshua_path.write_text(updated, encoding="utf-8")
            changed.append(str(joshua_path.relative_to(ROOT)))

    for slug in (
        "fine_line_tattoos_las_vegas_master_authority_guide",
        "best_fine_line_tattoos_in_vegas_ultimate_authority_guide",
    ):
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_fine_line_pages(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    artists_index = ROOT / "artists" / "code.html"
    if artists_index.is_file():
        raw = artists_index.read_text(encoding="utf-8")
        updated = patch_artists_index(raw)
        if updated != raw:
            artists_index.write_text(updated, encoding="utf-8")
            changed.append(str(artists_index.relative_to(ROOT)))

    homepage = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    if homepage.is_file():
        raw = homepage.read_text(encoding="utf-8")
        updated = patch_homepage(raw)
        if updated != raw:
            homepage.write_text(updated, encoding="utf-8")
            changed.append(str(homepage.relative_to(ROOT)))
            root_home = ROOT / "code.html"
            if root_home.is_file():
                root_home.write_text(updated, encoding="utf-8")
                changed.append(str(root_home.relative_to(ROOT)))

    for slug, block in INTERNAL_LINK_BLOCKS.items():
        path = ROOT / slug / "code.html"
        if not path.is_file():
            continue
        marker = re.search(r'data-woa-[^=]+="1"', block)
        marker_attr = marker.group(0) if marker else slug
        raw = path.read_text(encoding="utf-8")
        updated = inject_link_block(raw, marker_attr, block)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    print(f"[sharpen_entity_positioning] updated {len(changed)} files")
    for rel in changed:
        print(f"  - {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

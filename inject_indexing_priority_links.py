#!/usr/bin/env python3
"""Add a small, contextual second-discovery path to 30 high-value URLs.

This is intentionally not sitewide footer spam. Each block lives on an already
trusted/indexed parent page and points only to closely related content.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SECTIONS: dict[str, dict] = {
    "home_work_of_art_tattoo_piercing/code.html": {
        "id": "proof-trust",
        "heading": "More ways to evaluate the studio",
        "intro": "See the work, the client experience, and booking options beyond the main service pages.",
        "links": [
            ("/studio_gallery/", "Full studio portfolio"),
            ("/reviews/", "Client reviews"),
            ("/offsite_bookings/", "Private event and offsite tattoo bookings"),
        ],
    },
    "realism-tattoos-las-vegas/code.html": {
        "id": "realism-healed-proof",
        "heading": "More healed-work proof",
        "intro": "Compare finished work by style before choosing a direction for your piece.",
        "links": [
            ("/healed_black_grey_tattoos_las_vegas/", "Healed black and grey tattoos"),
            ("/healed_color_tattoos_las_vegas/", "Healed color tattoos"),
            ("/healed_portrait_tattoos_las_vegas/", "Healed portrait tattoos"),
        ],
    },
    "cover-up-tattoos-las-vegas/code.html": {
        "id": "coverup-planning",
        "heading": "Plan a cover-up with the old tattoo in mind",
        "intro": "Two supporting guides explain why darkness, existing pigment, and scar tissue change the design plan.",
        "links": [
            ("/knowledge/how-dark-can-cover-up-tattoo-be/", "How dark does a cover-up need to be?"),
            ("/scar_tissue_tattoo_skin_science_las_vegas_authority_guide/", "Tattooing over scar tissue"),
        ],
    },
    "fine_line_tattoos_las_vegas_master_authority_guide/code.html": {
        "id": "fine-line-longevity",
        "heading": "Fine-line longevity",
        "intro": "See what changes over time and which design choices help small details stay readable.",
        "links": [
            ("/knowledge/fine-line-tattoo-longevity/", "How fine-line tattoos age"),
        ],
    },
    "piercing-shop-standards/code.html": {
        "id": "piercing-standards-planning-guides",
        "heading": "Piercing planning guides from Katelyn's specialty areas",
        "intro": "Use these guides to narrow placement, healing, jewelry, and anatomy questions before booking.",
        "links": [
            ("/ear_piercing_guide_las_vegas/", "Ear piercing guide"),
            ("/facial_piercing_guide_las_vegas/", "Facial piercing guide"),
            ("/piercing_aftercare_guide_las_vegas/", "Piercing aftercare"),
            ("/piercing_healing_guide_las_vegas/", "Piercing healing timelines"),
            ("/piercing_jewelry_guide_las_vegas/", "Piercing jewelry guide"),
            ("/katelyn_ear_curation_las_vegas_authority_guide/", "Ear curation planning"),
            ("/katelyn_downsizing_jewelry_las_vegas_authority_guide/", "Jewelry downsizing"),
            ("/katelyn_anatomy_matters_las_vegas_authority_guide/", "Why anatomy matters"),
        ],
    },
    "katelyn_cole_piercing_authority_hub_las_vegas/code.html": {
        "id": "piercing-placement-deep-dives",
        "heading": "Placement deep-dives",
        "intro": "Compare individual placements once you know the general area you want pierced.",
        "links": [
            ("/oral_piercing_guide_las_vegas/", "Oral piercing guide"),
            ("/body_piercing_guide_las_vegas/", "Body piercing guide"),
            ("/conch_piercing_las_vegas_authority_guide/", "Conch piercing"),
            ("/daith_piercing_las_vegas_authority_guide/", "Daith piercing"),
            ("/industrial_piercing_las_vegas_authority_guide/", "Industrial piercing"),
            ("/nose_piercing_las_vegas_authority_guide/", "Nose piercing"),
            ("/tragus_piercing_las_vegas_authority_guide/", "Tragus piercing"),
            ("/eyebrow_piercing_las_vegas_authority_guide/", "Eyebrow piercing"),
        ],
    },
    "tattoo-skin-science/code.html": {
        "id": "skin-science-deep-dives",
        "heading": "Skin science deep-dives",
        "intro": "Go deeper into the specific structures and healing variables that affect tattoo planning.",
        "links": [
            ("/dermis_skin_science_las_vegas_authority_guide/", "Dermis: where tattoo ink lives"),
            ("/collagen_skin_science_las_vegas_authority_guide/", "Collagen and tattoo healing"),
            ("/macrophages_skin_science_las_vegas_authority_guide/", "Macrophages and tattoo pigment"),
            ("/aging_skin_skin_science_las_vegas_authority_guide/", "Aging skin and tattoos"),
            ("/stretch_marks_skin_science_las_vegas_authority_guide/", "Stretch marks and tattoo planning"),
        ],
    },
}

PRIORITY_30: tuple[str, ...] = tuple(
    href
    for section in SECTIONS.values()
    for href, _label in section["links"]
)


def render_block(section: dict) -> str:
    marker = f'data-woa-indexing-priority-links="{escape(section["id"])}"'
    items = "\n".join(
        f'<li><a class="text-secondary underline hover:no-underline" href="{escape(href)}">{escape(label)}</a></li>'
        for href, label in section["links"]
    )
    return f"""
<section class="py-10 px-margin-mobile md:px-margin-desktop border-t border-outline-variant/20 bg-surface-container-low/40" {marker}>
  <div class="max-w-5xl mx-auto space-y-4">
    <h2 class="font-headline-md text-on-surface text-2xl">{escape(section["heading"])}</h2>
    <p class="font-body-md text-on-surface-variant leading-relaxed">{escape(section["intro"])}</p>
    <nav aria-label="{escape(section["heading"])}">
      <ul class="grid gap-2 md:grid-cols-2 font-body-md text-on-surface-variant">
        {items}
      </ul>
    </nav>
  </div>
</section>
""".strip()


def insert_before_main_end(html: str, block: str, marker: str) -> str:
    if marker in html:
        return html
    pos = html.lower().rfind("</main>")
    if pos == -1:
        raise RuntimeError("Page has no closing </main>")
    return html[:pos] + "\n" + block + "\n" + html[pos:]


def main() -> int:
    if len(PRIORITY_30) != 30 or len(set(PRIORITY_30)) != 30:
        raise RuntimeError(f"Priority list must contain exactly 30 unique URLs; got {len(PRIORITY_30)}")

    changed = 0
    for rel, section in SECTIONS.items():
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        raw = path.read_text(encoding="utf-8")
        marker = f'data-woa-indexing-priority-links="{section["id"]}"'
        updated = insert_before_main_end(raw, render_block(section), marker)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] indexing-priority links: {rel} ({len(section['links'])})")

    print(f"[done] {changed} parent pages updated; {len(PRIORITY_30)} unique priority URLs linked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Align static pages with Yoast-style SEO: meta descriptions, OG/Twitter images."""

from __future__ import annotations

import re
from html import escape, unescape
from pathlib import Path

from woa_nav_config import GUIDE_META

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"
DEFAULT_OG = (
    f"{SITE}/home_work_of_art_tattoo_piercing/"
    "las-vegas-tattoo-hero-background.webp"
)

# Prefer a strong share image per guide (file must exist in slug folder or path below)
OG_IMAGE: dict[str, str] = {
    "home_work_of_art_tattoo_piercing": DEFAULT_OG,
    "cover-up-tattoos-las-vegas": (
        f"{SITE}/cover-up-tattoos-las-vegas/"
        "floral-tattoo-cover-up-before-after-las-vegas.webp"
    ),
    "walk_in_tattoos_las_vegas_authority_guide": (
        f"{SITE}/image_5_22_26_at_9.11_pm_1.png/"
        "professional-tattoo-artist-work-of-art-las-vegas-studio.webp"
    ),
    "realism_tattoos_las_vegas_master_authority_guide": (
        f"{SITE}/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp"
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide": (
        f"{SITE}/fine_line_tattoos_las_vegas_master_authority_guide/"
        "realism-tattoos-grim-reaper-dark-art.webp"
    ),
    "best_fine_line_tattoos_in_vegas_ultimate_authority_guide": (
        f"{SITE}/best_fine_line_tattoos_in_vegas_ultimate_authority_guide/"
        "best-tattoo-las-vegas-custom-sleeve-by-master-artist.webp"
    ),
    "best_piercing_shop_las_vegas_updated_jewelry_standards": (
        f"{SITE}/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp"
    ),
    "piercing-specials-las-vegas": (
        f"{SITE}/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp"
    ),
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": (
        f"{SITE}/best_tattoo_styles_for_sleeves_large_scale_project_hub/"
        "black-and-grey-artistry-dynamic-snake-masterpiece.webp"
    ),
    "appointments": (
        f"{SITE}/image_5_22_26_at_9.11_pm_1.png/"
        "professional-tattoo-artist-work-of-art-las-vegas-studio.webp"
    ),
    "artists": f"{SITE}/artists/joshua-cole/joshua-cole-portrait-las-vegas.webp",
    "reviews_vault_100_verified_masterpieces": (
        f"{SITE}/home_work_of_art_tattoo_piercing/client-portfolio/black-grey-lion-thigh-realism-las-vegas.webp"
    ),
    "review_funnel_google_authority_hub": DEFAULT_OG,
    "tattoo_pain_chart_placement_sensitivity_guide": (
        f"{SITE}/img_0131.jpeg/realism-tattoos-floral-and-roman-numeral-sleeve.webp"
    ),
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": (
        f"{SITE}/how_much_do_tattoos_cost_in_las_vegas_authority_guide/"
        "custom-tattoos-las-vegas-flying-dove-realism.webp"
    ),
}

DESC_EXTRA: dict[str, str] = {
    "appointments": (
        "Book tattoo and piercing appointments at Work of Art in Las Vegas — "
        "custom tattoos, consults, and walk-ins. 2375 E. Tropicana Ave, Suite 3. (725) 224-1240."
    ),
    "home_work_of_art_tattoo_piercing": (
        "Las Vegas tattoo and piercing studio on E. Tropicana — custom tattoos, "
        "black and grey realism, color work, cover-ups, and walk-ins. (725) 224-1240."
    ),
    "artists": (
        "Meet Joshua Cole, Katelyn Cole, and Teralyn at Work of Art in Las Vegas — "
        "custom tattoos, piercing, fineline floral work, script, and realism."
    ),
    "piercing-specials-las-vegas": (
        "Current piercing specials at Work of Art Las Vegas with Katelyn Cole — "
        "same-day availability, booking, jewelry-fit planning, aftercare, and directions."
    ),
}


def yoast_trim(text: str, max_len: int = 155) -> str:
    plain = unescape(text).strip()
    if len(plain) <= max_len:
        return plain
    cut = plain[: max_len - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def description_for(slug: str, title: str) -> str:
    if slug in DESC_EXTRA:
        return yoast_trim(DESC_EXTRA[slug])
    if slug in GUIDE_META:
        _label, blurb = GUIDE_META[slug]
        base = f"{blurb} Work of Art Tattoo & Piercing, Las Vegas — E. Tropicana."
        return yoast_trim(base)
    return yoast_trim(
        f"{title} — Work of Art Tattoo & Piercing, Las Vegas. "
        "Custom tattoos, piercing, and walk-ins near the Strip."
    )


def canonical_for(slug: str) -> str:
    if slug.startswith("home_work_of_art"):
        return f"{SITE}/"
    return f"{SITE}/{slug}/"


def og_image_for(slug: str) -> str:
    if slug in OG_IMAGE:
        return OG_IMAGE[slug]
    folder = ROOT / slug
    if folder.is_dir():
        for ext in ("*.webp", "*.png"):
            hits = sorted(folder.glob(ext))
            if hits:
                return f"{SITE}/{slug}/{hits[0].name}"
    return DEFAULT_OG


def parse_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html, re.I)
    return unescape(m.group(1).strip()) if m else "Work of Art Tattoo & Piercing | Las Vegas"


def replace_meta(html: str, *, name: str | None = None, prop: str | None = None, content: str) -> str:
    esc = escape(content)
    if name:
        pat = rf'(<meta\s+content=")[^"]*("(?:\s+name="{re.escape(name)}"|\s+name=\'{re.escape(name)}\'))'
        if re.search(pat, html, re.I):
            return re.sub(pat, rf"\1{esc}\2", html, count=1, flags=re.I)
        pat2 = rf'(<meta\s+name="{re.escape(name)}"\s+content=")[^"]*(")'
        if re.search(pat2, html, re.I):
            return re.sub(pat2, rf"\1{esc}\2", html, count=1, flags=re.I)
    if prop:
        pat = rf'(<meta\s+content=")[^"]*("\s+property="{re.escape(prop)}")'
        if re.search(pat, html, re.I):
            return re.sub(pat, rf"\1{esc}\2", html, count=1, flags=re.I)
    return html


def insert_head_block(html: str, block: str) -> str:
    m = re.search(r'(<meta\s+content="width=device-width[^>]*>)', html, re.I)
    if m:
        return html[: m.end()] + "\n" + block + html[m.end() :]
    m2 = re.search(r"(<head[^>]*>)", html, re.I)
    if m2:
        return html[: m2.end()] + "\n" + block + html[m2.end() :]
    return html


def build_head_extras(title: str, desc: str, slug: str) -> str:
    url = canonical_for(slug)
    image = og_image_for(slug)
    t, d = escape(title), escape(desc)
    lines = [
        f'<title>{t}</title>',
        f'<meta content="{d}" name="description"/>',
        f'<link href="{url}" rel="canonical"/>',
        '<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>',
        '<meta content="website" property="og:type"/>',
        f'<meta content="{url}" property="og:url"/>',
        f'<meta content="{t}" property="og:title"/>',
        f'<meta content="{d}" property="og:description"/>',
        f'<meta content="{image}" property="og:image"/>',
        '<meta content="1200" property="og:image:width"/>',
        '<meta content="630" property="og:image:height"/>',
        '<meta content="en_US" property="og:locale"/>',
        '<meta content="Work of Art Tattoo &amp; Piercing" property="og:site_name"/>',
        '<meta content="summary_large_image" name="twitter:card"/>',
        f'<meta content="{t}" name="twitter:title"/>',
        f'<meta content="{d}" name="twitter:description"/>',
        f'<meta content="{image}" name="twitter:image"/>',
    ]
    return "\n".join(lines)


def fix_file(path: Path) -> list[str]:
    changes: list[str] = []
    slug = path.parent.name
    html = path.read_text(encoding="utf-8")
    original = html

    if not re.search(r"<title>", html, re.I):
        title = "Tattoo Pain Chart Las Vegas | Placement Guide | Work of Art"
        if slug == "tattoo_pain_chart_placement_sensitivity_guide":
            title = "Tattoo Pain Chart Las Vegas | Placement Guide | Work of Art"
        desc = description_for(slug, title)
        html = insert_head_block(html, build_head_extras(title, desc, slug))
        changes.append("head+seo")
    else:
        title = parse_title(html)
        desc = description_for(slug, title)
        if re.search(r'name=["\']description["\']', html, re.I):
            html = replace_meta(html, name="description", content=desc)
        else:
            m = re.search(r"(</title>)", html, re.I)
            if m:
                html = (
                    html[: m.end()]
                    + f'\n<meta content="{escape(desc)}" name="description"/>'
                    + html[m.end() :]
                )
            changes.append("description")

        image = og_image_for(slug)
        if 'property="og:description"' in html:
            html = replace_meta(html, prop="og:description", content=desc)
        if 'property="og:image"' in html:
            html = replace_meta(html, prop="og:image", content=image)
        if 'property="og:title"' in html:
            html = replace_meta(html, prop="og:title", content=title)
        if 'property="og:url"' in html:
            html = replace_meta(html, prop="og:url", content=canonical_for(slug))

        if 'name="twitter:description"' in html or "twitter:description" in html:
            html = replace_meta(html, name="twitter:description", content=desc)
        else:
            # insert after twitter:card if present
            m = re.search(r'(<meta[^>]+name="twitter:card"[^>]*>)', html, re.I)
            if m:
                ins = (
                    f'\n<meta content="{escape(title)}" name="twitter:title"/>'
                    f'\n<meta content="{escape(desc)}" name="twitter:description"/>'
                    f'\n<meta content="{image}" name="twitter:image"/>'
                )
                html = html[: m.end()] + ins + html[m.end() :]
                changes.append("twitter")

        if 'property="og:image"' not in html:
            m = re.search(r'(<meta[^>]+property="og:description"[^>]*>)', html, re.I)
            if m:
                block = (
                    f'\n<meta content="{image}" property="og:image"/>'
                    '\n<meta content="1200" property="og:image:width"/>'
                    '\n<meta content="630" property="og:image:height"/>'
                )
                html = html[: m.end()] + block + html[m.end() :]
                changes.append("og:image")

        if 'name="twitter:image"' in html:
            html = replace_meta(html, name="twitter:image", content=image)

        # Replace generic fallback og description
        generic = "Las Vegas tattoo shop and piercing studio on E. Tropicana — Work of Art."
        if generic in html:
            html = html.replace(generic, desc)
            changes.append("generic-og-desc")

    if html != original:
        path.write_text(html, encoding="utf-8")
    return changes


def main() -> int:
    updated = 0
    for path in sorted(ROOT.glob("*/code.html")):
        if path.parent.name.startswith("."):
            continue
        ch = fix_file(path)
        if ch:
            print(f"{path.parent.name}: {', '.join(ch)}")
            updated += 1
    print(f"Updated {updated} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

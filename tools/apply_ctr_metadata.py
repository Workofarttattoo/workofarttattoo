#!/usr/bin/env python3
"""Preserve approved October 2026 CTR title/description edits after all page builders.

Run after angel-number injection: generated code.html and index.html are the
published artifacts. The build pipeline otherwise replaces edited page heads.
"""
from __future__ import annotations
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "cover-up-tattoos-las-vegas": (
        "Cover-Up Tattoos Las Vegas | Real Results & Consultations",
        "See real cover-up tattoo results in Las Vegas. Joshua Cole designs custom solutions for unwanted ink and scars. Send photos to discuss your options.",
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": (
        "Tattoo Prices Las Vegas | $100 Minimum & $200/hr",
        "Tattoo prices at Work of Art in Las Vegas start at $100; larger custom work is $200 per hour. See pricing factors and request a quote from Joshua.",
    ),
    "knowledge/tattoo-on-ribs-recovery": (
        "Rib Tattoo Pain & Healing Time | What to Expect",
        "How much do rib tattoos hurt, and how long do they heal? Learn about breathing, clothing, sleep and aftercare from a Las Vegas tattoo studio.",
    ),
    "epidermis_skin_science_las_vegas_authority_guide": (
        "Epidermis & Tattoos | Peeling, Healing and Ink",
        "Why does a tattoo peel, and where does the ink actually stay? Understand the epidermis, healing skin and tattoo longevity with our studio guide.",
    ),
    "tattoo-skin-science": (
        "Tattoo Skin Science | How Ink Heals and Ages",
        "Explore how tattoo ink settles in skin, why tattoos heal and fade, and how skin conditions affect results. Practical guidance from Work of Art Las Vegas.",
    ),
    "knowledge/best-soap-for-tattoo-aftercare": (
        "Best Soap for a New Tattoo | Safe Washing Guide",
        "Learn what to look for in a gentle, fragrance-free soap for fresh tattoos, what ingredients to avoid, and how to wash healing skin without scrubbing.",
    ),
    "las-vegas-tattoo-healing-guide": (
        "Fresh vs Healed Tattoos | Real Las Vegas Results",
        "See real fresh and healed tattoo photos from Work of Art Las Vegas. Compare how lines, shading and color settle as tattoos heal over time.",
    ),
    "knowledge/how-long-tattoo-session-last": (
        "How Long Does a Tattoo Take? Sessions by Size",
        "From small designs to large sleeves, learn what affects tattoo session length, why breaks matter and how to plan your appointment in Las Vegas.",
    ),
    "scar_tissue_tattoo_skin_science_las_vegas_authority_guide": (
        "Tattooing Over Scars | Timing, Risks & Cover-Ups",
        "Can you tattoo over a scar? Learn why scar maturity, texture and location matter, plus what to discuss during a cover-up consultation in Las Vegas.",
    ),
    "healed_tattoo_gallery_las_vegas": (
        "Healed Tattoo Gallery Las Vegas | Real Studio Photos",
        "Browse real healed tattoos from Work of Art in Las Vegas, including black-and-grey, fine-line, color and cover-up work. See how finished tattoos settle.",
    ),
}

TITLE_RE = re.compile(r"<title\b[^>]*>[\s\S]*?</title>", re.I)
META_RE = re.compile(r"<meta\b[^>]*>", re.I)
CONTENT_RE = re.compile(r'\bcontent\s*=\s*"[^"]*"', re.I | re.S)

def update_head(raw: str, title: str, description: str) -> str:
    safe_title, safe_desc = html.escape(title, quote=True), html.escape(description, quote=True)
    if len(TITLE_RE.findall(raw)) != 1:
        raise ValueError("Expected exactly one title tag")
    raw = TITLE_RE.sub(lambda _: "<title>" + safe_title + "</title>", raw)
    found_description = 0
    def change_meta(match: re.Match[str]) -> str:
        nonlocal found_description
        tag = match.group(0)
        lowered = tag.lower()
        kind = None
        if re.search(r'\bname\s*=\s*"description"', lowered):
            kind = "description"
            found_description += 1
        elif re.search(r'\bproperty\s*=\s*"og:title"', lowered) or re.search(r'\bname\s*=\s*"twitter:title"', lowered):
            kind = "title"
        elif re.search(r'\bproperty\s*=\s*"og:description"', lowered) or re.search(r'\bname\s*=\s*"twitter:description"', lowered):
            kind = "description"
        if kind is None:
            return tag
        content = safe_title if kind == "title" else safe_desc
        replacement = 'content="' + content + '"'
        if CONTENT_RE.search(tag):
            return CONTENT_RE.sub(lambda _: replacement, tag, count=1)
        return tag[:-1] + " " + replacement + ">"
    raw = META_RE.sub(change_meta, raw)
    if found_description != 1:
        raise ValueError("Expected exactly one meta description, got " + str(found_description))
    return raw

def main() -> None:
    changed = 0
    for slug, (title, description) in PAGES.items():
        for name in ("code.html", "index.html"):
            path = ROOT / slug / name
            if not path.is_file():
                raise SystemExit("Missing SEO page: " + str(path))
            original = path.read_text(encoding="utf-8")
            revised = update_head(original, title, description)
            if revised != original:
                path.write_text(revised, encoding="utf-8")
                changed += 1
    print("Applied approved CTR metadata to 10 pages, " + str(changed) + " files updated")

if __name__ == "__main__":
    main()

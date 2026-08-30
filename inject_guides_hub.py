#!/usr/bin/env python3
"""
1) Sticky guide hub bar on every informational guide page (obvious clickable links).
2) Homepage knowledge-base section listing every guide with a short blurb.

  python3 inject_guides_hub.py
  python3 inject_guides_hub.py --guides-only
  python3 inject_guides_hub.py --home-only
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import (
    HOME_SLUG,
    HREF_GUIDES_INDEX,
    HREF_KNOWLEDGE_VAULT,
    NAV_KNOWLEDGE_VAULT_LINK_LABEL,
    SKIP_GUIDE_SLUGS,
    discover_guide_entries,
    merged_export_roots,
    slug_to_guide_label,
)
from woa_start_here import START_HERE_PATHS

ROOT = Path(__file__).resolve().parent

# Homepage vault — links to Start Here hub (full intent paths live on /start_here/)
HOME_VAULT_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = ()

RECENTLY_UPDATED: tuple[tuple[str, str, str], ...] = (
    ("Tattoo Healing Database — timeline encyclopedia", "/healing_database_tattoo_timeline_encyclopedia_las_vegas/", "June 2026"),
    ("New healed black & grey gallery", "/healed_black_grey_tattoos_las_vegas/", "June 2026"),
    ("Complete helix piercing guide", "/helix_piercing_las_vegas_authority_guide/", "June 2026"),
    ("Piercing jewelry guide", "/piercing_jewelry_guide_las_vegas/", "June 2026"),
    ("Katelyn Cole — ear curation authority", "/katelyn_ear_curation_las_vegas_authority_guide/", "June 2026"),
    ("Desert piercing aftercare", "/piercing_aftercare_desert_climate_las_vegas_expert_guide/", "June 2026"),
    ("Real client tattoo timeline", "/real_client_tattoo_timeline_las_vegas/", "June 2026"),
)

PIERCING_HUB_SLUG = "piercing_types_las_vegas_authority_hub"
PIERCING_HUB_HREF = f"/{PIERCING_HUB_SLUG}/"

# Deep authority pages get a slim bar — full pill scroll stays on hub / homepage only.
COMPACT_HUB_SUFFIXES = (
    "_piercing_las_vegas_authority_guide",
    "_las_vegas_master_authority_guide",
    "_las_vegas_authority_guide",
    "_expert_aftercare_guide",
    "_large_scale_project_hub",
    "_selection_guide_2",
    "_ultimate_authority_guide",
    "_expert_guide",
    "_skin_science_las_vegas_authority_guide",
)

FULL_HUB_SLUGS = frozenset(
    {
        HOME_SLUG,
        PIERCING_HUB_SLUG,
        "katelyn_cole_piercing_authority_hub_las_vegas",
        "ear_piercing_guide_las_vegas",
        "facial_piercing_guide_las_vegas",
        "oral_piercing_guide_las_vegas",
        "body_piercing_guide_las_vegas",
        "piercing_aftercare_guide_las_vegas",
        "piercing_jewelry_guide_las_vegas",
        "piercing_healing_guide_las_vegas",
        "piercing_aftercare_desert_climate_las_vegas_expert_guide",
        "skin_science_tattoo_dermatology_authority_guide",
        "healing_database_tattoo_timeline_encyclopedia_las_vegas",
    }
)

HUB_STYLE = """
/* Work of Art — guide hub bar + knowledge base (inject_guides_hub.py) */
[data-woa-guide-hub-bar] {
  position: sticky;
  top: 4.25rem;
  z-index: 45;
  border-bottom: 1px solid rgba(68, 71, 72, 0.55);
  background: rgba(19, 19, 19, 0.96);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
[data-woa-guide-hub-bar] .woa-guide-hub-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.65rem;
  padding: 0.75rem 0;
  max-height: 9.5rem;
  overflow-y: auto;
}
[data-woa-guide-hub-bar][data-woa-guide-hub-compact="1"] .woa-guide-hub-scroll {
  max-height: none;
  overflow: visible;
}
[data-woa-guide-hub-bar] .woa-guide-pill {
  display: inline-flex;
  align-items: center;
  min-height: 2.25rem;
  padding: 0.35rem 0.85rem;
  border: 1px solid rgba(142, 145, 146, 0.45);
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 600;
  line-height: 1.25;
  color: #e5e2e1;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
[data-woa-guide-hub-bar] .woa-guide-pill:hover {
  border-color: #e9c349;
  color: #e9c349;
}
[data-woa-guide-hub-bar] .woa-guide-pill.is-current {
  background: rgba(233, 195, 73, 0.14);
  border-color: #e9c349;
  color: #e9c349;
}
[data-woa-guide-hub-bar] .woa-guide-pill-vault {
  border-color: rgba(233, 195, 73, 0.65);
  color: #e9c349;
  font-weight: 700;
}
[data-woa-guide-hub-bar] .woa-guide-pill-current-label {
  display: inline-flex;
  align-items: center;
  min-height: 2.25rem;
  padding: 0.35rem 0.85rem;
  border: 1px solid rgba(233, 195, 73, 0.35);
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #c4c7c7;
  white-space: nowrap;
}
#knowledge-base .woa-kb-card {
  display: block;
  padding: 1.25rem 1.5rem;
  border: 1px solid rgba(68, 71, 72, 0.55);
  background: rgba(32, 32, 31, 0.85);
  transition: border-color 0.2s, background 0.2s;
}
#knowledge-base .woa-kb-card:hover {
  border-color: rgba(233, 195, 73, 0.55);
  background: rgba(42, 42, 42, 0.95);
}
#knowledge-base .woa-kb-card h3 {
  margin: 0 0 0.5rem;
}
#homepage .woa-kb-card p {
  margin: 0;
}
#recently-updated .woa-update-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.5rem 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(68, 71, 72, 0.45);
}
#recently-updated .woa-update-row:last-child {
  border-bottom: none;
}
#recently-updated a {
  color: #e5e2e1;
  text-decoration: none;
  font-weight: 600;
}
#recently-updated a:hover {
  color: #e9c349;
}
#recently-updated time {
  font-size: 0.8125rem;
  color: #8e9192;
  white-space: nowrap;
}
#knowledge-base .woa-kb-group {
  max-width: 72rem;
  margin: 0 auto 1.5rem;
  border: 1px solid rgba(68, 71, 72, 0.45);
  background: rgba(25, 25, 25, 0.6);
}
#knowledge-base .woa-kb-group summary {
  cursor: pointer;
  list-style: none;
  padding: 1rem 1.25rem;
  font-weight: 700;
  color: #e5e2e1;
}
#knowledge-base .woa-kb-group summary::-webkit-details-marker {
  display: none;
}
#knowledge-base .woa-kb-group[open] summary {
  border-bottom: 1px solid rgba(68, 71, 72, 0.45);
  color: #e9c349;
}
#knowledge-base .woa-kb-group-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  padding: 1rem 1.25rem 1.25rem;
}
@media (min-width: 768px) {
  #knowledge-base .woa-kb-group-grid {
    grid-template-columns: 1fr 1fr;
  }
}
#knowledge-base .woa-kb-browse {
  text-align: center;
  padding-top: 1rem;
}
#knowledge-base .woa-kb-browse a {
  color: #e9c349;
  font-weight: 600;
  text-decoration: underline;
}
#knowledge-base .woa-start-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 3rem;
  padding: 0.75rem 2rem;
  background: #e9c349;
  color: #131313;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.8125rem;
  transition: opacity 0.2s;
}
#knowledge-base .woa-start-cta:hover {
  opacity: 0.92;
}
#knowledge-base .woa-intent-chip {
  display: block;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(68, 71, 72, 0.55);
  background: rgba(32, 32, 31, 0.85);
  font-size: 0.9375rem;
  color: #e5e2e1;
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s;
}
#knowledge-base .woa-intent-chip:hover {
  border-color: rgba(233, 195, 73, 0.55);
  color: #e9c349;
}
"""


def ensure_hub_css(soup: BeautifulSoup) -> None:
    head = soup.find("head")
    if not head:
        return
    for st in head.find_all("style"):
        if st.get("data-woa-guide-hub-css") == "1" or (
            st.string and "[data-woa-guide-hub-bar]" in (st.string or "")
        ):
            st.decompose()
    tag = soup.new_tag("style", attrs={"data-woa-guide-hub-css": "1"})
    tag.string = HUB_STYLE
    head.append(tag)


def uses_compact_hub(slug: str) -> bool:
    if slug in FULL_HUB_SLUGS:
        return False
    if slug.startswith("katelyn_") and slug.endswith("_authority_guide"):
        return True
    return any(slug.endswith(suffix) for suffix in COMPACT_HUB_SUFFIXES)


def parent_hub_for(slug: str) -> tuple[str, str] | None:
    if "piercing" in slug or slug.startswith("katelyn_"):
        return ("All piercing guides", PIERCING_HUB_HREF)
    return ("All tattoo guides", HREF_KNOWLEDGE_VAULT)


def build_guide_hub_bar(soup: BeautifulSoup, current_slug: str | None) -> BeautifulSoup:
    """Slim contextual bar — never list every guide (avoids sitemap-style nav)."""
    wrap = soup.new_tag(
        "nav",
        attrs={
            "aria-label": "Related guides",
            "data-woa-guide-hub-bar": "1",
            "data-woa-guide-hub-compact": "1",
            "class": [
                "px-margin-mobile",
                "md:px-margin-desktop",
            ],
        },
    )
    inner = soup.new_tag("div", attrs={"class": ["woa-guide-hub-scroll"]})
    vault = soup.new_tag(
        "a",
        href=HREF_KNOWLEDGE_VAULT,
        attrs={"class": ["woa-guide-pill", "woa-guide-pill-vault"]},
    )
    vault.string = NAV_KNOWLEDGE_VAULT_LINK_LABEL
    inner.append(vault)

    if current_slug:
        parent_label, parent_href = parent_hub_for(current_slug) or (
            "All guides",
            HREF_GUIDES_INDEX,
        )
        parent = soup.new_tag("a", href=parent_href, attrs={"class": ["woa-guide-pill"]})
        parent.string = parent_label
        inner.append(parent)
        current = soup.new_tag("span", attrs={"class": ["woa-guide-pill-current-label"]})
        current.string = slug_to_guide_label(current_slug, max_len=42)
        inner.append(current)
    wrap.append(inner)
    return wrap


def insert_before_main(soup: BeautifulSoup, node) -> bool:
    main = soup.find("main")
    if main:
        main.insert_before(node)
        return True
    body = soup.find("body")
    if not body:
        return False
    # Fallback: first page section after fixed header
    for child in body.children:
        if getattr(child, "name", None) in ("main", "section", "header"):
            if child.name == "header" and child.get("class"):
                cls = " ".join(child.get("class") or [])
                if "fixed" in cls or "sticky" in cls:
                    continue
            child.insert_before(node)
            return True
    body.insert(0, node)
    return True


def inject_guide_hub_bar(path: Path, slug: str, *, force: bool = False) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    has_bar = 'data-woa-guide-hub-bar="1"' in raw
    if has_bar and not force:
        return False
    soup = BeautifulSoup(raw, "html.parser")
    if has_bar and force:
        old = soup.find(attrs={"data-woa-guide-hub-bar": True})
        if old:
            old.decompose()
    ensure_hub_css(soup)
    bar = build_guide_hub_bar(soup, slug)
    if not insert_before_main(soup, bar):
        return False
    path.write_text(str(soup), encoding="utf-8")
    return True


def _kb_card(soup: BeautifulSoup, label: str, href: str, blurb: str):
    card = soup.new_tag("a", href=href, attrs={"class": ["woa-kb-card", "group"]})
    h3 = soup.new_tag(
        "h3",
        attrs={
            "class": [
                "font-headline-md",
                "text-[18px]",
                "text-on-surface",
                "group-hover:text-secondary",
                "transition-colors",
            ]
        },
    )
    h3.string = label
    p = soup.new_tag("p", attrs={"class": ["font-body-md", "text-on-surface-variant"]})
    p.string = blurb
    card.extend([h3, p])
    return card


def build_knowledge_base_section(soup: BeautifulSoup) -> BeautifulSoup:
    sec = soup.new_tag(
        "section",
        attrs={
            "id": "knowledge-base",
            "class": [
                "py-16",
                "md:py-section-gap",
                "px-margin-mobile",
                "md:px-margin-desktop",
                "bg-surface-container-low",
                "border-y",
                "border-outline-variant/10",
            ],
        },
    )
    head = soup.new_tag("div", attrs={"class": ["max-w-4xl", "mx-auto", "space-y-4", "mb-12", "text-center"]})
    span = soup.new_tag(
        "span",
        attrs={
            "class": [
                "font-label-caps",
                "text-label-caps",
                "text-secondary",
                "uppercase",
                "tracking-[0.2em]",
            ]
        },
    )
    span.string = "Guides & resources"
    h2 = soup.new_tag("h2", attrs={"class": ["font-headline-lg", "text-headline-lg", "text-on-surface"]})
    h2.string = "Not sure where to begin?"
    intro = soup.new_tag(
        "p",
        attrs={"class": ["font-body-lg", "text-body-lg", "text-on-surface-variant", "max-w-2xl", "mx-auto"]},
    )
    intro.string = (
        "Pick your situation on our Start Here page — first tattoo, Vegas visit, piercing, "
        "cover-up, healed proof, pricing, or meeting our artists."
    )
    cta_wrap = soup.new_tag("div", attrs={"class": ["pt-2"]})
    cta = soup.new_tag("a", href=HREF_KNOWLEDGE_VAULT, attrs={"class": ["woa-start-cta"]})
    cta.string = NAV_KNOWLEDGE_VAULT_LINK_LABEL.title()
    cta_wrap.append(cta)
    head.extend([span, h2, intro, cta_wrap])

    chip_grid = soup.new_tag(
        "div",
        attrs={"class": ["grid", "grid-cols-1", "sm:grid-cols-2", "lg:grid-cols-3", "gap-3", "max-w-4xl", "mx-auto", "mt-10", "text-left"]},
    )
    for path in START_HERE_PATHS:
        chip = soup.new_tag("a", href=f"{HREF_KNOWLEDGE_VAULT}#{path.anchor}", attrs={"class": ["woa-intent-chip"]})
        chip.string = path.title
        chip_grid.append(chip)
    head.append(chip_grid)

    groups_wrap = soup.new_tag("div", attrs={"class": ["space-y-4"]})
    by_slug = {slug: (label, href, blurb) for slug, label, href, blurb in discover_guide_entries()}
    for idx, (group_title, slugs) in enumerate(HOME_VAULT_GROUPS):
        details = soup.new_tag("details", attrs={"class": ["woa-kb-group"]})
        if idx == 0:
            details["open"] = "open"
        summary = soup.new_tag("summary")
        summary.string = group_title
        grid = soup.new_tag("div", attrs={"class": ["woa-kb-group-grid"]})
        for slug in slugs:
            row = by_slug.get(slug)
            if not row:
                continue
            label, href, blurb = row
            grid.append(_kb_card(soup, label, href, blurb))
        if not grid.contents:
            continue
        details.extend([summary, grid])
        groups_wrap.append(details)

    browse = soup.new_tag("p", attrs={"class": ["woa-kb-browse", "font-body-md", "text-on-surface-variant", "mt-10"]})
    browse.append("More: ")
    pierce = soup.new_tag("a", href=HREF_GUIDES_INDEX)
    pierce.string = "Piercing guides"
    browse.append(pierce)
    browse.append(" · Tattoo & healed proof: ")
    tattoo = soup.new_tag("a", href="/healed_tattoo_gallery_las_vegas/")
    tattoo.string = "Healed galleries"
    browse.append(tattoo)
    browse.append(" · Q&A: ")
    qa = soup.new_tag("a", href="/knowledge/")
    qa.string = "Knowledge base"
    browse.append(qa)

    sec.extend([head, groups_wrap, browse])
    return sec


def build_recently_updated_section(soup: BeautifulSoup) -> BeautifulSoup:
    sec = soup.new_tag(
        "section",
        attrs={
            "id": "recently-updated",
            "class": [
                "py-12",
                "md:py-16",
                "px-margin-mobile",
                "md:px-margin-desktop",
                "bg-background",
                "border-b",
                "border-outline-variant/10",
            ],
        },
    )
    head = soup.new_tag("div", attrs={"class": ["max-w-3xl", "mx-auto", "space-y-3", "mb-8"]})
    span = soup.new_tag(
        "span",
        attrs={
            "class": [
                "font-label-caps",
                "text-label-caps",
                "text-secondary",
                "uppercase",
                "tracking-[0.2em]",
            ]
        },
    )
    span.string = "Recently updated"
    h2 = soup.new_tag("h2", attrs={"class": ["font-headline-md", "text-on-surface", "text-2xl"]})
    h2.string = "Fresh guides & healed proof"
    intro = soup.new_tag("p", attrs={"class": ["font-body-md", "text-on-surface-variant"]})
    intro.string = (
        "We maintain these pages — new galleries, placement guides, and aftercare notes land here first."
    )
    head.extend([span, h2, intro])
    list_wrap = soup.new_tag("div", attrs={"class": ["max-w-3xl", "mx-auto"]})
    for label, href, when in RECENTLY_UPDATED:
        row = soup.new_tag("div", attrs={"class": ["woa-update-row"]})
        link = soup.new_tag("a", href=href)
        link.string = label
        time_tag = soup.new_tag("time", attrs={"datetime": "2026-06-01"})
        time_tag.string = when
        row.extend([link, time_tag])
        list_wrap.append(row)
    sec.extend([head, list_wrap])
    return sec


def refresh_home_recently_updated(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    old = soup.find(id="recently-updated")
    ensure_hub_css(soup)
    fresh = build_recently_updated_section(soup)
    if old:
        old.replace_with(fresh)
    else:
        kb = soup.find(id="knowledge-base")
        if kb:
            kb.insert_before(fresh)
        else:
            return False
    path.write_text(str(soup), encoding="utf-8")
    return True


def inject_home_recently_updated(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if 'id="recently-updated"' in raw:
        return refresh_home_recently_updated(path)
    soup = BeautifulSoup(raw, "html.parser")
    ensure_hub_css(soup)
    sec = build_recently_updated_section(soup)
    kb = soup.find(id="knowledge-base")
    if kb:
        kb.insert_before(sec)
    else:
        faq = soup.find(id="faq")
        if faq:
            faq.insert_before(sec)
        else:
            return False
    path.write_text(str(soup), encoding="utf-8")
    return True


def remove_home_recently_updated(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    old = soup.find(id="recently-updated")
    if not old:
        return False
    old.decompose()
    path.write_text(str(soup), encoding="utf-8")
    return True


def refresh_home_knowledge_base(path: Path) -> bool:
    """Replace #knowledge-base section with current copy and guide cards."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    if 'id="knowledge-base"' not in raw:
        return False
    soup = BeautifulSoup(raw, "html.parser")
    old = soup.find(id="knowledge-base")
    if not old:
        return False
    ensure_hub_css(soup)
    kb = build_knowledge_base_section(soup)
    old.replace_with(kb)
    path.write_text(str(soup), encoding="utf-8")
    return True


def inject_home_knowledge_base(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if 'id="knowledge-base"' in raw:
        return refresh_home_knowledge_base(path)
    soup = BeautifulSoup(raw, "html.parser")
    ensure_hub_css(soup)
    kb = build_knowledge_base_section(soup)
    faq = soup.find(id="faq")
    if faq:
        faq.insert_before(kb)
    else:
        main = soup.find("main")
        if main:
            main.append(kb)
        else:
            return False
    path.write_text(str(soup), encoding="utf-8")
    return True


def is_guide_slug(slug: str) -> bool:
    return slug not in SKIP_GUIDE_SLUGS and slug != HOME_SLUG


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--guides-only", action="store_true")
    ap.add_argument("--home-only", action="store_true")
    ap.add_argument(
        "--refresh",
        action="store_true",
        help="Replace existing hub bars and knowledge-base section",
    )
    args = ap.parse_args()

    do_guides = not args.home_only
    do_home = not args.guides_only

    n_bar = 0
    n_home = 0

    if do_guides:
        for slug, folder in merged_export_roots().items():
            if not is_guide_slug(slug):
                continue
            html = folder / "code.html"
            if inject_guide_hub_bar(html, slug, force=args.refresh):
                print(f"[hub bar] {slug}")
                n_bar += 1

    if do_home:
        home = merged_export_roots().get(HOME_SLUG)
        if home and (home / "code.html").is_file():
            home_html = home / "code.html"
            if inject_home_knowledge_base(home_html):
                print(f"[knowledge base] {HOME_SLUG}")
                n_home += 1
            if remove_home_recently_updated(home_html):
                print(f"[trim] removed recently-updated from {HOME_SLUG}")
                n_home += 1

    print(f"\nGuide hub bars: {n_bar}; homepage sections: {n_home}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

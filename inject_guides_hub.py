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
    SKIP_GUIDE_SLUGS,
    discover_guide_entries,
    merged_export_roots,
)

ROOT = Path(__file__).resolve().parent

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
#knowledge-base .woa-kb-card p {
  margin: 0;
}
"""


def ensure_hub_css(soup: BeautifulSoup) -> None:
    head = soup.find("head")
    if not head:
        return
    for st in head.find_all("style"):
        if st.string and "[data-woa-guide-hub-bar]" in (st.string or ""):
            return
    tag = soup.new_tag("style", attrs={"data-woa-guide-hub-css": "1"})
    tag.string = HUB_STYLE
    head.append(tag)


def build_guide_hub_bar(soup: BeautifulSoup, current_slug: str | None) -> BeautifulSoup:
    wrap = soup.new_tag(
        "nav",
        attrs={
            "aria-label": "All guides",
            "data-woa-guide-hub-bar": "1",
            "class": [
                "px-margin-mobile",
                "md:px-margin-desktop",
            ],
        },
    )
    inner = soup.new_tag("div", attrs={"class": ["woa-guide-hub-scroll"]})
    for slug, label, href, _blurb in discover_guide_entries():
        a = soup.new_tag("a", href=href, attrs={"class": ["woa-guide-pill"]})
        if slug == current_slug:
            a["class"].append("is-current")
            a["aria-current"] = "page"
        a.string = label
        inner.append(a)
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


def inject_guide_hub_bar(path: Path, slug: str) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if 'data-woa-guide-hub-bar="1"' in raw:
        return False
    soup = BeautifulSoup(raw, "html.parser")
    ensure_hub_css(soup)
    bar = build_guide_hub_bar(soup, slug)
    if not insert_before_main(soup, bar):
        return False
    path.write_text(str(soup), encoding="utf-8")
    return True


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
    span.string = "Expert Guides"
    h2 = soup.new_tag("h2", attrs={"class": ["font-headline-lg", "text-headline-lg", "text-on-surface"]})
    h2.string = "Our Las Vegas Tattoo & Piercing Knowledge Base"
    intro = soup.new_tag(
        "p",
        attrs={"class": ["font-body-lg", "text-body-lg", "text-on-surface-variant", "max-w-2xl", "mx-auto"]},
    )
    intro.string = (
        "Dozens of in-depth guides written by our team — pricing, placement, aftercare, "
        "walk-ins, realism, fine line, and how to choose the right artist before you commit."
    )
    head.extend([span, h2, intro])
    grid = soup.new_tag(
        "div",
        attrs={
            "class": [
                "grid",
                "grid-cols-1",
                "md:grid-cols-2",
                "gap-gutter",
                "max-w-6xl",
                "mx-auto",
            ]
        },
    )
    for slug, label, href, blurb in discover_guide_entries():
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
        grid.append(card)
    sec.extend([head, grid])
    return sec


def inject_home_knowledge_base(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if 'id="knowledge-base"' in raw:
        return False
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
            if inject_guide_hub_bar(html, slug):
                print(f"[hub bar] {slug}")
                n_bar += 1

    if do_home:
        home = merged_export_roots().get(HOME_SLUG)
        if home and (home / "code.html").is_file():
            if inject_home_knowledge_base(home / "code.html"):
                print(f"[knowledge base] {HOME_SLUG}")
                n_home += 1

    print(f"\nGuide hub bars: {n_bar}; homepage section: {n_home}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Replace desktop nav with six top-level sections + nested dropdowns:

Portfolio · Artists · Tattoo Guides · Piercing Guides · Locations · Book
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import (
    discover_artist_nav_entries,
    discover_nav_locations,
    discover_nav_piercing_guides,
    discover_nav_tattoo_guides,
    HREF_APPOINTMENTS,
    HREF_KNOWLEDGE_VAULT,
    NAV_PORTFOLIO,
)

from inject_mobile_hamburger_nav import (  # type: ignore
    collect_files,
    find_desktop_nav_strip,
    find_top_shell,
    rel_display,
)

_ROOT_A = Path(__file__).resolve().parent

DESKTOP_NAV_STYLE = """
/* Work of Art — unified desktop nav dropdown */
[data-woa-desktop-nav="1"] details.woa-desktop-dd > summary {
  list-style: none;
}
[data-woa-desktop-nav="1"] details.woa-desktop-dd > summary::-webkit-details-marker {
  display: none;
}
[data-woa-desktop-nav="1"] .woa-dd-panel {
  position: absolute;
  left: 0;
  margin-top: 2px;
  min-width: 14rem;
  max-width: min(90vw, 22rem);
  max-height: min(70vh, 24rem);
  overflow-x: hidden;
  overflow-y: auto;
  z-index: 100;
  border: 1px solid rgba(68, 71, 72, 0.65);
  background: rgba(19, 19, 19, 0.97);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.52);
}
[data-woa-desktop-nav="1"] .woa-dd-vault-link {
  color: #e9c349;
  font-weight: 600;
  letter-spacing: 0.02em;
}
[data-woa-desktop-nav="1"] .woa-dd-vault-link:hover {
  color: #f5d76e;
}
"""

TOP_LINK_CLASSES = (
    "woa-top-nav-link text-nav-link font-nav-link text-on-surface-variant hover:text-secondary "
    "transition-colors px-2 py-2 min-h-[40px] flex items-center whitespace-nowrap "
    "text-[15px] md:text-[16px] font-semibold tracking-tight"
)

SUMMARY_CLASSES = TOP_LINK_CLASSES + " cursor-pointer select-none list-none"


def ensure_desktop_nav_css(head, soup: BeautifulSoup) -> None:
    needle = "[data-woa-desktop-nav-css"
    if not head:
        return
    for st in head.find_all("style"):
        if st.string and needle in st.string:
            return
    tag = soup.new_tag("style", attrs={"data-woa-desktop-nav-css": "1"})
    tag.string = DESKTOP_NAV_STYLE
    head.append(tag)


def build_dropdown_details(
    soup: BeautifulSoup,
    *,
    summary_label: str,
    aria_label: str,
    items: list[tuple[str, str]],
    panel_max_height: str = "24rem",
):
    det = soup.new_tag(
        "details",
        attrs={
            "class": ["relative", "z-[70]", "woa-desktop-dd"],
            "aria-label": aria_label,
        },
    )
    sm = soup.new_tag("summary", attrs={"class": SUMMARY_CLASSES.split()})
    sm.string = summary_label
    pan = soup.new_tag(
        "div",
        attrs={"class": ["woa-dd-panel", "rounded-sm", "py-2"]},
    )
    if panel_max_height != "24rem":
        pan["style"] = f"max-height: min(70vh, {panel_max_height});"
    for label, href in items:
        a = soup.new_tag(
            "a",
            href=href,
            attrs={
                "class": [
                    "block",
                    "px-3",
                    "py-2",
                    "text-[13px]",
                    "leading-snug",
                    "text-on-surface",
                    "hover:text-secondary",
                    "transition-colors",
                ]
            },
        )
        a.string = label
        pan.append(a)
    det.append(sm)
    det.append(pan)
    return det


def build_artist_details(soup: BeautifulSoup):
    return build_dropdown_details(
        soup,
        summary_label="Artists",
        aria_label="Artists submenu",
        items=discover_artist_nav_entries(),
        panel_max_height="14rem",
    )


def build_desktop_strip(soup: BeautifulSoup):
    root = soup.new_tag(
        "div",
        attrs={
            "class": [
                "hidden",
                "md:flex",
                "flex-wrap",
                "justify-end",
                "items-center",
                "gap-1",
                "xl:gap-2",
            ],
            "data-woa-desktop-nav": "1",
        },
    )

    def a_link(href: str, label: str):
        tag = soup.new_tag(
            "a",
            href=href,
            attrs={"class": TOP_LINK_CLASSES.split()},
        )
        tag.string = label
        return tag

    root.append(
        build_dropdown_details(
            soup,
            summary_label="Portfolio",
            aria_label="Portfolio submenu",
            items=NAV_PORTFOLIO,
            panel_max_height="14rem",
        )
    )
    start = a_link(HREF_KNOWLEDGE_VAULT, "Start Here")
    start["class"] = (TOP_LINK_CLASSES + " text-secondary").split()
    root.append(start)
    root.append(build_artist_details(soup))
    root.append(
        build_dropdown_details(
            soup,
            summary_label="Tattoo Guides",
            aria_label="Tattoo guides submenu",
            items=discover_nav_tattoo_guides(),
        )
    )
    root.append(
        build_dropdown_details(
            soup,
            summary_label="Piercing Guides",
            aria_label="Piercing guides submenu",
            items=discover_nav_piercing_guides(),
        )
    )
    root.append(
        build_dropdown_details(
            soup,
            summary_label="Locations",
            aria_label="Locations submenu",
            items=discover_nav_locations(),
        )
    )
    root.append(a_link(HREF_APPOINTMENTS, "Book"))
    return root


def pick_nav_container(shell):
    m = shell.find(attrs={"data-woa-desktop-nav": "1"})
    if m and m.name in ("div", "nav"):
        return m
    return find_desktop_nav_strip(shell)


def apply_navigation(soup: BeautifulSoup) -> bool:
    shell = find_top_shell(soup)
    if not shell:
        return False
    holder = pick_nav_container(shell)
    if not holder:
        return False
    head = soup.find("head")
    ensure_desktop_nav_css(head, soup)
    blk = build_desktop_strip(soup)
    holder.clear()
    holder["data-woa-desktop-nav"] = "1"
    holder["class"] = blk.get("class", [])
    if "style" in holder.attrs:
        del holder["style"]
    for ch in list(blk.contents):
        holder.append(ch)
    return True


def upgrade_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    if apply_navigation(soup):
        path.write_text(str(soup), encoding="utf-8")
        return True
    return False


def load_injector():
    spec = importlib.util.spec_from_file_location(
        "woa_inj", _ROOT_A / "inject_mobile_hamburger_nav.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--desktop-only",
        action="store_true",
        help="Do not rerun inject_mobile_hamburger_nav.py --force",
    )
    args = ap.parse_args()

    tattoo = discover_nav_tattoo_guides()
    piercing = discover_nav_piercing_guides()
    locations = discover_nav_locations()
    print(
        f"Nav: Portfolio · Artists · Tattoo ({len(tattoo)}) · "
        f"Piercing ({len(piercing)}) · Locations ({len(locations)}) · Book"
    )

    n = 0
    for path in collect_files():
        if upgrade_file(path):
            print(f"[nav] {rel_display(path)}")
            n += 1

    print(f"\nUpdated desktop navigation markup in {n} file(s).")

    if not args.desktop_only:
        inj = load_injector()
        n_m = 0
        for p in collect_files():
            ok, st = inj.inject_for_file(p, force=True)
            if ok:
                n_m += 1
                print(f"[mnav] {rel_display(p)}")
        print(f"\nRebuilt mobile drawer in {n_m} file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

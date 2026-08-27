#!/usr/bin/env python3
"""
Replace the desktop `<header>/<nav>` link strip with a unified row:

Artists (dropdown) • Piercing • featured insider links • Insider Guides (dropdown + vault)
• Merchandise • Reviews • Appointments

Adds CSS for the Guides `<details>` panel. By default reruns inject mobile nav with
`--force` so the mobile drawer matches.

  python3 upgrade_site_navigation.py
  python3 upgrade_site_navigation.py --desktop-only
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import (
    discover_artist_nav_entries,
    discover_dropdown_guide_entries,
    discover_featured_guide_nav,
    HREF_APPOINTMENTS,
    HREF_KNOWLEDGE_VAULT,
    HREF_PIERCING,
    HREF_REVIEWS,
    MERCH_HREF,
    NAV_KNOWLEDGE_MENU_LABEL,
    NAV_KNOWLEDGE_VAULT_LINK_LABEL,
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
[data-woa-desktop-nav="1"] .woa-dd-sep {
  display: block;
  margin: 0.35rem 0.75rem;
  border-top: 1px solid rgba(68, 71, 72, 0.65);
}
@keyframes woa-topnav-fire-glow {
  0%,
  100% {
    color: #ffe088;
    text-shadow:
      0 0 6px rgba(233, 195, 73, 0.55),
      0 0 14px rgba(255, 90, 20, 0.2);
  }
  50% {
    color: #fff4cc;
    text-shadow:
      0 0 10px rgba(255, 224, 136, 0.95),
      0 0 22px rgba(255, 100, 20, 0.55),
      0 0 36px rgba(233, 195, 73, 0.35);
  }
}
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > a.woa-top-nav-link,
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > details.woa-desktop-dd > summary.woa-top-nav-link {
  animation: woa-topnav-fire-glow 2.6s ease-in-out infinite;
}
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > a.woa-top-nav-link:hover,
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > details.woa-desktop-dd > summary.woa-top-nav-link:hover,
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > a.woa-top-nav-link:focus-visible,
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > details.woa-desktop-dd > summary.woa-top-nav-link:focus-visible {
  color: #fff8e0;
}
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > a.woa-top-nav-link:nth-child(2n) {
  animation-delay: 0.3s;
}
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > a.woa-top-nav-link:nth-child(3n),
[data-woa-top-shell="1"] [data-woa-desktop-nav="1"] > details.woa-desktop-dd:nth-child(3n) > summary.woa-top-nav-link {
  animation-delay: 0.6s;
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


def build_knowledge_dropdown(soup: BeautifulSoup, guide_rows: list[tuple[str, str, str, str]]):
    det = soup.new_tag(
        "details",
        attrs={
            "class": ["relative", "z-[70]", "woa-desktop-dd"],
            "aria-label": "Insider guides submenu",
        },
    )
    sm = soup.new_tag("summary", attrs={"class": SUMMARY_CLASSES.split()})
    sm.string = NAV_KNOWLEDGE_MENU_LABEL
    pan = soup.new_tag(
        "div",
        attrs={"class": ["woa-dd-panel", "rounded-sm", "py-2"]},
    )
    vault = soup.new_tag(
        "a",
        href=HREF_KNOWLEDGE_VAULT,
        attrs={
            "class": [
                "block",
                "px-3",
                "py-2",
                "text-[13px]",
                "leading-snug",
                "woa-dd-vault-link",
                "transition-colors",
            ]
        },
    )
    vault.string = NAV_KNOWLEDGE_VAULT_LINK_LABEL
    pan.append(vault)
    sep = soup.new_tag("span", attrs={"class": ["woa-dd-sep"], "role": "separator"})
    pan.append(sep)
    for _slug, label, href, _blurb in guide_rows:
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


def build_desktop_strip(
    soup: BeautifulSoup,
    featured: list[tuple[str, str]],
    dropdown_guides: list[tuple[str, str, str, str]],
):
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

    root.append(build_artist_details(soup))
    root.append(a_link(HREF_PIERCING, "Piercing"))
    for label, href in featured:
        root.append(a_link(href, label))
    root.append(build_knowledge_dropdown(soup, dropdown_guides))
    root.append(a_link(MERCH_HREF, "Merchandise"))
    root.append(a_link(HREF_REVIEWS, "Reviews"))
    root.append(a_link(HREF_APPOINTMENTS, "Appointments"))
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
    featured = discover_featured_guide_nav()
    dropdown = discover_dropdown_guide_entries()
    head = soup.find("head")
    ensure_desktop_nav_css(head, soup)
    blk = build_desktop_strip(soup, featured, dropdown)
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
    """Import inject_mobile_hamburger_nav from sibling file robustly."""
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

    featured = discover_featured_guide_nav()
    dropdown = discover_dropdown_guide_entries()
    print(
        f"Nav: {len(featured)} featured insider links, "
        f"{len(dropdown)} in “{NAV_KNOWLEDGE_MENU_LABEL}” dropdown (+ vault)."
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
        skipped = []
        for p in collect_files():
            ok, st = inj.inject_for_file(p, force=True)
            if ok:
                n_m += 1
                print(f"[mnav] {rel_display(p)}")
            elif st != "ok":
                skipped.append((rel_display(p), st))
        print(f"\nRebuilt mobile drawer in {n_m} file(s).")
        for rel, reason in skipped:
            if reason not in {"ok"}:
                print(f"[mnav skip] {rel}: {reason}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

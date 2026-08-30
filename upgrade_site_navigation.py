#!/usr/bin/env python3
"""
Replace desktop nav with six top-level sections + nested dropdowns:

Portfolio · Artists · Tattoo Guides · Piercing Guides · Locations · Book
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import (
    REQUIRED_ARTIST_NAV_HREFS,
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
    find_book_cta,
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

DESKTOP_ARTIST_LINK_CLASS = (
    "block px-3 py-2 text-[13px] leading-snug text-on-surface "
    "hover:text-secondary transition-colors"
)
MOBILE_ARTIST_LINK_CLASS = (
    "block py-1.5 text-[13px] leading-snug font-medium text-secondary pl-3 "
    "border-b border-outline-variant/60 hover:text-secondary hover:bg-surface-container/40 "
    "transition-colors woa-mnav-mobile-link"
)

# Matches an Artists <details> panel regardless of BeautifulSoup whitespace.
_ARTISTS_PANEL_RE = re.compile(
    r"(<details\b(?=[^>]*\b(?:aria-label=\"Artists submenu\"|class=\"[^\"]*mobile-artists-dd))[^>]*>"
    r"\s*<summary\b[^>]*>\s*Artists\s*</summary>\s*"
    r"<div class=\"(?:woa-dd-panel|guides-sub)[^\"]*\"[^>]*>)"
    r"(.*?)"
    r"(</div>\s*</details>)",
    re.I | re.S,
)
_ARTISTS_SUMMARY_PANEL_RE = re.compile(
    r"(<details\b[^>]*>\s*<summary\b[^>]*>\s*Artists\s*</summary>\s*"
    r"<div class=\"(?:woa-dd-panel|guides-sub)[^\"]*\"[^>]*>)"
    r"(.*?)"
    r"(</div>\s*</details>)",
    re.I | re.S,
)

CONFLICT_MARK = "<<<<<<<"


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def artist_nav_anchors_html(*, mobile: bool) -> str:
    cls = MOBILE_ARTIST_LINK_CLASS if mobile else DESKTOP_ARTIST_LINK_CLASS
    parts: list[str] = []
    for label, href in discover_artist_nav_entries():
        shown = label
        if mobile and len(shown) > 56:
            shown = shown[:56] + "…"
        parts.append(f'<a class="{cls}" href="{_esc(href)}">{_esc(shown)}</a>')
    return "".join(parts)


def _replace_artists_panel(match: re.Match[str]) -> str:
    prefix, suffix = match.group(1), match.group(3)
    mobile = "guides-sub" in prefix or "mobile-artists-dd" in prefix
    return prefix + artist_nav_anchors_html(mobile=mobile) + suffix


def sync_artist_dropdowns_in_html(raw: str) -> tuple[str, int]:
    """Rewrite every Artists dropdown panel to ARTIST_NAV_ENTRIES."""
    updated, count = _ARTISTS_PANEL_RE.subn(_replace_artists_panel, raw)

    def _maybe(match: re.Match[str]) -> str:
        inner = match.group(2)
        if "/artists/teralyn/" in inner and "Fine Line" in inner and "Floral" in inner:
            return match.group(0)
        return _replace_artists_panel(match)

    updated, extra = _ARTISTS_SUMMARY_PANEL_RE.subn(_maybe, updated)
    return updated, count + extra


def has_conflict_markers(raw: str) -> bool:
    return CONFLICT_MARK in raw


def insert_desktop_nav_holder(shell, soup: BeautifulSoup):
    """Add a data-woa-desktop-nav strip to a simple logo + Book bar."""
    holder = soup.new_tag(
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
    book = find_book_cta(shell)
    if book is not None:
        book.insert_before(holder)
    else:
        shell.append(holder)
    return holder


def ensure_desktop_nav_css(head, soup: BeautifulSoup) -> None:
    if not head:
        return
    existing = head.find_all("style", attrs={"data-woa-desktop-nav-css": True})
    if existing:
        existing[0].string = DESKTOP_NAV_STYLE
        for duplicate in existing[1:]:
            duplicate.decompose()
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
        holder = insert_desktop_nav_holder(shell, soup)
    if not holder:
        return False
    head = soup.find("head")
    ensure_desktop_nav_css(head, soup)
    blk = build_desktop_strip(soup)
    holder.clear()
    holder["data-woa-desktop-nav"] = "1"
    holder["class"] = blk.get("class", [])
    if "style" in holder.attrs:
        del holder.attrs["style"]
    for ch in list(blk.contents):
        holder.append(ch)
    return True


def upgrade_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if has_conflict_markers(raw):
        return False
    soup = BeautifulSoup(raw, "html.parser")
    if apply_navigation(soup):
        path.write_text(str(soup), encoding="utf-8")
        return True
    return False


def sync_artist_dropdowns_file(path: Path) -> int:
    raw = path.read_text(encoding="utf-8", errors="replace")
    updated, count = sync_artist_dropdowns_in_html(raw)
    if updated != raw:
        path.write_text(updated, encoding="utf-8")
    return count


def public_html_files() -> list[Path]:
    """HTML that ships (code.html, index.html, artist builds) minus staging."""
    seen: set[str] = set()
    out: list[Path] = []
    for path in collect_files():
        rp = str(path.resolve())
        if rp in seen:
            continue
        seen.add(rp)
        out.append(path)
    return out


def needs_artist_nav_injection(raw: str) -> bool:
    if has_conflict_markers(raw):
        return False
    if "Artists submenu" in raw:
        return False
    if "fixed" not in raw or "top-0" not in raw:
        return False
    return True


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
    roster = ", ".join(label for label, _href in discover_artist_nav_entries()[1:])
    print(
        f"Nav: Portfolio · Artists ({roster}) · Tattoo ({len(tattoo)}) · "
        f"Piercing ({len(piercing)}) · Locations ({len(locations)}) · Book"
    )

    files = public_html_files()

    synced = 0
    for path in files:
        n = sync_artist_dropdowns_file(path)
        if n:
            print(f"[artists] {rel_display(path)} ({n} dropdown(s))")
            synced += 1
    print(f"\nSynced Artists dropdowns in {synced} file(s).")

    n = 0
    injected_paths: list[Path] = []
    for path in files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if not needs_artist_nav_injection(raw):
            continue
        if upgrade_file(path):
            print(f"[nav] {rel_display(path)}")
            n += 1
            injected_paths.append(path)
            sync_artist_dropdowns_file(path)

    print(f"\nInserted sitewide desktop navigation in {n} file(s).")

    if not args.desktop_only and injected_paths:
        inj = load_injector()
        n_m = 0
        for p in injected_paths:
            ok, _st = inj.inject_for_file(p, force=True)
            if ok:
                n_m += 1
                print(f"[mnav] {rel_display(p)}")
                sync_artist_dropdowns_file(p)
        print(f"\nRebuilt mobile drawer in {n_m} file(s).")

    missing = audit_artist_nav(files)
    if missing:
        print(f"\nArtists dropdowns still missing Teralyn ({len(missing)}):", file=sys.stderr)
        for rel in missing[:40]:
            print(f"  {rel}", file=sys.stderr)
        return 1
    print("\nAudit OK: every Artists dropdown includes Joshua, Katelyn, and Teralyn.")
    return 0


def audit_artist_nav(files: list[Path]) -> list[str]:
    missing: list[str] = []
    required = set(REQUIRED_ARTIST_NAV_HREFS)
    for path in files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "Artists submenu" not in raw and ">Artists</summary>" not in raw:
            continue
        for block in _ARTISTS_SUMMARY_PANEL_RE.findall(raw):
            inner = block[1] if isinstance(block, tuple) else block
            hrefs = set(re.findall(r'href="([^"]+)"', inner))
            labels = inner.lower()
            if not required.issubset(hrefs):
                missing.append(rel_display(path))
                break
            if "jay jay" in labels or "/jay_jay" in inner:
                missing.append(f"{rel_display(path)} (Jay Jay still in resident menu)")
                break
            if "/artists/teralyn/" in inner and "fine line" not in labels:
                missing.append(f"{rel_display(path)} (Teralyn label stale)")
                break
    return missing


if __name__ == "__main__":
    raise SystemExit(main())

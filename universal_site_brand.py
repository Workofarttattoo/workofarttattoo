#!/usr/bin/env python3
"""
Set the top-left site brand to "Work of Art Tattoo & Piercing" on every static page.

Targets code.html exports and artists_build/*.html. Replaces short "WORK OF ART"
labels, fixes hidden brands (opacity: 0), and links the brand to /.

  python3 universal_site_brand.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from inject_mobile_hamburger_nav import collect_files, find_top_shell, cls_join

_ROOT = Path(__file__).resolve().parent

BRAND_LABEL = "Work of Art Tattoo & Piercing"
BRAND_HREF = "/"

BRAND_CLASSES = [
    "woa-site-brand",
    "text-[10px]",
    "xs:text-[11px]",
    "sm:text-xs",
    "md:text-sm",
    "font-headline-md",
    "font-semibold",
    "text-on-surface",
    "uppercase",
    "tracking-tight",
    "leading-tight",
    "shrink-0",
    "hover:text-secondary",
    "transition-colors",
    "max-w-[11rem]",
    "sm:max-w-[13rem]",
    "md:max-w-none",
    "md:whitespace-nowrap",
]

BRAND_STYLE = """
/* Work of Art — universal header brand (universal_site_brand.py) */
a[data-woa-site-brand="1"],
[data-woa-site-brand="1"] {
  opacity: 1 !important;
  visibility: visible !important;
}
nav[data-woa-top-shell="1"] > a[data-woa-site-brand="1"],
header[data-woa-top-shell="1"] > a[data-woa-site-brand="1"] {
  flex: 0 1 auto;
  min-width: 0;
}
"""

BRAND_MARKERS = (
    "work of art tattoo",
    "work of art",
    "woa-site-brand",
)


def ensure_brand_css(head: Tag | None, soup: BeautifulSoup) -> None:
    if not head:
        return
    needle = "universal_site_brand.py"
    for st in head.find_all("style"):
        if st.string and needle in st.string:
            return
    tag = soup.new_tag("style", attrs={"data-woa-site-brand-css": "1"})
    tag.string = BRAND_STYLE
    head.append(tag)


def build_brand(soup: BeautifulSoup) -> Tag:
    a = soup.new_tag(
        "a",
        href=BRAND_HREF,
        attrs={
            "class": BRAND_CLASSES,
            "data-woa-site-brand": "1",
            "aria-label": BRAND_LABEL,
        },
    )
    a.string = BRAND_LABEL
    return a


def is_brand_candidate(el: Tag) -> bool:
    if el.name not in ("div", "a", "span"):
        return False
    if el.find(attrs={"data-woa-desktop-nav": "1"}):
        return False
    if el.find("button") and len(el.get_text(strip=True)) < 30:
        return False
    text = el.get_text(strip=True).lower()
    cc = cls_join(el).lower()
    if el.get("data-woa-site-brand") == "1":
        return True
    if any(m in text for m in BRAND_MARKERS if m != "woa-site-brand"):
        return True
    if "headline" in cc and len(text) < 80 and "book" not in text:
        if "work" in text or not text:
            return True
    return False


def find_brand_slot(shell: Tag) -> Tag | None:
    for child in shell.children:
        if not isinstance(child, Tag):
            continue
        if is_brand_candidate(child):
            return child
    for el in shell.find_all(["div", "a", "span"], recursive=False):
        if is_brand_candidate(el):
            return el
    return None


def strip_hidden_style(el: Tag) -> None:
    style = el.get("style")
    if not style:
        return
    style = re.sub(r"opacity\s*:\s*0\s*;?", "", style, flags=re.I)
    style = re.sub(r"visibility\s*:\s*hidden\s*;?", "", style, flags=re.I)
    style = style.strip().rstrip(";")
    if style:
        el["style"] = style
    elif "style" in el.attrs:
        del el["style"]


def apply_brand(soup: BeautifulSoup) -> bool:
    shell = find_top_shell(soup)
    if not shell:
        return False

    if "data-woa-top-shell" not in shell.attrs:
        shell["data-woa-top-shell"] = "1"

    brand = build_brand(soup)
    slot = find_brand_slot(shell)
    if slot:
        strip_hidden_style(slot)
        slot.replace_with(brand)
    else:
        shell.insert(0, brand)

    for el in shell.find_all(["div", "a", "span"]):
        t = el.get_text(strip=True).upper()
        if t in ("WORK OF ART", "WORK OF ART TATTOO") and el != brand:
            if not el.find_parent(attrs={"data-woa-site-brand": "1"}):
                el.decompose()

    ensure_brand_css(soup.find("head"), soup)
    return True


def collect_all_html() -> list[Path]:
    paths = list(collect_files())
    artists = _ROOT / "artists_build"
    if artists.is_dir():
        for html in sorted(artists.glob("*.html")):
            if html not in paths:
                paths.append(html)
    return paths


def main() -> int:
    updated = 0
    missing = []
    for path in collect_all_html():
        raw = path.read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(raw, "html.parser")
        if apply_brand(soup):
            path.write_text(str(soup), encoding="utf-8")
            print(f"[brand] {path.relative_to(_ROOT)}")
            updated += 1
        else:
            missing.append(path.relative_to(_ROOT))

    print(f"\nUpdated brand on {updated} file(s).")
    if missing:
        print(f"No top nav shell found ({len(missing)}):")
        for rel in missing[:15]:
            print(f"  - {rel}")
        if len(missing) > 15:
            print(f"  … and {len(missing) - 15} more")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())

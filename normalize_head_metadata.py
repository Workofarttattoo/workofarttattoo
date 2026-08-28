#!/usr/bin/env python3
"""Make generated HTML heads idempotent before deploy."""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SKIP_PARTS = frozenset({".git", "__pycache__", "skipped_upload_build", "artists_raw"})
MATERIAL_SYMBOLS_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
)
NESTED_NOSCRIPT_RE = re.compile(r"<noscript\b[^>]*>[\s\S]*?<noscript\b", re.I)
ENCODED_EMPTY_TAG_RE = re.compile(r"&lt;\s*&gt;|&lt;&gt;")
APPOINTMENT_SOCIAL_RE = re.compile(r"Book an Appointment\s*\|", re.I)

UNIQUE_META_NAMES = {
    "description",
    "viewport",
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:card",
}
UNIQUE_META_PROPS = {
    "og:url",
    "og:title",
    "og:description",
    "og:image",
    "og:type",
}


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name != "code.html" and path.parent.name != "artists_build":
            continue
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            out.append(path)
    root_home = ROOT / "code.html"
    if root_home.is_file() and root_home.resolve() not in seen:
        out.append(root_home)
    return out


def remove_duplicate_tags(tags, key_fn) -> bool:
    changed = False
    seen: set[str] = set()
    for tag in list(tags):
        key = key_fn(tag)
        if not key:
            continue
        if key in seen:
            tag.decompose()
            changed = True
        else:
            seen.add(key)
    return changed


def normalize_material_symbols(html: str) -> str:
    if "Material+Symbols" not in html and "Material Symbols" not in html:
        return html
    # Drop every Material Symbols link/preload/noscript tangle and re-add one preload + one noscript.
    html = re.sub(
        r'<link\b[^>]*href="[^"]*Material\+Symbols[^"]*"[^>]*>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<noscript>\s*<link\b[^>]*href="[^"]*Material\+Symbols[^"]*"[^>]*>\s*</noscript>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<link\b[^>]*href="[^"]*Material\+Symbols[^"]*"[^>]*>\s*</noscript>\s*',
        "",
        html,
        flags=re.I,
    )
    block = (
        f'<link rel="preload" as="style" href="{MATERIAL_SYMBOLS_HREF}" '
        'onload="this.onload=null;this.rel=\'stylesheet\'"/>'
    )
    return html.replace("</head>", block + "\n</head>", 1)


def upsert_meta(head, soup: BeautifulSoup, *, attr: str, key: str, content: str) -> bool:
    if not content:
        return False
    selector = {attr: key}
    if head.find("meta", attrs=selector):
        return False
    tag = soup.new_tag("meta")
    tag[attr] = key
    tag["content"] = content
    head.append(tag)
    return True


def repair_meta(head, soup: BeautifulSoup, *, attr: str, key: str, content: str) -> bool:
    tag = head.find("meta", attrs={attr: key})
    if not tag:
        return upsert_meta(head, soup, attr=attr, key=key, content=content)
    current = (tag.get("content") or "").strip()
    if content and current != content:
        tag["content"] = content
        return True
    return False


def fill_social_metadata(head, soup: BeautifulSoup) -> bool:
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    description_tag = head.find("meta", attrs={"name": "description"})
    description = (description_tag or {}).get("content", "").strip()
    canonical_tag = head.find("link", rel=lambda rel: rel and "canonical" in rel)
    canonical = (canonical_tag or {}).get("href", "").strip()
    changed = False
    changed |= repair_meta(head, soup, attr="property", key="og:url", content=canonical)
    changed |= repair_meta(head, soup, attr="property", key="og:title", content=title)
    changed |= repair_meta(head, soup, attr="property", key="og:description", content=description)
    changed |= repair_meta(head, soup, attr="name", key="twitter:title", content=title)
    changed |= repair_meta(head, soup, attr="name", key="twitter:description", content=description)
    if (head.find("meta", property="og:title") or {}).get("content") and not head.find("meta", property="og:type"):
        changed |= upsert_meta(head, soup, attr="property", key="og:type", content="website")
    if (
        (head.find("meta", attrs={"name": "twitter:title"}) or {}).get("content")
        and not head.find("meta", attrs={"name": "twitter:card"})
    ):
        changed |= upsert_meta(head, soup, attr="name", key="twitter:card", content="summary_large_image")
    return changed


def normalize_html(html: str) -> tuple[str, bool]:
    original = html
    html = ENCODED_EMPTY_TAG_RE.sub("", html)
    html = normalize_material_symbols(html)
    soup = BeautifulSoup(html, "html.parser")
    head = soup.head
    if not head:
        return html, html != original

    remove_duplicate_tags(head.find_all("title"), lambda tag: "title")
    remove_duplicate_tags(head.find_all("link", rel=lambda rel: rel and "canonical" in rel), lambda tag: "canonical")
    remove_duplicate_tags(head.find_all("meta", charset=True), lambda tag: "charset")
    remove_duplicate_tags(
        head.find_all("meta", attrs={"name": True}),
        lambda tag: (tag.get("name") or "").lower() if (tag.get("name") or "").lower() in UNIQUE_META_NAMES else "",
    )
    remove_duplicate_tags(
        head.find_all("meta", attrs={"property": True}),
        lambda tag: (tag.get("property") or "").lower() if (tag.get("property") or "").lower() in UNIQUE_META_PROPS else "",
    )
    remove_duplicate_tags(
        head.find_all("link", rel=lambda rel: rel and "preconnect" in rel),
        lambda tag: (tag.get("href") or "").strip().lower(),
    )
    remove_duplicate_tags(
        head.find_all("link", href=True),
        lambda tag: "|".join(tag.get("rel") or []) + "|" + (tag.get("href") or "").strip()
        if not tag.find_parent("noscript")
        and ("stylesheet" in (tag.get("rel") or []) or "preload" in (tag.get("rel") or []))
        else "",
    )
    fill_social_metadata(head, soup)

    rendered = str(soup)
    return rendered, rendered != original


def main() -> int:
    updated = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8", errors="replace")
        html, changed = normalize_html(raw)
        if changed:
            path.write_text(html, encoding="utf-8")
            updated += 1
            print(f"[head] {path.relative_to(ROOT)}")
    print(f"Done: normalized {updated} HTML file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Publish short hyphenated URLs that mirror legacy guide folders."""

from __future__ import annotations

import re
from pathlib import Path

from woa_url_aliases import ALIASES_BY_SHORT, SITE, UrlAlias

ROOT = Path(__file__).resolve().parent
ASSET_EXT = {".png", ".webp", ".jpg", ".jpeg", ".gif", ".svg"}
COMPANION_FILES = {"index.html.md"}


def copy_alias_assets(alias: UrlAlias) -> int:
    """Mirror image assets from legacy source folder into short public slug folder."""
    src_dir = ROOT / alias.source_slug
    out_dir = ROOT / alias.short_slug
    if not src_dir.is_dir():
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for fpath in sorted(src_dir.iterdir()):
        if fpath.is_file() and (fpath.suffix.lower() in ASSET_EXT or fpath.name in COMPANION_FILES):
            dest = out_dir / fpath.name
            if not dest.exists() or fpath.stat().st_mtime > dest.stat().st_mtime:
                dest.write_bytes(fpath.read_bytes())
            n += 1
    return n


def patch_paths(html: str, alias: UrlAlias) -> str:
    short = f"/{alias.short_slug}/"
    short_canon = f"{SITE}{short}"
    legacy = f"/{alias.source_slug}/"
    legacy_canon = f"{SITE}{legacy}"

    html = re.sub(
        rf'<link href="{re.escape(legacy_canon)}" rel="canonical"/>',
        f'<link href="{short_canon}" rel="canonical"/>',
        html,
        count=1,
    )
    html = re.sub(
        rf'<meta content="{re.escape(legacy_canon)}" property="og:url"/>',
        f'<meta content="{short_canon}" property="og:url"/>',
        html,
        count=1,
    )
    html = html.replace(f'href="{legacy}"', f'href="{short}"')
    html = html.replace(legacy, short)
    html = html.replace(legacy_canon, short_canon)
    return html


def build_alias(alias: UrlAlias) -> bool:
    src = ROOT / alias.source_slug / "code.html"
    if not src.is_file():
        print(f"[skip] missing source {alias.source_slug}")
        return False
    out_dir = ROOT / alias.short_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    assets = copy_alias_assets(alias)
    html = patch_paths(src.read_text(encoding="utf-8"), alias)
    (out_dir / "code.html").write_text(html, encoding="utf-8")
    print(f"[ok] /{alias.short_slug}/ ← {alias.source_slug} ({assets} asset(s))")
    return True


def update_internal_links() -> int:
    """Point internal hrefs at short alias URLs."""
    n = 0
    for path in ROOT.rglob("code.html"):
        if path.parts[0].startswith("."):
            continue
        raw = path.read_text(encoding="utf-8")
        updated = raw
        for alias in ALIASES_BY_SHORT.values():
            old = f"/{alias.source_slug}/"
            new = f"/{alias.short_slug}/"
            if old in updated:
                updated = updated.replace(old, new)
            old_canon = f"https://www.workofarttattoo.com{old.rstrip('/')}/"
            new_canon = f"https://www.workofarttattoo.com{new}"
            updated = updated.replace(old_canon, new_canon)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            n += 1
            print(f"[links] {path.relative_to(ROOT)}")
    for html in (ROOT / "artists_build").glob("*.html"):
        raw = html.read_text(encoding="utf-8")
        updated = raw
        for alias in ALIASES_BY_SHORT.values():
            updated = updated.replace(f"/{alias.source_slug}/", f"/{alias.short_slug}/")
        if updated != raw:
            html.write_text(updated, encoding="utf-8")
            n += 1
            print(f"[links] {html.relative_to(ROOT)}")
    return n


def main() -> int:
    n = sum(build_alias(a) for a in ALIASES_BY_SHORT.values())
    linked = update_internal_links()
    print(f"Done: {n} alias page(s), {linked} file(s) internal links updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

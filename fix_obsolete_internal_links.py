#!/usr/bin/env python3
"""Replace internal hrefs to obsolete URLs with canonical targets."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from woa_page_consolidation import ALL_HREF_REPLACEMENTS

SKIP_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "node_modules",
    "skipped_upload_build",
    "audits",
    "artists_raw",
    ".snapshots",
    "piercing_asset_chunks",
}

GLOB_PATTERNS = (
    "**/code.html",
    "**/index.html",
    "llms.txt",
    "ai.txt",
    "robots.txt",
    "sitemap.xml",
    "sitemap-static-pages.xml",
    "**/index.html.md",
    "**/*.py",
    "**/*.json",
)

# Only touch JSON under siteData/
JSON_ALLOW = {"siteData"}

SKIP_FILES = {
    "fix_obsolete_internal_links.py",
    "woa_page_consolidation.py",
    "generate_cloudflare_bulk_redirects.py",
}


def iter_files() -> list[Path]:
    found: set[Path] = set()
    for pattern in GLOB_PATTERNS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix == ".json" and path.parent.name not in JSON_ALLOW:
                continue
            if path.name in SKIP_FILES:
                continue
            found.add(path)
    return sorted(found)


def apply_replacements(text: str) -> str:
    for old, new in ALL_HREF_REPLACEMENTS:
        text = text.replace(old, new)
        bare_old = old.rstrip("/")
        bare_new = new.rstrip("/")
        if bare_old != old:
            text = text.replace(bare_old, bare_new)
        # href without trailing slash in HTML attributes
        text = text.replace(f'href="{bare_old}"', f'href="{new}"')
    return text


def main() -> int:
    replacements = ALL_HREF_REPLACEMENTS
    if not replacements:
        print("[links] no replacements configured")
        return 0

    changed: list[str] = []
    for path in iter_files():
        raw = path.read_text(encoding="utf-8", errors="replace")
        updated = apply_replacements(raw)
        if updated == raw:
            continue
        path.write_text(updated, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))

    print(f"[links] updated {len(changed)} files")
    for rel in changed[:40]:
        print(f"  - {rel}")
    if len(changed) > 40:
        print(f"  ... and {len(changed) - 40} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

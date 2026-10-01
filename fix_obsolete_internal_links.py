#!/usr/bin/env python3
"""Replace internal hrefs to obsolete URLs with canonical targets."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from woa_page_consolidation import ALL_HREF_REPLACEMENTS, rewrite_internal_hrefs

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

# Do not rewrite Python. The homepage path appears in validator source as a
# quoted string, and collapsing it to "/" makes the sitemap check always fail.
GLOB_PATTERNS = (
    "**/code.html",
    "**/index.html",
    "llms.txt",
    "ai.txt",
    "robots.txt",
    "sitemap.xml",
    "sitemap-static-pages.xml",
    "**/index.html.md",
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
    text = rewrite_internal_hrefs(text)
    # Replace slashless paths only at a real boundary. A shorter slug must not
    # eat a longer one (guide + "_2" was becoming how-to-choose-a-tattoo-artist_2).
    for old, new in sorted(ALL_HREF_REPLACEMENTS, key=lambda pair: len(pair[0]), reverse=True):
        bare_old = old.rstrip("/")
        bare_new = new.rstrip("/")
        if not bare_old or not bare_new or bare_old == old:
            continue
        text = re.sub(
            re.escape(bare_old) + r'(?=/|["\'\s?#<]|$)',
            lambda _match, repl=bare_new: repl,
            text,
        )
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

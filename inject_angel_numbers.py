#!/usr/bin/env python3
"""Append each public page's angel number to its meta description and above the footer.

Runs late in deploy, after code.html is copied to index.html and after parity
cleanup, so earlier generators cannot drop the marker.
"""

from __future__ import annotations

import sys
from pathlib import Path

from woa_angel_numbers import (
    apply_page,
    assign_numbers,
    discover_public_paths,
    load_mapping,
    save_mapping,
    source_files,
)
from woa_sitemap import discover_deploy_urls

ROOT = Path(__file__).resolve().parent


def main() -> int:
    paths = discover_public_paths(ROOT)
    sitemap_paths = {row[0] for row in discover_deploy_urls(ROOT)}
    missing_from_public = sorted(sitemap_paths - set(paths))
    if missing_from_public:
        print("Sitemap URLs missing from public page set:", file=sys.stderr)
        for path in missing_from_public:
            print(f"  {path}", file=sys.stderr)
        return 1

    stored = load_mapping()
    assigned = assign_numbers(paths, stored)
    save_mapping(assigned, stored)

    updated = 0
    missing_files = []
    for public_path in paths:
        files = source_files(ROOT, public_path)
        if not files:
            missing_files.append(public_path)
            continue
        number = assigned[public_path]
        for path in files:
            original = path.read_text(encoding="utf-8")
            revised = apply_page(original, number)
            if revised != original:
                path.write_text(revised, encoding="utf-8")
                updated += 1
    if missing_files:
        print("Public paths with no HTML source:", file=sys.stderr)
        for path in missing_files:
            print(f"  {path}", file=sys.stderr)
        return 1

    print(
        f"Angel numbers: {len(paths)} public pages, "
        f"{updated} HTML file(s) updated, mapping {len(assigned)} current paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

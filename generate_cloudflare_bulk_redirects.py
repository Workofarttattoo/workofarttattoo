#!/usr/bin/env python3
"""Generate Cloudflare Bulk Redirects CSV for one-hop 301s to https://www."""

from __future__ import annotations

import csv
from pathlib import Path

from woa_canonical import CANONICAL_ORIGIN
from woa_page_consolidation import (
    CONSOLIDATION_REDIRECTS,
    GSC_OBSOLETE_PATH_REDIRECTS,
    gsc_obsolete_slug_redirects,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "config" / "cloudflare-bulk-redirects.csv"

HOST_PREFIXES = (
    "http://workofarttattoo.com",
    "http://www.workofarttattoo.com",
    "https://workofarttattoo.com",
    "https://www.workofarttattoo.com",
)

HEADER = (
    "source_url",
    "target_url",
    "status_code",
    "preserve_query_string",
    "include_subdomains",
    "subpath_matching",
    "path_matching",
)


def _path_variants(path: str) -> tuple[str, ...]:
    path = path if path.startswith("/") else f"/{path}"
    if path.endswith("/"):
        bare = path.rstrip("/")
        return (path, bare) if bare else (path,)
    return (path, f"{path}/")


def slug_redirect_rows() -> list[tuple[str, str, int, bool, bool, bool, bool]]:
    rows: list[tuple[str, str, int, bool, bool, bool, bool]] = []
    seen: set[tuple[str, str]] = set()

    redirect_map = dict(CONSOLIDATION_REDIRECTS)
    redirect_map.update(gsc_obsolete_slug_redirects())

    for slug, dest in sorted(redirect_map.items()):
        if not dest.startswith("/"):
            dest = f"/{dest}"
        if not dest.endswith("/"):
            dest = f"{dest}/"
        target = f"{CANONICAL_ORIGIN}{dest}"
        for variant in _path_variants(f"/{slug}"):
            for prefix in HOST_PREFIXES:
                source = f"{prefix}{variant}"
                key = (source, target)
                if key in seen:
                    continue
                seen.add(key)
                rows.append((source, target, 301, True, False, False, True))
    return rows


def path_redirect_rows() -> list[tuple[str, str, int, bool, bool, bool, bool]]:
    rows: list[tuple[str, str, int, bool, bool, bool, bool]] = []
    seen: set[tuple[str, str]] = set()
    for src, dest in GSC_OBSOLETE_PATH_REDIRECTS:
        if not dest.startswith("/"):
            dest = f"/{dest}"
        if not dest.endswith("/"):
            dest = f"{dest}/"
        target = f"{CANONICAL_ORIGIN}{dest}"
        for variant in _path_variants(src):
            for prefix in HOST_PREFIXES:
                source = f"{prefix}{variant}"
                key = (source, target)
                if key in seen:
                    continue
                seen.add(key)
                rows.append((source, target, 301, True, False, False, True))
    return rows


def host_canonical_rows() -> list[tuple[str, str, int, bool, bool, bool, bool]]:
    return [
        (
            "http://workofarttattoo.com/*",
            f"{CANONICAL_ORIGIN}/${{1}}",
            301,
            True,
            False,
            True,
            True,
        ),
        (
            "http://www.workofarttattoo.com/*",
            f"{CANONICAL_ORIGIN}/${{1}}",
            301,
            True,
            False,
            True,
            True,
        ),
        (
            "https://workofarttattoo.com/*",
            f"{CANONICAL_ORIGIN}/${{1}}",
            301,
            True,
            False,
            True,
            True,
        ),
    ]


def write_csv() -> Path:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = slug_redirect_rows() + path_redirect_rows() + host_canonical_rows()
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        writer.writerows(rows)
    return OUT


def main() -> int:
    path = write_csv()
    slug_count = len({s for s, _ in CONSOLIDATION_REDIRECTS} | set(gsc_obsolete_slug_redirects()))
    print(f"[cloudflare] wrote {path.relative_to(ROOT)}")
    print(f"  slug/path rules: {len(slug_redirect_rows()) + len(path_redirect_rows())} rows")
    print(f"  unique slugs: {slug_count}")
    print(f"  knowledge path rules: {len(GSC_OBSOLETE_PATH_REDIRECTS)}")
    print(f"  host wildcard rules: 3 (listed last — import order matters)")
    print("Import in Cloudflare Dashboard → Bulk Redirects before excluding slugs from gh-pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

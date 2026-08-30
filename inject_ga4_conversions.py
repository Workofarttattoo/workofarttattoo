#!/usr/bin/env python3
"""Inject GA4 conversion events on all static HTML pages with gtag."""

from __future__ import annotations

import sys
from pathlib import Path

from woa_ga4_conversions import inject_ga4_conversions

ROOT = Path(__file__).resolve().parent

SKIP_NAMES = frozenset(
    (
        "skipped_pages_clipboard.html",
        "joshua.raw.html",
        "katelyn.raw.html",
    )
)
SKIP_PARTS = frozenset(("artists_raw", "__pycache__", "skipped_upload_build"))


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()

    def add(p: Path) -> None:
        if not p.is_file():
            return
        if p.name in SKIP_NAMES:
            return
        if any(part in SKIP_PARTS for part in p.parts):
            return
        key = str(p.resolve())
        if key in seen:
            return
        seen.add(key)
        out.append(p)

    for p in sorted(ROOT.glob("*/code.html")):
        if not p.parent.name.startswith("."):
            add(p)
    add(ROOT / "code.html")
    for p in sorted((ROOT / "artists_build").glob("*.html")):
        add(p)
    for p in sorted((ROOT / "appointments").glob("*.html")):
        add(p)

    return sorted(out, key=lambda x: str(x))


def main() -> int:
    updated = 0
    skipped = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8")
        new_html, ok = inject_ga4_conversions(raw)
        if not ok:
            skipped += 1
            continue
        if new_html != raw:
            path.write_text(new_html, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} page(s) with GA4 conversions, {skipped} skipped (no gtag)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Insert GTM Kit noscript PHP immediately after the opening <body> tag on every page."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GTMKIT_NOSCRIPT = """<?php if ( function_exists( 'gtmkit_the_noscript_tag' ) ) { gtmkit_the_noscript_tag(); } ?>"""

BODY_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)
MARKER = "gtmkit_the_noscript_tag"

SKIP_NAMES = frozenset(
    (
        "skipped_pages_clipboard.html",
        "joshua.raw.html",
        "katelyn.raw.html",
    )
)

SKIP_PARTS = frozenset(("artists_raw", "__pycache__"))


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
    for p in sorted((ROOT / "skipped_upload_build").glob("*.html")):
        add(p)

    return sorted(out, key=lambda x: str(x))


def inject_noscript(html: str) -> tuple[str, bool]:
    if MARKER in html:
        return html, False
    m = BODY_RE.search(html)
    if not m:
        return html, False
    pos = m.end()
    return html[:pos] + "\n" + GTMKIT_NOSCRIPT + html[pos:], True


def main() -> int:
    updated = 0
    skipped = 0
    for path in iter_html_files():
        original = path.read_text(encoding="utf-8")
        new_html, ok = inject_noscript(original)
        if not ok:
            if not BODY_RE.search(original):
                print(f"no <body>: {path.relative_to(ROOT)}", file=sys.stderr)
            skipped += 1
            continue
        path.write_text(new_html, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
        updated += 1
    print(f"Done: {updated} updated, {skipped} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

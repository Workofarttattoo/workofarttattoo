#!/usr/bin/env python3
"""Ensure indexable robots meta and LLM discovery link on all public HTML pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://www.workofarttattoo.com"

ROBOTS_META = (
    '<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>'
)
LLMS_LINK = f'<link href="{SITE}/llms.txt" rel="alternate" title="LLMs" type="text/plain"/>'

HEAD_RE = re.compile(r"(<head[^>]*>)", re.IGNORECASE)
SKIP_PARTS = frozenset(("artists_raw", "__pycache__", "skipped_upload_build"))
SKIP_NAMES = frozenset(("joshua.raw.html", "katelyn.raw.html", "skipped_pages_clipboard.html"))


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()

    def add(p: Path) -> None:
        if not p.is_file() or p.name in SKIP_NAMES:
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


def inject(html: str) -> tuple[str, bool]:
    changed = False
    if 'name="robots"' not in html and "name='robots'" not in html:
        m = HEAD_RE.search(html)
        if m:
            html = html[: m.end()] + "\n" + ROBOTS_META + html[m.end() :]
            changed = True
    if "/llms.txt" not in html:
        m = HEAD_RE.search(html)
        if m:
            html = html[: m.end()] + "\n" + LLMS_LINK + html[m.end() :]
            changed = True
    return html, changed


def main() -> int:
    n = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8")
        updated, ok = inject(raw)
        if ok and updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            n += 1
    print(f"Done: {n} page(s) updated with robots meta / llms link")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

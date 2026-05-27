#!/usr/bin/env python3
"""Insert Google Analytics (gtag.js) immediately after <head> on every static page."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GA_ID = "G-XLXNGGW7SX"

GOOGLE_TAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());

gtag('config', '{GA_ID}');
</script>"""

HEAD_RE = re.compile(r"(<head[^>]*>)", re.IGNORECASE)

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


def already_has_tag(html: str) -> bool:
    return GA_ID in html or "googletagmanager.com/gtag/js" in html


def inject_tag(html: str) -> tuple[str, bool]:
    if already_has_tag(html):
        return html, False
    m = HEAD_RE.search(html)
    if not m:
        return html, False
    pos = m.end()
    return html[:pos] + "\n" + GOOGLE_TAG + html[pos:], True


def main() -> int:
    updated = 0
    skipped = 0
    for path in iter_html_files():
        original = path.read_text(encoding="utf-8")
        new_html, ok = inject_tag(original)
        if not ok:
            if not HEAD_RE.search(original):
                print(f"no <head>: {path.relative_to(ROOT)}", file=sys.stderr)
            skipped += 1
            continue
        path.write_text(new_html, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
        updated += 1
    print(f"Done: {updated} updated, {skipped} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

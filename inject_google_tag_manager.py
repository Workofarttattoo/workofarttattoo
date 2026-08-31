#!/usr/bin/env python3
"""Inject Google Tag Manager container on every public HTML export."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GTM_ID = "GTM-TZTQSQBB"

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

HEAD_RE = re.compile(r"(<head[^>]*>)", re.IGNORECASE)
BODY_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)

GTM_HEAD_BLOCK_RE = re.compile(
    r"<!-- Google Tag Manager -->\s*<script>[\s\S]*?</script>\s*<!-- End Google Tag Manager -->\s*",
    re.IGNORECASE,
)
GTM_BODY_BLOCK_RE = re.compile(
    r"<!-- Google Tag Manager \(noscript\) -->\s*<noscript>[\s\S]*?</noscript>\s*<!-- End Google Tag Manager \(noscript\) -->\s*",
    re.IGNORECASE,
)

SKIP_NAMES = frozenset(
    (
        "skipped_pages_clipboard.html",
        "joshua.raw.html",
        "katelyn.raw.html",
    )
)
SKIP_PARTS = frozenset({"artists_raw", "__pycache__", "skipped_upload_build", ".git"})


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
    add(ROOT / "artists" / "code.html")
    add(ROOT / "appointments" / "code.html")
    add(ROOT / "appointments" / "woa-booking-forms.html")
    return out


def inject_gtm(html: str) -> tuple[str, bool]:
    changed = False
    cleaned = GTM_HEAD_BLOCK_RE.sub("", html)
    cleaned = GTM_BODY_BLOCK_RE.sub("", cleaned)
    if cleaned != html:
        changed = True
        html = cleaned

    if GTM_ID not in html:
        head = HEAD_RE.search(html)
        if not head:
            return html, False
        pos = head.end()
        html = html[:pos] + "\n" + GTM_HEAD + html[pos:]
        changed = True

    if f"googletagmanager.com/ns.html?id={GTM_ID}" not in html:
        body = BODY_RE.search(html)
        if not body:
            return html, changed
        pos = body.end()
        html = html[:pos] + "\n" + GTM_BODY + html[pos:]
        changed = True

    return html, changed


def main() -> int:
    updated = 0
    failed = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8", errors="replace")
        new_html, ok = inject_gtm(raw)
        if GTM_ID not in new_html and HEAD_RE.search(raw):
            print(f"no <body>: {path.relative_to(ROOT)}", file=sys.stderr)
            failed += 1
        if ok:
            path.write_text(new_html, encoding="utf-8")
            print(f"[ok] {path.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} file(s) with GTM ({GTM_ID}), {failed} missing body tag")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

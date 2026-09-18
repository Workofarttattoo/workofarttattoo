#!/usr/bin/env python3
"""Replace duplicate homepage index with a permanent redirect to site root."""

from __future__ import annotations

import html
from pathlib import Path

from woa_nav_config import HOME_SLUG, SITE_CANONICAL_HOST

ROOT = Path(__file__).resolve().parent
TARGET = "/"


def redirect_html() -> str:
    canonical = SITE_CANONICAL_HOST + TARGET
    escaped_target = html.escape(TARGET)
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="noindex,follow" name="robots"/>
<meta content="0; url={escaped_target}" http-equiv="refresh"/>
<title>Redirecting | Work of Art</title>
<link href="{html.escape(canonical)}" rel="canonical"/>
</head>
<body>
<main>
<h1>Redirecting</h1>
<p><a href="{escaped_target}">Continue to Work of Art Tattoo &amp; Piercing</a></p>
</main>
</body></html>
"""


def main() -> int:
    out_dir = ROOT / HOME_SLUG
    if not out_dir.is_dir():
        print(f"[skip] missing {HOME_SLUG}/")
        return 0
    text = redirect_html()
    index_path = out_dir / "index.html"
    index_path.write_text(text, encoding="utf-8")
    print(f"[redirect] /{HOME_SLUG}/ index.html -> {TARGET} (code.html kept as homepage source)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

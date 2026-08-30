#!/usr/bin/env python3
"""Retire the underscore cover-up URL as a static GitHub Pages placeholder.

GitHub Pages cannot issue a server 301. The safest static equivalent is:
- canonical + og:url pointing at the clean authority URL
- noindex,follow so this folder cannot compete
- immediate meta refresh (delay 0) plus a visible fallback link
- no independent Service/FAQ schema or authority copy
"""

from __future__ import annotations

import html
from pathlib import Path

from woa_nav_config import SITE_CANONICAL_HOST

ROOT = Path(__file__).resolve().parent
LEGACY_SLUG = "cover_up_tattoos_las_vegas_master_authority_guide"
CANONICAL_PATH = "/cover-up-tattoos-las-vegas/"
CANONICAL_URL = f"{SITE_CANONICAL_HOST}{CANONICAL_PATH}"


def redirect_html() -> str:
    target = html.escape(CANONICAL_PATH)
    canonical = html.escape(CANONICAL_URL)
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="noindex,follow" name="robots"/>
<meta content="0; url={target}" http-equiv="refresh"/>
<title>Cover-Up Tattoos moved | Work of Art</title>
<meta content="This cover-up guide now lives at the canonical Work of Art URL." name="description"/>
<link href="{canonical}" rel="canonical"/>
<meta content="website" property="og:type"/>
<meta content="{canonical}" property="og:url"/>
<meta content="Cover-Up Tattoos Las Vegas | Work of Art" property="og:title"/>
</head>
<body>
<main>
<h1>This cover-up guide has moved</h1>
<p>The canonical Las Vegas cover-up tattoo guide is now at <a href="{target}">{target}</a>.</p>
<p><a href="{target}">Continue to the cover-up tattoos Las Vegas guide</a>.</p>
</main>
</body></html>
"""


def write_stub() -> Path:
    out_dir = ROOT / LEGACY_SLUG
    out_dir.mkdir(parents=True, exist_ok=True)
    html_text = redirect_html()
    code = out_dir / "code.html"
    index = out_dir / "index.html"
    code.write_text(html_text, encoding="utf-8")
    index.write_text(html_text, encoding="utf-8")
    return code


def main() -> int:
    path = write_stub()
    print(f"[redirect] /{LEGACY_SLUG}/ -> {CANONICAL_PATH} ({path.relative_to(ROOT)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

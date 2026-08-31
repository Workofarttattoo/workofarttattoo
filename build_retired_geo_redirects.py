#!/usr/bin/env python3
"""Write noindex redirect placeholders for merged geo pages kept on disk."""

from __future__ import annotations

import html
from pathlib import Path

from woa_geo_pages import GEO_PAGE_ACTIONS, GEO_PAGE_REDIRECTS
from woa_nav_config import SITE_CANONICAL_HOST

ROOT = Path(__file__).resolve().parent

# Legacy overlap pages outside GEO_PAGES that should not stay indexable.
EXTRA_CONSOLIDATION_STUBS: dict[str, str] = {
    "tattoo_shop_near_the_strip_geo_seo_optimized": "/tattoo_shop_near_the_strip_nap_corrected/",
}


def write_stub(slug: str, target: str) -> None:
    out_dir = ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    html_text = redirect_html(slug, target)
    (out_dir / "code.html").write_text(html_text, encoding="utf-8")
    (out_dir / "index.html").write_text(html_text, encoding="utf-8")


def redirect_html(slug: str, target: str) -> str:
    title = "Redirecting | Work of Art"
    canonical = f"{SITE_CANONICAL_HOST}{target}"
    escaped_target = html.escape(target)
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="noindex,follow" name="robots"/>
<meta content="0; url={escaped_target}" http-equiv="refresh"/>
<title>{title}</title>
<meta content="This geo page has been consolidated into a stronger Work of Art visitor guide." name="description"/>
<link href="{html.escape(canonical)}" rel="canonical"/>
</head>
<body>
<main>
<h1>Redirecting</h1>
<p>We&#8217;ve folded this page into a stronger visitor guide so everything lives in one place. <a href="{escaped_target}">Continue there for directions, timing, and booking</a>.</p>
</main>
</body></html>
"""


def main() -> int:
    count = 0
    for slug, action in sorted(GEO_PAGE_ACTIONS.items()):
        if action != "MERGE_301":
            continue
        target = GEO_PAGE_REDIRECTS[slug]
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "code.html").write_text(redirect_html(slug, target), encoding="utf-8")
        count += 1
        print(f"[redirect] /{slug}/ -> {target}")
    for slug, target in sorted(EXTRA_CONSOLIDATION_STUBS.items()):
        write_stub(slug, target)
        count += 1
        print(f"[redirect] /{slug}/ -> {target}")
    print(f"Done: {count} retired geo redirect placeholder(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

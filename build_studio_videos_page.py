#!/usr/bin/env python3
"""Generate studio_videos/code.html — tattoo video library page."""

from __future__ import annotations

import re
from pathlib import Path

from client_videos import (
    PAGE_SPOTLIGHT_MARKER_END,
    PAGE_SPOTLIGHT_MARKER_START,
    export_videos_catalog,
    render_video_repo_page,
)
from woa_sparkle_cursor import (
    sparkle_body_open,
    sparkle_footer_script,
    sparkle_head_link,
)

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "studio_videos"
OUT = OUT_DIR / "code.html"
SHELL_PATH = ROOT / "appointments" / "code.html"
SLUG = "studio_videos"
CANON = f"https://workofarttattoo.com/{SLUG}/"
OG_IMG = "https://workofarttattoo.com/home_work_of_art_tattoo_piercing/las-vegas-tattoo-hero-background.webp"
MAIN_OPEN = '<main class="relative pt-20 min-h-screen">'

PHP_GTM_RE = re.compile(r"<\?php[^?]*\?\>\s*", re.IGNORECASE)
GUIDE_HUB_RE = re.compile(
    r'<nav aria-label="All guides"[\s\S]*?</nav>\s*',
    re.IGNORECASE,
)
SPOTLIGHT_RE = re.compile(
    rf"{re.escape(PAGE_SPOTLIGHT_MARKER_START)}[\s\S]*?{re.escape(PAGE_SPOTLIGHT_MARKER_END)}\n?",
    re.MULTILINE,
)
SPOTLIGHT_VIDEO_RE = re.compile(
    r"<!-- WOA_PAGE_SPOTLIGHT_VIDEO_START -->[\s\S]*?<!-- WOA_PAGE_SPOTLIGHT_VIDEO_END -->\n?",
    re.MULTILINE,
)
DUP_NAV_CSS_RE = re.compile(
    r"(<style data-woa-desktop-nav-css=\"1\">[\s\S]*?</style>)(\s*<style data-woa-desktop-nav-css=\"1\">[\s\S]*?</style>)+",
    re.MULTILINE,
)

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XLXNGGW7SX"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-XLXNGGW7SX');
</script>
"""

VIDEO_META = f"""<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Studio Videos | Tattoo Reels &amp; Client Stories | Work of Art Las Vegas</title>
<meta content="Watch tattoo session reels, client interviews, and in-studio footage from Work of Art Tattoo &amp; Piercing in Las Vegas — official Instagram video library." name="description"/>
<link rel="canonical" href="{CANON}"/>
<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{CANON}"/>
<meta property="og:title" content="Studio Videos | Work of Art Tattoo Las Vegas"/>
<meta property="og:description" content="Tattoo reels, client interviews, and in-studio footage from Work of Art Las Vegas."/>
<meta property="og:image" content="{OG_IMG}"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:site_name" content="Work of Art Tattoo &amp; Piercing"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Studio Videos | Work of Art Las Vegas"/>
<meta name="twitter:description" content="Official tattoo video library — reels and client stories from our Las Vegas studio."/>
<meta name="twitter:image" content="{OG_IMG}"/>
"""


def _extract_head_assets(shell: str) -> str:
    start = shell.find('<script src="https://cdn.tailwindcss.com')
    if start < 0:
        raise ValueError("Shell missing tailwind CDN block")
    end = shell.find("</head>", start)
    assets = shell[start:end]
    assets = DUP_NAV_CSS_RE.sub(r"\1", assets, count=1)
    return assets


def _extract_body_chrome(shell: str) -> str:
    body_open = shell.find("<body")
    if body_open < 0:
        raise ValueError("Shell missing <body>")
    body_gt = shell.find(">", body_open) + 1
    main_idx = shell.index(MAIN_OPEN)
    chrome = shell[body_gt:main_idx]
    chrome = PHP_GTM_RE.sub("", chrome)
    chrome = GUIDE_HUB_RE.sub("", chrome)
    return chrome


def _extract_footer(shell: str) -> str:
    footer_idx = shell.find("<footer class=")
    if footer_idx < 0:
        raise ValueError("Shell missing footer")
    footer = shell[footer_idx:]
    footer = SPOTLIGHT_VIDEO_RE.sub("", footer)
    footer = SPOTLIGHT_RE.sub("", footer)
    return footer


def _build_head(shell: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        '<html class="dark" lang="en"><head>\n'
        + GTAG
        + VIDEO_META
        + sparkle_head_link()
        + _extract_head_assets(shell)
        + "</head>\n"
    )


def _inject_sparkle_script(footer: str) -> str:
    if 'data-woa-sparkle-cursor="1"' in footer:
        return footer
    marker = "</body>"
    idx = footer.rfind(marker)
    if idx < 0:
        return footer + sparkle_footer_script()
    return footer[:idx] + sparkle_footer_script() + "\n" + footer[idx:]


def main() -> int:
    shell = SHELL_PATH.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    export_videos_catalog(OUT_DIR / "videos.json")

    footer = _inject_sparkle_script(_extract_footer(shell))

    body = (
        _build_head(shell)
        + '<body class="font-body-md text-body-md bg-background selection:bg-secondary selection:text-surface-container-lowest">\n'
        + sparkle_body_open()
        + _extract_body_chrome(shell)
        + MAIN_OPEN
        + "\n"
        + render_video_repo_page()
        + "\n</main>\n"
        + footer
    )
    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_DIR / 'videos.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

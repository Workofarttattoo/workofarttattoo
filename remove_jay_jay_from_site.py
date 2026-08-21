#!/usr/bin/env python3
"""Remove Jay Jay from all static HTML and crawl assets."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_PARTS = frozenset({".git", "__pycache__", "node_modules", "jay_jay_artist_portfolio_authentic_masterpieces"})

JAY_NAV_DESKTOP = re.compile(
    r'<a class="block px-3 py-2 text-\[13px\] leading-snug text-on-surface hover:text-secondary transition-colors" '
    r'href="/jay_jay_artist_portfolio_authentic_masterpieces/">Jay Jay — Portfolio</a>\s*',
    re.I,
)
JAY_NAV_MOBILE = re.compile(
    r'<a class="block py-1\.5 text-\[13px\] leading-snug font-medium text-secondary pl-3 border-b border-outline-variant/60 '
    r'hover:text-secondary hover:bg-surface-container/40 transition-colors woa-mnav-mobile-link" '
    r'href="/jay_jay_artist_portfolio_authentic_masterpieces/">Jay Jay — Portfolio</a>\s*',
    re.I,
)
JAY_GUIDE_PILL = re.compile(
    r'<a class="woa-guide-pill" href="/jay_jay_artist_portfolio_authentic_masterpieces/">[^<]*</a>\s*',
    re.I,
)
JAY_ARTIST_CARD = re.compile(
    r'<a class="group text-center" href="/jay_jay_artist_portfolio_authentic_masterpieces/">.*?</a>\s*',
    re.DOTALL | re.I,
)
JAY_COVER_ARTICLE = re.compile(
    r'<article class="flex flex-col md:flex-row gap-8 p-8 border border-outline-variant bg-surface-container-low">\s*'
    r'<div class="w-full md:w-48 aspect-square bg-surface-container shrink-0 flex items-center justify-center font-label-caps text-secondary">JJ</div>\s*'
    r'<div>\s*<h3 class="font-headline-md text-headline-md mb-2">Jay Jay</h3>.*?</article>\s*',
    re.DOTALL | re.I,
)
JAY_APPT_OPTION = re.compile(r'<option value="Jay Jay">Jay Jay</option>\s*', re.I)
JAY_INTERNAL_LI = re.compile(
    r'<li><a class="text-secondary underline hover:no-underline" href="/jay_jay_artist_portfolio_authentic_masterpieces/">Jay Jay — portfolio</a></li>\s*',
    re.I,
)
JAY_PORTFOLIO_LINK = re.compile(
    r'<a[^>]*href="/jay_jay_artist_portfolio_authentic_masterpieces/"[^>]*>.*?</a>\s*',
    re.DOTALL | re.I,
)
JAY_GEO_ROSTER_CARD = re.compile(
    r'<div class="flex flex-col md:flex-row gap-6 p-6 bg-surface-container-low border border-surface-variant '
    r'hover:bg-surface-container transition-colors duration-300">\s*'
    r'<div class="w-full md:w-1/3">\s*'
    r'<h3 class="font-headline-md text-headline-md text-secondary"><a class="hover:underline" '
    r'href="/jay_jay_artist_portfolio_authentic_masterpieces/">Jay Jay</a></h3>.*?</div>\s*</div>\s*',
    re.DOTALL | re.I,
)

TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    ("Meet Joshua Cole, Jay Jay, and Katelyn Cole", "Meet Joshua Cole and Katelyn Cole"),
    ("Joshua Cole, Jay Jay, and Katelyn Cole", "Joshua Cole and Katelyn Cole"),
    ("Joshua Cole, Katelyn Cole, and Jay Jay", "Joshua Cole and Katelyn Cole"),
    ("Joshua Cole and Jay Jay (tattoo) and Katelyn Cole", "Joshua Cole (tattoo &amp; piercing) and Katelyn Cole"),
    ("Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing)", "Joshua Cole (tattoo &amp; piercing) and Katelyn Cole (piercing)"),
    ("Joshua Cole and Jay Jay tattoo in-studio; Katelyn Cole is our master piercer.", "Joshua Cole handles tattoo and piercing in-studio; Katelyn Cole is our master piercer."),
    ("Joshua Cole and Jay Jay lead tattoo work; Katelyn Cole leads piercing.", "Joshua Cole leads tattoo and piercing; Katelyn Cole leads piercing."),
    ("Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing) — our three in-studio residents.", "Joshua Cole (tattoo &amp; piercing) and Katelyn Cole (piercing) — our two in-studio residents."),
    ("two tattooists (Joshua Cole and Jay Jay) and master piercer Katelyn Cole", "Joshua Cole (tattoo &amp; piercing) and master piercer Katelyn Cole"),
    ("Joshua Cole (tattoo & piercing; studio lead), Jay Jay (tattoo), and Katelyn Cole (master piercer)", "Joshua Cole (tattoo &amp; piercing; studio lead) and Katelyn Cole (master piercer)"),
    ("Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer)", "Joshua Cole (tattoo &amp; piercing; studio lead who trains the team) and Katelyn Cole (master piercer)"),
    ("Joshua Cole (tattoo & piercing), Jay Jay (tattoo), and Katelyn Cole (piercing)", "Joshua Cole (tattoo &amp; piercing) and Katelyn Cole (piercing)"),
    ("Joshua Cole (tattoo & piercing; trains the team), Jay Jay (tattoo), and Katelyn Cole (piercing)", "Joshua Cole (tattoo &amp; piercing; trains the team) and Katelyn Cole (piercing)"),
    ("Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing)", "Joshua Cole (tattoo &amp; piercing) and Katelyn Cole (piercing)"),
    ("Joshua Cole or Jay Jay", "Joshua Cole"),
    ("Joshua Cole and Jay Jay", "Joshua Cole"),
    ("Jay Jay on tattoo and Katelyn Cole as master piercer", "Katelyn Cole as master piercer"),
    ("with Jay Jay on tattoo and Katelyn Cole", "with Katelyn Cole"),
    ("Jay Jay (tattoo)", ""),
    ("Jay Jay (tattoo), ", ""),
    (", Jay Jay (tattoo)", ""),
    ("Jay Jay — Portfolio", ""),
    ("Jay Jay Artist Portfolio", ""),
    ("Jay Jay — realism tattoo artist", "Joshua Cole — realism tattoo artist"),
    ("Artist: Jay Jay", "Artist: Joshua Cole"),
    ("Jay Jay handles bold illustrative cover-ups, ornamental flow, and pieces that need strong silhouette to hide old shapes underneath.", ""),
    ("<h3 class=\"font-headline-md text-headline-md mb-2\">Jay Jay</h3>", ""),
    ("3 in-studio (Joshua: tattoo & piercing + trains the team; Jay Jay: tattoo; Katelyn: piercing)", "2 in-studio (Joshua: tattoo & piercing + trains the team; Katelyn: piercing)"),
    ("Three in-studio residents — Joshua Cole (tattoo & piercing; trains the team), Jay Jay (tattoo), Katelyn Cole (piercing)", "Two in-studio residents — Joshua Cole (tattoo & piercing; trains the team) and Katelyn Cole (piercing)"),
    ("Three in-studio residents — Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing)", "Two in-studio residents — Joshua Cole (tattoo & piercing) and Katelyn Cole (piercing)"),
    ("three in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer)", "two in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team) and Katelyn Cole (master piercer)"),
    ("three in-studio artists: two tattooists (Joshua Cole and Jay Jay) and master piercer Katelyn Cole", "two in-studio artists: Joshua Cole (tattoo & piercing) and master piercer Katelyn Cole"),
    ("Three residents today", "Two residents today"),
    ("three in-studio residents", "two in-studio residents"),
    ("Three in-studio residents", "Two in-studio residents"),
    ("3 In-Studio Artists", "2 In-Studio Artists"),
    ("3 in-studio residents", "2 in-studio residents"),
    ("<h4 class=\"text-secondary font-headline-md\">3</h4>", "<h4 class=\"text-secondary font-headline-md\">2</h4>"),
    ("Tattoo work with Joshua Cole and Jay Jay", "Tattoo work with Joshua Cole"),
    ("Joshua Cole and Jay Jay; Joshua also offers piercing", "Joshua Cole offers tattoo and piercing"),
    ("Joshua Cole or Jay Jay — backed by a master piercer", "Joshua Cole — backed by master piercer"),
    ("one of our two in-studio tattoo artists — Joshua Cole or Jay Jay", "Joshua Cole"),
    ("Joshua Cole and Jay Jay tattoo in-studio", "Joshua Cole tattoos and pierces in-studio"),
    ("Joshua Cole offers tattoo and piercing and trains resident artists and alumni; Jay Jay leads tattoo sessions; Katelyn Cole leads piercing.", "Joshua Cole offers tattoo and piercing and trains resident artists and alumni; Katelyn Cole leads piercing."),
    (
        "3 in-studio — Joshua Cole (tattoo &amp; piercing; studio lead who trains artists), , Katelyn Cole (piercing).",
        "2 in-studio — Joshua Cole (tattoo &amp; piercing; studio lead who trains artists) and Katelyn Cole (piercing).",
    ),
    (
        "three in-studio artists: Joshua Cole (tattoo &amp; piercing; studio lead who trains the team), , and Katelyn Cole (master piercer).",
        "two in-studio artists: Joshua Cole (tattoo &amp; piercing; studio lead who trains the team) and Katelyn Cole (master piercer).",
    ),
    (", ,", " and"),
    ("Work of Art is led by Joshua Cole (tattoo, piercing, and artist training), with Jay Jay on tattoo and Katelyn Cole as master piercer. Three residents today;", "Work of Art is led by Joshua Cole (tattoo, piercing, and artist training) with Katelyn Cole as master piercer. Two residents today;"),
    ("Joshua Cole (tattoo & piercing; studio lead), Jay Jay (tattoo), and Katelyn Cole (master piercer). Book tattoo", "Joshua Cole (tattoo & piercing; studio lead) and Katelyn Cole (master piercer). Book tattoo"),
]


def iter_html() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if "skipped_upload_build" in path.parts:
            continue
        out.append(path)
    return out


def scrub_html(text: str) -> str:
    for pattern in (
        JAY_NAV_DESKTOP,
        JAY_NAV_MOBILE,
        JAY_GUIDE_PILL,
        JAY_ARTIST_CARD,
        JAY_COVER_ARTICLE,
        JAY_APPT_OPTION,
        JAY_INTERNAL_LI,
        JAY_PORTFOLIO_LINK,
        JAY_GEO_ROSTER_CARD,
    ):
        text = pattern.sub("", text)
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def main() -> int:
    changed = 0
    for path in iter_html():
        raw = path.read_text(encoding="utf-8", errors="replace")
        cleaned = scrub_html(raw)
        if cleaned != raw:
            path.write_text(cleaned, encoding="utf-8")
            changed += 1
            print(f"[ok] {path.relative_to(ROOT)}")
    print(f"Done: {changed} HTML file(s) cleaned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

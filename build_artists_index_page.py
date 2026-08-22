#!/usr/bin/env python3
"""Rebuild /artists/ index with resident artist portrait cards and portfolio links."""

from __future__ import annotations

import re
from pathlib import Path

from fix_homepage_portfolio import artist_cards_html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artists" / "code.html"


def main_body() -> str:
    cards = artist_cards_html()
    return f"""<h1 class="font-headline-lg text-on-surface mb-6">Artists at Work of Art</h1>
<p class="font-body-lg text-on-surface-variant mb-6">Three in-studio residents at 2375 E. Tropicana Ave, Suite 3 — Joshua Cole (tattoo &amp; piercing; studio lead), Katelyn Cole (master piercer), and Teralyn (fineline floral work, script, custom drawings by commission, and detailed smaller tattoos). Tap a portrait to open their bio or portfolio.</p>
<p class="font-body-md text-on-surface-variant mb-12"><a class="text-secondary underline hover:no-underline" href="/appointments/">Book an appointment</a> · <a class="text-secondary underline hover:no-underline" href="tel:+17252241240">725-224-1240</a> · <a class="text-secondary underline hover:no-underline" href="mailto:booking@workofarttattoo.com">booking@workofarttattoo.com</a></p>
<section aria-labelledby="woa-artists-roster-heading" class="mb-16">
<h2 class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-8 text-center" id="woa-artists-roster-heading">In-Studio Residents</h2>
{cards}
<div class="grid grid-cols-1 sm:grid-cols-3 gap-gutter max-w-5xl mx-auto mt-8 text-center">
<a class="font-label-caps text-label-caps text-secondary uppercase tracking-widest hover:underline" href="/artists/joshua-cole/">Joshua Cole — Tattoo Portfolio →</a>
<a class="font-label-caps text-label-caps text-secondary uppercase tracking-widest hover:underline" href="/artists/katelyn-cole/">Katelyn Cole — Piercing Portfolio →</a>
<a class="font-label-caps text-label-caps text-secondary uppercase tracking-widest hover:underline" href="/artists/teralyn/">Teralyn — Fineline Floral &amp; Script Bio →</a>
</div>
</section>
<p class="font-body-md text-on-surface-variant text-center"><a class="text-secondary underline hover:no-underline" href="/#portfolio">View full studio portfolio on the homepage</a></p>"""


def rebuild() -> None:
    if not OUT.is_file():
        raise SystemExit(f"Missing {OUT}")

    raw = OUT.read_text(encoding="utf-8")
    main_open = re.search(
        r'(<main class="pt-32 pb-24 px-margin-mobile md:px-margin-desktop max-w-4xl mx-auto">)',
        raw,
    )
    main_close = raw.find("</main>", main_open.end() if main_open else 0)
    if not main_open or main_close < 0:
        raise SystemExit("Could not locate <main> in artists/code.html")

    updated = raw[: main_open.end()] + "\n" + main_body() + "\n" + raw[main_close:]
    OUT.write_text(updated, encoding="utf-8")
    print(f"[ok] rebuilt {OUT.relative_to(ROOT)} ({len(updated):,} bytes)")


if __name__ == "__main__":
    rebuild()

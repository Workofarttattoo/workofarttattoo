#!/usr/bin/env python3
"""Homepage welcome — warm tone, Joshua's hospitality story, free consults."""

from __future__ import annotations

import re
from pathlib import Path

from woa_joshua_tattooing import homepage_at_work_picture
from woa_nav_config import (
    STUDIO_ADDRESS_SINGLE_LINE,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
    STUDIO_ROSTER_BLURB,
    STUDIO_STREET_ADDRESS,
)

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "home_work_of_art_tattoo_piercing"
CODE = HOME / "code.html"
ROOT_CODE = ROOT / "code.html"

MARKER_START = "<!-- WOA_HOME_WELCOME_START -->"
MARKER_END = "<!-- WOA_HOME_WELCOME_END -->"

WELCOME_HTML = f"""{MARKER_START}
<section class="woa-home-welcome px-margin-mobile md:px-margin-desktop pb-10 md:pb-14 bg-background border-b border-outline-variant/20" data-woa-home-welcome="1" id="welcome">
<div class="max-w-3xl mx-auto space-y-6">
<div class="flex flex-wrap gap-2 md:gap-3">
<span class="inline-flex items-center px-3 py-1.5 bg-secondary/15 border border-secondary/35 font-label-caps text-[10px] uppercase tracking-widest text-secondary">No attitudes</span>
<span class="inline-flex items-center px-3 py-1.5 bg-secondary/15 border border-secondary/35 font-label-caps text-[10px] uppercase tracking-widest text-secondary">Free consultations</span>
<span class="inline-flex items-center px-3 py-1.5 bg-secondary/15 border border-secondary/35 font-label-caps text-[10px] uppercase tracking-widest text-secondary">Walk-ins always welcome</span>
</div>
<h1 class="font-headline-xl text-[30px] sm:text-[36px] md:text-[42px] text-on-surface leading-tight">Tattoo &amp; Piercing Studio in Las Vegas</h1>
<p class="font-headline-md text-[22px] md:text-[28px] text-secondary leading-snug">You're welcome here — questions included.</p>
<p class="font-body-lg text-body-lg text-on-surface-variant leading-relaxed">
We're happy to answer every question we can — or guide you to someone who can. No pressure, no eye rolls, no making you feel small for asking.
</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">
We know what walking into a strange tattoo shop can feel like: the cool kids from school huddled at lunch, and you're the new kid looking for a seat — or even a friendly nod. At Work of Art, we lead with warmth that comes from a genuine heart of service.
</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">
Before I was a successful artist, I — <strong class="text-on-surface font-semibold">Joshua Cole</strong> — was a successful waiter at high-end fine-dining rooms: Spago, Jonathan Bentley's, Ruth's Chris Steak House, and The Shore Room at the Renaissance (Greek-inspired). Each taught me to take real pleasure in helping people, getting to know them, and making them feel appreciated and valued.
</p>
<p class="font-body-md text-on-surface-variant leading-relaxed">
I also attended art school, oil painting school, and illustration school, along with numerous seminars and other continuing-education opportunities to keep progressing as an artist. I design our merchandise, T-shirts, and all of our advertising.
</p>
<p class="font-body-md text-on-surface leading-relaxed border-l-2 border-secondary pl-5">
Don't just get a tattoo or piercing — leave feeling valued. Like you made a lifelong friend, or reconnected with an old one.
</p>
<div class="flex flex-col sm:flex-row flex-wrap gap-3 pt-2">
<a class="inline-flex justify-center bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest gold-glow transition-all" href="/appointments/">Book a free consult</a>
<a class="inline-flex justify-center border border-outline px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest hover:border-secondary transition-colors" href="{STUDIO_PHONE_TEL}">Call {STUDIO_PHONE_PARENS}</a>
<a class="inline-flex justify-center border border-outline-variant/50 px-8 py-4 font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant hover:text-secondary hover:border-secondary transition-colors" href="/walk_in_tattoos_las_vegas_authority_guide/">Walk-in info</a>
</div>
<p class="font-body-md text-on-surface-variant text-sm pt-1"><a class="text-secondary underline hover:no-underline" href="/official_location_hours_contact/" aria-label="{STUDIO_ADDRESS_SINGLE_LINE}">{STUDIO_STREET_ADDRESS}</a> · {STUDIO_ROSTER_BLURB}</p>
</div>
</section>
{MARKER_END}"""

WELCOME_RE = re.compile(
    rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}\s*",
    re.MULTILINE,
)

SOFTEN: tuple[tuple[str, str], ...] = (
    (
        "<span class=\"font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]\">Careful Studio Process</span>",
        "<span class=\"font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]\">Warm welcome, expert care</span>",
    ),
    (
        "<h2 class=\"font-headline-lg text-headline-lg text-on-surface\">Expert Piercing &amp; Luxury Jewelry</h2>",
        "<h2 class=\"font-headline-lg text-headline-lg text-on-surface\">Piercing with patience &amp; jewelry-fit planning</h2>",
    ),
    (
        "We provide a wide range of piercing services with placement planning, jewelry-fit guidance, and clear aftercare.",
        "Katelyn Cole pierces with calm, clear explanations — starter jewelry sized for swelling, a clean setup, and aftercare you can actually follow in Vegas heat. Questions welcome at every step.",
    ),
    (
        "<span class=\"font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]\">The Experience</span>\n<h2 class=\"font-headline-lg text-headline-lg text-on-surface\">A Legacy of Creative Vision</h2>",
        "<span class=\"font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]\">Joshua Cole</span>\n<h2 class=\"font-headline-lg text-headline-lg text-on-surface\">Artistry rooted in hospitality</h2>",
    ),
    (
        "Every tattoo at Work of Art is a unique collaboration between artist and client. We don't just replicate designs; we breathe life into your concepts through technical mastery.",
        "Every tattoo here is a conversation — your idea, my craft, and the same care I learned serving guests at Spago and Ruth's Chris: listen first, explain honestly, and make you feel looked after.",
    ),
    (
        "<h4 class=\"text-secondary font-headline-md\">2</h4>\n<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Artists in-studio today</p>",
        "<h4 class=\"text-secondary font-headline-md\">3</h4>\n<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Resident Artists</p>",
    ),
    (
        "While we recommend appointments for custom large-scale work, We offer same-day availability for both tattoos and piercings to accommodate your schedule.",
        "Walk-ins are always welcome when the schedule allows — and we're glad to talk through sizing, placement, and pricing before you commit to anything.",
    ),
)


BANNER_RE = re.compile(
    r"<!-- WOA_HERO_BANNER_START -->[\s\S]*?<!-- WOA_HERO_BANNER_END -->\s*",
    re.MULTILINE,
)


def ensure_banner_first(html: str) -> str:
    """Studio banner belongs above the welcome copy on first paint."""
    welcome_m = WELCOME_RE.search(html)
    banner_m = BANNER_RE.search(html)
    if not welcome_m or not banner_m or welcome_m.start() > banner_m.start():
        return html
    welcome_block = welcome_m.group(0)
    banner_block = banner_m.group(0)
    html = WELCOME_RE.sub("", html, count=1)
    html = BANNER_RE.sub("", html, count=1)
    return re.sub(
        r"(<main[^>]*>\s*)",
        rf"\1{banner_block}{welcome_block}",
        html,
        count=1,
    )


def inject_welcome(html: str) -> str:
    if MARKER_START in html:
        html = WELCOME_RE.sub(WELCOME_HTML + "\n", html, count=1)
    elif "<main" in html and "WOA_HERO_BANNER_END" in html:
        html = html.replace(
            "<!-- WOA_HERO_BANNER_END -->",
            "<!-- WOA_HERO_BANNER_END -->\n" + WELCOME_HTML + "\n",
            1,
        )
    elif "<main" in html and "WOA_HERO_BANNER_START" in html:
        html = html.replace(
            "<!-- WOA_HERO_BANNER_START -->",
            WELCOME_HTML + "\n<!-- WOA_HERO_BANNER_START -->",
            1,
        )
    elif "<main" in html:
        html = re.sub(
            r"(<main[^>]*>)",
            rf"\1\n{WELCOME_HTML}\n",
            html,
            count=1,
        )
    return ensure_banner_first(html)


def soften_copy(html: str) -> str:
    for old, new in SOFTEN:
        html = html.replace(old, new)
    return html


def fix_joshua_experience_image(html: str) -> str:
    """Joshua Cole block should show Joshua tattooing, not a healed tattoo photo."""
    marker = "<!-- Experience Section -->"
    if marker not in html:
        return html
    start = html.index(marker)
    end = html.find("<!-- FAQ Section -->", start)
    if end < 0:
        end = html.find("<section class=\"py-12 md:py-16", start + len(marker))
    if end < 0:
        return html
    block = html[start:end]
    if "aspect-square bg-surface-container overflow-hidden" not in block:
        return html
    picture = homepage_at_work_picture()
    new_block = re.sub(
        r"<div class=\"aspect-square bg-surface-container overflow-hidden border border-outline-variant/30\">\s*"
        r"(?:<picture>.*?</picture>|<img[^>]+>)\s*"
        r"</div>",
        f'<div class="aspect-square bg-surface-container overflow-hidden border border-outline-variant/30">{picture}</div>',
        block,
        count=1,
        flags=re.DOTALL,
    )
    if new_block == block:
        return html
    return html[:start] + new_block + html[end:]


def patch_html(html: str) -> str:
    html = inject_welcome(html)
    html = soften_copy(html)
    html = fix_joshua_experience_image(html)
    return html


def main() -> int:
    for path in (CODE, ROOT_CODE):
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = patch_html(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[welcome] {path.relative_to(ROOT)}")
        else:
            print(f"[skip] {path.relative_to(ROOT)} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

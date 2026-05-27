#!/usr/bin/env python3
"""Replace inflated or fictional artist roster copy with accurate studio facts."""

from __future__ import annotations

import re
from pathlib import Path

from woa_nav_config import ROOT_A, STUDIO_ROSTER_BLURB, STUDIO_ROSTER_LEGACY

ROOT = ROOT_A
SKIP_DIRS = frozenset({"artists_raw", ".git", "__pycache__", "node_modules"})
SKIP_FILES = frozenset({"skipped_pages_clipboard.html"})

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "<h4 class=\"text-secondary font-headline-md\">15+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Master Artists</p>",
        "<h4 class=\"text-secondary font-headline-md\">3</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Resident Artists</p>",
    ),
    (
        "<h4 class=\"text-secondary font-headline-md\">50k+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Hours Inked</p>",
        "<h4 class=\"text-secondary font-headline-md\">7+</h4>\n"
        "<p class=\"text-on-surface-variant font-label-caps text-[10px] uppercase tracking-widest\">Artists Mentored</p>",
    ),
    ("<p class=\"font-body-md\">4 Artists Available</p>", "<p class=\"font-body-md\">3 In-Studio Artists</p>"),
    ("<p class=\"font-body-md\">2 Tattoo · 1 Piercing</p>", "<p class=\"font-body-md\">3 In-Studio Artists</p>"),
    (
        "AWARD-WINNING RESIDENT ARTISTS",
        "THREE RESIDENT ARTISTS",
    ),
    (
        "A premier studio is a collective of resident artists with decades of combined experience. These are professionals who have spent years mastering specific styles—Realism, Traditional, Neo-Traditional, or Fine Line.",
        "A premier studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer).",
    ),
    (
        "A premier studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: two tattooists (Joshua Cole and Jay Jay) and master piercer Katelyn Cole, each with a clear specialty.",
        "A premier studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer).",
    ),
    (
        "At Work of Art, our collective is comprised of classically trained painters and illustrators. We believe that the ability to create original work on a canvas is the ultimate prerequisite for creating a masterpiece on the skin.",
        "At Work of Art, our small resident team is built on fine-art discipline and specialization — not volume. Joshua Cole offers tattoo and piercing and trains resident artists and alumni; Jay Jay leads tattoo sessions; Katelyn Cole leads piercing. Seven alumni trained here now run their own shops or travel as guest artists.",
    ),
    ("See the fine art roots of our master artists.", "Meet our three resident artists and their specialties."),
    ("Consult with our award-winning artists today", "Consult with our resident artists today"),
    ("Mark Thorne", "Joshua Cole"),
    ("Lead Artist &amp; Founder", "Lead Tattoo Artist — Black &amp; Grey Realism"),
    ("Followed Mark's desert healing guide", "Followed Work of Art's desert healing guide"),
    ("Artist: Thorne", "Artist: Joshua Cole"),
    ("Artist: Elara", "Artist: Jay Jay"),
    ("Piercing &amp; Fine Line", "Master Piercer"),
    ("Piercing & Fine Line", "Master Piercer"),
    ("Katelyn Cole — Piercing &amp; Fine Line", "Katelyn Cole — Master Piercer"),
    ("Katelyn Cole — Piercing & Fine Line", "Katelyn Cole — Master Piercer"),
    (
        "Joshua Cole, Katelyn Cole, and Jay Jay — the resident masters behind every piece at Work of Art Tattoo &amp; Piercing.",
        "Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer). Seven artists trained at Work of Art now own shops or travel as guest artists — we're proud of that legacy without pretending we have a dozen chairs filled today.",
    ),
    (
        "Joshua Cole and Jay Jay tattoo in-studio; Katelyn Cole is our master piercer. Seven artists trained at Work of Art now own shops or travel as guest artists — we're proud of that legacy without pretending we have a dozen chairs filled today.",
        f"{STUDIO_ROSTER_BLURB} {STUDIO_ROSTER_LEGACY}",
    ),
    (
        "Joshua Cole (tattoo & piercing; studio lead who trains the team), Jay Jay (tattoo), and Katelyn Cole (master piercer). Seven artists trained at Work of Art now own shops or travel as guest artists — we're proud of that legacy without pretending we have a dozen chairs filled today.",
        f"{STUDIO_ROSTER_BLURB} {STUDIO_ROSTER_LEGACY}",
    ),
    ("New Artist Coming Soon", ""),
    ("NEW ARTIST COMING SOON", ""),
    ("New artist coming soon", ""),
    (
        "Joshua Cole, Katelyn Cole, and Jay Jay — the resident masters at Work of Art Tattoo &amp; Piercing, Las Vegas.",
        "Joshua Cole (tattoo & piercing), Jay Jay (tattoo), and Katelyn Cole (piercing) — our three in-studio residents. Joshua trains artists across the studio and alumni network. Seven alumni trained here now lead their own studios or travel as guest artists.",
    ),
    (
        "Joshua Cole and Jay Jay (tattoo) and Katelyn Cole (piercing) — our three in-studio residents. Seven alumni trained here now lead their own studios or travel as guest artists.",
        "Joshua Cole (tattoo & piercing), Jay Jay (tattoo), and Katelyn Cole (piercing) — our three in-studio residents. Joshua trains artists across the studio and alumni network. Seven alumni trained here now lead their own studios or travel as guest artists.",
    ),
    (
        "two tattooists (Joshua Cole and Jay Jay) and master piercer Katelyn Cole",
        "Joshua Cole (tattoo & piercing; studio lead), Jay Jay (tattoo), and Katelyn Cole (master piercer)",
    ),
    (
        "Joshua Cole and Jay Jay lead tattoo work; Katelyn Cole leads piercing.",
        "Joshua Cole offers tattoo and piercing and trains the team; Jay Jay leads tattoo work; Katelyn Cole leads piercing.",
    ),
    (
        "Joshua Cole and Jay Jay tattoo in-studio; Katelyn Cole is our master piercer.",
        "Joshua Cole (tattoo & piercing; studio lead), Jay Jay (tattoo), and Katelyn Cole (master piercer).",
    ),
    (
        "2 tattoo artists and 1 master piercer",
        "Joshua Cole (tattoo & piercing; trains the team), Jay Jay (tattoo), and Katelyn Cole (piercing)",
    ),
    (
        "Tattoo services only — piercing is handled by Katelyn Cole.",
        "Master tattoo & piercing artist; studio founder who trains resident artists and alumni across Las Vegas.",
    ),
    (
        "Lead Tattoo Artist",
        "Master Artist — Tattoo &amp; Piercing",
    ),
    (
        "Lead Tattoo Artist — Black &amp; Grey Realism",
        "Master Artist — Tattoo, Piercing &amp; Training",
    ),
    (
        "Tattoo work at the studio is handled by Joshua Cole and Jay Jay.",
        "Tattoo work with Joshua Cole and Jay Jay; Joshua also offers piercing and trains artists at the studio.",
    ),
    (
        "Every tattoo at Work of Art is a collaboration with one of our two in-studio tattoo artists — Joshua Cole or Jay Jay — backed by a master piercer, Katelyn Cole.",
        "Work of Art is led by Joshua Cole (tattoo, piercing, and artist training), with Jay Jay on tattoo and Katelyn Cole as master piercer. Three residents today; seven alumni we trained now run their own shops or travel as guests.",
    ),
    (
        "Three in-studio residents — Joshua Cole and Jay Jay (tattoo), Katelyn Cole (piercing)",
        "Three in-studio residents — Joshua Cole (tattoo & piercing; trains the team), Jay Jay (tattoo), Katelyn Cole (piercing)",
    ),
]

MARCUS_SIDEBAR = re.compile(
    r"<h5 class=\"font-headline-md text-lg text-on-surface\">Marcus Vane</h5>\s*"
    r"<p class=\"font-label-caps text-\[10px\] text-secondary uppercase mb-4 tracking-widest\">"
    r"Studio Director &amp; Master Artist</p>\s*"
    r"<p class=\"font-body-md text-sm text-on-surface-variant leading-relaxed\">\s*"
    r"With over 22 years in the Las Vegas tattoo industry, Marcus has seen the evolution of the city's ink culture\.[^<]*</p>",
    re.DOTALL,
)

JOSHUA_SIDEBAR = """<h5 class="font-headline-md text-lg text-on-surface">Joshua Cole</h5>
<p class="font-label-caps text-[10px] text-secondary uppercase mb-4 tracking-widest">Master Artist — Tattoo &amp; Piercing</p>
<p class="font-body-md text-sm text-on-surface-variant leading-relaxed">
                    Joshua Cole is widely recognized for black and grey realism in Las Vegas and offers professional piercing. He trains resident artists and alumni across the valley from Work of Art Tattoo &amp; Piercing.
                </p>"""


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES or "skipped_upload_build" in path.parts:
            continue
        out.append(path)
    return out


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = MARCUS_SIDEBAR.sub(JOSHUA_SIDEBAR, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = [p for p in iter_html_files() if process(p)]
    for p in changed:
        print(p.relative_to(ROOT))
    print(f"---\nUpdated {len(changed)} files")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Replace empty superlatives with evidence-backed studio copy."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = frozenset({"artists_raw", "skipped_upload_build", ".git"})

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Located at 2375 E. Tropicana Ave, Suite 3, we offer elite artistry and medical-grade hygiene for every client.",
        "Located at 2375 E. Tropicana Ave, Suite 3 — three in-studio artists, healed portfolio photos, and a consult-first studio visit.",
    ),
    (
        "<h4 class=\"font-headline-md text-headline-md text-on-surface\">Elite Cleanliness</h4>",
        "<h4 class=\"font-headline-md text-headline-md text-on-surface\">Documented cleanliness</h4>",
    ),
    (
        "The premier destination for luxury tattoo and piercing experiences in Las Vegas. Expertly crafted, eternally personal.",
        "Three in-studio artists, consult-first booking, piercing consultations, and healed work on display — 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "Three in-studio artists, consult-first booking, implant-grade piercing jewelry, and healed work on display — 2375 E. Tropicana Ave, Suite 3.",
        "Three in-studio artists, consult-first booking, piercing consultations, and healed work on display — 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "The premier destination for high-contrast technical tattooing and micro-realism in the heart of Las Vegas.",
        "Fine line and black & grey work with healed photos at 6–12 months — Joshua Cole, 20+ years, consult-first on E. Tropicana.",
    ),
    (
        "The elite destination for large-scale tattoo artistry and technical precision in the heart of Las Vegas.",
        "Large-scale sleeves and back pieces planned session-by-session — healed portfolio, transparent quotes, Joshua Cole on E. Tropicana.",
    ),
    (
        "The premier destination for high-end artistry and clinical safety in Las Vegas. Excellence isn't an option; it's our standard.",
        "Consult-first tattoo and piercing planning, healed galleries, and named artists — Joshua Cole, Katelyn Cole, and Teralyn in-studio at 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "Work of Art Tattoo &amp; Piercing is widely recognized as the premier destination for ear curation in Las Vegas.",
        "Katelyn Cole leads ear curation at Work of Art — anatomy-first marking, jewelry planning, and downsizing on the calendar.",
    ),
    (
        "<p class=\"font-bold\">Elite Artistry</p>",
        "<p class=\"font-bold\">Healed portfolio on display</p>",
    ),
    (
        "Premier Tattoo &amp; Piercing Studio in the heart of Las Vegas. Where technical excellence meets elite artistry.",
        "Tattoo &amp; piercing studio on E. Tropicana — consult-first booking, healed galleries, and jewelry planning.",
    ),
    (
        "Premier Tattoo &amp; Piercing Studio located in the heart of Las Vegas. Artistry without compromise.",
        "Tattoo &amp; piercing at 2375 E. Tropicana Ave, Suite 3 — healed work, consult-first booking, (725) 224-1240.",
    ),
]


def iter_html() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in path.parts):
            continue
        out.append(path)
    return out


def main() -> int:
    changed = 0
    for path in iter_html():
        raw = path.read_text(encoding="utf-8")
        updated = raw
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
    print(f"Done: {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

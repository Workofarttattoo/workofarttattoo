#!/usr/bin/env python3
"""Visual-intent repairs that must survive static rebuilds."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SLEEVE = ROOT / "best_tattoo_styles_for_sleeves_large_scale_project_hub" / "code.html"
REALISM_ALIAS = ROOT / "realism-tattoos-las-vegas" / "code.html"
COVER_SLUGS = (
    ROOT / "cover-up-tattoos-las-vegas" / "code.html",
)

SPOTLIGHT_RE = re.compile(
    r"<!-- WOA_PAGE_SPOTLIGHT_VIDEO_START -->[\s\S]*?<!-- WOA_PAGE_SPOTLIGHT_VIDEO_END -->\s*",
    re.I,
)


def patch_sleeve() -> bool:
    if not SLEEVE.is_file():
        return False
    raw = SLEEVE.read_text(encoding="utf-8")
    text = raw

    def remove_piercing_spotlight(match: re.Match[str]) -> str:
        block = match.group(0)
        if "katelyn" in block.lower() or "piercing" in block.lower() or "C78fY1quCVF" in block:
            return ""
        return block

    text = SPOTLIGHT_RE.sub(remove_piercing_spotlight, text)
    text = text.replace("The Joshua Cole Collection", "Sleeve Style Reference Gallery")
    text = text.replace("CURATED MASTERWORKS", "REFERENCE AND STUDIO PLANNING EXAMPLES")
    text = re.sub(
        r"full back and sleeve tattoo masterpiece by Joshua Cole",
        "large-scale sleeve and back tattoo reference example",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"by Joshua Cole\. The",
        "used as a visual planning reference. The",
        text,
        flags=re.I,
    )
    if text != raw:
        SLEEVE.write_text(text, encoding="utf-8")
        return True
    return False


def patch_realism() -> bool:
    if not REALISM_ALIAS.is_file():
        return False
    raw = REALISM_ALIAS.read_text(encoding="utf-8")
    text = raw
    text = text.replace(">Angle 1<", ">Lion thigh detail<")
    text = text.replace(">Forearm Variation<", ">Separate forearm wildlife piece<")
    text = text.replace(
        "Lion thigh realism tattoo angle 1",
        "Black and grey lion thigh realism tattoo detail",
    )
    text = text.replace(
        "Roaring lion tiger forearm realism tattoo",
        "Separate roaring lion and tiger forearm realism tattoo",
    )
    if text != raw:
        REALISM_ALIAS.write_text(text, encoding="utf-8")
        return True
    return False


def patch_coverups() -> int:
    changed = 0
    for path in COVER_SLUGS:
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        text = raw
        text = text.replace(
            "Cover up tattoo Las Vegas — black and grey lion thigh realism, Work of Art Tattoo",
            "Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas",
        )
        text = text.replace(
            "Healed cover up tattoo Las Vegas — black and grey lion thigh realism",
            "Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas",
        )
        text = text.replace(
            "Color phoenix hand tattoo — cover-up work Las Vegas",
            "Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas",
        )
        if text != raw:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    changed = 0
    changed += int(patch_sleeve())
    changed += int(patch_realism())
    changed += patch_coverups()
    print(f"[visual-intent] repaired {changed} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

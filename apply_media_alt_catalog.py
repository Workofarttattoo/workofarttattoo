#!/usr/bin/env python3
"""Apply woa_media_alt_catalog.json to studio/offsite manifest KNOWN dicts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from woa_studio_media_manifest import MediaCategory

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "woa_media_alt_catalog.json"
STUDIO_MANIFEST = ROOT / "woa_studio_media_manifest.py"
OFFSITE_MANIFEST = ROOT / "woa_offsite_media_manifest.py"

PIERCE_WORDS = (
    "piercing", "septum", "nostril", "helix", "conch", "lobe", "tragus",
    "industrial", "labret", "eyebrow", "cartilage", "philtrum", "bridge piercing",
)
STUDIO_WORDS = (
    "storefront", "studio gallery", "group celebration", "instagram grid",
    "art car", "contact phone", "donning gloves", "guest admiring", "studio grid",
    "montage", "lifestyle instagram",
)
ART_WORDS = ("illustration", "framed", "pennywise", "drawing", "tattoo flash", "portrait art")


def infer_studio_category(title: str, alt: str) -> MediaCategory:
    text = f"{title} {alt}".lower()
    if any(w in text for w in PIERCE_WORDS):
        return MediaCategory.KATELYN_PIERCING
    if any(w in text for w in STUDIO_WORDS):
        return MediaCategory.STUDIO_LIFE
    if any(w in text for w in ART_WORDS):
        return MediaCategory.JOSHUA_ART
    return MediaCategory.JOSHUA_TATTOO


def py_quote(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def upsert_entry(text: str, prefix: str, line: str) -> str:
    pat = rf'    "{prefix}": \([^)]+\),\n'
    if re.search(pat, text):
        return re.sub(pat, line, text, count=1)
    return text.replace(
        "\n}\n\n\ndef slugify",
        "\n" + line + "\n}\n\n\ndef slugify",
        1,
    )


def upsert_offsite_entry(text: str, prefix: str, line: str) -> str:
    pat = rf'    "{prefix}": \([^)]+\),\n'
    if re.search(pat, text):
        return re.sub(pat, line, text, count=1)
    return text.replace(
        "\n}\n\nTYSON_PARTY_PREFIXES",
        "\n" + line + "\n}\n\nTYSON_PARTY_PREFIXES",
        1,
    )


def main() -> int:
    if not CATALOG.is_file():
        print(f"Missing {CATALOG}")
        return 2

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    studio_text = STUDIO_MANIFEST.read_text(encoding="utf-8")
    offsite_text = OFFSITE_MANIFEST.read_text(encoding="utf-8")
    studio_n = offsite_n = 0

    for prefix, meta in sorted(catalog.items()):
        title = meta["title"]
        alt = meta["alt"]
        if meta.get("scope") == "offsite":
            line = f'    "{prefix}": ({py_quote(title)}, {py_quote(alt)}),\n'
            offsite_text = upsert_offsite_entry(offsite_text, prefix, line)
            offsite_n += 1
        else:
            cat = infer_studio_category(title, alt)
            line = (
                f'    "{prefix}": (MediaCategory.{cat.name}, '
                f'{py_quote(title)}, {py_quote(alt)}),\n'
            )
            studio_text = upsert_entry(studio_text, prefix, line)
            studio_n += 1

    STUDIO_MANIFEST.write_text(studio_text, encoding="utf-8")
    OFFSITE_MANIFEST.write_text(offsite_text, encoding="utf-8")
    print(f"Applied {studio_n} studio + {offsite_n} offsite catalog entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

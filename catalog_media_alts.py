#!/usr/bin/env python3
"""Generate descriptive title + alt text for studio/offsite images via vision."""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from pathlib import Path

from woa_offsite_media_manifest import TYSON_KNOWN, offsite_manifest_items
from woa_studio_media_manifest import KNOWN, manifest_items

ROOT = Path(__file__).resolve().parent
ASSETS = Path("/Users/noone/.cursor/projects/Users-noone-Downloads-GitHub-workofarttattoo/assets")
OUT = ROOT / "woa_media_alt_catalog.json"

STUDIO_SUFFIX = " — Joshua Cole, Work of Art Las Vegas"
OFFSITE_SUFFIX = " — Joshua Cole offsite booking, Work of Art Las Vegas"


def find_asset(uuid_prefix: str) -> Path | None:
    for base in (ASSETS, ROOT / "studio_gallery", ROOT / "offsite_bookings"):
        if not base.is_dir():
            continue
        matches = sorted(base.glob(f"{uuid_prefix}*.png"))
        if matches:
            return matches[0]
        matches = sorted(base.glob(f"*{uuid_prefix[:8].lower()}*.png"))
        if matches:
            return matches[0]
    return None


def weak_known(prefix: str, title: str, alt: str) -> bool:
    weak = (
        "portfolio piece" in title.lower(),
        title.lower().startswith("original tattoo work"),
        title.lower() == "original illustration",
        title.lower() == "studio workspace",
        len(alt) < 40,
    )
    return any(weak)


def targets() -> list[tuple[str, str]]:
    """Return (uuid_prefix, scope) needing catalog entries."""
    out: list[tuple[str, str]] = []
    seen: set[str] = set()

    for item in manifest_items():
        if item.uuid_prefix in seen:
            continue
        seen.add(item.uuid_prefix)
        if item.uuid_prefix not in KNOWN or weak_known(item.uuid_prefix, item.title, item.alt):
            out.append((item.uuid_prefix, "studio"))

    for item in offsite_manifest_items():
        if item.uuid_prefix in seen:
            continue
        seen.add(item.uuid_prefix)
        if item.uuid_prefix not in TYSON_KNOWN:
            out.append((item.uuid_prefix, "offsite"))

    return out


def encode_image(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("ascii")


def describe_image(client, path: Path, scope: str) -> tuple[str, str]:
    from openai import OpenAI

    b64 = encode_image(path)
    context = (
        "Joshua Cole tattoo artist portfolio photo from Work of Art Tattoo Las Vegas."
        if scope == "studio"
        else "Joshua Cole mobile tattoo session at a private VIP offsite event (Party at Mike Tyson's House)."
    )
    prompt = f"""Describe this tattoo/piercing/studio photo for website accessibility alt text.

Context: {context}

Return JSON only:
{{"title": "Short caption (4-8 words, no quotes)", "alt": "One sentence describing what is visible — subject, style, placement if visible, action if in progress. No generic phrases like 'portfolio photo' or 'image 3'."}}

Rules:
- Be specific about tattoo subject (e.g. lion portrait, Norse sleeve, ear piercing).
- Mention black and grey, color, illustrative, realism when relevant.
- Do NOT include file names or numbers.
- alt must be under 130 characters."""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "low"},
                    },
                ],
            }
        ],
        max_tokens=200,
        temperature=0.2,
    )
    raw = resp.choices[0].message.content or "{}"
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    data = json.loads(raw)
    title = str(data.get("title", "")).strip().strip('"')
    alt = str(data.get("alt", "")).strip().strip('"')
    if not title:
        title = "Custom tattoo work"
    if not alt:
        alt = title
    suffix = STUDIO_SUFFIX if scope == "studio" else OFFSITE_SUFFIX
    if "work of art" not in alt.lower():
        alt = f"{alt.rstrip('.')}{suffix}"
    if len(alt) > 140:
        alt = alt[:137].rstrip(" ,—") + "…"
    return title, alt


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY required", file=sys.stderr)
        return 2

    existing: dict[str, dict[str, str]] = {}
    if OUT.is_file():
        existing = json.loads(OUT.read_text(encoding="utf-8"))

    from openai import OpenAI

    client = OpenAI()
    todo = targets()
    print(f"Cataloging {len(todo)} images…")

    for i, (prefix, scope) in enumerate(todo, 1):
        if prefix in existing and existing[prefix].get("title") and not existing[prefix].get("weak"):
            print(f"[{i}/{len(todo)}] skip {prefix} (cached)")
            continue
        path = find_asset(prefix)
        if not path:
            print(f"[{i}/{len(todo)}] missing asset {prefix}", file=sys.stderr)
            continue
        try:
            title, alt = describe_image(client, path, scope)
            existing[prefix] = {
                "scope": scope,
                "title": title,
                "alt": alt,
                "source": str(path.name),
            }
            print(f"[{i}/{len(todo)}] {prefix}: {title}")
        except Exception as exc:
            print(f"[{i}/{len(todo)}] error {prefix}: {exc}", file=sys.stderr)

    OUT.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(existing)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

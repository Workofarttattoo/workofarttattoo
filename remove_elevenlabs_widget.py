#!/usr/bin/env python3
"""Remove the retired ElevenLabs ConvAI call widget from generated HTML."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PATTERNS = (
    re.compile(
        r"\n?\s*<!--\s*ElevenLabs ConvAI Widget\s*-->\s*"
        r"<style[^>]*data-woa-convai-widget=[\"']1[\"'][^>]*>[\s\S]*?</style>\s*",
        re.I,
    ),
    re.compile(
        r"\n?\s*<style[^>]*data-woa-convai-widget=[\"']1[\"'][^>]*>[\s\S]*?</style>\s*",
        re.I,
    ),
    re.compile(
        r"\n?\s*<script[^>]+src=[\"'][^\"']*@elevenlabs/convai-widget-embed[^\"']*[\"'][^>]*></script>\s*",
        re.I,
    ),
    re.compile(r"\n?\s*<elevenlabs-convai\b[^>]*></elevenlabs-convai>\s*", re.I),
    re.compile(r"\n?\s*<!--\s*ElevenLabs ConvAI Widget\s*-->\s*", re.I),
)


def clean_html(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"elevenlabs|convai-widget|woa-convai-widget", html, re.I):
        return False
    cleaned = html
    for pattern in PATTERNS:
        cleaned = pattern.sub("\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if cleaned == html:
        raise SystemExit(f"ElevenLabs marker found but not removed in {path.relative_to(ROOT)}")
    path.write_text(cleaned, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if clean_html(path):
            print(f"[removed] {path.relative_to(ROOT)}")
            changed += 1
    print(f"[done] removed ElevenLabs widget from {changed} HTML file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

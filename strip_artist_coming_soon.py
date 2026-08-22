#!/usr/bin/env python3
"""Remove 'New Artist Coming Soon' placeholder cards and related copy from HTML exports."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = frozenset({"artists_raw", ".git", "__pycache__", "node_modules"})
SKIP_FILES = frozenset({"skipped_pages_clipboard.html"})

COMING_SOON = re.compile(
    r"new\s+artist[\s\S]{0,80}?coming\s+soon|coming\s+soon[\s\S]{0,40}?new\s+artist",
    re.IGNORECASE,
)

# Stitch-style artist tile (group link or plain div/article)
CARD_BLOCK = re.compile(
    r"<(?:a|article|div)\b[^>]*\bclass=\"[^\"]*(?:group\s+text-center|artist-card)[^\"]*\"[^>]*>"
    r"[\s\S]*?</(?:a|article|div)>",
    re.IGNORECASE,
)

TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    ("New Artist Coming Soon", ""),
    ("NEW ARTIST COMING SOON", ""),
    ("New artist coming soon", ""),
]


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES or "skipped_upload_build" in path.parts:
            continue
        out.append(path)
    return out


def strip_cards(text: str) -> tuple[str, int]:
    removed = 0
    for match in list(CARD_BLOCK.finditer(text)):
        block = match.group(0)
        if COMING_SOON.search(block):
            text = text.replace(block, "", 1)
            removed += 1
    return text, removed


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    text = original
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    text, n = strip_cards(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        if n:
            print(f"{path.relative_to(ROOT)} (removed {n} placeholder card(s))")
        else:
            print(f"{path.relative_to(ROOT)} (text cleanup)")
        return True
    return False


def main() -> None:
    changed = [p for p in iter_html_files() if process(p)]
    print(f"---\nUpdated {len(changed)} files")


if __name__ == "__main__":
    main()

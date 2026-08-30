#!/usr/bin/env python3
"""Fail if studio/offsite galleries contain generic alt text or placeholder filenames."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BAD_ALT_PATTERNS = (
    re.compile(r"Original tattoo work", re.I),
    re.compile(r"Realism portfolio piece", re.I),
    re.compile(r"Original illustration artwork", re.I),
    re.compile(r"Party session photo", re.I),
    re.compile(r"Offsite tattoo session at Party at Mike Tyson", re.I),
    re.compile(r"\b(image|photo)\s*\d+\b", re.I),
    re.compile(r"^Tattoo portfolio photo —", re.I),
)

BAD_FILE_PATTERNS = (
    "party-session-photo-",
    "original-tattoo-work-",
    "image",
)


def audit_html(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []
    for m in re.finditer(r'<img[^>]+alt="([^"]*)"[^>]*src="([^"]+)"', text):
        alt, src = m.group(1), m.group(2)
        if not alt.strip():
            issues.append(f"{path.name}: empty alt on {src}")
        for pat in BAD_ALT_PATTERNS:
            if pat.search(alt):
                issues.append(f"{path.name}: generic alt {alt[:60]!r}… on {src}")
        stem = Path(src).name.lower()
        for bad in BAD_FILE_PATTERNS:
            if bad in stem and re.search(rf"{bad}\d", stem):
                issues.append(f"{path.name}: placeholder filename {stem}")
    return issues


def main() -> int:
    issues: list[str] = []
    for slug in ("studio_gallery", "offsite_bookings"):
        code = ROOT / slug / "code.html"
        if code.is_file():
            issues.extend(audit_html(code))
        for img in (ROOT / slug).glob("*"):
            if img.suffix.lower() in {".png", ".webp"}:
                name = img.name.lower()
                if "party-session-photo-" in name or "original-tattoo-work-" in name:
                    issues.append(f"stale asset: {img}")

    if issues:
        for i in issues:
            print(f"[fail] {i}")
        return 1
    print("[ok] studio/offsite image alt audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

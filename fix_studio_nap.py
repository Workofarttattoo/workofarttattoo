#!/usr/bin/env python3
"""
Enforce one canonical NAP (name, address, phone) across static HTML exports.

Replaces Stitch placeholders, wrong numbers, and fake addresses with values
from woa_nav_config.py (GEO hub / GBP source of truth).

  python3 fix_studio_nap.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from woa_nav_config import (
    ROOT_A,
    ROOT_B,
    STUDIO_ADDRESS_HTML,
    STUDIO_ADDRESS_LOCALITY,
    STUDIO_ADDRESS_SINGLE_LINE,
    STUDIO_BOOKING_EMAIL,
    STUDIO_HOURS_HTML_GRID,
    STUDIO_PHONE_DISPLAY,
    STUDIO_PHONE_E164,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_SCHEMA,
    STUDIO_PHONE_TEL,
    STUDIO_POSTAL_CODE,
    STUDIO_STREET_ADDRESS,
)

SKIP_DIRS = frozenset({"artists_raw", ".git", "__pycache__", "node_modules"})
SKIP_FILES = frozenset({
    "skipped_pages_clipboard.html",
    "fix_studio_nap.py",
    "build_official_nap_page.py",
    "woa_nav_config.py",
    "woa_ai_crawl.py",
})
SKIP_PATH_PARTS = frozenset({"skipped_upload_build"})

# Literal wrong values seen in listings / Stitch exports (→ canonical)
TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    # Phones
    ("725-224-2931", STUDIO_PHONE_DISPLAY),
    ("(725) 224-2931", STUDIO_PHONE_PARENS),
    ("7252242931", STUDIO_PHONE_DISPLAY.replace("-", "")),
    ("tel:7252242931", STUDIO_PHONE_TEL),
    ("725-224-2617", STUDIO_PHONE_DISPLAY),
    ("(725) 224-2617", STUDIO_PHONE_PARENS),
    ("7252242617", STUDIO_PHONE_DISPLAY.replace("-", "")),
    ("tel:7252242617", STUDIO_PHONE_TEL),
    ("702-960-9607", STUDIO_PHONE_DISPLAY),
    ("(702) 960-9607", "(725) 224-1240"),
    ("7029609607", "7252241240"),
    ("tel:7029609607", STUDIO_PHONE_TEL),
    ("702-555-0199", STUDIO_PHONE_DISPLAY),
    ("(702) 555-0199", STUDIO_PHONE_PARENS),
    ("7025550199", "7252241240"),
    ("tel:7025550199", STUDIO_PHONE_TEL),
    # Normalize legacy tel: formats to E.164 href (display text unchanged)
    ("tel:725-224-1240", STUDIO_PHONE_TEL),
    ("tel:7252241240", STUDIO_PHONE_TEL),
    # Addresses (placeholders)
    (
        "1234 Art District Way, Suite 100<br/>Las Vegas, NV 89104",
        STUDIO_ADDRESS_HTML,
    ),
    (
        "1234 Art District Way, Suite 100, Las Vegas, NV 89104",
        STUDIO_ADDRESS_SINGLE_LINE,
    ),
    (
        "725 Art District Ln,<br/>Las Vegas, NV 89101",
        STUDIO_ADDRESS_HTML,
    ),
    ("725 Art District Ln", STUDIO_STREET_ADDRESS),
    (
        "Work of Art Tattoo & Piercing · 5025 E. Tropicana Ave, Las Vegas",
        f"Work of Art Tattoo & Piercing · {STUDIO_ADDRESS_SINGLE_LINE}",
    ),
    (
        "Work of Art Tattoo & Piercing at 5025 E. Tropicana Ave — minutes from the Strip",
        f"Work of Art Tattoo & Piercing at {STUDIO_STREET_ADDRESS} — minutes from the Strip",
    ),
    ("5025 E. Tropicana Ave, Las Vegas", f"{STUDIO_STREET_ADDRESS}, {STUDIO_ADDRESS_LOCALITY}"),
    ("5025 E. Tropicana Ave", STUDIO_STREET_ADDRESS),
    ("5025 E Tropicana", STUDIO_STREET_ADDRESS),
    ("5025 East Tropicana", STUDIO_STREET_ADDRESS),
    # Canonical 2375 — normalize casing, Ave, and missing city (GBP match)
    ("2375 E. Tropicana suite 3", STUDIO_STREET_ADDRESS),
    ("2375 E. Tropicana Suite 3, NV 89119", STUDIO_ADDRESS_SINGLE_LINE),
    ("2375 E. Tropicana suite 3, NV 89119", STUDIO_ADDRESS_SINGLE_LINE),
    ("2375 E. Tropicana suite 3 Las Vegas, NV 89119", STUDIO_ADDRESS_SINGLE_LINE),
    ("2375 E. Tropicana Ave Suite 3, Las Vegas, NV 89119", STUDIO_ADDRESS_SINGLE_LINE),
    ("2375 E. Tropicana Ave Suite 3", STUDIO_STREET_ADDRESS),
    ("2375 E. Tropicana Ave #3, Las Vegas, NV 89119", STUDIO_ADDRESS_SINGLE_LINE),
    ("2375 E. Tropicana Ave #3", STUDIO_STREET_ADDRESS),
    ("2375 E Tropicana Ave #3", STUDIO_STREET_ADDRESS),
    (
        "Directions to Work of Art at 2375 E. Tropicana Ave",
        f"Directions to Work of Art at {STUDIO_STREET_ADDRESS}",
    ),
    ("2375 E. Tropicana Ave", STUDIO_STREET_ADDRESS),
    (
        "Located at 2375 E. Tropicana, we offer",
        f"Located at {STUDIO_STREET_ADDRESS}, we offer",
    ),
    (
        "2375 E. Tropicana suite 3, NV 89119<br/>Serving Henderson",
        f"{STUDIO_ADDRESS_SINGLE_LINE}<br/>Serving Henderson",
    ),
    ('"postalCode": "89101"', f'"postalCode": "{STUDIO_POSTAL_CODE}"'),
    # Wrong hours block (geo SEO page)
    (
        '<div class="grid grid-cols-2 gap-4">\n'
        '<p class="text-on-surface-variant">MON - SAT</p>\n'
        "<p>12:00 PM - 10:00 PM</p>\n"
        '<p class="text-on-surface-variant">SUNDAY</p>\n'
        "<p>12:00 PM - 08:00 PM</p>\n"
        "</div>",
        STUDIO_HOURS_HTML_GRID,
    ),
]

PHONE_IN_TEXT = re.compile(
    r"(?<!\d)"  # not preceded by digit
    r"(?:\+1[-.\s]?)?(?:\(?725\)?[-.\s]?224[-.\s]?|702[-.\s]?)"
    r"(\d{4})"
    r"(?!\d)",
    re.IGNORECASE,
)


def site_roots() -> list[Path]:
    roots: list[Path] = []
    for base in (ROOT_A, ROOT_B):
        if base.is_dir():
            roots.append(base)
    return roots


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if any(part in SKIP_PATH_PARTS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() not in {".html", ".md", ".txt", ".py"}:
            continue
        out.append(path)
    return out


def replace_phones_regex(text: str) -> str:
    """Catch remaining 725-224-XXXX / 702-XXX-XXXX except canonical last4."""

    def sub(match: re.Match[str]) -> str:
        last4 = match.group(1)
        if last4 == "1240":
            return match.group(0)
        return STUDIO_PHONE_DISPLAY

    return PHONE_IN_TEXT.sub(sub, text)


def normalize_schema_telephone(text: str) -> str:
    if '"telephone"' not in text:
        return text

    def repl_ld_json(match: re.Match[str]) -> str:
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)

        def walk(obj: object) -> None:
            if isinstance(obj, dict):
                if "telephone" in obj and obj["telephone"] != STUDIO_PHONE_SCHEMA:
                    obj["telephone"] = STUDIO_PHONE_SCHEMA
                if "streetAddress" in obj and "Art District" in str(obj["streetAddress"]):
                    obj["streetAddress"] = STUDIO_STREET_ADDRESS
                if "streetAddress" in obj and "5025" in str(obj["streetAddress"]):
                    obj["streetAddress"] = STUDIO_STREET_ADDRESS
                if "streetAddress" in obj and "suite 3" in str(obj["streetAddress"]).lower():
                    obj["streetAddress"] = STUDIO_STREET_ADDRESS
                if "postalCode" in obj and obj["postalCode"] in ("89101", "89104"):
                    obj["postalCode"] = STUDIO_POSTAL_CODE
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)

        walk(data)
        return (
            '<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False)
            + "\n    </script>"
        )

    return re.sub(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        repl_ld_json,
        text,
        flags=re.DOTALL,
    )


def walk_in_footer_phone(text: str) -> str:
    """Walk-in page: plain <p> placeholder → linked canonical phone."""
    old = '<p class="font-body-md text-on-surface-variant">(702) 555-0199</p>'
    if old not in text or STUDIO_PHONE_TEL in text:
        return text
    new = (
        f'<a class="font-body-md text-on-surface-variant hover:text-primary transition-colors" '
        f'href="{STUDIO_PHONE_TEL}">{STUDIO_PHONE_PARENS}</a>'
    )
    return text.replace(old, new)


def geo_footer_phone_li(text: str) -> str:
    old = f"<li>702-555-0199</li>"
    if old not in text:
        return text
    new = (
        f'<li><a class="hover:text-primary transition-colors" href="{STUDIO_PHONE_TEL}">'
        f"{STUDIO_PHONE_DISPLAY}</a></li>"
    )
    return text.replace(old, new)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)

    text = replace_phones_regex(text)

    if path.suffix.lower() == ".html":
        text = normalize_schema_telephone(text)
        text = walk_in_footer_phone(text)
        text = geo_footer_phone_li(text)

    if path.name == "ai.txt" and "Contact:" in text:
        line = (
            f"Contact: {STUDIO_PHONE_DISPLAY} | {STUDIO_BOOKING_EMAIL} | "
            f"{STUDIO_ADDRESS_SINGLE_LINE}"
        )
        text = re.sub(r"^Contact:.*$", line, text, count=1, flags=re.MULTILINE)

    if path.name == "index.html.md" and "**Phone:**" in text:
        text = re.sub(
            r"\*\*Phone:\*\*[^\n]+",
            f"**Phone:** {STUDIO_PHONE_DISPLAY}",
            text,
            count=1,
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def audit_nap(root: Path) -> list[str]:
    """Return relative paths that still contain wrong address strings."""
    bad_patterns = ("5025", "2375 E. Tropicana suite 3")
    issues: list[str] = []
    for path in iter_files(root):
        if path.suffix.lower() != ".html":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in bad_patterns:
            if needle in text:
                rel = str(path.relative_to(root))
                issues.append(f"{rel}: contains {needle!r}")
                break
    return issues


def main() -> int:
    changed: list[str] = []
    for root in site_roots():
        for path in iter_files(root):
            if process_file(path):
                changed.append(str(path.relative_to(root)))
    if changed:
        print(f"NAP fixed in {len(changed)} file(s):")
        for rel in changed:
            print(f"  {rel}")
    else:
        print("NAP already consistent.")

    issues: list[str] = []
    for root in site_roots():
        issues.extend(audit_nap(root))
    if issues:
        print(f"\nNAP audit — {len(issues)} issue(s) remain:")
        for line in issues[:30]:
            print(f"  {line}")
        if len(issues) > 30:
            print(f"  … and {len(issues) - 30} more")
        return 1
    print("NAP audit: OK (no 5025 or non-canonical 2375 variants in HTML).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

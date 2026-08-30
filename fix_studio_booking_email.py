#!/usr/bin/env python3
"""
Standardize studio contact email from siteData/business.json sitewide.

- Replaces legacy booking/info addresses in HTML and Markdown
- Adds schema.org email on LocalBusiness / TattooParlor blocks when missing
- Injects footer mailto links labeled "Email us!" (not the raw address)
- Keeps mailto href on thewhiteknight702@gmail.com

  python3 fix_studio_booking_email.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from woa_nav_config import (
    HREF_BOOKING_MAILTO,
    ROOT_A,
    ROOT_B,
    STUDIO_BOOKING_EMAIL,
    STUDIO_BOOKING_LINK_LABEL,
)

SKIP_DIRS = frozenset({"artists_raw", ".git", "__pycache__", "node_modules", "tools"})
SKIP_FILES = frozenset(
    {
        "skipped_pages_clipboard.html",
        "fix_studio_booking_email.py",
    }
)
SKIP_PATH_PARTS = frozenset({"skipped_upload_build"})

LEGACY_EMAIL_PATTERNS = [
    re.compile(r"booking@workofarttattoo\.com", re.IGNORECASE),
    re.compile(r"thewhiteknight702@gmail\.com", re.IGNORECASE),
]

BOOKING_MARKER = HREF_BOOKING_MAILTO

FOOTER_EMAIL_LI = (
    f'<li class=""><a class="hover:text-secondary transition-colors" '
    f'href="{HREF_BOOKING_MAILTO}">{STUDIO_BOOKING_LINK_LABEL}</a></li>\n'
)

FOOTER_EMAIL_NAV = (
    f'<a class="font-body-md text-on-surface-variant hover:text-secondary '
    f'hover:underline decoration-secondary transition-all" '
    f'href="{HREF_BOOKING_MAILTO}">{STUDIO_BOOKING_LINK_LABEL}</a>\n'
)

GEO_NAP_EMAIL_BLOCK = (
    f'<a class="font-body-lg text-body-lg text-on-surface hover:text-secondary block mt-3" '
    f'href="{HREF_BOOKING_MAILTO}">{STUDIO_BOOKING_LINK_LABEL}</a>\n'
    f'<div class="font-body-md text-body-md text-on-surface-variant">Booking &amp; consult inbox</div>\n'
)

VISIBLE_MAILTO_EMAIL = re.compile(
    r'(<a\b[^>]*href="mailto:[^"]+"[^>]*>)([^<]*@[^<]*)(</a>)',
    re.IGNORECASE,
)

FORMSUBMIT_LEGACY = re.compile(
    r"https://formsubmit\.co/booking@workofarttattoo\.com",
    re.IGNORECASE,
)


def site_roots() -> list[Path]:
    roots: list[Path] = []
    for base in (ROOT_A, ROOT_B):
        if base.is_dir():
            roots.append(base)
    return roots


def iter_text_files(root: Path) -> list[Path]:
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
        if path.suffix.lower() not in {".html", ".md", ".txt"}:
            continue
        out.append(path)
    return out


def replace_legacy_emails(text: str) -> str:
    for pat in LEGACY_EMAIL_PATTERNS:
        text = pat.sub(STUDIO_BOOKING_EMAIL, text)
    text = FORMSUBMIT_LEGACY.sub(f"https://formsubmit.co/{STUDIO_BOOKING_EMAIL}", text)
    return text


def humanize_visible_email_links(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{STUDIO_BOOKING_LINK_LABEL}{match.group(3)}"

    return VISIBLE_MAILTO_EMAIL.sub(repl, text)


def soften_form_confirmation_copy(text: str) -> str:
    return text.replace(
        f"your request was sent to {STUDIO_BOOKING_EMAIL}. We will reply shortly.",
        "your request was sent. We will reply shortly.",
    ).replace(
        f"your request was sent to booking@workofarttattoo.com. We will reply shortly.",
        "your request was sent. We will reply shortly.",
    )


def inject_schema_email(text: str) -> str:
    if '"email"' in text and STUDIO_BOOKING_EMAIL in text:
        return text

    def repl_ld_json(match: re.Match[str]) -> str:
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)

        def walk(obj: object) -> None:
            if isinstance(obj, dict):
                t = obj.get("@type")
                if t in (
                    "LocalBusiness",
                    "TattooParlor",
                    "TattooShop",
                    "HealthAndBeautyBusiness",
                ):
                    if "email" not in obj:
                        obj["email"] = STUDIO_BOOKING_EMAIL
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


def inject_footer_contact_email(text: str) -> str:
    if BOOKING_MARKER in text:
        return text

    phone_li = re.compile(
        r'(<li class=""><a class="hover:text-secondary transition-colors" '
        r'href="tel:+17252241240">\(725\) 224-1240</a></li>\n)',
        re.IGNORECASE,
    )
    if phone_li.search(text):
        return phone_li.sub(r"\1" + FOOTER_EMAIL_LI, text, count=1)

    call_nav = re.compile(
        r'(<a class="font-body-md text-on-surface-variant hover:text-secondary '
        r'hover:underline decoration-secondary transition-all" '
        r'href="tel:+17252241240">Call \(725\) 224-1240</a>\n)',
        re.IGNORECASE,
    )
    if call_nav.search(text):
        return call_nav.sub(r"\1" + FOOTER_EMAIL_NAV, text, count=1)

    book_footer = re.compile(
        r'(<a class="font-body-md text-on-surface-variant hover:text-secondary '
        r'transition-colors" href="tel:+17252241240">\(725\) 224-1240</a>\n)(</div>)',
        re.IGNORECASE,
    )
    if book_footer.search(text):
        email_a = (
            f'<a class="font-body-md text-on-surface-variant hover:text-secondary '
            f'transition-colors" href="{HREF_BOOKING_MAILTO}">{STUDIO_BOOKING_LINK_LABEL}</a>\n'
        )
        return book_footer.sub(r"\1" + email_a + r"\2", text, count=1)

    return text


def inject_geo_hub_nap(text: str, path: Path) -> str:
    if path.parent.name != "geo_hub_ai_source_of_truth_work_of_art":
        return text
    if BOOKING_MARKER in text:
        return text
    needle = (
        '<div class="font-body-md text-body-md text-on-surface-variant">'
        "Direct Studio Line</div>\n"
    )
    if needle in text:
        return text.replace(needle, needle + GEO_NAP_EMAIL_BLOCK, 1)
    return text


def patch_markdown_geo(text: str, path: Path) -> str:
    if path.name != "index.html.md":
        return text
    if f"**Email:** {STUDIO_BOOKING_LINK_LABEL}" in text:
        return text
    if "**Phone:**" in text and "**Email:**" not in text:
        return text.replace(
            "**Phone:** (725) 224-1240\n",
            f"**Phone:** (725) 224-1240\n- **Email:** [{STUDIO_BOOKING_LINK_LABEL}]({HREF_BOOKING_MAILTO})\n",
            1,
        )
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    text = replace_legacy_emails(text)
    text = soften_form_confirmation_copy(text)
    if path.suffix.lower() == ".html":
        text = inject_schema_email(text)
        text = inject_footer_contact_email(text)
        text = inject_geo_hub_nap(text, path)
        text = humanize_visible_email_links(text)
    text = patch_markdown_geo(text, path)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    for root in site_roots():
        for path in iter_text_files(root):
            if process_file(path):
                changed.append(str(path.relative_to(root)))
    if not changed:
        print("No email changes needed.")
        return 0
    print(f"Updated {len(changed)} file(s):")
    for rel in changed:
        print(f"  {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

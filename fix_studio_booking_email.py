#!/usr/bin/env python3
"""
Hide public mailbox addresses and point FormSubmit at the booking recipient.

- Form actions and ajax URLs post to the booking recipient
- Visible contact becomes an obfuscated "Email us now" link
- JSON-LD email properties are removed
- Does not publish the recipient as page copy

  python3 fix_studio_booking_email.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from woa_email_link import apply_public_email_policy, email_us_anchor, write_email_script
from woa_nav_config import (
    ROOT_A,
    ROOT_B,
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
    re.compile(r"thewhiteknight702@gmail\.com", re.IGNORECASE),
    re.compile(r"kmorgen14@gmail\.com", re.IGNORECASE),
]

BOOKING_MARKER = "data-woa-email-us"

FOOTER_EMAIL_LI = (
    '<li class="">'
    + email_us_anchor("hover:text-secondary transition-colors")
    + "</li>\n"
)

FOOTER_EMAIL_NAV = (
    email_us_anchor(
        "font-body-md text-on-surface-variant hover:text-secondary "
        "hover:underline decoration-secondary transition-all"
    )
    + "\n"
)

GEO_NAP_EMAIL_BLOCK = (
    email_us_anchor("font-body-lg text-body-lg text-on-surface hover:text-secondary block mt-3")
    + "\n"
    + '<div class="font-body-md text-body-md text-on-surface-variant">Booking &amp; consult inbox</div>\n'
)

VISIBLE_MAILTO_EMAIL = re.compile(
    r'(<a\b[^>]*href="mailto:[^"]+"[^>]*>)([^<]*@[^<]*)(</a>)',
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
    """Keep the import used by page builders. Policy hides addresses and fixes FormSubmit."""
    return apply_public_email_policy(text)


def humanize_visible_email_links(text: str) -> str:
    return apply_public_email_policy(text)


def soften_form_confirmation_copy(text: str) -> str:
    return text.replace(
        "your request was sent to " + STUDIO_BOOKING_LINK_LABEL + ". We will reply shortly.",
        "your request was sent. We will reply shortly.",
    )


def inject_schema_email(text: str) -> str:
    """Schema must not publish a mailbox. Strip it instead of inserting one."""
    return apply_public_email_policy(text)


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
            email_us_anchor(
                "font-body-md text-on-surface-variant hover:text-secondary transition-colors"
            )
            + "\n"
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
            "**Phone:** (725) 224-1240\n- **Email:** [Email us now](https://www.workofarttattoo.com/appointments/)\n",
            1,
        )
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    if path.suffix.lower() == ".html":
        text = apply_public_email_policy(text)
        text = inject_footer_contact_email(text)
        text = inject_geo_hub_nap(text, path)
        text = apply_public_email_policy(text)
    text = patch_markdown_geo(text, path)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    write_email_script(ROOT_A)
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

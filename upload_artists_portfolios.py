#!/usr/bin/env python3
"""
Fix Stitch-export HTML artifacts (empty <head>, ```html fences) and upload artist pages.

Deploys:
  artists/katelyn-cole/index.html
  artists/joshua-cole/index.html

Requires: FTP_USER, FTP_PASS
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from ftplib import FTP, error_perm
from io import BytesIO
from pathlib import Path

HOST = "ftp.workofarttattoo.com"
KATELYN_BOOKING_URL = "https://jim.com/a/katelyn-delano-rose-morg"


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def strip_leading_section_comment(s: str) -> str:
    return re.sub(r"^<!--[^>]*?-->\s*", "", s.strip(), count=1, flags=re.DOTALL)


def strip_markdown_fences(s: str) -> str:
    s = re.sub(r"```html\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"```\s*", "", s)
    return s


def fix_html(doc: str, body_start_anchor: str) -> str:
    """Move orphan head-ish tags from after <body open> until anchor into real <head>."""
    doc = strip_leading_section_comment(doc)
    doc = strip_markdown_fences(doc)

    m = re.search(
        r"(<!DOCTYPE\s+[^>]+>)?\s*<html([^>]*)>\s*<head></head>\s*<body([^>]*)>\s*",
        doc,
        re.IGNORECASE | re.DOTALL,
    )
    if not m:
        raise ValueError("Expected Stitch pattern: <!DOCTYPE>? <html ...><head></head><body ...>.")

    doctype_line = "<!DOCTYPE html>"
    if m.group(1):
        doctype_line = m.group(1).strip()

    html_attrs = (m.group(2) or "").strip()
    body_attrs = (m.group(3) or "").strip()
    suffix = doc[m.end() :]

    idx = suffix.find(body_start_anchor)
    if idx == -1:
        raise ValueError(f"Anchor not found for body split: {body_start_anchor[:60]!r}")

    orphaned_head_bits = suffix[:idx].strip()
    body_markup = suffix[idx:]

    html_attr_str = f" {html_attrs}" if html_attrs else ""
    body_attr_str = f" {body_attrs}" if body_attrs else ""

    return (
        f"{doctype_line}\n"
        f"<html{html_attr_str}>\n"
        f"<head>\n{orphaned_head_bits}\n</head>\n"
        f"<body{body_attr_str}>\n{body_markup}\n</body>\n"
        "</html>\n"
    )


def extract_first_document_blob(block: str) -> str:
    """If two HTML docs pasted back-to-back, keep the first ending at first </html>."""
    low = block.lower()
    idx = low.find("</html>")
    if idx == -1:
        return block
    return block[: idx + len("</html>")]


def inject_katelyn_booking(html: str) -> str:
    """Give Katelyn's page direct booking CTAs plus a pricing/availability panel.

    Exact service and jewelry prices are maintained by Katelyn in her Jim booking
    profile, so the site links to that live source instead of duplicating prices
    that can become stale.
    """
    booking_attrs = (
        f'href="{KATELYN_BOOKING_URL}" target="_blank" '
        'rel="noopener noreferrer"'
    )

    # Convert the two original non-functional booking buttons into real links.
    html = re.sub(
        r'<button class="([^"]*bg-secondary[^"]*)">Book Katelyn</button>',
        rf'<a class="\1" {booking_attrs}>Book Katelyn</a>',
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r'<button class="([^"]*bg-secondary[^"]*)">Book Katelyn Cole</button>',
        rf'<a class="\1" {booking_attrs}>Book Katelyn Cole</a>',
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    marker = "<!-- Specialties Section -->"
    if "data-woa-katelyn-pricing" not in html and marker in html:
        pricing = f'''\n<section class="py-12 md:py-16 px-margin-desktop bg-surface-container border-b border-outline-variant/10" data-woa-katelyn-pricing="1" id="katelyn-pricing">
<div class="max-w-4xl mx-auto text-center space-y-6">
<span class="text-label-caps font-label-caps text-secondary block uppercase tracking-[0.3em]">Pricing &amp; Direct Booking</span>
<h2 class="text-headline-lg font-headline-lg text-on-surface">See Katelyn's Current Piercing Prices</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant max-w-3xl mx-auto">Katelyn keeps her current service pricing, appointment availability, and booking options on her direct booking page. Jewelry pricing can vary by material, style, and piece selected, so the booking page is the live source for current totals.</p>
<div class="flex flex-wrap justify-center gap-4 pt-2">
<a class="bg-secondary text-on-secondary px-10 py-4 text-label-caps font-label-caps uppercase gold-glow" {booking_attrs}>View Piercing Prices &amp; Book Katelyn</a>
<a class="border border-outline-variant text-on-surface px-10 py-4 text-label-caps font-label-caps uppercase hover:bg-surface-variant transition-colors" href="tel:+17252241240">Call the Studio</a>
</div>
<p class="text-sm text-on-surface-variant">For the most accurate price, choose the piercing service on Katelyn's booking page; jewelry upgrades are priced separately when applicable.</p>
</div>
</section>\n'''
        html = html.replace(marker, pricing + marker, 1)

    return html


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("katelyn_file", type=Path, help="Raw Katelyn HTML file from Stitch")
    ap.add_argument("joshua_file", type=Path, help="Raw Joshua HTML file from Stitch")
    args = ap.parse_args()

    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS (e.g. tattoojosh@workofarttattoo.com).", file=sys.stderr)
        return 1

    kt_raw = args.katelyn_file.read_text(encoding="utf-8", errors="strict")
    jc_raw = args.joshua_file.read_text(encoding="utf-8", errors="strict")

    kt_html = fix_html(
        extract_first_document_blob(kt_raw),
        '<header class="fixed top-0 left-0 w-full z-50 flex justify-between',
    )
    kt_html = inject_katelyn_booking(kt_html)
    jc_html = fix_html(
        extract_first_document_blob(jc_raw),
        "<!-- Sparkle Cursor Implementation -->",
    )

    ftp = FTP(HOST, timeout=120)
    ftp.login(user, pw)
    ftp.set_pasv(True)

    for rel, data in (
        ("artists/katelyn-cole/index.html", kt_html.encode("utf-8")),
        ("artists/joshua-cole/index.html", jc_html.encode("utf-8")),
    ):
        ftp_mkdir_p(ftp, str(Path(rel).parent))
        print(f"[up] /{rel} ({len(data)} bytes)")
        bio = BytesIO(data)
        ftp.storbinary(f"STOR {Path(rel).name}", bio)

    ftp.quit()
    print("Done.")
    print("https://workofarttattoo.com/artists/katelyn-cole/")
    print("https://workofarttattoo.com/artists/joshua-cole/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

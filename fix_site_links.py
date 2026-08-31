#!/usr/bin/env python3
"""Repair broken CTAs and placeholder hrefs across deployed HTML."""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

from woa_nav_config import HREF_APPOINTMENTS, ROOT_A

ROOT = ROOT_A
SKIP_DIRS = frozenset(
    {
        "artists_raw",
        ".git",
        "__pycache__",
        "node_modules",
    }
)
SKIP_FILES = frozenset({"skipped_pages_clipboard.html"})

BOOK_RE = re.compile(
    r"^(book\s*(now|appointment)|schedule\s*consultation|book\s*a\s*consultation|"
    r"book\s+(your\s+)?consultation|book\s+my\s+piercing|book\s+\w+)$",
    re.I,
)
PORTFOLIO_RE = re.compile(
    r"^(view\s+artist\s+portfolios?|explore\s+gallery|view\s+portfolios?|artist\s+portfolios?)$",
    re.I,
)
REVIEW_RE = re.compile(r"review\s+us\s+on\s+google", re.I)

PLACEHOLDER_HREF = re.compile(r"\{\{DATA:SCREEN:[^}]+\}\}")

# (link text regex, href) for anchors still on href="#"
HASH_TEXT_HREFS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"book\s*appointment", re.I), HREF_APPOINTMENTS),
    (re.compile(r"^book\s*now$", re.I), HREF_APPOINTMENTS),
    (re.compile(r"schedule\s*consultation", re.I), HREF_APPOINTMENTS),
    (re.compile(r"meet\s+(the\s+)?artists?", re.I), "/#gallery"),
    (re.compile(r"^artists$", re.I), "/artists/"),
    (re.compile(r"fine\s*art\s*portfolio", re.I), "/#gallery"),
    (re.compile(r"explore\s*gallery", re.I), "/#gallery"),
    (re.compile(r"view\s+artist\s+portfolios?", re.I), "/#meet-our-artists"),
    (re.compile(r"^reviews?$", re.I), "/reviews/"),
    (re.compile(r"leave\s+a\s+google\s+review", re.I), "/leave-a-review/"),
    (re.compile(r"review\s+us\s+on\s+google", re.I), "/leave-a-review/"),
    (re.compile(r"^piercing$", re.I), "/piercing-shop-standards/"),
    (re.compile(r"^merchandise$", re.I), "/merchandise/"),
    (re.compile(r"^appointments?$", re.I), HREF_APPOINTMENTS),
    (re.compile(r"privacy\s*policy", re.I), "/privacy-policy/"),
    (re.compile(r"terms\s*of\s*service", re.I), "/terms-of-service/"),
    (re.compile(r"studio\s*rules", re.I), "/studio-rules/"),
    (re.compile(r"^safety$", re.I), "/#faq"),
    (re.compile(r"view\s+full\s+gallery", re.I), "/#gallery"),
    (re.compile(r"black\s*&\s*grey\s*realism", re.I), "/realism-tattoos-las-vegas/"),
    (re.compile(r"color\s*realism", re.I), "/realism-tattoos-las-vegas/"),
    (re.compile(r"fine\s*line\s*tattoos?", re.I), "/fine_line_tattoos_las_vegas_master_authority_guide/"),
    (re.compile(r"neo-?traditional", re.I), "/best_tattoo_styles_for_sleeves_large_scale_project_hub/"),
    (re.compile(r"cover-?up", re.I), "/cover-up-tattoos-las-vegas/"),
    (re.compile(r"ear\s*piercing", re.I), "/ear_piercing_guide_las_vegas/"),
    (re.compile(r"facial\s*piercing", re.I), "/facial_piercing_guide_las_vegas/"),
    (re.compile(r"body\s*piercing", re.I), "/body_piercing_guide_las_vegas/"),
    (re.compile(r"jewelry\s*upgrade", re.I), "/piercing_jewelry_guide_las_vegas/"),
    (re.compile(r"aftercare\s*guide", re.I), "/piercing_aftercare_guide_las_vegas/"),
    (re.compile(r"studio\s*tour", re.I), "/studio_gallery/"),
    (re.compile(r"gift\s*cards?", re.I), "/appointments/"),
    (re.compile(r"get\s*directions", re.I), "/official_location_hours_contact/"),
]


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if "skipped_upload_build" in path.parts:
            continue
        out.append(path)
    return out


def process_file(path: Path) -> dict[str, int]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    original = raw

    raw = PLACEHOLDER_HREF.sub("/#gallery", raw)
    raw = raw.replace("{{DATA:SCREEN:SCREEN_133}}", "/#gallery")
    raw = raw.replace('href="#appointments"', f'href="{HREF_APPOINTMENTS}"')

    soup = BeautifulSoup(raw, "html.parser")
    stats = {
        "buttons_to_links": 0,
        "hash_links_fixed": 0,
        "placeholder_hrefs": 0,
    }

    for btn in list(soup.find_all("button")):
        if btn.get("data-mobile-nav-toggle") or btn.get("aria-controls"):
            continue
        if btn.get("type") == "submit":
            continue
        onclick = btn.get("onclick") or ""
        if onclick and "scroll" in onclick.lower():
            pass  # still convert header BOOK NOW to real appointments URL
        elif onclick:
            continue
        text = " ".join(btn.get_text(strip=True).split())
        text = re.sub(r"\s+material-symbols[^\s]*", "", text, flags=re.I).strip()
        if not text:
            continue
        href = None
        if BOOK_RE.match(text) or re.search(
            r"book\s+(now|appointment|your\s+consultation|my\s+piercing)|schedule\s*consultation",
            text,
            re.I,
        ):
            href = HREF_APPOINTMENTS
        elif PORTFOLIO_RE.match(text):
            href = "/#meet-our-artists"
        elif REVIEW_RE.search(text):
            href = "/review_funnel_google_authority_hub/"
        if not href:
            continue

        a = soup.new_tag("a", href=href)
        for k, v in btn.attrs.items():
            if k in ("type", "onclick"):
                continue
            a[k] = v
        a.extend(btn.contents)
        btn.replace_with(a)
        stats["buttons_to_links"] += 1

    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if PLACEHOLDER_HREF.search(href):
            a["href"] = "/#gallery"
            stats["placeholder_hrefs"] += 1
            continue
        if href != "#":
            continue
        text = " ".join(a.get_text(strip=True).split())
        for pat, target in HASH_TEXT_HREFS:
            if pat.search(text):
                a["href"] = target
                stats["hash_links_fixed"] += 1
                break
        else:
            if BOOK_RE.match(text) or re.search(r"book\s*appointment", text, re.I):
                a["href"] = HREF_APPOINTMENTS
                stats["hash_links_fixed"] += 1
            elif PORTFOLIO_RE.match(text):
                a["href"] = "/#meet-our-artists"
                stats["hash_links_fixed"] += 1

    out = str(soup)
    if out != original:
        path.write_text(out, encoding="utf-8")
    return stats


def main() -> None:
    totals = {"files": 0, "buttons_to_links": 0, "hash_links_fixed": 0, "placeholder_hrefs": 0}
    for path in iter_html_files():
        stats = process_file(path)
        if any(stats.values()):
            totals["files"] += 1
            for k in ("buttons_to_links", "hash_links_fixed", "placeholder_hrefs"):
                totals[k] += stats[k]
            print(f"{path.relative_to(ROOT)}: {stats}")
    print("---")
    print(f"Updated {totals['files']} files")
    print(
        f"  buttons→links: {totals['buttons_to_links']}, "
        f"hash fixes: {totals['hash_links_fixed']}, "
        f"placeholders: {totals['placeholder_hrefs']}"
    )


if __name__ == "__main__":
    main()

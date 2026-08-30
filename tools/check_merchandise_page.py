#!/usr/bin/env python3
"""Pre-commit QA for /merchandise/ — links, assets, and inquiry CTAs."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_merchandise_manifest import SLUG
from woa_nav_config import MERCH_HREF, STUDIO_BOOKING_EMAIL

MERCH_DIR = ROOT / SLUG
CODE_HTML = MERCH_DIR / "code.html"
INDEX_HTML = MERCH_DIR / "index.html"
CANONICAL = "https://www.workofarttattoo.com/merchandise/"

BANNED_HREF = re.compile(
    r"(?:^|/)(?:cart|account|checkout|shop|my-account)(?:/|$)",
    re.IGNORECASE,
)
BANNED_TEXT = re.compile(
    r"\b(?:add to cart|buy now|checkout|view cart|my account)\b",
    re.IGNORECASE,
)
ECOMMERCE_HOST = re.compile(
    r"(?:shopify|woocommerce|square\.site|bigcartel)",
    re.IGNORECASE,
)


def route_exists(href: str) -> bool:
    if not href or href.startswith(("#", "mailto:", "tel:", "sms:", "javascript:")):
        return True
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        return True
    path = parsed.path or href
    if not path.startswith("/"):
        return (ROOT / path).exists()
    rel = path.strip("/")
    if not rel:
        return CODE_HTML.is_file() or (ROOT / "home_work_of_art_tattoo_piercing" / "code.html").is_file()
    candidates = [
        ROOT / rel / "code.html",
        ROOT / rel / "index.html",
        ROOT / f"{rel}.html",
    ]
    if any(p.is_file() for p in candidates):
        return True
    return (ROOT / rel).exists()


def asset_exists(src: str) -> bool:
    if not src or src.startswith(("http://", "https://", "data:")):
        return True
    path = src.lstrip("/")
    return (ROOT / path).is_file()


def check_page(html_path: Path) -> list[str]:
    failures: list[str] = []
    text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    canonical = soup.find("link", rel="canonical")
    if not canonical or canonical.get("href") != CANONICAL:
        failures.append(f"{html_path.name}: canonical must be {CANONICAL}")

    if STUDIO_BOOKING_EMAIL not in text:
        failures.append(f"{html_path.name}: missing inquiry email {STUDIO_BOOKING_EMAIL}")

    if "thewhiteknight702@gmail.com" in text.lower():
        failures.append(f"{html_path.name}: legacy personal Gmail still present")

    for tag in soup.find_all(["a", "link", "script", "img", "source"]):
        for attr in ("href", "src", "srcset"):
            raw = tag.get(attr)
            if not raw:
                continue
            for part in raw.split(","):
                href = part.strip().split()[0] if part.strip() else ""
                if not href:
                    continue
                if BANNED_HREF.search(href) or ECOMMERCE_HOST.search(href):
                    failures.append(f"{html_path.name}: banned ecommerce link {href!r}")
                if href.startswith("/") and not asset_exists(href) and not route_exists(href):
                    failures.append(f"{html_path.name}: broken local target {href!r}")

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not asset_exists(src):
            failures.append(f"{html_path.name}: missing image {src!r}")

    for source in soup.find_all("source"):
        srcset = source.get("srcset", "")
        for part in srcset.split(","):
            href = part.strip().split()[0] if part.strip() else ""
            if href and not asset_exists(href):
                failures.append(f"{html_path.name}: missing source image {href!r}")

    visible = soup.get_text(" ", strip=True)
    if BANNED_TEXT.search(visible):
        failures.append(f"{html_path.name}: stale ecommerce UI copy detected")

    if "legacy shop" in visible.lower():
        failures.append(f"{html_path.name}: references legacy shop")

    mailtos = [
        a.get("href", "")
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("mailto:")
    ]
    if not mailtos:
        failures.append(f"{html_path.name}: no mailto inquiry CTA")
    elif not any(STUDIO_BOOKING_EMAIL in href for href in mailtos):
        failures.append(f"{html_path.name}: mailto links do not use {STUDIO_BOOKING_EMAIL}")

    return failures


def main() -> int:
    failures: list[str] = []

    if not CODE_HTML.is_file():
        failures.append(f"missing source page: {CODE_HTML.relative_to(ROOT)}")
        report(failures)
        return 1

    shutil.copy2(CODE_HTML, INDEX_HTML)

    for path in (CODE_HTML, INDEX_HTML):
        failures.extend(check_page(path))

    if MERCH_HREF != "/merchandise/":
        failures.append(f"MERCH_HREF drift: expected /merchandise/, got {MERCH_HREF}")

    report(failures)
    return 1 if failures else 0


def report(failures: list[str]) -> None:
    if failures:
        print("[merchandise QA] FAILED")
        for item in failures:
            print(f"  - {item}")
        return
    print("[merchandise QA] OK — code.html, index.html, assets, and inquiry CTAs verified")


if __name__ == "__main__":
    raise SystemExit(main())

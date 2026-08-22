#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import csv
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(p for p in ROOT.rglob("code.html") if ".git" not in p.parts)
INTERNAL_HOSTS = {"workofarttattoo.com", "www.workofarttattoo.com"}
DATA = json.loads((ROOT / "siteData" / "business.json").read_text(encoding="utf-8"))
REVIEWS = json.loads((ROOT / "siteData" / "reviews.json").read_text(encoding="utf-8"))
ARTISTS_RAW = json.loads((ROOT / "siteData" / "artists.json").read_text(encoding="utf-8"))
ARTISTS = ARTISTS_RAW["artists"] if isinstance(ARTISTS_RAW, dict) and "artists" in ARTISTS_RAW else ARTISTS_RAW
SOCIAL = json.loads((ROOT / "siteData" / "social.json").read_text(encoding="utf-8"))
CANONICAL_HOST = DATA["canonicalHost"].rstrip("/")
CANONICAL_NETLOC = urlparse(CANONICAL_HOST).netloc
REVIEW_COUNT = int(REVIEWS["googleReviewCount"])
ARTIST_NAMES = [artist["name"] for artist in ARTISTS]
ARTIST_COUNT = int(DATA["residentArtistCount"])
FORBIDDEN = {
    "legacy placeholder address": r"123\s+LV\s+Blvd",
    "wrong zip 89109": r"\b89109\b",
    "wrong zip 89101": r"\b89101\b",
    "old review count 2400": r"\b2,400\s+(google\s+)?reviews?\b|\b2400\s+(google\s+)?reviews?\b",
    "wrong artist count two": r"\btwo\s+(resident\s+artists|in-studio\s+artists|artists\s+in\s+studio)\b",
    "deprecated phone 725-224-1240": r"725[-\s.]224[-\s.]2617",
    "deprecated phone 725-224-1240": r"725[-\s.]224[-\s.]2931",
    "deprecated phone 725-260-6376": r"725[-\s.]260[-\s.]6376",
    "deprecated phone 725-224-1240": r"702[-\s.]960[-\s.]9607",
    "legacy email": r"Thewhiteknight702@gmail\.com",
    "tattoo/piercing contamination": r"where\s+do\s+you\s+(pierce|tattoo)\b|where\s+do\s+you\s+pierce\s+[^?<]{0,80}\btattoo\b|pierce\s+(fine[-\s]?line|realism|cover[-\s]?up)\s+tattoo",
    "old two-person roster": r"Joshua\s*(?:&amp;|&|and)\s*Katelyn\s+Cole\s+in-studio",
    "old rounded review claim": r"300\+\s+verified\s+five-star\s+reviews",
    "duplicate suite": r"Suite\s+3,\s*Suite\s+3",
    "stabislifee mislabeled as Joshua": r"@stabislifee[^<]{0,60}\(Joshua\)|Instagram\s*@stabislifee[^<]{0,60}Joshua",
    "established 2012 business claim": r"Established\s+2012",
    "unsupported highest rated": r"\bhighest[-\s]?rated\b",
    "unsupported number one": r"\bnumber\s+one\b",
    "unsupported #1": r"(?<![A-Za-z0-9])#1(?:\s|$)",
}

VISIBLE_ONLY_FORBIDDEN = {
    "unsupported highest rated",
    "unsupported number one",
    "unsupported #1",
}

UNIQUE_DATA_ATTRS = (
    "data-woa-desktop-nav-css",
    "data-woa-mobile-nav-css",
    "data-woa-sticky-book-cta",
    "data-woa-entity-schema",
    "data-woa-reel-list-schema",
    "data-woa-home-welcome",
    "data-woa-home-review-proof",
    "data-woa-google-tag-manager",
)

def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return "/" if rel == Path("code.html") else "/" + str(rel.parent).strip("/") + "/"

def visible_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ").split())

def load_decision_slugs(decisions: set[str]) -> set[str]:
    csv_path = ROOT / "audits" / "content-consolidation.csv"
    if not csv_path.is_file():
        return set()
    slugs: set[str] = set()
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if (row.get("decision") or "").upper() not in decisions:
                continue
            url = row.get("current_url") or ""
            slug = urlparse(url).path.strip("/")
            if slug:
                slugs.add(slug)
    return slugs

def load_merge_slugs() -> set[str]:
    return load_decision_slugs({"MERGE"})

def load_retired_slugs() -> set[str]:
    return load_decision_slugs({"MERGE", "301", "NOINDEX", "DELETE/410"})

def slug_for_path(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel == Path("code.html"):
        return ""
    if rel.name == "code.html":
        return str(rel.parent).strip("/")
    return str(rel).strip("/")

def assert_host(url: str, context: str, failures: list[str]) -> None:
    if not url.startswith("http"):
        return
    netloc = urlparse(url).netloc
    if netloc and netloc not in INTERNAL_HOSTS:
        return
    if netloc and netloc != CANONICAL_NETLOC:
        failures.append(f"{context}: canonical host mismatch: {url}")

def validate_sitewide_files(failures: list[str]) -> None:
    for name in ("sitemap.xml", "sitemap-static-pages.xml"):
        path = ROOT / name
        if not path.is_file():
            failures.append(f"{name}: missing")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for loc in re.findall(r"<loc>(.*?)</loc>", text):
            assert_host(loc, name, failures)
        for slug in load_merge_slugs():
            if f"/{slug}/" in text:
                failures.append(f"{name}: MERGE URL still appears in sitemap: /{slug}/")

def published_routes() -> set[str]:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        return set()
    routes: set[str] = set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    for loc in re.findall(r"<loc>(.*?)</loc>", text):
        parsed = urlparse(loc)
        route = parsed.path or "/"
        if not route.endswith("/"):
            route += "/"
        routes.add(route)
    return routes

def main() -> int:
    failures = []
    titles = {}
    retired_slugs = load_retired_slugs()
    published = published_routes()
    checked_pages = 0
    for path in HTML_FILES:
        slug = slug_for_path(path)
        if slug in retired_slugs:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        route = route_for(path)
        if published and route not in published:
            continue
        checked_pages += 1
        body_text = visible_text(BeautifulSoup(text, "html.parser"))
        for label, pattern in FORBIDDEN.items():
            haystack = body_text if label in VISIBLE_ONLY_FORBIDDEN else text
            if re.search(pattern, haystack, re.I):
                failures.append(f"{path.relative_to(ROOT)}: forbidden pattern: {label}")
        soup = BeautifulSoup(text, "html.parser")
        if "Google" in body_text and "review" in body_text.lower():
            visible_counts = {int(m.group(1).replace(",", "")) for m in re.finditer(r"\b(\d{2,4}(?:,\d{3})?)\s+(?:verified\s+)?(?:five-star\s+)?(?:Google\s+)?reviews?\b", body_text, re.I)}
            for count in visible_counts:
                if count != REVIEW_COUNT:
                    failures.append(f"{path.relative_to(ROOT)}: rendered review count {count} contradicts siteData {REVIEW_COUNT}")
        if re.search(r"\b(?:resident\s+artists|artists\s+in-studio|in-studio\s+artists)\b", body_text, re.I):
            if str(ARTIST_COUNT) not in body_text and "three" not in body_text.lower():
                failures.append(f"{path.relative_to(ROOT)}: rendered artist count may contradict siteData {ARTIST_COUNT}")
        if "resident artists" in body_text.lower() or "in-studio artists" in body_text.lower():
            missing = [name for name in ARTIST_NAMES if name.split()[0] not in body_text]
            if missing:
                failures.append(f"{path.relative_to(ROOT)}: incomplete artist roster near roster copy, missing {', '.join(missing)}")
        for attr in UNIQUE_DATA_ATTRS:
            count = len(soup.find_all(attrs={attr: True}))
            if count > 1:
                failures.append(f"{path.relative_to(ROOT)}: duplicate injected component {attr} appears {count} times")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        if not title:
            failures.append(f"{path.relative_to(ROOT)}: missing title")
        elif title in titles and route not in {"/"}:
            failures.append(f"{path.relative_to(ROOT)}: duplicate title also in {titles[title]}: {title}")
        else:
            titles[title] = path.relative_to(ROOT)
        h1s = soup.find_all("h1")
        if len(h1s) != 1:
            failures.append(f"{path.relative_to(ROOT)}: expected 1 h1, found {len(h1s)}")
        canonical = soup.find("link", rel="canonical")
        if not canonical:
            failures.append(f"{path.relative_to(ROOT)}: missing canonical")
        else:
            assert_host(canonical.get("href", ""), f"{path.relative_to(ROOT)} canonical", failures)
        og_url = soup.find("meta", property="og:url")
        if og_url:
            assert_host(og_url.get("content", ""), f"{path.relative_to(ROOT)} og:url", failures)
        schema_serialized: list[str] = []
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = script.string or script.get_text()
            if raw.strip():
                try:
                    parsed = json.loads(raw)
                except Exception as exc:
                    failures.append(f"{path.relative_to(ROOT)}: malformed JSON-LD: {exc}")
                    continue
                serialized = json.dumps(parsed)
                schema_serialized.append(serialized)
                for url in re.findall(r"https?://[^\"'\\s<>]+", serialized):
                    assert_host(url, f"{path.relative_to(ROOT)} JSON-LD", failures)
        combined_schema = "\n".join(schema_serialized)
        if route in {"/", "/official_location_hours_contact/", "/artists/"} and (
            "LocalBusiness" in combined_schema or "Organization" in combined_schema
        ):
            missing = [name for name in ARTIST_NAMES if name not in combined_schema]
            if missing:
                failures.append(f"{path.relative_to(ROOT)}: organization/location schema missing roster: {', '.join(missing)}")
    validate_sitewide_files(failures)
    if failures:
        print("SEO QA failed:")
        for f in failures[:250]:
            print("-", f)
        if len(failures) > 250:
            print(f"... {len(failures)-250} more failures")
        return 1
    print(f"SEO QA passed for {checked_pages} indexable HTML pages.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

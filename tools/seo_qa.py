#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import csv
import hashlib
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
STUDIO_SAMEAS = {
    SOCIAL.get("studioInstagram", "").rstrip("/"),
    SOCIAL.get("facebook", "").rstrip("/"),
} - {""}
PERSON_SAMEAS = {
    "Joshua Cole": {SOCIAL.get("joshuaInstagram", "").rstrip("/")} - {""},
    "Katelyn Cole": {SOCIAL.get("katelynInstagram", "").rstrip("/")} - {""},
    "Teralyn": {SOCIAL.get("teralynInstagram", "").rstrip("/")} - {""},
}
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
UNVERIFIED_SCHEMA_RE = re.compile(
    r"OpeningHoursSpecification|openingHours|implant-grade|implant grade|316L|surgical steel|"
    r"APP[-\s]aligned|APP piercing standards|Master Body Piercer|master piercer|"
    r"medical-grade piercing|medical-grade hygiene|hospital-grade",
    re.I,
)
APPOINTMENT_SOCIAL_RE = re.compile(r"Book an Appointment\s*\|", re.I)
BUILD_STAMP_RE = re.compile(rb"<!-- WOA_BUILD_STAMP: [^>]+ -->\n?")

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

def as_graph_nodes(parsed) -> list[dict]:
    if isinstance(parsed, dict) and isinstance(parsed.get("@graph"), list):
        return [node for node in parsed["@graph"] if isinstance(node, dict)]
    if isinstance(parsed, list):
        return [node for node in parsed if isinstance(node, dict)]
    if isinstance(parsed, dict):
        return [parsed]
    return []

def node_types(node: dict) -> set[str]:
    raw = node.get("@type")
    if isinstance(raw, list):
        return {str(item) for item in raw}
    if raw:
        return {str(raw)}
    return set()

def normalized_url(url: str) -> str:
    return (url or "").rstrip("/")

def validate_sameas(node: dict, context: str, failures: list[str]) -> None:
    same_as = node.get("sameAs")
    if not same_as:
        return
    urls = [normalized_url(url) for url in (same_as if isinstance(same_as, list) else [same_as]) if url]
    if len(urls) != len(set(urls)):
        failures.append(f"{context}: duplicate sameAs values")
    types = node_types(node)
    if "LocalBusiness" in types or "TattooParlor" in types or "Organization" in types:
        extra = sorted(set(urls) - STUDIO_SAMEAS)
        if extra:
            failures.append(f"{context}: LocalBusiness/Organization sameAs includes non-studio profile(s): {', '.join(extra)}")
    if "Person" in types:
        name = node.get("name", "")
        expected = PERSON_SAMEAS.get(name)
        if expected is not None:
            extra = sorted(set(urls) - expected)
            missing = sorted(expected - set(urls))
            if extra:
                failures.append(f"{context}: Person {name} sameAs includes profile(s) not owned by that person: {', '.join(extra)}")
            if missing:
                failures.append(f"{context}: Person {name} sameAs missing verified profile(s): {', '.join(missing)}")

def validate_head(soup: BeautifulSoup, raw: str, route: str, context: str, failures: list[str]) -> None:
    head = soup.head
    if not head:
        failures.append(f"{context}: missing head")
        return
    if len(head.find_all("title")) != 1:
        failures.append(f"{context}: expected exactly 1 title, found {len(head.find_all('title'))}")
    if len(head.find_all("link", rel=lambda rel: rel and "canonical" in rel)) != 1:
        failures.append(f"{context}: expected exactly 1 canonical")
    if len(head.find_all("meta", charset=True)) > 1:
        failures.append(f"{context}: duplicate charset meta")
    if len(head.find_all("meta", attrs={"name": "viewport"})) > 1:
        failures.append(f"{context}: duplicate viewport meta")
    title_text = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_description = (head.find("meta", attrs={"name": "description"}) or {}).get("content", "").strip()
    for selector, label in (
        (lambda: head.find("meta", attrs={"name": "description"}), "meta description"),
        (lambda: head.find("meta", property="og:url"), "og:url"),
        (lambda: head.find("meta", property="og:title"), "og:title"),
        (lambda: head.find("meta", property="og:description"), "og:description"),
        (lambda: head.find("meta", attrs={"name": "twitter:title"}), "twitter:title"),
        (lambda: head.find("meta", attrs={"name": "twitter:description"}), "twitter:description"),
    ):
        if not selector():
            failures.append(f"{context}: missing {label}")
    social_pairs = (
        ("og:title", (head.find("meta", property="og:title") or {}).get("content", "").strip(), title_text),
        (
            "og:description",
            (head.find("meta", property="og:description") or {}).get("content", "").strip(),
            meta_description,
        ),
        (
            "twitter:title",
            (head.find("meta", attrs={"name": "twitter:title"}) or {}).get("content", "").strip(),
            title_text,
        ),
        (
            "twitter:description",
            (head.find("meta", attrs={"name": "twitter:description"}) or {}).get("content", "").strip(),
            meta_description,
        ),
    )
    for label, actual, expected in social_pairs:
        if actual and expected and actual != expected:
            failures.append(f"{context}: social metadata mismatch for {label}")
    for rel in ("preconnect",):
        hrefs = [tag.get("href", "").strip() for tag in head.find_all("link", rel=lambda val: val and rel in val)]
        dupes = sorted({href for href in hrefs if href and hrefs.count(href) > 1})
        if dupes:
            failures.append(f"{context}: duplicate {rel} URL(s): {', '.join(dupes)}")
    active_asset_hrefs = [
        tag.get("href", "").strip()
        for tag in head.find_all("link", href=True)
        if not tag.find_parent("noscript")
        if "stylesheet" in (tag.get("rel") or []) or "preload" in (tag.get("rel") or [])
    ]
    dupes = sorted({href for href in active_asset_hrefs if href and active_asset_hrefs.count(href) > 1})
    if dupes:
        failures.append(f"{context}: duplicate stylesheet/preload URL(s): {', '.join(dupes[:5])}")
    if raw.count("GTM-TZTQSQBB") > 2:
        failures.append(f"{context}: duplicate GTM references")
    if raw.count("mixpanel.init(") > 1:
        failures.append(f"{context}: duplicate Mixpanel initialization")
    if re.search(r"<noscript\b[^>]*>[\s\S]*?<noscript\b", raw, re.I):
        failures.append(f"{context}: malformed nested noscript")
    if "&lt;&gt;" in raw or "&lt; &gt;" in raw:
        failures.append(f"{context}: literal encoded empty markup artifact")
    fields = [
        soup.title.string.strip() if soup.title and soup.title.string else "",
        (head.find("meta", property="og:title") or {}).get("content", ""),
        (head.find("meta", property="og:description") or {}).get("content", ""),
        (head.find("meta", attrs={"name": "twitter:title"}) or {}).get("content", ""),
        (head.find("meta", attrs={"name": "twitter:description"}) or {}).get("content", ""),
    ]
    if route != "/appointments/" and any(APPOINTMENT_SOCIAL_RE.search(field or "") for field in fields):
        failures.append(f"{context}: unrelated appointment social metadata")

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

def validate_idempotency_artifact(failures: list[str]) -> None:
    path = ROOT / "audits" / "build-idempotency.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"{path.relative_to(ROOT)}: malformed idempotency artifact: {exc}")
        return
    required = ("build1Hash", "build2Hash", "differences")
    missing = [key for key in required if key not in data]
    if missing:
        failures.append(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")
        return
    if not re.fullmatch(r"[0-9a-f]{64}", str(data["build1Hash"])):
        failures.append(f"{path.relative_to(ROOT)}: invalid build1Hash")
    if not re.fullmatch(r"[0-9a-f]{64}", str(data["build2Hash"])):
        failures.append(f"{path.relative_to(ROOT)}: invalid build2Hash")
    if data["build1Hash"] != data["build2Hash"]:
        failures.append(f"{path.relative_to(ROOT)}: complete-build hash mismatch")
    if data["differences"]:
        failures.append(f"{path.relative_to(ROOT)}: complete-build differences are not empty")

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
        validate_head(soup, text, route, str(path.relative_to(ROOT)), failures)
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
        schema_fingerprints: set[str] = set()
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = script.string or script.get_text()
            if raw.strip():
                try:
                    parsed = json.loads(raw)
                except Exception as exc:
                    failures.append(f"{path.relative_to(ROOT)}: malformed JSON-LD: {exc}")
                    continue
                serialized = json.dumps(parsed)
                if serialized in schema_fingerprints:
                    failures.append(f"{path.relative_to(ROOT)}: duplicate identical JSON-LD block")
                schema_fingerprints.add(serialized)
                schema_serialized.append(serialized)
                if '"AggregateRating"' in serialized:
                    failures.append(f"{path.relative_to(ROOT)}: unapproved AggregateRating schema")
                if UNVERIFIED_SCHEMA_RE.search(serialized):
                    failures.append(f"{path.relative_to(ROOT)}: unverified hours/material claim in JSON-LD")
                for node in as_graph_nodes(parsed):
                    validate_sameas(node, str(path.relative_to(ROOT)), failures)
                    types = node_types(node)
                    if "LocalBusiness" in types or "TattooParlor" in types:
                        if int(node.get("numberOfEmployees", ARTIST_COUNT)) != ARTIST_COUNT:
                            failures.append(f"{path.relative_to(ROOT)}: LocalBusiness numberOfEmployees does not match siteData")
                        employees = json.dumps(node.get("employee", []))
                        missing = [name for name in ("joshua-cole", "katelyn-cole", "teralyn") if name not in employees]
                        if missing:
                            failures.append(f"{path.relative_to(ROOT)}: LocalBusiness employee missing {', '.join(missing)}")
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
    validate_idempotency_artifact(failures)
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

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import csv
import hashlib
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from woa_geo_pages import GEO_PAGE_ACTIONS, GEO_PAGE_REDIRECTS
from woa_nav_config import REQUIRED_ARTIST_NAV_HREFS, STUDIO_STREET_ADDRESS
from woa_page_consolidation import RETIRE_OVERLAP_SLUGS

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
HOURS_VERIFIED = str(DATA.get("hours", {}).get("verificationStatus", "")).lower() == "verified"
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
    "deprecated phone (725) 224-1240": r"725[-\s.]224[-\s.]2617",
    "deprecated phone (725) 224-1240": r"725[-\s.]224[-\s.]2931",
    "deprecated phone 725-260-6376": r"725[-\s.]260[-\s.]6376",
    "deprecated phone (725) 224-1240": r"702[-\s.]960[-\s.]9607",
    "deprecated personal gmail inbox": r"thewhiteknight702@gmail\.com",
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
    "data-woa-piercing-decision",
)
UNVERIFIED_SCHEMA_RE = re.compile(
    r"OpeningHoursSpecification|openingHours|implant-grade|implant grade|316L|surgical steel|"
    r"APP[-\s]aligned|APP piercing standards|"
    r"medical[-\s]grade\s+(?:piercing|hygiene)|hospital-grade",
    re.I,
)
PIERCING_ROUTE_RE = re.compile(r"(piercing|katelyn|helix|conch|tragus|daith|rook|septum|nostril|labret|philtrum|navel|nipple|industrial)", re.I)
SKIN_SCIENCE_ROUTE_RE = re.compile(
    r"(dermis|epidermis|hypodermis|collagen|aging_skin|scar_tissue|macrophages|tattoo_permanence|why_tattoos_stay_forever|eczema|diabetes|psoriasis|stretch_marks|skin_science)",
    re.I,
)
SLEEVE_ROUTE_RE = re.compile(r"(sleeve|large_scale|large-scale)", re.I)
PIERCING_ASSET_RE = re.compile(
    r"(ear-piercing|helix|tragus|conch|nostril|septum|labret|piercing-session|piercing-setup|lobe-piercing)",
    re.I,
)
TATTOO_PROOF_IMAGE_RE = re.compile(
    r"(skull-hourglass|roaring-lion|all-seeing-eye|eagle-memorial|cover-up-tattoo|black-grey-lion|fresh-vs-healed|forearm-realism)",
    re.I,
)
PIERCING_CTA_BAD_RE = re.compile(
    r"send\s+a\s+reference\s+photo[^<]{0,120}(placement,\s*size,\s*and\s*timeline|timeline)",
    re.I,
)
APPOINTMENT_SOCIAL_RE = re.compile(r"Book an Appointment\s*\|", re.I)
BUILD_STAMP_RE = re.compile(rb"<!-- WOA_BUILD_STAMP: [^>]+ -->\n?")
PROMO_DATA = json.loads((ROOT / "siteData" / "piercing_promotions.json").read_text(encoding="utf-8")) if (ROOT / "siteData" / "piercing_promotions.json").is_file() else []
PROMO_SLUGS = {str(p.get("slug", "")).strip("/") for p in PROMO_DATA if p.get("slug")}
WEEKLY_PROMO_URL_RE = re.compile(r"/piercing-specials-las-vegas[-_/](?:20\d{2}|\d{1,2}[-_]\d{1,2}|week|weekly)", re.I)
SLEEVE_BRIDGE_MARKER = 'data-woa-sleeve-commercial-bridge="1"'
COVERUP_EVIDENCE_MARKER = 'data-woa-coverup-evidence="2026-08"'
OLD_COVERUP_IMAGE_RE = re.compile(
    r"cover-up-tattoo-phoenix-hand-las-vegas-after|"
    r"cover-up-tattoo-sunflower-over-black-ink-las-vegas|"
    r"cover-up-tattoo-faded-butterflies-hand-before|"
    r"cover-up-tattoo-faded-floral-leg-before|"
    r"healed-realism-seraphim-eye-wings-tattoo|"
    r"healed-black-grey-chain-heart-tattoo|"
    r"black-grey-collarbone-thorns-wreath-tattoo|"
    r"black-grey-realism-snake-sleeve-tattoo",
    re.I,
)
ELEVENLABS_RE = re.compile(
    r"elevenlabs|convai-widget|woa-convai-widget|<elevenlabs-convai\b|@elevenlabs/convai-widget-embed",
    re.I,
)
GEO_EXTRA_SLUGS = {
    "official_location_hours_contact",
    "tattoo_shop_near_the_strip_nap_corrected",
    "tattoo_shop_near_the_strip_geo_seo_optimized",
    "vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know",
    "vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison",
}
GEO_SLUGS = set(GEO_PAGE_ACTIONS) | GEO_EXTRA_SLUGS
MERGED_GEO_SLUGS = {
    slug for slug, action in GEO_PAGE_ACTIONS.items() if action == "MERGE_301"
} | set(GEO_PAGE_REDIRECTS)
GEO_STALE_RE = re.compile(r"\bHarry Reid International Airport\b", re.I)
GEO_EXACT_TIME_RE = re.compile(
    r"(?:about\s+|~)?\b\d{1,2}\s*[–-]\s*\d{1,2}\s*(?:min|mins|minutes)\b|"
    r"(?:about\s+|~)\b\d{1,2}\s*(?:min|mins|minutes)\b|"
    r"\b\d{1,2}\+\s*(?:min|mins|minutes)\b",
    re.I,
)
GEO_PRICE_RE = re.compile(r"(?:taxi|cab|rideshare|uber|lyft|parking|fare)[^.<]{0,80}\$\d+", re.I)
GEO_HOURS_RE = re.compile(
    r"Mon-Thu starts at 3 PM|Daily\s+12\s*pm\s*-\s*12\s*am|12:00\s*(?:PM)?\s*-\s*(?:12:00\s*AM|00:00)",
    re.I,
)
GEO_UNSUPPORTED_RE = re.compile(r"\b(?:best tattoo shop|best piercing shop|highest rated|#1|number one)\b", re.I)
GEO_FAKE_BRANCH_RE = re.compile(
    r"\b(?:inside|located in|located at)\s+(?:MGM|Mandalay|Luxor|Sphere|Fashion Show|Allegiant|T-Mobile|Fremont|UNLV)\b",
    re.I,
)
GEO_MINOR_POLICY_RE = re.compile(r"\b(?:minors?\s*14\+|parent\s*/\s*guardian|legal guardian|valid ID for both|consent on file)\b", re.I)
GEO_UNVERIFIED_OPERATIONS_RE = re.compile(r"\b(?:private lot|street parking|free studio lot|sterile setup)\b", re.I)
GEO_CABIN_PRESSURE_RE = re.compile(r"\bcabin pressure\b[^.]{0,120}\b(?:heal|healing|aftercare timing)\b", re.I)

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

def validate_piercing_page(soup: BeautifulSoup, raw: str, route: str, context: str, failures: list[str]) -> None:
    if not PIERCING_ROUTE_RE.search(route):
        return
    image_refs: list[str] = []
    for tag in soup.find_all(["img", "source"]):
        for attr in ("src", "srcset"):
            val = tag.get(attr)
            if val:
                image_refs.append(str(val))
    for tag in soup.find_all(style=True):
        style = str(tag.get("style") or "")
        if "background-image" in style:
            image_refs.append(style)
    if any(TATTOO_PROOF_IMAGE_RE.search(ref) for ref in image_refs):
        failures.append(f"{context}: piercing page contains tattoo proof imagery")
    if PIERCING_CTA_BAD_RE.search(raw):
        failures.append(f"{context}: piercing page contains tattoo reference-photo CTA copy")
    visible = visible_text(BeautifulSoup(raw, "html.parser"))
    for phrase in ("medical-grade", "hospital-grade", "APP-aligned", "surgical steel", "316L"):
        if phrase.lower() in visible.lower():
            failures.append(f"{context}: piercing page contains unverified visible claim: {phrase}")
    if route not in {"/artists/katelyn-cole/"} and "Joshua Cole's chair" in raw:
        failures.append(f"{context}: piercing page contains tattoo-artist proof-strip intro")
    if route == "/piercing-specials-las-vegas/":
        if soup.find("h1", string=re.compile(r"Piercing Specials in Las Vegas", re.I)) is None:
            failures.append(f"{context}: permanent specials page missing expected H1")
        if 'data-woa-piercing-special="1"' not in raw:
            failures.append(f"{context}: permanent specials page missing reusable promotion component")
        if re.search(r"\bcheap\s+piercings?\b", visible, re.I):
            failures.append(f"{context}: piercing specials competes on cheap")

def validate_visual_intent(soup: BeautifulSoup, raw: str, route: str, context: str, failures: list[str]) -> None:
    image_refs: list[str] = []
    for tag in soup.find_all(["img", "source"]):
        for attr in ("src", "srcset", "alt"):
            val = tag.get(attr)
            if val:
                image_refs.append(str(val))
    for tag in soup.find_all(style=True):
        image_refs.append(str(tag.get("style") or ""))
    joined_refs = "\n".join(image_refs)
    if SKIN_SCIENCE_ROUTE_RE.search(route) and PIERCING_ASSET_RE.search(joined_refs):
        failures.append(f"{context}: tattoo skin-science page contains piercing imagery or alt text")
    if SLEEVE_ROUTE_RE.search(route) and re.search(
        r"C78fY1quCVF|"
        r"<!-- WOA_PAGE_SPOTLIGHT_VIDEO_START -->[\s\S]{0,3000}(?:Katelyn|piercing in the studio|piercing placement|piercing-session)",
        raw,
        re.I,
    ):
        failures.append(f"{context}: sleeve/large-scale tattoo page contains piercing video module")
    if PIERCING_ROUTE_RE.search(route):
        h1 = soup.find("h1")
        first_img = soup.find("img")
        if h1 and first_img:
            first_ref = " ".join(str(first_img.get(attr, "")) for attr in ("src", "alt"))
            if TATTOO_PROOF_IMAGE_RE.search(first_ref):
                failures.append(f"{context}: piercing page first meaningful image is tattoo portfolio imagery")

def validate_promotion_model(failures: list[str]) -> None:
    required = {
        "id", "name", "slug", "headline", "description", "startDate", "endDate", "status",
        "discountType", "discountValue", "displayPrice", "eligiblePiercings", "jewelryTerms",
        "exclusions", "ctaText", "bookingUrl", "image", "altText", "analyticsCampaign",
    }
    statuses = {"ACTIVE", "UPCOMING", "EXPIRED"}
    if not PROMO_DATA:
        failures.append("siteData/piercing_promotions.json: missing promotion data")
        return
    for i, promo in enumerate(PROMO_DATA):
        missing = sorted(required - set(promo))
        if missing:
            failures.append(f"siteData/piercing_promotions.json[{i}]: missing {', '.join(missing)}")
        if str(promo.get("status", "")).upper() not in statuses:
            failures.append(f"siteData/piercing_promotions.json[{i}]: invalid status")
        if str(promo.get("slug", "")).strip("/") != "piercing-specials-las-vegas":
            failures.append(f"siteData/piercing_promotions.json[{i}]: promotions must use permanent specials slug")
        parsed_dates = {}
        for field in ("startDate", "endDate"):
            value = str(promo.get(field, "")).strip()
            if value:
                try:
                    parsed_dates[field] = date.fromisoformat(value)
                except ValueError:
                    failures.append(f"siteData/piercing_promotions.json[{i}]: invalid {field}")
        start = parsed_dates.get("startDate")
        end = parsed_dates.get("endDate")
        if start and end and start > end:
            failures.append(f"siteData/piercing_promotions.json[{i}]: startDate after endDate")
        image = str(promo.get("image", "")).strip()
        if image.startswith("/") and not (ROOT / image.lstrip("/")).is_file():
            failures.append(f"siteData/piercing_promotions.json[{i}]: missing promotion image {image}")

def validate_artist_nav(failures: list[str]) -> None:
    """Every rendered Artists dropdown must list Joshua, Katelyn, and Teralyn."""
    skip = {".git", "skipped_upload_build", "artists_raw", "node_modules", "__pycache__"}
    panel_re = re.compile(
        r"<details\b[^>]*>\s*<summary\b[^>]*>\s*Artists\s*</summary>\s*"
        r"<div class=\"(?:woa-dd-panel|guides-sub)[^\"]*\"[^>]*>(.*?)</div>\s*</details>",
        re.I | re.S,
    )
    required = set(REQUIRED_ARTIST_NAV_HREFS)
    for path in ROOT.rglob("*.html"):
        if any(part in skip for part in path.parts):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        panels = panel_re.findall(raw)
        if not panels:
            continue
        rel = str(path.relative_to(ROOT))
        for inner in panels:
            hrefs = set(re.findall(r'href="([^"]+)"', inner))
            text = re.sub(r"<[^>]+>", " ", inner)
            if not required.issubset(hrefs):
                missing = ", ".join(sorted(required - hrefs))
                failures.append(f"{rel}: Artists dropdown missing {missing}")
                break
            if re.search(r"jay[\s-]*jay", text, re.I) or "/jay_jay" in inner:
                failures.append(f"{rel}: Jay Jay remains in the current resident Artists menu")
                break
            if "/artists/teralyn/" in inner and not re.search(r"Fine Line", text, re.I):
                failures.append(f"{rel}: Teralyn Artists label is stale")
                break


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
        for slug in sorted(MERGED_GEO_SLUGS | RETIRE_OVERLAP_SLUGS):
            if f"/{slug}/" in text:
                failures.append(f"{name}: retired geo/overlap URL still appears in sitemap: /{slug}/")
        if WEEKLY_PROMO_URL_RE.search(text):
            failures.append(f"{name}: weekly/date-based piercing specials URL found")
        for slug in PROMO_SLUGS:
            if slug and f"/{slug}/" not in text:
                failures.append(f"{name}: permanent promotion URL missing from sitemap: /{slug}/")

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

def validate_analytics_source(failures: list[str]) -> None:
    ga_path = ROOT / "woa_ga4_conversions.py"
    booking_path = ROOT / "appointments" / "woa-booking.js"
    start_path = ROOT / "build_start_here_hub.py"
    for path in (ga_path, booking_path, start_path):
        if not path.is_file():
            failures.append(f"{path.relative_to(ROOT)}: missing analytics source")
            return

    ga = ga_path.read_text(encoding="utf-8", errors="ignore")
    booking = booking_path.read_text(encoding="utf-8", errors="ignore")
    start = start_path.read_text(encoding="utf-8", errors="ignore")

    required_events = (
        "booking_view",
        "booking_start",
        "booking_submit_attempt",
        "booking_submit",
        "piercing_cta_click",
        "piercing_booking_start",
        "piercing_booking_submit",
        "piercing_call_click",
        "piercing_text_click",
        "piercing_directions_click",
        "piercing_katelyn_click",
        "piercing_special_view",
        "piercing_special_click",
        "piercing_jewelry_click",
        "start_here_selection",
    )
    for event in required_events:
        if event not in ga:
            failures.append(f"{ga_path.relative_to(ROOT)}: missing GA4 event {event}")

    if 'send("booking_form_submit"' in ga:
        failures.append(f"{ga_path.relative_to(ROOT)}: legacy booking_form_submit still fires from source")

    submit_block = re.search(r'form\.addEventListener\("submit"[\s\S]*?\n  \}\}\);', ga)
    if submit_block and "piercing_booking_submit" in submit_block.group(0):
        failures.append(f"{ga_path.relative_to(ROOT)}: piercing_booking_submit fires on submit attempt")

    analytics_payload_forbidden = (
        "full_name",
        "data.email",
        "data.phone",
        "reference_links",
        "tattoo_description",
        "piercing_notes",
        "medical",
    )
    for phrase in analytics_payload_forbidden:
        if phrase in ga:
            failures.append(f"{ga_path.relative_to(ROOT)}: analytics source references possible PII field {phrase}")

    if "woa_booking_submit_success" not in booking:
        failures.append(f"{booking_path.relative_to(ROOT)}: booking success event bridge missing")
    if "dispatchBookingSuccess" not in booking:
        failures.append(f"{booking_path.relative_to(ROOT)}: AJAX/PHP success does not dispatch analytics completion")
    if "data-woa-start-here-selection" not in start:
        failures.append(f"{start_path.relative_to(ROOT)}: Start Here selections lack analytics attributes")

    generated_start = ROOT / "start_here" / "code.html"
    if generated_start.is_file() and "data-woa-start-here-selection" not in generated_start.read_text(encoding="utf-8", errors="ignore"):
        failures.append("start_here/code.html: missing generated Start Here selection tracking")

    generated_appointments = ROOT / "appointments" / "code.html"
    if generated_appointments.is_file():
        appointments = generated_appointments.read_text(encoding="utf-8", errors="ignore")
        for event in ("booking_view", "booking_start", "booking_submit", "booking_submit_attempt"):
            if event not in appointments:
                failures.append(f"appointments/code.html: missing generated analytics event {event}")

def validate_search_console_targets(failures: list[str]) -> None:
    sleeve_path = ROOT / "best_tattoo_styles_for_sleeves_large_scale_project_hub" / "code.html"
    if not sleeve_path.is_file():
        failures.append("best_tattoo_styles_for_sleeves_large_scale_project_hub/code.html: missing sleeve winner page")
        return
    sleeve_html = sleeve_path.read_text(encoding="utf-8", errors="ignore")
    if SLEEVE_BRIDGE_MARKER not in sleeve_html:
        failures.append("best_tattoo_styles_for_sleeves_large_scale_project_hub/code.html: missing sleeve commercial bridge")
    for required in ("/artists/joshua-cole/", "/healed_sleeve_tattoos_las_vegas/", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/", "/appointments/"):
        if required not in sleeve_html:
            failures.append(f"best_tattoo_styles_for_sleeves_large_scale_project_hub/code.html: missing sleeve bridge link {required}")
    for rel in ("cover-up-tattoos-las-vegas/code.html", "cover_up_tattoos_las_vegas_master_authority_guide/code.html"):
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"{rel}: missing cover-up page")
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if COVERUP_EVIDENCE_MARKER not in html:
            failures.append(f"{rel}: missing Joshua-supplied cover-up evidence section")
        if OLD_COVERUP_IMAGE_RE.search(html):
            failures.append(f"{rel}: old generic cover-up imagery still referenced")
        for required in (
            "floral-tattoo-cover-up-before-after-las-vegas",
            "large-scale-arm-rework-praying-hands-rose-las-vegas",
            "dark-pigment-black-grey-wing-eye-rework-las-vegas",
            "Send Joshua a Photo",
        ):
            if required not in html:
                failures.append(f"{rel}: missing cover-up evidence content {required}")

def validate_geo_page(
    soup: BeautifulSoup,
    raw: str,
    body_text: str,
    slug: str,
    context: str,
    failures: list[str],
    geo_intros: dict[str, list[str]],
    geo_faqs: dict[str, list[str]],
) -> None:
    if slug not in GEO_SLUGS:
        return
    if GEO_STALE_RE.search(raw):
        failures.append(f"{context}: stale Harry Reid International Airport airport reference")
    for label, pattern in (
        ("exact/unverified drive time", GEO_EXACT_TIME_RE),
        ("exact/unverified fare or parking price", GEO_PRICE_RE),
        ("unsupported geo superlative", GEO_UNSUPPORTED_RE),
        ("fake branch/location wording", GEO_FAKE_BRANCH_RE),
        ("unverified minor-policy detail", GEO_MINOR_POLICY_RE),
        ("unverified operational claim", GEO_UNVERIFIED_OPERATIONS_RE),
        ("unsupported cabin-pressure healing implication", GEO_CABIN_PRESSURE_RE),
    ):
        if pattern.search(body_text):
            failures.append(f"{context}: {label}")
    if not HOURS_VERIFIED and GEO_HOURS_RE.search(body_text):
        failures.append(f"{context}: unverified exact hours published")
    if not HOURS_VERIFIED and re.search(r"OpeningHoursSpecification|openingHours", raw, re.I):
        failures.append(f"{context}: unverified exact hours in schema")
    if slug in MERGED_GEO_SLUGS:
        robots = soup.find("meta", attrs={"name": "robots"})
        robots_content = (robots.get("content", "") if robots else "").lower()
        canonical = soup.find("link", rel="canonical")
        canonical_href = canonical.get("href", "") if canonical else ""
        expected = GEO_PAGE_REDIRECTS.get(slug) or "/tattoo_shop_near_the_strip_nap_corrected/"
        if "noindex" not in robots_content:
            failures.append(f"{context}: retired geo page is not noindex")
        if f"/{slug}/" in canonical_href:
            failures.append(f"{context}: retired geo page canonical points to itself")
        if expected not in raw:
            failures.append(f"{context}: retired geo page missing redirect target {expected}")
        return
    h1 = soup.find("h1")
    intro_tag = h1.find_next("p") if h1 else soup.find("p")
    intro = " ".join(intro_tag.get_text(" ").split()) if intro_tag else ""
    if len(intro) > 80:
        geo_intros.setdefault(intro.lower(), []).append(context)
    faq_texts = [
        " ".join(tag.get_text(" ").split()).lower()
        for tag in soup.find_all(["details", "summary"])
        if len(" ".join(tag.get_text(" ").split())) > 40
    ]
    if faq_texts:
        fingerprint = hashlib.sha256("\n".join(faq_texts).encode("utf-8")).hexdigest()
        geo_faqs.setdefault(fingerprint, []).append(context)
    for heading in soup.find_all(["h2", "h3"]):
        if heading.find_parent(attrs={"data-woa-piercing-special": True}):
            continue
        section_text = " ".join(heading.find_parent().get_text(" ").split()) if heading.find_parent() else ""
        if len(section_text) > 220:
            fingerprint = hashlib.sha256(section_text.lower().encode("utf-8")).hexdigest()
            geo_faqs.setdefault(f"section:{fingerprint}", []).append(context)
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw_schema = script.string or script.get_text()
        if not raw_schema.strip():
            continue
        try:
            parsed = json.loads(raw_schema)
        except Exception:
            continue
        for node in as_graph_nodes(parsed):
            types = node_types(node)
            if "LocalBusiness" not in types and "TattooParlor" not in types:
                continue
            serialized = json.dumps(node)
            address = json.dumps(node.get("address", {}))
            if STUDIO_STREET_ADDRESS not in address and STUDIO_STREET_ADDRESS not in serialized:
                failures.append(f"{context}: geo LocalBusiness schema does not use canonical studio address")
            if re.search(r"\b(MGM|Sphere|Allegiant|Mandalay|Fremont|UNLV|Henderson|Spring Valley|Summerlin)\b", address, re.I):
                failures.append(f"{context}: geo LocalBusiness schema appears to publish a fake location")

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
    validate_promotion_model(failures)
    titles = {}
    geo_intros: dict[str, list[str]] = {}
    geo_faqs: dict[str, list[str]] = {}
    retired_slugs = load_retired_slugs()
    published = published_routes()
    checked_pages = 0
    for path in HTML_FILES:
        slug = slug_for_path(path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        route = route_for(path)
        if slug in MERGED_GEO_SLUGS:
            soup = BeautifulSoup(text, "html.parser")
            body_text = visible_text(BeautifulSoup(text, "html.parser"))
            validate_geo_page(
                soup,
                text,
                body_text,
                slug,
                str(path.relative_to(ROOT)),
                failures,
                geo_intros,
                geo_faqs,
            )
            continue
        if slug in retired_slugs:
            continue
        if published and route not in published:
            continue
        checked_pages += 1
        if ELEVENLABS_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)}: retired ElevenLabs call widget still present")
        body_text = visible_text(BeautifulSoup(text, "html.parser"))
        for label, pattern in FORBIDDEN.items():
            haystack = body_text if label in VISIBLE_ONLY_FORBIDDEN else text
            if re.search(pattern, haystack, re.I):
                failures.append(f"{path.relative_to(ROOT)}: forbidden pattern: {label}")
        if WEEKLY_PROMO_URL_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)}: weekly/date-based piercing specials URL found")
        for retired_slug in MERGED_GEO_SLUGS:
            if f"/{retired_slug}/" in text:
                failures.append(f"{path.relative_to(ROOT)}: stale retired geo internal link: /{retired_slug}/")
        if route != "/piercing-specials-las-vegas/" and "Piercing Specials in Las Vegas" in body_text:
            failures.append(f"{path.relative_to(ROOT)}: duplicate piercing-specials H1/intent outside permanent URL")
        soup = BeautifulSoup(text, "html.parser")
        validate_head(soup, text, route, str(path.relative_to(ROOT)), failures)
        validate_piercing_page(soup, text, route, str(path.relative_to(ROOT)), failures)
        validate_visual_intent(soup, text, route, str(path.relative_to(ROOT)), failures)
        validate_geo_page(
            soup,
            text,
            body_text,
            slug,
            str(path.relative_to(ROOT)),
            failures,
            geo_intros,
            geo_faqs,
        )
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
    for intro, contexts in geo_intros.items():
        unique_contexts = sorted(set(contexts))
        if len(unique_contexts) > 1:
            failures.append(f"geo pages: duplicate intro across {', '.join(unique_contexts[:5])}")
    for contexts in geo_faqs.values():
        unique_contexts = sorted(set(contexts))
        if len(unique_contexts) > 2:
            failures.append(f"geo pages: duplicate FAQ block across {', '.join(unique_contexts[:5])}")
    validate_sitewide_files(failures)
    validate_artist_nav(failures)
    validate_idempotency_artifact(failures)
    validate_analytics_source(failures)
    validate_search_console_targets(failures)
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

#!/usr/bin/env python3
"""Audit and repair public SEO facts for the Work of Art static site."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
AUDITS = ROOT / "audits"
SITE = "https://www.workofarttattoo.com"

PUBLIC_EXTENSIONS = {".html", ".txt", ".xml", ".json", ".js", ".css", ".py", ".md"}
SKIP_PARTS = {".git", "__pycache__", "node_modules"}

BUSINESS_FACTS = {
    "name": "Work of Art Tattoo & Piercing",
    "address": "2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119",
    "street": "2375 E. Tropicana Ave, Suite 3",
    "city": "Las Vegas",
    "region": "NV",
    "postal_code": "89119",
    "phone": "(725) 224-1240",
    "phone_parens": "(725) 224-1240",
    "email": "thewhiteknight702@gmail.com",
    "google_rating": "5.0",
    "google_review_count": "323",
    "resident_artists": "3",
}

REPAIRS: list[tuple[str, str]] = [
    ("2375 E. Tropicana Suite 3", BUSINESS_FACTS["street"]),
    ("2375 E Tropicana Ave Suite 3", BUSINESS_FACTS["street"]),
    ("2375 E. Tropicana Ave, Suite 3", BUSINESS_FACTS["street"]),
    ("Hundreds of Google Reviews", "Google Reviews (323)"),
    ("Google reviews (2,400+)", "Google reviews (323)"),
    ("Google Reviews (2400+)", "Google Reviews (323)"),
    ("two in-studio artists", "three in-studio artists"),
    ("Two in-studio artists", "Three in-studio artists"),
    ("two resident artists", "three resident artists"),
    ("Two resident artists", "Our in-studio team"),
    ("Two Resident Tattoo Artists", "Three Resident Artists"),
    (
        "Two in-studio residents today — Joshua Cole and Katelyn Cole — not a rotating guest-artist wall.",
        "Three in-studio residents today — Joshua Cole, Katelyn Cole, and Teralyn — not a rotating guest-artist wall.",
    ),
    (
        "Work of Art has two in-studio artists: Joshua Cole (tattoo &amp; piercing; studio lead who trains the team) and Katelyn Cole (professional piercer).",
        "Work of Art has three in-studio artists: Joshua Cole (tattoo and piercing, studio lead), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fineline floral, script, custom drawings by commission, and high-detail small tattoos).",
    ),
    (
        "Joshua Cole — tattoo &amp; piercing. Katelyn Cole — professional piercer &amp; ear curation. Two resident artists, one address.",
        "Joshua Cole — tattoo artist and studio lead. Katelyn Cole — professional piercer &amp; ear curation. Teralyn — tattoo artist and piercer; fineline floral, script, commissioned custom drawings, and high-detail small tattoos. Our in-studio team, one address.",
    ),
    (
        "Where do you pierce realism tattoo in Las Vegas?",
        "Where do you do realism tattoos in Las Vegas?",
    ),
    (
        "Comparing tattoo and body piercing studios in las vegas or tattoo and body piercing studios las vegas listings? This guide helps you filter tattoo and body piercing studio and tattoos studios options — hygiene, healed portfolios, and artists who consult before they stencil — before you book a tattoo and body piercing studio in las vegas.",
        "If you are comparing Las Vegas tattoo and piercing studios, start with healed portfolios, licensing, hygiene, and whether the artist consults before they stencil.",
    ),
    (
        "If you are comparing Las Vegas tattoo and piercing studios, start with healed portfolios, licensing, hygiene, and whether the artist consults before they stencil.",
        "If you are comparing Las Vegas tattoo and piercing studios, start with healed portfolios, licensing, hygiene, and whether the artist consults before they stencil.",
    ),
    (
        "Tattoo and Body Piercing Studios Las Vegas vs Strip Shops | Work of Art",
        "Premium Tattoo & Piercing Studio vs Strip Shops | Work of Art",
    ),
    (
        "In a city built on quick wins and instant gratification, the Strip sells $40 walk-in tattoos next to bargain buffets. When you compare tattoo and body piercing studios in las vegas to high-volume strip booths, the gap is hygiene and healed quality — not price alone. This guide contrasts a licensed tattoo and body piercing studio las vegas collectors trust with tattoo and body piercing studios las vegas tourists should avoid: volume-first shops that stress sanitation and artistry.",
        "In a city built on quick wins and instant gratification, the Strip sells $40 walk-in tattoos next to bargain buffets. The real comparison is hygiene, healed quality, artist experience, and whether the studio can explain the process before you sit down. This guide contrasts a focused Las Vegas tattoo and piercing studio with high-volume storefronts where speed can put sanitation and artistry under pressure.",
    ),
]

BAD_FACT_PATTERNS = [
    r"123\s+LV\s+Blvd",
    r"\b89109\b",
    r"\b89101\b",
    r"2,400",
    r"\b2400\b",
    r"two\s+in-studio",
    r"two\s+resident",
    r"two\s+artists",
    r"tattoojosh@workofarttattoo\.com",
]

INTENT_WORDS = {
    "artist": ("artist", "portfolio", "joshua", "katelyn", "teralyn"),
    "pricing": ("price", "pricing", "cost", "under_100"),
    "piercing": ("piercing", "jewelry", "helix", "ear_", "facial", "oral", "body_"),
    "tattoo": ("tattoo", "realism", "cover", "fine_line", "walk_in", "healing"),
    "location": ("near", "location", "hours", "contact", "paradise", "strip", "airport", "henderson"),
    "gallery": ("gallery", "portfolio", "videos", "healed"),
}


def iter_text_files() -> Iterable[Path]:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in PUBLIC_EXTENSIONS:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        yield path


def iter_html_pages() -> Iterable[Path]:
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def public_url(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel == Path("code.html"):
        return f"{SITE}/"
    if rel.name == "code.html":
        return f"{SITE}/{'/'.join(rel.parts[:-1])}/"
    return f"{SITE}/{'/'.join(rel.parts)}"


def text_or_blank(node) -> str:
    if node is None:
        return ""
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def extract_meta(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    if not tag:
        tag = soup.find("meta", attrs={"property": name})
    return (tag.get("content") or "").strip() if tag else ""


def extract_author(text: str) -> str:
    for person in ("Joshua Cole", "Katelyn Cole", "Teralyn"):
        if person.lower() in text.lower():
            return person
    return ""


def page_type_and_intent(path: Path, title: str, h1: str) -> tuple[str, str, str]:
    haystack = " ".join(path.parts).lower() + " " + title.lower() + " " + h1.lower()
    page_type = "guide"
    primary_topic = "tattoo and piercing"
    intent = "local service research"
    for topic, words in INTENT_WORDS.items():
        if any(word in haystack for word in words):
            primary_topic = topic
            break
    if "artist" in haystack or "/artists/" in public_url(path):
        page_type = "artist"
        intent = "view artist portfolio and book"
    elif primary_topic == "location":
        page_type = "location"
        intent = "find studio location and contact"
    elif primary_topic == "pricing":
        page_type = "pricing"
        intent = "compare tattoo pricing"
    elif primary_topic == "gallery":
        page_type = "portfolio"
        intent = "view healed work and examples"
    elif primary_topic == "piercing":
        page_type = "piercing guide"
        intent = "research piercing service"
    return page_type, primary_topic, intent


def clean_url_for(path: Path) -> str:
    url = public_url(path)
    rel = path.relative_to(ROOT)
    slug = rel.parts[-2] if rel.name == "code.html" and len(rel.parts) > 1 else rel.stem
    explicit = {
        "how_much_do_tattoos_cost_in_las_vegas_authority_guide": "/tattoos/pricing/",
        "realism_tattoos_las_vegas_master_authority_guide": "/tattoos/realism/",
        "realism-tattoos-las-vegas": "/tattoos/realism/",
        "cover_up_tattoos_las_vegas_master_authority_guide": "/tattoos/cover-ups/",
        "cover-up-tattoos-las-vegas": "/tattoos/cover-ups/",
        "fine_line_tattoos_las_vegas_master_authority_guide": "/tattoos/fine-line/",
        "best_fine_line_tattoos_in_vegas_ultimate_authority_guide": "/tattoos/fine-line/",
        "walk_in_tattoos_las_vegas_authority_guide": "/tattoos/walk-ins/",
        "walk-in-tattoos-las-vegas": "/tattoos/walk-ins/",
        "tattoo_healing_in_desert_climate_expert_aftercare_guide": "/tattoos/aftercare/",
        "official_location_hours_contact": "/visit/",
        "tattoo_shop_near_the_strip_nap_corrected": "/visit/near-strip/",
        "tattoo_shop_paradise_nevada": "/visit/paradise/",
        "geo_hub_ai_source_of_truth_work_of_art": "/resources/ai-source/",
    }
    if slug in explicit:
        return f"{SITE}{explicit[slug]}"
    if "_" in slug or "authority" in slug or "master" in slug:
        clean = slug.replace("_", "-")
        clean = re.sub(r"-(authority|master|ultimate|guide|hub|las-vegas|updated|expert|selection)+", "", clean)
        clean = re.sub(r"-+", "-", clean).strip("-")
        return f"{SITE}/{clean}/"
    return url


def repair_files() -> list[tuple[str, int]]:
    changed = []
    for path in iter_text_files():
        if path.name == Path(__file__).name or "audits" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in REPAIRS:
            text = text.replace(old, new)
        if path.name == "remove_jay_jay_from_site.py":
            text = text.replace("Two residents today", "Three residents today")
            text = text.replace("two in-studio residents", "three in-studio residents")
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append((str(path.relative_to(ROOT)), original.count("\n") + 1))
    return changed


def write_inventory() -> int:
    rows = []
    duplicate_by_canonical: dict[str, list[str]] = defaultdict(list)
    parsed = []
    for path in iter_html_pages():
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        title = text_or_blank(soup.find("title"))
        h1 = text_or_blank(soup.find("h1"))
        canonical_tag = soup.find("link", rel=lambda value: value and "canonical" in value)
        canonical = (canonical_tag.get("href") or "").strip() if canonical_tag else ""
        robots = extract_meta(soup, "robots")
        index_status = "noindex" if "noindex" in robots.lower() else "index"
        page_type, primary_topic, intent = page_type_and_intent(path, title, h1)
        text = soup.get_text(" ", strip=True)
        author = extract_author(text)
        reviewer = ""
        m = re.search(r"Reviewed by\s+([A-Z][A-Za-z ]+)", text)
        if m:
            reviewer = m.group(1).strip()
        url = public_url(path)
        key = canonical or re.sub(r"\s+", " ", title.lower()).strip() or url
        duplicate_by_canonical[key].append(url)
        parsed.append((path, url, title, h1, canonical, index_status, page_type, primary_topic, intent, author, reviewer))

    for item in parsed:
        path, url, title, h1, canonical, index_status, page_type, primary_topic, intent, author, reviewer = item
        key = canonical or re.sub(r"\s+", " ", title.lower()).strip() or url
        cluster = " | ".join(sorted(duplicate_by_canonical[key])) if len(duplicate_by_canonical[key]) > 1 else ""
        clean_url = clean_url_for(path)
        notes = []
        action = "keep"
        if not title:
            notes.append("missing title")
            action = "repair metadata"
        if not h1:
            notes.append("missing h1")
            action = "repair metadata"
        if canonical and canonical.rstrip("/") != url.rstrip("/"):
            notes.append("canonical differs from file URL")
        if clean_url.rstrip("/") != url.rstrip("/"):
            action = "redirect to clean URL"
            notes.append(f"recommended clean URL: {clean_url}")
        if cluster:
            notes.append("duplicate canonical/title cluster")
        rows.append(
            {
                "url": url,
                "source_file": str(path.relative_to(ROOT)),
                "page_type": page_type,
                "title": title,
                "h1": h1,
                "canonical": canonical,
                "index_status": index_status,
                "primary_topic": primary_topic,
                "primary_search_intent": intent,
                "author": author,
                "reviewer": reviewer,
                "location_target": "Las Vegas, NV" if "las vegas" in (title + h1 + str(path)).lower() else "",
                "duplicate_cluster": cluster,
                "recommended_action": action,
                "notes": "; ".join(notes),
            }
        )

    AUDITS.mkdir(exist_ok=True)
    with (AUDITS / "seo-url-inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["url"]))
    return len(rows)


def write_fact_conflicts() -> int:
    fact_findings = []
    hours_findings = []
    fact_mismatches = 0
    combined = re.compile("|".join(BAD_FACT_PATTERNS), re.IGNORECASE)
    hours = re.compile(r"(daily[:\s].*12|12\s*:?\s*00\s*pm|12pm|12 pm|mon.?thu.*3\s*pm|3\s*pm.?9\s*pm)", re.IGNORECASE)
    for path in iter_text_files():
        if "audits" in path.parts or path.name == Path(__file__).name:
            continue
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = re.sub(r"\s+", " ", line).strip()
            if not stripped:
                continue
            if re.search(r"\b2400\b", stripped) and not re.search(r"google|review", stripped, re.IGNORECASE):
                continue
            if combined.search(stripped):
                fact_mismatches += 1
                fact_findings.append(("business fact mismatch", rel, lineno, stripped[:260]))
            elif hours.search(stripped):
                hours_findings.append(("opening hours statement", rel, lineno, stripped[:260]))

    lines = [
        "# Business Fact Conflicts",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Verified Source Of Truth",
        "",
        f"- Business: {BUSINESS_FACTS['name']}",
        f"- Address: {BUSINESS_FACTS['address']}",
        f"- Phone: {BUSINESS_FACTS['phone']}",
        f"- Email: {BUSINESS_FACTS['email']}",
        f"- Google rating/reviews: {BUSINESS_FACTS['google_rating']} stars, {BUSINESS_FACTS['google_review_count']} reviews",
        f"- Resident artist count: {BUSINESS_FACTS['resident_artists']}",
        "",
        "## Business Fact Mismatches",
        "",
    ]
    if fact_findings:
        for kind, rel, lineno, snippet in fact_findings:
            lines.append(f"- `{kind}` in `{rel}:{lineno}`: {snippet}")
    else:
        lines.append("- No unresolved public NAP/review-count/artist-count mismatches found by the configured scan.")
    lines.extend(
        [
            "",
            "## Opening-Hours Statements For Manual Review",
            "",
            "The brief did not provide a newly verified hours value, so these are inventoried instead of overwritten.",
            "",
        ]
    )
    seen_hour_snippets = set()
    for kind, rel, lineno, snippet in hours_findings:
        normalized = re.sub(r"\s+", " ", snippet.lower())
        if normalized in seen_hour_snippets:
            continue
        seen_hour_snippets.add(normalized)
        lines.append(f"- `{kind}` in `{rel}:{lineno}`: {snippet}")
    (AUDITS / "business-fact-conflicts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return fact_mismatches


def write_social_conflicts() -> int:
    known_handles = {"workofarttattoo", "stabislifee", "mischiefmodifies"}
    profile_re = re.compile(r"https?://(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)/?", re.IGNORECASE)
    mention_re = re.compile(r"@(workofarttattoo|stabislifee|mischiefmodifies)\b", re.IGNORECASE)
    expected = {
        "studio": {"workofarttattoo"},
        "joshua cole": {"workofarttattoo"},
        "katelyn cole": {"stabislifee"},
        "teralyn": {"mischiefmodifies"},
    }
    occurrences = []
    for path in iter_text_files():
        if "audits" in path.parts or path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), 1):
            handles = []
            for match in profile_re.finditer(line):
                handle = match.group(1).strip("/").lower()
                if handle in known_handles:
                    handles.append(handle)
            handles.extend(match.group(1).lower() for match in mention_re.finditer(line))
            for handle in sorted(set(handles)):
                nearby = line.lower()
                owners = {candidate for candidate in expected if candidate in nearby}
                owner = ", ".join(sorted(owners)) if owners else "unknown"
                status = "verified"
                if owners and not any(handle in expected[candidate] for candidate in owners):
                    status = "needs review"
                occurrences.append((status, owner, handle, str(path.relative_to(ROOT)), lineno))

    conflicts = sum(1 for status, *_rest in occurrences if status == "needs review")
    by_handle: dict[str, int] = defaultdict(int)
    for _status, _owner, handle, _rel, _lineno in occurrences:
        by_handle[handle] += 1

    lines = [
        "# Social Profile Conflicts",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Repo-Verified Handles",
        "",
        "- Studio / Joshua Cole: `@workofarttattoo`",
        "- Katelyn Cole: `@stabislifee`",
        "- Teralyn: `@mischiefmodifies`",
        "",
        "## Handle Counts",
        "",
    ]
    for handle, count in sorted(by_handle.items()):
        lines.append(f"- `@{handle}`: {count} occurrences")
    lines.extend(["", "## Possible Conflicts", ""])
    if conflicts:
        for status, owner, handle, rel, lineno in occurrences:
            if status == "needs review":
                lines.append(f"- `{status}` `{owner}` -> `@{handle}` in `{rel}:{lineno}`")
    else:
        lines.append("- No artist-handle conflicts found among known Instagram handles.")
    lines.extend(["", "## Sample Verified Occurrences", ""])
    for status, owner, handle, rel, lineno in occurrences[:75]:
        lines.append(f"- `{status}` `{owner}` -> `@{handle}` in `{rel}:{lineno}`")
    (AUDITS / "social-profile-conflicts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return conflicts


def write_migration_plan() -> int:
    rows = []
    seen = set()
    for path in iter_html_pages():
        old = public_url(path)
        clean = clean_url_for(path)
        if old in seen:
            continue
        seen.add(old)
        rel = str(path.relative_to(ROOT))
        if clean.rstrip("/") != old.rstrip("/"):
            action = "redirect"
            reason = "Clean URL removes generated slug wording and consolidates duplicate search intent."
        else:
            action = "keep"
            reason = "Already clean enough or needed as a static asset/page path."
        rows.append(
            {
                "old_url": old,
                "recommended_clean_url": clean,
                "keep_or_redirect": action,
                "reason": reason,
                "source_file": rel,
            }
        )
    with (AUDITS / "url-migration-plan.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["old_url"]))
    return len(rows)


def main() -> None:
    AUDITS.mkdir(exist_ok=True)
    changed = repair_files()
    inventory_count = write_inventory()
    fact_count = write_fact_conflicts()
    social_conflicts = write_social_conflicts()
    migration_count = write_migration_plan()
    print(f"repaired_files={len(changed)}")
    for rel, _lines in changed:
        print(f"  {rel}")
    print(f"inventory_rows={inventory_count}")
    print(f"business_fact_findings={fact_count}")
    print(f"social_conflicts={social_conflicts}")
    print(f"migration_rows={migration_count}")


if __name__ == "__main__":
    main()

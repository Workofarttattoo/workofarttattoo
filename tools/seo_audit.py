#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse, urldefrag

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.workofarttattoo.com"
HTML_FILES = sorted(p for p in ROOT.rglob("code.html") if ".git" not in p.parts)
LEGACY_PATTERNS = {
    "legacy placeholder address": r"123\s+LV\s+Blvd",
    "wrong zip 89109": r"\b89109\b",
    "wrong zip 89101": r"\b89101\b",
    "old review count 2400": r"\b2,400\b|\b2400\b",
    "wrong artist count two": r"\btwo\s+(resident\s+)?(artists|in-studio)\b",
    "deprecated phone 725-224-1240": r"725[-\s.]224[-\s.]2617",
    "deprecated phone 725-224-1240": r"725[-\s.]224[-\s.]2931",
    "deprecated phone 725-260-6376": r"725[-\s.]260[-\s.]6376",
    "deprecated phone 725-224-1240": r"702[-\s.]960[-\s.]9607",
    "legacy email": r"Thewhiteknight702@gmail\.com",
}
QUESTIONABLE_LANGUAGE = [
    "authority", "master authority", "ai source of truth", "geo", "highest rated", "#1", "number one", "premier", "leading", "industry standard", "look no further", "ultimate guide", "nestled in the heart"
]


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel == Path("code.html"):
        return "/"
    return "/" + str(rel.parent).strip("/") + "/"


def page_type(route: str, title: str) -> str:
    slug = route.strip("/")
    s = slug.lower()
    t = title.lower()
    if route == "/": return "home"
    if s.startswith("artists/") or s == "artists": return "artist"
    if "healing_database" in s: return "healing-database"
    if "healed" in s or "gallery" in s: return "gallery"
    if "piercing" in s: return "piercing"
    if "tattoo_shop_near" in s or s.startswith("geo_") or any(x in s for x in ["paradise", "spring_valley", "enterprise", "henderson", "airport", "strip", "sphere", "allegiant", "mgm"]): return "location"
    if "appointment" in s: return "conversion"
    if "skin_science" in s or "tattoo" in s or "styles" in s or "cover" in s or "realism" in s or "fine_line" in s: return "tattoo"
    if "faq" in t: return "faq"
    return "other"


def text_has_original_image(soup: BeautifulSoup) -> bool:
    imgs = soup.find_all("img")
    if not imgs: return False
    for img in imgs:
        src = img.get("src", "")
        alt = img.get("alt", "")
        if any(x in src.lower() for x in ["client-portfolio", "studio_gallery", "artists", "healed", "portfolio"]):
            return True
        if any(x in alt.lower() for x in ["work of art", "joshua", "katelyn", "teralyn", "healed", "client"]):
            return True
    return False


def intent_for(route: str, title: str, ptype: str) -> tuple[str, str, str]:
    slug = route.strip("/").replace("_", " ").replace("-", " ")
    if ptype == "home": return ("book tattoo or piercing studio in Las Vegas", "commercial", "high")
    if ptype == "artist": return ("evaluate and book a specific Work of Art artist", "commercial", "high")
    if ptype == "location": return ("plan travel to the studio from a Las Vegas area/landmark", "local", "high")
    if ptype == "piercing": return ("learn about or book piercing service: " + slug, "mixed", "high")
    if ptype == "tattoo": return ("learn about or book tattoo service/topic: " + slug, "mixed", "high")
    if ptype == "healing-database": return ("understand tattoo healing timing/stage", "informational", "medium")
    if ptype == "gallery": return ("inspect original work/proof", "commercial", "medium")
    return ("understand page topic: " + (title or slug), "mixed", "medium")


def recommended_action(route: str, ptype: str, text: str, has_case: bool, has_photo: bool, inbound: int) -> str:
    s = route.lower()
    if route in ["/", "/artists/", "/artists/joshua-cole/", "/artists/katelyn-cole/", "/artists/teralyn/", "/appointments/"]:
        return "KEEP"
    if ptype == "healing-database" and not has_case:
        return "MERGE"
    if ptype == "location" and not any(x in text.lower() for x in ["parking", "rideshare", "airport", "hotel", "walk", "drive", "minutes", "route"]):
        return "MERGE"
    if len(text) < 1200 and inbound <= 1:
        return "IMPROVE"
    if any(x in s for x in ["ai_source", "geo_hub"]):
        return "IMPROVE"
    return "KEEP" if (has_photo or has_case or inbound > 2) else "IMPROVE"


def main() -> int:
    pages = []
    links_out = defaultdict(list)
    inbound = Counter()
    route_to_file = {route_for(p): p for p in HTML_FILES}
    sitemap_urls = set()
    for sm in [ROOT / "sitemap.xml", ROOT / "sitemap-static-pages.xml"]:
        if sm.exists():
            for loc in re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8", errors="ignore"), re.I | re.S):
                path = urlparse(loc.strip()).path or "/"
                sitemap_urls.add(path if path.endswith("/") else path + "/")

    for path in HTML_FILES:
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        route = route_for(path)
        title = (soup.title.string.strip() if soup.title and soup.title.string else "")
        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc = desc_tag.get("content", "").strip() if desc_tag else ""
        can = soup.find("link", rel="canonical")
        canonical = can.get("href", "").strip() if can else ""
        robots = soup.find("meta", attrs={"name": "robots"})
        robots_content = robots.get("content", "").strip() if robots else ""
        indexable = "noindex" not in robots_content.lower()
        h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
        text = soup.get_text(" ", strip=True)
        ptype = page_type(route, title)
        primary_topic, primary_intent, local_intent = intent_for(route, title, ptype)
        has_photo = text_has_original_image(soup)
        has_video = bool(soup.find(["video", "iframe"])) or "VideoObject" in html
        has_case = bool(re.search(r"real case|case study|fresh.*healed|healed.*fresh|client example", text, re.I))
        firsthand = bool(re.search(r"what we see|in our studio|we see|studio observation|artist observation", text, re.I))
        author = ""
        reviewer = ""
        for name in ["Joshua Cole", "Katelyn Cole", "Teralyn"]:
            if name in text:
                if not author: author = name
                elif not reviewer and name != author: reviewer = name
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href or href.startswith(('#','mailto:','tel:','javascript:')):
                continue
            clean = urldefrag(href)[0]
            parsed = urlparse(clean)
            if parsed.netloc and "workofarttattoo.com" not in parsed.netloc:
                continue
            target = parsed.path if parsed.netloc else clean
            if not target.startswith("/"):
                continue
            if not target.endswith("/") and Path(target).suffix == "":
                target += "/"
            links_out[route].append((target, a.get_text(" ", strip=True)[:140]))
            inbound[target] += 1
        pages.append({
            "url": SITE + route,
            "route": route,
            "source_file": str(path.relative_to(ROOT)),
            "http_intent": "static-html-export",
            "page_type": ptype,
            "title": title,
            "meta_description": desc,
            "h1": " | ".join(h1s),
            "canonical": canonical,
            "robots": robots_content,
            "indexable": str(indexable).lower(),
            "author": author,
            "reviewer": reviewer,
            "primary_topic": primary_topic,
            "primary_intent": primary_intent,
            "local_intent": local_intent,
            "original_photos": str(has_photo).lower(),
            "original_video": str(has_video).lower(),
            "original_case_study": str(has_case).lower(),
            "firsthand_experience": str(firsthand).lower(),
            "duplicate_cluster": "healing database" if ptype == "healing-database" else ("location pages" if ptype == "location" else ""),
            "internal_links_in": 0,
            "internal_links_out": len(links_out[route]),
            "recommended_action": "",
            "notes": ""
        })

    for row in pages:
        route = row["route"]
        row["internal_links_in"] = inbound[route]
        src = ROOT / row["source_file"]
        text = BeautifulSoup(src.read_text(encoding="utf-8", errors="ignore"), "html.parser").get_text(" ", strip=True)
        row["recommended_action"] = recommended_action(route, row["page_type"], text, row["original_case_study"] == "true", row["original_photos"] == "true", inbound[route])
        notes = []
        if route not in sitemap_urls:
            notes.append("not in sitemap")
        if not row["canonical"]:
            notes.append("missing canonical")
        if row["h1"].count("|") > 0:
            notes.append("multiple h1s")
        if row["page_type"] == "healing-database" and row["original_case_study"] != "true":
            notes.append("healing page lacks documented real case evidence")
        row["notes"] = "; ".join(notes)
        row.pop("route")

    audits = ROOT / "audits"
    audits.mkdir(exist_ok=True)
    inv_fields = ["url","source_file","http_intent","page_type","title","meta_description","h1","canonical","robots","indexable","author","reviewer","primary_topic","primary_intent","local_intent","original_photos","original_video","original_case_study","firsthand_experience","duplicate_cluster","internal_links_in","internal_links_out","recommended_action","notes"]
    with (audits / "url-inventory.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=inv_fields, lineterminator="\n")
        w.writeheader(); w.writerows(pages)

    with (audits / "internal-link-map.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source","target","anchor","relationship","priority"], lineterminator="\n")
        w.writeheader()
        for source, targets in sorted(links_out.items()):
            for target, anchor in targets:
                relationship = "internal" if target in route_to_file else "internal-missing-or-asset"
                priority = "P0" if target not in route_to_file and not Path(target.lstrip('/')).exists() else "P2"
                w.writerow({"source": SITE + source, "target": target, "anchor": anchor, "relationship": relationship, "priority": priority})

    with (audits / "broken-links.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source","target","type","status","notes"], lineterminator="\n")
        w.writeheader()
        for source, targets in sorted(links_out.items()):
            for target, anchor in targets:
                if target in route_to_file:
                    continue
                if Path(target.lstrip('/')).exists():
                    continue
                w.writerow({"source": SITE + source, "target": target, "type": "internal", "status": "missing-local-target", "notes": anchor})

    with (audits / "entity-conflicts.md").open("w", encoding="utf-8") as f:
        f.write("# Entity / NAP Conflict Audit\n\n")
        f.write("Verified source of truth: `siteData/*.json`.\n\n")
        f.write("Correct business values: Work of Art Tattoo & Piercing; 2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119; 725-224-1240; booking@workofarttattoo.com; 3 resident artists; 5.0 rating; 323 Google reviews.\n\n")
        for label, pattern in LEGACY_PATTERNS.items():
            hits = []
            rx = re.compile(pattern, re.I)
            for path in list(HTML_FILES) + sorted(ROOT.glob("*.py")) + sorted((ROOT / "audits").glob("*.md")):
                if path.name == "entity-conflicts.md":
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
                if rx.search(text):
                    hits.append(str(path.relative_to(ROOT)))
            f.write(f"## {label}\n\n")
            if hits:
                f.write("Potential conflict locations:\n")
                for h in hits[:100]:
                    f.write(f"- `{h}`\n")
                if len(hits) > 100:
                    f.write(f"- ... {len(hits)-100} more repeated/static-export hits\n")
                f.write("\nRecommended action: inspect context before replacement; many hits may be generated script history rather than public pages.\n\n")
            else:
                f.write("No repository hits found.\n\n")

    with (audits / "content-consolidation.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["current_url","topic","overlap_url","unique_value","original_evidence","decision","target_url","redirect_required","reason"], lineterminator="\n")
        w.writeheader()
        for row in pages:
            if row["page_type"] == "healing-database":
                w.writerow({"current_url": row["url"], "topic": "tattoo healing timeline variation", "overlap_url": SITE + "/las-vegas-tattoo-healing-guide/", "unique_value": "low unless page has documented studio case evidence", "original_evidence": row["original_case_study"], "decision": "MERGE", "target_url": SITE + "/las-vegas-tattoo-healing-guide/", "redirect_required": "yes-after-map", "reason": "Thin healing-stage/style variants should not remain indexable without firsthand documentation."})
            elif row["page_type"] == "location" and row["recommended_action"] == "MERGE":
                w.writerow({"current_url": row["url"], "topic": "local/landmark page", "overlap_url": SITE + "/visit/", "unique_value": "needs route/parking/visitor logistics", "original_evidence": row["original_photos"], "decision": "MERGE", "target_url": SITE + "/visit/", "redirect_required": "yes-after-map", "reason": "Avoid near-identical geo pages without unique visitor utility."})

    with (audits / "url-migration-plan.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["old_url","new_url","reason","existing_internal_links","redirect","canonical_change","sitemap_change"], lineterminator="\n")
        w.writeheader()
        for row in pages:
            if row["page_type"] == "healing-database" and row["recommended_action"] == "MERGE":
                w.writerow({"old_url": row["url"], "new_url": SITE + "/las-vegas-tattoo-healing-guide/", "reason": "Consolidate thin healing variants after content merge", "existing_internal_links": row["internal_links_in"], "redirect": "301 required before removing old page", "canonical_change": "pending", "sitemap_change": "pending"})

    with (audits / "content-gap-opportunities.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["topic","user_intent","current_best_page","coverage_score","commercial_value","expert_available","original_evidence_available","recommended_action","priority"], lineterminator="\n")
        w.writeheader()
        topics = [
            ("Tattoo pain", "Understand pain by placement and plan appointment", "/tattoo_pain_chart_placement_sensitivity_guide/", 55, "high", "Joshua Cole", "partial", "Improve existing page with real studio observations and sourced health boundaries", "P1"),
            ("Swimming after tattoo", "Know when pools/hot tubs are safe after a Vegas tattoo", "/tattoo-aftercare-desert-climate/", 65, "high", "Joshua Cole", "partial", "Strengthen existing aftercare page rather than create many variants", "P1"),
            ("Piercing bumps", "Understand irritation signs and when to ask piercer/doctor", "/piercing_aftercare_guide_las_vegas/", 60, "high", "Katelyn Cole", "partial", "Improve existing piercing aftercare guide with conservative medical language", "P1"),
            ("Implant-grade titanium jewelry", "Choose safe starter jewelry", "/piercing_jewelry_guide_las_vegas/", 60, "high", "Katelyn Cole", "partial", "Improve existing jewelry guide and link to piercing hub", "P1"),
            ("Healed tattoo proof", "Compare fresh vs healed results", "/healed_tattoo_gallery_las_vegas/", 70, "high", "Joshua Cole", "yes", "Build structured case-study data over time", "P0"),
        ]
        for t in topics:
            w.writerow(dict(zip(["topic","user_intent","current_best_page","coverage_score","commercial_value","expert_available","original_evidence_available","recommended_action","priority"], t)))

    print(f"Inventoried {len(pages)} pages")
    print("Recommended actions", Counter(r["recommended_action"] for r in pages))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(p for p in ROOT.rglob("code.html") if ".git" not in p.parts)
DATA = json.loads((ROOT / "siteData" / "business.json").read_text(encoding="utf-8"))
FORBIDDEN = {
    "legacy placeholder address": r"123\s+LV\s+Blvd",
    "wrong zip 89109": r"\b89109\b",
    "wrong zip 89101": r"\b89101\b",
    "old review count 2400": r"\b2,400\s+(google\s+)?reviews?\b|\b2400\s+(google\s+)?reviews?\b",
    "wrong artist count two": r"\btwo\s+(resident\s+artists|in-studio\s+artists|artists\s+in\s+studio)\b",
    "deprecated phone 725-224-2617": r"725[-\s.]224[-\s.]2617",
    "deprecated phone 725-224-2931": r"725[-\s.]224[-\s.]2931",
    "deprecated phone 725-260-6376": r"725[-\s.]260[-\s.]6376",
    "deprecated phone 702-960-9607": r"702[-\s.]960[-\s.]9607",
    "legacy email": r"Thewhiteknight702@gmail\.com",
    "tattoo/piercing contamination": r"where\s+do\s+you\s+(pierce|tattoo)\b|where\s+do\s+you\s+pierce\s+[^?<]{0,80}\btattoo\b|pierce\s+(fine[-\s]?line|realism|cover[-\s]?up)\s+tattoo",
}

def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return "/" if rel == Path("code.html") else "/" + str(rel.parent).strip("/") + "/"

def main() -> int:
    failures = []
    titles = {}
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        route = route_for(path)
        for label, pattern in FORBIDDEN.items():
            if re.search(pattern, text, re.I):
                failures.append(f"{path.relative_to(ROOT)}: forbidden pattern: {label}")
        soup = BeautifulSoup(text, "html.parser")
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
        if not soup.find("link", rel="canonical"):
            failures.append(f"{path.relative_to(ROOT)}: missing canonical")
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = script.string or script.get_text()
            if raw.strip():
                try:
                    json.loads(raw)
                except Exception as exc:
                    failures.append(f"{path.relative_to(ROOT)}: malformed JSON-LD: {exc}")
    if failures:
        print("SEO QA failed:")
        for f in failures[:250]:
            print("-", f)
        if len(failures) > 250:
            print(f"... {len(failures)-250} more failures")
        return 1
    print(f"SEO QA passed for {len(HTML_FILES)} HTML pages.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

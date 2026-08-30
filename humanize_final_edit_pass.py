#!/usr/bin/env python3
"""Final human copy pass: repair casing damage, remove SEO jargon from visible
copy, humanize breadcrumb labels, and fix truncated TOC labels sitewide.

Run from repo root: python3 humanize_final_edit_pass.py
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXCLUDE_PARTS = {"skipped_upload_build", "artists_raw", "obsidian_gold", ".git", "node_modules"}
EXCLUDE_NAMES = {"skipped_pages_clipboard.html"}


def target_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in EXCLUDE_PARTS for part in p.parts):
            continue
        if p.name in EXCLUDE_NAMES:
            continue
        files.append(p)
    return files


# ---------------------------------------------------------------------------
# 1. Casing repair: a bad lowercase pass turned "Piercing" into "piercing" in
#    headings, nav labels, page titles, and the brand name.
# ---------------------------------------------------------------------------
TITLE_WORDS = (
    "Guide", "Guides", "Jewelry", "Aftercare", "Healing", "Shop", "Tips",
    "Topics", "Authority", "Services", "Minors", "Specials", "Hub", "Standards",
)
CASING_RULES: list[tuple[str, str]] = []
for w in TITLE_WORDS:
    CASING_RULES.append((f"piercing {w}", f"Piercing {w}"))
CASING_RULES += [
    ("piercing Las Vegas |", "Piercing Las Vegas |"),
    ("Tattoo &amp; piercing", "Tattoo &amp; Piercing"),
    ("Tattoo & piercing", "Tattoo & Piercing"),
    ("Tattoos &amp; piercing", "Tattoos &amp; Piercing"),
    ("Tattoos & piercing", "Tattoos & Piercing"),
    (">piercing ", ">Piercing "),
    (">piercing,", ">Piercing,"),
    ('content="piercing ', 'content="Piercing '),
]

# ---------------------------------------------------------------------------
# 2. Visible SEO jargon, leaked internal notes, and robotic copy.
# ---------------------------------------------------------------------------
COPY_RULES: list[tuple[str, str]] = [
    # Geo pages: "NAP" is directory-listing jargon, not reader language.
    (">Studio NAP</p>", ">Studio address &amp; contact</p>"),
    # Henderson page spoke to Google, not to the reader.
    (
        "This page stays indexed because Henderson clients often plan larger tattoos around artist fit and repeat sessions.",
        "Most of our Henderson clients are planning bigger work — sleeves, cover-ups, multi-session projects — where picking the right artist matters more than picking the closest chair.",
    ),
    (
        "Green Valley is consolidated here so Henderson searchers get one stronger page instead of thin neighborhood duplicates.",
        "If you're coming from Green Valley, this is your page too — same studio, same team, one honest set of directions.",
    ),
    # Paradise page.
    (
        "This page exists to clarify the real studio location, not to claim a second storefront.",
        "To be clear: this is not a second storefront. Paradise is simply the real locality around our E. Tropicana address.",
    ),
    (
        "This is the exact city/locality context for the studio address, not a doorway page pretending to be another branch.",
        "Same studio, same rooms, same team — Paradise just happens to be the locality our address technically sits in.",
    ),
    # Near-the-Strip hub page.
    (
        "This hub helps Strip visitors plan a real tattoo or piercing appointment at Work of Art without relying on thin neighborhood doorway pages.",
        "This page helps Strip visitors plan a real tattoo or piercing appointment at Work of Art — honest directions, honest timing, no gimmicks.",
    ),
    (
        "Use the canonical studio address:",
        "Use the exact studio address:",
    ),
    # Official location page: internal directory-cleanup directive shown to readers.
    (
        "(725) 224-1240 only. Remove any legacy listing numbers that do not forward to this line.",
        "(725) 224-1240 — this is the only number that reaches the studio. Older numbers still floating around on directory sites do not forward to us.",
    ),
    # Strip-vs-studio comparison: self-praising framing.
    (
        "This authoritative comparison breaks down the systemic differences between a premier Las Vegas tattoo and piercing shop and the high-volume, low-cost storefronts lining the Strip.",
        "Here is an honest breakdown of how a dedicated Las Vegas studio differs from the high-volume storefronts lining the Strip \u2014 and why that difference shows up on your skin years later.",
    ),
    # Pain chart intro: "authoritative analysis ... for the modern collector".
    (
        "An authoritative analysis of dermal sensitivity, nerve density, and pain management strategies for the modern collector. Precision artistry meets biological understanding.",
        "A straight answer to the question every client asks: where does it hurt most, why, and what we do in the chair to make the tougher spots manageable.",
    ),
    # Walk-in page footer tagline.
    (
        "Elevating the Vegas tattoo experience through clinical precision and healed portfolio work.",
        "Custom tattoos and piercings, a consult-first approach, and healed work to back it up.",
    ),
    # Pricing page badge.
    ("5.0 Star Rated Excellence", "5.0-Star Google Rating"),
    # Typos.
    ("with clearance and a adjusted plan", "with clearance and an adjusted plan"),
    ("rescue plan ( prescribed cream)", "rescue plan (a prescribed cream)"),
]

# ---------------------------------------------------------------------------
# 3. Breadcrumb pill labels: raw slugs like "eczema skin science las vegas"
#    become readable titles derived from the page's own directory.
# ---------------------------------------------------------------------------
PILL_RE = re.compile(r'(<span class="woa-guide-pill-current-label">)([^<]*)(</span>)')
SMALL_WORDS = {"a", "an", "and", "the", "of", "vs", "in", "for", "to", "on", "with", "near", "at", "by", "or"}
SPECIAL = {
    "unlv": "UNLV", "mgm": "MGM", "nv": "NV", "faq": "FAQ", "llc": "LLC",
    "tmobile": "T-Mobile", "ai": "AI", "geo": "GEO", "nap": "NAP", "qa": "Q&A",
}
TRAILING_NOISE = [
    "las vegas authority guide", "master authority guide", "ultimate authority guide",
    "authority guide", "authority hub", "nap corrected", "geo seo optimized",
    "las vegas", "las", "vegas",
]


def human_label(dirname: str) -> str:
    words = dirname.replace("_", " ").replace("-", " ").strip().lower()
    changed = True
    while changed:
        changed = False
        for noise in TRAILING_NOISE:
            if words.endswith(" " + noise):
                words = words[: -len(noise) - 1].rstrip()
                changed = True
    out = []
    for i, w in enumerate(words.split()):
        if w in SPECIAL:
            out.append(SPECIAL[w])
        elif w in SMALL_WORDS and i != 0:
            out.append(w)
        else:
            out.append(w.capitalize())
    return " ".join(out)


def fix_pill(path: Path, text: str, counts: Counter) -> str:
    if path.parent == ROOT or path.parent.name == "artists_build":
        return text

    def repl(m: re.Match) -> str:
        current = m.group(2).strip()
        # Only replace labels that are raw slug text (all lowercase).
        if current and current != current.lower():
            return m.group(0)
        label = human_label(path.parent.name)
        if not label:
            return m.group(0)
        counts["breadcrumb"] += 1
        return m.group(1) + label + m.group(3)

    return PILL_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# 4. TOC labels truncated mid-word by an old [:28] slice.
# ---------------------------------------------------------------------------
TOC_LINK_RE = re.compile(r'(<a class="text-secondary underline hover:no-underline text-sm" href="#([a-z0-9-]+)">)([^<]+)(</a>)')
HEADING_ID_RE = r'id="{aid}"[^>]*>\s*(?:<h[23][^>]*>)?([^<]+)<'


def fix_toc(text: str, counts: Counter) -> str:
    def repl(m: re.Match) -> str:
        aid, label = m.group(2), m.group(3)
        hm = re.search(HEADING_ID_RE.format(aid=re.escape(aid)), text, re.S)
        if not hm:
            return m.group(0)
        full = hm.group(1).split("\u2014")[0].strip()
        if full and full != label and full[:28].strip() == label.strip() and len(full) <= 60:
            counts["toc"] += 1
            return m.group(1) + full + m.group(4)
        return m.group(0)

    return TOC_LINK_RE.sub(repl, text)


def main() -> None:
    counts: Counter = Counter()
    touched = 0
    for path in target_files():
        original = path.read_text(encoding="utf-8")
        text = original
        for old, new in CASING_RULES:
            n = text.count(old)
            if n:
                counts[f"casing: {old[:40]}"] += n
                text = text.replace(old, new)
        for old, new in COPY_RULES:
            n = text.count(old)
            if n:
                counts[f"copy: {old[:50]}"] += n
                text = text.replace(old, new)
        text = fix_pill(path, text, counts)
        text = fix_toc(text, counts)
        if text != original:
            path.write_text(text, encoding="utf-8")
            touched += 1
    print(f"Touched {touched} files")
    for key, n in sorted(counts.items()):
        print(f"{n:6d}  {key}")


if __name__ == "__main__":
    main()

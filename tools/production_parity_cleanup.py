#!/usr/bin/env python3
"""Last-step production parity cleanup.

Fixes the homepage that actually ships to GitHub Pages, public booking email,
unverified footer credential claims, and cover-up internal links.

This must run AFTER prepare_site_deploy.py injectors and a_plus_cleanup.py.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", "skipped_upload_build", "audits", "tools", "artists_raw"}
PUBLIC_EMAIL = "booking@workofarttattoo.com"
LEGACY_COVER = "/cover_up_tattoos_las_vegas_master_authority_guide/"
CLEAN_COVER = "/cover-up-tattoos-las-vegas/"
GMAILS = ("thewhiteknight702@gmail.com", "kmorgen14@gmail.com")

SNHD_RE = re.compile(
    r'<div class="mt-10 pt-8 border-t border-outline-variant/10 max-w-3xl">\s*'
    r'<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-\[11px\]">(?:Licensed(?: &amp;|&) Permitted|Studio)</h5>\s*'
    r'<p class="mt-3 text-on-surface-variant text-\[13px\] font-body-md leading-relaxed">[^<]*'
    r"(?:Southern Nevada Health District|Body Art Card|OSHA bloodborne|Work of Art Tattoo)[^<]*</p>\s*</div>",
    re.I,
)
STUDIO_NAP_BLOCK_RE = re.compile(
    r'<div class="mt-10 pt-8 border-t border-outline-variant/10 max-w-3xl"(?:\s[^>]*)?>\s*'
    r'<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-\[11px\]">Studio</h5>\s*'
    r'<p class="mt-3 text-on-surface-variant text-\[13px\] font-body-md leading-relaxed">'
    r"Work of Art Tattoo &amp; Piercing<br/>2375 E\. Tropicana Ave, Suite 3<br/>"
    r"Las Vegas, NV 89119<br/>[\s\S]*?Daily 12 PM–12 AM</p>\s*</div>",
    re.I,
)
NAP_INLINE_BLOCK_RE = re.compile(
    r'<div class="mt-10 pt-8 border-t border-outline-variant/10 max-w-3xl"(?:\s[^>]*)?>\s*'
    r'<h5 class="font-label-caps text-on-surface uppercase tracking-widest text-\[11px\]">Studio</h5>\s*'
    r'<p class="mt-3 text-on-surface-variant text-\[13px\] font-body-md leading-relaxed">'
    r"Work of Art Tattoo &amp; Piercing — 2375 E\. Tropicana Ave, Suite 3, Las Vegas, NV 89119 "
    r"— \(725\) 224-1240 — booking@workofarttattoo\.com — Daily 12 PM–12 AM\.</p>\s*</div>",
    re.I,
)

HREF_LEGACY_RE = re.compile(
    r'href="(?:https://(?:www\.)?workofarttattoo\.com)?/cover_up_tattoos_las_vegas_master_authority_guide/"'
)

TERALYN_CARD = """<a class="group text-center" href="/artists/teralyn/">
<div class="aspect-[3/4] bg-surface-container mb-4 overflow-hidden relative border border-outline-variant/30">
<picture><source sizes="(max-width: 768px) 50vw, 350px" srcset="/artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas-400.webp 400w, /artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas.webp 800w" type="image/webp"/><img alt="Teralyn — tattoo artist and piercer, Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105" decoding="async" height="1067" loading="lazy" src="/artists/teralyn/teralyn-fine-line-tattoo-artist-las-vegas.jpg" width="800"/></picture>
<div class="absolute inset-0 bg-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
</div>
<span class="font-label-caps text-label-caps text-on-surface group-hover:text-secondary transition-colors block">Teralyn</span>
<span class="font-body-md text-[13px] text-on-surface-variant block mt-1">Tattoo Artist &amp; Piercer</span>
<a class="font-body-md text-[12px] text-secondary hover:underline block mt-2" href="https://www.instagram.com/mischiefmodifies/" rel="noopener noreferrer" target="_blank">@mischiefmodifies</a>
</a>
"""

HOMEPAGE_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Two resident specialists in-studio today — Joshua Cole (tattoo &amp; piercing; studio lead) and Katelyn Cole (professional piercer). Tattoo and piercing consults book seven nights a week at 2375 E. Tropicana Suite 3.",
        "Three in-studio residents today — Joshua Cole (tattoo artist and studio lead; also offers piercing), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fine line, floral, script, custom drawings, and detailed smaller tattoos). Tattoo and piercing consults book at 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "Two resident specialists in-studio today — Joshua Cole (tattoo & piercing; studio lead) and Katelyn Cole (professional piercer). Tattoo and piercing consults book seven nights a week at 2375 E. Tropicana Suite 3.",
        "Three in-studio residents today — Joshua Cole (tattoo artist and studio lead; also offers piercing), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fine line, floral, script, custom drawings, and detailed smaller tattoos). Tattoo and piercing consults book at 2375 E. Tropicana Ave, Suite 3.",
    ),
    ("2 In-Studio Specialists", "3 In-Studio Residents"),
    ("Meet Our Tattoo and piercing Shop Near Me Team", "Meet Our Las Vegas Tattoo and Piercing Team"),
    ("Meet Our Tattoo and Piercing Shop Near Me Team", "Meet Our Las Vegas Tattoo and Piercing Team"),
    (
        "Joshua Cole leads tattoo, piercing, and training; Katelyn Cole is our professional piercer — two resident specialists in-studio today with appointments open seven nights a week.",
        "Joshua Cole leads tattoo work and also offers piercing; Katelyn Cole is our professional piercer; Teralyn tattoos and pierces, including fine line, floral, script, and detailed smaller tattoos.",
    ),
    ("Joshua Cole and Joshua Cole", "Joshua Cole"),
    ("museum-level tattoos", "custom tattoo work"),
    ("museum-quality work", "custom tattoo work"),
    ("hospital-level sterilization", "a clean studio process"),
    ("Hospital-grade sterilization", "Clean studio practices"),
    ("Hospital-grade sterilization and single-use equipment are our baseline. We maintain the cleanest environment in Las Vegas.", "We use a clean studio process and single-use equipment."),
    ("elite artistry", "experienced artists"),
    ("clinical standards", "clean studio practices"),
    ("clinical precision", "careful placement"),
    ("master piercer", "professional piercer"),
    ("Master Piercer", "Professional Piercer"),
    ("medical-grade hygiene", "clean studio"),
    ("Body Piercing Store Near Me — Ear &amp; Helix", "Ear and Body Piercing in Las Vegas"),
    ("Body Piercing Store Near Me", "Ear and body piercing in Las Vegas"),
    ("Tattoo Body Piercing Near Me — Las Vegas", "Tattoo and Piercing in Las Vegas"),
    ("Tattoo Body Piercing Near Me", "tattoo and piercing in Las Vegas"),
    ("<strong>body piercing store near me</strong>", "tattoo and piercing studio in Las Vegas"),
    ("<strong>Tattoo body piercing near me</strong>", "A tattoo and piercing studio on E. Tropicana Ave"),
    ("<strong>ear and body piercing at Work of Art</strong>", "tattoo and piercing studio in Las Vegas"),
    ("<strong>tattoo and piercing at Work of Art</strong>", "A tattoo and piercing studio on E. Tropicana Ave"),
    ("Our body piercing shop near me on E. Tropicana", "Our studio on E. Tropicana Ave"),
    ("Why Locals Choose This Tattoo and piercing Shop Near Me", "Why Locals Choose This Tattoo and Piercing Studio"),
    ("Why Locals Choose This Tattoo and Piercing Shop Near Me", "Why Locals Choose This Tattoo and Piercing Studio"),
    ("Work of Art is the tattoo and piercing shop near me locals trust for", "Work of Art is the local tattoo and piercing studio collectors use for"),
    ("What tattoo and piercing shops in near me are worth it in Vegas?", "Which Las Vegas tattoo and piercing studios are worth a visit?"),
    ("tattoo and piercing shop near me pick just minutes from the Strip", "tattoo and piercing studio near the Las Vegas Strip"),
    ("the tattoo and piercing shop near me pick", "a tattoo and piercing studio near the Las Vegas Strip"),
    ("tattoo and body piercing studio near me", "tattoo and piercing studio in Las Vegas"),
    ("tattoo and piercing shops in near me", "tattoo and piercing studios near the Las Vegas Strip"),
    ("body piercings and tattoos near me", "tattoos and piercings in one studio"),
    ("black and grey tattoo artist near me", "black and grey tattoo artist in Las Vegas"),
    ("realism tattoo artist near me", "realism tattoo artist in Las Vegas"),
    ("piercing shops near me", "piercing studios in Las Vegas"),
    ("body piercing shop near me", "piercing studio in Las Vegas"),
    ("tattoo and piercing shop near by me", "tattoo and piercing studio in Las Vegas"),
    ("tattoo and piercing shop near me", "tattoo and piercing studio in Las Vegas"),
    ("studio tattoo near me", "tattoo studio in Las Vegas"),
    ("tattoos studio near me", "tattoo studio in Las Vegas"),
    ("nearest tattoo and piercing shop to me", "nearby tattoo and piercing studio"),
    ("What are the best tattoo and body piercing studios in Las Vegas?", "How do you choose a tattoo and piercing studio in Las Vegas?"),
    ("Who does the best realism tattoo in Las Vegas?", "Who does realism tattoo work at Work of Art?"),
    ("Best female piercers in Las Vegas?", "Who does piercing at Work of Art?"),
    ("What tattoo and piercing shop near me is best near the Las Vegas Strip?", "Where is Work of Art relative to the Las Vegas Strip?"),
    ("<strong>tattoo and body piercing studios in las vegas</strong>", "tattoo and piercing studios in Las Vegas"),
    ("<strong>tattoo and body piercing studio las vegas</strong>", "tattoo and piercing studio in Las Vegas"),
    ("<strong>tattoo and body piercing studio in las vegas</strong>", "tattoo and piercing studio in Las Vegas"),
    (
        "Tattoo and piercing Shop Near Me | Las Vegas | Work of Art",
        "Tattoo and Piercing Studio in Las Vegas | Work of Art",
    ),
    (
        "Where is a tattoo and piercing studio in Las Vegas or tattoo studio in Las Vegas in Vegas?",
        "Where is Work of Art in Las Vegas?",
    ),
    (
        "Where can I find a black and grey tattoo artist in Las Vegas in Vegas?",
        "Where can I find a black and grey tattoo artist in Las Vegas?",
    ),
    (
        "What piercing studios in Las Vegas are safe in Vegas?",
        "What should I look for in a Las Vegas piercing studio?",
    ),
    (
        "What tattoo and piercing studio in Las Vegas is best near the Las Vegas Strip?",
        "Where is Work of Art relative to the Las Vegas Strip?",
    ),
    (
        "What is the nearby tattoo and piercing studio from the Las Vegas Strip?",
        "How close is Work of Art to the Las Vegas Strip?",
    ),
    ("under the same licensed roof", "under the same roof"),
    (
        "same team as our tattoo and piercing studio in Las Vegas listings, with <strong>tattoo studio in Las Vegas</strong> convenience",
        "same team for east-Strip and UNLV-area visits, with one-studio convenience",
    ),
    (
        "tattoo and piercing studio in Las Vegas quality at 2375 E. Tropicana",
        "custom tattoo work and piercing consultations at 2375 E. Tropicana Ave",
    ),
    (
        "tattoo and piercing studio in Las Vegas quality without strip-mall shortcuts",
        "portfolios you can review before you book, without strip-mall shortcuts",
    ),
    (
        'href="https://www.instagram.com/stabislifee/?utm_source=instagram&amp;utm_medium=organic_social&amp;utm_campaign=katelyn_portfolio" rel="noopener noreferrer" target="_blank">Instagram — Joshua @stabislifee</a>',
        'href="https://www.instagram.com/workofarttattoo/?utm_source=instagram&amp;utm_medium=organic_social&amp;utm_campaign=joshua_portfolio" rel="noopener noreferrer" target="_blank">Instagram — Joshua @workofarttattoo</a>',
    ),
    (
        'href="https://www.instagram.com/workofarttattoo/?utm_source=instagram&amp;utm_medium=organic_social&amp;utm_campaign=joshua_portfolio" rel="noopener noreferrer" target="_blank">Instagram — Katelyn / Studio @workofarttattoo</a>',
        'href="https://www.instagram.com/stabislifee/?utm_source=instagram&amp;utm_medium=organic_social&amp;utm_campaign=katelyn_portfolio" rel="noopener noreferrer" target="_blank">Instagram — Katelyn @stabislifee</a>',
    ),
]

ARTISTS_INDEX_REPLACEMENTS = [
    (
        "Two resident specialists in-studio today at 2375 E. Tropicana Suite 3 — tattoo, piercing, and custom consults. No placeholder roster slots: everyone listed below books real sessions.",
        "Three in-studio residents at 2375 E. Tropicana Ave, Suite 3 — Joshua Cole, Katelyn Cole, and Teralyn. No placeholder roster slots: everyone listed below books real sessions.",
    ),
]

WALK_IN_REPLACEMENTS: list[tuple[str, str]] = [
    ("TWO RESIDENT SPECIALISTS", "3 IN-STUDIO RESIDENTS"),
    ("Two resident specialists", "Three in-studio residents"),
    ("two resident specialists", "three in-studio residents"),
]

REVIEW_COUNT_REPLACEMENTS: list[tuple[str, str]] = [
    ("5.0 RATING (480+ REVIEWS)", "5.0 RATING (323 REVIEWS)"),
    ("5.0 RATING (480 + REVIEWS)", "5.0 RATING (323 REVIEWS)"),
    ("5.0 RATING (hundreds of Google reviews)", "5.0 RATING (323 Google reviews)"),
    ("hundreds of Google reviews, 5.0 RATING", "323 Google reviews, 5.0 RATING"),
    ("Hundreds of Google Reviews", "323 Google Reviews"),
    ("hundreds of Google reviews", "323 Google reviews"),
    ("480+ REVIEWS", "323 REVIEWS"),
    ("480+ reviews", "323 reviews"),
    ("480+ Google reviews", "323 Google reviews"),
]


def iter_html() -> list[Path]:
    out = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def replace_public_email(text: str) -> str:
    for gmail in GMAILS:
        text = text.replace(gmail, PUBLIC_EMAIL)
    text = text.replace("Joshua Cole and Joshua Cole", "Joshua Cole")
    text = text.replace("Joshua Cole or Joshua Cole", "Joshua Cole")
    return text


def rewrite_cover_hrefs(text: str) -> str:
    text = HREF_LEGACY_RE.sub(f'href="{CLEAN_COVER}"', text)
    text = re.sub(
        r'(href=["\'])(?:https://(?:www\.)?workofarttattoo\.com)?/cover_up_tattoos_las_vegas_master_authority_guide/?(["\'])',
        rf"\1{CLEAN_COVER}\2",
        text,
    )
    return text


CLAIMS_SENTENCE_RE = re.compile(
    r"Work of Art(?: Tattoo(?: &amp;| &) [Pp]iercing)? operates under a Southern Nevada Health District body art\s+establishment Health Permit[.,]?\s*"
    r"(?:and\s+)?(?:[Aa]ll artists hold|[Ee]very artist maintains) a current Body Art Card"
    r"(?:\s+(?:plus|and)\s+(?:OSHA )?bloodborne pathogens (?:certification|training))?\.",
    re.S,
)
BEST_OF_PLACEHOLDER_RE = re.compile(
    r"\s*Work of Art has been recognized with Best of\s+Vegas awards in both 2025 and 2026 \[insert issuing publication once confirmed\s+from the plaque\]\.",
    re.S,
)
NAP_SENTENCE = (
    "Work of Art Tattoo &amp; Piercing — 2375 E. Tropicana Ave, Suite 3, Las Vegas, NV 89119 "
    "— (725) 224-1240 — booking@workofarttattoo.com — Daily 12 PM–12 AM."
)


def dedupe_nap_footer_blocks(text: str) -> str:
    """Keep one Studio NAP contact block; remove repeated footer injections."""
    matches = list(STUDIO_NAP_BLOCK_RE.finditer(text))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            text = text[: match.start()] + text[match.end() :]
    # Drop redundant one-line NAP when the formatted block already exists.
    if STUDIO_NAP_BLOCK_RE.search(text):
        text = NAP_INLINE_BLOCK_RE.sub("", text)
    return text


def strip_snhd_footer(text: str) -> str:
    # Remove unverified credential blocks instead of stacking another Studio NAP block.
    text = SNHD_RE.sub("", text)
    text = BEST_OF_PLACEHOLDER_RE.sub("", text)
    text = text.replace(" · Southern Nevada Health District Permitted", "")
    text = text.replace(" · Southern Nevada Health District permitted", "")
    text = text.replace(">Licensed &amp; Permitted<", ">Studio<")
    text = text.replace(">Licensed & Permitted<", ">Studio<")
    text = text.replace("current Body Art Card", "studio sanitation training")
    text = text.replace("OSHA bloodborne pathogens certification", "studio sanitation procedures")
    return dedupe_nap_footer_blocks(text)


def add_teralyn_card(text: str) -> str:
    """Add Teralyn only inside #meet-our-artists, never the #gallery roster."""
    section_start = text.find('id="meet-our-artists"')
    if section_start == -1:
        return text
    section_end = text.find("</section>", section_start)
    if section_end == -1:
        return text
    section = text[section_start:section_end]
    if 'href="/artists/teralyn/"' in section:
        return text
    marker = (
        '<span class="font-label-caps text-label-caps text-on-surface group-hover:text-secondary '
        'transition-colors block">Katelyn Cole</span>'
    )
    rel = section.find(marker)
    if rel == -1:
        return text
    close = section.find("</a>", rel)
    if close == -1:
        return text
    close += 4
    new_section = section[:close] + "\n" + TERALYN_CARD + section[close:]
    return text[:section_start] + new_section + text[section_end:]


def add_teralyn_footer_link(text: str) -> str:
    old = '<li class=""><a class="hover:text-secondary transition-colors" href="/artists/katelyn-cole/">Katelyn Cole</a></li>'
    new = (
        old
        + '\n<li class=""><a class="hover:text-secondary transition-colors" href="/artists/teralyn/">Teralyn</a></li>'
    )
    if 'href="/artists/teralyn/">Teralyn</a>' not in text:
        text = text.replace(old, new, 1)
    return text


def add_teralyn_nav_if_missing(text: str) -> str:
    if "/artists/teralyn/" in text:
        return text
    needle = 'href="/artists/katelyn-cole/">Katelyn Cole — Professional Piercer</a>'
    extra = (
        '<a class="block px-3 py-2 text-[13px] leading-snug text-on-surface hover:text-secondary transition-colors" '
        'href="/artists/teralyn/">Teralyn — Tattoos &amp; Piercing</a>'
    )
    if needle in text:
        text = text.replace(needle, needle + extra)
    mobile = (
        'href="/artists/katelyn-cole/">Katelyn Cole — Professional Piercer</a>'
    )
    return text


def ensure_homepage_deploy_audit(text: str) -> str:
    if "Three in-studio residents" not in text and "3 In-Studio Residents" not in text:
        needle = "Our in-studio team includes Joshua Cole"
        if needle in text:
            text = text.replace(
                needle,
                "Three in-studio residents today — our in-studio team includes Joshua Cole",
                1,
            )
    if PUBLIC_EMAIL not in text:
        text = text.replace(
            'href="tel:+17252241240">(725) 224-1240</a></li>\n',
            'href="tel:+17252241240">(725) 224-1240</a></li>\n'
            f'<li class=""><a class="hover:text-secondary transition-colors" href="mailto:{PUBLIC_EMAIL}">{PUBLIC_EMAIL}</a></li>\n',
            1,
        )
    return text


def fix_homepage(text: str) -> str:
    for old, new in HOMEPAGE_REPLACEMENTS:
        text = text.replace(old, new)
    text = add_teralyn_card(text)
    text = add_teralyn_footer_link(text)
    text = add_teralyn_nav_if_missing(text)
    text = ensure_homepage_deploy_audit(text)
    return text


def fix_walk_in_copy(text: str) -> str:
    for old, new in WALK_IN_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def fix_review_counts(text: str, path: Path) -> str:
    scoped = (
        "walk_in_tattoos_las_vegas_authority_guide" in path.as_posix()
        or "walk-in-tattoos-las-vegas" in path.as_posix()
        or "home_work_of_art_tattoo_piercing" in path.as_posix()
        or path.name in {"code.html", "index.html"} and path.parent == ROOT
    )
    if not scoped:
        return text
    for old, new in REVIEW_COUNT_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def fix_katelyn_grammar(text: str) -> str:
    replacements = {
        "she has focuses": "she focuses",
        "Katelyn has uses": "Katelyn uses",
        "clean studio process for clean studio process": "clean studio process",
        "careful placement in a Luxury Environment": "Clean studio practices",
        "Professional Piercer in Las Vegas\" by a loyal clientele": "professional piercer\" by clients",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def protect_canonical_cover_page(path: Path, text: str) -> str:
    """The clean cover-up URL must stay indexable. Never inherit the stub's noindex/refresh."""
    if "cover-up-tattoos-las-vegas" not in path.as_posix():
        return text
    if "cover_up_tattoos_las_vegas_master_authority_guide" in path.as_posix():
        return text
    text = re.sub(
        r'\s*<meta content="0;url=/cover-up-tattoos-las-vegas/" http-equiv="refresh"/>',
        "",
        text,
        count=1,
        flags=re.I,
    )
    text = re.sub(
        r'<meta content="noindex,\s*follow" name="robots"/>',
        '<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>',
        text,
        count=1,
        flags=re.I,
    )
    return text


def neutralize_legacy_cover_page(path: Path, text: str) -> str:
    if "cover_up_tattoos_las_vegas_master_authority_guide" not in path.as_posix():
        return text
    text = re.sub(
        r'<meta content="index, follow[^"]*" name="robots"/>',
        '<meta content="noindex, follow" name="robots"/>',
        text,
        count=1,
    )
    if 'http-equiv="refresh"' not in text.lower():
        text = text.replace(
            "<head>",
            '<head>\n<meta http-equiv="refresh" content="0;url=/cover-up-tattoos-las-vegas/"/>',
            1,
        )
    if 'rel="canonical"' not in text and "rel='canonical'" not in text:
        text = text.replace(
            "<head>",
            '<head>\n<link href="https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/" rel="canonical"/>',
            1,
        )
    else:
        text = re.sub(
            r'<link href="[^"]*cover_up_tattoos_las_vegas_master_authority_guide/?" rel="canonical"/>',
            '<link href="https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/" rel="canonical"/>',
            text,
        )
    return text


def patch_business_json() -> None:
    path = ROOT / "siteData" / "business.json"
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("bookingEmail") != PUBLIC_EMAIL:
        data["bookingEmail"] = PUBLIC_EMAIL
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"[ok] {path.relative_to(ROOT)}")


def main() -> int:
    changed = []
    homepage_names = {
        ROOT / "code.html",
        ROOT / "index.html",
        ROOT / "home_work_of_art_tattoo_piercing" / "code.html",
        ROOT / "home_work_of_art_tattoo_piercing" / "index.html",
    }
    walk_in_markers = (
        "walk_in_tattoos_las_vegas_authority_guide",
        "walk-in-tattoos-las-vegas",
    )
    katelyn_markers = (
        "artists/katelyn-cole/",
        "artists_build/katelyn-cole.html",
    )
    for path in iter_html():
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = raw
        if path in homepage_names or path.name in {"code.html", "index.html"} and "home_work_of_art" in path.as_posix():
            text = fix_homepage(text)
        if any(marker in path.as_posix() for marker in walk_in_markers):
            text = fix_walk_in_copy(text)
        if any(marker in path.as_posix() for marker in katelyn_markers):
            text = fix_katelyn_grammar(text)
        if path.as_posix().endswith("artists/index.html") or path.as_posix().endswith("artists/code.html"):
            for old, new in ARTISTS_INDEX_REPLACEMENTS:
                text = text.replace(old, new)
        text = fix_review_counts(text, path)
        text = replace_public_email(text)
        text = rewrite_cover_hrefs(text)
        text = strip_snhd_footer(text)
        text = neutralize_legacy_cover_page(path, text)
        text = protect_canonical_cover_page(path, text)
        text = dedupe_nap_footer_blocks(text)
        if text != raw:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    patch_business_json()

    # Keep root code.html aligned with the homepage export after edits.
    home = ROOT / "home_work_of_art_tattoo_piercing" / "code.html"
    root_code = ROOT / "code.html"
    if home.is_file():
        root_code.write_text(home.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Updated {len(changed)} HTML files")
    for rel in changed[:40]:
        print(rel)
    if len(changed) > 40:
        print(f"... +{len(changed) - 40} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

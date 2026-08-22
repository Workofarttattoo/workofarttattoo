#!/usr/bin/env python3
"""Final human-voice cleanup after generated sections are rebuilt."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("<title>Work of Art Tattoo &amp; Piercing — Official Location, Hours &amp; Contact | Work of Art</title>", "<title>Work of Art Tattoo &amp; Piercing — Location &amp; Hours</title>"),
    ("<title>Choosing a Tattoo Artist — Joshua Cole | Work of Art Las Vegas | Work of Art</title>", "<title>Choosing a Tattoo Artist — Joshua Cole | Work of Art</title>"),
    ("Verified Social Proof", "Client reviews"),
    ("LAS VEGAS' HIGHEST RATED WALK-IN STUDIO", "323 GOOGLE REVIEWS, 5.0 RATING"),
    ("Real Google Reviews — Las Vegas Collectors", "Real Google reviews from people who booked here"),
    ("Strategic Insights", "Quick answers"),
    ("Frequently Asked Artistry Questions", "Questions people ask before they book"),
    ("Polished, client-ready pieces from our Las Vegas portfolio.", "Real client work from the studio, photographed so you can see the style before you book."),
    ("Joshua — tattoo later upon request", "Joshua — tattoo availability by request"),
    ("official location hours contact", "Official Location & Hours"),
    ("helix piercing las vegas", "Helix Piercing Guide"),
    ("tattoo shop near mgm grand las vegas", "Near MGM Grand"),
    ("tattoo shop near allegiant stadium las…", "Near Allegiant Stadium"),
    ("tattoo shop near allegiant stadium las vegas", "Near Allegiant Stadium"),
    ("tattoo shop near las vegas airport", "Near Las Vegas Airport"),
    ("tattoo shop near the sphere las vegas", "Near the Sphere"),
    ("tattoo shop paradise nevada", "Paradise, NV"),
    ("tattoo shop spring valley las vegas", "Spring Valley"),
    ("tattoo shop enterprise las vegas", "Enterprise"),
    ("tattoo shop green valley henderson", "Green Valley / Henderson"),
    ("how to choose a tattoo artist  2", "How to Choose a Tattoo Artist"),
)

STICKY_LINK_RE = re.compile(
    r'<a\b(?=[^>]*\bdata-woa-sticky-book="1")[^>]*>.*?</a>\s*',
    re.DOTALL,
)


def polish_text(html: str) -> str:
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    return html


def dedupe_sticky_links(html: str) -> str:
    links = STICKY_LINK_RE.findall(html)
    if len(links) <= 1:
        return html
    keep = links[-1].strip() + "\n"
    html = STICKY_LINK_RE.sub("", html)
    if "</body>" in html:
        return html.replace("</body>", keep + "</body>", 1)
    return html + keep


def ensure_home_canonical(path: Path, html: str) -> str:
    is_home = path.name == "code.html" and path.parent in {
        ROOT,
        ROOT / "home_work_of_art_tattoo_piercing",
    }
    if not is_home or 'rel="canonical"' in html:
        return html
    canonical = '<link href="https://www.workofarttattoo.com/" rel="canonical"/>\n'
    if "</title>" in html:
        return html.replace("</title>", "</title>\n" + canonical, 1)
    if "</head>" in html:
        return html.replace("</head>", canonical + "</head>", 1)
    return html


def ensure_known_canonicals(path: Path, html: str) -> str:
    if 'rel="canonical"' in html:
        return html
    slug = path.parent.name if path.name == "code.html" else ""
    known = {
        "fine_line_tattoos_las_vegas_master_authority_guide": (
            "https://www.workofarttattoo.com/fine_line_tattoos_las_vegas_master_authority_guide/"
        ),
    }
    href = known.get(slug)
    if not href:
        return html
    canonical = f'<link href="{href}" rel="canonical"/>\n'
    if "</title>" in html:
        return html.replace("</title>", "</title>\n" + canonical, 1)
    if "</head>" in html:
        return html.replace("</head>", canonical + "</head>", 1)
    return html


KNOWN_DESCRIPTIONS: dict[str, str] = {
    "best_tattoo_styles_for_sleeves_large_scale_project_hub": (
        "Plan a sleeve or large-scale tattoo in Las Vegas with session pacing, style fit, "
        "reference prep, and artist guidance from Work of Art Tattoo & Piercing."
    ),
    "tattoo_pain_chart_placement_sensitivity_guide": (
        "Tattoo pain chart for common placements, session planning, and comfort tips from "
        "Work of Art Tattoo & Piercing in Las Vegas."
    ),
}


def _insert_after_title_or_head(html: str, tag: str) -> str:
    if "</title>" in html:
        return html.replace("</title>", "</title>\n" + tag, 1)
    if "</head>" in html:
        return html.replace("</head>", tag + "</head>", 1)
    return html


def ensure_basic_seo_head(path: Path, html: str) -> str:
    if path.name != "code.html":
        return html
    rel = path.parent.relative_to(ROOT)
    if len(rel.parts) != 1:
        return html
    slug = rel.parts[0]
    if slug.startswith(".") or slug in {"__pycache__", "artists_build"}:
        return html

    if 'rel="canonical"' not in html:
        canonical = f'<link href="https://www.workofarttattoo.com/{slug}/" rel="canonical"/>\n'
        html = _insert_after_title_or_head(html, canonical)

    if 'name="description"' not in html:
        description = KNOWN_DESCRIPTIONS.get(slug)
        if not description:
            title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
            title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else slug.replace("_", " ").title()
            title = re.sub(r"\s*\|\s*Work of Art.*$", "", title)
            description = (
                f"{title} from Work of Art Tattoo & Piercing in Las Vegas. "
                "Clear studio guidance, booking context, and real artist perspective."
            )
        description = description.replace('"', "&quot;")
        meta = f'<meta content="{description}" name="description"/>\n'
        html = _insert_after_title_or_head(html, meta)

    if 'name="robots"' not in html:
        robots = '<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>\n'
        if '<meta charset="utf-8"/>' in html:
            html = html.replace('<meta charset="utf-8"/>', '<meta charset="utf-8"/>\n' + robots, 1)
        else:
            html = _insert_after_title_or_head(html, robots)

    return html


def main() -> int:
    changed = 0
    targets = list(ROOT.rglob("code.html")) + list((ROOT / "artists_build").glob("*.html"))
    root_home = ROOT / "code.html"
    if root_home.is_file():
        targets.append(root_home)
    for path in sorted(set(targets)):
        if "skipped" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8")
        updated = ensure_basic_seo_head(
            path,
            ensure_known_canonicals(
                path,
                ensure_home_canonical(path, dedupe_sticky_links(polish_text(raw))),
            ),
        )
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"[ok] final copy polish updated {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

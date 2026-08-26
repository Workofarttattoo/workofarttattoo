#!/usr/bin/env python3
"""Install Katelyn's real piercing portfolio into matching site pages.

This script is idempotent. It expects optimized WEBP assets in:
  artists/katelyn-cole/piercing-portfolio/

It replaces the incorrect tattoo-image grids on Katelyn's profile, adds a real
piercing gallery to the main piercing guide, and adds placement-specific photo
sections to matching existing HTML pages when those pages are present in the
repository. It never creates SEO landing pages or invents placement claims.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "artists" / "katelyn-cole" / "piercing-portfolio"
WEB_ROOT = "/artists/katelyn-cole/piercing-portfolio"
MARKER_START = "<!-- WOA_KATELYN_PIERCING_PHOTOS_START -->"
MARKER_END = "<!-- WOA_KATELYN_PIERCING_PHOTOS_END -->"


def assets(prefix: str | tuple[str, ...]) -> list[Path]:
    prefixes = (prefix,) if isinstance(prefix, str) else prefix
    return sorted(
        p for p in ASSET_DIR.glob("*.webp")
        if any(p.name.startswith(x) for x in prefixes)
    )


def alt_for(path: Path) -> str:
    n = path.stem
    if "katelyn-professional-piercer" in n:
        return "Katelyn, professional piercer at Work of Art Tattoo & Piercing in Las Vegas"
    labels = [
        ("nostril", "Nostril piercing"),
        ("septum", "Septum piercing"),
        ("earlobe", "Ear lobe piercing"),
        ("helix", "Helix piercing"),
        ("ear-cartilage", "Ear cartilage piercing"),
        ("upper-ear", "Upper ear piercing"),
        ("curated-ear", "Curated ear piercings"),
        ("navel", "Navel piercing"),
        ("lip-labret", "Lip and labret piercing"),
        ("lip-nostril", "Facial piercing"),
        ("cheek", "Cheek piercing"),
        ("tongue", "Tongue piercing appointment"),
        ("ear-piercing-process", "Ear piercing appointment"),
        ("piercing-process", "Piercing appointment with Katelyn"),
        ("piercing-client", "Piercing client at Work of Art Tattoo & Piercing"),
        ("portfolio-mixed", "Piercing portfolio work by Katelyn"),
    ]
    for key, label in labels:
        if key in n:
            return f"{label} by Katelyn at Work of Art Tattoo & Piercing in Las Vegas"
    return "Piercing work by Katelyn at Work of Art Tattoo & Piercing in Las Vegas"


def img_tag(path: Path) -> str:
    src = f"{WEB_ROOT}/{path.name}"
    alt = html.escape(alt_for(path), quote=True)
    return (
        f'<figure class="overflow-hidden border border-outline-variant/20 bg-surface-container">'
        f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async" '
        f'class="w-full h-full object-cover object-center" width="600" height="600">'
        f'</figure>'
    )


def grid(paths: list[Path], cols: str = "grid-cols-2 md:grid-cols-3 lg:grid-cols-4") -> str:
    return f'<div class="grid {cols} gap-3">' + "".join(img_tag(p) for p in paths) + "</div>"


def replace_dense_grid_after_heading(doc: str, heading: str, paths: list[Path]) -> str:
    if not paths:
        return doc
    pat = re.compile(
        rf'(<h3[^>]*>\s*{re.escape(heading)}\s*</h3>.*?<div class="dense-grid">)(.*?)(</div>)',
        re.I | re.S,
    )
    replacement = lambda m: m.group(1) + "".join(img_tag(p) for p in paths) + m.group(3)
    return pat.sub(replacement, doc, count=1)


def update_katelyn_profile() -> bool:
    path = ROOT / "artists_build" / "katelyn-cole.html"
    if not path.is_file():
        return False
    doc = path.read_text(encoding="utf-8", errors="replace")
    old = doc

    ear = assets((
        "katelyn-earlobe-", "katelyn-helix-", "katelyn-ear-cartilage-",
        "katelyn-upper-ear-", "katelyn-curated-ear-", "katelyn-ear-piercing-process-",
    ))
    face_body = assets((
        "katelyn-nostril-", "katelyn-septum-", "katelyn-lip-labret-",
        "katelyn-lip-nostril-", "katelyn-cheek-", "katelyn-navel-", "katelyn-tongue-",
    ))
    studio = assets((
        "katelyn-piercing-process-", "katelyn-piercing-client-",
        "katelyn-professional-piercer-", "katelyn-piercing-portfolio-mixed-",
    ))

    doc = replace_dense_grid_after_heading(doc, "Anatomical Ear Curation", ear)
    doc = replace_dense_grid_after_heading(doc, "Facial &amp; Body Piercing", face_body)
    doc = replace_dense_grid_after_heading(doc, "Luxury Jewelry", studio)
    doc = doc.replace(">Luxury Jewelry<", ">Placement &amp; Studio Work<", 1)
    doc = doc.replace(">40+ Curated Designs<", ">Real Client Piercings<", 1)
    doc = doc.replace(">Visual Authority &amp; Precision<", ">Katelyn's Piercing Portfolio<", 1)
    doc = re.sub(
        r'Explore meticulously documented piercing case studies — ear curation, facial and body work, and luxury jewelry styling\.',
        "Real piercing work from the studio, organized by placement so you can see Katelyn's actual client work.",
        doc,
        count=1,
    )
    doc = doc.replace(">Scroll for 100+ Live Case Studies<", ">Real Piercing Work<", 1)

    if doc != old:
        path.write_text(doc, encoding="utf-8")
        return True
    return False


def insert_before_close(path: Path, section: str) -> bool:
    doc = path.read_text(encoding="utf-8", errors="replace")
    if MARKER_START in doc:
        # Replace our own prior insertion, so reruns stay current.
        doc2 = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            section,
            doc,
            flags=re.S,
        )
    elif "</main>" in doc:
        doc2 = doc.replace("</main>", section + "\n</main>", 1)
    elif "</body>" in doc:
        doc2 = doc.replace("</body>", section + "\n</body>", 1)
    else:
        return False
    if doc2 != doc:
        path.write_text(doc2, encoding="utf-8")
        return True
    return False


def section_for(title: str, intro: str, paths: list[Path]) -> str:
    if not paths:
        return ""
    return f'''{MARKER_START}
<section class="py-12 md:py-16 px-4 md:px-margin-desktop bg-background border-t border-outline-variant/20" data-woa-katelyn-piercing-photos="1">
  <div class="max-w-6xl mx-auto">
    <div class="max-w-3xl mb-8">
      <span class="text-label-caps font-label-caps text-secondary uppercase tracking-[0.2em]">Real studio work</span>
      <h2 class="text-headline-lg font-headline-lg text-on-surface mt-2">{html.escape(title)}</h2>
      <p class="text-body-lg font-body-lg text-on-surface-variant mt-3">{html.escape(intro)}</p>
    </div>
    {grid(paths)}
    <p class="mt-8 text-center"><a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-3 min-h-[48px] text-label-caps font-label-caps uppercase tracking-widest" href="https://jim.com/a/katelyn-delano-rose-morg" target="_blank" rel="noopener noreferrer">See Katelyn's Current Prices &amp; Book</a></p>
  </div>
</section>
{MARKER_END}'''


def update_main_piercing_guide() -> bool:
    path = ROOT / "best_piercing_shop_las_vegas_updated_jewelry_standards" / "code.html"
    if not path.is_file():
        return False
    representative: list[Path] = []
    for pref in (
        "katelyn-helix-", "katelyn-curated-ear-", "katelyn-nostril-", "katelyn-septum-",
        "katelyn-lip-labret-", "katelyn-navel-", "katelyn-earlobe-", "katelyn-cheek-",
        "katelyn-piercing-process-", "katelyn-professional-piercer-",
    ):
        found = assets(pref)
        if found:
            representative.extend(found[:2])
    sec = section_for(
        "Real Piercing Work by Katelyn",
        "These are real clients from Work of Art Tattoo & Piercing — not stock photos. Placement and jewelry are planned around the client's anatomy and the piercing being performed.",
        representative,
    )
    return bool(sec) and insert_before_close(path, sec)


PAGE_RULES = [
    (("nostril",), "Nostril Piercing Portfolio", "Real nostril piercing work by Katelyn.", ("katelyn-nostril-",)),
    (("septum",), "Septum Piercing Portfolio", "Real septum piercing work by Katelyn.", ("katelyn-septum-",)),
    (("helix",), "Helix Piercing Portfolio", "Real helix and compatible upper-ear placement work by Katelyn.", ("katelyn-helix-", "katelyn-upper-ear-", "katelyn-ear-cartilage-")),
    (("navel", "belly"), "Navel Piercing Portfolio", "Real navel piercing work by Katelyn.", ("katelyn-navel-",)),
    (("labret", "lip-piercing", "lip_piercing"), "Lip & Labret Piercing Portfolio", "Real lip and labret piercing work by Katelyn.", ("katelyn-lip-labret-", "katelyn-lip-nostril-")),
    (("cheek", "dimple"), "Cheek Piercing Portfolio", "Real cheek piercing work by Katelyn.", ("katelyn-cheek-",)),
    (("tongue",), "Tongue Piercing Studio Work", "A real tongue piercing appointment with Katelyn.", ("katelyn-tongue-",)),
    (("lobe", "ear-piercing", "ear_piercing"), "Ear Piercing Portfolio", "Real ear piercing and curated-ear work by Katelyn.", ("katelyn-earlobe-", "katelyn-helix-", "katelyn-ear-cartilage-", "katelyn-curated-ear-", "katelyn-upper-ear-")),
]


def update_matching_existing_pages() -> list[str]:
    changed: list[str] = []
    skip_roots = {"artists_build", "artists_raw", ".git", "node_modules"}
    for path in ROOT.rglob("*.html"):
        if any(part in skip_roots for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix().lower()
        # Main guide is handled separately with a broader gallery.
        if rel == "best_piercing_shop_las_vegas_updated_jewelry_standards/code.html":
            continue
        for needles, title, intro, prefixes in PAGE_RULES:
            if any(n in rel for n in needles):
                pics = assets(prefixes)
                sec = section_for(title, intro, pics)
                if sec and insert_before_close(path, sec):
                    changed.append(rel)
                break
    return changed


def main() -> int:
    if not ASSET_DIR.is_dir():
        raise SystemExit(f"Missing asset directory: {ASSET_DIR}")
    pics = list(ASSET_DIR.glob("*.webp"))
    if not pics:
        raise SystemExit("No Katelyn piercing WEBP assets found")

    changed = []
    if update_katelyn_profile():
        changed.append("artists_build/katelyn-cole.html")
    if update_main_piercing_guide():
        changed.append("best_piercing_shop_las_vegas_updated_jewelry_standards/code.html")
    changed.extend(update_matching_existing_pages())

    print(f"Katelyn piercing assets found: {len(pics)}")
    print("Updated files:")
    for rel in sorted(set(changed)):
        print(f"  - {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

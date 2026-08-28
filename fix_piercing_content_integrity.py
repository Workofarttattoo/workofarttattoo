#!/usr/bin/env python3
"""Final piercing content integrity pass for generated static pages.

This keeps piercing pages aligned with verified source-of-truth language:
Katelyn is a professional piercer, jewelry/material claims remain unverified
until the owner confirms them, and piercing pages should not show tattoo proof
modules as their local evidence.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PIERCING_ROUTE_RE = re.compile(
    r"(piercing|katelyn|helix|conch|tragus|daith|rook|septum|nostril|labret|philtrum|navel|nipple|industrial|cartilage|lobe|tongue|monroe|eyebrow)",
    re.I,
)

TRUST_SOURCE_ROUTE_RE = re.compile(
    r"(geo_hub_ai_source_of_truth_work_of_art|vegas_tattoo_shop_vs_cheap_strip_tattoo|tattoo_pain_chart_placement_sensitivity_guide|start_here)",
    re.I,
)
SLEEVE_ROUTE_RE = re.compile(r"(sleeve|large_scale|large-scale)", re.I)

TATTOO_PROOF_RE = re.compile(
    r"(skull-hourglass|roaring-lion|all-seeing-eye|eagle-memorial|cover-up-tattoo|black-grey-lion|forearm-realism)",
    re.I,
)

SPOTLIGHT_RE = re.compile(
    r"<!-- WOA_PAGE_SPOTLIGHT_VIDEO_START -->[\s\S]*?<!-- WOA_PAGE_SPOTLIGHT_VIDEO_END -->",
    re.I,
)

CURATED_PORTFOLIO_RE = re.compile(
    r"<!-- WOA_CURATED_PORTFOLIO_START -->[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->",
    re.I,
)

ORPHAN_TATTOO_PORTFOLIO_RE = re.compile(
    r'<a class="woa-curated-tile group" href="/#portfolio"><span>Lion Thigh Realism \(Client\)</span></a>[\s\S]*?<!-- WOA_CURATED_PORTFOLIO_END -->',
    re.I,
)

PIERCING_IMAGE_GRID = """<!-- WOA_CURATED_PORTFOLIO_START -->
<section class="woa-curated-portfolio py-14 bg-surface-container-low/35">
  <div class="container mx-auto px-4">
    <div class="max-w-5xl mx-auto">
      <p class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em] mb-3">Piercing proof</p>
      <h2 class="font-display text-display-sm text-on-surface mb-4">Real piercing work from Work of Art</h2>
      <p class="font-body-md text-on-surface-variant mb-6">Use these studio examples to compare placement, spacing, jewelry fit, and the kind of detail Katelyn plans before a piercing appointment.</p>
      <div class="woa-curated-grid">
        <a class="woa-curated-tile group" href="/artists/katelyn-cole/"><picture><source srcset="/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp" type="image/webp"/><img alt="Curated helix, tragus, and lobe piercings by Katelyn Cole at Work of Art Las Vegas" class="w-full h-full object-cover object-center" decoding="async" height="800" loading="lazy" src="/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.png" width="800"/></picture><span>Curated helix, tragus, and lobe</span></a>
        <a class="woa-curated-tile group" href="/artists/katelyn-cole/"><picture><source srcset="/studio_gallery/nostril-stud-on-smiling-client-dd626b1d.webp" type="image/webp"/><img alt="Nostril stud piercing by Katelyn Cole at Work of Art Las Vegas" class="w-full h-full object-cover object-center" decoding="async" height="800" loading="lazy" src="/studio_gallery/nostril-stud-on-smiling-client-dd626b1d.png" width="800"/></picture><span>Nostril stud placement</span></a>
        <a class="woa-curated-tile group" href="/artists/katelyn-cole/"><picture><source srcset="/studio_gallery/flat-and-conch-cartilage-studs-c317138a.webp" type="image/webp"/><img alt="Flat and conch cartilage piercings by Katelyn Cole at Work of Art Las Vegas" class="w-full h-full object-cover object-center" decoding="async" height="800" loading="lazy" src="/studio_gallery/flat-and-conch-cartilage-studs-c317138a.png" width="800"/></picture><span>Flat and conch cartilage</span></a>
      </div>
    </div>
  </div>
</section>
<!-- WOA_CURATED_PORTFOLIO_END -->"""

REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bProfessional Piercer\b"), "Professional Piercer"),
    (re.compile(r"\bProfessional Piercers\b"), "Professional Piercing"),
    (re.compile(r"\bProfessional Piercer\b"), "Professional Piercer"),
    (re.compile(r"\bprofessional piercer\b"), "professional piercer"),
    (re.compile(r"\bprofessional ear piercing\b", re.I), "calm ear piercing"),
    (re.compile(r"\bpiercing\b", re.I), "piercing"),
    (re.compile(r"\bprofessional piercing practices\b", re.I), "calm placement planning"),
    (re.compile(r"\bclean studio process\b", re.I), "clean studio process"),
    (re.compile(r"\bmedical-grade surgical steel\b", re.I), "starter jewelry options"),
    (re.compile(r"\bprofessional surface disinfectants\b", re.I), "studio disinfectants"),
    (re.compile(r"\bstudio sterilization protocols\b", re.I), "documented studio procedures"),
    (re.compile(r"\bcleaning chemicals\b", re.I), "clean procedure-room setup"),
    (re.compile(r"\bhospital-grade\b", re.I), "studio-grade"),
    (re.compile(r"\bAPP-aligned sterile technique and aftercare education\b", re.I), "Clean placement process and aftercare education"),
    (re.compile(r"\bAPP[-\s]aligned\b", re.I), "studio-documented"),
    (re.compile(r"\bimplant-grade titanium &amp; 316L surgical steel jewelry\b", re.I), "Starter jewelry fit and downsizing planning"),
    (re.compile(r"\bimplant-grade titanium and surgical steel in stock\b", re.I), "Jewelry-fit planning and downsizing guidance"),
    (re.compile(r"\b316L Surgical Grade\b", re.I), "Starter Jewelry Fit"),
    (re.compile(r"\b316L\s+surgical[-\s]grade\s+stainless\s+steel\b", re.I), "starter jewelry selected during your consult"),
    (re.compile(r"\b316L\s+steel\b", re.I), "starter jewelry"),
    (re.compile(r"\bsurgical steel\b", re.I), "starter jewelry"),
    (re.compile(r"\bimplant-grade titanium starter jewelry\b", re.I), "starter jewelry sized for swelling"),
    (re.compile(r"\bimplant-grade starter jewelry\b", re.I), "starter jewelry sized for swelling"),
    (re.compile(r"\bimplant-grade titanium jewelry\b", re.I), "starter jewelry selected for the placement"),
    (re.compile(r"\bimplant-grade materials\b", re.I), "documented studio materials"),
    (re.compile(r"\bimplant-grade jewelry standards\b", re.I), "jewelry-fit planning standards"),
    (re.compile(r"\bimplant-grade titanium\b", re.I), "starter jewelry"),
    (re.compile(r"\bimplant-grade jewelry\b", re.I), "jewelry-fit planning"),
    (re.compile(r"\bluxury implant-grade jewelry\b", re.I), "quality starter jewelry"),
    (re.compile(r"\bImplant-grade jewelry and anatomical placement\.", re.I), "Jewelry fit and anatomical placement."),
    (re.compile(r"\bprecision ear curation and piercing\b", re.I), "calm ear curation and piercing placement"),
    (re.compile(r"We use starter jewelry selected for the placement jewelry\. We never use &quot;starter jewelry&quot; or plated metals,[^.]*\.", re.I), "We choose starter jewelry by anatomy, swelling room, placement, and sensitivity history. Ask the studio to confirm current material options before booking."),
    (re.compile(r"We use implant-grade titanium jewelry\. We never use &quot;surgical steel&quot; or plated metals,[^.]*\.", re.I), "We choose starter jewelry by anatomy, swelling room, placement, and sensitivity history. Ask the studio to confirm current material options before booking."),
    (re.compile(r"At Work of Art Tattoo &amp; Piercing, Katelyn Cole uses high-quality starter jewelry, including specific titanium material claims\.[^<]*", re.I), "At Work of Art Tattoo &amp; Piercing, Katelyn Cole plans starter jewelry around anatomy, placement, swelling room, and current studio availability."),
    (re.compile(r"Katelyn Cole leads ear curation and piercing at Work of Art in Las Vegas\. Katelyn Cole leads the industry here,[^<]*", re.I), "Katelyn Cole leads ear curation and piercing planning at Work of Art in Las Vegas, using each client's anatomy and style goals to shape a balanced layout."),
    (re.compile(r"picked starter jewelry, and staged piercings", re.I), "planned starter jewelry fit and staged piercings"),
    (re.compile(r"Katelyn Cole's ear curation and implant-grade jewelry", re.I), "Katelyn Cole's ear curation and jewelry-fit planning"),
    (re.compile(r"Katelyn Cole \(professional piercer\)", re.I), "Katelyn Cole (professional piercer)"),
    (re.compile(r"Joshua Cole \(tattoo &amp; piercing; studio lead who trains the team\) and Katelyn Cole \(professional piercer\)", re.I), "Joshua Cole (tattoo and piercing, studio lead), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer; fineline floral work and script)"),
)


def is_public_html(path: Path) -> bool:
    if path.name != "code.html" and not (path.parent.name == "artists_build" and path.suffix == ".html"):
        return False
    parts = set(path.relative_to(ROOT).parts)
    return ".git" not in parts and "skipped_upload_build" not in parts and "artists_raw" not in parts


def route_key(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return "/".join(rel.parts).lower()


def clean_piercing_html(html: str) -> str:
    out = html
    for pattern, replacement in REPLACEMENTS:
        out = pattern.sub(replacement, out)
    out = out.replace("Facial piercing Work", "Facial Piercing Work")
    out = out.replace("Body piercing & Jewelry Fit", "Body Piercing & Jewelry Fit")
    out = out.replace("Body piercing &amp; Jewelry Fit", "Body Piercing &amp; Jewelry Fit")
    out = out.replace("piercing Portfolio", "Piercing Portfolio")
    out = re.sub(
        r"Fresh piercings start in starter jewelry \(ASTM F136\) or starter jewelry\s+—\s+never mystery metal from a kiosk\.",
        "Fresh piercing jewelry is selected during your consult based on anatomy, swelling room, placement, and current studio availability.",
        out,
        flags=re.I,
    )
    out = re.sub(
        r"I use sterile needle technique and starter jewelry sized for swelling for every ([^.<]+)\.",
        r"I plan every \1 around anatomy, swelling room, placement angle, and aftercare.",
        out,
        flags=re.I,
    )
    out = re.sub(
        r"Use these guides to plan ear piercing in Las Vegas, helix piercing with Katelyn Cole, starter jewelry piercing jewelry, and curated ear piercing consults before booking\.",
        "Use these guides to plan ear piercing in Las Vegas, helix piercing with Katelyn Cole, starter jewelry fit, and curated ear piercing consults before booking.",
        out,
        flags=re.I,
    )
    out = out.replace(
        '<a class="text-secondary underline" href="/piercing_jewelry_guide_las_vegas/">starter jewelry piercing jewelry</a>',
        '<a class="text-secondary underline" href="/piercing_jewelry_guide_las_vegas/">starter jewelry fit</a>',
    )
    out = out.replace(
        "Katelyn is our professional piercer only. For tattoos",
        "Katelyn is a professional piercer. For tattoos",
    )

    def replace_spotlight(match: re.Match[str]) -> str:
        block = match.group(0)
        if TATTOO_PROOF_RE.search(block):
            return ""
        return block

    out = SPOTLIGHT_RE.sub(replace_spotlight, out)

    def replace_curated(match: re.Match[str]) -> str:
        block = match.group(0)
        if TATTOO_PROOF_RE.search(block):
            return PIERCING_IMAGE_GRID
        return block

    out = CURATED_PORTFOLIO_RE.sub(replace_curated, out)
    out = ORPHAN_TATTOO_PORTFOLIO_RE.sub(PIERCING_IMAGE_GRID, out)
    return out


def clean_tattoo_visual_html(html: str) -> str:
    def replace_spotlight(match: re.Match[str]) -> str:
        block = match.group(0)
        if "katelyn" in block.lower() or "piercing" in block.lower() or "C78fY1quCVF" in block:
            return ""
        return block

    return SPOTLIGHT_RE.sub(replace_spotlight, html)


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not is_public_html(path):
            continue
        route = route_key(path)
        if not (PIERCING_ROUTE_RE.search(route) or TRUST_SOURCE_ROUTE_RE.search(route) or SLEEVE_ROUTE_RE.search(route)):
            continue
        raw = path.read_text(encoding="utf-8")
        new = clean_piercing_html(raw) if (PIERCING_ROUTE_RE.search(route) or TRUST_SOURCE_ROUTE_RE.search(route)) else raw
        if SLEEVE_ROUTE_RE.search(route):
            new = clean_tattoo_visual_html(new)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"[piercing-integrity] {path.relative_to(ROOT)}")
    print(f"[piercing-integrity] changed {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fix walk-in page blank middle: hero image, scroll visibility, footer order."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGETS = (
    ROOT / "walk-in-tattoos-las-vegas" / "code.html",
    ROOT / "walk_in_tattoos_las_vegas_authority_guide" / "code.html",
)

HERO_OLD = re.compile(
    r'<section class="relative h-\[921px\] flex items-center justify-center overflow-hidden">\s*'
    r'<div class="absolute inset-0 z-0">\s*'
    r'<div class="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent"></div>\s*'
    r"</div>",
    re.MULTILINE,
)

HERO_NEW = """<section class="relative min-h-[420px] md:min-h-[520px] max-h-[min(85vh,720px)] flex items-center justify-center overflow-hidden py-16 md:py-20">
<div class="absolute inset-0 z-0">
<picture>
<source srcset="/image_5_22_26_at_9.11_pm_1.png/professional-tattoo-artist-work-of-art-las-vegas-studio.webp" type="image/webp"/>
<img alt="Professional tattoo artist at Work of Art Tattoo &amp; Piercing, Las Vegas walk-in studio" class="w-full h-full object-cover opacity-60" decoding="async" height="800" loading="eager" src="/image_5_22_26_at_9.11_pm_1.png/professional-tattoo-artist-work-of-art-las-vegas-studio.png" width="1200"/>
</picture>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent"></div>
</div>"""

SCROLL_OLD = """        document.querySelectorAll('section').forEach(section => {
            section.classList.add('transition-all', 'duration-1000', 'opacity-0', 'translate-y-10');
            observer.observe(section);
        });"""

SCROLL_NEW = """        document.querySelectorAll('section').forEach((section, index) => {
            if (index === 0) {
                section.classList.add('opacity-100', 'translate-y-0');
                return;
            }
            section.classList.add('transition-all', 'duration-1000', 'opacity-0', 'translate-y-10');
            observer.observe(section);
        });"""

FOOTER_RE = re.compile(
    r"\n<footer class=\"w-full px-margin-mobile md:px-margin-desktop py-12 flex flex-col md:flex-row"
    r" justify-between items-start gap-8 border-t border-outline-variant bg-surface-container-lowest\">"
    r"[\s\S]*?</footer>\n",
    re.MULTILINE,
)

PROOF_STRIP_RE = re.compile(
    r'<section class="space-y-6 py-4" data-woa-guide-proof-strip="1" id="photos">[\s\S]*?</section>\n',
    re.MULTILINE,
)

CTA_REPLACEMENTS = (
    ('href="#availability"', 'href="/appointments/"'),
    ('href="#quote"', 'href="/appointments/"'),
)


def reorder_proof_strip(html: str) -> str:
    strip_match = PROOF_STRIP_RE.search(html)
    if not strip_match:
        return html
    strip_block = strip_match.group(0)
    html = html.replace(strip_block, "", 1)
    marker = 'data-woa-proof-block="1"'
    pos = html.find(marker)
    if pos < 0:
        return html.replace("</main>", strip_block + "</main>", 1)
    close = html.find("</section>", pos)
    if close < 0:
        return html.replace("</main>", strip_block + "</main>", 1)
    insert_at = close + len("</section>")
    return html[:insert_at] + "\n" + strip_block + html[insert_at:]


def fix_html(html: str) -> str:
    updated = HERO_OLD.sub(HERO_NEW, html, count=1)
    updated = updated.replace(SCROLL_OLD, SCROLL_NEW)
    for old, new in CTA_REPLACEMENTS:
        updated = updated.replace(old, new)

    footer_match = FOOTER_RE.search(updated)
    if footer_match and updated.find("</main>") > footer_match.start():
        footer_block = footer_match.group(0)
        updated = updated[: footer_match.start()] + updated[footer_match.end() :]
        updated = updated.replace("</main>", footer_block + "</main>", 1)

    updated = reorder_proof_strip(updated)
    return updated


def main() -> int:
    n = 0
    for path in TARGETS:
        if not path.is_file():
            print(f"[skip] missing {path.relative_to(ROOT)}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = fix_html(raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] {path.parent.name}/code.html")
            n += 1
        else:
            print(f"[skip] no changes {path.parent.name}/code.html")
    print(f"Done: {n} walk-in page(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

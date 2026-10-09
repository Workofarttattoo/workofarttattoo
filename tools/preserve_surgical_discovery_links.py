#!/usr/bin/env python3
"""Preserve four small contextual discovery links in final generated HTML."""
from pathlib import Path

LINKS = {
    "cover-up-tattoos-las-vegas": [
        ("/knowledge/black-and-grey-realism-explained/", "How black-and-grey realism works"),
        ("/knowledge/tattoo-aging-and-fading-over-time/", "How tattoos age and fade"),
    ],
    "piercing-guide-las-vegas": [
        ("/nose_piercing_las_vegas_authority_guide/", "Nose piercing options"),
        ("/knowledge/piercing-starter-jewelry-fit/", "Choosing properly fitted starter jewelry"),
    ],
}
MARKER = 'data-woa-surgical-discovery="2026-10"'

def apply(path, links):
    if not path.is_file():
        raise SystemExit(f"Missing page: {path}")
    body = path.read_text(encoding="utf-8")
    if MARKER in body:
        return
    missing = [(href, label) for href, label in links if f'href="{href}"' not in body]
    if not missing:
        return
    anchor = '<nav data-woa-guide-links="1"'
    # The site build can remove the guide nav before this preservation step.
    # Fall back to the end of <main> while keeping links inside page content.
    if anchor not in body:
        anchor = "</main>"
    if anchor not in body:
        raise SystemExit(f"Cannot find safe insertion point in {path}")
    items = "".join(f'<li><a class="text-secondary underline hover:no-underline" href="{href}">{label}</a></li>' for href, label in missing)
    block = f'<section {MARKER} class="py-6 px-margin-mobile md:px-margin-desktop bg-surface-container-low" aria-label="Related reading"><div class="max-w-4xl mx-auto"><h2 class="font-headline-md text-on-surface text-xl mb-3">Related reading</h2><ul class="font-body-md text-on-surface-variant space-y-2">{items}</ul></div></section>\n'
    body = body.replace(anchor, block + anchor, 1)
    path.write_text(body, encoding="utf-8")

def main():
    for slug, links in LINKS.items():
        for name in ("code.html", "index.html"):
            path = Path(slug) / name
            if path.exists():
                apply(path, links)
        published = Path(slug) / "index.html"
        if not published.exists():
            continue
        html = published.read_text(encoding="utf-8")
        for href, _ in links:
            if f'href="{href}"' not in html:
                raise SystemExit(f"Missing final internal link: {slug} -> {href}")
    print("Verified four contextual links in generated pages")

if __name__ == "__main__":
    main()

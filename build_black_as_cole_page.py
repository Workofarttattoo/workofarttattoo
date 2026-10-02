#!/usr/bin/env python3
"""Build /black-as-cole/ from media-manifest.json without moving originals."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "black-as-cole"
MANIFEST = PAGE / "media-manifest.json"
DERIV = PAGE / "derivatives"
TEMPLATE = ROOT / "joshua_oil_painting_black_grey_tattoo_aging_las_vegas" / "code.html"
SITE = "https://www.workofarttattoo.com"
CANON = f"{SITE}/black-as-cole/"
TITLE = "BLACK AS COLE | Fine Art by Joshua Cole"
DESCRIPTION = (
    "Black As Cole — original paintings, drawings, studies and dark surreal "
    "artwork by Las Vegas artist Joshua Cole."
)
HERO_SRC = "/merchandise/prismacolor-bristol-6e3d8efa.webp"

CATEGORY_LABELS = {
    "dark-surrealism": "Dark surrealism",
    "figure": "Figure / anatomy / portrait",
    "illustrative": "Illustrative + color",
    "artist": "Artist",
    "tattoo": "Tattoo",
}


def category_keys(work: dict) -> list[str]:
    raw = work.get("categories")
    if isinstance(raw, list):
        keys = [str(item) for item in raw if item]
        if keys:
            return keys
    category = work.get("category")
    return [str(category)] if category else []


def category_label(work: dict) -> str:
    labels: list[str] = []
    for key in category_keys(work):
        label = CATEGORY_LABELS.get(key, key)
        if label not in labels:
            labels.append(label)
    return " / ".join(labels)

ROOMS = (
    ("dark-surrealism", "Dark surrealism", None),
    ("figure", "Figure / anatomy / portrait", None),
    (
        "illustrative",
        "Illustrative + color",
        None,
    ),
)


def esc(value: str | None) -> str:
    return html.escape(value or "", quote=True)


def load_media() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(data["blackAsColeMedia"])


def make_derivatives(works: list[dict]) -> dict[str, list[tuple[int, str]]]:
    DERIV.mkdir(parents=True, exist_ok=True)
    srcsets: dict[str, list[tuple[int, str]]] = {}
    for work in works:
        if work.get("type") != "image":
            continue
        width = int(work["width"])
        page_master = str(work.get("src", "")).startswith("/black-as-cole/")
        if width <= 640 or (width < 1000 and not page_master):
            continue
        source = ROOT / work["src"].lstrip("/")
        image = Image.open(source)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        entries: list[tuple[int, str]] = []
        for target in (640, 960, 1280):
            if target >= width:
                continue
            dest = DERIV / f"{work['id']}-{target}.webp"
            if not dest.exists():
                height = round(int(work["height"]) * target / width)
                resized = image.resize((target, height), Image.Resampling.LANCZOS)
                frame = resized.convert("RGB")
                frame.save(dest, "WEBP", quality=84, method=6)
            entries.append((target, f"/black-as-cole/derivatives/{dest.name}"))
        entries.append((width, work["src"]))
        srcsets[work["id"]] = entries
    return srcsets


def img_tag(work: dict, srcsets: dict[str, list[tuple[int, str]]], *, hero: bool = False) -> str:
    src = work["src"]
    alt = esc(work["alt"])
    width = work["width"]
    height = work["height"]
    loading = "eager" if hero else "lazy"
    priority = ' fetchpriority="high"' if hero else ""
    extra = srcsets.get(work["id"])
    srcset = ""
    sizes = ""
    if extra:
        srcset = ", ".join(f"{esc(url)} {w}w" for w, url in extra)
        sizes = "(max-width: 720px) 92vw, 640px" if hero else "(max-width: 720px) 100vw, 46vw"
        src = extra[0][1]
        for candidate_width, candidate_url in extra:
            if candidate_width <= (960 if hero else 1280):
                src = candidate_url
    srcset_attr = f' srcset="{srcset}" sizes="{sizes}"' if srcset else ""
    return (
        f'<img src="{esc(src)}" alt="{alt}" width="{width}" height="{height}"'
        f'{srcset_attr} loading="{loading}" decoding="async"{priority}/>'
    )


def tile(work: dict, srcsets: dict[str, list[tuple[int, str]]]) -> str:
    title = work.get("title") or "Untitled"
    note = work.get("catalogNote") or ""
    category = category_label(work)
    return (
        f'<button type="button" class="bac-tile" data-bac-open data-bac-id="{esc(work["id"])}"'
        f' data-full="{esc(work["src"])}" data-alt="{esc(work["alt"])}"'
        f' data-title="{esc(title)}" data-category="{esc(category)}"'
        f' data-note="{esc(note)}" data-width="{work["width"]}" data-height="{work["height"]}">'
        f'{img_tag(work, srcsets)}</button>'
    )


def masonry(works: list[dict], srcsets: dict[str, list[tuple[int, str]]]) -> str:
    return '<div class="bac-masonry">' + "".join(tile(work, srcsets) for work in works) + "</div>"


def gallery_main(works: list[dict], srcsets: dict[str, list[tuple[int, str]]]) -> str:
    gallery = [work for work in works if work.get("placement") == "gallery"]
    hero = next(work for work in gallery if work.get("hero"))
    selected = [work for work in gallery if work.get("featured")]
    artist = next(work for work in works if work.get("placement") == "artist")
    rooms = []
    for key, label, _note in ROOMS:
        group = [work for work in gallery if key in category_keys(work)]
        if not group:
            continue
        rooms.append(
            f'<section class="bac-section bac-room" id="{esc(key)}" aria-labelledby="bac-{esc(key)}">'
            f'<div class="bac-section-head"><p class="bac-section-kicker">Collection</p>'
            f'<h2 id="bac-{esc(key)}">{esc(label)}</h2></div>'
            f"{masonry(group, srcsets)}</section>"
        )
    hero_img = img_tag(hero, srcsets, hero=True)
    artist_title = "Untitled"
    skin = [work for work in works if work.get("placement") == "skin"]
    skin_block = masonry(skin, srcsets) if skin else ""
    return f"""<main class="bac" id="black-as-cole">
<section class="bac-hero" aria-labelledby="bac-title">
<div class="bac-hero-copy">
<h1 id="bac-title">Black As Cole</h1>
<p class="bac-kicker bac-byline">Fine art by</p>
<p class="bac-artist">Joshua Cole</p>
<p class="bac-lede">Paintings, drawings, studies and experiments in light, anatomy, mortality and imagination.</p>
<div class="bac-hero-actions">
<a class="bac-link" href="#selected">Enter the gallery</a>
</div>
</div>
<figure class="bac-hero-figure">
<button type="button" class="bac-hero-open" data-bac-open data-bac-id="{esc(hero["id"])}" data-full="{esc(hero["src"])}" data-alt="{esc(hero["alt"])}" data-title="Untitled" data-category="{esc(category_label(hero))}" data-note="{esc(hero.get("catalogNote") or "")}" data-width="{hero["width"]}" data-height="{hero["height"]}">
{hero_img}
</button>
</figure>
</section>
<section class="bac-section" id="selected" aria-labelledby="bac-selected">
<div class="bac-section-head"><p class="bac-section-kicker">Gallery</p><h2 id="bac-selected">Selected work</h2></div>
{masonry(selected, srcsets)}
</section>
{''.join(rooms)}
<section class="bac-section" id="artist" aria-labelledby="bac-artist">
<div class="bac-statement">
<div>
<p class="bac-section-kicker">The artist</p>
<h2 id="bac-artist">Black As Cole</h2>
<p>Joshua Cole is a Las Vegas artist working across painting, drawing, tattooing and digital composition. His work moves between disciplined studies of light and anatomy and darker surreal imagery centered on mortality, transformation, identity and imagination.</p>
</div>
<figure class="bac-portrait">
<button type="button" class="bac-tile" data-bac-open data-bac-id="{esc(artist["id"])}" data-full="{esc(artist["src"])}" data-alt="{esc(artist["alt"])}" data-title="{esc(artist_title)}" data-category="Artist" data-note="" data-width="{artist["width"]}" data-height="{artist["height"]}">
<img src="{esc(artist["src"])}" alt="{esc(artist["alt"])}" width="{artist["width"]}" height="{artist["height"]}" loading="lazy" decoding="async"/>
</button>
</figure>
</div>
</section>
<section class="bac-section" id="skin" aria-labelledby="bac-skin">
<div class="bac-section-head">
<p class="bac-section-kicker">Secondary</p>
<h2 id="bac-skin">From canvas to skin</h2>
</div>
{skin_block}
<p class="bac-footnote">The same study of light, anatomy, and edge shows up in Joshua’s tattoo work.</p>
<p><a class="bac-link" href="/artists/joshua-cole/">View Joshua’s tattoo work</a></p>
</section>
<section class="bac-section" id="collect" aria-labelledby="bac-collect">
<div class="bac-section-head">
<p class="bac-section-kicker">Contact</p>
<h2 id="bac-collect">Collect / commission / collaborate</h2>
</div>
<div class="bac-contact-links">
<a class="bac-link" href="mailto:booking@workofarttattoo.com?subject=Artwork%20inquiry%20-%20Black%20As%20Cole">Inquire about artwork</a>
<a class="bac-link" href="mailto:booking@workofarttattoo.com?subject=Commission%20inquiry%20-%20Black%20As%20Cole">Commission a piece</a>
<a class="bac-link" href="/official_location_hours_contact/">Visit Work of Art</a>
</div>
</section>
<dialog class="bac-lightbox" id="bac-lightbox" aria-labelledby="bac-lb-title">
<div class="bac-lb-shell">
<div class="bac-lb-bar"><button type="button" class="bac-lb-close" data-bac-close>Close</button></div>
<div class="bac-lb-stage">
<button type="button" class="bac-lb-nav" data-bac-prev aria-label="Previous artwork">Prev</button>
<img id="bac-lb-img" alt=""/>
<button type="button" class="bac-lb-nav" data-bac-next aria-label="Next artwork">Next</button>
</div>
<div class="bac-lb-caption">
<p class="bac-lb-title" id="bac-lb-title"></p>
<p class="bac-lb-cat" id="bac-lb-cat"></p>
<p class="bac-lb-note" id="bac-lb-note"></p>
</div>
</div>
</dialog>
</main>"""


def schema_block(works: list[dict]) -> str:
    artist_id = f"{CANON}#joshua-cole"
    graph: list[dict] = [
        {
            "@type": "WebPage",
            "@id": f"{CANON}#page",
            "url": CANON,
            "name": TITLE,
            "description": DESCRIPTION,
            "inLanguage": "en-US",
            "about": {"@id": artist_id},
            "primaryImageOfPage": f"{SITE}{HERO_SRC}",
        },
        {
            "@type": ["Person", "VisualArtist"],
            "@id": artist_id,
            "name": "Joshua Cole",
            "url": f"{SITE}/artists/joshua-cole/",
            "homeLocation": {
                "@type": "Place",
                "name": "Las Vegas, Nevada",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Las Vegas",
                    "addressRegion": "NV",
                    "addressCountry": "US",
                },
            },
        },
    ]
    for work in works:
        if work.get("type") != "image" or work.get("placement") != "gallery":
            continue
        node = {
            "@type": ["VisualArtwork", "CreativeWork"],
            "@id": f"{CANON}#{work['id']}",
            "name": work.get("title") or "Untitled",
            "creator": {"@id": artist_id},
            "image": f"{SITE}{work['src']}",
            "description": work["alt"],
        }
        graph.append(node)
    payload = {"@context": "https://schema.org", "@graph": graph}
    return (
        '<script data-woa-entity-schema="1" type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False)
        + "</script>"
    )


def hero_preload(srcsets: dict[str, list[tuple[int, str]]]) -> str:
    entries = srcsets.get("skull-clock") or []
    if not entries:
        return f'<link rel="preload" as="image" href="{HERO_SRC}"/>'
    srcset = ", ".join(f"{url} {width}w" for width, url in entries)
    return (
        f'<link rel="preload" as="image" href="{entries[1][1] if len(entries) > 1 else entries[0][1]}" '
        f'imagesrcset="{srcset}" imagesizes="(max-width: 720px) 92vw, 640px"/>'
    )


def build_html(works: list[dict], srcsets: dict[str, list[tuple[int, str]]]) -> str:
    page = TEMPLATE.read_text(encoding="utf-8")
    start = page.find('<nav aria-label="Related guides"')
    end = page.find("<footer")
    if start < 0 or end < 0 or start > end:
        raise SystemExit("Could not find the template content region to replace")
    page = page[:start] + gallery_main(works, srcsets) + "\n" + page[end:]
    page = re.sub(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>',
        lambda _match: schema_block(works),
        page,
        count=1,
        flags=re.S,
    )
    page = page.replace("Oil Painting &amp; Tattoo Aging", TITLE)
    page = page.replace("Oil Painting & Tattoo Aging", TITLE)
    old_desc = (
        "How Joshua Cole&#x27;s classical painting background shapes black-and-grey tattoo design "
        "in Las Vegas — choices that heal cleanly and read well for years at Work of Art on E. Tropicana. 777"
    )
    page = page.replace(old_desc, esc(DESCRIPTION))
    page = page.replace(
        f"{SITE}/joshua_oil_painting_black_grey_tattoo_aging_las_vegas/",
        CANON,
    )
    page = page.replace(
        f"{SITE}/home_work_of_art_tattoo_piercing/las-vegas-tattoo-hero-background.webp",
        f"{SITE}{HERO_SRC}",
    )
    page = page.replace('property="og:image:width"/>', 'property="og:image:width"/>')
    page = page.replace(
        '<meta content="1200" property="og:image:width"/>',
        '<meta content="1920" property="og:image:width"/>',
    )
    page = page.replace(
        '<meta content="630" property="og:image:height"/>',
        '<meta content="2560" property="og:image:height"/>',
    )
    page = re.sub(
        r'<a\b(?=[^>]*\bdata-woa-sticky-book="1")[^>]*>.*?</a>\s*',
        "",
        page,
        count=1,
        flags=re.S,
    )
    page = page.replace(
        "</head>",
        hero_preload(srcsets)
        + '\n<link href="/black-as-cole/gallery.css" rel="stylesheet"/>\n</head>',
        1,
    )
    page = page.replace(
        "</body>",
        '<script src="/black-as-cole/gallery.js" defer></script>\n</body>',
        1,
    )
    if 'rel="canonical"' not in page or CANON not in page:
        raise SystemExit("Canonical was not written")
    if TITLE not in page:
        raise SystemExit("Title was not written")
    return page


def main() -> int:
    works = load_media()
    srcsets = make_derivatives(works)
    page = build_html(works, srcsets)
    (PAGE / "code.html").write_text(page, encoding="utf-8")
    (PAGE / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote {PAGE / 'code.html'} ({len(page):,} bytes)")
    print(f"Derivatives: {len(list(DERIV.glob('*.webp')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

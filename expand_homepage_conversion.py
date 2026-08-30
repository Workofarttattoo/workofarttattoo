#!/usr/bin/env python3
"""
Expand homepage with Google-style review proof and 30+ portfolio images.

  python3 expand_homepage_conversion.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME_SLUG = "home_work_of_art_tattoo_piercing"
HOME = ROOT / HOME_SLUG
CODE = HOME / "code.html"
CSS = HOME / "woa-home.css"

SKIP_PARTS = frozenset(
    {
        "skipped_upload_build",
        "artists_raw",
        "skipped_pages_clipboard",
        ".git",
        "assets",
    }
)
# Only real tattoo/piercing photos — never Stitch guide page screenshots.
ALLOWED_PARTS = frozenset(
    {
        "home_work_of_art_tattoo_piercing",
        "client-portfolio",
        "hero-premium",
        "cover-up-tattoos-las-vegas",
        "cover_up_tattoos_las_vegas_master_authority_guide",
        "artists",
        "reviews_vault_100_verified_masterpieces",
    }
)
SKIP_DIR_SUFFIXES = (
    "_authority_guide",
    "_hub",
    "appointments",
    "artists_build",
    "studio_videos",
    "merchandise",
    "geo_hub",
    "walk_in",
    "vegas_tattoo",
    "tattoo_shop",
    "how_to_choose",
    "how_much_do",
    "fine_line",
    "best_",
    "realism_tattoos",
)
SKIP_NAMES = frozenset(
    {
        "screen.png",
        "las-vegas-tattoo-hero-background.png",
        "custom-tattoos-las-vegas-epic-snake-texture.webp",
        "reviews-vault-100-verified-masterpieces-las-vegas.png",
        "review-funnel-google-authority-hub.png",
        "google-review-qr-code-nfc-sign-work-of-art-tattoo.png",
        "realism-tattoos-las-vegas-master-authority-guide.png",
        "work-of-art-logo.png",
    }
)
SKIP_STEMS = frozenset(
    {
        "realism-tattoos-las-vegas-master-authority-guide",
        "reviews-vault-100-verified-masterpieces-las-vegas",
        "review-funnel-google-authority-hub",
        "custom-tattoos-las-vegas-epic-snake-black-and-grey-realism",
    }
)

# Replaced in #studio-videos showcase band — keep out of masonry grid.
MASONRY_EXCLUDE_STEMS = frozenset(
    {
        "woman-skull-skeletal-hand-forearm-realism-las-vegas",
        "hero-woman-skull-skeletal-hand-forearm-realism",
        "cover-up-tattoo-sunflower-over-black-ink-las-vegas",
        "color-parrot-cover-up-forearm-las-vegas",
        "color-character-cover-up-over-geometric-las-vegas",
        "color-panther-snake-flames-upper-arm-las-vegas",
        "black-grey-realism-snake-sleeve-tattoo",
        "las-vegas-tattoo-artist-working-closeup",
        "hero-medusa-snake-hair-forearm-realism",
        "hero-lion-clock-realism-shoulder-tattoo",
        "hero-roaring-lion-tiger-forearm-realism",
        "hero-woman-skull-skeletal-hand-forearm-realism",
        "hero-archangel-michael-demon-upper-arm-realism",
        "medusa-snake-hair-forearm-realism-las-vegas",
        "money-rose-black-grey-realism-upper-arm-las-vegas",
        "lion-clock-realism-shoulder-tattoo-las-vegas",
        "roaring-lion-tiger-forearm-realism-las-vegas",
        "woman-skull-skeletal-hand-forearm-realism-las-vegas",
        "hundred-dollar-bill-forearm-realism-las-vegas",
    }
)

FEATURED_REVIEW = (
    "Shawn P.",
    "Google Review · Out-of-town visitor",
    "Absolutely Incredible Experience — Joshua Cole is a Master!",
    (
        "I recently visited this shop while in Vegas from out of town, and I cannot recommend it highly enough. "
        "My artist was Joshua Cole, and he completely exceeded every expectation I had.",
        "I came in wanting a half sleeve, and Joshua took his time from start to finish. He didn't rush a single step—"
        "he meticulously ensured every element was aligned perfectly and that the overall composition flowed correctly "
        "across my arm. You can tell he genuinely cares about the art and how it will look on your body for years to come.",
        "What really impressed me was how he designed the piece with future work in mind. He thought ahead about how "
        "additional tattoos could connect and complement what we were doing, showing me he's invested in the long-term "
        "vision, not just a quick session.",
        "The atmosphere was welcoming, professional, and comfortable throughout. I had an A++ time from consultation "
        "to completion. But what really set Joshua apart was his hospitality—when he learned I was visiting from out of "
        "town and didn't have a ride, he actually offered to drive me back to my hotel. That level of care is rare these days.",
        "If you're in Vegas or planning a visit, do yourself a favor and book with Joshua Cole. Whether you're local or "
        "traveling, this shop delivers top-tier artistry and genuine customer service. I'll definitely be returning for my "
        "next piece. Five stars isn't enough!",
    ),
)

# Additional short pull-quotes for the horizontal rail (verified only).
REVIEW_CARDS: list[tuple[str, str, str]] = []


def categorize(rel: str, stem: str) -> str:
    low = f"{rel}/{stem}".lower()
    parts: list[str] = ["all"]

    if "healed" in low:
        parts.append("healed")
    if any(
        x in low
        for x in (
            "cover-up",
            "coverup",
            "cover_up",
            "black-grey-lion-thigh-realism-las-vegas",
            "sunflower-over-black",
            "phoenix-hand",
        )
    ):
        parts.append("coverups")
    if any(x in low for x in ("sleeve", "snake-masterpiece", "roman-numeral-sleeve")):
        parts.append("sleeves")
    if any(
        x in low
        for x in (
            "fine-line",
            "fine_line",
            "roman-numeral",
            "nightmare-before",
        )
    ):
        parts.append("fine-line")
    if any(
        x in low
        for x in (
            "color",
            "sunflower",
            "phoenix",
            "butterfly",
            "nightmare",
        )
    ) and "black-and-grey" not in stem:
        parts.append("color-realism")
    if any(
        x in low
        for x in (
            "realism",
            "grim-reaper",
            "dove",
            "seraphim",
            "lion",
            "reaper",
            "epic-snake-black",
        )
    ):
        parts.append("black-grey")
    if "piercing" in low or "jewelry" in low or "katelyn" in low:
        parts.append("piercing")
    if "tattoo-portfolio" in low or "joshua-gallery" in low or "professional-tattoo" in low:
        parts.append("client")

    if len(parts) == 1:
        parts.append("black-grey")
    return " ".join(dict.fromkeys(parts))


def alt_from_stem(stem: str) -> str:
    words = stem.replace("-", " ").strip()
    return html.escape(f"{words} — Las Vegas tattoo portfolio at Work of Art")[:140]


def discover_images() -> list[dict]:
    seen: set[str] = set()
    items: list[dict] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(p in SKIP_PARTS for p in path.parts):
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix.lower() not in {".webp", ".png", ".jpeg", ".jpg"}:
            continue
        rel_dir = path.parent.relative_to(ROOT).as_posix()
        if not any(part in ALLOWED_PARTS for part in path.parts):
            continue
        if any(part.endswith(SKIP_DIR_SUFFIXES) for part in path.parts):
            continue
        if path.stem in SKIP_STEMS or path.stem in MASONRY_EXCLUDE_STEMS:
            continue
        if rel_dir == HOME_SLUG and path.stem in {
            "las-vegas-tattoo-hero-background",
            "custom-tattoos-las-vegas-epic-snake-texture",
        }:
            continue

        stem = path.stem
        if stem in seen or stem in MASONRY_EXCLUDE_STEMS:
            continue

        webp = path.with_suffix(".webp")
        png = path.with_suffix(".png")
        if path.suffix.lower() == ".png" and webp.is_file():
            continue
        if path.suffix.lower() == ".jpeg" and webp.is_file():
            continue
        if path.suffix.lower() == ".jpg" and webp.is_file():
            continue

        if webp.is_file():
            src_webp = f"/{rel_dir}/{webp.name}"
            fallback = png if png.is_file() else path
        else:
            src_webp = ""
            fallback = path

        src_fallback = f"/{rel_dir}/{fallback.name}"
        key = stem
        if key in seen:
            continue
        seen.add(key)

        items.append(
            {
                "stem": stem,
                "webp": src_webp,
                "png": src_fallback,
                "cats": categorize(rel_dir, stem),
                "alt": alt_from_stem(stem),
            }
        )

    priority = (
        "healed",
        "cover",
        "realism",
        "sleeve",
        "snake",
        "lion",
        "seraphim",
        "phoenix",
        "butterfly",
        "portfolio",
        "joshua-gallery",
    )

    def rank(item: dict) -> tuple[int, str]:
        low = item["stem"]
        for i, needle in enumerate(priority):
            if needle in low:
                return (i, low)
        return (len(priority), low)

    items.sort(key=rank)
    return items


def picture_cell(item: dict, lazy: bool = True) -> str:
    loading = "lazy" if lazy else "eager"
    webp = item["webp"]
    png = item["png"]
    alt = item["alt"]
    cats = item["cats"]
    if webp:
        pic = (
            f'<picture><source srcset="{webp}" type="image/webp"/>'
            f'<img alt="{alt}" class="w-full h-full object-cover object-center '
            f'transition-transform duration-500 group-hover:scale-105" '
            f'decoding="async" loading="{loading}" src="{png}" width="800" height="800"/></picture>'
        )
    else:
        pic = (
            f'<img alt="{alt}" class="w-full h-full object-cover object-center '
            f'transition-transform duration-500 group-hover:scale-105" '
            f'decoding="async" loading="{loading}" src="{png}" width="800" height="800"/>'
        )
    return (
        f'<div class="woa-gallery-tile group relative aspect-square bg-surface-container '
        f'overflow-hidden border border-outline-variant/20" data-category="{cats}">\n'
        f"{pic}\n"
        f'<div class="absolute inset-0 bg-gradient-to-t from-background/90 via-transparent '
        f'to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-3">'
        f'<span class="font-label-caps text-[9px] uppercase tracking-widest text-on-surface">'
        f'Work of Art · Las Vegas</span></div>\n</div>\n'
    )


def review_screenshot_figures() -> str:
    """Optional real PNG/WebP screenshots in home/google-review-screenshots/."""
    shots_dir = HOME / "google-review-screenshots"
    if not shots_dir.is_dir():
        shots_dir.mkdir(parents=True, exist_ok=True)
        readme = shots_dir / "README.txt"
        if not readme.exists():
            readme.write_text(
                "Drop Google review screenshots here (review-01.webp, review-02.webp, …).\n"
                "Re-run: python3 expand_homepage_conversion.py\n",
                encoding="utf-8",
            )
        return ""

    figures: list[str] = []
    for path in sorted(shots_dir.iterdir()):
        if path.suffix.lower() not in {".webp", ".png", ".jpg", ".jpeg"}:
            continue
        if path.name.startswith("."):
            continue
        rel = f"/{HOME_SLUG}/google-review-screenshots/{path.name}"
        webp = path.with_suffix(".webp")
        src = f"/{HOME_SLUG}/google-review-screenshots/{webp.name}" if webp.is_file() else rel
        alt = html.escape(f"Google review screenshot — Work of Art Tattoo Las Vegas")
        if webp.is_file() and path.suffix.lower() != ".webp":
            fig = (
                f'<figure class="woa-review-shot shrink-0 w-[min(78vw,260px)] md:w-[240px] snap-start">'
                f'<picture><source srcset="{src}" type="image/webp"/>'
                f'<img alt="{alt}" class="w-full h-auto rounded-sm border border-outline-variant/40 shadow-lg" '
                f'loading="lazy" src="{rel}" width="390" height="844"/></picture></figure>'
            )
        else:
            fig = (
                f'<figure class="woa-review-shot shrink-0 w-[min(78vw,260px)] md:w-[240px] snap-start">'
                f'<img alt="{alt}" class="w-full h-auto rounded-sm border border-outline-variant/40 shadow-lg" '
                f'loading="lazy" src="{rel}" width="390" height="844"/></figure>'
            )
        figures.append(fig)
    if not figures:
        return ""
    inner = "\n".join(figures)
    return f"""<div class="space-y-4">
<p class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Review screenshots</p>
<div class="woa-review-rail flex gap-4 overflow-x-auto pb-2 snap-x snap-mandatory scroll-smooth" aria-label="Google review screenshots">
{inner}
</div>
</div>"""


def featured_review_html() -> str:
    name, meta, headline, paragraphs = FEATURED_REVIEW
    initials = name.split()[0][0] + (name.split()[1][0] if len(name.split()) > 1 else "")
    body = "".join(
        f'<p class="font-body-md text-on-surface-variant leading-relaxed">{html.escape(p)}</p>'
        for p in paragraphs
    )
    return f"""<article class="woa-greview-featured bg-surface-container-high border border-outline-variant/30 p-8 md:p-10 space-y-6">
<div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-full bg-secondary/20 border border-secondary/40 flex items-center justify-center font-label-caps text-secondary">{html.escape(initials)}</div>
<div>
<p class="font-body-md text-on-surface font-medium text-lg">{html.escape(name)}</p>
<p class="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wide">{html.escape(meta)}</p>
</div>
</div>
<div class="flex gap-0.5 text-secondary" aria-label="5 out of 5 stars">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
</div>
<h3 class="font-headline-md text-on-surface text-xl md:text-2xl leading-snug">{html.escape(headline)}</h3>
<div class="space-y-4">{body}</div>
<div class="pt-4 border-t border-outline-variant/30 flex items-center gap-2">
<span class="material-symbols-outlined text-on-surface-variant text-lg">google</span>
<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Posted on Google</span>
</div>
</article>"""


def reviews_section_html() -> str:
    screenshots = review_screenshot_figures()
    featured = featured_review_html()
    cards = []
    for name, meta, quote in REVIEW_CARDS:
        cards.append(
            f"""<article class="woa-greview-card shrink-0 w-[min(88vw,320px)] md:w-[300px]">
<div class="flex items-center gap-3 mb-3">
<div class="w-10 h-10 rounded-full bg-secondary/20 border border-secondary/40 flex items-center justify-center font-label-caps text-secondary text-sm">{html.escape(name.split()[0][0] + (name.split()[1][0] if len(name.split()) > 1 else ""))}</div>
<div>
<p class="font-body-md text-on-surface font-medium">{html.escape(name)}</p>
<p class="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wide">{html.escape(meta)}</p>
</div>
<span class="material-symbols-outlined text-secondary ml-auto text-xl" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
<div class="flex gap-0.5 text-secondary mb-3" aria-hidden="true">
<span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
<p class="font-body-md text-on-surface-variant leading-relaxed text-[14px]">{html.escape(quote)}</p>
<div class="mt-4 pt-3 border-t border-outline-variant/30 flex items-center gap-2">
<span class="material-symbols-outlined text-on-surface-variant text-lg">google</span>
<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Posted on Google</span>
</div>
</article>"""
        )
    rail = "\n".join(cards)
    rail_block = ""
    if rail:
        rail_block = f"""<div class="space-y-4">
<p class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">More client feedback</p>
<div class="woa-review-rail flex gap-4 overflow-x-auto pb-4 snap-x snap-mandatory scroll-smooth" tabindex="0" aria-label="Google review highlights">
{rail}
</div>
</div>"""
    return f"""<!-- WOA_HOME_REVIEWS_START -->
<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container border-y border-outline-variant/10" id="reviews">
<div class="max-w-6xl mx-auto space-y-10">
<div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
<div class="space-y-4 max-w-2xl">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Client reviews</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Real Google reviews from people who booked here</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant">Recent feedback from locals and out-of-town clients — half sleeves, walk-ins, and long-term collectors who plan their next piece with Joshua Cole.</p>
</div>
<div class="flex flex-col sm:flex-row gap-3 shrink-0">
<a class="bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest text-center min-h-[48px] flex items-center justify-center gold-glow" href="/reviews_vault_100_verified_masterpieces/">All Reviews</a>
<a class="border border-outline-variant text-on-surface px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest text-center min-h-[48px] flex items-center justify-center hover:border-secondary transition-colors" href="/review_funnel_google_authority_hub/">Leave a Review</a>
</div>
</div>
{screenshots}
<div class="space-y-4">
<p class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Latest verified review</p>
{featured}
</div>
{rail_block}
<p class="font-body-md text-on-surface-variant text-center">Hundreds of positive Google reviews · Work of Art Tattoo &amp; Piercing, Las Vegas</p>
</div>
</section>
<!-- WOA_HOME_REVIEWS_END -->
"""


def masonry_section_html(items: list[dict]) -> str:
    tiles = "".join(picture_cell(it) for it in items[:40])
    count = len(items[:40])
    return f"""<!-- WOA_HOME_MASONRY_START -->
<div class="space-y-8 pt-12 border-t border-outline-variant/20" id="gallery-expanded">
<div class="text-center space-y-3">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Healed · Cover-Ups · Sleeves</span>
<h3 class="font-headline-md text-headline-md text-on-surface">Studio Portfolio — {count} Recent Pieces</h3>
<p class="font-body-md text-on-surface-variant max-w-2xl mx-auto">Filter by style. Every image is real Work of Art work — healed results, cover-ups, realism, and large-scale sessions.</p>
</div>
<div class="woa-gallery-masonry" id="home-gallery-masonry">
{tiles}
</div>
</div>
<!-- WOA_HOME_MASONRY_END -->
"""


def filter_buttons_html() -> str:
    return """<div aria-label="Gallery category filter" class="mt-8 mb-12 flex flex-wrap gap-3" id="gallery-filters">
<button class="px-6 py-2.5 bg-secondary text-on-secondary font-label-caps text-[11px] uppercase tracking-[0.15em] border border-secondary transition-all active:scale-95" data-filter="all" type="button">All</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="healed" type="button">Healed</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="coverups" type="button">Cover-Ups</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="black-grey" type="button">Realism</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="sleeves" type="button">Sleeves</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="fine-line" type="button">Fine Line</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="color-realism" type="button">Color</button>
<button class="px-6 py-2.5 bg-surface-container-high text-on-surface-variant font-label-caps text-[11px] uppercase tracking-[0.15em] border border-outline-variant/30 hover:border-secondary transition-all active:scale-95" data-filter="client" type="button">In-Studio</button>
</div>"""


def portfolio_rows_html(items: list[dict]) -> str:
    """Extra categorized rows inside #portfolio using unused high-value images."""
    healed = [i for i in items if "healed" in i["cats"]][:4]
    cover = [i for i in items if "coverups" in i["cats"] and i not in healed][:4]
    sleeves = [i for i in items if "sleeves" in i["cats"]][:4]
    client = [i for i in items if "client" in i["cats"]][:4]

    def row(title: str, row_items: list[dict]) -> str:
        if not row_items:
            return ""
        cells = "".join(picture_cell(x) for x in row_items)
        return f"""<div class="space-y-6">
<h3 class="font-label-caps text-on-surface uppercase tracking-widest border-l-2 border-secondary pl-4">{html.escape(title)}</h3>
<div class="grid grid-cols-2 md:grid-cols-4 gap-2 md:gap-4">
{cells}
</div>
</div>"""

    return (
        row("Healed Work", healed)
        + row("Cover-Ups &amp; Reworks", cover)
        + row("Sleeves &amp; Large Scale", sleeves)
        + row("In-Studio Sessions", client)
    )


def filter_script() -> str:
    return """<script data-woa-gallery-filter="1" type="text/javascript">(function () {
  "use strict";
  var filters = document.getElementById("gallery-filters");
  if (!filters) return;
  var buttons = filters.querySelectorAll("[data-filter]");
  var tiles = document.querySelectorAll(".woa-gallery-tile,[data-category][id='showcase-grid'] [data-category]");
  var masonry = document.querySelectorAll("#home-gallery-masonry .woa-gallery-tile");
  var allTiles = document.querySelectorAll(".woa-gallery-tile, #showcase-grid [data-category]");

  function setActive(btn) {
    buttons.forEach(function (b) {
      var on = b === btn;
      b.classList.toggle("bg-secondary", on);
      b.classList.toggle("text-on-secondary", on);
      b.classList.toggle("border-secondary", on);
      b.classList.toggle("bg-surface-container-high", !on);
      b.classList.toggle("text-on-surface-variant", !on);
      b.classList.toggle("border-outline-variant/30", !on);
    });
  }

  function apply(filter) {
    allTiles.forEach(function (el) {
      var cats = (el.getAttribute("data-category") || "").split(/\\s+/);
      var show = filter === "all" || cats.indexOf(filter) >= 0;
      el.style.display = show ? "" : "none";
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setActive(btn);
      apply(btn.getAttribute("data-filter") || "all");
    });
  });
})();</script>"""


def patch_css() -> None:
    block = """
/* Homepage conversion gallery + reviews (expand_homepage_conversion.py) */
.woa-review-rail {
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: rgba(233, 195, 73, 0.45) transparent;
}
.woa-review-rail::-webkit-scrollbar {
  height: 6px;
}
.woa-review-rail::-webkit-scrollbar-thumb {
  background: rgba(233, 195, 73, 0.45);
  border-radius: 3px;
}
.woa-review-shot {
  scroll-snap-align: start;
}
.woa-review-shot img {
  max-height: min(52vh, 520px);
  object-fit: cover;
  object-position: top center;
}
.woa-greview-card {
  scroll-snap-align: start;
  background: linear-gradient(145deg, #1c1b1b 0%, #131313 100%);
  border: 1px solid rgba(68, 71, 72, 0.55);
  padding: 1.25rem 1.35rem;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
}
.woa-gallery-masonry {
  columns: 2;
  column-gap: 0.5rem;
}
@media (min-width: 768px) {
  .woa-gallery-masonry {
    columns: 3;
    column-gap: 0.75rem;
  }
}
@media (min-width: 1024px) {
  .woa-gallery-masonry {
    columns: 4;
    column-gap: 1rem;
  }
}
.woa-gallery-masonry .woa-gallery-tile {
  break-inside: avoid;
  margin-bottom: 0.5rem;
}
@media (min-width: 768px) {
  .woa-gallery-masonry .woa-gallery-tile {
    margin-bottom: 0.75rem;
  }
}
"""
    text = CSS.read_text(encoding="utf-8")
    needle = "/* Homepage conversion gallery"
    if needle in text:
        return
    CSS.write_text(text.rstrip() + block, encoding="utf-8")


def patch_html(items: list[dict]) -> None:
    text = CODE.read_text(encoding="utf-8")

    reviews = reviews_section_html()
    if "WOA_HOME_REVIEWS_START" in text:
        text = re.sub(
            r"<!-- WOA_HOME_REVIEWS_START -->.*?<!-- WOA_HOME_REVIEWS_END -->",
            reviews,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        for anchor in (
            "</section>\n<!-- Portfolio Showcase Section -->",
            "</section>\n<!-- Discount Offer Section -->",
            "</section>\n<!-- Tattoo shop near me (local SEO) -->",
        ):
            if anchor in text:
                text = text.replace(anchor, "</section>\n" + reviews + "\n" + anchor.split("\n", 1)[1], 1)
                break
        else:
            text = text.replace(
                '<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop space-y-10 md:space-y-section-gap" id="gallery">',
                reviews + '\n<section class="py-16 md:py-section-gap px-margin-mobile md:px-margin-desktop space-y-10 md:space-y-section-gap" id="gallery">',
                1,
            )

    new_filters = filter_buttons_html()
    text = re.sub(
        r'<div aria-label="Gallery category filter" class="mt-8 mb-12 flex flex-wrap gap-3">.*?</div>\s*<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">',
        new_filters + '\n<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter" id="showcase-grid">',
        text,
        count=1,
        flags=re.DOTALL,
    )

    masonry = masonry_section_html(items)
    if "WOA_HOME_MASONRY_START" in text:
        text = re.sub(
            r"<!-- WOA_HOME_MASONRY_START -->.*?<!-- WOA_HOME_MASONRY_END -->",
            masonry,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        text = text.replace(
            '<div class="flex justify-center pt-8">\n<a class="bg-transparent text-on-surface px-12 py-5',
            masonry
            + '\n<div class="flex justify-center pt-8">\n<a class="bg-transparent text-on-surface px-12 py-5',
            1,
        )

    extra_rows = portfolio_rows_html(items)
    marker = "<!-- Fine Line Category -->"
    if extra_rows and marker in text and "Healed Work" not in text:
        text = text.replace(marker, extra_rows + "\n" + marker, 1)

    pierce_placeholders = """<div class="aspect-square bg-surface-container-high flex items-center justify-center p-4 border border-outline-variant/30">
<span class="font-label-caps text-on-surface-variant text-center">No Ego.<br/>Just Art.</span>
</div>
<div class="aspect-square bg-surface-container-high flex items-center justify-center p-4 border border-outline-variant/30">
<span class="font-label-caps text-on-surface-variant text-center">Vegas Style<br/>Without the Attitude</span>
</div>"""
    if pierce_placeholders in text:
        replacement = picture_cell(
            next(i for i in items if "healed" in i["cats"]),
            lazy=True,
        ) + picture_cell(
            next((i for i in items if "coverups" in i["cats"]), items[0]),
            lazy=True,
        )
        text = text.replace(pierce_placeholders, replacement, 1)

    if "data-woa-gallery-filter" not in text:
        text = text.replace("</body>", filter_script() + "\n</body>", 1)

    nav_reviews = 'href="/#faq">Reviews</a>'
    nav_reviews_new = 'href="/#reviews">Reviews</a>'
    text = text.replace(nav_reviews, nav_reviews_new)

    footer_reviews = 'href="#faq">Client Reviews</a>'
    if footer_reviews in text:
        text = text.replace(footer_reviews, 'href="/#reviews">Client Reviews</a>', 1)

    CODE.write_text(text, encoding="utf-8")


def main() -> int:
    items = discover_images()
    if len(items) < 30:
        print(f"Warning: only {len(items)} unique images found")
    patch_css()
    patch_html(items)
    print(f"Homepage updated: {len(items)} portfolio images catalogued, reviews section added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build merchandise/code.html — Joshua Cole original art & merch in current site style."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from woa_merchandise_manifest import CANON, MERCH_ITEMS, MerchItem, SLUG
from woa_nav_config import (
    HREF_BOOKING_MAILTO,
    STUDIO_BOOKING_EMAIL,
    STUDIO_BOOKING_LINK_LABEL,
    STUDIO_PHONE_PARENS,
    STUDIO_PHONE_TEL,
)

try:
    from fix_studio_booking_email import inject_schema_email, replace_legacy_emails
except ImportError:  # pragma: no cover
    def replace_legacy_emails(text: str) -> str:
        return text

    def inject_schema_email(text: str) -> str:
        return text

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / SLUG
OUT = OUT_DIR / "code.html"
TEMPLATE = ROOT / "offsite_bookings" / "code.html"

TITLE = "Merchandise & Original Art | Work of Art Tattoo Las Vegas"
DESCRIPTION = (
    "Original drawings and fine art by Joshua Cole — graphite, Prismacolor, watercolor, and mixed media. "
    f"Inquire in-studio or email {STUDIO_BOOKING_EMAIL}. Work of Art Tattoo & Piercing, Las Vegas."
)

OG_IMAGE_STEM = "colored-pencil-bridges-framed"

MERCH_CSS = """
<style data-woa-merch-css="1">
.woa-merch-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}
@media (min-width: 768px) {
  .woa-merch-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.5rem;
  }
}
.woa-merch-card {
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(68, 71, 72, 0.45);
  background: #0a0a0a;
  transition: border-color 0.2s ease, transform 0.2s ease;
}
.woa-merch-card:hover {
  border-color: rgba(233, 195, 73, 0.55);
  transform: translateY(-2px);
}
.woa-merch-photo {
  aspect-ratio: 4 / 5;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.woa-merch-photo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  background: #000;
}
.woa-merch-body {
  padding: 1rem 1.1rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}
.woa-merch-body h3 {
  font-size: 0.95rem;
  line-height: 1.35;
}
.woa-merch-body p {
  font-size: 0.8125rem;
  line-height: 1.5;
  flex: 1;
}
.woa-merch-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: 0.35rem;
  padding: 0.55rem 0.85rem;
  border: 1px solid rgba(233, 195, 73, 0.45);
  color: #e9c349;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
}
.woa-merch-cta:hover {
  background: rgba(233, 195, 73, 0.12);
  color: #ffe088;
}
</style>
"""


def download_assets(items: tuple[MerchItem, ...]) -> list[MerchItem]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok: list[MerchItem] = []
    for item in items:
        dst = OUT_DIR / f"{item.stem}.{item.ext}"
        if not dst.is_file():
            try:
                urllib.request.urlretrieve(item.source_url, dst)
                print(f"[dl] {item.stem}.{item.ext}")
            except OSError as exc:
                print(f"[warn] skip {item.stem}: {exc}")
                continue
        if item.ext != "webp" and shutil.which("cwebp"):
            webp = OUT_DIR / f"{item.stem}.webp"
            if not webp.is_file() or webp.stat().st_mtime < dst.stat().st_mtime:
                subprocess.run(
                    ["cwebp", "-q", "85", str(dst), "-o", str(webp)],
                    check=False,
                    capture_output=True,
                )
        ok.append(item)
    return ok


def picture(item: MerchItem) -> str:
    alt = html.escape(f"{item.title} — Joshua Cole original art, Work of Art Las Vegas")
    webp = OUT_DIR / f"{item.stem}.webp"
    if webp.is_file():
        return f"""<picture>
<source srcset="/{SLUG}/{item.stem}.webp" type="image/webp"/>
<img alt="{alt}" class="w-full h-full object-contain object-center" decoding="async" loading="lazy" src="/{SLUG}/{item.stem}.{item.ext}"/>
</picture>"""
    return f"""<img alt="{alt}" class="w-full h-full object-contain object-center" decoding="async" loading="lazy" src="/{SLUG}/{item.stem}.{item.ext}"/>"""


def merch_mailto(subject: str) -> str:
    return f"{HREF_BOOKING_MAILTO}?subject={urllib.parse.quote(subject, safe='')}"


def merch_card(item: MerchItem) -> str:
    title = html.escape(item.title)
    detail = html.escape(item.detail)
    mail_href = merch_mailto(f"Merchandise inquiry — {item.title}")
    return f"""<article class="woa-merch-card">
<div class="woa-merch-photo">{picture(item)}</div>
<div class="woa-merch-body">
<h3 class="font-headline-md text-on-surface">{title}</h3>
<p class="font-body-md text-on-surface-variant">{detail}</p>
<a class="woa-merch-cta" href="{mail_href}">Inquire by email</a>
</div>
</article>"""


def build_main(items: list[MerchItem]) -> str:
    cards = "".join(merch_card(i) for i in items)
    return f"""
<main class="relative pt-20">
<section class="px-margin-mobile md:px-margin-desktop pb-10 md:pb-14 bg-background border-b border-outline-variant/20">
<div class="max-w-4xl mx-auto space-y-5">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Joshua Cole · original art</span>
<h1 class="font-headline-xl text-[34px] sm:text-[40px] md:text-headline-xl text-on-surface leading-tight">Merchandise &amp; one-of-a-kind pieces</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant leading-relaxed max-w-2xl">
Every piece below is original work by Joshua Cole — graphite, Prismacolor, watercolor, and mixed media. Items are available in-studio at 2375 E. Tropicana Ave, Suite 3 or by email. Prices vary; inquire for the piece you want.
</p>
<div class="flex flex-col sm:flex-row flex-wrap gap-3 pt-1">
<a class="inline-flex justify-center bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest gold-glow transition-all" href="{merch_mailto('Merchandise inquiry')}">{STUDIO_BOOKING_LINK_LABEL}</a>
<a class="inline-flex justify-center border border-outline px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest hover:border-secondary transition-colors" href="{STUDIO_PHONE_TEL}">Call {STUDIO_PHONE_PARENS}</a>
<a class="inline-flex justify-center border border-outline-variant/50 px-8 py-4 font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant hover:text-secondary hover:border-secondary transition-colors" href="/artists/joshua-cole/">Joshua Cole portfolio</a>
</div>
</div>
</section>

<section class="py-12 md:py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-b border-outline-variant/10">
<div class="max-w-6xl mx-auto space-y-8">
<div class="text-center space-y-3 max-w-2xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">Available now</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Original art &amp; collectibles</h2>
<p class="font-body-md text-on-surface-variant">Studio photography on black — each piece is one of a kind. Email for availability and pricing.</p>
</div>
<div class="woa-merch-grid">{cards}</div>
</div>
</section>

<section class="py-12 md:py-16 px-margin-mobile md:px-margin-desktop bg-background text-center">
<div class="max-w-2xl mx-auto space-y-5">
<h2 class="font-headline-md text-on-surface">Visit the studio to see pieces in person</h2>
<p class="font-body-md text-on-surface-variant">Walk-ins welcome when the schedule allows. Ask for Joshua or mention the piece title when you arrive.</p>
<a class="inline-flex justify-center bg-secondary text-on-secondary px-10 py-4 font-label-caps text-label-caps uppercase tracking-widest gold-glow transition-all" href="/appointments/">Book a visit</a>
</div>
</section>
</main>
"""


def patch_meta(html_text: str) -> str:
    og_img = f"{CANON}{OG_IMAGE_STEM}.webp"
    html_text = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html_text, count=1)
    html_text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{DESCRIPTION}" name="description"/>',
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'<link href="https://www.workofarttattoo.com/[^"]*" rel="canonical"/>',
        f'<link href="{CANON}" rel="canonical"/>',
        html_text,
        count=1,
    )
    for prop, val in (
        ("og:url", CANON),
        ("og:title", TITLE),
        ("og:description", DESCRIPTION),
        ("og:image", og_img),
    ):
        html_text = re.sub(
            rf'<meta content="[^"]*" property="{prop}"/>',
            f'<meta content="{val}" property="{prop}"/>',
            html_text,
            count=1,
        )
    for name, val in (
        ("twitter:title", TITLE),
        ("twitter:description", DESCRIPTION),
        ("twitter:image", og_img),
    ):
        html_text = re.sub(
            rf'<meta content="[^"]*" name="{name}"/>',
            f'<meta content="{val}" name="{name}"/>',
            html_text,
            count=1,
        )
    return html_text


def patch_main(html_text: str, main: str) -> str:
    html_text = re.sub(
        r'<script data-woa-entity-schema="1" type="application/ld\\+json">.*?</script>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<main class="relative pt-20">.*?</main>',
        main.strip(),
        html_text,
        count=1,
        flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<nav[^>]*data-woa-topic-cluster="1"[^>]*>.*?</nav>\s*',
        "",
        html_text,
        flags=re.DOTALL,
    )
    if 'data-woa-merch-css="1"' not in html_text:
        html_text = html_text.replace("</head>", MERCH_CSS + "\n</head>", 1)
    return html_text


def main() -> int:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    items = download_assets(MERCH_ITEMS)
    if not items:
        raise SystemExit("No merchandise assets downloaded")
    html_text = TEMPLATE.read_text(encoding="utf-8")
    html_text = patch_meta(html_text)
    html_text = patch_main(html_text, build_main(items))
    html_text = replace_legacy_emails(html_text)
    html_text = inject_schema_email(html_text)
    OUT.write_text(html_text, encoding="utf-8")
    print(f"[ok] {OUT.relative_to(ROOT)} — {len(items)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

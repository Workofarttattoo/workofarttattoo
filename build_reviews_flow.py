#!/usr/bin/env python3
"""Upgrade /reviews/ and point the older leave-a-review URL at that canonical."""

from __future__ import annotations

import re
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent
GOOGLE_URL = (
    "https://www.google.com/maps/search/?api=1&query="
    "Work+of+Art+Tattoo+%26+Piercing+Las+Vegas"
)
GOOGLE_HREF = GOOGLE_URL.replace("&", "&amp;")
QR_WEB = "/reviews/google-maps-listing-qr.png"
CANONICAL = "https://www.workofarttattoo.com/reviews/"

FLOW = f"""
<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background border-y border-outline-variant/20" data-woa-review-flow="1" id="leave-a-google-review">
<div class="max-w-3xl mx-auto space-y-8">
<h2 class="font-headline-lg text-on-surface">Why a review helps</h2>
<p class="font-body-md text-on-surface-variant">People compare studios before they book. A review in your own words tells them what the consult, the session, and the shop were like. If you also want the studio to keep a healed photo, say so below and send the image by text or email. This form does not upload files.</p>
<p class="font-body-md text-on-surface-variant">The button and QR code open the Google Maps listing already published on this site: a search for Work of Art Tattoo &amp; Piercing, Las Vegas. The site files do not include a direct Google write-a-review link, so this is that same business listing. It is not a new place id.</p>
<p><a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest" href="{GOOGLE_HREF}" rel="noopener noreferrer" target="_blank">Open our Google listing</a></p>
<p id="woa-review-thanks" class="hidden font-body-md text-secondary" hidden>Thank you — your note was sent.</p>
<form action="https://formsubmit.co/thewhiteknight702@gmail.com" class="space-y-5 text-left" method="POST">
<input name="_subject" type="hidden" value="Review follow-up — healed photo or text permission"/>
<input name="_captcha" type="hidden" value="false"/>
<input name="_template" type="hidden" value="table"/>
<input name="_next" type="hidden" value="https://www.workofarttattoo.com/reviews/?sent=review-followup"/>
<input name="source_page" type="hidden" value="{CANONICAL}"/>
<input name="request_type" type="hidden" value="healed photo or review permission"/>
<label class="block space-y-2"><span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">Name</span><input class="w-full bg-background border border-outline-variant px-4 py-3 text-on-surface" name="name" type="text"/></label>
<label class="block space-y-2"><span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">Email *</span><input class="w-full bg-background border border-outline-variant px-4 py-3 text-on-surface" name="email" required type="email"/></label>
<label class="block space-y-2"><span class="font-label-caps text-[11px] uppercase tracking-widest text-on-surface-variant">Note</span><textarea class="w-full bg-background border border-outline-variant px-4 py-3 text-on-surface min-h-[120px]" name="message" placeholder="What should we know?"></textarea></label>
<label class="flex items-start gap-3"><input class="mt-1 accent-secondary" name="text_permission" type="checkbox" value="yes"/><span class="font-body-md text-on-surface-variant">You may quote this note on the studio site.</span></label>
<label class="flex items-start gap-3"><input class="mt-1 accent-secondary" name="healed_photo" type="checkbox" value="will email or text the image"/><span class="font-body-md text-on-surface-variant">I will send a healed photo by text or by replying to the studio email. I am not uploading a file here.</span></label>
<button class="bg-secondary text-on-secondary px-8 py-4 font-label-caps text-label-caps uppercase tracking-widest" type="submit">Send to the studio</button>
</form>
</div>
</section>
<script>
if (location.search.indexOf("sent=review-followup") >= 0) {{
  var note = document.getElementById("woa-review-thanks");
  if (note) {{ note.hidden = false; note.classList.remove("hidden"); }}
}}
</script>
"""

FLOW_RE = re.compile(
    r'\s*<section[^>]*data-woa-review-flow="1"[\s\S]*?</section>\s*<script>\s*if \(location\.search\.indexOf\("sent=review-followup"\)[\s\S]*?</script>\s*',
    re.MULTILINE,
)
SITEMAP_BLOCK = re.compile(
    r"\s*<url>\s*<loc>https://www\.workofarttattoo\.com/leave-a-review/</loc>.*?</url>",
    re.DOTALL,
)


def write_qr() -> None:
    dest = ROOT / "reviews" / "google-maps-listing-qr.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    segno.make(GOOGLE_URL, error="m").save(
        dest, scale=8, border=2, dark="#131313", light="#ffffff"
    )
    print(f"[ok] {dest.relative_to(ROOT)}")


def patch_reviews_page(path: Path) -> None:
    if not path.is_file():
        print(f"[skip] missing {path}")
        return
    raw = path.read_text(encoding="utf-8")
    updated = raw.replace('href="/leave-a-review/"', f'href="{GOOGLE_HREF}" rel="noopener noreferrer" target="_blank"')
    updated = updated.replace(
        "/leave-a-review/google-review-qr-code-nfc-sign-work-of-art-tattoo.png",
        QR_WEB,
    )
    updated = updated.replace(
        'alt="Google review qr code nfc sign tattoo — Leave a Google Review, Work of Art Tattoo &amp; Piercing, Las Vegas"',
        'alt="QR code for the Google Maps listing of Work of Art Tattoo and Piercing, Las Vegas"',
    )
    caption = (
        '<p class="mt-8 font-label-caps text-label-caps text-secondary">SCAN TO START</p>'
        '<p class="mt-4 font-body-md text-on-surface-variant text-center max-w-sm">This code opens the Google Maps listing already published on the site. '
        "The site files do not include a direct write-a-review link, so the code uses that same business listing.</p>"
    )
    needle = '<p class="mt-8 font-label-caps text-label-caps text-secondary">SCAN TO START</p>'
    if "This code opens the Google Maps listing" not in updated and needle in updated:
        updated = updated.replace(needle, caption, 1)
    updated = FLOW_RE.sub("\n", updated)
    anchor = "<!-- Conversion / Feedback Section -->"
    if anchor in updated:
        updated = updated.replace(anchor, FLOW + anchor, 1)
    elif "data-woa-review-flow" not in updated and "</main>" in updated:
        updated = updated.replace("</main>", FLOW + "\n</main>", 1)
    if updated != raw:
        path.write_text(updated, encoding="utf-8")
        print(f"[ok] {path.relative_to(ROOT)}")
    else:
        print(f"[skip] {path.relative_to(ROOT)}")


def retire_duplicate(path: Path) -> None:
    if not path.is_file():
        print(f"[skip] missing {path}")
        return
    raw = path.read_text(encoding="utf-8")
    updated = raw.replace(
        '<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>',
        '<meta content="noindex, follow" name="robots"/>',
    )
    updated = updated.replace(
        '<link href="https://www.workofarttattoo.com/leave-a-review/" rel="canonical"/>',
        f'<link href="{CANONICAL}" rel="canonical"/>',
    )
    updated = updated.replace(
        '<meta content="https://www.workofarttattoo.com/leave-a-review/" property="og:url"/>',
        f'<meta content="{CANONICAL}" property="og:url"/>',
    )
    note = (
        '<p class="font-body-md text-on-surface-variant max-w-2xl mb-6" data-woa-review-canonical-note="1">'
        'The review page for this studio is <a class="text-secondary underline" href="/reviews/">Client reviews</a>. '
        "This address stays available so older links still open.</p>\n"
    )
    h1 = '<h1 class="font-headline-xl text-headline-lg-mobile md:text-headline-xl mb-6">Client reviews &amp; healed work</h1>'
    if "data-woa-review-canonical-note" not in updated and h1 in updated:
        updated = updated.replace(h1, h1 + "\n" + note, 1)
    if updated != raw:
        path.write_text(updated, encoding="utf-8")
        print(f"[ok] noindex {path.relative_to(ROOT)}")
    else:
        print(f"[skip] {path.relative_to(ROOT)}")


def drop_sitemap_url() -> None:
    for name in ("sitemap.xml", "sitemap-static-pages.xml"):
        path = ROOT / name
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        updated = SITEMAP_BLOCK.sub("", raw)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            print(f"[ok] removed leave-a-review from {name}")


def main() -> int:
    write_qr()
    for rel in (
        "reviews/code.html",
        "reviews_vault_100_verified_masterpieces/code.html",
    ):
        patch_reviews_page(ROOT / rel)
    for rel in (
        "leave-a-review/code.html",
        "review_funnel_google_authority_hub/code.html",
    ):
        retire_duplicate(ROOT / rel)
    drop_sitemap_url()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

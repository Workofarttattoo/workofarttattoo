#!/usr/bin/env python3
"""Implement the next SEO growth actions we can do from the static site repo."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://workofarttattoo.com"

PRIORITY_URLS: tuple[tuple[str, str, str], ...] = (
    ("Homepage", "/", "Primary local entity and strongest branded result"),
    ("Appointments", "/appointments/", "Main conversion page"),
    ("Artists", "/artists/", "Routes Joshua and Katelyn queries"),
    ("Joshua Cole", "/artists/joshua-cole/", "Tattoo artist entity page"),
    ("Katelyn Cole", "/artists/katelyn-cole/", "Piercing artist entity page"),
    ("Tattoo pricing", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/", "Already ranking; push recrawl and links"),
    ("Cover-up tattoos", "/cover-up-tattoos-las-vegas/", "Money page for competitive cover-up intent"),
    ("Fine line tattoos", "/fine_line_tattoos_las_vegas_master_authority_guide/", "Money page for broad service intent"),
    ("Realism tattoos", "/realism-tattoos-las-vegas/", "Joshua/service match"),
    ("Body piercing guide", "/body_piercing_guide_las_vegas/", "Strong branded/service result"),
    ("Piercing guide", "/piercing-guide-las-vegas/", "Main piercing hub"),
    ("Helix piercing", "/helix-piercing-las-vegas/", "Long-tail piercing page"),
    ("Piercing jewelry", "/piercing_jewelry_guide_las_vegas/", "Trust/quality support page"),
    ("Near the Strip", "/tattoo_shop_near_the_strip_nap_corrected/", "Local geo hub"),
    ("Near MGM Grand", "/tattoo_shop_near_mgm_grand_las_vegas/", "Hotel/location long-tail"),
    ("Near the Sphere", "/tattoo_shop_near_the_sphere_las_vegas/", "Event/location long-tail"),
    ("Reviews", "/reviews_vault_100_verified_masterpieces/", "Trust page"),
    ("Studio videos", "/studio_videos/", "Proof and freshness"),
    ("Healing database", "/healing_database_tattoo_timeline_encyclopedia_las_vegas/", "New authority hub"),
    ("Skin science", "/skin_science_tattoo_dermatology_authority_guide/", "New authority hub"),
    ("Knowledge base", "/knowledge/", "Q&A hub"),
)


def link_card(title: str, href: str, text: str) -> str:
    return (
        '<a class="block border border-outline-variant/30 bg-background/40 p-4 '
        'hover:border-secondary transition-colors" '
        f'href="{href}">'
        f'<h3 class="font-headline-md text-on-surface text-lg">{title}</h3>'
        f'<p class="font-body-md text-on-surface-variant text-sm mt-2">{text}</p>'
        "</a>"
    )


def growth_block(marker: str, title: str, intro: str, cards: tuple[tuple[str, str, str], ...]) -> str:
    cards_html = "\n".join(link_card(*card) for card in cards)
    return f"""
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-background border-y border-outline-variant/20" data-woa-seo-growth="{marker}">
<div class="max-w-5xl mx-auto space-y-6">
<div class="max-w-3xl space-y-3">
<p class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Popular starting points</p>
<h2 class="font-headline-md text-on-surface text-2xl">{title}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">{intro}</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{cards_html}
</div>
</div>
</section>
"""


BLOCKS: dict[str, str] = {
    "home_work_of_art_tattoo_piercing/code.html": growth_block(
        "homepage-priority-links",
        "Start with the page that matches your question",
        "These are the pages people use most when they are comparing studios, checking price, or deciding whether to book.",
        (
            ("Tattoo pricing in Las Vegas", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/", "What affects price, session length, deposits, and how to ask for a realistic quote."),
            ("Cover-up tattoos", "/cover-up-tattoos-las-vegas/", "How we look at old ink, darkness, size, and whether laser needs to come first."),
            ("Fine line tattoos", "/fine_line_tattoos_las_vegas_master_authority_guide/", "What makes fine line work age well, where it works best, and when to adjust the idea."),
            ("Complete piercing guide", "/piercing-guide-las-vegas/", "Piercing placement, jewelry, healing, and how Katelyn plans anatomy-first work."),
            ("Near the Strip", "/tattoo_shop_near_the_strip_nap_corrected/", "Studio directions and why a short ride off the Strip can be worth it."),
            ("Reviews and healed proof", "/reviews_vault_100_verified_masterpieces/", "Client reviews, proof, and what to look for before trusting a studio."),
        ),
    ),
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide/code.html": growth_block(
        "pricing-cluster-links",
        "Price depends on the kind of tattoo",
        "A realistic quote starts with style, size, placement, existing ink, and how much drawing time the piece needs.",
        (
            ("Cover-up pricing", "/cover-up-tattoos-las-vegas/", "Old ink changes the plan, size, and sometimes the number of sessions."),
            ("Fine line tattoos", "/fine_line_tattoos_las_vegas_master_authority_guide/", "Small does not always mean simple; placement and detail matter."),
            ("Choose the right artist", "/how_to_choose_a_tattoo_artist_master_selection_guide_2/", "A cheaper mismatch costs more than a clean consult."),
        ),
    ),
    "cover-up-tattoos-las-vegas/code.html": growth_block(
        "coverup-cluster-links",
        "Plan the cover-up before chasing the design",
        "Cover-ups work best when the new piece is designed around what is already in the skin, not pasted over it.",
        (
            ("Tattoo pricing guide", "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/", "Budget for size, darkness, drawing time, and possible sessions."),
            ("Healed cover-up gallery", "/healed_cover_up_tattoos_las_vegas/", "Compare healed proof before deciding what is possible."),
            ("Joshua Cole portfolio", "/artists/joshua-cole/", "See the artist behind black and grey, realism, and cover-up planning."),
        ),
    ),
    "fine_line_tattoos_las_vegas_master_authority_guide/code.html": growth_block(
        "fine-line-cluster-links",
        "Fine line needs the right expectations",
        "Clean fine line work is about restraint: size, placement, skin texture, and how much detail can stay readable after healing.",
        (
            ("Fine line pain level", "/knowledge/fine-line-tattoo-pain-level/", "Quick answer for first-timers comparing placements."),
            ("Healed fine line gallery", "/healed_fine_line_tattoos_las_vegas/", "Use healed examples to judge detail and longevity."),
            ("Book a consult", "/appointments/", "Send size, placement, and references before choosing the smallest version."),
        ),
    ),
    "piercing-guide-las-vegas/code.html": growth_block(
        "piercing-cluster-links",
        "Piercing starts with anatomy and jewelry",
        "The best-looking piercing is the one that is placed for your anatomy and fitted with jewelry that can heal cleanly.",
        (
            ("Helix piercing guide", "/helix-piercing-las-vegas/", "Cartilage placement, sleeping pressure, downsizing, and healing expectations."),
            ("Piercing jewelry guide", "/piercing_jewelry_guide_las_vegas/", "Why implant-grade jewelry and sizing matter."),
            ("Katelyn Cole", "/artists/katelyn-cole/", "Meet the piercer for anatomy checks, ear styling, and jewelry changes."),
        ),
    ),
    "helix-piercing-las-vegas/code.html": growth_block(
        "helix-cluster-links",
        "After helix, the next decision is jewelry",
        "Helix piercings look best when the first jewelry protects healing, then styling comes after swelling settles.",
        (
            ("Piercing jewelry guide", "/piercing_jewelry_guide_las_vegas/", "Learn why size, metal, and threadless jewelry matter."),
            ("Ear curation guide", "/ear_curation_piercing_las_vegas_authority_guide/", "Plan a balanced ear instead of one isolated piercing."),
            ("Book with Katelyn", "/appointments/", "Send a note if you want a helix, stacked lobe, conch, or full ear plan."),
        ),
    ),
    "tattoo_shop_near_the_strip_nap_corrected/code.html": growth_block(
        "strip-location-links",
        "Nearby pages for Vegas visitors",
        "If you are comparing shops from a hotel, start with the page closest to where you are staying, then book through the same appointment form.",
        (
            ("Near MGM Grand", "/tattoo_shop_near_mgm_grand_las_vegas/", "Short ride from the south Strip and arena traffic."),
            ("Near the Sphere", "/tattoo_shop_near_the_sphere_las_vegas/", "Useful for event weekends and show traffic."),
            ("Official location and hours", "/official_location_hours_contact/", "Address, phone, hours, ID reminders, and arrival details."),
        ),
    ),
}


def insert_before_main_end(html: str, addition: str) -> str:
    marker = addition.split('data-woa-seo-growth="', 1)[1].split('"', 1)[0]
    if f'data-woa-seo-growth="{marker}"' in html:
        return html
    if "</main>" in html:
        return html.replace("</main>", addition + "\n</main>", 1)
    return html + addition


def write_text_artifacts() -> None:
    recrawl = ROOT / "search_console_recrawl_urls.csv"
    with recrawl.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["priority", "label", "url", "reason"])
        for i, (label, path, reason) in enumerate(PRIORITY_URLS, start=1):
            writer.writerow([i, label, f"{SITE}{path}", reason])

    gbp = ROOT / "google_business_profile_posts.md"
    gbp.write_text(
        """# Google Business Profile Post Drafts

Use one post every 2-3 days. Add a real studio/client image when posting.

## Tattoo Pricing
Wondering what affects tattoo pricing in Las Vegas? Size, placement, detail, cover-up needs, and drawing time all matter. We wrote a plain-English pricing guide so you can send a better request before booking.

CTA: Learn more
Link: https://workofarttattoo.com/how_much_do_tattoos_cost_in_las_vegas_authority_guide/

## Cover-Up Tattoos
Cover-ups need planning, not guesswork. Bring a clear photo of the old tattoo, the size you want, and the style you are open to. We will tell you honestly what can be covered and what needs more prep.

CTA: Book
Link: https://workofarttattoo.com/cover-up-tattoos-las-vegas/

## Piercing & Jewelry
A good piercing starts with anatomy and jewelry that can heal cleanly. Katelyn handles piercings, ear styling, jewelry changes, and placement checks at Work of Art on E. Tropicana.

CTA: Book
Link: https://workofarttattoo.com/piercing-guide-las-vegas/

## Fine Line Tattoos
Fine line tattoos need the right size, placement, and expectations so the work stays readable as it heals. Send references and we will help shape the idea before tattoo day.

CTA: Book
Link: https://workofarttattoo.com/fine_line_tattoos_las_vegas_master_authority_guide/

## Near the Strip
Staying near the Strip? Work of Art Tattoo & Piercing is a short ride from the resort corridor, with tattoos, piercings, consultations, and real studio portfolio work on display.

CTA: Directions
Link: https://workofarttattoo.com/tattoo_shop_near_the_strip_nap_corrected/
""",
        encoding="utf-8",
    )

    reviews = ROOT / "review_request_playbook.md"
    reviews.write_text(
        """# Review Request Playbook

Goal: fresh reviews that mention real services, not generic praise.

## Ask after a tattoo
Thank you again for coming in. If you are happy with the experience, a Google review helps people find the right studio. Mentioning the type of work helps a lot: cover-up, fine line, black and grey, realism, walk-in, or custom tattoo.

## Ask after a piercing
Thank you for trusting Katelyn/Work of Art. If the placement, jewelry, or appointment felt good, a Google review helps other piercing clients know what to expect. Helpful words: helix, ear piercing, jewelry change, anatomy check, piercing Las Vegas.

## Ask after a healed check-in
Glad to see it healing well. If you have a minute, a review that mentions the healed result helps future clients compare studios more honestly.

## Service phrases to naturally earn
- cover-up tattoo Las Vegas
- fine line tattoo Las Vegas
- black and grey tattoo
- realism tattoo
- helix piercing Las Vegas
- body piercing Las Vegas
- tattoo shop near the Strip
- clean studio
- listened to my idea
- healed well
""",
        encoding="utf-8",
    )

    citations = ROOT / "citation_outreach_targets.csv"
    rows = [
        ("Google Business Profile", "Update posts/services/photos weekly", "https://business.google.com/"),
        ("Bing Places", "Sync NAP and add website/service links", "https://www.bingplaces.com/"),
        ("Apple Business Connect", "Verify NAP, hours, photos", "https://businessconnect.apple.com/"),
        ("Yelp", "Check categories and service descriptions", "https://biz.yelp.com/"),
        ("Las Vegas local/event blogs", "Pitch offsite/private event tattoo page", "https://workofarttattoo.com/offsite_bookings/"),
        ("Tattoo/piercing resource mentions", "Pitch piercing guide and jewelry standards page", "https://workofarttattoo.com/piercing-guide-las-vegas/"),
    ]
    with citations.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["target", "action", "url"])
        writer.writerows(rows)


def main() -> int:
    changed = 0
    for rel, addition in BLOCKS.items():
        path = ROOT / rel
        if not path.is_file():
            print(f"[skip] {rel}")
            continue
        raw = path.read_text(encoding="utf-8")
        updated = insert_before_main_end(raw, addition)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] SEO growth links: {rel}")
    write_text_artifacts()
    print(f"[done] updated {changed} page(s); wrote recrawl, GBP, review, and citation files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

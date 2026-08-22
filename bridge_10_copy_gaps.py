#!/usr/bin/env python3
"""Add human trust/clarity sections that bridge the last SEO/conversion gaps."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def block(title: str, body: str, items: tuple[str, ...], marker: str) -> str:
    lis = "\n".join(f"<li>{item}</li>" for item in items)
    return f"""
<section class="py-12 px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" data-woa-gap-bridge="{marker}">
<div class="max-w-4xl mx-auto space-y-5">
<p class="font-label-caps text-[10px] uppercase tracking-[0.2em] text-secondary">Before you book</p>
<h2 class="font-headline-md text-on-surface text-2xl">{title}</h2>
<p class="font-body-md text-on-surface-variant leading-relaxed">{body}</p>
<ul class="font-body-md text-on-surface-variant space-y-2 list-disc pl-5">
{lis}
</ul>
</div>
</section>
"""


SECTIONS: dict[str, str] = {
    "home_work_of_art_tattoo_piercing/code.html": block(
        "Pick the path that matches what you need",
        "Most people land here with one of three questions: who should I book with, what will it cost, and whether the studio feels right. Start with the service that fits, then send references so we can point you the right way.",
        (
            '<strong class="text-on-surface">Tattoo consult:</strong> best for custom work, cover-ups, sleeves, portraits, fine line, and projects that need drawing time.',
            '<strong class="text-on-surface">Piercing appointment:</strong> best for anatomy checks, jewelry upgrades, ear curation, and first-time piercings.',
            '<strong class="text-on-surface">Just have questions:</strong> use the appointment form anyway; a quick note with photos is usually enough to get started.',
        ),
        "homepage-service-routing",
    ),
    "appointments/code.html": block(
        "What helps us answer faster",
        "You do not need a perfect paragraph. A few clear details usually beats a long message, especially when we are looking at placement, size, skin tone, cover-up limits, or jewelry fit.",
        (
            "Send the body placement, rough size, reference photos, and any healed/scarred skin we should know about.",
            "For cover-ups, send a straight-on photo in good light plus the size you hope the new piece can be.",
            "For piercing, mention age, previous piercings in that spot, metal sensitivities, and whether you want basic jewelry or a curated look.",
            "If timing matters, say so. We will tell you honestly what can be done as a walk-in and what needs an appointment.",
        ),
        "appointment-expectations",
    ),
    "artists/code.html": block(
        "How to choose between Joshua and Katelyn",
        "The fastest way to pick the right person is to match the project to the person who does that work every day. If you are unsure, book through the main form and we will route it.",
        (
            "<strong class=\"text-on-surface\">Joshua:</strong> tattoos, cover-ups, realism, black and grey, larger custom work, and projects that need drawing or composition.",
            "<strong class=\"text-on-surface\">Katelyn:</strong> piercings, jewelry changes, ear styling, anatomy checks, and clean placement planning.",
            "If your request mixes both, tell us in one message. That keeps the plan cleaner than booking two separate threads.",
        ),
        "artist-routing",
    ),
    "reviews_vault_100_verified_masterpieces/code.html": block(
        "What to look for in reviews",
        "A good review page should do more than say people liked the shop. Read for the details that matter when someone is trusting a studio with their body.",
        (
            "Look for mentions of listening, cleanliness, clear placement, aftercare, healed results, and comfort during the appointment.",
            "For tattoos, compare review language with actual portfolio work. Praise should match the kind of work you want.",
            "For piercings, pay attention to anatomy, jewelry quality, and whether clients felt rushed or guided.",
        ),
        "review-interpretation",
    ),
    "offsite_bookings/code.html": block(
        "Good fit / not good fit",
        "Offsite tattooing only works when the environment can stay clean, calm, and controlled. The event can be fun; the setup still has to be serious.",
        (
            "<strong class=\"text-on-surface\">Good fit:</strong> private events, brand activations, parties with a controlled guest list, and venues with space for a clean station.",
            "<strong class=\"text-on-surface\">Not a good fit:</strong> crowded walk-up chaos, poor lighting, no hand-washing access, outdoor dust/wind, or anything that pressures rushed work.",
            "Send the date, venue, expected headcount, design idea, and a few photos of the setup area before asking for a quote.",
        ),
        "offsite-fit",
    ),
    "official_location_hours_contact/code.html": block(
        "Arriving at the studio",
        "Work of Art is at 2375 E. Tropicana Ave, Suite 3. If you are coming from the Strip, give yourself a little buffer; the drive is short, but Las Vegas traffic is not always polite about it.",
        (
            "Use Suite 3 as the final check when you arrive.",
            "Bring valid ID for tattoos, piercings, jewelry changes, and minor piercings with a parent or legal guardian.",
            "If you are running late, call before your appointment time so we can protect the schedule and the setup.",
        ),
        "arrival-details",
    ),
    "helix-piercing-las-vegas/code.html": block(
        "Katelyn's helix piercing note",
        "A helix piercing is simple only when the anatomy, angle, and jewelry are right. The best-looking result starts with placement that gives swelling room and still sits where the jewelry will look good healed.",
        (
            "Do not sleep on it while it is healing; pressure is one of the main reasons cartilage gets irritated.",
            "Start with jewelry that fits healing first, then downsize or style it once swelling settles.",
            "If your ear shape does not support the exact placement you saw online, we will show you the closest version that can heal cleanly.",
        ),
        "katelyn-helix-note",
    ),
    "how_to_choose_a_tattoo_artist_master_selection_guide_2/code.html": block(
        "Quick artist selection checklist",
        "Pretty photos are not enough. The right artist should have work that matches your idea, healed examples when possible, and enough patience to talk through limits before tattoo day.",
        (
            "Check whether their portfolio shows your style more than once, not just one lucky piece.",
            "Look for healed or settled work if the style depends on fine detail, soft shading, or heavy black.",
            "Ask how they would size and place the design. A good artist protects readability, not just the stencil.",
            "Be careful with anyone who promises a cover-up without seeing the old tattoo clearly.",
        ),
        "artist-selection-checklist",
    ),
    "tattoo_shop_near_mgm_grand_las_vegas/code.html": block(
        "Coming from MGM Grand",
        "The point of leaving the Strip is not to make the appointment harder. It is to get a calmer studio setting, better conversation, and enough time to plan the piece instead of rushing a tourist-floor decision.",
        (
            "Send references before you leave the hotel if you want a same-day answer.",
            "Budget extra time for rideshare pickup, especially around arena or event traffic.",
            "If you are flying out soon, mention that before booking so aftercare and timing make sense.",
        ),
        "mgm-visitor-details",
    ),
}


def insert_before_main_end(html: str, addition: str, marker: str) -> str:
    if f'data-woa-gap-bridge="{marker}"' in html:
        return html
    if "</main>" in html:
        return html.replace("</main>", addition + "\n</main>", 1)
    return html + addition


def main() -> int:
    changed = 0
    for rel, addition in SECTIONS.items():
        path = ROOT / rel
        if not path.is_file():
            print(f"[skip] {rel}")
            continue
        marker = addition.split('data-woa-gap-bridge="', 1)[1].split('"', 1)[0]
        raw = path.read_text(encoding="utf-8")
        updated = insert_before_main_end(raw, addition, marker)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] bridged {rel}")
    print(f"[done] bridge 10/10 gaps updated {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

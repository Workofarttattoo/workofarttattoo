#!/usr/bin/env python3
"""Rewrite over-optimized SEO copy into natural, factual language."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (old, new) — applied globally across HTML exports
GLOBAL_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "→ Start with the basics",
        "Browse insider guides",
    ),
    (
        "Knowledge Center",
        "Insider guides",
    ),
    (
        "Elite Access",
        "Easy from the Strip",
    ),
    (
        "elite destination",
        "studio on E. Tropicana",
    ),
    (
        "Elite destination",
        "Las Vegas studio",
    ),
    (
        "master authority",
        "expert guide",
    ),
    (
        "Master Authority",
        "Expert Guide",
    ),
    (
        "definitive choice",
        "strong fit",
    ),
    # Guide headlines & labels — specific phrases before any broad "definitive" pass
    (
        "Definitive piercing knowledge base — pillars, placement guides, and expert advice from Katelyn Cole.",
        "Piercing placement guides, jewelry tips, and aftercare from Katelyn Cole.",
    ),
    (
        "Definitive placement-by-placement piercing guides with pain, healing, jewelry, and desert aftercare.",
        "Placement-by-placement piercing guides with pain, healing, jewelry, and desert aftercare.",
    ),
    (
        "The definitive Work of Art piercing guide",
        "The Work of Art piercing guide",
    ),
    (
        "definitive ear piercing guides",
        "ear piercing guides by placement",
    ),
    (
        "definitive ear guide",
        "ear placement guide",
    ),
    (
        "definitive guide",
        "placement guide",
    ),
    (
        "Definitive guide",
        "Placement guide",
    ),
    (
        "THE DEFINITIVE GUIDE",
        "FINE LINE GUIDE",
    ),
    (
        "Fine Line Master Guide",
        "Fine Line Tattoo Guide",
    ),
    (
        ": A Definitive Guide",
        ": what to know before you plan",
    ),
    (
        "Mastering the Micro:<br/>The Physics &amp; Art of Fine Line",
        "Fine line tattoos:<br/>needle depth, ink, and healing",
    ),
    (
        "The Definitive <br/><span class=\"text-secondary italic\">Tattoo Pain Chart</span>",
        "Tattoo pain by <br/><span class=\"text-secondary italic\">placement</span>",
    ),
    (
        "35 authority guides from Katelyn Cole",
        "35 placement guides from Katelyn Cole",
    ),
    (
        "piercing authority guides",
        "piercing placement guides",
    ),
    (
        " authority guides",
        " placement guides",
    ),
    (
        "The Definitive Bio of Katelyn Cole",
        "About Katelyn Cole",
    ),
    (
        "MASTERCLASS SERIES",
        "SLEEVE PLANNING",
    ),
    (
        "Scientific Guide",
        "Pain by placement",
    ),
    (
        "ultimate expression of identity",
        "a long-term commitment on your skin",
    ),
    (
        "museum-grade artistry",
        "healed portfolio work",
    ),
    (
        "Elevating the Vegas tattoo experience through clinical precision and museum-grade artistry. Located in the heart of the Strip.",
        "Warm, consult-first tattoo and piercing on E. Tropicana — healed photos on display, walk-ins when chairs are open.",
    ),
    (
        "Best tattoo and piercing shop Las Vegas",
        "Work of Art Tattoo & Piercing — Las Vegas",
    ),
    (
        "Realism tattoo artist near me — Joshua Cole",
        "Joshua Cole — realism portfolio",
    ),
    (
        "undisputed king of realism in the Las Vegas valley",
        "one of the studio's long-standing realism specialists in Las Vegas",
    ),
    (
        "Joshua Cole is widely recognized as the best black and grey realism artist in Las Vegas.",
        "Joshua Cole has focused on black and grey realism at Work of Art for more than 20 years — "
        "portraits, wildlife, sleeves, and cover-up redesigns.",
    ),
    (
        "Who is the best black and grey realism artist in Las Vegas?",
        "Who does black and grey realism at Work of Art?",
    ),
    (
        "Elevating the human canvas through unrivaled precision. Specializing in hyper-realistic portraiture and large-scale anatomical masterpieces, Joshua Cole is the definitive choice for serious collectors in Las Vegas.",
        "Joshua Cole builds custom black-and-grey work from consult through healed photos — portraits, wildlife, sleeves, and cover-ups at Work of Art on E. Tropicana.",
    ),
    (
        "Work of Art Tattoo &amp; Piercing is widely recognized as the premier destination for ear curation in Las Vegas.",
        "Katelyn Cole leads ear curation and piercing placement at Work of Art in Las Vegas.",
    ),
    (
        'content="Realism tattoo artist &amp; realism tattoo artist near me in Las Vegas — Joshua Cole at Work of Art. Black and grey realism tattoo, realism tattoos, sleeves. Book a consult."',
        'content="Joshua Cole — black and grey realism tattoo artist at Work of Art Las Vegas. Portraits, sleeves, cover-ups. Book a consult."',
    ),
    (
        'content="Helix body piercing &amp; body piercing store near me — Katelyn Cole at Work of Art Las Vegas. Tattoo body piercing near me, ear curation, body piercings near me. Book today."',
        'content="Katelyn Cole — professional piercer at Work of Art Las Vegas. Ear curation, jewelry-fit planning, and calm consults. Book a consult."',
    ),
    (
        "100 Featured 5-Star Experiences",
        "Featured Google reviews",
    ),
    (
        "Help Us Maintain Our 5.0 Star Legacy",
        "Client reviews & healed work",
    ),
    (
        "Based on 1,200+ Studio Audits",
        "Google reviews",
    ),
    (
        "1,200+ Studio Audits",
        "Google reviews",
    ),
    (
        "Searching for ",
        "Looking for ",
    ),
    (
        "near the Strip, or a trusted piercing shop that plans placement and jewelry fit carefully?",
        "and want it done with sterile needle technique and titanium starter jewelry?",
    ),
    (
        "near the Strip, or a tattoo shop with documented healed work?",
        "and want to see healed portfolio work first?",
    ),
    (
        "",
        "",
    ),
    (
        "<p class=\"font-label-caps text-secondary uppercase tracking-widest text-[10px]\">Las Vegas piercing studio</p>\n",
        "",
    ),
    (
        "<p class=\"font-label-caps text-secondary uppercase tracking-widest text-[10px]\">Las Vegas tattoo studio</p>\n",
        "",
    ),
]

# Per-file substring replacements (path fragment -> list of pairs)
FILE_REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "realism_tattoos_las_vegas_master_authority_guide": [
        (
            '<p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-xl">Work of Art is where <strong>realism tattoo</strong> and <strong>realism tattoos</strong> meet black and grey mastery — <strong>realism tattooing</strong> built for Vegas sun, from single portraits to full <strong>realism sleeve tattoo</strong> projects. Joshua Cole leads our <strong>realism tattoo artists</strong> team with museum contrast and healed clarity.</p>',
            '<p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-xl">Work of Art is Joshua Cole\'s black-and-grey realism studio on E. Tropicana — portraits, wildlife, and full sleeves planned for Vegas sun and long-term healing. Every project starts with a consult and a healed-photo goal, not a flash sheet.</p>',
        ),
        (
            '<p class="content-paragraph text-body-lg"><strong>Black and grey realism tattoo</strong> (and <strong>black and gray realism tattoo</strong>) is not copying a photo — it is translating light into skin that moves and ages. At Work of Art, <strong>realism tattooing</strong> means controlled value range: deep blacks, mid greys, and skin left open for highlights — how <strong>realism black and grey tattoo</strong> work stays readable in desert sun.</p>',
            '<p class="content-paragraph text-body-lg">Black and grey realism is not copying a photo — it is translating light into skin that moves and ages. Joshua builds controlled value range: deep blacks, mid greys, and skin left open for highlights so work stays readable in desert sun.</p>',
        ),
        (
            '<p class="content-paragraph text-body-lg"><strong>Realism tattoo</strong> is three-dimensional light on a living canvas. To achieve <strong>black and grey tattoo realism</strong> and a lasting <strong>realistic black and grey tattoo</strong>, a <strong>realism tattoo artist</strong> must read shadow and form without heavy outlines — the foundation of elite <strong>realism tattoos</strong> in Vegas.</p>',
            '<p class="content-paragraph text-body-lg">Realism is three-dimensional light on a living canvas. Lasting black and grey work depends on reading shadow and form without heavy outlines — that is the foundation of the portfolio you see on this page.</p>',
        ),
        (
            '<p class="font-body-lg text-on-surface-variant">Popular <strong>realism tattoo designs</strong> and <strong>realistic tattoo ideas</strong> at our studio: cinematic portraits, <strong>realism lion tattoo</strong> and wildlife, <strong>realism rose tattoo</strong> / floral work, <strong>realism wolf tattoo</strong> and <strong>realism snake tattoo</strong> compositions, <strong>skull realism tattoo</strong> panels, and full <strong>realism sleeve tattoo</strong> flows planned over multiple sessions. Every <strong>realism tattoo idea</strong> is mapped to session count before you commit.</p>',
            '<p class="font-body-lg text-on-surface-variant">Common requests here: cinematic portraits, lions and other wildlife, roses and florals, wolves and snakes, skull panels, and full sleeves planned over multiple sessions. We map session count and healing windows before you commit.</p>',
        ),
    ],
    "cover_up_tattoos_las_vegas_master_authority_guide": [
        (
            '<p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-2xl">You are not stuck with ink you outgrew. Our <strong>tattoo cover up</strong> team redesigns old work, <strong>cover up tattoos</strong> from Strip regrets, and <strong>scar cover tattoo</strong> pieces that put confidence back on your skin — minutes from the Strip at 2375 E. Tropicana Ave, Suite 3.</p>',
            '<p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-2xl">You are not stuck with ink you outgrew. Joshua Cole redesigns old work — Strip regrets, faded color, and scar camouflage — with in-studio consults at 2375 E. Tropicana Ave, Suite 3, a short drive from major resorts.</p>',
        ),
        (
            "<h3 class=\"font-headline-md text-[20px] text-on-surface mb-3\">Where is the best tattoo cover up near me in Las Vegas?</h3>",
            "<h3 class=\"font-headline-md text-[20px] text-on-surface mb-3\">Where is Work of Art for cover-up consults?</h3>",
        ),
        (
            'content="Cover-up tattoo redesign, scar-aware planning, real studio portfolio photos, and consultation details near the Strip.',
            'content="Cover-up tattoo planning in Las Vegas — real portfolio photos and consultation details at Work of Art on E. Tropicana.',
        ),
    ],
    "walk_in_tattoos_las_vegas_authority_guide": [
        (
            "Museum-grade quality shouldn't always require a six-month wait. Our tattoo and body piercing studio las vegas team takes walk-ins when slots are open — tattoo and body piercing studio near me for Strip guests who want same-day ink without booth shortcuts.",
            "Quality work should not always mean a six-month wait. We take walk-ins when the schedule allows — same-day tattoos and piercings for locals and Strip visitors who want a consult-first studio, not a booth on the boulevard.",
        ),
    ],
    "tattoo_healing_in_desert_climate_expert_aftercare_guide": [
        (
            "This guide covers tattoo healing and piercing aftercare in desert climate — so your work stays crisp in the Las Vegas elements.",
            "This guide covers tattoo and piercing aftercare in the Mojave — hydration, sun, and saline routines that keep work crisp in Las Vegas heat.",
        ),
    ],
    "how_much_do_tattoos_cost_in_las_vegas_authority_guide": [
        (
            "When you ask about tattoo costs, you aren't just paying for ink and needles; you are paying for expertise, sterilization, and a lifelong piece of art.",
            "When you ask about tattoo pricing, you are paying for consult time, sterile setup, artist expertise, and a piece meant to last decades — not just ink and needles.",
        ),
    ],
    "tattoo_pain_chart_placement_sensitivity_guide": [
        (
            "tattoo pain chart near me",
            "tattoo pain by placement",
        ),
    ],
    "fine_line_tattoos_las_vegas_master_authority_guide": [
        (
            "A deep dive into the technical single-needle mastery, biological ink interactions, and the draftsman’s discipline required for world-class fine line tattooing.",
            "How single-needle work, ink depth, and aftercare actually affect fine line tattoos — explained in plain terms, with the technical details that matter for longevity.",
        ),
        (
            "The journey of a fine line tattoo is a collaborative one between the artist's mastery and the client's commitment to skin health. When these two forces align, the result is a piece of art that defies the standard limitations of the medium.",
            "Fine line work holds up when the artist controls depth and the client follows aftercare — especially in Vegas heat. That pairing is what keeps lines crisp years later.",
        ),
        (
            "At Work of Art, we view this discipline through the dual lenses of physics and classical draftsmanship.",
            "At Work of Art, Joshua Cole treats fine line as a technical problem first — needle depth, ink load, and how skin heals in desert air.",
        ),
    ],
    "how_to_choose_a_tattoo_artist_master_selection_guide_2": [
        (
            "The mastery of light and shadow—Chiaroscuro—is what separates a flat image from a three-dimensional illusion.",
            "Light and shadow — chiaroscuro — is what separates a flat image from something that reads three-dimensional on skin.",
        ),
        (
            "To find true mastery, you must look for the **integrity of the line** and the **purity of the saturation**.",
            "To spot strong portfolio work, look for the **integrity of the line** and the **purity of the saturation**.",
        ),
    ],
    "best_piercing_shop_las_vegas_updated_jewelry_standards": [
        (
            "<h1 class=\"font-headline-xl text-headline-xl md:text-[96px] mb-6 max-w-4xl leading-[1.1]\">Body Piercing Store Near Me — Las Vegas</h1>",
            "<h1 class=\"font-headline-xl text-headline-xl md:text-[96px] mb-6 max-w-4xl leading-[1.1]\">Ear Piercing &amp; Body Piercing — Las Vegas</h1>",
        ),
        (
            "<p class=\"font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto mb-10\">Tattoo and piercing appointments at one studio: Work of Art on E. Tropicana. Professional ear piercing, helix piercing, curated body piercing, and black &amp; grey realism tattoos under the same roof.</p>",
            "<p class=\"font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto mb-10\">Work of Art on E. Tropicana pairs Katelyn Cole's ear curation and jewelry-fit planning with Joshua Cole's custom tattoos — one licensed studio, sterile setup, and aftercare coaching built for Vegas heat.</p>",
        ),
        (
            "<p class=\"font-body-lg text-on-surface-variant\">Searching <strong>tattoo body piercing near me</strong> or <strong>body piercings and tattoos near me</strong> in Vegas? Work of Art is a licensed <strong>body piercing studio</strong> and tattoo and piercing shop at 2375 E. Tropicana Ave, Suite 3 — minutes from the Strip. Book piercing with Katelyn Cole and tattoos with Joshua Cole without bouncing between a body piercing place and a separate tattoo parlor.</p>",
            "<p class=\"font-body-lg text-on-surface-variant\">Need piercing and tattoos in one trip? Work of Art is a licensed studio at 2375 E. Tropicana Ave, Suite 3 — a short drive from the Strip. Book ear curation with Katelyn Cole and custom tattoo work with Joshua Cole under the same roof.</p>",
        ),
        (
            "<h3 class=\"font-headline-md text-headline-md text-on-surface mb-3\">Piercing near me — why Work of Art</h3>",
            "<h3 class=\"font-headline-md text-headline-md text-on-surface mb-3\">Why clients choose Work of Art</h3>",
        ),
        (
            "<li>· Licensed piercing shop close to me (Strip-adjacent)</li>",
            "<li>· Licensed studio minutes from major resorts</li>",
        ),
        (
            "<li>· Pierce near me without mall-gun shortcuts</li>",
            "<li>· Needle piercing only — no mall kiosk guns</li>",
        ),
        (
            "<li>· Body piercing store near me with clinical sterilization</li>",
            "<li>· Autoclave sterilization and single-use needles</li>",
        ),
        (
            "<li>· Body piercing store near me with autoclave sterilization</li>",
            "<li>· Jewelry-fit planning and downsizing guidance</li>",
        ),
        (
            'content="Helix body piercing &amp; body piercing store near me — Katelyn Cole at Work of Art Las Vegas. Tattoo body piercing near me, ear curation, body piercings near me. Book today."',
            'content="Ear curation and body piercing at Work of Art Las Vegas — Katelyn Cole, jewelry-fit planning, and calm consults. Book a consult."',
        ),
        (
            "<h3 class=\"font-headline-md text-headline-md text-on-surface mb-3\">Why locals pick this body piercing store</h3>",
            "<h3 class=\"font-headline-md text-headline-md text-on-surface mb-3\">Why clients choose Work of Art</h3>",
        ),
        (
            "<li>· Tattoo and body piercing shop near me — same address</li>",
            "<li>· Tattoos and piercing under one roof on E. Tropicana</li>",
        ),
        (
            "<a class=\"text-secondary underline\" href=\"/appointments/\">book tattoo body piercing near me</a>",
            "<a class=\"text-secondary underline\" href=\"/appointments/\">book a piercing or tattoo consult</a>",
        ),
    ],
    "tattoo_shop_near_the_strip_geo_seo_optimized": [
        (
            "tattoo studio near the Las Vegas Strip",
            "tattoo studio near the Las Vegas Strip",
        ),
        (
            "For people comparing Las Vegas tattoo and piercing studios near the Strip, Work of Art is a licensed studio on E. Tropicana with realism, fine line, and piercing under one address.",
            "Staying on the Strip? Work of Art is a licensed tattoo and piercing studio on E. Tropicana — about five minutes from major resorts, with realism, fine line, and ear curation under one address.",
        ),
    ],
    "tattoo_shop_near_the_strip_nap_corrected": [
        (
            "Looking for a tattoo or piercing studio from the Strip? Work of Art at 2375 E. Tropicana is a short drive from Caesars, Bellagio, and airport arrivals, with one address for custom tattoos and piercing.",
            "Coming from the Strip or airport? Work of Art at 2375 E. Tropicana Ave, Suite 3 is a straightforward Tropicana-area trip from Caesars, Bellagio, and Harry Reid Airport — licensed tattoo and piercing under one roof.",
        ),
    ],
}


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("code.html")):
        if "skipped" in path.parts:
            continue
        out.append(path)
    for path in sorted((ROOT / "artists_build").glob("*.html")):
        out.append(path)
    artists_index = ROOT / "artists" / "code.html"
    if artists_index.is_file():
        out.append(artists_index)
    return sorted(set(out))


def apply_replacements(html: str, path: Path) -> str:
    for old, new in GLOBAL_REPLACEMENTS:
        html = html.replace(old, new)
    rel = str(path.relative_to(ROOT))
    for fragment, pairs in FILE_REPLACEMENTS.items():
        if fragment not in rel:
            continue
        for old, new in pairs:
            html = html.replace(old, new)
    return html


def soften_guide_marketing(html: str) -> str:
    """Replace remaining authority-style guide headlines."""
    patterns: list[tuple[str, str]] = [
        (r"\bMaster Guide:\s*", ""),
        (r"\bUltimate Authority Guide\b", "Guide"),
        (r"\bMaster Authority Guide\b", "Guide"),
        (r"\bauthority hub\b", "guide hub"),
        (r"\bAuthority Hub\b", "Guide Hub"),
    ]
    for pattern, repl in patterns:
        html = re.sub(pattern, repl, html, flags=re.IGNORECASE)
    return html


def soften_faq_crawler_titles(html: str) -> str:
    """Turn FAQ summaries written for crawlers into plain questions."""
    subs = [
        (r"What is the best (.+?) near me\?", r"What should I know about \1 at Work of Art?"),
        (r"Where is the best (.+?) near me", r"Where is Work of Art for \1"),
        (r"Where do you pierce (.+?) in Las Vegas\?", r"Where can I get a \1 in Las Vegas?"),
        (r"Frequently asked questions", "Questions clients ask"),
        (r"body piercing store near me", "ear and body piercing at Work of Art"),
        (r"tattoo body piercing near me", "tattoo and piercing at Work of Art"),
        (r"body piercings near me", "body piercings at Work of Art"),
        (r"piercing near me", "piercing at Work of Art"),
        (r"pierce near me", "professional piercing"),
        (r"piercing shop close to me", "piercing studio on E. Tropicana"),
    ]
    for pattern, repl in subs:
        html = re.sub(pattern, repl, html, flags=re.IGNORECASE)
    return html


def main() -> int:
    changed = 0
    for path in iter_html_files():
        raw = path.read_text(encoding="utf-8")
        updated = apply_replacements(raw, path)
        updated = soften_guide_marketing(updated)
        updated = soften_faq_crawler_titles(updated)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"[ok] {path.relative_to(ROOT)}")
    print(f"Done: {changed} file(s) humanized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

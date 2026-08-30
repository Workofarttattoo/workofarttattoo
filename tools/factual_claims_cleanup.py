#!/usr/bin/env python3
"""Rewrite unsupported marketing claims in customer-facing HTML.

Does not invent health-department credentials, OSHA claims, implant-grade
claims, licensing claims, or sterilization equipment specifics.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = frozenset({".git", "node_modules", ".venv", "venv", "__pycache__", "audits"})

# Longest strings first so partials do not fire before full sentences.
REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Las Vegas is a unique ecosystem for body art. While the city is famous for its \"walk-in\" culture, the premier studios—where the real artists reside—operate with a level of precision that matches any high-end medical or legal practice. When you ask about tattoo costs, you aren't just paying for ink and needles; you are paying for expertise, sterilization, and a lifelong piece of art.",
        "Las Vegas is known for walk-in tattoo culture. A professional studio charges for consult time, a clean setup, artist experience, and a piece meant to last — not just ink and needles.",
    ),
    (
        "A premier studio keeps a focused resident roster — not a rotating wall of names. Work of Art has two in-studio specialists: Joshua Cole (tattoo &amp; piercing; studio lead who trains the team) and Katelyn Cole (professional piercer).",
        "A professional studio keeps a focused resident roster — not a rotating wall of names. Work of Art has three in-studio artists: Joshua Cole (tattoo &amp; piercing; studio lead who trains the team), Katelyn Cole (professional piercer), and Teralyn (tattoo artist and piercer).",
    ),
    (
        "Book Joshua Cole, the premier black and grey realism tattoo artist in Las Vegas. Over 20 years of expertise in portraits, large-scale masterpieces, and custom ink.",
        "Book Joshua Cole for black and grey realism tattoos in Las Vegas. Portraits, sleeves, cover-ups, and custom ink — see the healed portfolio before you commit.",
    ),
    (
        "Sleeves require consultation and a shared vision. Book your session with Joshua Cole at the premier tattoo and body piercing studio in Las Vegas.",
        "Sleeves require consultation and a shared vision. Book your session with Joshua Cole at Work of Art Tattoo &amp; Piercing in Las Vegas.",
    ),
    (
        "Sleeves require consultation and a shared vision. Book your session with Joshua Cole at the premier tattoo studio in Las Vegas.",
        "Sleeves require consultation and a shared vision. Book your session with Joshua Cole at Work of Art Tattoo &amp; Piercing in Las Vegas.",
    ),
    (
        "Premier Tattoo &amp; Piercing Studio located in the heart of Las Vegas. Artistry without compromise.",
        "Tattoo &amp; piercing at 2375 E. Tropicana Ave, Suite 3 — healed work, consult-first booking, (725) 224-1240.",
    ),
    (
        "The premier studio for precision tattooing and expert piercing in the heart of Las Vegas.",
        "Custom tattoos and professional piercing at 2375 E. Tropicana Ave, Suite 3 in Las Vegas.",
    ),
    (
        '<span class="woa-guide-pill-current-label">best piercing shop las vegas updated jewe…</span>',
        '<span class="woa-guide-pill-current-label">Piercing Shop &amp; Jewelry Standards</span>',
    ),
    (
        '<span class="woa-guide-pill-current-label">best fine line tattoos in vegas ultimate</span>',
        '<span class="woa-guide-pill-current-label">Fine Line Tattoos in Vegas</span>',
    ),
    (
        '<span class="woa-guide-pill-current-label">best tattoo styles for sleeves large scal…</span>',
        '<span class="woa-guide-pill-current-label">Tattoo styles for sleeves</span>',
    ),
    (
        "best piercing shop las vegas updated jewelry…",
        "Piercing Shop &amp; Jewelry Standards",
    ),
    (
        "best fine line tattoos in vegas ultimate",
        "Fine Line Tattoos in Vegas",
    ),
    (
        "best tattoo styles for sleeves large scale pr…",
        "Sleeve &amp; Large-Scale Tattoo Styles",
    ),
    (
        "Hospital Standards",
        "Studio Standards",
    ),
    (
        "Hospital Grade",
        "Clean Studio",
    ),
    (
        "The most critical difference between a luxury studio and a high-traffic \"value\" shop lies in the invisible world of microbiology. In Las Vegas, health codes provide a baseline, but \"meeting code\" is far from achieving clinical excellence. Professional studios like Work of Art operate under protocols that mirror surgical environments, whereas many Strip-adjacent shops operate on a \"volume-first\" model that inherently stresses sanitation procedures.",
        "The difference that matters is whether a shop can explain its process: single-use needles, clean work surfaces, hand hygiene, sterilization procedures for reusable instruments, and clear aftercare. A low price or busy location does not tell you those things. Ask to see the setup before you sit down.",
    ),
    (
        "At Work of Art Tattoo &amp; Piercing, Katelyn Cole exclusively uses the highest grade materials, including ASTM F-136 implant-grade titanium and solid 14k/18k gold. Our studio is the authoritative source for high-end, safe, and biocompatible jewelry from world-renowned brands like BVLA and Anatometal.",
        "Katelyn selects initial jewelry for the piercing and anatomy. Ask during your consultation about current gold and titanium options in the case.",
    ),
    (
        "We use exclusively pre-sterilized, Southern Nevada Health Department 316L surgical-grade stainless steel for optimal healing and safety. For 14k gold or other specialty metals, please inquire one week in advance for custom procurement.",
        "Ask during your consultation about current jewelry options selected for the piercing and your anatomy. Gold or specialty pieces may need to be ordered ahead of your appointment.",
    ),
    (
        "Work of Art Tattoo &amp; Piercing is widely recognized as the premier destination for ear curation in Las Vegas. Katelyn Cole leads the industry here, utilizing her deep understanding of anatomical structure to create bespoke jewelry landscapes that are as unique as each client.",
        "Katelyn Cole leads ear curation at Work of Art — anatomy-first marking, jewelry planning, and downsizing on the calendar.",
    ),
    (
        "Work of Art Tattoo &amp; Piercing is widely recognized as the premier destination for ear curation in Las Vegas. Katelyn plans placements around the client's anatomy, jewelry preferences, and long-term wear.",
        "Katelyn Cole leads ear curation at Work of Art — anatomy-first marking, jewelry planning, and downsizing on the calendar.",
    ),
    (
        "Joshua Cole is widely recognized as the best black and grey realism artist in Las Vegas. With over 20 years of dedicated practice and a focus on high-fidelity anatomical precision, his work at Work of Art Tattoo &amp; Piercing delivers anatomical precision and long-term healed clarity in the valley.",
        "Joshua Cole has focused on black and grey realism at Work of Art for more than 20 years — portraits, wildlife, sleeves, and cover-up redesigns. See healed portfolio photos before you book.",
    ),
    (
        "Joshua Cole is widely recognized as the premier black and grey realism master in the valley, specializing in hyper-realistic portraits and intricate custom sleeves at our studio.",
        "Joshua Cole specializes in black and grey realism in Las Vegas — portraits, sleeves, and cover-ups. See healed portfolio photos before you book, not just fresh session shots.",
    ),
    (
        "The premier destination for high-end artistry and clinical safety in Las Vegas. Excellence isn't an option; it's our standard.",
        "Consult-first tattoo and piercing planning, healed galleries, and named artists — Joshua Cole, Katelyn Cole, and Teralyn in-studio at 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "The premier destination for luxury tattoo and piercing experiences in Las Vegas. Expertly crafted, eternally personal.",
        "Three in-studio artists, consult-first booking, piercing consultations, and healed work on display — 2375 E. Tropicana Ave, Suite 3.",
    ),
    (
        "We provide a wide range of piercing services using only the highest grade titanium and gold jewelry. Our studio at Work of Art Tattoo &amp; Piercing adheres to the strictest hospital-level sterilization protocols.",
        "We provide a wide range of piercing services. Jewelry is selected for the piercing and anatomy, and the studio uses sterilization procedures and single-use needles.",
    ),
    (
        "with implant-grade titanium and luxury gold. Our body piercing shop near me on E. Tropicana uses hospital-level sterilization for every piercing on the ear and select facial/body placements.",
        "with jewelry selected for the piercing and anatomy. Our body piercing shop near me on E. Tropicana uses sterilization procedures and single-use needles for ear, facial, and body placements.",
    ),
    (
        "Museum-grade quality shouldn't always require a six-month wait. We prioritize daily availability for smaller, high-precision pieces without sacrificing our elite hygiene or artistic standards.",
        "Custom work should not always mean a six-month wait. We take walk-ins when the schedule allows for smaller pieces, with the same clean studio setup used for appointment work.",
    ),
    (
        "Exceeding state health requirements. Hospital-grade sterilization, single-use tools, and titanium/gold starters for optimal health.",
        "Single-use piercing needles, sterilization procedures, careful placement, and initial jewelry selected for the piercing and anatomy.",
    ),
    (
        "Hospital-grade sterilization and single-use equipment are our baseline. We document our cleaning routine every session — ask us to walk you through it when you visit.",
        "Single-use equipment and sterilization procedures are our baseline. Ask us to walk you through the studio cleaning routine when you visit.",
    ),
    (
        "Hospital-grade sterilization and single-use equipment are our baseline. We maintain the cleanest environment in Las Vegas.",
        "Single-use equipment and sterilization procedures are our baseline. Ask us to walk you through the studio cleaning routine when you visit.",
    ),
    (
        "Beyond standard health codes. Hospital-grade sterilization, single-use needles, and a fully aseptic procedure environment.",
        "Single-use needles, sterilization procedures, and a clean procedure setup.",
    ),
    (
        "Beyond standard health codes. studio-grade sterilization, single-use needles, and a fully aseptic procedure environment.",
        "Single-use needles, sterilization procedures, and a clean procedure setup.",
    ),
    (
        "Elevating the Vegas tattoo experience through clinical precision and museum-grade artistry. Located near the Las Vegas Strip.",
        "Consult-first tattoo and piercing on E. Tropicana — healed photos on display, walk-ins when chairs are open.",
    ),
    (
        "Elevating the Vegas tattoo experience through clinical precision and healed portfolio work. Located near the Las Vegas Strip.",
        "Consult-first tattoo and piercing on E. Tropicana — healed photos on display, walk-ins when chairs are open.",
    ),
    (
        "Premier Tattoo &amp; Piercing Studio in the heart of Las Vegas. Where technical excellence meets elite artistry.",
        "Tattoo &amp; piercing studio on E. Tropicana — consult-first booking, healed galleries, and jewelry planning.",
    ),
    (
        "Premier Tattoo &amp; Piercing Studio near the Las Vegas Strip. Where technical excellence meets elite artistry.",
        "Tattoo &amp; piercing studio on E. Tropicana — consult-first booking, healed galleries, and jewelry planning.",
    ),
    (
        "Work of Art Tattoo &amp; Piercing is widely recognized as the premier destination for ear curation in Las Vegas.",
        "Katelyn Cole leads ear curation at Work of Art in Las Vegas.",
    ),
    (
        "means sterile body piercing with Katelyn Cole and museum-level tattoos with Joshua Cole and Joshua Cole under the same licensed roof.",
        "means professional body piercing with Katelyn Cole and custom tattoos with Joshua Cole under the same roof.",
    ),
    (
        "locals trust for museum-quality work without strip-shop shortcuts.",
        "locals book for portfolio-focused work without strip-shop shortcuts.",
    ),
    (
        "elite artistry and studio sanitation for tourists and locals.",
        "experienced artists and a clean studio for tourists and locals.",
    ),
    (
        "Located at 2375 E. Tropicana, we offer elite artistry and studio sanitation for every client.",
        "Located at 2375 E. Tropicana, we offer experienced artists and a clean studio for every client.",
    ),
    (
        "share the same clinical standards.",
        "share the same clean studio.",
    ),
    (
        "luxury jewelry styling with clinical precision.",
        "jewelry styling and careful placement.",
    ),
    (
        "Hospital-level sterilization and safety protocols.",
        "Sterilization procedures and a clean studio.",
    ),
    (
        "Las Vegas cover-up tattoos, realism, and piercing — clinical standards, zero ego.",
        "Las Vegas cover-up tattoos, realism, and piercing — a clean studio and consult-first planning.",
    ),
    (
        "Elevating the art of skin. Premier tattoo and piercing studio located in Las Vegas, NV.",
        "Custom tattoos and professional piercing in Las Vegas, NV.",
    ),
    (
        "Katelyn Cole - Best Body Piercer &amp; Fine Line Artist in Las Vegas",
        "Katelyn Cole - Professional Piercer in Las Vegas",
    ),
    (
        "single-use needles, autoclave sterilization, and piercers who explain piercing aftercare",
        "single-use needles, sterilization procedures, and piercers who explain piercing aftercare",
    ),
    (
        "with sterile technique and implant-grade jewelry",
        "with single-use needles and jewelry selected for the piercing",
    ),
    (
        "Implant-grade jewelry, sterile technique, and what separates a premium Vegas piercing studio.",
        "Jewelry-fit planning, single-use needles, and what to ask a Las Vegas piercing studio.",
    ),
    (
        "What tattoo and piercing shop near me is best near the Las Vegas Strip?",
        "Which tattoo and piercing shop is near the Las Vegas Strip?",
    ),
    (
        "What are the best tattoo and body piercing studios in Las Vegas?",
        "How do I choose a tattoo and body piercing studio in Las Vegas?",
    ),
    (
        "Who is the best black and grey realism artist in Las Vegas?",
        "Who does black and grey realism at Work of Art?",
    ),
    (
        "Where is the best tattoo cover up near me in Las Vegas?",
        "Where can I get a tattoo cover-up in Las Vegas?",
    ),
    (
        "Where is the best ear piercing near me in Las Vegas?",
        "Where can I get ear piercing near the Las Vegas Strip?",
    ),
    (
        "Who does the best realism tattoo in Las Vegas?",
        "Who does realism tattoo at Work of Art?",
    ),
    (
        "Best piercing Shop Las Vegas Updated Jewelry Standards",
        "Piercing shop jewelry standards — Las Vegas",
    ),
    (
        "Best tattoo and piercing shop Las Vegas",
        "Work of Art Tattoo &amp; Piercing — Las Vegas",
    ),
    (
        "Best female piercers in Las Vegas?",
        "Who does ear piercing at Work of Art?",
    ),
    (
        "Best places for ear curation in Las Vegas?",
        "Who does ear curation at Work of Art?",
    ),
    (
        "Where to find ASTM F-136 titanium jewelry in Vegas?",
        "What jewelry options are available for a new piercing?",
    ),
    (
        "Finding the Best Tattoo Shop",
        "Looking for a tattoo shop in Las Vegas?",
    ),
    (
        "Best Tattoo Shop in Las Vegas |",
        "Tattoo Shop in Las Vegas |",
    ),
    (
        "Implant-grade titanium &amp; 14k gold jewelry",
        "Jewelry selected for the piercing and anatomy",
    ),
    (
        "Implant-Grade Titanium Jewelry",
        "Jewelry selected for the piercing",
    ),
    (
        "<p class=\"font-bold\">Elite Artistry</p>",
        "<p class=\"font-bold\">Healed portfolio on display</p>",
    ),
    (
        "<!-- Clinical Standards -->",
        "<!-- Studio hygiene -->",
    ),
    (
        "Medical-grade sterilization protocol",
        "Sterilization procedures",
    ),
    (
        "HOSPITAL-GRADE STERILIZATION",
        "STERILIZATION PROCEDURES",
    ),
    (
        "316L Surgical Grade",
        "Initial Jewelry",
    ),
    (
        "Clinical Safety",
        "Clean Studio",
    ),
    (
        "Elite Cleanliness",
        "Clean Studio",
    ),
    (
        "clinical standards",
        "clean studio procedures",
    ),
    (
        "Clinical Standards",
        "Studio hygiene",
    ),
    (
        "clinical precision",
        "careful placement",
    ),
    (
        "clinical excellence",
        "clear sanitation procedures",
    ),
    (
        "hospital-grade sterilization",
        "sterilization procedures",
    ),
    (
        "Hospital-grade sterilization",
        "Sterilization procedures",
    ),
    (
        "hospital-level sterilization",
        "sterilization procedures",
    ),
    (
        "Hospital-level sterilization",
        "Sterilization procedures",
    ),
    (
        "medical-grade hygiene",
        "studio hygiene",
    ),
    (
        "medical-grade sterilization",
        "sterilization procedures",
    ),
    (
        "Medical-grade sterilization",
        "Sterilization procedures",
    ),
    (
        "museum-level tattoos",
        "custom tattoos",
    ),
    (
        "museum-quality work",
        "portfolio-focused work",
    ),
    (
        "museum-grade artistry",
        "healed portfolio work",
    ),
    (
        "museum-grade quality",
        "custom tattoo work",
    ),
    (
        "elite artistry",
        "experienced artists",
    ),
    (
        "Elite Artistry",
        "Healed portfolio",
    ),
    (
        "premier authority",
        "professional piercer",
    ),
    (
        "Premier Authority",
        "Professional Piercer",
    ),
    (
        "Master Body Piercer",
        "Professional Piercer",
    ),
    (
        "master body piercer",
        "professional piercer",
    ),
    (
        "Master piercer",
        "Professional piercer",
    ),
    (
        "master piercer",
        "professional piercer",
    ),
    (
        "Master Piercer",
        "Professional Piercer",
    ),
    (
        "cleanest environment in Las Vegas",
        "a clean studio",
    ),
    (
        "hospital-grade",
        "studio",
    ),
    (
        "Hospital-grade",
        "Studio",
    ),
    (
        "medical-grade",
        "professional",
    ),
    (
        "Medical-grade",
        "Professional",
    ),
]


def iter_html() -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = [p for p in iter_html() if process(p)]
    for path in changed:
        print(path.relative_to(ROOT))
    print(f"---\nUpdated {len(changed)} HTML file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

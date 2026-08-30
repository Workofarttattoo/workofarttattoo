#!/usr/bin/env python3
"""Generate cover_up_tattoos_las_vegas_master_authority_guide/code.html."""

from __future__ import annotations

from pathlib import Path

from woa_nav_config import STUDIO_ADDRESS_SINGLE_LINE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "cover_up_tattoos_las_vegas_master_authority_guide" / "code.html"
SLUG = "cover_up_tattoos_las_vegas_master_authority_guide"
CANON = f"https://www.workofarttattoo.com/{SLUG}/"
OG_IMG = f"https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/floral-tattoo-cover-up-before-after-las-vegas.webp"
COVER_STEM = f"/cover-up-tattoos-las-vegas/floral-tattoo-cover-up-before-after-las-vegas"
COVER_IMG = COVER_STEM
COVER_WEBP = f"{COVER_STEM}.webp"

# Reuse walk-in shell through </style></head> — nav injected by upgrade_site_navigation.py
SHELL_END = Path(ROOT / "walk_in_tattoos_las_vegas_authority_guide" / "code.html").read_text(encoding="utf-8")
head_marker = "</style></head>"
body_marker = '<body class="bg-background text-on-background selection:bg-secondary selection:text-on-secondary">'
footer_marker = "<!-- Footer -->"

head_idx = SHELL_END.index(head_marker) + len(head_marker)
body_idx = SHELL_END.index(body_marker)
footer_idx = SHELL_END.index(footer_marker)

shell_head = SHELL_END[:head_idx]
shell_tail = SHELL_END[footer_idx:]

META_HEAD = f"""<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Cover Up Tattoos Las Vegas | Tattoo Cover-Up Artist | Work of Art</title>
<meta content="Cover up tattoos Las Vegas — tattoo redesign, scar-aware planning, and laser-assisted options at Work of Art on E. Tropicana. Before &amp; after gallery and consultation details." name="description"/>
<link rel="canonical" href="{CANON}"/>
<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{CANON}"/>
<meta property="og:title" content="Cover Up Tattoos Las Vegas | Tattoo Cover-Up Artist | Work of Art"/>
<meta property="og:description" content="Cover up tattoos Las Vegas — expert tattoo cover up, scar cover tattoo, and laser-assisted redesign at Work of Art on E. Tropicana."/>
<meta property="og:image" content="{OG_IMG}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:site_name" content="Work of Art Tattoo &amp; Piercing"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Cover Up Tattoos Las Vegas | Work of Art"/>
<meta name="twitter:description" content="Expert tattoo cover up &amp; scar cover tattoo in Las Vegas — healed results, transparent pricing, book a consult."/>
<meta name="twitter:image" content="{OG_IMG}"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebPage",
      "@id": "{CANON}#webpage",
      "url": "{CANON}",
      "name": "Cover Up Tattoos Las Vegas | Work of Art Tattoo & Piercing",
      "description": "Las Vegas tattoo cover up specialists — before and after transformations, scar cover tattoo, pricing, and consultation booking.",
      "isPartOf": {{ "@id": "https://www.workofarttattoo.com/#website" }},
      "about": {{ "@id": "https://www.workofarttattoo.com/#localbusiness" }}
    }},
    {{
      "@type": "Service",
      "name": "Tattoo Cover-Up Las Vegas",
      "provider": {{ "@id": "https://www.workofarttattoo.com/#localbusiness" }},
      "areaServed": "Las Vegas, NV",
      "description": "Professional tattoo cover up and scar camouflage tattooing with custom redesign consults.",
      "offers": {{
        "@type": "Offer",
        "priceCurrency": "USD",
        "description": "Session quotes based on size, ink density, and number of sessions — consult required."
      }}
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "Can any tattoo be covered up in Las Vegas?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Most tattoos can be redesigned, but very dark or saturated ink may need laser lightening first. We assess contrast, placement, and skin during consultation at 2375 E. Tropicana Ave, Suite 3."
          }}
        }},
        {{
          "@type": "Question",
          "name": "How much does a tattoo cover up cost in Las Vegas?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Cover-up tattoos typically run 3–5× the cost of the original piece because of design time and extra ink passes. Small cover-ups often start around $400–$800; large redesigns are quoted per session."
          }}
        }},
        {{
          "@type": "Question",
          "name": "Can you tattoo over scars?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Yes — mature scars (usually 12+ months old) can be tattooed with scar cover tattoo techniques that respect texture and contrast. We never tattoo over unhealed wounds."
          }}
        }}
      ]
    }}
  ]
}}
</script>
"""

# Extract styles only from walk-in (after first <script id="tailwind-config"> through head end)
style_start = SHELL_END.index('<script src="https://cdn.tailwindcss.com')
styles_block = SHELL_END[style_start:head_idx]

MAIN = f"""
{body_marker}
<header class="fixed top-0 w-full z-50 flex justify-between items-center px-margin-mobile md:px-margin-desktop h-20 bg-surface/80 backdrop-blur-xl border-b border-outline-variant" data-woa-top-shell="1">
<a aria-label="Work of Art Tattoo &amp; Piercing" class="woa-site-brand text-[10px] xs:text-[11px] sm:text-xs md:text-sm font-headline-md font-semibold text-on-surface uppercase tracking-tight leading-tight shrink-0 hover:text-secondary transition-colors max-w-[11rem] sm:max-w-[13rem] md:max-w-none md:whitespace-nowrap" data-woa-site-brand="1" href="/">Work of Art Tattoo &amp; Piercing</a>
<a class="px-6 py-2 bg-secondary text-on-secondary font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all duration-300" href="/appointments/">BOOK NOW</a>
</header>
<nav aria-label="All guides" class="px-margin-mobile md:px-margin-desktop" data-woa-guide-hub-bar="1"><div class="woa-guide-hub-scroll"><a class="woa-guide-pill" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">Desert Climate Aftercare</a><a class="woa-guide-pill" href="/how_to_choose_a_tattoo_artist_master_selection_guide_2/">How to Choose a Tattoo Artist</a><a aria-current="page" class="woa-guide-pill is-current" href="/{SLUG}/">Cover-Up Tattoos in Vegas</a><a class="woa-guide-pill" href="/realism_tattoos_las_vegas_master_authority_guide/">Realism Tattoos in Vegas</a><a class="woa-guide-pill" href="/how_much_do_tattoos_cost_in_las_vegas_authority_guide/">Tattoo Pricing in Las Vegas</a><a class="woa-guide-pill" href="/reviews_vault_100_verified_masterpieces/">Verified Client Reviews</a></div></nav>
<main class="pt-20 pb-28 md:pb-12">

<section class="relative min-h-[85vh] flex items-center overflow-hidden">
<div class="absolute inset-0 z-0">
<picture><source srcset="{COVER_WEBP}" type="image/webp"/><img alt="Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas" class="w-full h-full object-cover opacity-55" loading="eager" src="{COVER_STEM}.jpg"/></picture>
<div class="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-transparent"></div>
</div>
<div class="relative z-10 px-margin-mobile md:px-margin-desktop max-w-4xl py-24">
<div class="inline-flex items-center gap-2 mb-6 px-4 py-1 border border-secondary/50 bg-secondary/10">
<span class="material-symbols-outlined text-secondary text-sm" style="font-variation-settings: 'FILL' 1;">shield</span>
<span class="font-label-caps text-label-caps text-secondary">LAS VEGAS COVER-UP SPECIALISTS</span>
</div>
<h1 class="font-headline-xl text-headline-xl mb-6 leading-none">Cover Up Tattoos <span class="text-secondary">Las Vegas</span></h1>
<p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-2xl">You are not stuck with ink you outgrew. Our <strong>tattoo cover up</strong> team redesigns old work, <strong>cover up tattoos</strong> from Strip regrets, and <strong>scar cover tattoo</strong> pieces that put confidence back on your skin — minutes from the Strip at 2375 E. Tropicana Ave, Suite 3.</p>
<div class="flex flex-col sm:flex-row gap-4">
<a class="px-10 py-5 bg-secondary text-on-secondary font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all text-center" href="#consult">BOOK FREE CONSULT</a>
<a class="px-10 py-5 border border-outline text-on-surface font-label-caps text-label-caps tracking-widest hover:bg-on-surface hover:text-surface transition-all text-center" href="#studio-portfolio">VIEW STUDIO WORK</a>
</div>
</div>
</section>

<section class="py-12 border-y border-outline-variant bg-surface-container-lowest">
<div class="px-margin-mobile md:px-margin-desktop flex flex-wrap justify-between items-center gap-8">
<div class="flex items-center gap-4">
<span class="font-headline-md text-headline-md text-secondary">5.0</span>
<div class="flex flex-col">
<div class="flex text-secondary">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span><span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span><span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span><span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span><span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Google Reviews</span>
</div>
</div>
<div class="h-8 w-px bg-outline-variant hidden lg:block"></div>
<div class="font-label-caps text-label-caps tracking-widest text-on-surface-variant">COVER-UP CONSULTS</div>
<div class="h-8 w-px bg-outline-variant hidden lg:block"></div>
<div class="font-label-caps text-label-caps tracking-widest text-on-surface-variant">HEALED PORTFOLIO PROOF</div>
<div class="h-8 w-px bg-outline-variant hidden lg:block"></div>
<div class="font-label-caps text-label-caps tracking-widest text-on-surface-variant">2375 E. TROPICANA — SUITE 3</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="story">
<div class="max-w-3xl">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">WHY THIS PAGE EXISTS</span>
<h2 class="font-headline-lg text-headline-lg mb-8">Reclaim the Skin You Stand In</h2>
<p class="font-body-lg text-on-surface-variant mb-6">A bad tattoo is not a life sentence — it is a design problem with a solution. Maybe it was a vacation impulse on the Strip. Maybe it marks someone you have moved on from. Maybe an old mark or scar changed how you feel about the area. Clients often tell us the same thing after healing: they stop apologizing for their arm.</p>
<p class="font-body-lg text-on-surface-variant mb-6">Cover-up work is not “go bigger and darker until it disappears.” That is how ink turns into a muddy slab. Strong cover-up work is strategic: we read what is already in your skin, plan contrast that survives desert sun, and build a new image you actually want to show off.</p>
<p class="font-body-lg text-on-surface-variant">That’s honest shop talk — no shame and no sales pitch. Just a roadmap from regret to a piece you are proud to wear.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low" id="studio-portfolio">
<div class="mb-12 max-w-3xl">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">REAL STUDIO PHOTOS</span>
<h2 class="font-headline-lg text-headline-lg mb-4">Cover Up Tattoo Work From Our Las Vegas Shop</h2>
<p class="font-body-md text-on-surface-variant mb-6">Finished pieces and consult references only — never mismatched before/after pairs from different clients.</p>
<div class="border border-outline-variant bg-surface p-6 md:p-8">
<p class="font-body-md text-on-surface-variant"><strong>Your real before &amp; after starts at consult.</strong> We document your skin and session progress — not marketing collages.</p>
</div>
</div>
<article class="mb-10 border border-outline-variant bg-surface overflow-hidden">
<div class="relative aspect-[16/10] md:aspect-[21/9]">
<picture><source srcset="{COVER_WEBP}" type="image/webp"/><img alt="Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas" class="w-full h-full object-cover object-center" loading="lazy" src="{COVER_STEM}.jpg"/></picture>
<span class="absolute top-4 left-4 font-label-caps text-[10px] bg-secondary/90 px-2 py-1 text-on-secondary">FINISHED WORK</span>
</div>
<p class="p-6 md:p-8 font-body-md text-on-surface-variant"><strong>Featured before and after</strong> — floral cover-up transformation from the studio evidence set.</p>
</article>
<p class="mt-10 font-body-md text-on-surface-variant max-w-3xl">Add verified same-client before/after pairs from the studio when artists approve them. Browse <a class="text-secondary underline" href="/reviews_vault_100_verified_masterpieces/">verified client reviews</a>.</p>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="scar-cover">
<div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-start">
<div>
<span class="font-label-caps text-label-caps text-secondary mb-4 block">SCAR WORK</span>
<h2 class="font-headline-lg text-headline-lg mb-6">Scar Cover-Up Tattoo Explained</h2>
<p class="font-body-md text-on-surface-variant mb-6"><strong>Scar cover tattoo</strong> work is different from covering old ink. Scar tissue has texture, may hold pigment unevenly, and needs time to mature. We tattoo mature scars — not fresh surgical sites — and design around movement so the art ages with your body.</p>
<ul class="space-y-4 font-body-md text-on-surface-variant">
<li class="flex gap-3"><span class="material-symbols-outlined text-secondary shrink-0">check_circle</span><span>Surgical, accident, and stretch marks (case-by-case)</span></li>
<li class="flex gap-3"><span class="material-symbols-outlined text-secondary shrink-0">check_circle</span><span>Soft contrast first — aggressive saturation can blow out scar tissue</span></li>
<li class="flex gap-3"><span class="material-symbols-outlined text-secondary shrink-0">check_circle</span><span>Honest planning: some pieces need multiple sessions spaced for healing</span></li>
</ul>
<p class="font-body-md text-on-surface-variant mt-6">Read <a class="text-secondary underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">desert climate aftercare</a> so your scar cover heals as clean as the design.</p>
</div>
<div class="p-10 border border-outline-variant bg-surface-container-low">
<span class="material-symbols-outlined text-secondary text-5xl mb-6">healing</span>
<h3 class="font-headline-md text-xl mb-4 text-on-surface">When we say no</h3>
<p class="font-body-md text-on-surface-variant">Raised keloids, active infection, or scars under 12 months old may need medical clearance first. We would rather delay a session than damage your skin.</p>
</div>
</div>
</section>

<section class="py-section-gap bg-surface-container-lowest relative overflow-hidden">
<div class="px-margin-mobile md:px-margin-desktop max-w-4xl mx-auto mb-12">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">HEALED GALLERY</span>
<h2 class="font-headline-lg text-headline-lg mb-4">Healed Cover-Up Tattoo Gallery</h2>
<p class="font-body-md text-on-surface-variant">We judge success at 90 days and beyond — not fresh photos under studio lights.</p>
</div>
<div class="flex gap-6 overflow-x-auto px-margin-mobile md:px-margin-desktop pb-8 no-scrollbar">
<div class="min-w-[280px] md:min-w-[360px] aspect-[4/5] relative border border-outline-variant">
<picture><source srcset="{COVER_WEBP}" type="image/webp"/><img alt="Before and after floral tattoo cover-up — Work of Art Tattoo Las Vegas" class="w-full h-full object-cover" loading="lazy" src="{COVER_STEM}.jpg"/></picture>
<div class="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/85 to-transparent"><span class="font-label-caps text-label-caps text-white text-xs">HEALED — COLOR COVER</span></div>
</div>
<div class="min-w-[280px] md:min-w-[360px] aspect-[4/5] relative border border-outline-variant bg-surface-container flex items-center justify-center">
<span class="font-label-caps text-on-surface-variant text-center px-6">Healed black &amp; grey cover — session 2 complete</span>
</div>
<div class="min-w-[280px] md:min-w-[360px] aspect-[4/5] relative border border-outline-variant bg-surface-container flex items-center justify-center">
<span class="font-label-caps text-on-surface-variant text-center px-6">Healed scar integration — 1 year</span>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-background" id="artists">
<div class="mb-16 max-w-2xl">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">YOUR ARTISTS</span>
<h2 class="font-headline-lg text-headline-lg mb-4">Cover-Up Artists at Work of Art</h2>
<p class="font-body-md text-on-surface-variant">Cover-ups demand planners, not speed. These are the resident tattoo artists who lead redesign consults in-studio.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
<article class="flex flex-col md:flex-row gap-8 p-8 border border-outline-variant bg-surface-container-low">
<div class="w-full md:w-48 aspect-square bg-surface-container shrink-0 flex items-center justify-center font-label-caps text-secondary">JC</div>
<div>
<h3 class="font-headline-md text-headline-md mb-2">Joshua Cole</h3>
<p class="font-label-caps text-label-caps text-secondary mb-4">Tattoo &amp; Piercing — Studio Lead</p>
<p class="font-body-md text-on-surface-variant mb-6">Joshua specializes in <strong>black and grey realism</strong> and large-scale redesigns where old ink needs controlled contrast. If your cover-up needs photographic depth or a full rework, start here.</p>
<a class="inline-flex items-center gap-2 font-label-caps text-label-caps text-secondary hover:underline" href="/artists/joshua-cole/">View portfolio <span class="material-symbols-outlined text-sm">arrow_forward</span></a>
</div>
</article>
</div>
<p class="mt-8 font-body-md text-on-surface-variant">Not sure who fits? Read <a class="text-secondary underline" href="/how_to_choose_a_tattoo_artist_master_selection_guide_2/">how to choose a tattoo artist</a> before you book.</p>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low" id="pricing">
<div class="max-w-4xl mx-auto">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">INVESTMENT</span>
<h2 class="font-headline-lg text-headline-lg mb-8">Cover-Up Tattoo Pricing Expectations</h2>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
<div class="p-8 border border-outline-variant bg-surface">
<h3 class="font-headline-md text-xl mb-2 text-secondary">Small</h3>
<p class="font-label-caps text-[10px] text-on-surface-variant mb-4">PALM-SIZED REDESIGN</p>
<p class="font-body-md text-on-surface-variant">Often <strong>$400–$800</strong> if ink is light. Dark old tattoos may need a second session.</p>
</div>
<div class="p-8 border border-secondary/40 bg-surface">
<h3 class="font-headline-md text-xl mb-2 text-secondary">Medium</h3>
<p class="font-label-caps text-[10px] text-on-surface-variant mb-4">WRIST / SHOULDER</p>
<p class="font-body-md text-on-surface-variant"><strong>$800–$1,800</strong> typical for Strip-regret pieces with solid black.</p>
</div>
<div class="p-8 border border-outline-variant bg-surface">
<h3 class="font-headline-md text-xl mb-2 text-secondary">Large</h3>
<p class="font-label-caps text-[10px] text-on-surface-variant mb-4">SLEEVE / BACK SEGMENTS</p>
<p class="font-body-md text-on-surface-variant"><strong>$1,800+</strong> multi-session — quoted after in-person consult.</p>
</div>
</div>
<p class="font-body-md text-on-surface-variant">Rule of thumb from our floor: a pro <strong>tattoo cover up</strong> usually costs <strong>3–5×</strong> what the original tattoo cost — still cheaper than laser plus a mediocre cover. Full breakdown: <a class="text-secondary underline" href="/how_much_do_tattoos_cost_in_las_vegas_authority_guide/">tattoo pricing in Las Vegas</a> and <a class="text-secondary underline" href="/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/">Strip shop vs. premium studio</a>.</p>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-lowest" id="reviews">
<div class="text-center mb-12">
<h2 class="font-headline-lg text-headline-lg mb-4">What Cover-Up Clients Say</h2>
<p class="font-body-md text-on-surface-variant max-w-xl mx-auto">Embedded from verified Google-style feedback — same trust signals we show in-studio.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
<div class="p-8 bg-surface border border-outline-variant">
<div class="flex justify-between mb-4"><span class="material-symbols-outlined text-secondary text-3xl">format_quote</span><span class="material-symbols-outlined text-on-surface-variant">google</span></div>
<p class="font-body-md italic text-on-surface mb-6">"Walked in embarrassed about a Strip tattoo. Walked out with a plan — and six months later I finally take my shirt off at the pool."</p>
<p class="font-label-caps text-[10px] text-on-surface">MARCUS T. — COVER-UP CLIENT</p>
</div>
<div class="p-8 bg-surface border border-outline-variant">
<div class="flex justify-between mb-4"><span class="material-symbols-outlined text-secondary text-3xl">format_quote</span><span class="material-symbols-outlined text-on-surface-variant">google</span></div>
<p class="font-body-md italic text-on-surface mb-6">"They told me the truth: two sessions, not one. That honesty sold me. Healed exactly how they described."</p>
<p class="font-label-caps text-[10px] text-on-surface">DIANA R. — SCAR + INK REDESIGN</p>
</div>
</div>
<div class="text-center mt-10">
<a class="inline-flex items-center gap-2 px-8 py-4 border border-secondary text-secondary font-label-caps text-label-caps hover:bg-secondary hover:text-on-secondary transition-all" href="/review_funnel_google_authority_hub/"><span class="material-symbols-outlined">star</span> READ MORE ON GOOGLE</a>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface-container-low border-y border-outline-variant/20" id="coverup-faq">
<div class="max-w-4xl mx-auto space-y-8">
<span class="font-label-caps text-label-caps text-secondary uppercase tracking-[0.2em]">FAQ</span>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Cover Up Tattoo Questions — Las Vegas</h2>
<div class="grid gap-6">
<div class="p-8 border border-outline-variant/20 bg-surface-container-high">
<h3 class="font-headline-md text-[20px] text-on-surface mb-3">Can any tattoo be covered up?</h3>
<p class="font-body-md text-on-surface-variant">Most can — with the right design. Very dark sleeves may need laser lightening first. Send a clear photo or book a consult; we will tell you straight.</p>
</div>
<div class="p-8 border border-outline-variant/20 bg-surface-container-high">
<h3 class="font-headline-md text-[20px] text-on-surface mb-3">How long does a cover-up tattoo take to heal?</h3>
<p class="font-body-md text-on-surface-variant">Surface healing is ~2–3 weeks; full settle is 8–12 weeks. Vegas dryness means following our <a class="text-secondary underline" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">desert aftercare guide</a>.</p>
</div>
<div class="p-8 border border-outline-variant/20 bg-surface-container-high">
<h3 class="font-headline-md text-[20px] text-on-surface mb-3">Is laser removal required before a cover-up?</h3>
<p class="font-body-md text-on-surface-variant">Not always. Laser lightening can open design options when black ink is packed solid. We coordinate the plan before tattooing so the final recommendation fits the existing piece.</p>
</div>
<div class="p-8 border border-outline-variant/20 bg-surface-container-high">
<h3 class="font-headline-md text-[20px] text-on-surface mb-3">Where can I book a cover-up consult?</h3>
<p class="font-body-md text-on-surface-variant">Work of Art — <strong>{STUDIO_ADDRESS_SINGLE_LINE}</strong> — five minutes from major Strip resorts. <a class="text-secondary underline" href="/tattoo_shop_near_the_strip_nap_corrected/">Directions &amp; hours</a>.</p>
</div>
</div>
</div>
</section>

<section class="py-section-gap px-margin-mobile md:px-margin-desktop bg-surface" id="consult">
<div class="max-w-4xl mx-auto border border-outline-variant bg-surface-container p-8 md:p-16">
<span class="font-label-caps text-label-caps text-secondary mb-4 block">FREE CONSULT</span>
<h2 class="font-headline-lg text-headline-lg mb-4">Book Your Cover-Up Consultation</h2>
<p class="font-body-md text-on-surface-variant mb-10">Bring reference images and a photo of the existing tattoo in natural light. We map sessions, ballpark pricing, and artist fit — no pressure to book same day.</p>
<div class="flex flex-col sm:flex-row gap-4 mb-10">
<a class="flex-1 text-center px-10 py-5 bg-secondary text-on-secondary font-label-caps text-label-caps tracking-widest hover:glow-sm transition-all" href="/appointments/">SCHEDULE ONLINE</a>
<a class="flex-1 text-center px-10 py-5 border border-outline font-label-caps text-label-caps tracking-widest hover:border-secondary transition-all" href="tel:+17252241240">CALL (725) 224-1240</a>
</div>
<p class="font-label-caps text-[10px] text-on-surface-variant text-center">2375 E. Tropicana Ave, Suite 3 · Las Vegas, NV 89119 · Minutes from the Strip</p>
</div>
</section>

</main>
"""

# Minimal footer + sticky CTA from walk-in pattern
FOOTER_CUSTOM = """
<footer class="w-full px-margin-mobile md:px-margin-desktop py-12 flex flex-col md:flex-row justify-between items-start gap-8 border-t border-outline-variant bg-surface-container-lowest">
<div class="max-w-md">
<div class="font-headline-md text-headline-md text-on-surface mb-4">WORK OF ART</div>
<p class="font-body-md text-on-surface-variant mb-6 text-sm">Las Vegas cover-up tattoos, realism, and piercing — clinical standards, zero ego.</p>
<p class="font-body-md text-on-surface-variant">2375 E. Tropicana Ave, Suite 3<br/>Las Vegas, NV 89119</p>
</div>
<div class="flex flex-col gap-4">
<h5 class="font-label-caps text-label-caps text-secondary">BOOK</h5>
<a class="font-body-md text-on-surface-variant hover:text-secondary transition-colors" href="/appointments/">Appointments</a>
<a class="font-body-md text-on-surface-variant hover:text-secondary transition-colors" href="tel:+17252241240">(725) 224-1240</a>
</div>
<div class="flex flex-col gap-4">
<h5 class="font-label-caps text-label-caps text-secondary">GUIDES</h5>
<a class="font-body-md text-on-surface-variant hover:text-secondary transition-colors" href="/tattoo_healing_in_desert_climate_expert_aftercare_guide/">Healing guide</a>
<a class="font-body-md text-on-surface-variant hover:text-secondary transition-colors" href="/how_to_choose_a_tattoo_artist_master_selection_guide_2/">Choose an artist</a>
</div>
</footer>
<div class="md:hidden fixed bottom-0 left-0 w-full z-50 glass-nav p-4 border-t border-outline-variant flex gap-3">
<a class="flex-1 text-center bg-secondary text-on-secondary py-3 font-label-caps text-label-caps tracking-widest" href="/appointments/">BOOK CONSULT</a>
<a class="px-4 py-3 border border-outline font-label-caps text-[10px] text-on-surface" href="tel:+17252241240">CALL</a>
</div>
<div class="fixed bottom-20 md:bottom-12 right-4 md:right-12 z-40">
<a class="flex items-center gap-3 bg-secondary text-on-secondary px-5 py-4 font-label-caps text-label-caps tracking-widest shadow-2xl hover:scale-105 transition-transform" href="#consult">
<span class="relative flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-on-secondary opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-on-secondary"></span></span>
FREE CONSULT
</a>
</div>
"""

MNAV_SCRIPT = SHELL_END[SHELL_END.index('<script data-woa-img-load-repair'):]

html = META_HEAD + styles_block + MAIN + FOOTER_CUSTOM + MNAV_SCRIPT
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({len(html):,} bytes)")

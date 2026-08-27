#!/usr/bin/env python3
"""Human/editorial cleanup for the deployed Katelyn profile."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'artists_build'/'katelyn-cole.html'
BOOK='https://jim.com/a/katelyn-delano-rose-morg'


def main():
    s=P.read_text(encoding='utf-8',errors='replace'); old=s
    replacements={
      'Helix body piercing &amp; body piercing store near me — Katelyn Cole at Work of Art Las Vegas. Tattoo body piercing near me, ear curation, body piercings near me. Book today.':'Professional ear, facial and body piercing with Katelyn Cole at Work of Art Las Vegas. Anatomy-aware placement, jewelry guidance, real studio work and direct booking.',
      'https://workofarttattoo.com/best_fine_line_tattoos_in_vegas_ultimate_authority_guide/best-tattoo-las-vegas-custom-sleeve-by-master-artist.webp':'https://workofarttattoo.com/artists/katelyn-cole/piercing-portfolio/katelyn-helix-piercing-02.webp',
      'Work of Art\'s dedicated piercing specialist. Katelyn Cole combines medical-grade safety with high-fashion jewelry design — anatomical ear curation, facial and body piercing, and luxury implant-grade jewelry. Tattoo work with Joshua Cole and Jay Jay; Joshua also offers piercing and trains artists at the studio.':'Work of Art\'s dedicated piercing specialist. Katelyn focuses on anatomy-aware ear curation, facial and body piercing, jewelry fit, calm consultations, and practical aftercare. Tattoo appointments are handled by the studio\'s tattoo artists.',
      'Watch Katelyn at Work of Art — precision ear curation and medical-grade piercing in Las Vegas.':'Watch Katelyn at Work of Art — ear curation and professional piercing in Las Vegas.',
      'Helix Body Piercing &amp; Body Piercing Store Near Me':'Ear, Facial &amp; Body Piercing',
      'Medical-Grade Piercing':'Clean, Professional Piercing',
      'Exceeding state health requirements. Hospital-grade sterilization, single-use tools, and titanium/gold starters for optimal health.':'Single-use piercing needles, studio sterilization protocols, careful placement, and appropriate initial jewelry selected for the piercing and anatomy.',
      'Katelyn Cole specializes in calm, medical-grade ear piercing for younger clients.':'Katelyn Cole offers calm, carefully explained ear-piercing appointments for younger clients who meet the studio\'s age and guardian requirements.',
      'Katelyn is our professional piercer only.':'Katelyn is our professional piercer.',
      'To guarantee sterilization and material safety, we only pierce with jewelry purchased from our studio.':'For new piercings, we use jewelry the studio can verify for material, fit, and sterilization.',
      'Katelyn provides a detailed aftercare kit and schedule to ensure your new piece heals perfectly without bumps or irritation.':'Katelyn provides aftercare guidance designed to support normal healing and help you recognize when irritation needs attention.',
      'Katelyn Cole leads the industry here, utilizing her deep understanding of anatomical structure to create bespoke jewelry landscapes that are as unique as each client.':'Katelyn plans placements around the client\'s anatomy, jewelry preferences, and long-term wear.',
      'Yes, Katelyn Cole is a top-rated professional piercer located just minutes from the Las Vegas Strip at Work of Art. As a leading female professional in the field, she provides a luxury, sterile environment and a sophisticated approach to body modification that is highly sought after by both locals and visitors.':'Yes. Katelyn is Work of Art\'s professional piercer at the Tropicana studio east of the Strip. She offers ear, facial, and body piercing with anatomy-aware placement and direct booking.',
      'At Work of Art Tattoo &amp; Piercing, Katelyn Cole uses high-quality implant-grade titanium, including ASTM F-136 titanium. Our studio is the authoritative source for high-end, safe, and biocompatible jewelry from world-renowned brands like BVLA and Anatometal.':'Ask Katelyn about the materials and jewelry available for your appointment. For initial piercings, the studio prioritizes quality jewelry appropriate for fresh piercings and proper fit.',
      'BVLA, Buddha Jewelry, Anatometal':'Placement, fit &amp; real studio work',
      'email thewhiteknight702@gmail.com':'email kmorgen14@gmail.com',
    }
    for a,b in replacements.items(): s=s.replace(a,b)

    bio='''<h2 class="text-headline-lg font-headline-lg mb-12">About Katelyn Cole</h2>
<div class="prose prose-invert prose-lg max-w-none text-on-surface-variant space-y-8 leading-relaxed">
<p class="text-xl text-on-surface font-medium">Katelyn is Work of Art's professional piercer, with a placement-first approach built around anatomy, jewelry fit, and a calm client experience.</p>
<p>For ear curation, she looks at the ear as a whole before suggesting individual placements. She marks placement with the client involved, explains when anatomy changes the best option, and plans initial jewelry with swelling and long-term wear in mind.</p>
<h3 class="text-headline-md text-on-surface mt-12 mb-4">What an appointment is like</h3>
<p>Appointments are practical and unhurried: anatomy check, placement mark, jewelry discussion, piercing, and clear aftercare. Single-use needles and the studio's sterilization and surface-disinfection procedures are part of the normal setup.</p>
<h3 class="text-headline-md text-on-surface mt-12 mb-4">Aftercare and follow-up</h3>
<p>Katelyn talks through pressure, snagging, sleep, headphones, swimming, downsizing, and other everyday factors that can affect healing. Healing time varies by placement, anatomy, jewelry, aftercare, pressure, and individual biology.</p>
</div></div>\n'''
    s=re.sub(r'(?is)<h2[^>]*>The Definitive Bio of Katelyn Cole</h2>.*?(?=<section\b[^>]*id="piercing-minors")',bio,s,count=1)
    s=re.sub(r'<span class="material-symbols-outlined[^>]*">(?:earbuds|face_5|vaccines)</span>','',s)
    s=s.replace('href="/appointments/">Book Piercing Appointment</a>',f'href="{BOOK}" target="_blank" rel="noopener noreferrer">View Prices &amp; Book Katelyn</a>')
    s=s.replace('href="/appointments/">Book a piercing appointment</a>',f'href="{BOOK}" target="_blank" rel="noopener noreferrer">View prices &amp; book Katelyn</a>')
    if 'data-woa-katelyn-direct-booking="1"' not in s:
        marker='<span class="text-label-caps font-label-caps text-secondary mb-4 block uppercase tracking-[0.3em]">Core Expertise</span>'
        block=f'''<section class="py-12 px-margin-desktop bg-surface-container border-y border-outline-variant/10" data-woa-katelyn-direct-booking="1"><div class="max-w-4xl mx-auto text-center"><span class="text-label-caps font-label-caps text-secondary uppercase tracking-[0.25em]">Current pricing &amp; availability</span><h2 class="text-headline-lg font-headline-lg text-on-surface mt-3">Piercing Prices &amp; Direct Booking</h2><p class="text-body-lg text-on-surface-variant mt-4 mb-6">Katelyn keeps her current service prices and appointment availability on her direct booking page. Jewelry upgrades can vary by the piece selected.</p><a class="bg-secondary text-on-secondary px-10 py-4 inline-block text-label-caps uppercase tracking-wider" href="{BOOK}" target="_blank" rel="noopener noreferrer">See Current Prices &amp; Book Katelyn</a><p class="text-sm text-on-surface-variant mt-4">Questions for Katelyn? <a href="mailto:kmorgen14@gmail.com">kmorgen14@gmail.com</a></p></div></section>'''
        s=s.replace(marker,block+marker,1)
    if s!=old:P.write_text(s,encoding='utf-8');print('updated',P)
    else:print('no changes')
    return 0
if __name__=='__main__':raise SystemExit(main())

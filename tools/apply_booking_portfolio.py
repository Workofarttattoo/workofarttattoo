"""Preserve the owner's three selected booking-page tattoo photographs."""
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PHOTOS = [
    ('/healed_tattoo_gallery_las_vegas/fresh-roaring-lion-thigh-black-grey-joshua-cole-las-vegas.webp', 'Roaring lion thigh tattoo'),
    ('/home_work_of_art_tattoo_piercing/client-portfolio/veiled-woman-statue-black-grey-realism-las-vegas.webp', 'Cloth-covered screaming statue tattoo'),
    ('/appointments/portfolio/woman-portrait-upper-arm-joshua-cole.jpeg', 'Woman portrait upper-arm tattoo'),
]
PIERCINGS = [
    ('/studio_gallery/curated-helix-tragus-lobe-piercings-88475d3e.webp', 'Curated ear piercings'),
    ('/artists/katelyn-cole/piercing-portfolio/katelyn-helix-piercing-02.webp', 'Helix piercing'),
    ('/studio_gallery/nostril-stud-on-smiling-client-dd626b1d.webp', 'Nostril piercing'),
]
CSS = '''<style data-woa-curated-css="1">
.woa-curated-portfolio { border-top: 1px solid rgba(68, 71, 72, 0.45); }
.woa-curated-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; }
@media (min-width: 768px) { .woa-curated-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.woa-curated-tile { display: block; margin: 0; background: #0d0d0d; border: 1px solid rgba(68, 71, 72, 0.35); }
.woa-curated-tile img { display: block; width: 100%; height: auto; aspect-ratio: 3 / 4; object-fit: contain; }
.woa-curated-tile figcaption { padding: 0.75rem; font-size: 0.75rem; line-height: 1.5; color: #e5e2e1; text-align: center; }
</style>'''

def grid(photos, artist):
    tiles = []
    for src, label in photos:
        with Image.open(ROOT / src.lstrip('/')) as photo:
            width, height = photo.size
        tiles.append(f'<figure class="woa-curated-tile"><img src="{src}" alt="{label} by {artist} at Work of Art Tattoo &amp; Piercing in Las Vegas" width="{width}" height="{height}" loading="lazy" decoding="async"/><figcaption>{label}</figcaption></figure>')
    return '<div class="woa-curated-grid">' + ''.join(tiles) + '</div>'


def apply(html):
    html = re.sub(r'<style data-woa-curated-css="1">.*?</style>\s*', '', html, flags=re.S)
    section = CSS + '''<!-- WOA_CURATED_PORTFOLIO_START -->
<section class="woa-curated-portfolio py-12 md:py-16 px-6 md:px-12 bg-surface-container-low" data-woa-curated="1">
<div class="max-w-6xl mx-auto space-y-6">
<div class="text-center space-y-2 max-w-2xl mx-auto">
<h2 class="font-headline-md text-2xl md:text-3xl text-on-surface">Tattoo &amp; piercing work from our studio</h2>
<p class="text-on-surface-variant text-sm">Real clients. Real studio work. Explore both before you book.</p>
</div>
<h3 class="font-headline-md text-xl text-on-surface">Tattoos by Joshua Cole</h3>
''' + grid(PHOTOS, 'Joshua Cole') + '''
<h3 class="font-headline-md text-xl text-on-surface pt-6">Piercings by Katelyn Cole</h3>
''' + grid(PIERCINGS, 'Katelyn Cole') + '''
<p class="text-center pt-4"><a class="text-secondary text-xs uppercase tracking-widest hover:underline" href="/studio_gallery/">View full studio gallery</a></p>
</div></section>
<!-- WOA_CURATED_PORTFOLIO_END -->'''
    html, count = re.subn(r'<!-- WOA_CURATED_PORTFOLIO_START -->.*?<!-- WOA_CURATED_PORTFOLIO_END -->', lambda m: section, html, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Booking portfolio section missing')
    return html

if __name__ == '__main__':
    for name in ('code.html', 'index.html'):
        path = ROOT / 'appointments' / name
        path.write_text(apply(path.read_text()))

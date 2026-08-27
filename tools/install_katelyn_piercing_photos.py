#!/usr/bin/env python3
"""Install Katelyn's real piercing photos into correctly matched static pages."""
from __future__ import annotations
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / 'artists' / 'katelyn-cole' / 'piercing-portfolio'
WEB_ROOT = '/artists/katelyn-cole/piercing-portfolio'
START='<!-- WOA_KATELYN_PIERCING_PHOTOS_START -->'
END='<!-- WOA_KATELYN_PIERCING_PHOTOS_END -->'


def assets(prefixes):
    if isinstance(prefixes,str): prefixes=(prefixes,)
    return sorted(p for p in ASSET_DIR.glob('*.webp') if any(p.name.startswith(x) for x in prefixes))


def alt_for(p: Path):
    n=p.stem
    labels=[('nostril','Nostril piercing'),('septum','Septum piercing'),('earlobe','Ear lobe piercing'),('helix','Helix piercing'),('upper-ear','Upper ear piercing'),('navel','Navel piercing'),('lip-labret','Lip and labret piercing'),('piercing-process','Piercing appointment'),('piercing-client','Piercing client')]
    for key,label in labels:
        if key in n: return f'{label} by Katelyn at Work of Art Tattoo & Piercing in Las Vegas'
    return 'Piercing work by Katelyn at Work of Art Tattoo & Piercing in Las Vegas'


def img_tag(p: Path):
    return (f'<figure class="overflow-hidden border border-outline-variant/20 bg-surface-container">'
            f'<img src="{WEB_ROOT}/{p.name}" alt="{html.escape(alt_for(p),quote=True)}" '
            f'loading="lazy" decoding="async" class="w-full h-full object-cover object-center" width="600" height="600">'
            f'</figure>')


def replace_marked_grid(doc: str, marker_text: str, pics):
    if not pics: return doc
    marker=f'<!-- {marker_text} -->'
    pat=re.compile(rf'({re.escape(marker)}.*?<div class="dense-grid">)(.*?)(</div>)',re.I|re.S)
    return pat.sub(lambda m:m.group(1)+''.join(img_tag(p) for p in pics)+m.group(3),doc,count=1)


def update_profile():
    path=ROOT/'artists_build'/'katelyn-cole.html'
    if not path.is_file(): return False
    doc=path.read_text(encoding='utf-8',errors='replace'); old=doc
    ear=assets(('katelyn-earlobe-','katelyn-helix-','katelyn-ear-cartilage-','katelyn-upper-ear-','katelyn-curated-ear-','katelyn-ear-piercing-process-'))
    face=assets(('katelyn-nostril-','katelyn-septum-','katelyn-lip-labret-','katelyn-lip-nostril-','katelyn-cheek-','katelyn-navel-','katelyn-tongue-'))
    studio=assets(('katelyn-piercing-process-','katelyn-piercing-client-','katelyn-professional-piercer-','katelyn-piercing-portfolio-mixed-'))
    doc=replace_marked_grid(doc,'BLOCK 1: Anatomical Ear Curation',ear)
    doc=replace_marked_grid(doc,'BLOCK 2: Facial & Body Piercing',face)
    doc=replace_marked_grid(doc,'BLOCK 3: Luxury Jewelry',studio)
    doc=doc.replace('>Luxury Jewelry<','>Placement &amp; Studio Work<',1)
    doc=doc.replace('>40+ Curated Designs<','>Real Client Piercings<',1)
    if doc!=old: path.write_text(doc,encoding='utf-8'); return True
    return False


def gallery_section(title,intro,pics):
    if not pics:return ''
    grid='<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">'+''.join(img_tag(p) for p in pics)+'</div>'
    return f'''{START}<section class="py-12 md:py-16 px-4 md:px-margin-desktop bg-background border-t border-outline-variant/20" data-woa-katelyn-piercing-photos="1"><div class="max-w-6xl mx-auto"><h2 class="text-headline-lg font-headline-lg text-on-surface">{html.escape(title)}</h2><p class="text-body-lg text-on-surface-variant mt-3 mb-8">{html.escape(intro)}</p>{grid}<p class="mt-8 text-center"><a class="inline-flex items-center justify-center bg-secondary text-on-secondary px-8 py-3 min-h-[48px] text-label-caps uppercase tracking-widest" href="https://jim.com/a/katelyn-delano-rose-morg" target="_blank" rel="noopener noreferrer">See Katelyn's Current Prices &amp; Book</a></p></div></section>{END}'''


def install_section(path:Path,section:str):
    if not section:return False
    doc=path.read_text(encoding='utf-8',errors='replace')
    if START in doc: new=re.sub(re.escape(START)+r'.*?'+re.escape(END),section,doc,flags=re.S)
    elif '</main>' in doc:new=doc.replace('</main>',section+'\n</main>',1)
    elif '</body>' in doc:new=doc.replace('</body>',section+'\n</body>',1)
    else:return False
    if new!=doc:path.write_text(new,encoding='utf-8');return True
    return False


def update_main_guide():
    p=ROOT/'best_piercing_shop_las_vegas_updated_jewelry_standards'/'code.html'
    if not p.is_file():return False
    pics=[]
    for pref in ('katelyn-helix-','katelyn-earlobe-','katelyn-nostril-','katelyn-septum-','katelyn-lip-labret-','katelyn-navel-','katelyn-piercing-process-'):
        pics.extend(assets(pref)[:2])
    return install_section(p,gallery_section('Real Piercing Work by Katelyn','Real clients from the studio, organized around the placements being shown.',pics))

RULES=[
(('nostril',),'Nostril Piercing Portfolio',( 'katelyn-nostril-',)),
(('septum',),'Septum Piercing Portfolio',( 'katelyn-septum-',)),
(('helix',),'Helix Piercing Portfolio',( 'katelyn-helix-','katelyn-upper-ear-')),
(('navel','belly'),'Navel Piercing Portfolio',( 'katelyn-navel-',)),
(('labret','lip-piercing','lip_piercing'),'Lip & Labret Piercing Portfolio',( 'katelyn-lip-labret-',)),
(('lobe','ear-piercing','ear_piercing'),'Ear Piercing Portfolio',( 'katelyn-earlobe-','katelyn-helix-','katelyn-upper-ear-')),
]

def update_matching_pages():
    changed=[]
    for p in ROOT.rglob('*.html'):
        if any(x in p.parts for x in ('artists_build','artists_raw','.git','node_modules')):continue
        rel=p.relative_to(ROOT).as_posix().lower()
        if rel=='best_piercing_shop_las_vegas_updated_jewelry_standards/code.html':continue
        for needles,title,prefixes in RULES:
            if any(n in rel for n in needles):
                pics=assets(prefixes)
                if install_section(p,gallery_section(title,'Real studio work by Katelyn for this placement.',pics)):changed.append(rel)
                break
    return changed

def main():
    pics=list(ASSET_DIR.glob('*.webp'))
    if not pics:raise SystemExit('No Katelyn piercing WebPs found')
    changed=[]
    if update_profile():changed.append('artists_build/katelyn-cole.html')
    if update_main_guide():changed.append('best_piercing_shop_las_vegas_updated_jewelry_standards/code.html')
    changed.extend(update_matching_pages())
    print(f'Katelyn piercing assets found: {len(pics)}')
    for x in sorted(set(changed)):print('updated',x)
    return 0

if __name__=='__main__':raise SystemExit(main())

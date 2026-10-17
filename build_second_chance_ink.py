#!/usr/bin/env python3
"""Publish the community initiative and preserve discovery after site generators."""
from pathlib import Path
from woa_email_link import apply_public_email_policy, write_email_script
ROOT = Path(__file__).resolve().parent

def main():
    page = ROOT / 'second-chance-ink'
    body = apply_public_email_policy((page / 'page.source').read_text())
    # Use the same verified analytics property as the studio.
    analytics = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-XLXNGGW7SX"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-XLXNGGW7SX');</script>'''
    body = body.replace('</head>', analytics + '</head>')
    for name in ('code.html', 'index.html'):
        (page / name).write_text(body)
    write_email_script(ROOT)
    marker = 'data-second-chance-discovery="1"'
    promo = '''<section data-second-chance-discovery="1" style="padding:48px 24px;background:#171817;border-block:1px solid #e9c34955;color:#f2eee4"><div style="max-width:1100px;margin:auto"><p style="color:#e9c349;font-size:12px;letter-spacing:3px;text-transform:uppercase">A Work of Art community initiative</p><h2 style="font-family:Cinzel,serif;font-size:32px;margin:12px 0">Second Chance Ink</h2><p style="max-width:700px;line-height:1.7">A new chapter, through art. Joshua Cole offers 1–2 donated gang-tattoo cover-ups each month as his schedule allows. Explore the offering, eligibility and the story behind it.</p><a href="/second-chance-ink/" style="display:inline-block;margin-top:20px;color:#e9c349;text-decoration:underline">Discover Second Chance Ink →</a></div></section>'''
    for slug in ('home_work_of_art_tattoo_piercing', 'cover-up-tattoos-las-vegas', ''):
        for name in ('code.html', 'index.html'):
            target = ROOT / slug / name
            if target.exists():
                text = target.read_text()
                if marker not in text and '</main>' in text:
                    target.write_text(text.replace('</main>', promo + '</main>', 1))
    print('Second Chance Ink page and discovery links ready.')

if __name__ == '__main__':
    main()

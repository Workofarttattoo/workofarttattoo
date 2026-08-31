# Image Audit — Work of Art Tattoo & Piercing

Audit date: 2026-08-31  
Scope: Flag uncertain assets; do **not** auto-delete without owner review.

## Confirmed real portfolio (keep)

- `/home_work_of_art_tattoo_piercing/client-portfolio/` — Client tattoo photography
- `/healed_tattoo_gallery_las_vegas/` — Fresh vs healed comparison assets
- `/studio_gallery/` — Studio and piercing portfolio
- `/artists/joshua-cole/`, `/artists/katelyn-cole/`, `/artists/teralyn/` — Artist-specific work
- Healed gallery slugs: `healed_black_grey_tattoos_las_vegas`, `healed_cover_up_tattoos_las_vegas`, `healed_fine_line_tattoos_las_vegas`, `healed_portrait_tattoos_las_vegas`, `healed_color_tattoos_las_vegas`

## Alt text guidance applied

- Descriptive, human-readable alts based on visible subject (artist, style, placement)
- No “near me” or keyword-stuffed alt attributes in build pipeline (`update_image_alt_text.py`)

## Items to review manually

| Asset / pattern | Concern | Recommendation |
|-----------------|---------|----------------|
| `custom-tattoos-las-vegas-epic-snake-texture.webp` (homepage texture) | Decorative texture, not a portfolio piece | Keep as atmosphere; alt is decorative/empty where appropriate |
| Stock hero placeholders in legacy skipped builds | `skipped_upload_build/`, `skipped_pages_clipboard.html` | Not deployed; ignore unless reactivated |
| Piercing specials imagery (`nipple-piercing-special-*`) | Real promo photography — verify ongoing offer | Keep if special is current |
| Geo page OG images (`tattoo-shop-near-*-las-vegas.png`) | May be composite/marketing | Replace with real studio or portfolio photo if owner prefers |

## Not flagged as problems

- Responsive `srcset` width tokens (e.g. `-480.webp`) are image dimensions, not review counts.
- `height="480"` on healed gallery thumbnails is layout metadata, not stale SEO copy.

## Next steps

1. Owner confirms piercing specials images match current offers.
2. Consider one authentic studio exterior/interior photo as default `og:image` on commercial pages.
3. Re-run `update_image_alt_text.py` after adding new portfolio uploads.

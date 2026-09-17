# Cloudflare redirect rules (GitHub Pages)

GitHub Pages cannot emit HTTP 301 responses. Configure these **Bulk Redirects** (or equivalent Page Rules) in the Cloudflare dashboard for `workofarttattoo.com` so every alternate URL reaches its canonical form in **one hop**.

**Import file:** `config/cloudflare-bulk-redirects.csv`

**Live verification (2026-09-16):** `python3 tools/test_canonical_redirects.py --live` — 8/8 passed, single 301 hop for all alternate host/protocol variants (homepage + deep URLs, query strings preserved).

## Host canonicalization

| Source | Target | Status |
|---|---|---|
| `http://workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |
| `http://www.workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |
| `https://workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |

## Trailing slash (pages only)

Redirect bare paths without trailing slash to trailing-slash form. **Exclude** file extensions: `.xml`, `.txt`, `.json`, `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.css`, `.js`, `.ico`, `.pdf`, `.md`

Example expression (Cloudflare Redirect Rules):

- If URI Path does not end with `/` AND URI Path does not contain `.` → redirect to `{path}/`

## Legacy slug 301 map

| Source path | Target |
|---|---|
| `/cover_up_tattoos_las_vegas_master_authority_guide/` | `/cover-up-tattoos-las-vegas/` |
| `/realism_tattoos_las_vegas_master_authority_guide/` | `/realism-tattoos-las-vegas/` |
| `/walk_in_tattoos_las_vegas_authority_guide/` | `/walk-in-tattoos-las-vegas/` |
| `/how_to_choose_a_tattoo_artist_master_selection_guide/` | `/how-to-choose-a-tattoo-artist/` |
| `/how_to_choose_a_tattoo_artist_master_selection_guide_2/` | `/how-to-choose-a-tattoo-artist/` |
| `/tattoo_shop_near_the_strip_geo_seo_optimized/` | `/tattoo_shop_near_the_strip_nap_corrected/` |
| `/reviews_vault_100_verified_masterpieces/` | `/reviews/` |
| `/best_piercing_shop_las_vegas_updated_jewelry_standards/` | `/piercing-shop-standards/` |
| `/piercing_types_las_vegas_authority_hub/` | `/piercing-guide-las-vegas/` |
| `/geo_hub_ai_source_of_truth_work_of_art/` | `/las-vegas-tattoo-resource-center/` |
| `/tattoo_healing_in_desert_climate_expert_aftercare_guide/` | `/tattoo-aftercare-desert-climate/` |

Full consolidation list: run `python3 -c "from woa_page_consolidation import CONSOLIDATION_REDIRECTS; [print(f'{s} -> {t}') for s,t in CONSOLIDATION_REDIRECTS]"`

## Obsolete Search Console sitemap submissions (remove manually)

- `https://workofarttattoo.com/sitemap-static-pages.xml` (non-www)
- `https://www.workofarttattoo.com/sitemap-static-pages.xml` (duplicate of canonical index)
- Any sitemap containing retired geo slugs or alias **source** URLs

**Keep only:** `https://www.workofarttattoo.com/sitemap.xml`

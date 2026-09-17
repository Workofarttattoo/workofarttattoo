# Cloudflare redirect rules (GitHub Pages)

GitHub Pages cannot emit HTTP 301 responses. Configure these **Bulk Redirects** in the Cloudflare dashboard for `workofarttattoo.com` so every alternate URL reaches its canonical form in **one hop**.

**Import file:** `config/cloudflare-bulk-redirects.csv` (regenerate with `python3 generate_cloudflare_bulk_redirects.py`)

**Validate locally:** `python3 tools/validate_gsc_redirects.py`  
**Validate live redirects:** `python3 tools/validate_gsc_redirects.py --live --crawl-sitemap`

## Host canonicalization (listed last in CSV — path rules must import first)

| Source | Target | Status |
|---|---|---|
| `http://workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |
| `http://www.workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |
| `https://workofarttattoo.com/*` | `https://www.workofarttattoo.com/$1` | 301 |

## GSC Wizard obsolete URLs (2026-09) — one-hop 301 map

| Source path | Target |
|---|---|
| `/realism_tattoos_las_vegas_master_authority_guide/` | `/realism-tattoos-las-vegas/` |
| `/skin_science_tattoo_dermatology_authority_guide/` | `/tattoo-skin-science/` |
| `/walk_in_tattoos_las_vegas_authority_guide/` | `/walk-in-tattoos-las-vegas/` |
| `/tattoo_healing_in_desert_climate_expert_aftercare_guide/` | `/tattoo-aftercare-desert-climate/` |
| `/piercing_types_las_vegas_authority_hub/` | `/piercing-guide-las-vegas/` |
| `/tattoo_healing_before_after_real_results/` | `/las-vegas-tattoo-healing-guide/` |
| `/tattoo_shop_near_the_strip_geo_seo_optimized/` | `/tattoo_shop_near_the_strip_nap_corrected/` |
| `/how_to_choose_a_tattoo_artist_master_selection_guide_2/` | `/how-to-choose-a-tattoo-artist/` |
| `/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/` | `/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/` |
| `/cover_up_tattoos_las_vegas_master_authority_guide/` | `/cover-up-tattoos-las-vegas/` |
| `/tattoo_shop_near_las_vegas_convention_center/` | `/tattoo_shop_near_the_strip_nap_corrected/` |
| `/healing_database_tattoo_timeline_encyclopedia_las_vegas/` | `/real_client_tattoo_timeline_las_vegas/` |
| `/tattoo_shop_enterprise_las_vegas/` | `/official_location_hours_contact/` |
| `/tattoo_shop_green_valley_henderson/` | `/tattoo_shop_serving_henderson_nevada/` |
| `/knowledge/implant-grade-titanium-vs-surgical-steel/` | `/katelyn_implant_grade_titanium_las_vegas_authority_guide/` |
| `/review_funnel_google_authority_hub/` | `/reviews/` |

Each path rule is emitted for all four host/protocol variants (`http`/`https` × apex/`www`) **before** the host wildcard rules so external links reach the final HTTPS-www URL in a single hop.

Full consolidation list (120+ slugs): `python3 -c "from woa_page_consolidation import CONSOLIDATION_REDIRECTS; [print(f'/{s}/ -> {d}') for s,d in CONSOLIDATION_REDIRECTS]"`

## Deploy notes

- Do **not** recreate duplicate HTML at obsolete URLs. Retired slugs are excluded from gh-pages via `RETIRE_OVERLAP_SLUGS`.
- Internal links now point directly at canonical targets (`fix_obsolete_internal_links.py` runs in `prepare_site_deploy.py`).
- Import Cloudflare CSV **before** the next gh-pages deploy removes obsolete folders (otherwise old URLs 404 until rules are live).

## Obsolete Search Console sitemap submissions (remove manually)

- `https://workofarttattoo.com/sitemap-static-pages.xml` (non-www)
- `https://www.workofarttattoo.com/sitemap-static-pages.xml` (duplicate of canonical index)
- Any sitemap containing retired geo slugs or alias **source** URLs

**Keep only:** `https://www.workofarttattoo.com/sitemap.xml`

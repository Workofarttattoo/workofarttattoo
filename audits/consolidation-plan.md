# Work of Art Index-Quality and Cannibalization Audit

Generated from the local repository on 2026-08-21. This is a planning audit only: no pages were deleted, redirected, noindexed, or merged.

## Outputs

- `audits/index-quality.csv`: page-by-page scoring for 282 public HTML URLs.
- `audits/cannibalization-map.csv`: keyword/topic clusters and recommended consolidation targets.
- `audits/consolidation-plan.md`: this implementation plan.

## Classification Summary

| Classification | Count |
|---|---:|
| KEEP | 24 |
| IMPROVE | 73 |
| MERGE | 168 |
| 301 | 14 |
| NOINDEX | 3 |
| DELETE/410 | 0 |

## Category Summary

| Category | KEEP | IMPROVE | MERGE | 301 | NOINDEX | DELETE/410 |
|---|---:|---:|---:|---:|---:|---:|
| artist | 4 | 0 | 0 | 0 | 0 | 0 |
| core-home | 1 | 0 | 0 | 1 | 0 | 0 |
| faq | 0 | 1 | 49 | 0 | 0 | 0 |
| healed-gallery | 1 | 6 | 0 | 0 | 0 | 0 |
| healing-aftercare | 5 | 1 | 0 | 1 | 0 | 0 |
| healing-database | 0 | 1 | 95 | 0 | 0 | 0 |
| legacy-artist-build | 0 | 0 | 0 | 5 | 0 | 0 |
| location | 0 | 1 | 10 | 1 | 0 | 0 |
| other | 0 | 6 | 0 | 1 | 2 | 0 |
| piercing-placement | 3 | 49 | 0 | 3 | 0 | 0 |
| skin-science | 0 | 1 | 12 | 0 | 0 | 0 |
| tattoo-style-pricing | 3 | 4 | 2 | 2 | 0 | 0 |
| utility-commercial | 7 | 3 | 0 | 0 | 1 | 0 |

## Decision Framework Used

Each page was scored 0-5 for unique search intent, firsthand information, original studio imagery, original artist commentary, unique factual information, overlap, commercial usefulness, local usefulness, and whether it would still deserve to exist if Google did not exist. Scores are heuristic, but based on parsed page data: title/H1/meta description, word count, image references, internal links, canonical/robots tags, URL patterns, and duplicate/overlap signals.

A page earns `KEEP` when it has durable business/user value: artist portfolio, appointment/contact, core studio, strong gallery proof, or a genuinely useful service page. `IMPROVE` means the page may deserve indexation, but needs more firsthand proof, clearer differentiation, stronger internal links, or better local/commercial utility. `MERGE` means preserve useful content but consolidate it into a stronger page. `301` means a redirect candidate after mapping. `NOINDEX` means useful for users or operations but weak for search indexation. `DELETE/410` is reserved for pages with no user value after redirects are mapped; none were automatically recommended for deletion in this audit.

## Highest-Priority Consolidations

### 1. Healing Database

Recommendation: make `/las-vegas-tattoo-healing-guide/` the primary indexable healing resource and merge the best real proof from `/tattoo_healing_before_after_real_results/` and the existing healing database hub into it.

The consolidated guide should contain: day 0, days 1-3, week 1, week 2, weeks 3-4, months 2-3, and months 6-12, with real Work of Art examples. Granular style/time pages should not remain indexable unless each has enough unique studio evidence: same-client photos, dates/stage labels, artist notes, Las Vegas desert aftercare observations, and clear internal demand.

Healing pages flagged for merge:
- `/healing_database_black_grey_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_black_grey_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_black_grey_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_color_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_color_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_cover_ups_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_cover_ups_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_fine_line_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_fine_line_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_neo_traditional_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_neo_traditional_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_tattoos_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style healing overview overlaps with master healing hub; keep subordinate only with enough real evidence
- `/healing_database_portraits_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_portraits_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_month_6_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_timeline_encyclopedia_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. hub overlaps with better real-example healing page; consolidate into one excellent healing resource
- `/healing_database_tattoo_week_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_week_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_week_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_tattoo_year_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_day_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_day_2_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_day_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_day_4_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_month_1_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- `/healing_database_traditional_month_3_las_vegas/`: MERGE -> https://www.workofarttattoo.com/las-vegas-tattoo-healing-guide/. style/time long-tail page should not remain indexable without unique studio documentation
- ... 6 more rows in CSV

### 2. Location And Landmark Pages

Recommendation: create or strengthen one `/visit/` or `/near-strip/` hub with exact route/travel information, parking, rideshare advice, hotel/show/pool/flight timing, local photos/maps, and specific visitor guidance. Do not keep neighborhood/landmark pages indexable merely because they contain a place name.

Location pages needing consolidation or improvement:
- `/tattoo_shop_enterprise_las_vegas/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_green_valley_henderson/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_near_allegiant_stadium_las_vegas/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_near_las_vegas_airport/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_near_mgm_grand_las_vegas/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_near_the_sphere_las_vegas/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_near_the_strip_geo_seo_optimized/`: 301 -> https://www.workofarttattoo.com/tattoo_shop_near_the_strip_nap_corrected/. central location/near-Strip intent; build as visit hub with route/parking/logistics; canonical differs from public URL; map redirect after confirming target
- `/tattoo_shop_near_the_strip_nap_corrected/`: IMPROVE -> https://www.workofarttattoo.com/visit/. central location/near-Strip intent; build as visit hub with route/parking/logistics
- `/tattoo_shop_paradise_nevada/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/tattoo_shop_spring_valley_las_vegas/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps
- `/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/`: MERGE -> https://www.workofarttattoo.com/visit/. near-identical geo/landmark page; keep indexable only with unique route, parking, venue timing, visitor advice, photos/maps

### 3. Tattoo Style Pages

Recommendation: keep only style pages that are portfolio-led and commercially useful. Merge generated authority-style variants into stronger artist/service pages unless they have real examples, pricing/session context, and Joshua/Teralyn commentary.

Tattoo style/pricing pages needing action:
- `/best_fine_line_tattoos_in_vegas_ultimate_authority_guide/`: MERGE -> https://www.workofarttattoo.com/artists/joshua-cole/. generated authority-style page overlaps artist/service pages; consolidate proof and commentary
- `/best_tattoo_styles_for_sleeves_large_scale_project_hub/`: IMPROVE. needs stronger original portfolio examples/commentary
- `/cover_up_tattoos_las_vegas_master_authority_guide/`: 301 -> https://www.workofarttattoo.com/cover-up-tattoos-las-vegas/. generated authority-style page overlaps artist/service pages; consolidate proof and commentary; canonical differs from public URL; map redirect after confirming target
- `/fine_line_tattoos_las_vegas_master_authority_guide/`: MERGE -> https://www.workofarttattoo.com/artists/joshua-cole/. generated authority-style page overlaps artist/service pages; consolidate proof and commentary
- `/flash_art_deals_under_100/`: IMPROVE. commercial tattoo style/pricing intent
- `/how_much_do_tattoos_cost_in_las_vegas_authority_guide/`: IMPROVE. commercial tattoo style/pricing intent
- `/joshua_oil_painting_black_grey_tattoo_aging_las_vegas/`: IMPROVE. needs stronger original portfolio examples/commentary
- `/realism_tattoos_las_vegas_master_authority_guide/`: 301 -> https://www.workofarttattoo.com/realism-tattoos-las-vegas/. generated authority-style page overlaps artist/service pages; consolidate proof and commentary; canonical differs from public URL; map redirect after confirming target

### 4. Piercing Placement Pages

Recommendation: keep the main piercing hub and high-value placement pages, but improve each placement page with Katelyn/Katie-specific anatomy guidance, jewelry examples, healing expectations, contraindications, and original photos. Exact duplicate URL variants should be redirected after mapping.

Piercing pages needing action:
- `/anti_eyebrow_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/anti_tragus_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/best_piercing_shop_las_vegas_updated_jewelry_standards/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/body_piercing_guide_las_vegas/`: IMPROVE. hub or major category page
- `/bridge_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/cartilage_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/conch_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/daith_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/ear_curation_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/ear_lobe_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/ear_piercing_guide_las_vegas/`: IMPROVE. hub or major category page
- `/ear_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/eyebrow_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/facial_piercing_guide_las_vegas/`: IMPROVE. hub or major category page
- `/flat_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/forward_helix_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/frog_eyes_tongue_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/genital_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/helix_piercing_las_vegas_authority_guide/`: 301 -> https://www.workofarttattoo.com/helix-piercing-las-vegas/. duplicate clean helix URL exists; canonical differs from public URL; map redirect after confirming target
- `/high_nostril_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/industrial_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_anatomy_matters_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_butterfly_backs_truth_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_downsizing_jewelry_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_ear_curation_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_gold_vs_titanium_las_vegas_authority_guide/`: 301 -> https://www.workofarttattoo.com/katelyn_implant_grade_titanium_las_vegas_authority_guide/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary; canonical differs from public URL; map redirect after confirming target
- `/katelyn_implant_grade_titanium_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_piercing_minors_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_sleeping_on_helix_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_threadless_jewelry_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/katelyn_why_piercings_reject_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/labret_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/lip_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/monroe_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/navel_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/nipple_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/nose_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/nostril_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/oral_piercing_guide_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/orbital_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/philtrum_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/piercing_jewelry_guide_las_vegas/`: IMPROVE. hub or major category page
- `/piercing_types_las_vegas_authority_hub/`: 301 -> https://www.workofarttattoo.com/piercing-guide-las-vegas/. hub or major category page; canonical differs from public URL; map redirect after confirming target
- `/rook_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/septum_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/snake_bites_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/snug_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/surface_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/tongue_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/tragus_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/upper_lobe_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary
- `/vertical_labret_piercing_las_vegas_authority_guide/`: IMPROVE -> https://www.workofarttattoo.com/piercing_types_las_vegas_authority_hub/. placement page can stay only with anatomy-specific advice, jewelry examples, photos, and Katelyn/Katie commentary

### 5. Healed Gallery Subcollections

Recommendation: keep the main healed gallery. Keep subcollections only if each has enough original healed examples and commentary to stand alone. Otherwise merge the best photos/captions into the main healed gallery and redirect.

Healed gallery subcollections:
- `/healed_black_grey_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_color_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_cover_up_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_fine_line_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_portrait_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_sleeve_tattoos_las_vegas/`: IMPROVE -> https://www.workofarttattoo.com/healed_tattoo_gallery_las_vegas/. subcollection needs enough distinct healed examples; otherwise merge to healed gallery
- `/healed_tattoo_gallery_las_vegas/`: KEEP. main healed proof gallery

### 6. FAQs And Legacy Pages

Recommendation: FAQ pages should answer real client questions with studio-specific examples and links to booking/service pages. Legacy build/raw pages should not be public competitors for canonical artist pages.

FAQ pages needing merge/improve:
- `/knowledge/best-soap-for-tattoo-aftercare/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/black-and-grey-realism-explained/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/can-you-get-tattoo-while-breastfeeding/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/can-you-swim-after-ear-piercing/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/`: IMPROVE. FAQ has narrow intent; add firsthand examples and internal links
- `/knowledge/cover-up-tattoo-consultation-what-happens/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/ear-curation-multiple-piercings-planning/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/fine-line-tattoo-longevity/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/fine-line-tattoo-pain-level/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/first-tattoo-tips-before-you-book/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-dark-can-cover-up-tattoo-be/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-long-piercing-heals/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-long-tattoo-session-last/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-much-does-tattoo-cost-las-vegas/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-often-wash-new-tattoo/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/how-to-compare-tattoo-studios/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/implant-grade-titanium-vs-surgical-steel/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/least-painful-tattoo-placements/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/luxury-studio-vs-strip-walk-in/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/most-painful-tattoo-placements/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/piercing-bump-vs-infection/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/sleeping-with-new-tattoo-tips/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/sleeve-tattoo-how-many-sessions/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-aftercare-lotion-vs-ointment/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-aging-and-fading-over-time/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-and-blood-donation-wait/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-consultation-what-to-bring/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-cover-up-laser-first/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-deposit-policy-why-required/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-etiquette-studio-behavior/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-flying-after-session/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-gym-workout-aftercare/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-healing-itching-desert-climate/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-healing-peeling-las-vegas/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-infection-signs-when-to-see-doctor/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-mri-with-ink/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-on-ribs-recovery/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-over-scar-tissue/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-scabbing-normal-or-problem/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-second-skin-saniderm-how-long/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-shop-minimum-explained/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-shop-near-strip-worth-drive/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-style-matching-artist/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-sunscreen-after-healing-las-vegas/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-swimming-after-getting-inked/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-tipping-las-vegas/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/tattoo-touch-up-timing/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/vegas-tattoo-aftercare-desert-climate/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/walk-in-tattoo-vs-appointment/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page
- `/knowledge/white-ink-tattoo-facts/`: MERGE -> https://www.workofarttattoo.com/knowledge/. FAQ answer should roll into knowledge hub unless expanded with studio-specific examples; thin page

Legacy/build URLs:
- `/artists_build/joshua-cole.html`: 301 -> https://www.workofarttattoo.com/artists/joshua-cole/. legacy build/raw artist duplicate; public only as build artifact; canonical differs from public URL; map redirect after confirming target
- `/artists_build/katelyn-cole.html`: 301 -> https://www.workofarttattoo.com/artists/katelyn-cole/. legacy build/raw artist duplicate; public only as build artifact; canonical differs from public URL; map redirect after confirming target
- `/artists_build/teralyn.html`: 301 -> https://www.workofarttattoo.com/artists/teralyn/. legacy build/raw artist duplicate; public only as build artifact; canonical differs from public URL; map redirect after confirming target; thin page
- `/artists_raw/joshua.raw.html`: 301 -> https://www.workofarttattoo.com/artists/. legacy build/raw artist duplicate; public only as build artifact
- `/artists_raw/katelyn.raw.html`: 301 -> https://www.workofarttattoo.com/artists/. legacy build/raw artist duplicate; public only as build artifact

## Redirect Mapping Before Any Destructive Work

Before deleting or merging content, create an explicit redirect map with source URL, target URL, reason, and validation status. Suggested order:

1. Lock the canonical healing guide target and decide whether `/tattoo_healing_before_after_real_results/` remains as a supporting proof page or merges into `/las-vegas-tattoo-healing-guide/`.
2. Build `/visit/` or choose `/tattoo_shop_near_the_strip_nap_corrected/` as the location hub, then map all low-unique geo pages into it.
3. Pick canonical clean URLs for tattoo styles, piercing placements, and healed gallery categories.
4. For each `MERGE` page, copy any unique photos, artist notes, FAQs, or local logistics into the target before redirecting.
5. Only after redirects and QA are complete should obsolete pages be considered for `DELETE/410`.

## Notes On Evidence Thresholds

A subordinate healing page should be indexable only when it contains enough Work of Art evidence to justify the exact style/time intent. Minimum threshold: original photo or video evidence, stage/date label, tattoo style and placement, artist attribution, what changed since the previous stage, aftercare/environment context, and a reason this cannot be adequately answered inside the master healing guide.

A location page should be indexable only when it solves a real visitor problem: route, parking, rideshare/dropoff, hotel/venue logistics, appointment timing around shows/flights/pools, unique local imagery/maps, and a distinct local query class. Without that, consolidate.

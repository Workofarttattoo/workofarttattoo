# Search Console + GA4 SEO Sprint

Date: 2026-08-25

This sprint uses the pasted Search Console and GA4 baseline as the evidence source. The repository does not currently include a URL-level GSC Pages export, query export with CTR/position, GA4 event export, or GSC Video invalid-item export, so those items are recorded as required inputs instead of guessed.

## 1. Sleeve Hub Audit

The winning URL is `/best_tattoo_styles_for_sleeves_large_scale_project_hub/`. Google's recommendation panel showed recent impressions up 276%, and visible queries include `arm sleeve tattoo`, `full sleeve tattoo`, `tattoo styles`, `tattoo styles names`, and a sleeve-pricing AI-style query.

Action completed: the source generator now injects a sleeve planning bridge from the hub to Joshua's portfolio, healed sleeve proof, project pricing, and appointments. This protects the informational winner while making the commercial next step more obvious.

## 2. Sleeve Cluster

See `audits/sleeve-cluster-map.csv`. Decision: keep one strong sleeve/style hub, use the session guide and pricing guide as support, and avoid creating duplicate full-sleeve or tattoo-style doorway pages.

## 3. Cover-Up Cluster

See `audits/cover-up-query-map.csv`. The two visible cover-up idea queries map to `/cover-up-tattoos-las-vegas/`. The old underscore master-authority URL remains a consolidation candidate, but this sprint did not delete or 301 it.

## 4. Skin/Dermis Diagnosis

See `audits/skin-dermis-diagnosis.csv`. The dermis page is the known decliner at -77% impressions, and Skin Science has 92 GA4 views with low engagement. Likely issue: intent mismatch and abstract framing, not a known technical indexing failure.

## 5. Indexing Matrix

See `audits/indexing-matrix.csv`. Search Console reports 197 indexed and 89 non-indexed URLs. Exact URL classification is blocked until the GSC Pages export/API is available.

## 6. Piercing Search Footprint

See `audits/piercing-search-footprint.csv`. Piercing demand is visible in GA4, especially `/piercing-guide-las-vegas/` at 162 views and `/helix-piercing-las-vegas/` at 78 views, but piercing queries are not present in the pasted top visible GSC sample.

## 7. CTR Opportunities

See `audits/ctr-opportunities.csv`. The immediate CTR/action test is the sleeve hub bridge and snippet alignment. CTR and average position were not included in the pasted sample, so no CTR deltas were invented.

## 8. Video Indexing

See `audits/video-indexing-audit.csv`. GSC reports 0 indexed video results. No VideoObject schema was added because required per-video metadata must be verified first.

## 9. Structured Data

GSC health from the brief: breadcrumbs 33 valid, image metadata 7 valid, profile page 1 valid, review snippets 37 valid, unparsable structured data 0. The sprint preserves healthy structured data and does not add fabricated AggregateRating or VideoObject data.

## 10. Conversion Integration

The previous GA4 funnel work remains the conversion layer. This sprint connects the visible top-of-funnel sleeve winner to high-intent pages: portfolio, healed proof, pricing, and appointments.

## 11. Pages to Invest In

- `/best_tattoo_styles_for_sleeves_large_scale_project_hub/`
- `/cover-up-tattoos-las-vegas/`
- `/piercing-guide-las-vegas/`
- `/appointments/`
- `/artists/joshua-cole/`
- `/artists/katelyn-cole/`
- `/helix-piercing-las-vegas/`

## 12. Pages to Maintain

- `/`
- `/artists/`
- `/studio_videos/` until video export identifies invalid items
- `/healed_sleeve_tattoos_las_vegas/`
- `/healed_cover_up_tattoos_las_vegas/`
- existing valid BreadcrumbList, ProfilePage, image metadata, and review snippet pages

## 13. Pages to Repair

- `/dermis_skin_science_las_vegas_authority_guide/`
- `/skin_science_tattoo_dermatology_authority_guide/`
- `/helix-piercing-las-vegas/`
- video pages once invalid video item URLs are exported

## 14. Pages to Consolidate

- `/cover_up_tattoos_las_vegas_master_authority_guide/` into `/cover-up-tattoos-las-vegas/` after final redirect mapping
- healing database pages already marked MERGE in `audits/content-consolidation.csv`, preserving any real studio evidence first

## 15. Pages to Retire

No pages were retired in this sprint. Retire/410 decisions still require redirect mapping and confirmation that no unique firsthand evidence would be lost.

## 16. Every File Changed

Generated sprint outputs:

- `audits/sleeve-cluster-map.csv`
- `audits/cover-up-query-map.csv`
- `audits/skin-dermis-diagnosis.csv`
- `audits/indexing-matrix.csv`
- `audits/piercing-search-footprint.csv`
- `audits/ctr-opportunities.csv`
- `audits/video-indexing-audit.csv`
- `audits/review-schema-audit.csv`
- `audits/seo-opportunity-score.csv`
- `audits/search-console-ga4-sprint-report.md`

Source/QA changes:

- `inject_tattoo_seo_conversion.py`
- `tools/seo_qa.py`
- `tools/gsc_ga4_sprint_report.py`

## 17. Build/Test Results

- `python3 -m py_compile inject_tattoo_seo_conversion.py tools/seo_qa.py tools/gsc_ga4_sprint_report.py`: passed.
- `python3 tools/gsc_ga4_sprint_report.py`: generated sprint report CSVs and markdown.
- `python3 prepare_seo.py`: completed.
- `python3 prepare_site_deploy.py`: completed.
- `python3 tools/seo_audit.py`: `Inventoried 287 pages`; `Recommended actions Counter({'KEEP': 183, 'MERGE': 55, 'IMPROVE': 49})`.
- `python3 tools/seo_qa.py`: `SEO QA passed for 181 indexable HTML pages.`
- Generated sleeve hub verified with `data-woa-sleeve-commercial-bridge="1"` and links to Joshua, healed sleeve proof, project pricing, and appointments.
- Indexable URL count before this sprint: 181 QA-scoped indexable HTML pages.
- Indexable URL count after this sprint: 181 QA-scoped indexable HTML pages.
- Destructive consolidation performed: none.

## SEO Opportunity Score

See `audits/seo-opportunity-score.csv`.

## Required External Exports

- Search Console query export with query, page, clicks, impressions, CTR, position
- Search Console Pages indexing export for the 89 non-indexed URLs
- Search Console Video indexing invalid-item export
- GA4 landing page plus conversion-event export connecting views to verified booking events

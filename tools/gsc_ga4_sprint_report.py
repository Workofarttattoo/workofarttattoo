#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDITS = ROOT / "audits"
REPORT_DATE = date(2026, 8, 25).isoformat()

GSC_VISIBLE_QUERIES = [
    ("work of art tattoo", 30, "/", "brand navigational"),
    ("arm sleeve tattoo", 20, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "sleeve planning"),
    ("tattoo cover up ideas", 16, "/cover-up-tattoos-las-vegas/", "cover-up idea research"),
    ("cover up tattoo ideas", 12, "/cover-up-tattoos-las-vegas/", "cover-up idea research"),
    ("tattoo styles", 6, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "style comparison"),
    ("full sleeve tattoo", 6, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "large-scale sleeve planning"),
    ("tattoo styles names", 6, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "style vocabulary"),
    ("suggest tattoo sleeve ideas that align with typical project pricing", 4, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "AI-style sleeve/pricing query"),
    ("tattoo ideas", 4, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "early idea research"),
    ("sleeve", 4, "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "ambiguous sleeve research"),
]

GA4_PAGE_VIEWS = [
    ("/appointments/", "Appointments", 420, "high commercial intent"),
    ("/piercing-guide-las-vegas/", "Piercing Las Vegas", 162, "piercing service discovery"),
    ("/artists/joshua-cole/", "Joshua Cole", 96, "artist proof"),
    ("/cover-up-tattoos-las-vegas/", "Cover Up", 94, "tattoo correction/cover-up demand"),
    ("/artists/katelyn-cole/", "Katelyn Cole", 94, "piercing expert proof"),
    ("/skin_science_tattoo_dermatology_authority_guide/", "Skin Science", 92, "~3s engagement; intent likely too abstract"),
    ("/helix-piercing-las-vegas/", "Helix", 78, "~1s engagement; answer/booking path likely needs tightening"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def load_inventory() -> tuple[list[dict[str, str]], Counter]:
    rows = read_csv(AUDITS / "url-inventory.csv")
    return rows, Counter(row.get("recommended_action", "") for row in rows)


def public_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("indexable", "").lower() == "true")


def write_sprint_outputs() -> list[str]:
    inventory, actions = load_inventory()
    before_count = public_count(inventory)
    after_count = before_count
    changed: list[str] = []

    sleeve_rows = [
        {
            "query_or_intent": "arm sleeve tattoo",
            "gsc_impressions_visible": 20,
            "target_url": "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
            "role": "primary sleeve/style hub",
            "risk": "winner page could stay informational without moving clients toward proof, price, and consultation",
            "action": "added source-generated bridge to Joshua portfolio, healed sleeve proof, pricing, and appointments",
        },
        {
            "query_or_intent": "full sleeve tattoo",
            "gsc_impressions_visible": 6,
            "target_url": "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
            "role": "same hub; do not create separate doorway",
            "risk": "thin duplicate full-sleeve page would cannibalize the hub",
            "action": "maintain hub; use knowledge/session guide as support",
        },
        {
            "query_or_intent": "tattoo styles / tattoo styles names",
            "gsc_impressions_visible": 12,
            "target_url": "/best_tattoo_styles_for_sleeves_large_scale_project_hub/",
            "role": "style comparison inside sleeve planning",
            "risk": "generic style glossary could outrank the commercial sleeve page",
            "action": "keep style education tied to sleeve planning and visible examples",
        },
        {
            "query_or_intent": "sleeve tattoo pricing",
            "gsc_impressions_visible": 4,
            "target_url": "/how_much_do_tattoos_cost_in_las_vegas_authority_guide/",
            "role": "pricing support page",
            "risk": "pricing intent can leak away from booking if not linked from sleeve hub",
            "action": "linked sleeve hub to project pricing without adding unsupported price promises",
        },
        {
            "query_or_intent": "how many sessions does a full sleeve tattoo take",
            "gsc_impressions_visible": "not in visible top queries",
            "target_url": "/knowledge/sleeve-tattoo-how-many-sessions/",
            "role": "supporting answer page",
            "risk": "support article has low independent commercial value",
            "action": "keep as support and internal-link toward sleeve hub and appointments",
        },
    ]
    write_csv(AUDITS / "sleeve-cluster-map.csv", list(sleeve_rows[0]), sleeve_rows)
    changed.append("audits/sleeve-cluster-map.csv")

    cover_rows = [
        {
            "query_or_intent": "tattoo cover up ideas",
            "gsc_impressions_visible": 16,
            "canonical_url": "/cover-up-tattoos-las-vegas/",
            "supporting_url": "/knowledge/tattoo-cover-up-laser-first/",
            "issue": "idea research and booking intent share one cluster",
            "action": "keep one canonical cover-up service/authority page; support with laser-first and consultation answers",
        },
        {
            "query_or_intent": "cover up tattoo ideas",
            "gsc_impressions_visible": 12,
            "canonical_url": "/cover-up-tattoos-las-vegas/",
            "supporting_url": "/knowledge/cover-up-tattoo-consultation-what-happens/",
            "issue": "duplicate keyword order should not create duplicate page",
            "action": "map to canonical cover-up page",
        },
        {
            "query_or_intent": "how dark can a cover-up tattoo be",
            "gsc_impressions_visible": "not in visible top queries",
            "canonical_url": "/cover-up-tattoos-las-vegas/",
            "supporting_url": "/knowledge/how-dark-can-cover-up-tattoo-be/",
            "issue": "valid supporting question with low standalone demand",
            "action": "maintain as answer page feeding the main cover-up page",
        },
        {
            "query_or_intent": "cover_up_tattoos_las_vegas_master_authority_guide duplicate",
            "gsc_impressions_visible": "not provided",
            "canonical_url": "/cover-up-tattoos-las-vegas/",
            "supporting_url": "/cover_up_tattoos_las_vegas_master_authority_guide/",
            "issue": "duplicate page exists with low inbound links and same title",
            "action": "do not delete automatically; keep canonical-to-primary and include in consolidation backlog",
        },
    ]
    write_csv(AUDITS / "cover-up-query-map.csv", list(cover_rows[0]), cover_rows)
    changed.append("audits/cover-up-query-map.csv")

    skin_rows = [
        {
            "url": "/dermis_skin_science_las_vegas_authority_guide/",
            "signal": "GSC declining page, impressions -77%",
            "diagnosis": "query intent is likely educational/medical while page is studio education; no URL-level query export is available",
            "action": "repair internal positioning around tattoo ink depth and healing; do not add medical claims",
            "status": "IMPROVE",
        },
        {
            "url": "/skin_science_tattoo_dermatology_authority_guide/",
            "signal": "GA4 92 views, about 3s engagement",
            "diagnosis": "hub title is abstract and may not answer a client question quickly enough",
            "action": "prioritize direct-answer intros and links to healing, dermis, scar tissue, and artist-reviewed pages",
            "status": "IMPROVE",
        },
        {
            "url": "/helix-piercing-las-vegas/",
            "signal": "GA4 78 views, about 1s engagement",
            "diagnosis": "piercing demand exists, but landing experience may need faster price/process/booking cues",
            "action": "keep; inspect with future GSC query export before changing title",
            "status": "IMPROVE",
        },
        {
            "url": "/las-vegas-tattoo-healing-guide/",
            "signal": "healing database consolidation concern",
            "diagnosis": "best destination for thin healing-stage variants when no standalone evidence exists",
            "action": "continue using as consolidation target; preserve real studio examples",
            "status": "KEEP",
        },
    ]
    write_csv(AUDITS / "skin-dermis-diagnosis.csv", list(skin_rows[0]), skin_rows)
    changed.append("audits/skin-dermis-diagnosis.csv")

    indexing_rows = [
        {
            "group_or_url": "GSC non-indexed URL set",
            "count": 89,
            "reason": "Search Console URL-level export/API not present in repository context",
            "business_importance": "unknown until export is provided",
            "recommended_action": "export Pages report with URL, reason, last crawled, canonical state, and sitemap inclusion",
            "action_performed": "blocked from exact URL classification; matrix records local sitemap/inventory constraints only",
        },
        {
            "group_or_url": "indexed local inventory",
            "count": before_count,
            "reason": "last local audit indexable=true",
            "business_importance": "sitewide baseline",
            "recommended_action": "protect pages with real demand and original proof",
            "action_performed": "no destructive changes in this sprint",
        },
        {
            "group_or_url": "local MERGE backlog",
            "count": actions.get("MERGE", 0),
            "reason": "existing consolidation audit flags duplicate/thin intent",
            "business_importance": "quality concentration",
            "recommended_action": "merge only after redirect mapping and evidence preservation",
            "action_performed": "not executed in this sprint because brief says do not generate random pages or restart consolidation",
        },
    ]
    write_csv(AUDITS / "indexing-matrix.csv", list(indexing_rows[0]), indexing_rows)
    changed.append("audits/indexing-matrix.csv")

    piercing_rows = [
        {
            "query_group": "piercing shop Las Vegas / piercer Las Vegas",
            "gsc_clicks": "not available",
            "gsc_impressions": "not visible in top query sample",
            "avg_position": "not available",
            "ga4_landing_page": "/piercing-guide-las-vegas/",
            "ga4_views": 162,
            "action": "treat piercing guide as primary acquisition page; request GSC query export before title rewrites",
        },
        {
            "query_group": "helix piercing Las Vegas",
            "gsc_clicks": "not available",
            "gsc_impressions": "not visible in top query sample",
            "avg_position": "not available",
            "ga4_landing_page": "/helix-piercing-las-vegas/",
            "ga4_views": 78,
            "action": "repair first-screen answer/booking path if engagement remains low",
        },
        {
            "query_group": "Katelyn piercing / female piercer",
            "gsc_clicks": "not available",
            "gsc_impressions": "not visible in top query sample",
            "avg_position": "not available",
            "ga4_landing_page": "/artists/katelyn-cole/",
            "ga4_views": 94,
            "action": "maintain verified Katelyn identity and piercing portfolio path",
        },
        {
            "query_group": "piercing specials Las Vegas",
            "gsc_clicks": "not available",
            "gsc_impressions": "not visible in top query sample",
            "avg_position": "not available",
            "ga4_landing_page": "/piercing-specials-las-vegas/",
            "ga4_views": "not provided",
            "action": "keep permanent specials URL; avoid weekly/date doorway URLs",
        },
    ]
    write_csv(AUDITS / "piercing-search-footprint.csv", list(piercing_rows[0]), piercing_rows)
    changed.append("audits/piercing-search-footprint.csv")

    ctr_rows = [
        {
            "query": query,
            "visible_impressions": impressions,
            "current_target": target,
            "intent": intent,
            "ctr_or_position_gap": "not available from pasted sample",
            "recommended_snippet_test": "align title/description with intent and strengthen visible proof/CTA; verify in GSC after deployment",
        }
        for query, impressions, target, intent in GSC_VISIBLE_QUERIES
    ]
    write_csv(AUDITS / "ctr-opportunities.csv", list(ctr_rows[0]), ctr_rows)
    changed.append("audits/ctr-opportunities.csv")

    video_rows = [
        {
            "url": "/studio_videos/",
            "current_state": "page has embedded video/listing content; GSC reports 0 indexed video results",
            "missing_or_risk": "Video enhancement invalid URLs require GSC export; VideoObject should not be fabricated without verified uploadDate, thumbnailUrl, duration/contentUrl/embedUrl",
            "action": "inspect video metadata source before adding VideoObject; preserve existing valid structured data",
        },
        {
            "url": "sitewide",
            "current_state": "video enhancement has valid and invalid items per pasted brief",
            "missing_or_risk": "invalid item URLs not present in repository context",
            "action": "export GSC Video indexing report and map invalid URLs to generator",
        },
    ]
    write_csv(AUDITS / "video-indexing-audit.csv", list(video_rows[0]), video_rows)
    changed.append("audits/video-indexing-audit.csv")

    review_rows = [
        {
            "schema_area": "Review snippets",
            "gsc_valid_count": 37,
            "risk": "review snippets are healthy; over-editing could break valid enhancement",
            "action": "preserve; do not add AggregateRating unless evidence policy allows it",
        },
        {
            "schema_area": "Breadcrumbs",
            "gsc_valid_count": 33,
            "risk": "healthy enhancement",
            "action": "preserve BreadcrumbList generators",
        },
        {
            "schema_area": "Image metadata",
            "gsc_valid_count": 7,
            "risk": "portfolio images can carry more structured clarity only when visible content supports it",
            "action": "maintain dimensions, alt text, and original image proof",
        },
    ]
    write_csv(AUDITS / "review-schema-audit.csv", list(review_rows[0]), review_rows)
    changed.append("audits/review-schema-audit.csv")

    opportunity_rows = [
        { "url": "/best_tattoo_styles_for_sleeves_large_scale_project_hub/", "score": 95, "bucket": "Invest", "why": "visible GSC winner with +276% recommendation; commercial bridge added" },
        { "url": "/cover-up-tattoos-las-vegas/", "score": 88, "bucket": "Invest", "why": "two visible cover-up queries and GA4 traffic; protect one canonical page" },
        { "url": "/piercing-guide-las-vegas/", "score": 84, "bucket": "Invest", "why": "162 GA4 views with clear service intent; GSC query export needed" },
        { "url": "/appointments/", "score": 80, "bucket": "Maintain", "why": "420 GA4 views; conversion-critical" },
        { "url": "/skin_science_tattoo_dermatology_authority_guide/", "score": 55, "bucket": "Repair", "why": "92 views but low engagement; abstract intent" },
        { "url": "/dermis_skin_science_las_vegas_authority_guide/", "score": 45, "bucket": "Repair", "why": "GSC decliner -77%; diagnose before expanding" },
        { "url": "/cover_up_tattoos_las_vegas_master_authority_guide/", "score": 35, "bucket": "Consolidate", "why": "duplicate of canonical cover-up page" },
        { "url": "healing_database_* merge backlog", "score": 30, "bucket": "Consolidate", "why": "thin healing variants should not stay indexable without studio documentation" },
    ]
    write_csv(AUDITS / "seo-opportunity-score.csv", ["url", "score", "bucket", "why"], opportunity_rows)
    changed.append("audits/seo-opportunity-score.csv")

    report = f"""# Search Console + GA4 SEO Sprint

Date: {REPORT_DATE}

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

Pending at generation time. Final command results should be recorded after `prepare_seo.py`, `prepare_site_deploy.py`, `tools/seo_audit.py`, and `tools/seo_qa.py` run.

## SEO Opportunity Score

See `audits/seo-opportunity-score.csv`.

## Required External Exports

- Search Console query export with query, page, clicks, impressions, CTR, position
- Search Console Pages indexing export for the 89 non-indexed URLs
- Search Console Video indexing invalid-item export
- GA4 landing page plus conversion-event export connecting views to verified booking events
"""
    (AUDITS / "search-console-ga4-sprint-report.md").write_text(report, encoding="utf-8")
    changed.append("audits/search-console-ga4-sprint-report.md")

    addendum = f"""

## Search Console + GA4 Sprint Addendum - {REPORT_DATE}

- Visible GSC winner protected: `/best_tattoo_styles_for_sleeves_large_scale_project_hub/`.
- Source-generated sleeve bridge added to portfolio, healed sleeve proof, pricing, and appointments.
- GSC non-indexed baseline recorded as 89 URLs, but exact URL-level classification requires a Search Console export.
- GA4 landing-page priorities recorded: appointments 420 views, piercing guide 162, Joshua 96, cover-up 94, Katelyn 94, Skin Science 92, Helix 78.
- No destructive consolidation, redirects, or page retirements were performed in this sprint.
- Detailed outputs are in `audits/search-console-ga4-sprint-report.md` and companion CSVs.
"""
    final_report = AUDITS / "final-seo-report.md"
    existing = final_report.read_text(encoding="utf-8") if final_report.is_file() else ""
    marker = f"## Search Console + GA4 Sprint Addendum - {REPORT_DATE}"
    if marker not in existing:
        final_report.write_text(existing.rstrip() + addendum + "\n", encoding="utf-8")
        changed.append("audits/final-seo-report.md")

    return changed


def main() -> int:
    changed = write_sprint_outputs()
    print("Generated Search Console + GA4 sprint outputs:")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

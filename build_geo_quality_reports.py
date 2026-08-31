#!/usr/bin/env python3
"""Write geo page index-quality audit artifacts."""

from __future__ import annotations

import csv
from pathlib import Path

from woa_geo_pages import GEO_PAGE_ACTIONS, GEO_PAGE_REDIRECTS

ROOT = Path(__file__).resolve().parent
AUDITS = ROOT / "audits"

ROWS = [
    {
        "url": "/official_location_hours_contact/",
        "page_type": "official_location",
        "action": "KEEP",
        "primary_intent": "Verify real studio address, contact, canonical NAP, and location facts.",
        "unique_value": "Canonical studio identity and single public address.",
        "unique_problem": "Clients and directories need one authoritative address, phone, email, and schedule-verification path.",
        "unique_modules": "NAP table; map embed; conservative schedule block; directory FAQ; artist roster",
        "indexing_reason": "This is the citation source of truth and would deserve to exist without Google.",
        "factual_cleanup": "Exact hours and minors-policy details kept conservative until owner verifies.",
        "risk_fixed_or_remaining": "Keep hours conservative until owner verifies.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo-shop-near-las-vegas-strip/",
        "page_type": "geo_hub",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Help Strip visitors plan tattoo and piercing appointments around hotels, shows, flights, pools, and sun.",
        "unique_value": "Central visitor hub with links to MGM, Sphere, Allegiant, airport, Paradise, Henderson, and Spring Valley guidance.",
        "unique_problem": "Strip visitors need one non-doorway planning hub for hotel, show, pool, sun, rideshare, and sober timing decisions.",
        "unique_modules": "Direct answer; Strip area routing; why leave the Strip; visitor aftercare; getting here without exact fares",
        "indexing_reason": "It consolidates weak Strip variants into a useful visitor planning page.",
        "factual_cleanup": "Removed exact fares, exact drive times, stale airport naming, and exact verified-hours claims.",
        "risk_fixed_or_remaining": "Removed exact fares, exact drive times, and stale airport naming.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_mgm_grand_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "South Strip and MGM-area visitor planning.",
        "unique_value": "Show-day, pool/sun, and south Strip routing advice.",
        "unique_problem": "MGM-area hotel guests need tattoo/piercing timing help around shows, alcohol, pools, and resort pickup zones.",
        "unique_modules": "MGM and south Strip planning; pool/sun/show timing; selected tattoo visuals",
        "indexing_reason": "MGM has distinct visitor logistics and meaningful local search intent.",
        "factual_cleanup": "Removed exact mileage, exact drive time, free parking, and two-person roster copy.",
        "risk_fixed_or_remaining": "Removed exact mileage, exact drive time, free parking, and two-person roster copy.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_the_sphere_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Sphere and north Strip show visitor planning.",
        "unique_value": "Venue timing, north Strip traffic, after-show sobriety, and aftercare guidance.",
        "unique_problem": "Sphere and Venetian-corridor visitors need show-day timing guidance before making tattoo or piercing plans.",
        "unique_modules": "Sphere and north Strip timing; after-show reality check; selected detail-work visual",
        "indexing_reason": "The Sphere corridor has a distinct event-timing use case that is not the same as MGM or airport traffic.",
        "factual_cleanup": "Removed exact travel times and parking-price claims.",
        "risk_fixed_or_remaining": "Removed exact travel times and parking-price claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_allegiant_stadium_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Allegiant Stadium event-day tattoo and piercing planning.",
        "unique_value": "Stadium traffic, clothing friction, sobriety, and Mandalay/Luxor crossover context.",
        "unique_problem": "Stadium visitors need help separating tattoo timing from kickoff, concert exits, clothing friction, and event traffic.",
        "unique_modules": "Stadium event logistics; south Strip crossover; selected event-weekend tattoo visual",
        "indexing_reason": "Allegiant has distinct event-day logistics and absorbs weaker Mandalay-adjacent intent.",
        "factual_cleanup": "Removed exact travel times and event parking price claims.",
        "risk_fixed_or_remaining": "Removed exact travel times and event parking price claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_las_vegas_airport/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Harry Reid International Airport travel-day planning.",
        "unique_value": "Flight, terminal, luggage, rental-car, and dry-air aftercare context.",
        "unique_problem": "Airport visitors need practical timing advice around flights, luggage straps, rental cars, cleaning access, and comfort.",
        "unique_modules": "Airport-day decisions; visitor aftercare checklist; selected tattoo and piercing visuals",
        "indexing_reason": "Airport planning is a distinct travel-intent page, not a neighborhood doorway page.",
        "factual_cleanup": "Removed Harry Reid International Airport as current naming, exact terminal drive times, airport fee claims, and unsupported cabin-pressure healing implications.",
        "risk_fixed_or_remaining": "Removed Harry Reid International Airport as current naming, exact terminal drive times, and airport fee claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_paradise_nevada/",
        "page_type": "locality",
        "action": "KEEP",
        "primary_intent": "Clarify the actual locality around Work of Art's E. Tropicana studio.",
        "unique_value": "Explains Paradise as the real place context without claiming a second location.",
        "unique_problem": "Maps and local entities often describe this part of Las Vegas as Paradise, so users need clear address/locality context.",
        "unique_modules": "Why Paradise matters; local client use case; mixed tattoo/piercing visuals",
        "indexing_reason": "It explains the real locality of the actual studio and prevents fake-branch confusion.",
        "factual_cleanup": "Removed exact block/minute claims and unsupported training claim.",
        "risk_fixed_or_remaining": "Removed exact block/minute claims and unsupported training claim.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_spring_valley_las_vegas/",
        "page_type": "geo_resident",
        "action": "KEEP_IMPROVE",
        "primary_intent": "West-valley clients planning repeat tattoo sessions or piercing consults.",
        "unique_value": "Spring Valley route-choice, large-project, and artist-fit context.",
        "unique_problem": "Spring Valley clients need repeat-appointment and west-valley route planning for larger projects.",
        "unique_modules": "West-valley appointment planning; artist-fit section; selected black-and-grey visual",
        "indexing_reason": "It serves resident repeat-session intent and absorbs weaker Summerlin intent.",
        "factual_cleanup": "Removed exact drive times and free parking copy.",
        "risk_fixed_or_remaining": "Removed exact drive times and free parking copy.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_serving_henderson_nevada/",
        "page_type": "geo_resident",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Henderson collectors choosing a destination artist for larger or repeat work.",
        "unique_value": "One consolidated Henderson page replacing Green Valley duplicate.",
        "unique_problem": "Henderson clients need one stronger destination-artist page instead of thin Green Valley/Henderson duplicates.",
        "unique_modules": "Henderson-to-Tropicana fit; when the trip is worth it; selected tattoo and piercing visuals",
        "indexing_reason": "Henderson has resident demand and repeat-session planning needs distinct from tourist landmark pages.",
        "factual_cleanup": "Green Valley duplicate consolidated; exact travel-time/free-parking claims removed.",
        "risk_fixed_or_remaining": "Green Valley links consolidated into this page.",
        "redirect_target": "",
    },
    {
        "url": "/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/",
        "page_type": "comparison",
        "action": "KEEP",
        "primary_intent": "Commercial comparison for visitors deciding between cheap Strip tattoos and a studio appointment.",
        "unique_value": "Decision support, not a thin location variant.",
        "unique_problem": "Visitors need buying-risk comparison before choosing a cheap Strip tattoo option.",
        "unique_modules": "Studio-vs-Strip comparison content",
        "indexing_reason": "This is a commercial decision-support page, not a doorway location variant.",
        "factual_cleanup": "No geo-hour or geo-fare claims added.",
        "risk_fixed_or_remaining": "Monitor for unsupported superlatives.",
        "redirect_target": "",
    },
    {
        "url": "/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/",
        "page_type": "comparison",
        "action": "KEEP",
        "primary_intent": "Expanded Strip-vs-studio commercial comparison.",
        "unique_value": "Visitor buying-risk framing and appointment guidance.",
        "unique_problem": "Visitors comparing studio quality against cheap Strip options need deeper appointment and quality-risk framing.",
        "unique_modules": "Expanded commercial comparison content",
        "indexing_reason": "It supports commercial decision-making; overlap should be reviewed in a later non-geo pass.",
        "factual_cleanup": "No geo-hour or geo-fare claims added.",
        "risk_fixed_or_remaining": "Monitor overlap with shorter comparison page in a future non-geo pass.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_the_strip_geo_seo_optimized/",
        "page_type": "legacy_geo_variant",
        "action": "MERGE_301",
        "primary_intent": "Legacy Strip location landing page.",
        "unique_value": "Superseded by the canonical near-Strip hub.",
        "unique_problem": "Users need the current Strip visitor hub instead of a duplicate legacy URL.",
        "unique_modules": "Redirect placeholder only",
        "indexing_reason": "Does not deserve independent indexing after consolidation.",
        "factual_cleanup": "Legacy exact minutes/free-lot claims retired behind redirect placeholder.",
        "risk_fixed_or_remaining": "Redirect preserves any legacy signals while removing duplicate indexable content.",
        "redirect_target": "/tattoo-shop-near-las-vegas-strip/",
    },
]

for slug, action in GEO_PAGE_ACTIONS.items():
    if action == "MERGE_301":
        ROWS.append(
            {
                "url": f"/{slug}/",
                "page_type": "weak_geo_variant",
                "action": action,
                "primary_intent": "Near-identical neighborhood or landmark location query.",
                "unique_value": "Insufficient unique visitor utility to remain indexable as a separate URL.",
                "unique_problem": "The query can be answered better by a stronger surviving locality, landmark, or visitor hub page.",
                "unique_modules": "Redirect placeholder only",
                "indexing_reason": "No independent indexation after consolidation.",
                "factual_cleanup": "Old exact hours, parking, minor-policy, sterile, and travel-time claims removed from indexable output.",
                "risk_fixed_or_remaining": "Redirect preserves intent while concentrating authority into a stronger nearby page.",
                "redirect_target": GEO_PAGE_REDIRECTS[slug],
            }
        )


def main() -> int:
    AUDITS.mkdir(parents=True, exist_ok=True)
    csv_path = AUDITS / "geo-page-index-quality.csv"
    fields = [
        "url",
        "page_type",
        "action",
        "primary_intent",
        "unique_value",
        "risk_fixed_or_remaining",
        "redirect_target",
        "unique_problem",
        "unique_modules",
        "indexing_reason",
        "factual_cleanup",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ROWS)

    before = len(ROWS)
    merged = sum(1 for row in ROWS if row["action"] == "MERGE_301")
    kept = sum(1 for row in ROWS if row["action"] == "KEEP")
    improved = sum(1 for row in ROWS if row["action"] == "KEEP_IMPROVE")
    noindex = sum(1 for row in ROWS if row["action"] == "NOINDEX")
    deleted = sum(1 for row in ROWS if row["action"] == "DELETE_410")
    after = before - merged
    surviving = [row for row in ROWS if row["action"] in {"KEEP", "KEEP_IMPROVE"}]
    surviving_report = "\n".join(
        f"""### `{row['url']}`
- Target intent: {row['primary_intent']}
- Unique problem: {row['unique_problem']}
- Unique modules: {row['unique_modules']}
- Why it deserves indexing: {row['indexing_reason']}
- Factual claims removed/softened: {row['factual_cleanup']}"""
        for row in surviving
    )
    report = f"""# Geo Page Index-Quality Cleanup

## Result

- TOTAL GEO PAGES BEFORE: {before}
- TOTAL INDEXABLE GEO PAGES AFTER: {after}
- KEEP: {kept}
- KEEP_IMPROVE: {improved}
- MERGE_301: {merged}
- NOINDEX: {noindex}
- DELETE_410: {deleted}

## What Changed

Weak neighborhood and landmark variants were consolidated into the near-Strip hub or the closest stronger page. The generator now publishes only geo pages with a distinct visitor or resident use case.

The near-Strip page is now a generated visitor hub for Strip hotel, show, airport, stadium, pool, sun, and rideshare planning. It links outward to the kept MGM, Sphere, Allegiant, airport, Paradise, Henderson, and Spring Valley pages.

Enterprise decision: MERGE_301. No concrete repository evidence was found proving meaningful Enterprise-specific organic demand or unique first-hand visitor utility. Useful south-valley context is handled by the near-Strip hub and Henderson/Spring Valley pages where relevant.

## Surviving Geo Pages

{surviving_report}

## Factual Risk Cleanup

Removed or blocked exact taxi/rideshare prices, exact drive-time claims, stale Harry Reid International Airport references as current naming, unverified daily hours language, free-parking/private-lot/street-parking claims, fake branch/location language, minors/guardian specifics, sterile/licensed/SNHD claims in geo copy, unsupported cabin-pressure healing implications, and unsupported geo superlatives from indexable geo pages.

## Template Duplication

- GEO TEMPLATE DUPLICATION BEFORE: Surviving geo pages shared the same directions/parking/proof/piercing/gallery/NAP pattern, and retired geo folders retained stale generated copies.
- GEO TEMPLATE DUPLICATION AFTER: Surviving generated pages use intent-specific modules and selected visuals. Retired geo URLs render noindex redirect placeholders.

## Redirects Created

""" + "\n".join(
        f"- `{row['url']}` -> `{row['redirect_target']}`"
        for row in ROWS
        if row["action"] == "MERGE_301"
    ) + """

## QA

- GEO QA FAILURES: See `python3 tools/seo_qa.py`; final run should be zero before deployment.

## Remaining Owner Verification

- Confirm current public hours before publishing exact opening-hours schema or visible hours on geo pages.
- Confirm parking wording if the owner wants more specific parking details.
- Confirm any minors, guardian, jewelry material, or sterile-technique claims before adding them to geo or piercing pages.
- UNVERIFIED GEO FACTS REMAINING: none intentionally published as verified in indexable geo boilerplate.
"""
    (AUDITS / "geo-page-final-report.md").write_text(report, encoding="utf-8")
    print(f"[ok] wrote {csv_path.relative_to(ROOT)}")
    print("[ok] wrote audits/geo-page-final-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

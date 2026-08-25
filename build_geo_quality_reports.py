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
        "risk_fixed_or_remaining": "Keep hours conservative until owner verifies.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_the_strip_nap_corrected/",
        "page_type": "geo_hub",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Help Strip visitors plan tattoo and piercing appointments around hotels, shows, flights, pools, and sun.",
        "unique_value": "Central visitor hub with links to MGM, Sphere, Allegiant, airport, Paradise, Henderson, and Spring Valley guidance.",
        "risk_fixed_or_remaining": "Removed exact fares, exact drive times, and stale airport naming.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_mgm_grand_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "South Strip and MGM-area visitor planning.",
        "unique_value": "Show-day, pool/sun, and south Strip routing advice.",
        "risk_fixed_or_remaining": "Removed exact mileage, exact drive time, free parking, and two-person roster copy.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_the_sphere_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Sphere and north Strip show visitor planning.",
        "unique_value": "Venue timing, north Strip traffic, after-show sobriety, and aftercare guidance.",
        "risk_fixed_or_remaining": "Removed exact travel times and parking-price claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_allegiant_stadium_las_vegas/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Allegiant Stadium event-day tattoo and piercing planning.",
        "unique_value": "Stadium traffic, clothing friction, sobriety, and Mandalay/Luxor crossover context.",
        "risk_fixed_or_remaining": "Removed exact travel times and event parking price claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_near_las_vegas_airport/",
        "page_type": "geo_landmark",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Harry Reid International Airport travel-day planning.",
        "unique_value": "Flight, terminal, luggage, rental-car, and dry-air aftercare context.",
        "risk_fixed_or_remaining": "Removed McCarran as current naming, exact terminal drive times, and airport fee claims.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_paradise_nevada/",
        "page_type": "locality",
        "action": "KEEP",
        "primary_intent": "Clarify the actual locality around Work of Art's E. Tropicana studio.",
        "unique_value": "Explains Paradise as the real place context without claiming a second location.",
        "risk_fixed_or_remaining": "Removed exact block/minute claims and unsupported training claim.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_spring_valley_las_vegas/",
        "page_type": "geo_resident",
        "action": "KEEP_IMPROVE",
        "primary_intent": "West-valley clients planning repeat tattoo sessions or piercing consults.",
        "unique_value": "Spring Valley route-choice, large-project, and artist-fit context.",
        "risk_fixed_or_remaining": "Removed exact drive times and free parking copy.",
        "redirect_target": "",
    },
    {
        "url": "/tattoo_shop_serving_henderson_nevada/",
        "page_type": "geo_resident",
        "action": "KEEP_IMPROVE",
        "primary_intent": "Henderson collectors choosing a destination artist for larger or repeat work.",
        "unique_value": "One consolidated Henderson page replacing Green Valley duplicate.",
        "risk_fixed_or_remaining": "Green Valley links consolidated into this page.",
        "redirect_target": "",
    },
    {
        "url": "/vegas_tattoo_shop_vs_cheap_strip_tattoo_what_you_need_to_know/",
        "page_type": "comparison",
        "action": "KEEP",
        "primary_intent": "Commercial comparison for visitors deciding between cheap Strip tattoos and a studio appointment.",
        "unique_value": "Decision support, not a thin location variant.",
        "risk_fixed_or_remaining": "Monitor for unsupported superlatives.",
        "redirect_target": "",
    },
    {
        "url": "/vegas_tattoo_shop_vs_cheap_strip_tattoo_ultimate_comparison/",
        "page_type": "comparison",
        "action": "KEEP",
        "primary_intent": "Expanded Strip-vs-studio commercial comparison.",
        "unique_value": "Visitor buying-risk framing and appointment guidance.",
        "risk_fixed_or_remaining": "Monitor overlap with shorter comparison page in a future non-geo pass.",
        "redirect_target": "",
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
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ROWS)

    before = len(ROWS)
    merged = sum(1 for row in ROWS if row["action"] == "MERGE_301")
    kept = sum(1 for row in ROWS if row["action"] == "KEEP")
    improved = sum(1 for row in ROWS if row["action"] == "KEEP_IMPROVE")
    after = before - merged
    report = f"""# Geo Page Index-Quality Cleanup

## Result

- GEO PAGES BEFORE: {before}
- GEO PAGES AFTER: {after}
- PAGES MERGED: {merged}
- PAGES KEPT: {kept}
- PAGES IMPROVED: {improved}

## What Changed

Weak neighborhood and landmark variants were consolidated into the near-Strip hub or the closest stronger page. The generator now publishes only geo pages with a distinct visitor or resident use case.

The near-Strip page is now a generated visitor hub for Strip hotel, show, airport, stadium, pool, sun, and rideshare planning. It links outward to the kept MGM, Sphere, Allegiant, airport, Paradise, Henderson, and Spring Valley pages.

## Factual Risk Cleanup

Removed or blocked exact taxi/rideshare prices, exact drive-time claims, stale McCarran references as current naming, unverified daily hours language, free-parking claims, fake branch/location language, and unsupported geo superlatives from indexable geo pages.

## Redirects Created

""" + "\n".join(
        f"- `{row['url']}` -> `{row['redirect_target']}`"
        for row in ROWS
        if row["action"] == "MERGE_301"
    ) + """

## Remaining Owner Verification

- Confirm current public hours before publishing exact opening-hours schema or visible hours on geo pages.
- Confirm parking wording if the owner wants more specific parking details.
- Confirm any minors, guardian, jewelry material, or sterile-technique claims before adding them to geo or piercing pages.
"""
    (AUDITS / "geo-page-final-report.md").write_text(report, encoding="utf-8")
    print(f"[ok] wrote {csv_path.relative_to(ROOT)}")
    print("[ok] wrote audits/geo-page-final-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

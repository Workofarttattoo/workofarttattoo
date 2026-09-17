#!/usr/bin/env python3
"""Print GA4 event ↔ GSC Wizard key-event map from siteData/analytics.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "siteData" / "analytics.json").read_text(encoding="utf-8"))


def main() -> int:
    print("Work of Art — GSC Wizard / GA4 connection map\n")
    print(f"GA4 measurement ID: {DATA['ga4MeasurementId']}")
    print(f"GTM container:       {DATA['gtmContainerId']}")
    print(f"Search Console URL:  {DATA['searchConsoleProperty']}")
    print(f"GSC Wizard MCP:      {DATA['gscWizard']['mcpEndpoint']}\n")

    key = DATA["keyEventsForGscWizard"]
    print("Mark as KEY EVENT in GA4 Admin (for GSC Wizard conversions):")
    print(f"  PRIMARY: {key['primary']}")
    for ev in key["recommendedSecondary"]:
        print(f"  secondary: {ev}")

    print("\nDo NOT mark as key events:")
    for ev in key["diagnosticNotKeyEvents"]:
        print(f"  - {ev}")

    print("\nPriority landing pages for blended GSC+GA4 reports:")
    for path in DATA["gscWizardBlendedReports"]["priorityLandingPages"]:
        print(f"  {DATA['canonicalSiteUrl'].rstrip('/')}{path}")

    print(f"\nEvent contract: {DATA['eventContractDoc']}")
    print(f"Setup guide:    analytics/gsc-wizard-ga4-setup.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

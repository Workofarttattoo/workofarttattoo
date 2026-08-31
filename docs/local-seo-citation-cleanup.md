# Local SEO Citation Cleanup

Track third-party NAP/entity corrections. This repository only fixes **on-site** consistency.

| Platform | Current incorrect information | Correct information | Priority | Suggested action | Status |
|----------|------------------------------|---------------------|----------|------------------|--------|
| TattooRate | Phone: (725) 224-1240 | (725) 224-1240 | P0 | Claim listing; update phone, name, address, URL | Open |
| Local Tattoo Shops | Phone: 725-260-6376 | (725) 224-1240 | P0 | Submit correction or claim | Open |
| Ink Roster | Phone: (725) 224-1240; email: access@thegavl.com; stale hours | (725) 224-1240; booking@workofarttattoo.com; Daily 12 PM–12 AM | P0 | Full profile update | Open |
| VegasNearMe | Phone: 702-224-2617; possibly 24h hours | (725) 224-1240; Daily 12 PM–12 AM | P1 | Correct phone and hours | Open |
| Hucklebuck Tattoo & Body Piercing | Legacy name at 2375 E Tropicana Ave Suite 3 | Work of Art Tattoo & Piercing | P0 | GBP merge/replace; disambiguate on aggregators | Open |
| Google Business Profile | Secondary phones may appear in old citations | Single line: (725) 224-1240 | P0 | Remove artist mobile / legacy numbers in GBP | Monitor |
| Yelp | Secondary phones in syndicated data | (725) 224-1240 | P1 | Audit Yelp + data vendors | Open |

## On-site source of truth

- `siteData/business.json`
- `siteData/contact.json`
- `siteData/artists.json`
- `woa_nav_config.py` (loads siteData at build time)

After external fixes, re-run `tools/seo_qa.py` and spot-check live SERP panels.

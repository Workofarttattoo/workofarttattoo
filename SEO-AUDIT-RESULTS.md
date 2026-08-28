# SEO Audit Results - Work of Art Tattoo & Piercing

Last updated: 2026-08-21

## P0 - Production blockers

| File | Route | Problem | Change made | Validation |
| --- | --- | --- | --- | --- |
| `CNAME` | Sitewide | GitHub Pages was configured for `www.workofarttattoo.com` while the site uses apex canonicals. | Changed CNAME to `workofarttattoo.com`. | `dig` confirmed Cloudflare nameservers and GitHub Pages A/CNAME records; `curl --resolve` confirmed GitHub receives the apex host. |
| `siteData/business.json` | Sitewide | Central business config listed `https://www.workofarttattoo.com` as canonical host while HTML, sitemap, and schema use apex. | Changed `canonicalHost` to `https://www.workofarttattoo.com`. | Canonical scan found `0` bad canonical tags across 276 pages. |
| `DNS-RECOVERY.md` | N/A | DNS/TLS cannot be fully repaired from static HTML. | Added recovery record list, external DNS findings, and GitHub Pages settings. | Live checks documented for NS, A, CNAME, DS, CAA, robots, sitemap, and HTTPS behavior. |

## P1 - Entity/local SEO errors

| File | Route | Problem | Change made | Validation |
| --- | --- | --- | --- | --- |
| `woa_nav_config.py` | Sitewide | Verified artist IG source needed to remain Joshua `@workofarttattoo`, Katie `@stabislifee`. | Confirmed shared constants match owner correction. | Searched rendered artist/profile pages for visible handle placement. |
| `woa_entity_schema.py` and rendered HTML pages | Sitewide JSON-LD | Teralyn schema used unsupported award wording. | Replaced "award-winning fine line floral work" with "fine line floral work." | Repo scan found no remaining public rendered occurrence of the unsupported phrase. |
| `code.html`, `home_work_of_art_tattoo_piercing/code.html`, `expand_homepage_conversion.py`, `fix_homepage_hero_ui.py` | `/` | Homepage copy used hard numeric review wording without a live review source in the repo. | Changed visible copy to conservative non-numeric wording: "Hundreds of positive Google reviews." | Scan found no remaining `300+ verified five-star` or `5.0 average` homepage wording. |

## P2 - Search quality

| File | Route | Problem | Change made | Validation |
| --- | --- | --- | --- | --- |
| `woa_piercing_seo.py` | Generated piercing guides | FAQ generator produced unnatural questions such as "Where do you pierce helix piercing in Las Vegas?" | Changed generator wording to "Where can I get a {placement} in Las Vegas?" | Public scan found no remaining `Where do you pierce` in rendered `code.html` pages. |
| `humanize_site_copy.py` | Future generated copy | A rewrite helper could reintroduce the malformed FAQ wording. | Changed helper replacement to clean up `Where do you pierce...` into `Where can I get...`. | Added stricter QA guard in `tools/seo_qa.py`. |
| 32 rendered FAQ pages | Piercing and tattoo service guides | Current HTML already contained malformed FAQ questions. | Rewrote rendered FAQ questions to natural "Where can I get a/an..." phrasing. | `python3 tools/seo_qa.py` passed for 276 HTML pages. |
| `humanize_site_copy.py` | Future local/near-Strip copy | Generator contained keyword-stuffed "tattoo and body piercing studios in las vegas" passages. | Rewrote those passages into natural local service copy. | Repo scan shows remaining instances only inside repair-script historical match strings, not rendered pages. |
| `tools/seo_qa.py` | QA | QA only caught some tattoo/piercing FAQ contamination. | Added a broader forbidden pattern for `where do you pierce`. | `python3 tools/seo_qa.py` passed after the new guard. |

## P3 - Enhancements

| File | Route | Problem | Change made | Validation |
| --- | --- | --- | --- | --- |
| `DNS-RECOVERY.md` | N/A | DNS repair steps were spread across conversation history. | Added a durable checklist for Cloudflare and GitHub Pages. | Cross-checked against live `dig`/`curl` results and GitHub Pages docs. |
| Sitewide rendered JSON-LD | Sitewide | Artist social links and Teralyn description needed consistency with source data. | Normalized `Person.sameAs` values while preserving Joshua/Katie handle ownership. | JSON-LD parsing remains valid in `tools/seo_qa.py`. |

## Remaining external action

GitHub Pages certificate issuance and Cloudflare DNS propagation are external to this repository. After this commit deploys, check GitHub Pages settings for:

- Custom domain: `workofarttattoo.com`
- DNS check: passing
- HTTPS certificate: issued
- Enforce HTTPS: enabled

If the apex still intermittently shows Bluehost after the DNS TTL expires, the next place to inspect is Cloudflare DNS for stale proxied/flattened records, wildcard records, or registrar-side DS/DNSSEC state.

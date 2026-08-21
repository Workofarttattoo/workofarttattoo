# DNS Recovery - Work of Art Tattoo & Piercing

Last checked: 2026-08-21 16:40 America/Los_Angeles

## Canonical production hostname

Use:

`https://workofarttattoo.com/`

The repository `CNAME` file has been set to:

`workofarttattoo.com`

This aligns GitHub Pages with the site's canonical tags, sitemap URLs, robots.txt sitemap references, OpenGraph URLs, and JSON-LD `@id` values.

## Current live findings

- Nameservers resolve to Cloudflare:
  - `jewel.ns.cloudflare.com`
  - `ricardo.ns.cloudflare.com`
- Public DNS for the apex returns the four GitHub Pages A records.
- Public DNS for `www` returns `workofarttattoo.github.io`.
- No DS record was returned during the check.
- No CAA record was returned during the check.
- `https://www.workofarttattoo.com/robots.txt` returned `200` from GitHub Pages.
- `https://www.workofarttattoo.com/sitemap.xml` returned `200` from GitHub Pages.
- Before this commit, the repo CNAME pointed to `www.workofarttattoo.com`, so GitHub Pages treated `www` as the configured custom domain and redirected the apex toward `www`.
- A normal curl to `https://workofarttattoo.com/` still returned a Bluehost suspended-page response during the check, while forcing GitHub's Pages IP returned GitHub. That indicates stale resolver/cache/proxy state or an external DNS/hosting record outside this repo, not a static HTML problem.

## DNS records to keep in Cloudflare

These values are from GitHub Pages documentation for custom domains.

| Type | Name | Value | Proxy |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | DNS only |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `workofarttattoo.github.io` | DNS only |

Optional AAAA records may be added only if IPv6 is desired and GitHub Pages accepts them in the Pages DNS check:

| Type | Name | Value | Proxy |
| --- | --- | --- | --- |
| AAAA | `@` | `2606:50c0:8000::153` | DNS only |
| AAAA | `@` | `2606:50c0:8001::153` | DNS only |
| AAAA | `@` | `2606:50c0:8002::153` | DNS only |
| AAAA | `@` | `2606:50c0:8003::153` | DNS only |

## DNS records to remove or avoid

- Any Bluehost A records for `@`, `www`, or wildcard hosts.
- Any Bluehost CNAME for `www`.
- Any ALIAS/ANAME/CNAME at the apex if the four GitHub A records are being used.
- Any wildcard record such as `*` pointing to Bluehost or GitHub Pages.
- Any stale DS record at the registrar if Cloudflare DNSSEC is not enabled.
- Any CAA record that blocks Let's Encrypt. No CAA record was present in the live check, which is acceptable.

## GitHub Pages settings

In GitHub repository settings:

1. Pages custom domain should be `workofarttattoo.com`.
2. Wait for DNS check to pass.
3. Wait for the TLS certificate to issue.
4. Enable **Enforce HTTPS** once available.

Expected final redirects:

- `http://workofarttattoo.com/*` -> `https://workofarttattoo.com/*`
- `http://www.workofarttattoo.com/*` -> `https://workofarttattoo.com/*`
- `https://www.workofarttattoo.com/*` -> `https://workofarttattoo.com/*`

If GitHub Pages keeps `www` as the required custom domain after this deployment, reverse the repo `CNAME` and site canonical host together. Do not leave repo `CNAME`, canonical tags, sitemap URLs, and GitHub Pages settings split across different hostnames.

Sources:

- GitHub Pages custom domain DNS records: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Pages HTTPS troubleshooting: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https

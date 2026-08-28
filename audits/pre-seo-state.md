# Pre-SEO State

Generated on 2026-08-21 on branch `seo/master-authority-rebuild`.

## Framework

The repository is a static HTML export. Public pages are stored as folders containing `code.html`, with the homepage at root `code.html`. No `package.json`, Next, Astro, or Vite config was found at repository root.

## Build Instructions

No package/build script is currently defined. The deployable artifact appears to be the repository contents as static files for GitHub Pages or FTP upload. Validation currently uses local Python scripts:

```bash
python3 tools/seo_audit.py
python3 tools/seo_qa.py
```

## Current Routing Architecture

- Public HTML pages found: 276
- Main page type counts: {'tattoo': 72, 'piercing': 55, 'conversion': 2, 'artist': 4, 'home': 1, 'other': 23, 'location': 15, 'gallery': 8, 'healing-database': 96}
- Root homepage: `/`
- Artist profiles: `/artists/`, `/artists/joshua-cole/`, `/artists/katelyn-cole/`, `/artists/teralyn/`
- Many legacy/static-export routes use underscore-heavy slugs, including healing database, authority guide, and location/landmark pages.

## Content Storage Method

Content is embedded directly in HTML files. Shared navigation, schema, and CTA blocks appear duplicated across many static pages rather than rendered from a live template.

## Analytics Detected

- Google Tag Manager container: `GTM-TZTQSQBB`
- Google Analytics / gtag ID: `G-XLXNGGW7SX`
- Several pages include custom `window.gtag("event", ...)` click instrumentation.

## Schema Detected

Most pages include JSON-LD blocks marked with `data-woa-entity-schema="1"`. Schema syntax is now covered by `tools/seo_qa.py`.

## Sitemap Implementation

- `sitemap.xml`
- `sitemap-static-pages.xml`

Both list static canonical URLs using `https://www.workofarttattoo.com/` host format, while `CNAME` is `www.workofarttattoo.com`. Canonical host policy should be finalized and synchronized.

## Robots Implementation

`robots.txt` allows all public crawling and references both XML sitemaps. It also contains AI-crawler-specific allow rules and comments pointing to LLM/AI discovery files.

## Current Audit Summary

- KEEP: 171
- IMPROVE: 50
- MERGE: 55
- 301/NOINDEX/410: not executed automatically; destructive consolidation remains pending redirect mapping.


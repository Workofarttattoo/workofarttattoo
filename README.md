# Work of Art Tattoo & Piercing - Site Deployment

This repository contains the source code and deployment scripts for the [Work of Art Tattoo](https://www.workofarttattoo.com/) website.

## Deployment

Production is deployed from GitHub. Push reconciled source changes to `main`; the `Deploy Work of Art Production` GitHub Actions workflow rebuilds the static site, generates `index.html` files from `code.html`, publishes the result to `gh-pages`, and verifies the live pages.

### Command

Run the following command from the repository root:

```bash
python3 prepare_site_deploy.py
git add -A
git commit -m "Update production site"
git push origin HEAD:main
```

### Prerequisites

1. **GitHub access**: You must be able to push to `main`.
2. **Python dependencies**: The deployment scripts require `beautifulsoup4` and `Pillow`.
   ```bash
   pip install beautifulsoup4 Pillow
   ```

## Script Overview

- `prepare_site_deploy.py`: Regenerates homepage, artist pages, SEO pages, schema, analytics snippets, and visual-intent repairs before a push.
- `.github/workflows/deploy-production.yml`: Rebuilds `main`, applies final QA cleanup, copies `code.html` pages to `index.html`, and publishes to `gh-pages`.
- `tools/a_plus_cleanup.py` and `tools/a_plus_claims_cleanup.py`: Final factual and claim-safety guards used by the production workflow.

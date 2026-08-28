# Work of Art Tattoo & Piercing

Static site for [www.workofarttattoo.com](https://www.workofarttattoo.com/).

## Hosting model (current)

| Layer | Where it lives |
|---|---|
| Site files / HTML | This GitHub repo |
| Production publish | GitHub Pages branch `gh-pages` |
| Custom domain | `www.workofarttattoo.com` via repo `CNAME` |
| Domain registration | Registrar / name ownership only (not web hosting) |
| DNS | Points the domain at GitHub Pages |

**Bluehost is not used for site hosting or FTP deploy anymore.** Do not upload the site to Bluehost `public_html` or run the legacy FTP scripts for production.

## Production deploy

Push (or merge) to `main`. GitHub Actions workflow **Deploy Work of Art Production** (`.github/workflows/deploy-production.yml`):

1. Builds `index.html` from source `code.html` pages
2. Overlays reviewed source onto the existing `gh-pages` tree (preserves live-only routes)
3. Audits critical files and internal links
4. Publishes to `gh-pages`
5. Verifies `www.workofarttattoo.com` serves the exact `DEPLOYED_MAIN_SHA`

Manual re-run: Actions → **Deploy Work of Art Production** → **Run workflow**.

## Local checks

```bash
pip install beautifulsoup4
python3 - <<'PY'
from pathlib import Path
import shutil
for code in Path('.').rglob('code.html'):
    if '.git' in code.parts or 'skipped_upload_build' in code.parts:
        continue
    shutil.copy2(code, code.with_name('index.html'))
print('Generated index.html companions from code.html')
PY
```

Live verification helper (reads the public site, does not FTP):

```bash
python3 verify_live_deploy.py
```

## Legacy FTP scripts (do not use for production)

Older helpers such as `deploy_stitch_site_root.py`, `upload_stitch_ftp.py`, and `seo_rewrite_image_alts.py --deploy` still contain Bluehost FTP code for historical recovery only. They are **not** the production path.

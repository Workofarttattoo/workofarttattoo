# Work of Art Tattoo & Piercing - Site Deployment

This repository contains the source code and deployment scripts for the [Work of Art Tattoo](https://workofarttattoo.com/) website.

## Deployment

To push all changes and pages to the live site, use the master deployment script. This script performs SEO optimizations on all HTML files and uploads core pages, artist portfolios, and authority guides via FTP.

### Command

Run the following command from the repository root:

```bash
FTP_USER=tattoojosh@workofarttattoo.com FTP_PASS=your_password python3 seo_rewrite_image_alts.py --deploy
```

### Prerequisites

1. **FTP Credentials**: You must set `FTP_USER` and `FTP_PASS` as environment variables.
2. **Python Dependencies**: The deployment scripts require `beautifulsoup4`.
   ```bash
   pip install beautifulsoup4
   ```

## Script Overview

- `seo_rewrite_image_alts.py --deploy`: Master script that runs SEO checks and orchestrates the full deployment.
- `deploy_stitch_site_root.py`: Handles the main site structure and homepage.
- `upload_artists_portfolios.py`: Deploys artist-specific pages.
- `upload_skipped_from_clipboard.py`: Handles additional SEO guides.

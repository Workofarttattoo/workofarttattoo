#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/home_work_of_art_tattoo_piercing"
npm install --no-save tailwindcss@3.4.17 @tailwindcss/forms @tailwindcss/container-queries
npx tailwindcss -c tailwind.config.cjs -i tw-input.css -o woa-tailwind.min.css --minify
ls -lh woa-tailwind.min.css

#!/bin/bash
set -e

cd "$(dirname "$0")/.."
npm run build

# rsync -a copies local permissions, so make everything world-readable first
# (dist/ and public/ are 700 locally, which would make the site return 403).
chmod -R u=rwX,go=rX dist

# P .htaccess: never let --delete remove a server-side .htaccess.
rsync -avz --delete \
  --exclude='.DS_Store' \
  --filter='P .htaccess' \
  dist/ w3_nervelab:www-root/

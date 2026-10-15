#!/usr/bin/env bash
# Publicerar A.Z & Kund i Fokus till GitHub Pages (projekt-sida).
set -euo pipefail
PROJ=/home/clawd/az-kund-i-fokus
cd "$PROJ"

# ateranvand autentiserad origin-url som redan satts pa main
REPO_AUTH=$(git -C "$PROJ" remote get-url origin)

echo "== 1. bygg med underkatalog-bas =="
BASE_PATH="/az-kund-i-fokus/" python3 build.py | tail -3

echo "== 2. kopiera byggd sajt =="
rm -rf /tmp/azkf-pages && mkdir -p /tmp/azkf-pages
cp -r index.html 404.html robots.txt sitemap.xml llms.txt assets bilder \
      tjanster priser omraden om-oss faq kontakt integritetspolicy /tmp/azkf-pages/
touch /tmp/azkf-pages/.nojekyll

echo "== 3. pusha till gh-pages =="
cd /tmp/azkf-pages
git init -q
git config user.email "oskarhellmer@gmail.com"
git config user.name "oskarhellmer-dev"
git add -A
git commit -q -m "build $(date +%F\ %H:%M)"
git branch -M gh-pages
git remote add origin "$REPO_AUTH"
GIT_TERMINAL_PROMPT=0 git -c credential.helper= push -f origin gh-pages 2>&1 | tail -2

echo "== 4. aterstall rot-bygge =="
cd "$PROJ" && python3 build.py >/dev/null && echo "root-build ok"

echo "KLART -> https://oskarhellmer-dev.github.io/az-kund-i-fokus/"

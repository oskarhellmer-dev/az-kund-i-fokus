# A.Z & Kund i Fokus — hemsida

Statisk sajt för A.Z & Kund i Fokus (Adrianna Zawada), lokal städfirma i Fengersfors, Dalsland.
Genereras av `build.py` (HTML + sitemap + robots + llms.txt). Bilder via `gen_imgs.py` (fal.ai Seedream v4).

## Bygg om sajten
```bash
python3 build.py          # genererar alla HTML-sidor, sitemap.xml, robots.txt, llms.txt
```

Ändra företagsuppgifter (telefon, e-post, SITE_URL m.m.) i KONFIG-blocket högst upp i `build.py`.

## Bilder
```bash
set -a; . /home/clawd/.hermes/fal.env; set +a
python3 gen_imgs.py       # AI-bilder (hero + tjänstekort) -> bilder/ (webp + jpg)
python3 gen_og.py         # og-bild + bearbetning av riktiga foton
```

## Deploy
Pusha till GitHub → Vercel auto-deployar, eller `vercel deploy --prod --token $VERCEL_TOKEN`.

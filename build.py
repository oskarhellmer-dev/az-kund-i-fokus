#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Byggscript för A.Z & Kund i Fokus (adrianna, Fengersfors).
Genererar statiska HTML-sidor + sitemap.xml + robots.txt + llms.txt.
Kör:  python3 build.py
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# Bas-sökväg: "/" för egen domän/Vercel, "/az-kund-i-fokus/" för GitHub Pages-projekt.
BASE = os.environ.get("BASE_PATH", "/")
if not BASE.endswith("/"):
    BASE += "/"

# ─────────────────────────── KONFIG ───────────────────────────
SITE_URL = "https://kundifokus.se"          # byt när domän är spikad
NAME     = "A.Z & Kund i Fokus"
LEGAL    = "Adrianna Jadwiga Zawada"
ORGNR    = "721130-XXXX"
PHONE    = "0722-199 943"                    # Adrianna
PHONE_TEL = "+46722199943"
EMAIL    = "adrianna.zawada.kundifokus@gmail.com"
INSTAGRAM = "https://www.instagram.com/a.z.kundifokus"
IG_HANDLE = "@a.z.kundifokus"
STREET   = "Genvägen 4 b Bv"
ZIP      = "662 95"
CITY     = "Fengersfors"
REGION   = "Värmlands län"
FOUNDED  = "2026-03-20"
BUILDMON = datetime.date.today().strftime("%Y-%m")
V      = BUILDMON  # cache-bust-sträng för bilder/css

# ─────────────────────────── IKONER ───────────────────────────
def ic(paths, size=22):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

IC = {
  "home":   ic('<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-6h6v6"/>'),
  "truck":  ic('<path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17.5" cy="18" r="1.6"/>'),
  "office": ic('<path d="M4 21V4h10v17"/><path d="M14 10h6v11"/><path d="M7 8h3M7 12h3M7 16h3"/>'),
  "house":  ic('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>'),
  "tools":  ic('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17v3h3l5.3-5.3a4 4 0 0 0 5.4-5.4l-2.3 2.3-2.1-2.1z"/>'),
  "spark":  ic('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>'),
  "check":  ic('<path d="M20 6 9 17l-5-5"/>'),
  "shield": ic('<path d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>'),
  "clock":  ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
  "pin":    ic('<path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>'),
  "phone":  ic('<path d="M5 4h4l2 5-2.5 1.5a12 12 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
  "mail":   ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
  "leaf":   ic('<path d="M20 4C9 4 4 9 4 20c11 0 16-5 16-16z"/><path d="M4 20C8 16 12 13 17 11"/>'),
  "euro":   ic('<path d="M15 6a6 6 0 1 0 0 12"/><path d="M5 10h8M5 14h8"/>'),
  "star":   ic('<path d="M12 3.5l2.5 5.3 5.7.6-4.3 3.8 1.2 5.6L12 16.9 6.9 18.8l1.2-5.6L3.8 9.4l5.7-.6z"/>'),
  "instagram": ic('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>'),
}

LOGO_IMG = ('<picture class="brandmark">'
            '<source srcset="/bilder/logo-mark-160.webp" type="image/webp">'
            '<img src="/bilder/logo-mark-160.png" alt="" width="44" height="44" decoding="async">'
            '</picture>')

# ─────────────────────────── NAV ───────────────────────────
NAV = [
    ("/", "Hem"),
    ("/tjanster/", "Tjänster"),
    ("/priser/", "Priser"),
    ("/omraden/", "Områden"),
    ("/om-oss/", "Om"),
    ("/faq/", "Frågor"),
    ("/kontakt/", "Kontakt"),
]

def nav_html(current):
    lis = []
    for u, t in NAV:
        cur = ' aria-current="page"' if u == current else ''
        lis.append(f'<li><a href="{u}"{cur}>{t}</a></li>')
    items = "".join(lis)
    return f'''<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/">
      {LOGO_IMG}
      <span class="bt">A.Z &amp; Kund i Fokus<small>Städ &amp; lokalvård · Åmål, Säffle med omnejd</small></span>
    </a>
    <nav aria-label="Huvudmeny">
      <ul class="nav-links" id="meny">{items}</ul>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-primary" href="/kontakt/">Få gratis offert</a>
      <button class="menu-btn" aria-label="Öppna meny" aria-expanded="false" aria-controls="meny" id="menybtn"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">{LOGO_IMG}
          <span class="bt" style="display:flex;flex-direction:column;color:#fff;font-weight:800">
            {NAME}<small style="color:#93a29f;font-weight:600">Städ &amp; lokalvård</small></span>
        </div>
        <p style="font-size:.95rem;max-width:38ch">Lokal städfirma i Fengersfors. Hemstäd, flyttstäd, kontorsstäd och stugstäd i Dalsland — med RUT-avdrag och nöjda kunder i fokus.</p>
        <a class="social" href="{INSTAGRAM}" target="_blank" rel="noopener me">{IC["instagram"]} {IG_HANDLE}</a>
      </div>
      <div>
        <h3>Tjänster</h3>
        <ul>
          <li><a href="/tjanster/hemstadning/">Hemstädning</a></li>
          <li><a href="/tjanster/flyttstadning/">Flyttstädning</a></li>
          <li><a href="/tjanster/kontorsstadning/">Kontorsstädning</a></li>
          <li><a href="/tjanster/fritidshus-airbnb/">Fritidshus &amp; Airbnb</a></li>
          <li><a href="/tjanster/byggstad-storstadning/">Stor- &amp; byggstädning</a></li>
        </ul>
      </div>
      <div>
        <h3>Kontakt</h3>
        <ul>
          <li>{STREET}, {ZIP} {CITY}</li>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Org.nr {ORGNR}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {datetime.date.today().year} {NAME} · Org.nr {ORGNR}</span>
      <span><a href="/integritetspolicy/">Integritetspolicy</a> · <a href="/omraden/">Områden</a> · Byggd av <a href="https://varmlandswebb.se" target="_blank" rel="noopener">varmlandswebb.se</a></span>
    </div>
  </div>
</footer>'''

MENU_JS = '''<script>
  (function(){
    var b=document.getElementById('menybtn'),m=document.getElementById('meny');
    if(!b)return;
    b.addEventListener('click',function(){
      var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');
    });
    m.addEventListener('click',function(e){if(e.target.tagName==='A')m.classList.remove('open');});
  })();
</script>'''

# ─────────────────────────── SCHEMA ───────────────────────────
AREAS = ["Fengersfors","Åmål","Bengtsfors","Säffle","Mellerud","Dals-Ed","Årjäng","Karlstad"]
def localbusiness_schema():
    return {
      "@type":"LocalBusiness",
      "@id": SITE_URL + "/#business",
      "name": NAME,
      "legalName": LEGAL,
      "description": "Lokal städfirma i Fengersfors som erbjuder hemstädning, flyttstädning, kontorsstädning och städning av fritidshus/Airbnb i Dalsland och västra Värmland. RUT-avdrag.",
      "url": SITE_URL + "/",
      "image": SITE_URL + "/bilder/og-kundifokus.jpg",
      "logo": SITE_URL + "/bilder/logo.png",
      "telephone": PHONE,
      "email": EMAIL,
      "priceRange": "$$",
      "currenciesAccepted": "SEK",
      "paymentAccepted": "Faktura, Swish, Kort",
      "taxID": ORGNR,
      "foundingDate": FOUNDED,
      "founder": {"@type":"Person","name":"Adrianna Zawada"},
      "address": {"@type":"PostalAddress","streetAddress":STREET,"postalCode":ZIP,"addressLocality":CITY,"addressRegion":REGION,"addressCountry":"SE"},
      "areaServed": [{"@type":"City","name":a} for a in AREAS],
      "sameAs": [INSTAGRAM],
      "openingHoursSpecification": [{
        "@type":"OpeningHoursSpecification",
        "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens":"07:00","closes":"18:00"}],
      "makesOffer": [
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Hemstädning"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Flyttstädning"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Kontorsstädning"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Städning av fritidshus och Airbnb"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Storstädning och byggstädning"}},
      ],
    }

def graph_ld(json_blocks):
    return ('<script type="application/ld+json">' +
            json.dumps({"@context":"https://schema.org","@graph":json_blocks},
                       ensure_ascii=False, separators=(",",":")) +
            '</script>')

def breadcrumb_ld(trail):
    # trail: list of (name, url-or-None)
    items=[]
    for i,(n,u) in enumerate(trail,1):
        it={"@type":"ListItem","position":i,"name":n}
        if u: it["item"]=SITE_URL+u
        items.append(it)
    return {"@type":"BreadcrumbList","itemListElement":items}

def faq_ld(qas):
    return {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}

def service_ld(name, desc, url):
    return {"@type":"Service","name":name,"description":desc,
            "serviceType":name,"provider":{"@id":SITE_URL+"/#business"},
            "areaServed":[{"@type":"City","name":a} for a in AREAS],
            "url":SITE_URL+url}

def crumbs_html(trail):
    parts=[]
    for i,(n,u) in enumerate(trail):
        if u and i<len(trail)-1:
            parts.append(f'<a href="{u}">{n}</a>')
        else:
            parts.append(f'<span aria-current="page" style="opacity:1;color:var(--ink);font-weight:600">{n}</span>')
    return '<nav class="wrap crumbs" aria-label="Brödsmulor">'+'<span>›</span>'.join(parts)+'</nav>'

# ─────────────────────────── HEAD ───────────────────────────
def head(title, desc, slug, extra_ld=None, og_img="/bilder/og-kundifokus.jpg", og_type="website", preload=""):
    canonical = SITE_URL + slug
    ld = [ {"@type":"WebSite","@id":SITE_URL+"/#website","url":SITE_URL+"/","name":NAME,"inLanguage":"sv-SE","publisher":{"@id":SITE_URL+"/#business"}},
           localbusiness_schema() ]
    if extra_ld: ld += extra_ld if isinstance(extra_ld,list) else [extra_ld]
    return f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="{LEGAL}">
<meta name="theme-color" content="#0b5fb4">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css?v={V}">
{preload}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="sv_SE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}{og_img}">
{graph_ld(ld)}
</head>
<body>
<a class="skip" href="#main">Till innehåll</a>'''

def end():
    return MENU_JS + "\n</body>\n</html>\n"

def rebase(html):
    """Prefixa interna root-absoluta länkar med BASE (för underkatalog-host)."""
    if BASE == "/":
        return html
    html = html.replace('href="/', 'href="' + BASE)
    html = html.replace('src="/', 'src="' + BASE)
    html = html.replace('srcset="/', 'srcset="' + BASE)
    html = html.replace('imagesrcset="/', 'imagesrcset="' + BASE)
    html = html.replace(', /bilder/', ', ' + BASE + 'bilder/')
    html = html.replace('content="/', 'content="' + BASE)
    return html

def write_page(slug, html):
    path = os.path.join(ROOT, slug.strip("/"), "index.html") if slug != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        f.write(rebase(html))
    print("  ✓", "/" if slug=="/" else slug)

# ─────────────────────────── DELAR ───────────────────────────
def price_rows(rows):
    out=[]
    for lbl, amt in rows:
        out.append(f'<div class="price-row"><span class="lbl">{lbl}</span><span class="dot"></span><span class="amt">{amt}</span></div>')
    return '<div class="price-wrap">'+''.join(out)+'</div>'

def faq_html(qas):
    d="".join(f'<details><summary>{q}</summary><div class="a">{a}</div></details>' for q,a in qas)
    return f'<div class="faq">{d}</div>'

CTA_BAND = f'''<div class="cta-band">
  <h2>Redo för en skinande ren vardag?</h2>
  <p>Hör av dig så tar vi fram ett kostnadsfritt förslag — med tydligt pris efter RUT-avdrag. Inga bindningstider.</p>
  <div class="hero-actions">
    <a class="btn btn-accent" href="/kontakt/">Begär gratis offert</a>
    <a class="btn btn-ghost" href="/priser/" style="background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.3)">Se priser</a>
  </div>
</div>'''

# ═══════════════════════════ SIDOR ═══════════════════════════

# ---------- STARTSIDA ----------
def page_index():
    title = "Städhjälp i Fengersfors, Åmål & Dalsland | Kund i Fokus"
    desc  = "Lokal städfirma i Fengersfors. Hemstädning, flyttstädning, kontorsstäd och stugstäd i Dalsland & västra Värmland. RUT-avdrag. Boka gratis offert idag."
    hl = faq_ld(HOME_FAQ)
    body = f'''
{nav_html("/")}
<main id="main">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">{IC["leaf"]} Lokal städfirma i Dalsland</span>
      <h1>Skinande rent hem — så att du får tid över till annat</h1>
      <p class="lead">A.Z &amp; Kund i Fokus städar hem, kontor och fritidshus i Fengersfors, Åmål, Bengtsfors och resten av Dalsland — och västra Värmland. Tryggt, noggrant och med <strong>RUT-avdrag</strong> — så du betalar betydligt mindre än du tror.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/kontakt/">Få gratis offert {IC["check"]}</a>
        <a class="btn btn-ghost" href="/priser/">Se priser efter RUT</a>
      </div>
      <div class="trust-row">
        <span>{IC["shield"]} Egen firma · fullt försäkrad</span>
        <span>{IC["euro"]} RUT-avdrag på köpet</span>
        <span>{IC["clock"]} Flexibla tider</span>
      </div>
    </div>
    <div class="hero-media">
      <picture>
        <source type="image/webp" srcset="/bilder/hero-400.webp?v={V} 400w, /bilder/hero-800.webp?v={V} 800w, /bilder/hero-1200.webp?v={V} 1200w" sizes="(max-width:940px) 90vw, 440px">
        <img src="/bilder/hero.jpg?v={V}" alt="Ljust och hemtrevligt vardagsrum efter städning av A.Z & Kund i Fokus" width="1200" height="1500" fetchpriority="high" decoding="async">
      </picture>
      <div class="hero-badge"><span class="num">190</span><small>kr/timme<br>efter RUT-avdrag</small></div>
    </div>
  </div>
</section>

<section class="bg-soft">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">{IC["spark"]} Allt du behöver</span>
      <h2>Städhjälp för hem, företag och fritidshus</h2>
      <p>Från återkommande hemstädning till flyttstäd, kontor och Airbnb — vi anpassar oss efter dig.</p>
    </div>
    <div class="grid grid-3" id="tjanster">
      {SVC_CARD("hemstadning","Hemstädning","home","Återkommande vecko- eller varannanveckasstäd av hemmet. Damm, golv, kök och badrum — alltid samma trygga resultat.","Läs mer")}
      {SVC_CARD("flyttstadning","Flyttstädning","truck","Godkänd flyttstädning inför besiktning av lägenhet eller hus — så att du får tillbaka depositionen.","Läs mer")}
      {SVC_CARD("kontorsstadning","Kontorsstädning","office","Lokalvård för kontor, butik och mindre företag. Fast schema och fakturering, utan krångel.","Läs mer")}
      {SVC_CARD("fritidshus-airbnb","Fritidshus & Airbnb","house","Nyckelfärdig städning av stugor och fritidshus mellan gäster — inklusive påfyllning och soptömning.","Läs mer")}
      {SVC_CARD("byggstad-storstadning","Stor- & byggstädning","tools","Storstädning och byggstädning inför inflytt. Passar perfekt som heldagsuppdrag i Säffle och Mellerud.","Läs mer")}
      <div class="card" style="display:flex;flex-direction:column;justify-content:center;background:linear-gradient(135deg,var(--brand),var(--brand-dark));color:#fff;border:0">
        <h3 style="color:#fff">Behöver du något annat?</h3>
        <p style="color:#d9ece8">Fönsterputs, trappstädning eller inför visning? Berätta vad du behöver — vi löser det mesta inom städ och småfix.</p>
        <a class="btn btn-ghost" style="background:#fff;border-color:#fff;color:var(--brand-dark);align-self:flex-start" href="/kontakt/">Kontakta oss</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{IC["euro"]} RUT-avdrag</span>
      <h2>Du betalar ungefär halva priset — tack vare RUT</h2>
      <p>RUT-avdraget ger dig <strong>50&nbsp;% rabatt på arbetskostnaden</strong> (upp till 50 000 kr per person och år). Vi sköter hela ansökan åt dig och drar av rabatten direkt på fakturan.</p>
    </div>
    <div class="grid grid-2">
      <div class="card"><div class="ic">{IC["euro"]}</div><h3>Så funkar det</h3><p>Du anlitar oss, vi utför städningen och rapporterar RUT till Skatteverket. Du behöver inte lyfta ett finger.</p></div>
      <div class="card"><div class="ic">{IC["check"]}</div><h3>Märks direkt</h3><p>Priset du ser i vår prislista är <em>efter</em> RUT-avdrag. Inga överraskningar när fakturan kommer.</p></div>
    </div>
  </div>
</section>

<section class="bg-soft">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">{IC["pin"]} Där vi jobbar</span>
      <h2>Lokala i Dalsland — och vi kommer till dig</h2>
      <p>Vi schemalägger i zoner så att vi håller nere restider och kan hålla priserna låga. Här är våra områden.</p>
    </div>
    <div class="grid grid-3">
      <div class="zone"><h3>Primär zon <span class="tag">Hemstäd</span></h3><p style="color:var(--muted);margin:6px 0 0">Återkommande städ nära Fengersfors.</p><div class="chips"><span class="chip">Fengersfors</span><span class="chip">Åmål</span><span class="chip">Bengtsfors</span></div></div>
      <div class="zone"><h3>Större uppdrag <span class="tag">Heldag</span></h3><p style="color:var(--muted);margin:6px 0 0">Flytt-, stor- och byggstäd.</p><div class="chips"><span class="chip">Säffle</span><span class="chip">Mellerud</span><span class="chip">Dals-Ed</span></div></div>
      <div class="zone"><h3>Fritidshus <span class="tag">Airbnb</span></h3><p style="color:var(--muted);margin:6px 0 0">Stugor &amp; uthyrning i Dalsland.</p><div class="chips"><span class="chip">Dalsland</span><span class="chip">Västra Värmland</span></div></div>
    </div>
    <div class="map-card" style="margin-top:26px">
      <picture><source type="image/webp" srcset="/bilder/karta-omrade-400.webp?v={V} 400w, /bilder/karta-omrade-800.webp?v={V} 800w, /bilder/karta-omrade-1200.webp?v={V} 1200w" sizes="(max-width:940px) 94vw, 1080px"><img src="/bilder/karta-omrade.jpg?v={V}" alt="Karta över serviceområdet runt Fengersfors, Åmål och Säffle" width="1200" height="680" loading="lazy" decoding="async"></picture>
      <div class="map-legend"><span><i class="base"></i> Vår bas (Fengersfors)</span><span><i class="area"></i> Orter vi arbetar i</span></div>
    </div>
    <p class="center" style="margin-top:24px"><a class="btn btn-ghost" href="/omraden/">Se alla områden och zoner</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">{IC["check"]} Så enkelt är det</span><h2>Från förfrågan till skinande rent</h2></div>
    <div class="steps grid grid-2">
      <div class="step"><span class="n"></span><div><h3>Hör av dig</h3><p>Ring eller fyll i formuläret. Berätta vad du behöver hjälp med.</p></div></div>
      <div class="step"><span class="n"></span><div><h3>Få ett fast förslag</h3><p>Du får ett tydligt pris — efter RUT, utan dolda avgifter.</p></div></div>
      <div class="step"><span class="n"></span><div><h3>Vi bokar en tid</h3><p>Vi hittar en tid som passar dig, och ser till att ha allt med oss.</p></div></div>
      <div class="step"><span class="n"></span><div><h3>Njut av ett rent hem</h3><p>Vi gör jobbet och stämmer av att allt blev som du vill.</p></div></div>
    </div>
  </div>
</section>

<section class="bg-soft">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">{IC["spark"]} Vanliga frågor</span><h2>Frågor och svar</h2></div>
    {faq_html(HOME_FAQ)}
    <p class="center" style="margin-top:20px"><a class="btn btn-ghost" href="/faq/">Fler frågor och svar</a></p>
  </div>
</section>

<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/", [hl, breadcrumb_ld([("Hem","/")])],
                preload=('<link rel="preload" as="image" type="image/webp" '
                         f'imagesrcset="/bilder/hero-400.webp?v={V} 400w, /bilder/hero-800.webp?v={V} 800w, /bilder/hero-1200.webp?v={V} 1200w" '
                         'imagesizes="(max-width:940px) 90vw, 440px" fetchpriority="high">')) + body + end()

def SVC_CARD(slug, name, icon, desc, more):
    return (f'<article class="svc"><a href="/tjanster/{slug}/">'
            f'<div class="thumb"><picture><source type="image/webp" srcset="/bilder/{slug}-800.webp?v={V} 800w" sizes="(max-width:720px) 90vw, 340px"><img src="/bilder/{slug}.jpg?v={V}" alt="{name} – A.Z &amp; Kund i Fokus" width="800" height="500" loading="lazy" decoding="async"></picture></div></a>'
            f'<div class="body"><div class="ic">{IC[icon]}</div><h3>{name}</h3><p>{desc}</p>'
            f'<a class="tipp" href="/tjanster/{slug}/">{more} →</a></div></article>')

HOME_FAQ = [
 ("Vad kostar hemstädning hos er?",
  "Hemstädning kostar från 380 kr/timme inkl. moms — vilket blir cirka 190 kr/timme efter RUT-avdrag. Exakt pris beror på yta och hur ofta du vill ha städning. Begär en gratis offert så får du ett fast pris."),
 ("Får jag RUT-avdrag?",
  "Ja. RUT-avdraget ger dig 50 % rabatt på arbetskostnaden för hemstädning, flyttstädning och fönsterputs, upp till 50 000 kr per person och år. Vi rapporterar till Skatteverket och drar av rabatten direkt på fakturan."),
 ("Städar ni hos företag?",
  "Absolut. Vi utför kontorsstädning och lokalvård åt mindre företag, butiker och kontor med fast schema och fakturering. Kontakta oss för en kostnadsfri offert."),
 ("Hjälper ni till med städning av fritidshus och Airbnb?",
  "Ja — det är en av våra specialiteter. Vi erbjuder nyckelfärdig städning av stugor och fritidshus mellan gäster, inklusive påfyllning av förbrukningsvaror och soptömning. Perfekt för dig som hyr ut på Airbnb."),
 ("Vilka områden jobbar ni i?",
  "Vi utgår från Fengersfors och jobbar i hela Dalsland och västra Värmland: Åmål, Bengtsfors, Säffle, Mellerud, Dals-Ed med flera. Hör av dig om du är osäker på om du ligger inom vårt område."),
 ("Hur bokar jag en städning?",
  "Ring oss eller fyll i formuläret på kontaktsidan. Vi återkommer med ett förslag på pris och tid — oftast samma dag."),
]

# ---------- TJÄNSTER (översikt + undersidor) ----------
def service_page(slug, name, icon, title, desc, intro, points, price_rows_data, faq):
    ld = [service_ld(name, desc, f"/tjanster/{slug}/"),
          breadcrumb_ld([("Hem","/"),("Tjänster","/tjanster/"),(name,f"/tjanster/{slug}/")]),
          faq_ld(faq)]
    pts = "".join(f"<li>{p}</li>" for p in points)
    body = f'''
{nav_html("/tjanster/")}
{crumbs_html([("Hem","/"),("Tjänster","/tjanster/"),(name,None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{IC[icon]} Tjänst</span>
  <h1>{name}</h1>
  <p>{intro}</p>
  <div class="hero-actions"><a class="btn btn-primary" href="/kontakt/">Begär gratis offert</a><a class="btn btn-ghost" href="/priser/">Se priser</a></div>
</div></section>
<section><div class="wrap">
  <div class="grid grid-2" style="align-items:center">
    <div class="prose">
      <h2>Det här ingår</h2>
      <ul>{pts}</ul>
    </div>
    <div>
      <picture><source type="image/webp" srcset="/bilder/{slug}-800.webp?v={V} 800w, /bilder/{slug}-1200.webp?v={V} 1200w" sizes="(max-width:940px) 90vw, 460px"><img src="/bilder/{slug}.jpg?v={V}" alt="{name} utförd av A.Z &amp; Kund i Fokus i Dalsland" width="1200" height="750" loading="lazy" decoding="async" style="border-radius:18px;box-shadow:var(--shadow-lg)"></picture>
    </div>
  </div>
</div></section>
<section class="bg-soft"><div class="wrap"><div class="section-head"><span class="eyebrow">{IC["euro"]} Priser</span><h2>Priser för {name.lower()}</h2><p>Priser efter RUT-avdrag där avdrag gäller. Slutpris bekräftas vid offert.</p></div>
{price_rows(price_rows_data)}
<p class="price-note">Städredskap och produkter ingår i priset. Kortare resor ingår — vid längre körning tillkommer 25 kr/mil, men handlar det om ett större uppdrag (flyttstädning, storstädning) bjuder vi på resan.</p>
</div></section>
<section><div class="wrap"><div class="section-head center"><h2>Vanliga frågor om {name.lower()}</h2></div>{faq_html(faq)}</div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, f"/tjanster/{slug}/", ld) + body + end()

def page_tjanster():
    title = "Tjänster – städning för hem, företag & fritidshus | A.Z & Kund i Fokus"
    desc  = "Hemstädning, flyttstädning, kontorsstädning, stugstädning och byggstädning i Dalsland. Lokal städfirma i Fengersfors med RUT-avdrag. Se alla tjänster."
    ld = [breadcrumb_ld([("Hem","/"),("Tjänster","/tjanster/")])]
    cards = "".join([
        SVC_CARD("hemstadning","Hemstädning","home","Återkommande städning av hemmet — vecka eller varannan vecka.","Läs mer"),
        SVC_CARD("flyttstadning","Flyttstädning","truck","Godkänd flyttstädning inför besiktning, med garanti.","Läs mer"),
        SVC_CARD("kontorsstadning","Kontorsstädning","office","Lokalvård för kontor och företag med fast schema.","Läs mer"),
        SVC_CARD("fritidshus-airbnb","Fritidshus & Airbnb","house","Nyckelfärdig städning av stugor mellan gäster.","Läs mer"),
        SVC_CARD("byggstad-storstadning","Stor- & byggstädning","tools","Heldagsuppdrag inför inflytt, efter renovering.","Läs mer"),
    ])
    body = f'''
{nav_html("/tjanster/")}
{crumbs_html([("Hem","/"),("Tjänster",None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <h1>Våra tjänster</h1>
  <p>Allt inom städ — för privatpersoner, företag och fritidshus i Dalsland och västra Värmland.</p>
</div></section>
<section><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/tjanster/", ld) + body + end()

def page_priser():
    title = "Priser städning efter RUT-avdrag | A.Z & Kund i Fokus"
    desc  = "Tydliga priser på hemstädning, flyttstädning och storstädning i Dalsland — efter RUT-avdrag. Se prislista och begär gratis offert."
    rows = [
        ("Hemstädning — per timme","380 kr"),
        ("Hemstädning — per timme efter RUT","ca 190 kr"),
        ("Flyttstädning upp till 60 m² (efter RUT)","från 1 495 kr"),
        ("Storstädning — per timme","380 kr"),
        ("Fönsterputs — per timme","380 kr"),
        ("Kontorsstädning — per timme (exkl. moms)","304 kr"),
        ("Stugstädning / Airbnb — per tillfälle","offert"),
    ]
    ld = [breadcrumb_ld([("Hem","/"),("Priser","/priser/")])]
    body = f'''
{nav_html("/priser/")}
{crumbs_html([("Hem","/"),("Priser",None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <h1>Priser</h1>
  <p>Vi tror på tydliga priser utan överraskningar. Nedan ser du våra priser <strong>efter RUT-avdrag</strong> där avdraget gäller.</p>
</div></section>
<section><div class="wrap prose">
  {price_rows(rows)}
  <p class="price-note">Priserna är exempel och bekräftas alltid i din offert. RUT-avdraget ger 50 % rabatt på arbetskostnaden, upp till 50 000 kr per person och år. Vid längre körning tillkommer 25 kr/mil — men vid ett större uppdrag (flyttstädning, storstädning) bjuder vi på resan.</p>
  <h2>Varför skiljer sig priset åt?</h2>
  <p>Priset beror på yta, hur ofta du vill ha städning och om det är ett engångs- eller återkommande uppdrag. Återkommande hemstädning blir oftast billigare per tillfälle. Hör av dig så räknar vi på just ditt hem.</p>
  <h2>Vad ingår i priset?</h2>
  <ul>
    <li><strong>Städredskap och produkter</strong> — vi tar med allt vi behöver, utan extra kostnad. Har du egna favoritprodukter använder vi gärna dem.</li>
    <li><strong>RUT-avdraget</strong> — vi rapporterar till Skatteverket och drar av rabatten direkt på din faktura.</li>
    <li><strong>Kortare resor</strong> — ingår i priset. Vid längre körning tillkommer 25 kr/mil.</li>
    <li><strong>Inga dolda avgifter</strong> — priset vi kommer överens om är priset du betalar.</li>
  </ul>
  <div class="note-box">Bor du längre bort? Flyttstädning, storstädning och byggstädning kan vi utföra som heldagsuppdrag även i Säffle, Mellerud och Dals-Ed.</div>
</div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/priser/", ld) + body + end()

def page_omraden():
    title = "Områden vi städar i – Dalsland & västra Värmland | A.Z & Kund i Fokus"
    desc  = "Vi städar i Fengersfors, Åmål, Bengtsfors, Säffle, Mellerud och Dals-Ed. Se våra zoner och boka lokal städhjälp i Dalsland."
    ld = [breadcrumb_ld([("Hem","/"),("Områden","/omraden/")])]
    def z(name, tag, text, chips):
        c="".join(f'<span class="chip">{x}</span>' for x in chips)
        return f'<div class="zone"><h3>{name} <span class="tag">{tag}</span></h3><p style="color:var(--muted);margin:6px 0 0">{text}</p><div class="chips">{c}</div></div>'
    body = f'''
{nav_html("/omraden/")}
{crumbs_html([("Hem","/"),("Områden",None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <h1>Områden vi städar i</h1>
  <p>Vi utgår från Fengersfors och arbetar i Dalsland (Västra Götaland) samt västra Värmland. Genom att jobba i zoner håller vi nere restider — och kan hålla priserna låga.</p>
</div></section>
<section><div class="wrap grid" style="gap:18px">
  {z("Fengersfors &amp; närområdet","Nära",  "Vår hemmabas. Här tar vi gärna återkommande hemstädning och mindre uppdrag med kort varsel.", ["Fengersfors","Tösse","Bäckefors"])}
  {z("Åmål","Hemstäd", "Vår huvudmarknad för återkommande hemstädning — cirka 20 minuter bort. Populärt för veckostädning.", ["Åmål","Edsleskog"])}
  {z("Bengtsfors","Hemstäd", "Nås på under en halvtimme. Här hjälper vi både privatpersoner och mindre företag.", ["Bengtsfors","Billingsfors","Dals Långed"])}
  {z("Säffle, Mellerud &amp; Dals-Ed","Heldag", "Längre bort — därför tar vi här främst större uppdrag som flyttstädning, storstädning och byggstädning.", ["Säffle","Mellerud","Dals-Ed","Åmål"])}
  {z("Fritidshus i Dalsland","Airbnb", "Dalsland är fullt av stugor och fritidshus. Vi sköter nyckelfärdig städning mellan gäster, åt både svenska och utländska ägare.", ["Dalsland","Västra Värmland"])}
</div></section>
<section><div class="wrap">
  <div class="map-card">
    <picture><source type="image/webp" srcset="/bilder/karta-omrade-400.webp?v={V} 400w, /bilder/karta-omrade-800.webp?v={V} 800w, /bilder/karta-omrade-1200.webp?v={V} 1200w" sizes="(max-width:940px) 94vw, 1080px"><img src="/bilder/karta-omrade.jpg?v={V}" alt="Karta över vårt serviceområde i Dalsland och västra Värmland" width="1200" height="680" loading="lazy" decoding="async"></picture>
    <div class="map-legend"><span><i class="base"></i> Vår bas (Fengersfors)</span><span><i class="area"></i> Orter vi arbetar i</span></div>
  </div>
</div></section>
<section class="bg-soft"><div class="wrap prose">
  <h2>Ligger du utanför dessa orter?</h2>
  <p>Hör ändå av dig! Vi tar gärna längre uppdrag om det gäller en heldag — flyttstäd, storstäd eller byggstäd — där resan ryms inom uppdraget. Ring eller skicka en förfrågan så berättar vi vad som passar.</p>
  <h2>Restider och resa</h2>
  <p>Vi utgår från Fengersfors och kortare resor ingår i priset. Vid längre körning tillkommer 25 kr/mil — men gäller det ett större uppdrag som flyttstädning eller storstädning bjuder vi på resan. Det gör att både du och vi slipper överraskningar.</p>
</div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/omraden/", ld) + body + end()

def page_omoss():
    title = "Om oss – lokal städfirma i Fengersfors | A.Z & Kund i Fokus"
    desc  = "A.Z & Kund i Fokus är en lokal städfirma i Fengersfors, grundad av Adrianna Zawada. Vi städar hem, kontor och fritidshus i Dalsland och västra Värmland."
    ld = [{"@type":"AboutPage"}, breadcrumb_ld([("Hem","/"),("Om","/om-oss/")])]
    body = f'''
{nav_html("/om-oss/")}
{crumbs_html([("Hem","/"),("Om",None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <h1>Om A.Z &amp; Kund i Fokus</h1>
  <p>En lokal städfirma i Fengersfors, grundad 2026 av Adrianna Zawada. Vi städar hem, kontor och fritidshus i Dalsland och västra Värmland — med kunden i fokus.</p>
</div></section>
<section><div class="wrap grid grid-2" style="align-items:center">
  <div class="prose">
    <h2>Kunden i fokus — på riktigt</h2>
    <p>Hos oss är du inte ett nummer i en stor kedja, utan en granne vi känner igen. Adrianna startade firman efter flera år i branschen för att kunna göra det där lilla extra — och verkligen se varje kund.</p>
    <p>Vi växer i vår egen takt, med målet att bli fler i teamet och finnas till hands för fler hem och företag i Dalsland och västra Värmland. På sikt vill vi även hjälpa till med små renoveringar och småfix — därav namnet <em>Kund i Fokus</em>.</p>
    <h2>Vad som alltid ingår</h2>
    <ul>
      <li>Egen firma med F-skatt, moms och ansvarsförsäkring</li>
      <li>Tydliga priser efter RUT-avdrag — inga dolda avgifter</li>
      <li>Kontakt med samma person varje gång</li>
      <li>Vi stämmer alltid av att du är nöjd</li>
    </ul>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <picture><source type="image/webp" srcset="/bilder/om-oss-1-600.webp?v={V} 600w, /bilder/om-oss-1-1000.webp?v={V} 1000w" sizes="(max-width:720px) 45vw, 230px"><img src="/bilder/om-oss-1.jpg?v={V}" alt="Städredskap i ett hemtrevligt hem i Dalsland – A.Z &amp; Kund i Fokus" width="1000" height="750" loading="lazy" decoding="async" style="border-radius:16px;box-shadow:var(--shadow)"></picture>
    <picture><source type="image/webp" srcset="/bilder/om-oss-2-600.webp?v={V} 600w, /bilder/om-oss-2-1000.webp?v={V} 1000w" sizes="(max-width:720px) 45vw, 230px"><img src="/bilder/om-oss-2.jpg?v={V}" alt="Ljus och hemtrevlig stugmiljö som vi städar i Dalsland" width="1000" height="750" loading="lazy" decoding="async" style="border-radius:16px;box-shadow:var(--shadow)"></picture>
    <p class="price-note" style="grid-column:1/-1;margin-top:2px">Bilder från vårt arbete i Dalsland och västra Värmland.</p>
  </div>
</div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/om-oss/", ld) + body + end()

def page_kontakt():
    title = "Kontakta oss – boka städning i Dalsland | A.Z & Kund i Fokus"
    desc  = "Kontakta A.Z & Kund i Fokus för gratis offert på städning i Fengersfors, Åmål och Dalsland. Ring, mejla eller fyll i formuläret."
    ld = [{"@type":"ContactPage"}, breadcrumb_ld([("Hem","/"),("Kontakt","/kontakt/")])]
    body = f'''
{nav_html("/kontakt/")}
{crumbs_html([("Hem","/"),("Kontakt",None)])}
<main id="main">
<section class="page-hero"><div class="wrap">
  <h1>Kontakta oss</h1>
  <p>Berätta vad du behöver hjälp med, så återkommer vi med ett kostnadsfritt förslag — oftast samma dag.</p>
</div></section>
<section><div class="wrap contact-grid">
  <div class="contact-card">
    <h2 class="mt-0">Kontaktuppgifter</h2>
    <ul class="contact-list">
      <li><span class="ic">{IC["phone"]}</span><div><b>Telefon</b><span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></div></li>
      <li><span class="ic">{IC["mail"]}</span><div><b>E-post</b><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></li>
      <li><span class="ic">{IC["instagram"]}</span><div><b>Instagram</b><span><a href="{INSTAGRAM}" target="_blank" rel="noopener me">{IG_HANDLE}</a></span></div></li>
      <li><span class="ic">{IC["pin"]}</span><div><b>Adress</b><span>{STREET}, {ZIP} {CITY}</span></div></li>
      <li><span class="ic">{IC["clock"]}</span><div><b>Öppettider</b><span>Måndag–fredag 07–18</span></div></li>
      <li><span class="ic">{IC["shield"]}</span><div><b>Företag</b><span>{LEGAL} · Org.nr {ORGNR}</span></div></li>
    </ul>
  </div>
  <div class="contact-card">
    <h2 class="mt-0">Skicka en förfrågan</h2>
    <form id="offert" novalidate>
      <div class="form-row">
        <div><label for="namn">Namn</label><input id="namn" name="namn" type="text" autocomplete="name" required></div>
        <div><label for="telefon">Telefon</label><input id="telefon" name="telefon" type="tel" autocomplete="tel" required></div>
      </div>
      <label for="epost">E-post</label>
      <input id="epost" name="epost" type="email" autocomplete="email" required>
      <label for="tjanst">Vad gäller det?</label>
      <select id="tjanst" name="tjanst">
        <option>Hemstädning</option>
        <option>Flyttstädning</option>
        <option>Kontorsstädning</option>
        <option>Fritidshus / Airbnb</option>
        <option>Stor- eller byggstädning</option>
        <option>Annat</option>
      </select>
      <label for="meddelande">Meddelande</label>
      <textarea id="meddelande" name="meddelande" placeholder="Berätta gärna om yta, hur ofta och var du bor."></textarea>
      <button class="btn btn-primary" type="submit" style="width:100%;justify-content:center">Skicka förfrågan {IC["check"]}</button>
      <p class="price-note" style="margin-top:12px">Genom att skicka godkänner du vår <a href="/integritetspolicy/">integritetspolicy</a>. Formuläret öppnar ditt e-postprogram med uppgifterna ifyllda.</p>
    </form>
  </div>
</div></section>
<section class="bg-soft"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{IC["pin"]} Hitta hit</span><h2>Vi utgår från Fengersfors</h2><p>Vår bas ligger på Genvägen 4 b i Fengersfors. Därifrån åker vi ut i hela området — Åmål, Bengtsfors, Säffle och omnejd.</p></div>
  <div class="map-card">
    <div id="map-slot">
      <picture><source type="image/webp" srcset="/bilder/karta-adress-400.webp?v={V} 400w, /bilder/karta-adress-800.webp?v={V} 800w, /bilder/karta-adress-1200.webp?v={V} 1200w" sizes="(max-width:940px) 94vw, 1080px"><img src="/bilder/karta-adress.jpg?v={V}" alt="Karta över Fengersfors med A.Z &amp; Kund i Fokus bas" width="1200" height="560" loading="lazy" decoding="async"></picture>
    </div>
    <div class="map-actions">
      <a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&amp;query=Genv%C3%A4gen%204%2C%20662%2095%20Fengersfors" target="_blank" rel="noopener">Öppna i Google Maps</a>
      <button class="btn btn-ghost" type="button" id="mapload">Visa interaktiv karta</button>
    </div>
  </div>
</div></section>
</main>
{FOOTER}
<script>
(function(){{
  var b=document.getElementById('mapload'); if(!b)return;
  b.addEventListener('click',function(){{
    var s=document.getElementById('map-slot');
    s.innerHTML='<iframe title="Karta \\u2013 Fengersfors" src="https://www.google.com/maps?q=Genv%C3%A4gen+4,+662+95+Fengersfors&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>';
    b.remove();
  }});
}})();
</script>
<script>
(function(){{
  var f=document.getElementById('offert'); if(!f)return;
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var g=function(id){{return (document.getElementById(id).value||'').trim();}};
    var body='Namn: '+g('namn')+'%0ATelefon: '+g('telefon')+'%0AE-post: '+g('epost')
      +'%0ATjänst: '+g('tjanst')+'%0A%0A'+encodeURIComponent(g('meddelande'));
    window.location.href='mailto:{EMAIL}?subject='+encodeURIComponent('Offertförfrågan – städning')+'&body='+body;
  }});
}})();
</script>
'''
    return head(title, desc, "/kontakt/", ld) + body + end()

FAQ_ALL = HOME_FAQ + [
 ("Tar ni med egna städprodukter och redskap?",
  "Ja, vi tar alltid med egna produkter och redskap — det ingår i priset utan extra kostnad. Har du egna favoritprodukter du vill att vi använder går det såklart bra."),
 ("Kostar det extra om ni har långt att köra?",
  "Kortare resor ingår. Vid längre körning tillkommer 25 kr/mil — men handlar det om ett större uppdrag som flyttstädning eller storstädning bjuder vi på resan."),
 ("Är ni försäkrade?",
  "Ja, vi är en registrerad enskild firma med F-skatt, moms och ansvarsförsäkring. Skulle något hända är du trygg."),
 ("Kan jag avboka eller flytta en tid?",
  "Absolut. Hör bara av dig i så god tid som möjligt, helst senast dagen innan, så bokar vi om tiden utan kostnad."),
 ("Städar ni efter renovering eller bygg?",
  "Ja, vi utför storstädning och byggstädning inför inflytt eller efter renovering. Det passar bäst som ett heldagsuppdrag."),
 ("Hur snabbt kan ni komma?",
  "Ofta inom några dagar. Hör av dig så snart du vet — vid återkommande hemstädning lägger vi upp ett fast schema direkt."),
]

def page_faq():
    title = "Vanliga frågor om städning & RUT | A.Z & Kund i Fokus"
    desc  = "Svar på vanliga frågor om hemstädning, flyttstädning, RUT-avdrag, priser och områden i Dalsland. Hitta svaret eller kontakta oss direkt."
    ld = [faq_ld(FAQ_ALL), breadcrumb_ld([("Hem","/"),("Frågor","/faq/")])]
    body = f'''
{nav_html("/faq/")}
{crumbs_html([("Hem","/"),("Frågor",None)])}
<main id="main">
<section class="page-hero"><div class="wrap"><h1>Vanliga frågor</h1><p>Här har vi samlat de frågor vi får oftast. Hittar du inte svaret? Hör av dig — vi hjälper dig gärna.</p></div></section>
<section><div class="wrap prose" style="max-width:820px">{faq_html(FAQ_ALL)}</div></section>
<section><div class="wrap">{CTA_BAND}</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/faq/", ld) + body + end()

def page_privacy():
    title = "Integritetspolicy | A.Z & Kund i Fokus"
    desc  = "Så hanterar A.Z & Kund i Fokus dina personuppgifter enligt GDPR — vilka uppgifter vi samlar in, varför och dina rättigheter."
    ld = [breadcrumb_ld([("Hem","/"),("Integritetspolicy","/integritetspolicy/")])]
    body = f'''
{nav_html("/")}
{crumbs_html([("Hem","/"),("Integritetspolicy",None)])}
<main id="main">
<section class="page-hero"><div class="wrap"><h1>Integritetspolicy</h1><p>Vi värnar om din integritet. Här beskriver vi hur vi behandlar dina personuppgifter.</p></div></section>
<section><div class="wrap prose">
  <h2>Personuppgiftsansvarig</h2>
  <p>{LEGAL}, {NAME}, {STREET}, {ZIP} {CITY}, org.nr {ORGNR}, är personuppgiftsansvarig för de uppgifter som samlas in via denna webbplats.</p>
  <h2>Vilka uppgifter samlar vi in?</h2>
  <ul>
    <li>De uppgifter du själv lämnar i vårt kontaktformulär: namn, telefon, e-post och ditt meddelande.</li>
    <li>Teknisk information som kan loggas av din webbläsare eller vår hostingleverantör.</li>
  </ul>
  <h2>Varför behandlar vi uppgifterna?</h2>
  <p>Vi använder uppgifterna enbart för att kunna svara på din förfrågan, lämna en offert och utföra den tjänst du beställer. Rättslig grund är fullgörande av avtal och berättigat intresse.</p>
  <h2>Hur länge sparas uppgifterna?</h2>
  <p>Vi sparar dina uppgifter så länge det behövs för att hantera ditt ärende och uppfylla bokförings- och skattelagstiftningens krav, därefter raderas de.</p>
  <h2>Dina rättigheter</h2>
  <p>Du har rätt att få information om vilka uppgifter vi behandlar, begära rättelse eller radering, invända mot behandlingen och begära dataportabilitet. Kontakta oss på <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>Cookies</h2>
  <p>Denna webbplats använder inga spårningscookies. Inga uppgifter delas med tredje part för marknadsföring.</p>
</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/integritetspolicy/", ld) + body + end()

def page_404():
    title = "Sidan hittades inte | A.Z & Kund i Fokus"
    desc  = "Sidan du letade efter finns inte. Gå tillbaka till startsidan eller kontakta A.Z & Kund i Fokus."
    body = f'''
{nav_html("/")}
<main id="main">
<section class="page-hero"><div class="wrap center" style="padding:60px 0">
  <h1>Hoppsan — sidan finns inte</h1>
  <p>Sidan du letade efter har flyttat eller aldrig funnits. Låt oss hjälpa dig vidare.</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="/">Till startsidan</a><a class="btn btn-ghost" href="/kontakt/">Kontakta oss</a></div>
</div></section>
</main>
{FOOTER}
'''
    return head(title, desc, "/404", og_type="website") + body + end()

# ---------- ROBOTS / SITEMAP / LLMS ----------
def write_robots():
    open(os.path.join(ROOT,"robots.txt"),"w").write(
f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
""")

def write_sitemap(pages):
    today = datetime.date.today().isoformat()
    urls=""
    for slug, prio in pages:
        loc = SITE_URL + (slug if slug!="/" else "/")
        urls += (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n'
                 f'    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>\n')
    open(os.path.join(ROOT,"sitemap.xml"),"w").write(
f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
""")

def write_llms():
    open(os.path.join(ROOT,"llms.txt"),"w",encoding="utf-8").write(f"""# {NAME}

> Lokal städfirma i Fengersfors (Dalsland) som erbjuder hemstädning, flyttstädning, kontorsstädning, städning av fritidshus/Airbnb samt stor- och byggstädning. RUT-avdrag. Verksam i Dalsland och västra Värmland.

## Tjänster
- [Hemstädning]({SITE_URL}/tjanster/hemstadning/): återkommande städning av hemmet.
- [Flyttstädning]({SITE_URL}/tjanster/flyttstadning/): godkänd flyttstäd inför besiktning.
- [Kontorsstädning]({SITE_URL}/tjanster/kontorsstadning/): lokalvård för företag.
- [Fritidshus & Airbnb]({SITE_URL}/tjanster/fritidshus-airbnb/): nyckelfärdig stugstädning mellan gäster.
- [Stor- & byggstädning]({SITE_URL}/tjanster/byggstad-storstadning/): heldagsuppdrag inför inflytt.

## Information
- [Priser]({SITE_URL}/priser/): priser efter RUT-avdrag.
- [Områden]({SITE_URL}/omraden/): Fengersfors, Åmål, Bengtsfors, Säffle, Mellerud, Dals-Ed.
- [Om oss]({SITE_URL}/om-oss/)
- [Vanliga frågor]({SITE_URL}/faq/)
- [Kontakt]({SITE_URL}/kontakt/): {PHONE} · {EMAIL} · {STREET}, {ZIP} {CITY}
- Instagram: {INSTAGRAM} ({IG_HANDLE})

## Företag
- Juridiskt namn: {LEGAL}
- Org.nr: {ORGNR}
- Grundat: {FOUNDED}
- Område: Dalsland & västra Värmland, Sverige
""")

# ─────────────────────────── MAIN ───────────────────────────
def main():
    print("Bygger A.Z & Kund i Fokus …")
    write_page("/", page_index())
    write_page("/tjanster/", page_tjanster())
    write_page("/tjanster/hemstadning/", service_page(
        "hemstadning","Hemstädning","home",
        "Hemstädning i Dalsland – återkommande städning | A.Z & Kund i Fokus",
        "Återkommande hemstädning i Fengersfors, Åmål och Bengtsfors. Vecka eller varannan vecka, alltid med samma kvalitet. Pris efter RUT-avdrag.",
        "Återkommande hemstädning som gör vardagen lättare — veckovis eller varannan vecka, precis som du vill.",
        ["Dammtorkning av alla ytor och möbler","Dammsugning och moppning av golv","Kök: bänkar, spis, fläkt och diskbänk","Badrum: dusch, toalett, handfat och kakel","Sängbäddning och allmän ordning","Fönsterputs vid behov — säg till innan"],
        [("Hemstädning — per timme","380 kr"),("Hemstädning — efter RUT","ca 190 kr"),("Återkommande avtal","rabatt per tillfälle")],
        [("Hur ofta kan jag få städning?","De vanligaste uppläggen är varje vecka eller varannan vecka. Du väljer helt själv — vi anpassar oss efter ditt behov."),
         ("Tar ni med produkter?","Ja, vi tar med egna produkter och redskap utan extra kostnad. Vill du hellre att vi använder dina egna går det bra.")]))
    write_page("/tjanster/flyttstadning/", service_page(
        "flyttstadning","Flyttstädning","truck",
        "Flyttstädning i Dalsland – godkänd inför besiktning | A.Z & Kund i Fokus",
        "Flyttstädning i Fengersfors, Åmål och Dalsland som klarar besiktningen. Fast pris efter RUT-avdrag och nöjd-kund-garanti.",
        "Flyttstädning som klarar besiktningen — så att du får tillbaka depositionen och kan lämna över med gott samvete.",
        ["Fullständig städning av hela bostaden","Ugn, kylskåp och köksskåp invändigt","Badrum avkalkat och skinande","Fönster, karmar och fönsterbleck","Garderober, golv och lister","Vi stämmer av mot mäklarens checklista"],
        [("Flyttstädning upp till 60 m² (efter RUT)","från 1 495 kr"),("Flyttstädning större bostad","offert"),("Fönsterputs ingår","ja")],
        [("Vad ingår i en flyttstädning?","En flyttstädning är mer grundlig än vanlig hemstädning. Vi städar hela bostaden inklusive invändigt i ugn, kyl och skåp samt fönster och karmar."),
         ("Får jag flyttstädningen godkänd?","Vi stämmer av mot den checklista som används vid besiktning och gör om något inte godkänns. Nöjd-kund-garanti gäller.")]))
    write_page("/tjanster/kontorsstadning/", service_page(
        "kontorsstadning","Kontorsstädning","office",
        "Kontorsstädning & lokalvård i Dalsland | A.Z & Kund i Fokus",
        "Kontorsstädning och lokalvård för företag i Bengtsfors, Åmål och Dalsland. Fast schema, tydlig fakturering och nöjda medarbetare.",
        "Lokalvård som håller kontoret fräscht och personalen nöjd — med fast schema och en faktura i månaden.",
        ["Daglig eller veckovis städning av kontor","Toaletter, kök och personalutrymmen","Papperskorgar och återvinning","Golvvård och moppning","Fönsterputs och storstäd vid behov","Anpassat schema efter era öppettider"],
        [("Kontorsstädning — per timme (exkl. moms)","304 kr"),("Återkommande avtal","skräddarsytt"),("Offert","kostnadsfri")],
        [("Städar ni utanför kontorstid?","Ja, vi anpassar oss efter era öppettider och kan städa tidig morgon eller kväll så att vi inte stör verksamheten."),
         ("Kan vi teckna avtal?","Ja, vi erbjuder återkommande avtal med fast schema och månadsfakturering. Kontakta oss för offert.")]))
    write_page("/tjanster/fritidshus-airbnb/", service_page(
        "fritidshus-airbnb","Fritidshus & Airbnb","house",
        "Städning av fritidshus & Airbnb i Dalsland | A.Z & Kund i Fokus",
        "Nyckelfärdig städning av stugor och fritidshus mellan gäster i Dalsland. Påfyllning och soptömning ingår. Perfekt för Airbnb-värdar.",
        "Nyckelfärdig städning av din stuga mellan gäster — så att varje gäst möts av ett fräscht hem och får toppbetyg.",
        ["Städning mellan gäster, alltid samma standard","Bäddning av sängar och fräscha handdukar","Badrum och kök grundligt rengjorda","Påfyllning av toalettpapper och förbrukningsvaror","Soptömning och koll av uteplats","Flexibla tider efter gästernas avresa"],
        [("Stugstädning / Airbnb — per tillfälle","offert"),("Påfyllning & soptömning","ingår"),("Återkommande värdavtal","rabatt")],
        [("Jobbar ni mellan gästerna?","Ja, det är precis det vi gör. Vi kommer efter gästernas avresa och gör stugan redo för nästa bokning, även med kort varsel."),
         ("Kan ni fylla på toalettpapper och tömma sopor?","Ja, nyckelfärdig service ingår: vi fyller på förbrukningsvaror, tömmer sopor och ser till att allt är klart för nästa gäst.")]))
    write_page("/tjanster/byggstad-storstadning/", service_page(
        "byggstad-storstadning","Stor- & byggstädning","tools",
        "Storstädning & byggstädning i Dalsland | A.Z & Kund i Fokus",
        "Storstädning och byggstädning inför inflytt eller efter renovering i Dalsland. Heldagsuppdrag i Säffle, Mellerud och Dals-Ed.",
        "Stor- och byggstädning inför inflytt eller efter renovering — ett heldagsuppdrag som gör att du kan flytta in i ett skinande hem.",
        ["Grovstädning efter bygge eller renovering","Borttagning av damm, färg- och bruksrester","Fönster, karmar och fönsterbleck","Golv och lister, hela bostaden","Ugn, kyl och skåp invändigt","Kan kombineras med flyttstädning"],
        [("Storstädning — per timme","380 kr"),("Byggstädning — heldagsuppdrag","offert"),("Kombination flytt + storstäd","offert")],
        [("Tar ni uppdrag längre bort?","Ja, för heldagsuppdrag som stor- och byggstädning åker vi gärna till Säffle, Mellerud och Dals-Ed. Hör av dig för offert."),
         ("Hur lång tid tar en byggstädning?","Det beror på yta och hur mycket byggdamm som finns. Vi tittar på objektet och ger ett fast pris på ett heldags- eller flerdagarsuppdrag.")]))
    write_page("/priser/", page_priser())
    write_page("/omraden/", page_omraden())
    write_page("/om-oss/", page_omoss())
    write_page("/kontakt/", page_kontakt())
    write_page("/faq/", page_faq())
    write_page("/integritetspolicy/", page_privacy())
    # 404 som egen fil (inte katalog)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(rebase(page_404()))
    print("  ✓ /404.html")
    write_robots()
    write_sitemap([("/", "1.0"),("/tjanster/","0.9"),("/priser/","0.9"),("/omraden/","0.8"),
                   ("/om-oss/","0.7"),("/faq/","0.7"),("/kontakt/","0.9"),
                   ("/tjanster/hemstadning/","0.8"),("/tjanster/flyttstadning/","0.8"),
                   ("/tjanster/kontorsstadning/","0.7"),("/tjanster/fritidshus-airbnb/","0.8"),
                   ("/tjanster/byggstad-storstadning/","0.7"),("/integritetspolicy/","0.3")])
    write_llms()
    print("Klart.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generator for The Corner Bakery Pasteleria & Market demo site (RGWebD).
Run from repo root:  python3 generator/build.py  [--base https://.../]
Writes static HTML into the repo root and copies CSS/JS into assets/."""
import json, os, shutil, sys, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, 'generator')
BASE = 'https://rgwebd.github.io/cornerbakery-annapolis/'
if '--base' in sys.argv: BASE = sys.argv[sys.argv.index('--base')+1]
VER = '5'

B = dict(
  name='The Corner Bakery Pasteleria & Market', short='The Corner Bakery',
  street='2140 Forest Dr', city='Annapolis', region='MD', zip='21401', plaza='Colonial Parole Center',
  phone='(443) 949-0309', tel='+14439490309', email='bakerygalleria@icloud.com',
  lat=38.9779628, lng=-76.536517,
  gmaps='https://maps.app.goo.gl/AZ5bBaq454hQ3mcL6',
  gplace='https://www.google.com/maps/place/The+Corner+Bakery+Pasteleria+%26+Market/@38.9779628,-76.536517,16z/data=!4m6!3m5!1s0x89b7f6c5efd0cb41:0xc60131baa17e5c86!8m2!3d38.9779628!4d-76.536517!16s%2Fg%2F11f4m7khv6',
  fb='https://www.facebook.com/TheCornerBakeryCafePasteleria/',
  dirs='https://www.google.com/maps/dir/?api=1&destination=The+Corner+Bakery+Pasteleria+%26+Market%2C+2140+Forest+Dr%2C+Annapolis%2C+MD+21401',
)
HOURS = [('Monday','7 AM – 9 PM',1),('Tuesday','7 AM – 9 PM',2),('Wednesday','7 AM – 9 PM',3),('Thursday','7 AM – 9 PM',4),('Friday','7 AM – 9 PM',5),('Saturday','6 AM – 9 PM',6),('Sunday','6 AM – 8 PM',0)]

REVIEWS = [
 ('Adriana F','Local Guide · Google','Best bakery around. This location always hits close to home every-time my father was from Mexico.. the bread is always sweet, fresh and soft.. the girls up front are always respectful and sweet. Highly recommend.'),
 ('Andrew Crawford','Google review','This place is a gem. Best Flan in the state. Very unique baked goods and treats. Swing by and check it out. The smell of the bakery will let you know you are the right place!'),
 ('jeffey martinez','Google review','This bakery did a great job making a special requested design for a birthday. The staff listened to what I wanted and surpassed our expectation! I would highly recommend them. Will definitely be coming back again'),
 ('Monica Yupe','Google review','Absolutely stunning birthday cake! Not only was it beautifully decorated, it. tasted amazing too. We will definitely come back request more cakes :)'),
 ('Madeleine Sofia Sanchez','Google review','My brother ordered me a choco flan with rocher ferrero filling and it was so good 😊 All my guest really loved the taste of the cake as well. Thank you for this wonderful birthday cake.'),
 ('M F','Google review','I ordered a custom cake for my son’s 2nd birthday , it was better than expected and it was delicious. 100% recommend and will be ordering from here again.'),
]

# ---------- image helpers ----------
IMG = os.path.join(ROOT,'assets','img')
_sz = {}
def size(fn):
    if fn not in _sz: _sz[fn] = Image.open(os.path.join(IMG,fn)).size
    return _sz[fn]
def img(n, alt, cls='', lazy=True, sizes='(max-width:900px) 92vw, 50vw', hero=False):
    w,h = size(n+'.webp'); sw,_ = size(n+'-s.webp')
    a = f' class="{cls}"' if cls else ''
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return (f'<img src="assets/img/{n}-s.webp" srcset="assets/img/{n}-s.webp {sw}w, assets/img/{n}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}"{a}{ld}>')

# ---------- icons ----------
I = {
 'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 'cake':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8"/><path d="M4 16s.5-1 2-1 2.5 2 4 2 2.5-2 4-2 2.5 2 4 2 2-1 2-1"/><path d="M2 21h20M7 8v3M12 8v3M17 8v3M7 4h.01M12 4h.01M17 4h.01"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 'arrow':'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'left':'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>',
 'right':'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>',
 'x':'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
 'heart':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
 'bag':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/></svg>',
 'sun':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 'tray':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 15h18M5 15a7 7 0 0 1 14 0M12 6V4M2 19h20"/></svg>',
 'star':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
 'check':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
 'no':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m5.7 5.7 12.6 12.6"/></svg>',
 'card':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
 'access':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4" r="2"/><path d="M19 13v-2a7 7 0 0 0-5-1H9l-1 6h7l2 5"/><path d="M8.5 16a5 5 0 1 0 6.5 4.8"/></svg>',
 'mail':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'fb':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6c0-.9.6-1 1-1h2V1.5h-3C10.9 1.5 10 3.8 10 5.6V8H7.5v3.6H10V22h4V11.6h3l.5-3.6z"/></svg>',
 'cup':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1.5 13h-11zM4 8h16M12 3v5M9 3h6"/></svg>',
}
STARS = '★★★★★'

# ---------- papel picado ----------
PIC_COLORS = ['#e8708a','#f4b23c','#17877f','#e8711e','#fff5e4','#8f6bd6']
def flag(c, k):
    holes = ['<circle cx="27" cy="22" r="7"/><path d="M27 34l5 8h-10z"/><circle cx="12" cy="44" r="3"/><circle cx="42" cy="44" r="3"/>',
             '<path d="M27 14l8 10-8 10-8-10z"/><circle cx="13" cy="20" r="3"/><circle cx="41" cy="20" r="3"/><path d="M14 44h26v4H14z"/>',
             '<path d="M27 16c5 0 8 4 8 8s-3 6-8 12c-5-6-8-8-8-12s3-8 8-8z"/><circle cx="12" cy="46" r="3"/><circle cx="27" cy="48" r="3"/><circle cx="42" cy="46" r="3"/>']
    h = holes[k%3]
    return (f'<li><svg viewBox="0 0 54 62" aria-hidden="true"><defs><mask id="pm{k}"><rect width="54" height="62" fill="#fff"/>'
            f'<g fill="#000">{h}<path d="M0 62 6 54l6 8 6-8 6 8 6-8 6 8 6-8 6 8 6-8v8z"/></g></mask></defs>'
            f'<rect width="54" height="62" fill="{c}" mask="url(#pm{k})"/></svg></li>')
def picado(n=14, start=0):
    flags = ''.join(flag(PIC_COLORS[(i+start)%len(PIC_COLORS)], i+start) for i in range(n))
    return (f'<div class="picado" aria-hidden="true"><svg viewBox="0 0 100 20" preserveAspectRatio="none"><path d="M0 6 Q50 14 100 6" stroke="#f4b23c" stroke-width=".4" fill="none"/></svg><ul>{flags}</ul></div>')

# ---------- schema ----------
def org_schema():
    return {
      "@context":"https://schema.org","@type":"Bakery","@id":BASE+"#bakery","name":B['name'],
      "alternateName":["The Corner Bakery","The Corner Bakery Cafe Panaderia y Pastelería"],
      "url":BASE,"image":[BASE+"assets/og-image.jpg",BASE+"assets/img/g23.webp",BASE+"assets/img/g24.webp"],
      "logo":BASE+"assets/brand/logo-640.png","telephone":B['tel'],"email":B['email'],
      "address":{"@type":"PostalAddress","streetAddress":B['street'],"addressLocality":B['city'],"addressRegion":B['region'],"postalCode":B['zip'],"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":B['lat'],"longitude":B['lng']},
      "hasMap":B['gplace'],"sameAs":[B['fb'],B['gplace']],
      "servesCuisine":["Latin American","Bakery","Desserts"],
      "openingHoursSpecification":[
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"21:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"06:00","closes":"21:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"06:00","closes":"20:00"}],
      "paymentAccepted":"Credit card, debit card, NFC mobile payments",
      "amenityFeature":[{"@type":"LocationFeatureSpecification","name":n,"value":True} for n in ["Takeout","Dine-in","Wheelchair accessible parking lot"]],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":3.7,"reviewCount":108,"bestRating":5},
      "review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":5,"bestRating":5},"reviewBody":t,"publisher":{"@type":"Organization","name":"Google"}} for n,_,t in REVIEWS],
      "knowsAbout":["Pan dulce","Conchas","Custom cakes","Birthday cakes","Tres leches cake","Flan","Rolled ice cream","Piñatas"],
    }
def crumbs_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

# ---------- layout ----------
PAGES = [('index.html','Home','Inicio'),('menu.html','Panadería & Menu','Qué horneamos'),('cakes.html','Custom Cakes','Pasteles'),('reviews.html','Reviews','Opiniones'),('visit.html','Visit & FAQ','Visítanos')]
def head(title, desc, path, schemas, og_img='assets/og-image.jpg', base_href=''):
    url = BASE + ('' if path=='index.html' else path)
    sch = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    p = base_href
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#2a150b">
<meta property="og:type" content="website"><meta property="og:site_name" content="{B['name']}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{BASE}{og_img}">
<link rel="icon" href="{p}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{p}assets/brand/favicon-32.png"><link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,500..900,0..100,0..1&family=Jost:wght@400;500;600;700&family=Yellowtail&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/styles.css?v={VER}">{sch}</head>'''

def nav(cur, p=''):
    links = ''.join(f'<li><a href="{p}{u}"{" aria-current=\"page\"" if u==cur else ""}>{n}</a></li>' for u,n,_ in PAGES)
    dl = ''.join(f'<a class="dl" href="{p}{u}"{" aria-current=\"page\"" if u==cur else ""}>{n}<small>{s}</small></a>' for u,n,s in PAGES)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<div class="holiday" role="note" hidden><b>Thanksgiving week:</b> our flyer says we’re <i lang="es">¡abierto toda la noche!</i> on Thu, Nov 26 — holiday hours may differ, so <a href="tel:{B['tel']}">call {B['phone']}</a> to confirm. <button type="button" aria-label="Dismiss holiday notice" style="position:absolute;right:10px;top:50%;translate:0 -50%;background:none;border:0;color:inherit;font-size:1.2rem">×</button></div>
<header class="nav"><div class="wrap">
<a class="brand" href="{p}index.html" aria-label="{B['short']} home"><img src="{p}assets/brand/logo-160.webp" width="160" height="173" alt="The Corner Bakery logo"><span><b>The Corner Bakery</b><small>Pastelería &amp; Market</small></span></a>
<nav aria-label="Main"><ul class="menu">{links}</ul></nav>
<div class="nav-cta"><a class="btn ghost sm hide-m mag" href="tel:{B['tel']}">{I['phone']}{B['phone']}</a><a class="btn gold sm mag" href="{p}cakes.html#order">{I['cake']}Order a cake</a>
<button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span></button></div>
</div></header>
<div class="drawer" id="drawer" aria-hidden="true">{dl}<div class="row"><a class="btn gold" href="tel:{B['tel']}">{I['phone']}Call {B['phone']}</a><a class="btn light" href="{B['dirs']}" target="_blank" rel="noopener">{I['pin']}Directions</a></div></div>'''

def footer(p=''):
    hrs = ''.join(f'<span>{d[:3]}</span><span>{h}</span>' for d,h,_ in HOURS)
    links = ''.join(f'<li><a href="{p}{u}">{n}</a></li>' for u,n,_ in PAGES)
    return f'''<footer class="foot">{picado(16,2)}<div class="wrap foot-grid">
<div class="fl"><img src="{p}assets/brand/logo-320.webp" width="320" height="345" alt="The Corner Bakery – Pastelería &amp; Market logo" loading="lazy"><p><b>{B['name']}</b><br>A Latino-owned panadería, pastelería &amp; little market in Annapolis.</p></div>
<div><h4>Pages</h4><ul>{links}<li><a href="{p}llms.txt">llms.txt</a></li></ul></div>
<div><h4>Find us</h4><ul><li><a href="{B['dirs']}" target="_blank" rel="noopener">{B['street']}<br>{B['city']}, {B['region']} {B['zip']}</a></li><li>In the {B['plaza']}</li><li><a href="tel:{B['tel']}">{B['phone']}</a></li><li><a href="mailto:{B['email']}">{B['email']}</a></li><li><a href="{B['fb']}" target="_blank" rel="noopener">Facebook</a> · <a href="{B['gplace']}" target="_blank" rel="noopener">Google</a></li></ul></div>
<div><h4>Horario</h4><div class="fh">{hrs}</div><p style="margin-top:10px;font-size:.85rem;opacity:.7">Holiday hours may differ.</p></div>
</div><div class="wrap credit"><span>© <span data-year>2026</span> {B['name']}</span><span>Design preview by <a href="https://github.com/RGWebD" rel="noopener">RGWebD</a> · photos from the bakery’s Google Business Profile</span></div></footer>
<div class="mbar" aria-label="Quick actions"><a href="tel:{B['tel']}">{I['phone']}Call</a><a href="{B['dirs']}" target="_blank" rel="noopener">{I['pin']}Directions</a><a href="{p}cakes.html#order">{I['cake']}Cake order</a></div>
<div class="demo" role="note"><span>Design preview by <b>RGWebD</b></span><button type="button" aria-label="Dismiss design preview note">×</button></div>
<script src="{p}assets/script.js?v={VER}" defer></script></body></html>'''

def live_chip():
    return '<span class="chip live" aria-live="polite"><span class="dot"></span><span class="lt">Open daily · 6–7 AM to 8–9 PM</span></span>'

def phero(title_html, eyebrow, lead, crumbs, image, cta, giant, tall=False):
    cr = ' / '.join(f'<a href="{u}">{n}</a>' for n,u in crumbs[:-1]) + f' / <span aria-current="page">{crumbs[-1][0]}</span>'
    return f'''<section class="phero">{picado(14)}<div class="giant" aria-hidden="true">{giant}</div><div class="wrap phero-grid">
<div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><span class="eyebrow">{eyebrow}</span><h1 class="split" style="margin-top:14px">{title_html}</h1><p class="lead rv">{lead}</p><div class="ctas rv d1" style="display:flex;gap:12px;flex-wrap:wrap">{cta}</div></div>
<div class="frame{' tall' if tall else ''} rv">{image}</div></div></section>'''

def cta_band(p=''):
    return f'''<section class="sec cta-band"><div class="wrap cta-grid">
<div><span class="eyebrow" style="color:var(--choc)">Ven con hambre</span><h2 class="split" style="margin-top:14px">Come hungry. <span class="script">Leave with a box.</span></h2>
<div class="addr rv"><span>{B['street']} · {B['plaza']} · {B['city']}, {B['region']} {B['zip']}</span><span>Open 7 days · Mon–Fri 7 AM–9 PM · Sat 6 AM–9 PM · Sun 6 AM–8 PM</span><a href="tel:{B['tel']}">{B['phone']}</a></div>
<div class="rv d1" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn mag" href="tel:{B['tel']}">{I['phone']}Call the bakery</a><a class="btn light mag" href="{B['dirs']}" target="_blank" rel="noopener">{I['pin']}Get directions</a></div></div>
<div class="frame rv">{img('g23','The Corner Bakery storefront on Forest Drive with its Panaderia & Pasteleria sign')}</div></div></section>'''

def page(path, title, desc, body, schemas, p=''):
    out = head(title, desc, path, schemas, base_href=p) + '<body class="grain">' + nav(path, p) + f'<main id="main">{body}</main>' + footer(p)
    with open(os.path.join(ROOT, path), 'w') as f: f.write(out)

# =============== HOME ===============
def home():
    mq1 = ''.join(f'<span>{t}</span>' for t in ['Conchas','Tres leches','Flan','Custom cakes','Pan dulce','<i>Pasteles en vaso</i>','Rolled ice cream','Birria sandwiches','Piñatas']*2)
    mq2 = ''.join(f'<span>{t}</span>' for t in ['Panadería','<i>Pastelería</i>','Market','Cumpleaños','Quinceañeras','Piñatas','Bodas','<i>Recién horneado</i>']*2)
    sp = [('Conchas','The classic shell-topped sweet bun — vanilla, chocolate and pink.',15,12,0),
          ('Marquesote','Soft, golden sponge cake squares.',16,31,0),
          ('Besos','Two domes of cake sandwiched together — a “kiss.”',52,30,0),
          ('Semita de piña','A filled sweet bread with pineapple.',82,41,0),
          ('Quesadilla','Not the taco kind — a sweet, cheesy pan dulce.',19,61,1),
          ('María Luisa','Layered cake slices with jam.',52,57,1),
          ('Marranitos','Little piggy-shaped molasses cookies.',22,74,1),
          ('Orejas','Flaky, caramelized “ear” pastries.',23,87,1)]
    pins = ''.join(f'<button class="pin" type="button" style="left:{x}%;top:{y}%" aria-expanded="false" aria-controls="pop{i}" aria-label="{n}">{i+1}</button><div class="pop{" below" if y<35 else ""}" id="pop{i}" role="dialog" aria-label="{n}" hidden style="left:{min(max(x,18),82)}%;top:{y}%"><b>{n}</b>{d}</div>' for i,(n,d,x,y,_) in enumerate(sp))
    slides = ''.join(f'<div class="slide"><figure class="quote"><span class="qmark" aria-hidden="true">“</span><div class="stars" aria-label="5 out of 5 stars">{STARS}</div><blockquote>{html.escape(t)}</blockquote><figcaption><cite>{html.escape(n)}<small>{m}</small></cite></figcaption></figure></div>' for n,m,t in REVIEWS)
    sprink = ''.join(f'<i style="left:{(i*37)%100}%;top:{(i*53)%100}%;background:{PIC_COLORS[i%4]};rotate:{(i*47)%180}deg;animation-delay:-{i%7}s"></i>' for i in range(26))
    body = f'''
<div class="loader" aria-hidden="true"><div class="half t"></div><div class="half b"></div><div class="lc"><svg class="steam" viewBox="0 0 100 60"><path d="M30 58c-8-12 8-18 0-30s6-18 0-26"/><path d="M50 58c-8-12 8-18 0-30s6-18 0-26"/><path d="M70 58c-8-12 8-18 0-30s6-18 0-26"/></svg><img src="assets/brand/logo-320.webp" width="320" height="345" alt=""><p>Recién horneado…</p></div></div>
<section class="hero">{picado(16)}<div class="giant" aria-hidden="true">Panadería</div>
<div class="wrap hero-grid">
<div class="hero-copy"><span class="eyebrow" style="color:var(--gold)">Annapolis · Panadería &amp; Pastelería</span>
<h1 class="split" style="margin-top:18px">Pan dulce, pasteles <span class="script">&amp; a little fiesta</span> every day.</h1>
<p class="lead rv d2">A Latino-owned bakery &amp; market in the {B['plaza']} — a whole wall of fresh conchas and pan dulce, custom cakes for every celebration, rolled ice cream, and piñatas for the party.</p>
<div class="ctas rv d3"><a class="btn gold mag" href="tel:{B['tel']}">{I['phone']}Call {B['phone']}</a><a class="btn ghost light mag" href="cakes.html#order">{I['cake']}Plan a custom cake</a></div>
<div class="trust rv d3">{live_chip()}<span class="chip">{I['heart']}Latino-owned</span><span class="chip">{I['bag']}Takeout · Dine-in</span></div>
</div>
<div class="hero-art">
<div class="arch">{img('g24','Self-serve pan dulce wall and glass pastry cases inside The Corner Bakery',lazy=False,sizes='(max-width:900px) 92vw, 46vw')}</div>
<figure class="polaroid p1" data-speed=".12">{img('g31','Conchas and sweet breads on a plate',sizes='220px')}<figcaption>conchas ♥</figcaption></figure>
<figure class="polaroid p2" data-speed="-.1">{img('g07','Two-tier pink cake with white orchids',sizes='220px')}<figcaption>pasteles</figcaption></figure>
<div class="stamp-wrap" aria-hidden="true"><svg class="ring stamp" viewBox="0 0 150 150" style="position:absolute;inset:0;width:150px;height:150px"><defs><path id="cp" d="M75 75m-58 0a58 58 0 1 1 116 0a58 58 0 1 1-116 0"/></defs><circle cx="75" cy="75" r="74" fill="#f4b23c"/><text font-family="Jost" font-weight="700" font-size="12.5" letter-spacing="3.2" fill="#2a150b"><textPath href="#cp">HORNEADO FRESCO · ANNAPOLIS · MD · </textPath></text></svg><div class="logo"><img src="assets/brand/logo-160.webp" width="160" height="173" alt=""></div></div>
</div></div></section>
<div class="mqwrap"><div class="marquee" aria-hidden="true"><div class="mq">{mq1}</div></div>
<div class="marquee alt" aria-hidden="true"><div class="mq">{mq2}</div></div></div>

<section class="sec"><div class="bgword" aria-hidden="true">Dulce</div><div class="wrap">
<div class="sec-head"><span class="eyebrow">Tres maneras de antojarse</span><h2 class="split">Three ways to treat yourself</h2><p class="lead rv">Grab a tray for the pastry wall, order a cake for the big day, or cool off with ice cream rolled to order.</p></div>
<div class="trio">
<a class="card tilt rv" href="menu.html#panaderia">{img('g37','Self-serve tray and tongs with conchas',sizes='(max-width:900px) 92vw, 33vw')}<span class="arrow">{I['arrow']}</span><div class="ct"><span class="script">La Panadería</span><h3>The pan dulce wall</h3><p>Conchas, besos, orejas, marranitos and more — pick your own with a tray and tongs.</p></div></a>
<a class="card tilt rv d1" href="cakes.html">{img('g11','Two-tier lavender drip cake with butterflies',sizes='(max-width:900px) 92vw, 33vw')}<span class="arrow">{I['arrow']}</span><div class="ct"><span class="script">La Pastelería</span><h3>Cakes for every fiesta</h3><p>Birthdays, quinceañeras, engagements and weddings — tres leches, choco flan and custom designs.</p></div></a>
<a class="card tilt rv d2" href="menu.html#helados">{img('g36','Rolled ice cream topped with popping boba',sizes='(max-width:900px) 92vw, 33vw')}<span class="arrow">{I['arrow']}</span><div class="ct"><span class="script">Helados &amp; más</span><h3>Rolled ice cream &amp; treats</h3><p>Ice cream rolls, cakes in a cup, juices, breakfast and birria sandwiches.</p></div></a>
</div></div></section>

<section class="sec paper"><div class="wrap">
<div class="sec-head center"><span class="eyebrow">Escoge tu pan</span><h2 class="split">Pick your pan</h2><p class="lead rv" style="margin-inline:auto">Tap a number to meet a few favorites from the wall. Not sure what to try? Ask at the counter.</p></div>
<div class="spot-stage rv">{img('g38','Pan dulce wall with chalk labels for conchas, besos, marquesote, orejas and more',sizes='(max-width:1240px) 92vw, 1220px')}{pins}</div>
</div></section>

<section class="sec"><div class="wrap why">
<div><span class="eyebrow">¿Por qué nosotros?</span><h2 class="split" style="margin-top:14px">A corner of home, <span class="script">right on Forest Drive</span></h2>
<ul>
<li class="rv"><span class="ic">{I['tray']}</span><div><b>A wall of pick-and-choose pastries</b>Grab a tray and tongs and build your own box of pan dulce.</div></li>
<li class="rv d1"><span class="ic">{I['cake']}</span><div><b>Cakes made to your idea</b>Bring a theme, a photo or just a feeling — the team designs it with you.</div></li>
<li class="rv d2"><span class="ic">{I['sun']}</span><div><b>Open early, seven days</b>Doors open at 7 AM on weekdays and 6 AM on weekends.</div></li>
<li class="rv d3"><span class="ic">{I['heart']}</span><div><b>Latino-owned, family flavors</b>Panadería and pastelería classics, plus a little market of party favorites.</div></li>
</ul></div>
<div class="collage"><figure class="c1" data-speed=".06">{img('g10','Glass display case full of decorated cakes',sizes='(max-width:900px) 52vw, 30vw')}</figure><figure class="c2" data-speed="-.08">{img('g02','Fruit-topped drip cake in the display case',sizes='(max-width:900px) 44vw, 24vw')}</figure><figure class="c3" data-speed=".1">{img('g27','Market aisle with piñatas hanging from the ceiling',sizes='(max-width:900px) 46vw, 26vw')}</figure><div class="sticker" aria-hidden="true">¡Hecho<br>aquí!</div></div>
</div></section>

<section class="sec dark stat-sec"><div class="bgword" aria-hidden="true">Horno</div><div class="wrap">
<div class="sec-head"><span class="eyebrow">Los números</span><h2 class="split">Baking around the clock — almost.</h2></div>
<div class="stats">
<div class="stat rv"><div class="num"><span data-to="7">7</span></div><p>days a week, every week</p></div>
<div class="stat rv d1"><div class="num"><span data-to="99">99</span></div><p>hours open each week</p></div>
<div class="stat rv d2"><div class="num"><span data-to="6">6</span><small>AM</small></div><p>weekend doors open</p></div>
<div class="stat rv d3"><div class="num"><span data-to="62">62</span></div><p>five-star reviews on Google</p></div>
</div></div></section>

<section class="sec cakeband"><div class="sprinkles" aria-hidden="true">{sprink}</div><div class="wrap cake-grid">
<div class="cake-stack">
<figure class="k1" data-speed=".08">{img('g12','Blue two-tier under-the-sea cake',sizes='(max-width:900px) 44vw, 22vw')}<figcaption>bajo el mar</figcaption></figure>
<figure class="k2" data-speed="-.05">{img('g30','Red and gold three-tier quinceañera cake with roses and a crown',sizes='(max-width:900px) 46vw, 22vw')}<figcaption>quince años</figcaption></figure>
<figure class="k3" data-speed=".12">{img('g28','Heart-shaped anime character cake with pastel piping',sizes='(max-width:900px) 44vw, 20vw')}<figcaption>con cariño</figcaption></figure>
<figure class="k4" data-speed="-.1">{img('g45','Heart cake reading I love you para mi amor',sizes='(max-width:900px) 38vw, 18vw')}<figcaption>para mi amor</figcaption></figure>
</div>
<div><span class="eyebrow">Pasteles para cada fiesta</span><h2 class="split" style="margin-top:14px">Your idea, <span class="script">baked beautifully.</span></h2>
<p class="lead rv">From a tres leches layer cake to a choco flan with Ferrero Rocher filling, customers come back for cakes that look the part and taste even better.</p>
<div class="occasions rv"><span>Cumpleaños</span><span>Quinceañeras</span><span>Engagements</span><span>Bodas</span><span>Kids’ themes</span><span>Just because</span></div>
<div class="rv d1" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn mag" href="cakes.html#order">{I['cake']}Start a cake request</a><a class="btn ghost mag" href="cakes.html#gallery">See the cake gallery</a></div></div>
</div></section>

<section class="sec reviews"><div class="wrap">
<div class="sec-head center"><span class="eyebrow" style="color:var(--gold)">Lo que dicen</span><h2 class="split">Sweet words from regulars</h2></div>
<div class="carousel rv" aria-roledescription="carousel" aria-label="Customer reviews"><div style="overflow:hidden"><div class="track">{slides}</div></div>
<div class="car-ctrl"><button class="arr prev" type="button" aria-label="Previous review">{I['left']}</button><div class="dots"></div><button class="arr next" type="button" aria-label="Next review">{I['right']}</button></div></div>
<p style="text-align:center;margin-top:26px"><a class="btn light sm" href="reviews.html">Read more reviews {I['arrow']}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Explora</span><h2 class="split">Plan your visit</h2></div>
<div class="teasers">
<a class="teaser rv" href="menu.html">{img('g21','Rack of packaged cookies and pastries',sizes='(max-width:600px) 92vw, (max-width:1100px) 46vw, 25vw')}<div><span class="script">Qué horneamos</span><h3>Panadería &amp; menu</h3></div></a>
<a class="teaser rv d1" href="cakes.html">{img('g04','Wedding cake display table with draped backdrop',sizes='(max-width:600px) 92vw, (max-width:1100px) 46vw, 25vw')}<div><span class="script">Pasteles</span><h3>Custom cakes</h3></div></a>
<a class="teaser rv d2" href="reviews.html">{img('g14','White cake with purple piping and roses',sizes='(max-width:600px) 92vw, (max-width:1100px) 46vw, 25vw')}<div><span class="script">Opiniones</span><h3>Reviews</h3></div></a>
<a class="teaser rv d3" href="visit.html">{img('g44','Bright bakery interior with long display counter',sizes='(max-width:600px) 92vw, (max-width:1100px) 46vw, 25vw')}<div><span class="script">Visítanos</span><h3>Hours, map &amp; FAQ</h3></div></a>
</div></div></section>
{cta_band()}'''
    page('index.html', 'The Corner Bakery Pastelería & Market | Latino Bakery in Annapolis, MD',
         'Latino-owned panadería & pastelería in Annapolis, MD: conchas and pan dulce, custom birthday & quinceañera cakes, tres leches, flan, rolled ice cream and piñatas. 2140 Forest Dr · (443) 949-0309.',
         body, [org_schema(), {"@context":"https://schema.org","@type":"WebSite","name":B['name'],"url":BASE}])

# =============== MENU ===============
def menu():
    tl = f'''<div class="timeline"><svg class="tl" aria-hidden="true"><path class="base" stroke="rgba(69,35,15,.15)" stroke-width="4" fill="none"/><path class="draw" stroke="#e8711e" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
<div class="step rv"><span class="n">1</span><h3>Grab a tray &amp; tongs</h3><p>They’re waiting by the pastry wall.</p></div>
<div class="step rv"><span class="n">2</span><h3>Pick what looks good</h3><p>Every bin is labeled — conchas, besos, orejas, marranitos, semitas and more.</p></div>
<div class="step rv"><span class="n">3</span><h3>Bring it to the counter</h3><p>Add a slice of tres leches, a flan or a juice, pay by card or phone, and you’re set.</p></div></div>'''
    feats = [
     ('panaderia','01','La Panadería','Pan dulce, every day','Mexican and Latin American sweet breads stacked high on a self-serve wall — the kind of place one reviewer called “finally a good place for pan dulce in Annapolis.”',['Conchas','Besos','Orejas','Marranitos','Semita de piña','Marquesote','Quesadilla','Pan integral'], 'g31','Conchas and sweet breads on a plate','g24','Pastry wall and glass cases',''),
     ('pasteleria','02','La Pastelería','Tres leches, flan &amp; cakes by the slice','Grab a slice of tres leches or a flan from the case, or a whole decorated cake for tonight. Reviewers rave about the flan and the tres leches layered cake.',['Tres leches','Flan','Choco flan','Milhojas','Whole decorated cakes'],'g40','Slice of tres leches topped with cinnamon and a cherry','g05','Refrigerated case of decorated cakes','Custom cakes have their own page — <a href="cakes.html">see Pasteles →</a>'),
     ('vaso','03','Pasteles en vaso','Cakes in a cup','Layers of cake, cream and fruit in a grab-and-go cup, chilled in the cooler by the counter. A Facebook fan asked, “Where can you pick up the best Tres Leches Cake in a cup?” — this is the place.',['Tres leches in a cup','Strawberry cups','Grab &amp; go'],'g08','Strawberry-topped cakes in cups in the cooler','g02','Fruit-topped drip cake',''),
     ('helados','04','Helados enrollados','Rolled ice cream, made to order','Ice cream is spread thin on an ice-cold plate, then scraped into rolls and topped — a treat that’s as fun to watch as it is to eat.',['Ice cream rolls','Fruit toppings','Popping boba'],'g49','Rolled ice cream being spread on the cold plate','g36','Rolled ice cream with popping boba',''),
     ('mercado','05','El Mercado','A little market &amp; piñatas','Party supplies and Latin American pantry favorites under a ceiling full of colorful piñatas — pick one up with the cake.',['Piñatas','Snacks &amp; drinks','Party favorites'],'g27','Market aisle with piñatas hanging from the ceiling','g44','Bakery interior and counter',''),
    ]
    fs = ''
    for k,(id_,n,es,h,p_,tags,a,aa,b,ba,note) in enumerate(feats):
        fs += f'''<article class="feature{' flip' if k%2 else ''}" id="{id_}"><div class="fimg rv"><div class="main">{img(a,aa)}</div><div class="sub" data-speed=".06">{img(b,ba,sizes='240px')}</div></div>
<div class="rv d1"><div class="num" aria-hidden="true">{n}</div><span class="script">{es}</span><h2 style="font-size:clamp(2rem,3.6vw,3rem);margin:6px 0 14px">{h}</h2><p>{p_}</p><div class="tags">{''.join(f'<span>{t}</span>' for t in tags)}</div>{f'<p class="note">{note}</p>' if note else ''}</div></article>'''
    body = phero('What we bake <span class="script">&amp; more</span>','Qué horneamos','Pan dulce, pastries, cakes by the slice, rolled ice cream, juices, breakfast and a little market — all under one roof on Forest Drive.',[('Home','index.html'),('Panadería & Menu','menu.html')],img('g38','Labeled pan dulce wall',lazy=False),f'<a class="btn gold mag" href="tel:{B["tel"]}">{I["phone"]}Call for today’s selection</a><a class="btn ghost light mag" href="#panaderia">Browse the menu</a>','Panadería') + f'''
<div class="mqwrap"><div class="marquee" aria-hidden="true"><div class="mq">{''.join(f'<span>{t}</span>' for t in ['Conchas','Orejas','Besos','Tres leches','Flan','<i>Milhojas</i>','Birria','Jugos','Huevos']*2)}</div></div></div>
<section class="sec"><div class="wrap">{fs}</div></section>
<section class="sec paper"><div class="wrap"><div class="sec-head"><span class="eyebrow">Desayuno, almuerzo &amp; bebidas</span><h2 class="split">Breakfast, sandwiches &amp; drinks</h2><p class="lead rv">Beyond the bakery case, the shop’s Facebook page features a rotating lineup of savory plates and drinks.</p></div>
<div class="textcards">
<div class="tcard rv"><span class="script">Desayuno</span><h3>Breakfast plates</h3><p>Egg dishes (<i lang="es">huevos</i>) for an early start — doors open at 7 AM weekdays and 6 AM weekends.</p></div>
<div class="tcard rv d1"><span class="script">Fresco y natural</span><h3>Birria sandwiches</h3><p>Slow-cooked birria on fresh bread, as featured on the bakery’s Facebook page.</p></div>
<div class="tcard rv"><span class="script">Jugos</span><h3>Juices &amp; drinks</h3><p>Fresh juices and cold drinks — watch Facebook for specials like the <b>99¢ juice</b> promo.</p></div>
<div class="tcard rv d1"><span class="script">Panes</span><h3>Baguettes &amp; savory breads</h3><p>Fresh baguettes and savory baked goods alongside the sweet stuff.</p></div>
</div><p class="note rv" style="max-width:720px;margin-top:26px">Selection changes day to day. For today’s menu and prices, <a href="tel:{B['tel']}">call {B['phone']}</a> or stop by.</p></div></section>
<section class="sec"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Cómo funciona</span><h2 class="split">How the pastry wall works</h2></div>{tl}</div></section>
{cta_band()}'''
    page('menu.html','Panadería & Menu — Pan Dulce, Tres Leches, Rolled Ice Cream | The Corner Bakery Annapolis',
         'Conchas and pan dulce from a self-serve wall, tres leches, flan, cakes in a cup, rolled ice cream, breakfast, birria sandwiches, juices and piñatas at The Corner Bakery in Annapolis, MD.',
         body,[org_schema(),crumbs_schema([('Home',''),('Panadería & Menu','menu.html')])])

# =============== CAKES ===============
def cakes():
    gal = [('g07','Two-tier pink cake with white orchids'),('g12','Under-the-sea two-tier cake'),('g11','Lavender drip cake with butterflies'),('g30','Red & gold quinceañera cake'),('g34','Race-track number cake'),('g03','Chocolate cake with strawberries'),('g28','Heart-shaped character cake'),('g13','Tiered wedding cake with fountain'),('g29','Flame-piped birthday cake'),('g33','Jungle-themed two-tier cake'),('g18','Photo cake with blue rosettes'),('g16','Gift-box cake for Mom'),('g25','Purple wedding cake display'),('g45','“I love you para mi amor” heart cake'),('g14','White cake with purple roses')]
    gi = ''.join(f'<button class="gi" type="button" data-full="assets/img/{n}.webp">{img(n,a,sizes="340px")}<span>{a}</span></button>' for n,a in gal)
    tl = f'''<div class="timeline"><svg class="tl" aria-hidden="true"><path class="base" stroke="rgba(255,245,228,.15)" stroke-width="4" fill="none"/><path class="draw" stroke="#f4b23c" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
<div class="step rv"><span class="n">1</span><h3>Share your idea</h3><p>Call {B['phone']} or email a photo, theme or color palette to <a href="mailto:{B['email']}">{B['email']}</a>.</p></div>
<div class="step rv"><span class="n">2</span><h3>Pick flavor &amp; size</h3><p>Tell us how many guests and what you love — tres leches layers, choco flan, fruit, chocolate. The team will talk you through options and pricing.</p></div>
<div class="step rv"><span class="n">3</span><h3>We bake &amp; decorate</h3><p>“The staff listened to what I wanted and surpassed our expectation!” — jeffey m.</p></div>
<div class="step rv"><span class="n">4</span><h3>Pick up &amp; celebrate</h3><p>Pick your cake up at the shop on Forest Drive (the bakery doesn’t deliver) — grab a piñata while you’re here.</p></div></div>'''
    occ = ['Cumpleaños','Quinceañeras','Engagements','Bodas','Kids’ themes','Para mi amor','Holidays']
    body = phero('Pasteles <span class="script">for every fiesta</span>','Custom cakes','Birthday cakes, quinceañera tiers, themed kids’ cakes and wedding cakes — designed around your idea and baked in Annapolis.',[('Home','index.html'),('Custom Cakes','cakes.html')],img('g04','Wedding cake table with tiered cakes and draped backdrop',lazy=False),f'<a class="btn gold mag" href="#order">{I["cake"]}Start a cake request</a><a class="btn ghost light mag" href="tel:{B["tel"]}">{I["phone"]}{B["phone"]}</a>','Pasteles') + f'''
<section class="sec" id="gallery"><div class="wrap gal-head"><div><span class="eyebrow">Galería</span><h2 class="split" style="margin-top:12px">Cakes from the bakery</h2><p class="rv muted">Drag, swipe or use the arrows · tap a cake to enlarge</p></div><div class="gal-btns"><button class="gal-prev" type="button" aria-label="Scroll gallery left">{I['left']}</button><button class="gal-next" type="button" aria-label="Scroll gallery right">{I['right']}</button></div></div>
<div class="gallery" role="list" aria-label="Cake gallery">{gi}</div></section>
<div class="cbx" role="dialog" aria-modal="true" aria-label="Cake photo viewer" aria-hidden="true"><button class="cbx-x" type="button" aria-label="Close">{I['x']}</button><button class="cbx-p" type="button" aria-label="Previous photo">{I['left']}</button><img alt=""><button class="cbx-n" type="button" aria-label="Next photo">{I['right']}</button><p class="cbx-cap"></p></div>
<section class="sec paper"><div class="wrap why">
<div><span class="eyebrow">Para cada ocasión</span><h2 class="split" style="margin-top:14px">Every kind of celebration</h2><p class="lead rv" style="margin-top:16px">One family ordered a tres leches Barbie cake last-minute for a daughter’s party; another planned an engagement cake and then their wedding cake. Whatever you’re celebrating, start with a call.</p>
<div class="occasions rv">{''.join(f'<span>{o}</span>' for o in occ)}</div>
<p class="rv">Specialties customers mention: <b>tres leches layered cakes</b>, <b>choco flan</b> (one with Ferrero Rocher filling!), fruit-topped cakes and fully custom themed designs.</p></div>
<div class="collage"><figure class="c1" data-speed=".06">{img('g33','Two-tier jungle cake at a party',sizes='(max-width:900px) 52vw, 30vw')}</figure><figure class="c2" data-speed="-.08">{img('g34','Number two race-track cake',sizes='(max-width:900px) 44vw, 24vw')}</figure><figure class="c3" data-speed=".1">{img('g10','Display case of cakes',sizes='(max-width:900px) 46vw, 26vw')}</figure><div class="sticker" aria-hidden="true">¡Feliz<br>día!</div></div>
</div></section>
<section class="sec dark"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Cómo pedir</span><h2 class="split">How custom cakes work</h2></div>{tl}</div></section>
<section class="sec" id="order"><div class="wrap order">
<div><span class="eyebrow">Pide tu pastel</span><h2 class="split" style="margin-top:14px">Start a <span class="script">cake request</span></h2><p class="lead rv" style="margin-top:16px">Fill this in and it opens a ready-to-send email to the bakery — attach an inspiration photo if you have one. Prefer to talk? Call <a href="tel:{B['tel']}">{B['phone']}</a>.</p>
<p class="note rv">Order timing and pricing depend on the design — the bakery will confirm both with you. Cakes are picked up at the shop.</p></div>
<form class="form rv" id="cake-form">
<label>Your name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Date needed<input name="date" type="date" required></label>
<label>Occasion<select name="occasion"><option>Birthday</option><option>Quinceañera</option><option>Engagement</option><option>Wedding</option><option>Other</option></select></label>
<label>Guests / size<input name="size" placeholder="e.g. about 30 people"></label>
<label>Flavor ideas<input name="flavor" placeholder="e.g. tres leches, choco flan"></label>
<label class="full">Design notes<textarea name="notes" placeholder="Theme, colors, characters, writing on the cake…"></textarea><small>Opens your email app addressed to {B['email']}. Nothing is sent until you hit send.</small></label>
<div class="full"><button class="btn mag" type="submit">{I['mail']}Write my cake email</button></div>
</form></div></section>
{cta_band()}'''
    faq = {"@context":"https://schema.org","@type":"Service","serviceType":"Custom cakes","provider":{"@id":BASE+"#bakery"},"areaServed":"Annapolis, MD","description":"Custom birthday, quinceañera, engagement and wedding cakes, including tres leches and choco flan, picked up at the bakery."}
    page('cakes.html','Custom Cakes in Annapolis — Birthday, Quinceañera & Wedding | The Corner Bakery',
         'Custom birthday, quinceañera and wedding cakes from The Corner Bakery Pastelería in Annapolis, MD — tres leches, choco flan and themed designs. Call (443) 949-0309.',
         body,[org_schema(),faq,crumbs_schema([('Home',''),('Custom Cakes','cakes.html')])])

# =============== REVIEWS ===============
def reviews():
    cards = ''.join(f'<article class="rcard rv"><div class="stars" aria-label="5 out of 5 stars">{STARS}</div><blockquote>{html.escape(t)}</blockquote><cite>{html.escape(n)}<small>{m}</small></cite></article>' for n,m,t in REVIEWS)
    body = phero('Lo que <span class="script">dicen</span>','Reviews','Word-for-word reviews from customers on Google — about the flan, the pan dulce and the cakes that made the party.',[('Home','index.html'),('Reviews','reviews.html')],img('g03','Chocolate cake topped with strawberries',lazy=False),f'<a class="btn gold mag" href="{B["gplace"]}" target="_blank" rel="noopener">Read all reviews on Google</a>','Opiniones',tall=True) + f'''
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">De Google</span><h2 class="split">Five-star favorites</h2></div><div class="rgrid">{cards}</div></div></section>
<section class="sec dark"><div class="wrap"><div class="sec-head"><span class="eyebrow">Lo que más mencionan</span><h2 class="split">What people keep coming back for</h2></div>
<div class="rtheme"><div class="rv"><b>The flan</b>“Best Flan in the state.” — Andrew C.</div><div class="rv d1"><b>Custom cakes</b>“Better than expected and it was delicious.” — M F</div><div class="rv d2"><b>Pan dulce</b>“The bread is always sweet, fresh and soft.” — Adriana F.</div></div></div></section>
<section class="sec paper"><div class="wrap" style="text-align:center"><span class="eyebrow">¿Ya nos visitaste?</span><h2 class="split" style="margin:14px 0 20px">Tell us how it went</h2><p class="lead rv" style="margin:0 auto 26px">Reviews help neighbors find a good concha. Share yours on Google.</p><a class="btn mag rv" href="{B['gplace']}" target="_blank" rel="noopener">{I['star']}Review us on Google</a></div></section>
{cta_band()}'''
    page('reviews.html','Reviews — The Corner Bakery Pastelería & Market, Annapolis MD',
         'What customers say about The Corner Bakery in Annapolis: the best flan in the state, fresh soft pan dulce and custom birthday cakes that surpassed expectations.',
         body,[org_schema(),crumbs_schema([('Home',''),('Reviews','reviews.html')])])

# =============== VISIT ===============
FAQ = [
 ('What are your hours?','Monday through Friday 7 AM–9 PM, Saturday 6 AM–9 PM and Sunday 6 AM–8 PM. Holiday hours may differ — call (443) 949-0309 to confirm.'),
 ('Are you open on Thanksgiving?','The bakery’s Facebook flyer says it will be open all night on Thursday, November 26, 2026 (Thanksgiving). Google notes that hours on Thanksgiving and Black Friday might differ, so please call (443) 949-0309 before you go.'),
 ('Where are you located?','2140 Forest Dr, Annapolis, MD 21401, inside the Colonial Parole Center. There is a wheelchair-accessible parking lot.'),
 ('Do you deliver?','No — the bakery offers takeout and on-site dining, but not delivery.'),
 ('Can I order a custom cake?','Yes. Call (443) 949-0309 or email bakerygalleria@icloud.com with your date, guest count, flavor ideas and a photo or theme. Cakes are picked up at the shop.'),
 ('What forms of payment do you take?','Credit cards, debit cards and NFC mobile payments (tap to pay).'),
 ('What do you sell besides bread?','Custom and birthday cakes, tres leches, flan, cakes in a cup, rolled ice cream, juices, breakfast items, birria sandwiches, piñatas and market items.'),
 ('Is The Corner Bakery Latino-owned?','Yes — the business identifies as Latino-owned on its Google Business Profile.'),
]
def visit():
    rows = ''.join(f'<tr data-d="{d}"><td>{n}</td><td>{h}</td></tr>' for n,h,d in HOURS)
    fq = ''.join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)
    q = 'The+Corner+Bakery+Pasteleria+%26+Market,+2140+Forest+Dr,+Annapolis,+MD+21401'
    amen = [('check','bag','Takeout'),('check','tray','Dine-in'),('no','no','No delivery'),('check','access','Accessible parking lot'),('check','card','Cards &amp; tap to pay'),('check','heart','Latino-owned')]
    am = ''.join(f'<div class="rv{" no" if k=="no" else ""}">{I[i]}{t}</div>' for k,i,t in amen)
    body = phero('Visítanos <span class="script">on Forest Drive</span>','Visit &amp; FAQ',f'Find us in the {B["plaza"]} at {B["street"]}, {B["city"]}. Open seven days, from early morning to evening.',[('Home','index.html'),('Visit & FAQ','visit.html')],img('g23','Storefront of The Corner Bakery with Panaderia & Pasteleria sign',lazy=False),f'<a class="btn gold mag" href="{B["dirs"]}" target="_blank" rel="noopener">{I["pin"]}Get directions</a><a class="btn ghost light mag" href="tel:{B["tel"]}">{I["phone"]}{B["phone"]}</a>','Visítanos') + f'''
<section class="sec"><div class="wrap visit-grid">
<div class="panel rv"><h3>Horario <span class="script" style="font-size:1.1em">hours</span></h3>{live_chip().replace('class="chip live"','class="chip live" style="background:var(--choc);color:var(--cream);margin-bottom:14px"')}<table class="hours"><caption class="skip">Weekly hours</caption><tbody>{rows}</tbody></table>
<p class="note">Holiday hours may differ. Thanksgiving (Thu, Nov 26, 2026): the bakery’s Facebook flyer says <i lang="es">¡Abierto toda la noche!</i> — call to confirm.</p>
<h3 style="margin-top:28px">Contact</h3><p><a href="tel:{B['tel']}"><b>{B['phone']}</b></a><br><a href="mailto:{B['email']}">{B['email']}</a><br>{B['street']}, {B['city']}, {B['region']} {B['zip']}<br><a href="{B['fb']}" target="_blank" rel="noopener">Facebook</a> · <a href="{B['gplace']}" target="_blank" rel="noopener">Google Maps</a></p></div>
<div class="map rv d1"><iframe title="Map to The Corner Bakery, 2140 Forest Dr, Annapolis" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={q}&amp;output=embed"></iframe></div>
</div></section>
<section class="sec paper"><div class="wrap"><div class="sec-head"><span class="eyebrow">Bueno saber</span><h2 class="split">Good to know</h2></div><div class="amen">{am}</div>
<div class="duo" style="margin-top:40px"><figure class="rv">{img('g44','Long bakery counter and bright dining area')}<figcaption>Inside: the long pastry counter</figcaption></figure><figure class="rv d1">{img('g27','Market area with piñatas and snacks')}<figcaption>The market corner, piñatas overhead</figcaption></figure></div></div></section>
<section class="sec" id="faq"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Preguntas</span><h2 class="split">Frequently asked questions</h2></div><div class="faq">{fq}</div></div></section>
{cta_band()}'''
    fqs = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    page('visit.html','Visit, Hours & FAQ — The Corner Bakery, 2140 Forest Dr, Annapolis MD',
         'Hours, directions, map and FAQ for The Corner Bakery Pastelería & Market at 2140 Forest Dr in the Colonial Parole Center, Annapolis, MD. Open 7 days. (443) 949-0309.',
         body,[org_schema(),fqs,crumbs_schema([('Home',''),('Visit & FAQ','visit.html')])])

# =============== 404 + text files ===============
def notfound():
    p = '/cornerbakery-annapolis/'
    body = f'''<section class="phero">{picado(14)}<div class="wrap nf"><div><span class="script" style="font-size:3rem;color:var(--gold)">¡Ay, caramba!</span><h1 style="margin:10px 0 18px">This page got eaten.</h1><p class="lead" style="margin:0 auto 26px;color:rgba(255,245,228,.85)">Probably by someone who really loves conchas. Let’s get you back to the good stuff.</p><a class="btn gold" href="{p}index.html">Back to the bakery</a></div></div></section>'''
    out = head('Page not found | The Corner Bakery', 'This page could not be found.', '404.html', [], base_href=p).replace('<head>','<head><meta name="robots" content="noindex">',1) + '<body class="grain">' + nav('', p) + f'<main id="main">{body}</main>' + footer(p)
    open(os.path.join(ROOT,'404.html'),'w').write(out)

def textfiles():
    urls = ''.join(f'<url><loc>{BASE}{"" if u=="index.html" else u}</loc><changefreq>monthly</changefreq><priority>{"1.0" if u=="index.html" else "0.8"}</priority></url>' for u,_,_ in PAGES)
    open(os.path.join(ROOT,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nDisallow: /generator/\n\nSitemap: {BASE}sitemap.xml\n')
    hrs = '\n'.join(f'- {d}: {h}' for d,h,_ in HOURS)
    fq = '\n'.join(f'- Q: {q}\n  A: {a}' for q,a in FAQ)
    open(os.path.join(ROOT,'llms.txt'),'w').write(f'''# {B['name']}

> Latino-owned bakery (panadería & pastelería) and small market in Annapolis, Maryland. Known for pan dulce and conchas from a self-serve pastry wall, custom birthday / quinceañera / wedding cakes, tres leches, flan, cakes in a cup, rolled ice cream, juices, breakfast items, birria sandwiches and piñatas.

- Address: {B['street']}, {B['city']}, {B['region']} {B['zip']} (in the {B['plaza']})
- Phone: {B['phone']}
- Email: {B['email']}
- Facebook: {B['fb']}
- Google Maps: {B['gplace']}
- Service options: takeout, dine-in. No delivery.
- Payments: credit cards, debit cards, NFC mobile payments.
- Accessibility: wheelchair-accessible parking lot.
- Google rating: 3.7 from 108 reviews (as of November 2026).

## Hours (America/New_York)
{hrs}
- Holiday hours may differ. Thanksgiving, Thu Nov 26 2026: a bakery flyer says "open all night"; Google says hours might differ. Call to confirm.

## Pages
- [Home]({BASE}): overview, highlights, reviews
- [Panadería & Menu]({BASE}menu.html): pan dulce, pastries, tres leches, flan, cakes in a cup, rolled ice cream, breakfast, sandwiches, drinks, market
- [Custom Cakes]({BASE}cakes.html): cake gallery, occasions, how to order (call or email; pickup at the shop)
- [Reviews]({BASE}reviews.html): word-for-word Google reviews
- [Visit & FAQ]({BASE}visit.html): hours, map, contact, FAQ

## FAQ
{fq}

Prices are not published online; call the bakery for current prices.
This site is a design preview by RGWebD.
''')

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT,'assets'), exist_ok=True)
    shutil.copy(os.path.join(GEN,'styles.css'), os.path.join(ROOT,'assets','styles.css'))
    shutil.copy(os.path.join(GEN,'script.js'), os.path.join(ROOT,'assets','script.js'))
    home(); menu(); cakes(); reviews(); visit(); notfound(); textfiles()
    print('built →', ROOT, 'base', BASE)

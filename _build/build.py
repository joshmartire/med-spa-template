#!/usr/bin/env python3
"""
Med Spa Website Template — static site generator (Rank Boss).

Usage:  python3 _build/build.py
Reads:  _build/site.config.json, _build/content_services.py, _build/content_cities.py, _build/pages.py, _build/art.py
Writes: the published site into the repository root (HTML pages, sitemap.xml, robots.txt, 404.html).

Everything client-specific lives in site.config.json: business details, the three brand colours, the services
offered, starting prices, photos, the hero claim, the opening animation and the treatment finder. Shared
components (nav, page header, footer, schema, metadata) live in this file, so one change updates every page on
the next build. Folders starting with "_" are never published. Never hand-edit the generated HTML.
"""
import json, os, re, html, posixpath, sys, hashlib, shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_services import SERVICES as ALL_SERVICES
from content_cities import CITIES
import pages as P
import photos as PH
import art as A

CFG = json.load(open(os.path.join(HERE, "site.config.json"), encoding="utf-8"))
ALL_SVC = {s["slug"]: s for s in ALL_SERVICES}

# ---- services the client offers. Removing a slug drops its pages, menu, footer and finder entries, sitemap URLs and
# form options. Links to it inside other text become plain text and are listed in _build/removed-service-mentions.txt.
_wanted = CFG.get("services") or [s["slug"] for s in ALL_SERVICES]
_unknown = [x for x in _wanted if x not in ALL_SVC]
if _unknown:
    sys.exit(f"site.config.json: unknown service slug(s) {_unknown}. Valid: {[s['slug'] for s in ALL_SERVICES]}")
SERVICES = [s for s in ALL_SERVICES if s["slug"] in _wanted]
if not SERVICES:
    sys.exit("site.config.json: services is empty. List at least one service slug.")
SVC = {s["slug"]: s for s in SERVICES}
REMOVED_MENTIONS = {}
CATS = [
    ("injectables", "Injectables", "Wrinkle-relaxing injections, fillers and skin boosters, placed in measured amounts by licensed injectors."),
    ("skin", "Skin", "Medical-grade facials, peels, microneedling and dermaplaning for clearer, smoother, brighter skin."),
    ("laser", "Laser and body", "Laser hair removal, IPL, radiofrequency tightening and body contouring, planned as a course."),
]
CATS = [c for c in CATS if any(s["cat"] == c[0] for s in SERVICES)]
CAT_LABEL = {c: l for c, l, _ in CATS}
CAT_TONE = {"injectables": "t-acc", "skin": "t-f2", "laser": "t-f3"}
CONCERNS = [
    ("lines", "Lines and wrinkles"), ("volume", "Lost volume"), ("lips", "Lips"), ("dull", "Dull or tired skin"),
    ("texture", "Texture and scarring"), ("spots", "Sun spots and redness"), ("hair", "Unwanted hair"),
    ("laxity", "Loose skin"), ("fat", "Stubborn fat"),
]
CONCERNS = [c for c in CONCERNS if any(c[0] in s["concerns"] for s in SERVICES)]
FINDER_ON = bool(CFG.get("finder", True))
INTRO_ON = bool(CFG.get("intro", True))
INTRO_SCOPE = CFG.get("intro_scope", "all")
PRICES = CFG.get("prices") or {}
CUR = CFG.get("currency", "CAD")

# ---- brand colours. The build stops if a colour can't carry its text at WCAG AA.
def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def _lum(h):
    v = [x / 255 for x in _rgb(h)]
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

INK = "#1c1517"     # page ground and dark text
PAPER = "#f7f1ef"   # porcelain: light panels and light text
PAPER_D = "#ece2df"
CHAR = "#2e2427"

def _colour(key, default, against, what):
    v = (CFG.get(key) or default).strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
        sys.exit(f"site.config.json: {key} must be a #rrggbb colour (got {v!r}).")
    if contrast(v, against) < 4.5:
        sys.exit(f"site.config.json: {key} {v} can't carry {what} ({contrast(v, against):.1f}:1, needs 4.5:1). "
                 f"{'Pick a lighter version of the colour.' if against == INK else 'Pick a deeper version of the colour.'}")
    return v
ACCENT = _colour("accent", "#f4b8c4", INK, "dark text")
F2 = _colour("field_2", "#c8d8c3", INK, "dark text")
F3 = _colour("field_3", "#6b1f37", PAPER, "light text")

# ---- logo
LOGO_FILE = (CFG.get("logo") or "").strip()
if LOGO_FILE and not os.path.isfile(os.path.join(ROOT, LOGO_FILE.lstrip("/"))):
    sys.exit(f"site.config.json: logo file not found: {LOGO_FILE}")
LOGO_W, LOGO_H = 160, 44

def prep_logo():
    global LOGO_W
    out = os.path.join(ROOT, "assets", "img", "client-logo.webp")
    if not LOGO_FILE:
        if os.path.exists(out): os.remove(out)
        return
    from PIL import Image
    im = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox() or (0, 0, im.width, im.height))
    if im.height > 240:
        im = im.resize((round(im.width * 240 / im.height), 240), Image.LANCZOS)
    im.save(out, "WEBP", quality=92, method=6)
    LOGO_W = max(1, round(im.width * LOGO_H / im.height))

PHOTOS = PH.load(CFG, ROOT, set(ALL_SVC), "site.config.json")
PHOTO_CLASSES = {"section": "svb gal", "head": "gal-h", "kicker": "vh", "h2": "sh", "lead": "lead", "group_title": True}

# ---- big picture slots (hero square, category sheets): the client's photo when supplied, else the drawing
SLOT_DIR = "assets/img/slots"
SLOTS = {}

def prep_slots():
    shutil.rmtree(os.path.join(ROOT, SLOT_DIR), ignore_errors=True)
    want = {}
    if CFG.get("hero_photo"):
        want["hero"] = CFG["hero_photo"]
    for k, v in (CFG.get("category_photos") or {}).items():
        if k in CAT_LABEL and v:
            want["cat-" + k] = v
    if not want:
        return
    from PIL import Image, ImageOps
    os.makedirs(os.path.join(ROOT, SLOT_DIR), exist_ok=True)
    for key, v in want.items():
        f, alt = (v.get("file") or "").strip(), (v.get("alt") or "").strip()
        src = os.path.join(ROOT, f.lstrip("/"))
        if not os.path.isfile(src):
            sys.exit(f"site.config.json: photo for {key} not found: {f}")
        if not alt:
            sys.exit(f"site.config.json: photo for {key} needs alt text")
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        side = min(im.size)
        im = im.crop(((im.width - side) // 2, (im.height - side) // 2, (im.width + side) // 2, (im.height + side) // 2)).resize((1000, 1000), Image.LANCZOS)
        name = f"{key}-{hashlib.md5(open(src, 'rb').read()).hexdigest()[:8]}.webp"
        im.save(os.path.join(ROOT, SLOT_DIR, name), "WEBP", quality=82, method=6)
        SLOTS[key] = (name, alt)

def slot(here, key, art_key, label, lazy=True):
    if key in SLOTS:
        name, alt = SLOTS[key]
        return (f'<img class="ph" src="{asset(here, "img/slots/" + name)}" width="1000" height="1000" alt="{html.escape(alt)}"'
                f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')
    return A.draw(art_key, label)

BIZ = CFG["business_name"]
DOMAIN = CFG["domain"].rstrip("/")
BASE = CFG.get("base_path", "/")
PHONE = CFG["phone_display"]
TEL = CFG["phone_e164"]
CTA = CFG["cta_label"]
PROV = CFG["province"]
CITY_NAMES = [c["name"] for c in CITIES]

def and_join(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]
CITY_TEXT = and_join(CITY_NAMES)

def disp(text):
    """Display headings are set lower case; keep acronyms upright."""
    return re.sub(r"\b(IPL|RF|ON)\b", r'<span class="ac">\1</span>', text)

def price_of(slug):
    p = PRICES.get(slug)
    if not p or p.get("from") is None:
        return None
    return p

def price_text(slug, short=False):
    p = price_of(slug)
    if not p:
        return "Priced at consultation"
    if p["from"] == 0:
        return "Complimentary"
    amt = f'${p["from"]:,}'
    return f"from {amt}" if short else f"From {amt} {p.get('unit', '')}".strip()

# ------------------------------------------------------------------ icons
UI = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
 "check": '<path d="M4 12l5 5L20 6"/>',
}

def ui(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{UI[name]}</svg>'

# brand mark: a small peony from above (five round petals around a centre)
import math as _m
LOGO_MARK = ('<svg class="mk" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
             + "".join(f'<circle cx="{20 + 10 * _m.cos(_m.radians(a)):.1f}" cy="{20 + 10 * _m.sin(_m.radians(a)):.1f}" r="9" class="mk-p"/>' for a in range(-90, 270, 72))
             + '<circle cx="20" cy="20" r="8" class="mk-c"/><circle cx="20" cy="20" r="3.2" class="k-p"/></svg>')

# ------------------------------------------------------------------ opening animation: "the bloom"
# The peony mark blooms ring by ring on the deep field, the business name rises letter by letter, then the panel lifts
# away. Timings live in main.css (OPENING ANIMATION); main.js lets a tap or key skip it and removes it at the end.
def intro_markup():
    import math
    rings = ""
    for k, (r, n, pr, cls, start) in enumerate(((110, 9, 64, "k-a", 10), (62, 8, 48, "k-3", 30), (30, 6, 26, "k-a", 0))):
        for i in range(n):
            t = math.radians(start + i * 360 / n)
            rings += (f'<circle class="{cls}" style="--d:{k * 260 + i * 40}ms" cx="{200 + r * math.cos(t):.1f}" cy="{200 + r * math.sin(t):.1f}" r="{pr}"/>')
    rings += '<circle class="k-p" style="--d:900ms" cx="200" cy="200" r="22"/>'
    letters = "".join(f'<span style="--i:{i}">{html.escape(ch) if ch != " " else "&nbsp;"}</span>' for i, ch in enumerate(BIZ))
    return f'''<div class="intro" aria-hidden="true">
<svg class="intro-bloom" viewBox="0 0 400 400">{rings}</svg>
<p class="intro-name">{letters}</p>
<p class="intro-sub">{html.escape(CFG.get("short_tagline", ""))} · {html.escape(CFG["region_label"])}</p>
</div>'''

# ------------------------------------------------------------------ urls
def url_of(path):
    if path == "index.html":
        return DOMAIN + "/"
    if path.endswith("/index.html"):
        return DOMAIN + "/" + path[:-len("index.html")]
    return DOMAIN + "/" + path

def href(from_path, to_path):
    from_dir = posixpath.dirname(from_path)
    if to_path.endswith("index.html"):
        rel = posixpath.relpath(posixpath.dirname(to_path) or ".", from_dir or ".")
        return "./" if rel == "." else rel + "/"
    return posixpath.relpath(to_path, from_dir or ".")

def asset(from_path, a):
    return posixpath.relpath("assets/" + a, posixpath.dirname(from_path) or ".")

_VER = {}
def vasset(from_path, a):
    if a not in _VER:
        _VER[a] = hashlib.md5(open(os.path.join(ROOT, "assets", a), "rb").read()).hexdigest()[:8]
    return asset(from_path, a) + "?v=" + _VER[a]

PATH = {
 "home": "index.html",
 "services": "treatments/index.html",
 "menu": "treatment-menu/index.html",
 "areas": "service-areas/index.html",
 "about": "about/index.html",
 "faq": "faq/index.html",
 "contact": "book/index.html",
 "thanks": "thank-you/index.html",
 "privacy": "privacy-policy.html",
 "terms": "terms-and-conditions.html",
 "cookies": "cookie-policy.html",
}
def svc_path(slug): return f"treatments/{slug}/index.html"
def svc_city_path(slug, city): return f"treatments/{slug}/{city}/index.html"
def city_path(city): return f"service-areas/{city}/index.html"

def expand(text, here):
    """Replace {biz}/{phone} tokens and [[key|anchor]] links."""
    text = text.replace("{biz}", html.escape(BIZ)).replace("{phone}", html.escape(PHONE))
    def link(m):
        key, anchor = m.group(1), m.group(2)
        if key == "finder":
            target = (PATH["services"] if FINDER_ON else None)
            if not target:
                return anchor
            return f'<a href="{href(here, target)}#finder">{anchor}</a>'
        if key.startswith("area:"): target = city_path(key[5:])
        elif key in PATH: target = PATH[key]
        elif key in SVC: target = svc_path(key)
        elif key in ALL_SVC:
            start = max(text.rfind(". ", 0, m.start()), text.rfind(">", 0, m.start())) + 1
            ends = [i for i in (text.find(". ", m.end()), text.find("<", m.end())) if i != -1]
            sentence = re.sub(r"\[\[[a-z0-9:\-]+\|([^\]]+)\]\]", r"\1", text[start:(min(ends) + 1 if ends else len(text))]).strip().rstrip("<").strip()
            REMOVED_MENTIONS.setdefault(sentence, set()).add(ALL_SVC[key]["name"])
            return anchor
        else: raise SystemExit(f"Unknown link target [[{key}]]")
        return f'<a href="{href(here, target)}">{anchor}</a>'
    return re.sub(r"\[\[([a-z0-9:\-]+)\|([^\]]+)\]\]", link, text)

# ------------------------------------------------------------------ shared components
def brand_inner(here):
    if LOGO_FILE:
        return f'<img class="brand-logo" src="{asset(here, "img/client-logo.webp")}" alt="{html.escape(BIZ)}" width="{LOGO_W}" height="{LOGO_H}" decoding="async">'
    return f'{LOGO_MARK}<span class="bn">{html.escape(BIZ)}</span>'

def nav_html(here, active):
    def a(key, label):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href(here, PATH[key])}"{cur}>{label}</a>'
    cols = ""
    for cat, label, _ in CATS:
        items = "".join(f'<a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a>' for s in SERVICES if s["cat"] == cat)
        cols += f'<div class="mg-c"><p class="mg-t">{label}</p>{items}</div>'
    cols += f'<div class="mg-c mg-all"><a href="{href(here, PATH["services"])}">All treatments {ui("arrow")}</a><a href="{href(here, PATH["menu"])}">Treatment menu and prices {ui("arrow")}</a></div>'
    areas = "".join(f'<a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES) + f'<a href="{href(here, PATH["areas"])}">All areas</a>'
    t_cur = ' aria-current="page"' if active == "services" else ""
    a_cur = ' aria-current="page"' if active == "areas" else ""
    mobile_groups = "".join(
        f'<p class="mp-g">{label}</p>' + "".join(f'<a class="sub" href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a>' for s in SERVICES if s["cat"] == cat)
        for cat, label, _ in CATS)
    return f'''<nav class="nav" aria-label="Main">
<a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
<div class="links">
<div class="dd"><button class="ddb" type="button" aria-expanded="false" aria-controls="mg-t"{t_cur}>Treatments {ui("chev", "chev")}</button><div class="ddm mg" id="mg-t">{cols}</div></div>
{a("menu", "Prices")}
<div class="dd"><button class="ddb" type="button" aria-expanded="false" aria-controls="mg-a"{a_cur}>Areas {ui("chev", "chev")}</button><div class="ddm" id="mg-a">{areas}</div></div>
{a("about", "About")}{a("faq", "FAQ")}
</div>
<a class="ntel" href="tel:{TEL}">{PHONE}</a>
<a class="btn" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="mp" aria-label="Open menu"><i></i><i></i><i></i></button>
</nav>
<div class="mp" id="mp">
<a href="{href(here, PATH["home"])}">Home</a>
<a href="{href(here, PATH["services"])}">Treatments</a>
{mobile_groups}
<a href="{href(here, PATH["menu"])}">Prices</a>
<a href="{href(here, PATH["areas"])}">Areas</a>
<a href="{href(here, PATH["about"])}">About</a>
<a href="{href(here, PATH["faq"])}">FAQ</a>
<a href="{href(here, PATH["contact"])}">{CTA}</a>
<a href="tel:{TEL}">Call {PHONE}</a>
</div>'''

def hours_text():
    return [f'{h["label"]}: {fmt_time(h["open"])} to {fmt_time(h["close"])}' for h in CFG.get("hours") or []]

def fmt_time(t):
    hh, mm = map(int, t.split(":"))
    suf = "a.m." if hh < 12 else "p.m."
    return f"{hh % 12 or 12}:{mm:02d} {suf}" if mm else f"{hh % 12 or 12} {suf}"

def address_text():
    a = CFG.get("address")
    return f'{a["street"]}, {a["city"]}, {a["region"]} {a["postal"]}' if a else ""

def cta_panel(here, title="Still you, just fresher", text=None, tone="t-f3"):
    text = text or f"Book a complimentary consultation and leave with a plan, not a sales pitch."
    return f'''<section class="cta panel {tone}" aria-labelledby="cta-h">
<h2 class="cta-h" id="cta-h">{disp(title)}</h2>
<div class="cta-row"><p>{text}</p><div class="cta-b"><a class="btn on-dark" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="tlink" href="tel:{TEL}">or call {PHONE}</a></div></div>
</section>'''

def footer_html(here):
    tre = "".join(f'<a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a>' for s in SERVICES)
    areas = "".join(f'<a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES)
    links = [("Google Business Profile", CFG.get("google_business_profile_url"))] + [(p.get("name"), p.get("url")) for p in CFG.get("social_profiles", [])]
    links = [(n, u) for n, u in links if u]
    prof = ("<p>" + " · ".join(f'<a href="{html.escape(u)}" rel="noopener">{html.escape(n)}</a>' for n, u in links) + "</p>") if links else ""
    addr = f'<p>{html.escape(address_text())}</p>' if address_text() else ""
    return f'''<footer class="foot">
<div class="ft f1"><a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
<p class="say">Injectables, skin and laser treatments in {html.escape(CITY_NAMES[0])}, planned to look like you.</p>
<p class="legal">© {date.today().year} {html.escape(CFG["legal_name"])}. <a href="https://getrankboss.com" rel="noopener">Site by Rank Boss</a></p></div>
<div class="ft f2"><p class="h">Treatments</p><nav class="fl" aria-label="Treatments">{tre}</nav></div>
<div class="ft f3"><p class="h">Visit</p><a class="ph2" href="tel:{TEL}">{PHONE}</a><a class="mail" href="mailto:{CFG["email"]}">{CFG["email"]}</a>{addr}<p>{"<br>".join(hours_text())}<br>{html.escape(CFG.get("hours_note", ""))}</p>{prof}</div>
<div class="ft f4"><p class="h">Areas</p><nav class="fl" aria-label="Service areas">{areas}</nav>
<p class="h">Clinic</p><nav class="fl" aria-label="Clinic"><a href="{href(here, PATH["menu"])}">Treatment menu</a><a href="{href(here, PATH["about"])}">About</a><a href="{href(here, PATH["faq"])}">FAQ</a><a href="{href(here, PATH["contact"])}">Book a consultation</a></nav>
<nav class="fl legal" aria-label="Legal"><a href="{href(here, PATH["privacy"])}">Privacy Policy</a><a href="{href(here, PATH["terms"])}">Terms &amp; Conditions</a><a href="{href(here, PATH["cookies"])}">Cookie Policy</a></nav></div>
</footer>
<div class="callbar"><a class="btn ghost" href="tel:{TEL}">{ui("phone")} Call</a><a class="btn" href="{href(here, PATH["contact"])}">Book</a></div>'''

def crumbs_html(here, trail):
    items = "".join(f'<li><span aria-current="page">{l}</span></li>' if p is None else f'<li><a href="{href(here, p)}">{l}</a></li>' for l, p in trail)
    return f'<nav class="bc" aria-label="Breadcrumb"><ol>{items}</ol></nav>'

def crumbs_schema(trail, here):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": html.unescape(re.sub("<[^>]+>", "", l)), "item": url_of(p if p else here)} for i, (l, p) in enumerate(trail, 1)]}

def business_ref():
    return {"@type": "MedicalBusiness", "@id": DOMAIN + "/#business", "name": BIZ, "url": DOMAIN + "/", "telephone": TEL}

def business_entity():
    e = {"@type": "MedicalBusiness", "@id": DOMAIN + "/#business", "name": BIZ,
         "description": f"Medical aesthetics clinic offering injectables, skin treatments and laser in {CITY_TEXT}, {PROV}.",
         "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo.png", "image": DOMAIN + "/assets/img/og-default.png",
         "telephone": TEL, "email": CFG["email"],
         "areaServed": [{"@type": "City", "name": f'{c["name"]}, {PROV}'} for c in CITIES],
         "knowsAbout": [s["name"] for s in SERVICES]}
    if CFG.get("legal_name") and CFG["legal_name"] != BIZ:
        e["legalName"] = CFG["legal_name"]
    a = CFG.get("address")
    if a:
        e["address"] = {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": CFG["country"]}
    if CFG.get("hours"):
        e["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["open"], "closes": h["close"]} for h in CFG["hours"]]
    same = [u for u in [CFG.get("google_business_profile_url")] + [p.get("url") for p in CFG.get("social_profiles", [])] if u]
    if same:
        e["sameAs"] = same
    return e

PAGES = []

def demo_bar():
    if not CFG.get("demo_mode"):
        return ""
    return ('<aside class="demo-bar" aria-label="Website demo notice">Website demo: the business name, phone, email, address, providers and prices on this site are '
            'samples, not a real company.</aside>')

def page(path, *, title, desc, body, active=None, crumbs=None, schema=None, noindex=False, scripts_extra="", body_class=""):
    full_title = title if BIZ in title else f"{title} | {BIZ}"
    if len(full_title) > 65 and BIZ not in title:
        full_title = title
    robots = "noindex, follow" if (noindex or CFG.get("demo_mode")) else "index, follow"
    graph = list(schema or [])
    if crumbs:
        graph.append(crumbs_schema(crumbs, path))
    ld = ""
    if graph:
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
    canonical = url_of(path) if path != "404.html" else DOMAIN + "/404.html"
    verify = f'<meta name="google-site-verification" content="{html.escape(CFG["google_site_verification"])}">' if CFG.get("google_site_verification") else ""
    intro_here = INTRO_ON and not noindex and (INTRO_SCOPE == "all" or path == "index.html")
    if intro_here:
        boot = ('<script>(function(d){d.className=d.className.replace("no-js","js");try{if(sessionStorage.getItem("ms-intro")||location.hash.length>1||'
                'matchMedia("(prefers-reduced-motion: reduce)").matches)d.className+=" no-intro"}catch(e){d.className+=" no-intro"}})(document.documentElement)</script>')
    else:
        boot = '<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>'
    html_cls = "no-js" + (" has-demo" if CFG.get("demo_mode") else "") + ("" if intro_here else " no-intro")
    out = f'''<!doctype html>
<html lang="en-CA" class="{html_cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{verify}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{html.escape(BIZ)}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(BIZ)}, medical aesthetics in {html.escape(CFG["region_label"])}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{INK}">
<link rel="icon" href="{asset(path, "img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{asset(path, "img/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{asset(path, "img/apple-touch-icon.png")}">
<link rel="preload" href="{asset(path, "fonts/b800.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset(path, "fonts/b400.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{vasset(path, "css/main.css")}">
<style>:root{{--acc:{ACCENT};--f2:{F2};--f3:{F3}}}</style>
{boot}
{ld}
</head>
<body{f' class="{body_class}"' if body_class else ""}>
<a class="skip" href="#main">Skip to content</a>
{demo_bar()}
{intro_markup() if intro_here else ""}
{body}
{footer_html(path)}
<script src="{vasset(path, "js/main.js")}" defer></script>
{scripts_extra}
</body>
</html>
'''
    out = re.sub(r"\n{2,}", "\n", out)
    dest = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(dest) or ROOT, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    PAGES.append({"path": path, "url": canonical if path != "404.html" else None, "title": full_title, "noindex": noindex})

def page_head(here, *, h1, lead, crumbs, active, tone="t-acc", art="peony", art_label=None, ctas=True, slot_key=None, size=""):
    btns = ""
    if ctas:
        btns = (f'<div class="btns"><a class="btn{" on-dark" if tone == "t-f3" else ""}" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>'
                f'<a class="tlink" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>')
    pic = (f'<div class="pkh-art">{slot(here, slot_key, art, art_label, lazy=False) if slot_key else A.draw(art, art_label)}</div>') if art else ""
    return f'''<header class="pkh {tone}{" " + size if size else ""}">
{nav_html(here, active)}
<div class="pkh-g{"" if art else " noart"}"><div class="pkh-t">{crumbs_html(here, crumbs)}
<h1 class="d">{disp(h1)}</h1>
<p class="lead">{lead}</p>
{btns}</div>{pic}</div>
</header>
<main id="main">'''

def faq_bands(faqs, here, head=None, head_id="faq-h"):
    rows = "".join(f'<div class="fb"><h3>{html.escape(q)}</h3><p>{expand(a, here)}</p></div>' for q, a in faqs)
    top = f'<div class="fb-h t-acc"><h2 class="d" id="{head_id}">{disp(head)}</h2></div>' if head else ""
    return f'<section class="fbs panel"{f" aria-labelledby=\"{head_id}\"" if head else ""}>{top}{rows}</section>'

def faq_list(faqs, here):
    return '<div class="faq">' + "".join(
        f'<details><summary>{html.escape(q)}</summary><div class="faq-a"><p>{expand(a, here)}</p></div></details>' for q, a in faqs) + "</div>"

def glance(s, here):
    rows = [("Treatment time", s["time"]), ("Downtime", s["downtime"]), ("Sessions", s["sessions"]), ("Price", price_text(s["slug"]))]
    return '<dl class="gl">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"

BEFORE = {
    "injectables": "Before injectables, let us know about any medications, supplements, recent dental work, cold sores, pregnancy or upcoming events. Avoiding alcohol and blood-thinning supplements for a day or two beforehand can reduce bruising, unless your doctor has told you to take them. Plan important events at least two weeks after treatment.",
    "skin": "Before a skin treatment, tell us about any retinoids, acne medications, recent waxing, peels or sun exposure, and any history of cold sores. Some products need to be paused a few days beforehand, and treatments are rescheduled over a fresh sunburn or tan. Come with clean skin if you can.",
    "laser": "Before laser and energy treatments, avoid tanning, sunless tanner and sunburn for several weeks, and tell us about any medications that make skin sensitive to light, recent treatments, implants or pregnancy. Shave the area the day before laser hair removal unless we tell you otherwise.",
}

def aside_html(here, s=None, city=None):
    hours = "<br>".join(hours_text())
    blocks = [f'''<div class="as t-acc"><h2>Book a consultation</h2><p>A complimentary conversation about your goals, your history and an honest plan.</p>
<a class="btn" href="{href(here, PATH["contact"]) + ("?t=" + s["slug"] if s else "")}">{CTA} {ui("arrow")}</a><a class="tlink" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>''']
    if s:
        rel = "".join(f'<li><a href="{href(here, svc_path(r) if not city else svc_city_path(r, city["slug"]))}">{SVC[r]["name"]}{" in " + city["name"] if city else ""}</a></li>' for r in s["related"] if r in SVC)
        if rel:
            blocks.append(f'<div class="as t-paper-d"><h2>Pairs well with</h2><ul>{rel}</ul></div>')
        cl = "".join(f'<li><a href="{href(here, svc_city_path(s["slug"], c["slug"]))}"{" aria-current=\"page\"" if city and c["slug"] == city["slug"] else ""}>{s["name"]} in {c["name"]}</a></li>' for c in CITIES)
        blocks.append(f'<div class="as t-paper-d"><h2>Nearby</h2><ul>{cl}</ul></div>')
    blocks.append(f'<div class="as t-paper-d"><h2>Hours</h2><p>{hours}<br>{html.escape(CFG.get("hours_note", ""))}</p></div>')
    return '<aside class="aside" aria-label="Book and visit">' + "".join(blocks) + "</aside>"

# ------------------------------------------------------------------ treatment finder (the live thing)
def finder_html(here, head_tag="h2"):
    if not FINDER_ON:
        return ""
    chips = "".join(f'<label class="chip"><input type="checkbox" name="c" value="{k}"><span>{l}</span></label>' for k, l in CONCERNS)
    items = ""
    for s in SERVICES:
        cn = ", ".join(l for k, l in CONCERNS if k in s["concerns"])
        items += (f'<li class="fr {CAT_TONE[s["cat"]]}" data-c="{" ".join(s["concerns"])}" data-dt="{s["dt"]}"><a href="{href(here, svc_path(s["slug"]))}">'
                  f'<span class="fr-n">{s["name"]}</span><span class="fr-c">For {cn.lower()}</span>'
                  f'<span class="fr-m"><span>{s["time"]}</span><span>{s["downtime"] if "downtime" in s["downtime"].lower() else "Downtime: " + s["downtime"].lower()}</span><span>{price_text(s["slug"], short=True).capitalize()}</span></span></a></li>')
    return f'''<section class="finder panel t-paper" id="finder" aria-labelledby="finder-h">
<div class="fd-top"><{head_tag} class="sh d r" id="finder-h">Find your treatment</{head_tag}><p class="lead r">Pick what you'd like to change. We'll show the treatments that address it, how long they take and the downtime to plan for.</p></div>
<form class="fd-f r" aria-label="Treatment finder" onsubmit="return false">
<fieldset><legend>What would you like to change?</legend><div class="chips">{chips}</div></fieldset>
<fieldset class="fd-dt"><legend>Downtime you can plan for</legend><div class="seg"><label><input type="radio" name="dt" value="9" checked><span>Some is fine</span></label><label><input type="radio" name="dt" value="0"><span>No downtime</span></label></div></fieldset>
</form>
<p class="fd-n" id="fd-n" role="status" aria-live="polite">All {len(SERVICES)} treatments</p>
<ul class="fd-r" id="fd-r">{items}</ul>
<p class="fd-none" id="fd-none" hidden>Nothing here matches every choice. Try "Some is fine" for downtime, or <a href="{href(here, PATH["contact"])}">book a consultation</a> and we'll talk it through.</p>
<div class="fd-go"><a class="btn" id="fd-book" href="{href(here, PATH["contact"])}">Ask about these at a consultation {ui("arrow")}</a><p class="small">A guide, not a diagnosis. Your provider confirms what suits you at your consultation.</p></div>
</section>'''

# ------------------------------------------------------------------ pages
def lower_name(s):
    """Service name mid-sentence: lower case, acronyms kept."""
    return " ".join(w if re.fullmatch(r"(IPL|RF)", w) else w.lower() for w in s["name"].split(" "))

def sentence_name(s):
    n = lower_name(s)
    return n[0].upper() + n[1:]

def build_service(s):
    here = svc_path(s["slug"])
    crumbs = [("Home", PATH["home"]), ("Treatments", PATH["services"]), (s["name"], None)]
    cities = "".join(f'<a class="pill" href="{href(here, svc_city_path(s["slug"], c["slug"]))}">{s["name"]} in {c["name"]}</a>' for c in CITIES)
    content = f'''{page_head(here, h1=s["h1"], lead=s["lead"], crumbs=crumbs, active="services", tone=CAT_TONE[s["cat"]], art=s["art"])}
<section class="svb panel t-paper"><div class="svg2">
<div class="prose r">
{glance(s, here)}
{expand(s["body"], here)}
<h2>Before your appointment</h2>
<p>{BEFORE[s["cat"]]}</p>
<h2>What affects the price</h2>
{expand(s["cost"], here)}
<h2>{s["name"]} questions</h2>
{faq_list(s["faqs"], here)}
<h2>Where we offer {lower_name(s)}</h2>
<p>We see clients for {lower_name(s)} from {CITY_TEXT}. See notes for your area:</p>
<div class="pills">{cities}</div>
<p class="prov">{html.escape(CFG.get("provider_line", ""))} Results vary from person to person.</p>
</div>
{aside_html(here, s)}
</div></section>
{PH.gallery(PH.for_service(PHOTOS, s["slug"]), lambda x: asset(here, x[len("/assets/"):]), f"{s['name']} at {BIZ}", kicker="Our work", limit=3, classes=PHOTO_CLASSES)}
{cta_panel(here)}
</main>'''
    schema = [{"@type": "Service", "@id": url_of(here) + "#service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "url": url_of(here),
               "provider": business_ref(), "areaServed": [{"@type": "City", "name": f'{c["name"]}, {PROV}'} for c in CITIES]}]
    page(here, title=s["title"], desc=s["desc"], body=content, active="services", crumbs=crumbs, schema=schema)

def build_service_city(s, c, idx):
    here = svc_city_path(s["slug"], c["slug"])
    crumbs = [("Home", PATH["home"]), ("Treatments", PATH["services"]), (s["name"], svc_path(s["slug"])), (c["name"], None)]
    labels = re.findall(r"<li><strong>([^<]+)\.</strong>", s["body"])
    included = "".join(f"<li>{l}</li>" for l in labels)
    facts = c["facts"]
    f1, f2 = facts[idx % len(facts)], facts[(idx + 3) % len(facts)]
    others = [x for x in CITIES if x["slug"] != c["slug"]]
    other_links = " and ".join(f'<a href="{href(here, svc_city_path(s["slug"], o["slug"]))}">{lower_name(s)} in {o["name"]}</a>' for o in others)
    rel = [r for r in s["related"] if r in SVC]
    rel_links = ", ".join(f'<a href="{href(here, svc_city_path(r, c["slug"]))}">{lower_name(SVC[r])}</a>' for r in rel)
    rel_sentence = f"{c['name']} clients considering {lower_name(s)} often ask about {rel_links} too. " if rel_links else ""
    body = f'''<h2>{s["name"]} for {c["name"]} clients</h2>
<p>{c["short"]} {s["short"]}</p>
<p>{f1}</p>
<h2>What it can address</h2>
<p>Your plan depends on your consultation. {sentence_name(s)} can help with:</p>
<ul>{included}</ul>
{glance(s, here)}
<p>How it works, what to expect and common questions are on our main <a href="{href(here, svc_path(s["slug"]))}">{lower_name(s)} page</a>.</p>
<h2>Planning around life in {c["name"]}</h2>
<p>{c["cat"][s["cat"]]}</p>
<p>{f2}</p>
<h2>Getting to the clinic</h2>
<p>{c["visit"]} {"Starting prices are on our <a href=\"" + href(here, PATH["menu"]) + "\">treatment menu</a>." }</p>
<h2>More for {c["name"]} clients</h2>
<p>{rel_sentence}We also have pages for {other_links}. Every treatment we offer is listed on our <a href="{href(here, city_path(c["slug"]))}">{c["name"]} area page</a>.</p>'''
    content = f'''{page_head(here, h1=f'{s["name"]} in {c["name"]}', lead=f'{sentence_name(s)} for clients in {c["name"]}, {PROV}: planned at a complimentary consultation with a licensed provider.', crumbs=crumbs, active="services", tone=CAT_TONE[s["cat"]], art=s["art"])}
<section class="svb panel t-paper"><div class="svg2">
<div class="prose r">{expand(body, here)}</div>
{aside_html(here, s, c)}
</div></section>
{cta_panel(here, title=f"{c['name']}, let's talk")}
</main>'''
    desc = f'{sentence_name(s)} for clients in {c["name"]}, {PROV}: {s["short"][0].lower() + s["short"][1:]}'
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",") + "…"
    schema = [{"@type": "Service", "@id": url_of(here) + "#service", "name": f'{s["name"]} in {c["name"]}, {PROV}', "serviceType": s["name"], "url": url_of(here),
               "provider": business_ref(), "areaServed": {"@type": "City", "name": f'{c["name"]}, {PROV}'}}]
    page(here, title=f'{s["name"]} in {c["name"]}, {PROV}', desc=desc, body=content, active="services", crumbs=crumbs, schema=schema)

def cat_sheets(here, sticky=True, city=None, head_tag="h2", item_tag="h3"):
    """The treatment families as stacked colour sheets (sticky on the home page)."""
    p = P.home(CFG, CITIES, SERVICES)
    out = ""
    for i, (cat, label, blurb) in enumerate(CATS):
        name, text = p["cats"][cat]
        if city:
            text = city["cat"][cat]
        rows = "".join(f'<li><a href="{href(here, svc_city_path(s["slug"], city["slug"]) if city else svc_path(s["slug"]))}"><span>{s["name"]}</span><span class="pr">{price_text(s["slug"], short=True)}</span></a></li>'
                       for s in SERVICES if s["cat"] == cat)
        pic = slot(here, "cat-" + cat, A.CAT_ART[cat], None)
        out += (f'<article class="sheet {CAT_TONE[cat]}" style="--i:{i}"><div class="sh-t"><{item_tag} class="sh-n d">{disp(name)}</{item_tag}><p>{text}</p>'
                f'<ul class="sh-l">{rows}</ul></div><div class="sh-p">{pic}</div></article>')
    return f'<div class="sheets{" sticky" if sticky else ""}">{out}</div>'

def build_services_hub():
    here = PATH["services"]
    crumbs = [("Home", PATH["home"]), ("Treatments", None)]
    content = f'''{page_head(here, h1="Treatments", lead=f"{len(SERVICES)} treatments across injectables, skin and laser, each planned at a complimentary consultation in {CITY_NAMES[0]}.", crumbs=crumbs, active="services", tone="t-acc", art="peony")}
{finder_html(here)}
<section class="tsec" aria-labelledby="fam-h"><h2 class="vh" id="fam-h">Treatments by type</h2>{cat_sheets(here, sticky=False)}</section>
{cta_panel(here)}
</main>'''
    items = [{"@type": "ListItem", "position": i, "url": url_of(svc_path(s["slug"])), "name": s["name"]} for i, s in enumerate(SERVICES, 1)]
    page(here, title="Treatments", desc=f"Injectables, skin treatments, laser and body contouring at {BIZ} in {CITY_NAMES[0]}, with a treatment finder and starting prices.", body=content,
         active="services", crumbs=crumbs, schema=[{"@type": "ItemList", "itemListElement": items}], scripts_extra=f'<script src="{vasset(here, "js/finder.js")}" defer></script>' if FINDER_ON else "")

def menu_rows(here):
    out = ""
    for cat, label, _ in CATS:
        rows = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}"><span class="mn-n">{s["name"]}</span><span class="mn-u">{html.escape(s["time"])}</span><span class="mn-p">{price_text(s["slug"])}</span></a></li>'
                       for s in SERVICES if s["cat"] == cat)
        out += f'<div class="mn-g"><h3>{label}</h3><ul>{rows}</ul></div>'
    return out

def build_menu():
    here = PATH["menu"]
    crumbs = [("Home", PATH["home"]), ("Treatment menu", None)]
    consult = price_text("consultation")
    note = '<p class="demo-note">Website demo: these prices are samples. Each clinic sets its own.</p>' if CFG.get("demo_mode") else ""
    content = f'''{page_head(here, h1="Treatment menu", lead="Starting prices for every treatment we offer. Your exact price depends on your plan and is confirmed at your consultation, before anything begins.", crumbs=crumbs, active="menu", tone="t-f2", art="jar")}
<section class="mnu" aria-labelledby="mnu-h">
<div class="mn-c panel t-acc"><h2 class="d" id="mnu-h">Your first visit</h2><p>A relaxed conversation with a provider about your skin and your goals, and a plan you can take home. No obligation.</p>
<p class="big d">{consult.lower()}</p><a class="btn" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a></div>
<div class="mn-l panel t-char"><h2 class="d">Starting prices</h2>{menu_rows(here)}{note}</div>
</section>
<section class="svb panel t-paper"><div class="prose narrow r">
<h2>How pricing works</h2>
<p>Most treatments are priced per area, per syringe, per session or as a package for a series. The price that suits you depends on what you want to change, how many areas are involved and how your skin or face responds, which is why we confirm it at your consultation. You'll always know the price before treatment begins.</p>
<p>Not sure where to start? Try the [[finder|treatment finder]], read our [[faq|frequently asked questions]] or simply [[contact|book a consultation]].</p>
<p class="prov">Prices in {CUR}, before applicable taxes. {html.escape(CFG.get("provider_line", ""))}</p>
</div></section>
{cta_panel(here)}
</main>'''
    offers = [{"@type": "Offer", "name": s["name"], "url": url_of(svc_path(s["slug"])), "priceCurrency": CUR,
               "priceSpecification": {"@type": "PriceSpecification", "minPrice": price_of(s["slug"])["from"], "priceCurrency": CUR}}
              for s in SERVICES if price_of(s["slug"])]
    schema = [{"@type": "OfferCatalog", "name": f"{BIZ} treatment menu", "url": url_of(here), "itemListElement": offers}]
    content = content.replace("[[finder|treatment finder]]", "[[finder|treatment finder]]")
    page(here, title="Treatment Menu and Prices", desc=f"Starting prices for injectables, skin treatments, laser hair removal and body contouring at {BIZ}. Consultations are complimentary.",
         body=expand(content, here), active="menu", crumbs=crumbs, schema=schema)

def build_city_hub(c):
    here = city_path(c["slug"])
    crumbs = [("Home", PATH["home"]), ("Areas", PATH["areas"]), (c["name"], None)]
    hub = "".join(f"<p>{p}</p>" for p in c["hub"])
    others = " · ".join(f'<a href="{href(here, city_path(o["slug"]))}">{o["name"]}</a>' for o in CITIES if o["slug"] != c["slug"])
    content = f'''{page_head(here, h1=f'Med spa treatments in {c["name"]}', lead=c["intro"], crumbs=crumbs, active="areas", tone="t-f2", art="peony")}
<section class="svb panel t-paper"><div class="prose narrow r">{hub}<h2>Getting here</h2><p>{c["visit"]}</p><p>Also nearby: {others}</p></div></section>
<section class="tsec" aria-labelledby="ct-h"><h2 class="vh" id="ct-h">Treatments for {c["name"]} clients</h2>{cat_sheets(here, sticky=False, city=c)}</section>
{cta_panel(here, title=f"{c['name']}, we're close by")}
</main>'''
    page(here, title=c["title"], desc=c["desc"], body=content, active="areas", crumbs=crumbs)

def build_areas_hub():
    here = PATH["areas"]
    crumbs = [("Home", PATH["home"]), ("Areas", None)]
    rows = "".join(f'<li><a class="ar r" href="{href(here, city_path(c["slug"]))}"><span class="ar-n d">{c["name"]}</span><span class="ar-t">{c["intro"]}</span></a></li>' for c in CITIES)
    content = f'''{page_head(here, h1="Areas we serve", lead=f"Clients come to us from {CITY_TEXT}. Each area page lists every treatment, with notes for that town.", crumbs=crumbs, active="areas", tone="t-acc", art="peony")}
<section class="areas panel t-paper" aria-labelledby="ar-h"><h2 class="vh" id="ar-h">Towns</h2><ul class="ar-l">{rows}</ul>
<p class="r">Coming from somewhere else in {html.escape(CFG["region_label"])}? <a href="{href(here, PATH["contact"])}">Book a consultation</a> and we'll see you at the clinic.</p></section>
{cta_panel(here)}
</main>'''
    page(here, title=f"Areas: {CITY_TEXT}", desc=f"Medical aesthetics for clients in {CITY_TEXT}, {PROV}: injectables, skin, laser and body treatments, with notes for each town.", body=content, active="areas", crumbs=crumbs)

def build_home():
    here = PATH["home"]
    p = P.home(CFG, CITIES, SERVICES)
    claim = CFG.get("hero_claim") or BIZ
    unit = f'<span class="mq-u">{html.escape(claim)}<i class="dot" aria-hidden="true"></i></span>'
    group = unit * 4
    line = f'<span class="mq-g">{group}</span><span class="mq-g" aria-hidden="true">{group}</span>'
    hero_pic = slot(here, "hero", "peony_tonal", None, lazy=False)
    steps = "".join(f'<div class="vb {t}" style="--i:{i}"><p class="vb-w d" aria-hidden="true">{v.lower()}</p><div class="vb-t"><h3>{v}</h3><p>{d}</p></div><div class="vb-a">{A.draw(a)}</div></div>'
                    for i, ((v, d), t, a) in enumerate(zip(p["steps"], ["t-acc", "t-f2", "t-f3", "t-paper"], ["peony", "jar", "drop", "mirror"])))
    w1, w2 = P.APPROACH["words"]
    c1, c2 = P.APPROACH["captions"]
    areas = "".join(f'<li><a class="ar r" href="{href(here, city_path(c["slug"]))}"><span class="ar-n d">{c["name"]}</span><span class="ar-t">{c["short"]}</span></a></li>' for c in CITIES)
    content = f'''<header class="hero t-paper">
{nav_html(here, "home")}
<h1 class="mq-band"><span class="vh">{html.escape(claim)}: {html.escape(BIZ)}, medical aesthetics in {html.escape(CITY_NAMES[0])}</span>
<span class="mq-sq" aria-hidden="true">{hero_pic}</span>
<span class="mq mq-ink" aria-hidden="true"><span class="mq-tr">{line}</span></span>
<span class="mq mq-lt" aria-hidden="true"><span class="mq-tr">{line}</span></span>
</h1>
<div class="hero-c"><p class="hero-s">{p["sentence"]}</p><p class="hero-f">{p["fact"]} · {html.escape(CITY_NAMES[0])}, {PROV}</p></div>
<div class="hero-b"><p>{html.escape(address_text() or CFG["region_label"])}</p><a class="btn" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a></div>
</header>
<main id="main">
<section class="treat" aria-labelledby="tr-h"><h2 class="sh d r" id="tr-h">{p["treat_head"]}</h2>{cat_sheets(here)}</section>
{finder_html(here)}
<section class="appr panel t-f2" aria-labelledby="ap-h">
<div class="ap-top"><h2 class="sh d r" id="ap-h">{p["approach_head"]}</h2><p class="lead r">{p["approach_text"]}</p></div>
<div class="ap-w"><figure><figcaption>{c1}</figcaption><p class="spec spec-a" aria-hidden="true">{w1}</p></figure><figure><figcaption>{c2}</figcaption><p class="spec spec-b" aria-hidden="true">{w2}</p></figure></div>
</section>
<section class="verbs" aria-labelledby="vb-h"><h2 class="vh" id="vb-h">How a visit works</h2>{steps}</section>
<section class="mnu" aria-labelledby="mn-h">
<div class="mn-c panel t-acc"><h2 class="d">{p["consult_title"]}</h2><p>{p["consult_text"]}</p><p class="big d">{price_text("consultation").lower()}</p><a class="btn" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a></div>
<div class="mn-l panel t-char"><h2 class="d" id="mn-h">{p["menu_head"]}</h2>{menu_rows(here)}<a class="tlink" href="{href(here, PATH["menu"])}">Full treatment menu {ui("arrow")}</a></div>
</section>
<section class="areas panel t-paper" aria-labelledby="ar-h"><div class="ar-top"><h2 class="sh d r" id="ar-h">{p["areas_head"]}</h2><p class="lead r">{p["areas_lead"]}</p></div><ul class="ar-l">{areas}</ul></section>
{faq_bands(p["faqs"], here, head=p["faq_head"])}
{cta_panel(here, title=p["close_head"], text=p["close_text"])}
</main>'''
    website = {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BIZ, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-CA"}
    page(here, title=f"{BIZ} | Med Spa in {CITY_NAMES[0]}, {PROV}", desc=p["desc"], body=content, active="home", schema=[business_entity(), website], body_class="home",
         scripts_extra=f'<script src="{vasset(here, "js/finder.js")}" defer></script>' if FINDER_ON else "")

def build_simple(key, *, title, desc, h1, lead, inner, active=None, noindex=False, aside=True, schema=None, cta=True, hero_ctas=True):
    here = PATH[key]
    crumbs = [("Home", PATH["home"]), (h1[0].upper() + h1[1:], None)]
    side = aside_html(here) if aside else ""
    grid = "svg2" if aside else "solo"
    content = f'''{page_head(here, h1=h1, lead=lead, crumbs=crumbs, active=active, tone="t-f2" if key in ("privacy", "terms", "cookies") else "t-acc", art=None if key in ("privacy", "terms", "cookies", "thanks") else "peony", ctas=hero_ctas, size="sm" if not aside else "")}
<section class="svb panel t-paper"><div class="{grid}"><div class="prose r{" narrow" if not aside else ""}">{expand(inner(here), here)}</div>{side}</div></section>
{cta_panel(here) if cta else ""}
</main>'''
    page(here, title=title, desc=desc, body=content, active=active, crumbs=crumbs, noindex=noindex, schema=schema)

def build_contact():
    here = PATH["contact"]
    crumbs = [("Home", PATH["home"]), ("Book a consultation", None)]
    def fld(id_, label, inp, req=True, full=False, hint=""):
        r = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="opt">(optional)</span>'
        h = f'<span class="hint" id="{id_}-hint">{hint}</span>' if hint else ""
        return f'<div class="field{" full" if full else ""}"><label for="{id_}">{label}{r}</label>{inp}{h}<span class="err" id="{id_}-error" aria-live="polite"></span></div>'
    tchecks = "".join(f'<label class="chip"><input type="checkbox" name="treatments" value="{html.escape(s["name"])}" data-slug="{s["slug"]}"><span>{s["name"]}</span></label>' for s in SERVICES)
    tchecks += '<label class="chip"><input type="checkbox" name="treatments" value="Not sure yet"><span>Not sure yet</span></label>'
    days = sorted({d for h in CFG.get("hours") or [] for d in h["days"]}, key=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index)
    dchecks = "".join(f'<label class="chip"><input type="checkbox" name="preferred days" value="{d}"><span>{d[:3]}</span></label>' for d in days)
    times = "".join(f'<label class="chip"><input type="radio" name="preferred time" value="{t}"{" checked" if i == 0 else ""}><span>{t}</span></label>' for i, t in enumerate(["Any time", "Morning", "Afternoon", "Evening"]))
    form = f'''<form class="cform" action="{html.escape(CFG["form_endpoint"])}" method="POST" data-validate novalidate>
<p class="cf-status" role="alert"></p>
<input type="hidden" name="_subject" value="New consultation request: {html.escape(BIZ)} website">
<input type="hidden" name="_next" value="{url_of(PATH["thanks"])}">
<input type="hidden" name="_template" value="table">
<div class="hp" aria-hidden="true"><label for="hp-field">Leave this field empty</label><input id="hp-field" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{fld("name", "Full name", '<input id="name" name="name" type="text" autocomplete="name" required data-label="your name" aria-describedby="name-error">')}
{fld("phone", "Phone", '<input id="phone" name="phone" type="tel" autocomplete="tel" required data-label="a phone number" aria-describedby="phone-error">')}
{fld("email", "Email", '<input id="email" name="email" type="email" autocomplete="email" required data-label="an email address" aria-describedby="email-error">', full=True)}
<fieldset class="field full"><legend>Treatments you're interested in <span class="opt">(optional)</span></legend><div class="chips">{tchecks}</div></fieldset>
<fieldset class="field"><legend>New or returning client</legend><div class="chips"><label class="chip"><input type="radio" name="client" value="New client" checked><span>New</span></label><label class="chip"><input type="radio" name="client" value="Returning client"><span>Returning</span></label></div></fieldset>
<fieldset class="field"><legend>Preferred time</legend><div class="chips">{times}</div></fieldset>
<fieldset class="field full"><legend>Preferred days <span class="opt">(optional)</span></legend><div class="chips">{dchecks}</div></fieldset>
{fld("message", "Anything we should know?", '<textarea id="message" name="message" rows="4" aria-describedby="message-hint message-error"></textarea>', req=False, full=True, hint="Please don't include medical history here. We'll go over it privately at your consultation.")}
<p class="cf-note full">We use your details only to respond and book your consultation. See our <a href="{href(here, PATH["privacy"])}">Privacy Policy</a>.</p>
<div class="full"><button class="btn" type="submit">Request my consultation {ui("arrow")}</button></div>
</form>'''
    a = address_text()
    content = f'''{page_head(here, h1="Book a consultation", lead="Tell us how to reach you and what you're curious about. We'll call or email to confirm a time for your complimentary consultation.", crumbs=crumbs, active="contact", tone="t-acc", art="peony", ctas=False)}
<section class="svb panel t-paper"><div class="svg2 book">
<div class="r"><h2 class="sh2">Your request</h2>{form}</div>
<aside class="aside" aria-label="Clinic details">
<div class="as t-f2"><h2>Visit</h2><ul class="cl"><li><span>Call</span><a href="tel:{TEL}">{PHONE}</a></li><li><span>Email</span><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li>{f"<li><span>Address</span><p>{html.escape(a)}</p></li>" if a else ""}<li><span>Hours</span><p>{"<br>".join(hours_text())}<br>{html.escape(CFG.get("hours_note", ""))}</p></li></ul></div>
<div class="as t-paper-d"><h2>What happens next</h2><ol class="nx"><li><strong>We confirm a time</strong> by phone or email.</li><li><strong>Your consultation.</strong> Goals, medical history and an honest plan, with prices.</li><li><strong>Your choice.</strong> Book treatment then, later or not at all.</li></ol></div>
</aside>
</div></section>
</main>'''
    schema = [{"@type": "ContactPage", "url": url_of(here), "name": f"Book a consultation at {BIZ}", "about": {"@id": DOMAIN + "/#business"}}]
    page(here, title="Book a Consultation", desc=f"Request a complimentary consultation at {BIZ} in {CITY_NAMES[0]}. Call {PHONE} or send a request online.", body=content, active="contact", crumbs=crumbs, schema=schema)

def build_404():
    here = "404.html"
    global href, asset
    rel_href, rel_asset = href, asset
    def abs_href(_from, to):
        if to == "index.html": return BASE
        if to.endswith("index.html"): return BASE + to[:-len("index.html")]
        return BASE + to
    href = abs_href
    asset = lambda _f, a: BASE + "assets/" + a
    links = "".join(f'<li><a href="{abs_href(None, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES)
    content = f'''{page_head(here, h1="Page not found", lead="The page you're looking for may have moved. Try one of these instead.", crumbs=[("Home", PATH["home"]), ("Page not found", None)], active=None, tone="t-acc", art="drop", ctas=False)}
<section class="svb panel t-paper"><div class="prose narrow"><h2>Treatments</h2><ul>{links}</ul><p><a href="{BASE}">Back to home</a> · <a href="{abs_href(None, PATH["contact"])}">Book a consultation</a></p></div></section>
</main>'''
    page(here, title="Page Not Found", desc="The page you're looking for couldn't be found.", body=content, noindex=True)
    href, asset = rel_href, rel_asset

def write_sitemap_robots():
    urls = [p for p in PAGES if p["url"] and not p["noindex"]]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{html.escape(p['url'])}</loc></url>" for p in urls]
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    return len(urls)

def write_cname():
    host = re.sub(r"^https?://", "", DOMAIN).strip("/")
    cname = os.path.join(ROOT, "CNAME")
    if "example.com" in host or host.endswith(".pages.dev"):
        if os.path.exists(cname): os.remove(cname)
        return None
    open(cname, "w").write(host + "\n")
    return host

def main():
    for d in ("treatments", "service-areas", "treatment-menu", "book", "about", "faq", "thank-you"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    prep_logo()
    prep_slots()
    PH.process(PHOTOS, ROOT)
    PH.ensure_css(os.path.join(ROOT, "assets", "css", "main.css"))
    try:
        import runpy
        runpy.run_path(os.path.join(HERE, "make_images.py"), run_name="__main__")
    except ImportError as e:
        print(f"WARNING: brand images not regenerated ({e}). pip install pillow fonttools brotli")
    build_home()
    build_services_hub()
    build_menu()
    for i, s in enumerate(SERVICES):
        build_service(s)
        for c in CITIES:
            build_service_city(s, c, i)
    build_areas_hub()
    for c in CITIES:
        build_city_hub(c)
    for key, spec in P.simple_pages(CFG, CITIES, SERVICES, CITY_TEXT).items():
        build_simple(key, **spec)
    build_contact()
    build_404()
    n = write_sitemap_robots()
    host = write_cname()
    json.dump([{"path": p["path"], "url": p["url"], "title": p["title"], "indexable": bool(p["url"]) and not p["noindex"]} for p in PAGES],
              open(os.path.join(HERE, "page-inventory.json"), "w"), indent=1)
    print(f"Built {len(PAGES)} pages, {n} URLs in sitemap.xml. CNAME: {host or 'not written (demo or example domain)'}")
    if CFG.get("demo_mode"):
        print("WARNING: demo_mode is ON. Every page has noindex and the demo banner. Set demo_mode to false at launch.")
    review = os.path.join(HERE, "removed-service-mentions.txt")
    if REMOVED_MENTIONS:
        with open(review, "w", encoding="utf-8") as f:
            f.write("Sentences that mention services this client does NOT offer. The links were turned into plain text,\n"
                    "but the wording may still imply the service is offered. Reword or remove each one in _build/content_*.py\n"
                    "or _build/pages.py, then rebuild until this file is gone.\n\n")
            for sent, names in sorted(REMOVED_MENTIONS.items()):
                f.write(f"- [{', '.join(sorted(names))}] {sent}\n")
        print(f"CLIENT REVIEW: {len(REMOVED_MENTIONS)} sentence(s) mention services this client does not offer. See _build/removed-service-mentions.txt")
    elif os.path.exists(review):
        os.remove(review)
    if not LOGO_FILE:
        print("CLIENT INPUT NEEDED: no client logo file (config 'logo'); the built-in mark and business name are used.")
    if not SLOTS:
        print("CLIENT INPUT NEEDED: no hero_photo or category_photos; the drawn artwork fills the picture slots.")
    for k in ["domain", "phone_display", "email", "form_endpoint"]:
        if "example" in str(CFG[k]) or "555-01" in str(CFG[k]):
            print(f"WARNING: {k} still has a sample value: {CFG[k]}")

if __name__ == "__main__":
    main()

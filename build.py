# -*- coding: utf-8 -*-
"""Statischer Build des Strandkompass nach dem Muster von Vogelkompass und Waldtierkompass."""
import os, json, shutil, html, random, subprocess
from data import SPECIES, PAIRS, EXT, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS, SEA_NOTE
CREDITS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "credits.json"), encoding="utf-8"))

SITE = "Strandkompass"
DOMAIN = "https://strandkompass.de"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MSHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
BY = {s["k"]: s for s in SPECIES}
PAIRBY = {p["k"]: p for p in PAIRS}
TAG = "schobiwan-21"

esc = lambda s: html.escape(str(s), quote=True)

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def art_of(key):
    if key in BY:
        return BY[key]["art"], BY[key]["grp"]
    e = EXT[key]
    grp = {"felid": "Raubtiere", "canid_large": "Raubtiere", "mustelid_small": "Raubtiere", "newt": "Amphibien",
           "lizard": "Reptilien", "rodent": "Kleinsäuger"}[e["art"]]
    return e["art"], grp

def name_of(key):
    return BY[key]["n"] if key in BY else EXT[key]["n"]

def lat_of(key):
    return BY[key]["lat"] if key in BY else EXT[key]["lat"]

def ein(g, case="nom"):
    if case == "dat":
        return "der" if g == "f" else "dem"
    return "eine" if g == "f" else "ein"

def mlist(ms):
    ms = list(ms)
    if len(ms) == 12:
        return "ganzjährig"
    names = [MONTHS[m - 1] for m in ms]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " und " + names[-1]

def mrange(ms):
    ms = sorted(ms)
    if len(ms) == 12:
        return "ganzjährig"
    return f"{MONTHS[ms[0]-1]} bis {MONTHS[ms[-1]-1]}"

# ------------------------------------------------------------------ Icons
ICON = {
 "find": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>',
 "track": '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="15.5" rx="4" ry="3.5"/><circle cx="6.5" cy="10" r="1.7"/><circle cx="10" cy="6.5" r="1.7"/><circle cx="14" cy="6.5" r="1.7"/><circle cx="17.5" cy="10" r="1.7"/></svg>',
 "pair": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="8" height="12" rx="2"/><rect x="13" y="6" width="8" height="12" rx="2"/></svg>',
 "year": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 "arrow": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"></path></svg>',
 "wave": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9c2.2 0 2.2-2 4.5-2S9.8 9 12 9s2.3-2 4.5-2S18.8 9 21 9M3 15c2.2 0 2.2-2 4.5-2s2.3 2 4.5 2 2.3-2 4.5-2 2.3 2 4.5 2"/></svg>',
 "bird": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 14c3.5 0 5.5-1.6 7-4.5C11.4 6.8 13.2 5 16 5c2 0 3.6 1.3 4 3l1.5.6-1.6.9c-.4 4.6-3.8 8.5-9.4 8.5H6.5"/><path d="M9 17.5 7.5 20M12 17.5 11 20"/><circle cx="16.3" cy="8.2" r=".6" fill="currentColor" stroke="none"/></svg>',
 "seas": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4.5h7v15H4zM13 4.5h7v15h-7z"/><path d="M5.5 14c1 0 1-1 2-1s1 1 2 1M14.5 14c1 0 1-1 2-1s1 1 2 1"/></svg>',
 "nord": '<svg viewBox="0 0 16 16" aria-hidden="true"><text x="8" y="11.6" text-anchor="middle" font-size="10" font-weight="700" font-family="sans-serif" fill="currentColor" stroke="none">N</text></svg>',
 "ost": '<svg viewBox="0 0 16 16" aria-hidden="true"><text x="8" y="11.6" text-anchor="middle" font-size="10" font-weight="700" font-family="sans-serif" fill="currentColor" stroke="none">O</text></svg>',
}
ACT_ICON = {"nord": "nord", "ost": "ost"}

def icon_symbols():
    out = []
    for k in ("nord", "ost"):
        inner = ICON[k].split(">", 1)[1].rsplit("</svg>", 1)[0]
        out.append(f'<symbol id="i-{k}" viewBox="0 0 16 16">{inner}</symbol>')
    return "".join(out)

def act_svg(a):
    return f'<svg aria-hidden="true"><use href="#i-{ACT_ICON[a]}"></use></svg>'

SPIRAL = '<path d="M24.59 25.31 L24.59 25.41 L24.58 25.51 L24.56 25.61 L24.53 25.71 L24.49 25.81 L24.44 25.91 L24.39 26.01 L24.32 26.11 L24.24 26.20 L24.16 26.29 L24.06 26.38 L23.96 26.46 L23.85 26.53 L23.73 26.60 L23.60 26.66 L23.47 26.72 L23.33 26.76 L23.18 26.80 L23.02 26.82 L22.87 26.84 L22.70 26.84 L22.54 26.84 L22.37 26.82 L22.19 26.79 L22.02 26.75 L21.85 26.70 L21.67 26.63 L21.50 26.55 L21.33 26.46 L21.16 26.36 L20.99 26.24 L20.83 26.11 L20.67 25.97 L20.53 25.82 L20.38 25.66 L20.25 25.48 L20.12 25.29 L20.01 25.09 L19.90 24.88 L19.81 24.66 L19.72 24.44 L19.65 24.20 L19.60 23.96 L19.55 23.71 L19.53 23.45 L19.51 23.19 L19.51 22.92 L19.53 22.65 L19.57 22.38 L19.62 22.10 L19.69 21.83 L19.77 21.55 L19.87 21.28 L19.99 21.01 L20.13 20.74 L20.28 20.48 L20.45 20.22 L20.64 19.97 L20.85 19.73 L21.07 19.50 L21.31 19.28 L21.56 19.07 L21.83 18.87 L22.11 18.68 L22.41 18.51 L22.72 18.36 L23.04 18.22 L23.37 18.10 L23.71 17.99 L24.06 17.91 L24.43 17.84 L24.79 17.79 L25.17 17.77 L25.55 17.76 L25.93 17.78 L26.32 17.82 L26.71 17.88 L27.09 17.96 L27.48 18.07 L27.86 18.20 L28.24 18.35 L28.62 18.52 L28.99 18.72 L29.35 18.94 L29.70 19.18 L30.04 19.45 L30.36 19.73 L30.68 20.04 L30.98 20.36 L31.26 20.71 L31.53 21.07 L31.78 21.46 L32.01 21.86 L32.21 22.27 L32.40 22.70 L32.57 23.14 L32.71 23.60 L32.82 24.07 L32.91 24.54 L32.98 25.03 L33.01 25.52 L33.02 26.02 L33.01 26.52 L32.96 27.03 L32.89 27.53 L32.79 28.04 L32.65 28.54 L32.49 29.04 L32.30 29.53 L32.09 30.02 L31.84 30.50 L31.57 30.96 L31.26 31.42 L30.94 31.86 L30.58 32.28 L30.20 32.69 L29.79 33.08 L29.36 33.45 L28.91 33.79 L28.43 34.12 L27.94 34.42 L27.42 34.69 L26.89 34.94 L26.34 35.16 L25.77 35.35 L25.19 35.50 L24.60 35.63 L24.00 35.73 L23.39 35.79 L22.77 35.82 L22.15 35.82 L21.53 35.78 L20.90 35.71 L20.27 35.60 L19.65 35.46 L19.03 35.28 L18.42 35.06 L17.82 34.82 L17.22 34.53 L16.64 34.22 L16.08 33.87 L15.53 33.48 L15.00 33.07 L14.49 32.62 L14.00 32.15 L13.54 31.64 L13.10 31.11 L12.69 30.55 L12.31 29.96 L11.95 29.35 L11.63 28.72 L11.35 28.07 L11.09 27.40 L10.88 26.71 L10.70 26.01 L10.56 25.29 L10.45 24.57 L10.39 23.83 L10.37 23.09 L10.38 22.34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>'
LOGO = ('<svg class="logo-defs" aria-hidden="true" focusable="false"><symbol id="logo-mark" viewBox="0 0 48 48">'
        '<circle cx="24" cy="24" r="21" fill="none" stroke="currentColor" stroke-width="2.2"></circle>'
        '<circle cx="24" cy="24" r="17" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity=".6"></circle>'
        + SPIRAL + '<path d="M24 1.8 26.6 7.4H21.4z" fill="var(--logo-accent)"></path>'
        '</symbol>' + icon_symbols() + '</svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#33413f"/>'
           '<circle cx="24" cy="25" r="17.5" fill="none" stroke="#f3eee3" stroke-width="2.4"/>'
           '<g color="#f3eee3" transform="translate(0 1)">' + SPIRAL + '</g><path d="M24 4.5 27 10.5H21z" fill="#ef7a5a"/></svg>')

LDJSON = ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/",
          "inLanguage": "de-DE", "description": "Strandfunde an Nord- und Ostsee bestimmen: Muscheln, Quallen, Krebse, Bernstein und mehr."}, ensure_ascii=False) + '</script>')

TABS = [("index", "Bestimmen", "Funde", "find"), ("nordsee-ostsee", "Nord- & Ostsee", "Meere", "seas"), ("am-strand", "Am Strand", "Strand", "wave"),
        ("unterscheiden", "Doppelgänger", "Vergleich", "pair"), ("strandjahr", "Strandjahr", "Jahr", "year")]

# Gewähltes Meer früh setzen, damit beim Laden nichts springt
SEA_BOOT = '<script>try{var s=localStorage.getItem("sk-sea");if(s==="nord"||s==="ost")document.documentElement.dataset.sea=s}catch(e){}</script>'

def seaswitch(extra=""):
    """Umschalter Beide · Nordsee · Ostsee; app.js merkt sich die Wahl."""
    b = lambda v, t: f'<button type="button" class="seabtn" data-sea-set="{v}" aria-pressed="{"true" if not v else "false"}">{t}</button>'
    return (f'<div class="seasw{(" " + extra) if extra else ""}" role="group" aria-label="Meer wählen">'
            f'{b("", "Beide Meere")}{b("nord", "Nordsee")}{b("ost", "Ostsee")}</div>')

def seabar(R):
    return (f'<div class="seabar"><div class="wrap seabar-in"><span class="seabar-l">Zeige Funde von</span>{seaswitch()}'
            f'<a class="seabar-more" href="{R}nordsee-ostsee/index.html">Was ist der Unterschied?</a></div></div>')

def acts_attr(acts):
    return "|".join(acts)

def counts(ss, label_one=None):
    """Zahl, die sich beim Umschalten des Meeres anpasst."""
    a = len(ss); n = sum(1 for x in ss if "nord" in x["act"]); o = sum(1 for x in ss if "ost" in x["act"])
    return f'<span data-cnt-all="{a}" data-cnt-nord="{n}" data-cnt-ost="{o}">{a}</span>'


# ------------------------------------------------------------------ Layout
def page(path, title, desc, body, active=None, scripts=(), crumbs=None, data=None, is_home=False, og="og.jpg", seafilter=True):
    depth = path.count("/")
    R = "../" * depth
    canon = DOMAIN + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)
    tabs = []
    for key, label, short, ic in TABS:
        href = R + ("index.html" if key == "index" else f"{key}/index.html")
        cur = ' aria-current="page"' if active == key else ""
        tabs.append(f'<li><a class="tab" href="{href}"{cur}> {ICON[ic]}<span class="tl">{label}</span><span class="ts">{short}</span> </a></li>')
    cr = ""
    if crumbs:
        items = [f'<li><a href="{R}index.html">Start</a></li>']
        for (lab, href) in crumbs[:-1]:
            items.append(f'<li><a href="{R}{href}">{esc(lab)}</a></li>')
        items.append(f'<li><span aria-current="page">{esc(crumbs[-1][0])}</span></li>')
        cr = f'<nav class="crumbs wrap" aria-label="Brotkrumen"><ol> {" ".join(items)} </ol></nav>'
    dj = f'<script type="application/json" id="wk-data">{json.dumps(data, ensure_ascii=False)}</script>' if data is not None else ""
    sc = f'<script type="module" src="{R}assets/{(scripts[0] if scripts else "app.js")}"></script>'
    full_title = title if is_home else f"{title} · {SITE}"
    return f'''<!DOCTYPE html><html lang="de" data-root="{R or './'}" data-index> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}"><meta name="theme-color" content="#33413f" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#1b2423" media="(prefers-color-scheme: dark)"><meta name="color-scheme" content="light dark">{SEA_BOOT}<link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="preload" href="{R}fonts/young-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{R}fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="de_DE"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/photos/{og}"><meta name="twitter:card" content="summary_large_image">{LDJSON if is_home else ""}<link rel="stylesheet" href="{R}assets/site.css"></head> <body> {LOGO} <a class="skip" href="#main">Zum Inhalt springen</a> <nav class="appnav" aria-label="Hauptnavigation"> <div class="wrap"> <a class="brand" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span><span class="sr-only">, zur Startseite</span></a> <ul class="tabs"> {"".join(tabs)} </ul> </div> </nav> <main id="main" tabindex="-1"{' class="seafilter"' if seafilter else ""}> {cr} {body} </main> {footer(R)} {dj}{sc} </body> </html>'''

def footer(R):
    ent = [("arten/index.html", "Alle Strandfunde"), ("nordsee-ostsee/index.html", "Nordsee und Ostsee"), ("am-strand/index.html", "Sicher am Strand"), ("unterscheiden/index.html", "Doppelgänger unterscheiden"),
           ("strandjahr/index.html", "Strandjahr und Kalender"), ("ausruestung/index.html", "Ausrüstung")]
    leg = [("impressum/index.html", "Impressum"), ("datenschutz/index.html", "Datenschutz"), ("bildnachweis/index.html", "Bildnachweis und Lizenzen")]
    li = lambda xs: "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in xs)
    return f'''<footer> <div class="wrap"> <a class="flogo" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span></a> <div class="fcols"> <nav aria-label="Entdecken"><p class="fhead">Entdecken</p><ul>{li(ent)}</ul></nav> <nav aria-label="Rechtliches"><p class="fhead">Rechtliches</p><ul>{li(leg)}</ul></nav> <nav aria-label="Schwesterseiten"><p class="fhead">Schwesterseiten</p><ul><li><a href="https://vogelkompass.de/" rel="noopener">Vogelkompass: Vögel bestimmen</a></li><li><a href="https://waldtierkompass.de/" rel="noopener">Waldtierkompass: Waldtiere bestimmen</a></li></ul></nav> </div> <p class="footnote">Fotos: Wikimedia Commons, unter freien Lizenzen. Mit * markierte Links sind Werbelinks. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> </div> </footer>'''

# ------------------------------------------------------------------ Bausteine
def img(R, key, alt="", eager=False, cls="", sizes="(max-width: 600px) 92vw, 400px"):
    lz = "eager" if eager else "lazy"
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{R}photos/{key}.webp" srcset="{R}photos/{key}-400.webp 400w, {R}photos/{key}.webp 720w" sizes="{sizes}" '
            f'alt="{esc(alt)}" width="720" height="576" loading="{lz}" decoding="async">')

def lic_url(lic):
    """Link auf den Lizenztext (Creative Commons verlangt ihn bei jeder Nutzung)."""
    import re as _re
    m = _re.match(r"CC (BY(?:-SA)?) (\d\.\d)(?: (\w\w))?$", lic)
    if m:
        return f"https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/" + (f"{m.group(3)}/" if m.group(3) else "")
    if lic == "CC0":
        return "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
    return ""

def lic_link(lic):
    u = lic_url(lic)
    return f'<a href="{u}" target="_blank" rel="noopener license">{esc(lic)}</a>' if u else esc(lic)

def credit_parts(a, lic, url):
    return (f'Foto: <a href="{esc(url)}" target="_blank" rel="noopener">{esc(a)}</a>, {lic_link(lic)}')

def credit(key, short=False):
    a, lic, url = CREDITS[key]
    return credit_parts(a, lic, url) + ("" if short else ", Wikimedia Commons, zugeschnitten")

def cred(key):
    """Kleine Bildangabe direkt auf dem Foto, liegt über dem Kartenlink."""
    return f'<small class="cred">{credit(key, True)}</small>'

def card(R, s, i=0, hidden=False):
    acts = "".join(f'<span class="act" title="{ACTS[a]}">{act_svg(a)}<span class="sr-only">{ACTS[a]}</span></span>' for a in s["act"])
    search = " ".join([s["n"], s["lat"], s["grp"]] + [ACTS[a] for a in s["act"]])
    return (f'<li class="bird" id="{s["k"]}" style="--i:{i}" data-key="{s["k"]}" data-name="{esc(s["n"])}" data-search="{esc(search)}" '
            f'data-grp="{esc(s["grp"])}" data-act="{"|".join(s["act"])}" data-hab="{esc("|".join(s["hab"]))}" data-size="{s["size"]}" data-mid="{s["mid"]}" '
            f'data-present="{",".join(map(str, s["p"]))}" data-peak="{",".join(map(str, s["h"]))}"{" hidden" if hidden else ""}> '
            f'{img(R, s["k"], "", eager=i < 6)}{cred(s["k"])} <div class="txt"> <h3><a class="open" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></h3> '
            f'<span class="meta"><span class="latin" lang="la">{esc(s["lat"])}</span><span class="size">{esc(s["sz"])}</span></span> '
            f'<span class="row"><span class="tag status">{esc(s["grp"])}</span></span> <p class="short">{esc(s["short"])}</p> </div> '
            f'<span class="acts">{acts}</span> </li>')

def months_bar(s):
    out = []
    for m in range(1, 13):
        cls = "h" if m in s["h"] else ("p" if m in s["p"] else "")
        t = "Hauptzeit" if cls == "h" else ("aktiv" if cls == "p" else "kaum zu sehen")
        out.append(f'<span data-month="{m}" class="{cls}" title="{MONTHS[m-1]}: {t}">{MSHORT[m-1]}</span>')
    return f'<div class="months" aria-hidden="true"> {"".join(out)} </div>'

PRODUCTS = {
 "uvlampe": dict(cat="Bernsteinsuche", name="UV-Taschenlampe 365 nm", by="Auswahl bei Amazon", tip=True, icon="lamp",
   why="Bernstein leuchtet unter UV-Licht bläulich bis gelb und fällt so im Tangsaum sofort auf. Nicht in die Augen leuchten.",
   url="https://www.amazon.de/s?k=uv+taschenlampe+365nm&tag=" + TAG),
 "buch": dict(cat="Buch", name="Bestimmungsbuch Strand und Küste", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Ein handliches Bestimmungsbuch für Muscheln, Schnecken, Quallen und Strandfunde an Nord- und Ostsee passt in jede Strandtasche.",
   url="https://www.amazon.de/s?k=bestimmungsbuch+strand+k%C3%BCste+nordsee+ostsee&tag=" + TAG),
 "becherlupe": dict(cat="Für Kinder", name="Becherlupe", by="Auswahl bei Amazon", tip=False, icon="lens",
   why="Krabbe, Garnele oder Seestachelbeere kurz in Meerwasser setzen und von allen Seiten vergrößert anschauen. Danach zurück ins Wasser.",
   url="https://www.amazon.de/s?k=becherlupe+kinder&tag=" + TAG),
 "kescher": dict(cat="Für Kinder", name="Kescher mit Teleskopstiel", by="Auswahl bei Amazon", tip=False, icon="net",
   why="Für Garnelen und kleine Krebse im Priel. Ein feines Netz schont die Tiere.",
   url="https://www.amazon.de/s?k=kescher+teleskop+kinder&tag=" + TAG),
 "forscherset": dict(cat="Für Kinder", name="Eimer-Set für Strandforscher", by="Auswahl bei Amazon", tip=False, icon="bucket",
   why="Eimer, Schaufel und Sieb für Sandburgen und zum kurzen Anschauen von Strandfunden.",
   url="https://www.amazon.de/s?k=strandspielzeug+set+eimer+sieb&tag=" + TAG),
 "wattschuhe": dict(cat="Watt", name="Wattschuhe", by="Auswahl bei Amazon", tip=False, icon="shoe",
   why="Schützen im Watt vor scharfen Austern, Seepocken und Muschelschalen und sitzen auch im Schlick fest am Fuß.",
   url="https://www.amazon.de/s?k=wattschuhe&tag=" + TAG),
 "fernglas": dict(cat="Fernglas", name="Celestron Nature DX 8x42", by="Celestron", tip=False, icon="binoc",
   why="Für Seevögel im Watt und Robben auf der Sandbank, aus sicherem Abstand. 8-fache Vergrößerung, wasserdicht und leicht.",
   url="https://www.amazon.de/dp/B00B73JONS?tag=" + TAG),
 "vogelbuch": dict(cat="Buch", name="Vogelführer für Küste und Meer", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Möwen, Watvögel und Seeschwalben ähneln sich oft. Ein Vogelführer mit Bildern der Jugend- und Winterkleider hilft beim Bestimmen.",
   url="https://www.amazon.de/s?k=vogelf%C3%BChrer+k%C3%BCste+seev%C3%B6gel&tag=" + TAG),
 "sammelbox": dict(cat="Sammeln", name="Sortierbox für Muscheln und Steine", by="Auswahl bei Amazon", tip=False, icon="box",
   why="Mit vielen kleinen Fächern, damit zerbrechliche Funde wie Herzigel und Plattmuscheln heil nach Hause kommen.",
   url="https://www.amazon.de/s?k=sortierbox+f%C3%A4cher+klein&tag=" + TAG),
 "strandmuschel": dict(cat="Strandtag", name="Strandmuschel mit UV-Schutz", by="Auswahl bei Amazon", tip=False, icon="tent",
   why="Schützt an windigen Tagen vor Sonne und Sand. Achte auf einfachen Aufbau und ein kleines Packmaß.",
   url="https://www.amazon.de/s?k=strandmuschel+uv+schutz&tag=" + TAG),
}
PHOTO = {
 "uvlampe": ("Amber Bugs", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Dominican_Amber_Fossilized_Wasp_Enhydro_02.png"),
 "forscherset": ("David", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Sand_bucket.jpg"),
}
GEAR_GRP = {
 "Seevögel": ["fernglas", "vogelbuch", "strandmuschel"],
 "Muscheln": ["buch", "sammelbox", "wattschuhe"],
 "Schnecken": ["buch", "becherlupe", "sammelbox"],
 "Quallen": ["buch", "becherlupe", "strandmuschel"],
 "Krebse & Würmer": ["kescher", "becherlupe", "wattschuhe"],
 "Seesterne & Seeigel": ["sammelbox", "buch", "becherlupe"],
 "Tang & Seegras": ["buch", "becherlupe", "wattschuhe"],
 "Strandfunde": ["uvlampe", "sammelbox", "buch"],
 "Meeressäuger": ["fernglas", "buch", "strandmuschel"],
}
GEAR_FOR = {
 "bernstein": ["uvlampe", "sammelbox", "buch"],
 "nordseegarnele": ["kescher", "becherlupe", "forscherset"],
 "strandkrabbe": ["kescher", "becherlupe", "forscherset"],
 "auster": ["wattschuhe", "buch", "sammelbox"],
}
PICON = {
 "binoc": '<circle cx="8" cy="15" r="4.5"/><circle cx="16" cy="15" r="4.5"/><path d="M8 10.5V6h3v6M16 10.5V6h-3v6"/>',
 "lamp": '<path d="M9 3h6v5l-1 2v10h-4V10L9 8z"/><path d="M12 13v3"/>',
 "book": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
 "lens": '<circle cx="10" cy="10" r="5.5"/><path d="m14 14 6 6"/>',
 "net": '<path d="M4 20 11 13"/><ellipse cx="15" cy="9" rx="5.5" ry="4.5" transform="rotate(-45 15 9)"/><path d="M12 6l6 6M14 4.5l5.5 5.5"/>',
 "bucket": '<path d="M5 8h14l-1.5 12h-11z"/><path d="M5 8c0-4 14-4 14 0"/>',
 "shoe": '<path d="M3 15c0-3 1-7 3-7 1 0 2 2 4 3s7 1 9 3 2 3 2 3H3z"/><path d="M3 18h18"/>',
 "box": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M9 6v12M15 6v12M3 12h18"/>',
 "tent": '<path d="M3 19C3 10 8 5 14 5s7 6 7 14z"/><path d="M14 5c-3 3-4 8-4 14"/>',
}

def product(R, key, compact=False):
    p = PRODUCTS[key]
    tip = '<span class="ptip">Unser Tipp</span>' if p["tip"] and not compact else ""
    why = f'<p class="pwhy">{esc(p["why"])}</p>' if not compact else ""
    meta = f'<span>{p["cat"]}{" · Unser Tipp" if (p["tip"] and compact) else ""}</span>'
    pic = (f'<img src="{R}photos/p-{key}-400.webp" srcset="{R}photos/p-{key}-400.webp 400w, {R}photos/p-{key}.webp 720w" '
           f'sizes="{"88px" if compact else "(max-width: 600px) 92vw, 360px"}" alt="" width="400" height="300" loading="lazy" decoding="async">'
) if key in PHOTO else f'<span class="picon"><svg viewBox="0 0 24 24" aria-hidden="true">{PICON[p["icon"]]}</svg></span>'
    under = f'<small class="pcred">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (key in PHOTO and not compact) else ""
    return (f'<li class="product{" pick" if p["tip"] else ""}"> <div class="pimg">{pic}{tip}</div>{under} '
            f'<div class="pbody"> <p class="pmeta">{meta}<span class="pad">Anzeige</span></p> <h3 class="pname">{esc(p["name"])}</h3> <p class="pby">{esc(p["by"])}</p> {why} {f'<small class="pcred2">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (compact and key in PHOTO) else ""} '
            f'<a class="plink" href="{p["url"]}" target="_blank" rel="sponsored nofollow noopener"><span>Bei Amazon ansehen<span aria-hidden="true">*</span></span>{ICON["arrow"]}'
            f'<span class="sr-only"> {esc(p["name"])} (Werbelink, öffnet in neuem Fenster)</span></a> </div> </li>')

ADNOTE = '<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Wenn du über diesen Link etwas kaufst, erhält der Strandkompass eine kleine Provision von Amazon. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>'

def pair_card(R, p, h="h2"):
    figs = "".join(f'<figure>{img(R, k if k in BY else "x-" + k)}<figcaption>{esc(name_of(k))}<small>{credit(k if k in BY else "x-" + k, True)}</small></figcaption></figure>' for k in (p["a"], p["b"]))
    return (f'<li class="pair"> <div class="ph" aria-hidden="true"> {figs} </div> <div class="pb"> <{h}><a class="pair-link" href="{R}unterscheiden/{p["k"]}/index.html">'
            f'{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</a></{h}> <p>{esc(p["short"])}</p> <span class="to" aria-hidden="true">Alle Unterschiede</span> </div> </li>')

def chipset(legend, g, items):
    return f'<fieldset><legend>{legend}</legend><div class="fchips">' + "".join(
        f'<button class="chip" type="button" data-g="{g}" data-v="{esc(v)}" aria-pressed="false">{esc(t)}</button>' for v, t in items) + '</div></fieldset>'

# ------------------------------------------------------------------ Seiten
# Spierentonne (rot-weiß) als kleines Zeichen
BUOY = ('<svg class="buoy" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 16 17H8z" fill="var(--rust)"/>'
        '<path d="M10.2 9h3.6l1 3.8H9.2z" fill="#fff"/><path d="M5 19.5c1.4 0 1.4-1.2 2.8-1.2s1.4 1.2 2.8 1.2 1.4-1.2 2.8-1.2 1.4 1.2 2.8 1.2 1.4-1.2 2.8-1.2" fill="none" stroke="var(--seen)" stroke-width="1.6" stroke-linecap="round"/></svg>')
# Rippelmarken wie im Watt bei Ebbe
def _ripples():
    import math
    paths = []
    for i in range(7):
        y0 = 18 + i * 15; amp = 3.2 + (i % 3) * .9; ph = i * 1.3; per = 46 + (i % 2) * 10
        pts = " ".join(f"{x:.0f},{y0 + amp * math.sin(x / per + ph) + 1.6 * math.sin(x / 13 + ph * 2):.1f}" for x in range(0, 1441, 12))
        paths.append(f'<polyline points="{pts}"/>')
    return ('<svg class="h6-ripples" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true" focusable="false">' + "".join(paths) + '</svg>')
RIPPLES = _ripples()

BIRD_PRIO = ["eiderente", "basstoelpel", "trottellumme", "austernfischer", "saebelschnaebler", "brandgans", "ringelgans", "sanderling",
             "alpenstrandlaeufer", "mantelmoewe", "flussseeschwalbe", "silbermoewe", "kormoran", "sturmmoewe", "lachmoewe", "heringsmoewe"]

def birdband(R):
    birds = sorted([x for x in SPECIES if x["grp"] == "Seevögel"], key=lambda x: BIRD_PRIO.index(x["k"]) if x["k"] in BIRD_PRIO else 99)
    tiles = "".join(
        f'<li data-act="{acts_attr(x["act"])}"><a href="{R}arten/{x["k"]}/index.html"><img src="{R}photos/{x["k"]}-400.webp" alt="" width="400" height="320" loading="lazy" decoding="async">'
        f'<span class="bt-n">{esc(x["n"])}</span><span class="bt-s">{esc(x["sz"])}{" · nur Nordsee" if x["act"] == ["nord"] else ""}</span></a>{cred(x["k"])}</li>' for x in birds)
    return (f'<section class="birdband" aria-labelledby="bb-h"> <div class="wrap"> <div class="bb-head"><div><p class="kicker">{ICON["bird"]}Zuerst die Seevögel</p>'
            f'<h2 id="bb-h">Seevögel an der Küste</h2><p class="bb-sub">Möwen, Watvögel, Meeresenten und die Felsenbrüter von Helgoland: {counts(birds)} Arten, die dir an Nord- und Ostsee begegnen.</p></div>'
            f'<div class="bb-links"><button type="button" class="btn" data-hgrp="Seevögel">Alle Seevögel in der Liste</button><a class="btn ghost" href="{R}unterscheiden/index.html#voegel">Möwen unterscheiden</a></div></div>'
            f'<ul class="birdtiles">{tiles}</ul> </div> </section>')

def seapair(R):
    def card_(k, title, facts, txt):
        n = sum(1 for x in SPECIES if k in x["act"]); only = sum(1 for x in SPECIES if x["act"] == [k])
        lis = "".join(f"<li>{esc(f)}</li>" for f in facts)
        return (f'<li class="seacard seacard-{k}"><a href="{R}{"nordsee" if k == "nord" else "ostsee"}/index.html"><b>{title}</b><span>{esc(txt)}</span>'
                f'<ul>{lis}</ul><span class="sc-n">{n} Arten und Funde{f", {only} davon nur hier" if only else ""}</span></a></li>')
    return (f'<section class="block seapair" aria-labelledby="sp-h"><div class="wrap"><h2 id="sp-h">Nordsee oder Ostsee?</h2>'
            f'<p class="intro">Die beiden Meere sind sehr verschieden. Das merkst du schon daran, was am Strand liegt und welche Vögel dort leben.</p><ul class="seacards">'
            + card_("nord", "Nordsee", ["Ebbe und Flut, 2 bis 4 Meter Unterschied", "Wattenmeer, Halligen und Sandbänke", "Seehunde, Basstölpel und Trottellummen"],
                    "Salziges Gezeitenmeer mit dem Wattenmeer, einem der wichtigsten Rastgebiete für Zugvögel weltweit.")
            + card_("ost", "Ostsee", ["Kaum Gezeiten, der Wind bestimmt den Wasserstand", "Viel weniger Salz als die Nordsee", "Bernstein, Feuersteine und Steilküsten"],
                    "Ein fast geschlossenes Binnenmeer mit Bodden, Förden und Steilküsten. Im Winter rasten hier riesige Entenschwärme.")
            + f'</ul><p class="actions"><a class="btn ghost" href="{R}nordsee-ostsee/index.html">Alle Unterschiede im Vergleich</a></p></div></section>')

def build_home():
    R = ""
    filt = (chipset("Gruppe", "grp", [(g, g) for g in GROUPS]) +
            chipset("Meer", "act", [(k, v) for k, v in ACTS.items()]) +
            chipset("Lebensraum", "hab", [(h, h) for h in HABS]) +
            chipset("Größe", "size", list(SIZES.items())) +
            '<fieldset><legend>Außerdem</legend><div class="fchips"><button class="chip" type="button" data-g="flag" data-v="now" aria-pressed="false">Jetzt im <span data-now-name>November</span> zu finden</button>'
            '</div></fieldset>')
    cards = "".join(card(R, s, i) for i, s in enumerate(sorted(SPECIES, key=lambda x: (x["grp"] != "Seevögel", x["n"]))))
    NOWM_BUILD = 11
    # Reihenfolge für Tier des Monats und Karussell: auffällige Funde zuerst
    PRIO = BIRD_PRIO + ["kegelrobbe", "seehund", "schweinswal", "bernstein", "kompassqualle", "feuerqualle", "ohrenqualle", "lungenqualle", "seestern",
            "nixentaeschchen", "wellhornschnecke", "strandkrabbe", "einsiedlerkrebs", "seestachelbeere", "blaue-nesselqualle", "herzigel", "donnerkeil"]
    pr = lambda x: PRIO.index(x["k"]) if x["k"] in PRIO else 99
    ranked = sorted(SPECIES, key=lambda x: (0 if NOWM_BUILD in x["h"] else 1, pr(x), x["n"]))
    def nowcard(x, i):
        first = x["hl"].split(". ")[0].rstrip(".") + "."
        return (f'<li data-act="{acts_attr(x["act"])}" data-bird="{1 if x["grp"] == "Seevögel" else 0}" data-peak="{",".join(map(str, x["h"]))}" data-present="{",".join(map(str, x["p"]))}" data-k="{x["k"]}" data-name="{esc(x["n"])}" '
                f'data-hl="{esc(first)}"{"" if NOWM_BUILD in x["p"] else " hidden"}>'
                f'<a href="arten/{x["k"]}/index.html"><img src="photos/{x["k"]}-400.webp" alt="" width="400" height="300" loading="{"eager" if i < 5 else "lazy"}" decoding="async">'
                f'<span class="nc-ov"><b>{esc(x["n"])}</b><i>Beste Zeit</i></span></a>{cred(x["k"])}</li>')
    nowc = "".join(nowcard(x, i) for i, x in enumerate(ranked))
    sp = ranked[0]
    sp_first = sp["hl"].split(". ")[0].rstrip(".") + "."
    gcount = {g: sum(1 for x in SPECIES if x["grp"] == g) for g in GROUPS}
    gchips = "".join(f'<button type="button" class="hchip" data-hgrp="{g}">{g}<span>{gcount[g]}</span></button>' for g in GROUPS)
    events = "".join(f'<ul class="h5-events" data-m="{m}"{"" if m == NOWM_BUILD else " hidden"}>' + "".join(ev_li(e) for e in MONTH_EVENTS[m]) + "</ul>" for m in range(1, 13))
    body = f'''<header class="hero6"> <div class="wrap hero6-in"> <div class="h6-text"> <p class="h6-kicker">{BUOY}<span>Nordsee &amp; Ostsee</span><span aria-hidden="true">·</span><span>{counts(SPECIES)} Arten und Funde</span></p> <h1>Wer <em>fliegt</em> da?<br>Was <em>liegt</em> da?</h1> <p class="lede">Seevögel, Muscheln, Quallen und Strandfunde bestimmen: am Foto und an wenigen sicheren Merkmalen.</p> <form class="hsearch" id="hsearch" role="search" aria-label="Fund suchen"> <label for="hq"><span class="sr-only">Fund suchen</span>{ICON["find"]}<input type="search" id="hq" placeholder="Zum Beispiel Austernfischer" autocomplete="off" enterkeyhint="search"></label> <button class="hsearch-btn" type="submit">Suchen</button> </form> <div class="h6-sea"><span class="h6-l">Ich bin an der</span>{seaswitch()}</div> <div class="hchips" role="group" aria-label="Nach Gruppe zeigen">{gchips}</div> </div>
<figure class="spot6" id="spot"> <a href="arten/{sp["k"]}/index.html" id="spot-link" class="s6-photo"><img id="spot-img" src="photos/{sp["k"]}.webp" srcset="photos/{sp["k"]}-400.webp 400w, photos/{sp["k"]}.webp 720w" sizes="(max-width: 900px) 92vw, 560px" alt="" width="720" height="576" fetchpriority="high"></a> <figcaption class="s6-label"><span class="spot-tag">Fund des Monats · <span data-now-name>November</span></span><b id="spot-name">{esc(sp["n"])}</b><span id="spot-hl">{esc(sp_first)}</span></figcaption> <small class="spot-cred" id="spot-cred">{credit(sp["k"], True)}</small> </figure> </div>
<div class="wrap h6-month"><h2 class="h5-mh">Am Strand im <span data-now-name>November</span></h2>{events}</div> {RIPPLES} </header>
{birdband(R)}
<section class="nowband" aria-labelledby="now-h"> <div class="wrap"> <div class="now-head"><h2 id="now-h">Jetzt im <span data-now-name>November</span> zu finden</h2><div class="now-nav"><a href="strandjahr/index.html" data-now-link>Alle im <span data-now-name>November</span></a><button class="cbtn" type="button" id="now-prev" aria-controls="nowcards" aria-label="Vorherige Funde" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14.5 6-6 6 6 6"/></svg></button><button class="cbtn" type="button" id="now-next" aria-controls="nowcards" aria-label="Weitere Funde"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9.5 6 6 6-6 6"/></svg></button></div></div> <ul class="nowcards" id="nowcards">{nowc}</ul> </div> </section>
<div class="bar" id="arten"> <div class="wrap barrow" role="search" aria-label="Funde suchen und filtern"> <label class="search" for="q">{ICON["find"]}<span class="sr-only">Fund suchen</span> <input type="search" id="q" placeholder="Suchen, z. B. Qualle" autocomplete="off" enterkeyhint="search"></label> <button class="chip ftoggle" id="f-toggle" type="button" aria-expanded="false" aria-controls="fpanel"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"></path></svg>Filter<b class="fcount" id="fcount" hidden></b></button> <label class="sortsel" for="sort"><span>Sortieren</span> <select id="sort"><option value="now">Jetzt zu finden zuerst</option><option value="az">Name A–Z</option><option value="size">Größe, klein zuerst</option></select></label> <span class="rcount" id="rcount" aria-live="polite">{len(SPECIES)} Funde</span> </div> <div class="fpanel" id="fpanel" hidden> <div class="wrap fgrid"> {filt} <div class="factions"><button class="btn ghost" id="f-reset" type="button">Alle Filter zurücksetzen</button><button class="btn" id="f-done" type="button">Ergebnisse anzeigen</button></div> </div> </div> <div class="wrap active" id="active" hidden></div> </div>
<section class="sub" aria-labelledby="arten-h"> <div class="wrap"> <h2 class="sr-only" id="arten-h">Funde</h2> <ul class="grid" id="grid"> {cards} </ul> <div class="empty" id="empty" hidden><p>Kein Fund passt zu deiner Suche oder Auswahl.</p><button class="btn ghost" type="button" id="empty-reset">Suche und Filter zurücksetzen</button></div> </div> </section>
{seapair(R)}
<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Gut ausgerüstet an den Strand</h2><a class="gearmore" href="ausruestung/index.html">Alle Empfehlungen ansehen</a></div><ul class="products"> {"".join(product(R, g) for g in ("fernglas", "vogelbuch", "uvlampe", "buch", "becherlupe", "kescher", "wattschuhe", "sammelbox"))} </ul>{ADNOTE}</div></section>
<section class="block"> <div class="wrap"> <h2>Weiter entdecken</h2> <ul class="explore"> <li><a href="am-strand/index.html"><b>Sicher am Strand</b><span>Welche Quallen brennen, was tun bei einem Heuler, und warum du Bernstein nie in die Hosentasche steckst.</span></a></li> <li><a href="unterscheiden/index.html"><b>Doppelgänger unterscheiden</b><span>Silbermöwe oder Heringsmöwe, Ohrenqualle oder Kompassqualle: {len(PAIRS)} Vergleiche mit den entscheidenden Merkmalen.</span></a></li> <li><a href="strandjahr/index.html"><b>Das Strandjahr</b><span>Lummensprung, Vogelzug, Quallenzeit und Bernstein nach dem Sturm: was am Strand wann passiert, Monat für Monat.</span></a></li> <li><a href="ausruestung/index.html"><b>Ausrüstung</b><span>UV-Lampe für die Bernsteinsuche, Becherlupe, Kescher und Wattschuhe.</span></a></li> <li><a href="nordsee-ostsee/index.html"><b>Nordsee oder Ostsee?</b><span>Gezeiten, Salzgehalt, Watt und Steilküste: was die beiden Meere unterscheidet und was du wo findest.</span></a></li> <li><a href="https://vogelkompass.de/" rel="noopener"><b>Noch mehr Vögel</b><span>Garten-, Feld- und Waldvögel bestimmst du auf der Schwesterseite Vogelkompass.</span></a></li> </ul> </div> </section>'''
    write("index.html", page("index.html", "Strandkompass – Seevögel und Strandfunde an Nord- und Ostsee bestimmen",
        f"Seevögel und Strandfunde bestimmen: {len(SPECIES)} Möwen, Watvögel, Muscheln, Quallen, Krebse, Robben und Steine von Nord- und Ostsee mit Doppelgängern und Strandkalender.",
        body, active="index", scripts=("home.js",), is_home=True))

def build_arten_index():
    R = "../"
    sec = []
    for g in GROUPS:
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=lambda x: x["n"])
        sec.append(f'<h2 class="h3 grp-h" data-grp-h="{esc(g)}">{g}</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul>')
    body = seabar(R) + f'<section class="block page"> <div class="wrap"> <h1>Alle Strandfunde</h1> <p class="intro">{counts(SPECIES)} Arten und Funde, nach Gruppen geordnet, die Seevögel zuerst. Zum Suchen und Filtern geht es zur <a href="../index.html#arten">Startseite</a>.</p> {"".join(sec)} </div> </section>'
    write("arten/index.html", page("arten/index.html", "Alle Strandfunde", "Alle Strandfunde im Überblick: Seevögel, Muscheln, Schnecken, Quallen, Krebse, Seesterne, Tang, Steine und Meeressäuger.", body, crumbs=[("Funde", "")]))

def trackbox(s):
    return ""

def seabox(s):
    note = SEA_NOTE.get(s["k"], {})
    cols = ""
    for a in ("nord", "ost"):
        has = a in s["act"]
        txt = note.get(a) or (f"An der {ACTS[a]} zu finden." if has else f"An der {ACTS[a]} kaum oder gar nicht.")
        cols += (f'<div class="seacol seacol-{a}{"" if has else " no"}"><h3>{ACTS[a]}</h3>'
                 f'<p class="seayes">{"Kommt vor" if has else "Kaum oder gar nicht"}</p><p>{esc(txt)}</p></div>')
    return f'<section class="seabox" aria-labelledby="h-sea"><h2 id="h-sea">Nordsee und Ostsee</h2><div class="seacols">{cols}</div></section>'

def build_species(s):
    R = "../../"
    k = s["k"]
    acts = ", ".join(ACTS[a] for a in s["act"])
    habs = "".join(f"<span>{esc(h)}</span>" for h in s["hab"])
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] + [("Meer", acts)])
    life = "".join(f'<details class="fold" open data-fold><summary><h3>{esc(a)}</h3></summary><p>{esc(b)}</p></details>' for a, b in s["life"])
    peaklinks = [f'<a href="{R}strandjahr/{MSLUG[m-1]}/index.html">{MONTHS[m-1]}</a>' for m in s["h"]]
    pl = peaklinks[0] if len(peaklinks) == 1 else ", ".join(peaklinks[:-1]) + " und " + peaklinks[-1]
    yeartext = (f'{"Das" if s["g"]=="n" else ("Die" if s["g"]=="f" else "Der")} {esc(s["n"])} ist {"das ganze Jahr über zu finden" if len(s["p"])==12 else "von " + mrange(s["p"]) + " zu finden"}. '
                f'Am besten im {pl}. {esc(s["hl"])}')
    alike = ""
    if s["alike"]:
        p = PAIRBY[s["alike"]]
        other = p["b"] if p["a"] == k else p["a"]
        okey = other if other in BY else "x-" + other
        alike = (f'<section class="alike" aria-labelledby="h-alike"> {img(R, okey, name_of(other))} <div> <h2 id="h-alike">Nicht verwechseln mit {ein(BY[other]["g"] if other in BY else EXT[other]["g"], "dat")} {esc(name_of(other))}</h2> '
                 f'<p>{esc(p["short"])}</p> <p><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}? Alle Unterschiede</a></p> </div> </section>')
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    gear = GEAR_FOR.get(k) or GEAR_GRP[s["grp"]]
    body = f'''<article class="sp wrap"> <div class="sp-top"> <figure class="sp-photo"> {img(R, k, s["n"], eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> <div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> <p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{"".join(f'<span class="tag act-tag act-{a}">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])}{'<span class="tag act-tag act-none">nicht an der Ostsee</span>' if s["act"] == ["nord"] else ""}</p> <p class="habs">{habs}</p> <p class="text">{esc(s["short"])} {esc(s["hl"])}</p> {trackbox(s)} </div> </div>
<div class="sp-cols"> <div class="sp-main"> <section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {"sie" if s["g"]=="f" else ("es" if s["g"]=="n" else "ihn")}</h2> <ul class="marks">{"".join(f"<li>{esc(m)}</li>" for m in s["marks"])}</ul> <dl class="facts">{facts}</dl> </section> {seabox(s)} <section aria-labelledby="h-year"> <h2 id="h-year">Wann im Jahr</h2> {months_bar(s)} <p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{yeartext}</p> </section> <section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> <section class="helpbox" aria-label="Hilfe und Beobachtung"> <details class="fold" open data-fold><summary><h2>Rücksicht und Sicherheit</h2></summary><p>{esc(s["help"])}</p></details> <details class="fold" open data-fold><summary><h2>Suchtipp</h2></summary><p>{esc(s["tip"])}</p></details> </section> {alike} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> <ul class="morelinks"> <li><a href="{wiki}" target="_blank" rel="noopener">Wikipedia<span class="sr-only"> (öffnet in neuem Fenster)</span></a></li> </ul> </section> </div>
<aside class="sp-side" aria-label="Empfehlungen"> <section class="gearbox" aria-labelledby="h-gear"><h2 id="h-gear">Passend dazu</h2><ul class="products compact"> {"".join(product(R, g, True) for g in gear)} </ul>{ADNOTE}</section> </aside> </div> </article>'''
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", f"{s['n']} erkennen", f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Lebensweise und wann du {'sie' if s['g']=='f' else ('es' if s['g']=='n' else 'ihn')} am Strand findest.",
                                        body, crumbs=[("Funde", "arten/index.html"), (s["n"], "")], og=f"{k}.webp"))

def build_pairs():
    R = "../"
    isb = lambda p: p["a"] in BY and BY[p["a"]]["grp"] == "Seevögel"
    body = (f'<section class="block page"> <div class="wrap"> <h1>Doppelgänger unterscheiden</h1> <p class="intro">Am Strand sieht sich manches zum Verwechseln ähnlich: Möwen, Strandläufer und Seeschwalben ebenso wie Quallen, bei denen der Unterschied sogar wichtig ist. Diese Merkmale helfen beim Unterscheiden.</p>'
            f'<h2 class="h3 grp-h" id="voegel">Seevögel</h2><ul class="pairs">{"".join(pair_card(R, p, "h3") for p in PAIRS if isb(p))}</ul>'
            f'<h2 class="h3 grp-h" id="funde">Strandfunde und Meerestiere</h2><ul class="pairs">{"".join(pair_card(R, p, "h3") for p in PAIRS if not isb(p))}</ul> </div> </section>')
    write("unterscheiden/index.html", page("unterscheiden/index.html", "Doppelgänger unterscheiden", "Silbermöwe oder Heringsmöwe, Sanderling oder Alpenstrandläufer, Ohrenqualle oder Kompassqualle: Seevögel und Strandfunde sicher unterscheiden.", body, active="unterscheiden", crumbs=[("Doppelgänger", "")]))
    for p in PAIRS:
        R = "../../"
        figs = ""
        for k in (p["a"], p["b"]):
            ik = k if k in BY else "x-" + k
            figs += f'<figure>{img(R, ik, name_of(k), eager=True)}<figcaption>{esc(name_of(k))} <i lang="la">{esc(lat_of(k))}</i><small>{credit(ik)}</small></figcaption></figure>'
        rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in p["rows"])
        btns = " ".join(f'<a class="btn{"" if i==0 else " ghost"}" href="{R}arten/{k}/index.html">{esc(name_of(k))} im Porträt</a>' for i, k in enumerate([x for x in (p["a"], p["b"]) if x in BY]))
        others = [q for q in PAIRS if q["k"] != p["k"]]
        rnd = random.Random(p["k"]); rel = rnd.sample(others, 3)
        body = f'''<article class="wrap pairpage"> <h1>{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</h1> <p class="intro">{esc(p["short"])}</p> <div class="ph big"> {figs} </div> <section aria-labelledby="h-cmp"> <h2 id="h-cmp">Die Unterschiede</h2> <div class="cmp-wrap"><table class="cmp"> <thead><tr><td></td><th scope="col">{esc(name_of(p["a"]))}</th><th scope="col">{esc(name_of(p["b"]))}</th></tr></thead> <tbody>{rows}</tbody> </table></div> <p class="merksatz"><b>Merkhilfe:</b> {esc(p["tip"])}</p> <p class="actions"> {btns} </p> </section> <section class="related" aria-labelledby="h-more"> <h2 id="h-more">Weitere Doppelgänger</h2> <ul class="pairs three">{"".join(pair_card(R, q, "h3") for q in rel)}</ul> </section> </article>'''
        write(f"unterscheiden/{p['k']}/index.html", page(f"unterscheiden/{p['k']}/index.html", f"{name_of(p['a'])} oder {name_of(p['b'])}?", p["short"], body, active="unterscheiden",
              crumbs=[("Doppelgänger", "unterscheiden/index.html"), (f"{name_of(p['a'])} oder {name_of(p['b'])}", "")]))

def cal_table(R):
    head = "".join(f'<th scope="col" data-month="{m}"><a href="{R}strandjahr/{MSLUG[m-1]}/index.html"><abbr title="{MONTHS[m-1]}">{MSHORT[m-1]}</abbr></a></th>' for m in range(1, 13))
    rows = []
    for g in GROUPS:
        rows.append(f'<tr class="grow"><th scope="rowgroup" colspan="13">{g}</th></tr>')
        for s in sorted([x for x in SPECIES if x["grp"] == g], key=lambda x: x["n"]):
            tds = ""
            for m in range(1, 13):
                c = "h" if m in s["h"] else ("p" if m in s["p"] else "")
                t = "beste Zeit" if c == "h" else ("zu finden" if c == "p" else "kaum zu finden")
                tds += f'<td data-month="{m}" class="m {c}" title="{esc(s["n"])}, {MONTHS[m-1]}: {t}"><span class="sr-only">{MONTHS[m-1]}: {t}</span></td>'
            rows.append(f'<tr data-act="{acts_attr(s["act"])}"><th scope="row" class="n"><a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></th> {tds} </tr>')
    return f'<div class="cal-wrap"><table class="cal"> <caption class="sr-only">Wann welcher Fund zu erwarten ist</caption> <thead><tr><th scope="col"><span class="sr-only">Art</span></th> {head}</tr></thead> <tbody> {"".join(rows)} </tbody> </table></div>'

def build_year():
    R = "../"
    links = ""
    for m in range(1, 13):
        links += f'<li data-month="{m}"><a href="{R}strandjahr/{MSLUG[m-1]}/index.html"><b>{MONTHS[m-1]}</b><span>{counts([s for s in SPECIES if m in s["p"]])} zu finden, {counts([s for s in SPECIES if m in s["h"]])} in bester Zeit</span></a></li>'
    events = "".join(f'<li data-month="{m}"><b>{MONTHS[m-1]}</b>' + "".join(f'<span data-sea-only="{sea}">{esc(t)}</span>' for sea, t in MONTH_EVENTS[m][:2]) + '</li>' for m in range(1, 13))
    body = seabar(R) + f'''<section class="block page"> <div class="wrap"> <h1>Das Strandjahr</h1> <p class="intro">Was am Strand wann passiert: Vogelzug im Wattenmeer, Lummensprung, Quallenzeit, Heuler und Bernstein nach dem Sturm. Wähle einen Monat, um zu sehen, was du dann findest.</p> <ul class="monthlinks">{links}</ul> </div> </section>
<section class="block" aria-labelledby="h-ev"> <div class="wrap"> <h2 id="h-ev">Das Wichtigste im Jahreslauf</h2> <ul class="yearline">{events}</ul> </div> </section>
<section class="block" aria-labelledby="h-cal"> <div class="wrap"> <h2 id="h-cal">Wann findest du was?</h2> <p class="intro">Monate, in denen du den Fund erwarten kannst, und wann die besten Chancen sind. Der aktuelle Monat ist farbig umrandet.</p> <p class="swipe">Seitlich wischen, um alle Monate zu sehen.</p> {cal_table(R)} </div> </section>'''
    write("strandjahr/index.html", page("strandjahr/index.html", "Das Strandjahr", "Strandkalender für Nord- und Ostsee: wann Quallen, Heuler, Bernstein und Strandfunde zu erwarten sind, Monat für Monat.", body, active="strandjahr", crumbs=[("Strandjahr", "")]))
    for m in range(1, 13):
        R = "../../"
        bf = lambda x: (x["grp"] != "Seevögel", x["n"])
        peak = sorted([s for s in SPECIES if m in s["h"]], key=bf)
        act = sorted([s for s in SPECIES if m in s["p"] and m not in s["h"]], key=bf)
        sleep = sorted([s for s in SPECIES if m not in s["p"]], key=lambda x: x["n"])
        ev = "".join(ev_li(e, True) for e in MONTH_EVENTS[m])
        prev_m, next_m = (m - 2) % 12 + 1, m % 12 + 1
        sl = (f'<section class="block" aria-labelledby="h-sl"><div class="wrap"><h2 id="h-sl">Jetzt kaum zu finden</h2><div class="pills">'
              + "".join(f'<a data-act="{acts_attr(s["act"])}" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a>' for s in sleep) + '</div></div></section>') if sleep else ""
        body = seabar(R) + f'''<section class="block page"> <div class="wrap"> <h1>Der Strand im {MONTHS[m-1]}</h1> <p class="intro">{counts(peak + act)} der {counts(SPECIES)} Arten und Funde kannst du im {MONTHS[m-1]} erwarten, {counts(peak)} davon besonders häufig.</p> <ul class="evlist">{ev}</ul> <p class="actions"><a class="btn ghost" href="{R}strandjahr/{MSLUG[prev_m-1]}/index.html">← {MONTHS[prev_m-1]}</a> <a class="btn ghost" href="{R}strandjahr/{MSLUG[next_m-1]}/index.html">{MONTHS[next_m-1]} →</a></p> </div> </section>
<section class="block" aria-labelledby="h-pk"><div class="wrap"><h2 id="h-pk">Jetzt besonders gut zu finden</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(peak))}</ul></div></section>
<section class="block" aria-labelledby="h-ac"><div class="wrap"><h2 id="h-ac">Außerdem zu finden</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(act))}</ul></div></section> {sl} {month_gear(R, m)}'''
        write(f"strandjahr/{MSLUG[m-1]}/index.html", page(f"strandjahr/{MSLUG[m-1]}/index.html", f"Am Strand im {MONTHS[m-1]}", f"Was du im {MONTHS[m-1]} an Nord- und Ostsee findest: {MONTH_EVENTS[m][0][1]}", body, active="strandjahr",
              crumbs=[("Strandjahr", "strandjahr/index.html"), (MONTHS[m-1], "")]))

SEA_LBL = {"nord": "Nordsee", "ost": "Ostsee", "beide": "Nord- und Ostsee"}

def ev_li(e, tag=False):
    sea, t = e
    lab = f'<span class="evsea evsea-{sea}">{SEA_LBL[sea]}</span> ' if tag else ""
    return f'<li data-sea-only="{sea}">{lab}{esc(t)}</li>'

def month_gear(R, m):
    picks = ("uvlampe", "sammelbox", "fernglas", "buch") if m in (10, 11, 12, 1, 2, 3) else ("becherlupe", "kescher", "wattschuhe", "strandmuschel")
    return (f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Passend zum {MONTHS[m-1]}</h2><a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div>'
            f'<ul class="products">{"".join(product(R, g) for g in picks)}</ul>{ADNOTE}</div></section>')

SEA_INFO = {
 "nord": dict(slug="nordsee", name="Nordsee", h1="Strandfunde und Seevögel an der Nordsee",
   lede="Die Nordsee ist ein offenes, salziges Gezeitenmeer. Zweimal am Tag fällt das Wattenmeer trocken, und Millionen Zugvögel finden hier Nahrung.",
   facts=[("Gezeiten", "Ebbe und Flut zweimal täglich, an der deutschen Küste etwa 2 bis 4 Meter Unterschied"),
          ("Salzgehalt", "etwa 3 bis 3,5 Prozent, im Wattenmeer etwas weniger"),
          ("Küste", "Wattenmeer, Inseln, Halligen, breite Sandstrände und Deiche"),
          ("Schutzgebiet", "Nationalparks Wattenmeer, seit 2009 UNESCO-Weltnaturerbe")],
   places=[("Helgoland", "Basstölpel und Trottellummen am Lummenfelsen, Kegelrobben auf der Düne."),
           ("Sylt und Amrum", "Breite Sandstrände mit Sanderlingen, nach Sturm Bernstein und Schwertmuscheln."),
           ("Halligen", "Ringelgänse im Frühjahr, Austernfischer und Seeschwalben im Sommer."),
           ("St. Peter-Ording", "Kilometerweiter Strand, Salzwiesen und Watt mit vielen Watvögeln."),
           ("Ostfriesische Inseln", "Möwenkolonien, Watt und Seehundbänke zwischen den Inseln."),
           ("Cuxhaven und Elbmündung", "Watt, Wattwanderungen und im Sommer Tausende Brandgänse.")],
   why=[("Das Wattenmeer", "Bei Ebbe liegt der Meeresboden frei. In einem Quadratmeter Watt leben Tausende Würmer, Schnecken und Muscheln. Das macht das Wattenmeer zur wichtigsten Tankstelle für Zugvögel zwischen Arktis und Afrika."),
        ("Viel Salz, viele Arten", "Weil die Nordsee offen zum Atlantik ist, leben hier mehr Meerestiere als in der Ostsee: Schwertmuscheln, Wellhornschnecken, Seeigel und Rochen."),
        ("Sicherheit", "Die Flut kommt schnell. Vor einer Wattwanderung die Gezeiten prüfen und längere Strecken nur mit Führung gehen.")]),
 "ost": dict(slug="ostsee", name="Ostsee", h1="Strandfunde und Seevögel an der Ostsee",
   lede="Die Ostsee ist ein fast geschlossenes Binnenmeer mit wenig Salz und kaum Gezeiten. Dafür gibt es Steilküsten, Bodden, Förden und die besten Bernsteinstrände.",
   facts=[("Gezeiten", "kaum spürbar, nur wenige Zentimeter; Wind kann den Wasserstand aber um mehr als einen Meter heben oder senken"),
          ("Salzgehalt", "rund 1,5 Prozent in der Kieler Bucht, vor Usedom unter 1 Prozent"),
          ("Küste", "Sand- und Steinstrände, Steilküsten, Kreidefelsen, Bodden und Förden"),
          ("Schutzgebiete", "Nationalparks Jasmund und Vorpommersche Boddenlandschaft")],
   places=[("Usedom", "Klassische Bernsteinküste. Achtung: Weißer Phosphor sieht Bernstein ähnlich."),
           ("Rügen", "Kreidefelsen, Steinstrände mit Feuersteinen und Donnerkeilen, Kegelrobben vor der Küste."),
           ("Fischland-Darß-Zingst", "Weststrand und Bodden, im Herbst Kraniche und rastende Gänse."),
           ("Fehmarn", "Seevögel an der Steilküste, im Winter Eiderenten und Meeresenten vor dem Strand."),
           ("Kieler und Flensburger Förde", "Möwen, Kormorane und Eiderenten in den Häfen."),
           ("Lübecker Bucht", "Steilküste am Brodtener Ufer, Steinstrände und Ohrenquallen im Sommer.")],
   why=[("Warum so wenig Salz?", "Viele Flüsse bringen Süßwasser, und mit der Nordsee ist die Ostsee nur über schmale Meerengen verbunden. Salzwasser strömt vor allem bei starken Stürmen ein."),
        ("Weniger Arten, dafür andere", "Viele Meerestiere vertragen das Brackwasser nicht. Muscheln bleiben kleiner, Seesterne gibt es nur im Westen. Dafür überwintern hier riesige Schwärme von Meeresenten."),
        ("Bernstein und Steine", "Die Ostsee ist die Bernsteinküste Deutschlands. Nach auflandigem Wind im Herbst und Winter lohnt die Suche im frischen Tang, am besten mit einer Metalldose statt der Hosentasche.")]),
}

def build_seas():
    for k in ("nord", "ost"):
        I = SEA_INFO[k]; R = "../"
        here = [x for x in SPECIES if k in x["act"]]
        only = [x for x in here if x["act"] == [k]]
        both = [x for x in here if len(x["act"]) == 2]
        other = "ost" if k == "nord" else "nord"
        not_here = [x for x in SPECIES if x["act"] == [other]]
        order = lambda ss: sorted(ss, key=lambda x: (GROUPS.index(x["grp"]), x["n"]))
        facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in I["facts"])
        places = "".join(f'<li><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in I["places"])
        why = "".join(f'<h2>{esc(a)}</h2><p>{esc(b)}</p>' for a, b in I["why"])
        birds = [x for x in order(here) if x["grp"] == "Seevögel"]
        rest = [x for x in order(here) if x["grp"] != "Seevögel"]
        sec = lambda hid, t, intro, ss: (f'<section class="block" aria-labelledby="{hid}"><div class="wrap"><h2 id="{hid}">{t}</h2>{intro}'
                                        f'<ul class="grid">{"".join(card(R, x, i) for i, x in enumerate(ss))}</ul></div></section>') if ss else ""
        miss = (f'<section class="block"><div class="wrap"><h2>An der {I["name"]} kaum zu finden</h2><p class="intro">Diese Arten und Funde gibt es nur an der {SEA_INFO[other]["name"]}.</p><div class="pills">'
                + "".join(f'<a href="{R}arten/{x["k"]}/index.html">{esc(x["n"])}</a>' for x in order(not_here)) + '</div></div></section>') if not_here else ""
        body = f'''<section class="block page seahero seahero-{k}"> <div class="wrap"> <p class="kicker">{ICON["seas"]}Nord- und Ostsee</p> <h1>{esc(I["h1"])}</h1> <p class="intro">{esc(I["lede"])}</p> <dl class="facts seafacts">{facts}</dl> <p class="row"><span class="tag">{len(here)} Arten und Funde</span><span class="tag">{len(birds)} Seevögel</span>{f'<span class="tag status">{len(only)} nur an der {I["name"]}</span>' if only else ""}</p> </div> </section>
{sec("h-birds", f"Seevögel an der {I['name']}", "", birds)}
{sec("h-rest", f"Strandfunde und Meerestiere an der {I['name']}", f'<p class="intro">{"Mit Markierung N oder O siehst du, ob es den Fund auch am anderen Meer gibt."}</p>', rest)}
{miss}
<section class="block" aria-labelledby="h-places"><div class="wrap"><h2 id="h-places">Gute Orte an der {I["name"]}</h2><ul class="explore tips">{places}</ul></div></section>
<section class="block"><div class="wrap prose">{why}<p><a href="{R}nordsee-ostsee/index.html">Nordsee und Ostsee im Vergleich</a> · <a href="{R}{SEA_INFO[other]["slug"]}/index.html">Zur {SEA_INFO[other]["name"]}</a></p></div></section>'''
        write(f'{I["slug"]}/index.html', page(f'{I["slug"]}/index.html', I["h1"], f'{I["lede"]} {len(here)} Seevögel und Strandfunde an der {I["name"]} bestimmen.', body,
              active="nordsee-ostsee", crumbs=[("Nord- & Ostsee", "nordsee-ostsee/index.html"), (I["name"], "")], seafilter=False))
    # Vergleichsseite
    R = "../"
    N, O = SEA_INFO["nord"], SEA_INFO["ost"]
    rows = [("Gezeiten", N["facts"][0][1], O["facts"][0][1]), ("Salzgehalt", N["facts"][1][1], O["facts"][1][1]), ("Küste", N["facts"][2][1], O["facts"][2][1]),
            ("Schutzgebiete", N["facts"][3][1], O["facts"][3][1]),
            ("Typische Seevögel", "Austernfischer, Säbelschnäbler, Ringelgans, Sanderling; Basstölpel und Trottellumme auf Helgoland", "Eiderenten zu Tausenden im Winter, Kormorane, Möwen und Seeschwalben"),
            ("Typische Funde", "Schwertmuscheln, Wellhornschnecken, Rochen-Eier, Herzigel", "Bernstein, Hühnergötter, Donnerkeile"),
            ("Quallen", "Kompassqualle, Feuerqualle, Blaue Nesselqualle, Lungenqualle", "vor allem Ohrenquallen, im Spätsommer Feuerquallen"),
            ("Robben", "Seehunde im Wattenmeer, Kegelrobben auf Helgoland", "selten, Kegelrobben vor allem vor Rügen")]
    trs = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in rows)
    body = f'''<section class="block page"> <div class="wrap"> <p class="kicker">{ICON["seas"]}Zwei Meere, zwei Welten</p> <h1>Nordsee und Ostsee im Vergleich</h1> <p class="intro">Beide Meere liegen nur rund 100 Kilometer auseinander und sind doch ganz verschieden: Die Nordsee hat Ebbe und Flut und viel Salz, die Ostsee kaum Gezeiten und Brackwasser. Das bestimmt, welche Vögel, Tiere und Funde du am Strand entdeckst.</p> <div class="cmp-wrap"><table class="cmp seacmp"> <thead><tr><td></td><th scope="col">Nordsee</th><th scope="col">Ostsee</th></tr></thead> <tbody>{trs}</tbody> </table></div> </div> </section>
{seapair(R)}
<section class="block"><div class="wrap prose"><h2>Warum hat die Ostsee kaum Ebbe und Flut?</h2><p>Gezeiten entstehen durch die Anziehung von Mond und Sonne. In einem großen, offenen Meer wie dem Atlantik baut sich dabei eine Flutwelle auf, die bis in die Nordsee läuft. Die Ostsee ist dafür zu klein und nur über schmale Meerengen mit der Nordsee verbunden. Ihr Wasserstand ändert sich deshalb vor allem durch Wind: Bei starkem Nordostwind kann es an der deutschen Küste zu Sturmfluten kommen.</p><h2>Was bedeutet das am Strand?</h2><p>An der Nordsee lohnt es sich, nach den Gezeiten zu planen: Bei Niedrigwasser suchen Watvögel im Watt nach Futter, bei Hochwasser sammeln sie sich an Rastplätzen. An der Ostsee kommt es eher auf den Wind an: Nach auflandigem Sturm liegt im Spülsaum am meisten, auch Bernstein.</p><h2>Am Strandkompass umschalten</h2><p>Oben auf der Startseite, in der Liste aller Funde und im Strandjahr kannst du zwischen „Beide Meere“, „Nordsee“ und „Ostsee“ wählen. Dann siehst du nur, was es an deinem Meer gibt. Die Wahl merkt sich dein Browser, bis du sie änderst.</p></div></section>'''
    write("nordsee-ostsee/index.html", page("nordsee-ostsee/index.html", "Nordsee und Ostsee im Vergleich", "Gezeiten, Salzgehalt, Küste, Seevögel und Strandfunde: Was Nordsee und Ostsee unterscheidet und was du wo findest.", body,
          active="nordsee-ostsee", crumbs=[("Nord- & Ostsee", "")], seafilter=False))

def build_beach():
    R = "../"
    qrows = ""
    for k, burn, lvl in [("seestachelbeere", "nie, Rippenquallen haben keine Nesselzellen", "g"), ("ohrenqualle", "kaum spürbar", "g"),
                         ("lungenqualle", "schwach, kann auf empfindlicher Haut jucken", "y"), ("blaue-nesselqualle", "spürbar", "o"),
                         ("kompassqualle", "deutlich, wie Brennnesseln", "o"), ("feuerqualle", "stark, auch abgerissene Tentakel", "r")]:
        qrows += f'<tr><th scope="row"><a href="{R}arten/{k}/index.html">{esc(BY[k]["n"])}</a></th><td><span class="burn burn-{lvl}" aria-hidden="true"></span>{esc(burn)}</td></tr>'
    body = f'''<section class="block page"> <div class="wrap"> <h1>Sicher am Strand</h1> <p class="intro">Die meisten Funde am Strand sind harmlos und schön zum Anschauen. Bei einigen Quallen, bei Robben und bei Bernstein an der Ostsee lohnt es sich aber, ein paar Dinge zu wissen.</p> </div> </section>
<section class="block" aria-labelledby="h-q"><div class="wrap"><h2 id="h-q">Welche Quallen brennen?</h2><p class="intro">Auch tote, angespülte Quallen können noch nesseln. Fass im Zweifel keine Qualle an.</p><div class="cmp-wrap"><table class="cmp"><thead><tr><th scope="col">Qualle</th><th scope="col">Brennt sie?</th></tr></thead><tbody>{qrows}</tbody></table></div>
<h3 class="h3 sub-h">Was tun nach Quallenkontakt?</h3><ol class="steps"><li><b>Aus dem Wasser gehen</b> Ruhig bleiben und die Stelle nicht reiben.</li><li><b>Mit Meerwasser abspülen</b> Kein Süßwasser verwenden, es kann weitere Nesselzellen auslösen.</li><li><b>Tentakelreste entfernen</b> Vorsichtig mit einer Karte oder einem Stöckchen abstreifen, nicht mit bloßen Fingern.</li><li><b>Bei starken Beschwerden Hilfe holen</b> Bei Atemnot, Kreislaufproblemen oder großflächigen Verbrennungen sofort die 112 rufen oder die Badeaufsicht ansprechen.</li></ol></div></section>
<section class="block" aria-labelledby="h-heuler"><div class="wrap"><h2 id="h-heuler">Junge Robbe allein am Strand?</h2><p class="intro">Junge Seehunde, die nach ihrer Mutter rufen, heißen Heuler. Meist ist die Mutter nur auf Jagd und kommt zurück, wenn es ruhig ist.</p><ol class="steps"><li><b>Abstand halten</b> Möglichst weit weg bleiben, empfohlen werden mehrere hundert Meter. Bei Kegelrobben auf Helgoland mindestens 30 Meter.</li><li><b>Nicht anfassen</b> Robben können beißen. Fasst ein Mensch das Junge an, nimmt die Mutter es oft nicht mehr an.</li><li><b>Hunde anleinen</b> Auch neugierige Hunde verscheuchen die Mutter.</li><li><b>Melden</b> Die Seehundstation, die Nationalparkverwaltung oder die Polizei verständigen. Sie entscheiden, ob das Tier Hilfe braucht.</li></ol></div></section>
<section class="block" aria-labelledby="h-phos"><div class="wrap"><div class="warnbox"><h2 id="h-phos">Bernstein oder Phosphor?</h2><p>An der Ostseeküste, vor allem auf Usedom, werden manchmal Brocken aus weißem Phosphor angespült. Sie stammen aus Brandbomben des Zweiten Weltkriegs und sehen Bernstein sehr ähnlich. Trocknet Phosphor, kann er sich bei über 20 Grad selbst entzünden und schwere Verbrennungen verursachen.</p><ul><li>Strandfunde nie in die Hosen- oder Jackentasche stecken, sondern in einer Metalldose sammeln.</li><li>Bernstein fühlt sich warm und sehr leicht an, Phosphor ist schwerer und riecht oft nach Knoblauch.</li><li>Bei Verdacht nicht anfassen, Abstand halten und die Polizei verständigen. Hat Phosphor die Haut berührt, die Stelle mit viel Wasser kühlen und den Notruf 112 wählen.</li></ul></div></div></section>
<section class="block" aria-labelledby="h-watt"><div class="wrap"><h2 id="h-watt">Ebbe, Flut und Watt</h2><ul class="explore tips"><li><div><b>Gezeiten kennen</b><span>Die Flut kommt im Watt schneller, als man denkt, und Priele füllen sich zuerst. Hoch- und Niedrigwasserzeiten veröffentlicht das <a href="https://www.bsh.de/DE/DATEN/Vorhersagen/Gezeiten/gezeiten_node.html" target="_blank" rel="noopener">Bundesamt für Seeschifffahrt und Hydrographie</a>.</span></div></li><li><div><b>Wattwanderung mit Führung</b><span>Längere Strecken, etwa zu Inseln, nur mit zertifizierten Wattführerinnen und Wattführern gehen.</span></div></li><li><div><b>Nationalpark-Regeln</b><span>Im Nationalpark Wattenmeer gibt es Ruhezonen, die nicht betreten werden dürfen. Schilder vor Ort und die <a href="https://www.nationalpark-wattenmeer.de/" target="_blank" rel="noopener">Nationalparkverwaltungen</a> informieren.</span></div></li><li><div><b>Was darf ich mitnehmen?</b><span>Leere Schalen, Bernstein und einzelne Steine sind meist in Ordnung. Lebende Tiere bleiben am Strand, und im Nationalpark gelten die Regeln vor Ort.</span></div></li></ul></div></section>'''
    body += f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Für den Strandtag</h2><a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div><ul class="products">{"".join(product(R, g) for g in ("uvlampe", "wattschuhe", "buch", "fernglas"))}</ul>{ADNOTE}</div></section>'
    write("am-strand/index.html", page("am-strand/index.html", "Sicher am Strand", "Welche Quallen brennen, was tun bei einem Heuler und warum Bernstein an der Ostsee in eine Metalldose gehört: Sicherheit am Strand von Nord- und Ostsee.", body, active="am-strand", crumbs=[("Am Strand", "")]))

def build_gear():
    R = "../"
    gsec = lambda t, ks: f'<h2 class="h3 gear-h">{t}</h2><ul class="products">{"".join(product(R, k) for k in ks)}</ul>'
    body = f'''<section class="block page"> <div class="wrap"> <h1>Ausrüstung für Strandforscher</h1> <p class="intro">Für die meisten Funde brauchst du nur offene Augen und einen Gang am Spülsaum nach dem Sturm. Diese Dinge machen es leichter und schöner, vor allem mit Kindern.</p> {gsec("Suchen und Bestimmen", ("uvlampe", "buch", "becherlupe", "sammelbox"))}{gsec("Für Kinder", ("kescher", "forscherset"))}{gsec("Watt und Strandtag", ("wattschuhe", "fernglas", "strandmuschel"))}{ADNOTE} </div> </section>
<section class="block"><div class="wrap prose"><h2>Mit UV-Licht nach Bernstein suchen</h2><p>Bernstein leuchtet unter ultraviolettem Licht mit 365 Nanometern bläulich bis gelblich. Am besten suchst du in der Dämmerung im frischen Tangsaum nach einem auflandigen Sturm. Leuchte nie in Augen und achte auf Lampen mit Filter, die kaum sichtbares Licht abgeben.</p><h2>Tiere nur kurz anschauen</h2><p>Krebse, Garnelen und Seestachelbeeren kannst du für ein paar Minuten in Meerwasser in einer Becherlupe beobachten. Stelle sie nicht in die Sonne und bringe sie danach genau dorthin zurück, wo du sie gefunden hast.</p></div></section>'''
    write("ausruestung/index.html", page("ausruestung/index.html", "Ausrüstung", "UV-Taschenlampe für Bernstein, Becherlupe, Kescher, Wattschuhe und Bestimmungsbuch: Ausrüstung für Strandforscher an Nord- und Ostsee.", body, crumbs=[("Ausrüstung", "")]))

def build_legal():
    R = "../"
    imp = f'''<section class="block page"> <div class="wrap prose"> <h1>Impressum</h1> <h2>Angaben gemäß § 5 DDG und § 18 Abs. 1 MStV</h2> <p>Nico Schober<br>Herzogin-Cecilie-Allee 10<br>28217 Bremen<br>Deutschland</p> <h2>Kontakt</h2> <p>E-Mail: <a href="mailto:info@nicoschober.com">info@nicoschober.com</a></p> <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2> <p>Nico Schober, Anschrift wie oben.</p> <h2>Art des Angebots</h2> <p>Der Strandkompass ist ein privates Informationsangebot. Er verkauft selbst keine Waren oder Dienstleistungen. Einige Seiten enthalten gekennzeichnete Werbelinks zum Amazon-Partnerprogramm; kaufst du über einen solchen Link ein, erhält der Betreiber eine Provision. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> <h2>Haftung für Inhalte</h2> <p>Die Inhalte wurden mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität kann jedoch keine Gewähr übernommen werden. Angaben zu Aktivitätszeiten und Verbreitung sind grobe Richtwerte und können regional abweichen. Die Seite ersetzt keine fachliche oder ärztliche Beratung, etwa nach Quallenkontakt oder bei gestrandeten Tieren. Im Notfall die 112 wählen.</p> <h2>Haftung für Links</h2> <p>Diese Seite enthält Links zu externen Websites, auf deren Inhalte kein Einfluss besteht. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren keine Rechtsverstöße erkennbar. Werden Rechtsverletzungen bekannt, wird der betreffende Link umgehend entfernt.</p> <h2>Urheberrecht</h2> <p>Texte und Gestaltung dieser Seite stammen vom Betreiber. Die Fotos stammen von Dritten und stehen unter freien Lizenzen; Urheber und Lizenzen sind aufgeführt unter <a href="../bildnachweis/index.html">Bildnachweis und Lizenzen</a>.</p> </div> </section>'''
    write("impressum/index.html", page("impressum/index.html", "Impressum", "Impressum des Strandkompass.", imp, crumbs=[("Impressum", "")]))
    ds = f'''<section class="block page"> <div class="wrap prose"> <h1>Datenschutzerklärung</h1> <p class="stand">Stand: November 2026</p> <h2>1. Verantwortlicher</h2> <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist der im <a href="../impressum/index.html">Impressum</a> genannte Betreiber.</p> <h2>2. Das Wichtigste in Kürze</h2> <ul> <li>Es gibt keine Registrierung, keine Cookies, kein Tracking und keine Reichweitenmessung. Werbung gibt es nur in Form gekennzeichneter Links zu Amazon, die erst beim Anklicken eine Verbindung aufbauen.</li> <li>Die Seite setzt keine Cookies. Wenn du zwischen Nordsee und Ostsee umschaltest, merkt sich dein Browser diese Wahl im lokalen Speicher (siehe Abschnitt 3a).</li> <li>Schriftarten, Fotos und Zeichnungen werden vom selben Server geladen wie die Seite selbst. Es findet keine Verbindung zu Google Fonts oder anderen Drittanbietern statt.</li> </ul> <h2>3. Hosting und Server-Protokolle</h2> <p>Diese Website wird bei statichost.eu gehostet, einem Dienst von Variable Object Assignment, c/o Knackeriet, Svartmangatan 9, 111 29 Stockholm, Schweden. Die Server stehen nach Angaben des Anbieters in der Europäischen Union; eine Übermittlung in Drittländer findet nicht statt.</p> <p>Beim Aufruf der Seite verarbeitet der Anbieter deine IP-Adresse sowie technisch notwendige Angaben zur Anfrage (abgerufene Datei, Zeitpunkt, Browser), um dir die Seite ausliefern zu können. Nach Angaben des Anbieters wird die IP-Adresse dabei nur für die Dauer der Anfrage im Arbeitsspeicher verarbeitet und nicht protokolliert. Für die Abrechnung werden technische Protokolle ohne personenbezogene Daten (vor allem die übertragene Datenmenge) höchstens sieben Tage aufbewahrt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; das berechtigte Interesse liegt in der zuverlässigen und sicheren Bereitstellung der Website. statichost.eu ist Auftragsverarbeiter im Sinne von Art. 28 DSGVO; der Anbieter stellt dafür einen eigenen Vertrag zur Auftragsverarbeitung bereit. Weitere Informationen: <a href="https://www.statichost.eu/privacy/" rel="noopener">Datenschutzerklärung von statichost.eu</a>.</p> <h2>3a. Gemerkte Auswahl im Browser</h2> <p>Wählst du oben auf der Seite „Nordsee“ oder „Ostsee“, wird diese Auswahl unter dem Namen <code>sk-sea</code> im lokalen Speicher (localStorage) deines Browsers abgelegt, damit du sie nicht auf jeder Seite neu treffen musst. Der Eintrag enthält nur das gewählte Meer, wird nicht an den Server übertragen und bleibt, bis du „Beide Meere“ wählst oder die Website-Daten in deinem Browser löschst. Rechtsgrundlage ist § 25 Abs. 2 Nr. 2 TDDDG, weil die Speicherung für die von dir ausdrücklich gewünschte Funktion erforderlich ist.</p> <h2>4. Werbelinks zum Amazon-Partnerprogramm</h2> <p>Einige Seiten enthalten mit einem Sternchen gekennzeichnete Links zu Produkten bei Amazon.de. Der Betreiber nimmt am Partnerprogramm von Amazon Europe Core S.à r.l. teil und erhält eine Provision, wenn du über einen solchen Link einkaufst. Auf dieser Website werden dafür keine Skripte, Bilder oder Cookies von Amazon geladen. Erst wenn du einen Werbelink anklickst, wirst du zu Amazon weitergeleitet; Amazon kann dann Cookies setzen, um die Herkunft der Bestellung zuzuordnen. Einzelheiten findest du in der <a href="https://www.amazon.de/gp/help/customer/display.html?nodeId=201909010" target="_blank" rel="noopener">Datenschutzerklärung von Amazon<span class="sr-only"> (öffnet in neuem Fenster)</span></a>.</p> <h2>5. Externe Links</h2> <p>Die Seite verlinkt auf externe Angebote wie Wikipedia, den Vogelkompass oder den Waldtierkompass. Erst wenn du einen solchen Link anklickst, wird eine Verbindung zum jeweiligen Anbieter aufgebaut.</p> <h2>6. Kontakt per E-Mail</h2> <p>Wenn du mir eine E-Mail schreibst, verarbeite ich deine Adresse und den Inhalt der Nachricht, um dir zu antworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Die Nachricht wird gelöscht, sobald dein Anliegen erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p> <h2>7. Deine Rechte</h2> <p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Wende dich dafür an die im Impressum genannte Adresse. Außerdem kannst du dich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO). Für den Betreiber zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit der Freien Hansestadt Bremen.</p> </div> </section>'''
    write("datenschutz/index.html", page("datenschutz/index.html", "Datenschutz", "Datenschutzerklärung des Strandkompass.", ds, crumbs=[("Datenschutz", "")]))
    rows = ""
    for k in sorted(CREDITS, key=lambda x: name_of(x[2:] if x.startswith("x-") else x)):
        a_, lic, url = CREDITS[k]
        n = name_of(k[2:] if k.startswith("x-") else k)
        rows += f'<tr><th scope="row">{esc(n)}</th><td>{esc(a_)}</td><td>{lic_link(lic)}</td><td><a href="{esc(url)}" target="_blank" rel="noopener">Quelle<span class="sr-only"> (öffnet in neuem Fenster)</span></a></td></tr>'
    prows = "".join(f'<tr><th scope="row">{esc(PRODUCTS[k]["name"])}</th><td>{esc(a_)}</td><td>{lic_link(lic)}</td><td><a href="{esc(url)}" target="_blank" rel="noopener">Quelle<span class="sr-only"> (öffnet in neuem Fenster)</span></a></td></tr>' for k, (a_, lic, url) in PHOTO.items())
    bn = f'''<section class="block page"> <div class="wrap prose"> <h1>Bildnachweis und Lizenzen</h1> <h2>Fotos</h2> <p>Alle Fotos stammen von Wikimedia Commons und stehen unter den genannten freien Lizenzen. Für die Seite wurden sie verkleinert und zugeschnitten. Die Lizenz ist jeweils mit ihrem Lizenztext verlinkt, die Quelle mit der Originaldatei. Bearbeitete Fotos unter einer Share-alike-Lizenz (BY-SA) stehen unter derselben Lizenz wie das Original.</p> </div> <div class="wrap"><div class="cmp-wrap"><table class="cmp"><thead><tr><td>Fund</td><th scope="col">Urheber</th><th scope="col">Lizenz</th><th scope="col">Quelle</th></tr></thead><tbody>{rows}</tbody></table></div></div> <div class="wrap prose"> <h2>Fotos zu den Produktempfehlungen</h2> <p>Die Fotos sind als Beispielfoto gekennzeichnet. Sie zeigen typische Geräte und Beispiele, nicht das verlinkte Produkt. Sichtbare Markenlogos wurden unkenntlich gemacht.</p> </div> <div class="wrap"><div class="cmp-wrap"><table class="cmp"><thead><tr><td>Empfehlung</td><th scope="col">Urheber</th><th scope="col">Lizenz</th><th scope="col">Quelle</th></tr></thead><tbody>{prows}</tbody></table></div></div> <div class="wrap prose"> <h2>Schriften</h2> <p>Young Serif (Bastien Sozeau) und Instrument Sans (Instrument), beide unter der SIL Open Font License 1.1, lokal eingebunden über das Projekt Fontsource.</p> </div> </section>'''
    write("bildnachweis/index.html", page("bildnachweis/index.html", "Bildnachweis und Lizenzen", "Bildnachweis und Lizenzen des Strandkompass.", bn, crumbs=[("Bildnachweis", "")]))

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "node_modules", ".bin")
SAFELIST = ["now", "open", "calm", "scrolled", "clear", "fcount", "pk"]

def build_assets():
    from PIL import Image
    write("favicon.svg", FAVICON)
    shutil.copytree(os.path.join(HERE, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "photos"), exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "photos")):
        if f.endswith(".webp"):
            shutil.copy(os.path.join(HERE, "photos", f), os.path.join(OUT, "photos", f))
    # Vorschaubild für soziale Netzwerke (1.91:1)
    im = Image.open(os.path.join(HERE, "photos_src", "sk-og.jpg")).convert("RGB")
    w, h = im.size; th = round(w / 1.91); y = (h - th) // 2
    im.crop((0, y, w, y + th)).save(os.path.join(OUT, "photos", "og.jpg"), quality=80, optimize=True, progressive=True)

def finalize():
    """CSS entschlacken und minifizieren, JS bündeln, Sitemap schreiben."""
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    css_src = os.path.join(OUT, "assets", "_full.css")
    with open(css_src, "w", encoding="utf-8") as f:
        f.write(open(os.path.join(HERE, "src", "css", "base.css"), encoding="utf-8").read() + open(os.path.join(HERE, "src", "css", "extra.css"), encoding="utf-8").read())
    purged = os.path.join(OUT, "assets", "_purged.css")
    subprocess.run([os.path.join(TOOLS, "purgecss"), "--css", css_src, "--content", f"{OUT}/**/*.html", f"{HERE}/src/js/*.js",
                    "--safelist", *SAFELIST, "--output", purged], check=True)
    subprocess.run([os.path.join(TOOLS, "lightningcss"), "--minify", "--targets", ">= 0.5%", purged, "-o", os.path.join(OUT, "assets", "site.css")], check=True)
    os.remove(css_src); os.remove(purged)
    for f in os.listdir(os.path.join(OUT, "assets")):
        if f.endswith(".js"):
            os.remove(os.path.join(OUT, "assets", f))
    entries = [os.path.join(HERE, "src", "js", f) for f in ("app.js", "home.js")]
    subprocess.run([os.path.join(TOOLS, "esbuild"), *entries, "--bundle", "--format=esm", "--minify", "--target=es2020",
                    "--legal-comments=none", f"--outdir={os.path.join(OUT, 'assets')}", "--log-level=warning"], check=True)
    urls = []
    for d, _, fs in os.walk(OUT):
        for f in fs:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(d, f), OUT).replace(os.sep, "/")
                urls.append(DOMAIN + "/" + rel[:-len("index.html")])
    urls.sort(key=lambda u: (u.count("/"), u))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    # Zeitpunkt des Builds, um zu prüfen, ob die Live-Seite aktuell ist
    import datetime as _dt
    write("version.txt", _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    build_assets(); build_home(); build_arten_index()
    for s in SPECIES:
        build_species(s)
    build_pairs(); build_year(); build_seas(); build_beach(); build_gear(); build_legal()
    finalize()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("Dateien:", n)

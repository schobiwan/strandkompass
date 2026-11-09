# -*- coding: utf-8 -*-
"""Seitengerüst: Kopf, Navigation, Fuß und Meer-Umschalter."""
from .core import *
from .icons import *

# Strukturierte Daten (schema.org): Herausgeber und Website sind über @id verknüpft; die Startseite beschreibt sie vollständig
ORG_ID, WEBSITE_ID = DOMAIN + "/#org", DOMAIN + "/#website"
AUTHOR = {"@type": "Person", "name": "Nico Schober", "url": DOMAIN + "/ueber/"}
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
LDJSON = ld({"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": ORG_ID, "name": SITE, "url": DOMAIN + "/", "logo": DOMAIN + "/icon-512.png",
     "founder": {"@type": "Person", "name": "Nico Schober"}, "sameAs": ["https://vogelkompass.de/", "https://waldtierkompass.de/"]},
    {"@type": "WebSite", "@id": WEBSITE_ID, "name": SITE, "url": DOMAIN + "/", "inLanguage": "de-DE", "publisher": {"@id": ORG_ID},
     "description": "Seevögel, Robben und Wale an Nord- und Ostsee bestimmen, dazu Quallen, Muscheln und Strandfunde."}]})

def crumbs_ld(crumbs):
    items = [(SITE, DOMAIN + "/")] + [(lab, DOMAIN + "/" + href.replace("index.html", "")) for lab, href in crumbs[:-1]] + [(crumbs[-1][0], None)]
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})} for i, (n, u) in enumerate(items)]})

# Hauptnavigation nach den Fragen der Besucher (wie beim Vogelkompass):
# Bestimmen ▾ (Wer ist das?) · Nord- & Ostsee ▾ (Was gibt es wo?) · Küstenjahr (Was ist jetzt los?) · Unterwegs ▾ (Sicher und gut ausgerüstet)
# Ohne JavaScript führen die Menü-Reiter auf ihre Übersichtsseite.
def _n(g): return sum(1 for x in SPECIES if x["grp"] in g)
NAV = [
    dict(key="bestimmen", label="Bestimmen", short="Bestimmen", icon="bino", href="index.html", intro="Wer oder was ist das?", items=[
        ("index.html#arten", "Suchen und filtern", "Nach Name oder Merkmal, z. B. „Möwe“ oder „brennt“"),
        ("arten/index.html#seevoegel", "Seevögel", f"{_n(('Seevögel',))} Arten, von der Möwe bis zum Basstölpel"),
        ("arten/index.html#robben", "Robben, Wale und Delfine", f"{_n(('Robben', 'Wale & Delfine'))} Arten, vom Seehund bis zum Pottwal"),
        ("arten/index.html#quallen", "Quallen, Muscheln und Strandfunde", f"{len(SPECIES) - _n(('Seevögel', 'Robben', 'Wale & Delfine'))} Arten und Funde am Spülsaum"),
        ("aussehen/index.html", "Nach Aussehen", "Möwe mit schwarzem Kopf, rote Qualle …"),
        ("unterscheiden/index.html", "Doppelgänger unterscheiden", f"{len(PAIRS)} ähnliche Arten im direkten Vergleich"),
        ("arten/index.html", "Alle Arten im Überblick", f"{len(SPECIES)} Steckbriefe nach Gruppen"),
    ]),
    dict(key="meere", label="Nord- & Ostsee", short="Meere", icon="seas", href="nordsee-ostsee/index.html", intro="Was gibt es wo zu sehen?", items=[
        ("nordsee/index.html", "Nordsee", "Wattenmeer, Helgoland, Seehunde und Kegelrobben"),
        ("ostsee/index.html", "Ostsee", "Bodden, Steilküsten, Eiderenten und Bernstein"),
        ("nordsee-ostsee/index.html", "Nordsee und Ostsee im Vergleich", "Gezeiten, Salz und welche Tiere wo leben"),
    ]),
    dict(key="jahr", label="Küstenjahr", short="Jahr", icon="year", href="strandjahr/index.html"),
    dict(key="unterwegs", label="Unterwegs", short="Unterwegs", icon="pack", href="am-strand/index.html", intro="Sicher und gut ausgerüstet an die Küste", items=[
        ("am-strand/index.html", "Sicher am Strand", "Quallen, Heuler, Phosphor und das Watt"),
        ("ausruestung/index.html", "Ausrüstung", "Fernglas, Vogelführer, UV-Lampe und Wattschuhe"),
        ("ratgeber/fernglas/index.html", "Fernglas für die Küste", "8x42 oder 10x42? Vier Gläser im Vergleich"),
    ]),
]
# Seiten-Schlüssel (active) → Bereich der Navigation
AREA = {"index": "bestimmen", "arten": "bestimmen", "unterscheiden": "bestimmen", "nordsee-ostsee": "meere", "nordsee": "meere", "ostsee": "meere",
        "strandjahr": "jahr", "am-strand": "unterwegs", "ausruestung": "unterwegs", "aussehen": "bestimmen"}

def nav_tabs(R, path, active):
    area = AREA.get(active or "", None)
    out = []
    for m in NAV:
        cur = ' aria-current="true"' if area == m["key"] else ""
        inner = f'{ICON[m["icon"]]}<span class="tl">{m["label"]}</span><span class="ts">{m["short"]}</span>'
        if "items" not in m:
            out.append(f'<li><a class="tab" href="{R}{m["href"]}"{cur.replace("true", "page")}>{inner}</a></li>')
            continue
        lis = "".join(f'<li><a href="{R}{h}"{" aria-current=\"page\"" if h == path else ""}><b>{t}</b><span>{d}</span></a></li>' for h, t, d in m["items"])
        out.append(f'<li class="has-menu"><a class="tab" href="{R}{m["href"]}" data-menu="{m["key"]}"{cur}>{inner}{ICON["chev"]}</a>'
                   f'<div class="mpanel" id="menu-{m["key"]}" hidden><p class="mintro">{m["intro"]}</p><ul>{lis}</ul></div></li>')
    return "".join(out)

# Gewähltes Meer früh setzen, damit beim Laden nichts springt
SEA_BOOT = '<script>try{var s=localStorage.getItem("sk-sea");if(s==="nord"||s==="ost")document.documentElement.dataset.sea=s}catch(e){}</script>'

def seaswitch(extra=""):
    """Umschalter Beide · Nordsee · Ostsee; app.js merkt sich die Wahl."""
    b = lambda v, t: f'<button type="button" class="seabtn{"" if v else " seabtn-all"}" data-sea-set="{v}" aria-pressed="{"true" if not v else "false"}">{t}</button>'
    return (f'<div class="seasw{(" " + extra) if extra else ""}" role="group" aria-label="Meer wählen">'
            f'{b("", "Beide Meere")}{b("nord", "Nordsee")}{b("ost", "Ostsee")}</div>')

def seabar(R):
    return (f'<div class="seabar"><div class="wrap seabar-in"><span class="seabar-l">Zeige Arten von</span>{seaswitch()}'
            f'<a class="seabar-more" href="{R}nordsee-ostsee/index.html">Was ist der Unterschied?</a></div></div>')

# ------------------------------------------------------------------ Layout
SEARCH_DLG = ('<dialog class="sdlg" id="sdlg" aria-labelledby="sdlg-title"> <form method="get" action="{R}index.html" class="sform" id="sform">'
              '<h2 class="sr-only" id="sdlg-title">Art suchen</h2><label class="search" for="sq">' + ICON["find"] + '<span class="sr-only">Name oder Aussehen</span>'
              '<input type="search" id="sq" name="q" placeholder="Name oder Aussehen, z. B. roter Schnabel" autocomplete="off" enterkeyhint="search"></label>'
              '<button type="button" class="sclose" id="sclose">Schließen</button></form> <p class="sr-only" id="sstatus" role="status" aria-live="polite"></p><ul class="sresults" id="sresults" aria-label="Treffer"></ul>'
              '<p class="smore" id="smore" hidden><a id="smore-link" href="{R}index.html#arten">Alle Treffer mit Filtern anzeigen</a></p> </dialog>')

def page(path, title, desc, body, active=None, scripts=(), crumbs=None, data=None, is_home=False, og="og.jpg", seafilter=True, root=None, noindex=False, extra_ld=""):
    """root: fester Pfad zur Wurzel, z. B. "/" für die 404-Seite, die unter beliebigen Adressen erscheint."""
    depth = path.count("/")
    R = "../" * depth if root is None else root
    canon = DOMAIN + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)
    cr = ""
    if crumbs:
        items = [f'<li><a href="{R}index.html">Start</a></li>']
        for (lab, href) in crumbs[:-1]:
            items.append(f'<li><a href="{R}{href}">{esc(lab)}</a></li>')
        items.append(f'<li><span aria-current="page">{esc(crumbs[-1][0])}</span></li>')
        cr = f'<nav class="crumbs wrap" aria-label="Brotkrumen"><ol> {" ".join(items)} </ol></nav>'
        extra_ld += crumbs_ld(crumbs)
    dj = f'<script type="application/json" id="wk-data">{json.dumps(data, ensure_ascii=False)}</script>' if data is not None else ""
    sc = f'<script type="module" src="{R}assets/{(scripts[0] if scripts else "app.js")}"></script>'
    full_title = title if is_home else f"{title} · {SITE}"
    return f'''<!DOCTYPE html><html lang="de" data-root="{R or './'}" data-index> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}">{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">'}<meta name="theme-color" content="#fbf6ea" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#14232c" media="(prefers-color-scheme: dark)"><meta name="color-scheme" content="light dark">{SEA_BOOT}<link rel="icon" href="{R}favicon.ico" sizes="32x32"><link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{R}apple-touch-icon.png"><link rel="manifest" href="{R}site.webmanifest"><link rel="preload" href="{R}fonts/outfit-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{R}fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="de_DE"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/photos/{og}"><meta name="twitter:card" content="summary_large_image">{LDJSON if is_home else ""}{extra_ld}<link rel="stylesheet" href="{R}assets/site.css"></head> <body> {LOGO} <a class="skip" href="#main">Zum Inhalt springen</a> <nav class="appnav" aria-label="Hauptnavigation"> <div class="wrap"> <a class="brand" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span><span class="sr-only">, zur Startseite</span></a> <ul class="tabs" id="tabs"> {nav_tabs(R, path, active)} </ul> <button class="navsearch" type="button" id="navsearch" aria-haspopup="dialog" aria-controls="sdlg">{ICON["find"]}<span class="sr-only">Art suchen</span><span class="nsl" aria-hidden="true">Suchen</span></button> </div> <div class="mbackdrop" id="mbackdrop" hidden></div> </nav> {SEARCH_DLG.replace("{R}", R or "")} <main id="main" tabindex="-1"{' class="seafilter"' if seafilter else ""}> {cr} {body} </main> {footer(R)} {dj}{sc} </body> </html>'''

def footer(R):
    best = [("arten/index.html#seevoegel", "Seevögel"), ("arten/index.html#robben", "Robben, Wale und Delfine"), ("arten/index.html#quallen", "Quallen, Muscheln und Strandfunde"),
            ("aussehen/index.html", "Nach Aussehen bestimmen"), ("unterscheiden/index.html", "Doppelgänger unterscheiden"), ("arten/index.html", "Alle Arten im Überblick")]
    ent = [("nordsee/index.html", "Nordsee"), ("ostsee/index.html", "Ostsee"), ("strandjahr/index.html", "Küstenjahr"),
           ("am-strand/index.html", "Sicher am Strand"), ("ausruestung/index.html", "Ausrüstung"), ("ratgeber/fernglas/index.html", "Fernglas für die Küste")]
    leg = [("ueber/index.html", "Über den Meereskompass"), ("impressum/index.html", "Impressum"), ("datenschutz/index.html", "Datenschutz"), ("bildnachweis/index.html", "Bildnachweis und Lizenzen")]
    li = lambda xs: "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in xs)
    return f'''<footer> <div class="wrap"> <a class="flogo" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span></a> <div class="fcols"> <nav aria-label="Bestimmen"><p class="fhead">Bestimmen</p><ul>{li(best)}</ul></nav> <nav aria-label="An der Küste"><p class="fhead">An der Küste</p><ul>{li(ent)}</ul></nav> <nav aria-label="Über die Seite"><p class="fhead">Über die Seite</p><ul>{li(leg)}</ul></nav> <nav aria-label="Schwesterseiten"><p class="fhead">Schwesterseiten</p><ul><li><a href="https://vogelkompass.de/" rel="noopener">Vogelkompass: Vögel bestimmen</a></li><li><a href="https://waldtierkompass.de/" rel="noopener">Waldtierkompass: Waldtiere bestimmen</a></li></ul></nav> </div> <p class="footnote">Fotos: Wikimedia Commons, unter freien Lizenzen. Mit * markierte Links sind Werbelinks. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> </div> </footer>'''

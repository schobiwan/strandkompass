# -*- coding: utf-8 -*-
"""Seitengerüst: Kopf, Navigation, Fuß und Meer-Umschalter."""
from .core import *
from .icons import *

LDJSON = ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/",
          "inLanguage": "de-DE", "description": "Strandfunde an Nord- und Ostsee bestimmen: Muscheln, Quallen, Krebse, Bernstein und mehr."}, ensure_ascii=False) + '</script>')

TABS = [("index", "Bestimmen", "Funde", "find"), ("nordsee-ostsee", "Nord- & Ostsee", "Meere", "seas"), ("am-strand", "Am Strand", "Strand", "wave"),
        ("unterscheiden", "Doppelgänger", "Vergleich", "pair"), ("strandjahr", "Strandjahr", "Jahr", "year")]

# Gewähltes Meer früh setzen, damit beim Laden nichts springt
SEA_BOOT = '<script>try{var s=localStorage.getItem("sk-sea");if(s==="nord"||s==="ost")document.documentElement.dataset.sea=s}catch(e){}</script>'

def seaswitch(extra=""):
    """Umschalter Beide · Nordsee · Ostsee; app.js merkt sich die Wahl."""
    b = lambda v, t: f'<button type="button" class="seabtn{"" if v else " seabtn-all"}" data-sea-set="{v}" aria-pressed="{"true" if not v else "false"}">{t}</button>'
    return (f'<div class="seasw{(" " + extra) if extra else ""}" role="group" aria-label="Meer wählen">'
            f'{b("", "Beide Meere")}{b("nord", "Nordsee")}{b("ost", "Ostsee")}</div>')

def seabar(R):
    return (f'<div class="seabar"><div class="wrap seabar-in"><span class="seabar-l">Zeige Funde von</span>{seaswitch()}'
            f'<a class="seabar-more" href="{R}nordsee-ostsee/index.html">Was ist der Unterschied?</a></div></div>')

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
    return f'''<!DOCTYPE html><html lang="de" data-root="{R or './'}" data-index> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}"><meta name="theme-color" content="#fbf6ea" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#14232c" media="(prefers-color-scheme: dark)"><meta name="color-scheme" content="light dark">{SEA_BOOT}<link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="preload" href="{R}fonts/outfit-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{R}fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="de_DE"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/photos/{og}"><meta name="twitter:card" content="summary_large_image">{LDJSON if is_home else ""}<link rel="stylesheet" href="{R}assets/site.css"></head> <body> {LOGO} <a class="skip" href="#main">Zum Inhalt springen</a> <nav class="appnav" aria-label="Hauptnavigation"> <div class="wrap"> <a class="brand" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span><span class="sr-only">, zur Startseite</span></a> <ul class="tabs"> {"".join(tabs)} </ul> </div> </nav> <main id="main" tabindex="-1"{' class="seafilter"' if seafilter else ""}> {cr} {body} </main> {footer(R)} {dj}{sc} </body> </html>'''

def footer(R):
    ent = [("arten/index.html", "Alle Strandfunde"), ("nordsee-ostsee/index.html", "Nordsee und Ostsee"), ("am-strand/index.html", "Sicher am Strand"), ("unterscheiden/index.html", "Doppelgänger unterscheiden"),
           ("strandjahr/index.html", "Strandjahr und Kalender"), ("ausruestung/index.html", "Ausrüstung")]
    leg = [("impressum/index.html", "Impressum"), ("datenschutz/index.html", "Datenschutz"), ("bildnachweis/index.html", "Bildnachweis und Lizenzen")]
    li = lambda xs: "".join(f'<li><a href="{R}{h}">{t}</a></li>' for h, t in xs)
    return f'''<footer> <div class="wrap"> <a class="flogo" href="{R}index.html"><svg class="logo" aria-hidden="true"><use href="#logo-mark"></use></svg><span>{SITE}</span></a> <div class="fcols"> <nav aria-label="Entdecken"><p class="fhead">Entdecken</p><ul>{li(ent)}</ul></nav> <nav aria-label="Rechtliches"><p class="fhead">Rechtliches</p><ul>{li(leg)}</ul></nav> <nav aria-label="Schwesterseiten"><p class="fhead">Schwesterseiten</p><ul><li><a href="https://vogelkompass.de/" rel="noopener">Vogelkompass: Vögel bestimmen</a></li><li><a href="https://waldtierkompass.de/" rel="noopener">Waldtierkompass: Waldtiere bestimmen</a></li></ul></nav> </div> <p class="footnote">Fotos: Wikimedia Commons, unter freien Lizenzen. Mit * markierte Links sind Werbelinks. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p> </div> </footer>'''

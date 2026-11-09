# -*- coding: utf-8 -*-
"""Schriften, Fotos, CSS und JS bündeln, Sitemap schreiben."""
import os, shutil, subprocess, datetime, json
from .core import *
from .icons import FAVICON

TOOLS = os.path.join(ROOT, "node_modules", ".bin")

SAFELIST = ["now", "open", "calm", "scrolled", "clear", "fcount", "pk", "playing", "snone", "suggest-btn"]

HEADERS = """# Meereskompass – Header für statichost.eu (auch Cloudflare Pages und Netlify verstehen dieses Format)
*
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
/assets/*
    Cache-Control: public, max-age=604800
/fonts/*
    Cache-Control: public, max-age=31536000, immutable
/photos/*
    Cache-Control: public, max-age=2592000
/audio/*
    Cache-Control: public, max-age=2592000
"""

def build_assets():
    from PIL import Image
    write("favicon.svg", FAVICON)
    # favicon.ico, Apple-Touch-Icon und App-Icons (aus favicon.svg gerendert, liegen fertig in icons/)
    for f in os.listdir(os.path.join(ROOT, "icons")):
        shutil.copy(os.path.join(ROOT, "icons", f), os.path.join(OUT, f))
    write("site.webmanifest", json.dumps({"name": SITE, "short_name": SITE, "description": "Seevögel, Robben, Wale und Strandfunde an Nord- und Ostsee erkennen",
        "lang": "de", "start_url": "/", "display": "browser", "background_color": "#f3eee3", "theme_color": "#33413f",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False, indent=2) + "\n")
    # Header für statichost.eu: lange Zwischenspeicherung für Dateien, die sich selten ändern
    write("_headers", HEADERS)
    shutil.copytree(os.path.join(ROOT, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "photos"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "photos")):
        if f.endswith(".webp"):
            shutil.copy(os.path.join(ROOT, "photos", f), os.path.join(OUT, "photos", f))
    if os.path.isdir(os.path.join(ROOT, "audio")):
        shutil.copytree(os.path.join(ROOT, "audio"), os.path.join(OUT, "audio"), dirs_exist_ok=True)
    # Vorschaubild für soziale Netzwerke (1.91:1)
    im = Image.open(os.path.join(ROOT, "photos_src", "sk-og.jpg")).convert("RGB")
    w, h = im.size; th = round(w / 1.91); y = (h - th) // 2
    im.crop((0, y, w, y + th)).save(os.path.join(OUT, "photos", "og.jpg"), quality=80, optimize=True, progressive=True)

def finalize():
    """CSS entschlacken und minifizieren, JS bündeln, Sitemap schreiben."""
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    css_src = os.path.join(OUT, "assets", "_full.css")
    with open(css_src, "w", encoding="utf-8") as f:
        f.write(open(os.path.join(ROOT, "src", "css", "base.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "css", "extra.css"), encoding="utf-8").read())
    purged = os.path.join(OUT, "assets", "_purged.css")
    subprocess.run([os.path.join(TOOLS, "purgecss"), "--css", css_src, "--content", f"{OUT}/**/*.html", f"{ROOT}/src/js/*.js",
                    "--safelist", *SAFELIST, "--output", purged], check=True)
    subprocess.run([os.path.join(TOOLS, "lightningcss"), "--minify", "--targets", ">= 0.5%", purged, "-o", os.path.join(OUT, "assets", "site.css")], check=True)
    os.remove(css_src); os.remove(purged)
    for f in os.listdir(os.path.join(OUT, "assets")):
        if f.endswith(".js"):
            os.remove(os.path.join(OUT, "assets", f))
    entries = [os.path.join(ROOT, "src", "js", f) for f in ("app.js", "home.js")]
    subprocess.run([os.path.join(TOOLS, "esbuild"), *entries, "--bundle", "--format=esm", "--minify", "--target=es2020",
                    "--legal-comments=none", f"--outdir={os.path.join(OUT, 'assets')}", "--log-level=warning"], check=True)
    # Sitemap mit Bildangaben: Art- und Vergleichsseiten nennen ihre Fotos, damit Google sie in der Bildersuche der richtigen Seite zuordnet
    pics = {f"arten/{s['k']}/": [s["k"]] for s in SPECIES}
    pics.update({f"unterscheiden/{p['k']}/": [photo_key(p["a"]), photo_key(p["b"])] for p in PAIRS})
    urls = []
    for d, _, fs in os.walk(OUT):
        for f in fs:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(d, f), OUT).replace(os.sep, "/")
                urls.append(rel[:-len("index.html")])
    urls.sort(key=lambda u: (u.count("/"), u))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
          + "".join(f"  <url><loc>{DOMAIN}/{u}</loc>" + "".join(f"<image:image><image:loc>{DOMAIN}/photos/{k}.webp</image:loc></image:image>" for k in pics.get(u, []))
                    + "</url>\n" for u in urls) + "</urlset>\n")
    write("llms.txt", llms_txt())
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    # Zeitpunkt des Builds, um zu prüfen, ob die Live-Seite aktuell ist
    write("version.txt", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


def llms_txt():
    """Kompakte Übersicht für KI-Assistenten und KI-Suchmaschinen (Vorschlag llmstxt.org)."""
    u = lambda path: f"{DOMAIN}/{path}"
    groups = "\n".join(f"- [{g}]({u('arten/#' + gslug(g))})" for g in GROUPS)
    arten = "\n".join(f"- [{s['n']} ({s['lat']})]({u('arten/' + s['k'] + '/')}): {s['short']}" for s in sorted(SPECIES, key=skey))
    pairs = "\n".join(f"- [{name_of(p['a'])} oder {name_of(p['b'])}?]({u('unterscheiden/' + p['k'] + '/')})" for p in PAIRS)
    return f"""# {SITE}

> Seevögel, Robben, Wale und Delfine an Nord- und Ostsee erkennen, dazu Quallen, Muscheln und andere Strandfunde: {len(SPECIES)} Steckbriefe mit Foto, Merkmalen, Vorkommen in Nordsee und Ostsee und im Jahresverlauf, Rufe der Seevögel zum Anhören und {len(PAIRS)} Vergleiche ähnlicher Arten. Privates, unabhängiges Angebot von Nico Schober aus Bremen. Fotos und Rufaufnahmen von Wikimedia Commons unter freien Lizenzen.

Sprache: Deutsch. Angaben zu Vorkommen und Jahreszeiten sind grobe Richtwerte für die deutsche Küste.

## Bestimmen
- [Startseite mit Suche und Filtern]({u('')})
- [Alle Arten und Funde nach Gruppen]({u('arten/')})
- [Doppelgänger unterscheiden]({u('unterscheiden/')}): ähnliche Arten im direkten Vergleich
- [Küstenjahr]({u('strandjahr/')}): was in welchem Monat zu sehen ist

## Gruppen
{groups}

## Nordsee und Ostsee
- [Nordsee]({u('nordsee/')})
- [Ostsee]({u('ostsee/')})
- [Nordsee und Ostsee im Vergleich]({u('nordsee-ostsee/')})

## Unterwegs
- [Sicher am Strand]({u('am-strand/')}): Quallen, Heuler, Phosphor, Watt
- [Ausrüstung]({u('ausruestung/')}): Fernglas, Bestimmungsbücher, UV-Lampe, Wattschuhe

## Arten
{arten}

## Vergleiche
{pairs}

## Rechtliches
- [Impressum]({u('impressum/')})
- [Bildnachweis und Lizenzen]({u('bildnachweis/')})
"""

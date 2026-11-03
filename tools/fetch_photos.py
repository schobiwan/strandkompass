# -*- coding: utf-8 -*-
"""Lädt Fotos von Wikimedia Commons (läuft in GitHub Actions).
Liste: tools/photo_list.json  {key: ["Wikipedia-Artikel de", "Artikel en"] oder "File:Name.jpg"}
Ergebnis: photos_src/incoming/<key>.jpg (+ <key>-alt.jpg) und meta.json"""
import json, os, re, sys, time, urllib.parse, urllib.request, html

UA = "StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass)"
OUT = "photos_src/incoming"
os.makedirs(OUT, exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            print("retry", url, e); time.sleep(3 * (i + 1))
    raise SystemExit("failed " + url)

def api(host, **p):
    p.update(format="json", formatversion="2")
    return json.loads(get(f"https://{host}/w/api.php?" + urllib.parse.urlencode(p)))

def lead_file(lang, title):
    d = api(f"{lang}.wikipedia.org", action="query", prop="pageimages", piprop="name", titles=title, redirects=1)
    pg = d["query"]["pages"][0]
    return ("File:" + pg["pageimage"]) if "pageimage" in pg else None

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def fetch(key, ftitle, suffix=""):
    d = api("commons.wikimedia.org", action="query", prop="imageinfo", titles=ftitle,
            iiprop="url|extmetadata|size", iiurlwidth=1400)
    pg = d["query"]["pages"][0]
    ii = pg["imageinfo"][0]
    md = ii.get("extmetadata", {})
    data = get(ii.get("thumburl") or ii["url"])
    fn = f"{key}{suffix}.jpg"
    open(os.path.join(OUT, fn), "wb").write(data)
    return {"file": fn, "title": pg["title"], "url": ii["descriptionurl"],
            "artist": strip(md.get("Artist", {}).get("value")),
            "license": strip(md.get("LicenseShortName", {}).get("value")),
            "w": ii.get("width"), "h": ii.get("height")}

lst = json.load(open("tools/photo_list.json", encoding="utf-8"))
meta = {}
for key, spec in lst.items():
    files = []
    if isinstance(spec, str):
        files = [spec]
    else:
        for lang, t in zip(("de", "en"), spec):
            try:
                f = lead_file(lang, t)
            except SystemExit:
                f = None
            if f and f not in files:
                files.append(f)
    meta[key] = []
    for i, f in enumerate(files):
        try:
            meta[key].append(fetch(key, f, "" if i == 0 else f"-alt{i}"))
            print("ok", key, f)
        except Exception as e:
            print("FEHLER", key, f, e)
        time.sleep(0.5)
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

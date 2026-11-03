# -*- coding: utf-8 -*-
"""Lädt Tonaufnahmen von Wikimedia Commons (läuft in GitHub Actions).
Liste: tools/audio_list.json  {key: "Lateinischer Name"} oder {key: "File:Name.ogg"}
Je Art: die Aufnahme aus Wikidata (Eigenschaft P51) und die besten Treffer der Commons-Suche.
Ergebnis: audio_src/incoming/<key>-<n>.<ext> und meta.json"""
import json, os, re, time, html, urllib.parse, urllib.request

UA = "StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass)"
OUT = "audio_src/incoming"
os.makedirs(OUT, exist_ok=True)

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:
            print("retry", url[:100], e); time.sleep(3 * (i + 1))
    return None

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def wikidata_audio(latin):
    q = f'SELECT ?a WHERE {{ ?t wdt:P225 "{latin}" ; wdt:P51 ?a . }}'
    d = get("https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q))
    if not d: return []
    return ["File:" + urllib.parse.unquote(b["a"]["value"].rsplit("/", 1)[1]).replace("_", " ") for b in d["results"]["bindings"]]

def commons_search(latin, n=4):
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(
        action="query", list="search", srsearch=f'"{latin}" filetype:audio', srnamespace=6, srlimit=n, format="json")))
    return [x["title"] for x in (d or {}).get("query", {}).get("search", [])]

def info(title):
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(
        action="query", prop="imageinfo", titles=title, iiprop="url|extmetadata|size|mime", format="json", formatversion=2)))
    pg = d["query"]["pages"][0]
    if "imageinfo" not in pg: return None
    ii = pg["imageinfo"][0]; md = ii.get("extmetadata", {})
    return {"title": pg["title"], "url": ii["url"], "page": ii["descriptionurl"], "size": ii.get("size"), "duration": ii.get("duration"),
            "mime": ii.get("mime"), "artist": strip(md.get("Artist", {}).get("value")),
            "license": strip(md.get("LicenseShortName", {}).get("value")), "desc": strip(md.get("ImageDescription", {}).get("value"))[:200]}

lst = json.load(open("tools/audio_list.json", encoding="utf-8"))
meta = {}
for key, spec in lst.items():
    titles = [spec] if spec.startswith("File:") else []
    if not titles:
        titles = wikidata_audio(spec)
        for t in commons_search(spec):
            if t not in titles: titles.append(t)
    meta[key] = []
    for i, t in enumerate(titles[:5]):
        m = info(t)
        if not m or (m["size"] or 0) > 25_000_000: continue
        ext = m["url"].rsplit(".", 1)[1].lower()
        data = get(m["url"], binary=True)
        if not data: continue
        fn = f"{key}-{i}.{ext}"
        open(os.path.join(OUT, fn), "wb").write(data)
        m["file"] = fn; meta[key].append(m)
        print("ok", key, t, m["license"], m["duration"])
        time.sleep(0.5)
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

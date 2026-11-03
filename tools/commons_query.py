# -*- coding: utf-8 -*-
"""Hilfsabfragen an Wikimedia Commons (läuft in GitHub Actions).
tools/commons_query.json: {"wikitext": [Dateititel], "audio_search": {key: Suchbegriff}}
Ergebnis: audio_src/query/result.json und gefundene Dateien als <key>-s<n>.<ext>"""
import json, os, re, time, html, urllib.parse, urllib.request
UA = "StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass)"
OUT = "audio_src/query"; os.makedirs(OUT, exist_ok=True)
def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = r.read(); return d if binary else json.loads(d)
        except Exception as e:
            print("retry", e); time.sleep(3 * (i + 1))
api = lambda **p: get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(p, format="json", formatversion=2)))
strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
q = json.load(open("tools/commons_query.json", encoding="utf-8"))
res = {"wikitext": {}, "search": {}}
for t in q.get("wikitext", []):
    d = api(action="query", prop="revisions", rvprop="content", rvslots="main", titles=t)
    pg = d["query"]["pages"][0]
    res["wikitext"][t] = pg["revisions"][0]["slots"]["main"]["content"][:3000] if "revisions" in pg else None
for key, term in q.get("audio_search", {}).items():
    d = api(action="query", list="search", srsearch=term + " filetype:audio", srnamespace=6, srlimit=10)
    res["search"][key] = []
    n = 0
    for hit in d["query"]["search"]:
        t = hit["title"]
        if re.search(r"^File:(De|Jer|En|Fr|Nl)-", t): continue
        ii = api(action="query", prop="imageinfo", titles=t, iiprop="url|extmetadata|size")["query"]["pages"][0]["imageinfo"][0]
        md = ii.get("extmetadata", {})
        m = {"title": t, "page": ii["descriptionurl"], "duration": ii.get("duration"), "artist": strip(md.get("Artist", {}).get("value")),
             "license": strip(md.get("LicenseShortName", {}).get("value"))}
        if n < 3 and (ii.get("size") or 0) < 25_000_000:
            ext = ii["url"].split("?")[0].rsplit(".", 1)[1].lower()
            fn = f"{key}-s{n}.{ext}"; open(os.path.join(OUT, fn), "wb").write(get(ii["url"], True)); m["file"] = fn; n += 1
        res["search"][key].append(m)
json.dump(res, open(os.path.join(OUT, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

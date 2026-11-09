# -*- coding: utf-8 -*-
"""Seiten „Nach Aussehen“: Übersicht und je eine Seite pro Merkmal (z. B. Möwe mit schwarzem Kopf)."""
from ..core import *
from ..layout import *
from ..components import *
from data_aussehen import LOOKS

def looks_for(key):
    """Merkmal-Seiten, auf denen eine Art vorkommt (für Links von der Artseite)."""
    return [m for m in LOOKS if any(k == key for k, _ in m["items"])]

def mcard(R, key, why, i):
    s = BY[key]
    return (f'<li class="mcard" data-act="{acts_attr(s["act"])}"><a href="{R}arten/{key}/index.html">{img(R, key, "", eager=i < 3, sizes="(max-width: 600px) 92vw, 300px")}'
            f'<span class="mname">{esc(s["n"])}</span><span class="mwhy">{esc(why)}</span><span class="mmeta">{esc(s["grp"])} · {esc(s["sz"])}</span></a>{cred(key)}</li>')

def others_nav(R, cur=None):
    return '<ul class="mother">' + "".join(f'<li><a href="{R}aussehen/{o["slug"]}/index.html">{esc(o["h1"])}</a></li>' for o in LOOKS if o is not cur) + '</ul>'

def build_looks():
    R = "../"
    birds = [m for m in LOOKS if BY[m["items"][0][0]]["grp"] == "Seevögel"]
    sea = [m for m in LOOKS if BY[m["items"][0][0]]["grp"] in ("Robben", "Wale & Delfine")]
    rest = [m for m in LOOKS if m not in birds and m not in sea]
    tile = lambda m: (f'<li class="mcard"><a href="{R}aussehen/{m["slug"]}/index.html">{img(R, m.get("cover", m["items"][0][0]), "", sizes="(max-width: 600px) 92vw, 300px")}'
                      f'<span class="mname">{esc(m["h1"])}</span><span class="mwhy">{esc(", ".join(BY[k]["n"] for k, _ in m["items"][:3]))}{" …" if len(m["items"]) > 3 else ""}</span></a>{cred(m.get("cover", m["items"][0][0]))}</li>')
    sec = lambda h, i, ms: f'<h2 class="h3 grp-h" id="{i}">{h}</h2><ul class="mlist">{"".join(tile(m) for m in ms)}</ul>'
    body = ('<section class="block page"> <div class="wrap"> <h1>Nach Aussehen bestimmen</h1> <p class="intro">Du kennst den Namen nicht, aber weißt, wie es aussah? Wähle das auffälligste Merkmal. Jede Seite zeigt die passenden Arten mit Foto und dem Unterschied, auf den es ankommt.</p>'
            + sec("Seevögel", "voegel", birds) + sec("Robben, Wale und Delfine", "meeressaeuger", sea) + sec("Quallen und Strandfunde", "funde", rest)
            + f'<p class="mtip">Nicht dabei? Auf der <a href="{R}index.html#arten">Startseite</a> kannst du nach mehreren Merkmalen zugleich suchen, zum Beispiel „gelbe Beine“ oder „brennt“.</p> </div> </section>')
    ld_list = ld({"@context": "https://schema.org", "@type": "ItemList", "name": "Nach Aussehen bestimmen", "numberOfItems": len(LOOKS),
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": m["h1"], "url": f'{DOMAIN}/aussehen/{m["slug"]}/'} for i, m in enumerate(LOOKS)]})
    write("aussehen/index.html", page("aussehen/index.html", "Nach Aussehen bestimmen", "Möwe mit schwarzem Kopf, rote Qualle oder schwarzes Ei am Strand? Bestimme Seevögel, Meerestiere und Strandfunde nach ihrem auffälligsten Merkmal.",
                                      body, active="aussehen", crumbs=[("Nach Aussehen", "")], seafilter=False, extra_ld=ld_list))
    for m in LOOKS:
        R = "../../"
        keys = {k for k, _ in m["items"]}
        pairs = [p for p in PAIRS if p["a"] in keys and p["b"] in keys]
        pp = ('<h2 class="mh2">Leicht zu verwechseln</h2><ul class="mother">' + "".join(
              f'<li><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</a></li>' for p in pairs) + '</ul>') if pairs else ""
        body = (f'<section class="block page"> <div class="wrap"> <h1>{esc(m["h1"])}</h1> <p class="intro">{esc(m["intro"])}</p>'
                f'<ul class="mlist">{"".join(mcard(R, k, w, i) for i, (k, w) in enumerate(m["items"]))}</ul> {pp}'
                f'<p class="mtip">Nicht dabei? Auf der <a href="{R}index.html#arten">Startseite</a> kannst du nach mehreren Merkmalen zugleich suchen.</p>'
                f'<h2 class="mh2">Weitere Merkmale</h2>{others_nav(R, m)} </div> </section>')
        names = ", ".join(BY[k]["n"] for k, _ in m["items"])
        ld_list = ld({"@context": "https://schema.org", "@type": "ItemList", "name": m["h1"], "numberOfItems": len(m["items"]),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": BY[k]["n"], "url": f"{DOMAIN}/arten/{k}/"} for i, (k, _) in enumerate(m["items"])]})
        desc = f'{m["h1"]}? {len(m["items"])} Arten von Nord- und Ostsee, auf die das passt, mit Foto und Erkennungsmerkmal: {names}.'
        write(f'aussehen/{m["slug"]}/index.html', page(f'aussehen/{m["slug"]}/index.html', m["title"], desc[:300], body, active="aussehen",
              crumbs=[("Nach Aussehen", "aussehen/index.html"), (m["h1"], "")], seafilter=False, og=f'{m["items"][0][0]}.webp', extra_ld=ld_list))

# -*- coding: utf-8 -*-
"""Gruppenseiten /arten/<gruppe>/ (z. B. /arten/quallen/): eigene Einstiegsseiten für Suchen wie „Quallen Ostsee“ oder „Robben Nordsee“."""
from ..core import *
from ..layout import *
from ..components import *
from .looks import looks_for
from data_gruppen import GROUP_INFO


def group_url(g, R=""):
    return f"{R}arten/{gslug(g)}/index.html"


def build_groups():
    R = "../../"
    for g in GROUPS:
        I = GROUP_INFO[g]
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=skey)
        keys = {s["k"] for s in ss}
        n_nord = sum(1 for s in ss if "nord" in s["act"])
        n_ost = sum(1 for s in ss if "ost" in s["act"])
        only_n = [s for s in ss if s["act"] == ["nord"]]
        intro = "".join(f'<p class="intro">{esc(p)}</p>' for p in I["intro"])
        tags = (f'<p class="row"><span class="tag">{counts(ss)} {"Funde" if g == "Strandfunde" else "Arten"}</span>'
                f'<span class="tag">{n_nord} an der Nordsee</span><span class="tag">{n_ost} an der Ostsee</span></p>')
        burn = (f'<section class="block" aria-labelledby="h-burn"><div class="wrap"><h2 id="h-burn">Welche Quallen brennen?</h2>{burn_table(R)}'
                f'<p>Was nach Quallenkontakt hilft, steht unter <a href="{R}am-strand/index.html">Sicher am Strand</a>.</p></div></section>') if g == "Quallen" else ""
        nord_only = (f'<p>Nur an der Nordsee: {", ".join(esc(s["n"]) for s in only_n)}. '
                     f'Welche Arten es an deinem Meer gibt, zeigen die Seiten <a href="{R}nordsee/index.html">Nordsee</a> und <a href="{R}ostsee/index.html">Ostsee</a>.</p>') if only_n else ""
        pairs = [p for p in PAIRS if p["a"] in keys or p["b"] in keys]
        pp = ('<h2>Leicht zu verwechseln</h2><div class="pills">' + "".join(
              f'<a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</a>' for p in pairs) + '</div>') if pairs else ""
        looks = []
        for s in ss:
            for m in looks_for(s["k"]):
                if m not in looks:
                    looks.append(m)
        lk = ('<h2>Nach Aussehen bestimmen</h2><div class="pills">' + "".join(
              f'<a href="{R}aussehen/{m["slug"]}/index.html">{esc(m["h1"])}</a>' for m in looks) + '</div>') if looks else ""
        others = ('<h2>Weitere Gruppen</h2><div class="pills">' + "".join(
                  f'<a href="{group_url(o, R)}">{esc(o)}</a>' for o in GROUPS if o != g) + f'<a href="{R}arten/index.html">Alle Arten</a></div>')
        body = (seabar(R) + f'<section class="block page"> <div class="wrap"> <h1>{esc(I["h1"])}</h1> {intro} {tags} '
                f'<ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul> </div> </section>'
                f'{burn}'
                f'<section class="block"><div class="wrap"><div class="prose">{nord_only}{pp}{lk}{others}</div> {byline(R)} </div></section>')
        ld_list = ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": I["h1"], "description": I["desc"], "inLanguage": "de-DE",
                      "url": f"{DOMAIN}/arten/{gslug(g)}/", "isPartOf": {"@id": WEBSITE_ID}, "publisher": {"@id": ORG_ID},
                      "dateModified": CONTENT_UPDATED,
                      "mainEntity": {"@type": "ItemList", "numberOfItems": len(ss),
                                     "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["n"], "url": f"{DOMAIN}/arten/{s['k']}/"} for i, s in enumerate(ss)]}})
        write(f"arten/{gslug(g)}/index.html", page(f"arten/{gslug(g)}/index.html", I["title"], I["desc"], body, active="index",
              crumbs=[("Alle Arten", "arten/index.html"), (g, "")], og=f'{ss[0]["k"]}.webp', extra_ld=ld_list))

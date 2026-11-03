# -*- coding: utf-8 -*-
"""Doppelgänger: Übersicht und Vergleichsseiten."""
import random
from ..core import *
from ..layout import *
from ..components import *

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
            ik = photo_key(k)
            figs += f'<figure>{img(R, ik, name_of(k), eager=True)}{play_button(R, ik, name_of(k), "play-fig")}<figcaption>{esc(name_of(k))} <i lang="la">{esc(lat_of(k))}</i><small>{credit(ik)}</small></figcaption></figure>'
        call = lambda k: (BY[k] if k in BY else EXT[k]).get("call")
        extra = [("Ruf", call(p["a"]), call(p["b"]))] if call(p["a"]) and call(p["b"]) else []
        rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in list(p["rows"]) + extra)
        btns = " ".join(f'<a class="btn{"" if i==0 else " ghost"}" href="{R}arten/{k}/index.html">{esc(name_of(k))} im Porträt</a>' for i, k in enumerate([x for x in (p["a"], p["b"]) if x in BY]))
        others = [q for q in PAIRS if q["k"] != p["k"]]
        rnd = random.Random(p["k"]); rel = rnd.sample(others, 3)
        body = f'''<article class="wrap pairpage"> <h1>{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</h1> <p class="intro">{esc(p["short"])}</p> <div class="ph big"> {figs} </div> <section aria-labelledby="h-cmp"> <h2 id="h-cmp">Die Unterschiede</h2> <div class="cmp-wrap"><table class="cmp"> <thead><tr><td></td><th scope="col">{esc(name_of(p["a"]))}</th><th scope="col">{esc(name_of(p["b"]))}</th></tr></thead> <tbody>{rows}</tbody> </table></div> <p class="merksatz"><b>Merkhilfe:</b> {esc(p["tip"])}</p> <p class="actions"> {btns} </p> </section> <section class="related" aria-labelledby="h-more"> <h2 id="h-more">Weitere Doppelgänger</h2> <ul class="pairs three">{"".join(pair_card(R, q, "h3") for q in rel)}</ul> </section> </article>'''
        write(f"unterscheiden/{p['k']}/index.html", page(f"unterscheiden/{p['k']}/index.html", f"{name_of(p['a'])} oder {name_of(p['b'])}?", p["short"], body, active="unterscheiden",
              crumbs=[("Doppelgänger", "unterscheiden/index.html"), (f"{name_of(p['a'])} oder {name_of(p['b'])}", "")]))

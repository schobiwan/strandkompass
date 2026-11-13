# -*- coding: utf-8 -*-
"""Doppelgänger: Übersicht und Vergleichsseiten."""
import random
from ..core import *
from ..layout import *
from ..components import *

def build_pairs():
    R = "../"
    grp = lambda p: BY[p["a"]]["grp"] if p["a"] in BY else ""
    sec = [("voegel", "Seevögel", lambda g: g == "Seevögel"), ("robben-wale", "Robben, Wale und Delfine", lambda g: g in ("Robben", "Wale & Delfine")),
           ("funde", "Quallen, Muscheln und andere Funde", lambda g: g not in ("Seevögel", "Robben", "Wale & Delfine"))]
    lists = "".join(f'<h2 class="h3 grp-h" id="{i}">{t}</h2><ul class="pairs">{"".join(pair_card(R, p, "h3") for p in PAIRS if f(grp(p)))}</ul>' for i, t, f in sec)
    body = (f'<section class="block page"> <div class="wrap"> <h1>Doppelgänger unterscheiden</h1> <p class="intro">An der Küste sieht sich vieles zum Verwechseln ähnlich: Möwen und Strandläufer, Seehund und Kegelrobbe, Schweinswal und Tümmler. Bei Quallen ist der Unterschied sogar wichtig, weil manche brennen. Diese Merkmale helfen dir.</p>'
            f'{lists} </div> </section>')
    write("unterscheiden/index.html", page("unterscheiden/index.html", "Doppelgänger unterscheiden", "Silbermöwe oder Heringsmöwe, Seehund oder Kegelrobbe, Schweinswal oder Tümmler: Seevögel, Robben, Wale und Quallen sicher unterscheiden.", body, active="unterscheiden", crumbs=[("Doppelgänger", "")]))
    for p in PAIRS:
        R = "../../"
        figs = ""
        for k in (p["a"], p["b"]):
            ik = photo_key(k)
            col = 1 if k == p["a"] else 2
            figs += f'<figure>{img(R, ik, f"{name_of(k)}: {p['rows'][0][0]} {p['rows'][0][col]}", eager=True)}{play_button(R, ik, name_of(k), "play-fig")}<figcaption>{esc(name_of(k))} <i lang="la">{esc(lat_of(k))}</i><small>{credit(ik)}</small></figcaption></figure>'
        call = lambda k: (BY[k] if k in BY else EXT[k]).get("call")
        extra = [("Ruf", call(p["a"]), call(p["b"]))] if call(p["a"]) and call(p["b"]) else []
        rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in list(p["rows"]) + extra)
        btns = " ".join(f'<a class="btn{"" if i==0 else " ghost"}" href="{R}arten/{k}/index.html">{esc(name_of(k))} im Porträt</a>' for i, k in enumerate([x for x in (p["a"], p["b"]) if x in BY]))
        others = [q for q in PAIRS if q["k"] != p["k"]]
        rnd = random.Random(p["k"]); rel = rnd.sample(others, 3)
        body = f'''<article class="wrap pairpage"> <h1>{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</h1> <p class="intro">{esc(p["short"])}</p> {tldr_box(p["tip"])} <div class="ph big"> {figs} </div> <section aria-labelledby="h-cmp"> <h2 id="h-cmp">Die Unterschiede</h2> <div class="cmp-wrap"><table class="cmp"> <thead><tr><td></td><th scope="col">{esc(name_of(p["a"]))}</th><th scope="col">{esc(name_of(p["b"]))}</th></tr></thead> <tbody>{rows}</tbody> </table></div> <p class="actions"> {btns} </p> </section> {byline(R, f'{name_of(p["a"])} oder {name_of(p["b"])}')} <details class="fold related" open data-fold><summary><h2>Weitere Doppelgänger</h2></summary> <ul class="pairs three">{"".join(pair_card(R, q, "h3") for q in rel)}</ul> </details> </article>'''
        write(f"unterscheiden/{p['k']}/index.html", page(f"unterscheiden/{p['k']}/index.html", f"{name_of(p['a'])} oder {name_of(p['b'])}? So erkennst du den Unterschied", p["short"], body, active="unterscheiden",
              crumbs=[("Doppelgänger", "unterscheiden/index.html"), (f"{name_of(p['a'])} oder {name_of(p['b'])}", "")]))

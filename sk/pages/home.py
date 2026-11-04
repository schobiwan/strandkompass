# -*- coding: utf-8 -*-
"""Startseite mit Seevögel-Band, Karussell und Fundliste."""
from ..core import *
from ..icons import *
from ..layout import *
from ..components import *
from ..products import *

BIRD_PRIO = ["eiderente", "basstoelpel", "trottellumme", "austernfischer", "saebelschnaebler", "brandgans", "ringelgans", "sanderling",
             "alpenstrandlaeufer", "mantelmoewe", "flussseeschwalbe", "silbermoewe", "kormoran", "sturmmoewe", "lachmoewe", "heringsmoewe"]

def birdband(R):
    birds = sorted([x for x in SPECIES if x["grp"] == "Seevögel"], key=lambda x: BIRD_PRIO.index(x["k"]) if x["k"] in BIRD_PRIO else 99)
    tiles = "".join(
        f'<li data-k="{x["k"]}" data-act="{acts_attr(x["act"])}"><a href="{R}arten/{x["k"]}/index.html"><img src="{R}photos/{x["k"]}-400.webp" alt="" width="400" height="320" loading="lazy" decoding="async">'
        f'<span class="bt-n">{esc(x["n"])}</span><span class="bt-s">{esc(x["sz"])}{" · nur Nordsee" if x["act"] == ["nord"] else ""}</span></a>{play_button(R, x["k"], x["n"], "play-sm")}{cred(x["k"])}</li>' for x in birds)
    return (f'<section class="birdband" aria-labelledby="bb-h"> <div class="wrap"> <div class="bb-head"><div><p class="kicker">{ICON["bird"]}Seevögel</p>'
            f'<h2 id="bb-h">Seevögel an der Küste</h2><p class="bb-sub">Möwen, Watvögel, Meeresenten und die Felsenbrüter von Helgoland: {counts(birds)} Arten, die dir an Nord- und Ostsee begegnen.</p></div>'
            f'<div class="bb-links"><button type="button" class="btn" data-hgrp="Seevögel">Alle Seevögel in der Liste</button><a class="btn ghost" href="{R}unterscheiden/index.html#voegel">Möwen unterscheiden</a></div></div>'
            f'<ul class="birdtiles">{tiles}</ul> </div> </section>')

def build_home():
    R = ""
    filt = (chipset("Gruppe", "grp", [(g, g) for g in GROUPS]) +
            chipset("Meer", "act", [(k, v) for k, v in ACTS.items()]) +
            chipset("Lebensraum", "hab", [(h, h) for h in HABS]) +
            chipset("Größe", "size", list(SIZES.items())) +
            '<fieldset><legend>Außerdem</legend><div class="fchips"><button class="chip" type="button" data-g="flag" data-v="now" aria-pressed="false">Jetzt im <span data-now-name>November</span> zu finden</button>'
            '</div></fieldset>')
    cards = "".join(card(R, s, i) for i, s in enumerate(sorted(SPECIES, key=skey)))
    NOWM_BUILD = 11
    # Reihenfolge für Tier des Monats und Karussell: auffällige Funde zuerst
    PRIO = BIRD_PRIO + ["kegelrobbe", "seehund", "schweinswal", "bernstein", "kompassqualle", "feuerqualle", "ohrenqualle", "lungenqualle", "seestern",
            "nixentaeschchen", "wellhornschnecke", "strandkrabbe", "einsiedlerkrebs", "seestachelbeere", "blaue-nesselqualle", "herzigel", "donnerkeil"]
    pr = lambda x: PRIO.index(x["k"]) if x["k"] in PRIO else 99
    ranked = sorted(SPECIES, key=lambda x: (0 if NOWM_BUILD in x["h"] else 1, pr(x), skey(x)))
    sp = ranked[0]
    import json
    spotdata = json.dumps([{"k": x["k"], "n": x["n"], "hl": x["hl"].split(". ")[0].rstrip(".") + ".", "h": x["h"], "p": x["p"], "act": x["act"]} for x in ranked], ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    sp_first = sp["hl"].split(". ")[0].rstrip(".") + "."
    gcount = {g: sum(1 for x in SPECIES if x["grp"] == g) for g in GROUPS}
    top = ("Seevögel", "Meeressäuger", "Muscheln", "Quallen")
    gchips = ("".join(f'<button type="button" class="hchip" data-hgrp="{g}">{g}<span class="sr-only"> ({gcount[g]})</span></button>' for g in top)
              + '<a class="hchip hchip-all" href="arten/index.html">Alle Gruppen</a>')
    body = f'''<header class="hero6"> <div class="wrap hero6-in"> <div class="h6-text"> <p class="h6-kicker">{BUOY}<span>Nordsee &amp; Ostsee</span><span aria-hidden="true">·</span><span>{counts(SPECIES)} Arten und Funde</span></p> <h1 class="h6-title"><span class="ht-row"><span class="ht-ico ht-bird">{ICON["bird"]}</span>Wer fliegt da?</span> <span class="ht-row"><span class="ht-ico ht-shell">{SHELL}</span>Was liegt da?</span></h1> <p class="lede">Seevögel, Robben und Wale, Muscheln, Quallen und Strandfunde bestimmen: am Foto und an wenigen sicheren Merkmalen.</p> <form class="hsearch" id="hsearch" role="search" aria-label="Fund suchen"> <label for="hq"><span class="sr-only">Fund suchen</span>{ICON["find"]}<input type="search" id="hq" placeholder="Zum Beispiel Austernfischer" autocomplete="off" enterkeyhint="search"></label> <button class="hsearch-btn" type="submit">Suchen</button> </form> <div class="h6-sea"><span class="h6-l">Ich bin an der</span>{seaswitch()}</div> <div class="hchips" role="group" aria-label="Nach Gruppe zeigen">{gchips}</div> </div>
<figure class="spot6" id="spot"> <a href="arten/{sp["k"]}/index.html" id="spot-link" class="s6-link"><span class="s6-photo"><img id="spot-img" src="photos/{sp["k"]}.webp" srcset="photos/{sp["k"]}-400.webp 400w, photos/{sp["k"]}.webp 720w" sizes="(max-width: 900px) 92vw, 560px" alt="" width="720" height="576" fetchpriority="high"></span> <span class="s6-label"><span class="spot-tag">Fund des Monats · <span data-now-name>November</span></span><b id="spot-name">{esc(sp["n"])}</b><span id="spot-hl">{esc(sp_first)}</span></span></a> <small class="spot-cred" id="spot-cred">{credit(sp["k"], True)}</small> </figure> </div>
{RIPPLES} </header>
{birdband(R)}
<div class="wrap grid-head"><h2 id="arten-h">Alle Funde</h2><p class="actlegend"><span class="act">{act_svg("nord")}</span> Nordsee <span class="act act-o">{act_svg("ost")}</span> Ostsee</p></div> <div class="bar" id="arten"> <div class="wrap barrow" role="search" aria-label="Funde suchen und filtern"> <label class="search" for="q">{ICON["find"]}<span class="sr-only">Fund suchen</span> <input type="search" id="q" placeholder="Suchen, z. B. Qualle" autocomplete="off" enterkeyhint="search"></label> <button class="chip ftoggle" id="f-toggle" type="button" aria-expanded="false" aria-controls="fpanel"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"></path></svg>Filter<b class="fcount" id="fcount" hidden></b></button> <label class="sortsel" for="sort"><span>Sortieren</span> <select id="sort"><option value="now">Jetzt zu finden zuerst</option><option value="az">Name A–Z</option><option value="size">Größe, klein zuerst</option></select></label> <span class="rcount" id="rcount" aria-live="polite">{len(SPECIES)} Funde</span> </div> <div class="fpanel" id="fpanel" hidden> <div class="wrap fgrid"> {filt} <div class="factions"><button class="btn ghost" id="f-reset" type="button">Alle Filter zurücksetzen</button><button class="btn" id="f-done" type="button">Ergebnisse anzeigen</button></div> </div> </div> <div class="wrap active" id="active" hidden></div> </div>
<section class="sub" aria-labelledby="arten-h"> <div class="wrap"> <ul class="grid" id="grid"> {cards} </ul> <p class="gridmore" id="gridmore" hidden><button class="btn ghost" type="button" id="more-btn"></button></p> <div class="empty" id="empty" hidden><p>Kein Fund passt zu deiner Suche oder Auswahl.</p><button class="btn ghost" type="button" id="empty-reset">Suche und Filter zurücksetzen</button></div> </div> </section>
{seapair(R)}
<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Gut ausgerüstet an den Strand</h2><a class="gearmore" href="ausruestung/index.html">Alle Empfehlungen ansehen</a></div><ul class="products"> {"".join(product(R, g) for g in ("uvlampe", "fernglas", "vogelbuch", "buch"))} </ul>{ADNOTE}</div></section>
<section class="block"> <div class="wrap"> <h2>Weiter entdecken</h2> <ul class="explore"> <li><a href="arten/index.html"><b>Alle Funde nach Gruppen</b><span>Alle {len(SPECIES)} Arten und Funde auf einen Blick, von den Seevögeln bis zu Bernstein und Donnerkeil.</span></a></li> <li><a href="ausruestung/index.html"><b>Ausrüstung</b><span>UV-Lampe für die Bernsteinsuche, Becherlupe, Kescher und Wattschuhe.</span></a></li> <li><a href="https://vogelkompass.de/" rel="noopener"><b>Noch mehr Vögel</b><span>Garten-, Feld- und Waldvögel bestimmst du auf der Schwesterseite Vogelkompass.</span></a></li> </ul> </div> </section> <script type="application/json" id="spotdata">{spotdata}</script>'''
    write("index.html", page("index.html", "Strandkompass – Seevögel und Strandfunde an Nord- und Ostsee bestimmen",
        f"Seevögel und Strandfunde bestimmen: {len(SPECIES)} Möwen, Watvögel, Robben, Wale, Muscheln, Quallen, Krebse und Steine von Nord- und Ostsee mit Doppelgängern und Strandkalender.",
        body, active="index", scripts=("home.js",), is_home=True))

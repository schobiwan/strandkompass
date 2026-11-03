# -*- coding: utf-8 -*-
"""Übersicht aller Funde und die einzelnen Fundseiten."""
from ..core import *
from ..icons import *
from ..layout import *
from ..components import *
from ..products import *

def build_arten_index():
    R = "../"
    sec = []
    for g in GROUPS:
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=lambda x: x["n"])
        sec.append(f'<h2 class="h3 grp-h" data-grp-h="{esc(g)}">{g}</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul>')
    body = seabar(R) + f'<section class="block page"> <div class="wrap"> <h1>Alle Strandfunde</h1> <p class="intro">{counts(SPECIES)} Arten und Funde, nach Gruppen geordnet, die Seevögel zuerst. Zum Suchen und Filtern geht es zur <a href="../index.html#arten">Startseite</a>.</p> {"".join(sec)} </div> </section>'
    write("arten/index.html", page("arten/index.html", "Alle Strandfunde", "Alle Strandfunde im Überblick: Seevögel, Muscheln, Schnecken, Quallen, Krebse, Seesterne, Tang, Steine und Meeressäuger.", body, crumbs=[("Funde", "")]))

def build_species(s):
    R = "../../"
    k = s["k"]
    acts = ", ".join(ACTS[a] for a in s["act"])
    habs = "".join(f"<span>{esc(h)}</span>" for h in s["hab"])
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] + [("Meer", acts)])
    life = "".join(f'<details class="fold" open data-fold><summary><h3>{esc(a)}</h3></summary><p>{esc(b)}</p></details>' for a, b in s["life"])
    peaklinks = [f'<a href="{R}strandjahr/{MSLUG[m-1]}/index.html">{MONTHS[m-1]}</a>' for m in s["h"]]
    pl = peaklinks[0] if len(peaklinks) == 1 else ", ".join(peaklinks[:-1]) + " und " + peaklinks[-1]
    yeartext = (f'{"Das" if s["g"]=="n" else ("Die" if s["g"]=="f" else "Der")} {esc(s["n"])} ist {"das ganze Jahr über zu finden" if len(s["p"])==12 else "von " + mrange(s["p"]) + " zu finden"}. '
                f'Am besten im {pl}. {esc(s["hl"])}')
    alike = ""
    if s["alike"]:
        p = PAIRBY[s["alike"]]
        other = p["b"] if p["a"] == k else p["a"]
        okey = photo_key(other)
        alike = (f'<section class="alike" aria-labelledby="h-alike"> {img(R, okey, name_of(other))} <div> <h2 id="h-alike">Nicht verwechseln mit {ein(BY[other]["g"] if other in BY else EXT[other]["g"], "dat")} {esc(name_of(other))}</h2> '
                 f'<p>{esc(p["short"])}</p> <p><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}? Alle Unterschiede</a></p> </div> </section>')
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    gear = GEAR_FOR.get(k) or GEAR_GRP[s["grp"]]
    body = f'''<article class="sp wrap"> <div class="sp-top"> <figure class="sp-photo"> {img(R, k, s["n"], eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> <div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> <p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{"".join(f'<span class="tag act-tag act-{a}">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])}{'<span class="tag act-tag act-none">nicht an der Ostsee</span>' if s["act"] == ["nord"] else ""}</p> <p class="habs">{habs}</p> <p class="text">{esc(s["short"])} {esc(s["hl"])}</p>  </div> </div>
<div class="sp-cols"> <div class="sp-main"> <section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {"sie" if s["g"]=="f" else ("es" if s["g"]=="n" else "ihn")}</h2> <ul class="marks">{"".join(f"<li>{esc(m)}</li>" for m in s["marks"])}</ul> <dl class="facts">{facts}</dl> </section> {seabox(s)} <section aria-labelledby="h-year"> <h2 id="h-year">Wann im Jahr</h2> {months_bar(s)} <p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{yeartext}</p> </section> <section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> <section class="helpbox" aria-label="Hilfe und Beobachtung"> <details class="fold" open data-fold><summary><h2>Rücksicht und Sicherheit</h2></summary><p>{esc(s["help"])}</p></details> <details class="fold" open data-fold><summary><h2>Suchtipp</h2></summary><p>{esc(s["tip"])}</p></details> </section> {alike} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> <ul class="morelinks"> <li><a href="{wiki}" target="_blank" rel="noopener">Wikipedia<span class="sr-only"> (öffnet in neuem Fenster)</span></a></li> </ul> </section> </div>
<aside class="sp-side" aria-label="Empfehlungen"> <section class="gearbox" aria-labelledby="h-gear"><h2 id="h-gear">Passend dazu</h2><ul class="products compact"> {"".join(product(R, g, True) for g in gear)} </ul>{ADNOTE}</section> </aside> </div> </article>'''
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", f"{s['n']} erkennen", f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Lebensweise und wann du {'sie' if s['g']=='f' else ('es' if s['g']=='n' else 'ihn')} am Strand findest.",
                                        body, crumbs=[("Funde", "arten/index.html"), (s["n"], "")], og=f"{k}.webp"))

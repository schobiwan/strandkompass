# -*- coding: utf-8 -*-
"""Übersicht aller Arten und Funde und die einzelnen Artseiten."""
from ..core import *
from ..icons import *
from ..layout import *
from ..components import *
from ..products import *
from .looks import looks_for

def build_arten_index():
    R = "../"
    sec = []
    for g in GROUPS:
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=skey)
        sec.append(f'<h2 class="h3 grp-h" id="{gslug(g)}" data-grp-h="{esc(g)}">{esc(g)}</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul>')
    jump = '<nav class="pills grpjump" aria-label="Gruppen">' + "".join(f'<a href="#{gslug(g)}">{esc(g)}</a>' for g in GROUPS) + '</nav>'
    body = seabar(R) + f'<section class="block page"> <div class="wrap"> <h1>Alle Arten und Funde</h1> <p class="intro">{counts(SPECIES)} Arten und Funde, nach Gruppen geordnet: zuerst Seevögel, dann Robben, Wale und Delfine, danach Quallen, Muscheln und andere Strandfunde. Suchen und filtern kannst du auf der <a href="../index.html#arten">Startseite</a>.</p> {jump} {"".join(sec)} </div> </section>'
    write("arten/index.html", page("arten/index.html", "Alle Arten und Funde", "Alle Arten und Funde im Überblick: Seevögel, Robben, Wale und Delfine, Quallen, Muscheln, Schnecken, Krebse, Seesterne, Tang und Strandfunde.", body, active="index", crumbs=[("Alle Arten", "")]))

def build_species(s):
    R = "../../"
    k = s["k"]
    habs = " · ".join(esc(h) for h in s["hab"])
    # Meer, Ruf, Fundort und Brennen stehen schon oben (Marken, Ruf-Kasten, Kurz gesagt), deshalb nicht noch einmal im Steckbrief
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] if not (a == "Ruf" and s.get("call")) and a not in ("Wo zu finden", "Brennt sie?"))
    life = "".join(f'<details class="fold" open data-fold><summary><h3>{esc(a)}</h3></summary><p>{esc(b)}</p></details>' for a, b in s["life"])
    peak = [MONTHS[m-1] for m in s["h"]]
    pl = peak[0] if len(peak) == 1 else ", ".join(peak[:-1]) + " und " + peak[-1]
    # Der Satz zur Jahreszeit (hl) steht schon in der Einleitung, hier nur die Monate
    yeartext = (f'{esc(mit_artikel(k).capitalize()[0] + mit_artikel(k)[1:])} ist {"das ganze Jahr über zu finden" if len(s["p"])==12 else "von " + mrange(s["p"]) + " zu finden"}. '
                f'Am besten im {pl}. <a href="{R}strandjahr/index.html">Im Küstenjahr ansehen</a>')
    alike = ""
    if s["alike"]:
        p = PAIRBY[s["alike"]]
        other = p["b"] if p["a"] == k else p["a"]
        okey = photo_key(other)
        alike = (f'<section class="alike" aria-labelledby="h-alike"> {img(R, okey, name_of(other))} <div> <h2 id="h-alike">Nicht verwechseln mit {esc(mit_artikel(other, "dat"))}</h2> '
                 f'<p>{esc(p["short"])}</p> <p><a href="{R}unterscheiden/{p["k"]}/index.html">{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}? Alle Unterschiede</a></p> </div> </section>')
    sib = [x for x in sorted(SPECIES, key=skey) if x["grp"] == s["grp"] and x["k"] != k][:6]
    same = (f'<p class="h4">Mehr {esc(s["grp"])}</p><div class="pills">' + "".join(f'<a href="{R}arten/{x["k"]}/index.html">{esc(x["n"])}</a>' for x in sib) + '</div>') if sib else ""
    lk = looks_for(k)
    same += (f'<p class="h4">Nach Aussehen</p><div class="pills">' + "".join(f'<a href="{R}aussehen/{m["slug"]}/index.html">{esc(m["h1"])}</a>' for m in lk) + '</div>') if lk else ""
    same += '<p class="h4">Weiterlesen</p>' if same else ""
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    gear = GEAR_FOR.get(k) or GEAR_GRP[s["grp"]]
    # Überschriften als Fragen, wie Leute sie suchen; Tiere beobachtet man, Funde findet man
    nom, acc, dat = (esc(mit_artikel(k, c)) for c in ("nom", "acc", "dat"))
    see, verb = ("zu sehen", "beobachtest") if s["grp"] in MOBILE else ("zu finden", "findest")
    dat = "beim " + dat[4:] if dat.startswith("dem ") else "bei " + dat
    # Kurz gesagt: das Wichtigste auf einen Blick, ganz oben
    fact = dict(s["facts"])
    when = mrange(s["p"]); when = when[0].upper() + when[1:] + (f", am besten im {pl}" if len(s["h"]) < 12 else "")
    third = (("Brennt sie?", fact["Brennt sie?"]) if "Brennt sie?" in fact else ("Ruf", s["call"]) if s.get("call") else ("Größe", fact["Größe"]))
    # was im Kasten steht, nicht noch einmal im Steckbrief
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] if not (a == "Ruf" and s.get("call")) and a not in ("Wo zu finden", third[0]))
    tldr = ('<section class="tldr" aria-labelledby="h-tldr"><h2 id="h-tldr">Kurz gesagt</h2><dl>'
            f'<dt>Erkennen</dt><dd>{" · ".join(esc(m) for m in s["marks"][:2])}</dd>'
            f'<dt>{"Zu sehen" if see == "zu sehen" else "Zu finden"}</dt><dd>{esc(when)}</dd>'
            f'<dt>Wo</dt><dd>{esc(fact["Wo zu finden"])}</dd>'
            f'<dt>{esc(third[0])}</dt><dd>{esc(third[1])}</dd></dl></section>')
    # Blättern: vorherige und nächste Art in der Reihenfolge der Übersicht (Gruppe, dann Name)
    order = [x for g in GROUPS for x in sorted((y for y in SPECIES if y["grp"] == g), key=skey)]
    i = order.index(s)
    prv, nxt = (order[i - 1] if i > 0 else None), (order[i + 1] if i < len(order) - 1 else None)
    pager = ('<nav class="pager" aria-label="Weitere Arten">'
             + (f'<a rel="prev" href="{R}arten/{prv["k"]}/index.html"><span>Vorherige Art</span><b>{esc(prv["n"])}</b></a>' if prv else "")
             + (f'<a rel="next" href="{R}arten/{nxt["k"]}/index.html"><span>Nächste Art</span><b>{esc(nxt["n"])}</b></a>' if nxt else "") + '</nav>')
    page_ld = ld({"@context": "https://schema.org", "@type": "WebPage", "name": f'{s["n"]} ({s["lat"]})', "description": s["short"], "inLanguage": "de-DE",
                  "url": f'{DOMAIN}/arten/{k}/', "isPartOf": {"@id": WEBSITE_ID}, "publisher": {"@id": ORG_ID}, "author": AUTHOR,
                  "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/photos/{k}.webp"},
                  "about": {"@type": "Thing", "name": s["n"], "alternateName": s["lat"]}})
    body = f'''<article class="sp wrap"> <div class="sp-top"> <figure class="sp-photo"> {img(R, k, s["n"], eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> <div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> <p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{"".join(f'<span class="tag act-tag act-{a}">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])}{'<span class="tag act-tag act-none">nicht an der Ostsee</span>' if s["act"] == ["nord"] else ""}</p> <p class="habs"><span class="habs-l">Lebensraum:</span> {habs}</p> {callbox(R, s)} <p class="text">{esc(s["short"])} {esc(s["hl"])}</p>  </div> </div>
<div class="sp-cols"> <div class="sp-main"> {tldr} <section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {acc}</h2> <ul class="marks">{"".join(f"<li>{esc(m)}</li>" for m in s["marks"])}</ul> <dl class="facts">{facts}</dl> </section> {seabox(s)} <section aria-labelledby="h-year"> <h2 id="h-year">Wann ist {nom} {see}?</h2> {months_bar(s)} <p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{yeartext}</p> </section> <section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> <section class="helpbox" aria-label="Hilfe und Beobachtung"> <details class="fold" open data-fold><summary><h2>Was du {dat} beachten solltest</h2></summary><p>{esc(s["help"])}</p></details> <details class="fold" open data-fold><summary><h2>Wo und wie du {acc} {verb}</h2></summary><p>{esc(s["tip"])}</p></details> </section> {alike} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> {same} <ul class="morelinks"> <li><a href="{wiki}" target="_blank" rel="noopener">Wikipedia<span class="sr-only"> (öffnet in neuem Fenster)</span></a></li> </ul> </section> {pager} </div>
<aside class="sp-side" aria-label="Empfehlungen"> <section class="gearbox" aria-labelledby="h-gear"><h2 id="h-gear">Passend dazu</h2><ul class="products compact"> {"".join(product(R, g, True) for g in gear)} </ul>{ADNOTE}</section> </aside> </div> </article>'''
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", f"{s['n']} erkennen", f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Lebensweise und wann du {'sie' if s['g']=='f' else ('es' if s['g']=='n' else 'ihn')} am Strand findest.",
                                        body, active="index", crumbs=[("Alle Arten", "arten/index.html"), (s["n"], "")], og=f"{k}.webp", extra_ld=page_ld))

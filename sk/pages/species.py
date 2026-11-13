# -*- coding: utf-8 -*-
"""Übersicht aller Arten und Funde und die einzelnen Artseiten."""
from ..core import *
from ..icons import *
from ..layout import *
from ..components import *
from ..products import species_pick, gear_inline, AD_SHORT
from ..trips import species_tour
from .looks import looks_for

def build_arten_index():
    R = "../"
    sec = []
    for g in GROUPS:
        ss = sorted([s for s in SPECIES if s["grp"] == g], key=skey)
        sec.append(f'<h2 class="h3 grp-h" id="{gslug(g)}" data-grp-h="{esc(g)}"><a href="{gslug(g)}/index.html">{esc(g)}</a></h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(ss))}</ul>')
    jump = '<nav class="pills grpjump" aria-label="Gruppen">' + "".join(f'<a href="#{gslug(g)}">{esc(g)}</a>' for g in GROUPS) + '</nav>'
    body = seabar(R) + f'<section class="block page"> <div class="wrap"> <h1>Alle Arten und Funde</h1> <p class="intro">{counts(SPECIES)} Arten und Funde, nach Gruppen geordnet: zuerst Seevögel, dann Robben, Wale und Delfine, danach Quallen, Muscheln und andere Strandfunde. Suchen und filtern kannst du auf der <a href="../index.html#arten">Startseite</a>.</p> {jump} {"".join(sec)} </div> </section>'
    write("arten/index.html", page("arten/index.html", "Alle Arten an Nord- und Ostsee: Seevögel, Robben, Quallen, Muscheln", "Alle Arten und Funde im Überblick: Seevögel, Robben, Wale und Delfine, Quallen, Muscheln, Schnecken, Krebse, Seesterne, Tang und Strandfunde.", body, active="index", crumbs=[("Alle Arten", "")]))

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
    wiki = "https://de.wikipedia.org/w/index.php?search=" + s["lat"].replace(" ", "+")
    # „Mehr erfahren“ als Zeilen: links die Art des Links, rechts die Links; auf dem Handy untereinander
    pill = lambda h, t: f'<a href="{h}">{esc(t)}</a>'
    rows = [(f'Mehr {esc(s["grp"])}', pill(f'{R}arten/{gslug(s["grp"])}/index.html', f'Alle {s["grp"]}') + "".join(pill(f'{R}arten/{x["k"]}/index.html', x["n"]) for x in sib)),
            ("Nach Aussehen", "".join(pill(f'{R}aussehen/{m["slug"]}/index.html', m["h1"]) for m in looks_for(k))),
            ("Ausrüstung", (pill(f"{R}ratgeber/fernglas/index.html", "Fernglas für die Küste") if s["grp"] in MOBILE else "") + gear_inline(species_pick(s))),
            ("Erleben", species_tour(s)),
            ("Weiterlesen", ext_link(wiki, 'Wikipedia'))]
    adshort = AD_SHORT.replace("Werbelink zu Amazon: Kaufst du darüber", "Werbelink zu Amazon bzw. GetYourGuide: Kaufst oder buchst du darüber") if species_tour(s) else AD_SHORT
    more = '<dl class="morerows">' + "".join(f'<div><dt>{t}</dt><dd class="pills">{v}</dd></div>' for t, v in rows if v) + '</dl>' 
    # Überschriften als Fragen, wie Leute sie suchen; Tiere beobachtet man, Funde findet man
    nom, acc, dat = (esc(mit_artikel(k, c)) for c in ("nom", "acc", "dat"))
    see, verb = ("zu sehen", "beobachtest") if s["grp"] in MOBILE else ("zu finden", "findest")
    dat = "beim " + dat[4:] if dat.startswith("dem ") else "bei " + dat
    # Kurz gesagt: wann, wo und das Wichtigste daneben (die Merkmale stehen direkt links bzw. darunter)
    fact = dict(s["facts"])
    when = mrange(s["p"]); when = when[0].upper() + when[1:] + (f", am besten im {pl}" if len(s["h"]) < 12 else "")
    third = (("Brennt sie?", fact["Brennt sie?"]) if "Brennt sie?" in fact else ("Ruf", s["call"]) if s.get("call") else ("Größe", fact["Größe"]))
    # was im Kasten steht, nicht noch einmal im Steckbrief
    facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["facts"] if not (a == "Ruf" and s.get("call")) and a not in ("Wo zu finden", third[0]))
    tldr = tldr_box([("Zu sehen" if see == "zu sehen" else "Zu finden", when), ("Wo", fact["Wo zu finden"]), third])
    # Blättern: vorherige und nächste Art in der Reihenfolge der Übersicht (Gruppe, dann Name)
    order = [x for g in GROUPS for x in sorted((y for y in SPECIES if y["grp"] == g), key=skey)]
    i = order.index(s)
    prv, nxt = (order[i - 1] if i > 0 else None), (order[i + 1] if i < len(order) - 1 else None)
    pager = ('<nav class="pager" aria-label="Weitere Arten">'
             + (f'<a rel="prev" href="{R}arten/{prv["k"]}/index.html"><span>Vorherige Art</span><b>{esc(prv["n"])}</b></a>' if prv else "")
             + (f'<a rel="next" href="{R}arten/{nxt["k"]}/index.html"><span>Nächste Art</span><b>{esc(nxt["n"])}</b></a>' if nxt else "") + '</nav>')
    # Titel nach Suchabsicht: bei Seevögeln mit Ruf wird oft nach dem Ruf gesucht, bei Quallen nach „brennt“
    title = (f"{s['n']}: Ruf anhören, Merkmale und Doppelgänger" if k in AUDIO else
             f"{s['n']}: Brennt sie? Merkmale und Vorkommen" if "Brennt sie?" in fact else
             f"{s['n']} erkennen: Merkmale und Vorkommen")
    audio_ld = {"audio": {"@type": "AudioObject", "name": f"Ruf: {s['n']}", "contentUrl": f"{DOMAIN}/audio/{k}.mp3", "encodingFormat": "audio/mpeg"}} if k in AUDIO else {}
    page_ld = ld({"@context": "https://schema.org", "@type": "WebPage", "name": f'{s["n"]} ({s["lat"]})', "description": s["short"], "inLanguage": "de-DE",
                  "url": f'{DOMAIN}/arten/{k}/', "isPartOf": {"@id": WEBSITE_ID}, "publisher": {"@id": ORG_ID}, "author": AUTHOR,
                  "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/photos/{k}.webp"},
                  "about": {"@type": "Thing", "name": s["n"], "alternateName": s["lat"]},
                  "datePublished": CONTENT_PUBLISHED, "dateModified": CONTENT_UPDATED, **audio_ld})
    body = f'''<article class="sp wrap"> <div class="sp-top"> <figure class="sp-photo"> {img(R, k, f'{s["n"]}: {s["marks"][0]}', eager=True, sizes="(max-width: 760px) 92vw, 560px")} <figcaption>{credit(k)}</figcaption> </figure> <div class="sp-intro"> <h1>{esc(s["n"])}</h1> <p class="latin" lang="la">{esc(s["lat"])}</p> <p class="row"><span class="tag status">{esc(s["grp"])}</span><span class="tag">{esc(s["sz"])}</span>{"".join(f'<span class="tag act-tag act-{a}">{act_svg(a)}{ACTS[a]}</span>' for a in s["act"])}{'<span class="tag act-tag act-none">nicht an der Ostsee</span>' if s["act"] == ["nord"] else ""}</p> <p class="habs"><span class="habs-l">Lebensraum:</span> {habs}</p> {callbox(R, s)} <p class="text">{esc(s["short"])} {esc(s["hl"])}</p>  </div> </div>
<div class="sp-cols"> <aside class="sp-side" aria-label="Auf einen Blick"> {tldr} </aside> <div class="sp-main"> <section aria-labelledby="h-marks"> <h2 id="h-marks">So erkennst du {acc}</h2> <ul class="marks">{"".join(f"<li>{esc(m)}</li>" for m in s["marks"])}</ul> <dl class="facts">{facts}</dl> </section> {seabox(s)} <section aria-labelledby="h-year"> <h2 id="h-year">Wann ist {nom} {see}?</h2> {months_bar(s)} <p class="sr-only">Aktiv: {mlist(s["p"])}. Hauptzeit: {mlist(s["h"])}.</p> <p class="yeartext">{yeartext}</p> </section> <section class="life" aria-labelledby="h-life"> <h2 id="h-life">Lebensweise</h2> {life} </section> <section class="helpbox" aria-label="Hilfe und Beobachtung"> <details class="fold" open data-fold><summary><h2>Was du {dat} beachten solltest</h2></summary><p>{esc(s["help"])}</p></details> <details class="fold" open data-fold><summary><h2>Wo und wie du {acc} {verb}</h2></summary><p>{esc(s["tip"])}</p></details> </section> {alike} <section class="more" aria-labelledby="h-more"> <h2 id="h-more">Mehr erfahren</h2> {more} {adshort} </section> {byline(R)} {pager} </div> </div> </article>'''
    write(f"arten/{k}/index.html", page(f"arten/{k}/index.html", title, f"{s['n']} ({s['lat']}): {s['short']} Merkmale, Lebensweise und wann du {'sie' if s['g']=='f' else ('es' if s['g']=='n' else 'ihn')} am Strand findest.",
                                        body, active="index", crumbs=[("Alle Arten", "arten/index.html"), (s["grp"], f'arten/{gslug(s["grp"])}/index.html'), (s["n"], "")], og=f"{k}.webp", extra_ld=page_ld))

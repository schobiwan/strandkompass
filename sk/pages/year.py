# -*- coding: utf-8 -*-
"""Küstenjahr: Kalender und Monatsseiten (URL bleibt /strandjahr/)."""
from ..core import *
from ..layout import *
from ..components import *
from ..products import *

def cal_table(R):
    head = "".join(f'<th scope="col" data-month="{m}"><a href="{R}strandjahr/{MSLUG[m-1]}/index.html"><abbr title="{MONTHS[m-1]}"><span class="ml">{MSHORT[m-1]}</span><span class="ms" aria-hidden="true">{MONTHS[m-1][0]}</span></abbr></a></th>' for m in range(1, 13))
    rows = []
    for g in GROUPS:
        rows.append(f'<tr class="grow"><th scope="rowgroup" colspan="13">{g}</th></tr>')
        for s in sorted([x for x in SPECIES if x["grp"] == g], key=skey):
            tds = ""
            for m in range(1, 13):
                c = "h" if m in s["h"] else ("p" if m in s["p"] else "")
                t = "beste Zeit" if c == "h" else ("zu finden" if c == "p" else "kaum zu finden")
                tds += f'<td data-month="{m}" class="m {c}" title="{esc(s["n"])}, {MONTHS[m-1]}: {t}"><span class="sr-only">{MONTHS[m-1]}: {t}</span></td>'
            rows.append(f'<tr data-act="{acts_attr(s["act"])}"><th scope="row" class="n"><a href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></th> {tds} </tr>')
    return f'<div class="cal-wrap"><table class="cal"> <caption class="sr-only">Wann welche Art zu erwarten ist</caption> <thead><tr><th scope="col"><span class="sr-only">Art</span></th> {head}</tr></thead> <tbody> {"".join(rows)} </tbody> </table></div>'

def build_year():
    R = "../"
    links = ""
    for m in range(1, 13):
        links += f'<li data-month="{m}"><a href="{R}strandjahr/{MSLUG[m-1]}/index.html"><b>{MONTHS[m-1]}</b><span>{counts([s for s in SPECIES if m in s["p"]])} zu finden, {counts([s for s in SPECIES if m in s["h"]])} in bester Zeit</span></a></li>'
    events = "".join(f'<li data-month="{m}"><b>{MONTHS[m-1]}</b>' + "".join(f'<span data-sea-only="{sea}">{esc(t)}</span>' for sea, t in MONTH_EVENTS[m][:2]) + '</li>' for m in range(1, 13))
    body = seabar(R) + f'''<section class="block page"> <div class="wrap"> <h1>Das Küstenjahr</h1> <p class="intro">Was an der Küste wann passiert: Vogelzug im Wattenmeer, Lummensprung, Heuler auf den Sandbänken, Quallenzeit und Bernstein nach dem Sturm. Wähle einen Monat, um zu sehen, was du dann entdecken kannst.</p> <ul class="monthlinks">{links}</ul> </div> </section>
<section class="block" aria-labelledby="h-ev"> <div class="wrap"> <h2 id="h-ev">Das Wichtigste im Jahreslauf</h2> <ul class="yearline" data-scroll-now>{events}</ul> </div> </section>
<section class="block" aria-labelledby="h-cal"> <div class="wrap"> <h2 id="h-cal">Wann findest du was?</h2> <p class="intro">Monate, in denen du eine Art erwarten kannst, und wann die besten Chancen sind.</p> <ul class="callegend" aria-label="Legende"><li><i class="lgi p"></i>zu finden</li><li><i class="lgi h"></i>beste Zeit</li><li><i class="lgi now"></i>aktueller Monat</li></ul> {cal_table(R)} </div> </section>'''
    write("strandjahr/index.html", page("strandjahr/index.html", "Das Küstenjahr", "Küstenkalender für Nord- und Ostsee: wann Seevögel, Heuler, Schweinswale, Quallen und Bernstein zu erwarten sind, Monat für Monat.", body, active="strandjahr", crumbs=[("Küstenjahr", "")]))
    for m in range(1, 13):
        R = "../../"
        bf = lambda x: (x["grp"] != "Seevögel", skey(x))
        peak = sorted([s for s in SPECIES if m in s["h"]], key=bf)
        act = sorted([s for s in SPECIES if m in s["p"] and m not in s["h"]], key=bf)
        sleep = sorted([s for s in SPECIES if m not in s["p"]], key=skey)
        ev = "".join(ev_li(e, True) for e in MONTH_EVENTS[m])
        prev_m, next_m = (m - 2) % 12 + 1, m % 12 + 1
        sl = ('<section class="block" aria-labelledby="h-sl"><div class="wrap"><h2 id="h-sl">Jetzt kaum zu finden</h2><div class="pills">'
              + "".join(f'<a data-act="{acts_attr(s["act"])}" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a>' for s in sleep) + '</div></div></section>') if sleep else ""
        body = seabar(R) + f'''<section class="block page"> <div class="wrap"> <h1>Die Küste im {MONTHS[m-1]}</h1> <p class="intro">{counts(peak + act)} der {counts(SPECIES)} Arten und Funde kannst du im {MONTHS[m-1]} erwarten, {counts(peak)} davon besonders häufig.</p> <ul class="evlist">{ev}</ul> <p class="actions"><a class="btn ghost" href="{R}strandjahr/{MSLUG[prev_m-1]}/index.html">← {MONTHS[prev_m-1]}</a> <a class="btn ghost" href="{R}strandjahr/{MSLUG[next_m-1]}/index.html">{MONTHS[next_m-1]} →</a></p> </div> </section>
<section class="block" aria-labelledby="h-pk"><div class="wrap"><h2 id="h-pk">Jetzt besonders gut zu sehen</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(peak))}</ul></div></section>
<section class="block" aria-labelledby="h-ac"><div class="wrap"><h2 id="h-ac">Außerdem zu finden</h2><ul class="grid">{"".join(card(R, s, i) for i, s in enumerate(act))}</ul></div></section> {sl} {month_gear(R, m)}'''
        write(f"strandjahr/{MSLUG[m-1]}/index.html", page(f"strandjahr/{MSLUG[m-1]}/index.html", f"Die Küste im {MONTHS[m-1]}", f"Was du im {MONTHS[m-1]} an Nord- und Ostsee entdecken kannst: {MONTH_EVENTS[m][0][1]}", body, active="strandjahr",
              crumbs=[("Küstenjahr", "strandjahr/index.html"), (MONTHS[m-1], "")]))

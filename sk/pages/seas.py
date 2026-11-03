# -*- coding: utf-8 -*-
"""Nordsee, Ostsee und der Vergleich beider Meere."""
from ..core import *
from ..icons import *
from ..layout import *
from ..components import *

def build_seas():
    for k in ("nord", "ost"):
        I = SEA_INFO[k]; R = "../"
        here = [x for x in SPECIES if k in x["act"]]
        only = [x for x in here if x["act"] == [k]]
        other = "ost" if k == "nord" else "nord"
        not_here = [x for x in SPECIES if x["act"] == [other]]
        order = lambda ss: sorted(ss, key=lambda x: (GROUPS.index(x["grp"]), x["n"]))
        facts = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in I["facts"])
        places = "".join(f'<li><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in I["places"])
        why = "".join(f'<h2>{esc(a)}</h2><p>{esc(b)}</p>' for a, b in I["why"])
        birds = [x for x in order(here) if x["grp"] == "Seevögel"]
        rest = [x for x in order(here) if x["grp"] != "Seevögel"]
        sec = lambda hid, t, intro, ss: (f'<section class="block" aria-labelledby="{hid}"><div class="wrap"><h2 id="{hid}">{t}</h2>{intro}'
                                        f'<ul class="grid">{"".join(card(R, x, i) for i, x in enumerate(ss))}</ul></div></section>') if ss else ""
        miss = (f'<section class="block"><div class="wrap"><h2>An der {I["name"]} kaum zu finden</h2><p class="intro">Diese Arten und Funde gibt es nur an der {SEA_INFO[other]["name"]}.</p><div class="pills">'
                + "".join(f'<a href="{R}arten/{x["k"]}/index.html">{esc(x["n"])}</a>' for x in order(not_here)) + '</div></div></section>') if not_here else ""
        body = f'''<section class="block page seahero seahero-{k}"> <div class="wrap"> <p class="kicker">{ICON["seas"]}Nord- und Ostsee</p> <h1>{esc(I["h1"])}</h1> <p class="intro">{esc(I["lede"])}</p> <dl class="facts seafacts">{facts}</dl> <p class="row"><span class="tag">{len(here)} Arten und Funde</span><span class="tag">{len(birds)} Seevögel</span>{f'<span class="tag status">{len(only)} nur an der {I["name"]}</span>' if only else ""}</p> </div> </section>
{sec("h-birds", f"Seevögel an der {I['name']}", "", birds)}
{sec("h-rest", f"Strandfunde und Meerestiere an der {I['name']}", f'<p class="intro">{"Mit Markierung N oder O siehst du, ob es den Fund auch am anderen Meer gibt."}</p>', rest)}
{miss}
<section class="block" aria-labelledby="h-places"><div class="wrap"><h2 id="h-places">Gute Orte an der {I["name"]}</h2><ul class="explore tips">{places}</ul></div></section>
<section class="block"><div class="wrap prose">{why}<p><a href="{R}nordsee-ostsee/index.html">Nordsee und Ostsee im Vergleich</a> · <a href="{R}{SEA_INFO[other]["slug"]}/index.html">Zur {SEA_INFO[other]["name"]}</a></p></div></section>'''
        write(f'{I["slug"]}/index.html', page(f'{I["slug"]}/index.html', I["h1"], f'{I["lede"]} {len(here)} Seevögel und Strandfunde an der {I["name"]} bestimmen.', body,
              active="nordsee-ostsee", crumbs=[("Nord- & Ostsee", "nordsee-ostsee/index.html"), (I["name"], "")], seafilter=False))
    # Vergleichsseite
    R = "../"
    N, O = SEA_INFO["nord"], SEA_INFO["ost"]
    rows = [("Gezeiten", N["facts"][0][1], O["facts"][0][1]), ("Salzgehalt", N["facts"][1][1], O["facts"][1][1]), ("Küste", N["facts"][2][1], O["facts"][2][1]),
            ("Schutzgebiete", N["facts"][3][1], O["facts"][3][1]),
            ("Typische Seevögel", "Austernfischer, Säbelschnäbler, Ringelgans, Sanderling; Basstölpel und Trottellumme auf Helgoland", "Eiderenten zu Tausenden im Winter, Kormorane, Möwen und Seeschwalben"),
            ("Typische Funde", "Schwertmuscheln, Wellhornschnecken, Rochen-Eier, Herzigel", "Bernstein, Hühnergötter, Donnerkeile"),
            ("Quallen", "Kompassqualle, Feuerqualle, Blaue Nesselqualle, Lungenqualle", "vor allem Ohrenquallen, im Spätsommer Feuerquallen"),
            ("Robben", "Seehunde im Wattenmeer, Kegelrobben auf Helgoland", "selten, Kegelrobben vor allem vor Rügen")]
    trs = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in rows)
    body = f'''<section class="block page"> <div class="wrap"> <p class="kicker">{ICON["seas"]}Zwei Meere, zwei Welten</p> <h1>Nordsee und Ostsee im Vergleich</h1> <p class="intro">Beide Meere liegen nur rund 100 Kilometer auseinander und sind doch ganz verschieden: Die Nordsee hat Ebbe und Flut und viel Salz, die Ostsee kaum Gezeiten und Brackwasser. Das bestimmt, welche Vögel, Tiere und Funde du am Strand entdeckst.</p> <div class="cmp-wrap"><table class="cmp seacmp"> <thead><tr><td></td><th scope="col">Nordsee</th><th scope="col">Ostsee</th></tr></thead> <tbody>{trs}</tbody> </table></div> </div> </section>
{seapair(R)}
<section class="block"><div class="wrap prose"><h2>Warum hat die Ostsee kaum Ebbe und Flut?</h2><p>Gezeiten entstehen durch die Anziehung von Mond und Sonne. In einem großen, offenen Meer wie dem Atlantik baut sich dabei eine Flutwelle auf, die bis in die Nordsee läuft. Die Ostsee ist dafür zu klein und nur über schmale Meerengen mit der Nordsee verbunden. Ihr Wasserstand ändert sich deshalb vor allem durch Wind: Bei starkem Nordostwind kann es an der deutschen Küste zu Sturmfluten kommen.</p><h2>Was bedeutet das am Strand?</h2><p>An der Nordsee lohnt es sich, nach den Gezeiten zu planen: Bei Niedrigwasser suchen Watvögel im Watt nach Futter, bei Hochwasser sammeln sie sich an Rastplätzen. An der Ostsee kommt es eher auf den Wind an: Nach auflandigem Sturm liegt im Spülsaum am meisten, auch Bernstein.</p><h2>Am Strandkompass umschalten</h2><p>Oben auf der Startseite, in der Liste aller Funde und im Strandjahr kannst du zwischen „Beide Meere“, „Nordsee“ und „Ostsee“ wählen. Dann siehst du nur, was es an deinem Meer gibt. Die Wahl merkt sich dein Browser, bis du sie änderst.</p></div></section>'''
    write("nordsee-ostsee/index.html", page("nordsee-ostsee/index.html", "Nordsee und Ostsee im Vergleich", "Gezeiten, Salzgehalt, Küste, Seevögel und Strandfunde: Was Nordsee und Ostsee unterscheidet und was du wo findest.", body,
          active="nordsee-ostsee", crumbs=[("Nord- & Ostsee", "")], seafilter=False))

# -*- coding: utf-8 -*-
"""Kaufratgeber „Fernglas für die Küste“: Zahlen verstehen, 8x42 oder 10x42, Kaufkriterien für Wind, Gischt und Salz,
vier Modelle im Vergleich, Pflege, häufige Fragen. Technische Daten aus Herstellerangaben und Testberichten (Quellen unten),
Stand November 2026, dieselben Modelle wie im Fernglas-Ratgeber des Vogelkompass. Bei Modellwechseln hier anpassen."""
from ..core import *
from ..layout import *
from ..components import ad_link, ext_link, byline
from ..products import ADNOTE, adbanner

amazon_dp = lambda asin: f"https://www.amazon.de/dp/{asin}?tag={TAG}"
amazon_s = lambda q: "https://www.amazon.de/s?k=" + q.replace(" ", "+") + "&tag=" + TAG

MODELLE = [
    dict(id="celestron", name="Celestron Nature DX 8x42", klasse="Einstieg", gewicht="rund 650 g (gemessen)", sehfeld="129 m", nah="2,0 m", augen="17,5 mm",
         gut=["Günstiger Einstieg mit klarem, hellem Bild", "Wasserdicht, Prismen aus BaK-4-Glas"],
         achtung=["Bei trübem Licht schwächer als teurere Gläser", "Bild zum Rand hin weniger scharf"], link=amazon_dp("B00B73JONS")),
    dict(id="vortex", name="Vortex Diamondback HD 8x42", klasse="Mittelklasse", gewicht="618 g", sehfeld="131 m", nah="1,5 m", augen="17 mm",
         gut=["Leicht und handlich, gut für lange Strandwanderungen", "Unbegrenzte Garantie des Herstellers (VIP), auch bei Missgeschicken"],
         achtung=["Fokusrad anfangs sehr schwergängig"], link=amazon_dp("B07V3L3KFC")),
    dict(id="nikon", name="Nikon Monarch M7 8x42", klasse="Gehobene Mittelklasse", gewicht="670 g", sehfeld="145 m", nah="2,5 m", augen="17,1 mm",
         gut=["Sehr weites Sehfeld: fliegende Seevögel und auftauchende Schweinswale sind schnell gefunden", "ED-Glas gegen Farbsäume, wasserdicht bis 1 m"],
         achtung=["Deutlich teurer als die Einsteigergläser"], link=amazon_s("Nikon Monarch M7 8x42")),
    dict(id="zeiss", name="Zeiss Terra ED 8x42", klasse="Gehobene Mittelklasse", gewicht="725 g", sehfeld="125 m", nah="1,6 m", augen="18 mm",
         gut=["ED-Glas, robust, wasserdicht und mit Stickstoff gefüllt", "Großer Augenabstand für Brillenträger"],
         achtung=["Schwerstes Glas im Vergleich", "Sehfeld kleiner als beim Nikon"], link=amazon_s("Zeiss Terra ED 8x42")),
]

FAQ = [
    ("Welches Fernglas ist für die Küste am besten?", "Für die meisten Menschen ein wasserdichtes 8x42. Es lässt sich auch bei Wind ruhig halten, zeigt ein weites Bild und ist bei grauem Himmel hell genug. Wer vor allem weit entfernte Robbenbänke oder Seevögel auf dem Meer beobachtet, greift zum 10x42."),
    ("8x42 oder 10x42 an Nord- und Ostsee?", "8x42, wenn du Vögel im Watt, am Spülsaum und im Flug finden willst: Das Bild wackelt weniger und ist größer. 10x42, wenn du meistens weit hinausschaust, etwa auf Sandbänke oder vom Deich aufs Meer. Viele der Modelle hier gibt es in beiden Ausführungen."),
    ("Schadet Salzwasser dem Fernglas?", "Ein wasserdichtes Glas verträgt Gischt und Regen. Salz und Sand gehören aber nicht auf die Linsen: erst Sand wegblasen oder mit einem Pinsel entfernen, dann mit einem feuchten Linsentuch wischen, nie trocken reiben. Das Gehäuse kannst du mit einem feuchten Tuch abwischen."),
    ("Brauche ich ein Spektiv für Robben?", "Für den Anfang nicht. Seehunde und Kegelrobben auf entfernten Sandbänken siehst du mit einem 10x42 gut. Ein Spektiv auf einem Stativ zeigt mehr Einzelheiten, ist aber schwer. Näher kommst du bei einer Fahrt zu den Seehundbänken, ohne die Tiere zu stören."),
    ("Welches Fernglas eignet sich für Brillenträger?", "Achte auf einen Augenabstand von mindestens 15 mm und auf Augenmuscheln, die sich herunterdrehen lassen. Alle Gläser in diesem Vergleich bieten 17 mm oder mehr."),
]

SOURCES = [
    ("Vortex: Diamondback HD 8x42, technische Daten", "https://vortexoptics.com/vortex-diamondback-hd-8x42-binoculars.html"),
    ("Nikon: MONARCH M7 8x42, technische Daten", "https://imaging.nikon.com/sport-optics/lineup/binoculars/monarch/monarch_m7_x42/"),
    ("Zeiss: Terra ED 8x42, technische Daten", "https://www.zeiss.com/consumer-products/us/hunting/binoculars/terra-ed-pocket/terra-ed-8x42.html"),
    ("OutdoorGearLab: Celestron Nature DX 8x42 im Test", "https://www.outdoorgearlab.com/reviews/camping-and-hiking/binoculars/celestron-nature-dx-8x42"),
    ("Cornell Lab of Ornithology (All About Birds): Vortex Diamondback HD 8x42 im Test (Februar 2023)", "https://www.allaboutbirds.org/news/?p=55900"),
]

def build_guide():
    R = "../../"
    tips = lambda xs: '<ul class="tips">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in xs) + "</ul>"
    rows = "".join(f'<tr><th scope="row"><a href="#{m["id"]}">{esc(m["name"])}</a></th><td>{m["klasse"]}</td><td>{m["gewicht"]}</td><td>{m["sehfeld"]}</td><td>{m["nah"]}</td><td>{m["augen"]}</td></tr>' for m in MODELLE)
    models = "".join(
        f'<section class="block rtype" id="{m["id"]}" aria-labelledby="h-{m["id"]}"><div class="wrap"><h2 id="h-{m["id"]}">{esc(m["name"])}</h2><div class="rcols">'
        f'<div><h3>Spricht dafür</h3><ul class="rlist plus">{"".join(f"<li>{esc(g)}</li>" for g in m["gut"])}</ul></div>'
        f'<div><h3>Darauf achten</h3><ul class="rlist minus">{"".join(f"<li>{esc(g)}</li>" for g in m["achtung"])}</ul></div></div>'
        f'<p class="rsearch">{ad_link(m["link"], esc(m["name"]) + " bei Amazon ansehen", cls="btn ghost")}</p></div></section>'
        for m in MODELLE)
    # Häufige Fragen: am Computer offen, auf dem Handy eingeklappt (Inhalt bleibt vollständig im HTML)
    faq = '<div class="faq">' + "".join(f'<details class="fold faqitem" open data-fold><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>' for q, a in FAQ) + "</div>"
    src = '<h3 class="srchead">Quellen</h3><ul class="srclist">' + "".join(f"<li>{ext_link(esc(u), esc(t))}</li>" for t, u in SOURCES) + "</ul>"
    body = f'''<section class="block page"> <div class="wrap"> <h1>Fernglas für die Küste</h1>
<p class="intro">An der Küste ist fast alles weit weg: die Robben auf der Sandbank, die Eiderenten draußen auf dem Wasser, der Basstölpel über den Wellen. Mit einem guten Fernglas erkennst du sie trotzdem. Es muss aber Wind, Gischt und Sand aushalten.</p>
{adbanner("Ich habe die Gläser nicht selbst getestet. Die Daten stammen von den Herstellern und aus den unten genannten Testberichten, Stand November 2026.")}
<p><b>Kurz gesagt:</b> Nimm ein <b>wasserdichtes 8x42</b> mit einem Sehfeld von mindestens 120 Metern auf 1.000 Meter. Schaust du vor allem weit aufs Meer oder auf Robbenbänke, ist ein <b>10x42</b> die bessere Wahl. Für den Einstieg reicht ein günstiges Glas.</p>
<nav class="toc" aria-label="Auf dieser Seite"><a href="#zahlen">Was 8x42 bedeutet</a><a href="#kriterien">Worauf es an der Küste ankommt</a><a href="#modelle">Modelle im Vergleich</a><a href="#pflege">Pflege nach dem Strand</a><a href="#fragen">Fragen</a></nav> </div> </section>
<section class="block" id="zahlen" aria-labelledby="h-zahl"><div class="wrap"><h2 id="h-zahl">Was 8x42 bedeutet</h2>{tips([
    ("8: die Vergrößerung", "Das Tier erscheint 8-mal näher. Mehr Vergrößerung macht das Bild unruhiger, besonders bei Wind. 8-fach ist der beste Kompromiss, 10-fach lohnt sich für sehr weite Entfernungen."),
    ("42: der Objektivdurchmesser", "Die großen Linsen vorne sind 42 mm groß. Sie sammeln genug Licht für graue Tage und die Dämmerung, in der viele Seevögel ziehen."),
    ("Austrittspupille: 42 geteilt durch 8", "Ergibt rund 5 mm. Ab etwa 5 mm bleibt das Bild auch bei bedecktem Himmel hell. Beim 10x42 sind es gut 4 mm, das reicht am hellen Strand meist auch."),
    ("Sehfeld in Metern auf 1.000 Meter", "Wie breit der sichtbare Ausschnitt in einem Kilometer Entfernung ist. Je größer, desto schneller findest du einen fliegenden Vogel oder einen kurz auftauchenden Schweinswal.")])}</div></section>
<section class="block" id="kriterien" aria-labelledby="h-krit"><div class="wrap"><h2 id="h-krit">Worauf es an der Küste ankommt</h2>{tips([
    ("Wasserdicht und gasgefüllt", "Gischt, Regen und feuchte Luft sind an der Küste normal. Stickstoff oder Argon im Inneren verhindern, dass das Glas von innen beschlägt."),
    ("8x42 oder 10x42", "8x42 für Watt, Spülsaum und Vögel im Flug. 10x42 für Robbenbänke, Seevögel weit draußen und den Blick vom Deich aufs Meer."),
    ("Weites Sehfeld", "Seevögel fliegen schnell, Schweinswale zeigen sich nur kurz. Mit einem weiten Sehfeld findest du sie rechtzeitig."),
    ("Gewicht um 600 bis 700 g", "Bei langen Wanderungen am Strand zählt jedes Gramm. Ein Glas, das zu schwer ist, bleibt im Ferienhaus."),
    ("Gummiarmierung und Schutzkappen", "Eine griffige Gummihülle schützt vor Stößen, Kappen auf den Linsen vor Sand und Salz. Ein breiter Trageriemen hält das Glas bei Wind sicher."),
    ("Brillenträger", "Mindestens 15 mm Augenabstand und Augenmuscheln zum Herunterdrehen, damit du mit Brille das ganze Bild siehst.")])}</div></section>
<section class="block" id="modelle" aria-labelledby="h-mod"><div class="wrap"><h2 id="h-mod">Vier 8x42-Ferngläser im Vergleich</h2>
<p class="intro">Vier bewährte Gläser vom Einstieg bis zur gehobenen Mittelklasse. Die Preise schwanken stark, deshalb nenne ich Preisklassen und verlinke auf die aktuellen Angebote.</p>
<div class="cmp-wrap" tabindex="0" role="region" aria-label="Vergleichstabelle, seitlich scrollbar"><table class="cmp"><thead><tr><td>Modell</td><th scope="col">Preisklasse</th><th scope="col">Gewicht</th><th scope="col">Sehfeld auf 1.000 m</th><th scope="col">Naheinstellung</th><th scope="col">Augenabstand</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="thumbnote">Angaben laut Hersteller, beim Celestron Gewicht laut Testmessung von OutdoorGearLab. Stand November 2026.</p></div></section>
{models}
<section class="block" id="pflege" aria-labelledby="h-pfl"><div class="wrap"><h2 id="h-pfl">Pflege nach dem Strand</h2><ol class="tiplist">
<li><b>Sand zuerst:</b> Puste Sandkörner von den Linsen oder nimm einen weichen Pinsel. Wer gleich wischt, zerkratzt die Vergütung.</li>
<li><b>Salz lösen:</b> Wische die Linsen mit einem leicht angefeuchteten Linsentuch ab, das Gehäuse mit einem feuchten Tuch.</li>
<li><b>Trocknen lassen:</b> Lass das Glas ohne Kappen bei Zimmertemperatur trocknen, bevor du es wegpackst.</li>
<li><b>Abstand halten:</b> Mit dem Fernglas musst du nicht nah heran. Halte Abstand zu Robben und rastenden Vögeln, besonders zur Brutzeit und bei Heulern.</li>
</ol></div></section>
<section class="block" id="fragen" aria-labelledby="h-faq"><div class="wrap"><h2 id="h-faq">Häufige Fragen</h2>{faq}
<p class="intro">Was du sonst an die Küste mitnimmst, zeigt die Seite <a href="{R}ausruestung/index.html">Ausrüstung</a>. Welche Tiere gerade zu sehen sind, steht im <a href="{R}strandjahr/index.html" data-now-link>Küstenjahr</a>.</p>
{src}{ADNOTE}{byline(R, "Fernglas für die Küste")}</div></section>'''
    ld_all = ld({"@context": "https://schema.org", "@type": "Article", "headline": "Fernglas für die Küste: 8x42 oder 10x42 und vier Modelle im Vergleich", "inLanguage": "de-DE",
                 "author": AUTHOR, "publisher": {"@id": ORG_ID}, "datePublished": "2026-11-09", "dateModified": "2026-11-09", "mainEntityOfPage": f"{DOMAIN}/ratgeber/fernglas/"}) + \
             ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    write("ratgeber/fernglas/index.html", page("ratgeber/fernglas/index.html", "Fernglas für die Küste: 8x42 oder 10x42?",
          "Welches Fernglas für Nord- und Ostsee? Was 8x42 bedeutet, wann 10x42 besser ist, worauf du bei Gischt und Sand achtest und vier bewährte Ferngläser im Vergleich.",
          body, active="ausruestung", crumbs=[("Ausrüstung", "ausruestung/index.html"), ("Fernglas für die Küste", "")], seafilter=False, extra_ld=ld_all))

# -*- coding: utf-8 -*-
"""Produktempfehlungen als Text mit Amazon-Werbelinks (ohne Produktbilder)."""
from .core import *
from .components import *

PRODUCTS = {
 "uvlampe": dict(name="UV-Taschenlampe 365 nm",
   why="Bernstein leuchtet unter UV-Licht bläulich bis gelb und fällt so im Tangsaum sofort auf. Nicht in die Augen leuchten.",
   url="https://www.amazon.de/s?k=uv+taschenlampe+365nm&tag=" + TAG),
 "buch": dict(name="Bestimmungsbuch Strand und Küste",
   why="Ein handliches Bestimmungsbuch für Muscheln, Schnecken, Quallen und Strandfunde an Nord- und Ostsee passt in jede Strandtasche.",
   url="https://www.amazon.de/s?k=bestimmungsbuch+strand+k%C3%BCste+nordsee+ostsee&tag=" + TAG),
 "becherlupe": dict(name="Becherlupe",
   why="Krabbe, Garnele oder Seestachelbeere kurz in Meerwasser setzen und von allen Seiten vergrößert anschauen. Danach zurück ins Wasser.",
   url="https://www.amazon.de/s?k=becherlupe+kinder&tag=" + TAG),
 "kescher": dict(name="Kescher mit Teleskopstiel",
   why="Für Garnelen und kleine Krebse im Priel. Ein feines Netz schont die Tiere.",
   url="https://www.amazon.de/s?k=kescher+teleskop+kinder&tag=" + TAG),
 "forscherset": dict(name="Eimer-Set für Strandforscher",
   why="Eimer, Schaufel und Sieb für Sandburgen und zum kurzen Anschauen von Strandfunden.",
   url="https://www.amazon.de/s?k=strandspielzeug+set+eimer+sieb&tag=" + TAG),
 "wattschuhe": dict(name="Wattschuhe",
   why="Schützen im Watt vor scharfen Austern, Seepocken und Muschelschalen und sitzen auch im Schlick fest am Fuß.",
   url="https://www.amazon.de/s?k=wattschuhe&tag=" + TAG),
 "fernglas": dict(name="Celestron Nature DX 8x42",
   why="Für Seevögel im Watt und Robben auf der Sandbank, aus sicherem Abstand. 8-fache Vergrößerung, wasserdicht und leicht.",
   url="https://www.amazon.de/dp/B00B73JONS?tag=" + TAG),
 "vogelbuch": dict(name="Vogelführer für Küste und Meer",
   why="Möwen, Watvögel und Seeschwalben ähneln sich oft. Ein Vogelführer mit Bildern der Jugend- und Winterkleider hilft beim Bestimmen.",
   url="https://www.amazon.de/s?k=vogelf%C3%BChrer+k%C3%BCste+seev%C3%B6gel&tag=" + TAG),
 "sammelbox": dict(name="Sortierbox für Muscheln und Steine",
   why="Mit vielen kleinen Fächern, damit zerbrechliche Funde wie Herzigel und Plattmuscheln heil nach Hause kommen.",
   url="https://www.amazon.de/s?k=sortierbox+f%C3%A4cher+klein&tag=" + TAG),
 "strandmuschel": dict(name="Strandmuschel mit UV-Schutz",
   why="Schützt an windigen Tagen vor Sonne und Sand. Achte auf einfachen Aufbau und ein kleines Packmaß.",
   url="https://www.amazon.de/s?k=strandmuschel+uv+schutz&tag=" + TAG),
}

# Je Artseite ein dezenter Text-Werbelink unter „Mehr erfahren“, passend zur Gruppe
SPECIES_PICK = {"Seevögel": "vogelbuch", "Robben": "fernglas", "Wale & Delfine": "fernglas"}
SPECIES_PICK_FOR = {"bernstein": "uvlampe"}

def species_pick(s):
    return SPECIES_PICK_FOR.get(s["k"]) or SPECIES_PICK.get(s["grp"], "buch")

def gear_inline(key):
    """Ein einzelner Werbelink als Pille, mit Sternchen; Hinweis darunter."""
    p = PRODUCTS[key]
    return (f'<li><a href="{p["url"]}" target="_blank" rel="sponsored nofollow noopener">{esc(p["name"])}<span aria-hidden="true">*</span>'
            f'<span class="sr-only"> (Werbelink, öffnet in neuem Fenster)</span></a></li>')

AD_SHORT = '<p class="adshort"><span aria-hidden="true">*</span> Werbelink zu Amazon: Kaufst du darüber, erhält der Meereskompass eine kleine Provision. Für dich ändert sich am Preis nichts.</p>'

def gear_list(keys):
    """Empfehlungen als schlichte Textliste: Name als Werbelink, darunter kurz, wofür."""
    li = "".join(f'<li><a href="{PRODUCTS[k]["url"]}" target="_blank" rel="sponsored nofollow noopener">{esc(PRODUCTS[k]["name"])}<span aria-hidden="true">*</span>'
                 f'<span class="sr-only"> (Werbelink, öffnet in neuem Fenster)</span></a><span>{esc(PRODUCTS[k]["why"])}</span></li>' for k in keys)
    return f'<ul class="gearlist">{li}</ul>'

ADNOTE = '<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Wenn du über diesen Link etwas kaufst, erhält der Meereskompass eine kleine Provision von Amazon. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>'

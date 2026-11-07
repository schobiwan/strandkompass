# -*- coding: utf-8 -*-
"""Produktempfehlungen mit Amazon-Werbelinks."""
from .core import *
from .icons import *
from .components import *

PRODUCTS = {
 "uvlampe": dict(cat="Bernsteinsuche", name="UV-Taschenlampe 365 nm", by="Auswahl bei Amazon", tip=True, icon="lamp",
   why="Bernstein leuchtet unter UV-Licht bläulich bis gelb und fällt so im Tangsaum sofort auf. Nicht in die Augen leuchten.",
   url="https://www.amazon.de/s?k=uv+taschenlampe+365nm&tag=" + TAG),
 "buch": dict(cat="Buch", name="Bestimmungsbuch Strand und Küste", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Ein handliches Bestimmungsbuch für Muscheln, Schnecken, Quallen und Strandfunde an Nord- und Ostsee passt in jede Strandtasche.",
   url="https://www.amazon.de/s?k=bestimmungsbuch+strand+k%C3%BCste+nordsee+ostsee&tag=" + TAG),
 "becherlupe": dict(cat="Für Kinder", name="Becherlupe", by="Auswahl bei Amazon", tip=False, icon="lens",
   why="Krabbe, Garnele oder Seestachelbeere kurz in Meerwasser setzen und von allen Seiten vergrößert anschauen. Danach zurück ins Wasser.",
   url="https://www.amazon.de/s?k=becherlupe+kinder&tag=" + TAG),
 "kescher": dict(cat="Für Kinder", name="Kescher mit Teleskopstiel", by="Auswahl bei Amazon", tip=False, icon="net",
   why="Für Garnelen und kleine Krebse im Priel. Ein feines Netz schont die Tiere.",
   url="https://www.amazon.de/s?k=kescher+teleskop+kinder&tag=" + TAG),
 "forscherset": dict(cat="Für Kinder", name="Eimer-Set für Strandforscher", by="Auswahl bei Amazon", tip=False, icon="bucket",
   why="Eimer, Schaufel und Sieb für Sandburgen und zum kurzen Anschauen von Strandfunden.",
   url="https://www.amazon.de/s?k=strandspielzeug+set+eimer+sieb&tag=" + TAG),
 "wattschuhe": dict(cat="Watt", name="Wattschuhe", by="Auswahl bei Amazon", tip=False, icon="shoe",
   why="Schützen im Watt vor scharfen Austern, Seepocken und Muschelschalen und sitzen auch im Schlick fest am Fuß.",
   url="https://www.amazon.de/s?k=wattschuhe&tag=" + TAG),
 "fernglas": dict(cat="Fernglas", name="Celestron Nature DX 8x42", by="Celestron", tip=False, icon="binoc",
   why="Für Seevögel im Watt und Robben auf der Sandbank, aus sicherem Abstand. 8-fache Vergrößerung, wasserdicht und leicht.",
   url="https://www.amazon.de/dp/B00B73JONS?tag=" + TAG),
 "vogelbuch": dict(cat="Buch", name="Vogelführer für Küste und Meer", by="Auswahl bei Amazon", tip=True, icon="book",
   why="Möwen, Watvögel und Seeschwalben ähneln sich oft. Ein Vogelführer mit Bildern der Jugend- und Winterkleider hilft beim Bestimmen.",
   url="https://www.amazon.de/s?k=vogelf%C3%BChrer+k%C3%BCste+seev%C3%B6gel&tag=" + TAG),
 "sammelbox": dict(cat="Sammeln", name="Sortierbox für Muscheln und Steine", by="Auswahl bei Amazon", tip=False, icon="box",
   why="Mit vielen kleinen Fächern, damit zerbrechliche Funde wie Herzigel und Plattmuscheln heil nach Hause kommen.",
   url="https://www.amazon.de/s?k=sortierbox+f%C3%A4cher+klein&tag=" + TAG),
 "strandmuschel": dict(cat="Strandtag", name="Strandmuschel mit UV-Schutz", by="Auswahl bei Amazon", tip=False, icon="tent",
   why="Schützt an windigen Tagen vor Sonne und Sand. Achte auf einfachen Aufbau und ein kleines Packmaß.",
   url="https://www.amazon.de/s?k=strandmuschel+uv+schutz&tag=" + TAG),
}

PHOTO = {
 "uvlampe": ("Amber Bugs", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Dominican_Amber_Fossilized_Wasp_Enhydro_02.png"),
 "forscherset": ("David", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Sand_bucket.jpg"),
 "fernglas": ("Jacek Halicki", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:2020_Lornetka_Baigish_8x30.jpg"),
 "wattschuhe": ("Mattes", "CC BY 2.0 de", "https://commons.wikimedia.org/wiki/File:Badeschuhe.JPG"),
 "strandmuschel": ("Camper2", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Strandmuschel.jpg"),
 "kescher": ("Huangdan2060", "CC BY 3.0", "https://commons.wikimedia.org/wiki/File:Landing_net_2.jpg"),
 "vogelbuch": ("USFWS Mountain-Prairie", "gemeinfrei", "https://commons.wikimedia.org/wiki/File:U_of_M_Ornithology_Class_4-12-14_(13799829933).jpg"),
 "buch": ("R. Tucker Abbott, American Seashells (1954)", "gemeinfrei", "https://commons.wikimedia.org/wiki/File:American_seashells_(1954)_(17540656063).jpg"),
 "sammelbox": ("Andrea Michelbach", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Shells_%26_book.jpg"),
}

GEAR_GRP = {
 "Seevögel": ["fernglas", "vogelbuch", "strandmuschel"],
 "Muscheln": ["buch", "sammelbox", "wattschuhe"],
 "Schnecken": ["buch", "becherlupe", "sammelbox"],
 "Quallen": ["buch", "becherlupe", "strandmuschel"],
 "Krebse & Würmer": ["kescher", "becherlupe", "wattschuhe"],
 "Seesterne & Seeigel": ["sammelbox", "buch", "becherlupe"],
 "Tang & Seegras": ["buch", "becherlupe", "wattschuhe"],
 "Strandfunde": ["uvlampe", "sammelbox", "buch"],
 "Meeressäuger": ["fernglas", "buch", "strandmuschel"],
}

GEAR_FOR = {
 "bernstein": ["uvlampe", "sammelbox", "buch"],
 "nordseegarnele": ["kescher", "becherlupe", "forscherset"],
 "strandkrabbe": ["kescher", "becherlupe", "forscherset"],
 "auster": ["wattschuhe", "buch", "sammelbox"],
}

PICON = {
 "binoc": '<circle cx="8" cy="15" r="4.5"/><circle cx="16" cy="15" r="4.5"/><path d="M8 10.5V6h3v6M16 10.5V6h-3v6"/>',
 "lamp": '<path d="M9 3h6v5l-1 2v10h-4V10L9 8z"/><path d="M12 13v3"/>',
 "book": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
 "lens": '<circle cx="10" cy="10" r="5.5"/><path d="m14 14 6 6"/>',
 "net": '<path d="M4 20 11 13"/><ellipse cx="15" cy="9" rx="5.5" ry="4.5" transform="rotate(-45 15 9)"/><path d="M12 6l6 6M14 4.5l5.5 5.5"/>',
 "bucket": '<path d="M5 8h14l-1.5 12h-11z"/><path d="M5 8c0-4 14-4 14 0"/>',
 "shoe": '<path d="M3 15c0-3 1-7 3-7 1 0 2 2 4 3s7 1 9 3 2 3 2 3H3z"/><path d="M3 18h18"/>',
 "box": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M9 6v12M15 6v12M3 12h18"/>',
 "tent": '<path d="M3 19C3 10 8 5 14 5s7 6 7 14z"/><path d="M14 5c-3 3-4 8-4 14"/>',
}

def product(R, key, compact=False):
    p = PRODUCTS[key]
    tip = '<span class="ptip">Unser Tipp</span>' if p["tip"] and not compact else ""
    why = f'<p class="pwhy">{esc(p["why"])}</p>' if not compact else ""
    meta = f'<span>{p["cat"]}{" · Unser Tipp" if (p["tip"] and compact) else ""}</span>'
    pic = (f'<img src="{R}photos/p-{key}-400.webp" srcset="{R}photos/p-{key}-400.webp 400w, {R}photos/p-{key}.webp 720w" '
           f'sizes="{"88px" if compact else "(max-width: 600px) 92vw, 360px"}" alt="" width="400" height="300" loading="lazy" decoding="async">'
) if key in PHOTO else f'<span class="picon"><svg viewBox="0 0 24 24" aria-hidden="true">{PICON[p["icon"]]}</svg></span>'
    under = f'<small class="pcred">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (key in PHOTO and not compact) else ""
    return (f'<li class="product{" pick" if p["tip"] else ""}{"" if key in PHOTO else " nopic"}"> <div class="pimg">{pic}{tip}</div>{under} '
            f'<div class="pbody"> <p class="pmeta">{meta}<span class="pad">Anzeige</span></p> <h3 class="pname">{esc(p["name"])}</h3> <p class="pby">{esc(p["by"])}</p> {why} {f'<small class="pcred2">Beispielfoto · {credit_parts(*PHOTO[key])}</small>' if (compact and key in PHOTO) else ""} '
            f'<a class="plink" href="{p["url"]}" target="_blank" rel="sponsored nofollow noopener"><span>Bei Amazon ansehen<span aria-hidden="true">*</span></span>{ICON["arrow"]}'
            f'<span class="sr-only"> {esc(p["name"])} (Werbelink, öffnet in neuem Fenster)</span></a> </div> </li>')

ADNOTE = '<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Wenn du über diesen Link etwas kaufst, erhält der Strandkompass eine kleine Provision von Amazon. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>'

def month_gear(R, m):
    picks = ("uvlampe", "sammelbox", "fernglas", "buch") if m in (10, 11, 12, 1, 2, 3) else ("becherlupe", "kescher", "wattschuhe", "strandmuschel")
    return (f'<section class="gearband" aria-labelledby="h-gear"><div class="wrap"><div class="head-row"><h2 id="h-gear">Passend zum {MONTHS[m-1]}</h2><a class="gearmore" href="{R}ausruestung/index.html">Alle Empfehlungen ansehen</a></div>'
            f'<ul class="products">{"".join(product(R, g) for g in picks)}</ul>{ADNOTE}</div></section>')

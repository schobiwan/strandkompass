# -*- coding: utf-8 -*-
"""Reise-Werbelinks als Text: Touren über GetYourGuide, Ferienwohnungen über Holidu (Awin).
Alles bleibt leer, solange TRIPS_ON falsch ist (keine Partner-IDs eingetragen)."""
from urllib.parse import quote
from .core import *
from .components import *

def gyg(q):
    return f"https://www.getyourguide.de/s/?q={quote(q)}&partner_id={GYG_PARTNER or 'PARTNER-ID'}"

def holidu(region):
    dest = f"https://www.holidu.de/s/{quote(region)}"
    return f"https://www.awin1.com/cread.php?awinmid={AWIN_HOLIDU or 'PROGRAMM-ID'}&awinaffid={AWIN_AFF or 'PUBLISHER-ID'}&ued={quote(dest, safe='')}"

TOURS = {
 "seehundbank": dict(name="Fahrt zu den Seehundbänken", url=gyg("Seehundbank"),
   why="Mit dem Schiff zu den Sandbänken im Wattenmeer, auf denen Seehunde und oft auch Kegelrobben ruhen. Die Schiffe halten Abstand, ein Fernglas lohnt sich."),
 "helgoland": dict(name="Tagesausflug nach Helgoland", url=gyg("Helgoland"),
   why="Von April bis Juli brüten am Lummenfelsen Basstölpel und Trottellummen, auf der Düne liegen Kegelrobben. Im Winter kommen dort die Robbenjungen zur Welt."),
 "watt": dict(name="Wattwanderung mit Führung", url=gyg("Wattwanderung"),
   why="Wattführerinnen und Wattführer kennen Priele und Gezeiten und zeigen, was im Schlick lebt, vom Wattwurm bis zur Strandkrabbe."),
 "ostsee": dict(name="Schiffsausflug an der Ostseeküste", url=gyg("Rügen Bootstour"),
   why="Zu den Kreidefelsen von Rügen oder entlang der Bodden. Mit Glück zeigen sich Schweinswale, im Winter rasten Eiderenten auf dem Wasser."),
}
STAYS = {
 "nord": dict(name="Ferienwohnungen an der Nordsee", url=holidu("Nordsee"),
   why="Für ein paar Tage am Wattenmeer: Wer nah am Deich wohnt, kann bei jedem Niedrigwasser hinaus."),
 "ost": dict(name="Ferienwohnungen an der Ostsee", url=holidu("Ostsee"),
   why="Für Bernsteinsuche nach dem Sturm und Wintervögel an der Küste."),
}
# Artseite → passende Tour
SPECIES_TOUR = {"seehund": "seehundbank", "kegelrobbe": "helgoland", "basstoelpel": "helgoland", "trottellumme": "helgoland",
                "wattwurm": "watt", "schweinswal": "ostsee"}
SEA_TRIPS = {"nord": ("seehundbank", "helgoland", "watt"), "ost": ("ostsee",)}

def trip_ad(url, text):
    return ext_link(url, text, rel="sponsored nofollow noopener", mark="*")

def species_tour(s):
    """Pille für „Mehr erfahren“, oder leer."""
    t = SPECIES_TOUR.get(s["k"]) if TRIPS_ON else None
    return trip_ad(TOURS[t]["url"], esc(TOURS[t]["name"])) if t else ""

def trip_list(items):
    li = "".join(f'<li>{trip_ad(x["url"], esc(x["name"]))}<span>{esc(x["why"])}</span></li>' for x in items)
    return f'<ul class="gearlist">{li}</ul>'

TRIP_NOTE = ('<p class="adnote"><span aria-hidden="true">*</span> Werbelink: Buchst du über einen dieser Links eine Tour bei GetYourGuide '
             'oder eine Unterkunft bei Holidu, erhält der Meereskompass eine kleine Provision. Für dich ändert sich am Preis nichts.</p>')

def sea_trips(k, name):
    """Abschnitt „Hinfahren und erleben“ für die Nordsee- bzw. Ostsee-Seite, oder leer."""
    if not TRIPS_ON:
        return ""
    items = [TOURS[t] for t in SEA_TRIPS[k]] + [STAYS[k]]
    return (f'<section class="block" aria-labelledby="h-trips"><div class="wrap"><h2 id="h-trips">Hinfahren und erleben</h2>'
            f'<p class="intro">Touren und Unterkünfte, mit denen du die Tiere an der {name} selbst sehen kannst.</p>{trip_list(items)}{TRIP_NOTE}</div></section>')

def watt_tour():
    return " " + trip_ad(TOURS["watt"]["url"], "Wattwanderung mit Führung buchen") if TRIPS_ON else ""

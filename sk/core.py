# -*- coding: utf-8 -*-
"""Grundlagen: Pfade, Konstanten, Daten-Nachschlagen und kleine Helfer."""
import os, json, html, re
from data import SPECIES, PAIRS, EXT, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS, SEA_NOTE, SEA_INFO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDITS = json.load(open(os.path.join(ROOT, "credits.json"), encoding="utf-8"))
# Tonaufnahmen: key -> [Urheber, Lizenz, Quelle, Sekunden]
AUDIO = json.load(open(os.path.join(ROOT, "audio.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "audio.json")) else {}
SITE = "Meereskompass"
DOMAIN = "https://meereskompass.de"
OUT = os.path.join(ROOT, "dist")
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MSHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
BY = {s["k"]: s for s in SPECIES}
# Doppelgänger in der Reihenfolge der Gruppen: Vögel, Robben, Wale, dann die übrigen Funde
PAIRS.sort(key=lambda p: GROUPS.index(BY[p["a"]]["grp"]) if p["a"] in BY else len(GROUPS))
PAIRBY = {p["k"]: p for p in PAIRS}
TAG = "schobiwan-21"
# Reise-Partnerprogramme: IDs eintragen, sobald die Anmeldung bestätigt ist. Solange sie leer sind,
# erscheinen keine Reiselinks auf der Seite. Mit SK_TRIPS=1 baut man eine Vorschau mit Platzhaltern.
GYG_PARTNER = ""            # GetYourGuide Partner-ID (partner.getyourguide.com)
AWIN_AFF = ""               # deine Awin-Publisher-ID
AWIN_HOLIDU = ""            # Awin-Programm-ID von Holidu bzw. „Ferienwohnungen DE“
TRIPS_ON = bool(GYG_PARTNER or os.environ.get("SK_TRIPS") == "1")


def gslug(g):
    """Anker einer Gruppe: „Wale & Delfine“ → wale-delfine, „Seevögel“ → seevoegel."""
    import re as _re
    t = g.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return _re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def skey(x):
    """Sortierschlüssel nach Duden: Umlaute wie Grundbuchstaben (Säbelschnäbler vor Sturmmöwe)."""
    n = x["n"] if isinstance(x, dict) else x
    return n.lower().replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss")

def esc(s):
    """HTML-sicher ausgeben (auch für Attribute)."""
    return html.escape(str(s), quote=True)

_IDX = re.compile(r'((?:href|action)=")((?:\.\./)*(?:[^"#?:]*/)?)index\.html')

def pretty(html):
    """Saubere URLs: Verweise auf …/index.html zeigen auf das Verzeichnis (…/), die Startseite auf ./"""
    return _IDX.sub(lambda m: m.group(1) + (m.group(2) or "./"), html)

def write(path, content):
    if path.endswith(".html"):
        content = pretty(content)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def photo_key(key):
    """Fotoname: Funde unter ihrem Schlüssel, Doppelgänger ohne eigene Seite mit Vorsilbe x-."""
    return key if key in BY else "x-" + key

def name_of(key):
    return BY[key]["n"] if key in BY else EXT[key]["n"]

def lat_of(key):
    return BY[key]["lat"] if key in BY else EXT[key]["lat"]

MOBILE = ("Seevögel", "Robben", "Wale & Delfine")

# Stand der Steckbriefe, Vergleiche und Merkmal-Seiten: bei inhaltlichen Änderungen anheben (Sitemap lastmod, strukturierte Daten, sichtbarer Stand)
CONTENT_PUBLISHED = "2026-11-03"
CONTENT_UPDATED = "2026-11-09"
STAND = "November 2026"

def mit_artikel(key, case="nom"):
    """Name mit bestimmtem Artikel, Adjektiv schwach gebeugt: der Große Tümmler, den Großen Tümmler, der Blauen Nesselqualle."""
    n, g = re.sub(r"\s*\(.*?\)", "", name_of(key)), (BY[key]["g"] if key in BY else EXT[key]["g"])  # ohne Klammerzusatz
    art = {"nom": {"m": "der", "f": "die", "n": "das"}, "acc": {"m": "den", "f": "die", "n": "das"}, "dat": {"m": "dem", "f": "der", "n": "dem"}}[case][g]
    w = n.split(" ")
    if len(w) > 1 and w[1][:1].isupper() and w[0].endswith(("er", "es", "e")):
        stem = w[0][:-2] if w[0].endswith(("er", "es")) else w[0][:-1]
        weak_e = case == "nom" or (case == "acc" and g != "m")
        w[0] = stem + ("e" if weak_e else "en")
    return f"{art} {' '.join(w)}"

def mlist(ms):
    ms = list(ms)
    if len(ms) == 12:
        return "ganzjährig"
    names = [MONTHS[m - 1] for m in ms]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " und " + names[-1]

def mrange(ms):
    ms = sorted(ms)
    if len(ms) == 12:
        return "ganzjährig"
    return f"{MONTHS[ms[0]-1]} bis {MONTHS[ms[-1]-1]}"


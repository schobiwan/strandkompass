# -*- coding: utf-8 -*-
"""Grundlagen: Pfade, Konstanten, Daten-Nachschlagen und kleine Helfer."""
import os, json, html
from data import SPECIES, PAIRS, EXT, GROUPS, HABS, ACTS, SIZES, MONTH_EVENTS, SEA_NOTE, SEA_INFO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDITS = json.load(open(os.path.join(ROOT, "credits.json"), encoding="utf-8"))
# Tonaufnahmen: key -> [Urheber, Lizenz, Quelle, Sekunden]
AUDIO = json.load(open(os.path.join(ROOT, "audio.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "audio.json")) else {}
SITE = "Strandkompass"
DOMAIN = "https://strandkompass.de"
OUT = os.path.join(ROOT, "dist")
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MSHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MSLUG = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
BY = {s["k"]: s for s in SPECIES}
PAIRBY = {p["k"]: p for p in PAIRS}
TAG = "schobiwan-21"


def skey(x):
    """Sortierschlüssel nach Duden: Umlaute wie Grundbuchstaben (Säbelschnäbler vor Sturmmöwe)."""
    n = x["n"] if isinstance(x, dict) else x
    return n.lower().replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss")

def esc(s):
    """HTML-sicher ausgeben (auch für Attribute)."""
    return html.escape(str(s), quote=True)

def write(path, content):
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

def ein(g, case="nom"):
    if case == "dat":
        return "der" if g == "f" else "dem"
    return "eine" if g == "f" else "ein"

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


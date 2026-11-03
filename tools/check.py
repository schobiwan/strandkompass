# -*- coding: utf-8 -*-
"""Prüft die gebaute Seite in dist/ und die Inhalte in data.py.

Aufruf: python3 tools/check.py   (nach python3 build.py)

- interne Links, Bilder und srcset-Angaben zeigen auf vorhandene Dateien
- jeder Fund und jeder Doppelgänger hat Foto und Bildnachweis
- jeder Doppelgänger-Verweis in data.py gibt es auch als Vergleich
- jeder Monat hat Ereignisse für Nordsee und Ostsee
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from data import SPECIES, EXT, PAIRS, MONTH_EVENTS  # noqa: E402

DIST = os.path.join(ROOT, "dist")
problems = []

# Links und Bilder
for d, _, files in os.walk(DIST):
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(d, f)
        page = open(path, encoding="utf-8").read()
        refs = re.findall(r'(?:href|src)="([^"#]+)', page)
        for srcset in re.findall(r'srcset="([^"]+)"', page):
            refs += [part.strip().split(" ")[0] for part in srcset.split(",")]
        for ref in refs:
            if ref.startswith(("http:", "https:", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, ref))):
                problems.append(f"Kaputter Verweis in {os.path.relpath(path, DIST)}: {ref}")

# Fotos und Bildnachweise
credits = json.load(open(os.path.join(ROOT, "credits.json"), encoding="utf-8"))
keys = [s["k"] for s in SPECIES] + ["x-" + k for k in EXT]
for k in keys:
    if k not in credits:
        problems.append(f"Bildnachweis fehlt: {k}")
    for name in (f"{k}.webp", f"{k}-400.webp"):
        if not os.path.exists(os.path.join(ROOT, "photos", name)):
            problems.append(f"Foto fehlt: photos/{name}")

# Vogelrufe: jeder Seevogel hat Beschreibung und Aufnahme
audio_path = os.path.join(ROOT, "audio.json")
audio = json.load(open(audio_path, encoding="utf-8")) if os.path.exists(audio_path) else {}
for s in SPECIES:
    if s["grp"] != "Seevögel":
        continue
    if not s.get("call"):
        problems.append(f"Rufbeschreibung fehlt: {s['k']}")
    if s["k"] not in audio:
        problems.append(f"Tonaufnahme fehlt: {s['k']}")
for k in audio:
    if not os.path.exists(os.path.join(ROOT, "audio", f"{k}.mp3")):
        problems.append(f"Tondatei fehlt: audio/{k}.mp3")

# Doppelgänger
pair_keys = {p["k"] for p in PAIRS}
for s in SPECIES:
    if s["alike"] and s["alike"] not in pair_keys:
        problems.append(f"{s['k']}: Doppelgänger {s['alike']} gibt es nicht")

# Ereignisse je Meer
for m, events in MONTH_EVENTS.items():
    seas = {sea for sea, _ in events}
    for sea in ("nord", "ost"):
        if sea not in seas and "beide" not in seas:
            problems.append(f"Monat {m}: kein Ereignis für {sea}")

if problems:
    print("\n".join(problems))
    sys.exit(f"{len(problems)} Probleme gefunden")
print(f"Alles in Ordnung: {len(SPECIES)} Funde, {len(PAIRS)} Doppelgänger, {sum(1 for _ in os.walk(DIST))} Ordner geprüft")

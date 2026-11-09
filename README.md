# Meereskompass

Statische Website zum Bestimmen von Seevögeln, Robben und Walen an Nord- und Ostsee,
dazu Quallen, Muscheln und Strandfunde. Schwesterseite von Vogelkompass und Waldtierkompass.

Domain: meereskompass.de (frühere Arbeitsnamen: Strandkompass, Küstenkompass; das Repository heißt weiter `strandkompass`).
Reihenfolge der Gruppen überall: Seevögel, Robben, Wale & Delfine, danach die übrigen Funde.

## Bauen

```
npm ci                  # einmalig: esbuild, lightningcss, purgecss
python3 build.py        # erzeugt die fertige Seite in dist/
python3 tools/check.py  # prüft Links, Fotos, Bildnachweise und Daten
```

`dist/` wird mit ins Repository eingecheckt. statichost.eu veröffentlicht den Ordner direkt (siehe `statichost.yml`).

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `data.py` | Alle Inhalte: Funde, Doppelgänger, Strandjahr, Nordsee/Ostsee |
| `data_aussehen.py` | Seiten „Nach Aussehen“ (Merkmal → passende Arten) |
| `credits.json` | Bildnachweise (Urheber, Lizenz, Quelle) je Foto |
| `photos/` | Fotos als WebP, 720 × 576 und 400 × 320 |
| `sk/core.py` | Pfade, Konstanten, Stand der Inhalte, Helfer (Sortierung, Artikel) |
| `sk/icons.py` | Symbole, Logo, Tonne, Rippelmarken |
| `sk/layout.py` | Seitengerüst, Navigation, Fuß, Meer-Umschalter |
| `sk/components.py` | Bausteine: Fotos, Bildangaben, Fundkarten, „Kurz gesagt“, externe und Werbelinks |
| `sk/products.py` | Empfehlungen als Text-Werbelinks (Amazon), ohne Produktbilder |
| `sk/pages/` | Die Seiten: Start, Arten, Doppelgänger, Nach Aussehen, Küstenjahr, Meere, Fernglas-Ratgeber, Info, Über, 404 |
| `sk/assets.py` | Schriften, Fotos und Icons kopieren, CSS/JS bündeln, Sitemap, llms.txt, _headers |
| `src/css/` | `base.css` (Grundgerüst), `extra.css` (Meereskompass) |
| `src/js/` | `app.js` (jede Seite, mit Menü, Schnellsuche, Tönen), `home.js` (Startseite), `search.js` (Suche) |
| `icons/` | Favicon und App-Icons (aus `favicon.svg` gerendert) |
| `tools/` | Prüfskript, Foto- und Ton-Werkzeuge |

## Neue Fotos

Die Fotos kommen von Wikimedia Commons. Ein GitHub-Workflow lädt sie:

1. Arten in `tools/photo_list.json` eintragen (Wikipedia-Artikel oder `File:Name.jpg`).
2. Workflow „Fotos laden“ unter *Actions* starten. Das Ergebnis landet im Zweig `fotos-eingang`.
3. Fotos zuschneiden, nach `photos/` legen und Urheber, Lizenz und Quelle in `credits.json` eintragen.

# Meereskompass – Arbeitsregeln für Claude

Website meereskompass.de (statisch, Python-Generator `build.py` + Paket `sk/`, Repository heißt weiter `strandkompass`). Betreiber: Nico Schober. Antworten auf Deutsch, Anrede „Nico“. Schwesterseite von vogelkompass.de; Neuerungen dort werden auf Wunsch übernommen, wenn sie hier sinnvoll sind.

## Grundregeln von Nico
- Kein Entwurf: Änderungen direkt umsetzen, testen und auf `main` pushen. `dist/` wird mit eingecheckt, statichost veröffentlicht den Ordner nach dem Push.
- Nach jeder Änderung zusätzlich das Vorschau-Artifact neu veröffentlichen (siehe unten).
- Design nur auf ausdrücklichen Wunsch ändern. Barrierefreiheit: WCAG AA.
- **PageSpeed darf sich nie verschlechtern:** vor jedem Push `npm run perf` (muss grün sein).
- Nie Dateien von Nico löschen. Dateien für Nico gehen in Google Drive.
- Tonalität: Tiere beobachten und ihnen helfen, nie „anlocken“. Reihenfolge der Gruppen: Seevögel, Robben, Wale & Delfine, dann der Rest.
- Werbung nur als Text-Werbelinks (Amazon-Tag `schobiwan-21`), keine Produktbilder. Feedback nur per E-Mail-Link (`feedback_href` in `sk/components.py`), kein Kontaktformular.

## Ablauf je Änderung
1. `npm ci` (einmalig), dann `python3 build.py`
2. `python3 tools/check.py` (Links, Fotos, Bildnachweise, Daten)
3. `npm run perf` (Lighthouse Handy, 5 Seitentypen, Median aus 3 Läufen; Budget in `tests/perf.mjs`). Nur die Startseite: `NUR_START=1 node tests/perf.mjs`. Zum Vergleich auch den Stand vor der Änderung messen, die Punkte schwanken um etwa ±3.
4. Barrierefreiheit hell und dunkel mit axe prüfen (z. B. axe-core per Playwright gegen `dist/`)
5. Commit als Nico: `git -c user.name="Nico Schober" -c user.email="info@nicoschober.com" commit …`, dann `git push origin main`
6. Vorschau veröffentlichen

## Vorschau-Artifact
- Artifact „Meereskompass Website“: https://claude.ai/artifact/6N5Ft7rGrivLCDRvnM5TDv
- Inhalt ist `dist/` (ohne `photos_src`), höchstens 256 Dateien pro Aufruf, daher in zwei Teilen veröffentlichen.
- Ein Artifact fasst höchstens 512 Dateien. Seit Nov. 2026 fehlen dort deshalb robots.txt, sitemap.xml, llms.txt, die Schrift-Lizenztexte und die nicht mehr genutzten x-Fotos. Seit 18. Nov. 2026 außerdem 404.html, site.webmanifest, icon-192/512.png und apple-touch-icon.png (Platz für neue Seiten). Das Artifact ist damit wieder bei 511 von 512 Dateien: vor neuen Seiten weitere unwichtige Dateien per `remove` herausnehmen. Am einfachsten nur geänderte Dateien hochladen (`git diff --name-only HEAD~1 -- dist`).

## Nützliches
- Neue Arten: Eintrag in `data.py` (dazu `CALLS` und `SEA_NOTE`), Foto plus Nachweis in `credits.json`, bei Seevögeln Ruf in `audio/` und `audio.json`. Commons blockt Anfragen aus der Claude-Umgebung oft (HTTP 429), dann über GitHub Actions laden. Die Startseiten-Karten tragen keine Suchtexte, `home.js` lädt sie bei der ersten Suche aus `search.json`.
- Monat der Startseite (Tier des Monats, „Jetzt im …“) wird beim Bauen gesetzt (`NOWM_BUILD` in `sk/core.py`, überschreibbar mit `BUILD_MONTH`); `.github/workflows/monatlich.yml` baut am 1. jedes Monats neu und pusht `dist/`.
- Aussehen-Seiten: Titel, die auf „: diese Arten passen“ enden, werden automatisch zu „<h1>? n Arten mit Fotos“ (Formel vom Vogelkompass, rankt dort am besten).
- Inhalte: `data.py` (Arten), `data_aussehen.py`, `data_gruppen.py`, `data_helfen.py` (Anleitungen „Tieren helfen“ unter /helfen/).
- Familienmodus (`?familie`): blendet Werbung aus; Abschnitte mit Klasse `adsec` verschwinden ganz, Blöcke mit `famonly` erscheinen dafür.
- Fotos: Neben jedem WebP liegt eine AVIF-Fassung (`node tools/make_avif.mjs` nach neuen Fotos). Fotos immer über `img()`/`thumb()` in `sk/components.py` einbinden, die das `<picture>` mit AVIF-Quelle schreiben.
- Getestet und verworfen (Nov. 2026): kritisches CSS inline (verschlechterte LCP auf Start- und Bildseiten), eigenes kleineres CSS für die Startseite (kein Gewinn), Schriften weiter verkleinern (unter 10 %).
- Keine Einblende-Animationen beim ersten Zeichnen für Karten. Ersatzschriften mit angepassten Maßen am Anfang von `src/css/base.css` verhindern Verrutschen beim Schriftwechsel (CLS 0).

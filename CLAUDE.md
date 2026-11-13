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
3. `npm run perf` (Lighthouse Handy, 5 Seitentypen, Median aus 3 Läufen; Budget in `tests/perf.mjs`)
4. Barrierefreiheit hell und dunkel mit axe prüfen (z. B. axe-core per Playwright gegen `dist/`)
5. Commit als Nico: `git -c user.name="Nico Schober" -c user.email="info@nicoschober.com" commit …`, dann `git push origin main`
6. Vorschau veröffentlichen

## Vorschau-Artifact
- Artifact „Meereskompass Website“: https://claude.ai/artifact/6N5Ft7rGrivLCDRvnM5TDv
- Inhalt ist `dist/` (ohne `photos_src`), höchstens 256 Dateien pro Aufruf, daher in zwei Teilen veröffentlichen.

## Nützliches
- Inhalte: `data.py` (Arten), `data_aussehen.py`, `data_gruppen.py`, `data_helfen.py` (Anleitungen „Tieren helfen“ unter /helfen/).
- Familienmodus (`?familie`): blendet Werbung aus; Abschnitte mit Klasse `adsec` verschwinden ganz, Blöcke mit `famonly` erscheinen dafür.
- Keine Einblende-Animationen beim ersten Zeichnen für Karten. Ersatzschriften mit angepassten Maßen am Anfang von `src/css/base.css` verhindern Verrutschen beim Schriftwechsel (CLS 0).

# Meereskompass – Arbeitsregeln für Claude

Website meereskompass.de (statisch, Python-Generator `build.py` + Paket `sk/`, Repository heißt weiter `strandkompass`). Schwesterseite von vogelkompass.de; Neuerungen dort werden auf Wunsch übernommen, wenn sie hier sinnvoll sind.

## Gemeinsame Regeln aller Kompassseiten
Gilt gleich für Vogel-, Waldtier-, Meeres- und Gartentierkompass. Dieser Abschnitt ist in allen vier Repositories identisch; Änderungen in alle vier übernehmen.

- Betreiber: Nico Schober. Antworten auf Deutsch, Anrede „Nico“.
- Kein Entwurf: Änderungen direkt umsetzen, testen und auf `main` pushen. Erst dann „live“ melden, wenn die Änderung wirklich online ist (z. B. `/version.txt` oder die geänderte Seite abrufen), nicht schon nach dem Push.
- Bei jeder Änderung Barrierefreiheit (WCAG AA, axe hell und dunkel) und PageSpeed prüfen – das muss immer sein. **PageSpeed darf sich nie verschlechtern.**
- Design nur auf ausdrücklichen Wunsch ändern. Keine neuen Einblende-Animationen beim Laden (PageSpeed wertet ausgeblendeten Inhalt als nicht sichtbar); Vogel- und Meereskompass haben keine, Wald- und Gartentierkompass blenden ihre Tierkarten noch ein.
- Nie Dateien von Nico löschen. Dateien für Nico gehen in Google Drive.
- Tonalität: Tiere beobachten und ihnen helfen, nie „anlocken“.
- Werbung: Amazon-Partner-Tag `schobiwan-21`, Werbelinks mit * gekennzeichnet. Feedback nur per E-Mail-Link an info@nicoschober.com, kein Kontaktformular. Keine Cookies, kein Tracking.
- Commit als Nico: `git -c user.name="Nico Schober" -c user.email="info@nicoschober.com" commit …`
- Veröffentlicht wird nur `dist/` (`statichost.yml`: `public: dist`), Quellcode bleibt privat.
- Strukturdaten: Nico Schober überall mit derselben Kennung `https://nicoschober.com/#person`. Über-Seite nach dem Muster „Über den …: Macher, Quellen, Finanzierung“.
- Monatlicher Neubau am 1. jedes Monats per GitHub Actions (`.github/workflows/monatlich.yml`).

### Tests (gleicher Umfang auf allen vier Seiten)
- `npm test`: Seitentest mit echtem Browser über alle Seiten, hell und dunkel: Statuscode, Titel höchstens 70 Zeichen und keiner doppelt, Beschreibung 50–160 Zeichen, genau eine h1, Bilder, JSON-LD, interne Links, Skriptfehler, axe; außerdem kein seitliches Scrollen bei 320–1280 px. Dazu die eigenen Prüfungen der Seite.
- `npm run perf`: Leistungsbudget mit Lighthouse (Handy, wie PageSpeed Insights), 5 Seitentypen, Median aus 3 Läufen. Ziel wie beim Vogelkompass: 95 Punkte, LCP 2,5 s, Speed Index 2 s, Blockierzeit 250 ms, CLS 0,01. Wo eine Seite heute darunter liegt, steht ihr aktueller Stand als Untergrenze in der Konfiguration.
- Wald-, Meeres- und Gartentierkompass nutzen dafür dieselben Dateien `tests/kompass/serve.mjs`, `seiten.mjs` und `perf.mjs` (nur `kompass.config.mjs` ist je Seite verschieden). Der Vogelkompass prüft dasselbe mit `tests/e2e.mjs` und `tests/perf.mjs`.

## Eigene Regeln Meereskompass
- Reihenfolge der Gruppen: Seevögel, Robben, Wale & Delfine, dann der Rest.
- Werbung nur als Text-Werbelinks, keine Produktbilder. Feedback-Link: `feedback_href` in `sk/components.py`.
- Nach jeder Änderung zusätzlich das Vorschau-Artifact neu veröffentlichen (siehe unten).

## Ablauf je Änderung
1. `npm ci` (einmalig), dann `npm run build`
2. `npm test` (`tools/check.py`: Links, Fotos, Bildnachweise, Daten; dann der gemeinsame Seitentest mit axe hell und dunkel)
3. `npm run perf` (Leistungsbudget, Seiten und Grenzen in `tests/kompass/kompass.config.mjs`). Nur die Startseite: `NUR_START=1 npm run perf`. Zum Vergleich auch den Stand vor der Änderung messen, die Punkte schwanken um etwa ±3.
4. Commit als Nico, dann `git push origin main`
5. Vorschau veröffentlichen und prüfen, dass die Änderung live ist (`https://meereskompass.de/version.txt`)

## Vorschau-Artifact
- Artifact „Meereskompass Website“: https://claude.ai/artifact/6N5Ft7rGrivLCDRvnM5TDv
- Inhalt ist `dist/` (ohne `photos_src`), höchstens 256 Dateien pro Aufruf, daher in zwei Teilen veröffentlichen.
- Ein Artifact fasst höchstens 512 Dateien. Seit Nov. 2026 fehlen dort deshalb robots.txt, sitemap.xml, llms.txt, die Schrift-Lizenztexte und die nicht mehr genutzten x-Fotos. Seit 18. Nov. 2026 außerdem die `photos/*-400.webp` (Browser nehmen dort ohnehin die AVIF-Fassung), dadurch rund 440 von 512 Dateien. Am einfachsten nur geänderte Dateien hochladen (`git diff --name-only HEAD~1 -- dist`).

## Nützliches
- Neue Arten: Eintrag in `data.py` (dazu `CALLS` und `SEA_NOTE`), Foto plus Nachweis in `credits.json`, bei Seevögeln Ruf in `audio/` und `audio.json`. Commons blockt Anfragen aus der Claude-Umgebung oft (HTTP 429), dann über GitHub Actions laden. Die Startseiten-Karten tragen keine Suchtexte, `home.js` lädt sie bei der ersten Suche aus `search.json`.
- Monat der Startseite (Tier des Monats, „Jetzt im …“) wird beim Bauen gesetzt (`NOWM_BUILD` in `sk/core.py`, überschreibbar mit `BUILD_MONTH`); `.github/workflows/monatlich.yml` baut am 1. jedes Monats neu und pusht `dist/`.
- Aussehen-Seiten: Titel, die auf „: diese Arten passen“ enden, werden automatisch zu „<h1>? n Arten mit Fotos“ (Formel vom Vogelkompass, rankt dort am besten).
- Inhalte: `data.py` (Arten), `data_aussehen.py`, `data_gruppen.py`, `data_helfen.py` (Anleitungen „Tieren helfen“ unter /helfen/).
- Familienmodus (`?familie`): blendet Werbung aus; Abschnitte mit Klasse `adsec` verschwinden ganz, Blöcke mit `famonly` erscheinen dafür.
- Fotos: Neben jedem WebP liegt eine AVIF-Fassung (`node tools/make_avif.mjs` nach neuen Fotos). Fotos immer über `img()`/`thumb()` in `sk/components.py` einbinden, die das `<picture>` mit AVIF-Quelle schreiben.
- Getestet und verworfen (Nov. 2026): kritisches CSS inline (verschlechterte LCP auf Start- und Bildseiten), eigenes kleineres CSS für die Startseite (kein Gewinn), Schriften weiter verkleinern (unter 10 %).
- Keine Einblende-Animationen beim ersten Zeichnen für Karten. Ersatzschriften mit angepassten Maßen am Anfang von `src/css/base.css` verhindern Verrutschen beim Schriftwechsel (CLS 0).

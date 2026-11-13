// Leistungsbudget wie beim Vogelkompass: Lighthouse (Handy, gedrosselt wie PageSpeed Insights) auf den wichtigsten Seitentypen.
// Jede Seite läuft dreimal, gewertet wird der Median. Schlägt fehl, sobald eine Seite unter das Budget fällt.
// Aufruf: npm run perf (nach npm run build). Braucht Chrome (CHROME_PATH, sonst /usr/bin/google-chrome) und Netz für npx.
// Hinweis: Der lokale Server liefert ohne Kompression aus, die Werte sind deshalb strenger als live bei statichost.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

/* Budget je Seite: Datenmenge höchstens (KB), rund 10 % über dem Stand vom 13.11.2026 (ohne Kompression gemessen).
   Die Punkte schwanken in dieser Umgebung um etwa ±3, daher liegt die Grenze etwas unter dem gemessenen Median. */
const PAGES = [
  { path: '', name: 'Startseite', kb: 920 },
  { path: 'arten/seehund/', name: 'Artseite', kb: 270 },
  { path: 'arten/robben/', name: 'Gruppe', kb: 260 },
  { path: 'unterscheiden/seehund-oder-kegelrobbe/', name: 'Vergleich', kb: 270 },
  { path: 'helfen/robbe-am-strand/', name: 'Anleitung', kb: 230 },
];
const MIN_SCORE = 78, MAX_TBT = 250, MAX_CLS = 0.01, RUNS = 3;

const root = path.resolve(import.meta.dirname, '..', 'dist');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.woff2': 'font/woff2',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.json': 'application/json', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${server.address().port}`;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mk-perf-'));
const median = a => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];
let failed = 0;
try {
  for (const pg of PAGES) {
    const runs = [];
    for (let i = 0; i < RUNS; i++) {
      const out = path.join(tmp, `r${i}.json`);
      await promisify(execFile)('npx', ['--yes', 'lighthouse@12.8.2', `${url}/${pg.path}`, '--only-categories=performance', '--form-factor=mobile',
        '--output=json', `--output-path=${out}`, '--chrome-flags=--headless=new --no-sandbox', '--quiet'],
        { timeout: 180000, env: { ...process.env, CHROME_PATH: process.env.CHROME_PATH || '/usr/bin/google-chrome' } });
      const r = JSON.parse(fs.readFileSync(out, 'utf8')), a = r.audits;
      runs.push({ score: Math.round(r.categories.performance.score * 100), tbt: a['total-blocking-time'].numericValue,
        lcp: a['largest-contentful-paint'].numericValue, si: a['speed-index'].numericValue, cls: a['cumulative-layout-shift'].numericValue, kb: a['total-byte-weight'].numericValue / 1024 });
    }
    const m = Object.fromEntries(['score', 'tbt', 'lcp', 'si', 'cls', 'kb'].map(k => [k, median(runs.map(r => r[k]))]));
    const errs = [];
    if (m.score < MIN_SCORE) errs.push(`Punkte ${m.score} < ${MIN_SCORE}`);
    if (m.tbt > MAX_TBT) errs.push(`Blockierzeit ${Math.round(m.tbt)} ms > ${MAX_TBT}`);
    if (m.cls > MAX_CLS) errs.push(`CLS ${m.cls.toFixed(3)} > ${MAX_CLS}`);
    if (m.kb > pg.kb) errs.push(`${Math.round(m.kb)} KB > ${pg.kb} KB`);
    failed += errs.length ? 1 : 0;
    console.log(`${errs.length ? '✗' : '✓'} ${pg.name.padEnd(11)} ${m.score} Punkte · TBT ${Math.round(m.tbt)} ms · LCP ${(m.lcp / 1000).toFixed(1)} s · SI ${(m.si / 1000).toFixed(1)} s · CLS ${m.cls.toFixed(3)} · ${Math.round(m.kb)} KB${errs.length ? '  → ' + errs.join(', ') : ''}`);
  }
} finally { server.close(); fs.rmSync(tmp, { recursive: true, force: true }); }
console.log(failed ? `\n${failed} Seite(n) über dem Leistungsbudget` : '\nLeistungsbudget eingehalten');
process.exit(failed ? 1 : 0);

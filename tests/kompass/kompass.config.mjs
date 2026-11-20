// Einstellungen für den gemeinsamen Test der Kompassseiten (serve.mjs, seiten.mjs und perf.mjs sind in allen Repositories gleich).
// Leistungsbudget: Ziel sind die Grenzen des Vogelkompass (95 Punkte, LCP 2,5 s, Speed Index 2 s, Blockierzeit 250 ms, CLS 0,01).
// kb = Datenmenge höchstens, rund 10 % über dem Stand vom 20.11.2026 (Median, gzip wie bei statichost).
export default {
  dist: '../../dist',
  perf: [
    { path: '', name: 'Startseite', kb: 560 },
    { path: 'arten/seehund/', name: 'Artseite', kb: 150 },
    { path: 'arten/robben/', name: 'Gruppe', kb: 140 },
    { path: 'unterscheiden/seehund-oder-kegelrobbe/', name: 'Vergleich', kb: 140 },
    { path: 'helfen/robbe-am-strand/', name: 'Anleitung', kb: 120 },
  ],
};

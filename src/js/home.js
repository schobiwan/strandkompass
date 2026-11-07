// Startseite: Suche, Filter und Sortierung
import { getSea } from "./app.js";
import { $, $$, nums, escapeHtml, NOW, reduced, setPressed, focusEl } from "./util.js";
import { prepare, rank, suggest } from "./search.js";

const grid = $("grid");
const q = $("q");
const sortSel = $("sort");
const animals = $$("#grid > li.bird").map((li) => ({
  li,
  key: li.dataset.key,
  name: li.dataset.name,
  search: prepare(li.dataset.search, li.dataset.alt || "", (li.dataset.marks || "").split("|")),
  score: 0,
  grp: li.dataset.grp,
  act: li.dataset.act.split("|"),
  hab: li.dataset.hab.split("|"),
  size: li.dataset.size,
  mid: Number(li.dataset.mid),
  present: nums(li.dataset.present),
  peak: nums(li.dataset.peak),
}));
const TOTAL = animals.length;
const SETS = ["grp", "act", "hab", "size"];
const LABEL = {
  act: { nord: "Nordsee", ost: "Ostsee" },
  size: { s: "klein (bis 3 cm)", m: "handgroß (3–10 cm)", l: "groß (10–40 cm)", xl: "sehr groß (über 40 cm)" },
};

const state = {
  q: "", grp: new Set(), act: new Set(), hab: new Set(), size: new Set(), now: false, sort: "now",
  count() { return SETS.reduce((n, k) => n + this[k].size, 0) + (this.now ? 1 : 0); },
  reset(keepQuery = false) {
    if (!keepQuery) { this.q = ""; q.value = ""; }
    SETS.forEach((k) => this[k].clear());
    this.now = false;
  },
  matches(a) {
    a.score = rank(a.search, this.q);
    return a.score >= 0
      && (!this.grp.size || this.grp.has(a.grp))
      && (!this.act.size || a.act.some((x) => this.act.has(x)))
      && (!this.hab.size || a.hab.some((x) => this.hab.has(x)))
      && (!this.size.size || this.size.has(a.size))
      && (!this.now || a.present.includes(NOW))
      && (!getSea() || a.act.includes(getSea()));
  },
};

const byName = (a, b) => a.name.localeCompare(b.name, "de");
const nowRank = (a) => (a.peak.includes(NOW) ? 0 : a.present.includes(NOW) ? 1 : 2);
let lastOrder = "";

// Ohne Suche und Filter zeigt die Startseite nur die ersten Funde; Vögel, Robben und Wale stehen dann in den Bändern darüber
const FIRST = 12;
const BANDED = new Set(["Seevögel", "Robben", "Wale & Delfine"]);
let expanded = false;
const moreBox = $("gridmore"), moreBtn = $("more-btn");

function render() {
  let list = animals.filter((a) => state.matches(a));
  // Mit Suchbegriff zuerst nach Treffergüte: Name vor Doppelgänger vor Aussehen
  const byScore = (a, b) => (state.q.trim() ? a.score - b.score : 0);
  if (state.sort === "az") list.sort((a, b) => byScore(a, b) || byName(a, b));
  else if (state.sort === "size") list.sort((a, b) => byScore(a, b) || a.mid - b.mid || byName(a, b));
  else list.sort((a, b) => byScore(a, b) || nowRank(a) - nowRank(b) || byName(a, b));
  const full = list.length;
  const collapsed = !expanded && !state.q.trim() && !state.count();
  if (collapsed) list = list.filter((a) => !BANDED.has(a.grp)).slice(0, FIRST);
  if (moreBox) {
    moreBox.hidden = !collapsed || list.length >= full;
    moreBtn.textContent = `Alle ${full} Arten und Funde anzeigen`;
  }
  const order = list.map((a) => a.key).join();
  grid.classList.toggle("calm", order === lastOrder);
  if (order !== lastOrder) {
    animals.forEach((a) => { a.li.hidden = true; });
    list.forEach((a, i) => {
      a.li.hidden = false;
      a.li.style.setProperty("--i", String(Math.min(i, 14)));
      grid.appendChild(a.li);
    });
    if (!reduced()) list.forEach((a) => { a.li.style.animation = "none"; void a.li.offsetWidth; a.li.style.animation = ""; });
  }
  lastOrder = order;
  $("empty").hidden = list.length > 0;
  // Tippfehler: ähnlichsten Namen vorschlagen
  const hint = $("suggest"), guess = !list.length && state.q.trim() ? suggest(state.q, animals.map((a) => a.name)) : null;
  hint.hidden = !guess;
  if (guess) hint.innerHTML = `Meintest du <button type="button" class="suggest-btn" data-guess="${escapeHtml(guess)}">${escapeHtml(guess)}</button>?`;

  const n = state.count();
  const fc = $("fcount");
  fc.hidden = !n;
  fc.innerHTML = `${n}<span class="sr-only"> aktiv</span>`;
  const sea = getSea();
  const base = sea ? animals.filter((a) => a.act.includes(sea)).length : TOTAL;
  const where = sea === "nord" ? " an der Nordsee" : sea === "ost" ? " an der Ostsee" : "";
  $("rcount").textContent = full === base ? `${base} Arten und Funde${where}` : `${full} von ${base}${where}`;

  $$(".fchips .chip").forEach((c) => {
    const g = c.dataset.g, v = c.dataset.v;
    setPressed(c, g === "flag" ? state[v] : state[g].has(v));
  });

  const chips = [];
  const chip = (attrs, label) => `<button type="button" ${attrs} aria-label="Filter ${escapeHtml(label)} entfernen">${escapeHtml(label)}</button>`;
  if (state.q.trim()) chips.push(chip('data-rm="q"', `Suche: „${state.q.trim()}“`));
  SETS.forEach((g) => state[g].forEach((v) => chips.push(chip(`data-rm="${g}" data-v="${escapeHtml(v)}"`, LABEL[g]?.[v] || v))));
  if (state.now) chips.push(chip('data-rm="now"', "Jetzt zu finden"));
  if (chips.length > 1) chips.push('<button type="button" class="clear" data-rm="all">Alles zurücksetzen</button>');
  const act = $("active");
  act.innerHTML = chips.join("");
  act.hidden = !chips.length;
}

let t = 0;
q.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { state.q = q.value; render(); }, 120); });
q.addEventListener("keydown", (e) => { if (e.key === "Escape" && q.value) { e.preventDefault(); q.value = ""; state.q = ""; render(); } });
sortSel.addEventListener("change", () => { state.sort = sortSel.value; render(); });

const panel = $("fpanel"), toggle = $("f-toggle");
const showPanel = (on = panel.hidden) => { panel.hidden = !on; toggle.setAttribute("aria-expanded", String(on)); };
toggle.addEventListener("click", () => showPanel());
$("f-done").addEventListener("click", () => { showPanel(false); toggle.focus(); });
$("f-reset").addEventListener("click", () => { state.reset(true); render(); });
$("empty-reset").addEventListener("click", () => { state.reset(); render(); focusEl(q); });
$("suggest").addEventListener("click", (e) => {
  const b = e.target.closest("[data-guess]");
  if (!b) return;
  q.value = b.dataset.guess; state.q = q.value; render(); focusEl(q);
});
// Suchbegriff aus der Schnellsuche anderer Seiten (?q=…)
const urlQ = new URLSearchParams(location.search).get("q");
if (urlQ) { q.value = urlQ; state.q = urlQ; }
panel.addEventListener("click", (e) => {
  const c = e.target.closest(".fchips .chip");
  if (!c) return;
  const g = c.dataset.g, v = c.dataset.v;
  if (g === "flag") state[v] = !state[v];
  else state[g].has(v) ? state[g].delete(v) : state[g].add(v);
  render();
});
$("active").addEventListener("click", (e) => {
  const b = e.target.closest("[data-rm]");
  if (!b) return;
  const r = b.dataset.rm;
  if (r === "all") state.reset();
  else if (r === "q") { state.q = ""; q.value = ""; }
  else if (r === "now") state.now = false;
  else state[r].delete(b.dataset.v);
  render();
  focusEl($("active").querySelector("button") || q);
});
moreBtn?.addEventListener("click", () => {
  const n = grid.querySelectorAll("li.bird:not([hidden])").length;
  expanded = true; render();
  focusEl(grid.querySelectorAll("li.bird:not([hidden]) a.open")[n] || q);
});
render();
grid.classList.add("calm");

// Fund des Monats: erste Art in Hauptzeit, Seevögel haben Vorrang (Reihenfolge aus dem Build)
const SPOT = JSON.parse($("spotdata")?.textContent || "[]");
$$(".birdtiles").forEach((ul) => [...ul.children].forEach((li, i) => { li.dataset.o = String(i); }));
function setupNow() {
  const sea = getSea();
  const items = SPOT.filter((x) => !sea || x.act.includes(sea));
  const top = items.find((x) => x.h.includes(NOW)) || items.find((x) => x.p.includes(NOW));
  if (!top) return;
  if (top.k !== $("spot-link")?.getAttribute("href")?.split("/")[1]) {
    const im = $("spot-img");
    $("spot-link").href = `arten/${top.k}/index.html`;
    im.src = `photos/${top.k}.webp`;
    im.srcset = `photos/${top.k}-400.webp 400w, photos/${top.k}.webp 720w`;
    $("spot-name").textContent = top.n;
    $("spot-hl").textContent = top.hl;
    $("spot-cred").innerHTML = document.getElementById(top.k)?.querySelector(":scope > small")?.innerHTML || "";
  }
  // In den Bändern rückt die Art aus dem Kopfbereich ans Ende, damit sie nicht doppelt vorn steht
  $$(".birdtiles").forEach((band) => {
    const tiles = [...band.children];
    tiles.sort((a, b) => (a.dataset.k === top.k) - (b.dataset.k === top.k) || Number(a.dataset.o) - Number(b.dataset.o));
    tiles.forEach((li) => band.appendChild(li));
  });
}
setupNow();
document.addEventListener("seachange", () => { setupNow(); render(); });

// Tiergruppen im Kopfbereich und im Seevögel-Band setzen den Gruppenfilter
$$("[data-hgrp]").forEach((b) => b.addEventListener("click", () => {
  state.grp.clear(); b.dataset.hgrp.split("|").forEach((g) => state.grp.add(g)); render();
  $("arten").scrollIntoView({ behavior: reduced() ? "auto" : "smooth" });
}));

// Suche im Kopfbereich steuert das Raster
const hq = $("hq");
$("hsearch")?.addEventListener("submit", (e) => {
  e.preventDefault();
  q.value = hq.value; state.q = hq.value; render();
  $("arten").scrollIntoView({ behavior: reduced() ? "auto" : "smooth" });
});
hq?.addEventListener("input", () => { q.value = hq.value; state.q = hq.value; render(); });


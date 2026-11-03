// Vogelrufe abspielen: ein gemeinsamer Player für alle Knöpfe mit data-play
import { $$ } from "./util.js";

let audio = null, current = null, raf = 0;

function setState(btn, playing) {
  btn.setAttribute("aria-pressed", String(playing));
  btn.classList.toggle("playing", playing);
  if (!playing) btn.style.setProperty("--p", "0");
}

function tick() {
  if (!audio || !current) return;
  const p = audio.duration ? audio.currentTime / audio.duration : 0;
  current.style.setProperty("--p", String(p));
  raf = requestAnimationFrame(tick);
}

function stop() {
  if (audio) audio.pause();
  if (current) setState(current, false);
  cancelAnimationFrame(raf);
  current = null;
}

document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-play]");
  if (!btn) return;
  e.preventDefault();
  if (current === btn) { stop(); return; }
  stop();
  audio = audio || new Audio();
  audio.src = btn.dataset.src;
  audio.onended = stop;
  audio.onerror = stop;
  current = btn;
  setState(btn, true);
  audio.play().then(() => { raf = requestAnimationFrame(tick); }).catch(stop);
});

document.addEventListener("keydown", (e) => { if (e.key === "Escape" && current) stop(); });
$$("[data-play]").forEach((b) => setState(b, false));

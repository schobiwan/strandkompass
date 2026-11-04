# -*- coding: utf-8 -*-
"""Wiederverwendbare Bausteine: Fotos, Bildnachweise, Karten, Kästen."""
from .core import *
from .icons import *

def acts_attr(acts):
    return "|".join(acts)

def counts(ss):
    """Zahl, die sich beim Umschalten des Meeres anpasst."""
    a = len(ss); n = sum(1 for x in ss if "nord" in x["act"]); o = sum(1 for x in ss if "ost" in x["act"])
    return f'<span data-cnt-all="{a}" data-cnt-nord="{n}" data-cnt-ost="{o}">{a}</span>'

# ------------------------------------------------------------------ Bausteine
def img(R, key, alt="", eager=False, cls="", sizes="(max-width: 600px) 92vw, 400px"):
    lz = "eager" if eager else "lazy"
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{R}photos/{key}.webp" srcset="{R}photos/{key}-400.webp 400w, {R}photos/{key}.webp 720w" sizes="{sizes}" '
            f'alt="{esc(alt)}" width="720" height="576" loading="{lz}" decoding="async">')

def lic_url(lic):
    """Link auf den Lizenztext (Creative Commons verlangt ihn bei jeder Nutzung)."""
    import re as _re
    m = _re.match(r"CC (BY(?:-SA)?) (\d\.\d)(?: (\w\w))?$", lic)
    if m:
        return f"https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/" + (f"{m.group(3)}/" if m.group(3) else "")
    if lic == "CC0":
        return "https://creativecommons.org/publicdomain/zero/1.0/deed.de"
    return ""

def lic_link(lic):
    u = lic_url(lic)
    return f'<a href="{u}" target="_blank" rel="noopener license">{esc(lic)}</a>' if u else esc(lic)

def credit_parts(a, lic, url):
    return (f'Foto: <a href="{esc(url)}" target="_blank" rel="noopener">{esc(a)}</a>, {lic_link(lic)}')

def credit(key, short=False):
    a, lic, url = CREDITS[key]
    return credit_parts(a, lic, url) + ("" if short else ", Wikimedia Commons, zugeschnitten")

def cred(key):
    """Kleine Bildangabe direkt auf dem Foto, liegt über dem Kartenlink."""
    return f'<small class="cred">{credit(key, True)}</small>'

def card(R, s, i=0):
    acts = "".join(f'<span class="act" title="{ACTS[a]}">{act_svg(a)}<span class="sr-only">{ACTS[a]}</span></span>' for a in s["act"])
    search = " ".join([s["n"], s["lat"], s["grp"]] + [ACTS[a] for a in s["act"]])
    return (f'<li class="bird" id="{s["k"]}" style="--i:{i}" data-key="{s["k"]}" data-name="{esc(s["n"])}" data-search="{esc(search)}" '
            f'data-grp="{esc(s["grp"])}" data-act="{"|".join(s["act"])}" data-hab="{esc("|".join(s["hab"]))}" data-size="{s["size"]}" data-mid="{s["mid"]}" '
            f'data-present="{",".join(map(str, s["p"]))}" data-peak="{",".join(map(str, s["h"]))}"> '
            f'{img(R, s["k"], "", eager=i < 6)}{cred(s["k"])} <div class="txt"> <h3><a class="open" href="{R}arten/{s["k"]}/index.html">{esc(s["n"])}</a></h3> '
            f'<span class="meta"><span class="latin" lang="la">{esc(s["lat"])}</span><span class="size">{esc(s["sz"])}</span></span> '
            f'<span class="row"><span class="tag status">{esc(s["grp"])}</span></span> <p class="short">{esc(s["short"])}</p> </div> '
            f'<span class="acts">{acts}</span> </li>')

def months_bar(s):
    out = []
    for m in range(1, 13):
        cls = "h" if m in s["h"] else ("p" if m in s["p"] else "")
        t = "Hauptzeit" if cls == "h" else ("aktiv" if cls == "p" else "kaum zu sehen")
        out.append(f'<span data-month="{m}" class="{cls}" title="{MONTHS[m-1]}: {t}">{MSHORT[m-1]}</span>')
    return (f'<div class="months" aria-hidden="true"> {"".join(out)} </div>'
            '<ul class="monthlegend" aria-hidden="true"><li><i class="p"></i>zu finden</li><li><i class="h"></i>beste Zeit</li><li><i class="now"></i>jetzt</li></ul>')

def pair_card(R, p, h="h2"):
    figs = "".join(f'<figure>{img(R, photo_key(k))}<figcaption><span aria-hidden="true">{esc(name_of(k))}</span><small>{credit(photo_key(k), True)}</small></figcaption></figure>' for k in (p["a"], p["b"]))
    return (f'<li class="pair"> <div class="ph"> {figs} </div> <div class="pb"> <{h}><a class="pair-link" href="{R}unterscheiden/{p["k"]}/index.html">'
            f'{esc(name_of(p["a"]))} oder {esc(name_of(p["b"]))}?</a></{h}> <p>{esc(p["short"])}</p> <span class="to" aria-hidden="true">Alle Unterschiede</span> </div> </li>')

def chipset(legend, g, items):
    return f'<fieldset><legend>{legend}</legend><div class="fchips">' + "".join(
        f'<button class="chip" type="button" data-g="{g}" data-v="{esc(v)}" aria-pressed="false">{esc(t)}</button>' for v, t in items) + '</div></fieldset>'

def seapair(R, overview=False):
    def card_(k, title, facts, txt):
        n = sum(1 for x in SPECIES if k in x["act"]); only = sum(1 for x in SPECIES if x["act"] == [k])
        lis = "" if overview else "".join(f"<li>{esc(f)}</li>" for f in facts)
        return (f'<li class="seacard seacard-{k}"><a href="{R}{"nordsee" if k == "nord" else "ostsee"}/index.html"><b>{title}</b><span>{esc(txt)}</span>'
                f'<ul>{lis}</ul><span class="sc-n">{n} Arten und Funde{f", {only} davon nur hier" if only else ""}</span></a></li>')
    head = ('<h2 id="sp-h">Alle Funde je Meer</h2><p class="intro">Was du nur an der Nordsee oder nur an der Ostsee findest, mit allen Arten und Funden.</p>' if overview else
            '<h2 id="sp-h">Nordsee oder Ostsee?</h2><p class="intro">Die beiden Meere sind sehr verschieden. Das merkst du schon daran, was am Strand liegt und welche Vögel dort leben.</p>')
    return ('<section class="block seapair" aria-labelledby="sp-h"><div class="wrap">' + head + '<ul class="seacards">'
            + card_("nord", "Nordsee", ["Ebbe und Flut, 2 bis 4 Meter Unterschied", "Wattenmeer, Halligen und Sandbänke", "Seehunde, Basstölpel und Trottellummen"],
                    "Salziges Gezeitenmeer mit dem Wattenmeer, einem der wichtigsten Rastgebiete für Zugvögel weltweit.")
            + card_("ost", "Ostsee", ["Kaum Gezeiten, der Wind bestimmt den Wasserstand", "Viel weniger Salz als die Nordsee", "Bernstein, Feuersteine und Steilküsten"],
                    "Ein fast geschlossenes Binnenmeer mit Bodden, Förden und Steilküsten. Im Winter rasten hier riesige Entenschwärme.")
            + '</ul>' + ('' if overview else f'<p class="actions"><a class="btn ghost" href="{R}nordsee-ostsee/index.html">Alle Unterschiede im Vergleich</a></p>') + '</div></section>')

def seabox(s):
    note = SEA_NOTE.get(s["k"], {})
    cols = ""
    for a in ("nord", "ost"):
        has = a in s["act"]
        txt = note.get(a) or (f"An der {ACTS[a]} zu finden." if has else f"An der {ACTS[a]} kaum oder gar nicht.")
        cols += (f'<div class="seacol seacol-{a}{"" if has else " no"}"><h3>{ACTS[a]}</h3>'
                 f'<p class="seayes">{"Kommt vor" if has else "Kaum oder gar nicht"}</p><p>{esc(txt)}</p></div>')
    return f'<section class="seabox" aria-labelledby="h-sea"><h2 id="h-sea">Nordsee und Ostsee</h2><div class="seacols">{cols}</div></section>'

SEA_LBL = {"nord": "Nordsee", "ost": "Ostsee", "beide": "Nord- und Ostsee"}

def ev_li(e, tag=False):
    sea, t = e
    lab = f'<span class="evsea evsea-{sea}">{SEA_LBL[sea]}</span> ' if tag else ""
    return f'<li data-sea-only="{sea}">{lab}{esc(t)}</li>'


# ------------------------------------------------------------------ Vogelrufe
PLAY_ICON = ('<svg class="i-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3v10l8-5z"/></svg>'
             '<svg class="i-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 3h3v10H4zM9 3h3v10H9z"/></svg>')

def play_button(R, key, name, cls=""):
    """Abspielknopf für den Ruf; leer, wenn es keine Aufnahme gibt."""
    if key not in AUDIO:
        return ""
    sec = AUDIO[key][3]
    return (f'<button type="button" class="play{(" " + cls) if cls else ""}" data-play data-src="{R}audio/{key}.mp3" aria-pressed="false" '
            f'aria-label="Ruf: {esc(name)} anhören, {sec} Sekunden">{PLAY_ICON}</button>')

def sound_credit(key):
    a, lic, url, _ = AUDIO[key]
    return f'Aufnahme: <a href="{esc(url)}" target="_blank" rel="noopener">{esc(a)}</a>, {lic_link(lic)}'

def callbox(R, s):
    """Ruf mit Abspielknopf, Beschreibung und Nachweis der Aufnahme."""
    if not s.get("call"):
        return ""
    btn = play_button(R, s["k"], s["n"], "play-lg")
    sec = f'<span class="cb-sec">{AUDIO[s["k"]][3]} Sekunden</span>' if s["k"] in AUDIO else ""
    cr = f'<small class="cb-cred">{sound_credit(s["k"])}</small>' if s["k"] in AUDIO else ""
    return (f'<div class="callbox">{btn}<div class="cb-txt"><p class="cb-h">Ruf {sec}</p><p class="cb-call">{esc(s["call"])}</p>{cr}</div></div>')

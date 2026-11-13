# -*- coding: utf-8 -*-
"""Anleitungen „Helfen an der Küste“ (/helfen/ und /helfen/<slug>/), Gegenstück zu „Selber machen“ beim Vogelkompass.
Inhalte in data_helfen.py. Ohne Werbung: Diese Seiten sind auch das Ziel des Ersatzblocks im Familienmodus (helfen_cards)."""
from ..core import *
from ..layout import *
from ..components import *
from data_helfen import GUIDES, TEASERS

GUIDE_BY = {g["slug"]: g for g in GUIDES}
PUBLISHED = "2026-11-13"


def helfen_cards(R, slugs=None):
    """Karten zu den Anleitungen (ganze Fläche ist der Link)."""
    gs = [GUIDE_BY[s] for s in slugs] if slugs else GUIDES
    return '<ul class="explore">' + "".join(
        f'<li><a href="{R}helfen/{g["slug"]}/index.html"><b>{esc(g["name"])}</b><span>{esc(g["card"])}</span></a></li>' for g in gs) + "</ul>"


def helfen_teaser(R, slugs, extra_cls="", hid="h-helfen"):
    """Block „Helfen an der Küste“ mit passenden Anleitungen, z. B. auf Gruppenseiten."""
    cls = f"block {extra_cls}".strip()
    return (f'<section class="{cls}" aria-labelledby="{hid}"><div class="wrap"><h2 id="{hid}">Helfen an der Küste</h2>'
            f'<p class="intro">Was du tun kannst, wenn ein Tier Hilfe braucht, und wie du beobachtest, ohne zu stören. '
            f'Alle Anleitungen findest du unter <a href="{R}helfen/index.html">Tieren helfen</a>.</p>{helfen_cards(R, slugs)}</div></section>')


def group_teaser(R, g):
    return helfen_teaser(R, TEASERS[g]) if g in TEASERS else ""


def _html(R, s):
    return s.replace("{R}", R)


def build_helfen():
    R = "../"
    body = (f'<section class="block page"> <div class="wrap"> <h1>Tieren an der Küste helfen</h1> '
            f'<p class="intro">Eine junge Robbe allein am Strand, ein verölter Seevogel, ein toter Schweinswal im Spülsaum: An der Küste begegnen dir manchmal Tiere, die Hilfe zu brauchen scheinen. '
            f'Meist hilfst du am meisten mit Abstand und einer Meldung an die richtige Stelle. Diese Anleitungen zeigen, was zu tun ist, und wie du Seevögel und Strandleben beobachtest, ohne zu stören.</p> '
            f'{helfen_cards(R)} </div> </section>'
            f'<section class="block"><div class="wrap"><div class="prose"><h2>Auch wichtig</h2><p>Welche Quallen brennen, was nach Quallenkontakt hilft und warum Bernstein an der Ostsee in eine Metalldose gehört, '
            f'steht unter <a href="{R}am-strand/index.html">Sicher am Strand</a>. Hoch- und Niedrigwasserzeiten und die Regeln im Nationalpark findest du dort ebenfalls.</p></div>{byline(R, "Tieren helfen")}</div></section>')
    ld_list = ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tieren an der Küste helfen", "inLanguage": "de-DE", "url": f"{DOMAIN}/helfen/",
                  "isPartOf": {"@id": WEBSITE_ID}, "publisher": {"@id": ORG_ID},
                  "mainEntity": {"@type": "ItemList", "numberOfItems": len(GUIDES), "itemListElement": [
                      {"@type": "ListItem", "position": i + 1, "name": g["title"], "url": f"{DOMAIN}/helfen/{g['slug']}/"} for i, g in enumerate(GUIDES)]}})
    write("helfen/index.html", page("helfen/index.html", "Tieren an der Küste helfen: Robbe, Seevogel, Wal",
          "Junge Robbe allein am Strand, verölter Seevogel, toter Schweinswal: So hilfst du an Nord- und Ostsee richtig. Dazu Strandmüll sammeln und Vögel beobachten, ohne zu stören.",
          body, active="helfen", crumbs=[("Tieren helfen", "")], seafilter=False, extra_ld=ld_list))

    R = "../../"
    for i, g in enumerate(GUIDES):
        path = f"helfen/{g['slug']}/index.html"
        k = g["photo"]
        steps = '<ol class="steps">' + "".join(f"<li><b>{esc(a)}</b> {_html(R, b)}</li>" for a, b in g["steps"]) + "</ol>"
        tips = '<ul class="explore tips">' + "".join(f"<li><div><b>{esc(a)}</b><span>{_html(R, b)}</span></div></li>" for a, b in g["tips"]) + "</ul>"
        sp = '<div class="pills">' + "".join(f'<a href="{R}arten/{s}/index.html">{esc(name_of(s))}</a>' for s in g["species"]) + "</div>"
        faq = '<div class="faq">' + "".join(f'<details class="fold faqitem" open data-fold><summary><h3>{esc(q)}</h3></summary><p>{_html(R, a)}</p></details>' for q, a in g["faq"]) + "</div>"
        src = ('<h3 class="srchead">Quellen</h3><ul class="srclist">' + "".join(f"<li>{ext_link(esc(u), esc(t))}</li>" for t, u in g["sources"]) + "</ul>") if g["sources"] else ""
        more = [GUIDES[(i + n) % len(GUIDES)]["slug"] for n in (1, 2, 3)]
        body = (f'<section class="block page"> <div class="wrap"> <div class="hp-head"> <div> <h1>{esc(g["title"])}</h1> <p class="intro">{esc(g["intro"])}</p> </div> '
                f'<figure class="hp-photo">{img(R, k, name_of(k), eager=True, sizes="(max-width: 760px) 92vw, 420px")}<figcaption>{credit(k)}</figcaption></figure> </div> '
                f'{tldr_box(g["tldr"])} </div> </section>'
                f'<section class="block" aria-labelledby="h-steps"><div class="wrap"><h2 id="h-steps">So hilfst du richtig</h2>{steps}</div></section>'
                f'<section class="block" aria-labelledby="h-tips"><div class="wrap"><h2 id="h-tips">Gut zu wissen</h2>{tips}</div></section>'
                f'<section class="block" aria-labelledby="h-arten"><div class="wrap"><h2 id="h-arten">Die Arten dazu</h2>{sp}</div></section>'
                f'<section class="block" aria-labelledby="h-faq"><div class="wrap"><h2 id="h-faq">Häufige Fragen</h2>{faq}{src}{byline(R, g["name"])}</div></section>'
                f'<section class="block" aria-labelledby="h-more"><div class="wrap"><h2 id="h-more">Weitere Anleitungen</h2>'
                f'<p class="intro">Alle Anleitungen findest du unter <a href="{R}helfen/index.html">Tieren helfen</a>.</p>{helfen_cards(R, more)}</div></section>')
        plain = lambda t: re.sub(r"<[^>]+>", "", t.replace("{R}", ""))
        ld_all = ld({"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "inLanguage": "de-DE",
                     "image": f"{DOMAIN}/photos/{k}.webp", "author": AUTHOR, "publisher": {"@id": ORG_ID},
                     "datePublished": PUBLISHED, "dateModified": PUBLISHED, "mainEntityOfPage": f"{DOMAIN}/helfen/{g['slug']}/"}) + \
                 ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                     {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in g["faq"]]})
        write(path, page(path, g["title"], g["desc"], body, active="helfen", seafilter=False, og=f"{k}.webp",
                         crumbs=[("Tieren helfen", "helfen/index.html"), (g["name"], "")], extra_ld=ld_all))

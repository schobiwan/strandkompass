# -*- coding: utf-8 -*-
"""Anleitungen „Helfen an der Küste“ (/helfen/<slug>/): richtig handeln bei Robben, Totfunden, kranken Seevögeln,
Müll am Strand, beim Entdecken mit Kindern und beim Beobachten rastender Vögel.
Gegenstück zu „Selber machen“ beim Vogelkompass. Grundlage sind Seehundstationen, Deutsches Meeresmuseum,
Nationalparkverwaltungen, Landesbehörden und NABU (Quellen je Anleitung). Stand der Telefonnummern: November 2026.

Felder: slug, name (Kurzname für Karten), title (h1 und Seitentitel), desc (Meta-Beschreibung), photo (Artschlüssel fürs Foto),
card (Text der Karte), intro, tldr [(Begriff, Text)], steps [(Schritt, Text)], tips [(Titel, Text)], species [Artschlüssel],
faq [(Frage, Antwort)], sources [(Titel, URL)]. In steps, tips und intro ist einfaches HTML erlaubt (Links, Telefonnummern)."""

SEEHUNDSTATION_NORDDEICH = ("Seehundstation Nationalpark-Haus Norden-Norddeich", "https://www.seehundstation-norddeich.de/")
SH_SEEHUNDE = ("Land Schleswig-Holstein: Seehundmanagement im Nationalpark Wattenmeer", "https://www.schleswig-holstein.de/DE/fachinhalte/N/nationalpark_wattenmeer/Seehundmanagement")
SH_MEERESSAEUGER = ("Land Schleswig-Holstein: Meeressäuger, Sichtungen und Funde melden", "https://www.schleswig-holstein.de/DE/fachinhalte/A/artenschutz/meeressaeuger.html")
NABU_MEERESMUSEUM = ("NABU: Deutsches Meeresmuseum sammelt Fundmeldungen", "https://www.nabu.de/news/2017/10/23350.html")
NABU_VOGELGRIPPE = ("NABU: Vogelgrippe bedroht Wildvögel und Geflügel", "https://www.nabu.de/tiere-und-pflanzen/voegel/gefaehrdungen/krankheiten/vogelgrippe/32514.html")
SH_GEFLUEGELPEST = ("Land Schleswig-Holstein: Geflügelpest", "https://www.schleswig-holstein.de/DE/landesregierung/themen/landwirtschaft/gefluegelpest/gefluegelpest_node.html")
NABU_SAMMELAKTION = ("NABU: Eine Müllsammelaktion organisieren", "https://www.nabu.de/aktiv-werden/mitmachaktionen/meere-ohne-plastik/gewaesserretter/eine-muellsammelaktion-organisieren")
NABU_ICCD = ("NABU: Küstenputztag (International Coastal Cleanup Day)", "https://www.nabu.de/aktiv-werden/mitmachaktionen/meere-ohne-plastik/international-coastal-cleanup-day")
NLPV_MUELL = ("Nationalpark Niedersächsisches Wattenmeer: Faltblatt Meeresmüll und Strand-Müll-Boxen", "https://www.nationalpark-wattenmeer.de/wp-content/uploads/2025/03/fb_meeresmuell_nlpv_202502_web.pdf")
NATIONALPARK = ("Nationalpark Wattenmeer: Informationen der Nationalparkverwaltungen", "https://www.nationalpark-wattenmeer.de/")

TEL_FRIEDRICHSKOOG = '<a href="tel:+4948541372">04854 1372</a>'
TEL_NORDDEICH = '<a href="tel:+494931973330">04931 973330</a>'
TEL_MEERESMUSEUM = '<a href="tel:+49383126503333">03831 2650 3333</a>'

GUIDES = [
    dict(
        slug="robbe-am-strand", name="Junge Robbe am Strand", photo="seehund",
        title="Junge Robbe am Strand: richtig helfen",
        desc="Junger Seehund oder Kegelrobbe allein am Strand? Abstand halten, nicht anfassen, im Zweifel melden: So hilfst du richtig, mit Meldestellen für Nord- und Ostsee.",
        card="Abstand halten, nicht anfassen, Hunde an die Leine. Und wann du wen anrufst.",
        intro="Im Sommer an der Nordsee und im Winter auf Helgoland und an der Ostsee liegen manchmal junge Robben allein am Strand. Fast immer ist alles in Ordnung: Die Mutter jagt im Wasser und kommt zurück, wenn es ruhig ist. Am meisten hilfst du, wenn du Abstand hältst und weitergehst.",
        tldr=[("Abstand", "mindestens 300 Meter, den Weg zum Wasser frei lassen"), ("Nie", "anfassen, füttern, ins Wasser scheuchen oder einpacken"),
              ("Melden", "nur wenn das Tier verletzt oder krank wirkt oder an einem belebten Strand liegt"), ("Wer entscheidet", "Seehundjäger, Ranger und Seehundstationen")],
        steps=[
            ("Stehen bleiben und Abstand halten", "Halte mindestens 300 Meter Abstand, auf der Helgoländer Düne mindestens 30 Meter. Mit dem Fernglas siehst du trotzdem alles."),
            ("Weg zum Wasser frei lassen", "Stell dich nie zwischen Robbe und Meer. Die Mutter kommt nur zurück, wenn der Weg frei und der Strand ruhig ist."),
            ("Nicht anfassen", "Robben können kräftig beißen und Krankheiten übertragen. Hat ein Mensch das Junge berührt, nimmt die Mutter es oft nicht mehr an."),
            ("Hunde anleinen und weitergehen", "Leine deinen Hund an und verlasse den Fundort. Die Robbe muss nicht bewacht werden, und Menschentrauben halten die Mutter fern."),
            ("Im Zweifel melden", f"Wirkt das Tier verletzt, sehr mager oder krank, oder liegt es mitten zwischen Badegästen: in Schleswig-Holstein die Seehundstation Friedrichskoog ({TEL_FRIEDRICHSKOOG}), einen Seehundjäger über die Polizei oder die Robben.App, in Niedersachsen die Seehundstation Norddeich ({TEL_NORDDEICH}), in Mecklenburg-Vorpommern das Deutsche Meeresmuseum ({TEL_MEERESMUSEUM})."),
            ("Fachleuten die Entscheidung lassen", "Ob ein Tier Hilfe braucht, entscheiden Seehundjäger, Ranger oder die Seehundstation vor Ort. Nimm ein Tier nie selbst mit, auch nicht im Auto zur Station."),
        ],
        tips=[
            ("Heuler oder nur allein?", "Heuler sind junge Seehunde, die ihre Mutter dauerhaft verloren haben. Ein Junges, das allein liegt oder ruft, ist deshalb noch lange kein Heuler."),
            ("Wann es Jungtiere gibt", "Seehunde werden an der Nordsee im Juni und Juli geboren. Kegelrobben bekommen ihre Jungen im Winter, vor allem auf der Helgoländer Düne. Ab dem Spätsommer sind junge Seehunde meist schon selbstständig."),
            ("Erwachsene Robben ruhen auch", "Robben verdauen und ruhen an Land. Eine erwachsene Robbe am Strand ist kein Notfall, solange niemand sie bedrängt."),
            ("Fotos aus der Ferne", "Ein Foto mit Zoom hilft den Fachleuten bei der Einschätzung, wenn du das Tier meldest. Nah heran musst du dafür nicht."),
        ],
        species=["seehund", "kegelrobbe"],
        faq=[
            ("Darf ich eine junge Robbe ins Wasser zurücktragen?", "Nein. Robben sind Wildtiere und dürfen nicht angefasst werden. Ein Junges liegt meist absichtlich an Land und wartet auf die Mutter. Ins Wasser getragen, kann es erschöpfen und ertrinken."),
            ("Wem melde ich eine junge Robbe?", f"In Schleswig-Holstein der Seehundstation Friedrichskoog ({TEL_FRIEDRICHSKOOG}), einem Seehundjäger über die Polizei oder über die Robben.App. In Niedersachsen der Seehundstation Norddeich ({TEL_NORDDEICH}). An der Küste von Mecklenburg-Vorpommern dem Deutschen Meeresmuseum in Stralsund ({TEL_MEERESMUSEUM})."),
            ("Was passiert mit einem gemeldeten Heuler?", "Fachleute prüfen das Tier. Echte Heuler kommen in eine der beiden Seehundstationen in Friedrichskoog oder Norddeich, werden dort aufgezogen und später wieder ausgewildert."),
            ("Warum heißen sie Seehundjäger, wenn Seehunde nicht gejagt werden?", "Die Jagd auf Seehunde ist verboten. Seehundjäger sind ausgebildete Ehrenamtliche, die sich im Auftrag des Landes um angespülte, verletzte oder kranke Robben kümmern."),
        ],
        sources=[SEEHUNDSTATION_NORDDEICH, SH_SEEHUNDE, NABU_MEERESMUSEUM],
    ),
    dict(
        slug="totfund-melden", name="Toter Wal oder Robbe gefunden", photo="schweinswal",
        title="Toter Schweinswal oder Robbe: Fund melden",
        desc="Ein toter Schweinswal, Seehund oder eine Kegelrobbe am Strand? Warum jeder Fund zählt, wem du ihn an Nord- und Ostsee meldest und welche Angaben helfen.",
        card="Jeder Fund zählt für die Forschung. Wem du ihn meldest und was du dabei beachtest.",
        intro="Tote Schweinswale und Robben am Strand sind traurig, aber für den Meeresschutz wertvoll. Fachleute untersuchen die Tiere und erfahren so, woran sie gestorben sind, etwa an Krankheiten, an Unterwasserlärm oder als Beifang in Stellnetzen. Dafür müssen die Funde gemeldet und rasch geborgen werden.",
        tldr=[("Nicht anfassen", "auch tote Tiere können Krankheiten übertragen"), ("Melden", "mit genauem Fundort, Datum und Fotos"),
              ("Nordsee", "Niedersachsen: Seehundstation Norddeich, Schleswig-Holstein: Seehundjäger, Polizei oder Nationalpark"), ("Ostsee", "Mecklenburg-Vorpommern: Deutsches Meeresmuseum")],
        steps=[
            ("Abstand halten, nicht anfassen", "Fass das Tier nicht an und halte Hunde fern. Tote Meeressäuger können Krankheitserreger tragen."),
            ("Fundort festhalten", "Merke dir den genauen Ort, am besten mit den Koordinaten aus der Karten-App, dazu Datum und Uhrzeit."),
            ("Fotos machen", "Fotografiere das ganze Tier von der Seite, den Kopf und auffällige Verletzungen oder Netzspuren. Ein Gegenstand zum Größenvergleich hilft."),
            ("Fund melden", f"In Niedersachsen der Seehundstation Norddeich ({TEL_NORDDEICH}). In Schleswig-Holstein einem Seehundjäger über die Polizei, über die Robben.App oder der Nationalparkverwaltung. In Mecklenburg-Vorpommern dem Deutschen Meeresmuseum ({TEL_MEERESMUSEUM})."),
            ("Liegen lassen", "Nimm keine Teile mit, auch keine Zähne oder Knochen. Schweinswale und Robben sind streng geschützt, und die Fachleute brauchen das vollständige Tier."),
        ],
        tips=[
            ("Schweinswal oder Robbe?", 'Schweinswale haben eine kleine dreieckige Rückenflosse und keine Beine. Robben haben Flossen mit Krallen und Fell. Hilfe beim Bestimmen geben die Steckbriefe unten.'),
            ("Lebende Wale melden", "Siehst du einen lebenden Schweinswal von Land oder vom Boot aus, freut sich das Deutsche Meeresmuseum ebenfalls über die Meldung, an der Ostsee zum Beispiel über die App OstSeeTiere."),
            ("Gestrandeter lebender Wal", "Ein lebender Wal am Strand ist ein Notfall: sofort die Polizei (110) rufen, Abstand halten und den Fachleuten nicht im Weg stehen."),
            ("Warum es sich lohnt", "Nur ein Teil der toten Tiere wird überhaupt angespült und gefunden. Deshalb zählt jede einzelne Meldung."),
        ],
        species=["schweinswal", "seehund", "kegelrobbe", "zwergwal"],
        faq=[
            ("Wem melde ich einen toten Schweinswal an der Ostsee?", f"In Mecklenburg-Vorpommern dem Deutschen Meeresmuseum in Stralsund, Telefon {TEL_MEERESMUSEUM}. In Schleswig-Holstein einem Seehundjäger über die Polizei oder der Nationalparkverwaltung."),
            ("Wem melde ich eine tote Robbe an der Nordsee?", f"In Niedersachsen der Seehundstation Nationalpark-Haus Norddeich ({TEL_NORDDEICH}). In Schleswig-Holstein einem Seehundjäger über die Polizei oder über die Robben.App."),
            ("Darf ich einen Zahn oder Knochen mitnehmen?", "Nein. Schweinswale und Robben sind streng geschützt, auch tote Tiere und ihre Teile. Lass alles liegen und melde den Fund."),
        ],
        sources=[NABU_MEERESMUSEUM, SH_MEERESSAEUGER, SEEHUNDSTATION_NORDDEICH],
    ),
    dict(
        slug="seevogel-gefunden", name="Kranker oder toter Seevogel", photo="trottellumme",
        title="Kranker oder toter Seevogel: was tun?",
        desc="Ein verölter, kranker oder toter Seevogel am Strand? Warum du ihn nicht anfassen solltest, wem du ihn meldest und was bei Vogelgrippe gilt.",
        card="Nicht anfassen, Hunde fernhalten, melden. Was bei Öl und Vogelgrippe gilt.",
        intro="Nach Stürmen liegen manchmal erschöpfte, verölte oder tote Seevögel am Strand, oft Trottellummen, Eiderenten oder Möwen. Der Wunsch zu helfen ist groß. Am besten hilfst du aber, wenn du den Vogel nicht anfasst und den Fund meldest, denn auch die Vogelgrippe kann dahinterstecken.",
        tldr=[("Nicht anfassen", "weder lebende noch tote Vögel"), ("Hunde", "anleinen und fernhalten"),
              ("Tote oder kranke Vögel", "dem Veterinäramt oder Ordnungsamt melden, sonst der Polizei"), ("Verölte Vögel", "nicht selbst waschen, Fachleute verständigen")],
        steps=[
            ("Abstand halten", "Bleib einige Meter entfernt, damit der Vogel nicht in Panik flüchtet. Ein geschwächter Vogel verbraucht dabei seine letzten Kräfte."),
            ("Nicht anfassen", "Fass weder lebende noch tote Vögel mit bloßen Händen an. Hattest du doch Kontakt, wasche dir gründlich die Hände mit Wasser und Seife."),
            ("Hunde fernhalten", "Leine deinen Hund an. Hunde können sich bei kranken oder toten Vögeln anstecken."),
            ("Fund melden", "Tote oder krank wirkende Wasser- und Seevögel meldest du dem Veterinäramt oder Ordnungsamt des Landkreises, außerhalb der Dienstzeit der Polizei. Im Nationalpark helfen auch Ranger und Nationalpark-Häuser weiter."),
            ("Ort und Fotos angeben", "Sag genau, wo der Vogel liegt, und mach ein Foto. Bei mehreren toten Vögeln an einer Stelle ist die Meldung besonders wichtig."),
        ],
        tips=[
            ("Verölte Vögel nicht waschen", "Öl im Gefieder lässt Vögel auskühlen, und beim Putzen schlucken sie das Öl. Selbst waschen schadet mehr, als es hilft. Das überlassen Fachleute einer Pflegestation."),
            ("Nicht mitnehmen", "Bring einen Seevogel nicht selbst zum Tierarzt oder nach Hause. Bei Verdacht auf Vogelgrippe kann das die Krankheit weitertragen."),
            ("Nicht füttern", "Brot und Essensreste schaden Seevögeln. Ein geschwächter Vogel braucht Ruhe, keine Nahrung von Menschen."),
            ("Einzelne tote Möwe", "Ein einzelner toter Vogel am Spülsaum ist leider normal. Liegen aber mehrere an einer Stelle, melde den Fund unbedingt."),
        ],
        species=["trottellumme", "eiderente", "basstoelpel", "silbermoewe", "lachmoewe"],
        faq=[
            ("Ist die Vogelgrippe für Menschen gefährlich?", "Ansteckungen von Menschen sind sehr selten. Trotzdem gilt: tote oder kranke Wildvögel nicht anfassen, und wenn es doch passiert ist, gründlich die Hände waschen."),
            ("Wem melde ich einen toten Seevogel?", "Dem Veterinäramt oder Ordnungsamt des Landkreises, in dem der Fundort liegt. Außerhalb der Dienstzeiten kannst du die Polizei verständigen."),
            ("Kann ich einen verölten Vogel retten?", "Bitte nicht selbst. Fasse ihn nicht an und melde den Fund der Polizei, der Nationalparkverwaltung oder dem Veterinäramt. Fachleute entscheiden, ob eine Pflege Aussicht auf Erfolg hat."),
        ],
        sources=[NABU_VOGELGRIPPE, SH_GEFLUEGELPEST, NATIONALPARK],
    ),
    dict(
        slug="strandmuell-sammeln", name="Strandmüll sammeln", photo="basstoelpel",
        title="Strandmüll sammeln: so geht es richtig",
        desc="Müll am Strand sammeln, allein, mit Kindern oder als Gruppe: was du brauchst, was du liegen lässt, wo der Müll hinkommt und wie dein Fund der Forschung hilft.",
        card="Handschuhe, Beutel, offene Augen. Was du liegen lässt und wo der Müll hinkommt.",
        intro="Plastikteile, Schnüre, Flaschendeckel und Zigarettenkippen landen an jedem Strand. Seevögel verheddern sich in Netzresten oder halten Plastik für Futter. Jedes Teil, das du aufhebst, kommt nicht zurück ins Meer. Schon zehn Minuten auf dem Rückweg vom Strandspaziergang helfen.",
        tldr=[("Mitnehmen", "Handschuhe, Beutel, nach Lust eine Greifzange"), ("Liegen lassen", "Spritzen, Kanister mit Inhalt, Munition und bernsteinartige Brocken"),
              ("Wohin damit", "in Strand-Müll-Boxen oder Mülleimer am Strandübergang"), ("Dünen und Ruhezonen", "nicht betreten, auch nicht zum Sammeln")],
        steps=[
            ("Ausrüsten", "Zieh feste Handschuhe an und nimm einen Beutel oder Eimer mit. Eine Greifzange schont den Rücken, mit Kindern reichen Handschuhe."),
            ("Am Spülsaum sammeln", "Geh die Linie aus Tang und Treibgut ab, die das letzte Hochwasser hinterlassen hat. Dort liegt das meiste, auch kleine Plastikteile."),
            ("Auf Wegen bleiben", "Betritt keine Dünen, Salzwiesen oder Ruhezonen des Nationalparks und halte Abstand zu rastenden Vögeln und Robben."),
            ("Gefährliches liegen lassen", "Spritzen, Glasbruch, Kanister mit unbekanntem Inhalt und rostige Metallteile nicht anfassen. Munition oder Verdacht auf Phosphor sofort der Polizei melden."),
            ("Richtig entsorgen", "Wirf den Müll in eine Strand-Müll-Box oder einen Mülleimer am Strandübergang. Größere Mengen kannst du bei der Gemeinde oder Kurverwaltung melden."),
            ("Fund melden", "Schreibst du auf, was du gefunden hast, hilft das der Forschung. Der NABU sammelt die Ergebnisse von Sammelaktionen auf gewässerretter.de."),
        ],
        tips=[
            ("Netzreste besonders wichtig", "Schnüre und Netzreste sind für Seevögel am gefährlichsten. Basstölpel bauen sie in ihre Nester ein und verfangen sich darin."),
            ("Lebendes bleibt da", "Tang, Muschelschalen, Quallen und Krebse gehören zum Strand. Gesammelt wird nur, was der Mensch gemacht hat."),
            ("Gemeinsam sammeln", "Am Küstenputztag im September rufen NABU und andere Verbände an vielen Stränden zum gemeinsamen Sammeln auf. Du kannst auch selbst eine Aktion anmelden."),
            ("Bernstein oder Phosphor?", 'An der Ostsee sehen Phosphorbrocken aus alten Brandbomben wie Bernstein aus und können sich entzünden. Mehr dazu unter <a href="{R}am-strand/index.html#h-phos">Sicher am Strand</a>.'),
        ],
        species=["basstoelpel", "eiderente", "schweinswal"],
        faq=[
            ("Darf ich am Strand Müll sammeln?", "Ja, auf allen öffentlichen Strandabschnitten. In Nationalparks bleibst du dabei auf den erlaubten Flächen und betrittst keine Ruhezonen und Dünen."),
            ("Wohin mit dem gesammelten Müll?", "In die Strand-Müll-Boxen, die es an vielen Stränden gibt, oder in die Mülleimer an den Strandübergängen. So ist sichergestellt, dass er ordentlich entsorgt wird."),
            ("Was mache ich mit Munition oder Phosphor?", "Nicht anfassen, Abstand halten, die Stelle markieren, wenn das gefahrlos geht, und die Polizei verständigen."),
        ],
        sources=[NABU_SAMMELAKTION, NABU_ICCD, NLPV_MUELL],
    ),
    dict(
        slug="spuelsaum-entdecken", name="Spülsaum entdecken mit Kindern", photo="nixentaeschchen",
        title="Spülsaum entdecken mit Kindern",
        desc="Muscheln, Nixentäschchen und Krabben: So wird der Spülsaum zum Entdeckerpfad für Kinder, mit Suchliste, Becherlupe und Regeln, damit alle Tiere heil bleiben.",
        card="Eine Suchliste für den Tangsaum, eine Becherlupe und drei Regeln, damit alle Tiere heil bleiben.",
        intro="Der Spülsaum ist die Linie aus Tang, Schalen und Treibgut, die das Meer am Strand zurücklässt. Für Kinder ist er eine Schatzkiste: leere Muschelschalen, Eikapseln von Rochen, Krebspanzer und mit Glück ein Seestern. Mit einer kleinen Suchliste wird daraus ein Ausflug, bei dem alle etwas lernen und die Tiere heil bleiben.",
        tldr=[("Beste Zeit", "nach auflandigem Wind und bei ablaufendem Wasser"), ("Dabei", "Eimer mit Meerwasser, Becherlupe, Handschuhe für Größere"),
              ("Regel 1", "Lebende Tiere kurz ansehen und genau dorthin zurückbringen"), ("Regel 2", "Quallen und unbekannte Brocken nicht anfassen")],
        steps=[
            ("Richtige Zeit wählen", "Nach einem auflandigen Wind liegt am meisten im Spülsaum. Bei ablaufendem Wasser ist der frische Saum gut zu erreichen."),
            ("Suchliste mitnehmen", "Herzmuschel, Miesmuschel, Wellhornschnecke, Nixentäschchen, Sepiaschale, Strandkrabbe, Blasentang und Seestern: Wer findet die meisten?"),
            ("Lebende Tiere schonend ansehen", "Krabben und Garnelen kurz in einer Becherlupe mit Meerwasser beobachten, nicht in die Sonne stellen und nach wenigen Minuten genau dort zurücksetzen, wo sie waren."),
            ("Bestimmen", "Mit den Fotos im Meereskompass lässt sich fast jeder Fund benennen. Die Suche nach Aussehen hilft, wenn der Name fehlt."),
            ("Nur Leeres mitnehmen", "Leere Schalen und einzelne Steine sind meist in Ordnung. Im Nationalpark gelten die Regeln vor Ort, und Bernsteinfunde kommen in eine Metalldose."),
        ],
        tips=[
            ("Quallen nur ansehen", 'Auch angespülte Quallen können noch nesseln. Welche brennen, steht unter <a href="{R}am-strand/index.html#h-q">Sicher am Strand</a>.'),
            ("Nixentäschchen umdrehen", "Die schwarzen Kapseln mit Hörnchen sind Eihüllen von Rochen. Gegen das Licht gehalten sieht man, ob sie schon leer sind."),
            ("Muscheln mit Loch", "Ein kreisrundes Loch in der Schale stammt meist von einer Raubschnecke. Solche Schalen eignen sich gut für eine Kette."),
            ("Fundstücke nach dem Sturm", 'Im Herbst und Winter bringen Stürme oft besonders viel an Land. Was gerade zu finden ist, zeigt das <a href="{R}strandjahr/index.html">Küstenjahr</a>.'),
        ],
        species=["herzmuschel", "miesmuschel", "wellhornschnecke", "nixentaeschchen", "sepiaschale", "strandkrabbe", "blasentang", "seestern"],
        faq=[
            ("Darf ich Muscheln vom Strand mitnehmen?", "Leere Schalen in kleiner Menge sind meist erlaubt. Lebende Tiere bleiben am Strand. Im Nationalpark gelten zusätzlich die Regeln vor Ort, Ruhezonen sind tabu."),
            ("Ab welchem Alter macht das Spaß?", "Schon kleine Kinder suchen gern Schalen. Ab dem Grundschulalter wird das Bestimmen mit Fotos spannend, und die Suchliste wird zum Wettbewerb."),
            ("Wie lange darf eine Krabbe im Eimer bleiben?", "Nur wenige Minuten, im Schatten und in frischem Meerwasser. Dann geht sie genau dorthin zurück, wo sie gefunden wurde."),
        ],
        sources=[NATIONALPARK],
    ),
    dict(
        slug="seevoegel-nicht-stoeren", name="Vögel beobachten ohne zu stören", photo="alpenstrandlaeufer",
        title="Seevögel beobachten, ohne zu stören",
        desc="Rastende Watvögel, Brutkolonien und Hochwasser-Rastplätze: Wie du Seevögel an Nord- und Ostsee beobachtest, ohne sie aufzuscheuchen, und warum das so wichtig ist.",
        card="Rastplätze bei Hochwasser, Brutzeit, Hunde und Drohnen: so siehst du viel und störst nicht.",
        intro="Watvögel wie Alpenstrandläufer und Knutts fliegen tausende Kilometer und müssen sich im Wattenmeer satt fressen. Bei Hochwasser drängen sie sich auf wenigen trockenen Flächen zusammen. Wird ein Schwarm dort immer wieder aufgescheucht, kostet das Energie, die den Vögeln später auf dem Zug fehlt. Mit etwas Abstand siehst du trotzdem alles.",
        tldr=[("Abstand", "so weit, dass die Vögel ruhig bleiben, mit Fernglas statt nah heran"), ("Hochwasser", "Rastplätze besonders meiden"),
              ("Hunde", "an die Leine, wo Vögel rasten oder brüten"), ("Drohnen", "über Nationalparks und Naturschutzgebieten verboten")],
        steps=[
            ("Fernglas statt Annäherung", "Bleib stehen, sobald Vögel den Kopf heben, unruhig werden oder abrücken. Das ist das Zeichen, dass du nah genug bist."),
            ("Hochwasser-Rastplätze meiden", "Bei Hochwasser sitzen Watvögel dicht gedrängt auf Sandbänken, Spülsäumen und Salzwiesen. Beobachte sie vom Deich oder Weg aus."),
            ("Auf Wegen bleiben", "In der Brutzeit von April bis Juli brüten Austernfischer, Seeschwalben und Regenpfeifer am Boden. Ihre Gelege sind im Sand kaum zu sehen."),
            ("Hund an die Leine", "Ein frei laufender Hund scheucht in Sekunden einen ganzen Schwarm auf. Viele Strände im Nationalpark haben Leinenpflicht."),
            ("Keine Drohne fliegen", "Über Nationalparks und Naturschutzgebieten dürfen Drohnen nicht fliegen. Vögel halten sie für Greifvögel und fliehen."),
        ],
        tips=[
            ("Warnrufe ernst nehmen", "Kreisen Seeschwalben rufend über dir oder stoßen auf dich herab, bist du einem Nest zu nah. Geh ruhig zurück."),
            ("Beste Zeit zum Beobachten", "Zwei bis drei Stunden vor Hochwasser kommen die Vögel nah an die Küste, weil das Watt überflutet wird. Ein ruhiger Platz am Deich ist dann ideal."),
            ("Führungen nutzen", "Ranger und Schutzstationen bieten Vogelführungen an. Dort lernst du die Arten kennen und siehst sie mit Spektiv ganz nah."),
            ("Mitzählen", 'Welche Arten gerade rasten, zeigt das <a href="{R}strandjahr/index.html">Küstenjahr</a>. Zum Bestimmen im Gelände hilft das passende <a href="{R}ratgeber/fernglas/index.html">Fernglas</a>.'),
        ],
        species=["alpenstrandlaeufer", "sanderling", "austernfischer", "ringelgans", "brandgans", "flussseeschwalbe"],
        faq=[
            ("Wie nah darf ich an rastende Vögel heran?", "Eine feste Zahl gibt es nicht. Bleib stehen, sobald die Vögel unruhig werden, und geh dann lieber ein Stück zurück. Mit dem Fernglas siehst du sie aus der Entfernung genauso gut."),
            ("Warum ist Aufscheuchen so schlimm?", "Jedes Auffliegen kostet Energie. Zugvögel brauchen ihre Fettreserven für Flüge von tausenden Kilometern. Wird ein Schwarm oft gestört, kann er sich nicht genug anfressen."),
            ("Darf ich im Nationalpark eine Drohne fliegen?", "Nein. Über Nationalparks und Naturschutzgebieten ist der Betrieb von Drohnen grundsätzlich verboten."),
        ],
        sources=[NATIONALPARK],
    ),
]

# Welche Anleitungen auf welchen Seiten als Block „Helfen an der Küste“ erscheinen (Gruppe → Anleitungen)
TEASERS = {
    "Robben": ["robbe-am-strand", "totfund-melden", "strandmuell-sammeln"],
    "Wale & Delfine": ["totfund-melden", "strandmuell-sammeln", "robbe-am-strand"],
    "Seevögel": ["seevoegel-nicht-stoeren", "seevogel-gefunden", "strandmuell-sammeln"],
    "Muscheln": ["spuelsaum-entdecken", "strandmuell-sammeln", "seevoegel-nicht-stoeren"],
    "Strandfunde": ["spuelsaum-entdecken", "strandmuell-sammeln", "seevogel-gefunden"],
}

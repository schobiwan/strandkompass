# -*- coding: utf-8 -*-
"""Gruppenseiten /arten/<gruppe>/: Titel und Einleitung nach Suchabsicht (z. B. „Quallen Ostsee“, „Robben Nordsee“).

Schlüssel = Gruppenname aus data.GROUPS. Die Karten, Zahlen und Verweise kommen automatisch aus data.py.
"""

GROUP_INFO = {
    "Seevögel": dict(
        title="Seevögel an Nord- und Ostsee bestimmen: Möwen, Watvögel, Enten",
        h1="Seevögel an Nord- und Ostsee",
        desc="Seevögel der deutschen Küste mit Foto, Ruf zum Anhören und Erkennungsmerkmalen: Möwen, Austernfischer, Säbelschnäbler, Eiderente, Basstölpel und mehr.",
        intro=["An der deutschen Küste begegnen dir vor allem Möwen, Watvögel und Meeresenten. Möwen unterscheidest du am besten an Rückenfarbe, Beinen und Schnabel, Watvögel an der Schnabelform und daran, wie sie sich bewegen.",
               "Basstölpel und Trottellumme brüten in Deutschland nur auf Helgoland. Bei fast allen Seevögeln kannst du dir den Ruf anhören."]),
    "Robben": dict(
        title="Robben an Nord- und Ostsee: Seehund und Kegelrobbe erkennen",
        h1="Robben an Nord- und Ostsee",
        desc="Seehund oder Kegelrobbe? Die beiden Robbenarten der deutschen Küste mit Foto, Merkmalen, Vorkommen an Nordsee und Ostsee und Tipps zum Beobachten.",
        intro=["An der deutschen Küste leben zwei Robbenarten: der Seehund und die Kegelrobbe. Seehunde liegen vor allem auf den Sandbänken im Wattenmeer. Kegelrobben, die größten Raubtiere Deutschlands, siehst du auf Helgoland und immer öfter auch an der Ostsee vor Rügen.",
               "Am sichersten unterscheidest du die beiden an der Kopfform: rundlicher Kopf mit kurzer Schnauze beim Seehund, lange, gerade Schnauze bei der Kegelrobbe. Liegt ein junger Seehund allein am Strand, halte Abstand und gib der Seehundstation Bescheid."]),
    "Wale & Delfine": dict(
        title="Wale und Delfine in Nord- und Ostsee: Schweinswal, Tümmler und Co.",
        h1="Wale und Delfine in Nord- und Ostsee",
        desc="Welche Wale und Delfine gibt es in Nordsee und Ostsee? Schweinswal, Großer Tümmler, Weißschnauzendelfin, Zwergwal und seltene Gäste mit Foto und Merkmalen.",
        intro=["Der einzige Wal, der dauerhaft an der deutschen Küste lebt, ist der Schweinswal, ein kleiner Zahnwal von etwa anderthalb Metern Länge. Mit etwas Glück siehst du ihn in der Nordsee und in der westlichen Ostsee vom Strand oder von der Fähre aus.",
               "Große Tümmler, Weißschnauzendelfine und Zwergwale kommen gelegentlich vor. Buckelwale und Pottwale verirren sich nur selten in unsere Meere."]),
    "Muscheln": dict(
        title="Muscheln an Nord- und Ostsee bestimmen: Strandfunde mit Foto",
        h1="Muscheln an Nord- und Ostsee",
        desc="Muscheln am Strand bestimmen: Herzmuschel, Miesmuschel, Sandklaffmuschel, Schwertmuschel, Pazifische Auster und Baltische Plattmuschel mit Foto und Merkmalen.",
        intro=["Am Spülsaum liegen vor allem Schalen von Herzmuscheln, Miesmuscheln und Sandklaffmuscheln. Die Amerikanische Schwertmuschel und die Pazifische Auster sind eingewandert und heute an der Nordsee häufig.",
               "An der Ostsee ist die Baltische Plattmuschel typisch, weil sie mit dem wenig salzigen Wasser gut zurechtkommt. Achte beim Bestimmen auf Form, Rippen und die Farbe der Innenseite."]),
    "Schnecken": dict(
        title="Schnecken am Strand von Nord- und Ostsee bestimmen",
        h1="Schnecken an Nord- und Ostsee",
        desc="Meeresschnecken am Strand erkennen: Gemeine Strandschnecke, Wellhornschnecke und Pantoffelschnecke mit Foto, Merkmalen und Vorkommen.",
        intro=["Die häufigste Schnecke an Steinen und Buhnen ist die Gemeine Strandschnecke. An der Nordsee findest du außerdem die großen Gehäuse der Wellhornschnecke und die flachen Schalen der Pantoffelschnecke, die oft zu kleinen Türmen aufeinandersitzen.",
               "Leere Gehäuse der Wellhornschnecke bewohnen gern Einsiedlerkrebse."]),
    "Quallen": dict(
        title="Quallen in Nord- und Ostsee: Welche brennen?",
        h1="Quallen an Nord- und Ostsee",
        desc="Welche Quallen gibt es in Nordsee und Ostsee und welche brennen? Ohrenqualle, Feuerqualle, Kompassqualle, Blaue Nesselqualle und mehr mit Foto auf einen Blick.",
        intro=["In der Ostsee treiben vor allem Ohrenquallen, die kaum brennen, und im Spätsommer Feuerquallen. Die Nordsee hat mehr Arten: Kompassqualle, Blaue Nesselqualle und die große Lungenqualle kommen dazu.",
               "Auch gestrandete Quallen und abgerissene Tentakel können noch nesseln, also besser nicht anfassen. Die Seestachelbeere ist streng genommen keine Qualle, sondern eine Rippenqualle ohne Nesselzellen."]),
    "Krebse & Würmer": dict(
        title="Krebse und Würmer am Strand: Strandkrabbe, Garnele, Wattwurm",
        h1="Krebse und Würmer an Nord- und Ostsee",
        desc="Strandkrabbe, Einsiedlerkrebs, Nordseegarnele, Seepocke und Wattwurm: Krebse und Würmer im Watt und am Spülsaum mit Foto und Merkmalen.",
        intro=["Im Watt und am Spülsaum leben viele kleine Tiere, die man leicht übersieht. Die Strandkrabbe ist die häufigste Krabbe an Nord- und Ostsee, die Nordseegarnele kennst du als „Krabbe“ vom Fischbrötchen.",
               "Die geringelten Sandhäufchen im Watt stammen vom Wattwurm, der darunter im Boden lebt. Seepocken sind übrigens auch Krebse, obwohl sie eher wie kleine Muscheln aussehen."]),
    "Seesterne & Seeigel": dict(
        title="Seestern und Seeigel am Strand von Nord- und Ostsee",
        h1="Seesterne und Seeigel an Nord- und Ostsee",
        desc="Gemeiner Seestern und Herzigel: Welche Stachelhäuter du am Strand von Nord- und Ostsee findest, mit Foto, Merkmalen und Vorkommen.",
        intro=["Der Gemeine Seestern ist der Seestern, den du an Nord- und Ostsee am ehesten findest, oft nach einem Sturm am Spülsaum. In der salzarmen östlichen Ostsee wird er selten.",
               "Der Herzigel lebt eingegraben im Sand der Nordsee. Am Strand findest du meist nur seine zerbrechliche, weiße Schale ohne Stacheln."]),
    "Tang & Seegras": dict(
        title="Tang und Seegras am Strand: Blasentang, Meersalat, Seegras",
        h1="Tang und Seegras an Nord- und Ostsee",
        desc="Was liegt da grün und braun am Strand? Blasentang, Meersalat und Seegras von Nord- und Ostsee mit Foto und Merkmalen erkennen.",
        intro=["Was am Spülsaum grün und braun liegt, ist meist Tang oder Seegras. Blasentang erkennst du an den luftgefüllten Blasen, Meersalat an den dünnen, hellgrünen Blättern.",
               "Seegras ist keine Alge, sondern eine Blütenpflanze. Es bildet unter Wasser Wiesen, die vielen Fischen und Krebsen als Kinderstube dienen."]),
    "Strandfunde": dict(
        title="Strandfunde an Nord- und Ostsee: Bernstein, Hühnergott und Co.",
        h1="Besondere Strandfunde an Nord- und Ostsee",
        desc="Bernstein, Hühnergott, Donnerkeil, Rochen-Ei, Katzenhai-Ei und Sepiaschale: besondere Strandfunde von Nord- und Ostsee mit Foto erkennen.",
        intro=["Neben Muscheln und Schnecken spült das Meer auch besondere Funde an. An der Ostsee suchen viele nach Bernstein, Hühnergöttern und Donnerkeilen, den versteinerten Resten urzeitlicher Tintenfische. An der Nordsee findest du die schwarzen Eikapseln von Rochen und Katzenhaien und weiße Sepiaschalen.",
               "Vorsicht bei Bernstein: Weißer Phosphor aus alter Munition sieht ihm ähnlich und kann sich auf der Haut entzünden."]),
}

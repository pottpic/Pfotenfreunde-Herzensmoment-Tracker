# Newsletter Weihnachtsaktion 2026 – Aufbau mit CleverReach + erste Ausgaben

**Erstellt:** 29.10.2026 von Postpfote (newsletter)
**Status:** ENTWURF. Nichts eingerichtet, nichts verschickt. Termine, Orte, Preise und Pakete sind **nicht bestätigt**. Platzhalter: [TERMIN], [ORT], [PREIS/PAKET], [BUCHUNGSLINK], dazu [BESTELLFRIST] und [ANMELDELINK].
**Grundlage:** Trend-Report von Witterung (`pottpic-team/trends/2026-10-29-weihnachtsaktion.md`), Planungsentwurf von Fotopfote (`pottpic-team/shooting-planung/2026-10-29-weihnachts-minishootings.md`), CleverReach-Hilfeseiten (Quellen ganz unten).

---

## 0. Ganz kurz vorweg, ehrlich

- **Der Newsletter rettet die Weihnachtsaktion 2026 nicht, er fängt grad erst an.** Die Liste startet bei null. Anmelden dürfen sich nur Leute, die das selbst wollen und per Mail bestätigen (Double-Opt-in). Für die Minis im November macht Instagram also die meiste Arbeit. Der Newsletter ist der Anfang von was, das nächstes Jahr richtig trägt.
- **Bestandskund:innen bitte nicht einfach importieren und anschreiben.** Auch wenn du ihre Mail-Adressen von früheren Shootings hast: Ohne ihre Einwilligung für den Newsletter is das Werbung ohne Erlaubnis. CleverReach fragt außerdem bei der Konto-Prüfung, woher deine Adressen kommen (Quelle 6). Es gibt im Gesetz eine enge Ausnahme für Bestandskund:innen (§ 7 Abs. 3 UWG), aber die hat mehrere Bedingungen, z. B. dass die Leute schon bei der Erfassung der Adresse auf ihr Widerspruchsrecht hingewiesen worden sind. **Das bitte nicht auf eigene Faust machen, sondern prüfen lassen** (Anwält:in oder z. B. IHK-Beratung). Sicherer Weg: Die alten Kund:innen über Instagram, persönlich oder auf deiner Website einladen, sich selbst einzutragen.
- **Rechtliches allgemein:** Alles hier ist keine Rechtsberatung. Impressum, Datenschutzerklärung und Anmeldetexte solltest du einmal prüfen lassen.

---

## 1. CleverReach-Schnellstart (das Minimum für den ersten Versand)

Was ich belegen konnte, steht mit Quelle dabei. Wo ich mir nicht sicher bin, steht **[nicht geprüft]**. Die Menünamen können in deinem Konto etwas anders heißen, weil CleverReach seine Oberfläche ab und zu umbaut.

### Was dich das kostet
- **Lite-Tarif ist kostenlos**, ohne Zeitlimit und ohne Zahlungsdaten: bis **250 Empfänger:innen** und **1.000 Mails pro Monat** (Quelle 1). Für den Start reicht das völlig. Beispiel: 2 Ausgaben im Monat an 250 Leute sind 500 Mails.
- Im Lite-Tarif ist **eine Automatisierung** dabei, das reicht für die Willkommensmail (Quelle 2).
- Im Lite-Tarif sind die Newsletter **nicht werbefrei**, „werbefrei“ gibt’s erst ab Basic (Quelle 2). Heißt vermutlich: Unten steht ein kleiner CleverReach-Hinweis. Wie genau der aussieht, konnte ich nicht nachsehen **[nicht geprüft]**.
- Basic gibt’s laut Suchergebnis ab ca. 15 €/Monat, jährlich im Voraus bezahlt (Quelle 1). Brauchst du jetzt aber nicht.

### Schritt für Schritt

**Schritt 1: Konto anlegen und deine Daten vollständig eintragen (Tag 1, ca. 30 Min)**
1. Auf cleverreach.com kostenlos registrieren (Lite).
2. Unter **Mein Konto › Einstellungen › Meine Daten** alles ausfüllen: Name, Pottpic, Adresse, Telefon. CleverReach schreibt selbst, dass vollständige Angaben die Prüfung deines Kontos schneller machen (Quelle 4).
3. **Wichtig zu wissen:** CleverReach prüft **jedes** neue Konto, bevor du verschicken darfst, und fragt dabei, woher deine Adressen kommen (Quelle 6). Wie lange das dauert, hab ich **nicht** rausgefunden. Deshalb diesen Schritt **sofort** machen, dann läuft die Prüfung, während du den Rest einrichtest. Antwort ehrlich: „Ich fange neu an, alle Adressen kommen über mein Anmeldeformular mit Double-Opt-in.“

**Schritt 2: Impressum für die Mails hinterlegen (Tag 1, 10 Min)**
- Unter **Mein Konto › Einstellungen › E-Mail-Impressum** (englisch „Email Legal Notice“) dein Impressum eintragen: Name, Pottpic, Anschrift, Kontakt-Mail, ggf. Telefon und USt-ID, so wie’s auch auf pottpic.de steht (Quelle 5).
- Ohne vollständiges Impressum darfst du laut CleverReach gar nicht verschicken (Quelle 5). Das Impressum steht dann automatisch unten in jeder Mail.

**Schritt 3: Absender einrichten, mit deiner eigenen Adresse (Tag 1 bis 3)**
- Absender ist **mk@pottpic.de** oder z. B. eine eigene Adresse wie moni@pottpic.de. **Keine** GMX-, Gmail- oder T-Online-Adresse: Das landet laut CleverReach sehr wahrscheinlich im Spam (Quelle 7).
- **DKIM einrichten.** Klingt technisch, is aber nur ein „Echtheits-Stempel“ für deine Mails. CleverReach verlangt das inzwischen für den Versand (Quelle 8). So geht’s (Quelle 8):
  1. In CleverReach: **Einstellungen › DKIM** öffnen, Domain **pottpic.de** eintragen, Schlüssel erzeugen lassen.
  2. CleverReach zeigt dir einen **Text-Eintrag (TXT-Record)**. Den musst du bei dem Anbieter eintragen, bei dem pottpic.de liegt (dein Webhoster, z. B. da, wo du die Domain bezahlst). Wenn du nicht weißt, wie: Den Eintrag an deinen Webhoster-Support oder an den, der deine Website gebaut hat, schicken und sagen „Bitte diesen DKIM-TXT-Eintrag für pottpic.de anlegen.“ Das is für die 5 Minuten Arbeit.
  3. **1–2 Tage warten**, dann in CleverReach auf „Prüfen“ klicken und DKIM aktivieren. Klappt’s nicht, nochmal 24–48 Stunden warten (Quelle 8).
- CleverReach empfiehlt zusätzlich **SPF und DMARC** (auch nur Einträge beim Webhoster, Quelle 8/9). Falls dein Webhoster-Support eh grad dran is: gleich mitmachen lassen. Wenn’s schon einen SPF-Eintrag für pottpic.de gibt (z. B. weil du über deinen Webhoster mailst), darf der **nicht** einfach doppelt angelegt werden, der Support muss den bestehenden ergänzen.
- Übergangslösung: Ohne eigene DKIM-Domain schreibt CleverReach deine Absenderadresse um und nutzt seinen eigenen Schlüssel, das sieht aber weniger nach dir aus und kommt schlechter an (Quelle 8). Also lieber richtig machen.

**Schritt 4: Empfängerliste anlegen (Tag 1, 5 Min)**
- Eine Liste reicht für den Anfang, z. B. **„Pottpic Newsletter“**. Keine Adressen importieren (siehe oben).
- Merk dir: Ein Formular hängt immer an **genau einer** Liste, und das kann man hinterher nicht mehr ändern (Quelle 10). Also erst Liste, dann Formular.

**Schritt 5: Anmeldeformular mit Double-Opt-in bauen (Tag 2, ca. 1 Stunde)**
- Unter **Formulare › Formular hinzufügen** ein neues Formular anlegen und die Liste „Pottpic Newsletter“ auswählen (Quelle 10).
- **Double-Opt-in is bei CleverReach-Formularen immer an**, du musst nix extra einschalten (Quelle 6/11). Heißt: Wer sich einträgt, kriegt erst ’ne Mail mit Bestätigungslink und landet erst nach dem Klick auf deiner Liste. Die Anmeldungen werden automatisch protokolliert, das is dein Nachweis (Quelle 11).
- **Felder:** Nur E-Mail (Pflicht) und Vorname (freiwillig, für „Hey Sabine“). Optional „Name deines Hundes“ (freiwillig). Mehr nicht. Je weniger Felder, desto mehr Leute machen mit.
- **Text überm Formular** (Vorschlag in deiner Stimme): „Ab und zu ’ne Mail von mir: freie Termine, Aktionen und ’n bisschen was aus dem Shooting-Alltag. Kein Spam, versprochen, und abmelden geht mit einem Klick.“
- **Datenschutz-Hinweis unterm Formular:** Kurz sagen, wofür die Adresse genutzt wird, dass CleverReach verschickt, dass man sich jederzeit abmelden kann, und auf deine Datenschutzerklärung verlinken. Wie man den Formular-Hinweis ändert, steht in Quelle 12. **Den genauen Wortlaut bitte prüfen lassen.**
- **Bestätigungsmail (Double-Opt-in-Mail) anpassen** (Quelle 10). Vorschlag:
  > Betreff: Kurz noch bestätigen, dann biste dabei
  > Hey, schön, dass du dich eingetragen hast! Klick bitte einmal auf den Link hier drunter, damit ich weiß, dass du’s wirklich warst. Wenn nicht: einfach ignorieren, dann passiert nix. Moni
- **Bestätigungsseite** (kommt nach dem Klick): „Geschafft, du bist dabei! Gleich kommt noch ’ne kleine Mail von mir.“

**Schritt 6: Formular verteilen (Tag 2)**
- Jedes Formular hat einen **eigenen Link** (unter dem Reiter „Quellcode / Verbreitung“), den du teilen kannst. Zusätzlich kannst du es als **Landingpage** (eigene kleine Seite bei CleverReach) anlegen und den Link kopieren (Quelle 13/14). Das is dein **[ANMELDELINK]** für Link in Bio und Stories.
- **Auf pottpic.de:** Unter demselben Reiter gibt’s Quellcode zum Einbauen in die Website (Quelle 10/13). Wenn das zu fummelig is: Erstmal einfach einen Button „Newsletter“ auf die Website, der auf den Landingpage-Link zeigt. Einbauen kann `umsetzung`.

**Schritt 7: Datenschutzerklärung auf pottpic.de ergänzen (Tag 2–3)**
- Da muss rein, dass du einen Newsletter hast, dass CleverReach verschickt und Öffnungen/Klicks misst (falls du das nutzt), und wie man sich abmeldet. **[nicht geprüft: genauer Text]** Am besten mit deinem Datenschutz-Generator oder deiner Beratung aktualisieren.
- Mit CleverReach brauchst du einen **Vertrag zur Auftragsverarbeitung (AVV)**, weil die deine Kundendaten für dich verarbeiten. Ob und wo CleverReach den im Konto anbietet, konnte ich in dieser Sitzung **nicht nachprüfen**. Bitte im Konto unter Einstellungen danach gucken oder beim CleverReach-Support fragen.

**Schritt 8: Willkommensmail als Automatisierung (Tag 3, optional)**
- Mit der einen Automatisierung im Lite-Tarif (Quelle 2): „Neue:r Empfänger:in in Liste ‚Pottpic Newsletter‘ → Willkommensmail senden“. Wie genau du das im Automations-Editor klickst, hab ich nicht im Detail nachgelesen **[nicht geprüft]**. Wenn’s hakt: Erstmal weglassen, die Willkommensmail kann auch später kommen.

**Schritt 9: Vor jedem Versand**
- Abmeldelink: In den CleverReach-Vorlagen steht er **automatisch** unten im Footer über dem Impressum (Quelle 15). Nicht rauslöschen! Falls doch weg: im Editor über das Klammer-Symbol › Links › Abmeldelink wieder einfügen.
- **Testmail an dich selbst** schicken, am Handy angucken, alle Links einmal anklicken.
- CleverReach lässt dich vor jedem Versand die Anti-Spam-Regeln per Häkchen bestätigen (Quelle 6). Das is normal.
- **Ich verschick nix, du testest und drückst selbst auf Senden.**

### Zeitplan, realistisch
| Wann | Was |
|---|---|
| Do 29.10. / Fr 30.10. | Konto + Meine Daten + Impressum (Konto-Prüfung startet). DKIM-Eintrag an Webhoster schicken. Liste anlegen |
| Sa 31.10. – Mo 02.11. | Formular + Bestätigungsmail + Landingpage. Datenschutzerklärung anpassen. DKIM prüfen |
| Di 03.11. | Anmeldelink in Bio + Website, erste Story (siehe Teil 4) |
| Do 05.11. | Ankündigung auf Instagram (laut Fotopfote), mit Hinweis auf den Newsletter |
| **Fr 06.11.** | **Ausgabe 1 raus, wenn Konto freigeschaltet und DKIM aktiv.** Sonst **Mo 09.11.** (dann noch vor Buchungsschluss WE 1 am Di 10.11. laut Fotopfote) |
| **Mo 30.11.** | **Ausgabe 2 raus** (Tag nach dem 1. Advent) |

Unsicher ist vor allem die Konto-Prüfung bei CleverReach. Dazu hab ich keine Dauer gefunden. Wenn bis Mi 04.11. nix kommt: beim CleverReach-Support nachfragen.

---

## 2. Willkommensmail (für neue Anmeldungen)

**Betreff:** Schön, dass du da bist (und dein Hund natürlich auch)
**Vorschautext:** Kurz zu mir, und was du von mir kriegst. Is nicht viel, versprochen.

> Hey {Vorname, sonst „du“},
>
> schön, dass du dich eingetragen hast. Ich bin Moni von Pottpic, ich fotografier Hunde hier im Ruhrgebiet, und zwar so, wie sie halt sind. Mit schiefem Ohr, mit Sabber, mit Matschpfoten. Ich mein, genau das is ja das, was du später vermisst.
>
> Was du von mir kriegst? Ab und zu ’ne Mail, nicht jede Woche, eher so ein-, zweimal im Monat. Drin stehen freie Termine, Aktionen wie grade die Weihnachts-Minis, ’n paar Einblicke hinter die Kamera und ab und zu ’n Tipp für deinen Alltag mit Hund. Und was es Neues gibt bei der Derner Schnauzenbande und den Pfotenfreunden.
>
> Eine Bitte hätt ich: Antworte doch einfach auf diese Mail und erzähl mir kurz, wer bei dir wohnt. Name, Alter, größter Spleen. Ich les das wirklich, und dann weiß ich auch, für wen ich hier eigentlich schreibe.
>
> Bis bald,
> Moni
>
> PS: Damit meine Mails nicht im Spam landen, zieh mich gern einmal in deinen Posteingang oder speicher mk@pottpic.de als Kontakt.

**Bildidee:** Ein echtes Foto von dir mit Kamera und Hund (z. B. Luke), gern ’n bisschen schief und lachend, kein Studio-Porträt.
**Hinweis:** Das Antworten auf die Mail is gleichzeitig gut für die Zustellbarkeit und für deine Themenideen.

---

## 3. Zwei fertige Ausgaben

### Ausgabe 1: Weihnachts-Minis + Produkte (Versand Fr 06.11., Ausweich Mo 09.11.)

**Betreff, 3 Varianten:**
1. Was dein Hund sich zu Weihnachten wünscht (Spoiler: ’ne alte Socke)
2. Weihnachts-Minis 2026: kurz, entspannt, mit Matschpfoten
3. 20 Minuten, ein Hund, und ’n Bild, das bleibt

**Vorschautext:** Ich mach dieses Jahr Weihnachts-Minis. Hier steht, wann, wo und was du am Ende in der Hand hast.

**Text:**

> Hey {Vorname},
>
> ich hab Luke neulich gefragt, was er sich zu Weihnachten wünscht. Okay, er hat nicht geantwortet. Aber wenn ich so guck, was er den ganzen Tag macht, steht auf seinem Wunschzettel: ’ne alte Socke, der Platz auf dem Sofa, auf dem eigentlich ich sitzen wollte, und die eine Pfütze am Ende vom Feldweg. Mehr braucht der nicht, weißt du.
>
> Und ich? Ich wünsch mir eigentlich nur ’n Foto davon, wie er halt einfach is.
>
> Genau deswegen mach ich dieses Jahr **Weihnachts-Minis**.
>
> **Was is das?**
> Ein kurzes Shooting, ca. 20 Minuten, für dich und deinen Hund. Klingt kurz, is aber für die meisten Hunde genau richtig. Wir machen Schnüffelpause, keiner muss stillsitzen, und wenn dein Hund keinen Bock auf Mütze hat, kriegt er halt keine. Gern bringst du sein Lieblingsding mit, die Socke, das zerkaute Kuscheltier, egal. Das sind am Ende oft die schönsten Bilder.
>
> **Wann und wo?**
> [TERMIN] · [ORT]
> Die Plätze pro Tag sind halt begrenzt, weil zwischen den Hunden immer Luft bleiben soll.
>
> **Was hast du am Ende in der Hand?**
> Aus deinen Bildern machen wir was, das unter’n Baum passt:
> - was Kleines, z. B. Weihnachtskarten oder ’n Anhänger für den Baum, perfekt für Oma, Patentante und so
> - was zum Durchblättern, ’n Kalender
> - oder das große Ding: ’n Wandbild, das bleibt
>
> [PREIS/PAKET – z. B. was im Mini enthalten is und was ab welchem Betrag dazukommt]
>
> **Wichtig, weil Weihnachten nicht wartet:** Das Labor braucht seine Zeit. Damit alles rechtzeitig bei dir is, gibt’s nach dem Shooting eine feste Frist, bis wann du deine Lieblinge aussuchst. Die sag ich dir bei der Buchung.
>
> **[Hier buchst du deinen Platz → BUCHUNGSLINK]**
>
> Wenn du unsicher bist, ob dein Hund sowas mitmacht, schreib mir einfach. Ängstlich, alt, Welpe, zu wild, das kriegen wir alles hin. Ich mein, ich hab schon Hunde fotografiert, die die ganze Zeit nur auf Frauchens Schoß saßen, und das waren am Ende mit die schönsten Bilder.
>
> Bis bald,
> Moni

**Bildideen:**
- **Oben:** Bild vom „Probe-Shooting“ mit Luke (Idee von Witterung): Kranz-Versuch, gern der Fail mit Kopf daneben, oder Luke mit seiner Socke vor Lichterketten-Bokeh.
- **Mitte:** Kleine Reihe mit echten Produktmustern (Karte, Anhänger, Kalender, Wandbild), selbst fotografiert, kein Mockup. Falls noch keine Muster da: weglassen statt Mockup.
- Bilder erstellt `umsetzung`. Bitte keine Kundenfotos ohne Okay der Hundemenschen verwenden.

**Einladung am Ende:** Ein großer Button „Platz buchen“ → [BUCHUNGSLINK]. Sonst keine weiteren Links, außer dem Abmeldelink im Footer.

**Was Moni vorher füllen muss:** [TERMIN], [ORT], [PREIS/PAKET], [BUCHUNGSLINK]. Produktliste an das anpassen, was du wirklich anbietest (Anhänger/Ornament, Kalender usw. sind bisher nur Vorschläge aus dem Trend-Report).

---

### Ausgabe 2: Bestell-Deadline, letzte Chance (Versand Mo 30.11.)

**Hauptthema:** Bis [BESTELLFRIST] bestellen, dann liegt’s unterm Baum.

**Achtung, Abgrenzung:** Fotopfote plant am **01.12.** eine persönliche Erinnerung an alle Mini-Kund:innen wegen ihrer Auswahlfrist. Die gehört **nicht** in den Newsletter (sonst kriegen die Leute’s doppelt, und nicht alle Kund:innen sind im Newsletter). Ausgabe 2 geht an alle auf der Liste und ist allgemeiner. Wer im Mini war, kriegt zusätzlich die persönliche Mail.

**Offene Entscheidung für dich:** Was kann jemand, der **nicht** im Mini war, Ende November noch bestellen? Mögliche Varianten (du entscheidest, ich hab nix davon festgelegt):
- (A) Restplätze / späte Termine, falls du die anbietest
- (B) Produkte aus Bildern von **früheren** Shootings bei dir
- (C) Shooting-Gutschein fürs Frühjahr zum Verschenken
Ich hab den Text so geschrieben, dass du die passenden Blöcke drinlässt und den Rest löschst.

**Betreff, 3 Varianten:**
1. Noch bis [BESTELLFRIST], dann liegt’s unterm Baum
2. Kurz und ehrlich: Das Labor wartet nicht auf uns
3. Letzte Chance für dein Hundegeschenk (diesmal wirklich)

**Vorschautext:** Damit dein Hund rechtzeitig an der Wand hängt: Bis wann du bestellen musst und was noch geht.

**Text:**

> Hey {Vorname},
>
> gestern war 1. Advent, und bei mir sieht’s grad so aus: Rechner an, Tee kalt, und ganz viele Hundegesichter auf dem Bildschirm. Die Weihnachts-Minis sind durch, und ehrlich, ich bin immer noch ganz geflasht. [OPTIONAL: Ein konkreter Moment aus den Minis, z. B. „Frieda, 11 Jahre, null Bock auf Mütze. Hat sie auch nicht gekriegt. Und das Bild mit ihrer grauen Schnauze vorm Kranz, also… ich sag nix.“ Nur mit Okay der Hundemenschen.]
>
> Jetzt kommt der unromantische Teil, sorry: **Das Labor hat ’n Bestellschluss.** Damit alles noch vor Weihnachten bei dir is, muss deine Bestellung bis **[BESTELLFRIST]** bei mir sein. Danach kann ich’s leider nicht mehr versprechen.
>
> **Du warst bei den Minis dabei?**
> Dann guck nochmal in deine Galerie. Karte, Anhänger, Kalender, Wandbild, was immer du dir vorgenommen hast: jetzt is der Moment. [PREIS/PAKET]
>
> [BLOCK A, nur wenn’s Restplätze gibt:]
> **Du hast’s nicht geschafft, willst aber noch?**
> Ich hab noch [ANZAHL] Plätze am [TERMIN] in [ORT]. Is knapp, aber machbar. → [BUCHUNGSLINK]
>
> [BLOCK B, nur wenn du das anbietest:]
> **Du hattest schon mal ’n Shooting bei mir?**
> Dann kannst du auch aus deinen älteren Bildern noch was bestellen. Schreib mir einfach, welches Bild, und ich kümmer mich drum.
>
> [BLOCK C, nur wenn du das anbietest:]
> **Du suchst noch was für ’n Hundemenschen in deinem Leben?**
> Verschenk ’n Shooting. Gutschein kommt rechtzeitig, das Shooting machen wir dann im Frühjahr, wenn’s wieder hell is. [PREIS/PAKET]
>
> Und wenn du einfach nur mitlesen wolltest: Auch schön. Lass deinem Hund ’n schönen Advent, mit Socke und Sofa und allem.
>
> Moni
>
> PS: Wenn ihr euer Paket auspackt und ihr Lust habt, das kurz zu filmen, schick’s mir gern. Ich würd’s im Dezember (nur mit eurem Okay) zeigen.

**Bildideen:**
- **Oben:** Ein Lieblingsbild aus den Minis, nur mit ausdrücklichem Okay der Hundemenschen. Alternativ Luke.
- **Mitte:** Ein fertiges Produkt im echten Leben, z. B. Karte auf’m Küchentisch, Wandbild an der Wand. Muster selbst fotografieren.
- Optional kleines Element mit der Frist groß drauf (z. B. „Bestellen bis [BESTELLFRIST]“). Grafik über `umsetzung`.

**Einladung am Ende:** Ein Button, je nach Variante: „Zur Galerie“ (Mini-Kund:innen haben ihren eigenen Link, im Newsletter also eher „Antworte mir einfach“) **oder** „Platz buchen“ → [BUCHUNGSLINK] **oder** „Gutschein anfragen“. Bitte nur **einen** Haupt-Button, sonst weiß keiner, wohin.

**Was Moni vorher füllen muss:** [BESTELLFRIST] (aus deinem Labor-Bestellschluss, Fotopfote plant intern mit Sa 05.12. als letztem Labor-Tag, das is aber nur eine Annahme), Blöcke A/B/C entscheiden, [PREIS/PAKET], ggf. [ANZAHL], [TERMIN], [ORT], [BUCHUNGSLINK].

---

## 4. Erste Anmeldungen kriegen (klein und realistisch)

Ehrliche Erwartung: Im ersten Monat wird die Liste klein sein. Zahl kann ich nicht seriös schätzen, eher „ein paar Dutzend“ als „ein paar Hundert“ **(Schätzung, keine Daten)**. Das is okay. Lieber 30 Leute, die deine Mails wirklich lesen.

**Kleiner Anreiz, der nix kostet:** „Wer im Newsletter is, erfährt’s zuerst.“ Also z. B. neue Termine oder Restplätze 24 Stunden vor Instagram. Das musst du dann aber auch wirklich so machen. Rabatt als Anreiz würd ich erst festlegen, wenn die Preise stehen (du entscheidest).

1. **Link in Bio + Story mit Link-Sticker (ab Di 03.11.)**
   Story-Text: „Ich starte ’nen Newsletter. Nicht oft, nicht nervig. Wer drin is, hört von freien Weihnachts-Plätzen zuerst.“ Link-Sticker auf [ANMELDELINK]. Die Story nach der Ankündigung am 05.11. einmal wiederholen.
2. **Im Ankündigungs-Post und im Probe-Shooting-Reel** (Bellfluencerin/`social-media`): letzter Satz „Newsletter-Link in Bio, da gibt’s Restplätze zuerst.“
3. **pottpic.de:** Button „Newsletter“ im Menü oder Footer und auf der Kontaktseite. Baut `umsetzung`.
4. **Am Shooting-Tag:** Kleines Aufsteller-Kärtchen mit QR-Code zum [ANMELDELINK] am Set oder am Treffpunkt („Für Restplätze und Termine: hier eintragen“). Die Leute tragen sich **selbst** am Handy ein, du schreibst keine Adressen auf. Kommt mit auf Fotopfotes Packliste.
5. **In der Galerie-Mail nach dem Shooting:** Ein Satz mit Link „Wenn du hören willst, wann’s wieder Termine gibt, trag dich hier ein“. Nur Einladung, **kein automatisches Eintragen** der Kund:innen.
6. **Derner Schnauzenbande:** Nur mit Okay des Vereins: QR-Kärtchen im Vereinsheim oder kurzer Hinweis in der Vereinsgruppe. Keine Vereins-Mailliste für Pottpic nutzen.
7. **Herzensmoment-Tracker:** Später ein kleiner Hinweis/Link „Newsletter von Pottpic“ im Tracker. Das is ’ne Idee für `umsetzung`, ich hab am Tracker nix geändert.
8. **Wenn dir alte Kund:innen sowieso grad schreiben** (Insta-DM, Mail): ganz natürlich den Link mitschicken, „falls du willst“. **Keine Rundmail an alle alten Kund:innen**, auch keine „Willst du in meinen Newsletter?“-Mail. Auch so ’ne Mail kann schon als Werbung zählen (prüfen lassen).

---

## 5. Offene Fragen an Moni

1. Wo liegt pottpic.de (welcher Webhoster), und wer kann dort den DKIM-Eintrag anlegen?
2. Welche Absenderadresse willst du: mk@pottpic.de oder eine eigene (z. B. moni@pottpic.de)? Antworten sollten bei dir ankommen.
3. Gibt’s auf pottpic.de schon eine Datenschutzerklärung, die du selbst anpassen kannst (Generator?), oder macht das jemand für dich?
4. Ausgabe 2: Welche Blöcke (A Restplätze, B ältere Shootings, C Gutschein) gibt’s wirklich?
5. Anreiz „Newsletter erfährt’s zuerst“: okay für dich?
6. Willkommensmail gleich als Automatisierung oder erstmal ohne?

---

## Quellen (Suchergebnisse vom 29.10.2026; die Seiten selbst konnte ich in dieser Sitzung nicht öffnen, cleverreach.com war für Direktabrufe gesperrt. Ich kenne die Inhalte nur aus den Suchzusammenfassungen.)

1. CleverReach Preise: https://www.cleverreach.com/en/plans-and-pricing/ · https://support.cleverreach.com/hc/en-us/articles/115001183694-CleverReach-pricing-in-detail
2. Tarife im Detail (Lite: 1 Automatisierung, nicht werbefrei): https://support.cleverreach.com/hc/en-us/articles/20859150858642-Our-plans-and-pricings-in-detail · https://support.cleverreach.com/hc/en-us/articles/202372631-CleverReach-plans-Overview
3. Erste Schritte: https://support.cleverreach.com/hc/en-us/articles/19259782054674-First-steps-with-CleverReach
4. Kontodaten: https://support.cleverreach.com/hc/en-us/articles/202402882-Updating-user-information-in-your-account
5. Impressum: https://support.cleverreach.com/hc/en-us/articles/202403052-Adapting-and-adding-the-legal-notice-imprint · https://support.cleverreach.com/hc/en-us/articles/202372561-Legal-information-in-your-emails
6. Richtlinien Verteilerlisten / Kontoprüfung: https://support.cleverreach.com/hc/en-us/articles/202372671-Our-guidelines-for-using-distribution-lists
7. Absenderadresse: https://support.cleverreach.com/hc/de/articles/360014099454-Absenderadresse
8. DKIM: https://support.cleverreach.com/hc/en-us/articles/360016467539-Set-up-DKIM · https://www.cleverreach.com/en/push-magazin/email-marketing-tips/newsletter-trends/dkim-2024/
9. SPF: https://support.cleverreach.com/hc/en-us/articles/202372691-Does-CleverReach-support-SPF
10. Formulare Übersicht: https://support.cleverreach.com/hc/en-us/articles/202373311-Forms-for-newsletters-overview
11. Double-Opt-in-Formulare: https://www.cleverreach.com/en/newsletter-tool/managing-newsletter-recipients/double-opt-in-signup-forms-for-newsletters/
12. Formular-Hinweistext ändern: https://support.cleverreach.com/hc/en-us/articles/202543592-How-do-I-change-the-legal-notice-in-a-form
13. Landingpage: https://support.cleverreach.com/hc/en-us/articles/20594472647186-Create-and-edit-landing-page
14. Formulare kreativ nutzen: https://www.cleverreach.com/en/push-magazin/newsletter-subscription/win-new-email-subscribers-use-legally-compliant-signup-forms-creatively/
15. Abmeldelink: https://support.cleverreach.com/hc/en-us/articles/202373331-Newsletter-Editor-Insert-unsubscribe-link
16. DSGVO-Checkliste von CleverReach (Herstellermaterial, keine Rechtsberatung): https://www.cleverreach.com/wp-content/uploads/2024/08/cleverreach-dsgvo-checkliste-n-1.pdf

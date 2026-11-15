# Kundenmagnet Weihnachten: aus „tolle Bilder!“ wird Geld

Stand: So 15.11.2026 (abends überarbeitet) · Leitwolf · **Entwurf. Nichts gepostet, nichts eingeplant, nichts verschickt.**

**Was gilt (Monis Entscheidungen vom 15.11.):**
- Verkauft werden **nur Gutscheine**: „Kleines Glück“ 99 € und „Herzensmoment“ 189 €, auf Nachfrage Wertgutschein ab 50 €. **Preise freigegeben.**
- Geshootet wird **ab Frühjahr 2027**, Termin sucht man sich zusammen mit Moni aus.
- **Keine Mini-Termine, keine Platzzahl.** Nur ein Satz für Leute, die ihre Bilder noch vor Weihnachten wollen: *„Du willst deine Bilder noch vor Weihnachten? Schreib mir einfach, vormittags geht im Dezember noch etwas.“* Moni entscheidet pro Anfrage.
- Alles läuft über **WhatsApp 0176 21681512**. Die QR-Codes auf Aushang und Karten öffnen WhatsApp mit fertiger Nachricht, inklusive Herkunft.
- Aushang hängt auch bei der **Derner Schnauzenbande** (eigener QR-Code, Werbung dort mit Moni geklärt).

---

## 0. Erst einmal das Wichtigste, Moni

Dass alle „wow, tolle Bilder“ sagen und keiner liked oder bucht, heißt **nicht**, dass deine Bilder nichts taugen. Das heißt etwas anderes:

1. **Loben kostet nichts, ein Like ist öffentlich, Kaufen kostet Geld.** Das sind drei verschiedene Schritte. Viele bleiben beim ersten stehen, weil ihnen keiner sagt, was der nächste Schritt ist.
2. **Bisher gab es keinen nächsten Schritt.** Kein Angebot mit Preis, kein Knopf, kein QR-Code. Wer begeistert war, wusste schlicht nicht, wohin damit. Das ist jetzt behoben.
3. **Instagram zeigt deine Posts nur einem Teil deiner Follower.** Wenig Likes heißt oft: wenig Leute haben es überhaupt gesehen. Nicht: Leute fanden es doof.
4. **Viele, die dich loben, sind Freunde, Bekannte, andere Fotograf:innen.** Die meinen das ehrlich, aber die kaufen nicht. Deine Kund:innen sind deren Schwester, deren Kollegin, die Frau aus der Hundeschule. An die kommst du über Empfehlung, Aushänge und Gutscheine. Dafür brauchst du keine Reichweite.

**Ab jetzt zählen wir keine Herzchen mehr, sondern Gespräche.** Ein Post mit 9 Likes, der 2 WhatsApps bringt, ist besser als einer mit 90 Likes und null Nachrichten. Dein Zähler steht in Abschnitt 6.

---

## 1. So läuft es

```
Aushang / Karte (QR)  ─┐
Insta-Post / Story    ─┼──►  WhatsApp an dich, Nachricht ist schon vorgeschrieben
Bio-Link              ─┤        (inkl. „ich habe deinen Aushang bei … gesehen“)
persönliche Nachricht ─┘                          │
                                 Du antwortest, schickst Rechnung (Überweisung/PayPal)
                                                  │
                         Gutschein-PDF raus (angebot/gutschein.html)
                                                  │
                         Shooting ab Frühjahr 2027 → Bilder → Bitte um Empfehlung
                                                  │
                                            neue Leute
```

Der **schnellste Weg zu Geld ohne Reichweite**: dein WhatsApp-Status. Den sehen alle mit deiner Nummer, ganz ohne Algorithmus. Bilder und Texte: `2026-11-15-ohne-reichweite.md`.

---

## 2. Was fertig ist

| Was | Datei | Was es macht |
|---|---|---|
| **Aushang A4** | `angebot/aushang.html` | Großer QR-Code, beide Gutscheine mit Preis, Dezember-Satz, Nummer als Text, unten 8 Abreißzettel mit QR |
| **Aushang Derner Schnauzenbande** | `angebot/aushang.html?wo=derner-schnauzenbande` | Wie oben, aber die WhatsApp sagt „…Aushang bei Derner Schnauzenbande…“ |
| **Karten zum Auslegen** | `angebot/karten.html` | 8 Karten pro A4-Blatt zum Ausschneiden, mit QR und Nummer. Am besten auf dickem Papier |
| **Gutschein zum Ausdrucken** | `angebot/gutschein.html` | Name, Paket, Nummer eintippen → „Als PDF speichern“ → nach Zahlungseingang verschicken |
| **QR-Codes** | `angebot/qr/` | `aushang`, `karte`, `derner-schnauzenbande` als SVG und PNG, alle geprüft. Neuer Code pro Laden: `python3 angebot/qr/qr_machen.py hundeschule-xy` |
| **Angebotsseite** | `angebot/index.html` | Gutscheine, Dezember-Kasten, FAQ (auch für ängstliche Hunde), WhatsApp-Knöpfe. Braucht GitHub Pages, um online zu sein. **Für Aushänge nicht nötig.** |

Alles zum Ändern (Preise, Nummer, „ab Frühjahr“, Dezember-Satz) steht in **`angebot/konfig.js`** und gilt für Seite, Aushang und Karten gleichzeitig.

**Fertige WhatsApp-Links zum Kopieren** (z. B. für Bio, Story-Link-Sticker, Facebook):
- Instagram: `https://wa.me/4917621681512?text=Hey%20Moni%2C%20ich%20habe%20dich%20auf%20Instagram%20gesehen%20und%20m%C3%B6chte%20mehr%20%C3%BCber%20den%20Gutschein%20wissen%21`
- Facebook: `https://wa.me/4917621681512?text=Hey%20Moni%2C%20ich%20habe%20dich%20auf%20Facebook%20gesehen%20und%20m%C3%B6chte%20mehr%20%C3%BCber%20den%20Gutschein%20wissen%21`

So steht auch bei Insta und Facebook in der Nachricht, woher die Leute kommen.

---

## 3. Preise (✅ freigegeben am 15.11.2026)

| Gutschein | Preis | Inhalt |
|---|---|---|
| **„Kleines Glück“** | **99 €** | 30 Min Shooting, 5 bearbeitete Lieblingsbilder als Datei, Gutschein-PDF |
| **„Herzensmoment“** | **189 €** | 60 Min Shooting am Lieblingsort, 12 bearbeitete Lieblingsbilder als Datei, gern mit Mensch, Gutschein-PDF |
| Wertgutschein (nur auf Nachfrage) | ab 50 € | für Leute, denen 99 € als Geschenk zu viel sind, oder zum Zusammenlegen |

Gültig bis 31.12.2027. Shooting ab Frühjahr 2027. Du bist Kleinunternehmerin, darum steht nirgends Umsatzsteuer.

**Warum Gutscheine statt Mini-Termine:** Das Geld kommt trotzdem jetzt rein, du kannst bis Heiligabend verkaufen statt nur bis Anfang Dezember, und du hast keinen Stress mit Dezember-Licht, Regen und Bearbeiten unter Zeitdruck. Im Frühling gibt es schöneres Licht, und die Bilder sind gleich Werbung für die nächste Runde.

**Woher die Preise kommen:** Der einzige echte Vergleich, den wir haben: Herzensblick (Dortmund) nimmt laut Suchergebnis 150 € fürs Shooting plus 35 € je Bild (Markt-Check vom 30.10.). Für 5 Bilder wären das dort 325 €. Die 99 € sind also bewusst ein Einstiegspreis, kein Marktwert. Später kannst du hochgehen.

**Offen, entscheidest du pro Anfrage:** Was ein Dezember-Shooting kostet. Naheliegend wär der Preis von „Kleines Glück“ (99 €), aber das ist nur eine Idee.

---

## 4. Texte zum Rauskopieren

### 4A. Antwort auf Lob-Kommentare (öffentlich, kurz)
> Danke dir, echt! 🤎 Falls du mal Bilder von deinem Hund willst oder wem eins schenken magst: Ich habe gerade Shooting-Gutscheine, alles über den Link in meiner Bio.

### 4B. DM, wenn jemand „GUTSCHEIN“ kommentiert
> Hey, schön, dass du dich meldest! 🐾
> Also, es gibt zwei Gutscheine: „Kleines Glück“ mit 30 Minuten Shooting und 5 Lieblingsbildern für 99 €, und „Herzensmoment“ mit einer ganzen Stunde und 12 Bildern für 189 €. Geshootet wird ab Frühjahr, den Termin sucht ihr euch dann mit mir aus.
> Der Gutschein kommt als hübsches PDF zum Ausdrucken, liegt also pünktlich unterm Baum.
> Schreib mir einfach, welcher es sein soll und für wen, dann schicke ich dir alles. Oder direkt per WhatsApp: 0176 21681512

### 4C. ~~20-Leute-Liste~~ → ersetzt
Gibt es nicht (Moni hat keine Liste, im Verein läuft gerade das Adventsshooting beim Pfotenzauber). Stattdessen: **WhatsApp-Status, Pottpic-Seite auf Facebook, Homepage** mit fertigen Bildern und Texten in `2026-11-15-ohne-reichweite.md`.

### 4D. Nachfassen (ca. 3 Tage später, nur 1×)
> Hey, nur kurz, damit es nicht untergeht: Wenn du einen Gutschein noch vor Weihnachten haben willst, sag mir einfach bis [DATUM – legst du fest] Bescheid. Kein Druck, ich wollte es nur gesagt haben. 🐾

### 4E. Wenn jemand sagt „ist mir gerade zu teuer“
> Versteh ich total. Es gibt auch einen Wertgutschein ab 50 €, den kann man z. B. von der Familie zusammenlegen lassen. Und sonst bist du einfach nächstes Jahr dabei. 🤎

### 4F. Wenn jemand die Bilder noch vor Weihnachten will
> Oh, das bekommen wir vielleicht noch hin! Im Dezember geht es bei mir nur vormittags, weil es ja so früh dunkel wird. Wann könntest du denn? Dann schaue ich, ob es passt, und sage dir alles Weitere.

### 4G. Wenn der Gutschein bezahlt ist (mit dem PDF)
> Juhu, danke dir! 🎁 Hier ist der Gutschein zum Ausdrucken. Wer ihn bekommt, meldet sich einfach bei mir, dann suchen wir zusammen einen Termin im Frühjahr. Ich freue mich jetzt schon auf den Hund!

### 4H. Nach dem Shooting im Frühjahr (wenn die Bilder raus sind)
> Ich hoffe, du hast genauso viel Spaß mit den Bildern wie ich beim Bearbeiten! Wenn es dir gefallen hat, würdest du mir einen riesen Gefallen tun: Teil ein Bild und markier @pottpic, oder sag es einer Freundin mit Hund weiter. Davon lebt so ein kleines Fotografinnen-Business wirklich. 🐾

---

## 5. Post-Plan bis Weihnachten (Vorschlag)

Jeder Pottpic-Post bekommt **#esbeginntmiteinemwau**. Erst nach deinem „passt“ wird was eingeplant. Metricool hängt laut letzter Prüfung (12.11.) noch an keinem Netzwerk, da musst du einmal Instagram verbinden, sonst kann ich nichts einplanen.

| Tag | Was | Wofür |
|---|---|---|
| **vorher** | Bio-Link auf den WhatsApp-Link (Instagram) aus Abschnitt 2 stellen | Ohne Link läuft nichts |
| **Mi 18.11.** | Karussell: 3 deiner Lieblingsbilder, „Welches soll auf meinen Gutschein? 1, 2 oder 3?“ | Super einfacher Kommentar, wärmt das Konto auf |
| **Fr 20.11.** | Haupt-Post: Gutscheine (Karussell: Foto → beide Gutscheine → So läuft es) | CTA: „Schreib GUTSCHEIN in die Kommentare“ |
| **So 22.11.** | Story: Umfrage „Wem würdest du ein Hundeshooting schenken? Mama / Schwester / Freundin / Mir selbst 😄“ + Link-Sticker | Wer abstimmt, bekommt 4B per DM |
| **Di 24.11.** | Reel: Luke als Testhund, „So läuft ein Shooting bei mir“ (Quatsch und Pannen erlaubt) | Zeigt, dass es locker ist. Hilft Unsicheren |
| **Do 26.11.** | Post: „Für die Person, die schon alles hat …“ + „Markier wen“ | Gutschein-Verkauf übers Markieren |
| Sa 28.11. | nichts für Pottpic (Pfotenzauber vom Verein) | Luft holen |
| **Di 01.12.** | Story: „Du willst deine Bilder noch vor Weihnachten? Schreib mir, vormittags geht noch etwas.“ | Für die, die selbst Bilder wollen |
| **Do 03.12.** | Post: So sieht der Gutschein aus (Foto vom ausgedruckten Gutschein, z. B. mit Luke daneben) | Macht es greifbar |
| **Di 08.12.** | Story: Fragensticker „Frag mich alles zum Shooting“ | Nimmt Unsicherheit raus |
| **Mo 14.12. / Fr 18.12. / Mo 21.12.** | „Last-Minute-Geschenk: Gutschein kommt als PDF“ | Bis wann du PDFs rausschickst, legst du fest |

Falls „Echt jetzt!“ am 30.11. startet: Das läuft montags 18 Uhr, Gutschein-Posts dann lieber mittags.

### Caption Karussell (Mi 18.11.)
> Ich brauche mal kurz eure Hilfe. Ich mache gerade Gutscheine fertig, und ich kann mich echt nicht entscheiden, welches Bild drauf soll. 🙈
>
> 1, 2 oder 3? Schreibt es mir in die Kommentare, ich nehme das mit den meisten Stimmen.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #dortmund #hundeliebe

### Caption Haupt-Post (Fr 20.11.)
> Ich meine, Fotos vom Hund hast du ja. Tausend Stück wahrscheinlich. Aber wie viele, wo er nicht gerade wegschaut, und wo du auch mal mit drauf bist? 😄
>
> Darum gibt es jetzt meine Shooting-Gutscheine. „Kleines Glück“ mit 30 Minuten und 5 Lieblingsbildern für 99 €, oder „Herzensmoment“ mit einer ganzen Stunde und 12 Bildern für 189 €. Geshootet wird im Frühjahr, wenn es wieder grün ist und hell, den Termin sucht ihr euch aus.
>
> Kommt als hübsches PDF zum Ausdrucken, liegt also pünktlich unterm Baum. 🎁
>
> Schreib **GUTSCHEIN** in die Kommentare, dann schicke ich dir alles. Oder direkt über den Link in meiner Bio.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #dortmund #hundeshooting #weihnachtsgeschenk #gutschein #hundeliebe

### Caption Reel mit Luke (Di 24.11.)
> So läuft ein Shooting bei mir. Also eigentlich. Luke hatte da so seine eigenen Vorstellungen. 😅
>
> Aber genau so soll es sein: Hunde dürfen Hunde sein, und die schönsten Bilder kommen sowieso meistens zwischendurch.
>
> Wenn du das deinem Lieblingsmenschen mit Hund schenken willst: Gutscheine gibt es über den Link in der Bio.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #hundeshooting #labrador #weihnachtsgeschenk

### Caption Gutschein-Post (Do 26.11.)
> Du kennst bestimmt auch so jemanden. Hat eigentlich alles, will nichts, sagt jedes Jahr „ach, schenk mir nichts“. Aber der Hund ist das Allerwichtigste. 🤎
>
> Dann schenk doch ein Shooting. Kommt als hübscher Gutschein zum Ausdrucken, und geshootet wird im Frühjahr, wann es passt.
>
> Markier mal die Person, die das braucht. 👇 Alles Weitere über den Link in der Bio.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #weihnachtsgeschenk #geschenkidee #hundemenschen

### Caption „So sieht der Gutschein aus“ (Do 03.12.)
> Falls du dich gefragt hast, wie so ein Gutschein von mir eigentlich aussieht: so! 🎁
>
> Kommt als PDF, du druckst ihn aus, Schleife drum, fertig. Luke findet, er sieht gut aus. Aber Luke findet auch Socken gut, also …
>
> Gutscheine gibt es ab 99 €, alles über den Link in der Bio.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #gutschein #weihnachtsgeschenk #hundeliebe

### Caption Last-Minute (Mo 14.12. / Fr 18.12. / Mo 21.12.)
> Noch kein Geschenk? Ich sage ja nichts. 😄
>
> Mein Shooting-Gutschein kommt als PDF, also auch noch, wenn es knapp wird. Schreib mir bis [DATUM – legst du fest], dann liegt er rechtzeitig unterm Baum.
>
> #esbeginntmiteinemwau #pottpic #hundefotografie #ruhrgebiet #lastminutegeschenk #weihnachtsgeschenk #gutschein

---

## 6. Dein neuer Zähler (statt Likes)

Einfach eine Strichliste im Handy, jeden Abend 1 Minute. Woher jemand kommt, steht ja meistens schon in der WhatsApp.

| Datum | Anfragen | Davon gekauft | € | Woher (Aushang wo, Karte, Insta, Facebook, persönlich, Empfehlung) |
|---|---|---|---|---|

Am Di 01.12. schauen wir zusammen drauf. Dann wissen wir, was wirklich Geld bringt, und nicht, was nur Herzchen bringt.

---

## 7. Was du jetzt tun musst

- [x] **Preise** freigegeben (15.11.)
- [x] **Nur Gutscheine**, Dezember auf Anfrage (15.11.)
- [x] **WhatsApp-Nummer** eingetragen
- [x] **Werbung bei der Derner Schnauzenbande** geklärt
- [ ] **Aushang einmal mit dem Handy scannen**, dann drucken und aufhängen
- [ ] **Bio-Link** auf den Instagram-WhatsApp-Link aus Abschnitt 2 stellen
- [ ] **WhatsApp-Status Mi 18.11. abends**, Facebook-Post anpinnen, Kasten auf die Homepage (`2026-11-15-ohne-reichweite.md`)
- [ ] **Bis wann du Gutschein-PDFs vor Weihnachten rausschickst** (für 4D und die Last-Minute-Posts)
- [ ] **Foto** für den Aushang (statt Herz) und für den Karussell-Post am 18.11.
- [ ] **Metricool:** Instagram verbinden, dann plane ich die Posts nach deinem Okay ein
- [ ] Optional: GitHub Pages einschalten, wenn du die Angebotsseite auch online haben willst

---

Quellen Preisvergleich: Markt-Check vom 30.10.2026 (`pottpic-team/analyse/2026-10-30-markt-check.md`, Herzensblick: [herzensblick.com](https://herzensblick.com/)). Websuche vom 15.11.2026 brachte keine Ruhrgebiets-Preise für Hundeshootings, nur allgemeine Ratgeber, z. B. [format.com: Christmas Mini Session Prices](https://format.com/magazine/christmas-mini-sessions-prices).

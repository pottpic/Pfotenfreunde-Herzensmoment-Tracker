# Derner Schnauzenbande e.V. – gemeinsamer Kontext fürs Vereinsteam

Dieser Ordner (`derner-team/`) gehört **nur** dem Verein. Komplett getrennt von Pottpic – keine Pottpic-Regeln, kein Pottpic-Hashtag, keine Pottpic-Agenten hier reinmischen.

## Der Verein
- Name: **Derner Schnauzenbande** – immer genau so geschrieben. Nie „Derna“, nie „Dernaer“, nie „Schnauzen-Bande“.
- Adresse: Derner Straße 415, 44329 Dortmund
- Website: www.dernerschnauzenbande.de (läuft über ClubDesk)
- 1. Vorsitzende: Sabine Stempel
- 2. Vorsitzende: Moni – macht Website, Social Media und Verwaltung. Moni ist die, mit der das Team redet.
- **Freilauf:** beaufsichtigt, mittwochs ab 17 Uhr, alle Hundeleute sind eingeladen (nicht nur Mitglieder).
- Achtung Begriff: **„Vorsitz“** meint im Vereinsalltag meist die Hundesport-Übung (Hund sitzt vor dem Menschen), **nicht** das Amt. Im Zweifel nachfragen.

## Look
- Logo: `logo/derner-schnauzenbande-logo.png` (drei Hundeköpfe unterm Bogen, Herz, Schriftzug)
- Dunkelgrün ca. **#2F5D50**
- Creme ca. **#FAF1E0**
- Einblendungen, Cover, Grafiken immer in diesen zwei Farben.

## Ton (Monis Stimme)
- Locker, warm, direkt, immer per Du. Ruhrpott darf durchkommen.
- Einschübe wie „weißt du“, „ich mein“, „halt“, „eigentlich“; verschluckte Silben wie „’n“, „grade“, „ma“, „is“.
- Keine Floskeln („Wir freuen uns sehr…“, „unvergessliche Momente“), kein Marketing-Sprech, kein glattes KI-Deutsch.
- Emojis dosiert – nur wo’s passt, nie als Deko-Kette.

## Regeln für alle
1. **KI-Bilder und KI-Grafiken sind erlaubt – aber nicht übertreiben** (Monis Entscheidung vom 31.10.2026). Echte Fotos von echten Menschen und Hunden haben Vorrang, Rückblicke und Vereinsalltag immer mit echten Fotos. Nie echte Mitglieder oder Vereinshunde per KI nachbauen. Fotorealistische KI-Bilder bei Meta als KI kennzeichnen.
2. **KI-Videos** nur auf Monis ausdrückliches Ja für ein **konkretes** Video:
   - nur über Magnific/Freepik,
   - vorher Kosten (Credits/Euro) nennen,
   - nie echte Mitglieder oder Vereinshunde nachbauen,
   - immer sichtbar als KI kennzeichnen.
3. **Freigabe:** Moni gibt Bild und Text immer selbst frei. Ohne ihr Ja wird nichts gepostet, hochgeladen oder verschickt.
4. Instagram und Facebook laufen über die **Meta Business Suite** (Moni postet selbst).
5. **Reels immer stumm** (keine Tonspur, keine Musik in der Datei).
6. **Ohne API und ohne Zusatzkosten** – Ausnahme nur KI-Videos (oder kostenpflichtige KI-Bilder) nach Monis Ja mit Kostennennung vorher.
7. **Erst fragen, dann loslegen.** Rückfragen mit Antwortmöglichkeiten zum Antippen.
8. **Nichts erfinden:** keine Termine, Namen, Zahlen, Zitate oder Erlebnisse, die Moni nicht genannt hat. Fehlt was → als Lücke markieren `[??? …]`.
9. **Datenschutz:** Fotos nur mit Einwilligung der gezeigten Personen. Keine Nachnamen, Adressen oder Kennzeichen von Mitgliedern ohne Okay. Kinder nur mit Einwilligung der Eltern.

## Das Team (`.claude/agents/`)
| Agent | Aufgabe |
|---|---|
| `derner-chef` | Startet alles, fragt nach, verteilt, lässt prüfen, bringt Moni die Freigabe |
| `derner-social-texter` | Posts, Captions, Reel-Texte für Instagram & Facebook |
| `derner-foto-pruefer` | Fotos auswählen, alles prüfen – meldet nur, ändert nichts |
| `derner-website-events` | ClubDesk-Texte, Event-Abläufe, Termine, Social-Zeitleiste |
| `derner-newsletter` | Schnauzenpost (CleverReach, Vereins-Account) |
| `derner-trendsetter` | Schaut, was andere Hundevereine machen, bewertet Ideen |
| `derner-video-editor` | Handy-Videos → stumme Reels mit FFmpeg |

Ablauf: Moni → `derner-chef` (Rückfragen) → passende Mitarbeiter → `derner-foto-pruefer` → `derner-chef` bringt Moni Bild + Text zur Freigabe.

## Arbeitszeiten
- **`derner-trendsetter` ist rund um die Uhr im Dienst:** Eine geplante Aufgabe weckt ihn **alle 4 Stunden** (Monis Entscheidung vom 31.10.2026). Er sucht, bewertet und legt alles unter `ergebnisse/trends/` ab.
- Findet er was richtig Gutes, meldet er’s dem **Leitwolf** (= `derner-chef`). Der Leitwolf entscheidet, welche Mitarbeiter sich drum kümmern sollen, und schickt Moni den Vorschlag als **Push aufs Handy**.
- **Alle anderen arbeiten nur auf Zuruf**, also wenn Moni was will oder wenn der Leitwolf sie nach einem Trend-Fund einteilt. Und das erst, **nachdem Moni Ja gesagt hat**.
- Kein Fund, kein Ping. Moni wird nur gestört, wenn’s was taugt.

## Nutzungslimit-Bremse
- Vor jedem Trendsetter-Lauf und bevor der Leitwolf größere Arbeit verteilt, wird das Claude-Nutzungslimit gecheckt. Das geht über die Ereignisse der eigenen Sitzung (`get_session` ohne ID → `list_events` mit `kinds: ["rate_limit_event"]` → das neueste Ereignis → `unifiedWindows`).
- **Grenze:** 5-Stunden-Fenster ab **80 %** oder Wochenfenster ab **90 %**, oder der Status is nicht mehr „allowed“.
- Wird die Grenze erreicht: **nicht weiterarbeiten.** Stattdessen gibt’s ’nen kurzen Tipp an Moni: „Limit fast voll (X %). Ich setz aus, ab HH:MM Uhr is wieder frei (in ca. N Std.).“ Die Zeit steht in `resetsAt` und wird in Europe/Berlin umgerechnet.
- Dieser Tipp darf auch erst beim nächsten Lauf kommen. Echtzeit is nicht nötig.
- Lässt sich das Limit nicht auslesen, wird normal weitergearbeitet, und das kommt mit in den Bericht.

## Bedienung (wie bei Pottpic)
- **Chef in der Leiste:** die angepinnte Seite „Derner Leitwolf“ (Quelle: `team/leitwolf.src.html`, bauen mit `python3 team/build.py`). Da gibt’s **„Mal eben was“** (ein Post sofort) und **„Team los“** (startet ’ne Sitzung mit `/derner-los`).
- **`/derner-los <Thema>`** in Claude Code: Der Leitwolf legt mit dem ganzen Team los.
- **Geplante Aufgaben mit Ping:** Trendsetter (alle 4 Std.), Posting-Wecker (täglich 8:37 Uhr, liest `ergebnisse/postplan.md`), Schnauzenpost-Entwurf (1. Sonntag im Monat, 10:43 Uhr).

## Ablage
- Ergebnisse: `ergebnisse/<bereich>/JJJJ-MM-TT-thema.md` (Bereiche: social, website, newsletter, trends, video)
- Fertige Videos/Cover: `ergebnisse/video/JJJJ-MM-TT-thema/`

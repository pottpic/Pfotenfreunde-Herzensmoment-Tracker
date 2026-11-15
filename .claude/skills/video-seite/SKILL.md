---
name: video-seite
description: Video-Seite – macht aus einem YouTube-Video ein Transkript und daraus eine fertige Webseite (Blogartikel, Landingpage oder Kurzfassung) im Look von Pottpic, Derner Schnauzenbande oder Pfotenfreunde. Ohne API-Schlüssel, 0 €. Nutzen bei „/video-seite <link>“, „mach aus dem Video 'ne Seite“, „transkribier das Video“ oder wenn Moni einen YouTube-Link schickt und einen Text oder eine Webseite daraus will.
---

# Video-Seite

Du bist **Leitwolf**. Lies zuerst `CLAUDE.md` und `pottpic-team/seiten-werkstatt/LIESMICH.md`. Geht's um den Verein, gilt für den Text `derner-team/KONTEXT.md`.

## Ablauf

1. **Fragen, was fehlt** (AskUserQuestion, Empfehlung zuerst) – nur das, was Moni nicht schon gesagt hat:
   - Art: Blogartikel / Landingpage / Kurzfassung
   - Marke: Pottpic / Derner / Pfotenfreunde
   - Text: umschreiben oder nur aufbereiten
   - Bei Landingpage: Wohin soll der Knopf führen? (Link nie erfinden)
2. **Transkript holen:** `pip install -q yt-dlp`, dann
   `python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py holen <link>`
   - Meldet YouTube „not a bot“ oder 429: **nicht tricksen** (keine Cookies, keine anderen Dienste, keine Wiederholschleife). Moni bitten, das Transkript zu kopieren (unter dem Video: … → Transkript anzeigen) und in den Chat zu schicken. Dann als Textdatei ablegen und mit `--text` weiter.
   - Kommt ein 403 vom Netzwerk: Die Sitzung läuft nicht in der Umgebung mit YouTube-Zugriff. Moni sagen, Plan B anbieten.
3. **Nur aufbereiten:** `… bauen <ordner>` → `transkript.html`. Fertig.
4. **Umschreiben:** `transkript.md` lesen und `seite.json` schreiben (Aufbau siehe LIESMICH).
   - Monis Stimme nach `CLAUDE.md` (Derner: Vereinsstimme). Aus Gesprochenem wird lesbarer Text, kein Abtippen.
   - Nur was im Video gesagt wird. Nix dazuerfinden, keine Zahlen, Kunden oder Bewertungen.
   - Automatische Untertitel verhören sich, vor allem bei Namen und Orten. Was unsicher ist, bei Moni nachfragen statt raten.
   - **Fremdes Video** (`eigenes: false` in `video.json`): Gedanken mit eigenen Worten zusammenfassen, keine Sätze übernehmen, kurz halten. Die Quelle setzt das Skript selbst drunter.
   - Dann `… bauen <ordner>` → `index.html`.
5. **Zeigen:** Seite als Datei an Moni schicken (SendUserFile). Moni sagt „jo“ oder „ändern“.
6. **Ablegen:** Ordner liegt unter `pottpic-team/seiten-werkstatt/seiten/` und kommt mit ins Regal (`main`).

## Regeln
- Online stellen ist Veröffentlichen: nur mit Monis Okay, und nur mit Impressum- und Datenschutz-Link in der `seite.json`.
- Das aufbereitete Transkript von 'nem fremden Video geht nie online.
- Derner-Seiten nie mit Pottpic-Farben oder #esbeginntmiteinemwau.

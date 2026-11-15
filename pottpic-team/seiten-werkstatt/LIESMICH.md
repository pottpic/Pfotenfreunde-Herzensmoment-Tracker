# Seiten-Werkstatt

Macht aus 'nem YouTube-Video erst ein Transkript und dann 'ne fertige Webseite. Kostet nix, braucht keinen API-Schlüssel, läuft hier in der Sitzung.

## Für Moni, ganz kurz
1. YouTube-Link schicken und sagen, was es werden soll: **Blogartikel**, **Landingpage** oder **Kurzfassung** – und für wen: **Pottpic**, **Derner** oder **Pfotenfreunde**.
2. Dazu sagen: **umschreiben** (das Team macht 'nen richtigen Text in deinem Ton draus) oder **nur aufbereiten** (das Gesprochene in Absätzen mit Zeitmarken).
3. Seite angucken → „jo“ oder „ändern“.

Wenn YouTube mal nicht mitspielt (passiert, siehe unten): unter dem Video auf **… → Transkript anzeigen**, alles markieren, kopieren und in den Chat schicken. Dann geht's damit weiter.

## Für das Team
```
python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py holen <youtube-link> [--sprache de] [--eigenes ja|nein]
python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py bauen <ordner> [--art artikel|landingpage|kurz] [--marke pottpic|derner|pfotenfreunde]
```
Einmal pro Sitzung vorher: `pip install yt-dlp`.

`holen` legt `seiten/JJJJ-MM-TT-titel/` an:
- `video.json` – Titel, Kanal, Link, Kapitel, eigenes Video ja/nein
- `transkript.json` – Zeilen mit Sekunden
- `transkript.md` – zum Lesen und als Grundlage fürs Umschreiben

`bauen` macht die Seite:
- **Mit `seite.json`** im Ordner → `index.html` (umgeschriebener Text).
- **Ohne `seite.json`** (oder mit `--roh`) → `transkript.html` (nur aufbereitet, immer als Artikel).

### Plan B: Transkript von Hand
```
python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py holen <youtube-link> --text kopiert.txt --titel "Titel" --kanal "Kanalname"
```
Die Textdatei darf so aussehen, wie YouTube es beim Kopieren ausspuckt (Zeitmarke und Text abwechselnd).

### seite.json (schreibt das Team beim Umschreiben)
```json
{
  "art": "artikel",
  "marke": "pottpic",
  "titel": "Überschrift der Seite",
  "einleitung": "Zwei, drei Sätze. Leerzeile = neuer Absatz.",
  "kernpunkte": ["Punkt eins", "Punkt zwei", "Punkt drei"],
  "abschnitte": [
    {"ueberschrift": "Zwischenüberschrift", "zeit": 95, "text": "Fließtext …", "liste": ["optional", "als Liste"]}
  ],
  "knopf": {"satz": "Satz über dem Knopf", "text": "Knopf-Text", "link": "https://…"},
  "impressum": "https://…",
  "datenschutz": "https://…",
  "video_einbetten": true
}
```
- `zeit` sind Sekunden im Video, daraus wird ein Sprung-Link.
- `artikel`: Titel, Einleitung, Video, Kernpunkte, Abschnitte. `landingpage`: Titel, Einleitung, Kernpunkte, Video, Abschnitte, Knopf. `kurz`: Titel, Einleitung, Kernpunkte, Video, Knopf.
- Der Knopf erscheint nur mit Text und Link. Links nie erfinden, bei Moni nachfragen.
- Bevor 'ne Seite online geht, müssen `impressum` und `datenschutz` drinstehen.

### Eigene und fremde Videos
- Eigene Kanäle stehen oben im Skript (`EIGENE_KANAELE`). Passt der Kanalname nicht, mit `--eigenes ja` nachhelfen.
- **Fremdes Video:** Unter der Seite steht immer die Quelle mit Link. Der Text wird mit eigenen Worten geschrieben, nix eins zu eins übernommen. Das aufbereitete Transkript von 'nem fremden Video ist nur zum internen Lesen: Es kriegt 'nen Hinweis-Balken und `noindex`.

### Look
Eine einzelne HTML-Datei, ohne fremde Schriften oder Bilder, hell und dunkel, passt aufs Handy.
- `pottpic`: Navy + Gold auf Creme
- `derner`: Dunkelgrün + Creme, ohne Pottpic-Farben
- `pfotenfreunde`: die warmen Töne vom Herzensmoment-Tracker

Das Video lädt erst, wenn jemand auf „Video abspielen“ klickt (vorher geht nix an YouTube).

### Was nicht geht
- YouTube lässt Cloud-Rechner nicht immer ran („Sign in to confirm you're not a bot“ oder Fehler 429). Dann nicht tricksen und nicht dauernd neu probieren, sondern Plan B.
- Die Sitzung braucht 'ne Umgebung, in der `www.youtube.com` erlaubt ist (Umgebung „pfotenfreunde-herzensmoment-tracker“).
- Videos ganz ohne Untertitel gehen nur über Plan B. Automatische Untertitel haben Fehler, vor allem bei Namen – beim Umschreiben gegenlesen.

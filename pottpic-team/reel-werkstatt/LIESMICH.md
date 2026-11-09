# Reel-Werkstatt

Macht aus 'nem Ordner mit Fotos ein fertiges Reel (9:16, stumm) plus Cover. Kostet nix, läuft komplett hier in der Sitzung.

## Für Moni, ganz kurz
1. Fotos in den Ordner legen, den das Team dir sagt (oder einfach im Chat schicken und sagen, für welche Idee).
2. Sagen: „Bau ma das Reel.“
3. Reel angucken → „jo“ oder „ändern“. Den Sound suchst du in der Insta-App aus.

## Für das Team
```
python3 pottpic-team/reel-werkstatt/reel_bauen.py <ordner> [--marke pottpic|derner] [--ziel <ordner>]
```
Ergebnis landet im Ordner: `<titel>-reel.mp4` und `<titel>-cover.jpg`.

### reel.json (optional, liegt im Foto-Ordner)
```json
{
  "titel": "2026-11-10-laub-luke",
  "marke": "pottpic",
  "hook": "So sieht 'n echtes Shooting aus",
  "folien": [
    {"foto": "01.jpg", "text": ""},
    {"foto": "02.jpg", "text": "Erst ma schnüffeln, weißt du"},
    {"foto": "03.jpg", "text": "Dann kommt der Blick"}
  ],
  "schluss": "Für Erinnerungen, die bleiben.",
  "sekunden_pro_foto": 2.6
}
```
- Der Hook ersetzt den Text der ersten Folie.
- Fehlt ein Foto aus dem Plan, nimmt das Skript das nächste freie. Übrige Fotos hängt es ohne Text hinten an.
- Ohne `reel.json`: alle Fotos nach Dateiname, ohne Text.
- Emojis fliegen aus den Einblendungen raus (kann die Schrift nicht), die gehören in die Caption.
- HEIC-Fotos vom iPhone gehen nur, wenn `pillow-heif` installiert is, sonst vorher als JPG.

### Look
Foto als Abzug mit hellem Rand, leicht schräg, langsamer Zoom, Creme-Papier mit leichtem Korn, oben klein der Absender, unten der Text, am Ende die Schlusskarte.
- `pottpic`: Navy + Gold, „Für Erinnerungen, die bleiben.“ · pottpic.de
- `derner`: Dunkelgrün + Creme, ohne Pottpic-Farben

Eigene Handschrift-Schrift (z. B. Caveat, frei/OFL): `.ttf` in `pottpic-team/reel-werkstatt/schrift/` legen, dann nimmt das Skript die für die Texte. Ohne die gibt's Inter.

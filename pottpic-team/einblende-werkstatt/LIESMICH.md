# Einblende-Werkstatt

Legt „5 Punkte“-Einblendungen im Pottpic-Look über ein fertiges Reel (9:16). Kostet nix, läuft hier in der Sitzung.

## Für Moni, ganz kurz
1. Dein fertiges Reel im Chat schicken und sagen, welcher Plan (z. B. „Gassi im Laub“).
2. Das Team legt die Einblendungen drüber.
3. Angucken → „jo“ oder „ändern“.

## Für das Team
```
python3 pottpic-team/einblende-werkstatt/einblenden.py <plan.json> --video <reel.mp4>   # fertiges Reel
python3 pottpic-team/einblende-werkstatt/einblenden.py <plan.json> --demo [--dauer 19]  # Vorschau mit Platzhalter
```
Ergebnis liegt neben der plan.json: `<titel>.mp4` (Ton vom Original bleibt) und `<titel>-nur-einblendungen.mov`
(transparent, ProRes 4444, zum Drüberlegen in CapCut/Edits – groß, nicht ins Repo committen).

Ablauf: Intro-Karte mit Titel + 5er-Leiste (3,4 s) → Punkt 1–5 gleichmäßig verteilt (Zahlenkarte, Titel-Chip,
Handschrift-Satz, oben kleine Fortschrittspunkte, beim letzten „Zum Schluss“) → Schlusskarte mit Frage (3 s).
Mindestlänge vom Reel: ca. 16 Sekunden.

Beispiel-Plan: `pottpic-team/video/2026-11-21-gassi-im-laub/plan.json`.
Schriften (OFL, frei nutzbar): Montserrat + Caveat in `schrift/`. Farben: Navy, Gold, Creme wie die Reel-Werkstatt.
Text in den Einblendungen ohne Emojis, Stimme nach CLAUDE.md („ist“, „nicht“, „mal“, „gerade“).

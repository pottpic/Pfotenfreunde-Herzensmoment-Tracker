Testlauf – nicht entschieden

# Zahlenlage Pottpic (Stand 12.11.2026)

Nasenarbeit (`analyse`) · Runde 1 Testlauf · nur gelesen, nichts verändert.

## 1. Was es schon gibt (Dateien unter `pottpic-team/analyse/`)
- `2026-10-30-echt-jetzt-messbogen.md` und `.xlsx`: Messbogen mit 6 Kennzahlen, Terminen bis 22.02.2027, Signalen zum Nachsteuern. Alle Werte leer, alle Ziele ausdrücklich Schätzungen.
- `2026-10-30-markt-check.md`: Wettbewerber und Ideen aus öffentlichen Quellen. Dort steht selbst: keine eigenen Zahlen von Moni.

**Echte Pottpic-Zahlen gibt es damit bisher keine.** Weder Follower, Reichweite, Saves/Shares, Profilaufrufe, Link-Klicks, Newsletter-Abos noch Anfragen oder Buchungen. Das Startwert-Fenster 19.10.–01.11. (Messtag 02.11.) ist laut Dateien nicht ausgefüllt. Ob Moni es woanders (z. B. auf Papier) ausgefüllt hat, ist nicht belegt.

## 2. Metricool: was holbar ist (nur lesend geprüft)
- `getBrandSettings`: Fehler, wörtlich: "This brand doesn't have any social network connected yet. Ask the user to connect at least one network before continuing here: https://app.metricool.com/brands/connections?blogId=4643778"
- `getAnalyticsAvailableMetrics` (instagram): klappt, liefert nur die Liste möglicher Metriken (z. B. Followers, Views, Reach). Das sind keine Pottpic-Daten.
- `getAnalyticsDataByMetrics` (Followers + Reach, 19.10.–01.11., Brand-ID aus dem Link oben): lieferte `{"rows":[["0.0","0.0","20261101"]]}`. Das ist **keine echte Zahl**, sondern leer, weil kein Netzwerk hängt. Nicht als "0 Follower" lesen.
- Fazit: Zahlen aus Metricool sind **zurzeit nicht holbar**. `getBestTimeToPostByNetwork` nicht probiert, würde ohne Netzwerk dasselbe ergeben (Annahme, nicht geprüft).

## 3. Was fehlt, und was Moni tun muss
| Fehlt | Wie man es kriegt |
|---|---|
| Instagram (ggf. Facebook, TikTok) in Metricool | Link oben öffnen, Netzwerk verbinden (braucht Instagram-Business- bzw. Creator-Konto). Danach holt Nasenarbeit die Zahlen selbst. |
| Startwert 19.10.–01.11. | Instagram-Kontoübersicht, Zeitraum benutzerdefiniert: Profilaufrufe, Link-Klicks. Dazu Gespeichert + Geteilt der letzten 3 normalen Reels. Anleitung: Messbogen Abschnitt 2. |
| Anfragen mit Herkunft | Blatt "Anfragen" in der xlsx ausfüllen. Ohne das kann man nicht sagen, was Buchungen statt Likes bringt. |
| Newsletter-Stand | CleverReach, aktive Empfänger (laut Messbogen wahrscheinlich 0 oder sehr klein). |
| Rückwirkende Daten | Ob Metricool nach dem Verbinden auch Zeiträume davor zeigt und was der Gratis-Tarif hergibt, ist nicht belegt. Nach dem Verbinden prüfen. |

## 4. Übergabe
Nichts zu empfehlen, solange keine Daten da sind. Sobald das Netzwerk hängt: Nasenarbeit zieht den Startwert, danach Monats-Kurzbericht (3 Erkenntnisse, 3 Empfehlungen, 1 Experiment).

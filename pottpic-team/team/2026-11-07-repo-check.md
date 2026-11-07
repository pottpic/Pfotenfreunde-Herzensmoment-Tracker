# Repo-Check: Was fehlt immer? (07.11.2026)

Noch nix repariert, nur rausgesucht. Fixen nach Monis Okay.

## Das große Problem: Sachen landen in Nebenschubladen
Jede Sitzung arbeitet in 'nem eigenen Zweig (Branch). Neue Sitzungen starten aber immer von `main`.
Was nicht in `main` gemergt is, kennt das Team beim nächsten Mal nicht.

| Zweig | Was drin is | Merge in main |
|---|---|---|
| claude/hunde-reel-trends (PR #13 offen) | Trend-Report Anfang Nov, Reel-Konzept Luke crasht Herbst-Reel, Pfotenfreunde-Post Hundebeichte | sauber |
| claude/luke-und-ich-bild | Bild „Wir zwei.“ Feed + Story, 3 Spruch-Varianten, Caption | sauber |
| claude/team-entwuerfe | Wochen-Paket KW45, Skool-Posts 02.11. | sauber |
| claude/napfzeit-kalorien-app | Napfzeit Kalorien-Tracker (Web-App) | sauber |
| claude/reel-regenrunde | Derner Reel Regenrunde mit Covern, Endkarte | sauber |
| claude/pottpic-team-google-drive-hsqpid | kleine Änderung: Leitwolf sagt Bescheid, wann's nach Claude Code geht | sauber |
| claude/loving-einstein-g6u1pf | Metricool-Einbau (diese Sitzung) | sauber |
| derner-team | altes, paralleles Derner-Team: Silvester-Reihe, Schnauzenpost Nov, Pfotenzauber-Posts + Flyer, Logo, Foto-Einwilligung, Advent-Ideen, Leitwolf-Seite | 1 Konflikt (derner-los/SKILL.md) – mit Gefühl: nur Ergebnisse rüberholen, die alten Doppel-Agenten nicht |

Schon erledigt / leer: claude/derner-team, claude/derner-hundeplan-januar, claude/pottpic-vorrang.

## Kleinere Lücken
- Connectors nicht verbunden: Metricool (fehlt noch), Canva und Magnific (brauchen 'ne Anmeldung in claude.ai). Macherpfote und Schnittpfote rechnen aber damit.
- README is fast leer.

## Vorschlag zum Fixen
1. Die sauberen Zweige nacheinander in main holen (per PR, Moni klickt „Merge“).
2. derner-team-Zweig: nur die Ergebnisse unter `derner-team/` einsortieren, Konflikt von Hand lösen.
3. Danach alte Zweige aufräumen.
4. Ab dann: am Ende jeder Sitzung PR auf und mergen, damit nix mehr liegen bleibt.

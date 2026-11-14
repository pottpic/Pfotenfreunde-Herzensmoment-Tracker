# Limit-Balken

Zeigt über dem Eingabefeld von Claude Code zwei kleine Balken: wie viel vom **5-Stunden-Limit** und vom **Wochenlimit** schon verbraucht is – mit Prozent und wann's sich wieder zurücksetzt. Grün bis 69 %, gelb ab 70 %, rot ab 90 %. Die Werte kommen mit den Antworten mit, ganz am Anfang steht da also kurz „noch keine Werte“.

## Installieren

In diesem Repo passiert das automatisch über `.claude/settings.json` (Claude Code fragt einmal, ob der Marktplatz „pottpic“ und das Plugin rein dürfen).

Von Hand, im Terminal an der Eingabe:

```
/plugin install limit-balken --marketplace pottpic/Pfotenfreunde-Herzensmoment-Tracker
```

Aus der Shell:

```
claude plugin install limit-balken --marketplace pottpic/Pfotenfreunde-Herzensmoment-Tracker
```

Das Repo is privat: Installieren klappt nur mit GitHub-Zugang zum Repo auf dem Rechner (SSH-Key oder `gh auth login` + `gh auth setup-git`).

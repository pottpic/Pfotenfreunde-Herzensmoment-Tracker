---
name: regal-aufraeumen
description: Holt alle offenen `claude/…`-Zweige der geplanten Aufgaben (Routinen) per PR nach `main` und meldet Moni, welche Zweige sie auf GitHub von Hand löschen kann. Nutzen bei „Regal aufräumen“, „Zweige mergen“ oder „was liegt noch rum“.
---

# Regal aufräumen

Routinen (geplante Aufgaben) dürfen nicht auf `main` pushen (Sperre, 403). Sie legen ihre Ergebnisse auf Zweigen `claude/<kurzname>-JJJJ-MM-TT` ab. Dieser Skill bringt sie nach `main`. Das Ablegen im Repo braucht kein extra Okay von Moni (Regel „Alles ins Regal“ in `CLAUDE.md`). Gepostet, eingeplant oder verschickt wird dadurch nix.

Repo-Kürzel unten: `R=pottpic/pfotenfreunde-herzensmoment-tracker`. Alles per `gh api` (REST) – `gh pr …` geht hier nich.

1. **Zweige auflisten:** `git ls-remote --heads origin 'claude/*'`. Nix da? Dann sag Moni „Regal is schon leer“ und hör auf.
2. **Schon erledigte überspringen:** Pro Zweig die Spitze (SHA) merken. Ein Zweig is erledigt, wenn
   - `gh api repos/$R/compare/main...BRANCH --jq .ahead_by` = 0 ist, oder
   - es einen gemergten PR gibt, dessen `head.sha` der Zweigspitze entspricht: `gh api "repos/$R/pulls?head=pottpic:BRANCH&state=closed" --jq '.[] | select(.merged_at != null) | .head.sha'`.
3. **Ältesten zuerst mergen** (nach Commit-Datum), damit Konflikte seltener sind:
   - PR anlegen: `gh api repos/$R/pulls -f title="Regal: BRANCH" -f head=BRANCH -f base=main -f body="Aufräumen der Routinen-Ergebnisse."`
   - Mergen: `gh api -X PUT repos/$R/pulls/NR/merge -f merge_method=merge`. Geht „merge“ nich, dann `squash`.
   - Konflikt (405/409)? Nix erzwingen: Zweig auslassen, Moni die Dateien nennen.
4. **Zweige löschen geht nich** (Proxy sperrt das). Sag Moni, welche Zweige jetzt erledigt sind, und gib ihr den Link zum Löschen: https://github.com/pottpic/Pfotenfreunde-Herzensmoment-Tracker/branches
5. **Meldung in Monis Stimme, kurz:** was neu in `main` is (Dateinamen), was nich ging und warum.

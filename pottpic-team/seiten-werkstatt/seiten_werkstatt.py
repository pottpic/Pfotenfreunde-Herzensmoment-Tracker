#!/usr/bin/env python3
"""Seiten-Werkstatt: holt das Transkript von einem YouTube-Video und baut daraus eine Webseite.

Zwei Schritte:
    python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py holen <youtube-link> [--sprache de] [--eigenes ja|nein]
    python3 pottpic-team/seiten-werkstatt/seiten_werkstatt.py bauen <ordner> [--art artikel|landingpage|kurz] [--marke pottpic|derner|pfotenfreunde]

`holen` legt einen Ordner `seiten/JJJJ-MM-TT-titel/` an mit `video.json` (Titel, Kanal, Link, Kapitel),
`transkript.json` (Zeilen mit Sekunden) und `transkript.md` (zum Lesen).
Klappt der Abruf nicht (YouTube sperrt manchmal), geht es auch mit einem kopierten Transkript:
    ... holen <youtube-link> --text kopiert.txt --titel "Titel vom Video" --kanal "Kanalname"

`bauen` macht daraus `index.html`:
- Liegt eine `seite.json` im Ordner (umgeschriebener Text), wird die genommen.
- Ohne `seite.json` wird das Transkript nur sauber aufbereitet (Absätze mit Zeitmarken).

Kosten: 0 €. Kein API-Schlüssel. Untertitel kommen über yt-dlp (pip install yt-dlp).
"""
import argparse, datetime, html, json, re, sys, tempfile, unicodedata
from pathlib import Path

HIER = Path(__file__).resolve().parent
SEITEN = HIER / "seiten"

# Kanäle, die Moni gehören. Alles andere gilt als fremdes Video (Quelle wird genannt,
# das aufbereitete Transkript bleibt intern).
EIGENE_KANAELE = ("pottpic", "derner schnauzenbande", "pfotenfreunde")

MARKEN = {
    # Pottpic: Navy + Gold auf Creme.
    "pottpic": dict(name="Pottpic", zeile="Hundefotografie im Ruhrgebiet", web="https://www.pottpic.de",
                    schluss="Für Erinnerungen, die bleiben.",
                    hell=dict(bg="#FAF5EC", paper="#FFFDF8", ink="#1F2A44", muted="#5D6579", line="#E6DCC8",
                              akzent="#C9A24A", knopf="#1F2A44", auf_knopf="#FAF5EC"),
                    dunkel=dict(bg="#141A2A", paper="#1C2438", ink="#F3ECDD", muted="#A9B0C2", line="#2E3852",
                                akzent="#D9B866", knopf="#D9B866", auf_knopf="#141A2A")),
    # Derner Schnauzenbande: Creme + Dunkelgrün (nie mit Pottpic-Farben mischen).
    "derner": dict(name="Derner Schnauzenbande", zeile="Hundesport in Dortmund-Derne", web="",
                   schluss="",
                   hell=dict(bg="#FAF1E0", paper="#FFFBF2", ink="#1F3A33", muted="#5B6F68", line="#E3D6BD",
                             akzent="#2F5D50", knopf="#2F5D50", auf_knopf="#FAF1E0"),
                   dunkel=dict(bg="#14211D", paper="#1B2C27", ink="#F1E8D6", muted="#A9B8B0", line="#2E4640",
                               akzent="#7FB3A2", knopf="#7FB3A2", auf_knopf="#10201B")),
    # Pfotenfreunde: die warmen Töne vom Herzensmoment-Tracker.
    "pfotenfreunde": dict(name="Pfotenfreunde", zeile="Die Community für Hundemenschen", web="",
                          schluss="",
                          hell=dict(bg="#FDF7EF", paper="#FFFCF7", ink="#1A120B", muted="#7A6654", line="#EADCC8",
                                    akzent="#C9651A", knopf="#3D2C1E", auf_knopf="#FDF7EF"),
                          dunkel=dict(bg="#17110C", paper="#211912", ink="#F6ECE0", muted="#A99583", line="#3A2D22",
                                      akzent="#F5A623", knopf="#F5A623", auf_knopf="#17110C")),
}
ARTEN = ("artikel", "landingpage", "kurz")


# ---------- kleine Helfer ----------

def video_id(link):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", link)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", link.strip()):
        return link.strip()
    sys.exit(f"Das sieht nicht nach 'nem YouTube-Link aus: {link}")


def slug(text, laenge=50):
    text = text.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:laenge].strip("-") or "video"


def zeit(sek):
    sek = int(sek)
    h, m, s = sek // 3600, sek % 3600 // 60, sek % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def ist_eigenes(kanal):
    k = (kanal or "").lower()
    return any(e in k for e in EIGENE_KANAELE)


def e(text):
    return html.escape(str(text), quote=True)


def sicherer_link(link):
    link = str(link or "").strip()
    return link if re.match(r"^(https?://|mailto:|tel:|#|/)", link) else ""


# ---------- Schritt 1: Transkript holen ----------

def json3_zeilen(datei):
    """YouTube-Untertitel (json3) -> [{start, text}]"""
    zeilen = []
    for ev in json.loads(Path(datei).read_text(encoding="utf-8")).get("events", []):
        text = "".join(s.get("utf8", "") for s in ev.get("segs") or [])
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            zeilen.append({"start": round(ev.get("tStartMs", 0) / 1000, 1), "text": text})
    return zeilen


def text_zeilen(datei):
    """Kopiertes Transkript (Zeitmarke und Text abwechselnd oder in einer Zeile) -> [{start, text}]"""
    zeilen, start = [], 0.0
    marke = re.compile(r"^\[?((?:\d{1,2}:)?\d{1,2}:\d{2})\]?\s*(.*)$")
    for roh in Path(datei).read_text(encoding="utf-8").splitlines():
        roh = roh.strip()
        if not roh:
            continue
        m = marke.match(roh)
        if m:
            teile = [int(t) for t in m.group(1).split(":")]
            start = float(sum(t * 60 ** i for i, t in enumerate(reversed(teile))))
            roh = m.group(2).strip()
            if not roh:
                continue
        zeilen.append({"start": start, "text": roh})
    return zeilen


def von_youtube(vid, sprache):
    try:
        import yt_dlp
    except ImportError:
        sys.exit("yt-dlp fehlt. Einmal ausführen: pip install yt-dlp")
    link = f"https://www.youtube.com/watch?v={vid}"
    plan_b = ("Plan B: Transkript bei YouTube kopieren (unter dem Video: … → Transkript anzeigen), "
              "in 'ne Textdatei packen und nochmal mit --text <datei> --titel … --kanal … starten.")
    try:
        with yt_dlp.YoutubeDL(dict(skip_download=True, quiet=True, no_warnings=True)) as ydl:
            info = ydl.extract_info(link, download=False)
            von_hand, auto = info.get("subtitles") or {}, info.get("automatic_captions") or {}
            # Erst echte Untertitel in der Wunschsprache, dann automatische, dann Englisch, dann was da ist.
            # Genau EINE Spur laden (sonst macht YouTube bei zu vielen Anfragen dicht).
            wahl = [(von_hand, sprache), (auto, f"{sprache}-orig"), (auto, sprache), (von_hand, "en"),
                    (auto, "en-orig"), (auto, "en")]
            wahl += [(von_hand, s) for s in von_hand if s != "live_chat"]
            wahl += [(auto, s) for s in auto if s.endswith("-orig")]
            spur = next(((q, s) for q, s in wahl if any(f.get("ext") == "json3" for f in q.get(s) or [])), None)
            if not spur:
                sys.exit("Das Video hat keine Untertitel (auch keine automatischen). " + plan_b)
            quelle, sprache_ist = spur
            adresse = next(f["url"] for f in quelle[sprache_ist] if f.get("ext") == "json3")
            roh = ydl.urlopen(adresse).read()
    except SystemExit:
        raise
    except Exception as fehler:  # YouTube sperrt manchmal oder das Netz lässt es nicht durch
        sys.exit(f"YouTube hat nicht geliefert: {fehler}\n{plan_b}")
    automatisch = quelle is auto
    sprache_ist = sprache_ist.replace("-orig", "")
    with tempfile.TemporaryDirectory() as tmp:
        datei = Path(tmp) / "untertitel.json3"
        datei.write_bytes(roh)
        zeilen = json3_zeilen(datei)
    if not zeilen:
        sys.exit("YouTube hat leere Untertitel geschickt. " + plan_b)
    video = dict(id=vid, link=link, titel=info.get("title") or vid, kanal=info.get("channel") or info.get("uploader") or "",
                 kanal_link=info.get("channel_url") or "", dauer=info.get("duration") or 0,
                 datum=info.get("upload_date") or "", sprache=sprache_ist, automatisch=automatisch,
                 kapitel=[dict(start=k.get("start_time", 0), titel=k.get("title", "")) for k in info.get("chapters") or []])
    return video, zeilen


def holen(a):
    vid = video_id(a.link)
    if a.text:
        zeilen = text_zeilen(a.text)
        if not zeilen:
            sys.exit(f"In {a.text} steht nix drin.")
        video = dict(id=vid, link=f"https://www.youtube.com/watch?v={vid}", titel=a.titel or vid, kanal=a.kanal or "",
                     kanal_link="", dauer=int(zeilen[-1]["start"]), datum="", sprache=a.sprache, automatisch=False, kapitel=[])
    else:
        video, zeilen = von_youtube(vid, a.sprache)
        if a.titel:
            video["titel"] = a.titel
        if a.kanal:
            video["kanal"] = a.kanal
    video["eigenes"] = {"ja": True, "nein": False}.get(a.eigenes, ist_eigenes(video["kanal"]))

    ziel = Path(a.ziel) if a.ziel else SEITEN / f"{datetime.date.today():%Y-%m-%d}-{slug(video['titel'])}"
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / "video.json").write_text(json.dumps(video, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ziel / "transkript.json").write_text(json.dumps(zeilen, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    md = [f"# Transkript: {video['titel']}", "",
          f"- Video: {video['link']}", f"- Kanal: {video['kanal'] or 'unbekannt'}",
          f"- Eigenes Video: {'ja' if video['eigenes'] else 'nein (Quelle nennen, nix eins zu eins übernehmen)'}",
          f"- Untertitel: {video['sprache']}{' (automatisch erzeugt, kann Fehler haben)' if video['automatisch'] else ''}", ""]
    for absatz in absaetze(zeilen):
        md += [f"**[{zeit(absatz['start'])}]** {absatz['text']}", ""]
    (ziel / "transkript.md").write_text("\n".join(md), encoding="utf-8")

    woerter = sum(len(z["text"].split()) for z in zeilen)
    print(f"Transkript liegt in {ziel}")
    print(f"  {video['titel']} · {video['kanal'] or 'Kanal unbekannt'} · {zeit(video['dauer'])} · {woerter} Wörter"
          f" · {'eigenes' if video['eigenes'] else 'fremdes'} Video")
    return ziel


# ---------- Transkript in Absätze packen ----------

def absaetze(zeilen, max_woerter=90, pause=2.5):
    """Fasst Untertitel-Zeilen zu lesbaren Absätzen zusammen (neuer Absatz bei Pause oder wenn's lang wird)."""
    fertig, aktuell, start, letzte = [], [], 0.0, None
    for z in zeilen:
        text = z["text"]
        n = sum(len(t.split()) for t in aktuell)
        satzende = bool(aktuell) and aktuell[-1].rstrip().endswith((".", "!", "?"))
        neue_pause = letzte is not None and z["start"] - letzte > pause and n >= 25
        if aktuell and (neue_pause or (n >= max_woerter and satzende) or n >= max_woerter * 1.6):
            fertig.append({"start": start, "text": " ".join(aktuell)})
            aktuell = []
        if not aktuell:
            start = z["start"]
        aktuell.append(text)
        letzte = z["start"]
    if aktuell:
        fertig.append({"start": start, "text": " ".join(aktuell)})
    return fertig


def roh_seite(video, zeilen):
    """Ohne seite.json: Transkript nur aufbereiten, Kapitel vom Video als Überschriften."""
    alle = absaetze(zeilen)
    kapitel = sorted(video.get("kapitel") or [], key=lambda k: k["start"])
    abschnitte = []
    if kapitel:
        for i, k in enumerate(kapitel):
            ende = kapitel[i + 1]["start"] if i + 1 < len(kapitel) else float("inf")
            teil = [x for x in alle if k["start"] <= x["start"] < ende]
            if teil:
                abschnitte.append(dict(ueberschrift=k["titel"], zeit=k["start"], absaetze=teil))
        davor = [x for x in alle if x["start"] < kapitel[0]["start"]]
        if davor:
            abschnitte.insert(0, dict(ueberschrift="", zeit=0, absaetze=davor))
    else:
        abschnitte = [dict(ueberschrift="", zeit=0, absaetze=alle)]
    return dict(art="artikel", titel=video["titel"], roh=True, abschnitte=abschnitte)


# ---------- Schritt 2: Seite bauen ----------

CSS = """
:root{%(hell)s color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){%(dunkel)s color-scheme:dark}}
:root[data-theme="dark"]{%(dunkel)s color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.65 Georgia,"Iowan Old Style","Times New Roman",serif}
.wrap{max-width:720px;margin:0 auto;padding:0 20px}
header.kopf{padding:22px 0;border-bottom:1px solid var(--line)}
.absender{font:600 .8rem/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);text-decoration:none}
.absender span{color:var(--muted);font-weight:400;letter-spacing:.04em;text-transform:none;margin-left:.6em}
main{padding:44px 0 56px}
.dach{font:600 .78rem/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 14px;padding-left:12px;border-left:3px solid var(--akzent)}
h1{font-size:clamp(2rem,6vw,3rem);line-height:1.12;margin:0 0 18px;text-wrap:balance;letter-spacing:-.01em}
h2{font-size:1.45rem;line-height:1.25;margin:2.4em 0 .5em;text-wrap:balance}
p{margin:0 0 1.1em}
.einleitung{font-size:1.2rem;line-height:1.55;color:var(--muted)}
a{color:inherit;text-decoration-color:var(--akzent);text-underline-offset:3px}
.video{margin:34px 0;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.video .rahmen{position:relative;aspect-ratio:16/9;display:grid;place-items:center;text-align:center;padding:20px}
.video iframe{position:absolute;inset:0;width:100%%;height:100%%;border:0}
.video small{display:block;color:var(--muted);font:.8rem/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;margin-top:12px;max-width:34em}
button,.knopf{font:600 1rem/1 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--knopf);color:var(--auf-knopf);border:0;border-radius:999px;padding:15px 26px;cursor:pointer;text-decoration:none;display:inline-block}
button:focus-visible,.knopf:focus-visible,a:focus-visible{outline:3px solid var(--akzent);outline-offset:3px}
.marke{font:600 .78rem/1 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--muted);text-decoration:underline;text-decoration-color:var(--akzent);text-underline-offset:3px;margin-right:.6em;white-space:nowrap;font-variant-numeric:tabular-nums}
.punkte{list-style:none;padding:0;margin:30px 0;display:grid;gap:12px}
.punkte li{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--akzent);border-radius:10px;padding:14px 18px}
ul.liste{padding-left:1.2em;margin:0 0 1.1em}
ul.liste li{margin-bottom:.4em}
.held{padding:20px 0 8px}
.ruf{margin:44px 0 0;padding:34px 26px;background:var(--paper);border:1px solid var(--line);border-radius:14px;text-align:center}
.ruf p{font-size:1.15rem;margin-bottom:20px}
.quelle{margin-top:44px;padding:16px 18px;border:1px dashed var(--line);border-radius:10px;color:var(--muted);font:.9rem/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.intern{background:var(--ink);color:var(--bg);font:600 .9rem/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;padding:10px 20px;text-align:center}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--muted);font:.88rem/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
footer a{margin-right:1.2em}
footer .schluss{font:italic 1.05rem/1.4 Georgia,serif;color:var(--ink);margin:0 0 8px}
"""


def farben(palette):
    return "".join(f"--{k.replace('_', '-')}:{v};" for k, v in palette.items())


def absatz_html(text):
    return "".join(f"<p>{e(teil.strip())}</p>" for teil in re.split(r"\n\s*\n", str(text)) if teil.strip())


def marke_html(video, sek):
    if sek is None:
        return ""
    return (f'<a class="marke" href="{e(video["link"])}&amp;t={int(sek)}s" rel="noopener" '
            f'title="Im Video an diese Stelle springen">{zeit(sek)}</a>')


def video_html(video):
    vid = e(video["id"])
    return f"""<div class="video"><div class="rahmen" id="video">
<div><button type="button" id="video-laden">Video abspielen</button>
<small>Das Video kommt von YouTube. Erst wenn du klickst, wird es geladen – dabei gehen Daten an YouTube/Google.</small></div>
</div></div>
<script>
document.getElementById('video-laden').addEventListener('click',function(){{
  var f=document.createElement('iframe');
  f.src='https://www.youtube-nocookie.com/embed/{vid}?autoplay=1';
  f.title={json.dumps(video["titel"], ensure_ascii=False).replace("</", "<\\/")};
  f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
  f.allowFullscreen=true;
  var r=document.getElementById('video');r.innerHTML='';r.appendChild(f);
}});
</script>"""


def abschnitte_html(seite, video):
    teile = []
    for ab in seite.get("abschnitte") or []:
        if ab.get("ueberschrift"):
            teile.append(f"<h2>{e(ab['ueberschrift'])}</h2>")
        if "absaetze" in ab:  # aufbereitetes Transkript: jeder Absatz mit Zeitmarke
            for x in ab["absaetze"]:
                teile.append(f"<p>{marke_html(video, x['start'])}{e(x['text'])}</p>")
        else:
            if ab.get("zeit") is not None and ab.get("ueberschrift"):
                teile.append(f"<p>{marke_html(video, ab['zeit'])}</p>")
            teile.append(absatz_html(ab.get("text", "")))
            if ab.get("liste"):
                teile.append('<ul class="liste">' + "".join(f"<li>{e(p)}</li>" for p in ab["liste"]) + "</ul>")
    return "\n".join(teile)


def punkte_html(seite):
    punkte = seite.get("kernpunkte") or []
    return ('<ul class="punkte">' + "".join(f"<li>{e(p)}</li>" for p in punkte) + "</ul>") if punkte else ""


def ruf_html(seite):
    knopf = seite.get("knopf") or {}
    link = sicherer_link(knopf.get("link"))
    if not (knopf.get("text") and link):
        return ""
    satz = f"<p>{e(knopf['satz'])}</p>" if knopf.get("satz") else ""
    return f'<div class="ruf">{satz}<a class="knopf" href="{e(link)}">{e(knopf["text"])}</a></div>'


def quelle_html(video, roh=False):
    kanal = e(video.get("kanal") or "unbekannt")
    if video.get("kanal_link"):
        kanal = f'<a href="{e(video["kanal_link"])}" rel="noopener">{kanal}</a>'
    if video.get("eigenes"):
        return ""
    if roh:
        return (f'<p class="quelle">Das ist das Transkript vom Video '
                f'<a href="{e(video["link"])}" rel="noopener">„{e(video["titel"])}“</a> von {kanal}. '
                f'Das Video und der Text gehören {kanal}.</p>')
    return (f'<p class="quelle">Die Seite fasst mit eigenen Worten zusammen, worum es im Video '
            f'<a href="{e(video["link"])}" rel="noopener">„{e(video["titel"])}“</a> von {kanal} geht. '
            f'Das Video und alle Rechte daran gehören {kanal}.</p>')


def seite_html(seite, video, marke_name):
    marke = MARKEN[marke_name]
    art = seite.get("art", "artikel")
    roh = bool(seite.get("roh"))
    intern = roh and not video.get("eigenes")
    titel = seite.get("titel") or video["titel"]
    einleitung = f'<div class="einleitung">{absatz_html(seite["einleitung"])}</div>' if seite.get("einleitung") else ""
    dach = seite.get("dach") or {"artikel": "Zum Nachlesen", "landingpage": "", "kurz": "Kurz und knapp"}[art]
    if roh:
        dach = "Transkript zum Nachlesen"
    dach_h = f'<p class="dach">{e(dach)}</p>' if dach else ""
    mit_video = seite.get("video_einbetten", True)
    v = video_html(video) if mit_video else ""

    if art == "landingpage":
        inhalt = (f'<div class="held">{dach_h}<h1>{e(titel)}</h1>{einleitung}</div>'
                  f"{punkte_html(seite)}{v}{abschnitte_html(seite, video)}{ruf_html(seite)}")
    elif art == "kurz":
        inhalt = f"{dach_h}<h1>{e(titel)}</h1>{einleitung}{punkte_html(seite)}{v}{ruf_html(seite)}"
    else:
        inhalt = (f"{dach_h}<h1>{e(titel)}</h1>{einleitung}{v}{punkte_html(seite)}"
                  f"{abschnitte_html(seite, video)}{ruf_html(seite)}")
    inhalt += quelle_html(video, roh)

    banner = ('<div class="intern">Nur intern: Das ist das Transkript von einem fremden Video. '
              'So nicht veröffentlichen.</div>') if intern else ""
    kopf_link = f'<a class="absender" href="{e(marke["web"])}">' if marke["web"] else '<span class="absender">'
    kopf_ende = "</a>" if marke["web"] else "</span>"
    fuss = []
    if marke["schluss"]:
        fuss.append(f'<p class="schluss">{e(marke["schluss"])}</p>')
    links = []
    if marke["web"]:
        links.append(f'<a href="{e(marke["web"])}">{e(marke["web"].split("//")[-1].replace("www.", ""))}</a>')
    for name in ("impressum", "datenschutz"):
        ziel = sicherer_link(seite.get(name))
        if ziel:
            links.append(f'<a href="{e(ziel)}">{name.capitalize()}</a>')
    fuss.append(f'<p>{e(marke["name"])} · {e(marke["zeile"])}</p>')
    if links:
        fuss.append("<p>" + "".join(links) + "</p>")
    beschreibung = seite.get("beschreibung") or (re.split(r"\n\s*\n", seite.get("einleitung", ""))[0] if seite.get("einleitung") else titel)
    css = CSS % dict(hell=farben(marke["hell"]), dunkel=farben(marke["dunkel"]))
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)} · {e(marke["name"])}</title>
<meta name="description" content="{e(beschreibung[:160])}">
{'<meta name="robots" content="noindex, nofollow">' if intern else ''}
<meta name="theme-color" content="{marke['hell']['bg']}">
<style>{css}</style>
</head>
<body>
{banner}
<header class="kopf"><div class="wrap">{kopf_link}{e(marke["name"])}<span>{e(marke["zeile"])}</span>{kopf_ende}</div></header>
<main><div class="wrap">
{inhalt}
</div></main>
<footer><div class="wrap">{"".join(fuss)}</div></footer>
</body>
</html>
"""


def bauen(a):
    ordner = Path(a.ordner)
    if not (ordner / "video.json").exists():
        sys.exit(f"In {ordner} liegt kein video.json. Erst `holen` laufen lassen.")
    video = json.loads((ordner / "video.json").read_text(encoding="utf-8"))
    plan = ordner / "seite.json"
    if plan.exists() and not a.roh:
        seite = json.loads(plan.read_text(encoding="utf-8"))
    else:
        zeilen = json.loads((ordner / "transkript.json").read_text(encoding="utf-8"))
        seite = roh_seite(video, zeilen)
        if a.art and a.art != "artikel":
            sys.exit("Landingpage und Kurzfassung brauchen 'ne seite.json (umgeschriebener Text). "
                     "Ohne die geht nur das aufbereitete Transkript als Artikel.")
    if a.art:
        seite["art"] = a.art
    if seite.get("art", "artikel") not in ARTEN:
        sys.exit(f"Die Art '{seite.get('art')}' kenn ich nicht. Geht: {', '.join(ARTEN)}")
    marke = a.marke or seite.get("marke") or "pottpic"
    if marke not in MARKEN:
        sys.exit(f"Die Marke '{marke}' kenn ich nicht. Geht: {', '.join(MARKEN)}")
    name = a.datei or ("transkript.html" if seite.get("roh") else "index.html")
    ziel = ordner / name
    ziel.write_text(seite_html(seite, video, marke), encoding="utf-8")
    hinweis = ""
    if seite.get("roh") and not video.get("eigenes"):
        hinweis = " (fremdes Video: nur intern, mit Hinweis-Balken und ohne Google-Index)"
    print(f"Seite gebaut: {ziel} · {seite.get('art', 'artikel')} · {marke}{hinweis}")
    return ziel


def main():
    p = argparse.ArgumentParser(description="Seiten-Werkstatt: YouTube-Transkript holen und Webseite bauen.")
    sub = p.add_subparsers(dest="befehl", required=True)
    h = sub.add_parser("holen", help="Transkript von einem YouTube-Video holen")
    h.add_argument("link")
    h.add_argument("--sprache", default="de")
    h.add_argument("--eigenes", choices=("ja", "nein"), help="Ist es Monis eigenes Video? (sonst nach Kanalname)")
    h.add_argument("--text", help="Plan B: Textdatei mit kopiertem Transkript")
    h.add_argument("--titel")
    h.add_argument("--kanal")
    h.add_argument("--ziel", help="Zielordner (sonst seiten/JJJJ-MM-TT-titel)")
    h.set_defaults(lauf=holen)
    b = sub.add_parser("bauen", help="Aus dem Ordner eine Webseite bauen")
    b.add_argument("ordner")
    b.add_argument("--art", choices=ARTEN)
    b.add_argument("--marke", choices=tuple(MARKEN))
    b.add_argument("--roh", action="store_true", help="seite.json ignorieren, nur das Transkript aufbereiten")
    b.add_argument("--datei", help="Dateiname der Ausgabe (sonst index.html bzw. transkript.html)")
    b.set_defaults(lauf=bauen)
    a = p.parse_args()
    a.lauf(a)


if __name__ == "__main__":
    main()

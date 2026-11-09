#!/usr/bin/env python3
"""Reel-Werkstatt: macht aus einem Foto-Ordner ein fertiges 9:16-Reel (stumm) plus Cover.

Aufruf:
    python3 pottpic-team/reel-werkstatt/reel_bauen.py <ordner> [--marke pottpic|derner] [--ziel <ordner>]

Im Ordner liegen die Fotos (jpg/jpeg/png/webp/heic*) und optional eine `reel.json`:
{
  "titel": "kurzname",                 # Dateiname der Ausgabe
  "hook": "Text in den ersten 2 Sekunden",
  "folien": [ {"foto": "01.jpg", "text": "Einblendung"}, ... ],   # optional, sonst alle Fotos nach Name
  "schluss": "Für Erinnerungen, die bleiben.",
  "sekunden_pro_foto": 2.6
}
Ohne `reel.json` nimmt das Skript alle Fotos nach Dateiname, ohne Texte.
(*HEIC nur, wenn pillow-heif installiert ist – sonst vorher als JPG exportieren.)

Kosten: 0 €. Läuft lokal mit Pillow + ffmpeg. Keine Musik (Sound wählt Moni in der App).
"""
import argparse, json, math, os, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30
HIER = Path(__file__).resolve().parent

MARKEN = {
    # Pottpic: Navy + Gold auf Creme. Eigener Look: Foto als Abzug mit Rand, leicht schräg.
    "pottpic": dict(bg=(250, 245, 236), ink=(31, 42, 68), akzent=(201, 162, 74), rand=(255, 253, 248),
                    absender="pottpic", zeile2="Hundefotografie im Ruhrgebiet", web="pottpic.de",
                    schluss="Für Erinnerungen, die bleiben."),
    # Derner Schnauzenbande: Creme + Dunkelgrün (nie mit Pottpic-Farben mischen).
    "derner": dict(bg=(250, 241, 224), ink=(47, 93, 80), akzent=(47, 93, 80), rand=(255, 252, 244),
                   absender="Derner Schnauzenbande", zeile2="Hundesport in Dortmund-Derne", web="",
                   schluss="Komm vorbei – wir freu'n uns auf euch."),
}

BILD_ENDUNGEN = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}


def schrift(gewicht, groesse):
    """Eigene Schrift aus schrift/ nehmen (z. B. Caveat), sonst Inter, sonst DejaVu."""
    eigene = sorted((HIER / "schrift").glob("*.[ot]tf")) if (HIER / "schrift").exists() else []
    kandidaten = []
    if gewicht == "hand" and eigene:
        kandidaten.append(str(eigene[0]))
    kandidaten += {
        "fett": ["/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "hand": ["/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "normal": ["/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    }[gewicht]
    for k in kandidaten:
        if os.path.exists(k):
            return ImageFont.truetype(k, groesse)
    return ImageFont.load_default()


def ohne_emoji(text):
    """Emojis kann die Schrift nicht – die kommen in die Caption, nicht ins Bild."""
    return " ".join("".join(c for c in text if ord(c) < 0x2190 or c in "♥").split(" ")).strip()


def umbrechen(draw, text, font, breite):
    text = ohne_emoji(text)
    zeilen = []
    for absatz in text.split("\n"):
        zeile = ""
        for wort in absatz.split():
            probe = (zeile + " " + wort).strip()
            if draw.textlength(probe, font=font) <= breite:
                zeile = probe
            else:
                if zeile:
                    zeilen.append(zeile)
                zeile = wort
        zeilen.append(zeile)
    return zeilen


def text_block(draw, text, font, mitte_y, farbe, breite=W - 160, abstand=1.18):
    zeilen = umbrechen(draw, text, font, breite)
    hoehe = font.size * abstand
    y = mitte_y - hoehe * len(zeilen) / 2
    for z in zeilen:
        draw.text((W / 2, y + hoehe / 2), z, font=font, fill=farbe, anchor="mm")
        y += hoehe


def foto_laden(pfad):
    if pfad.suffix.lower() in {".heic", ".heif"}:
        try:
            import pillow_heif  # noqa
            pillow_heif.register_heif_opener()
        except ImportError:
            sys.exit(f"{pfad.name}: HEIC kann ich hier nicht lesen – bitte als JPG exportieren.")
    return ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")


def hintergrund(m):
    """Creme-Papier mit ganz leichtem Korn – sieht nach Abzug aus, nicht nach Vorlage."""
    rnd = random.Random(7)
    bg = Image.new("RGB", (W, H), m["bg"])
    korn = Image.effect_noise((W // 4, H // 4), 10).resize((W, H)).convert("L")
    bg = Image.blend(bg, Image.merge("RGB", [korn] * 3), 0.035)
    d = ImageDraw.Draw(bg)
    d.text((70, 92), m["absender"], font=schrift("fett", 40), fill=m["ink"], anchor="lm")
    d.line([(70, 128), (70 + rnd.randint(150, 190), 128)], fill=m["akzent"], width=5)
    return bg


# Abzug: Foto 900x1125 (4:5) mit Rand, leicht gedreht – abwechselnd links/rechts.
FOTO_W, FOTO_H, RAND = 880, 1100, 26


def abzug(foto, t, nr, m):
    """Ken-Burns im Abzug: langsam reinzoomen, Richtung wechselt pro Foto."""
    zoom = 1.0 + 0.08 * t
    fw, fh = foto.size
    ziel = FOTO_W / FOTO_H
    if fw / fh > ziel:
        cw, ch = fh * ziel, fh
    else:
        cw, ch = fw, fw / ziel
    cw, ch = cw / zoom, ch / zoom
    richtung = [(0.5, 0.45), (0.42, 0.5), (0.58, 0.5), (0.5, 0.55)][nr % 4]
    cx = (fw - cw) * (0.5 + (richtung[0] - 0.5) * t * 2)
    cy = (fh - ch) * (0.5 + (richtung[1] - 0.5) * t * 2)
    bild = foto.crop((int(cx), int(cy), int(cx + cw), int(cy + ch))).resize((FOTO_W, FOTO_H), Image.LANCZOS)
    karte = Image.new("RGBA", (FOTO_W + 2 * RAND, FOTO_H + 2 * RAND + 70), m["rand"] + (255,))
    karte.paste(bild, (RAND, RAND))
    winkel = [-2.2, 1.6, -1.2, 2.0][nr % 4]
    return karte.rotate(winkel, resample=Image.BICUBIC, expand=True)


def schatten(karte):
    a = karte.split()[3]
    s = Image.new("RGBA", karte.size, (0, 0, 0, 0))
    s.putalpha(a.point(lambda v: int(v * 0.28)))
    return s.filter(ImageFilter.GaussianBlur(18))


def folie_bild(bg, foto, text, t, nr, m, hook=False):
    f = bg.copy()
    karte = abzug(foto, t, nr, m)
    x = (W - karte.width) // 2
    y = 200 if text else 330
    f.paste(schatten(karte), (x + 10, y + 22), schatten(karte))
    f.paste(karte, (x, y), karte)
    d = ImageDraw.Draw(f)
    if text:
        groesse = 74 if hook else 64
        text_block(d, text, schrift("hand", groesse), 1560, m["ink"])
    return f


def schluss_bild(bg, m, schluss):
    f = bg.copy()
    d = ImageDraw.Draw(f)
    text_block(d, schluss, schrift("hand", 84), 860, m["ink"])
    d.line([(W / 2 - 90, 1010), (W / 2 + 90, 1010)], fill=m["akzent"], width=6)
    d.text((W / 2, 1100), m["zeile2"], font=schrift("normal", 42), fill=m["ink"], anchor="mm")
    if m["web"]:
        d.text((W / 2, 1170), m["web"], font=schrift("fett", 48), fill=m["akzent"], anchor="mm")
    return f


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ordner")
    ap.add_argument("--marke", choices=MARKEN, default=None)
    ap.add_argument("--ziel", default=None)
    a = ap.parse_args()

    ordner = Path(a.ordner)
    plan = {}
    if (ordner / "reel.json").exists():
        plan = json.loads((ordner / "reel.json").read_text(encoding="utf-8"))
    marke = a.marke or plan.get("marke", "pottpic")
    m = MARKEN[marke]
    fotos = sorted(p for p in ordner.iterdir() if p.suffix.lower() in BILD_ENDUNGEN)
    if not fotos:
        sys.exit(f"Keine Fotos in {ordner} gefunden.")

    folien = plan.get("folien") or [{"foto": p.name, "text": ""} for p in fotos]
    # Fotos, die im Plan fehlen, hinten dranhängen; fehlende Dateien → nächstes freies Foto nehmen.
    benutzt = {f.get("foto") for f in folien}
    frei = [p.name for p in fotos if p.name not in benutzt]
    for f in folien:
        if not f.get("foto") or not (ordner / f["foto"]).exists():
            if not frei:
                sys.exit("Im Plan stehen mehr Folien als Fotos im Ordner. Bitte Fotos nachlegen.")
            f["foto"] = frei.pop(0)
    folien += [{"foto": n, "text": ""} for n in frei]

    hook = plan.get("hook", "")
    schluss = plan.get("schluss", m["schluss"])
    sek = float(plan.get("sekunden_pro_foto", 2.6))
    titel = plan.get("titel", ordner.name)
    ziel = Path(a.ziel) if a.ziel else ordner
    ziel.mkdir(parents=True, exist_ok=True)
    video = ziel / f"{titel}-reel.mp4"
    cover = ziel / f"{titel}-cover.jpg"

    bg = hintergrund(m)
    geladen = [foto_laden(ordner / f["foto"]) for f in folien]
    # Hook steht auf dem ersten Foto (statt dessen Text), damit's ab Sekunde 0 losgeht.
    texte = [f.get("text", "") for f in folien]
    if hook:
        texte[0] = hook

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ueber = int(0.35 * FPS)  # Überblendung
    n = int(sek * FPS)

    def frames_folie(i):
        for k in range(n):
            yield folie_bild(bg, geladen[i], texte[i], k / max(n - 1, 1), i, m, hook=(i == 0 and bool(hook)))

    letzte = None
    for i in range(len(folien)):
        for k, fr in enumerate(frames_folie(i)):
            if letzte is not None and k < ueber:
                fr = Image.blend(letzte, fr, ease(k / ueber))
            ff.stdin.write(fr.tobytes())
            if k == n - 1:
                letzte = fr
        if i == 0:
            fr0 = folie_bild(bg, geladen[0], texte[0], 0.15, 0, m, hook=bool(hook))
            fr0.save(cover, quality=92)
    ende = schluss_bild(bg, m, schluss)
    for k in range(int(2.4 * FPS)):
        fr = Image.blend(letzte, ende, ease(k / ueber)) if k < ueber else ende
        ff.stdin.write(fr.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg hat gemeckert – Reel nicht fertig.")
    dauer = len(folien) * sek + 2.4
    print(f"Fertig: {video} ({dauer:.1f} s, {len(folien)} Fotos, Marke {marke})")
    print(f"Cover:  {cover}")


if __name__ == "__main__":
    main()

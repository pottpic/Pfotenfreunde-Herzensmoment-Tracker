#!/usr/bin/env python3
"""Einblende-Werkstatt: legt "5 Punkte"-Einblendungen im Pottpic-Look über ein fertiges Reel.

  python3 einblenden.py plan.json --video mein-reel.mp4      -> fertiges Reel mit Einblendungen
  python3 einblenden.py plan.json --demo                      -> Vorschau mit Platzhalter-Hintergrund
  zusätzlich immer: <titel>-nur-einblendungen.mov (transparent, zum Drüberlegen in CapCut/Edits)

Kostet nix, braucht nur Python (Pillow) und ffmpeg.
"""
import argparse, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
HIER = Path(__file__).resolve().parent
SCHRIFT = HIER / "schrift"

CREME = (250, 245, 236)
NAVY = (31, 42, 68)
GOLD = (201, 162, 74)
WEISS = (255, 253, 248)

X = 84            # linker Rand – rechts sind die Insta-Knöpfe, unten die Caption, also oben links bleiben
_fonts = {}


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(SCHRIFT / f"{name}.ttf"), size)
    return _fonts[key]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = max(0.0, min(1.0, x))
    c = 1.5
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def schatten(img, radius=18, alpha=90, versatz=(0, 10)):
    """Weicher Schatten unter einem RGBA-Element."""
    pad = radius * 3
    s = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    maske = img.split()[3].point(lambda a: a * alpha // 255)
    s.paste((0, 0, 0, 255), (pad + versatz[0], pad + versatz[1]), maske)
    s = s.filter(ImageFilter.GaussianBlur(radius))
    s.alpha_composite(img, (pad, pad))
    return s, pad


def text_mit_schatten(text, f, farbe, schatten_alpha=150):
    l, t, r, b = f.getbbox(text)
    img = Image.new("RGBA", (r + 8, b + 8), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4, 4), text, font=f, fill=farbe)
    return schatten(img, radius=10, alpha=schatten_alpha, versatz=(0, 4))


def umbrechen(text, f, breite):
    zeilen, aktuell = [], ""
    for wort in text.split():
        probe = (aktuell + " " + wort).strip()
        if f.getlength(probe) <= breite or not aktuell:
            aktuell = probe
        else:
            zeilen.append(aktuell)
            aktuell = wort
    if aktuell:
        zeilen.append(aktuell)
    return zeilen


def einblenden(layer, el, pos, a, dy=0, scale=1.0):
    """Element mit Deckkraft a (0..1), Versatz dy und Skalierung auf die Ebene setzen."""
    if a <= 0.01:
        return
    img, pad = el
    if scale != 1.0:
        nw, nh = max(1, int(img.width * scale)), max(1, int(img.height * scale))
        cx, cy = pos[0] - pad + img.width / 2, pos[1] - pad + img.height / 2
        img = img.resize((nw, nh), Image.LANCZOS)
        ox, oy = int(cx - nw / 2), int(cy - nh / 2 + dy)
    else:
        ox, oy = int(pos[0] - pad), int(pos[1] - pad + dy)
    if a < 1:
        r, g, b, al = img.split()
        img = Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))
    layer.alpha_composite(img, (ox, oy)) if 0 <= ox and 0 <= oy and ox + img.width <= W and oy + img.height <= H else _sicher(layer, img, ox, oy)


def _sicher(layer, img, ox, oy):
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(img, (ox, oy), img)
    layer.alpha_composite(tmp)


# ---------- Bausteine ----------

def zahl_karte(n):
    gr = 230
    img = Image.new("RGBA", (gr, gr), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, gr - 1, gr - 1), radius=44, fill=WEISS + (255,))
    d.text((gr / 2, gr / 2 + 6), str(n), font=font("Caveat-SemiBold", 190), fill=GOLD, anchor="mm")
    return schatten(img, radius=22, alpha=110, versatz=(0, 12))


def chip(text, bg=NAVY, fg=WEISS, groesse=46):
    f = font("Montserrat-ExtraBold", groesse)
    tw = f.getlength(text)
    h = int(groesse * 1.75)
    img = Image.new("RGBA", (int(tw + groesse * 1.3), h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, h - 1), radius=h // 2, fill=bg + (255,))
    d.text((img.width / 2, h / 2 + 1), text, font=f, fill=fg, anchor="mm")
    return schatten(img, radius=14, alpha=90, versatz=(0, 6))


def hand_zeilen(text, groesse=78, breite=W - 2 * X):
    f = font("Caveat-SemiBold", groesse)
    return [text_mit_schatten(z, f, WEISS, schatten_alpha=200) for z in umbrechen(text, f, breite)]


def intro_karte(p):
    """Creme-Karte oben: Kicker, Titel mit Handschrift-Wort, darunter die 5er-Leiste (ohne Punkte)."""
    bw = W - 2 * 60
    img = Image.new("RGBA", (bw, 640), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, bw - 1, 639), radius=48, fill=CREME + (244,))
    k = font("Montserrat-SemiBold", 26)
    kicker = " ".join(p["kicker"].upper())
    d.text((64, 70), kicker, font=k, fill=GOLD, anchor="lm")
    f1 = font("Montserrat-ExtraBold", 92)
    fh = font("Caveat-SemiBold", 104)
    y = 150
    d.text((60, y), p["titel_1"], font=f1, fill=NAVY, anchor="lt")
    x2 = 60 + f1.getlength(p["titel_1"]) + 22
    d.text((x2, y + 52), p["titel_hand"], font=fh, fill=GOLD, anchor="lm")
    d.text((60, y + 108), p["titel_2"], font=f1, fill=NAVY, anchor="lt")
    return img


def leiste_punkt(i, label, letzter, aktiv=True):
    gr = 92
    img = Image.new("RGBA", (190, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = 95
    fill = NAVY if letzter else WEISS
    d.ellipse((cx - gr / 2, 4, cx + gr / 2, 4 + gr), fill=fill + (255,), outline=(225, 215, 196, 255), width=3)
    d.text((cx, 4 + gr / 2 + 4), str(i), font=font("Caveat-SemiBold", 70), fill=(GOLD if not letzter else WEISS), anchor="mm")
    d.text((cx, gr + 34), label, font=font("Montserrat-SemiBold", 25), fill=NAVY, anchor="mm")
    return img


def fortschritt(aktiv_idx, n=5):
    """Kleine Punkte-Leiste oben während der Punkte."""
    img = Image.new("RGBA", (n * 46, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i in range(n):
        x = i * 46 + 15
        if i == aktiv_idx:
            d.rounded_rectangle((x - 15, 3, x + 21, 27), radius=12, fill=GOLD + (255,))
        else:
            d.ellipse((x - 9, 6, x + 9, 24), fill=WEISS + ((255,) if i < aktiv_idx else (140,)))
    return schatten(img, radius=6, alpha=120, versatz=(0, 2))


def outro_karte(p):
    bw = W - 2 * 60
    f1 = font("Montserrat-ExtraBold", 74)
    fh = font("Caveat-SemiBold", 78)
    zeilen = umbrechen(p["outro_frage"], f1, bw - 120)
    hand = umbrechen(p["outro_hand"], fh, bw - 120)
    hoehe = 110 + len(zeilen) * 88 + 20 + len(hand) * 82 + 150
    img = Image.new("RGBA", (bw, hoehe), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, bw - 1, hoehe - 1), radius=48, fill=CREME + (246,))
    y = 90
    for z in zeilen:
        d.text((bw / 2, y), z, font=f1, fill=NAVY, anchor="mm"); y += 88
    y += 20
    for z in hand:
        d.text((bw / 2, y), z, font=fh, fill=GOLD, anchor="mm"); y += 82
    y += 40
    d.line((bw / 2 - 60, y - 20, bw / 2 + 60, y - 20), fill=GOLD, width=3)
    d.text((bw / 2, y + 30), p.get("absender", "pottpic.de"), font=font("Montserrat-SemiBold", 34), fill=NAVY, anchor="mm")
    return schatten(img, radius=26, alpha=100, versatz=(0, 14))


# ---------- Ablauf ----------

def zeitplan(p, dauer):
    intro = p.get("intro_sekunden", 3.4)
    outro = p.get("outro_sekunden", 3.0)
    n = len(p["punkte"])
    seg = (dauer - intro - outro) / n
    if seg < 1.8:
        sys.exit(f"Video zu kurz ({dauer:.1f}s) – für {n} Punkte braucht's mindestens {intro + outro + n * 1.8:.0f} Sekunden.")
    return intro, outro, seg


def baue_ebenen(p, dauer):
    intro, outro, seg = zeitplan(p, dauer)
    n = len(p["punkte"])
    karte_intro = intro_karte(p)
    karte_intro_s = schatten(karte_intro, radius=26, alpha=100, versatz=(0, 14))
    leiste = [leiste_punkt(i + 1, pk["kurz"], i == n - 1) for i, pk in enumerate(p["punkte"])]
    punkte = []
    for i, pk in enumerate(p["punkte"]):
        punkte.append(dict(
            karte=zahl_karte(i + 1),
            vorlauf=chip(p.get("letzter_vorlauf", "Zum Schluss"), bg=GOLD, fg=WEISS, groesse=30) if i == n - 1 else None,
            chip=chip(pk["titel"]),
            hand=hand_zeilen(pk["satz"]),
        ))
    fort = [fortschritt(i, n) for i in range(n)]
    karte_outro = outro_karte(p)
    intro_y = 210
    # Weicher dunkler Verlauf oben, damit die weiße Handschrift auch auf hellem Laub lesbar bleibt
    verlauf = Image.new("RGBA", (W, 1000), (0, 0, 0, 0))
    vd = ImageDraw.Draw(verlauf)
    for yy in range(1000):
        vd.line((0, yy, W, yy), fill=(20, 16, 12, int(120 * (1 - yy / 1000) ** 1.6)))

    def frame(t):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # Intro
        if t < intro + 0.4:
            raus = ease((t - intro) / 0.4) if t > intro else 0
            a = ease(t / 0.45) * (1 - raus)
            einblenden(layer, karte_intro_s, (60, intro_y), a, dy=(1 - ease(t / 0.5)) * 40 - raus * 30)
            # Leiste: Punkte nacheinander
            for i, el in enumerate(leiste):
                start = 0.7 + i * 0.28
                ai = ease((t - start) / 0.3) * (1 - raus)
                x = 60 + 20 + i * ((W - 120 - 40 - 190) / (n - 1))
                einblenden(layer, (el, 0), (x, intro_y + 420), ai, dy=(1 - ease((t - start) / 0.3)) * 20, scale=0.85 + 0.15 * ease_back((t - start) / 0.35))
            # gestrichelte Linie wächst mit
            lw = ease((t - 0.6) / 1.5) * (1 - raus)
            if lw > 0:
                d = ImageDraw.Draw(layer)
                x0, x1 = 60 + 20 + 95 + 46, 60 + 20 + (n - 1) * ((W - 120 - 40 - 190) / (n - 1)) + 95 - 46
                xe = x0 + (x1 - x0) * lw
                for xx in range(int(x0), int(xe), 18):
                    d.line((xx, intro_y + 420 + 50, min(xx + 9, xe), intro_y + 420 + 50), fill=GOLD + (int(220 * (1 - raus)),), width=3)
        # Punkte
        s_end = intro + n * seg
        va = ease((t - intro + 0.2) / 0.4) * (1 - ease((t - s_end) / 0.4))
        einblenden(layer, (verlauf, 0), (0, 0), va)
        for i, pk in enumerate(punkte):
            s0 = intro + i * seg
            s1 = s0 + seg
            if s0 - 0.05 <= t <= s1 + 0.35:
                lt = t - s0
                raus = ease((t - s1 + 0.3) / 0.3) if t > s1 - 0.3 else 0
                y = 300
                if pk["vorlauf"]:
                    a = ease((lt - 0.0) / 0.3) * (1 - raus)
                    einblenden(layer, pk["vorlauf"], (X, y - 90), a, dy=(1 - ease(lt / 0.3)) * 16)
                einblenden(layer, pk["karte"], (X, y), (1 - raus) * ease(lt / 0.2), scale=0.6 + 0.4 * ease_back(lt / 0.4))
                a = ease((lt - 0.35) / 0.3) * (1 - raus)
                einblenden(layer, pk["chip"], (X, y + 270), a, dy=(1 - ease((lt - 0.35) / 0.3)) * 24)
                for j, z in enumerate(pk["hand"]):
                    st = 0.65 + j * 0.15
                    a = ease((lt - st) / 0.35) * (1 - raus)
                    einblenden(layer, z, (X + 4, y + 380 + j * 86), a, dy=(1 - ease((lt - st) / 0.35)) * 18)
                einblenden(layer, fort[i], (X, 150), (1 - raus) * ease(lt / 0.3))
        # Outro
        so = dauer - outro
        if t >= so:
            lt = t - so
            einblenden(layer, karte_outro, (60, 520), ease(lt / 0.4), dy=(1 - ease(lt / 0.45)) * 50, scale=0.94 + 0.06 * ease(lt / 0.45))
        return layer

    return frame


def dauer_von(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def platzhalter(ziel, dauer):
    """Warmer Herbst-Hintergrund mit Hinweis – nur für die Vorschau, bis Monis Reel da ist."""
    import random
    random.seed(7)
    bw, bh = 1400, 2400
    img = Image.new("RGB", (bw, bh), (120, 70, 35))
    d = ImageDraw.Draw(img)
    for y in range(bh):
        k = y / bh
        d.line((0, y, bw, y), fill=(int(150 - 70 * k), int(95 - 45 * k), int(45 - 20 * k)))
    for _ in range(260):
        x, y, r = random.randint(0, bw), random.randint(0, bh), random.randint(20, 110)
        c = random.choice([(214, 128, 40), (190, 80, 30), (235, 175, 70), (140, 60, 25), (240, 200, 120)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    img = img.filter(ImageFilter.GaussianBlur(28))
    d = ImageDraw.Draw(img)
    d.text((bw / 2, bh * 0.80), "Platzhalter – hier kommt dein Reel rein", font=font("Montserrat-SemiBold", 34),
           fill=(255, 240, 220), anchor="mm")
    p = ziel.with_suffix(".png")
    img.save(p)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(p), "-t", f"{dauer}", "-r", str(FPS),
                    "-vf", f"crop={W}:{H}:'(iw-{W})/2+60*sin(t/3)':'(ih-{H})/2-120*t/{dauer}'",
                    "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "20", str(ziel)], check=True)
    p.unlink()
    return ziel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--video", help="Monis fertiges Reel")
    ap.add_argument("--demo", action="store_true", help="Vorschau mit Platzhalter")
    ap.add_argument("--dauer", type=float, default=19.0, help="Länge der Demo in Sekunden")
    ap.add_argument("--ziel", default=None)
    ap.add_argument("--min-dauer", type=float, default=18.0,
                    help="Ist das Reel kürzer, wird es in Zeitlupe gestreckt (ohne Ton – Sound kommt in der Insta-App drauf)")
    a = ap.parse_args()

    plan_pfad = Path(a.plan)
    p = json.loads(plan_pfad.read_text(encoding="utf-8"))
    ziel = Path(a.ziel or plan_pfad.parent)
    ziel.mkdir(parents=True, exist_ok=True)
    titel = p.get("titel", "einblendungen")

    if a.video:
        quelle = Path(a.video)
        dauer = dauer_von(quelle)
        if dauer < a.min_dauer:
            faktor = a.min_dauer / dauer
            gestreckt = ziel / f"{titel}-zeitlupe.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(quelle), "-an",
                            "-vf", f"setpts={faktor:.4f}*PTS,fps={FPS}", "-c:v", "libx264", "-crf", "16", str(gestreckt)], check=True)
            print(f"Reel war {dauer:.1f}s – auf {a.min_dauer:.0f}s gestreckt (Zeitlupe, ohne Ton).")
            quelle, dauer = gestreckt, dauer_von(gestreckt)
            a.zeitlupe_tmp = gestreckt
    elif a.demo:
        dauer = a.dauer
        quelle = platzhalter(ziel / f"{titel}-platzhalter.mp4", dauer)
    else:
        sys.exit("Entweder --video <reel> oder --demo angeben.")

    frame = baue_ebenen(p, dauer)
    n_frames = int(round(dauer * FPS))

    fertig = ziel / f"{titel}{'-demo' if a.demo and not a.video else ''}.mp4"
    nur = ziel / f"{titel}-nur-einblendungen.mov"
    mix = subprocess.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(quelle),
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-filter_complex",
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac",
        "-shortest", "-movflags", "+faststart", str(fertig)], stdin=subprocess.PIPE)
    alpha = subprocess.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0", "-qscale:v", "11", str(nur)],
        stdin=subprocess.PIPE)
    for i in range(n_frames):
        roh = frame(i / FPS).tobytes()
        mix.stdin.write(roh)
        alpha.stdin.write(roh)
    for pr in (mix, alpha):
        pr.stdin.close()
        pr.wait()
    if (a.demo and not a.video) or getattr(a, "zeitlupe_tmp", None):
        quelle.unlink()
    print(fertig)
    print(nur)


if __name__ == "__main__":
    main()

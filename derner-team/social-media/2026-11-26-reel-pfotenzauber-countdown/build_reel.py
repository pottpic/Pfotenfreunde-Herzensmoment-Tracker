"""Pfotenzauber im Advent – Countdown-Reel aus 5 KI-Bildern: langsame Kamerafahrten, gut lesbar, stumm."""
import math, random, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UP, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
XF = 0.5  # Überblendung in Sekunden

def load(name):
    return Image.open(os.path.join(UP, name)).convert("RGBA")

def ease(x):
    x = min(1, max(0, x))
    return x * x * (3 - 2 * x)

def lerp(a, b, x):
    return a + (b - a) * x

def cam_path(keys):
    """keys: [(t, cx, cy, z)] -> Funktion t -> (cx, cy, z), weich interpoliert."""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1:]
        for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
            if t <= t1:
                x = ease((t - t0) / (t1 - t0)) if t1 > t0 else 1
                return tuple(lerp(p, q, x) for p, q in zip(a, b))
        return keys[-1][1:]
    return f

def render(img, base_scale, cam, bg):
    cx, cy, z = cam
    S = base_scale * z
    layer = img.transform((W, H), Image.AFFINE, (1 / S, 0, cx - (W / 2) / S, 0, 1 / S, cy - (H / 2) / S),
                          resample=Image.BICUBIC)
    out = bg.copy()
    out.alpha_composite(layer)
    return out

# ---------------------------------------------------------------- Szenen (Reihenfolge = Countdown)
scenes = []

def vertical(name, dur, start_c, end_c, z0=1.0, z1=1.06):
    img = load(name)
    s = max(W / img.width, H / img.height)
    bg = Image.new("RGBA", (W, H), (20, 20, 40, 255))
    path = cam_path([(0, *start_c, z0), (dur, *end_c, z1)])
    scenes.append((dur, lambda t: render(img, s, path(t), bg)))

# 1) „Noch zweimal schlafen, Luke!“ – Kamera fährt langsam Richtung Sprechblase
vertical("e5f91a2e-image.png", 4.6, (470, 836), (430, 760))
# 2) „Zählt Dösen auch?“ – Lukes Antwort
vertical("19b49fc0-image.png", 4.2, (470, 860), (470, 700))
# 3) „Lichter an. Morgen geht's los!“
vertical("79778d6c-image.png", 4.2, (470, 760), (500, 820))
# 4) Comic: Rucksack packen – Überblick, dann Bild für Bild
comic = load("00486ce2-image.png")
cs = W / comic.width
cbg = comic.resize((int(comic.width * H / comic.height * 1.05), int(H * 1.05))).filter(ImageFilter.GaussianBlur(34))
cbg = Image.eval(cbg.convert("RGB"), lambda v: int(v * 0.5)).convert("RGBA")
cbg = cbg.crop(((cbg.width - W) // 2, (cbg.height - H) // 2, (cbg.width - W) // 2 + W, (cbg.height - H) // 2 + H))
P1, P2, P3 = (561, 215), (561, 672), (561, 1150)
comic_keys = [(0, 561, 701, 1.0), (1.3, 561, 701, 1.0),
              (2.0, *P1, 1.46), (5.4, *P1, 1.5),
              (6.1, *P2, 1.46), (9.3, *P2, 1.5),
              (10.0, *P3, 1.04), (12.4, *P3, 1.07)]
cpath = cam_path(comic_keys)
scenes.append((12.4, lambda t: render(comic, cs, cpath(t), cbg)))
# 5) „Morgen um drei. Mensch nicht vergessen!“ – Schluss mit Banner
vertical("d6582d00-image.png", 5.8, (470, 760), (470, 900), 1.06, 1.0)

# ---------------------------------------------------------------- Overlays
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 34)
label = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(label)
tw = font.getlength("KI generiert")
x1, y1 = 1046, 1858
x0, y0 = x1 - tw - 44, y1 - 58
d.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(255, 252, 244, 255), outline=(20, 20, 20, 255), width=3)
d.text(((x0 + x1) / 2, (y0 + y1) / 2), "KI generiert", font=font, fill=(15, 15, 15, 255), anchor="mm")

random.seed(5)
SNOW = [(random.uniform(0, W), random.uniform(0, H), random.uniform(35, 80), random.uniform(1.8, 4.2),
         random.uniform(0, 6.28)) for _ in range(38)]

def snow(img, t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    for x0_, y0_, v, r, ph in SNOW:
        y = (y0_ + v * t) % (H + 20) - 10
        x = x0_ + 18 * math.sin(t * 0.9 + ph)
        dd.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 150))
    img.alpha_composite(lay)

# ---------------------------------------------------------------- Zeitleiste mit Überblendungen
starts, t = [], 0.0
for i, (dur, _) in enumerate(scenes):
    starts.append(t)
    t += dur - (XF if i < len(scenes) - 1 else 0)
TOTAL = t

def frame(tg):
    active = [(i, tg - s) for i, s in enumerate(starts) if s <= tg < s + scenes[i][0]]
    i, lt = active[-1]
    img = scenes[i][1](lt)
    if len(active) > 1:
        j, lt2 = active[0]
        prev = scenes[j][1](lt2)
        img = Image.blend(prev, img, ease(lt / XF))
    snow(img, tg)
    # eigenes „KI generiert“ nur beim Comic (die Hochkant-Bilder haben's schon drin)
    CI = 3
    w = 0.0
    for k, lt_ in active:
        if k == CI:
            w = 1.0 if len(active) == 1 else (ease(lt / XF) if k == i else 1 - ease(lt / XF))
    if w > 0:
        lab = label if w >= 1 else Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), label, w)
        img.alpha_composite(lab)
    return img.convert("RGB")

if __name__ == "__main__":
    nfr = int(TOTAL * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                            "-vf", f"fade=in:st=0:d=0.4,fade=out:st={TOTAL - 0.7}:d=0.7",
                            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
                            os.path.join(OUT, "reel.mp4")], stdin=subprocess.PIPE)
    for f in range(nfr):
        enc.stdin.write(frame(f / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    for k, tt in enumerate([2.0, 6.0, 10.0, 13.5, 17.0, 21.0, 24.5, 28.0]):
        frame(min(tt, TOTAL - 0.8)).resize((270, 480)).save(os.path.join(OUT, f"chk_{k}.png"))
    print("ok", round(TOTAL, 2))

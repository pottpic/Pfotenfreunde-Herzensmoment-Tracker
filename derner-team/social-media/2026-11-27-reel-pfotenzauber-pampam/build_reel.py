"""Pfotenzauber im Advent – Pam-pam-Reel: Bilder schießen im Takt rein, Sterne, WOW/BÄM/YEAH/DYNAMIT,
eigener 128-BPM-Beat, Flyer zum Schluss lange sichtbar."""
import math, random, subprocess, sys, os, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UP, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
BPM = 128.0
B = 60 / BPM
TOTAL_BEATS = 64
DUR = TOTAL_BEATS * B
SR = 44100

GREEN = (29, 58, 37)
GREEN2 = (44, 86, 56)
CREAM = (243, 235, 217)
GOLD = (255, 205, 64)
RED = (214, 58, 44)
INK = (35, 18, 10)
FD = "/usr/share/fonts/opentype/inter/"

def up(n):
    return Image.open(os.path.join(UP, n)).convert("RGBA")

def blur_bg(img, dark=0.45):
    s = max(W / img.width, H / img.height) * 1.08
    b = img.resize((int(img.width * s), int(img.height * s))).filter(ImageFilter.GaussianBlur(36))
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    return Image.eval(b.convert("RGB"), lambda v: int(v * dark)).convert("RGBA")

def ease_out(x):
    x = min(1, max(0, x)); return 1 - (1 - x) ** 3

# ---------------------------------------------------------------- Material
V1 = up("a3318b37-image.png")       # Lichter an
V2 = up("fb2804a7-image.png")       # Zählt Dösen auch?
CA = up("a7b7037a-image.png")       # Comic: Menschen geweckt (mit KI-Label)
CB = up("5c611a4c-image.png")       # Comic: Sitz und warten
FLY = up("109efc6c-image.jpg")      # Flyer – immer zuletzt
vs = max(W / V1.width, H / V1.height)
V1s = V1.resize((round(V1.width * vs), round(V1.height * vs)), Image.LANCZOS)
V2s = V2.resize((round(V2.width * vs), round(V2.height * vs)), Image.LANCZOS)
cs = W / CA.width
CY0 = (H - CA.height * cs) / 2
def panels(img, cuts):
    out = []
    for y0, y1 in cuts:
        p = img.crop((0, y0, img.width, y1))
        out.append((p.resize((W, round((y1 - y0) * cs)), Image.LANCZOS), CY0 + y0 * cs))
    return out
PA = panels(CA, [(0, 458), (458, 856), (856, 1402)])
PB = panels(CB, [(0, 447), (447, 865), (865, 1402)])
BG_A, BG_B = blur_bg(CA), blur_bg(CB)
fs = W / FLY.width
FLYs = FLY.resize((W, round(FLY.height * fs)), Image.LANCZOS)
FY0 = (H - FLYs.height) / 2
BG_F = blur_bg(FLY, 0.5)

lab_font = ImageFont.truetype(FD + "Inter-SemiBold.otf", 30)
def ki_label():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tw = lab_font.getlength("KI generiert"); x1, y1 = W - 26, int(CY0 + CA.height * cs) - 14
    d.rounded_rectangle((x1 - tw - 36, y1 - 50, x1, y1), radius=14, fill=(255, 252, 244, 255), outline=(20, 20, 20, 255), width=3)
    d.text((x1 - (tw + 36) / 2, y1 - 25), "KI generiert", font=lab_font, fill=(15, 15, 15, 255), anchor="mm")
    return im
KI = ki_label()

# ---------------------------------------------------------------- Sticker-Wörter
_sc = {}
def sticker(text, size, fill=GOLD, stroke=INK):
    k = (text, size, fill)
    if k not in _sc:
        f = ImageFont.truetype(FD + "InterDisplay-Black.otf", size)
        sw = max(8, size // 11)
        bb = f.getbbox(text, stroke_width=sw)
        im = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((20 - bb[0] + 10, 20 - bb[1] + 12), text, font=f, fill=(0, 0, 0, 110), stroke_width=sw, stroke_fill=(0, 0, 0, 110))
        d.text((20 - bb[0], 20 - bb[1]), text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
        _sc[k] = im
    return _sc[k]

# (beat, text, x, y, rot, size, fill, dauer_in_beats)
STICKERS = [
    (0, "3", 540, 900, -6, 520, GOLD, 1), (1, "2", 540, 900, 6, 520, GOLD, 1), (2, "1", 540, 900, -4, 520, GOLD, 1),
    (3, "WUFF!", 540, 900, -8, 260, RED, 1),
    (8, "WOW!", 270, 1060, -14, 170, GOLD, 1.5),
    (10, "YEAH!", 540, 900, -8, 250, GOLD, 2),
    (16, "BÄM!", 820, 1020, 12, 180, RED, 1.5),
    (18, "DYNAMIT!", 540, 900, 7, 190, RED, 2),
    (27, "HAHA!", 790, 170, 10, 140, GOLD, 2),
    (32, "WOW!", 540, 900, -10, 280, GOLD, 2),
    (41, "YEAH!", 280, 170, -10, 140, GOLD, 2),
    (46, "SAMSTAG!", 540, 900, -6, 190, GOLD, 2),
]

def draw_stickers(img, beat):
    for b0, txt, x, y, rot, size, fill, dur in STICKERS:
        u = (beat - b0) * B
        if u < 0 or beat > b0 + dur:
            continue
        end_u = (b0 + dur - beat) * B
        s = 1 + 0.9 * math.exp(-u * 16) * math.cos(u * 30)
        s *= min(1, end_u / 0.08) if end_u < 0.08 else 1
        st = sticker(txt, size, fill)
        r = rot + 8 * math.exp(-u * 10) * math.sin(u * 25)
        iw, ih = max(1, int(st.width * s)), max(1, int(st.height * s))
        im = st.resize((iw, ih), Image.BILINEAR).rotate(r, resample=Image.BILINEAR, expand=True)
        img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

# ---------------------------------------------------------------- Sterne
random.seed(4)
def star_pts(cx, cy, r, rot):
    pts = []
    for k in range(10):
        a = rot + k * math.pi / 5 - math.pi / 2
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

BURSTS = []  # (zeit, cx, cy, anzahl, kraft)
def burst(beat, cx=540, cy=900, n=34, power=1.0):
    parts = []
    for _ in range(n):
        ang = random.uniform(0, 2 * math.pi); v = random.uniform(500, 1500) * power
        parts.append((ang, v, random.uniform(12, 42), random.uniform(-8, 8), random.choice([GOLD, GOLD, CREAM, RED, (255, 255, 255)]),
                      random.uniform(0.55, 0.95)))
    BURSTS.append((beat * B, cx, cy, parts))

def draw_bursts(img, t):
    lay = None
    for t0, cx, cy, parts in BURSTS:
        u = t - t0
        if u < 0 or u > 1.0:
            continue
        if lay is None:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for ang, v, r, spin, col, life in parts:
            if u > life:
                continue
            dist = v * (1 - math.exp(-u * 3.2)) / 3.2
            x = cx + math.cos(ang) * dist; y = cy + math.sin(ang) * dist + 300 * u * u
            a = int(255 * (1 - u / life) ** 0.7)
            rr = r * (0.6 + 0.4 * math.exp(-u * 3))
            d.polygon(star_pts(x, y, rr, spin * u), fill=col + (a,))
    if lay is not None:
        img.alpha_composite(lay)

# Sterne bei jedem Knall
for b in (0, 1, 2):
    burst(b, n=16, power=0.7)
burst(3, n=40, power=1.2)
for b in (4, 12, 48):
    burst(b, n=44, power=1.3)
for b in (10, 18, 32, 46):
    burst(b, n=40, power=1.2)
for b, (pi, py) in zip((20, 21, 22), PA):
    burst(b, 540, py + pi.height / 2, 22, 0.9)
for b, (pi, py) in zip((34, 35, 36), PB):
    burst(b, 540, py + pi.height / 2, 22, 0.9)

# ---------------------------------------------------------------- Szenen
def sunburst(t, c1=GREEN, c2=GREEN2):
    img = Image.new("RGBA", (W, H), c1 + (255,))
    d = ImageDraw.Draw(img)
    rot = t * 0.6; R = 2400
    for k in range(18):
        a0 = rot + k * 2 * math.pi / 18; a1 = a0 + math.pi / 18
        d.polygon([(540, 900), (540 + R * math.cos(a0), 900 + R * math.sin(a0)), (540 + R * math.cos(a1), 900 + R * math.sin(a1))], fill=c2 + (255,))
    return img

def slam_scale(u):
    return 1 + 0.45 * math.exp(-u * 14) * math.cos(u * 12) if u >= 0 else None

def pulse(beat):
    u = (beat - math.floor(beat)) * B
    return 1 + 0.018 * math.exp(-u * 9)

def place(canvas, im, cx, cy, s, rot=0.0):
    iw, ih = max(1, int(im.width * s)), max(1, int(im.height * s))
    r = im.resize((iw, ih), Image.BILINEAR)
    if abs(rot) > 0.2:
        r = r.rotate(rot, resample=Image.BILINEAR, expand=True)
    canvas.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))

def scene_vertical(img_s, beat, b0):
    u = (beat - b0) * B
    s = slam_scale(u) * pulse(beat)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    place(canvas, img_s, W / 2, H / 2, s, rot=5 * math.exp(-u * 10))
    return canvas

def scene_comic(pan, bg, beat, b0, label=None):
    canvas = bg.copy()
    P = pulse(beat)
    dirs = [-1, 1, 0]
    for k, (pim, py) in enumerate(pan):
        u = (beat - (b0 + k)) * B
        if u < 0:
            continue
        e = ease_out(u / 0.16)
        if dirs[k] == 0:
            cx, cy = W / 2, py + pim.height / 2 + (1 - e) * 1100
        else:
            cx, cy = W / 2 + dirs[k] * (1 - e) * 1300, py + pim.height / 2
        s = (1 + 0.12 * math.exp(-max(0, u - 0.16) * 12) * (e >= 1)) * P
        place(canvas, pim, cx, H / 2 + (cy - H / 2) * P, s)
    if label is not None and beat >= b0 + 2:
        canvas.alpha_composite(label)
    return canvas

def scene_flyer(beat, b0):
    u = (beat - b0) * B
    canvas = BG_F.copy()
    s = slam_scale(u) * (1 + 0.035 * max(0, u - 0.4) / ((TOTAL_BEATS - b0) * B))
    place(canvas, FLYs, W / 2, H / 2, s, rot=4 * math.exp(-u * 10))
    return canvas

SLAMS = [0, 1, 2, 3, 4, 10, 12, 18, 20, 21, 22, 32, 34, 35, 36, 46, 48]

def frame(t):
    beat = t / B
    if beat < 4:
        img = sunburst(t)
    elif beat < 10:
        img = scene_vertical(V1s, beat, 4)
    elif beat < 12:
        img = sunburst(t, GREEN, (120, 30, 30))
    elif beat < 18:
        img = scene_vertical(V2s, beat, 12)
    elif beat < 20:
        img = sunburst(t, (90, 20, 20), RED)
    elif beat < 32:
        img = scene_comic(PA, BG_A, beat, 20)
    elif beat < 34:
        img = sunburst(t)
    elif beat < 46:
        img = scene_comic(PB, BG_B, beat, 34, KI)
    elif beat < 48:
        img = sunburst(t, GREEN, (150, 115, 30))
    else:
        img = scene_flyer(beat, 48)
    draw_bursts(img, t)
    draw_stickers(img, beat)
    # Blitz + Wackler bei jedem Knall
    last = max([b for b in SLAMS if b <= beat], default=None)
    if last is not None:
        u = (beat - last) * B
        if u < 0.14:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(170 * (1 - u / 0.14))))
            img.alpha_composite(fl)
        if u < 0.3:
            a = 22 * math.exp(-u * 12)
            dx, dy = int(a * math.sin(u * 90)), int(a * math.cos(u * 70))
            img = Image.Image.transform(img, img.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), fillcolor=(0, 0, 0, 255))
    return img.convert("RGB")

# ---------------------------------------------------------------- Musik (eigen, 128 BPM)
N = int((DUR + 0.3) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(9)
def tt(d): return np.arange(int(d * SR)) / SR
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def smooth(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - max(pan, 0)); R[i:i + len(sig)] += sig * g * (1 + min(pan, 0))
def kick():
    t = tt(0.4); f = 46 + 120 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7); s[:50] += np.linspace(0.7, 0, 50); return s
def clap():
    t = tt(0.22); n = rng.standard_normal(len(t)); n = n - smooth(n, 9); env = np.exp(-t * 20)
    for o in (0.008, 0.017):
        k = int(o * SR); env[k:] += 0.6 * np.exp(-t[: len(t) - k] * 60)
    return n * env * 0.5
def hat(d=0.05, dec=70):
    t = tt(d); n = rng.standard_normal(len(t)); n = np.diff(np.diff(n, prepend=0), prepend=0); return n * np.exp(-t * dec) * 0.22
def sleigh():
    t = tt(0.12); n = np.diff(rng.standard_normal(len(t)), prepend=0); return n * np.exp(-t * 22) * (1 + 0.8 * np.sin(2 * np.pi * 31 * t)) * 0.14
def bass(m, d):
    t = tt(d); f = mf(m); s = np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t)
    s = smooth(s, 18); return s * np.minimum(1, t / 0.005) * np.exp(-t * 6) * 0.38
def stab(ms, d=0.3):
    t = tt(d); s = np.zeros(len(t))
    for m in ms:
        for det in (-0.1, 0.1):
            f = mf(m + det); s += 2 * ((t * f) % 1) - 1
    s = smooth(s, 10); return s * np.exp(-t * 9) * 0.06
def boom():
    t = tt(1.1); f = 38 + 70 * np.exp(-t * 9); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    n = rng.standard_normal(len(t)); n = smooth(n, 30) * np.exp(-t * 6) * 2; return (s + n) * 0.55
def crash(d=1.5):
    t = tt(d); n = rng.standard_normal(len(t)); n = n - smooth(n, 5); return n * np.exp(-t * 2.8) * 0.15
def whoosh(d=0.45):
    t = tt(d); n = rng.standard_normal(len(t)); x = t / d
    lo = smooth(n, 40); hi = n - lo; s = lo * (1 - x) + hi * x
    return s * x ** 2 * 0.35
def blip(m):
    t = tt(0.25); f = mf(m); return np.sin(2 * np.pi * f * t) * np.exp(-t * 14) * 0.3
def bell(m, d=0.9):
    t = tt(d); f = mf(m); idx = 2.2 * np.exp(-t * 5)
    return np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 3.5 * f * t)) * np.exp(-t * 3.4) * 0.3

CH = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]  # C G Am F
# Countdown
for b, m in zip((0, 1, 2), (72, 74, 76)):
    add(boom(), b * B, 0.6); add(blip(m), b * B); add(blip(m + 12), b * B, 0.5)
add(whoosh(B), 3 * B - B); add(boom(), 3 * B, 0.8); add(stab(CH[0][1]), 3 * B)
for bar in range(1, 16):
    b0 = bar * 4; t0 = b0 * B
    if b0 >= 64: break
    root, chord = CH[bar % 4]
    end_part = b0 >= 48
    for k in range(4):
        tb = t0 + k * B
        add(kick(), tb, 0.9)
        if k in (1, 3): add(clap(), tb, 0.75)
        add(hat(0.12, 30), tb + B / 2, 0.55, pan=0.25)
        if not end_part:
            for s16 in (1, 3): add(hat(), tb + s16 * B / 4, 0.35, pan=-0.2)
        add(sleigh(), tb + B * 0.75, 0.7, pan=-0.3)
        add(bass(root, B / 2), tb + B / 2, 1.0)
    if end_part:   # Flyer: festliche Glöckchen-Melodie
        for pos, off in [(0, 12), (2, 16), (3, 19), (4, 24), (6, 19)]:
            add(bell(chord[0] + off - 12), t0 + pos * B / 2, 0.9, pan=0.2)
# Knaller-Akzente
for b in (4, 12, 20, 34, 48):
    add(whoosh(), b * B - 0.45, 1.0); add(boom(), b * B, 1.0); add(crash(), b * B, 0.9)
for b in (10, 18, 32, 46):
    add(crash(), b * B, 0.8); add(stab([72, 76, 79]), b * B, 1.2)
for b in (21, 22, 35, 36):
    add(stab([67, 72, 76]), b * B, 0.9); add(boom(), b * B, 0.35)
# Snare-Wirbel vor dem Flyer
for k in range(16):
    add(clap(), 44 * B + k * B / 4, 0.25 + 0.6 * k / 16)
# Schluss
add(stab([60, 64, 67, 72], 1.6), 62 * B, 1.4); add(bell(84, 1.8), 62 * B, 1.0); add(crash(2.0), 62 * B, 0.8)

mix = np.stack([L, R], 1)[: int(DUR * SR)]
mix = np.tanh(mix * 0.95); mix /= np.abs(mix).max() / 0.88
fade = np.ones(len(mix)); fl = int(0.9 * SR); fade[-fl:] = np.linspace(1, 0, fl); mix *= fade[:, None]
with wave.open(os.path.join(OUT, "beat.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())

if "--checks" in sys.argv:
    for k, bt in enumerate([0.3, 3.2, 4.3, 8.3, 10.3, 16.2, 22.5, 27.3, 36.5, 46.2, 49, 60]):
        frame(bt * B).resize((216, 384)).save(os.path.join(OUT, f"chk_{k:02d}.png"))
    print("checks ok"); sys.exit()

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-i", os.path.join(OUT, "beat.wav"), "-vf", f"fade=out:st={DUR - 0.7}:d=0.7",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                        "-c:v", "libx264", "-preset", "medium", "-b:v", "8M", "-maxrate", "11M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", os.path.join(OUT, "reel.mp4")], stdin=subprocess.PIPE)
for f in range(int(DUR * FPS)):
    enc.stdin.write(frame(f / FPS).tobytes())
enc.stdin.close(); enc.wait()
print("ok", round(DUR, 2))

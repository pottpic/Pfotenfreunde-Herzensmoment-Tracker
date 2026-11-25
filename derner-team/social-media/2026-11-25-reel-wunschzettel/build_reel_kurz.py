"""Derner Schnauzenbande – Wunschzettel-Reel: Text-Animation + selbst gebauter Beat (120 BPM)."""
import math, random, subprocess, sys, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
BPM = 120.0
BEAT = 60.0 / BPM
TOTAL_BEATS = 52
DUR = TOTAL_BEATS * BEAT
SR = 44100

CREAM = (243, 235, 217)
GREEN = (29, 58, 37)
RED = (196, 64, 44)
GOLD = (226, 184, 96)
FD = "/usr/share/fonts/opentype/inter/"
FONTS = {"n": FD + "InterDisplay-Bold.otf", "b": FD + "InterDisplay-ExtraBold.otf",
         "huge": FD + "InterDisplay-Black.otf", "letters": FD + "InterDisplay-Black.otf"}
SIZES = {"n": 74, "b": 108, "huge": 176, "letters": 150, "emoji": 140}
EMOJI_FONT = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
MAXW = 940
CY = 900

# ---------------------------------------------------------------- Inhalt
# (start_beat, end_beat, bg, [(text, entry_beat, kind, flags)])
CARDS = [
    (0, 4, "c", [("Lieber", 0, "n", ""), ("Weihnachtsmann,", 1, "b", "")]),
    (4, 8, "g", [("Ich bin jetzt neu bei der", 4, "n", ""), ("Derner", 5, "b", ""), ("Schnauzenbande!", 6, "b", ""), ("🐾❤", 7, "emoji", "acc")]),
    (8, 16, "c", [("Gaaaaannnzzzz", 8, "letters", "step=0.25"), ("vvvviiiiieeeeel", 12, "letters", "step=0.125"), ("Leckerli.", 14, "huge", "acc shake")]),
    (16, 24, "g", [("Mein altes Körbchen", 16, "n", ""), ("hat mich angegriffen …", 17, "b", ""), ("Das Körbchen hab ich", 19, "n", ""), ("erledigt 💪", 20, "huge", "acc shake")]),
    (24, 32, "c", [("Aber weißt du,", 24, "b", ""), ("was ich mir", 26, "n", ""), ("am allermeisten", 27, "b", ""), ("wünsche?", 28, "huge", "acc")]),
    (32, 40, "g", [("Dass meine Familie", 32, "n", ""), ("gesund und glücklich bleibt", 33, "b", ""), ("und jeden Tag ganz viel", 35, "n", ""), ("Liebe ❤", 36, "huge", "acc")]),
    (40, 46, "c", [("Ach ja, und 'n", 40, "n", ""), ("Quietscheball! 🎾", 40.5, "b", "acc shake"), ("Ich verspreche,", 41.5, "n", ""), ("ihn wiederzubringen …", 42, "n", ""), ("… meistens jedenfalls 😉", 43, "b", "acc")]),
    (46, 52, "g", [("Frohe", 46, "huge", "acc"), ("Weihnachten!", 47, "huge", "acc"), ("🐾", 48, "emoji", ""), ("Derner Schnauzenbande", 48.5, "b", ""), ("@dernerschnauzenbande", 49.5, "n", "small"), ("www.dernerschnauzenbande.de", 50, "n", "small")]),
]
DRUMLESS = [(24, 32)]          # Breakdown vor „am allermeisten“
LETTER_BLIPS = []              # (zeit, index) für die Leckerli-Pling-Töne

# ---------------------------------------------------------------- Text-Rendering
_cache = {}

def is_emoji(ch):
    return ord(ch) >= 0x2600 and ch not in "…„“"

def emoji_img(ch, size, tint=None):
    if ch != "🐾":
        tint = None
    key = ("e", ch, size, tint)
    if key not in _cache and ch == "🎾":   # eigener gelber Quietscheball statt Tennis-Emoji
        n = int(size) * 4
        im = Image.new("RGBA", (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((4, 4, n - 4, n - 4), fill=(247, 206, 46))
        d.ellipse((n * 0.18, n * 0.12, n * 0.5, n * 0.38), fill=(252, 232, 140))
        d.arc((-n * 0.45, n * 0.08, n * 0.42, n * 0.92), -60, 60, fill=(255, 250, 235), width=int(n * 0.06))
        d.arc((n * 0.58, n * 0.08, n * 1.45, n * 0.92), 120, 240, fill=(255, 250, 235), width=int(n * 0.06))
        _cache[key] = im.resize((int(size), int(size)), Image.LANCZOS)
    if key not in _cache:
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 0), ch, font=EMOJI_FONT, embedded_color=True)
        im = im.crop(im.getbbox())
        s = size / im.height
        im = im.resize((max(1, int(im.width * s)), int(size)), Image.LANCZOS)
        if tint:
            solid = Image.new("RGBA", im.size, tint + (255,))
            solid.putalpha(im.getchannel("A"))
            im = solid
        _cache[key] = im
    return _cache[key]

def runs(text):
    out, cur, cur_e = [], "", None
    for ch in text.replace("️", ""):
        e = is_emoji(ch)
        if cur and e != cur_e:
            out.append((cur, cur_e)); cur = ""
        cur += ch; cur_e = e
    if cur:
        out.append((cur, cur_e))
    return out

def render_line(text, kind, color, size=None):
    size = size or SIZES[kind]
    key = (text, kind, color, size)
    if key in _cache:
        return _cache[key]
    if kind == "emoji":
        parts = [emoji_img(ch, size, color) for ch in text.replace("️", "")]
        gap = int(size * 0.15)
        w = sum(p.width for p in parts) + gap * (len(parts) - 1)
        im = Image.new("RGBA", (w, size + 10), (0, 0, 0, 0))
        x = 0
        for p in parts:
            im.paste(p, (x, 5), p); x += p.width + gap
        _cache[key] = im
        return im
    font = ImageFont.truetype(FONTS[kind], size)
    segs = runs(text)
    widths = []
    for s, e in segs:
        widths.append(emoji_img(s[0], int(size * 0.95)).width * len(s) if e else font.getlength(s))
    total = int(sum(widths)) + 4
    if total > MAXW:
        res = render_line(text, kind, color, int(size * MAXW / total))
        _cache[key] = res
        return res
    asc, desc = font.getmetrics()
    im = Image.new("RGBA", (total, asc + desc + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 2
    for (s, e), wdt in zip(segs, widths):
        if e:
            for ch in s:
                ei = emoji_img(ch, int(size * 0.95), color)
                im.paste(ei, (int(x), int(asc - ei.height * 0.9)), ei)
                x += ei.width
        else:
            d.text((x, asc), s, font=font, fill=color, anchor="ls")
            x += wdt
    _cache[key] = im
    return im

def letter_imgs(text, color):
    """Einzelbuchstaben + x-Positionen, auf MAXW gefittet."""
    key = ("L", text, color)
    if key in _cache:
        return _cache[key]
    size = SIZES["letters"]
    font = ImageFont.truetype(FONTS["letters"], size)
    tw = font.getlength(text)
    if tw > MAXW:
        size = int(size * MAXW / tw); font = ImageFont.truetype(FONTS["letters"], size)
        tw = font.getlength(text)
    asc, desc = font.getmetrics()
    items = []
    for i, ch in enumerate(text):
        x = font.getlength(text[:i])
        cw = int(font.getlength(ch)) + 6
        im = Image.new("RGBA", (cw, asc + desc + 6), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((3, asc), ch, font=font, fill=color, anchor="ls")
        items.append((x, im))
    res = (items, int(tw), asc + desc + 6)
    _cache[key] = res
    return res

# ---------------------------------------------------------------- Animation
def pop(u):
    if u < 0:
        return 0.0, 0.0
    s = 1 - math.exp(-u * 11) * math.cos(u * 22) * 0.5
    a = min(1.0, u / 0.06)
    return s, a

def drums_on(beat):
    return not any(a <= beat < b for a, b in DRUMLESS)

def pulse(t):
    b = t / BEAT
    if not drums_on(b) or b >= 48:
        return 1.0
    u = (b - math.floor(b)) * BEAT
    return 1 + 0.022 * math.exp(-u * 10)

def colors(bg):
    if bg == "c":
        return CREAM, GREEN, RED
    return GREEN, CREAM, GOLD

random.seed(7)
SNOW = [(random.uniform(0, W), random.uniform(0, H), random.uniform(50, 130), random.uniform(3, 9),
         random.uniform(0, 6.28), random.uniform(0.4, 1.0)) for _ in range(60)]

def draw_snow(img, t, bg):
    d = ImageDraw.Draw(img)
    bgc, fg, _ = colors(bg)
    for x0, y0, v, r, ph, al in SNOW:
        y = (y0 + v * t) % (H + 40) - 20
        x = x0 + 25 * math.sin(t * 1.1 + ph)
        a = (0.55 if bg == "g" else 0.14) * al
        col = CREAM if bg == "g" else GREEN
        c = tuple(int(bgc[i] * (1 - a) + col[i] * a) for i in range(3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)

def card_layout(card):
    s0, s1, bg, lines = card
    _, fg, acc = colors(bg)
    items = []
    for text, eb, kind, flags in lines:
        col = acc if "acc" in flags else fg
        if kind == "letters":
            _, tw, th = letter_imgs(text, col)
            items.append(("L", text, eb, col, flags, tw, th))
        else:
            k = kind
            im = render_line(text, k, col, int(SIZES[k] * 0.62) if "small" in flags else None)
            items.append(("T", im, eb, col, flags, im.width, im.height))
    gap = 14
    total = sum(it[6] for it in items) + gap * (len(items) - 1)
    y = CY - total / 2
    placed = []
    for it in items:
        placed.append((it, y))
        y += it[6] + gap
    return placed

LAYOUTS = [card_layout(c) for c in CARDS]
NCARDS = len(CARDS)

def render_card(ci, t):
    card = CARDS[ci]
    bg = card[2]
    img = Image.new("RGB", (W, H), colors(bg)[0])
    draw_snow(img, t, bg)
    beat = t / BEAT
    P = pulse(t)
    # Shake nach Flag
    dx = dy = 0.0
    for (it, y) in LAYOUTS[ci]:
        if "shake" in it[4]:
            u = t - it[2] * BEAT
            if 0 <= u < 0.5:
                amp = 22 * math.exp(-u * 9)
                dx += amp * math.sin(u * 95); dy += amp * math.cos(u * 77)
    for (it, y) in LAYOUTS[ci]:
        kind, payload, eb, col, flags, w, h = it
        cy_line = y + h / 2
        cy_line = CY + (cy_line - CY) * P + dy
        if kind == "L":
            items, tw, th = letter_imgs(payload, col)
            step = float(flags.split("step=")[1].split()[0])
            x0 = W / 2 - tw / 2 + dx
            for i, (lx, im) in enumerate(items):
                u = t - (eb + i * step) * BEAT
                s, a = pop(u)
                if a <= 0:
                    continue
                s *= P
                iw, ih = max(1, int(im.width * s)), max(1, int(im.height * s))
                ri = im.resize((iw, ih), Image.BILINEAR)
                if a < 1:
                    ri.putalpha(ri.getchannel("A").point(lambda v: int(v * a)))
                cx = x0 + lx + im.width / 2
                hop = -30 * math.exp(-max(u, 0) * 14)
                img.paste(ri, (int(cx - iw / 2), int(cy_line - ih / 2 + hop)), ri)
            continue
        u = t - eb * BEAT
        s, a = pop(u)
        if a <= 0:
            continue
        s *= P
        im = payload
        if kind == "T" and (h > 150 or w < 200):  # große Wörter & Emojis: leichter Dreh beim Reinploppen
            rot = 7 * math.exp(-u * 8) * math.cos(u * 18)
        else:
            rot = 0
        iw, ih = max(1, int(im.width * s)), max(1, int(im.height * s))
        ri = im.resize((iw, ih), Image.BILINEAR)
        if abs(rot) > 0.3:
            ri = ri.rotate(rot, resample=Image.BILINEAR, expand=True)
        if a < 1:
            ri.putalpha(ri.getchannel("A").point(lambda v: int(v * a)))
        slide = 45 * math.exp(-u * 12)
        img.paste(ri, (int(W / 2 - ri.width / 2 + dx), int(cy_line - ri.height / 2 + slide)), ri)
    return img

def frame_at(t):
    beat = t / BEAT
    ci = max(i for i, c in enumerate(CARDS[:NCARDS]) if c[0] <= beat + 1e-9)
    cur = render_card(ci, t)
    u = t - CARDS[ci][0] * BEAT
    if ci > 0 and u < 0.2:
        prev = render_card(ci - 1, t)
        e = 1 - (1 - u / 0.2) ** 3
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        if ci % 2:
            md.rectangle((0, int(H * (1 - e)), W, H), fill=255)   # von unten rein
        else:
            md.rectangle((0, 0, W, int(H * e)), fill=255)          # von oben rein
        cur = Image.composite(cur, prev, mask)
    return cur

# ---------------------------------------------------------------- Musik
N = int((DUR + 0.5) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(3)

def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - max(pan, 0))
    R[i:i + len(sig)] += sig * g * (1 + min(pan, 0))

def tt(d):
    return np.arange(int(d * SR)) / SR

def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def smooth(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def kick():
    t = tt(0.4); f = 48 + 110 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    s[:60] += np.linspace(0.6, 0, 60)
    return s

def clap():
    t = tt(0.22); n = rng.standard_normal(len(t)); n = n - smooth(n, 9)
    env = np.exp(-t * 22)
    for off in (0.009, 0.018):
        k = int(off * SR); env[k:] += 0.6 * np.exp(-t[: len(t) - k] * 60)
    return n * env * 0.5

def hat(d=0.05):
    t = tt(d); n = rng.standard_normal(len(t)); n = np.diff(np.diff(n, prepend=0), prepend=0)
    return n * np.exp(-t * 70) * 0.25

def sleigh():
    t = tt(0.14); n = rng.standard_normal(len(t)); n = np.diff(n, prepend=0)
    return n * np.exp(-t * 20) * (1 + 0.8 * np.sin(2 * np.pi * 31 * t)) * 0.18

def bell(m, d=0.9):
    t = tt(d); f = mf(m)
    idx = 2.2 * np.exp(-t * 5)
    return np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 3.5 * f * t)) * np.exp(-t * 3.2) * 0.32

def bass(m, d):
    t = tt(d); f = mf(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / 0.006) * np.exp(-t * 5)
    return s * env * 0.42

def pad(ms, d):
    t = tt(d); s = np.zeros(len(t))
    for m in ms:
        for det in (-0.12, 0.12):
            f = mf(m + det)
            s += np.sin(2 * np.pi * f * t) + 0.2 * np.sin(6 * np.pi * f * t) / 3
    env = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.2)
    return s * env * 0.035

def crash(d=1.6):
    t = tt(d); n = rng.standard_normal(len(t)); n = n - smooth(n, 5)
    return n * np.exp(-t * 2.6) * 0.16

def blip(m):
    t = tt(0.12); f = mf(m)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 30) * 0.28

# Akkorde je Takt: C – Am – F – G (eigene Progression, kein bekanntes Lied)
CH = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]
# eigenes Glöckchen-Motiv: (Achtel-Position, Halbton-Offset zur Akkord-Basis-Tonleiter)
MOTIF = [(0, 12), (1, 16), (2, 19), (3, 16), (4, 21), (6, 19), (7, 16)]
MOTIF_B = [(0, 19), (2, 17), (3, 16), (4, 14), (5, 12), (6, 14)]

for bar in range(TOTAL_BEATS // 4 + 1):
    b0 = bar * 4
    t0 = b0 * BEAT
    if b0 >= 48:
        break
    root, chord = CH[bar % 4]
    breakdown = 24 <= b0 < 32
    light = False
    add(pad(chord, 4 * BEAT + 0.1), t0, 1.0)
    # Bell-Melodie auf Akkordtönen
    mot = MOTIF if bar % 2 == 0 else MOTIF_B
    for pos, off in mot:
        base = chord[0] - 12
        note = base + off
        # an Akkord-Leiter anlehnen
        add(bell(note), t0 + pos * BEAT / 2, 0.9 if not breakdown else 1.1, pan=0.25 * math.sin(pos))
    if breakdown:
        if b0 == 28:  # Snare-Roll + Riser in den Drop
            for k in range(16):
                frac = k / 16
                add(clap(), t0 + k * BEAT / 4, 0.25 + 0.75 * frac)
            t = tt(4 * BEAT); n = rng.standard_normal(len(t)); n = n - smooth(n, 3)
            add(n * (t / t[-1]) ** 2 * 0.12, t0)
        continue
    for k in range(4):
        tb = t0 + k * BEAT
        add(kick(), tb, 0.95)
        if k in (1, 3):
            add(clap(), tb, 0.8)
        for e in range(2):
            add(bass(root + (12 if e else 0), BEAT / 2), tb + e * BEAT / 2, 1.0)
        if not light:
            for s16 in range(4):
                add(hat(), tb + s16 * BEAT / 4, 0.7 if s16 % 2 else 0.4, pan=0.3)
            add(sleigh(), tb + BEAT / 2, 0.9, pan=-0.35)
            if b0 >= 32:
                add(sleigh(), tb + BEAT * 0.75, 0.6, pan=0.35)

# Akzente auf den Hits
for b in (0, 4, 8, 14, 20, 32, 36, 46):
    add(crash(), b * BEAT, 1.0 if b in (14, 20, 32, 46) else 0.6)
# Pling je Buchstabe bei „Gaaaannnzzzz vvviiieeel“
scale = [72, 74, 76, 79, 81, 84, 86, 88]
for text, eb, kind, flags in CARDS[2][3]:
    if kind == "letters":
        step = float(flags.split("step=")[1])
        for i, _ in enumerate(text):
            add(blip(scale[i % len(scale)] + (12 if step < 0.2 else 0)), (eb + i * step) * BEAT, 0.8)
# Schlussakkord
add(pad([48, 55, 60, 64, 67], 2.0), 48 * BEAT, 2.0)
add(bell(72, 1.8), 48 * BEAT, 1.2); add(bell(79, 1.8), 48 * BEAT + 0.05, 0.9)
add(kick(), 48 * BEAT, 1.0); add(crash(2.2), 48 * BEAT, 1.0)
# Quietsche-Ball: Tonhöhe hoch und wieder runter
def squeak(d=0.28, f0=900, f1=1700):
    t = tt(d); x = t / d
    f = f0 + (f1 - f0) * np.sin(np.pi * x)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.03) * 0.22
add(squeak(), 40.5 * BEAT, 1.0)
add(squeak(0.18, 1100, 1900), 43 * BEAT, 0.9); add(squeak(0.18, 1100, 1900), 43.5 * BEAT, 0.7)

mix = np.stack([L, R], 1)
mix = np.tanh(mix * 0.9)
mix /= np.abs(mix).max() / 0.89
fade = np.ones(N); fl = int(1.0 * SR); fade[-fl:] = np.linspace(1, 0, fl)
mix *= fade[:, None]
pcm = (mix * 32767).astype("<i2")
with wave.open(os.path.join(OUT, "beat.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("audio ok", DUR)

# ---------------------------------------------------------------- Video
if "--covers-only" not in sys.argv:
    nfr = int(DUR * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", os.path.join(OUT, "beat.wav"),
                            "-vf", f"fade=out:st={DUR - 0.8}:d=0.8", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                            "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            os.path.join(OUT, "reel.mp4")], stdin=subprocess.PIPE)
    for f in range(nfr):
        enc.stdin.write(frame_at(f / FPS).tobytes())
        if f % 150 == 0:
            print("frame", f, "/", nfr, flush=True)
    enc.stdin.close(); enc.wait()
    print("video ok")

# ---------------------------------------------------------------- Cover
cover_card = (0, 4, "g", [("Mein", 0, "b", ""), ("Wunschzettel", 0, "huge", "acc"), ("an den Weihnachtsmann", 0, "n", ""), ("🐾🎄", 0, "emoji", "acc")])
CARDS.append(cover_card); LAYOUTS.append(card_layout(cover_card))
render_card(len(CARDS) - 1, 3.0).save(os.path.join(OUT, "cover1.png"))
frame_at(15.5 * BEAT).save(os.path.join(OUT, "cover2.png"))     # Leckerli
frame_at(21.5 * BEAT).save(os.path.join(OUT, "cover3.png"))   # erledigt
for b in (3, 7.5, 15, 23, 31, 39, 45, 51):
    frame_at(b * BEAT).resize((270, 480)).save(os.path.join(OUT, f"chk_{int(b*10):03d}.png"))
print("covers ok")

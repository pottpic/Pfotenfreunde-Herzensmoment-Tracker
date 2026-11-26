"""Ruhiger Weihnachts-Beat (84 BPM) fürs Pfotenzauber-Countdown-Reel. Eigenproduktion, kein bekanntes Lied."""
import sys, wave
import numpy as np

OUT, DUR = sys.argv[1], float(sys.argv[2])
SR = 44100
BPM = 84.0
BEAT = 60 / BPM
N = int((DUR + 0.2) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(11)

def tt(d): return np.arange(int(d * SR)) / SR
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def smooth(x, k): return np.convolve(x, np.ones(k) / k, mode="same")

def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - max(pan, 0))
    R[i:i + len(sig)] += sig * g * (1 + min(pan, 0))

def musicbox(m, d=1.6):
    t = tt(d); f = mf(m)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t * 6) + 0.12 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t * 12)
    return s * np.minimum(1, t / 0.003) * np.exp(-t * 2.6) * 0.2

def pad(ms, d):
    t = tt(d); s = np.zeros(len(t))
    for m in ms:
        for det in (-0.08, 0.08):
            f = mf(m + det)
            s += np.sin(2 * np.pi * f * t) + 0.15 * np.sin(4 * np.pi * f * t)
    s = smooth(s, 6)
    env = np.minimum(1, t / 0.6) * np.minimum(1, np.maximum(0, d - t) / 0.6)
    return s * env * 0.03

def bass(m, d):
    t = tt(d); f = mf(m)
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / 0.02) * np.exp(-t * 1.6) * 0.32

def softkick():
    t = tt(0.35); f = 45 + 50 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.6

def shaker(g=1.0):
    t = tt(0.09); n = rng.standard_normal(len(t)); n = n - smooth(n, 4)
    env = np.minimum(1, t / 0.02) * np.exp(-t * 40)
    return n * env * 0.05 * g

def rim():
    t = tt(0.08); n = rng.standard_normal(len(t)); n = n - smooth(n, 12)
    return (n * 0.4 + np.sin(2 * np.pi * 1700 * t)) * np.exp(-t * 55) * 0.07

def sleighsoft():
    t = tt(0.2); n = rng.standard_normal(len(t)); n = np.diff(n, prepend=0)
    return n * np.exp(-t * 14) * (1 + 0.7 * np.sin(2 * np.pi * 29 * t)) * 0.06

# F – C/E – Dm – B♭ (je ein Takt)
CH = [(41, [65, 69, 72]), (40, [64, 67, 72]), (38, [62, 65, 69]), (34, [62, 65, 70])]
# eigenes Spieluhr-Motiv je Takt: (Position in Achteln, Note)
MEL = [
    [(0, 77), (2, 76), (3, 74), (4, 72), (6, 74)],
    [(0, 76), (2, 72), (4, 79), (6, 77)],
    [(0, 74), (2, 77), (3, 76), (4, 74), (6, 72)],
    [(0, 70), (2, 74), (4, 77), (5, 76), (6, 74)],
]
bars = int(DUR / (4 * BEAT)) + 1
for bar in range(bars):
    t0 = bar * 4 * BEAT
    if t0 > DUR - 1.0: break
    root, chord = CH[bar % 4]
    add(pad(chord, 4 * BEAT + 0.6), t0)
    add(bass(root, 2 * BEAT), t0); add(bass(root + 7, 2 * BEAT), t0 + 2 * BEAT, 0.7)
    for pos, n in MEL[bar % 4]:
        add(musicbox(n), t0 + pos * BEAT / 2, 1.0 if bar >= 1 else 0.7, pan=0.2 if pos % 4 else -0.2)
    if bar >= 1 and t0 < DUR - 3:   # Takt 1: nur Spieluhr + Fläche, dann sanfter Groove
        for k in range(4):
            tb = t0 + k * BEAT
            if k in (0, 2): add(softkick(), tb)
            if k in (1, 3): add(rim(), tb, pan=0.15)
            for e in range(2): add(shaker(0.6 if e else 1.0), tb + e * BEAT / 2, pan=-0.3)
        add(sleighsoft(), t0 + 3.5 * BEAT, pan=0.3)
# Schlussakkord
tend = (int((DUR - 2.4) / BEAT)) * BEAT
add(pad([53, 60, 65, 69, 72], DUR - tend + 0.2), tend, 1.3)
add(musicbox(77, 2.5), tend, 1.1); add(musicbox(84, 2.5), tend + 0.12, 0.7)

mix = np.stack([L, R], 1)[: int(DUR * SR)]
mix = np.tanh(mix * 0.9)
mix /= np.abs(mix).max() / 0.85
fade = np.ones(len(mix)); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl)
fi = int(0.3 * SR); fade[:fi] *= np.linspace(0, 1, fi)
mix *= fade[:, None]
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("ok")

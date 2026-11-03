"""Original background score for the DAMI motion video (numpy synthesis, no samples). Usage: music.py out.wav"""

import sys
import wave

import numpy as np

SR, DUR = 44100, 52.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)


def env(start, attack, length, release):
    """Gain envelope over the whole track: ramp up, hold, ramp down."""
    g = np.clip((t - start) / attack, 0, 1) * np.clip((start + length - t) / release, 0, 1)
    return g


def lowpass(x, cutoff):
    """FFT brick-wall-ish lowpass with a soft knee."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def note(freq):
    return 440 * 2 ** ((freq - 69) / 12)


mix = np.zeros((N, 2))

# heartbeat intro (lub-dub at 72 bpm)
for b in np.arange(0.15, 4.2, 60 / 72):
    for off, amp in ((0, 1.0), (0.22, 0.7)):
        s = int((b + off) * SR)
        n = int(0.25 * SR)
        k = np.arange(n) / SR
        thump = amp * np.sin(2 * np.pi * (55 - 20 * k) * k) * np.exp(-k * 18)
        mix[s:s + n] += thump[:, None] * 0.9

# chord pad: Am - F - C - G, 5 s each, entering at 3.8 s
chords = [(57, 60, 64), (53, 57, 60), (48, 55, 64), (55, 59, 62)]
pad = np.zeros(N)
for i, start in enumerate(np.arange(3.8, DUR, 5.0)):
    ch = chords[i % 4]
    g = env(start, 1.2, 5.6, 1.4)
    idx = g > 0
    for m in ch:
        for det in (-0.08, 0.0, 0.08):
            f = note(m + det)
            ph = 2 * np.pi * f * t[idx]
            pad[idx] += g[idx] * (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph))
pad = lowpass(pad, 1400) * 0.035
mix[:, 0] += pad
mix[:, 1] += np.roll(pad, 220)

# bass on chord roots
bass = np.zeros(N)
for i, start in enumerate(np.arange(4.0, 47, 0.625 * 2)):
    root = chords[int((start - 3.8) // 5) % 4][0] - 24
    s, n = int(start * SR), int(1.1 * SR)
    k = np.arange(min(n, N - s)) / SR
    bass[s:s + len(k)] += np.sin(2 * np.pi * note(root) * k) * np.exp(-k * 2.2) * np.clip(k * 60, 0, 1)
mix += (bass * 0.16)[:, None]

# kick from 9 s, hats from 14 s (96 bpm)
beat = 0.625
for b in np.arange(9.0, 46.9, beat):
    s = int(b * SR)
    n = int(0.3 * SR)
    k = np.arange(min(n, N - s)) / SR
    kick = np.sin(2 * np.pi * (48 + 110 * np.exp(-k * 30)) * k) * np.exp(-k * 9)
    mix[s:s + len(k)] += (kick * 0.42)[:, None]
for h in np.arange(14.0 + beat / 2, 46.9, beat / 2):
    s = int(h * SR)
    n = int(0.06 * SR)
    noise = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 70)
    noise = noise - np.convolve(noise, np.ones(6) / 6, "same")
    pan = 0.6 if int(h / (beat / 2)) % 2 else 0.4
    mix[s:s + n, 0] += noise * 0.05 * pan
    mix[s:s + n, 1] += noise * 0.05 * (1 - pan)

# pluck arpeggio from 20 s (sixteenths over chord tones)
for j, a in enumerate(np.arange(20.0, 46.5, beat / 2)):
    ch = chords[int((a - 3.8) // 5) % 4]
    m = ch[j % 3] + 12 * (1 + (j // 3) % 2)
    s, n = int(a * SR), int(0.35 * SR)
    k = np.arange(min(n, N - s)) / SR
    pl = (np.sin(2 * np.pi * note(m) * k) + 0.3 * np.sin(4 * np.pi * note(m) * k)) * np.exp(-k * 9)
    pan = 0.3 + 0.4 * ((j * 3) % 5) / 4
    mix[s:s + len(k), 0] += pl * 0.06 * pan
    mix[s:s + len(k), 1] += pl * 0.06 * (1 - pan)

# risers before each scene change, and a closing impact
for c in (4.0, 9.0, 14.0, 20.0, 31.0, 36.0, 42.0, 47.0):
    s, n = int((c - 0.9) * SR), int(0.9 * SR)
    k = np.arange(n) / n
    w = lowpass(rng.standard_normal(n), 3000) * k ** 2 * 0.12
    mix[s:s + n] += w[:, None]
s, n = int(47.0 * SR), int(4 * SR)
k = np.arange(n) / SR
boom = np.sin(2 * np.pi * (40 + 60 * np.exp(-k * 8)) * k) * np.exp(-k * 1.6) * 0.6
mix[s:s + n] += boom[:, None]

# master: fade in/out, soft clip, normalise to -1 dBFS
mix *= np.clip(t / 0.5, 0, 1)[:, None] * np.clip((DUR - t) / 3.0, 0, 1)[:, None]
mix = np.tanh(mix * 1.3)
mix *= 0.89 / np.abs(mix).max()
pcm = (mix * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(sys.argv[1])

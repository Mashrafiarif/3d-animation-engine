"""Generate original synchronized sound effects using only Python's standard library.
Usage: python3 sound.py 4 output/sfx.wav
"""
import array
import math
import os
import random
import sys
import wave

seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
output = sys.argv[2] if len(sys.argv) > 2 else 'output/sfx.wav'
sr = 44100
n = round(seconds * sr)
samples = array.array('f', [0.0]) * n
rng = random.Random(2026)

def ping(start, freq=660, length=0.38, gain=0.23):
    first = int(start * sr)
    for j in range(min(int(length * sr), n - first)):
        t = j / sr
        envelope = (1 - math.exp(-80 * t)) * math.exp(-13 * t)
        val = math.sin(2 * math.pi * freq * t) + 0.33 * math.sin(2 * math.pi * freq * 1.5 * t)
        samples[first + j] += gain * envelope * val

def whoosh(start, length=0.52, gain=0.12):
    first = int(start * sr)
    previous = 0.0
    for j in range(min(int(length * sr), n - first)):
        t = j / sr
        u = t / length
        envelope = math.sin(math.pi * u) ** 2
        white = rng.uniform(-1, 1)
        previous = 0.85 * previous + 0.15 * white
        samples[first + j] += gain * envelope * previous

for start in (0.12, 2.12, 3.40):
    if start < seconds:
        ping(start, 640 + int(80 * start))
for start in (0.85, 2.84):
    if start < seconds:
        whoosh(start)

os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
with wave.open(output, 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sr)
    pcm = array.array('h', (int(max(-1.0, min(1.0, s)) * 26000) for s in samples))
    wav.writeframes(pcm.tobytes())
print(f'Generated {output} ({seconds:g} seconds)')

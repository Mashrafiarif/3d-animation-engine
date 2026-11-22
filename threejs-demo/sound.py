"""Original synchronized SFX for V3's five-second animation.
Run: python3 sound.py 5 output/sfx.wav
All event times correspond to the 5-second storyboard inside index.html.
"""
import array
import math
import os
import random
import sys
import wave

seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
out = sys.argv[2] if len(sys.argv) > 2 else 'output/sfx.wav'
if not 0 < seconds <= 120:
    raise ValueError('Duration must be 0 < seconds <= 120')
sr = 44100
count = int(round(seconds * sr))
L = array.array('f', [0.0]) * count
R = array.array('f', [0.0]) * count
rng = random.Random(20261122)

def add(t, value, pan=0):
    i = int(t * sr)
    if i < 0 or i >= count:
        return
    lvol = math.sqrt((1 - pan) * .5)
    rvol = math.sqrt((1 + pan) * .5)
    L[i] += value * lvol
    R[i] += value * rvol

def step(t, pan):
    low = 0
    for j in range(round(.16*sr)):
        s=j/sr
        low=.87*low+.13*rng.uniform(-1,1)
        env=math.exp(-25*s)
        add(t+s,.24*env*low+.18*math.sin(2*math.pi*(105-55*s)*s)*env,pan)

def bell(t, freq, duration=.35, amp=.22, pan=0):
    for j in range(round(duration*sr)):
        s=j/sr
        env=(1-math.exp(-90*s))*math.exp(-8*s)
        y=(math.sin(2*math.pi*freq*s)+.23*math.sin(2*math.pi*freq*2.007*s))*env*amp
        add(t+s,y,pan)

def airy(t,duration=.6,level=.19,pan=0):
    prev=0
    for j in range(round(duration*sr)):
        s=j/sr
        prev=.82*prev+.18*rng.uniform(-1,1)
        env=math.sin(math.pi*s/duration)**2
        add(t+s,level*prev*env,pan)

def sparkle(t):
    notes=[587.33,739.99,880.,1174.66,1479.98,1760.]
    for i,f in enumerate(notes):
        bell(t+i*.083,f,.40,.19/(1+.13*i),-.42+.16*i)

def glow(t):
    for j in range(round(.90*sr)):
        s=j/sr
        env=(1-math.exp(-15*s))*math.exp(-2.7*s)
        f=230+300*s
        add(t+s,.07*env*(math.sin(2*math.pi*f*s)+.3*math.sin(2*math.pi*(f*1.51)*s)),.08)

# The contact points are physically planted at these precise times in the scene.
for i,t in enumerate((.18,.54,.90,1.26)):
    step(t,-.26 if i%2==0 else .26)
# Stop and gaze, arm reaches, hand closes, lift, active crystal, surprised reaction.
bell(1.70,700,.42,.20,.23)
airy(2.30,.72,.21,.34)
bell(3.20,405,.25,.25,.42) # physical pickup click
bell(3.37,606,.34,.17,.28)
airy(3.40,.56,.14,.27)     # lift
sparkle(4.01)
glow(4.05)
bell(4.22,783.99,.44,.14,-.2)
bell(4.43,1046.5,.48,.12,.23)

os.makedirs(os.path.dirname(out) or '.',exist_ok=True)
pcm=array.array('h')
peak=0
for left,right in zip(L,R):
    left=math.tanh(left*1.9)*.78
    right=math.tanh(right*1.9)*.78
    peak=max(peak,abs(left),abs(right))
    pcm.append(round(max(-1,min(1,left))*32767))
    pcm.append(round(max(-1,min(1,right))*32767))
with wave.open(out,'wb') as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(sr)
    f.writeframes(pcm.tobytes())
print(f'Original SFX: {out}, {seconds:g}s, stereo 44.1kHz, peak {peak:.3f}')

"""Original, timestamped stereo sound for the 8-second Three.js character story.
No third-party libraries. Run: python3 sound.py 8 output/sfx.wav
Events exactly match the animation timeline declared in index.html.
"""
import array
import math
import os
import random
import sys
import wave

seconds=float(sys.argv[1]) if len(sys.argv)>1 else 8.0
output=sys.argv[2] if len(sys.argv)>2 else 'output/sfx.wav'
if not 0 < seconds <= 120:
    raise ValueError('seconds must be between 0 and 120')
sr=44100
n=round(seconds*sr)
left=array.array('f',[0.0])*n
right=array.array('f',[0.0])*n
rng=random.Random(20261122)

def put(at,s,pan=0):
    i=int(at*sr)
    if not 0 <= i < n:return
    a=math.sqrt((1-pan)*.5)
    b=math.sqrt((1+pan)*.5)
    left[i]+=s*a
    right[i]+=s*b

def tone(start,freq,length,amp=.25,decay=7,pan=0):
    for j in range(max(0,min(n-int(start*sr),int(length*sr)))):
        t=j/sr
        env=(1-math.exp(-80*t))*math.exp(-decay*t)
        sample=(math.sin(2*math.pi*freq*t)+.30*math.sin(2*math.pi*freq*2.02*t))*env*amp
        put(start+t,sample,pan)

def soft_step(start,pan=0):
    # Filtered low percussive thud, not a repeating beep.
    prev=0.0
    for j in range(max(0,min(n-int(start*sr),int(.18*sr)))):
        t=j/sr
        prev=.90*prev+.10*rng.uniform(-1,1)
        envelope=math.exp(-28*t)
        bump=math.sin(2*math.pi*(96-36*t)*t)*math.exp(-21*t)
        put(start+t,.18*envelope*prev+.17*bump,pan)

def swoosh(start,length=.53,amp=.21,pan=0):
    prev=0.0
    for j in range(max(0,min(n-int(start*sr),int(length*sr)))):
        t=j/sr; u=t/length
        prev=.82*prev+.18*rng.uniform(-1,1)
        env=math.sin(math.pi*u)**2
        put(start+t,amp*prev*env,pan)

def sparkle(start,length=1.15,amp=.18):
    for k in range(11):
        at=start+.087*k
        tone(at,660*2**([0,4,7,11,12][k%5]/12),.32,amp/(1+.12*k),10,(-1)**k*.35)

def chord(start,tones,length=.95,amp=.15):
    for k,f in enumerate(tones):
        tone(start+.04*k,f,length,amp,4,(-1)**k*.35)

# WALK: heel-to-toe sounds occur at visible foot cycles.
for i,at in enumerate((.22,.67,1.12,1.57)):
    soft_step(at,-.24 if i%2 else .24)
# NOTICE, REACH, CONTACT, LIFT, MAGIC, SURPRISE, TURN, END.
tone(2.10,784,.40,.21,9,.3)
swoosh(2.65,.60,.22,.45)
soft_step(3.49,.2)
tone(3.53,495,.28,.20,12,.25)
tone(3.83,622,.45,.15,7,.25)
tone(4.18,784,.45,.13,7,.27)
sparkle(4.72,1.0,.17)
chord(5.12,(523.25,659.25,783.99),.90,.10)
swoosh(6.39,.70,.16,-.35)
chord(7.23,(392,523.25,659.25),.7,.09)

os.makedirs(os.path.dirname(output) or '.',exist_ok=True)
# Mild compression, then avoid clipping; approximately broadcast-safe SFX levels.
with wave.open(output,'wb') as wav:
    wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(sr)
    pcm=array.array('h')
    for a,b in zip(left,right):
        pcm.append(int(max(-1,min(1,math.tanh(a*1.5)*.75))*32767))
        pcm.append(int(max(-1,min(1,math.tanh(b*1.5)*.75))*32767))
    wav.writeframes(pcm.tobytes())
print(f'Generated {output}: {seconds:g} s, {sr} Hz, stereo, synchronized original SFX')

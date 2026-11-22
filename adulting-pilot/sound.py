#!/usr/bin/env python3
"""Original 15-second stereo score and action SFX for ADULTING.EXE pilot.
Pure Python stdlib: no external services, accounts, or royalty/licensing issues.
Run: python3 sound.py 15 output/sfx.wav
"""
import sys, wave, math, random, os, array
SAMPLE_RATE=44100
DURATION=float(sys.argv[1]) if len(sys.argv)>1 else 15.0
OUT=sys.argv[2] if len(sys.argv)>2 else 'output/sfx.wav'
N=int(SAMPLE_RATE*DURATION)
left=array.array('f',[0.0])*N
right=array.array('f',[0.0])*N
rng=random.Random(3027)
TAU=2*math.pi

def put(start,duration,generator,vol=0.2,pan=0.0):
    first=max(0,int(start*SAMPLE_RATE))
    count=min(int(duration*SAMPLE_RATE),N-first)
    if count<=0:return
    lvol=vol*math.sqrt((1-pan)*.5)
    rvol=vol*math.sqrt((1+pan)*.5)
    for i in range(count):
        t=i/SAMPLE_RATE
        s=generator(t,duration)
        left[first+i]+=lvol*s
        right[first+i]+=rvol*s

def note(start,freq,seconds=.28,vol=.075,pan=0):
    def gen(t,d):
        env=(1-math.exp(-t*55))*math.exp(-t*10.5)
        return env*(math.sin(TAU*freq*t)+.19*math.sin(TAU*2*freq*t))
    put(start,seconds,gen,vol,pan)

def click(t,vol=.20,pan=0):
    def gen(x,d):return math.exp(-x*75)*(rng.uniform(-1,1)*.54+math.sin(TAU*(125-30*x)*x))
    put(t,.115,gen,vol,pan)

def foot(t,pan=0):
    def gen(x,d):return math.exp(-x*35)*(.65*rng.uniform(-1,1)+.35*math.sin(TAU*62*x))
    put(t,.16,gen,.16,pan)

def beep(t,f=790,seconds=.22,vol=.24,pan=0):
    def gen(x,d):
        env=math.sin(math.pi*min(1,x/d))**.9
        return env*(math.sin(TAU*(f*x+90*x*x))+.17*math.sin(TAU*2*f*x))
    put(t,seconds,gen,vol,pan)

def sweep(t,seconds=.26,vol=.13,pan=0):
    def gen(x,d):return math.sin(math.pi*x/d)**2 * math.sin(TAU*(380*x+900*x*x))
    put(t,seconds,gen,vol,pan)

def chime(t):
    for idx,f in enumerate([440,554.37,659.25,880]):
        note(t+idx*.09,f,.44,.12,pan=(-.45+idx*.28))

# Gentle original music composed for this clip: no pre-existing melody or samples.
# 4/4 upbeat 116 BPM; understated synth plucks beneath the joke.
scale=[220,261.63,329.63,392,329.63,261.63,246.94,293.66,
       220,261.63,329.63,440,392,329.63,261.63,220,
       196,246.94,293.66,392,329.63,293.66,246.94,196,
       220,261.63,329.63,392,440,329.63]
for i,f in enumerate(scale):
    st=i*.48
    if st>DURATION-.15:break
    note(st,f,.32,.10,pan=-.3 if i%2 else .3)
    if i%4==0:note(st,f/2,.42,.075)
# Footfalls and fabric/door swoosh.
for t,p in [(0.49,-.3),(.99,.25),(1.47,-.3),(1.98,.25)]:foot(t,p)
sweep(2.32,.23,.10,-.1)
sweep(3.18,.22,.13,.3)
click(4.32,.11,.3)
# Digital robot turn and message streaks.
beep(6.08,690,.21,.17,.42)
beep(6.48,950,.18,.16,.32)
for i in range(5):
    click(6.80+i*.25,.10,pan=(i-2)*.2)
beep(8.16,1180,.20,.17,.3)
# Awkward beat at 9 seconds: bass plop, sparse accent.
beep(9.08,145,.28,.18,-.3)
click(9.74,.07,-.1)
# Punchline: a small motor, then an exaggerated confirmation button.
sweep(12.14,.39,.14,.38)
beep(13.44,430,.14,.27,.28)
click(13.55,.37,.15)
chime(13.76)
# Dry comedy ending; lower backing underneath final deadpan.
note(14.47,130.81,.41,.17)
# Soft cap, avoid clipping, short fade ends.
peak=max(max(abs(v) for v in left),max(abs(v) for v in right),1e-8)
gain=min(1.0,0.78/peak)
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True)
with wave.open(OUT,'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SAMPLE_RATE)
    buf=array.array('h')
    for i,(a,b) in enumerate(zip(left,right)):
        fade=min(1.0,(N-i)/(SAMPLE_RATE*.16))
        buf.append(int(max(-1,min(1,a*gain*fade))*32767))
        buf.append(int(max(-1,min(1,b*gain*fade))*32767))
    w.writeframes(buf.tobytes())
print(f'Generated original stereo soundtrack: {OUT} ({DURATION:.2f}s; peak before normalization {peak:.3f})')

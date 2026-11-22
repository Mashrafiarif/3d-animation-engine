# ADULTING.EXE — Max's First Day (Pilot 01)

Fully code-generated **15-second stylized 3D cartoon** with a character-led office joke and **original stereo SFX/music**. There are **NO recorded character voices yet**; the dialogue is represented by large on-screen captions in this version. It is an animation-blocking and pacing test.

## Storyboard: 15.0 seconds

| Time | Shot | Action | On-screen speaker and line | Sound cues |
|---|---|---|---|---|
| 00:00–00:03 | Tracking medium | Max walks into office, adjusts posture, nervous smile | MAX: OKAY… FIRST DAY. NEW JOB. NEW LIFE. | Four footsteps, light music, cloth swish |
| 00:03–00:06 | Office 2-shot | Boss points to robot | BOSS: MEET OUR NEW AI ASSISTANT. | Pan swoosh, click |
| 00:06–00:09 | Robot close | Robot turns and waves, floating email cards appear | ROBOT: I ALREADY ANSWERED YOUR EMAILS. | Robot beeps, digital clicks |
| 00:09–00:12 | Max close | Max freezes, eyes widen, points at himself | MAX: THEN… WHY DID YOU HIRE ME? | Comedic record drop, silence-like beat |
| 00:12–00:13.65 | Robot close | Robot gestures at a lime run button | ROBOT: TO CLICK… | Servo swoosh, button click |
| 00:13.65–00:15 | Max deadpan close | Max stares at the audience | ROBOT: RUN WORKFLOW. | Comedic chime and sting |

## Project structure

- `index.html`: complete Three.js office world, procedural characters, rigging, deterministic `renderAt(t)`, captions, camera and action timeline
- `render.mjs`: original screenshot-by-timestamp Playwright renderer (same mechanism used by your V1–V3 projects)
- `sound.py`: self-contained original soundtrack and timestamped SFX; no external libraries
- `package.json`: npm dependency manifest, Three.js + Playwright
- `.github/workflows/max-pilot.yml`: run by GitHub Actions, stored separately from this folder in the repo

## Running locally (optional)

With Node 22, Chromium, Python and FFmpeg available:

```bash
npm install
npx playwright install --with-deps --only-shell chromium
node render.mjs --width 432 --height 768 --fps 24 --seconds 15
python3 sound.py 15 output/sfx.wav
ffmpeg -y -framerate 24 -i output/frame_%05d.png -i output/sfx.wav -c:v libx264 -pix_fmt yuv420p -c:a aac -t 15 output/max-first-day-15s.mp4
```

## GitHub upload from an iPhone

1. At repository root, create `adulting-pilot/.gitkeep` with `placeholder` contents, commit.
2. Open `adulting-pilot`, then use `••• → Upload files` to upload the **five files** from `01_UPLOAD_IN_ADULTING_PILOT`.
3. Open `.github/workflows`, upload the **one** `max-pilot.yml` file from `02_UPLOAD_IN_WORKFLOWS`, commit.
4. Go to Actions, choose **Render MAX Pilot — Adulting.EXE**, tap **Run workflow**.
5. Use **portrait-preview, 24 FPS** for the first run. The duration is already fixed at **15 seconds**.
6. Download the artifact `MAX-first-day-15s-preview` and extract the MP4. Send the MP4 for actual render review.

Nothing in this package replaces your existing `threejs-demo` or `threejs-demo.yml`.

## Verification status

**Checked:** JavaScript syntax, Python compilation, workflow YAML structure, original stereo WAV output and 15-second duration.

**Not yet checked:** actual Three.js WebGL frame rendering or end-to-end GitHub Actions execution. The first Actions run is the source of truth for visual quality and success. It may need debugging based on run logs.

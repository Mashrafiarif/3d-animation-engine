# Three.js animation demo for your existing Ai-video repository

This addition keeps existing files and workflows untouched. It adds only:

- `.github/workflows/threejs-demo.yml` — manually triggered renderer.
- `threejs-demo/index.html` — procedural 3D mascot/scene/camera.
- `threejs-demo/render.mjs` — renders exact timestamps with Playwright and headless Chromium/SwiftShader.
- `threejs-demo/sound.py` — original sound effects.
- `threejs-demo/package.json` — npm dependencies.
- `threejs-demo/README.md` — this guide.

## Upload from iPhone

A ZIP cannot be committed to GitHub and automatically expanded. Extract this ZIP in the iPhone **Files** app first. Then upload the five `threejs-demo/` files preserving their folder path, and separately add the workflow file with the exact path `.github/workflows/threejs-demo.yml` using **Add file → Create new file** on GitHub's website. Select `main` (or your repository's actual default branch) when committing. If Safari hides the web editor, use **Request Desktop Website**.

**Do not overwrite your existing repo-root `index.html`, `package.json` or workflows.**

After files are in GitHub:

1. Go to `https://github.com/Mashrafiarif/Ai-video/actions` and find **Render Three.js Demo with Sound**.
2. Tap **Run workflow**. Start with quality = `preview`, fps = `24`, seconds = `4`.
3. Wait for the run to complete; open it and download the `threejs-demo-video-with-sound` artifact.
4. Unzip to get `animation.mp4` and `sfx.wav`.

Quality choices: `preview` (640×360), `hd` (1280×720), `full` (1920×1080), `portrait-preview` (360×640), `portrait-hd` (720×1280), `portrait-full` (1080×1920). FPS options: 24, 30, 60. Duration options: 4, 8, 12 seconds. Start small: **the free standard GitHub Linux runner has no dedicated GPU**, and 1080p/60fps is slow and can time out.

The workflow can optionally mix in a file named `narration.mp3` stored in `threejs-demo/`. Do not commit confidential narration into a public repository.

## Technology / architecture

Three.js scene runs in Chromium via Playwright. Code sets the exact time for each 3D frame and screenshots the canvas. Python generates original sound effects, FFmpeg encodes PNGs and audio into H.264 + AAC MP4. This is genuine rasterized 3D geometry (not AI-generated stills). The sample is a demo, not a tested cinematic quality guarantee.

The demo has not been executed end-to-end on a current GitHub runner. Chromium WebGL software support sometimes changes; see the Actions log if rendering fails.

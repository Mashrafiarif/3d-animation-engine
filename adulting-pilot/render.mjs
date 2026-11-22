import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const get = (key, fallback) => {
  const i = args.indexOf(`--${key}`);
  return i === -1 ? fallback : Number(args[i + 1]);
};
const width = get('width', 640), height = get('height', 360);
const fps = get('fps', 24), seconds = get('seconds', 4);
if (![width, height, fps, seconds].every(Number.isFinite) || width < 1 || height < 1 || fps < 1 || seconds < 1) {
  throw Error('Invalid width/height/fps/seconds');
}
const out = path.join(root, 'output');
fs.mkdirSync(out, { recursive: true });

const server = http.createServer((req, res) => {
  const url = new URL(req.url ?? '/', 'http://127.0.0.1');
  const name = url.pathname === '/' ? '/index.html' : decodeURIComponent(url.pathname);
  const filename = path.resolve(root, '.' + name);
  if (!filename.startsWith(root + path.sep)) {
    res.writeHead(403).end(); return;
  }
  fs.readFile(filename, (err, data) => {
    if (err) { res.writeHead(404).end('not found'); return; }
    const type = filename.endsWith('.js') ? 'text/javascript' : filename.endsWith('.html') ? 'text/html' : 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-cache' });
    res.end(data);
  });
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const addr = server.address();
let browser;
try {
  browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']
  });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  page.on('pageerror', (error) => console.error('Browser error:', error.message));
  page.on('console', (message) => { if (message.type() === 'error') console.error('Page:', message.text()); });
  await page.goto(`http://127.0.0.1:${addr.port}/?w=${width}&h=${height}`, { waitUntil: 'load' });
  await page.waitForFunction(() => window.animationReady === true, { timeout: 60000 });
  const count = Math.ceil(fps * seconds);
  for (let frame = 0; frame < count; frame++) {
    const time = frame / fps;
    await page.evaluate((t) => window.renderAt(t), time);
    await page.screenshot({ path: path.join(out, `frame_${String(frame).padStart(5, '0')}.png`), timeout: 120000 });
    if ((frame + 1) % Math.max(1, Math.floor(fps)) === 0 || frame + 1 === count) {
      console.log(`Rendered ${frame + 1}/${count} frames (${Math.round((frame + 1) / count * 100)}%)`);
    }
  }
  console.log('Frames ready.');
} finally {
  if (browser) await browser.close();
  server.close();
}

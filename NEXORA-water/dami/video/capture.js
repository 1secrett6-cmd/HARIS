// Renders motion.html frame by frame and pipes JPEGs to ffmpeg. Usage: node capture.js <page.html> <music.wav> <out.mp4> [fps] [seconds]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const [, , page, music, out, fpsArg, secArg] = process.argv;
const FPS = +(fpsArg || 30), SEC = +(secArg || 52);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', (x) => errs.push(String(x)));
  await p.goto('file://' + page); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', music,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(FPS * SEC);
  for (let i = 0; i < total; i++) {
    await p.evaluate((t) => window.render(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  await b.close();
  if (errs.length) { console.error(errs); process.exit(1); }
})();

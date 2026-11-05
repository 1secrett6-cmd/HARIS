// Renders each job's HTML to a PDF (one page per element) and PNGs per element. Usage: node render.js jobs.json
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    const errs = []; p.on('pageerror', (x) => errs.push(String(x)));
    await p.goto('file://' + j.html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.pdf({ path: j.pdf, width: j.w + 'px', height: j.h + 'px', printBackground: true, pageRanges: j.pages || '', margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    const els = await p.$$(j.sel);
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${j.png}_${String(i + 1).padStart(2, '0')}.png` });
    if (errs.length) { console.error(j.html, errs); process.exit(1); }
    await p.close();
  }
  await b.close();
})();

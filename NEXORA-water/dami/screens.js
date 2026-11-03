// Captures screenshots of the DAMI app for the proposal and deck. Usage: node screens.js <dami.html> <outdir>
const { chromium } = require('playwright');
const [, , app, out] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1360, height: 860 }, deviceScaleFactor: 1.5 });
  const errs = []; p.on('pageerror', (x) => errs.push(String(x)));
  await p.goto('file://' + app); await p.waitForTimeout(700);
  await p.screenshot({ path: out + '/dash.png' });
  await p.click('#nav button[data-v=sos]'); await p.waitForTimeout(300);
  await p.click('#find'); await p.waitForTimeout(400); await p.click('#launch'); await p.waitForTimeout(2600);
  await p.screenshot({ path: out + '/sos.png' });
  await p.click('#nav button[data-v=fc]'); await p.waitForTimeout(500); await p.screenshot({ path: out + '/forecast.png' });
  await p.click('#nav button[data-v=donors]'); await p.waitForTimeout(300); await p.click('#d-send'); await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/donors.png' });
  await p.click('#nav button[data-v=mci]'); await p.waitForTimeout(300); await p.click('#mci-go'); await p.waitForTimeout(3500);
  await p.screenshot({ path: out + '/mci.png' });
  if (errs.length) { console.error(errs); process.exit(1); }
  await b.close();
})();

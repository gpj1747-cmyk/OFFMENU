// Renderiza manual/pdf-build.html a manual/OFFMENU-manual-de-identidad.pdf (A4 apaisado)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + path.join(__dirname, 'pdf-build.html'), { waitUntil: 'networkidle' });
  await p.waitForSelector('body[data-ready="1"]'); await p.waitForTimeout(600);
  const over = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((pg, i) => {
    const R = pg.getBoundingClientRect(); let worst = 0;
    pg.querySelectorAll('.body *, .side *').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) worst = Math.max(worst, r.bottom - (R.bottom - 40)); });
    return worst > 0 ? (i + 1) + ':' + Math.round(worst) : null; }).filter(Boolean));
  console.log('desbordes (página:px):', over.join(' ') || 'ninguno');
  await p.pdf({ path: path.join(__dirname, 'OFFMENU-manual-de-identidad.pdf'), printBackground: true, preferCSSPageSize: true });
  await b.close();
})();

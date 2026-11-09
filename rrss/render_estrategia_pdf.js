// Exporta rrss/estrategia.html a rrss/OFFMENU-estrategia-redes.pdf (A4 vertical)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
  await p.goto('file://' + path.join(__dirname, 'estrategia.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: path.join(__dirname, 'OFFMENU-estrategia-redes.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();

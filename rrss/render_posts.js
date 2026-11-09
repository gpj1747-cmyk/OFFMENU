// Exporta cada .post de posts-build.html a rrss/posts/<id>.png (1080 × 1350)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 1400 } });
  await p.goto('file://' + path.join(__dirname, 'posts-build.html'), { waitUntil: 'networkidle' });
  await p.waitForSelector('body[data-ready="1"]'); await p.waitForTimeout(400);
  const ids = await p.$$eval('.post', els => els.map(e => e.id));
  for (const id of ids) { await (await p.$('#' + id)).screenshot({ path: path.join(__dirname, 'posts', id + '.png') }); }
  console.log(ids.length + ' posts'); await b.close();
})();

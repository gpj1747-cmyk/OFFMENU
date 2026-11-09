// Exporta favicons, foto de perfil e imagen OG en PNG
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const K = __dirname;
  const shot = async (svg, s, out) => { const p = await b.newPage({ viewport: { width: s, height: s } }); await p.setContent(`<style>body{margin:0}svg{display:block;width:${s}px;height:${s}px}</style>${svg}`); await p.screenshot({ path: out }); await p.close(); };
  const fav = fs.readFileSync(path.join(K, 'favicon/favicon.svg'), 'utf8');
  for (const s of [16, 32, 48, 180, 192, 512]) await shot(fav, s, path.join(K, 'favicon', s === 180 ? 'apple-touch-icon.png' : `favicon-${s}.png`));
  const per = fs.readFileSync(path.join(K, 'perfil/offmenu-perfil-instagram.svg'), 'utf8');
  for (const s of [1080, 2048]) await shot(per, s, path.join(K, 'perfil', `offmenu-perfil-instagram-${s}.png`));
  const logo = fs.readFileSync(path.join(K, '../logo/svg/offmenu-logotipo-plantilla.svg'), 'utf8');
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Schibsted+Grotesk:wght@800&display=swap"><style>body{margin:0;width:1200px;height:630px;background:#42000E;color:#fff;font-family:'Schibsted Grotesk';display:flex;flex-direction:column;justify-content:space-between;padding:72px 80px;box-sizing:border-box}.l svg{width:760px;height:auto;display:block;color:#fff;--line:#F5302A}h1{margin:0;font-size:54px;font-weight:800;letter-spacing:-.035em;line-height:1}.r{display:flex;justify-content:space-between;align-items:flex-end}.m{font-family:'IBM Plex Mono';font-size:22px;letter-spacing:.06em;text-transform:uppercase;color:#F5302A}</style><div class="l">${logo}</div><div class="r"><h1>Cambia la carta,<br>no el QR.</h1><span class="m">offmenu.es</span></div>`);
  await p.waitForTimeout(1200); await p.screenshot({ path: path.join(K, 'og-image.png') });
  await b.close(); console.log('kit exportado');
})();

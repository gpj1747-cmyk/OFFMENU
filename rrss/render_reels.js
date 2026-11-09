// Renderiza cada reel fotograma a fotograma (30 fps) y lo monta en MP4 con ffmpeg.
// Uso: node rrss/render_reels.js [nombre ...]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs'); const { execSync } = require('child_process');
const FPS = 30;
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : ['presentacion', 'cafe', 'pulpo'];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'reels-build.html'), { waitUntil: 'networkidle' });
  await p.waitForSelector('body[data-ready="1"]');
  for (const n of names) {
    const tmp = path.join(require('os').tmpdir(), 'om-reel-' + n); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    await p.evaluate(n => window.__build(n), n);
    const dur = await p.evaluate(n => window.__dur(n), n); const total = Math.round(dur * FPS);
    for (let f = 0; f < total; f++) {
      await p.evaluate(t => window.__render(t), f / FPS);
      await p.screenshot({ path: path.join(tmp, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    }
    const out = path.join(__dirname, 'reels', 'reel-' + n + '.mp4');
    execSync(`ffmpeg -v error -y -framerate ${FPS} -i ${tmp}/%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart "${out}"`);
    fs.copyFileSync(path.join(tmp, String(Math.round(total * 0.35)).padStart(5, '0') + '.jpg'), path.join(__dirname, 'reels', 'reel-' + n + '-portada.jpg'));
    console.log(n, total, 'fotogramas →', path.relative(process.cwd(), out));
  }
  await b.close();
})();

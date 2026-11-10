const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const ROOT = require('path').resolve(__dirname, '..');
const SRC = require('path').join(__dirname, 'svg');
const OUT = require('path').join(ROOT, 'assets', 'img');
fs.mkdirSync(OUT, { recursive: true });

const jobs = [
  ['dash-hero', 1560, 1040],
  ['dash-inventory', 1440, 900],
  ['dash-sales', 1440, 900],
  ['dash-wholesale', 1440, 900],
  ['dash-expenses', 1440, 900],
  ['dash-reporting', 1440, 900],
  ['og-image', 1200, 630],
];

(async () => {
  for (const [name, w, h] of jobs) {
    const svg = fs.readFileSync(path.join(SRC, name + '.svg'));
    const base = sharp(svg, { density: 96 }).resize(w, h, { fit: 'fill' });
    await base.clone().png({ compressionLevel: 9, palette: true, quality: 92 })
      .toFile(path.join(OUT, name + '.png'));
    await base.clone().jpeg({ quality: 90, mozjpeg: true })
      .toFile(path.join(OUT, name + '.jpg'));
    console.log('rendered', name);
  }
  // webp for site usage
  for (const [name, w, h] of jobs) {
    await sharp(fs.readFileSync(path.join(SRC, name + '.svg')), { density: 96 })
      .resize(w, h, { fit: 'fill' }).webp({ quality: 88, effort: 6 })
      .toFile(path.join(OUT, name + '.webp'));
  }
  console.log('webp done');
})();

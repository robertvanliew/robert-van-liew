// Captures live-site screenshots for the Jersey City Sound and Lily's Secret
// case studies. Committed so shots can be retaken when either site changes.
//
// Usage: node capture_case_studies.js
//        node capture_case_studies.js jcs
//        node capture_case_studies.js lily

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const OUT = path.join(__dirname, 'images');

const DESKTOP = { width: 1440, height: 900, deviceScaleFactor: 2 };
const MOBILE = { width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true };

async function settle(page) {
  try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 1200));
}

async function shoot(page, url, viewport, file, opts = {}) {
  await page.setViewport(viewport);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  await settle(page);
  if (opts.before) await opts.before(page);
  // WebP at q92 is visually lossless on these screenshots and roughly 90%
  // smaller than PNG at the same 2x resolution. Do not switch back to PNG:
  // the case study pages were 7 MB of images before this.
  const target = path.join(OUT, file);
  await page.screenshot({
    path: target,
    type: 'webp',
    quality: 92,
    fullPage: false,
  });
  console.log('captured', file);
}

async function captureJcs(page) {
  const base = 'https://jerseycitysound.com';
  await shoot(page, base + '/archive.html', DESKTOP, 'jcs-archive.webp');
  await shoot(page, base + '/entry-dj-dx.html', DESKTOP, 'jcs-entry.webp');
  await shoot(page, base + '/legends.html', DESKTOP, 'jcs-legends.webp');
  await shoot(page, base + '/entry-dj-dx.html', MOBILE, 'jcs-entry-mobile.webp');
}

async function captureLily(page) {
  const base = 'https://www.lilysecretcandles.com';

  await shoot(page, base + '/', DESKTOP, 'lily-hero.webp');

  await shoot(page, base + '/', DESKTOP, 'lily-reveal.webp', {
    before: async p => {
      await p.evaluate(() => {
        const s = document.getElementById('secret');
        if (s) s.scrollIntoView({ block: 'center' });
      });
      await new Promise(r => setTimeout(r, 800));
      await p.evaluate(() => {
        const b = document.getElementById('lightBtn');
        if (b) b.click();
      });
      await new Promise(r => setTimeout(r, 5000));
    },
  });

  await shoot(page, base + '/', DESKTOP, 'lily-builder.webp', {
    before: async p => {
      // Sections carry a .reveal class driven by an IntersectionObserver, so
      // content is transparent until it has been scrolled past once. Walk the
      // page down to fire every observer before framing the shot.
      await p.evaluate(async () => {
        const step = window.innerHeight * 0.8;
        for (let y = 0; y < document.body.scrollHeight; y += step) {
          window.scrollTo(0, y);
          await new Promise(r => setTimeout(r, 120));
        }
      });
      await new Promise(r => setTimeout(r, 800));

      // .builder holds the actual step fieldsets. #create includes the section
      // header above it, which frames mostly empty background.
      const found = await p.evaluate(() => {
        const t = document.querySelector('#create .builder');
        if (!t) return false;
        const y = t.getBoundingClientRect().top + window.scrollY;
        window.scrollTo(0, y - 40);
        return true;
      });
      if (!found) throw new Error('#create .builder not found');
      await new Promise(r => setTimeout(r, 1500));

      const filled = await p.evaluate(() => {
        const chips = document.getElementById('fragChips');
        return !!chips && chips.children.length > 0;
      });
      if (!filled) throw new Error('fragrance chips did not render');
    },
  });

  await shoot(page, base + '/', MOBILE, 'lily-rtl.webp', {
    before: async p => {
      // The menu items are buttons carrying data-lang. Click the button, not
      // the li that wraps it, or the language never changes.
      await p.evaluate(() => {
        const btn = document.getElementById('langBtn');
        if (btn) btn.click();
      });
      await new Promise(r => setTimeout(r, 500));
      const switched = await p.evaluate(() => {
        const ar = document.querySelector('#langMenu button[data-lang="ar"]');
        if (!ar) return false;
        ar.click();
        return true;
      });
      if (!switched) throw new Error('Arabic language button not found');
      await new Promise(r => setTimeout(r, 1800));
      // Close the dropdown and dismiss the promo ribbon so the figure shows the
      // mirrored layout rather than an open menu.
      await p.evaluate(() => {
        const btn = document.getElementById('langBtn');
        if (btn && btn.getAttribute('aria-expanded') === 'true') btn.click();
        const close = document.getElementById('ribbonClose');
        if (close) close.click();
        window.scrollTo(0, 0);
      });
      await new Promise(r => setTimeout(r, 900));
      const dir = await p.evaluate(() => document.documentElement.getAttribute('dir'));
      if (dir !== 'rtl') throw new Error('expected dir="rtl", got ' + dir);
      await new Promise(r => setTimeout(r, 300));
    },
  });
}

(async () => {
  const which = process.argv[2] || 'all';
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error') console.log('  page error:', m.text()); });

  try {
    if (which === 'all' || which === 'jcs') await captureJcs(page);
    if (which === 'all' || which === 'lily') await captureLily(page);
  } finally {
    await browser.close();
  }
  console.log('done');
})();

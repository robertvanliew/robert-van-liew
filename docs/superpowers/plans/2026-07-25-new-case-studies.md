# New Case Studies Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship two new case study pages on robertvanliew.com, The Jersey City Sound and Lily's Secret, with real captured imagery, portfolio cards, and routing.

**Architecture:** Both pages are static HTML cloned from `case-study-take-me-back-bingo.html`, the current best-formed template. Each page carries its own inline `<style>` block, which is the established pattern in this repo. Only the two accent tokens change per project so the whole case study set reads as one site. Imagery is captured from the live sites with a committed puppeteer script.

**Tech Stack:** Static HTML, CSS, JSON-LD, puppeteer 24.x (already in devDependencies), Vercel rewrites.

**Spec:** `docs/superpowers/specs/2026-07-25-new-case-studies-design.md`

## Global Constraints

Every task's requirements implicitly include this section.

- **No em dashes** in any file that ships. Use periods, commas, colons, or semicolons.
- **No AI-tell vocabulary** anywhere: `delve`, `tapestry`, `ever-evolving`, `robust`, `leverage`, `seamlessly`, `navigate the landscape`, `crafted`, `curated`, `elevated`, `bespoke`, `thoughtful`, `elegantly`, `beautifully`.
- **No "it's not just X, it's Y"** constructions. No faux-profound openers.
- **No AI tooling named in narrative prose.** Claude and Gemini appear only in the portfolio Tools list, nowhere in case study copy.
- **Verified numbers only.** The verified facts are: 247 generated entries, 248 total entry pages, 1 hand-authored page (`entry-dj-dx.html`), 10 memorial entries, 6 languages, 7 fragrances, Lighthouse 98/100/100/100.
- **Domain in canonical/OG/Twitter URLs is `https://www.robertvanliew.com`** with no trailing slash before the route.
- Every file written is committed. Frequent commits, one per task.

---

## File Structure

| File | Responsibility |
|---|---|
| `capture_case_studies.js` | Puppeteer capture of live-site screenshots into `images/`. Committed so shots can be retaken. |
| `verify_case_studies.js` | Verification sweep: em dashes, banned phrases, JSON-LD validity, image path existence. |
| `case-study-jersey-city-sound.html` | The JCS case study page, self-contained. |
| `case-study-lilys-secret.html` | The Lily's Secret case study page, self-contained. |
| `Portfolio.html` | Two new `.project-card` blocks appended to the work grid. |
| `vercel.json` | Two rewrites. |
| `sitemap.xml` | Two url entries. |
| `llms.txt` | Two case study lines. |

---

## Verified Facts Reference

Copy values from here. Do not re-derive, do not round.

**The Jersey City Sound** (`C:\Users\12124\Documents\Jersey City Sound`, live at jerseycitysound.com)

- `data/entries.json` is a dict with keys `entries` and `discovered_candidates`. `entries` has **247** items.
- Entry object keys: `card`, `entry_no`, `facts`, `genres`, `name`, `roles`, `slug`, `sources`, `status`, `todo_robert`, `years_active`.
- `status` distribution: **237 archive, 10 memorial**.
- `design/` holds **248** `entry-*.html` files. The extra one is `entry-dj-dx.html`, hand-authored, absent from `entries.json`, left untouched by the generator.
- Generator: `execution/generate_entry_pages.py`. Run with `py execution/generate_entry_pages.py`.
- Non-entry pages in `design/`: `index`, `archive`, `legends`, `sources`, `history`, `charts`, `chilltown`, `jersey-city-djs`, `report`, `report-001-not-from-jersey-city`, `about`, `corrections`, `suggest-edit`, `verify`, `privacy`, `terms`, `404`.
- Also generated: `archive-data.js` (client-side search index), `llms.txt`, `llms-full.txt`, `robots.txt`, `sitemap.xml`.
- Deploy: `.github/workflows/deploy-pages.yml` publishes `design/` to GitHub Pages on push to main. Custom domain via `design/CNAME`.
- Owner: Frankpella LLC. Content licensed CC BY-SA 4.0.
- Brand tokens from `JERSEY-CITY-SOUND-DESIGN-SPEC.md`: `--ink #0B0B0C`, `--paper #F7F4EC`, `--cream #F5F2EA`, `--night #0E0E10`, `--gold #C9A227`, `--gold-light #EED27A`, `--gold-deep #9C7A14`, `--gold-ink #7A5E0E`, `--rule #D9D2C2`.
- Editorial standard: cite-or-cut. Mission line: "Every voice in the city, on the record."
- Logos in `design/assets/`: `jerseycitysound-primary.png`, `jerseycitysound-reversed.png`, `jerseycitysound-transparent.png`, `jerseycitysound-transparent-light.png`, `jerseycitysound-cream.png`.

**Lily's Secret** (`C:\Users\12124\Documents\Lily's Website`, live at lilysecretcandles.com)

- Palette from `css/styles.css` `:root`: `--wine-900 #2B0710`, `--wine-800 #3A0A15`, `--wine-700 #4A0E1C`, `--wine-600 #5E1626`, `--wine-500 #732033`, `--cream #F3EBDB`, `--cream-100 #FBF6EC`, `--cream-200 #EDE2CD`, `--gold #C9A24B`, `--gold-bright #E6C67E`, `--gold-deep #7D5A1C`, `--ink #2A1712`, `--ink-soft #5C463C`.
- Type: Cormorant Garamond display, Jost body.
- Stylesheet comment names the direction: "Sealed-Letter Luxury. Deep wine, antique gold, cream, candle-glow."
- Languages in `js/i18n.js`: **en, ar, tr, fr, ru, hi**. Arabic is full RTL.
- **7** fragrances: Exotic Dream, Amber Tale, Velvet Coffee, Summer Sun, Pure Silk, Sweet Escape, Istanbul Tulip.
- Schema in `index.html`: `Organization` + `LocalBusiness` (`addressCountry: AE`, `areaServed: United Arab Emirates`), `WebSite`, `Product`, `ItemList` of the 7 fragrances, `FAQPage` with 5 questions.
- Order delivery: Formspree, endpoint held in a single `FORM_ENDPOINT` constant in `js/main.js`. Empty string falls back to a pre-filled email.
- Public address `hello@lilysecretcandles.com` is an ImprovMX alias forwarding to the studio inbox.
- Sections: hero, promise, secret, how, fragrances, craft, occasions, contact.
- Interactive reveal element ids: `#candle`, `#flame`, `#disc`, `#secretMsg`, `#lightBtn`, `#nextMsg`, `#revealHint`, `#revealList`.
- Commit `a03d5cf` records "Add hero video; Lighthouse pass → 98/100/100/100".
- Commit `a60968c` records "Add a rising smoke wisp when the candle is blown out".
- Legal pages with real registered entity and licence details: `terms.html`, `privacy.html`, `returns.html`.
- Images available at `assets/images/`: `hero-candle-seal.jpeg`, `product-clean.jpeg`, `product-white.jpeg`, `lifestyle-cafe.jpeg`, `journey-4panel.jpeg`, `message-disc-topdown.jpeg`, `disc-dubai.jpeg`, `disc-flame.jpeg`, `disc-habibi.jpeg`, `behind-pour-1.jpeg`, `behind-pour-2.jpeg`, `launch-banner.jpeg`, `logo-seal.png`, `og-share.jpg`.

**Accent tokens to use**

| Page | `--accent` | `--accent-warm` | Figure frame bg | Figure frame border |
|---|---|---|---|---|
| Jersey City Sound | `#9C7A14` | `#C9A227` | `#0E0E10` | `rgba(201,162,39,0.22)` |
| Lily's Secret | `#7D5A1C` | `#C9A24B` | `#2B0710` | `rgba(201,162,75,0.22)` |

---

## Task 1: Capture script and imagery

**Files:**
- Create: `capture_case_studies.js`
- Create: `images/jcs-archive.png`, `images/jcs-entry.png`, `images/jcs-legends.png`, `images/jcs-entry-mobile.png`, `images/jcs-logo.png`
- Create: `images/lily-hero.jpg`, `images/lily-reveal.jpg`, `images/lily-builder.jpg`, `images/lily-rtl.jpg`, `images/lily-card.jpg`

**Interfaces:**
- Consumes: nothing.
- Produces: the ten image files above. Tasks 2, 3, and 4 reference these exact paths.

- [ ] **Step 1: Write the capture script**

Create `capture_case_studies.js`:

```js
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
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.evaluate(() => new Promise(r => setTimeout(r, 1200)));
}

async function shoot(page, url, viewport, file, opts = {}) {
  await page.setViewport(viewport);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  await settle(page);
  if (opts.before) await opts.before(page);
  const target = path.join(OUT, file);
  const isJpeg = file.endsWith('.jpg');
  await page.screenshot({
    path: target,
    type: isJpeg ? 'jpeg' : 'png',
    quality: isJpeg ? 85 : undefined,
    fullPage: false,
  });
  console.log('captured', file);
}

async function captureJcs(page) {
  const base = 'https://jerseycitysound.com';
  await shoot(page, base + '/archive.html', DESKTOP, 'jcs-archive.png');
  await shoot(page, base + '/entry-dj-dx.html', DESKTOP, 'jcs-entry.png');
  await shoot(page, base + '/legends.html', DESKTOP, 'jcs-legends.png');
  await shoot(page, base + '/entry-dj-dx.html', MOBILE, 'jcs-entry-mobile.png');
}

async function captureLily(page) {
  const base = 'https://www.lilysecretcandles.com';

  await shoot(page, base + '/', DESKTOP, 'lily-hero.jpg');

  await shoot(page, base + '/', DESKTOP, 'lily-reveal.jpg', {
    before: async p => {
      await p.evaluate(() => {
        const s = document.getElementById('secret');
        if (s) s.scrollIntoView({ behavior: 'instant', block: 'center' });
      });
      await p.evaluate(() => new Promise(r => setTimeout(r, 600)));
      await p.evaluate(() => {
        const b = document.getElementById('lightBtn');
        if (b) b.click();
      });
      await p.evaluate(() => new Promise(r => setTimeout(r, 4500)));
    },
  });

  await shoot(page, base + '/', DESKTOP, 'lily-builder.jpg', {
    before: async p => {
      await p.evaluate(() => {
        const t = document.getElementById('contact') || document.getElementById('occasions');
        if (t) t.scrollIntoView({ behavior: 'instant', block: 'start' });
      });
      await p.evaluate(() => new Promise(r => setTimeout(r, 900)));
    },
  });

  await shoot(page, base + '/', MOBILE, 'lily-rtl.jpg', {
    before: async p => {
      await p.evaluate(() => {
        const btn = document.getElementById('langBtn');
        if (btn) btn.click();
      });
      await p.evaluate(() => new Promise(r => setTimeout(r, 400)));
      await p.evaluate(() => {
        const items = Array.from(document.querySelectorAll('#langMenu [role="option"], #langMenu li, #langMenu button'));
        const ar = items.find(el => /ar|عرب/i.test(el.textContent || '') || el.dataset.lang === 'ar');
        if (ar) ar.click();
      });
      await p.evaluate(() => new Promise(r => setTimeout(r, 1500)));
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
```

- [ ] **Step 2: Run the capture and verify it produced files**

```bash
node capture_case_studies.js
```

Expected: eight "captured" lines then "done". If a page 404s or a selector misses, note which one and continue; Step 4 covers the fallback.

- [ ] **Step 3: Copy the two card images from the project folders**

```bash
cp "/c/Users/12124/Documents/Jersey City Sound/design/assets/jerseycitysound-reversed.png" images/jcs-logo.png
cp "/c/Users/12124/Documents/Lily's Website/assets/images/hero-candle-seal.jpeg" images/lily-card.jpg
```

- [ ] **Step 4: Verify all ten files exist and are non-trivial**

```bash
for f in jcs-archive.png jcs-entry.png jcs-legends.png jcs-entry-mobile.png jcs-logo.png \
         lily-hero.jpg lily-reveal.jpg lily-builder.jpg lily-rtl.jpg lily-card.jpg; do
  if [ -s "images/$f" ]; then
    echo "OK   $f $(stat -c%s "images/$f") bytes"
  else
    echo "MISS $f"
  fi
done
```

Expected: ten `OK` lines, every size above 20000 bytes.

For any `MISS`, fall back to the corresponding source asset in the project folder and adjust that figure's caption in Task 2 or Task 3 so it never claims to be a screenshot of something it is not. Record which figures fell back.

- [ ] **Step 5: Visually confirm the two interaction shots**

Open `images/lily-reveal.jpg` and `images/jcs-legends.png`. The reveal shot must show the message visible in the glass, not the unlit candle. The Legends shot must show the dark night theme, not the paper theme. If either is wrong, adjust the wait in `capture_case_studies.js` and rerun `node capture_case_studies.js lily` or `jcs`.

- [ ] **Step 6: Commit**

```bash
git add capture_case_studies.js images/jcs-*.png images/lily-*.jpg
git commit -m "feat(case-study): add capture script and live-site imagery for two new case studies"
```

---

## Task 2: The Jersey City Sound case study page

**Files:**
- Create: `case-study-jersey-city-sound.html`
- Reference: `case-study-take-me-back-bingo.html` (template source, do not modify)

**Interfaces:**
- Consumes: `images/jcs-archive.png`, `images/jcs-entry.png`, `images/jcs-legends.png`, `images/jcs-entry-mobile.png` from Task 1.
- Produces: the file `case-study-jersey-city-sound.html`, reachable at route `/jersey-city-sound-case-study` once Task 5 lands.

- [ ] **Step 1: Copy the template**

```bash
cp case-study-take-me-back-bingo.html case-study-jersey-city-sound.html
```

- [ ] **Step 2: Replace the head block**

Replace everything from `<title>` through the closing `</script>` of the JSON-LD block with:

```html
<title>The Jersey City Sound, Case Study, Robert Van Liew</title>
<meta name="description" content="Case study: a static encyclopedia-archive of Jersey City music culture. 247 entries generated from one data file, a cite-or-cut editorial standard, and a schema layer built to be cited by search engines and language models.">
<meta name="author" content="Robert Van Liew">
<link rel="canonical" href="https://www.robertvanliew.com/jersey-city-sound-case-study">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">

<meta property="og:type" content="article">
<meta property="og:url" content="https://www.robertvanliew.com/jersey-city-sound-case-study">
<meta property="og:title" content="The Jersey City Sound, Case Study, Robert Van Liew">
<meta property="og:description" content="247 entries generated from one data file, a cite-or-cut editorial standard, and a schema layer built to be cited by search engines and language models.">
<meta property="og:image" content="https://www.robertvanliew.com/images/og-cover.png">
<meta property="og:site_name" content="Robert Van Liew">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://www.robertvanliew.com/jersey-city-sound-case-study">
<meta name="twitter:title" content="The Jersey City Sound, Case Study, Robert Van Liew">
<meta name="twitter:description" content="247 entries generated from one data file, a cite-or-cut editorial standard, and a schema layer built to be cited by search engines and language models.">
<meta name="twitter:image" content="https://www.robertvanliew.com/images/og-cover.png">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CreativeWork",
      "@id": "https://www.robertvanliew.com/jersey-city-sound-case-study#creativework",
      "name": "The Jersey City Sound, Case Study",
      "url": "https://www.robertvanliew.com/jersey-city-sound-case-study",
      "description": "Case study covering the design and build of jerseycitysound.com. Information architecture where 247 entries live in one data file, a Python generator that writes the entire site, a cite-or-cut editorial standard, and a schema layer built for citation by search engines and language models.",
      "datePublished": "2026-07-25",
      "dateModified": "2026-07-25",
      "author": {
        "@type": "Person",
        "name": "Robert Van Liew",
        "url": "https://www.robertvanliew.com/"
      },
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://www.robertvanliew.com/#website"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.robertvanliew.com/" },
        { "@type": "ListItem", "position": 2, "name": "Work", "item": "https://www.robertvanliew.com/#work" },
        { "@type": "ListItem", "position": 3, "name": "The Jersey City Sound", "item": "https://www.robertvanliew.com/jersey-city-sound-case-study" }
      ]
    }
  ]
}
</script>
```

- [ ] **Step 3: Swap the accent tokens and figure frame**

In the `:root` block, change only these two lines:

```css
    --accent:      #9C7A14;
    --accent-warm: #C9A227;
```

In `.cs-figure__frame`, change the background and border:

```css
  .cs-figure__frame {
    background: #0E0E10;
    border: 1px solid rgba(201, 162, 39, 0.22);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 18px 48px rgba(11, 11, 12, 0.22);
  }
```

Leave every other token and rule untouched.

- [ ] **Step 4: Replace the nav and page body**

Replace everything between `<body>` and `</body>` with:

```html
<nav>
  <a href="/" class="nav-back">&larr; Portfolio</a>
  <span class="nav-crumb">case study / jersey-city-sound</span>
  <span class="nav-tag">Archive &middot; 2026</span>
</nav>

<div class="page">

  <div class="project-eyebrow">
    <a href="/" class="nav-back">&larr; Work</a>
    <span class="sep">/</span>
    <span class="crumb-cur">The Jersey City Sound</span>
  </div>

  <h1 class="title">The Jersey City <em>Sound</em></h1>

  <div class="project-tags">
    <span>Information Architecture</span>
    <span>Static Generation</span>
    <span>Editorial Standards</span>
    <span>Schema &amp; AEO</span>
    <span>End-to-End</span>
  </div>

  <div class="cs-intro">
    <div class="cs-desc">
      Jersey City has produced DJs, producers, and artists for fifty years, and almost none of it has been written down in one place. The Jersey City Sound is the archive that fixes that. It documents the people, venues, crews, and labels that built the scene, with a source attached to every claim. The site has to outlive its own maintenance, so it is static HTML with no framework, no bundler, and no database. I founded it, designed it, and built it at <a href="https://jerseycitysound.com" target="_blank" rel="noopener">jerseycitysound.com</a>. This case study covers the two decisions that carry the project: an information architecture where every entry lives in one data file and the whole site is generated from it, and a discovery layer built so that search engines and language models cite the archive by name.
    </div>
    <div class="cs-meta-list">
      <div class="cs-meta-item">
        <div class="k">Role</div>
        <div class="v">Founder, Designer &amp; Engineer</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Owner</div>
        <div class="v">Frankpella LLC</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Stack</div>
        <div class="v">Static HTML, CSS, Python, GitHub Actions, GitHub Pages</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Live</div>
        <div class="v"><a href="https://jerseycitysound.com" target="_blank" rel="noopener">jerseycitysound.com &nearr;</a></div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Scope</div>
        <div class="v">Brand system, information architecture, entry template, generator, search, schema, memorial wing</div>
      </div>
    </div>
  </div>

  <div class="cs-section">
    <div class="cs-section-label">01 &middot; Information Architecture</div>
    <h2 class="cs-section-title">247 Entries, One Source of Truth</h2>
    <p class="cs-section-body">An archive fails in one of two ways. It either becomes a CMS nobody maintains, or it becomes a pile of hand-edited pages that drift out of sync. The decision here was to make the data the site. Every entry, with its facts, sources, cross-links, galleries, and media, lives in a single file at <code>data/entries.json</code>. There are <strong>247</strong> of them. Nothing about an entry is stored in its page, because the page does not exist until the generator writes it.</p>
    <p class="cs-section-body">One Python file, <code>execution/generate_entry_pages.py</code>, reads that data and writes the site. Every entry page, the archive index, the Legends memorial wing, the Sources bibliography, the sitemap, <code>robots.txt</code>, and <code>llms.txt</code>. It also deletes orphans, so an entry removed from the data disappears from the site instead of lingering as a dead URL. A correction from a family member is a one-line edit and a commit, not a content migration.</p>
    <p class="cs-section-body">There is exactly one exception. <code>entry-dj-dx.html</code> is hand-authored and the generator leaves it alone, which makes <strong>248</strong> entry pages against 247 data records. That exception is the proof the template is right. A page written by hand and a page written by the script are indistinguishable in the browser, which is the standard the entry template had to meet before I let it generate anything.</p>

    <div class="schema-grid">
      <div class="schema-pill">
        <div class="k">Source of truth</div>
        <div class="v">One JSON file</div>
        <div class="sub">247 entries with facts, sources, roles, years, galleries</div>
      </div>
      <div class="schema-pill">
        <div class="k">Generator</div>
        <div class="v">248 pages, one script</div>
        <div class="sub">Entries, archive, Legends, sources, sitemap, robots, llms.txt</div>
      </div>
      <div class="schema-pill">
        <div class="k">Editorial standard</div>
        <div class="v">Cite or cut</div>
        <div class="sub">Numbered sources block built into the template, not optional</div>
      </div>
      <div class="schema-pill">
        <div class="k">Legends wing</div>
        <div class="v">10 memorial entries</div>
        <div class="sub">Night and gold inversion, same logo, same grid</div>
      </div>
      <div class="schema-pill">
        <div class="k">Search</div>
        <div class="v">Generated index</div>
        <div class="sub">archive-data.js, client-side, no server, no query cost</div>
      </div>
      <div class="schema-pill">
        <div class="k">Deployment</div>
        <div class="v">Push to publish</div>
        <div class="sub">GitHub Actions ships the built folder to Pages on every push</div>
      </div>
    </div>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/jcs-archive.png" alt="The Jersey City Sound archive index, an A to Z list of documented entries on archival paper" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 1.</strong> The archive index. Every entry the generator has written, filterable by role and era, searching against a client-side index that is itself generated from the same data file.</figcaption>
    </figure>

    <p class="cs-section-body" style="margin-top:28px;">The entry template is the core unit, so it got the most attention. Breadcrumb, entry number set in letterspaced caps, name in a display serif, then a Record Card infobox holding the portrait, years active, roles, genres, notable works, affiliations, and official links behind a gold hairline frame. Below that a lead paragraph, then Career, Notable Works, Credits and Receipts, In the Community, Gallery, numbered Sources, a claim bar, and three related entries. The lead paragraph is written to a specific brief: forty to sixty words, self-contained, answering who this person is with no surrounding context needed. That is the passage a reader skims and the passage a language model quotes.</p>

    <p class="cs-section-body">The editorial standard is cite or cut. Nothing enters the archive without a source. That is a design constraint before it is an editorial one, because it forces the numbered sources block into the template as a permanent section rather than an optional footer. It also sets the tone: museum label, not music blog. Factual, warm, no hype, no beef. Receipts instead of adjectives.</p>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/jcs-entry.png" alt="An entry page showing the Record Card infobox, lead paragraph, and numbered sources" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 2.</strong> An entry page. The Record Card carries the structured facts, the lead paragraph is written to stand alone, and the numbered sources sit on the page rather than behind a link.</figcaption>
    </figure>

    <p class="cs-section-body" style="margin-top:28px;">The site runs two themes. Archival paper by default, warm and slightly off-white, with hairline rules instead of boxes and gold used like gilding at roughly five percent of any page. The Legends memorial wing inverts to night and gold. Same logo, same typefaces, same grid, same spacing. Ten entries live there. The inversion is enough to make the wing feel like a different room without making it a second brand, which matters because these are memorial pages for people the community lost and they should not read like a themed microsite.</p>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/jcs-legends.png" alt="The Legends memorial wing rendered in the night and gold theme" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 3.</strong> The Legends wing. The theme inverts to night and gold, everything else holds, so the memorial pages read as part of the same building.</figcaption>
    </figure>
  </div>

  <div class="cs-section">
    <div class="cs-section-label">02 &middot; Discovery</div>
    <h2 class="cs-section-title">Built to Be Cited</h2>
    <p class="cs-section-body">An archive that nobody finds is a private document. The goal was blunter than ranking: when someone asks who the first Jersey City DJs were, whether they ask Google or they ask a model, the answer should come from the people who were actually there. That means writing for extraction, not just for keywords.</p>
    <p class="cs-section-body">Every entry ships <strong>Person</strong> or <strong>MusicGroup</strong> schema with <code>sameAs</code> links out to official sites, streaming profiles, and Wikidata, plus a <strong>BreadcrumbList</strong>. Sitewide there is <strong>Organization</strong> with <code>areaServed</code> set to Jersey City, and <strong>WebSite</strong>. The pillar and history pages carry <strong>FAQPage</strong> blocks phrased the way people actually ask. The sitemap is generated, so it cannot fall behind the content.</p>
    <p class="cs-section-body">The writing does the rest. Claims are countable. Years active, residencies with date ranges, stream counts, release numbers, each with a source next to it. "Legendary" is not a fact and does not appear. Language models extract passages rather than pages, so the lead paragraph on every entry is built as a standalone definition and the sources sit inline where they can be seen. <code>llms.txt</code> and <code>llms-full.txt</code> sit at the root, and <code>robots.txt</code> explicitly welcomes GPTBot, ClaudeBot, PerplexityBot, and Google-Extended rather than defaulting them out.</p>

    <div class="schema-grid">
      <div class="schema-pill">
        <div class="k">Person / MusicGroup</div>
        <div class="v">Per entry</div>
        <div class="sub">sameAs out to official sites, streaming, and Wikidata</div>
      </div>
      <div class="schema-pill">
        <div class="k">Organization</div>
        <div class="v">Geographic anchor</div>
        <div class="sub">areaServed Jersey City, founder linked, sitewide WebSite graph</div>
      </div>
      <div class="schema-pill">
        <div class="k">Lead paragraph</div>
        <div class="v">Extractable by design</div>
        <div class="sub">40 to 60 words, self-contained, written to be quoted</div>
      </div>
      <div class="schema-pill">
        <div class="k">Sources</div>
        <div class="v">Numbered, on the page</div>
        <div class="sub">Visible citations, not a link to a bibliography</div>
      </div>
      <div class="schema-pill">
        <div class="k">llms.txt</div>
        <div class="v">Two files</div>
        <div class="sub">Short index and a full dump, both generated</div>
      </div>
      <div class="schema-pill">
        <div class="k">robots.txt</div>
        <div class="v">Crawlers welcomed</div>
        <div class="sub">GPTBot, ClaudeBot, PerplexityBot, Google-Extended allowed</div>
      </div>
    </div>

    <div class="flow-card">
      <div class="flow-row">
        <div class="flow-step">01 &middot; Document</div>
        <div class="flow-body">A name comes in from the community, often through Instagram or a family member. Facts get verified against a real source. If there is no source, it does not ship. The entry is added to <code>data/entries.json</code> with its citations attached.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">02 &middot; Generate</div>
        <div class="flow-body">One command rewrites every page from the data. The entry page, the archive index, the Legends wing if the entry is memorial, the sources bibliography, the search index, the sitemap, and both llms files. Orphaned pages are removed in the same pass.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">03 &middot; Publish</div>
        <div class="flow-body">Push to main. GitHub Actions ships the built folder to Pages behind the custom domain. There is no build server to maintain and no database to migrate, which is the point when the goal is permanence.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">04 &middot; Get cited</div>
        <div class="flow-body">Each documented name is a query with almost no competition. Every one that surfaces feeds authority back to the head terms, and the structured lead paragraph gives models something clean to quote when the question is asked in natural language.</div>
      </div>
    </div>

    <figure class="cs-figure cs-figure--phone">
      <div class="cs-figure__frame">
        <img src="images/jcs-entry-mobile.png" alt="An entry page on a phone, with the Record Card stacked above the article body" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 4.</strong> On mobile the Record Card moves from the right rail to the top of the page, so the structured facts arrive before the prose instead of after it.</figcaption>
    </figure>
  </div>

  <div class="outro">
    <div class="cs-section-label">Outro</div>
    <p class="outro-body">This one is a monument, not a media site. Static HTML with no dependencies means it still loads in twenty years, which is the actual requirement when the subject is people's history. The generator means a correction becomes a live page in one commit. The schema means the archive answers the question wherever the question gets asked. The hardest part was never the code. It was holding the line on cite or cut when a good story arrived without a source.</p>
    <a class="outro-cta" href="https://jerseycitysound.com" target="_blank" rel="noopener">Visit the live site &nearr;</a>
  </div>

</div>
```

- [ ] **Step 5: Verify no em dashes and no banned phrases**

```bash
grep -n "—" case-study-jersey-city-sound.html; echo "em-dash exit=$? (1 = clean)"
grep -niE "delve|tapestry|ever-evolving|robust|leverage|seamlessly|navigate the landscape|crafted|curated|elevated|bespoke|thoughtful" case-study-jersey-city-sound.html; echo "phrase exit=$? (1 = clean)"
```

Expected: both report `exit=1`.

- [ ] **Step 6: Verify the JSON-LD parses**

```bash
node -e "const h=require('fs').readFileSync('case-study-jersey-city-sound.html','utf8');const m=h.match(/<script type=\"application\/ld\+json\">([\s\S]*?)<\/script>/);JSON.parse(m[1]);console.log('JSON-LD OK')"
```

Expected: `JSON-LD OK`.

- [ ] **Step 7: Verify no stale Take Me Back Bingo strings survived the copy**

```bash
grep -niE "take.?me.?back|bingo|takemebackbingo|High Class Experience" case-study-jersey-city-sound.html; echo "exit=$? (1 = clean)"
```

Expected: `exit=1`.

- [ ] **Step 8: Verify every image path resolves**

```bash
grep -oE 'src="images/[^"]+"' case-study-jersey-city-sound.html | sed 's/src="//;s/"//' | while read p; do
  [ -s "$p" ] && echo "OK   $p" || echo "MISS $p"
done
```

Expected: four `OK` lines, no `MISS`.

- [ ] **Step 9: Open it and check the render**

Open `case-study-jersey-city-sound.html` in a browser. Confirm: gold accent on the italic title word, all four figures visible on dark frames, no console errors, and the layout collapses to one column when the window is narrowed below 820px.

- [ ] **Step 10: Commit**

```bash
git add case-study-jersey-city-sound.html
git commit -m "feat(case-study): add The Jersey City Sound case study"
```

---

## Task 3: The Lily's Secret case study page

**Files:**
- Create: `case-study-lilys-secret.html`
- Reference: `case-study-take-me-back-bingo.html` (template source, do not modify)

**Interfaces:**
- Consumes: `images/lily-hero.jpg`, `images/lily-reveal.jpg`, `images/lily-builder.jpg`, `images/lily-rtl.jpg` from Task 1.
- Produces: the file `case-study-lilys-secret.html`, reachable at route `/lilys-secret-case-study` once Task 5 lands.

- [ ] **Step 1: Copy the template**

```bash
cp case-study-take-me-back-bingo.html case-study-lilys-secret.html
```

- [ ] **Step 2: Replace the head block**

Replace everything from `<title>` through the closing `</script>` of the JSON-LD block with:

```html
<title>Lily's Secret, Case Study, Robert Van Liew</title>
<meta name="description" content="Case study: a UAE candle brand whose product hides a personal message in the wax. An interactive reveal that explains the product without copy, six languages including full Arabic RTL, and an order system that always lands in English.">
<meta name="author" content="Robert Van Liew">
<link rel="canonical" href="https://www.robertvanliew.com/lilys-secret-case-study">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">

<meta property="og:type" content="article">
<meta property="og:url" content="https://www.robertvanliew.com/lilys-secret-case-study">
<meta property="og:title" content="Lily's Secret, Case Study, Robert Van Liew">
<meta property="og:description" content="An interactive reveal that explains an invisible product, six languages including full Arabic RTL, and an order system that always lands in English.">
<meta property="og:image" content="https://www.robertvanliew.com/images/og-cover.png">
<meta property="og:site_name" content="Robert Van Liew">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://www.robertvanliew.com/lilys-secret-case-study">
<meta name="twitter:title" content="Lily's Secret, Case Study, Robert Van Liew">
<meta name="twitter:description" content="An interactive reveal that explains an invisible product, six languages including full Arabic RTL, and an order system that always lands in English.">
<meta name="twitter:image" content="https://www.robertvanliew.com/images/og-cover.png">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CreativeWork",
      "@id": "https://www.robertvanliew.com/lilys-secret-case-study#creativework",
      "name": "Lily's Secret, Case Study",
      "url": "https://www.robertvanliew.com/lilys-secret-case-study",
      "description": "Case study covering the design and build of lilysecretcandles.com. An interactive candle that reveals a hidden message, a made-to-order builder, six-language localisation including full Arabic right-to-left, and an order pipeline that delivers in English regardless of the visitor's language.",
      "datePublished": "2026-07-25",
      "dateModified": "2026-07-25",
      "author": {
        "@type": "Person",
        "name": "Robert Van Liew",
        "url": "https://www.robertvanliew.com/"
      },
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://www.robertvanliew.com/#website"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.robertvanliew.com/" },
        { "@type": "ListItem", "position": 2, "name": "Work", "item": "https://www.robertvanliew.com/#work" },
        { "@type": "ListItem", "position": 3, "name": "Lily's Secret", "item": "https://www.robertvanliew.com/lilys-secret-case-study" }
      ]
    }
  ]
}
</script>
```

- [ ] **Step 3: Swap the accent tokens and figure frame**

In the `:root` block, change only these two lines:

```css
    --accent:      #7D5A1C;
    --accent-warm: #C9A24B;
```

In `.cs-figure__frame`:

```css
  .cs-figure__frame {
    background: #2B0710;
    border: 1px solid rgba(201, 162, 75, 0.22);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 18px 48px rgba(43, 7, 16, 0.28);
  }
```

Leave every other token and rule untouched.

- [ ] **Step 4: Replace the nav and page body**

Replace everything between `<body>` and `</body>` with:

```html
<nav>
  <a href="/" class="nav-back">&larr; Portfolio</a>
  <span class="nav-crumb">case study / lilys-secret</span>
  <span class="nav-tag">Brand &middot; 2026</span>
</nav>

<div class="page">

  <div class="project-eyebrow">
    <a href="/" class="nav-back">&larr; Work</a>
    <span class="sep">/</span>
    <span class="crumb-cur">Lily's Secret</span>
  </div>

  <h1 class="title">Lily's <em>Secret</em></h1>

  <div class="project-tags">
    <span>Brand Site</span>
    <span>Interactive Product Demo</span>
    <span>Six-Language i18n</span>
    <span>Arabic RTL</span>
    <span>Order Systems</span>
  </div>

  <div class="cs-intro">
    <div class="cs-desc">
      Lily's Secret makes candles with a personal message set into the bottom of the glass. You only read it once the flame has burned all the way down. That is a lovely product and a hard website, because the thing you are selling is invisible in every photograph of it. The brief added two more constraints: customers across six language groups, and no online payment, since every candle is poured to order and confirmed by hand. I designed and built the site at <a href="https://www.lilysecretcandles.com" target="_blank" rel="noopener">lilysecretcandles.com</a>. This case study covers the interaction that explains the product without a line of marketing copy, and the language and order systems that let one person in the UAE actually run it.
    </div>
    <div class="cs-meta-list">
      <div class="cs-meta-item">
        <div class="k">Role</div>
        <div class="v">Designer &amp; Engineer</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Client</div>
        <div class="v">Lily's Secret, United Arab Emirates</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Stack</div>
        <div class="v">HTML, CSS, Vanilla JS, Formspree, WhatsApp, ImprovMX</div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Live</div>
        <div class="v"><a href="https://www.lilysecretcandles.com" target="_blank" rel="noopener">lilysecretcandles.com &nearr;</a></div>
      </div>
      <div class="cs-meta-item">
        <div class="k">Scope</div>
        <div class="v">Site design, interactive reveal, order builder, six languages with RTL, schema, legal pages</div>
      </div>
    </div>
  </div>

  <div class="cs-section">
    <div class="cs-section-label">01 &middot; The Core Interaction</div>
    <h2 class="cs-section-title">You Have to Burn It to Read It</h2>
    <p class="cs-section-body">The product problem came first. A candle photographs like a candle. The message is under the wax, so the one thing that makes this brand different is the one thing a photograph cannot show. Every version of solving that with copy read like a riddle, and riddles do not sell gifts.</p>
    <p class="cs-section-body">So the site does it instead of describing it. There is a candle on the page. You press to light it, the flame catches, the wax burns down, and the message appears at the bottom of the glass. A second button reveals another one, which is the beat that teaches the real point: the message is not ours, it is whatever you write. Blow it out and a wisp of smoke rises. That detail earns its keep, because it is the moment the object stops reading as a graphic and starts reading as a thing.</p>
    <p class="cs-section-body">From there the builder does the selling. Fragrance, message, occasion, sent. There is deliberately no checkout. Every candle is poured to order and confirmed personally, so a cart would promise a transaction the studio does not actually offer. Seven signature scents are presented as discs with their own photography: Exotic Dream, Amber Tale, Velvet Coffee, Summer Sun, Pure Silk, Sweet Escape, and Istanbul Tulip, with a request-your-own-blend path for anyone who wants something else.</p>

    <div class="schema-grid">
      <div class="schema-pill">
        <div class="k">Reveal</div>
        <div class="v">Light, burn, read</div>
        <div class="sub">Press to light, wax burns down, hidden message appears</div>
      </div>
      <div class="schema-pill">
        <div class="k">Second message</div>
        <div class="v">Teaches the point</div>
        <div class="sub">Reveal another, so the message reads as the buyer's, not ours</div>
      </div>
      <div class="schema-pill">
        <div class="k">Builder</div>
        <div class="v">No checkout by design</div>
        <div class="sub">Fragrance, message, occasion. Confirmed personally, not charged</div>
      </div>
      <div class="schema-pill">
        <div class="k">Fragrances</div>
        <div class="v">Seven signatures</div>
        <div class="sub">Each with its own disc photography and scent note</div>
      </div>
      <div class="schema-pill">
        <div class="k">Palette</div>
        <div class="v">Wine, gold, cream</div>
        <div class="sub">Cormorant Garamond display, Jost body, candle-glow accents</div>
      </div>
      <div class="schema-pill">
        <div class="k">Performance</div>
        <div class="v">98 / 100 / 100 / 100</div>
        <div class="sub">Lighthouse, after the hero video landed</div>
      </div>
    </div>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/lily-reveal.jpg" alt="The interactive candle after being lit, with the hidden message showing at the bottom of the glass" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 1.</strong> The reveal. Press to light, the wax burns down, the message shows. This is the entire product pitch, and it runs before the visitor has read a word about how it works.</figcaption>
    </figure>

    <p class="cs-section-body" style="margin-top:28px;">The art direction called for restraint more than it called for ideas. The brand handed over a full shoot: polished product work, a lifestyle set, a four-panel making-of, and a pile of casual kitchen and pouring footage. The casual material is genuinely charming and it stayed off the page. At this price point the handmade story has to be told by the polished four-panel journey and the hero video, because a phone snap of a saucepan reads as a hobby, not a studio. That was a call I made and defended, and it is the difference between the site supporting the price and quietly arguing against it.</p>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/lily-hero.jpg" alt="The Lily's Secret home page hero in deep wine and antique gold" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 2.</strong> Deep wine, antique gold, cream, and candle-glow. Cormorant Garamond for display, Jost for body, with gold held back so it reads as gilding rather than decoration.</figcaption>
    </figure>
  </div>

  <div class="cs-section">
    <div class="cs-section-label">02 &middot; Language and Orders</div>
    <h2 class="cs-section-title">Six Languages In, English Out</h2>
    <p class="cs-section-body">The customer base spans the UAE and the diaspora shopping into it, so the site ships in <strong>six languages</strong>: English, Arabic, Turkish, French, Russian, and Hindi. Arabic runs full right-to-left, which means the layout mirrors, not only the text. The choice persists in the visitor's browser, so nobody picks their language twice.</p>
    <p class="cs-section-body">The decision that makes the whole thing operable is on the other end. Orders always arrive at the studio <strong>in English</strong>, whatever language the visitor used. The owner should never open an order she cannot read, and no translation step should sit between a customer's message and the candle it goes into. A six-language storefront with a one-language inbox is what lets a single person run this without hiring.</p>
    <p class="cs-section-body">Both the contact chat and the order builder post straight to the studio inbox through Formspree, so the customer never opens their own mail client and never loses the thread to a half-written draft. Delivery is governed by one <code>FORM_ENDPOINT</code> constant. Set it to an empty string and the whole site falls back to a pre-filled email instead. One line, two modes, no branching code.</p>
    <p class="cs-section-body">Failure is handled out loud. If a send fails because the visitor is offline or the form is over quota, the chat says so and points at WhatsApp and Instagram. Nothing disappears silently, which matters more here than on most sites: the thing being submitted is a personal message someone just spent five minutes writing.</p>

    <div class="schema-grid">
      <div class="schema-pill">
        <div class="k">Languages</div>
        <div class="v">Six, one engine</div>
        <div class="sub">English, Arabic, Turkish, French, Russian, Hindi</div>
      </div>
      <div class="schema-pill">
        <div class="k">Arabic</div>
        <div class="v">Full RTL</div>
        <div class="sub">Layout mirrors, not just the text direction</div>
      </div>
      <div class="schema-pill">
        <div class="k">Orders</div>
        <div class="v">Always English</div>
        <div class="sub">Six languages in, one readable inbox out</div>
      </div>
      <div class="schema-pill">
        <div class="k">Delivery</div>
        <div class="v">One constant</div>
        <div class="sub">FORM_ENDPOINT governs Formspree or email fallback</div>
      </div>
      <div class="schema-pill">
        <div class="k">Failure path</div>
        <div class="v">Never silent</div>
        <div class="sub">Offline or over quota routes to WhatsApp and Instagram</div>
      </div>
      <div class="schema-pill">
        <div class="k">Schema</div>
        <div class="v">Product plus place</div>
        <div class="sub">LocalBusiness AE, Product, ItemList of 7, FAQPage</div>
      </div>
    </div>

    <div class="flow-card">
      <div class="flow-row">
        <div class="flow-step">01 &middot; Choose</div>
        <div class="flow-body">The globe menu switches the whole site between six languages. Arabic mirrors the layout. The choice is stored in the browser, so a returning visitor lands in their own language without asking.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">02 &middot; Build</div>
        <div class="flow-body">Fragrance, secret message, occasion. No payment step, because every candle is poured to order and priced in conversation. The builder collects what the studio needs to quote and nothing it does not.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">03 &middot; Send</div>
        <div class="flow-body">The submission posts to the studio inbox through Formspree and the chat shows a localized confirmation. If it fails, the visitor is handed WhatsApp and Instagram rather than a dead end.</div>
      </div>
      <div class="flow-row">
        <div class="flow-step">04 &middot; Receive</div>
        <div class="flow-body">The order lands in English no matter which language it was written in, at an ImprovMX alias that forwards to the studio. The public brand address stays stable even if the inbox behind it changes.</div>
      </div>
    </div>

    <figure class="cs-figure cs-figure--phone">
      <div class="cs-figure__frame">
        <img src="images/lily-rtl.jpg" alt="The site rendered in Arabic on a phone, with the layout mirrored right to left" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 3.</strong> Arabic on mobile. The navigation, the type, and the section rhythm all mirror. Getting this right meant the layout could not rely on left-anchored spacing anywhere.</figcaption>
    </figure>

    <p class="cs-section-body" style="margin-top:28px;">Discovery and trust were the last pieces. The home page carries <strong>Organization</strong> and <strong>LocalBusiness</strong> schema anchored to the UAE, a <strong>Product</strong> block with offers, an <strong>ItemList</strong> declaring all seven fragrances as individual products so each scent can surface on its own, and a <strong>FAQPage</strong> answering the questions a first-time buyer actually asks: what this is, how the secret works, where the candles are made, how to order, and what the scents are. Underneath that sit real terms, privacy, and returns pages with the registered entity and licence details, because a brand asking for a stranger's personal message and no payment up front has to look like a real company before it looks like a nice one.</p>

    <figure class="cs-figure">
      <div class="cs-figure__frame">
        <img src="images/lily-builder.jpg" alt="The Create Your Candle order builder with fragrance, message, and occasion inputs" loading="lazy">
      </div>
      <figcaption class="cs-figure__caption"><strong>Fig 4.</strong> The order builder. Fragrance, message, occasion, sent to the studio directly. The visitor never opens their own email client and never sees a checkout that would misrepresent how the studio works.</figcaption>
    </figure>
  </div>

  <div class="outro">
    <div class="cs-section-label">Outro</div>
    <p class="outro-body">The product is a surprise that only works once, and the site had to give that surprise away without spoiling it, in six languages, to a buyer who cannot pay online and has to trust a stranger with something personal. The candle does the explaining. The language and order systems make sure whoever gets convinced can actually place the order, and that the studio can read it when it arrives.</p>
    <a class="outro-cta" href="https://www.lilysecretcandles.com" target="_blank" rel="noopener">Visit the live site &nearr;</a>
  </div>

</div>
```

- [ ] **Step 5: Verify no em dashes and no banned phrases**

```bash
grep -n "—" case-study-lilys-secret.html; echo "em-dash exit=$? (1 = clean)"
grep -niE "delve|tapestry|ever-evolving|robust|leverage|seamlessly|navigate the landscape|crafted|curated|elevated|bespoke|thoughtful" case-study-lilys-secret.html; echo "phrase exit=$? (1 = clean)"
```

Expected: both report `exit=1`. Note the constraint from the spec: the brand uses "bespoke" for itself, but it must not appear in this page's prose. "Poured to order" is the phrasing used instead.

- [ ] **Step 6: Verify the JSON-LD parses**

```bash
node -e "const h=require('fs').readFileSync('case-study-lilys-secret.html','utf8');const m=h.match(/<script type=\"application\/ld\+json\">([\s\S]*?)<\/script>/);JSON.parse(m[1]);console.log('JSON-LD OK')"
```

Expected: `JSON-LD OK`.

- [ ] **Step 7: Verify no stale template strings survived the copy**

```bash
grep -niE "take.?me.?back|bingo|takemebackbingo|High Class Experience" case-study-lilys-secret.html; echo "exit=$? (1 = clean)"
```

Expected: `exit=1`.

- [ ] **Step 8: Verify every image path resolves**

```bash
grep -oE 'src="images/[^"]+"' case-study-lilys-secret.html | sed 's/src="//;s/"//' | while read p; do
  [ -s "$p" ] && echo "OK   $p" || echo "MISS $p"
done
```

Expected: four `OK` lines, no `MISS`.

- [ ] **Step 9: Open it and check the render**

Open `case-study-lilys-secret.html` in a browser. Confirm: gold accent on the italic title word, all four figures on deep wine frames, the phone-width figure centered, no console errors, and a clean one-column collapse below 820px.

- [ ] **Step 10: Commit**

```bash
git add case-study-lilys-secret.html
git commit -m "feat(case-study): add Lily's Secret case study"
```

---

## Task 4: Portfolio cards

**Files:**
- Modify: `Portfolio.html`, inserting after the Take Me Back Bingo card block that currently ends around line 1786, before the closing `</div>` of the work grid at line 1789.

**Interfaces:**
- Consumes: `images/jcs-logo.png` and `images/lily-card.jpg` from Task 1. Links to the routes created in Task 5.
- Produces: two clickable cards in the work grid.

- [ ] **Step 1: Locate the insertion point**

```bash
grep -n "05 Take Me Back Bingo" Portfolio.html
sed -n '1786,1792p' Portfolio.html
```

Expected: the Take Me Back Bingo card closes with `</div>`, then blank lines, then the `</div>` that closes `.projects-grid` and `</section>`. Insert the new markup immediately after the Take Me Back Bingo card's closing `</div>` and before the grid's closing `</div>`.

- [ ] **Step 2: Insert the two cards**

```html
          <!-- 06 The Jersey City Sound -->
          <div class="project-card flip">
            <div class="mockup"
              style="cursor:pointer;background:#0E0E10;border:1px solid rgba(201,162,39,0.22);display:flex;align-items:center;justify-content:center;padding:48px 36px;"
              onclick="window.location='/jersey-city-sound-case-study'">
              <img src="images/jcs-logo.png" alt="The Jersey City Sound wordmark"
                style="width:80%;max-width:340px;height:auto;object-fit:contain;transition:transform .3s ease;"
                onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
            </div>
            <div class="info">
              <h2>The Jersey City <em>Sound</em></h2>
              <div class="tags">Information architecture &nbsp;·&nbsp; Static generation &nbsp;·&nbsp; Schema &amp; AEO &nbsp;·&nbsp; Editorial standards</div>
              <p>Founder, designer, and engineer on a permanent encyclopedia-archive of Jersey City music culture. 247 entries live in one data file and a single Python generator writes the entire site: every entry page, the archive index, the Legends memorial wing, the sources bibliography, the search index, and the sitemap. Built as static HTML with no framework and no database, because the requirement is that it still loads in twenty years.</p>
              <button class="case-link" onclick="window.location='/jersey-city-sound-case-study'"
                style="all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent);border-bottom:1px solid transparent;transition:border-color .15s;margin-top:4px;">View
                Case Study &rarr;</button>
            </div>
          </div>

          <!-- 07 Lily's Secret -->
          <div class="project-card">
            <div class="mockup"
              style="cursor:pointer;background:#2B0710;border:1px solid rgba(201,162,75,0.22);padding:0;overflow:hidden;display:block;line-height:0;"
              onclick="window.location='/lilys-secret-case-study'">
              <img src="images/lily-card.jpg" alt="A Lily's Secret candle with the gold wax seal"
                style="width:100% !important;height:auto !important;min-height:unset !important;display:block;object-fit:cover;transition:transform .4s ease;"
                onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
            </div>
            <div class="info">
              <h2>Lily's <em>Secret</em></h2>
              <div class="tags">Brand site &nbsp;·&nbsp; Interactive demo &nbsp;·&nbsp; Six-language i18n &nbsp;·&nbsp; Arabic RTL</div>
              <p>Design and build for a UAE candle brand whose product hides a personal message under the wax, readable only once the candle has burned down. The site solves an invisible product with an interactive candle you can light on the page, ships in six languages with full Arabic right-to-left, and routes every order to the studio in English no matter which language the customer used.</p>
              <button class="case-link" onclick="window.location='/lilys-secret-case-study'"
                style="all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent);border-bottom:1px solid transparent;transition:border-color .15s;margin-top:4px;">View
                Case Study &rarr;</button>
            </div>
          </div>
```

- [ ] **Step 3: Verify the card count and that the grid still closes correctly**

```bash
grep -c "class=\"project-card" Portfolio.html
grep -n "01 \|02 \|03 \|04 \|05 \|06 \|07 " Portfolio.html | grep -iE "smart|jersey|julie|dmc|take me back|lily"
```

Expected: 7 project cards, and the comment list reads 01 through 07 in order.

- [ ] **Step 4: Verify no em dashes were introduced**

```bash
grep -n "—" Portfolio.html; echo "exit=$? (1 = clean)"
```

Expected: `exit=1`.

- [ ] **Step 5: Open the portfolio and check both cards**

Open `Portfolio.html`, go to the Work panel, scroll to the bottom of the grid. Confirm both new cards render, both images load, hover scales work, and the card layout matches its neighbours at desktop and at mobile width.

- [ ] **Step 6: Commit**

```bash
git add Portfolio.html
git commit -m "feat(portfolio): add Jersey City Sound and Lily's Secret work cards"
```

---

## Task 5: Routing, sitemap, and llms.txt

**Files:**
- Modify: `vercel.json`, the `rewrites` array
- Modify: `sitemap.xml`
- Modify: `llms.txt`

**Interfaces:**
- Consumes: the two HTML files from Tasks 2 and 3, and the card links from Task 4.
- Produces: working routes `/jersey-city-sound-case-study` and `/lilys-secret-case-study`.

- [ ] **Step 1: Add the two rewrites**

In `vercel.json`, append to the `rewrites` array after the Take Me Back Bingo entry:

```json
    { "source": "/jersey-city-sound-case-study", "destination": "/case-study-jersey-city-sound.html" },
    { "source": "/lilys-secret-case-study", "destination": "/case-study-lilys-secret.html" }
```

Make sure the preceding entry now ends with a comma and the array still closes correctly.

- [ ] **Step 2: Verify vercel.json is valid JSON**

```bash
node -e "const c=require('./vercel.json');console.log('rewrites:',c.rewrites.length);console.log(c.rewrites.slice(-2))"
```

Expected: `rewrites: 7` and the last two entries are the new ones.

- [ ] **Step 3: Add the two sitemap entries**

Read the existing `sitemap.xml` first and match its exact element order and indentation. Append two `<url>` blocks before `</urlset>`:

```xml
  <url>
    <loc>https://www.robertvanliew.com/jersey-city-sound-case-study</loc>
    <lastmod>2026-07-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.robertvanliew.com/lilys-secret-case-study</loc>
    <lastmod>2026-07-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
```

If the existing entries omit `changefreq` or use different priorities, match them instead of the values above. Consistency with the file wins over the values in this plan.

- [ ] **Step 4: Verify the sitemap is well-formed and has the right URL count**

```bash
node -e "
const s=require('fs').readFileSync('sitemap.xml','utf8');
const locs=[...s.matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1]);
console.log('urls:',locs.length);
locs.forEach(l=>console.log(' ',l));
const open=(s.match(/<url>/g)||[]).length, close=(s.match(/<\/url>/g)||[]).length;
if(open!==close) throw new Error('unbalanced url tags');
console.log('well-formed');
"
```

Expected: the two new URLs listed, `well-formed` printed.

- [ ] **Step 5: Add the two llms.txt lines**

Read `llms.txt` and match the exact format used by the existing five case study lines. Add one line per new case study in the same section, using the same separator and phrasing pattern. Do not invent a new format.

- [ ] **Step 6: Verify llms.txt mentions both and has no em dashes**

```bash
grep -n "jersey-city-sound-case-study\|lilys-secret-case-study" llms.txt
grep -n "—" llms.txt; echo "em-dash exit=$? (1 = clean)"
```

Expected: both routes found, `exit=1` on the em dash check.

- [ ] **Step 7: Commit**

```bash
git add vercel.json sitemap.xml llms.txt
git commit -m "feat(routing): add routes, sitemap, and llms entries for the two new case studies"
```

---

## Task 6: Verification sweep

**Files:**
- Create: `verify_case_studies.js`

**Interfaces:**
- Consumes: everything from Tasks 1 through 5.
- Produces: a repeatable check that fails loudly if any constraint is violated.

- [ ] **Step 1: Write the verification script**

Create `verify_case_studies.js`:

```js
// Verification sweep for the case study pages. Run: node verify_case_studies.js
const fs = require('fs');
const path = require('path');

const PAGES = [
  'case-study-jersey-city-sound.html',
  'case-study-lilys-secret.html',
];

const BANNED = [
  'delve', 'tapestry', 'ever-evolving', 'robust', 'leverage', 'seamlessly',
  'navigate the landscape', 'crafted', 'curated', 'elevated', 'bespoke',
  'thoughtful', 'elegantly', 'beautifully', 'in today\'s fast-paced',
];

const STALE = ['take me back', 'takemebackbingo', 'bingo', 'High Class Experience'];

let failures = 0;
const fail = m => { console.log('FAIL ' + m); failures++; };
const pass = m => console.log('ok   ' + m);

for (const page of PAGES) {
  if (!fs.existsSync(page)) { fail(page + ' does not exist'); continue; }
  const html = fs.readFileSync(page, 'utf8');

  if (html.includes('\u2014')) fail(page + ' contains an em dash');
  else pass(page + ' no em dashes');

  const hits = BANNED.filter(w => html.toLowerCase().includes(w.toLowerCase()));
  if (hits.length) fail(page + ' banned phrases: ' + hits.join(', '));
  else pass(page + ' no banned phrases');

  const stale = STALE.filter(w => html.toLowerCase().includes(w.toLowerCase()));
  if (stale.length) fail(page + ' stale template strings: ' + stale.join(', '));
  else pass(page + ' no stale template strings');

  const m = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  if (!m) fail(page + ' has no JSON-LD block');
  else {
    try { JSON.parse(m[1]); pass(page + ' JSON-LD parses'); }
    catch (e) { fail(page + ' JSON-LD invalid: ' + e.message); }
  }

  const slug = page.replace('case-study-', '').replace('.html', '');
  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/);
  if (!canonical) fail(page + ' has no canonical');
  else if (!canonical[1].startsWith('https://www.robertvanliew.com/')) fail(page + ' canonical wrong host: ' + canonical[1]);
  else pass(page + ' canonical ' + canonical[1]);

  const imgs = [...html.matchAll(/src="(images\/[^"]+)"/g)].map(x => x[1]);
  if (!imgs.length) fail(page + ' references no images');
  for (const img of imgs) {
    if (fs.existsSync(img) && fs.statSync(img).size > 1000) pass(page + ' image ' + img);
    else fail(page + ' missing or empty image ' + img);
  }
}

// routing
const vercel = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
for (const route of ['/jersey-city-sound-case-study', '/lilys-secret-case-study']) {
  const r = vercel.rewrites.find(x => x.source === route);
  if (!r) fail('vercel.json missing rewrite for ' + route);
  else if (!fs.existsSync(r.destination.replace(/^\//, ''))) fail('rewrite target missing: ' + r.destination);
  else pass('route ' + route + ' -> ' + r.destination);
}

// sitemap
const sm = fs.readFileSync('sitemap.xml', 'utf8');
for (const route of ['jersey-city-sound-case-study', 'lilys-secret-case-study']) {
  if (sm.includes(route)) pass('sitemap has ' + route);
  else fail('sitemap missing ' + route);
}
if ((sm.match(/<url>/g) || []).length !== (sm.match(/<\/url>/g) || []).length) fail('sitemap has unbalanced url tags');
else pass('sitemap well-formed');

// portfolio cards
const pf = fs.readFileSync('Portfolio.html', 'utf8');
for (const route of ['/jersey-city-sound-case-study', '/lilys-secret-case-study']) {
  if (pf.includes(route)) pass('Portfolio links ' + route);
  else fail('Portfolio missing link to ' + route);
}
if (pf.includes('\u2014')) fail('Portfolio.html contains an em dash');
else pass('Portfolio.html no em dashes');

console.log('');
console.log(failures ? failures + ' FAILURE(S)' : 'ALL CHECKS PASSED');
process.exit(failures ? 1 : 0);
```

- [ ] **Step 2: Run it and confirm it fails on nothing**

```bash
node verify_case_studies.js
```

Expected: `ALL CHECKS PASSED` and exit code 0. Fix any `FAIL` line in the file it names, then rerun.

- [ ] **Step 3: Confirm the script actually catches problems**

Temporarily introduce a fault and confirm the checker sees it:

```bash
cp case-study-lilys-secret.html /tmp/lily.bak
printf '\n<!-- \xe2\x80\x94 -->\n' >> case-study-lilys-secret.html
node verify_case_studies.js; echo "exit=$? (should be 1)"
cp /tmp/lily.bak case-study-lilys-secret.html
node verify_case_studies.js; echo "exit=$? (should be 0)"
```

Expected: exit 1 with an em dash failure, then exit 0 after the restore. A checker that never fails is not a checker.

- [ ] **Step 4: Manual pass on both pages at two widths**

Open both case studies and `Portfolio.html`. At 1440px and at 375px confirm: no horizontal scroll, figures fit their frames, the meta list stacks below the description on the narrow width, and no text runs under an image.

- [ ] **Step 5: Commit**

```bash
git add verify_case_studies.js
git commit -m "chore(case-study): add verification sweep for case study constraints"
```

---

## Self-Review

**Spec coverage.** Spec §3 template and accents: Task 2 Step 3, Task 3 Step 3. §4 JCS content: Task 2 Step 4. §5 Lily's content: Task 3 Step 4. §6 cards: Task 4. §7 routing, sitemap, llms: Task 5. §8 capture: Task 1. §9 writing rules: Global Constraints, enforced in Tasks 2, 3, 4, 6. §10 verification, all eight points: Task 2 Steps 5 to 9, Task 3 Steps 5 to 9, Task 5 Steps 2, 4, 6, and Task 6. No gaps.

**Placeholder scan.** Every step has literal content. The two places a judgement call remains are Task 5 Step 3 and Step 5, where the instruction is to match the existing file's format rather than impose a new one, with the fallback values given inline. That is a deliberate deference to the file, not a missing detail.

**Type consistency.** Image filenames are identical across Task 1 outputs, Task 2 and 3 `src` attributes, Task 4 card markup, and the Task 6 checker. Routes are identical across Task 4 links, Task 5 rewrites and sitemap, and the Task 6 checker. Accent hex values match the spec table. The 247 / 248 / 10 / 6 / 7 figures are used consistently and all trace to the Verified Facts Reference.

**Open item resolved.** The spec flagged the 247 versus 248 discrepancy as must-verify. It is resolved: 247 records in `entries.json`, plus the hand-authored `entry-dj-dx.html`, equals 248 entry pages. Both numbers appear in the copy and the difference is explained on the page rather than smoothed over.

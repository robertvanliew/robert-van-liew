# Design: Jersey City Sound and Lily's Secret case studies

**Date:** 2026-07-25
**Status:** Approved
**Scope:** Two new case study pages on robertvanliew.com, two new portfolio cards, routing, sitemap, llms.txt, and captured imagery.

---

## 1. Goal

Add two production case studies to the portfolio, matching the depth and visual system of
the existing five (Smart Deductions, Jersey Club Radio, Julie Schatz, DMC Canada, Take Me
Back Bingo). Both subject projects are live and shipped:

- **The Jersey City Sound** (jerseycitysound.com), a static encyclopedia-archive of Jersey
  City music culture. 247 entries, generated from a single JSON source of truth.
- **Lily's Secret** (lilysecretcandles.com), a UAE candle brand whose product hides a
  personal message in the wax. Six-language static site with an interactive reveal and an
  order builder.

Both are named and linked. Lily's Secret is credited as client work.

---

## 2. Files changed

| File | Change |
|---|---|
| `case-study-jersey-city-sound.html` | New. Cloned from `case-study-take-me-back-bingo.html`. |
| `case-study-lilys-secret.html` | New. Same template. |
| `Portfolio.html` | Two new `.project-card` blocks appended to the work grid after Take Me Back Bingo (cards 06 and 07). |
| `vercel.json` | Two rewrites added. |
| `sitemap.xml` | Two `<url>` entries added. |
| `llms.txt` | Two case study lines added. |
| `capture_case_studies.js` | New. Puppeteer capture script, committed so shots can be retaken. |
| `images/jcs-*.png`, `images/lily-*.jpg` | New captured and sourced imagery. |

No existing case study page is modified. No shared stylesheet is modified: each case study
page carries its own inline `<style>` block, which is the established pattern in this repo.

---

## 3. Template and visual system

Both pages are built from `case-study-take-me-back-bingo.html`, which is the current
best-formed template. Preserved verbatim:

- The `nav` bar with back link, breadcrumb, and right-hand tag.
- `.page` wrapper at `max-width: 1100px`.
- `.project-eyebrow`, `h1.title` with italic accent `em`, `.project-tags`.
- `.cs-intro` two-column grid (description plus `.cs-meta-list` with Role, Client, Stack,
  Live, Scope).
- `.cs-section` blocks with `.cs-section-label`, `.cs-section-title`, `.cs-section-body`.
- `.schema-grid` of `.schema-pill` cards for at-a-glance system inventories.
- `.flow-card` with `.flow-row` steps for sequential flows.
- `.cs-figure` with `.cs-figure__frame` and `.cs-figure__caption`, plus the
  `.cs-figure--phone` modifier for mobile shots.
- `.outro` with `.outro-cta`.
- The single `@media (max-width: 820px)` block.

**Only the two accent tokens change per project.** The chrome, ink, paper, and edge tokens
stay identical across all case studies so the set reads as one site.

| Page | `--accent` | `--accent-warm` | Figure frame background |
|---|---|---|---|
| Jersey City Sound | `#9C7A14` (gold-deep, readable on paper) | `#C9A227` (brand gold) | `#0E0E10` (JCS night) |
| Lily's Secret | brand gold sampled from `css/styles.css` `:root` | brand rose/wax secondary | deep wax tone from the same `:root` |

Lily's exact hex values are read from the live project's `css/styles.css` at build time
rather than guessed.

---

## 4. Content: The Jersey City Sound

**Route:** `/jersey-city-sound-case-study`
**Title:** The Jersey City *Sound*
**Nav tag:** Archive · 2026
**Tags:** Information Architecture, Static Generation, Editorial Standards, Schema & AEO, End-to-End

**Meta block**

- Role: Founder, Designer, and Engineer
- Client: Frankpella LLC
- Stack: Static HTML, CSS, Python generator, GitHub Actions, GitHub Pages
- Live: jerseycitysound.com
- Scope: Brand system, information architecture, entry template, generator, search, schema, memorial wing

**Intro paragraph.** The archive exists because Jersey City's music history has never been
written down in one place. The site documents the DJs, artists, producers, venues, crews,
and labels that built the scene, with a citation on every claim. It has to survive decades,
so it is pure static HTML with no framework, no bundler, and no database. The case study
covers the two decisions that carry the project: an information architecture where 247
entries live in one data file and the entire site is generated from it, and a discovery
layer built so that both search engines and language models cite the archive by name.

### Section 01 · Information Architecture
*"247 Entries, One Source of Truth"*

Points to make, all verified against the project:

- `data/entries.json` holds every entry with its facts, sources, cross-links, galleries,
  and media. 247 entries at time of writing.
- `execution/generate_entry_pages.py` reads that file and writes every entry page plus the
  archive index, the Legends wing, the Sources page, sitemap, robots.txt, and llms.txt. It
  also removes orphaned pages for entries deleted or renamed.
- Entry count must be verified at implementation time before it is written into the page.
  A `"slug"` grep of `entries.json` returns 247 and `design/` holds 248 `entry-*.html`
  files. The one-file gap is resolved before any number ships, and the page states the
  verified count only.
- One page, `design/entry-dj-dx.html`, is hand-authored and deliberately left untouched by
  the generator. That exception is the proof the template is right: the handcrafted page and
  the generated pages are indistinguishable.
- The editorial standard is cite-or-cut. Nothing enters the archive without a source. This
  is a design constraint as much as an editorial one, because it forces a numbered sources
  block into the entry template rather than leaving citations optional.
- Entry anatomy: breadcrumb, entry number in letterspaced caps, name in display serif, a
  Record Card infobox with portrait and years active and roles and official links, a lead
  paragraph written to be quotable on its own, then Career, Notable Works, Credits and
  Receipts, In the Community, Gallery, Sources, claim bar, related entries.
- Dual theme. Archival paper by default. The Legends memorial wing inverts to night and
  gold. Same logo, same type, same grid, so the memorial wing reads as a different room in
  the same building rather than a second brand.
- Deployment is a GitHub Actions workflow publishing the `design/` folder to Pages on every
  push to main.

**Schema grid (6 pills):** Source of truth, Generator, Entry template, Legends wing, Search
index, Deployment.

**Figures:** archive index (desktop), an entry page showing the Record Card and the numbered
sources block (desktop), the Legends wing in night theme (desktop), an entry page on mobile.

### Section 02 · Discovery
*"Built to Be Cited"*

- Per-entry `Person` or `MusicGroup` schema with `sameAs` links out to official sites,
  streaming, and Wikidata, plus `BreadcrumbList` on every page.
- `Organization` with `areaServed` set to Jersey City, plus `WebSite` sitewide, and
  `FAQPage` on the pillar and history pages.
- The lead paragraph on every entry is written as a self-contained 40 to 60 word definition,
  because that is the passage a language model extracts and quotes.
- Receipts as numbers rather than adjectives. Years active, residencies with date ranges,
  stream counts. Countable claims with sources attached.
- `archive-data.js` is a generated client-side search index, so search works with no server
  and no query cost.
- `llms.txt` at the root, and robots.txt that explicitly allows GPTBot, ClaudeBot,
  PerplexityBot, and Google-Extended.
- The long-tail thesis: 247 documented names are 247 queries with almost no competition.
  Each one that ranks feeds authority back to the head terms like "jersey city djs."

**Flow card (4 steps):** Data, Generate, Publish, Get cited.

### Outro
The archive is a monument, not a media site. Static HTML with no dependencies means it still
loads in twenty years. The generator means a correction from a family member becomes a live
page edit in one commit. The schema means that when someone asks an AI who the first Jersey
City DJs were, the answer comes from the people who were actually there.

---

## 5. Content: Lily's Secret

**Route:** `/lilys-secret-case-study`
**Title:** Lily's *Secret*
**Nav tag:** Brand · 2026
**Tags:** Brand Site, Interactive Product Demo, Six-Language i18n, RTL, Order Systems

**Meta block**

- Role: Designer & Engineer
- Client: Lily's Secret, United Arab Emirates
- Stack: HTML, CSS, Vanilla JS, Formspree, WhatsApp, ImprovMX
- Live: lilysecretcandles.com
- Scope: Site design, interactive reveal, order builder, six-language i18n with RTL, schema, legal pages

**Intro paragraph.** Lily's Secret makes candles with a personal message hidden at the
bottom of the glass, revealed only when the flame has burned all the way down. The brief was
a site that could sell a product nobody has seen before, to customers across six language
groups, with no online payment because every candle is made to order. The case study covers
the interaction that explains the product without a word of copy, and the language and order
systems underneath it.

### Section 01 · The Product Is the Interaction
*"You Have to Burn It to Read It"*

- The core problem: the product's value is invisible in a photograph. A candle looks like a
  candle. The message is under the wax.
- The answer is an interactive candle on the page. Press to light, the flame animates, the
  wax burns down, and the hidden message appears at the bottom of the glass. A second button
  reveals another message so the visitor understands the message is theirs to write.
- A rising smoke wisp fires when the candle is blown out. Small detail, but it closes the
  loop and makes the object feel real.
- The Create Your Candle builder is the conversion path: fragrance, message, occasion. No
  payment is taken, by design, because every order is confirmed personally.
- Seven signature fragrances presented as discs, each with its own photography.
- Restraint call: the folder holds casual kitchen and pouring footage. Only the polished
  photography went on the page. The hero video and the four-panel journey carry the handmade
  story without undercutting the price point.
- Hero video plus poster frames, and a Lighthouse pass at 98/100/100/100 after adding them.

**Schema grid (6 pills):** Interactive reveal, Order builder, Fragrance system, Hero video,
Performance, Photography direction.

**Figures:** hero (desktop), the candle mid-reveal with the message showing (desktop or
phone), the Create Your Candle builder (desktop), English and Arabic side by side (two phone
frames or one split figure).

### Section 02 · Six Languages, One Studio Inbox
*"Six Languages In, English Out"*

- `js/i18n.js` carries English, Arabic, Turkish, French, Russian, and Hindi. Arabic runs
  full right-to-left, which means the layout mirrors, not just the text.
- The visitor's choice persists in their browser.
- Orders always arrive at the studio in English regardless of the language the visitor used.
  The owner should never have to translate an incoming order. This is the decision that
  makes the multilingual site actually operable by one person.
- Both the contact chat and the order builder post straight to the studio inbox through
  Formspree. The customer never opens their own mail client. A localized confirmation shows
  in the chat.
- Failure is handled out loud. If a submission fails from being offline or over quota, the
  chat shows an error and points to WhatsApp and Instagram. Nothing is lost silently.
- A single `FORM_ENDPOINT` constant near the top of the submit section governs delivery.
  Setting it to an empty string falls back to a pre-filled email. One line, two modes.
- The public address is an ImprovMX alias forwarding to the studio inbox, so the brand email
  is stable even if the underlying inbox changes.
- Schema: `Organization` and `LocalBusiness` with `addressCountry` AE and `areaServed` UAE,
  `Product` with offers, an `ItemList` of all seven fragrances as individual products, and a
  `FAQPage` answering what the product is and how the secret works.
- Real UAE legal pages with the registered entity and licence details: terms, privacy,
  returns.

**Flow card (4 steps):** Choose language, Build the candle, Send, Receive in English.

### Outro
The product is a surprise that only works once. The site had to give that surprise away
without spoiling it, in six languages, to a buyer who cannot pay online and has to trust a
stranger with a personal message. The interactive candle does the explaining. The language
and order systems make sure that whoever is convinced can actually place the order, and that
the studio can read it.

---

## 6. Portfolio cards

Two new `.project-card` blocks appended after the Take Me Back Bingo card in the work grid,
using the existing markup and inline style conventions.

**Card 06, Jersey City Sound.** Logo treatment, following the Jersey Club Radio and Take Me
Back Bingo pattern. `design/assets/jerseycitysound-reversed.png` centered on the JCS night
background `#0E0E10` with a gold hairline border, scale-on-hover. Heading "Jersey City
*Sound*". Tags: Information architecture · Static generation · Schema & AEO · Editorial
standards.

**Card 07, Lily's Secret.** Photographic treatment, following the DMC Canada pattern.
`assets/images/hero-candle-seal.jpeg` full-bleed in the mockup frame. Heading "Lily's
*Secret*". Tags: Brand site · Interactive demo · Six-language i18n · RTL.

Both cards get a one-paragraph description and the standard `.case-link` button.

---

## 7. Routing, sitemap, llms.txt

`vercel.json` rewrites, appended to the existing array:

```json
{ "source": "/jersey-city-sound-case-study", "destination": "/case-study-jersey-city-sound.html" },
{ "source": "/lilys-secret-case-study", "destination": "/case-study-lilys-secret.html" }
```

`sitemap.xml` gets two `<url>` entries matching the format of the existing case study
entries, with `lastmod` 2026-07-25.

`llms.txt` gets one line per case study in the same format as the existing five.

---

## 8. Image capture

New file `capture_case_studies.js`, using the puppeteer already in `package.json`
devDependencies. Committed rather than run once and discarded, so shots can be retaken when
either site changes.

- Desktop viewport 1440x900, `deviceScaleFactor: 2`.
- Mobile viewport 390x844, `deviceScaleFactor: 3`, `isMobile: true`.
- Waits for network idle and for fonts to load before shooting.
- For Lily's candle reveal, clicks `#lightBtn`, waits for the reveal animation, then shoots.
- For Arabic, sets the language through the language menu and waits for the RTL layout to
  settle.
- Writes PNG for the JCS shots (type and hairlines) and JPEG at quality 85 for the Lily's
  shots (photography).

Targets:

| Output | Source |
|---|---|
| `images/jcs-archive.png` | jerseycitysound.com/archive.html, desktop |
| `images/jcs-entry.png` | a representative entry page, desktop |
| `images/jcs-legends.png` | the Legends wing, desktop |
| `images/jcs-entry-mobile.png` | the same entry page, mobile |
| `images/jcs-logo.png` | copied from `design/assets/jerseycitysound-reversed.png` |
| `images/lily-hero.jpg` | lilysecretcandles.com, desktop |
| `images/lily-reveal.jpg` | the candle after `#lightBtn`, desktop |
| `images/lily-builder.jpg` | the Create Your Candle section, desktop |
| `images/lily-rtl.jpg` | Arabic layout, mobile |
| `images/lily-card.jpg` | copied from `assets/images/hero-candle-seal.jpeg` |

If a live page fails to capture, the fallback is the corresponding asset already in the
project folder, and the figure caption is adjusted so it never claims to be a screenshot of
something it is not.

---

## 9. Writing rules

Binding for every string that ships, including body copy, meta descriptions, OG
descriptions, JSON-LD descriptions, alt text, and figure captions:

- No em dashes anywhere. Use periods, commas, colons, or semicolons. Restructure the
  sentence rather than reaching for a dash.
- No AI-tell vocabulary: delve, tapestry, ever-evolving, robust, leverage, seamlessly,
  navigate the landscape, crafted, curated, elevated, bespoke, thoughtful.
- No "it's not just X, it's Y" constructions and no faux-profound openers.
- Note: the Lily's Secret brand copy uses "bespoke" for itself. The case study says "made to
  order" or "hand-poured to order" in Robert's own prose, and only quotes the brand's word if
  quoting the brand directly.
- No mention of AI tooling in any narrative prose. Claude and Gemini stay in the Tools list
  on the portfolio, nowhere else.
- Specific concrete nouns and countable claims. 247 entries, six languages, 98/100/100/100.

---

## 10. Verification

1. Every claim in both case studies is traceable to a file, a commit, or the live site.
   Nothing invented, no rounded-up numbers.
2. Both pages open locally with no console errors and no broken image paths.
3. Both JSON-LD blocks parse as valid JSON and validate as schema.org.
4. The 820px breakpoint collapses `.cs-intro`, `.schema-grid`, and `.flow-row` correctly on
   both pages.
5. Both new routes resolve, and both new portfolio cards navigate to them.
6. `sitemap.xml` remains well-formed XML.
7. A grep across both new files finds zero em dashes and zero banned phrases.
8. Canonical, OG, and Twitter URLs on each page point at the new route, not a copied TMB URL.

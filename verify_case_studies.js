// Verification sweep for the case study pages. Run: node verify_case_studies.js
// Fails loudly on em dashes, AI-tell vocabulary, stale template strings, invalid
// JSON-LD, wrong canonicals, missing images, or broken routing.

const fs = require('fs');

const PAGES = [
  'case-study-jersey-city-sound.html',
  'case-study-lilys-secret.html',
];

const ROUTES = [
  '/jersey-city-sound-case-study',
  '/lilys-secret-case-study',
];

const BANNED = [
  'delve', 'tapestry', 'ever-evolving', 'robust', 'leverage', 'seamlessly',
  'navigate the landscape', 'crafted', 'curated', 'elevated', 'bespoke',
  'thoughtful', 'elegantly', 'beautifully', "in today's fast-paced",
];

// Strings that mean a template copy was left half-edited.
const STALE = ['take me back', 'takemebackbingo', 'bingo', 'high class experience'];

let failures = 0;
const fail = m => { console.log('FAIL ' + m); failures++; };
const pass = m => console.log('ok   ' + m);

for (const page of PAGES) {
  if (!fs.existsSync(page)) { fail(page + ' does not exist'); continue; }
  const html = fs.readFileSync(page, 'utf8');

  if (html.includes('—')) fail(page + ' contains an em dash');
  else pass(page + ' no em dashes');

  const hits = BANNED.filter(w => html.toLowerCase().includes(w.toLowerCase()));
  if (hits.length) fail(page + ' banned phrases: ' + hits.join(', '));
  else pass(page + ' no banned phrases');

  const stale = STALE.filter(w => html.toLowerCase().includes(w));
  if (stale.length) fail(page + ' stale template strings: ' + stale.join(', '));
  else pass(page + ' no stale template strings');

  const m = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  if (!m) fail(page + ' has no JSON-LD block');
  else {
    try { JSON.parse(m[1]); pass(page + ' JSON-LD parses'); }
    catch (e) { fail(page + ' JSON-LD invalid: ' + e.message); }
  }

  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/);
  if (!canonical) fail(page + ' has no canonical');
  else if (!canonical[1].startsWith('https://www.robertvanliew.com/')) fail(page + ' canonical wrong host: ' + canonical[1]);
  else pass(page + ' canonical ' + canonical[1]);

  // Canonical, og:url and twitter:url must all agree, or a copied template
  // silently points social traffic at the wrong case study.
  const og = html.match(/<meta property="og:url" content="([^"]+)"/);
  const tw = html.match(/<meta name="twitter:url" content="([^"]+)"/);
  if (canonical && og && tw) {
    if (og[1] === canonical[1] && tw[1] === canonical[1]) pass(page + ' canonical, og:url, twitter:url agree');
    else fail(page + ' url mismatch: canonical=' + canonical[1] + ' og=' + og[1] + ' twitter=' + tw[1]);
  } else fail(page + ' missing og:url or twitter:url');

  const imgs = [...html.matchAll(/src="(images\/[^"]+)"/g)].map(x => x[1]);
  if (!imgs.length) fail(page + ' references no images');
  for (const img of imgs) {
    if (fs.existsSync(img) && fs.statSync(img).size > 1000) pass(page + ' image ' + img);
    else fail(page + ' missing or empty image ' + img);
  }
}

// routing
const vercel = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
for (const route of ROUTES) {
  const r = vercel.rewrites.find(x => x.source === route);
  if (!r) fail('vercel.json missing rewrite for ' + route);
  else if (!fs.existsSync(r.destination.replace(/^\//, ''))) fail('rewrite target missing: ' + r.destination);
  else pass('route ' + route + ' -> ' + r.destination);
}

// sitemap
const sm = fs.readFileSync('sitemap.xml', 'utf8');
for (const route of ROUTES) {
  if (sm.includes(route)) pass('sitemap has ' + route);
  else fail('sitemap missing ' + route);
}
if ((sm.match(/<url>/g) || []).length !== (sm.match(/<\/url>/g) || []).length) fail('sitemap has unbalanced url tags');
else pass('sitemap well-formed');

// llms.txt
const llms = fs.readFileSync('llms.txt', 'utf8');
for (const route of ROUTES) {
  if (llms.includes(route)) pass('llms.txt has ' + route);
  else fail('llms.txt missing ' + route);
}

// portfolio cards
const pf = fs.readFileSync('Portfolio.html', 'utf8');
for (const route of ROUTES) {
  if (pf.includes(route)) pass('Portfolio links ' + route);
  else fail('Portfolio missing link to ' + route);
}
if (pf.includes('—')) fail('Portfolio.html contains an em dash');
else pass('Portfolio.html no em dashes');

for (const img of ['images/jcs-logo.png', 'images/lily-card.jpg']) {
  if (pf.includes(img) && fs.existsSync(img)) pass('Portfolio card image ' + img);
  else fail('Portfolio card image missing: ' + img);
}

console.log('');
console.log(failures ? failures + ' FAILURE(S)' : 'ALL CHECKS PASSED');
process.exit(failures ? 1 : 0);

// Tells IndexNow engines (Bing, Yandex, Seznam, Naver, and partners) that the
// site changed, so they recrawl now instead of whenever they next visit.
// Google does not use IndexNow; it reads sitemap.xml via Search Console.
//
// Usage: node indexnow.js                 submit every URL in sitemap.xml
//        node indexnow.js /resume /work   submit only these paths
//
// The key must stay in sync with the key file served at the site root.

const fs = require('fs');
const path = require('path');

const HOST = 'www.robertvanliew.com';
const KEY = '2279b5c4fdb18f2b86e587e2095f4563';

function urlsFromSitemap() {
  const xml = fs.readFileSync(path.join(__dirname, 'sitemap.xml'), 'utf8');
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim());
}

(async () => {
  const args = process.argv.slice(2);
  const urlList = args.length
    ? args.map(p => `https://${HOST}${p.startsWith('/') ? p : '/' + p}`)
    : urlsFromSitemap();

  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList }),
  });

  // 200 = accepted, 202 = accepted and key check pending. Anything else is a failure.
  console.log(`IndexNow ${res.status} for ${urlList.length} URLs`);
  if (res.status !== 200 && res.status !== 202) {
    console.error(await res.text());
    process.exit(1);
  }
})();

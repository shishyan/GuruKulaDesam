import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    print("Navigating to https://studio.youtube.com/artist/a_Ut4CMfM98eM/releases ...")
    page.goto('https://studio.youtube.com/artist/a_Ut4CMfM98eM/releases')
    time.sleep(6)

    # Let's take a screenshot and inspect text
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\artist_releases_page.png')

    res = page.evaluate('''() => {
        // Collect all release titles, links, and table data
        const items = [];
        document.querySelectorAll('ytcp-release-row, tr, [id="row-container"], ytcp-entity-table-row, [role="row"]').forEach(r => {
            const titleEl = r.querySelector('#title, .title, a, [id*="title"]');
            if (titleEl && titleEl.innerText.trim()) {
                items.push({
                    title: titleEl.innerText.trim(),
                    href: titleEl.href || '',
                    fullText: (r.innerText || '').replace(/\\s+/g, ' ').trim()
                });
            }
        });
        
        // Also look for any links to playlists or albums
        const allLinks = Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim(),
            href: a.href
        })).filter(x => x.text && (x.href.includes('playlist') || x.href.includes('album') || x.href.includes('release') || x.href.includes('video')));

        return {
            title: document.title,
            bodyText: (document.body.innerText || '').slice(0, 2000),
            itemsCount: items.length,
            items: items.slice(0, 50),
            linksCount: allLinks.length,
            links: allLinks.slice(0, 50)
        };
    }''')

    print("Page Title:", res.get('title'))
    print("Items Count:", res.get('itemsCount'))
    print("Links Count:", res.get('linksCount'))
    print("\nBody Snippet:\n", res.get('bodyText')[:600])

    print("\nItems:")
    for it in res.get('items', []):
        print(f"  {it['title']} | {it.get('href')} | {it.get('fullText')[:80]}")

    print("\nLinks:")
    for l in res.get('links', []):
        print(f"  {l['text']} -> {l['href']}")

    # Save full json output
    with open('production/artist_releases_dump.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)

    page.close()

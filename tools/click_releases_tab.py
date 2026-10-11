import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    print("Navigating to Content Playlists first...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
    time.sleep(5)

    print("Clicking Releases tab...")
    page.evaluate('''() => {
        const tab = document.querySelector('#artist-releases-tab');
        if (tab) {
            tab.click();
        } else {
            Array.from(document.querySelectorAll('tp-yt-paper-tab')).find(t => t.innerText.trim() === 'Releases').click();
        }
    }''')
    time.sleep(8)
    print("Current URL:", page.url)

    # Take screenshot
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\studio_releases_clicked.png')

    data = page.evaluate('''() => {
        const rows = [];
        document.querySelectorAll('ytcp-release-row, tr, [id="row-container"], ytcp-entity-table-row, [role="row"]').forEach(r => {
            const titleEl = r.querySelector('#title, .title, a, [id*="title"]');
            if (titleEl && titleEl.innerText && titleEl.innerText.trim()) {
                rows.push({
                    title: titleEl.innerText.trim(),
                    href: titleEl.href || '',
                    fullText: (r.innerText || '').replace(/\\s+/g, ' ').trim()
                });
            }
        });

        const links = Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim(),
            href: a.href
        })).filter(x => x.text && (x.href.includes('playlist') || x.href.includes('album') || x.href.includes('release') || x.href.includes('artist') || x.href.includes('music')));

        return {
            title: document.title,
            bodySnippet: (document.body.innerText || '').slice(0, 1500),
            rowsCount: rows.length,
            rows: rows,
            linksCount: links.length,
            links: links
        };
    }''')

    print("Rows Count:", data.get('rowsCount'))
    print("Body snippet:\n", data.get('bodySnippet')[:500])
    print("Sample Rows:")
    for r in data.get('rows', [])[:20]:
        print("  ", r['title'], "-->", r.get('fullText')[:100])

    print("Links:")
    for l in data.get('links', [])[:20]:
        print("  ", l['text'], "-->", l.get('href'))

    with open('production/releases_tab_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    page.close()

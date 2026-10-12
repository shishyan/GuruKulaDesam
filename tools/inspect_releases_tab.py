import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    # Try both releases URLs
    urls_to_try = [
        'https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/releases',
        'https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/releases'
    ]

    for u in urls_to_try:
        print(f"\nNavigating to {u} ...")
        page.goto(u)
        time.sleep(5)
        print("Current URL:", page.url)

        res = page.evaluate('''() => {
            const rows = [];
            // Query table rows or release cards
            document.querySelectorAll('ytcp-release-row, tr, [id="row-container"], ytcp-entity-table-row').forEach(r => {
                const t = r.querySelector('#title, .title, a');
                if (t && t.innerText.trim()) {
                    rows.push({
                        title: t.innerText.trim(),
                        href: t.href || '',
                        text: r.innerText.replace(/\\n+/g, ' | ').trim()
                    });
                }
            });
            const links = Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href })).filter(x => x.text && (x.href.includes('release') || x.href.includes('album') || x.href.includes('playlist') || x.href.includes('edit')));
            return {
                title: document.title,
                bodySnippet: document.body.innerText.slice(0, 1000),
                rows: rows.slice(0, 20),
                totalRows: rows.length,
                links: links.slice(0, 20)
            };
        }''')
        print("Page title:", res.get('title'))
        print("Snippet:", repr(res.get('bodySnippet', '')[:300]))
        print("Total rows:", res.get('totalRows'))
        for r in res.get('rows', []):
            print("  Row:", r['title'], "-->", r.get('text')[:100])
        if res.get('totalRows', 0) > 0:
            break

    page.close()

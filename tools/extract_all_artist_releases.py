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
        if (tab) tab.click();
    }''')
    time.sleep(6)

    # Check pagination elements: "Rows per page", total count, next button
    pagination_info = page.evaluate('''() => {
        const pag = document.querySelector('ytcp-table-footer, ytcp-entity-table-footer, [id*="footer"], [class*="footer"]');
        return {
            text: pag ? pag.innerText.replace(/\\n+/g, ' ').trim() : 'no footer',
            nextBtn: !!document.querySelector('#navigate-after, [aria-label="Next page"], [id*="next"]')
        };
    }''')
    print("Pagination info:", pagination_info)

    all_releases = []
    page_num = 1

    while True:
        print(f"\n--- Extracting Page {page_num} ---")
        time.sleep(3)
        rows_data = page.evaluate('''() => {
            const rows = [];
            // Query each row
            document.querySelectorAll('ytcp-release-row, tr, [id="row-container"], ytcp-entity-table-row, [role="row"]').forEach(r => {
                const titleEl = r.querySelector('#title, .title, a, [id*="title"]');
                if (titleEl && titleEl.innerText && titleEl.innerText.trim()) {
                    const text = titleEl.innerText.trim();
                    const href = titleEl.href || (r.querySelector('a') ? r.querySelector('a').href : '');
                    // Parse metadata columns if any
                    rows.push({
                        title: text,
                        href: href,
                        rowText: (r.innerText || '').replace(/\\n+/g, ' | ').trim()
                    });
                }
            });
            return rows;
        }''')

        print(f"Found {len(rows_data)} rows on page {page_num}")
        for r in rows_data:
            all_releases.append(r)
            print(f"  {r['title']} | {r['rowText']}")

        # Check if next button is enabled
        next_status = page.evaluate('''() => {
            const nextBtn = document.querySelector('#navigate-after:not([disabled]), [aria-label="Next page"]:not([disabled])');
            if (nextBtn && nextBtn.getAttribute('aria-disabled') !== 'true') {
                nextBtn.click();
                return { clicked: true };
            }
            return { clicked: false };
        }''')

        if not next_status.get('clicked'):
            print("No more pages or next button disabled.")
            break

        page_num += 1
        time.sleep(4)

    print(f"\nTotal Releases Extracted: {len(all_releases)}")

    # Save to production/all_artist_releases.json
    with open('production/all_artist_releases.json', 'w', encoding='utf-8') as f:
        json.dump(all_releases, f, indent=2, ensure_ascii=False)

    page.close()

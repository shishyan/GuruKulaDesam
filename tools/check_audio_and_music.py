import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    def safe_eval(expr):
        try:
            return page.evaluate(expr)
        except Exception as e:
            return str(e)

    # 1. Check Studio Podcasts tab
    print("Checking Podcasts tab...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/podcasts')
    time.sleep(5)
    podcasts = safe_eval('''() => {
        return {
            text: document.body.innerText.slice(0, 800),
            links: Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href })).filter(x => x.text)
        }
    }''')
    print("Podcasts page:")
    print("Text:", repr(podcasts.get('text', '')[:300]))
    print("Links:", podcasts.get('links'))

    # 2. Check YouTube Music channel page
    print("\nChecking YouTube Music...")
    page.goto('https://music.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q')
    time.sleep(5)
    ymusic = safe_eval('''() => {
        const sections = [];
        document.querySelectorAll('ytmusic-carousel-shelf-renderer, ytmusic-shelf-renderer').forEach(s => {
            const h = s.querySelector('h2');
            const items = Array.from(s.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href })).filter(x => x.text);
            sections.push({
                heading: h ? h.innerText.trim() : 'Unknown',
                items: items.slice(0, 10)
            });
        });
        return {
            title: document.title,
            sections: sections,
            body: document.body.innerText.slice(0, 800)
        };
    }''')
    print("Music.youtube.com info:")
    print("Title:", ymusic.get('title'))
    print("Sections:", ymusic.get('sections'))

    # 3. Check YouTube Studio Videos tab filtered by "Thirukkural" or "திருக்குறள்"
    print("\nChecking Studio Videos with search 'திருக்குறள்'...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/videos/upload?filter=%5B%7B%22name%22%3A%22SEARCH%22%2C%22value%22%3A%22%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AF%81%E0%AE%95%E0%AF%8D%E0%AE%95%E0%AF%81%E0%AE%B1%E0%AE%B3%E0%AF%8D%22%7D%5D')
    time.sleep(6)
    video_search = safe_eval('''() => {
        const totalCountEl = document.querySelector('.page-description, #total-count, span[class*="total-count"]');
        const rows = [];
        document.querySelectorAll('ytcp-video-row, tr[id*="row"]').forEach(r => {
            const t = r.querySelector('#video-title, #title');
            if (t) rows.push(t.innerText.trim());
        });
        return {
            total: totalCountEl ? totalCountEl.innerText.trim() : 'unknown',
            rowsCount: rows.length,
            sampleRows: rows.slice(0, 10),
            body: document.body.innerText.slice(0, 500)
        };
    }''')
    print("Studio Videos filtered by Thirukkural:")
    print(video_search)

    page.close()

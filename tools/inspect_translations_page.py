import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    url = "https://studio.youtube.com/video/IHMZsM7LJf8/translations"
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='networkidle')
    time.sleep(4)
    
    screenshot_path = "scratch/translations_page_IHMZsM7LJf8.png"
    page.screenshot(path=screenshot_path)
    print(f"Saved screenshot to {screenshot_path}")
    
    # Inspect rows and buttons
    rows = page.evaluate("""() => {
        const rows = document.querySelectorAll('ytcp-video-translations-row, ytcp-table-row, [role="row"]');
        return Array.from(rows).map(r => ({
            text: r.innerText.replace(/\\s+/g, ' ').trim(),
            buttons: Array.from(r.querySelectorAll('button, ytcp-button, [role="button"]')).map(b => b.innerText.trim() || b.getAttribute('aria-label') || b.id)
        }));
    }""")
    print(f"Found {len(rows)} table rows:")
    for i, r in enumerate(rows):
        print(f"Row {i}: {r['text'][:100]}")
        print(f"   Buttons: {r['buttons']}")

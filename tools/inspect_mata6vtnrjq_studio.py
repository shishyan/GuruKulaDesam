import time, sys, pathlib, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
target_url = f"https://studio.youtube.com/video/{vid}/translations"

print("Connecting to Chrome port 9225...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    context = browser.contexts[0]
    page = context.pages[0] if context.pages else context.new_page()
    
    print(f"Current page URL: {page.url}", flush=True)
    if not page.url.startswith(target_url):
        print(f"Navigating to {target_url}...", flush=True)
        page.goto(target_url, timeout=30000)
    
    print("Waiting 5s for Studio DOM...", flush=True)
    time.sleep(5)
    
    print(f"Page title: {page.title()}", flush=True)
    screenshot_path = "scratch/studio_subtitles_Mata6vtnrjQ.png"
    page.screenshot(path=screenshot_path)
    print(f"Saved screenshot to {screenshot_path}", flush=True)
    
    # Inspect rows and buttons
    rows_info = page.evaluate("""() => {
        let results = [];
        let rows = Array.from(document.querySelectorAll('ytcp-video-translation-row, tr, [role="row"]'));
        for (let r of rows) {
            results.push({
                text: (r.innerText || '').replace(/\\n+/g, ' | ').trim()
            });
        }
        return results;
    }""")
    print("Table rows found:", len(rows_info), flush=True)
    for r in rows_info[:10]:
        print("  ROW:", r['text'], flush=True)

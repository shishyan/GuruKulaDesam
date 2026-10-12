import sys
import time
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Scroll to load all rows
    print("Scrolling page to load full playlist for audit...", flush=True)
    for _ in range(5):
        rows = page.locator('ytd-playlist-video-renderer')
        rows.last.scroll_into_view_if_needed()
        time.sleep(1.2)
        
    rows = page.locator('ytd-playlist-video-renderer')
    total = rows.count()
    print(f"Total rendered videos in playlist: {total}\n", flush=True)
    
    audit_results = []
    for i in range(total):
        r = rows.nth(i)
        title_el = r.locator('#video-title')
        title = title_el.inner_text().strip() if title_el.count() > 0 else 'Unknown'
        href = title_el.get_attribute('href') if title_el.count() > 0 else ''
        vid_match = re.search(r'v=([a-zA-Z0-9_-]{11})', href)
        vid = vid_match.group(1) if vid_match else 'Unknown'
        audit_results.append({'position': i, 'videoId': vid, 'title': title})
        
    with open('production/final_sorted_playlist_audit.json', 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)
        
    print(f"{'Pos':<4} | {'Video ID':<12} | {'Title'}")
    print("-" * 75)
    for item in audit_results[:25]:
        print(f"{item['position']:<4} | {item['videoId']:<12} | {item['title'][:55]}")
    print("...")
    for item in audit_results[-10:]:
        print(f"{item['position']:<4} | {item['videoId']:<12} | {item['title'][:55]}")

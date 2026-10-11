import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    first_row = page.locator('ytd-playlist-video-renderer').first
    drag_handle = first_row.locator('#reorder')
    print('Drag handle count:', drag_handle.count())
    if drag_handle.count() > 0:
        info = drag_handle.first.evaluate('el => ({tag: el.tagName, class: el.className, draggable: el.draggable, aria: el.getAttribute("aria-grabbed")})')
        print('Drag handle info:', info)

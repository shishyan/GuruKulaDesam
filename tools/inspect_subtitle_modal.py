import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Inspect all interactive elements inside dialog/modal
    dialog = page.locator("ytcp-dialog, ytcp-subtitles-editor, [role='dialog']")
    print(f"Dialog count: {dialog.count()}")
    
    buttons = page.locator("button, ytcp-button, ytcp-icon-button, [role='button']").all()
    print(f"Total buttons on page: {len(buttons)}")
    for b in buttons:
        try:
            if b.is_visible():
                txt = b.inner_text().strip()
                aria = b.get_attribute("aria-label") or ""
                id_attr = b.get_attribute("id") or ""
                print(f"  Visible: txt='{txt}' | aria='{aria}' | id='{id_attr}'")
        except Exception:
            pass

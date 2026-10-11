import sys, time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    # 1. Dismiss "Cannot publish empty subtitles" dialog if open
    cancel = page.locator('button:has-text("Cancel"), ytcp-button:has-text("Cancel")').first
    if cancel.is_visible():
        print("Dismissing empty dialog...")
        cancel.click()
        time.sleep(1)
        
    # 2. Look for "Edit as text" button
    eat = page.locator('button:has-text("Edit as text"), ytcp-button:has-text("Edit as text"), [aria-label*="text"]').first
    if eat.is_visible():
        print(f"Clicking 'Edit as text' ({eat.inner_text().strip()})...")
        eat.click()
        time.sleep(2)
    else:
        print("Edit as text not directly visible, searching all buttons...")
        for b in page.locator('button, ytcp-button').all():
            try:
                if 'text' in (b.inner_text() or '').lower():
                    print("  Candidate:", b.inner_text().strip())
                    b.click()
                    time.sleep(2)
                    break
            except:
                pass
                
    # 3. Check textareas
    textareas = page.locator('textarea, ytcp-text-area, [contenteditable="true"]').all()
    print("Found textareas:", len(textareas))
    for i, t in enumerate(textareas):
        try:
            print(f"  [{i}] tag={t.evaluate('el => el.tagName')}, visible={t.is_visible()}, val={t.input_value()[:50] if hasattr(t, 'input_value') else ''}")
        except Exception as e:
            print(f"  [{i}] error: {e}")
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/shot_after_edit_text.png")
    print("Saved shot_after_edit_text.png")

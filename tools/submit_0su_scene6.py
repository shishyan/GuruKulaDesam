import time
from playwright.sync_api import sync_playwright

prompt = (
    "Create a single continuous 16:9 cinematic silent visual shot at 24 fps. "
    "Close atmospheric pan over bronze Kuthuvilakku oil lamps gently flickering in temple sanctum mandapam. "
    "Sacred dhoopam sambrani incense smoke drifting softly against carved granite temple pillars. "
    "*Exclusions:* No rapid motion, no modern artifacts, no text, no audio."
)

print("Submitting distinct Scene 06 for Track 0SUn5igNEE0...")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    
    editor = page.locator('div.ProseMirror').first
    if not editor.is_visible():
        page.locator('div:has-text("What do you want to create?")').last.click()
        page.wait_for_timeout(300)
        
    editor.click()
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(300)
    
    page.evaluate(
        """(text) => {
            const el = document.querySelector('div.ProseMirror');
            if (el) {
                el.focus();
                document.execCommand('insertText', false, text);
            }
        }""",
        prompt
    )
    page.wait_for_timeout(1000)
    
    submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward"), button[aria-label*="Send" i], button[aria-label*="Generate" i]').first
    if submit_btn.is_visible() and submit_btn.is_enabled():
        print("Clicking submit arrow button...")
        submit_btn.click()
    else:
        print("Pressing Enter to submit...")
        page.keyboard.press("Enter")
        
    page.wait_for_timeout(3000)
    print("Submitted Scene 06 successfully!")
    browser.close()

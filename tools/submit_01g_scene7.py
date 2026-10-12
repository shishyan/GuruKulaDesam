import time
from playwright.sync_api import sync_playwright

scene_7_prompt = (
    "Create a single continuous 16:9 cinematic silent visual shot at 24 fps from the temple mandapam. "
    "Panoramic slow crane rise overlooking the tranquil Kaveri river ghats and sacred coconut palm groves under soft dawn skies. "
    "Distant Dravidian temple gopuram illuminated in morning mist. "
    "*Exclusions:* No text, no modern items, no digital zoom, no camera shake, no audio."
)

print("Submitting Scene 07 for Track 01g0sJdaL2I on Google Flow...")

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
        scene_7_prompt
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
    print("Submitted Scene 07 successfully!")
    browser.close()

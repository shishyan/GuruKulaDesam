import time
from playwright.sync_api import sync_playwright

track_id = "--4jzoezBW8"
scene_1_prompt = (
    "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. "
    "Wide aerial glide over majestic Western Ghats mountain ridges in ancient Tamil Nadu at predawn. "
    "Layered misty green peaks, morning clouds drifting gently across forested valleys, "
    "pristine mountain stream flowing through weathered granite boulders. 8k resolution, calm spiritual grandeur. "
    "Exclusions: No modern items, no roads, no buildings, no text."
)

print(f"Submitting Scene 01 for Track {track_id} on Google Flow (nagaraj957@gmail.com)...")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    
    # 1. Locate and click input editor
    editor = page.locator('div.ProseMirror').first
    if not editor.is_visible():
        print("Clicking prompt area to focus...")
        page.locator('div:has-text("What do you want to create?")').last.click()
        page.wait_for_timeout(300)
        
    editor.click()
    page.wait_for_timeout(300)
    
    # 2. Insert prompt text
    page.evaluate(
        """(text) => {
            const el = document.querySelector('div.ProseMirror');
            if (el) {
                el.focus();
                document.execCommand('insertText', false, text);
            }
        }""",
        scene_1_prompt
    )
    page.wait_for_timeout(1000)
    
    # 3. Click Submit button
    submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward"), button[aria-label*="Send" i], button[aria-label*="Generate" i]').first
    if submit_btn.is_visible() and submit_btn.is_enabled():
        print("Clicking submit arrow button...")
        submit_btn.click()
    else:
        print("Pressing Enter to submit...")
        page.keyboard.press("Enter")
        
    page.wait_for_timeout(4000)
    page.screenshot(path='production/flow_generating_scene01.png')
    print("Submitted Scene 01! Screenshot saved to production/flow_generating_scene01.png")
    browser.close()

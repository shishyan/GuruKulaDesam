from playwright.sync_api import sync_playwright

prompt = (
    "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. "
    "Wide aerial glide over majestic Western Ghats mountain ridges in ancient Tamil Nadu at predawn. "
    "Layered misty green peaks, morning clouds drifting gently across forested valleys, "
    "pristine mountain stream flowing through weathered granite boulders. 8k resolution, calm spiritual grandeur. "
    "Exclusions: No modern items, no roads, no buildings, no text."
)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9225')
    page = browser.contexts[0].pages[0]
    
    # Locate ProseMirror editor
    editor = page.locator('div.ProseMirror').first
    if not editor.is_visible():
        print("ERROR: ProseMirror input not visible!")
    else:
        print("Focusing prompt input...")
        editor.click()
        page.wait_for_timeout(300)
        
        # Insert text
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

        # Click submit button
        submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward")').first
        if submit_btn.is_visible() and submit_btn.is_enabled():
            print("Clicking submit button...")
            submit_btn.click()
        else:
            print("Pressing Enter to submit...")
            page.keyboard.press("Enter")
            
        page.wait_for_timeout(4000)
        page.screenshot(path='production/flow_submitted_scene1.png')
        print("Submitted! Screenshot saved to production/flow_submitted_scene1.png")

    browser.close()

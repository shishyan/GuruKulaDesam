from playwright.sync_api import sync_playwright

prompt = """Slow cinematic crane rise looking out from the temple mandapam. Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. Wide aerial glide over majestic Western Ghats mountain ridges in ancient Tamil Nadu at predawn. Layered misty green peaks, morning clouds drifting gently across forested valleys, pristine mountain stream flowing through weathered granite boulders. 8k resolution, calm spiritual grandeur. *Exclusions:* No modern items, no roads, no buildings, no text.. panoramic view of Kaveri river ghats and coconut palm groves under soft dawn skies."""

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    flow_page.keyboard.press('Escape')
    flow_page.wait_for_timeout(300)
    
    editor = flow_page.locator('div.ProseMirror').first
    editor.click()
    flow_page.wait_for_timeout(200)
    flow_page.keyboard.press('Control+A')
    flow_page.keyboard.press('Backspace')
    flow_page.wait_for_timeout(200)
    
    flow_page.evaluate("""(text) => {
        const el = document.querySelector('div.ProseMirror');
        if (el) {
            el.focus();
            document.execCommand('insertText', false, text);
        }
    }""", prompt)
    flow_page.wait_for_timeout(500)
    
    gen_btn = flow_page.locator('button.generate-icon-button, button[aria-label*="Start generation" i]').last
    print("Submit button visible:", gen_btn.is_visible())
    gen_btn.click(force=True)
    print("Submitted Scene 7 prompt!")
    flow_page.wait_for_timeout(3000)
    browser.close()

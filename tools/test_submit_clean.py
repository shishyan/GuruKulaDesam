import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    # 1. Close any overlay
    flow_page.keyboard.press('Escape')
    flow_page.wait_for_timeout(300)
    
    # 2. Enter prompt into editor
    prompt = 'Create a single continuous 16:9 cinematic slow tracking shot at 24 fps. Ancient Chola bronze sculpture of Nataraja dancing in cosmic ring of flames within granite shrine. Oil lamps flicker casting warm spiritual light. Profound inner peace, ethical clarity, timeless wisdom. Exclusions: No rapid motion, no modern artifacts, no text.'
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
    
    # 3. Click generate
    gen_btn = flow_page.locator('button.generate-icon-button, button[aria-label*="Start generation" i]').last
    print('Gen button visible:', gen_btn.is_visible())
    gen_btn.click(force=True)
    print('Clicked generate button!')
    
    # Check status over 20s
    for s in range(10):
        flow_page.wait_for_timeout(2000)
        body = flow_page.locator('body').inner_text()
        has_stop = 'Stop' in body
        print(f'T+{(s+1)*2}s: hasStop={has_stop}')
        if has_stop:
            break
            
    browser.close()

import sys
from playwright.sync_api import sync_playwright

prompt = sys.argv[1] if len(sys.argv) > 1 else ""
if not prompt:
    print("No prompt provided!")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    flow_page.keyboard.press('Escape')
    flow_page.wait_for_timeout(200)
    
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
    flow_page.wait_for_timeout(400)
    
    btn = flow_page.locator("button[aria-label*='Start generation' i], button.generate-icon-button").last
    box = btn.bounding_box()
    if box:
        flow_page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        print("Clicked generate via mouse!")
    else:
        btn.click(force=True)
        print("Clicked generate via force click!")
        
    flow_page.wait_for_timeout(2000)
    browser.close()

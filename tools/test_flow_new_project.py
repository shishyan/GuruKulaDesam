import sys
from playwright.sync_api import sync_playwright

def test_new_project():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9225")
        ctx = browser.contexts[0]
        flow_page = None
        for page in ctx.pages:
            if "flow.google" in page.url:
                flow_page = page
                break
        
        if not flow_page:
            print("No flow page found!")
            browser.close()
            return

        print("Current Flow URL:", flow_page.url)
        btn = flow_page.locator("button:has-text('New project'), [role='button']:has-text('New project')").first
        if btn.is_visible():
            print("Clicking New project button...")
            btn.click()
            flow_page.wait_for_timeout(5000)
            print("URL after click:", flow_page.url)
            flow_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_new_project_screen.png")
            
            # List all buttons and inputs
            buttons = [b.inner_text().strip() for b in flow_page.locator("button, [role='button']").all() if b.is_visible()]
            print("Visible buttons:", buttons[:25])
            
            inputs = flow_page.locator("textarea, input, [contenteditable='true'], .ProseMirror").all()
            print(f"Found {len(inputs)} editable inputs:")
            for i, inp in enumerate(inputs):
                tag = inp.evaluate("el => el.tagName")
                cls = inp.evaluate("el => el.className")
                aria = inp.evaluate("el => el.getAttribute('aria-label') || el.placeholder || ''")
                print(f"  [{i}] {tag} | class: {cls[:40]} | label: {aria}")

        browser.close()

if __name__ == "__main__":
    test_new_project()

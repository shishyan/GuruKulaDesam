import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def submit_current_prompt():
    print("Connecting to Chrome on port 9225...")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9225")
        ctx = browser.contexts[0]
        flow_page = None
        for page in ctx.pages:
            if "flow.google" in page.url:
                flow_page = page
                break

        if not flow_page:
            print("ERROR: Flow page not found!")
            browser.close()
            return

        print("Flow page found:", flow_page.url)

        # Click the submit / arrow_forward button
        send_btn = flow_page.locator("button:has-text('arrow_forward'), [role='button']:has-text('arrow_forward'), button[aria-label*='Send' i], button[aria-label*='Generate' i]").first
        if not send_btn.is_visible():
            send_btn = flow_page.locator("button").filter(has_text="arrow_forward").first

        print(f"Send button visible: {send_btn.is_visible()}, enabled: {send_btn.is_enabled()}")
        if send_btn.is_visible():
            send_btn.click()
            print("Clicked submit button!")
            flow_page.wait_for_timeout(3000)

        # Check for approval option-row (Always approve)
        print("Checking for credit approval...")
        for i in range(10):
            flow_page.wait_for_timeout(2000)
            appr = flow_page.locator(".option-row:has-text('Always approve'), .option-row:has-text('Approve')").first
            if appr.count() > 0 and appr.is_visible():
                print(f"Found approval: '{appr.inner_text().strip()}'. Clicking...")
                appr.click()
                flow_page.wait_for_timeout(2000)
                break
            
            # Check if stop button already active
            stop = flow_page.locator("button:has-text('stop'), [role='button']:has-text('stop')").first
            if stop.count() > 0 and stop.is_visible():
                print("Generation in progress (Stop button visible)!")
                break

        # Save screenshot
        shot = "C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_scene3_generating.png"
        flow_page.screenshot(path=shot)
        print(f"Screenshot saved to {shot}")

        browser.close()

if __name__ == "__main__":
    submit_current_prompt()

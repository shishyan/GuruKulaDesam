import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

def submit_test():
    prompt = (
        "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. "
        "Early morning mist gradually lifts over the majestic sacred granite hill of Palani Sivagiri in ancient Tamil Nadu. "
        "Golden dawn sunlight bathes the ancient winding stone stairway and the glistening golden Vimana sanctum tower crowning the hilltop. "
        "Flocks of white temple doves fly gracefully through the cool morning sky above lush emerald coconut palms. "
        "Exclusions: No electrical towers, no modern roads, no text, no subtitles."
    )

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
            print("ERROR: Google Flow tab not found!")
            browser.close()
            return

        print(f"Attached to Flow: {flow_page.url}")
        
        # Ensure we are in a project workspace
        if "/project/" not in flow_page.url:
            print("Navigating to new project...")
            btn = flow_page.locator("button:has-text('New project'), [role='button']:has-text('New project')").first
            if btn.is_visible():
                btn.click()
                flow_page.wait_for_timeout(4000)

        print(f"Current workspace URL: {flow_page.url}")

        # Locate ProseMirror editor
        editor = flow_page.locator("div.ProseMirror").first
        if not editor.is_visible():
            print("ERROR: ProseMirror input not visible!")
            browser.close()
            return

        print("Focusing prompt input...")
        editor.click()
        flow_page.wait_for_timeout(500)
        
        # Clear existing text if any
        flow_page.keyboard.press("Control+A")
        flow_page.keyboard.press("Backspace")
        flow_page.wait_for_timeout(300)

        print(f"Typing sacred prompt ({len(prompt)} chars)...")
        # Use fill or insert_text for speed and accuracy
        flow_page.evaluate(
            """(text) => {
                const el = document.querySelector('div.ProseMirror');
                if (el) {
                    el.focus();
                    document.execCommand('insertText', false, text);
                }
            }""",
            prompt
        )
        flow_page.wait_for_timeout(1000)

        # Check arrow_forward submit button
        submit_btn = flow_page.locator("button:has-text('arrow_forward'), [role='button']:has-text('arrow_forward'), button[aria-label*='Send' i], button[aria-label*='Generate' i]").first
        if not submit_btn.is_visible():
            submit_btn = flow_page.locator("button").filter(has_text="arrow_forward").first

        print(f"Submit button found: {submit_btn.is_visible()}, enabled: {submit_btn.is_enabled()}")
        
        if submit_btn.is_visible() and submit_btn.is_enabled():
            print("Clicking submit button...")
            submit_btn.click()
            flow_page.wait_for_timeout(3000)
        else:
            print("Pressing Enter to submit...")
            editor.focus()
            flow_page.keyboard.press("Enter")
            flow_page.wait_for_timeout(3000)

        # Take screenshot of what happened
        artifact_shot = Path("C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_after_submit.png")
        flow_page.screenshot(path=str(artifact_shot))
        print(f"Screenshot saved to {artifact_shot.name}")

        # Check for approval modal or assistant response
        print("Checking page for approval prompt or generation status...")
        for i in range(15):
            flow_page.wait_for_timeout(2000)
            body_txt = flow_page.locator("body").inner_text()
            
            # Check for credits / approval
            if "approve" in body_txt.lower():
                print(f"Approval request detected at {i*2}s!")
                # Find approve buttons
                appr_btns = flow_page.locator("button:has-text('Always approve'), [role='button']:has-text('Always approve'), button:has-text('Approve'), [role='button']:has-text('Approve')").all()
                for b in appr_btns:
                    if b.is_visible():
                        print(f"Clicking approval button: '{b.inner_text().strip()}'")
                        b.click()
                        flow_page.wait_for_timeout(2000)
                        break
                break
            
            # Check for generation indicator or stop button
            stop_btn = flow_page.locator("button:has-text('stop'), [role='button']:has-text('stop')").first
            if stop_btn.is_visible():
                print(f"Generation actively in progress (Stop button visible at {i*2}s)...")
                break
                
            if i % 3 == 0:
                print(f"Waiting for generation/approval... ({i*2}s)")

        # Final screenshot after check
        flow_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_generation_state.png")
        print("Final screenshot saved to flow_generation_state.png")
        browser.close()

if __name__ == "__main__":
    submit_test()

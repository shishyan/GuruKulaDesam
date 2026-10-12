import time
import json
from playwright.sync_api import sync_playwright

with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

track_data = next((t for t in data["tracks"] if t["track_id"] == "-9bZmHzYO2g"), None)
scene5 = next((s for s in track_data["scenes"] if s["scene_num"] == 5), None)
prompt = scene5["prompt"]

print("Connecting to Chrome on port 9222 for Track -9bZmHzYO2g Scene 5...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    flow_page = [page for page in ctx.pages if "flow.google.com" in page.url][0]
    
    editor = flow_page.locator("div.ProseMirror").first
    editor.click()
    flow_page.wait_for_timeout(300)
    
    flow_page.keyboard.press("Control+A")
    flow_page.keyboard.press("Backspace")
    flow_page.wait_for_timeout(300)
    
    print(f"Inserting Scene 5 prompt ({len(prompt)} chars)...")
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
    flow_page.wait_for_timeout(500)
    
    submit_btn = flow_page.locator("button.generate-icon-button, button[aria-label*='Start generation' i]").first
    if submit_btn.is_visible() and submit_btn.is_enabled():
        print("Clicking submit button...")
        submit_btn.click()
    else:
        print("Pressing Enter...")
        editor.focus()
        flow_page.keyboard.press("Enter")
        
    flow_page.wait_for_timeout(4000)
    
    for i in range(12):
        body_text = flow_page.locator("body").inner_text()
        has_stop = "Stop" in body_text
        print(f"[{i*2}s] Stop visible: {has_stop}")
        if has_stop:
            print("Scene 5 render has successfully started!")
            break
        flow_page.wait_for_timeout(2000)
        
    browser.close()
